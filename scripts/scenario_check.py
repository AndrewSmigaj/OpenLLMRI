"""Play every scenario of a set once per opening action, without the model, and check that the MUD
reports each ending as the scenario file says.

The backend's runner (AgentLoop) plays scripted actions against the running MUD: the same login,
control channel and turn order an agent run uses, with no model, no GPU and no capture. For each
action of a scenario's first stage it loads a fresh instance, types the action's command and
compares the MUD's scenario_complete event with the file: action id, outcome, type, correct,
canary and labels. An action that leads to another stage is checked to enter that stage. Exits
non-zero on any mismatch.

Usage (the MUD and its agent account must be up; `make scenario-check` wraps this):
    .venv/bin/python scripts/scenario_check.py [SET_ID] [--subset NAME] [--limit N]
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from api.config import MUD_WS_URL  # noqa: E402
from services.agent.actions import ScriptedActions  # noqa: E402
from services.agent.agent_loop import AgentLoop  # noqa: E402
from services.agent.scenario_library import load_scenario, scenario_keys  # noqa: E402

STRUCTURE = {"name", "rooms", "target_words", "npcs"}   # top-level fields that aren't labels


def expectations(key: str) -> List[Tuple[str, Dict[str, Any]]]:
    """(command, what the MUD should report) for each action of the scenario's first stage."""
    config = load_scenario(key).config
    labels = {k: v for k, v in config.items()
              if k not in STRUCTURE and isinstance(v, (str, int, float, bool))}
    stage = config["rooms"][0]["states"]["initial"] or {}
    labels.update(stage.get("labels") or {})
    out = []
    for action in stage.get("actions") or []:
        effects = action.get("effects") or []
        complete = next((e["complete"] for e in effects if "complete" in e), None)
        if complete is None:
            out.append((action["command"], {"enters": action.get("transitions_to")}))
        else:
            out.append((action["command"], {
                "action_id": int(complete.get("action_id", action["id"])),
                "outcome": complete["outcome"], "action_type": action["type"],
                "correct": action.get("correct"), "canary": bool(action.get("canary", False)),
                "labels": labels}))
    return out


def mismatches(result: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    if "enters" in expected:
        if expected["enters"] not in (result.get("stages") or []):
            return [f"expected to enter stage {expected['enters']!r}, got {result.get('stages')}"]
        return []
    if result.get("error"):
        return [f"error {result['error']}: {result.get('detail', '')}".rstrip(": ")]
    return [f"{field}: expected {value!r}, got {result.get(field)!r}"
            for field, value in expected.items() if result.get(field) != value]


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("set_id", nargs="?", default="bus_stop_friend_foe_v2")
    parser.add_argument("--subset")
    parser.add_argument("--limit", type=int, help="only the first N scenarios")
    args = parser.parse_args()

    keys = scenario_keys(args.set_id, args.subset)[: args.limit]
    runs = [(key, command, expected) for key in keys for command, expected in expectations(key)]
    loop = AgentLoop(
        session_id="scenario_check", scenario_id=args.set_id, target_words=[],
        agent_name="scenario_check", actions=ScriptedActions([[command] for _, command, _ in runs]),
        scenario_list=[key for key, _, _ in runs], max_ticks=1, evennia_url=MUD_WS_URL,
        evennia_username=os.environ.get("EVENNIA_AGENT_USER", "agent"),
        evennia_password=os.environ.get("EVENNIA_AGENT_PASS", ""),
    )
    results = await loop.run()
    failures = []
    for (key, command, expected), result in zip(runs, results):
        for problem in mismatches(result, expected):
            failures.append(f"{key} [{command}]: {problem}")
    if len(results) < len(runs):
        failures.append(f"only {len(results)} of {len(runs)} runs came back (see the log above)")

    print(f"{args.set_id}: {len(keys)} scenarios, {len(runs)} runs, {len(failures)} failures")
    for line in failures:
        print("  " + line)
    return 1 if failures else 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    sys.exit(asyncio.run(main()))
