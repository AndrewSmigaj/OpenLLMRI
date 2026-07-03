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
                            {"id": "cushion", "label": "cushion", "material": "foam",
                             "mass_g": 800, "attachment": "clipped",
                             "outputs_when_removed": ["loose_foam"]},
                        ])])
        self.tool = create_object(
            "typeclasses.objects.Object", key="multitool", location=self.room1, aliases=["knife"],
            attributes=[("sim_id", "multitool"), ("materials", ["steel"]), ("mass_g", 150),
                        ("state", {"edge": 0.8, "leverage": 0.5})])  # mirrors build.py:40-42

    def _said(self, m):
        # stock commands (look) send msg(text=(str, {...})) kwarg tuples; sim commands positional str
        out = []
        for c in m.call_args_list:
            t = c.args[0] if c.args else c.kwargs.get("text")
            if isinstance(t, tuple):
                t = t[0]
            if t is not None:
                out.append(str(t))
        return " ".join(out).lower()

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
        assert all(o.key == "glass shard" for o in shards), "derived names read material-first"

    # --- presentation (DR-23): scene-as-prose + the unified renderer ---

    def test_look_renders_prose_not_a_contents_list(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("look")
        said = self._said(m)
        assert "you see:" not in said, "the stock contents list must be gone"
        assert "wrenched sideways" in said, "the seat's authored scene phrase should carry the room"
        assert "multitool" in said, "everything present is still mentioned (weighting, not hiding)"

    def test_server_start_loads_the_content_registries(self):
        # regression (2026-07-03): the login auto-look fired before any command import on a fresh
        # server, so the appearance registry was empty and look degraded to bare fallbacks.
        from world.sim import narrator, presentation
        narrator.load_responses({})
        presentation.load_appearance({})
        from server.conf.at_server_startstop import at_server_start
        at_server_start()
        assert presentation._APPEARANCE, "at_server_start must load the appearance registry"
        assert narrator.get("cut.too_dull"), "at_server_start must load the narration templates"

    def test_look_at_equals_examine(self):
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("look at seat")
        with mock.patch.object(self.char1, "msg") as m2:
            self.char1.execute_cmd("examine seat")
        assert self._said(m1) == self._said(m2), "look at X and examine X are the same renderer"
        assert "held by stitching" in self._said(m2), "parts weave in as physical prose"
        assert "(foam" not in self._said(m2), "attachments are never rendered as data"

    # --- attachment honesty (DR-05a / DR-09a) ---

    def test_cut_clipped_cushion_end_to_end_mints_foam_scraps(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("cut the cushion with the multitool")
        assert all(p["id"] != "cushion" for p in (self.seat.db.parts or [])), "cushion extracted"
        scraps = [o for o in self.room1.contents
                  if str(o.db.sim_id).startswith("seat:cushion_scrap")]
        assert len(scraps) == 3 and sum(o.db.mass_g for o in scraps) == 800
        assert all(o.key == "foam scrap" for o in scraps)
        said = self._said(m)
        assert "foam scrap" in said and "crushed clips" in said

    def test_pry_stitched_cover_explains_the_stitching(self):
        before = [dict(p) for p in self.seat.db.parts]
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("pry the cover off the seat with the multitool")
        assert [dict(p) for p in self.seat.db.parts] == before, "an explained refusal changes nothing"
        said = self._said(m)
        assert "stitching" in said and "cushion" in said, "explains why + hints the pryable sibling"

    # --- the numbered disambiguation menu (slice-fix M3) ---

    def test_numbered_menu_pick_runs_the_original_command(self):
        self._spawn("whisky bottle", "bottle", ["glass"], 500, ["bottle"])
        with mock.patch.object(self.char1, "msg") as m1:
            self.char1.execute_cmd("break the bottle")
            self.char1.execute_cmd("examine shard")           # 3 identical "glass shard"s
        said = self._said(m1)
        assert "which shard" in said and "1." in said and "3." in said, "expected a numbered menu"
        with mock.patch.object(self.char1, "msg") as m2:
            self.char1.execute_cmd("2")                        # the pick re-runs 'examine shard'
        said2 = self._said(m2)
        assert "which shard" not in said2 and "glass" in said2, "the pick should run examine, not re-menu"

    def test_pick_preserves_the_with_tool(self):
        self._spawn("whisky bottle", "bottle", ["glass"], 500, ["bottle"])
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("break the bottle")
            self.char1.execute_cmd("cut shard with multitool")  # ambiguous X + a WITH tool
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("2")
        assert "multitool" in self._said(m), "the WITH slot must survive the numbered pick"

    def test_stale_menu_pick_degrades_cleanly(self):
        self._spawn("whisky bottle", "bottle", ["glass"], 500, ["bottle"])
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("break the bottle")
            self.char1.execute_cmd("examine shard")
        for o in list(self.room1.contents):                    # the world moves on mid-menu
            if str(o.db.sim_id).startswith("bottle:shard"):
                o.delete()
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("2")                        # must answer, never crash
        assert self._said(m), "a stale pick should get an informative answer"

    def test_number_without_menu_teaches_the_grammar(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("2")
        assert "verb" in self._said(m) or "examine" in self._said(m)

    def test_real_scenario_loads_and_new_verbs_work_end_to_end(self):
        """Runs the ACTUAL build.build() (17 objects, ZONED as of P3) and drives verbs through the
        command path — now WALKING the crash site between them: the automated equivalent of the
        load-scenario smoke, the scenario regression guard, and an end-to-end P3 exit-gate script."""
        from world.scenarios.whiteout import build as scenario
        room = scenario.build()
        self.char1.location = room                   # unzoned char → default zone (mid cabin)
        sims = {o.db.sim_id for o in room.contents}
        assert {"seat", "multitool", "tinder", "lighter", "ice", "snowdrift", "bottle", "wire",
                "paracord", "blanket", "manual", "canteen", "jerrycan", "jacket", "chocolate",
                "pilot"} <= sims, "the enriched crash cabin should have loaded"

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("get the lighter")            # mid cabin
            self.char1.execute_cmd("go to the rear cabin")
            self.char1.execute_cmd("break the bottle")           # rear cabin
            self.char1.execute_cmd("go to the breach")
            self.char1.execute_cmd("melt the ice with the lighter")   # outside the tail
            self.char1.execute_cmd("go to the treeline")
            self.char1.execute_cmd("light the tinder with the lighter")
        tinder = next(o for o in room.contents if o.db.sim_id == "tinder")
        assert (tinder.db.state or {}).get("lit") is True
        assert any(o.db.sim_id == "ice:melt:loose" and o.db.mass_g == 600 for o in room.contents)
        assert sum(1 for o in room.contents if str(o.db.sim_id).startswith("bottle:shard")) == 3
