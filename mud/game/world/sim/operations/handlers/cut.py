"""world.sim.operations.handlers.cut — the `cut` operation (DR-05, D12). Pure, functions-first.

`cut X [off Y] [with Z]` cuts *through* X. Outcome is systemic, by X's attachment + material
(D12/DR-05a — the attachment gates HOW the material comes free, never WHETHER):
  - a part on a CUTTABLE attachment (stitched/tied/…) is FREED intact (detached → a loose object);
  - a part on a MECHANICAL attachment (clipped/bolted/…) is HACKED OUT destructively — the blade
    can't beat the fastener, so the material comes away as scraps (mass conserved; the wrecked
    fastener is recorded as a residue state);
  - a part that is INTEGRAL (`fixed`/unknown) refuses with a physical explanation (+ at most one
    sibling near-miss, DR-09a);
  - a standalone thing is DIVIDED into two pieces (conserving mass);
  - a too-dull tool won't bite (informative redirect — the material gate comes FIRST).
Returns None only if `cut` doesn't apply to X at all (e.g. a liquid) — the resolver then redirects.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (CUTTABLE_ATTACH, PRYABLE_ATTACH, attachment_phrase,
                                           capability, derived_id, material_of, prop, resolve_ref,
                                           sibling_hint, tool_phrase)

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
    tool = tool_phrase(attempt.tool, world)

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

    if part is not None and part.attachment in PRYABLE_ATTACH:
        # destructive extraction (DR-05a): the blade defeats the material but not the fastener —
        # the part comes out as scraps; the wrecked fastener is a recorded residue fact (DR-11).
        n = 3
        base = part.mass_g // n
        masses = [base] * (n - 1) + [part.mass_g - base * (n - 1)]
        scrap = f"{part.material}_scrap"
        eff = (effects.remove_part(ent.id, part.id),
               effects.set_attr(ent.id, f"residue_{part.id}", part.attachment)) + tuple(
            effects.create_object(scrap, derived_id(ent.id, f"{part.id}_scrap{i}"),
                                  {"material": part.material, "mass_g": m,
                                   "provenance": [f"hacked from {ent.id}"]})
            for i, m in enumerate(masses))
        ev = (Event(EventKind.IMPACT, ent.id, loudness=0.45,
                    data={"verb": "cut", "part": part.id, "destructive": True}),)
        return ActionResult(
            Resolution.SUCCESS, effects=eff, events=ev, tier="op:cut:hack_out",
            narration=narrator.narrate("cut.hack_out",
                                       {"tool": tool, "part": part.id, "target": ent.name,
                                        "output": scrap.replace("_", " "),
                                        "residue": attachment_phrase(part.attachment, "residue")}),
        )

    if part is not None:  # integral (fixed/unknown attachment) → explain the physics; one near-miss
        def can_cut(p):
            m = materials.get(p.material)
            return (p.attachment in CUTTABLE_ATTACH and m is not None
                    and "cut_resistance" in m.props and edge >= prop(m, "cut_resistance") - _SLACK)
        line = narrator.narrate("cut.integral", {"tool": tool, "part": part.id,
                                                 "why": attachment_phrase(part.attachment)})
        sib = sibling_hint(ent, part, can_cut)
        if sib:
            line += " " + narrator.narrate("hint.sibling",
                                           {"sibling": sib.id,
                                            "sibling_phrase": attachment_phrase(sib.attachment, "hint")})
        return ActionResult(Resolution.REDIRECT, tier="op:cut:integral", narration=line)

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
