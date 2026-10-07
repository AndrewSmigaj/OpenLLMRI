#!/usr/bin/env python3
"""fuzz — the solvability-fuzz harness (DR-18). Drives the pure resolver over a combo grid of
(verb x target x tool [x relation x Y]) on a fixture world and checks: every attempt RESOLVES (no crash,
a valid Resolution) and every effect-producing action BALANCES in the conservation ledger. Deterministic
(P1 has no RNG). Exit 0 if clean; 1 with a report otherwise.

Runs on the host (pure core, no Evennia). The fixture + grid live in the shared, pure
`world.scenarios.whiteout._probe` so this harness and the Tier-1 fuzz test can never drift. The full
ScriptedBrain fuzz over live runs is P2.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game"))

from world.scenarios.whiteout._probe import probe_grid, probe_world               # noqa: E402
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE               # noqa: E402
from world.sim import narrator                                                    # noqa: E402
from world.sim.conservation.ledger import check                                  # noqa: E402
from world.sim.contracts import Resolution                                        # noqa: E402
from world.sim.materials import load_materials                                    # noqa: E402
from world.sim.resolver import resolve                                            # noqa: E402

MATS = load_materials(MATERIAL_TABLE)
_OK = (Resolution.SUCCESS, Resolution.PARTIAL, Resolution.REDIRECT)


def main():
    narrator.load_responses({})
    w = probe_world()
    total = unresolved = violations = 0
    for a in probe_grid():
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
            print(f"  CONSERVATION VIOLATION: {a.verb} {a.X} -> {check(w, list(r.effects)).reason}")
    print(f"fuzz: {total} attempts — {unresolved} unresolved, {violations} conservation violations.")
    return 1 if (unresolved or violations) else 0


if __name__ == "__main__":
    sys.exit(main())
