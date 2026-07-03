"""game.commands.cmd_items — stock drop/look with the DR-08a numbered disambiguation menu.

Thin subclasses of Evennia's CmdDrop/CmdLook: a pre-flight quiet search detects a TRUE multimatch
and shows the same numbered menu the taught-grammar commands use; everything else defers to stock.
GET LIVES IN THE TAUGHT GRAMMAR now (the `take` op owns get/grab — DR-24; the old CmdGet subclass
was removed to defuse the CmdSet matchset trap, see containment.md). A pick (a bare number, caught
by the unmatched-input command) re-issues the original command with Evennia's native `name-N`
ordinal, recomputed against the manager's stable id-ordered search at pick time.
`give` is deferred (third use). One pending menu per caller; the latest question wins.

Note: search-lock filtering happens after the manager computes ordinals, so a search-locked object
could in principle desync the re-issue index — no Whiteout content uses search locks (accepted).
"""
from __future__ import annotations

from evennia.commands.default.general import (CmdDrop as DefaultCmdDrop,
                                              CmdInventory as DefaultCmdInventory,
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


def _menu_if_multimatch(cmd, where):
    """Pre-flight for a stock item command. True if handled (menu shown / too-far answered)."""
    caller = cmd.caller
    cmd_act._PENDING.pop(caller.id, None)          # any fresh command supersedes a pending menu
    if not cmd.args:
        return False
    objs = _search(caller, cmd.args, where)
    if len(objs) <= 1:
        return False
    if getattr(cmd, "number", 0) and len({o.key for o in objs}) == 1:
        return False                                # a leading-count stack — stock handles it
    _show_stock_menu(caller, " ".join(cmd.raw_string.split()), cmd.cmdstring, cmd.args, where, objs)
    return True


class CmdDrop(DefaultCmdDrop):
    __doc__ = DefaultCmdDrop.__doc__

    def func(self):
        self.args = _strip_articles(self.args)
        if _menu_if_multimatch(self, "inv"):
            return
        super().func()


class CmdInventory(DefaultCmdInventory):
    __doc__ = DefaultCmdInventory.__doc__

    def func(self):
        """DR-25: carried and worn split, plus the warmth band."""
        caller = self.caller
        items = list(caller.contents)
        if not items:
            caller.msg("You are not carrying anything.")
            return
        from typeclasses.worldview import to_entity_state
        from world.scenarios.whiteout import content
        from world.sim.systems import warmth
        worn_objs = [o for o in items if (o.db.state or {}).get("worn_by")]
        carried = sorted(o.key for o in items if o not in worn_objs)
        lines = []
        if carried:
            lines.append("You are carrying: " + ", ".join(carried) + ".")
        if worn_objs:
            lines.append("Wearing: " + ", ".join(sorted(o.key for o in worn_objs)) + ".")
        worn_ents = [to_entity_state(o) for o in worn_objs]
        band = warmth.warmth_band(warmth.clothing_warmth(worn_ents, content.MATERIALS))
        lines.append(f"You are {band}.")
        caller.msg("\n".join(lines))


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
