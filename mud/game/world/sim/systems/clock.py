"""world.sim.systems.clock — the continuously running real-time clock (DR-14, GDD §9). Pure.

LOCKED model: time advances on its own at a fixed real→game pace; **no modes, no planning freeze, no
fast-forward**; nobody can stall it. A deterministic LOGICAL clock — the wall-clock (the heartbeat
Script) decides WHEN a tick fires; WHAT a tick does is this pure function of (state, dt), so the
fuzzer/replay can drive logical ticks reproducibly (DR-12). P1 is minimal: advance world-time; the
placeholder exposure tick emits nothing consequential (real warmth/fire/cold-death is P5).
"""
from __future__ import annotations


def tick(dt, world_time):
    """Advance the logical clock by `dt` game-minutes. Returns (new_world_time, events). Deterministic
    — no random/time/wall-clock."""
    return int(world_time) + int(dt), ()
