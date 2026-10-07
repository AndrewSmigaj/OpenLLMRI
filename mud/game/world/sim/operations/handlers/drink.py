"""world.sim.operations.handlers.drink — the `drink` operation (DR-05). Pure.

`drink X` drinks a potable liquid — the payoff of melting snow. Frozen water can't be drunk (melt it
first → informative redirect). Drinking consumes the liquid (its mass leaves the modeled scene → the
environment sink; the ledger balances it). Returns None if X isn't drinkable at all.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import material_of, prop, resolve_ref

VERBS = ("drink", "sip", "gulp", "swig")


def resolve_drink(attempt, world, materials):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or prop(mat, "potability") <= 0.0:
        return None  # not drinkable → resolver redirects
    if "frozen_water" in mat.tags:
        return ActionResult(Resolution.REDIRECT, tier="op:drink:frozen",
                            narration=narrator.narrate("drink.frozen", {"target": ent.name}))

    tepid = prop(mat, "potability") < 0.5
    template = "drink.risky" if tepid else "drink.slake"
    eff = (effects.consume(ent.id),)
    return ActionResult(Resolution.SUCCESS, effects=eff, tier="op:drink:drink",
                        narration=narrator.narrate(template, {"target": ent.name}))
