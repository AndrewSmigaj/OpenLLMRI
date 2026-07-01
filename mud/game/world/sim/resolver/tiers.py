"""world.sim.resolver.tiers — the §26 resolution tiers (DR-09, D1). Pure.

resolve() walks the tiers and returns the FIRST that produces a result; EVERYTHING resolves (SUCCESS /
PARTIAL / informative REDIRECT — never a hard "you can't do that"). Tier 3 is **verb→handler dispatch**
(functions-first, D1); the (verb, relation, material_of_X, material_of_Y) index is P2 (`resolver/index.py`
stays a stub).

  tier 1  authored-special    a per-object authored rule (e.g. the radio FSM), passed in `authored`
  tier 3  operation×material  handler_for(verb)(attempt, world, materials) -> ActionResult | None
  tier 5  informative redirect  generic_redirect(...)  (coarse plausible-verbs, D2)

A tier-5 result carries tier="redirect:generic" — the shell records that as a wall-sensor gap (P1.7).
"""
from __future__ import annotations

from world.sim.contracts import ActionResult
from world.sim.operations.registry import handler_for
from world.sim.resolver.redirect import generic_redirect


def resolve(attempt, world, materials, authored=None) -> ActionResult:
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
