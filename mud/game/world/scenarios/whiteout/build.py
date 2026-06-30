"""Whiteout scenario loader (Evennia shell side). `build()` creates the rooms/objects/zones from the
manifest; run via `make load-scenario SCENARIO=whiteout`. Implemented in roadmap P1.

(May import evennia once implemented — it is the imperative-shell loader, NOT pure-core. Kept
import-free as a stub so the scaffold imports on the host without Evennia.)
"""
from __future__ import annotations


def build():
    """Create the Whiteout scene (rooms/objects/zones) in Evennia from the manifest. Roadmap P1."""
    raise NotImplementedError("scenarios.whiteout.build — roadmap P1")
