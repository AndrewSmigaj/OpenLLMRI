"""world.sim.operations.interpreter — runs the declarative Operation schema (DR-05).

Evaluates the closed Predicate/Modifier/EffectSpec expression language deterministically. Common
stateless op×material cases are data run here; stateful ops (the radio FSM, the systems/*) are plain
Python behind the SAME interface and register identically — the resolver doesn't care which a given
operation is.

BUILD ORDER (DR-05, the system's biggest bet): write the first 2-3 operations as plain Python functions
FIRST; extract this interpreter only once the repetition is undeniable (avoid the premature-abstraction
trap). What the DSL CANNOT express is documented alongside it so authors know when to drop to Python.
Pure.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, ActionResult, Operation, WorldView  # noqa: F401


def evaluate(op: Operation, attempt: ActionAttempt, world: WorldView) -> "ActionResult | None":
    """Evaluate a declarative operation against the attempt + world. Returns an ActionResult, or None
    if this operation doesn't apply (the resolver then tries the next tier). Implemented in roadmap
    P1/P2. See operations/README.md."""
    raise NotImplementedError("operations.evaluate — roadmap P1")
