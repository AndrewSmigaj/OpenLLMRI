"""world.sim.operations.handlers.melt — the `melt` operation (DR-05). Pure.

`melt X [with Z]` turns frozen water (snow/ice) into drinkable water, given heat — the tool's flame OR any
lit thing reachable (melt snow off the fire you just lit). Mass is conserved exactly: the ice is consumed
and an equal mass of water is minted. Returns None if X isn't frozen water at all.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import derived_id, heat_source_available, material_of, resolve_ref

VERBS = ("melt", "thaw")


def resolve_melt(attempt, world, materials):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or "frozen_water" not in mat.tags:
        return None  # nothing meltable here → resolver redirects
    if ent.parts:
        return ActionResult(Resolution.REDIRECT, tier="op:melt:composite",
                            narration=narrator.narrate("melt.composite", {"target": ent.name}))
    if not heat_source_available(attempt, world):
        return ActionResult(Resolution.REDIRECT, tier="op:melt:no_heat",
                            narration=narrator.narrate("melt.no_heat", {"target": ent.name}))

    eff = (
        effects.consume(ent.id),
        effects.create_object("water", derived_id(ent.id, "melt"),
                              {"material": "water", "mass_g": ent.mass_g,
                               "provenance": [f"melted {ent.id}"]}),
    )
    ev = (Event(EventKind.FIRE_STATE_CHANGE, ent.id, loudness=0.1, data={"verb": "melt"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:melt:water",
                        narration=narrator.narrate("melt.water", {"target": ent.name}))
