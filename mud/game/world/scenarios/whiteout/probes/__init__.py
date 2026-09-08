"""Whiteout — the probe corpus (DR-18a): executable coverage. Each module contributes a list of
probe dicts (see world.sim.testing.probes); `PROBES` is the union; `BASELINE` the committed passing
count that may never drop (the ratchet). Sources: the room censuses, the example chain, the
phrasing corpus, the rescue graph, the dilemma set. No self-graded probes: every probe cites its
source or Andrew's approval."""
from __future__ import annotations

import os

from world.scenarios.whiteout.probes.census import PROBES as _CENSUS
from world.scenarios.whiteout.probes.chain import PROBES as _CHAIN

PROBES: list[dict] = list(_CHAIN) + list(_CENSUS)
BASELINE_PATH = os.path.join(os.path.dirname(__file__), "BASELINE")


def baseline() -> int:
    try:
        with open(BASELINE_PATH, encoding="utf-8") as fh:
            return int(fh.read().strip() or 0)
    except FileNotFoundError:
        return 0


def _check_unique():
    seen = set()
    for p in PROBES:
        if p["id"] in seen:
            raise ValueError(f"duplicate probe id {p['id']!r}")
        seen.add(p["id"])


_check_unique()
