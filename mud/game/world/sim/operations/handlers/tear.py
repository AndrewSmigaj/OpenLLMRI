"""world.sim.operations.handlers.tear — the `tear` operation (DR-05). Pure.

`tear X [off Y]` tears X apart by hand (no tool needed). Governed by the material's tear_resistance vs
the force bare hands can apply: a weak/flexible material tears — a part on a tearable attachment is
FREED, a standalone sheet is torn into STRIPS (conserving mass); a tough material won't tear (redirect →
try cutting). Returns None if X has no tear axis at all (metal, liquid) so the resolver redirects.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (CUTTABLE_ATTACH, PRYABLE_ATTACH, attachment_phrase,
                                           derived_id, material_of, prop, resolve_ref,
                                           sibling_hint)

VERBS = ("tear", "rip", "shred")
_HAND_FORCE = 0.45   # what bare hands can tear through (fabric/paper), a shade above 'low'
_SLACK = 0.1


def resolve_tear(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None or "tear_resistance" not in mat.props:
        return None  # nothing tearable here (metal, liquid) → resolver redirects
    resistance = prop(mat, "tear_resistance")
    target = part.id if part else ent.name

    if resistance > _HAND_FORCE + _SLACK:
        return ActionResult(Resolution.REDIRECT, tier="op:tear:too_tough",
                            narration=narrator.narrate("tear.too_tough", {"target": target}))

    if part is not None and part.attachment in CUTTABLE_ATTACH:
        output = part.outputs_when_removed[0] if part.outputs_when_removed else f"loose_{part.material}"
        eff = (
            effects.remove_part(ent.id, part.id),
            effects.create_object(output, derived_id(ent.id, part.id),
                                  {"material": part.material, "mass_g": part.mass_g,
                                   "provenance": [f"torn from {ent.id}"]}),
        )
        ev = (Event(EventKind.IMPACT, ent.id, loudness=0.25, data={"verb": "tear", "part": part.id}),)
        return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:tear:free",
                            narration=narrator.narrate("tear.free", {"target": ent.name, "part": part.id,
                                                                     "output": output.replace("_", " ")}))
    if part is not None and part.attachment in PRYABLE_ATTACH:
        # destructive extraction (DR-05a): hands beat the material but not the fastener — the
        # part comes out in torn fistfuls; the wrecked fastener is a recorded residue fact.
        n = 3
        base = part.mass_g // n
        masses = [base] * (n - 1) + [part.mass_g - base * (n - 1)]
        scrap = f"{part.material}_scrap"
        eff = (effects.remove_part(ent.id, part.id),
               effects.set_attr(ent.id, f"residue_{part.id}", part.attachment)) + tuple(
            effects.create_object(scrap, derived_id(ent.id, f"{part.id}_scrap{i}"),
                                  {"material": part.material, "mass_g": m,
                                   "provenance": [f"ripped from {ent.id}"]})
            for i, m in enumerate(masses))
        ev = (Event(EventKind.IMPACT, ent.id, loudness=0.3,
                    data={"verb": "tear", "part": part.id, "destructive": True}),)
        return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:tear:rip_out",
                            narration=narrator.narrate("tear.rip_out",
                                                       {"part": part.id, "target": ent.name,
                                                        "output": scrap.replace("_", " "),
                                                        "residue": attachment_phrase(part.attachment,
                                                                                     "residue")}))

    if part is not None:  # integral (fixed/unknown attachment) → explain the physics; one near-miss
        def can_tear(p):
            m = materials.get(p.material)
            return (p.attachment in CUTTABLE_ATTACH and m is not None
                    and "tear_resistance" in m.props
                    and prop(m, "tear_resistance") <= _HAND_FORCE + _SLACK)
        line = narrator.narrate("tear.integral", {"part": part.id,
                                                  "why": attachment_phrase(part.attachment)})
        sib = sibling_hint(ent, part, can_tear)
        if sib:
            line += " " + narrator.narrate("hint.sibling",
                                           {"sibling": sib.id,
                                            "sibling_phrase": attachment_phrase(sib.attachment, "hint")})
        return ActionResult(Resolution.REDIRECT, tier="op:tear:integral", narration=line)

    if ent.parts:  # a composite thing isn't torn as a whole → name a part
        return ActionResult(Resolution.REDIRECT, tier="op:tear:composite",
                            narration=narrator.narrate("tear.composite", {"target": ent.name}))

    # standalone sheet → tear into two strips (mass conserved: a + b == original)
    mat_id = ent.materials[0] if ent.materials else "material"
    a = ent.mass_g // 2
    b = ent.mass_g - a
    eff = (
        effects.consume(ent.id),
        effects.create_object(f"{mat_id}_strip", derived_id(ent.id, "a"),
                              {"material": mat_id, "mass_g": a, "provenance": [f"torn from {ent.id}"]}),
        effects.create_object(f"{mat_id}_strip", derived_id(ent.id, "b"),
                              {"material": mat_id, "mass_g": b, "provenance": [f"torn from {ent.id}"]}),
    )
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.2, data={"verb": "tear"}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:tear:strips",
                        narration=narrator.narrate("tear.strips", {"target": ent.name}))
