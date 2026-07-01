"""Tier-1: solvability fuzz (every attempt resolves + conserves) + seeded-replay determinism (P1.10).

Drives the pure resolver over the shared probe grid (world.scenarios.whiteout._probe — the SAME fixture
tools/fuzz.py uses, so host harness and unit test can't drift). Asserts: nothing crashes, everything
resolves to SUCCESS/PARTIAL/REDIRECT, every effect balances in the ledger, and replay is byte-identical.
"""
from world.scenarios.whiteout._probe import probe_grid, probe_world
from world.sim import narrator
from world.sim.conservation.ledger import check
from world.sim.contracts import Resolution
from world.sim.materials import load_materials
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim.resolver import resolve

MATS = load_materials(MATERIAL_TABLE)
_OK = (Resolution.SUCCESS, Resolution.PARTIAL, Resolution.REDIRECT)


def test_every_attempt_resolves_and_conserves():
    narrator.load_responses({})
    w = probe_world()
    n = 0
    for a in probe_grid():
        r = resolve(a, w, MATS)                                   # never raises, never None
        assert r is not None and r.resolution in _OK, f"unresolved: {a.verb} {a.X}"
        if r.effects:
            assert check(w, list(r.effects)).ok, f"conservation: {a.verb} {a.X}"
        n += 1
    assert n > 400, "the grid should be a real sweep"


def test_seeded_replay_is_deterministic():
    narrator.load_responses({})
    w = probe_world()
    for a in probe_grid():
        assert resolve(a, w, MATS) == resolve(a, w, MATS)         # pure + no RNG -> byte-identical (DR-12)
