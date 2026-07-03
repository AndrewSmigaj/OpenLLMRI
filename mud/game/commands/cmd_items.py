"""game.commands.cmd_items — stock get/drop with the DR-08a numbered disambiguation menu.

Thin subclasses of Evennia's CmdGet/CmdDrop: a pre-flight quiet search detects a TRUE multimatch
(more than one hit that isn't a leading-count stack of identical keys) and shows the same numbered
menu the taught-grammar commands use; everything else defers to the stock implementation (single
match, no match, stacked counts). A pick (a bare number, caught by the unmatched-input command)
re-issues the original command with Evennia's native `name-N` ordinal, recomputed against the
manager's stable id-ordered search at pick time — so picks are reorder-immune and stale-safe.
`give` is deferred (third use). One pending menu per caller; the latest question wins.

Note: search-lock filtering happens after the manager computes ordinals, so a search-locked object
could in principle desync the re-issue index — no Whiteout content uses search locks (accepted).
"""
from __future__ import annotations

from evennia.commands.default.general import (CmdDrop as DefaultCmdDrop, CmdGet as DefaultCmdGet,
                                              CmdLook as DefaultCmdLook)

from commands import cmd_act  # shared pending-menu map; import direction: cmd_items -> cmd_act only


_ARTICLES = ("the ", "a ", "an ", "some ")


def _strip_articles(args: str) -> str:
    """The taught grammar ignores articles; the stock item commands must match ('get the ice')."""
    a = (args or "").strip()
    low = a.lower()
    for art in _ARTICLES:
        if low.startswith(art):
            return a[len(art):].strip()
    return a


def _search(caller, query, where):
    """The same candidate set at menu time and pick time: room / inventory / both ('around' —
    stock look's default candidates). Quiet, id-ordered (stable), always a list."""
    loc = {"room": caller.location, "inv": caller}.get(where)
    if loc is None:
        return list(caller.search(query, quiet=True) or [])
    return list(caller.search(query, location=loc, quiet=True) or [])


def _show_stock_menu(caller, raw, cmdstring, query, where, objs):
    options = [(obj, obj.get_display_name(caller)) for obj in objs]
    cmd_act._PENDING[caller.id] = {"kind": "stock", "raw": raw, "cmdstring": cmdstring,
                                   "query": query, "where": where, "options": options}
    opts = "\n".join(f"  {i}. {label}" for i, (_obj, label) in enumerate(options, 1))
    caller.msg(f"Which {query} do you mean?\n{opts}\n"
               f"Type a number to choose — I'll redo '{raw}' with your pick. (Or rephrase.)")


def stock_pick(caller, pend, n):
    """Resolve a numbered pick from a stock-command menu: re-issue `<cmd> <query>-<index>` with the
    index recomputed against a fresh id-ordered search (stale-safe — a vanished pick degrades to an
    informative message, or a fresh menu when several still match)."""
    obj, label = pend["options"][n - 1]
    fresh = _search(caller, pend["query"], pend["where"])
    if getattr(obj, "pk", None) is None or obj not in fresh:
        caller.msg(f"The {label} isn't there any more.")
        if len(fresh) > 1:
            _show_stock_menu(caller, pend["raw"], pend["cmdstring"], pend["query"],
                             pend["where"], fresh)
        return
    caller.execute_cmd(f"{pend['cmdstring']} {pend['query']}-{fresh.index(obj) + 1}")


def _reach_filter(caller, objs):
    """DR-13a for stock get: (same-zone objs, a representative far obj or None). Unzoned rooms
    filter nothing (the one-zone compat rule)."""
    from typeclasses.worldview import zone_of
    from world.sim.space import zones as zonemap
    room = getattr(caller, "location", None)
    if room is None or not room.db.default_zone or not zonemap.loaded():
        return objs, None
    lzone = zone_of(caller, room)
    same = [o for o in objs if zone_of(o, room) == lzone]
    far = next((o for o in objs if o not in same), None)
    return same, far


def _menu_if_multimatch(cmd, where):
    """Pre-flight for a stock item command. True if handled (menu shown / too-far answered)."""
    caller = cmd.caller
    cmd_act._PENDING.pop(caller.id, None)          # any fresh command supersedes a pending menu
    if not cmd.args:
        return False
    objs = _search(caller, cmd.args, where)
    if where == "room":                            # the reach gate applies to taking, not dropping
        same, far = _reach_filter(caller, objs)
        if not same and far is not None:
            from typeclasses.worldview import zone_of
            from world.sim import narrator
            from world.sim.space import direction, zones as zonemap
            room = caller.location
            dphrase = direction.phrase(zone_of(caller, room), zone_of(far, room)) or "some way off"
            caller.msg(narrator.narrate("reach.too_far",
                                        {"target": far.key, "direction": dphrase, "verb": "take"}))
            return True
        objs = same or objs
        if len(objs) == 1:
            # a single in-reach match among far duplicates: stock search would multimatch on the
            # NAME, so re-issue with the manager's ordinal for exactly this object
            full = _search(caller, cmd.args, where)
            if len(full) > 1:
                caller.execute_cmd(f"{cmd.cmdstring} {cmd.args}-{full.index(objs[0]) + 1}")
                return True
    if len(objs) <= 1:
        return False
    if getattr(cmd, "number", 0) and len({o.key for o in objs}) == 1:
        return False                                # a leading-count stack — stock handles it
    _show_stock_menu(caller, " ".join(cmd.raw_string.split()), cmd.cmdstring, cmd.args, where, objs)
    return True


class CmdGet(DefaultCmdGet):
    __doc__ = DefaultCmdGet.__doc__

    def func(self):
        self.args = _strip_articles(self.args)
        if _menu_if_multimatch(self, "room"):
            return
        super().func()


class CmdDrop(DefaultCmdDrop):
    __doc__ = DefaultCmdDrop.__doc__

    def func(self):
        self.args = _strip_articles(self.args)
        if _menu_if_multimatch(self, "inv"):
            return
        super().func()


class CmdLook(DefaultCmdLook):
    __doc__ = DefaultCmdLook.__doc__

    def func(self):
        # MUD convention (DR-23): `look at X` ≡ `look X` ≡ `examine X` — strip the 'at'.
        self.args = self.args.strip()
        if self.args.lower().startswith("at "):
            self.args = self.args[3:].strip()
        self.args = _strip_articles(self.args)
        if self.args and _menu_if_multimatch(self, "around"):
            return
        super().func()
