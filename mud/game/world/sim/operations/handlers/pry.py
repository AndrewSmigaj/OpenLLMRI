"""world.sim.operations.handlers.pry — the `pry` operation (DR-05, D12). Pure.

`pry X [off Y] [with Z]` frees a part held by a PRYABLE attachment if the tool gives enough leverage.
The resistance is set by the ATTACHMENT (a clip pops easily; a bolt really wants a wrench), not the
part's material stiffness — the attachment is what holds it. Returns None if X isn't a pryable part →
the resolver redirects. (Attachment difficulties are tunable content.)
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (PRYABLE_ATTACH, capability, derived_id, name_of,
                                           resolve_ref)

VERBS = ("pry", "lever", "wrench", "force")
_SLACK = 0.1
_ATTACH_DIFFICULTY = {          # how much leverage each attachment demands
    "clipped": 0.3, "pinned": 0.4, "wedged": 0.45, "nailed": 0.5, "screwed": 0.6, "bolted": 0.8,
}


def resolve_pry(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    if part is None or part.attachment not in PRYABLE_ATTACH:
        return None  # nothing pryable here → let the resolver redirect

    hold = _ATTACH_DIFFICULTY.get(part.attachment, 0.5)
    leverage = capability(attempt.tool, world, "leverage")
    tool = name_of(attempt.tool, world) or "your bare hands"

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
