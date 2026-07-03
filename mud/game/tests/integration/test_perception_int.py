"""Tier-2 integration: zones + movement on the REAL crash-site scenario (DR-13a).

Movement lands in P3.2; the perception exit-gate scripts (fading detail, graded events, the
reach gate) join in P3.3.
"""
from unittest import mock

from evennia.utils.test_resources import EvenniaTest


class TestMovement(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        from world.scenarios.whiteout.build import build
        content.load()
        self.scene = build()
        self.char1.location = self.scene    # unzoned character → room default_zone (mid_cabin)

    def _said(self, m):
        out = []
        for c in m.call_args_list:
            t = c.args[0] if c.args else c.kwargs.get("text")
            if isinstance(t, tuple):
                t = t[0]
            if t is not None:
                out.append(str(t))
        return " ".join(out).lower()

    def _zone(self):
        return (self.char1.db.state or {}).get("zone")

    def test_go_moves_the_zone_attribute_and_narrates_arrival(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("go to the rear cabin")
        assert self._zone() == "rear_cabin"
        assert "you make your way to the rear cabin" in self._said(m)

    def test_no_route_names_direction_and_first_step(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("go to the treeline")
        assert self._zone() is None, "no move happened"
        said = self._said(m)
        assert "to the north" in said and "rear cabin" in said

    def test_bare_go_orients(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("go")
        said = self._said(m)
        assert "you're in the mid cabin" in said
        assert "cockpit" in said and "rear cabin" in said

    def test_minted_scraps_inherit_the_actors_zone(self):
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("cut the cushion with the multitool")
        scraps = [o for o in self.scene.contents
                  if str(o.db.sim_id).startswith("seat:cushion_scrap")]
        assert scraps and all((o.db.state or {}).get("zone") == "mid_cabin" for o in scraps)

    def test_dropped_object_syncs_to_the_droppers_zone(self):
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("get multitool")
            self.char1.execute_cmd("go to the rear cabin")
            self.char1.execute_cmd("drop multitool")
        tool = next(o for o in self.scene.contents if o.db.sim_id == "multitool")
        assert (tool.db.state or {}).get("zone") == "rear_cabin"

    def test_walk_the_breach_to_the_treeline(self):
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("go to the rear cabin")
            self.char1.execute_cmd("go to the breach")
            self.char1.execute_cmd("go to the treeline")
        assert self._zone() == "treeline"
