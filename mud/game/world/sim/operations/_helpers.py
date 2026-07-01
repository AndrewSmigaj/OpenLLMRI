"""world.sim.operations._helpers — shared pure helpers for the operation handlers (DR-05). Pure.

No Evennia, no RNG (P1 is deterministic, D3). Handlers read the world (EntityState snapshots) + the
materials table and return Effects/Events.
"""
from __future__ import annotations

from world.sim.contracts import Material

# Attachments a cutting tool can sever → cutting a part on one of these FREES it (D12).
CUTTABLE_ATTACH = frozenset({"stitched", "sewn", "tied", "lashed", "cordage", "glued", "taped"})
# Attachments a prying tool can defeat → prying a part on one of these frees it.
PRYABLE_ATTACH = frozenset({"bolted", "screwed", "wedged", "nailed", "clipped", "pinned"})


def resolve_ref(ref, world):
    """Return (EntityState, Part | None) for a NounRef, or (None, None) if it can't be resolved."""
    if ref is None:
        return None, None
    ent = world.get(ref.entity_id)
    if ent is None:
        return None, None
    if ref.part_id:
        for p in ent.parts:
            if p.id == ref.part_id:
                return ent, p
        return ent, None
    return ent, None


def material_id_of(ref, world):
    """The material id of a ref's part (if a part) else the entity's primary material."""
    ent, part = resolve_ref(ref, world)
    if ent is None:
        return None
    if part is not None:
        return part.material
    return ent.materials[0] if ent.materials else None


def material_of(ref, world, materials):
    """The Material object for a ref, or None."""
    mid = material_id_of(ref, world)
    return materials.get(mid) if mid else None


def prop(material, axis: str) -> float:
    """A material's intensive property (0.0 if the material/axis is absent)."""
    if material is None:
        return 0.0
    return float(material.props.get(axis, 0.0))


def capability(ref, world, axis: str) -> float:
    """A tool/object capability value from its `state` (e.g. 'edge' = cut quality, 'leverage' = pry).
    0.0 if there is no tool (bare hands) or the capability is absent."""
    ent, _ = resolve_ref(ref, world)
    if ent is None:
        return 0.0
    val = ent.state.get(axis, 0.0)
    return float(val) if isinstance(val, (int, float)) and not isinstance(val, bool) else 0.0


def name_of(ref, world):
    """A ref's display name (the entity name), or None."""
    ent, _ = resolve_ref(ref, world)
    return ent.name if ent else None


def derived_id(parent_id: str, tag: str) -> str:
    """A DETERMINISTIC id for an object minted from `parent_id` (DR-12; never uuid/dbref)."""
    return f"{parent_id}:{tag}:loose"
