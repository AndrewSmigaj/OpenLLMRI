"""Tier-2 integration: stock get/drop share the DR-08a numbered menu (cmd_items subclasses).

The menu must appear on a true multimatch, a bare-number pick must re-run the original intent on
the chosen object, leading-count stacking must stay stock, and stale picks must degrade cleanly.
"""
from unittest import mock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest


class TestStockMenus(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        content.load()

    def _said(self, m):
        return " ".join(str(c.args[0]) for c in m.call_args_list if c.args).lower()

    def _spawn_shards(self, n=3, where=None):
        return [create_object("typeclasses.objects.Object", key="glass shard",
                              location=(where or self.room1),
                              attributes=[("sim_id", f"bottle:shard{i}:loose"),
                                          ("materials", ["glass"]), ("mass_g", 100),
                                          ("state", {})])
                for i in range(n)]

    def _carried(self):
        return [o for o in self.char1.contents if o.key == "glass shard"]

    def test_get_multimatch_shows_numbered_menu_and_pick_takes_one(self):
        self._spawn_shards(3)
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("get shard")
        said = self._said(m)
        assert "which shard" in said and "1." in said and "3." in said, "expected our numbered menu"
        assert "more than one match" not in said, "stock multimatch text must not appear"
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("2")
        assert len(self._carried()) == 1, "the pick should take exactly one shard"

    def test_drop_multimatch_menu_pick_drops_the_chosen_one(self):
        self._spawn_shards(2, where=self.char1)
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("drop shard")
        assert "which shard" in self._said(m)
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("1")
        assert len(self._carried()) == 1
        assert len([o for o in self.room1.contents if o.key == "glass shard"]) == 1

    def test_get_with_leading_count_still_stacks(self):
        self._spawn_shards(3)
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("get 3 shard")
        assert "which shard" not in self._said(m), "a count of identical things must not menu"
        assert len(self._carried()) == 3

    def test_stock_pick_after_world_change_degrades_cleanly(self):
        shards = self._spawn_shards(3)
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("get shard")
        shards[1].delete()                      # option 2's object vanishes mid-menu
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("2")
        assert self._said(m), "a stale pick should get an informative answer, never a traceback"

    def test_stock_menu_supersedes_sim_menu_and_vice_versa(self):
        self._spawn_shards(2)
        with mock.patch.object(self.char1, "msg"):
            self.char1.execute_cmd("examine shard")   # sim menu pending
            self.char1.execute_cmd("get shard")       # stock menu replaces it
            self.char1.execute_cmd("1")               # answers the STOCK menu
        assert len(self._carried()) == 1
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd("get shard")       # stock menu (1 in room... now single match)
        # the reverse order: stock menu then sim menu wins
        self._spawn_shards(2)
        with mock.patch.object(self.char1, "msg") as m2:
            self.char1.execute_cmd("get shard")       # stock menu pending (>1 in room again)
            self.char1.execute_cmd("examine shard")   # sim menu replaces it
            self.char1.execute_cmd("1")
        assert "made of glass" in self._said(m2), "the pick should answer the sim examine menu"
