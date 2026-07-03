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


class TestPerceptionExitGates(TestMovement):
    """The three roadmap P3 exit gates, as scripts against the real scenario."""

    def _look(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("look")
        return self._said(m)

    def test_exit_gate_1_crossing_the_scene_fades_detail(self):
        said = self._look()                              # mid cabin: with the seat
        assert "you are in the mid cabin" in said
        assert "wrenched sideways" in said, "same zone: the full authored scene phrase"

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("go to the rear cabin")
        said = self._look()                              # adjacent: clear, direction-framed
        assert "to the south" in said and "seat" in said

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("go to the breach")
        said = self._look()                              # near: names only
        assert "make out" in said and "aircraft seat" in said
        assert "wrenched sideways" not in said, "the authored phrase faded with distance"

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("go to the treeline")
        said = self._look()                              # distant: vague, unnamed
        assert "aircraft seat" not in said and "multitool" not in said
        assert "shape" in said and "snow" in said

    def test_exit_gate_2_one_event_two_perceptions(self):
        self.char2.location = self.scene                 # default zone: mid cabin (with char1)
        with mock.patch.object(self.char2, "msg"):
            self.char2.execute_cmd("go to the rear cabin")
        with mock.patch.object(self.char2, "msg") as m2:
            self.char1.execute_cmd("cut the cover off the seat with the multitool")
        heard = self._said(m2)                           # adjacent: the full line, direction-framed
        assert "to the south" in heard and "saws at the cover" in heard

        with mock.patch.object(self.char2, "msg"):
            self.char2.execute_cmd("go to the breach")
            self.char2.execute_cmd("go to the treeline")
        with mock.patch.object(self.char2, "msg") as m3:
            self.char1.execute_cmd("cut the jacket with the multitool")
        heard = self._said(m3)                           # distant: vague, no verb, no target
        assert "saws" not in heard and "jacket" not in heard
        assert "someone is moving" in heard

    def test_exit_gate_3_manipulation_blocked_beyond_reach_then_succeeds(self):
        tinder = next(o for o in self.scene.contents if o.db.sim_id == "tinder")
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("light the tinder with the lighter")
        said = self._said(m)                             # tinder is at the treeline, 3 zones off
        assert "too far away to light" in said and "to the north" in said
        assert not (tinder.db.state or {}).get("lit"), "blocked: no state change"

        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("get the ice")        # outside_tail: the stock-get reach gate
        assert "too far away to take" in self._said(m)

        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("get the lighter")    # same zone: fine
            self.char1.execute_cmd("go to the rear cabin")
            self.char1.execute_cmd("go to the breach")
            self.char1.execute_cmd("go to the treeline")
            self.char1.execute_cmd("light the tinder with the lighter")
        assert (tinder.db.state or {}).get("lit") is True, "in reach, the same command succeeds"

    def test_look_at_a_far_thing_gives_the_s17_answer(self):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("look at the radio")  # cockpit, adjacent — visible, unreachable
        said = self._said(m)
        assert "too far away to inspect" in said and "to the south" in said
