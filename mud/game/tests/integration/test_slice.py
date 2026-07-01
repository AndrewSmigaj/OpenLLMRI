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
