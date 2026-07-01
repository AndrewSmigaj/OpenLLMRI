"""Tier-2 integration: the co-op slice end-to-end on real Evennia (P1.7).

Two characters in one room; char1 acts, char2 hears it via the propagator; the world state (Attributes)
changes and mass conserves. Run: `make test-int`. Uses Evennia's EvenniaTest (self.char1/char2/room1).
"""
from unittest import mock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


class TestSlice(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        content.load()
        self.seat = create_object(
            "typeclasses.objects.Object", key="aircraft seat", location=self.room1, aliases=["seat"],
            attributes=[("sim_id", "seat"), ("materials", ["steel"]), ("mass_g", 5000),
                        ("state", {"ident": "11B"}),
                        ("parts", [
                            {"id": "cover", "label": "cover", "material": "synthetic_fabric",
                             "mass_g": 200, "attachment": "stitched",
                             "outputs_when_removed": ["loose_fabric"]},
                            {"id": "bolt", "label": "bolt", "material": "steel", "mass_g": 30,
                             "attachment": "bolted"},
                        ])])
        self.tool = create_object(
            "typeclasses.objects.Object", key="multitool", location=self.room1, aliases=["knife"],
            attributes=[("sim_id", "multitool"), ("materials", ["steel"]), ("mass_g", 150),
                        ("state", {"edge": 0.8})])

    def _said(self, m):
        return " ".join(str(c.args[0]) for c in m.call_args_list if c.args).lower()

    def _loose(self):
        return [o for o in self.room1.contents if o.db.sim_id == "seat:cover:loose"]

    def test_cut_frees_cover_and_conserves_mass(self):
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("cut cover off seat with multitool")
        assert all(p["id"] != "cover" for p in (self.seat.db.parts or [])), "cover should be detached"
        loose = self._loose()
        assert len(loose) == 1 and loose[0].db.mass_g == 200, "a 200g loose fabric object should be minted"
        assert "comes away" in self._said(m1) or "come" in self._said(m1)

    def test_cut_steel_bolt_redirects_without_state_change(self):
        before = [dict(p) for p in self.seat.db.parts]
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("cut bolt with multitool")
        assert [dict(p) for p in self.seat.db.parts] == before, "a failed cut must not change state"
        assert "skates off" in self._said(m1) or "keener" in self._said(m1)

    def test_second_player_hears_the_action(self):
        with mock.patch.object(self.char2, "msg") as m2:
            self.char1.execute_cmd("cut cover off seat with multitool")
        heard = self._said(m2)
        assert self.char1.key.lower() in heard or "saw" in heard, "char2 should perceive char1's action"

    def test_unknown_input_teaches_the_grammar(self):
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("frobnicate the seat")
        assert "verb" in self._said(m1) or "examine" in self._said(m1)

    def test_examine_lists_parts_with_ids(self):
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("examine seat")
        said = self._said(m1)
        assert "cover" in said and "bolt" in said and "11b" in said

    def test_clock_advances_via_the_shell(self):
        from typeclasses.apply import advance_clock
        advance_clock(self.room1, 5)
        assert self.room1.db.world_time == 5
        advance_clock(self.room1, 3)
        assert self.room1.db.world_time == 8   # deterministic, cumulative

    # --- the enriched operations, through the real command → apply → state path ---

    def _spawn(self, key, sim_id, materials, mass_g, aliases=(), state=None):
        return create_object("typeclasses.objects.Object", key=key, location=self.room1,
                             aliases=list(aliases),
                             attributes=[("sim_id", sim_id), ("materials", materials),
                                         ("mass_g", mass_g), ("state", state or {})])

    def test_light_sets_the_lit_state(self):
        tinder = self._spawn("dry grass", "tinder", ["dry_grass"], 40, ["tinder"])
        self._spawn("lighter", "lighter", ["plastic"], 20, ["lighter"], state={"ignition": True})
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("light the tinder with the lighter")
        assert (tinder.db.state or {}).get("lit") is True

    def test_melt_ice_mints_water_conserving_mass(self):
        self._spawn("chunk of ice", "ice", ["ice"], 600, ["ice"])
        self._spawn("lighter", "lighter", ["plastic"], 20, ["lighter"], state={"ignition": True})
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("melt the ice with the lighter")
        assert all(o.db.sim_id != "ice" for o in self.room1.contents), "the ice should be gone"
        water = [o for o in self.room1.contents if o.db.sim_id == "ice:melt:loose"]
        assert len(water) == 1 and water[0].db.mass_g == 600 and water[0].db.materials == ["water"]

    def test_pour_water_douses_a_fire(self):
        fire = self._spawn("campfire", "fire", ["wood"], 2000, ["campfire", "fire"], state={"lit": True})
        self._spawn("water", "water", ["water"], 500, ["water"])
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("pour the water on the campfire")
        assert (fire.db.state or {}).get("lit") is False, "the fire should be out"
        assert all(o.db.sim_id != "water" for o in self.room1.contents), "the water is spent"

    def test_break_bottle_shatters_conserving_mass(self):
        self._spawn("whisky bottle", "bottle", ["glass"], 500, ["bottle"])
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("break the bottle")
        assert all(o.db.sim_id != "bottle" for o in self.room1.contents), "the bottle is gone"
        shards = [o for o in self.room1.contents if str(o.db.sim_id).startswith("bottle:shard")]
        assert len(shards) == 3 and sum(o.db.mass_g for o in shards) == 500

    def test_real_scenario_loads_and_new_verbs_work_end_to_end(self):
        """Runs the ACTUAL build.build() (17 objects) and drives new verbs through the command path — the
        automated equivalent of the load-scenario smoke, and a regression guard on the scenario itself."""
        from world.scenarios.whiteout import build as scenario
        room = scenario.build()
        self.char1.location = room
        sims = {o.db.sim_id for o in room.contents}
        assert {"seat", "multitool", "tinder", "lighter", "ice", "snowdrift", "bottle", "wire",
                "paracord", "blanket", "manual", "canteen", "jerrycan", "jacket", "chocolate",
                "pilot"} <= sims, "the enriched crash cabin should have loaded"

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("light the tinder with the lighter")
            self.char1.execute_cmd("melt the ice with the lighter")
            self.char1.execute_cmd("break the bottle")
        tinder = next(o for o in room.contents if o.db.sim_id == "tinder")
        assert (tinder.db.state or {}).get("lit") is True
        assert any(o.db.sim_id == "ice:melt:loose" and o.db.mass_g == 600 for o in room.contents)
        assert sum(1 for o in room.contents if str(o.db.sim_id).startswith("bottle:shard")) == 3
