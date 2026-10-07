"""world.sim.operations.handlers.eat — the `eat` operation (DR-05). Pure.

`eat X` eats something edible — the food half of the survival loop (drink is the other). Governed by the
material's `edibility`; eating consumes it (mass leaves the modeled scene → the environment sink, ledger
balanced). Returns None if X isn't edible at all, so the resolver redirects.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import material_of, prop, resolve_ref

VERBS = ("eat", "bite", "chew", "devour")


def resolve_eat(attempt, world, materials):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or prop(mat, "edibility") <= 0.0:
        return None  # not edible → resolver redirects
    meagre = prop(mat, "edibility") < 0.5
    template = "eat.meagre" if meagre else "eat.eat"
    return ActionResult(Resolution.SUCCESS, effects=(effects.consume(ent.id),), tier="op:eat:eat",
                        narration=narrator.narrate(template, {"target": ent.name}))
