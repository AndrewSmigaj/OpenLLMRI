"""world.sim.operations.handlers.light — the `light` operation (DR-05). Pure.

`light X [with Z]` sets a flammable thing ALIGHT so it becomes a flame/heat source (a STATE change,
`lit=True`) — distinct from `burn`, which consumes a thing in a fire. This is what starts a fire: light
the tinder with the lighter, and the lit tinder can then ignite `burn`, warm a `melt`, or be `pour`-doused.
Needs a spark (an ignition tool or an already-lit thing); returns None if X isn't flammable at all.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import has_ignition, material_of, prop, resolve_ref

VERBS = ("light", "kindle", "spark", "strike")


def resolve_light(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or prop(mat, "burnability") <= 0.0:
        return None  # nothing to set alight → resolver redirects
    target = part.id if part else ent.name

    if (ent.state or {}).get("lit"):
        return ActionResult(Resolution.REDIRECT, tier="op:light:already",
                            narration=narrator.narrate("light.already", {"target": target}))
    if not has_ignition(attempt.tool, world):
        return ActionResult(Resolution.REDIRECT, tier="op:light:no_spark",
                            narration=narrator.narrate("light.no_spark", {"target": target}))
    if prop(mat, "ignition_difficulty") >= 0.85:
        return ActionResult(Resolution.REDIRECT, tier="op:light:wont_catch",
                            narration=narrator.narrate("light.wont_catch", {"target": target}))

    eff = (effects.set_attr(ent.id, "lit", True),)
    ev = (Event(EventKind.FIRE_STATE_CHANGE, ent.id, loudness=0.2, data={"verb": "light"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:light:lit",
                        narration=narrator.narrate("light.lit", {"target": target}))
