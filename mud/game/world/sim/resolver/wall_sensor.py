"""world.sim.resolver.wall_sensor — the build-time authoring-queue record (DR-18). Pure.

A sensible attempt that reaches the generic redirect (no authored rule) is a GAP: `gap_record` returns a
serializable record the shell persists to the build-time authoring queue, so devs can author the missing
interaction later. Players never trigger generation; the LLM is never in the world. No I/O here — the
shell writes.
"""
from __future__ import annotations


def gap_record(attempt, world=None) -> dict:
    """A serializable record of an unhandled sensible attempt (for the authoring queue)."""
    x = attempt.X
    return {
        "raw": attempt.raw,
        "verb": attempt.verb,
        "target": x.entity_id if x else None,
        "part": x.part_id if x else None,
        "relation": attempt.relation,
    }
