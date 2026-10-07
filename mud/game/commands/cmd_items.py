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


# --- scene-space placement (DR-24 / scene-spaces): drop into a space; look at a space -------------
_PLACE_RELATIONS = (" onto ", " into ", " on ", " in ")


def _current_zone(caller):
    """The caller's zone, or None in an unzoned world / before zones load."""
    room = getattr(caller, "location", None)
    if room is None or not getattr(room.db, "default_zone", None):
        return None
    from typeclasses.worldview import zone_of
    from world.sim.space import zones as zonemap
    return zone_of(caller, room) if zonemap.loaded() else None


def _space_names(zone):
    """The zone's spaces as a friendly 'the A, the B or the C' (primary aliases), for the drop ask."""
    from world.sim.space import spaces as spacemap
    names = [(sp.aliases[0] if sp.aliases else sp.id.replace("_", " "))
             for sp in spacemap.for_zone(zone)]
    if not names:
        return ""
    if len(names) == 1:
        return f"the {names[0]}"
    return "the " + ", the ".join(names[:-1]) + f" or the {names[-1]}"


def _split_place(caller, args, zone):
    """Parse a trailing 'on/in <space>' off a drop → (space_id, object_args, ask_message):
    a resolved placement → (sid, 'X', None); a place named but unknown here → (None, 'X', an ask
    listing the spaces); no place named, or the word is part of the object → (None, args, None)."""
    if not zone:
        return None, args, None
    from world.sim.space import spaces as spacemap
    low = args.lower()
    for rel in _PLACE_RELATIONS:
        idx = low.rfind(rel)
        if idx == -1:
            continue
        head, tail = args[:idx].strip(), _strip_articles(args[idx + len(rel):])
        if not head or not tail or not _search(caller, head, "inv"):
            continue                               # the word is part of the object name, not a place
        sid = spacemap.resolve_space(zone, tail)
        if sid:
            return sid, head, None
        names = _space_names(zone)
        ask = f'There\'s nowhere called "{tail}" here.' + (f" You could set it {names}." if names else "")
        return None, head, ask
    return None, args, None


def _place_in_space(caller, objs, zone, sid):
    """Override freshly-dropped objects' space to `sid` via a set_attr Effect, and confirm."""
    if not objs:
        return
    from typeclasses.apply import apply as apply_effects
    from typeclasses.worldview import EvenniaWorldView
    from world.sim import effects
    from world.sim.space import spaces as spacemap
    room = caller.location
    world = EvenniaWorldView(room, caller, seed=(getattr(room.db, "seed", 0) or 0))
    apply_effects([effects.set_attr(o.db.sim_id or o.key, "space", sid) for o in objs], world)
    sp = spacemap.get(zone, sid)
    where = sp.aliases[0] if sp and sp.aliases else sid.replace("_", " ")
    caller.msg(f"You set {', '.join(o.key for o in objs)} down on the {where}.")


def _look_space(caller, phrase):
    """`look at <space>`: render the named space UNCAPPED. True if `phrase` was a space (handled)."""
    room = getattr(caller, "location", None)
    zone = _current_zone(caller)
    if zone is None or room is None:
        return False
    from typeclasses.worldview import to_entity_state, zone_of
    from world.sim import presentation
    ents = []
    for o in room.filter_visible(room.contents_get(content_type="object"), caller):
        if zone_of(o, room) == zone:
            e = to_entity_state(o)
            e.state["zone"] = zone
            ents.append(e)
    text = presentation.look_space(zone, phrase, ents)
    if text is None:
        return False
    caller.msg(text)
    return True


class CmdDrop(DefaultCmdDrop):
    __doc__ = DefaultCmdDrop.__doc__

    def func(self):
        self.args = _strip_articles(self.args)
        zone = _current_zone(self.caller)
        sid, obj_args, ask = _split_place(self.caller, self.args, zone)
        if ask:
            self.caller.msg(ask)
            return
        self.args = obj_args
        if _menu_if_multimatch(self, "inv"):
            return
        room = self.caller.location
        before = set(room.contents) if room else set()
        super().func()                             # stock drop → at_drop sets zone + default space
        if sid and room:
            _place_in_space(self.caller, [o for o in room.contents if o not in before], zone, sid)


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
        if self.args:
            if _menu_if_multimatch(self, "around"):
                return
            if not _search(self.caller, self.args, "around"):
                # stock search can't see spaces, zone nouns, or revealed-container contents. A space
                # name renders that space uncapped; else the sim examine path (which sees zone nouns
                # + revealed contents — look at X ≡ examine X holds everywhere, DR-23/DR-24).
                if _look_space(self.caller, self.args):
                    return
                cmd_act._run_action(self.caller, f"examine {self.args}")
                return
        super().func()
