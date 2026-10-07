"""Tier-2 integration: the institute — the hub, the polysemy lab and the simulator.

Institute rooms tell the app where a character is (room_entered / room_left, the old prototype's
contract); the lab sends its preset; the simulator browses the scenario library and loads from it;
scenario moves run the rooms' hooks but stay silent; and walking between areas carries nothing across.
"""
import os
from pathlib import Path
from unittest import mock

import yaml
from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

LIBRARY = str(Path(__file__).resolve().parents[1] / "staged" / "library")
AREA_PACKAGES = ("commands.winter_survival", "commands.staged", "commands.institute")


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
class TestInstitute(EvenniaTest):
    """char1's account is a Developer (a researcher); char2's has no permissions (a visitor)."""

    def setUp(self):
        super().setUp()
        from world.institute.build import build
        self.start = create_object("typeclasses.rooms.Room", key="Limbo")
        self.hub, self.lab, self.sim = build(start=self.start)

    def _move(self, char, destination, **kwargs):
        with mock.patch.object(char, "msg") as m:
            char.move_to(destination, **kwargs)
        return m

    def _run(self, line, char=None):
        char = char or self.char1
        with mock.patch.object(char, "msg") as m:
            char.execute_cmd(line)
        return m

    def _area_commands(self, char):
        char.at_cmdset_get()
        return {type(c).__module__ for c in char.cmdset.current.commands
                if type(c).__module__.startswith(AREA_PACKAGES)}

    def test_the_build_makes_the_start_room_the_hub_and_is_idempotent(self):
        from world.institute.build import build
        assert self.hub == self.start and type(self.hub).__name__ == "HubRoom"
        assert self.hub.key == "Hub" and "Placeholder" in self.hub.db.desc
        assert build() == (self.hub, self.lab, self.sim)
        assert sorted(e.key for e in self.hub.exits) == ["polysemy lab", "simulator"]
        assert [e.destination for e in self.lab.exits] == [self.hub]
        assert [e.destination for e in self.sim.exits] == [self.hub]
        assert self.lab.key == "Polysemy Lab"

    def test_arriving_and_leaving_tell_the_app_the_room_and_the_role(self):
        m = self._move(self.char1, self.hub)
        assert _oob(m, "room_entered") == [{"room_type": "hub", "role": "researcher"}]
        m = self._move(self.char2, self.hub)
        assert _oob(m, "room_entered") == [{"room_type": "hub", "role": "visitor"}]
        m = self._move(self.char2, self.room1)
        assert _oob(m, "room_left") == [{"room_type": "hub"}] and not _oob(m, "room_entered")

    def test_the_lab_sends_its_preset_as_the_old_prototype_did(self):
        from typeclasses.institute.rooms import lab_presets_root
        preset = yaml.safe_load((lab_presets_root() / "polysemy_tank.yaml").read_text())
        # The old MicroWorldRoom's payload, built from the same preset file.
        expected = {"room_type": "micro_world", "role": "visitor",
                    "session_id": preset["session_id"],
                    "clustering_schema": preset["clustering_schema"],
                    "viz_preset": preset["viz_preset"]}
        assert _oob(self._move(self.char2, self.lab), "room_entered") == [expected]
        assert expected["session_id"] == "session_1434a9be"
        assert expected["clustering_schema"] == "tank_polysemy_k6_n20"
        assert expected["viz_preset"]["clustering_schema"] == "tank_polysemy_k6_n20"

    def test_logging_in_inside_an_institute_room_tells_the_app(self):
        self.char1.move_to(self.lab, quiet=True)
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.at_post_puppet()
        assert [c["room_type"] for c in _oob(m, "room_entered")] == ["micro_world"]

    def test_the_simulator_lists_the_sets_and_a_sets_scenarios(self):
        self.char2.move_to(self.sim, quiet=True)
        listing = _texts(self._run("simulator", self.char2))
        assert "fixture_set@1" in listing and "2 scenarios" in listing and "verbs_only (1)" in listing
        assert "fixture_world@1" in listing and "world" in listing
        scenarios = _texts(self._run("simulator fixture_set", self.char2))
        assert scenarios.startswith("fixture_set@1: 2 scenarios")
        assert "fixture_stranger" in scenarios and "fixture_verbs" in scenarios
        assert "fixture_world@1 is a world" in _texts(self._run("simulator fixture_world", self.char2))
        assert "no scenario set 'nothing'" in _texts(self._run("simulator nothing", self.char2))

    def test_visitors_browse_but_only_researchers_load(self):
        self.char2.move_to(self.sim, quiet=True)
        m = self._run("simulate fixture_set fixture_stranger", self.char2)
        assert "Only researchers" in _texts(m) and self.char2.location == self.sim

    def test_simulate_loads_a_staged_scenario_and_leave_comes_back(self):
        from typeclasses.staged.rooms import StagedRoom
        self.char1.move_to(self.sim, quiet=True)
        m = self._run("simulate fixture_set/verbs_only")
        room = self.char1.location
        assert isinstance(room, StagedRoom) and room.db.scenario_key == "fixture_set/fixture_verbs"
        assert _oob(m, "room_left") == [{"room_type": "simulator"}]
        assert _oob(m, "stage_entered")[0]["scenario"] == "fixture_set/fixture_verbs"
        agent_sees = "\n".join(_texts(self._run(c)) for c in ("look", "inventory", "actions"))
        assert agent_sees in _texts(m), "it shows what the runner reads first: the room, the inventory, the choices"
        assert "help stranger — Help the stranger up" in agent_sees
        m = self._run("leave")
        assert self.char1.location == self.sim
        assert _oob(m, "room_entered") == [{"room_type": "simulator", "role": "researcher"}]

    def test_simulate_names_a_scenario_or_reports_why_not(self):
        self.char1.move_to(self.sim, quiet=True)
        assert "no scenario 'missing'" in _texts(self._run("simulate fixture_set missing"))
        assert "no scenario 'fixture_stranger'" in _texts(
            self._run("simulate fixture_set/verbs_only fixture_stranger"))
        assert "no subset 'other'" in _texts(self._run("simulate fixture_set/other"))
        assert self.char1.location == self.sim, "a failed load changes nothing"
        self._run("simulate fixture_set fixture_stranger")
        assert self.char1.location.db.scenario_key == "fixture_set/fixture_stranger"

    def test_a_scenario_load_is_silent_but_tells_the_app_the_player_left(self):
        from typeclasses.staged.instances import end_scenario, load_scenario
        self.char1.move_to(self.hub, quiet=True)
        with mock.patch.object(self.char1, "msg") as m:
            load_scenario(self.char1, "fixture_set/fixture_stranger")
        assert _texts(m) == "" and _oob(m, "room_left") == [{"room_type": "hub"}]
        with mock.patch.object(self.char1, "msg") as m:
            end_scenario(self.char1)
        assert _texts(m) == "" and _oob(m, "room_entered") == [{"room_type": "hub", "role": "researcher"}]

    def test_simulate_enters_a_worlds_one_shared_room(self):
        from world.scenarios.winter_survival import content
        content.load()
        self.char1.move_to(self.sim, quiet=True)
        m = self._run("simulate fixture_world")
        cabin = self.char1.location
        assert type(cabin).__name__ == "WinterSurvivalRoom" and cabin.key == "crash cabin"
        assert _oob(m, "room_left") == [{"room_type": "simulator"}]
        assert self._area_commands(self.char1) == {"commands.winter_survival.cmd_act",
                                                    "commands.winter_survival.cmd_items",
                                                    "commands.winter_survival.cmd_speech"}
        self.char1.move_to(self.sim, quiet=True)
        self._run("simulate fixture_world")
        assert self.char1.location == cabin, "the same cabin, not a second one"

    def test_walking_staged_then_hub_then_the_world_carries_nothing_across(self):
        from world.scenarios.winter_survival import content
        content.load()
        before = set(self.char1.contents)
        self.char1.move_to(self.sim, quiet=True)
        self._run("simulate fixture_set fixture_verbs")
        self._run("give the map to the stranger")        # play it to the end
        self._run("leave")
        self._run("hub")
        assert self.char1.location == self.hub and self._area_commands(self.char1) == set()
        assert set(self.char1.contents) == before and self.char1.db.staged_return is None
        self._run("simulator")                          # in the hub, the exit to the simulator
        self._run("simulate fixture_world")
        self.char1.move_to(self.hub, quiet=True)
        assert self._area_commands(self.char1) == set()
        assert set(self.char1.contents) == before

    def test_every_command_in_the_simulator_has_the_prompt_and_the_claim(self):
        from commands.command import AreaInputMixin, PromptMixin
        self.char1.move_to(self.sim, quiet=True)
        self.char1.at_cmdset_get()
        cmds = self.char1.cmdset.current.commands
        assert {"CmdSimulator", "CmdSimulate"} <= {type(c).__name__ for c in cmds}
        missing = sorted({type(c).__name__ for c in cmds
                          if not (isinstance(c, PromptMixin) and isinstance(c, AreaInputMixin))})
        assert not missing, f"commands without the prompt or the claim: {missing}"
