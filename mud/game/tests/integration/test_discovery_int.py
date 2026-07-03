"""Tier-2 integration: DR-24 discovery on the REAL re-stowed scenario — earn everything."""
from unittest import mock

from evennia.utils.test_resources import EvenniaTest


class TestDiscovery(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        from world.scenarios.whiteout.build import build
        content.load()
        self.scene = build()
        self.char1.location = self.scene       # default zone: mid cabin

    def _said(self, m):
        out = []
        for c in m.call_args_list:
            t = c.args[0] if c.args else c.kwargs.get("text")
            if isinstance(t, tuple):
                t = t[0]
            if t is not None:
                out.append(str(t))
        return " ".join(out).lower()

    def _do(self, *cmds):
        with mock.patch.object(self.char1, "msg") as m:
            for c in cmds:
                self.char1.execute_cmd(c)
        return self._said(m)

    def _carried(self, sim_id):
        return any(o.db.sim_id == sim_id for o in self.char1.contents)

    def test_scene_shows_fixtures_never_contents(self):
        said = self._do("look")
        assert "duffel" in said and "overhead bin" in said, "containers are the scene"
        for hidden in ("multitool", "lighter", "chocolate", "socks", "first-aid", "wire"):
            assert hidden not in said, f"{hidden} must be EARNED, not listed"

    def test_the_canonical_discovery_script(self):
        said = self._do("open the forward overhead bin")
        assert "you open the forward overhead bin" in said
        said = self._do("examine the forward overhead bin")
        assert "first-aid kit" in said, "revealed contents weave into examine"
        self._do("take the kit")
        assert self._carried("firstaid")

        said = self._do("search the duffel")
        assert "multitool" in said and "socks" in said and "paracord" in said
        self._do("take the multitool from the duffel")
        assert self._carried("multitool")

        said = self._do("search the seat")
        assert "seatback pocket" in said
        said = self._do("search the seatback pocket")
        assert "chocolate" in said
        self._do("take the chocolate")
        assert self._carried("chocolate")

        said = self._do("go to the cockpit", "frisk the pilot")
        assert "lighter" in said and "jacket" not in said, "worn layers aren't pocket finds"
        self._do("take the lighter")
        assert self._carried("lighter")

        said = self._do("take the jacket")
        assert "he doesn't mind" in said, "stripping the dead gets the dignity line"
        assert self._carried("jacket")

    def test_pry_the_aft_bin_then_the_backpack_chain(self):
        said = self._do("go to the rear cabin", "open the aft bin")
        assert "lever" in said, "the jammed bin hints at leverage"
        self._do("go to the mid cabin", "search the duffel", "take the multitool",
                 "go to the rear cabin")
        said = self._do("pry the aft bin with the multitool")
        assert "hangs open" in said
        said = self._do("examine the aft bin")
        assert "backpack" in said
        said = self._do("search the backpack")
        assert "canteen" in said and "shirt" in said

    def test_pry_the_panel_reveals_the_wire(self):
        self._do("search the duffel", "take the multitool", "go to the cockpit")
        said = self._do("pry the panel with the multitool")
        assert "hangs open" in said
        self._do("take the wire from the panel")
        assert self._carried("wire")

    def test_dig_the_snowdrift_for_the_gloves(self):
        said = self._do("go to the rear cabin", "dig the snowdrift")
        assert "leather gloves" in said and "sleeves" in said
        self._do("take the gloves")
        assert self._carried("gloves")

    def test_fixed_and_heavy_refuse_honestly(self):
        said = self._do("take the seat")
        assert "part of the wreck" in said
        said = self._do("go to the cockpit", "take the pilot")
        assert "dead weight" in said

    def test_the_wear_loop_and_the_warmth_band(self):
        said = self._do("go to the rear cabin", "wear the blanket")   # straight off the floor
        assert "you pull on the wool blanket" in said
        said = self._do("inventory")
        assert "wearing: wool blanket" in said
        said = self._do("go to the mid cabin", "search the duffel", "take the socks",
                        "wear the socks", "examine me")
        assert "wool blanket" in said and "wool socks" in said
        assert "you are" in said                       # the warmth band line
        look_me = self._do("look at me")
        exam_me = self._do("examine me")
        assert look_me == exam_me, "look at me ≡ examine me, byte for byte"
        said = self._do("drop the blanket")
        assert "take it off first" in said
        said = self._do("take off the blanket")
        assert "you take off the wool blanket" in said

    def test_the_pilot_wears_his_jacket_visibly(self):
        said = self._do("go to the cockpit", "examine the pilot")
        assert "wears" in said and "flight jacket" in said, "the worn layer IS the frisk clue"

    def test_put_it_back(self):
        self._do("search the duffel", "take the socks")
        assert self._carried("socks")
        said = self._do("put the socks in the duffel")
        assert "you stow the wool socks" in said
        assert not self._carried("socks")
