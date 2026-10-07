"""Tier-2 integration: staged scenarios in the MUD — fresh instances, the room's claim on typed actions,
what the player reads, the structured messages, the control channel and the prompt."""
import os
from pathlib import Path
from unittest import mock

from evennia.utils.test_resources import EvenniaTest

LIBRARY = str(Path(__file__).resolve().parents[1] / "staged" / "library")
KEY = "fixture_set/fixture_stranger"
VERBS = "fixture_set/fixture_verbs"


def _texts(m):
    out = []
    for c in m.call_args_list:
        t = c.args[0] if c.args else c.kwargs.get("text")
        if isinstance(t, tuple):
            t = t[0]
        if t is not None:
            out.append(str(t))
    return "\n".join(out)


def _oob(m, name):
    return [c.kwargs[name][0] for c in m.call_args_list if name in c.kwargs]


@mock.patch.dict(os.environ, {"SCENARIO_LIBRARY": LIBRARY})
class TestStaged(EvenniaTest):
    def _load(self, key=KEY):
        from typeclasses.staged.instances import load_scenario
        with mock.patch.object(self.char1, "msg") as m:
            room, _ = load_scenario(self.char1, key)
        return room, m

    def _run(self, line, char=None):
        char = char or self.char1
        with mock.patch.object(char, "msg") as m:
            char.execute_cmd(line)
        return m

    def test_a_load_puts_the_player_in_a_fresh_instance_and_reports_the_first_stage(self):
        from typeclasses.staged.rooms import StagedRoom
        start = self.char1.location
        room, m = self._load()
        assert isinstance(room, StagedRoom) and self.char1.location == room
        assert room.key == "Test Room" and self.char1.db.staged_return == start
        assert _texts(m) == "", "a load is silent: the runner decides what the player reads"
        [entered] = _oob(m, "stage_entered")
        assert entered["scenario"] == KEY and entered["set"] == "fixture_set@1"
        assert entered["stage"] == "initial" and len(entered["file_hash"]) == 64
        assert entered["labels"] == {"scene_id": "fixture", "condition": "friend",
                                     "ground_truth": "friend", "intent": "unknown"}

    def test_the_player_reads_the_scenario(self):
        self._load()
        assert "A plain test room.\nA stranger is here, waiting by the door.\nYou see: bench." in _texts(self._run("look"))
        assert _texts(self._run("examine the stranger")) == "The stranger looks tired."
        assert _texts(self._run("look at bench")) == "A wooden bench."
        assert _texts(self._run("inventory")) == "You are carrying: map."
        assert _texts(self._run("actions")) == ("What will you do about the stranger?\n"
                                                "greet stranger — Greet the stranger\n"
                                                "leave — Walk away")

    def test_a_typed_action_is_claimed_and_others_see_the_typed_line(self):
        room, _ = self._load()
        self.char2.move_to(room, quiet=True, move_hooks=False)
        with mock.patch.object(self.char2, "msg") as seen:
            m = self._run("Greet the stranger.")
        assert _texts(m) == "You greet the stranger.\nThe stranger nods."
        assert "Char: Greet the stranger." in _texts(seen)
        [entered] = _oob(m, "stage_entered")
        assert entered["stage"] == "reveal" and entered["labels"]["ground_truth"] == "foe"
        assert any("prompt" in c.kwargs for c in m.call_args_list), "a claimed line ends with the prompt"
        assert _texts(self._run("examine stranger")) == "The stranger is smiling."

    def test_an_action_wins_over_a_command_that_shares_its_verb(self):
        self._load(VERBS)
        assert _texts(self._run("help the stranger")) == "You help the stranger to their feet."
        m = self._run("give the map to the stranger")
        assert _texts(m).startswith("You hand over the map.")
        assert _oob(m, "scenario_complete")[0]["action_id"] == 2

    def test_completion_sends_the_marker_and_the_structured_message_and_stays_put(self):
        room, _ = self._load()
        m = self._run("leave")          # an open action: it wins over the builders' `leave`
        assert _texts(m) == "You walk away.\n[SCENARIO_COMPLETE]"
        [done] = _oob(m, "scenario_complete")
        assert {k: done[k] for k in ("action_id", "outcome", "action_type", "correct", "canary")} == {
            "action_id": 2, "outcome": "enemy", "action_type": "enemy", "correct": False,
            "canary": False}
        assert done["labels"]["intent"] == "unknown" and done["scenario"] == KEY
        assert self.char1.location == room, "no move inside the action that ends the scenario"

    def test_a_line_that_is_no_open_action_goes_to_the_commands(self):
        self._load()
        assert "not available" in _texts(self._run("dance wildly"))
        assert "Command 'shove stranger' is not available" in _texts(self._run("shove stranger"))

    def test_the_next_load_is_fresh_and_deletes_the_old_instance(self):
        from evennia import ObjectDB
        start = self.char1.location
        first, _ = self._load()
        self._run("greet stranger")
        first_id = first.id
        second, _ = self._load()
        assert second.id != first_id and not ObjectDB.objects.filter(id=first_id).exists()
        assert second.play().stage == "initial" and self.char1.location == second
        assert self.char1.db.staged_return == start, "still the room the first load started from"

    def test_ending_takes_the_player_back_and_deletes_the_instance(self):
        from evennia import ObjectDB
        from typeclasses.staged.instances import end_scenario
        start = self.char1.location
        room, _ = self._load()
        room_id = room.id
        assert end_scenario(self.char1) and self.char1.location == start
        assert not ObjectDB.objects.filter(id=room_id).exists() and self.char1.db.staged_return is None
        assert not end_scenario(self.char1)

    def test_the_control_channel(self):
        from server.conf.inputfuncs import scenario
        self.session.puppet = self.char1

        def call(**kwargs):
            with mock.patch.object(self.session, "msg") as m:
                scenario(self.session, **kwargs)
            return m.call_args.kwargs["scenario"][0]

        status = call(cmd="status")
        assert status["ok"] and status["logged_in"] and status["character"] == "Char"
        loaded = call(cmd="load", key=KEY)
        assert loaded["ok"] and loaded["scenario"] == KEY and loaded["set"] == "fixture_set@1"
        assert loaded["stage"] == "initial" and loaded["room"] == "Test Room"
        bad = call(cmd="load", key="fixture_set/no_such_file")
        assert not bad["ok"] and "no scenario 'no_such_file'" in bad["error"]
        assert bad["room"] == "Test Room", "a bad load changes nothing"
        ended = call(cmd="end")
        assert ended["ok"] and ended["room"] == self.room1.key
        assert not call(cmd="end")["ok"] and "unknown scenario command" in call(cmd="jump")["error"]

    def test_every_command_in_a_staged_room_has_the_prompt_and_the_claim(self):
        from commands.command import AreaInputMixin, PromptMixin
        self._load()
        self.char1.at_cmdset_get()
        cmds = self.char1.cmdset.current.commands
        assert {type(c).__name__ for c in cmds} >= {"CmdStagedLook", "CmdStagedExamine",
                                                     "CmdStagedInventory", "CmdActions", "CmdLeave"}
        missing = sorted({type(c).__name__ for c in cmds
                          if not (isinstance(c, PromptMixin) and isinstance(c, AreaInputMixin))})
        assert not missing, f"commands without the prompt or the claim: {missing}"
