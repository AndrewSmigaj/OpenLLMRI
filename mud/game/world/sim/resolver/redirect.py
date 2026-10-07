"""world.sim.resolver.redirect — the coarse informative redirect (DR-09, D2). Pure.

When no rule fires, name a few PLAUSIBLE verbs for the target — from each operation's `applies_to`
matched against the target's material tags + part attachment. P1 is coarse by design: precise
smallest-unmet-precondition ranking needs declarative preconditions (the DSL) → P2. Always informative,
never a flat "you can't do that".
"""
from __future__ import annotations

from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import material_of, resolve_ref
from world.sim.operations.registry import OPERATIONS


def generic_redirect(attempt, world, materials) -> ActionResult:
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return ActionResult(Resolution.REDIRECT, narration="You don't see that here.",
                            tier="redirect:no_target")

    tags = set()
    mat = material_of(attempt.X, world, materials)
    if mat is not None:
        tags |= set(mat.tags)
    if part is not None:
        tags.add(part.attachment)

    plausible = [op.id for op in OPERATIONS.values()
                 if op.id != attempt.verb and op.applies_to and (set(op.applies_to) & tags)]
    target = part.id if part else ent.name
    if plausible:
        return ActionResult(Resolution.REDIRECT, tier="redirect:generic",
                            narration=f"You can't {attempt.verb} the {target} like that — but you could "
                                      f"{_or_list(plausible[:3])} it.")
    return ActionResult(Resolution.REDIRECT, tier="redirect:generic",
                        narration=f"Nothing you try seems to affect the {target}.")


def _or_list(items) -> str:
    items = list(items)
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} or {items[1]}"
    return ", ".join(items[:-1]) + f", or {items[-1]}"
