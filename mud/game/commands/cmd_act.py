"""game.commands.cmd_act — the taught-grammar action command + the unmatched-input nudge (DR-08, D5).

`CmdAction` is keyed on every operation verb (from the registry); `self.cmdstring` is the matched verb.
It builds a read-only WorldView, parses the line (returning the teaching nudge or a disambiguation list
as needed), resolves through the pure engine, applies effects via the single `apply()` writer, sends the
first-person narration to the actor, and propagates events to the other players. `CmdNoMatch` catches
anything unmatched and teaches the grammar (never Evennia's "Huh?").
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
        caller = self.caller
        room = caller.location
        if room is None:
            caller.msg("You are nowhere in particular.")
            return

        line = f"{self.cmdstring} {self.args}".strip()
        world = EvenniaWorldView(room, caller, seed=(room.db.seed or 0))
        result = parse(line, VERB_TO_OP, world.reachables())

        if isinstance(result, ParseError):
            caller.msg(result.nudge)
            return
        if isinstance(result, Disambiguation):
            opts = "\n".join(f"  - {o.label}   (try: {self.cmdstring} {o.ref})" for o in result.options)
            caller.msg(f"Which {result.term} do you mean?\n{opts}")
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


class CmdNoMatch(Command):
    """Fires on input matching no command — teaches the grammar instead of Evennia's 'Huh?'."""
    key = CMD_NOMATCH
    locks = "cmd:all()"

    def func(self):
        self.caller.msg("I don't know how to do that. Try:  " + _FORMAT)
