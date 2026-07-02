"""world.sim.operations.handlers.cut — the `cut` operation (DR-05, D12). Pure, functions-first.

`cut X [off Y] [with Z]` cuts *through* X. Outcome is systemic, by X's attachment + material (D12):
  - a part on a CUTTABLE attachment (stitched/tied/…) is FREED (detached → a loose object);
  - a part on a non-cuttable attachment (bolted/…) is slashed but NOT freed (informative redirect);
  - a standalone thing is DIVIDED into two pieces (conserving mass);
  - a too-dull tool skates off (informative redirect).
Returns None only if `cut` doesn't apply to X at all (e.g. a liquid) — the resolver then redirects.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (CUTTABLE_ATTACH, capability, derived_id, material_of,
                                           name_of, prop, resolve_ref)

VERBS = ("cut", "saw", "slice", "sever", "slash")
_SLACK = 0.1  # a tool slightly under the resistance still bites (graded, not a hard cliff)


def resolve_cut(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or "cut_resistance" not in mat.props:
        return None  # nothing cuttable here (e.g. water) → let the resolver redirect
    resistance = prop(mat, "cut_resistance")
    edge = capability(attempt.tool, world, "edge")            # 0.0 = bare hands
    tool = name_of(attempt.tool, world) or "your bare hands"

    if edge < resistance - _SLACK:
        return ActionResult(
            Resolution.REDIRECT, tier="op:cut:too_dull",
            narration=narrator.narrate("cut.too_dull",
                                       {"tool": tool, "target": part.id if part else ent.name}),
        )

    if part is not None and part.attachment in CUTTABLE_ATTACH:
        output = part.outputs_when_removed[0] if part.outputs_when_removed else f"loose_{part.material}"
        eff = (
            effects.remove_part(ent.id, part.id),
            effects.create_object(output, derived_id(ent.id, part.id),
                                  {"material": part.material, "mass_g": part.mass_g,
                                   "provenance": [f"cut from {ent.id}"]}),
        )
        ev = (Event(EventKind.IMPACT, ent.id, loudness=0.35, data={"verb": "cut", "part": part.id}),)
        return ActionResult(
            Resolution.SUCCESS, effects=eff, events=ev, tier="op:cut:free",
            narration=narrator.narrate("cut.free", {"tool": tool, "target": ent.name, "part": part.id,
                                                    "output": output.replace("_", " ")}),
        )

    if part is not None:  # cuttable material but a non-cuttable attachment → slash, don't free
        return ActionResult(
            Resolution.REDIRECT, tier="op:cut:slash_fixed",
            narration=narrator.narrate("cut.slash_fixed",
                                       {"tool": tool, "part": part.id, "attachment": part.attachment}),
        )

    # standalone thing → divide into two pieces (mass conserved: a + b == original)
    mat_id = ent.materials[0] if ent.materials else "material"
    a = ent.mass_g // 2
    b = ent.mass_g - a
    eff = (
        effects.consume(ent.id),
        effects.create_object(f"{mat_id}_piece", derived_id(ent.id, "a"),
                              {"material": mat_id, "mass_g": a, "provenance": [f"cut from {ent.id}"]}),
        effects.create_object(f"{mat_id}_piece", derived_id(ent.id, "b"),
                              {"material": mat_id, "mass_g": b, "provenance": [f"cut from {ent.id}"]}),
    )
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.3, data={"verb": "cut"}),)
    return ActionResult(
        Resolution.SUCCESS, effects=eff, events=ev, tier="op:cut:divide",
        narration=narrator.narrate("cut.divide", {"tool": tool, "target": ent.name}),
    )
