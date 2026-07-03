"""world.sim.operations.handlers.examine — inspect an object (D10, DR-23). Pure.

`examine X` (≡ `look at X` — the shell's `return_appearance` delegates to the SAME renderer) shows
`presentation.describe`: authored state-conditioned prose, the systemic condition, and the PARTS
woven as physical sentences **with their names intact** (so a player can reference them). Returns a
SUCCESS description with no effects. The `detail` arg is the perception context — always 'full' in
P1; DR-13 later supplies a band-limited context here WITHOUT changing the signature.
"""
from __future__ import annotations

from world.sim import presentation
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import resolve_ref

VERBS = ("examine", "inspect", "x", "study", "check")


def resolve_examine(attempt, world, materials, detail: str = "full"):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    return ActionResult(Resolution.SUCCESS, narration=presentation.describe(ent),
                        tier="op:examine")
