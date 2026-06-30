"""world.sim.resolver.index — the operation×material index (DR-09). Pure.

A dict keyed by `(operation_id, relation, material_of_X, material_of_Y)` → operation schema + material
tuning; O(1) lookup. Single-object actions key with relation/material_of_Y = None, so the common case
is effectively `(operation_id, material_of_X)`; two-object (relational) actions key on the full tuple,
which is how the engine GENERATES outcomes for PAIRS of materials (the seat's fabric *against* the
door's steel).
"""
from __future__ import annotations


def build_index(operations) -> dict:
    """Build the (verb, relation, material_of_X, material_of_Y) → rule index. Roadmap P1/P2."""
    raise NotImplementedError("resolver.index.build_index — roadmap P1")
