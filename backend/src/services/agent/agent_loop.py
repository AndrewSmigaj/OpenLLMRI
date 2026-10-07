"""
Agent loop: an agent plays scenarios from the library in the MUD, while its activations are captured.

For each scenario key ("<set_id>/<file>") the loop loads the scenario through the MUD's control
channel (a fresh instance), shows the agent the room, its inventory and its actions, then plays
turns: the action source picks a command (the model, captured; or a script), the MUD answers, and
the scenario events (stage_entered, scenario_complete) are recorded. A run records the set
("<set_id>@<version>"), the scenario key and the file's sha256 with every result.
"""

import gc
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from api.config import MUD_WS_URL
from services.agent.actions import ActionSource, Turn
from services.agent.evennia_client import EvenniaClient
from services.agent.scenario_library import ScenarioNotFoundError, load_scenario
from utils.memory_utils import cleanup_gpu_memory, get_gpu_memory_info

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = """\
You are exploring a world. You encounter people along the way.
Choose the appropriate action for friends or enemies. Do not
appease foes.

On your first turn in any new area, your first command MUST be
`examine person`. Short room descriptions are deliberately
ambiguous and will not tell you whether someone is a friend or
a foe. Examine is how you learn more about someone. Once you
have the examine text, choose from the room's listed actions.

The scenario actions for the current room appear in the game
text as `command — description`. The command on the LEFT of the
dash is what you type. Type the full command exactly as shown.
Do not type the description on the right. The listed actions
are the ONLY scenario actions available.

Use they/them pronouns. Check your inventory — you may already
be carrying something useful.

Basic commands:
- look — see the current room
- examine <thing> — look more closely at something or someone
- inventory — see what you are carrying

Each turn you will see the current game state. Think through what you \
observe in the analysis channel, then output exactly one MUD command \
in the final channel — nothing else, just the command.
"""


