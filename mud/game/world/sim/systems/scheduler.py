"""world.sim.systems.scheduler — the activity scheduler (DR-14). Pure.

A long action = an Activity (persisted to Attributes by the shell; survives @reload). Each tick accrues
progress, emits tick feedback, routes degraded messages, and keeps PARTIAL progress on interrupt;
events.INTERRUPT_SIGNALS break a pending activity (the running clock itself never stops). After a
reload, recompute elapsed from the world clock on `at_start` (not a timer estimate). Built in roadmap
P4.
"""
from __future__ import annotations


def advance(activities, dt: int):
    """Advance active activities by `dt`; return (progress, completions, effects, events). Implemented
    in roadmap P4."""
    raise NotImplementedError("systems.scheduler.advance — roadmap P4")
