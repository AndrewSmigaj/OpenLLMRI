"""Tier-2: the crash draw on real Evennia — build.dress() loads a slot INTO a character (worn things
worn, pockets searched by their owner, the wound on the character) and the self-view reads it."""
from unittest import mock

from evennia.utils.test_resources import EvenniaTest


class TestKit(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        from world.scenarios.whiteout.build import build, dress
        content.load()
        self.scene = build()
        self.char1.move_to(self.scene, quiet=True)
        self.char1.db.sim_id = "me"
        dress(self.char1, "townie")

    def _said(self, m):
        out = []
        for c in m.call_args_list:
            t = c.args[0] if c.args else c.kwargs.get("text")
            if isinstance(t, tuple):
                t = t[0]
            if t is not None:
                out.append(str(t))
        return " ".join(out).lower()

    def test_dressed_character_wears_pockets_and_wound(self):
        worn = [o for o in self.char1.contents if (o.db.state or {}).get("worn_by") == "me"]
        assert {o.key for o in worn} >= {"denim jacket", "cotton hoodie", "jeans", "sneakers"}
        pockets = [o for o in self.char1.contents if o.key == "pockets"][0]
        assert {o.key for o in pockets.contents} >= {"phone", "wallet", "ring of keys"}
        assert (self.char1.db.state or {}).get("wounds")[0]["kind"] == "cut"
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("examine me")
            self.char1.execute_cmd("examine pockets")
            self.char1.execute_cmd("take the phone")
        said = self._said(m)
        assert "denim jacket" in said and "forearm is cut and bleeding" in said
        assert "phone" in said and "wallet" in said
        assert any(o.key == "phone" and o.location == self.char1 for o in self.char1.contents)
