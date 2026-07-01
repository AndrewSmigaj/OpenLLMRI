#!/usr/bin/env python3
"""fuzz — the solvability-fuzz harness (DR-18). Drives the pure resolver over a combo grid of
(verb x target x tool) on a fixture world and checks: every attempt RESOLVES (no crash, a valid
Resolution) and every effect-producing action BALANCES in the conservation ledger. Deterministic
(P1 has no RNG). Exit 0 if clean; 1 with a report otherwise.

Runs on the host (pure core, no Evennia). The full ScriptedBrain fuzz over live runs is P2.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game"))

from world.scenarios.whiteout.materials.table import MATERIAL_TABLE            # noqa: E402
from world.sim import narrator                                                # noqa: E402
from world.sim.conservation.ledger import check                              # noqa: E402
from world.sim.contracts import ActionAttempt, EntityState, NounRef, Part, Resolution  # noqa: E402
from world.sim.materials import load_materials                               # noqa: E402
from world.sim.operations.registry import OPERATIONS                         # noqa: E402
from world.sim.resolver import resolve                                       # noqa: E402

MATS = load_materials(MATERIAL_TABLE)
_OK = (Resolution.SUCCESS, Resolution.PARTIAL, Resolution.REDIRECT)


class _World:
    seed_state = 0
    def __init__(self, ents):
        self._e = {e.id: e for e in ents}
    def get(self, i):
        return self._e.get(i)
    def reachable(self, a):
        return list(self._e)
    def in_zone(self, z):
        return list(self._e)


def world():
    seat = EntityState(id="seat", name="seat", materials=["steel"], mass_g=5000, state={"ident": "11B"},
                       parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",)),
                              Part("latch", "aluminum", 60, "clipped", ("loose_latch",)),
                              Part("bolt", "steel", 30, "bolted")])
    return _World([seat,
                   EntityState(id="multitool", name="multitool", mass_g=150, state={"edge": 0.8, "leverage": 0.5}),
                   EntityState(id="tinder", name="tinder", materials=["dry_grass"], mass_g=40),
                   EntityState(id="lighter", name="lighter", mass_g=20, tags=["ignition"]),
                   EntityState(id="pool", name="puddle", materials=["water"], mass_g=1000)])


def grid():
    targets = [NounRef("seat"), NounRef("seat", "cover"), NounRef("seat", "latch"), NounRef("seat", "bolt"),
               NounRef("multitool"), NounRef("tinder"), NounRef("pool"), NounRef("ghost")]
    tools = [None, NounRef("multitool"), NounRef("lighter")]
    for verb in list(OPERATIONS) + ["polish", "sing"]:
        for x in targets:
            for t in tools:
                yield ActionAttempt(actor="p", verb=verb, X=x, tool=t, raw=f"{verb} {x.entity_id}")


def main():
    narrator.load_responses({})
    w = world()
    total = unresolved = violations = 0
    for a in grid():
        total += 1
        try:
            r = resolve(a, w, MATS)
        except Exception as e:  # a crash IS an unresolved attempt
            unresolved += 1
            print(f"  CRASH: {a.verb} {a.X}: {type(e).__name__}: {e}")
            continue
        if r is None or r.resolution not in _OK:
            unresolved += 1
            print(f"  UNRESOLVED: {a.verb} {a.X}")
        elif r.effects and not check(w, list(r.effects)).ok:
            violations += 1
            print(f"  CONSERVATION VIOLATION: {a.verb} {a.X}")
    print(f"fuzz: {total} attempts — {unresolved} unresolved, {violations} conservation violations.")
    return 1 if (unresolved or violations) else 0


if __name__ == "__main__":
    sys.exit(main())
