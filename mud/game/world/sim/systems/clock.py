"""world.sim.systems.clock — the continuously running real-time clock (DR-14, GDD §9). Pure.

LOCKED model: game time advances on its own at a fixed real→game pace (a tunable constant, ~10-20
real-seconds per game-minute). **NO modes, no planning freeze, no fast-forward**; nobody can stall or
yank it. Under the hood it is a deterministic LOGICAL clock — time is an INPUT — so the wall-clock only
decides WHEN a tick fires while `tick(dt, ...)` is a pure function of (state, dt); the fuzzer/replay
drive logical ticks directly and stay byte-reproducible (DR-12). Built in roadmap P4.
"""
from __future__ import annotations


def tick(dt: int, world_time: int):
    """Advance the logical clock by `dt` game-minutes; return (new_world_time, due_events). A pure
    function of (state, dt) — no `random`/`time`/wall-clock. Implemented in roadmap P4."""
    raise NotImplementedError("systems.clock.tick — roadmap P4")
