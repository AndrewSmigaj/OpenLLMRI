"""world.sim.materials — the material library + the ordinal→numeric map (DR-04). Pure: stdlib only.

The authored table (the quality anchor, e.g. `scenarios/whiteout/materials/table.py`) uses ordinal
WORDS; `load_materials` maps them to numbers via `ORDINAL`. Props are INTENSIVE (gates / rank-relations),
never summed; conserved mass is real integer grams on EntityState/Part, never here.

(In P1 this inline word→number mapping IS the bake; the DR-17 bake pipeline formalizes it in P2.)
"""
from __future__ import annotations

from world.sim.contracts import ORDINAL, Material


def _to_number(value) -> float:
    """Map an ordinal word to its number; pass numbers through. Raise on an unknown word."""
    if isinstance(value, bool):  # guard: bool is an int subclass
        raise ValueError(f"material property may not be a bool: {value!r}")
    if isinstance(value, (int, float)):
        return float(value)
    if value in ORDINAL:
        return ORDINAL[value]
    raise ValueError(f"unknown ordinal {value!r} (expected one of {sorted(ORDINAL)} or a number)")


def load_materials(table: dict) -> dict[str, Material]:
    """Build the id→Material map from an authored/baked table.

    `table` maps `material_id -> {"props": {axis: ordinal_word_or_number, ...}, "tags": (...)}`.
    """
    out: dict[str, Material] = {}
    for mid, spec in table.items():
        props = {axis: _to_number(v) for axis, v in spec.get("props", {}).items()}
        out[mid] = Material(id=mid, props=props, tags=tuple(spec.get("tags", ())))
    return out
