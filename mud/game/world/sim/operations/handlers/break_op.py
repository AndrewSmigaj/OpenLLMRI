"""world.sim.operations.handlers.break_op — the `break` operation (DR-05). Pure.

(The module is `break_op` because `break` is a Python keyword; the verb is still "break".)

`break X [with Z]` applies blunt force. Outcome is systemic, by the material:
  - BRITTLE (glass/ice) → SHATTERS into shards (mass conserved), loud;
  - a rigid but non-metal solid (wood/plastic) → SNAPS into pieces if you can bring enough force,
    else you can't get the leverage (redirect);
  - a metal → too tough/ductile to break (redirect → cut it or bend it);
  - anything soft/floppy/liquid → None (the resolver redirects).
Force = bare hands + whatever heft/leverage the tool lends.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import (capability, derived_id, material_of, prop, resolve_ref,
                                           tool_phrase)

VERBS = ("break", "smash", "snap", "shatter")
_HAND_FORCE = 0.4
_SLACK = 0.1


def resolve_break(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None:
        return None
    mat = material_of(attempt.X, world, materials)
    if mat is None:
        return None
    tags = set(mat.tags)
    brittle = "brittle" in tags
    metal = "metal" in tags
    rigidity = prop(mat, "rigidity")
    target = part.id if part else ent.name

    if not brittle and rigidity < 0.5 and not metal:
        return None  # soft / floppy / liquid → resolver redirects

    if metal and not brittle:
        return ActionResult(Resolution.REDIRECT, tier="op:break:too_tough",
                            narration=narrator.narrate("break.too_tough", {"target": target}))

    if part is None and ent.parts:  # a composite isn't smashed as a whole → name a part
        return ActionResult(Resolution.REDIRECT, tier="op:break:composite",
                            narration=narrator.narrate("break.composite", {"target": ent.name}))

    if brittle:
        return _shatter(ent, part, "shard", 3, loud=0.7, tier="op:break:shatter",
                        template_id="break.shatter", target=target)

    force = _HAND_FORCE + capability(attempt.tool, world, "leverage") * 0.6
    if force < rigidity - _SLACK:
        tool = tool_phrase(attempt.tool, world)
        return ActionResult(Resolution.REDIRECT, tier="op:break:no_force",
                            narration=narrator.narrate("break.no_force", {"target": target, "tool": tool}))
    return _shatter(ent, part, "piece", 2, loud=0.5, tier="op:break:snap",
                    template_id="break.snap", target=target)


def _shatter(ent, part, piece_word, n, loud, tier, template_id, target):
    """Remove the mass (a part, or the whole standalone object) and mint `n` pieces summing to it."""
    parent = ent.id
    mat_id = part.material if part else (ent.materials[0] if ent.materials else "material")
    mass = part.mass_g if part else ent.mass_g
    base = mass // n
    masses = [base] * (n - 1) + [mass - base * (n - 1)]
    remove = effects.remove_part(parent, part.id) if part else effects.consume(parent)
    made = tuple(effects.create_object(f"{mat_id}_{piece_word}", derived_id(parent, f"{piece_word}{i}"),
                                       {"material": mat_id, "mass_g": m, "provenance": [f"broke {parent}"]})
                 for i, m in enumerate(masses))
    ev = (Event(EventKind.IMPACT, parent, loudness=loud, data={"verb": "break"}),)
    return ActionResult(Resolution.SUCCESS, effects=(remove,) + made, events=ev, tier=tier,
                        narration=narrator.narrate(template_id, {"target": target, "pieces": n}))
