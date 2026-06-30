"""world.sim.resolver.wall_sensor — the build-time authoring queue (DR-18). Pure.

Sensible attempts that hit the generic redirect (no authored rule) are LOGGED here so developers can
author the missing interaction AT BUILD TIME. Players never trigger generation; the LLM is never in the
world. This module only produces a record; the shell persists it.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, WorldView  # noqa: F401


def log_gap(attempt: ActionAttempt, world: WorldView) -> dict:
    """Return a wall-sensor record for an unhandled sensible attempt (for the build-time queue).
    Roadmap P1."""
    raise NotImplementedError("resolver.wall_sensor.log_gap — roadmap P1")
