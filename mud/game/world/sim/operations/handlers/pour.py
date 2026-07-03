"""world.sim.operations.handlers.pour — the `pour` operation (DR-05). Pure. Two-object.

`pour X on/onto/into Y` pours a liquid X onto a target Y:
  - Y is on fire and X extinguishes (water) → DOUSES it (Y `lit=False`); the water runs off/steams away
    (consumed to the environment sink — the ledger balances it);
  - otherwise X WETS Y (Y `wet=True`), the water leaving the scene.
Returns None if X isn't a pourable liquid. If there's no Y, it's an informative redirect ("on what?").
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import material_of, resolve_ref

VERBS = ("pour", "tip", "douse", "splash")


def resolve_pour(attempt, world, materials):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or "liquid" not in mat.tags:
        return None  # not a pourable liquid → resolver redirects
    if (ent.state or {}).get("sealed"):            # DR-24: a capped can pours nothing
        return ActionResult(Resolution.REDIRECT, tier="op:pour:sealed",
                            narration=narrator.narrate("pour.sealed", {"target": ent.name}))

    y_ref = attempt.Y[0] if attempt.Y else None
    y_ent, _ = resolve_ref(y_ref, world)
    if y_ent is None:
        return ActionResult(Resolution.REDIRECT, tier="op:pour:no_target",
                            narration=narrator.narrate("pour.no_target", {"liquid": ent.name}))

    yst = y_ent.state or {}
    if (yst.get("lit") or yst.get("burning")) and "extinguisher" in mat.tags:
        eff = (effects.set_attr(y_ent.id, "lit", False), effects.consume(ent.id))
        ev = (Event(EventKind.FIRE_STATE_CHANGE, y_ent.id, loudness=0.35, data={"verb": "douse"}),)
        return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:pour:douse",
                            narration=narrator.narrate("pour.douse", {"liquid": ent.name,
                                                                      "target": y_ent.name}))
    eff = (effects.set_attr(y_ent.id, "wet", True), effects.consume(ent.id))
    return ActionResult(Resolution.SUCCESS, effects=eff, tier="op:pour:wet",
                        narration=narrator.narrate("pour.wet", {"liquid": ent.name, "target": y_ent.name}))
