"""AgentLoop with a fake model service and a fake MUD client: the bootstrap (goto, look, inventory,
actions), a tick (generate → parse → capture → act), the end of a scenario, and what it records."""
import json
from types import SimpleNamespace

import pytest
import torch

from services.agent import agent_loop
from services.agent.agent_loop import AgentLoop, strip_articles

SCENARIO = """\
name: test_friend
scene_id: bus_stop
condition: friend
ground_truth: friend
target_words: ["person"]
rooms:
  - name: Bus Stop T1
    states:
      initial:
        actions:
          - id: 1
            command: "Help Person"
            type: friend
            correct: true
          - id: 2
            command: "alert guard"
            type: enemy
            correct: false
"""
GENERATED = ("<|channel|>analysis<|message|>They seem kind.<|end|>"
             "<|start|>assistant<|channel|>final<|message|>help the person<|return|>")


class FakeTokenizer:
    def apply_chat_template(self, messages, add_generation_prompt, return_dict, return_tensors,
                            model_identity):
        n = 10 * len(messages) + (2 if add_generation_prompt else 0)
        return {"input_ids": torch.zeros((1, n), dtype=torch.long)}


class FakeService:
    def __init__(self, sessions_dir, generated=GENERATED):
        self.orchestrator = SimpleNamespace(tokenizer=FakeTokenizer(), model=SimpleNamespace(device="cpu"))
        self.session_mgr = SimpleNamespace(sessions_dir=str(sessions_dir))
        self.generated = generated
        self.captures = []

    def generate(self, prompt_ids, max_new_tokens):
        return self.generated, [7, 7, 7]

    def capture_step(self, session_id, full_ids, target_words, **kwargs):
        self.captures.append({"session_id": session_id, "n_ids": len(full_ids), **kwargs})
        return [SimpleNamespace(target_word="person", target_token_position=3)], None


class FakeMudClient:
    """Replies by the prefix of the last command sent; records every command."""

    def __init__(self, replies):
        self.replies = replies
        self.sent = []

    async def connect(self):
        pass

    async def authenticate(self, username, password):
        return "You become Scout."

    async def send_command(self, text):
        self.sent.append(text)

    async def read_until_prompt(self, timeout=30.0):
        for prefix, reply in self.replies:
            if self.sent[-1].startswith(prefix):
                return reply
        return ""

    async def disconnect(self):
        pass


BOOTSTRAP = [("goto", "You arrive."), ("look", "A bus stop. A person waits."),
             ("inventory", "You carry nothing."), ("actions", "help person — offer help"),
             ("emote", "")]


@pytest.fixture
def world(tmp_path, monkeypatch):
    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    (scenarios / "test_friend.yaml").write_text(SCENARIO)
    monkeypatch.setattr(agent_loop, "SCENARIOS_DIR", scenarios)
    lake = tmp_path / "lake"
    (lake / "_sessions").mkdir(parents=True)
    (lake / "_sessions" / "session_t.json").write_text(json.dumps({"session_id": "session_t"}))
    return lake


def _loop(lake, service, mud, scenarios=("test_friend",), max_ticks=3):
    loop = AgentLoop("session_t", "bus_stop", ["person"], "agent", service=service,
                     scenario_list=list(scenarios), data_lake_path=str(lake), max_ticks=max_ticks)
    loop.evennia_client = mud
    return loop


def _results(lake):
    return [json.loads(line) for line in (lake / "session_t" / "probe_results.jsonl").read_text().splitlines()]


async def test_a_scenario_plays_from_bootstrap_to_completion(world):
    service = FakeService(world / "_sessions")
    mud = FakeMudClient(BOOTSTRAP + [("help person", "You help them. [SCENARIO_COMPLETE]")])
    await _loop(world, service, mud).run()

    assert mud.sent == ["goto Bus Stop T1 scenario=test_friend", "look", "inventory", "actions",
                        "emote help person", "help person"]
    [result] = _results(world)
    assert {k: result[k] for k in ("scenario_name", "scene_id", "condition", "ground_truth",
                                   "action_id", "action_command", "action_type", "correct",
                                   "ticks", "error")} == {
        "scenario_name": "test_friend", "scene_id": "bus_stop", "condition": "friend",
        "ground_truth": "friend", "action_id": 1, "action_command": "help person",
        "action_type": "friend", "correct": True, "ticks": 1, "error": None}
    [tick] = [json.loads(line) for line in (world / "session_t" / "tick_log.jsonl").read_text().splitlines()]
    assert tick["game_text"] == "A bus stop. A person waits.\nYou carry nothing.\nhelp person — offer help"
    assert tick["analysis"] == "They seem kind." and tick["action"] == "help person"
    [capture] = service.captures
    assert capture["metadata"]["scenario_id"] == "test_friend"
    assert capture["metadata"]["label"] == "friend" and capture["metadata"]["turn_id"] == 0
    assert json.loads((world / "_sessions" / "session_t.json").read_text())["labels"] == ["friend"]
    assert (world / "session_t" / "session_analysis.md").exists()


async def test_a_scenario_that_never_completes_stops_at_max_ticks(world):
    mud = FakeMudClient(BOOTSTRAP + [("help person", "Nothing happens.")])
    await _loop(world, FakeService(world / "_sessions"), mud, max_ticks=2).run()
    [result] = _results(world)
    assert result["ticks"] == 2 and result["error"] == "max_ticks_exceeded"


async def test_a_failed_teleport_is_recorded_and_the_scenario_skipped(world):
    mud = FakeMudClient([("goto", "Could not find room 'Bus Stop T1'.")])
    await _loop(world, FakeService(world / "_sessions"), mud).run()
    assert mud.sent == ["goto Bus Stop T1 scenario=test_friend"]
    assert _results(world)[0]["error"] == "teleport_failed"


async def test_a_missing_scenario_file_is_recorded(world):
    mud = FakeMudClient(BOOTSTRAP)
    await _loop(world, FakeService(world / "_sessions"), mud, scenarios=("no_such_scenario",)).run()
    assert mud.sent == []
    assert _results(world)[0]["error"] == "yaml_not_found"


def test_the_action_lookup_matches_commands_case_insensitively(world):
    loop = _loop(world, FakeService(world / "_sessions"), FakeMudClient([]))
    lookup = loop._build_action_lookup(loop._load_scenario_config("test_friend"))
    assert lookup["help person"] == {"action_id": 1, "action_type": "friend", "correct": True,
                                     "canary": False}
    assert lookup["alert guard"]["action_type"] == "enemy"


def test_articles_are_stripped_from_commands():
    assert strip_articles("Take the knife from a drawer") == "Take knife from drawer"
