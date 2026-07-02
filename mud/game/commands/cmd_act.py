"""game.commands.cmd_act — the taught-grammar action command + the unmatched-input nudge (DR-08, D5).

`CmdAction` is keyed on every operation verb (from the registry); `self.cmdstring` is the matched verb.
It builds a read-only WorldView, parses the line (returning the teaching nudge or a NUMBERED
disambiguation menu as needed), resolves through the pure engine, applies effects via the single
`apply()` writer, sends the first-person narration to the actor, and propagates events to the other
players. `CmdNoMatch` catches anything unmatched: a bare number picks from a pending menu — re-running
the WHOLE original line with that slot pinned (parse `bindings`) — otherwise it teaches the grammar
(never Evennia's "Huh?").
"""
from __future__ import annotations

from dataclasses import replace

from evennia.commands.cmdhandler import CMD_NOMATCH
from evennia.utils import logger

from commands.command import Command
from typeclasses.apply import LedgerError, apply, get_sink
from typeclasses.propagator import propagate
from typeclasses.worldview import EvenniaWorldView
from world.scenarios.whiteout import content
from world.sim.contracts import Disambiguation, ParseError
from world.sim.operations.registry import VERB_TO_OP
from world.sim.parser import parse
from world.sim.resolver import resolve

content.load()                       # install narration templates when the cmdset loads
MATERIALS = content.MATERIALS
_VERBS = sorted(VERB_TO_OP)

_FORMAT = ("VERB thing [RELATION thing] [WITH tool]  — e.g. 'cut the cover off the seat with the "
           "multitool'. Type 'examine <thing>' to see what you can name.")

# Pending numbered disambiguation menus, keyed by caller dbref. EPHEMERAL UI state, deliberately NOT
# a .db/.ndb Attribute — world state changes only via apply() (DR-10); a menu is a question, not a
# fact. One record per caller (a fresh command supersedes it); evaporates on @reload, harmlessly.
_PENDING: dict = {}


def _show_menu(caller, line, disambig, bindings):
    _PENDING[caller.id] = {"kind": "sim", "raw": line, "term": disambig.term,
                           "options": disambig.options, "bindings": dict(bindings or {})}
    opts = "\n".join(f"  {i}. {o.label}" for i, o in enumerate(disambig.options, 1))
    caller.msg(f"Which {disambig.term} do you mean?\n{opts}\n"
               f"Type a number to choose — I'll redo '{line}' with your pick. (Or rephrase.)")


def _run_action(caller, line, bindings=None):
    """Parse → resolve → apply → narrate for a full command line (fresh, or a menu-pick re-run)."""
    room = caller.location
    if room is None:
        caller.msg("You are nowhere in particular.")
        return
    world = EvenniaWorldView(room, caller, seed=(room.db.seed or 0))
    result = parse(line, VERB_TO_OP, world.reachables(), bindings=bindings)

    if isinstance(result, ParseError):
        caller.msg(result.nudge)
        return
    if isinstance(result, Disambiguation):
        _show_menu(caller, line, result, bindings)
        return

    attempt = replace(result, actor=(caller.db.sim_id or caller.key))
    action = resolve(attempt, world, MATERIALS)

    if action.effects:
        try:
            apply(list(action.effects), world, sink=get_sink(room))
        except LedgerError as err:
            logger.log_err(f"[whiteout] ledger rejected: {err}  (line={line!r})")
            caller.msg("Something about that doesn't add up physically. (Logged for the builders.)")
            return

    if action.narration:
        caller.msg(action.narration)
    propagate(room, action.events, caller)


class CmdAction(Command):
    """Do something to the world.

    Usage:
      <verb> <thing> [<relation> <thing>] [with <tool>]

    Examples:
      cut the cover off the seat with the multitool
      pry the panel off the seat
      burn the tinder with the lighter
      examine the seat
    """
    key = _VERBS[0]
    aliases = _VERBS[1:]
    locks = "cmd:all()"
    help_category = "Interaction"

    def func(self):
        _PENDING.pop(self.caller.id, None)         # any fresh command supersedes a pending menu
        line = " ".join(f"{self.cmdstring} {self.args}".split())   # normalized — menus echo this line
        _run_action(self.caller, line)


class CmdNoMatch(Command):
    """Fires on input matching no command — a menu pick (bare number while a numbered disambiguation
    menu is pending) or the grammar nudge. Never Evennia's 'Huh?'."""
    key = CMD_NOMATCH
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        arg = (self.args or "").strip()
        pend = _PENDING.get(caller.id)
        if pend and arg.isdigit():
            n = int(arg)
            if 1 <= n <= len(pend["options"]):
                _PENDING.pop(caller.id, None)
                if pend.get("kind") == "stock":              # a stock get/drop menu (cmd_items)
                    from commands.cmd_items import stock_pick
                    stock_pick(caller, pend, n)
                    return
                o = pend["options"][n - 1]
                bindings = dict(pend["bindings"])
                bindings[pend["term"]] = (o.entity_id, o.part_id)
                _run_action(caller, pend["raw"], bindings)   # the WHOLE line, slot pinned
                return
            caller.msg(f"Pick a number from 1 to {len(pend['options'])}, or retype the command.")
            return
        caller.msg("I don't know how to do that. Try:  " + _FORMAT)
