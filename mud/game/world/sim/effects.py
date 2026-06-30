"""world.sim.effects — Effect constructors + the canonical effect kinds (DR-10).

Effects are the ONLY state-mutation instruction. The shell's `apply()` (in game/typeclasses — the
imperative shell, NOT here) is the single ENFORCED writer: atomic (transaction.atomic), ledger-gated,
updating the Attribute AND its Tag mirror together; a lint forbids raw obj.db.x= / .attributes.add /
.tags.add anywhere else. This module is pure: it only CONSTRUCTS Effects; it never applies them.
"""
from __future__ import annotations

from typing import Protocol

from world.sim.contracts import ActionResult, Effect, EffectKind  # noqa: F401


class Applier(Protocol):
    """The shell-side writer contract — implemented in game/typeclasses (the imperative shell), NOT
    in world/sim. Documented here so the boundary is explicit and lint-checkable:

        apply(result: ActionResult) -> None   # ledger-gated, atomic; the ONLY writer (DR-10).
    """
    def apply(self, result: ActionResult) -> None: ...


def set_attr(target_id: str, key: str, value) -> Effect:
    """Construct a SET_ATTR effect. (Constructors are wired in roadmap P1.)"""
    raise NotImplementedError("effects.set_attr — roadmap P1")


def remove_part(target_id: str, part_id: str) -> Effect:
    """Construct a REMOVE_PART effect (its mass must be balanced by the ledger, DR-11). Roadmap P1."""
    raise NotImplementedError("effects.remove_part — roadmap P1")


def create_object(template_id: str, from_part: str | None = None) -> Effect:
    """Construct a CREATE_OBJECT effect for a derived object, conserving state/mass. Roadmap P1."""
    raise NotImplementedError("effects.create_object — roadmap P1")
