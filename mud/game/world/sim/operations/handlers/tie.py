"""world.sim.operations.handlers.tie — the `tie` operation (DR-05). Pure. Two-object.

`tie X to Y` (or `tie Y with X`) binds cordage to an anchor — the basis of every makeshift rig (a strap,
a splint, a lashed frame, a snare). The cord is X if X is cordage, else the tool. A tie is a STATE change
(`tied_to` / `secured`), mass unchanged. Returns None if there's nothing cordage-like to tie with.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import material_of, resolve_ref

VERBS = ("tie", "lash", "fasten", "bind", "secure", "knot")
_CORDAGE = frozenset({"cordage", "webbing", "wire"})


def _is_cordage(ref, world, materials):
    mat = material_of(ref, world, materials)
    return mat is not None and bool(set(mat.tags) & _CORDAGE)


def resolve_tie(attempt, world, materials):
    x_ent, _ = resolve_ref(attempt.X, world)
    if x_ent is None:
        return None

    if _is_cordage(attempt.X, world, materials):
        cord_ent, anchor_ref = x_ent, (attempt.Y[0] if attempt.Y else None)
    elif attempt.tool is not None and _is_cordage(attempt.tool, world, materials):
        cord_ent, anchor_ref = resolve_ref(attempt.tool, world)[0], attempt.X
    else:
        return None  # nothing to tie with → resolver redirects

    anchor_ent, _ = resolve_ref(anchor_ref, world)
    if anchor_ent is None:
        return ActionResult(Resolution.REDIRECT, tier="op:tie:no_anchor",
                            narration=narrator.narrate("tie.no_anchor", {"cord": cord_ent.name}))

    eff = (effects.set_attr(cord_ent.id, "tied_to", anchor_ent.id),
           effects.set_attr(anchor_ent.id, "secured", True))
    ev = (Event(EventKind.IMPACT, cord_ent.id, loudness=0.1, data={"verb": "tie"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:tie:knot",
                        narration=narrator.narrate("tie.knot", {"cord": cord_ent.name,
                                                                "anchor": anchor_ent.name}))
