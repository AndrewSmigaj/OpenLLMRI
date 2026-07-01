"""Tier-1: the logical clock advances deterministically (DR-14, P1.8)."""
from world.sim.systems.clock import tick


def test_tick_advances_time():
    assert tick(1, 100) == (101, ())
    assert tick(5, 0) == (5, ())


def test_tick_is_deterministic():
    assert tick(3, 42) == tick(3, 42)   # pure — same input, same output (DR-12)
