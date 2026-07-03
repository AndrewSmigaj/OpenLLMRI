"""world.sim.operations.handlers.pry — the `pry` operation (DR-05, D12). Pure.

`pry X [off Y] [with Z]` frees a part held by a PRYABLE attachment if the tool gives enough leverage.
The resistance is set by the ATTACHMENT (a clip pops easily; a bolt really wants a wrench), not the
part's material stiffness — the attachment is what holds it. Pry is the ONLY way to remove a part
INTACT off a mechanical fastener (cut/tear extract destructively, DR-05a). A non-pryable part gets a
physical explanation + at most one sibling near-miss (DR-09a); a whole-entity pry returns None → the
resolver redirects. (Attachment difficulties are tunable content.)
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (PRYABLE_ATTACH, attachment_phrase, capability,
                                           derived_id, resolve_ref, sibling_hint, tool_phrase)

VERBS = ("pry", "lever", "wrench", "force")
_SLACK = 0.1
_ATTACH_DIFFICULTY = {          # how much leverage each attachment demands
    "clipped": 0.3, "pinned": 0.4, "wedged": 0.45, "nailed": 0.5, "screwed": 0.6, "bolted": 0.8,
}


def resolve_pry(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    if part is None:
        st = ent.state or {}
        if st.get("jammed"):                       # DR-24: a buckled lid is exactly a pry's job
            leverage = capability(attempt.tool, world, "leverage")
            tool = tool_phrase(attempt.tool, world)
            if leverage >= 0.5 - _SLACK:
                eff = (effects.set_attr(ent.id, "jammed", False),
                       effects.set_attr(ent.id, "open", True))
                ev = (Event(EventKind.IMPACT, ent.id, loudness=0.55, data={"verb": "pry"}),)
                return ActionResult(Resolution.SUCCESS, effects=eff, events=ev,
                                    tier="op:pry:open",
                                    narration=narrator.narrate("pry.open",
                                                               {"tool": tool, "target": ent.name}))
            return ActionResult(Resolution.REDIRECT, tier="op:pry:no_leverage",
                                narration=narrator.narrate("pry.no_leverage",
                                                           {"tool": tool, "part": ent.name}))
        return None  # whole-entity pry → let the resolver redirect

    leverage = capability(attempt.tool, world, "leverage")

    if part.attachment not in PRYABLE_ATTACH:
        # nothing mechanical to lever against → explain the physics; one near-miss (DR-09a)
        def can_pry(p):
            return (p.attachment in PRYABLE_ATTACH
                    and leverage >= _ATTACH_DIFFICULTY.get(p.attachment, 0.5) - _SLACK)
        line = narrator.narrate("pry.no_purchase", {"part": part.id,
                                                    "why": attachment_phrase(part.attachment)})
        sib = sibling_hint(ent, part, can_pry)
        if sib:
            line += " " + narrator.narrate("hint.sibling",
                                           {"sibling": sib.id,
                                            "sibling_phrase": attachment_phrase(sib.attachment, "hint")})
        return ActionResult(Resolution.REDIRECT, tier="op:pry:no_purchase", narration=line)

    hold = _ATTACH_DIFFICULTY.get(part.attachment, 0.5)
    tool = tool_phrase(attempt.tool, world)

    if leverage < hold - _SLACK:
        return ActionResult(Resolution.REDIRECT, tier="op:pry:no_leverage",
                            narration=narrator.narrate("pry.no_leverage", {"tool": tool, "part": part.id}))

    output = part.outputs_when_removed[0] if part.outputs_when_removed else f"loose_{part.material}"
    eff = (
        effects.remove_part(ent.id, part.id),
        effects.create_object(output, derived_id(ent.id, part.id),
                              {"material": part.material, "mass_g": part.mass_g,
                               "provenance": [f"pried from {ent.id}"]}),
    )
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.5, data={"verb": "pry", "part": part.id}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:pry:free",
                        narration=narrator.narrate("pry.free", {"tool": tool, "target": ent.name,
                                                                "part": part.id,
                                                                "output": output.replace("_", " ")}))
