"""world.sim.operations.handlers.wrap — the `wrap` operation (DR-05). Pure. Two-object.

`wrap X around Y` (or `wrap Y with X`) wraps a flexible/insulating material around a target — a bandage on
a wound, a blanket for warmth, padding on a grip. The wrapper is X if X is wrappable, else the tool. A wrap
is a STATE change (`wrapped`, plus `insulated` if the wrapper insulates), mass unchanged. Returns None if
there's nothing wrappable involved.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import material_of, prop, resolve_ref

VERBS = ("wrap", "bandage", "insulate", "swaddle")
_WRAPPABLE = frozenset({"fabric", "flexible", "insulating"})


def _is_wrappable(ref, world, materials):
    mat = material_of(ref, world, materials)
    return mat is not None and bool(set(mat.tags) & _WRAPPABLE)


def resolve_wrap(attempt, world, materials):
    x_ent, _ = resolve_ref(attempt.X, world)
    if x_ent is None:
        return None

    if _is_wrappable(attempt.X, world, materials):
        wrap_ref, wrap_ent, target_ref = attempt.X, x_ent, (attempt.Y[0] if attempt.Y else None)
    elif attempt.tool is not None and _is_wrappable(attempt.tool, world, materials):
        wrap_ref = attempt.tool
        wrap_ent, target_ref = resolve_ref(attempt.tool, world)[0], attempt.X
    else:
        return None  # nothing wrappable → resolver redirects

    target_ent, _ = resolve_ref(target_ref, world)
    if target_ent is None:
        return ActionResult(Resolution.REDIRECT, tier="op:wrap:no_target",
                            narration=narrator.narrate("wrap.no_target", {"wrap": wrap_ent.name}))

    mat = material_of(wrap_ref, world, materials)
    insulating = mat is not None and ("insulating" in mat.tags or prop(mat, "insulation") >= 0.5)
    eff = [effects.set_attr(target_ent.id, "wrapped", True)]
    if insulating:
        eff.append(effects.set_attr(target_ent.id, "insulated", True))
    ev = (Event(EventKind.IMPACT, target_ent.id, loudness=0.05, data={"verb": "wrap"}),)
    template = "wrap.insulate" if insulating else "wrap.wrapped"
    return ActionResult(Resolution.SUCCESS, effects=tuple(eff), events=ev, tier="op:wrap:wrapped",
                        narration=narrator.narrate(template, {"wrap": wrap_ent.name,
                                                              "target": target_ent.name}))
