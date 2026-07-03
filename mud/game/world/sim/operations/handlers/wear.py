"""world.sim.operations.handlers.wear — clothing (DR-25). Pure.

`wear/don X`: wearability is DERIVED from materials (fabric/flexible/soft/insulating, light
enough, not a fixture/liquid/lunch) — the blanket wears as a cloak, a freed seat cover wraps.
Auto-takes from the floor (transfer LAST, DR-24 rule). `remove/doff/shed X` (and "take X off",
routed from the take handler) puts it back in your hands. Unlimited linear layering v1 —
"wear everything" (tuning surface recorded in DR-25).
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import resolve_ref
from world.sim.systems import warmth

VERBS = ("wear", "don")
SHED_VERBS = ("remove", "doff", "shed")


def resolve_wear(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    st = ent.state or {}
    if st.get("worn_by") == attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:wear:already",
                            narration=narrator.narrate("wear.already", {"target": ent.name}))
    if st.get("worn_by"):
        return ActionResult(Resolution.REDIRECT, tier="op:wear:worn_other",
                            narration=narrator.narrate("wear.worn_other", {"target": ent.name}))
    if not warmth.wearable(ent, materials):
        return ActionResult(Resolution.REDIRECT, tier="op:wear:unwearable",
                            narration=narrator.narrate("wear.unwearable", {"target": ent.name}))
    eff = (effects.set_attr(ent.id, "worn_by", attempt.actor),)
    if st.get("in") != attempt.actor:
        eff = eff + (effects.transfer(ent.id, attempt.actor),)      # auto-take; transfer LAST
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.1, data={"verb": "wear"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:wear:wear",
                        narration=narrator.narrate("wear.wear", {"target": ent.name}))


def resolve_shed(attempt, world, materials, ref=None):
    target = ref or attempt.X or (attempt.Y[0] if attempt.Y else None)
    ent, part = resolve_ref(target, world)
    if ent is None or part is not None:
        return None
    if (ent.state or {}).get("worn_by") != attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:wear:not_worn",
                            narration=narrator.narrate("wear.not_worn", {"target": ent.name}))
    return ActionResult(Resolution.SUCCESS,
                        effects=(effects.set_attr(ent.id, "worn_by", None),),
                        tier="op:wear:shed",
                        narration=narrator.narrate("wear.shed", {"target": ent.name}))
