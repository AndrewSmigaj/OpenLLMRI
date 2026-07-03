"""world.sim.operations.handlers.read — authored text on things (DR-24 content, §38 clues). Pure.

`read/skim/peruse X`: renders the appearance registry's state-conditioned `read` entry (the
flight manual carries the pencilled GUARD-frequency clue). Paper without authored text reads as
nothing much; everything else falls to the resolver.
"""
from __future__ import annotations

from world.sim import narrator, presentation
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import material_of, resolve_ref

VERBS = ("read", "skim", "peruse")


def resolve_read(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    text = presentation.read_text(ent)
    if text:
        return ActionResult(Resolution.SUCCESS, narration=text, tier="op:read:read")
    mat = material_of(attempt.X, world, materials)
    if mat is not None and ("paper" in mat.tags):
        return ActionResult(Resolution.REDIRECT, tier="op:read:nothing",
                            narration=narrator.narrate("read.nothing_much", {"target": ent.name}))
    return None
