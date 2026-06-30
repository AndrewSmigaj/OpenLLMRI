"""world.sim.resolver.tiers — the §26 resolution tiers (DR-09). Pure.

resolve(attempt, world) walks tiers in order and returns the first hit; EVERYTHING resolves (success /
partial / informative redirect). Specificity dispatch (DR-05): most-specific rule wins, ties broken by
declared integer priority — never file order.

    1 authored-special    (puzzle-critical object rule, e.g. the radio FSM)
    2 object-rule         (rare per-object override)
    3 operation×material  (THE WORKHORSE — index keyed (verb, relation, material_of_X, material_of_Y))
    4 generic-physics     (mass/temperature/containment defaults)
    5 informative-redirect (ranked by smallest unmet-precondition gap; same target first; cap 2-3)

Unhandled-but-sensible attempts log to the wall-sensor for build-time authoring (DR-18). The resolver is
pure: it reads `world` (snapshots) and returns Effects/Events — it never writes.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, ActionResult, WorldView  # noqa: F401


def resolve(attempt: ActionAttempt, world: WorldView) -> ActionResult:
    """Resolve a parsed attempt to an ActionResult. Implemented in roadmap P1. See resolver/README.md."""
    raise NotImplementedError("resolver.resolve — roadmap P1")
