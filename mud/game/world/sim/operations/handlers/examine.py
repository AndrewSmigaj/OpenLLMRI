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
    line = presentation.describe(ent)
    if attempt.X is not None and attempt.X.entity_id == attempt.actor:
        from world.sim.systems import warmth                     # DR-25: the self-view
        worn = [e for e in (world.get(i) for i in world.reachable(attempt.actor))
                if e is not None and (e.state or {}).get("worn_by") == attempt.actor]
        line = f"{line} {warmth.worn_summary(worn, materials)}"
    return ActionResult(Resolution.SUCCESS, narration=line, tier="op:examine")
