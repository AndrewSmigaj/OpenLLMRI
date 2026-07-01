"""world.sim.operations.handlers.burn — the `burn` operation (DR-05). Pure.

`burn X [with Z]` needs a flammable target and an ignition source (a lit tool / the scene's
fire-makings). Consumes the target → ash, with the rest of the mass leaving as smoke/heat to the
environment sink (the ledger balances it, DR-11). Returns None if X won't burn at all.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import derived_id, material_of, prop, resolve_ref

VERBS = ("burn", "ignite", "torch")
_ASH_FRACTION = 0.15   # ~15% of mass remains as ash; the rest → smoke/heat to the sink (DR-11)


def resolve_burn(attempt, world, materials):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or prop(mat, "burnability") <= 0.0:
        return None  # won't burn → let the resolver redirect

    if not _has_flame(attempt.tool, world):
        return ActionResult(Resolution.REDIRECT, tier="op:burn:no_flame",
                            narration=narrator.narrate("burn.no_flame", {"target": ent.name}))
    if prop(mat, "ignition_difficulty") >= 0.85 and prop(mat, "burnability") < 0.7:
        return ActionResult(Resolution.REDIRECT, tier="op:burn:wont_catch",
                            narration=narrator.narrate("burn.wont_catch", {"target": ent.name}))

    ash_mass = int(ent.mass_g * _ASH_FRACTION)
    eff = (
        effects.consume(ent.id),
        effects.create_object("ash", derived_id(ent.id, "ash"),
                              {"material": "ash", "mass_g": ash_mass, "provenance": [f"burned {ent.id}"]}),
    )
    ev = (Event(EventKind.FIRE_STATE_CHANGE, ent.id, loudness=0.4, data={"verb": "burn"}),)
    smoke = "acrid black smoke" if prop(mat, "smoke_toxicity") >= 0.7 else "thin pale smoke"
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:burn:success",
                        narration=narrator.narrate("burn.success", {"target": ent.name, "smoke": smoke}))


def _has_flame(tool_ref, world) -> bool:
    """A flame is present if the tool provides ignition (a lit/ignition state or tag). Bare hands don't."""
    ent, _ = resolve_ref(tool_ref, world)
    if ent is None:
        return False
    st = ent.state or {}
    return bool(st.get("lit") or st.get("ignition")) or "ignition" in ent.tags or "lit" in ent.tags
