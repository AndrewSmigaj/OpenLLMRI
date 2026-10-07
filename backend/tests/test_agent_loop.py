"""AgentLoop with fake action sources and a fake MUD: a scenario loaded through the control channel
and played to its scenario_complete event, what a run records (the set, the key, the file hash, the
stages), the model's channels kept, the pinned date, failed loads, max ticks, and scripted runs."""
import hashlib
import json
from types import SimpleNamespace

import pytest

from services.agent import scenario_library
from services.agent.actions import ModelActions, ScriptedActions
from services.agent.agent_loop import AgentLoop

KEY = "test_set/test_friend"
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
            command: "help person"
            type: friend
            correct: true
            effects:
              - complete: {outcome: friend, action_id: 1}
"""
GENERATED = ("<|channel|>analysis<|message|>They seem kind.<|end|>"
             "<|start|>assistant<|channel|>final<|message|>help the person<|return|>")
PIN = "2026-04-22"
DONE = {"scenario": KEY, "set": "test_set@1", "action_id": 1, "outcome": "friend",
        "action_type": "friend", "correct": True, "canary": False,
        "labels": {"condition": "friend", "ground_truth": "friend"}}


class FakeTokenizer:
    """Renders a conversation as text with today's date line, as the real template does."""

    def __init__(self):
        self.encoded = []

    def apply_chat_template(self, messages, tokenize, add_generation_prompt, model_identity):
        assert tokenize is False
        body = "".join(f"<{m['role']}>{m['content']}" for m in messages)
        return f"Current date: 2026-10-06\n{body}" + ("<assistant>" if add_generation_prompt else "")

    def encode(self, text, add_special_tokens):
        self.encoded.append(text)
        return list(range(len(text)))


class FakeService:
    """The model: its channel markers are special tokens, stripped unless the decode keeps them."""

    def __init__(self):
        self.tokenizer = FakeTokenizer()
        self.orchestrator = SimpleNamespace(tokenizer=self.tokenizer)
        self.captures = []

    def generate(self, prompt_ids, max_new_tokens, skip_special_tokens=True):
        if skip_special_tokens:
            return "analysisThey seem kind.assistantfinalhelp the person", [7, 7, 7]
        return GENERATED, [7, 7, 7]

    def capture_step(self, session_id, full_ids, target_words, **kwargs):
        self.captures.append({"session_id": session_id, "n_ids": len(full_ids), **kwargs})
        return [SimpleNamespace(target_word="person", target_token_position=3)], None


class FakeMud:
    """Replies to commands by prefix; answers the control channel; queues scenario events."""

    def __init__(self, replies, load=None, events_on=None):
        self.replies = replies
        self.load = load if load is not None else {"ok": True, "scenario": KEY, "set": "test_set@1",
                                                   "stage": "initial"}
        self.events_on = events_on or {}      # command prefix → events it triggers
        self.sent, self.control, self.events = [], [], []

    async def connect(self):
        pass

    async def authenticate(self, username, password):
        return "You become Scout."

    async def scenario(self, cmd, **kwargs):
        self.control.append((cmd, kwargs))
        if cmd == "load":
            if self.load.get("ok"):
                self.events.append(("stage_entered", {"scenario": KEY, "stage": "initial",
                                                      "labels": {}}))
            return {**self.load, "file_hash": self.file_hash}
        return {"ok": True}

    async def send_command(self, text):
        self.sent.append(text)
        for prefix, events in self.events_on.items():
            if text.startswith(prefix):
                self.events.extend(events)

    async def read_until_prompt(self, timeout=30.0):
        for prefix, reply in self.replies:
            if self.sent[-1].startswith(prefix):
                return reply
        return ""

    def drain_events(self):
        events, self.events = self.events, []
        return events

    async def disconnect(self):
        pass


BOOTSTRAP = [("look", "A bus stop. A person is here, waiting."),
             ("inventory", "You are carrying: map."), ("actions", "help person — offer help")]


@pytest.fixture
def world(tmp_path, monkeypatch):
    library = tmp_path / "scenarios"
    (library / "test_set" / "scenarios").mkdir(parents=True)
    (library / "test_set" / "set.yaml").write_text("id: test_set\nversion: 1\nkind: staged\n")
    (library / "test_set" / "scenarios" / "test_friend.yaml").write_text(SCENARIO)
    monkeypatch.setattr(scenario_library.config, "SCENARIO_LIBRARY", library)
    lake = tmp_path / "lake"
    (lake / "_sessions").mkdir(parents=True)
    (lake / "_sessions" / "session_t.json").write_text(json.dumps({"session_id": "session_t"}))
    return SimpleNamespace(lake=lake, file_hash=hashlib.sha256(SCENARIO.encode()).hexdigest())


def _mud(world, replies, **kwargs):
    mud = FakeMud(replies, **kwargs)
    mud.file_hash = world.file_hash
    return mud


def _loop(world, actions, mud, keys=(KEY,), max_ticks=3, lake=True):
    loop = AgentLoop("session_t", "bus_stop", ["person"], "agent", actions=actions,
                     scenario_list=list(keys), max_ticks=max_ticks,
                     data_lake_path=str(world.lake) if lake else None,
                     sessions_dir=world.lake / "_sessions" if lake else None)
    loop.evennia_client = mud
    return loop


