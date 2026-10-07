"""Tier-2 integration: watching an agent play, guests, and running agents from the simulator.

A watcher follows a character into each scenario instance it loads and back out; in a scenario's
room it reads but can't act or speak (anything said there would reach the player's observation, an
agent's prompt). Guests are visitors. The simulator's `agent` command asks the backend to run the
model on library keys.
"""
import os
from pathlib import Path
from unittest import mock

from django.conf import settings
from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

LIBRARY = str(Path(__file__).resolve().parents[1] / "staged" / "library")
STRANGER = "fixture_set/fixture_stranger"
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


@mock.patch.dict(os.environ, {"SCENARIO_LIBRARY": LIBRARY})
class TestWatching(EvenniaTest):
    """char1 (a researcher) plays; char2 (a visitor) watches."""

    def setUp(self):
        super().setUp()
        from world.institute.build import build
        self.hub, self.lab, self.sim = build(start=create_object("typeclasses.rooms.Room", key="Limbo"))
        self.char1.move_to(self.hub, quiet=True)
        self.char2.move_to(self.hub, quiet=True)

    def _run(self, line, char):
        with mock.patch.object(char, "msg") as m:
            char.execute_cmd(line)
        return m

    def test_a_watcher_follows_the_player_into_each_new_instance_and_back(self):
        from typeclasses.staged.instances import end_scenario, load_scenario
        assert "You are watching Char." in _texts(self._run("watch char", self.char2))
        first, _ = load_scenario(self.char1, STRANGER)
        assert self.char2.location == first
        second, _ = load_scenario(self.char1, VERBS)
        assert self.char2.location == second, "moved along before the old instance was deleted"
        end_scenario(self.char1)
        assert self.char1.location == self.hub and self.char2.location == self.hub

    def test_a_watcher_reads_but_cannot_act_or_speak(self):
        from typeclasses.staged.instances import load_scenario
        self._run("watch char", self.char2)
        room, _ = load_scenario(self.char1, STRANGER)
        assert "A plain test room." in _texts(self._run("look", self.char2))
        with mock.patch.object(self.char1, "msg") as player:
            m = self._run("greet stranger", self.char2)          # an open action: not the watcher's
            self._run("say hello", self.char2)
        assert room.play().stage == "initial", "a watcher's line is never claimed as an action"
        assert "not available" in _texts(m)
        assert _texts(player) == "", "nothing a watcher types reaches the player"

    def test_watchers_read_what_the_player_types(self):
        from typeclasses.staged.instances import load_scenario
        self._run("watch char", self.char2)
        load_scenario(self.char1, STRANGER)
        with mock.patch.object(self.char2, "msg") as seen:
            self.char1.execute_cmd("examine stranger")
            self.char1.execute_cmd("look {at} $you()")       # read as typed, never as a format
            self.char1.execute_cmd("greet stranger")
        assert "Char: examine stranger" in _texts(seen) and "Char: greet stranger" in _texts(seen)
        assert "Char: look {at} $you()" in _texts(seen)

    def test_unwatch_goes_back_to_where_watching_started(self):
        from typeclasses.staged.instances import load_scenario
        self.char2.move_to(self.lab, quiet=True)
        self._run("watch char", self.char2)
        load_scenario(self.char1, STRANGER)
        self._run("unwatch", self.char2)
        assert self.char2.location == self.lab and self.char2.db.watching is None
        assert not self.char1.db.watchers
        assert "aren't watching" in _texts(self._run("unwatch", self.char2))

    def test_watching_someone_not_in_the_world_follows_them_into_their_next_scenario(self):
        from typeclasses.staged.instances import load_scenario
        self.char1.location = None                     # logged out, as an agent is between runs
        assert "next scenario it loads" in _texts(self._run("watch char", self.char2))
        assert self.char2.location == self.hub
        self.char1.location = self.hub                 # it logs in, and its run loads a scenario
        room, _ = load_scenario(self.char1, STRANGER)
        assert self.char2.location == room

    def test_a_watcher_leaving_the_game_is_never_announced_to_the_player(self):
        from typeclasses.staged.instances import load_scenario
        self._run("watch char", self.char2)
        load_scenario(self.char1, STRANGER)
        with mock.patch.object(self.char1, "msg") as player:
            self.char2.at_pre_unpuppet()               # Account.unpuppet_object's order
            self.char2.at_post_unpuppet(self.account2)
        assert _texts(player) == "", "'Char2 has left the game.' would reach an agent's prompt"
        assert self.char2.db.watching is None and not self.char1.db.watchers

    def test_a_watcher_cannot_follow_into_a_world(self):
        from world.scenarios.winter_survival import content
        content.load()
        cabin = create_object("typeclasses.winter_survival.rooms.WinterSurvivalRoom", key="crash cabin")
        self.char1.move_to(cabin, quiet=True)
        assert "can't follow yet" in _texts(self._run("watch char", self.char2))
        assert self.char2.location == self.hub

    def test_guests_are_visitors_in_the_hub(self):
        from typeclasses.institute.rooms import role_of
        from evennia.utils.utils import class_from_module
        assert settings.GUEST_ENABLED
        Guest = class_from_module(settings.BASE_GUEST_TYPECLASS)
        # A guest's character starts at START_LOCATION, which in the MUD is the hub (#2, `make institute`).
        with mock.patch.object(settings, "START_LOCATION", self.hub.dbref):
            account, errors = Guest.create(ip="127.0.0.1")
        assert account is not None, errors
        [character] = account.characters.all()
        assert character.location == self.hub and role_of(character) == "visitor"


