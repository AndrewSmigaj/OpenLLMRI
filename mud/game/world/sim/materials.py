"""world.sim.materials — the material library + the ordinal→numeric map (DR-04).

The canonical source is a hand-curated `materials.table` per scenario (the quality anchor, DR-17);
the baked form has numbers. ~25 materials for the first scene. Pure: stdlib only.

`props` are INTENSIVE ordinal values (gates / rank-relations), never summed. Conserved mass is REAL
integer grams on EntityState/Part, never an ordinal here.
"""
from __future__ import annotations

from world.sim.contracts import Material, ORDINAL  # noqa: F401  (ORDINAL re-exported for authors)


def load_materials(baked: dict) -> dict[str, Material]:
    """Build the id→Material map from the BAKED table (ordinals already mapped to numbers via
    ORDINAL). Implemented in roadmap P1. See docs/scenarios/whiteout/roadmap.md."""
    raise NotImplementedError("materials.load_materials — roadmap P1")
