"""world.sim.operations.handlers.bend — the `bend` operation (DR-05). Pure.

`bend X` reshapes something ductile (wire, thin metal, plastic) — it takes a SET (a hook, a straightened
antenna). Governed by bend_resistance: too stiff (steel, glass) resists → redirect; a pure fabric or a
liquid has no shape to take → None. A successful bend is a STATE change (`shape`), mass unchanged — which
is what makes wire into a hook, a lever, a splint, an antenna.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import material_of, prop, resolve_ref

VERBS = ("bend", "fold", "straighten", "twist", "curl")
_HAND_BEND = 0.6   # bare hands can bend up to ~'high' resistance with effort
_SLACK = 0.1


def resolve_bend(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or "bend_resistance" not in mat.props:
        return None  # no bend axis (liquid, snow) → resolver redirects
    tags = set(mat.tags)
    if "flexible" in tags and "rigidity" not in mat.props and "wire" not in tags:
        return None  # a pure fabric just flops; there's no shape to bend into

    resistance = prop(mat, "bend_resistance")
    target = part.id if part else ent.name
    if resistance > _HAND_BEND + _SLACK:
        return ActionResult(Resolution.REDIRECT, tier="op:bend:too_stiff",
                            narration=narrator.narrate("bend.too_stiff", {"target": target}))

    eff = (effects.set_attr(ent.id, "shape", "bent"),)
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.15, data={"verb": "bend"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:bend:shaped",
                        narration=narrator.narrate("bend.shaped", {"target": target}))
