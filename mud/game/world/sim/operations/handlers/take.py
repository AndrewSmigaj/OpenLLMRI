"""world.sim.operations.handlers.take — acquire and stow things (DR-24). Pure.

`take/get/grab/collect X [from Y]`: a loose thing in reach transfers to your hands. Contents of
unrevealed containers never even parse (the pool walk hides them), so reaching here means the
thing is honestly available. Parts stay attached (cut/pry/tear them free); the worn-by-the-living,
the fixed, and the very heavy refuse honestly; a dead wearer can be stripped (the dignity lives in
the template). `put/stow X into Y` is the other half. TRANSFER effects go LAST in every tuple
(DR-24 rollback rule).
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import attachment_phrase, resolve_ref

VERBS = ("take", "get", "grab", "collect")
PUT_VERBS = ("put", "stow", "stash")
_MAX_CARRY_G = 12_000


def resolve_take(attempt, world, materials):
    ref = attempt.X or (attempt.Y[0] if attempt.Y else None)
    ent, part = resolve_ref(ref, world)
    if ent is None:
        return None
    if part is not None:
        return ActionResult(Resolution.REDIRECT, tier="op:take:attached",
                            narration=narrator.narrate("take.attached",
                                                       {"part": part.id,
                                                        "why": attachment_phrase(part.attachment,
                                                                                 "hint")}))
    st = ent.state or {}
    if ent.id == attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:take:self",
                            narration=narrator.narrate("take.self", {}))
    if st.get("worn_by") == attempt.actor:
        if attempt.relation == "off":
            try:                                                 # "take off X" = shed (DR-25)
                from world.sim.operations.handlers import wear as wear_mod
                return wear_mod.resolve_shed(attempt, world, materials, ref=ref)
            except ImportError:
                pass
        return ActionResult(Resolution.REDIRECT, tier="op:take:worn_self",
                            narration=narrator.narrate("take.worn_self", {"target": ent.name}))
    if st.get("in") == attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:take:already",
                            narration=narrator.narrate("take.already", {"target": ent.name}))
    wearer_id = st.get("worn_by")
    if wearer_id:
        wearer = world.get(wearer_id)
        if wearer is not None and not (wearer.state or {}).get("dead"):
            return ActionResult(Resolution.REDIRECT, tier="op:take:worn_other",
                                narration=narrator.narrate("take.worn_other",
                                                           {"target": ent.name,
                                                            "wearer": wearer.name}))
        eff = (effects.set_attr(ent.id, "worn_by", None),
               effects.transfer(ent.id, attempt.actor))
        ev = (Event(EventKind.IMPACT, ent.id, loudness=0.15, data={"verb": "take"}),)
        return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:take:strip",
                            narration=narrator.narrate("take.strip_dead", {"target": ent.name}))
    if st.get("fixed"):
        return ActionResult(Resolution.REDIRECT, tier="op:take:fixed",
                            narration=narrator.narrate("take.fixed", {"target": ent.name}))
    total = ent.mass_g + sum(p.mass_g for p in ent.parts)
    if total > _MAX_CARRY_G:
        return ActionResult(Resolution.REDIRECT, tier="op:take:too_heavy",
                            narration=narrator.narrate("take.too_heavy", {"target": ent.name}))
    container = world.get(st["in"]) if st.get("in") else None
    eff = (effects.transfer(ent.id, attempt.actor),)
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.15, data={"verb": "take"}),)
    if container is not None:
        line = narrator.narrate("take.from", {"target": ent.name, "container": container.name})
    else:
        line = narrator.narrate("take.take", {"target": ent.name})
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:take:take",
                        narration=line)


def resolve_put(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    st = ent.state or {}
    dest_ref = attempt.Y[0] if attempt.Y else None
    dest, _ = resolve_ref(dest_ref, world) if dest_ref is not None else (None, None)
    if st.get("in") != attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:put:not_held",
                            narration=narrator.narrate("put.not_held", {"target": ent.name}))
    if st.get("worn_by") == attempt.actor:
        return ActionResult(Resolution.REDIRECT, tier="op:put:worn",
                            narration=narrator.narrate("put.worn", {"target": ent.name}))
    if dest is None:
        return ActionResult(Resolution.REDIRECT, tier="op:put:where",
                            narration=narrator.narrate("put.where", {"target": ent.name}))
    dst = dest.state or {}
    if not dst.get("container"):
        return ActionResult(Resolution.REDIRECT, tier="op:put:not_container",
                            narration=narrator.narrate("put.not_container", {"dest": dest.name}))
    if dst.get("jammed") or ("open" in dst and not dst.get("open")):
        return ActionResult(Resolution.REDIRECT, tier="op:put:shut",
                            narration=narrator.narrate("put.shut", {"dest": dest.name}))
    eff = (effects.transfer(ent.id, dest.id),)
    return ActionResult(Resolution.SUCCESS, effects=eff, tier="op:put:into",
                        narration=narrator.narrate("put.into",
                                                   {"target": ent.name, "dest": dest.name}))