@mock.patch.dict(os.environ, {"SCENARIO_LIBRARY": LIBRARY, "EVENNIA_AGENT_USER": "agent"})
class TestAgentFromTheSimulator(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.institute.build import build
        _, _, self.sim = build(start=create_object("typeclasses.rooms.Room", key="Limbo"))
        self.char1.move_to(self.sim, quiet=True)
        self.calls = []

    def _backend(self, reply):
        def ask(path, payload, on_reply, on_error):
            self.calls.append((path, payload))
            on_reply(reply)
        return mock.patch("commands.institute.commands.ask_backend", ask)

    def _run(self, line, char=None):
        char = char or self.char1
        with mock.patch.object(char, "msg") as m:
            char.execute_cmd(line)
        return m

    def test_agent_run_asks_the_backend_to_play_library_keys(self):
        with self._backend({"session_id": "session_x"}):
            m = self._run("agent run fixture_set/verbs_only")
        [(path, payload)] = self.calls
        assert path == "/api/agent/start" and payload["auto_start"] is True
        assert payload["scenario_list"] == [VERBS] and payload["scenario_id"] == "fixture_set"
        assert payload["target_words"] == ["stranger"]
        assert "session_x started on 1 scenario(s)" in _texts(m) and "watch agent" in _texts(m)
        assert self.char1.db.agent_session == "session_x"
        with self._backend({"session_id": "session_x", "total_turns": 3}):
            m = self._run("agent stop")
        assert self.calls[-1] == ("/api/agent/stop", {"session_id": "session_x"})
        assert "stopped after 3 turns" in _texts(m) and self.char1.db.agent_session is None

    def test_a_refusal_is_reported_and_a_bad_key_never_reaches_the_backend(self):
        def refuse(path, payload, on_reply, on_error):
            self.calls.append(path)
            on_error("409 Agent loop already running for session session_y. Stop it first.")
        with mock.patch("commands.institute.commands.ask_backend", refuse):
            m = self._run("agent run fixture_set fixture_stranger")
        assert "already running" in _texts(m)
        with self._backend({}):
            m = self._run("agent run fixture_set nothing_here")
        assert "no scenario 'nothing_here'" in _texts(m) and self.calls == ["/api/agent/start"]

    def test_visitors_cannot_run_agents(self):
        self.char2.move_to(self.sim, quiet=True)
        with self._backend({}):
            m = self._run("agent run fixture_set", self.char2)
        assert "Only researchers" in _texts(m) and not self.calls