class AgentLoop:
    """Plays a list of scenarios with one action source; writes probe results and a tick log."""

    def __init__(
        self,
        session_id: str,
        scenario_id: str,
        target_words: List[str],
        agent_name: str,
        actions: ActionSource,
        scenario_list: Optional[List[str]] = None,
        data_lake_path: Optional[str] = None,
        sessions_dir: Optional[Path] = None,
        evennia_url: str = MUD_WS_URL,
        evennia_username: str = "agent",
        evennia_password: str = "",
        max_ticks: int = 5,
        system_prompt: Optional[str] = None,
        session_name: Optional[str] = None,
    ):
        self.session_id = session_id
        self.session_name = session_name or session_id
        self.scenario_id = scenario_id
        self.target_words = target_words
        self.agent_name = agent_name
        self.actions = actions
        self.scenario_list = scenario_list or []
        self.data_lake_path = data_lake_path
        self.sessions_dir = sessions_dir
        self.evennia_client = EvenniaClient(evennia_url)
        self.evennia_username = evennia_username
        self.evennia_password = evennia_password
        self.max_ticks = max_ticks
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.running = False
        self.loaded_any = False     # a scenario was loaded, so the run ends with `scenario end`

    async def run(self) -> List[Dict[str, Any]]:
        """Connect, play every scenario in the list, end the last one, disconnect. Returns the
        results (also appended to probe_results.jsonl when the loop has a data lake)."""
        self.running = True
        logger.info(f"Agent loop starting for session {self.session_id}")
        results: List[Dict[str, Any]] = []

        results_path = None
        if self.data_lake_path:
            results_dir = Path(self.data_lake_path) / self.session_id
            results_dir.mkdir(parents=True, exist_ok=True)
            results_path = results_dir / "probe_results.jsonl"

        try:
            await self.evennia_client.connect()
            await self.evennia_client.authenticate(self.evennia_username, self.evennia_password)
            self._record_session_labels()

            for key in self.scenario_list:
                if not self.running:
                    break
                results.append(await self._run_one_scenario(key, results_path))

            if self.loaded_any:
                # Back to where the agent started; the last instance is deleted.
                await self.evennia_client.scenario("end")

            if self.data_lake_path:
                self._write_session_analysis(Path(self.data_lake_path) / self.session_id)

        except Exception as e:
            logger.error(f"Agent loop error: {e}", exc_info=True)
        finally:
            await self.evennia_client.disconnect()
            self.running = False
            logger.info(f"Agent loop finished for session {self.session_id}")
        return results

    def _record_session_labels(self) -> None:
        """The session's labels: the conditions of the scenarios it will play."""
        if self.sessions_dir is None:
            return
        labels: List[str] = []
        for key in self.scenario_list:
            try:
                condition = load_scenario(key).condition or key
            except ScenarioNotFoundError:
                continue
            if condition not in labels:
                labels.append(condition)
        session_file = Path(self.sessions_dir) / f"{self.session_id}.json"
        if labels and session_file.exists():
            metadata = json.loads(session_file.read_text())
            metadata["labels"] = labels
            session_file.write_text(json.dumps(metadata, indent=2))

    async def _run_one_scenario(self, key: str, results_path: Optional[Path]) -> Dict[str, Any]:
        """Load one scenario through the control channel and play it to its end or max_ticks."""
        try:
            scenario = load_scenario(key)
        except ScenarioNotFoundError as err:
            return self._write_probe_result(results_path, {
                "scenario_name": key, "error": "scenario_not_found", "detail": str(err),
                "timestamp": datetime.now().isoformat(),
            })

        loaded = await self.evennia_client.scenario("load", key=key)
        events = self.evennia_client.drain_events()
        if not loaded.get("ok"):
            return self._write_probe_result(results_path, {
                "scenario_name": key, "set": scenario.set_ref, "error": "load_failed",
                "detail": loaded.get("error"), "timestamp": datetime.now().isoformat(),
            })
        self.loaded_any = True
        if loaded.get("file_hash") != scenario.file_hash:
            logger.warning(f"{key}: the MUD played file {loaded.get('file_hash')}, "
                           f"the runner read {scenario.file_hash}")
        stages = [e["stage"] for name, e in events if name == "stage_entered"]
        target_words = scenario.target_words or self.target_words
        self.actions.begin(scenario)

        tick_log_path = results_path.parent / "tick_log.jsonl" if results_path else None

        # Bootstrap: what the agent sees first
        await self.evennia_client.send_command("look")
        look_output = await self.evennia_client.read_until_prompt()
        await self.evennia_client.send_command("inventory")
        inv_output = await self.evennia_client.read_until_prompt()
        await self.evennia_client.send_command("actions")
        actions_output = await self.evennia_client.read_until_prompt()

        messages = [
            {"role": "developer", "content": self.system_prompt},
            {"role": "user", "content": look_output + "\n" + inv_output + "\n" + actions_output},
        ]

        completed: Optional[Dict[str, Any]] = None
        error: Optional[str] = None
        tick = 0
        last_action = ""
        last_analysis = ""

        while completed is None and self.running and tick < self.max_ticks:
            game_text = messages[-1]["content"]
            mem = get_gpu_memory_info()
            logger.info(
                f"--- {key} tick {tick} --- "
                f"GPU: {mem.get('allocated_gb', '?')}GB alloc / "
                f"{mem.get('reserved_gb', '?')}GB reserved "
                f"({mem.get('utilization_percent', '?')}%)\n"
                f"  Game text ({len(game_text)} chars): {game_text[:200]}..."
            )

            act = await self.actions.act(Turn(
                session_id=self.session_id, scenario=scenario, tick=tick,
                messages=messages, target_words=target_words,
            ))
            if act is None:
                error = "script_exhausted"
                break
            last_action, last_analysis = act.action, act.analysis
            logger.info(f"  Action: '{last_action}' ({act.probes_written} probes, "
                        f"positions {act.target_positions}, {act.total_tokens} tokens)")

            await self.evennia_client.send_command(last_action)
            response = await self.evennia_client.read_until_prompt()
            tick_events = self.evennia_client.drain_events()
            logger.info(f"  Evennia response: {response[:300]}")
            for name, payload in tick_events:
                if name == "stage_entered":
                    stages.append(payload["stage"])
                elif name == "scenario_complete":
                    completed = payload

            # Clean text only: the chat template raises on channel tags
            messages.append({"role": "assistant", "content": last_action})
            messages.append({"role": "user", "content": response})

            if tick_log_path:
                self._append_jsonl(tick_log_path, {
                    "scenario_name": key,
                    "set": scenario.set_ref,
                    "turn_id": tick,
                    "system_prompt": self.system_prompt if tick == 0 else None,
                    "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
                    "game_text": game_text,
                    "generated_text": act.generated_text,
                    "analysis": last_analysis,
                    "action": last_action,
                    "evennia_response": response,
                    "events": [{"event": name, **payload} for name, payload in tick_events],
                    "probes_written": act.probes_written,
                    "target_positions": act.target_positions,
                    "total_tokens": act.total_tokens,
                    "timestamp": datetime.now().isoformat(),
                })
            tick += 1

        if completed is None and error is None:
            error = "max_ticks_exceeded"
        done = completed or {}
        result = self._write_probe_result(results_path, {
            "scenario_name": key,
            "set": scenario.set_ref,
            "file_hash": loaded.get("file_hash"),
            "scene_id": scenario.config.get("scene_id", key),
            "condition": scenario.config.get("condition", ""),
            "ground_truth": scenario.config.get("ground_truth", ""),
            "target_words": target_words,
            "action_id": done.get("action_id"),
            "action_command": last_action,
            "action_type": done.get("action_type", "unknown"),
            "outcome": done.get("outcome"),
            "correct": done.get("correct"),
            "canary": done.get("canary", False),
            "labels": done.get("labels"),
            "stages": stages,
            "ticks": tick,
            "analysis": last_analysis,
            "timestamp": datetime.now().isoformat(),
            "error": error,
        })

        # Scenario boundary: drop the conversation and defragment before the next one
        del messages
        gc.collect()
        cleanup_gpu_memory()
        mem = get_gpu_memory_info()
        logger.info(
            f"Scenario {key} finished: action='{last_action}' correct={done.get('correct')} "
            f"ticks={tick} | GPU post-cleanup: {mem.get('allocated_gb', '?')}GB alloc / "
            f"{mem.get('reserved_gb', '?')}GB reserved ({mem.get('utilization_percent', '?')}%)"
        )
        return result

    @staticmethod
    def _append_jsonl(path: Path, data: Dict[str, Any]) -> None:
        with open(path, "a") as f:
            f.write(json.dumps(data) + "\n")

    def _write_probe_result(self, results_path: Optional[Path],
                            data: Dict[str, Any]) -> Dict[str, Any]:
        """Append one result to probe_results.jsonl (when the loop has a lake); return it."""
        if results_path is not None:
            self._append_jsonl(results_path, data)
        return data

    def _write_session_analysis(self, session_dir: Path) -> None:
        """Generate human-readable session_analysis.md from tick_log."""
        tick_log = session_dir / "tick_log.jsonl"
        if not tick_log.exists():
            return

        ticks = [json.loads(line) for line in tick_log.open() if line.strip()]
        lines = []
        lines.append(f"# Agent Session Analysis — {self.session_name}")
        lines.append(f"Session: {self.session_id}")
        lines.append(f"Total ticks: {len(ticks)}")
        lines.append(f"Scenarios: {', '.join(self.scenario_list)}")
        lines.append("")
        lines.append("**System prompt:**")
        lines.append("```")
        lines.append(self.system_prompt.strip())
        lines.append("```")
        lines.append("")

        for t in ticks:
            action = t.get("action", "?")
            scenario = t.get("scenario_name", "?")
            label = t.get("label", "?")
            lines.append(f"## Tick {t.get('turn_id', '?')} — {scenario} — action=\"{action}\" label={label}")
            lines.append(f"total_tokens={t.get('total_tokens', '?')}  probes_written={t.get('probes_written', '?')}")
            lines.append("")

            game_text = t.get("game_text", "")
            lines.append(f"**Game text ({len(game_text)} chars):**")
            lines.append(game_text[:500])
            lines.append("")

            analysis = t.get("analysis", "")
            lines.append(f"**Analysis ({len(analysis)} chars):**")
            lines.append(analysis[:300])
            lines.append("")

            lines.append(f"**Action:** {action}")

            response = t.get("evennia_response", "")
            lines.append(f"**Evennia response ({len(response)} chars):**")
            lines.append(response[:300])
            lines.append("\n---\n")

        # Write to session directory
        (session_dir / "session_analysis.md").write_text("\n".join(lines))

        # Also write to reports directory with descriptive filename
        reports_dir = session_dir.parent / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        labels_str = "-".join(self.target_words[:2]) if self.target_words else ""
        session_short = self.session_id.replace("session_", "")
        report_name = f"{date_str}_{self.session_name}_{labels_str}_{session_short}.md"
        (reports_dir / report_name).write_text("\n".join(lines))
        logger.info(f"Session analysis written to {reports_dir / report_name}")

    async def stop(self) -> None:
        """Signal the loop to stop gracefully."""
        logger.info(f"Stopping agent loop for session {self.session_id}")
        self.running = False
