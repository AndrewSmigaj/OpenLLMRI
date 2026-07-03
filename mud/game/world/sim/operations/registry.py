"""world.sim.operations.registry — verb→handler registry + parser metadata (DR-05, functions-first).

This is the seam the DSL extends in P2 (a new handler-producer behind the same `Op` interface). For
now each `Op` binds a canonical id to a pure handler function + the metadata the parser and the
coarse redirect need (`verbs` synonyms, `relations`, `applies_to` tags/attachments).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from world.sim.operations.handlers import (bend, break_op, burn, cut, drink, eat, examine, light, melt,
                                           move, pour, pry, tear, tie, wrap)


@dataclass(frozen=True)
class Op:
    id: str
    verbs: tuple[str, ...]
    handler: Callable                 # resolve_<op>(attempt, world, materials) -> ActionResult | None
    relations: tuple[str, ...] = ()   # relations this op accepts (off, from, …)
    applies_to: tuple[str, ...] = ()  # material tags / attachments the coarse redirect suggests it for (D2)


OPERATIONS: dict[str, Op] = {
    "cut": Op("cut", cut.VERBS, cut.resolve_cut, relations=("off", "from"),
              applies_to=("fabric", "cordage", "flexible", "stitched", "tied", "webbing")),
    "tear": Op("tear", tear.VERBS, tear.resolve_tear, relations=("off", "from"),
               applies_to=("fabric", "flexible", "paper", "stitched", "tied")),
    "burn": Op("burn", burn.VERBS, burn.resolve_burn,
               applies_to=("flammable", "fuel", "tinder", "fabric")),
    "light": Op("light", light.VERBS, light.resolve_light,
                applies_to=("flammable", "tinder", "fuel")),
    "melt": Op("melt", melt.VERBS, melt.resolve_melt,
               applies_to=("frozen_water", "cold", "ice")),
    "pour": Op("pour", pour.VERBS, pour.resolve_pour, relations=("on", "into", "onto"),
               applies_to=("liquid",)),
    "pry": Op("pry", pry.VERBS, pry.resolve_pry, relations=("off", "from", "open"),
              applies_to=("bolted", "wedged", "clipped", "metal", "rigid")),
    "break": Op("break", break_op.VERBS, break_op.resolve_break,
                applies_to=("brittle", "rigid", "glass", "wood")),
    "bend": Op("bend", bend.VERBS, bend.resolve_bend,
               applies_to=("wire", "metal", "synthetic", "flexible")),
    "tie": Op("tie", tie.VERBS, tie.resolve_tie, relations=("to", "between", "around"),
              applies_to=("cordage", "webbing", "wire")),
    "wrap": Op("wrap", wrap.VERBS, wrap.resolve_wrap, relations=("around", "over"),
               applies_to=("fabric", "flexible", "insulating")),
    "drink": Op("drink", drink.VERBS, drink.resolve_drink,
                applies_to=("liquid", "potable")),
    "eat": Op("eat", eat.VERBS, eat.resolve_eat,
              applies_to=("edible", "food")),
    "examine": Op("examine", examine.VERBS, examine.resolve_examine),
    "move": Op("move", move.VERBS, move.resolve_move, relations=("to", "into", "on")),
}

# synonym verb → canonical operation id (feeds the parser's synonym table, P1.5)
VERB_TO_OP: dict[str, str] = {v: op.id for op in OPERATIONS.values() for v in op.verbs}


def handler_for(verb: str):
    """The handler for a (possibly-synonym) verb, or None if the verb is unknown."""
    op_id = VERB_TO_OP.get(verb)
    return OPERATIONS[op_id].handler if op_id else None
