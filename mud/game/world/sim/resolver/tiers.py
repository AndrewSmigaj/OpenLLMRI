"""world.sim.resolver.tiers — the §26 resolution tiers (DR-09, D1). Pure.

resolve() walks the tiers and returns the FIRST that produces a result; EVERYTHING resolves (SUCCESS /
PARTIAL / informative REDIRECT — never a hard "you can't do that"). Tier 3 is **verb→handler dispatch**
(functions-first, D1); the (verb, relation, material_of_X, material_of_Y) index is P2 (`resolver/index.py`
stays a stub).

  tier 1  authored-special    a per-object authored rule (e.g. the radio FSM), passed in `authored`
  tier 3  operation×material  handler_for(verb)(attempt, world, materials) -> ActionResult | None
  tier 5  informative redirect  generic_redirect(...)  (coarse plausible-verbs, D2)

A tier-5 result carries tier="redirect:generic" — the shell records that as a wall-sensor gap (P1.7).

DR-13a: the REACH GATE runs before every tier — a bound X/Y/tool outside the actor's zone gets the
§17 "too far to {verb} from here" redirect (with direction), gating every verb incl. examine and
future authored rules. `move` is exempt (it's how you close distance); an unzoned world never
gates (the one-zone compat rule). `redirect:too_far` is a perception outcome, NOT a wall-sensor gap.
"""
from __future__ import annotations

from world.sim import narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations.registry import handler_for
from world.sim.resolver.redirect import generic_redirect
from world.sim.space import direction


def _reach_gate(attempt, world) -> "ActionResult | None":
    if attempt.verb == "move":
        return None
    actor = world.get(attempt.actor)
    actor_zone = (actor.state or {}).get("zone") if actor else None
    if actor_zone is None:
        return None                                    # one-zone world: nothing to gate
    refs = (("target", attempt.X),) + tuple(("target", y) for y in (attempt.Y or ())) \
        + (("tool", attempt.tool),)
    for role, ref in refs:
        if ref is None or ref.entity_id.startswith("zone:"):
            continue
        ent = world.get(ref.entity_id)
        zone = (ent.state or {}).get("zone") if ent else None
        if zone is None or zone == actor_zone:
            continue
        dphrase = direction.phrase(actor_zone, zone) or "some way off"
        if role == "tool":
            line = narrator.narrate("reach.tool_too_far", {"tool": ent.name, "direction": dphrase})
        else:
            line = narrator.narrate("reach.too_far", {"target": ent.name, "direction": dphrase,
                                                      "verb": attempt.verb})
        return ActionResult(Resolution.REDIRECT, tier="redirect:too_far", narration=line)
    return None


def resolve(attempt, world, materials, authored=None) -> ActionResult:
    # tier 0 — the reach gate (DR-13a): perception answers before physics gets a say
    gated = _reach_gate(attempt, world)
    if gated is not None:
        return gated

    # tier 1 — authored-special (a per-object rule, e.g. the radio stub)
    if authored and attempt.X is not None:
        rule = authored.get(attempt.X.entity_id)
        if rule is not None:
            r = rule(attempt, world, materials)
            if r is not None:
                return r

    # tier 3 — operation × material (verb → handler)
    handler = handler_for(attempt.verb)
    if handler is not None:
        r = handler(attempt, world, materials)
        if r is not None:
            return r

    # tier 5 — informative redirect (never a flat refusal)
    return generic_redirect(attempt, world, materials)
