"""world.sim.operations._helpers — shared pure helpers for the operation handlers (DR-05). Pure.

No Evennia, no RNG (P1 is deterministic, D3). Handlers read the world (EntityState snapshots) + the
materials table and return Effects/Events.
"""
from __future__ import annotations

from world.sim import narrator
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


def tool_phrase(ref, world):
    """The pre-articled tool phrase for narration: 'the multitool' / 'your bare hands'. Templates
    never write their own article before {tool} (see docs/guides/authoring-actions.md)."""
    name = name_of(ref, world)
    return f"the {name}" if name else "your bare hands"


def attachment_phrase(attachment: str, kind: str = "explain") -> str:
    """A content-tunable physical phrase for an attachment (DR-09a). Voice lives in the scenario
    responses: `attachment.explain.clipped`, etc. Kinds: `explain` (why the verb failed) ·
    `residue` (what the wrecked fastener leaves behind) · `hint` (short neutral state for sibling
    near-misses). Falls back to the kind's `_` entry, then to a literal '{attachment} fast'."""
    phrase = narrator.get(f"attachment.{kind}.{attachment}")
    if phrase is not None:
        return phrase
    fallback = narrator.get(f"attachment.{kind}._") or "{attachment} fast"
    return narrator.render(fallback, {"attachment": attachment})


def sibling_hint(ent, part, can_do):
    """The FIRST sibling Part of `ent` (parts order is deterministic) other than `part` for which
    `can_do(sibling)` is True, else None. At most one, same entity only; `can_do` must close over
    the held tool so a hint is only offered when the verb genuinely works with what the player
    has. Callers phrase it naming the PART, never the method (DR-09a)."""
    for p in ent.parts:
        if part is not None and p.id == part.id:
            continue
        if can_do(p):
            return p
    return None


def derived_id(parent_id: str, tag: str) -> str:
    """A DETERMINISTIC id for an object minted from `parent_id` (DR-12; never uuid/dbref)."""
    return f"{parent_id}:{tag}:loose"


def has_ignition(ref, world) -> bool:
    """True if `ref` provides a flame/spark (a lit or ignition state/tag). Bare hands don't. Shared by
    light/melt (and mirrors burn's own check)."""
    ent, _ = resolve_ref(ref, world)
    if ent is None:
        return False
    st = ent.state or {}
    return bool(st.get("lit") or st.get("ignition")) or "ignition" in ent.tags or "lit" in ent.tags


def heat_source_available(attempt, world) -> bool:
    """True if there's usable heat: the tool provides a flame, OR anything reachable is lit/burning (so
    'light the tinder, then melt snow off its warmth' works without holding the flame)."""
    if has_ignition(attempt.tool, world):
        return True
    for sid in world.reachable(getattr(attempt, "actor", "") or ""):
        e = world.get(sid)
        if e is not None and (has_ignition_state(e)):
            return True
    return False


def has_ignition_state(ent) -> bool:
    """True if an EntityState is itself a flame/heat source (lit/ignition)."""
    st = ent.state or {}
    return bool(st.get("lit") or st.get("ignition")) or "ignition" in ent.tags or "lit" in ent.tags
