"""world.sim.effects — Effect constructors + the canonical effect kinds (DR-10).

Effects are the ONLY state-mutation instruction. The shell's `apply(effects, world)` (in
game/typeclasses/apply.py — the imperative shell, NOT here) is the single ENFORCED writer: atomic
(transaction.atomic), ledger-gated, Attribute + Tag mirror together, `reset_cache()` on rollback. This
module is pure: it only CONSTRUCTS Effects; it never applies them.
"""
from __future__ import annotations

from typing import Protocol

from world.sim.contracts import Effect, EffectKind


class Applier(Protocol):
    """The shell-side single writer contract (implemented in game/typeclasses/apply.py, NOT in
    world/sim). Documented here so the boundary is explicit and lint-checkable:

        apply(effects: list[Effect], world) -> None   # ledger-gated, atomic; the ONLY writer (DR-10).
    """
    def apply(self, effects, world) -> None: ...


def set_attr(target_id: str, key: str, value) -> Effect:
    """Set a payload attribute on an entity (absolute)."""
    return Effect(EffectKind.SET_ATTR, target_id, {"key": key, "value": value})


def adjust_attr(target_id: str, key: str, delta) -> Effect:
    """Adjust a numeric attribute by `delta` (relative)."""
    return Effect(EffectKind.ADJUST_ATTR, target_id, {"key": key, "delta": delta})


def create_object(template: str, sim_id: str, args: "dict | None" = None) -> Effect:
    """Mint a derived object (e.g. a removed part becoming a loose object). `sim_id` is the
    DETERMINISTIC new id (D3/DR-12); `args` carries the conserved state (material, mass_g,
    temperature_c, provenance, …) so the ledger balances."""
    return Effect(EffectKind.CREATE_OBJECT, sim_id, {"template": template, **(args or {})})


def remove_part(target_id: str, part_id: str) -> Effect:
    """Remove a part from a composite object (its mass must be balanced by a paired CREATE_OBJECT/
    CONSUME in the same apply())."""
    return Effect(EffectKind.REMOVE_PART, target_id, {"part_id": part_id})


def consume(target_id: str, mass_g: "int | None" = None) -> Effect:
    """Consume an object (or `mass_g` of it) — e.g. fuel burned; the consumed mass goes to the sink."""
    return Effect(EffectKind.CONSUME, target_id, {"mass_g": mass_g})


def move_zone(target_id: str, zone: str) -> Effect:
    """Move an entity to a zone (perception/space, P3; the effect kind exists now for the seam)."""
    return Effect(EffectKind.MOVE_ZONE, target_id, {"zone": zone})


def set_owner(target_id: str, owner: "str | None") -> Effect:
    """Set or clear an entity's owner/provenance."""
    return Effect(EffectKind.SET_OWNER, target_id, {"owner": owner})