def _jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


async def test_a_scenario_is_loaded_and_played_to_its_complete_event(world):
    service = FakeService()
    mud = _mud(world, BOOTSTRAP + [("help", "You help them.\n[SCENARIO_COMPLETE]")],
               events_on={"help": [("scenario_complete", DONE)]})
    await _loop(world, ModelActions(service, PIN), mud).run()

    assert mud.control == [("load", {"key": KEY}), ("end", {})]
    assert mud.sent == ["look", "inventory", "actions", "help the person"]
    [result] = _jsonl(world.lake / "session_t" / "probe_results.jsonl")
    assert {k: result[k] for k in ("scenario_name", "set", "file_hash", "condition", "action_id",
                                   "action_command", "action_type", "outcome", "correct",
                                   "canary", "stages", "ticks", "error")} == {
        "scenario_name": KEY, "set": "test_set@1", "file_hash": world.file_hash,
        "condition": "friend", "action_id": 1, "action_command": "help the person",
        "action_type": "friend", "outcome": "friend", "correct": True, "canary": False,
        "stages": ["initial"], "ticks": 1, "error": None}
    assert result["labels"] == DONE["labels"]
    [tick] = _jsonl(world.lake / "session_t" / "tick_log.jsonl")
    assert tick["game_text"] == ("A bus stop. A person is here, waiting.\nYou are carrying: map.\n"
                                 "help person — offer help")
    assert tick["analysis"] == "They seem kind." and tick["action"] == "help the person"
    assert tick["events"] == [{"event": "scenario_complete", **DONE}]
    [capture] = service.captures
    assert capture["metadata"]["scenario_id"] == KEY and capture["metadata"]["label"] == "friend"
    assert "input_text" not in capture["metadata"], "offsets are taken against the decoded sequence"
    labels = json.loads((world.lake / "_sessions" / "session_t.json").read_text())["labels"]
    assert labels == ["friend"]
    assert (world.lake / "session_t" / "session_analysis.md").exists()


async def test_the_model_output_keeps_its_channel_markers(world):
    # The markers are special tokens: decoded without them, no channel parses and the whole output
    # would reach the MUD as the action.
    mud = _mud(world, BOOTSTRAP, events_on={"help": [("scenario_complete", DONE)]})
    [result] = await _loop(world, ModelActions(FakeService(), PIN), mud, lake=False).run()
    assert mud.sent[-1] == "help the person" and result["analysis"] == "They seem kind."


async def test_every_turn_shows_the_pinned_date(world):
    service = FakeService()
    mud = _mud(world, BOOTSTRAP + [("help", "Nothing happens.")])
    await _loop(world, ModelActions(service, PIN), mud, max_ticks=2, lake=False).run()
    assert service.tokenizer.encoded
    assert all(f"Current date: {PIN}" in t and "2026-10-06" not in t
               for t in service.tokenizer.encoded)


async def test_a_scenario_that_never_completes_stops_at_max_ticks(world):
    mud = _mud(world, BOOTSTRAP + [("help", "Nothing happens.")])
    [result] = await _loop(world, ModelActions(FakeService(), PIN), mud, max_ticks=2).run()
    assert result["ticks"] == 2 and result["error"] == "max_ticks_exceeded"
    assert result["action_id"] is None and result["outcome"] is None


async def test_a_failed_load_is_recorded_and_nothing_is_played(world):
    mud = _mud(world, BOOTSTRAP, load={"ok": False, "error": "test_set: no scenario 'x'"})
    [result] = await _loop(world, ModelActions(FakeService(), PIN), mud).run()
    assert result["error"] == "load_failed" and "no scenario" in result["detail"]
    assert mud.sent == []


async def test_an_unknown_key_is_recorded_before_the_mud_is_asked(world):
    mud = _mud(world, BOOTSTRAP)
    [result] = await _loop(world, ModelActions(FakeService(), PIN), mud,
                           keys=("test_set/missing",)).run()
    assert result["error"] == "scenario_not_found" and mud.control == []


async def test_scripted_actions_play_the_same_loop_without_a_model(world):
    mud = _mud(world, BOOTSTRAP + [("examine", "The person looks tired.")],
               events_on={"help": [("stage_entered", {"stage": "after", "labels": {}}),
                                   ("scenario_complete", DONE)]})
    scripts = ScriptedActions([["examine person", "help person"]])
    [result] = await _loop(world, scripts, mud, lake=False).run()
    assert mud.sent == ["look", "inventory", "actions", "examine person", "help person"]
    assert result["ticks"] == 2 and result["action_id"] == 1 and result["error"] is None
    assert result["stages"] == ["initial", "after"]


async def test_a_script_that_runs_out_ends_the_scenario(world):
    mud = _mud(world, BOOTSTRAP)
    [result] = await _loop(world, ScriptedActions([[]]), mud, lake=False).run()
    assert result["error"] == "script_exhausted" and result["ticks"] == 0
