"""Whiteout — the pure probe world + attempt grid for the solvability fuzz (DR-18).

Shared by `tools/fuzz.py` (the host harness) and `game/tests/sim/test_fuzz.py` (Tier-1) so the two can
never drift. Pure: builds `EntityState` fixtures + a combinatorial grid of `ActionAttempt`s (every verb ×
every target × every tool, plus two-object relational attempts for pour/tie/wrap). No Evennia, no RNG.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, EntityState, NounRef, Part
from world.sim.operations.registry import OPERATIONS


class ProbeWorld:
    """A minimal WorldView over the fixture entities (get / reachable / in_zone / seed_state)."""
    seed_state = 0

    def __init__(self, ents):
        self._e = {e.id: e for e in ents}

    def get(self, i):
        return self._e.get(i)

    def reachable(self, a):
        return list(self._e)

    def in_zone(self, z):
        return list(self._e)


def probe_world():
    seat = EntityState(id="seat", name="aircraft seat", materials=["steel"], mass_g=5000,
                       state={"ident": "11B"},
                       parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",)),
                              Part("latch", "aluminum", 60, "clipped", ("loose_latch",)),
                              Part("bolt", "steel", 30, "bolted")])
    return ProbeWorld([
        seat,
        EntityState(id="multitool", name="multitool", materials=["steel"], mass_g=150,
                    state={"edge": 0.8, "leverage": 0.5}),
        EntityState(id="tinder", name="dry grass", materials=["dry_grass"], mass_g=40),
        EntityState(id="lighter", name="lighter", materials=["plastic"], mass_g=20,
                    state={"ignition": True}),
        EntityState(id="campfire", name="campfire", materials=["wood"], mass_g=2000, state={"lit": True}),
        EntityState(id="pool", name="puddle", materials=["water"], mass_g=1000),
        EntityState(id="canteen", name="canteen", materials=["water"], mass_g=600),
        EntityState(id="ice", name="chunk of ice", materials=["ice"], mass_g=600),
        EntityState(id="snow", name="snowdrift", materials=["snow"], mass_g=4000),
        EntityState(id="wire", name="coil of wire", materials=["copper_wire"], mass_g=120),
        EntityState(id="bottle", name="bottle", materials=["glass"], mass_g=500),
        EntityState(id="paracord", name="paracord", materials=["nylon_webbing"], mass_g=90),
        EntityState(id="blanket", name="wool blanket", materials=["wool"], mass_g=700),
        EntityState(id="manual", name="flight manual", materials=["paper"], mass_g=300),
        EntityState(id="jerrycan", name="jerry can", materials=["fuel"], mass_g=3000),
        EntityState(id="plank", name="plank", materials=["wood"], mass_g=600),
        EntityState(id="chocolate", name="chocolate bar", materials=["chocolate"], mass_g=100),
        EntityState(id="pilot", name="the pilot", materials=["flesh"], mass_g=78000, state={"dead": True}),
    ])


_TARGETS = ["seat", "multitool", "tinder", "pool", "canteen", "ice", "snow", "wire", "bottle",
            "paracord", "blanket", "manual", "jerrycan", "campfire", "plank", "chocolate", "pilot",
            "ghost"]
_PARTS = [("seat", "cover"), ("seat", "latch"), ("seat", "bolt")]
_TOOLS = [None, "multitool", "lighter"]
_LIQUIDS_CORDS_WRAPS = ["pool", "canteen", "paracord", "wire", "blanket"]
_REL = [("on", "campfire"), ("on", "blanket"), ("to", "seat"), ("around", "seat"),
        ("into", "canteen"), ("on", "ghost")]


def probe_grid():
    """Yield every (verb × target × tool) attempt, plus two-object relational attempts. `ghost` is an
    absent id (tests the no-target path); every attempt must still RESOLVE and every effect CONSERVE."""
    verbs = list(OPERATIONS) + ["polish", "sing"]              # + two nonsense verbs (must still resolve)
    xs = [NounRef(t) for t in _TARGETS] + [NounRef(o, p) for o, p in _PARTS]
    for verb in verbs:
        for x in xs:
            for t in _TOOLS:
                yield ActionAttempt(actor="p", verb=verb, X=x, tool=(NounRef(t) if t else None),
                                    raw=f"{verb} {x.entity_id}")
        for xid in _LIQUIDS_CORDS_WRAPS:
            for rel, y in _REL:
                yield ActionAttempt(actor="p", verb=verb, X=NounRef(xid), relation=rel,
                                    Y=(NounRef(y),), raw=f"{verb} {xid} {rel} {y}")
