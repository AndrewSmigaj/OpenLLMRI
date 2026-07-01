"""Tier-1: solvability fuzz (every attempt resolves + conserves) + seeded-replay determinism (P1.10)."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim import narrator
from world.sim.conservation.ledger import check
from world.sim.contracts import ActionAttempt, EntityState, NounRef, Part, Resolution
from world.sim.materials import load_materials
from world.sim.operations.registry import OPERATIONS
from world.sim.resolver import resolve

MATS = load_materials(MATERIAL_TABLE)
_OK = (Resolution.SUCCESS, Resolution.PARTIAL, Resolution.REDIRECT)


class FakeWorld:
    seed_state = 0
    def __init__(self, ents):
        self._e = {e.id: e for e in ents}
    def get(self, i):
        return self._e.get(i)
    def reachable(self, a):
        return list(self._e)
    def in_zone(self, z):
        return list(self._e)


def _world():
    seat = EntityState(id="seat", name="seat", materials=["steel"], mass_g=5000, state={"ident": "11B"},
                       parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",)),
                              Part("latch", "aluminum", 60, "clipped", ("loose_latch",)),
                              Part("bolt", "steel", 30, "bolted")])
    return FakeWorld([seat,
                      EntityState(id="multitool", name="multitool", mass_g=150, state={"edge": 0.8, "leverage": 0.5}),
                      EntityState(id="tinder", name="tinder", materials=["dry_grass"], mass_g=40),
                      EntityState(id="lighter", name="lighter", mass_g=20, tags=["ignition"]),
                      EntityState(id="pool", name="puddle", materials=["water"], mass_g=1000)])


def _grid():
    narrator.load_responses({})
    targets = [NounRef("seat"), NounRef("seat", "cover"), NounRef("seat", "latch"), NounRef("seat", "bolt"),
               NounRef("multitool"), NounRef("tinder"), NounRef("pool"), NounRef("ghost")]
    tools = [None, NounRef("multitool"), NounRef("lighter")]
    for verb in list(OPERATIONS) + ["polish", "sing"]:
        for x in targets:
            for t in tools:
                yield ActionAttempt(actor="p", verb=verb, X=x, tool=t, raw=f"{verb} {x.entity_id}")


def test_every_attempt_resolves_and_conserves():
    w = _world()
    n = 0
    for a in _grid():
        r = resolve(a, w, MATS)                                   # never raises, never None
        assert r is not None and r.resolution in _OK, f"unresolved: {a.verb} {a.X}"
        if r.effects:
            assert check(w, list(r.effects)).ok, f"conservation violation: {a.verb} {a.X}"
        n += 1
    assert n > 100, "the grid should be a real sweep"


def test_seeded_replay_is_deterministic():
    w = _world()
    for a in _grid():
        assert resolve(a, w, MATS) == resolve(a, w, MATS)         # pure + no RNG -> byte-identical (DR-12)
