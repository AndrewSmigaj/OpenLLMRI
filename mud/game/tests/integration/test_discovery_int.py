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

        said = self._do("search the duffel bag")
        assert "multitool" in said and "socks" in said and "paracord" in said
        self._do("take the multitool from the duffel bag")
        assert self._carried("multitool")

        said = self._do("search 11b")
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
        self._do("go to the mid cabin", "search the duffel bag", "take the multitool",
                 "go to the rear cabin")
        said = self._do("pry the aft bin with the multitool")
        assert "hangs open" in said
        said = self._do("examine the aft bin")
        assert "backpack" in said
        said = self._do("search the backpack")
        assert "canteen" in said and "shirt" in said

    def test_pry_the_panel_reveals_the_wire(self):
        self._do("search the duffel bag", "take the multitool", "go to the cockpit")
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
        said = self._do("take 11b")
        assert "part of the wreck" in said
        said = self._do("go to the cockpit", "take the pilot")
        assert "dead weight" in said

    def test_the_wear_loop_and_the_warmth_band(self):
        said = self._do("go to the rear cabin", "wear the blanket")   # straight off the floor
        assert "you pull on the wool blanket" in said
        said = self._do("inventory")
        assert "wearing: wool blanket" in said
        said = self._do("go to the mid cabin", "search the duffel bag", "take the socks",
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

    def test_read_the_manual_for_the_guard_frequency(self):
        said = self._do("go to the cockpit", "read the manual")
        assert "121.5" in said, "the §38 clue is earned by reading, not listed"

    def test_talking_gets_honest_silence(self):
        said = self._do("go to the cockpit", "talk to the pilot")
        assert "nobody will" in said
        said = self._do("talk to the radio")
        assert "nothing to say" in said

    def test_look_at_a_zone_gives_its_survey(self):
        said = self._do("look at the cockpit")
        assert "shattered instruments" in said, "stock look routes zone nouns to the sim path"

    def test_the_cabin_desc_stays_indoors(self):
        self._do("go to the rear cabin", "go to the breach")   # arrive-looks captured separately
        said = self._do("look")
        assert "you are in the torn tail opening" in said
        assert "crushed cabin of a downed light plane" not in said

    # --- the scattered wreck (§8b: the crash is the difficulty engine) ---

    def test_the_tail_is_a_real_expedition(self):
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("go to the rear cabin")
            self.char1.execute_cmd("go to the breach")
            self.char1.execute_cmd("go to the debris trail")
            self.char1.execute_cmd("go to the tail section")
        assert (self.char1.db.state or {}).get("zone") == "tail_section"

    def test_the_kit_scattered_and_the_hatchet_is_buried(self):
        self._do("go to the rear cabin", "go to the breach", "go to the debris trail")
        said = self._do("search the torn survival duffel")
        assert "ration tin" in said and "matchbox" in said and "headnet" in said
        assert "hatchet" not in said, "the hatchet was FLUNG, not bagged (power costs distance)"
        said = self._do("dig the wind-packed drift")
        assert "hatchet" in said and "flare" in said
        self._do("take the hatchet")
        said = self._do("examine the hatchet")
        assert "cracked" in said and "broken" in said, "the crash damaged the prize"

    def test_the_soaked_matches_tell_their_bootstrap_story(self):
        self._do("go to the rear cabin", "go to the breach", "go to the debris trail",
                 "search the torn survival duffel")
        said = self._do("examine the matchbox")
        assert "soaked" in said and "dried" in said

    def test_the_tail_cone_pry_and_the_prizes(self):
        self._do("search the duffel bag", "take the multitool",
                 "go to the rear cabin", "go to the breach", "go to the debris trail",
                 "go to the tail section")
        said = self._do("open the tail cone")
        assert "lever" in said
        said = self._do("pry the tail cone with the multitool")
        assert "hangs open" in said
        said = self._do("examine the tail cone")
        assert "sleeping bag" in said and "snowshoes" in said
        self._do("take the sleeping bag")
        said = self._do("wear the sleeping bag")
        assert "you pull on the sleeping bag" in said
        said = self._do("examine the emergency locator transmitter")
        assert "121.5" in said and "sheared" in said, "the ELT tells the rescue arc's story"

    def test_the_paper_tells_stories(self):
        self._do("go to the rear cabin", "go to the breach", "go to the debris trail",
                 "search the mail sack")
        said = self._do("read the letters")
        assert "slapshot" in said, "the mail is people, not loot"
        said = self._do("go to the breach", "go to the rear cabin", "go to the mid cabin",
                        "go to the cockpit", "read the chart")
        assert "cabin" in said and "wood stove" in said, "the chart plants the next scene"

    def test_put_it_back(self):
        self._do("search the duffel bag", "take the socks")
        assert self._carried("socks")
        said = self._do("put the socks in the duffel bag")
        assert "you stow the wool socks" in said
        assert not self._carried("socks")
