"""world.sim.conservation.ledger — the pre-commit conservation ledger (DR-11, §24).

Runs INSIDE the shell's apply(), BEFORE commit. Mass is real integer grams and balances EXACTLY (no
float tolerance); the accountable environment sink absorbs legitimate losses (smoke/heat) and may only
GROW — not a silent catch-all. Energy is a GATE, not a balanced channel (qualitative physics: ordinal
energy can't be conserved unambiguously). A rejection is a BUG (unphysical content), not a player
failure. Pure: stdlib only.
"""
from __future__ import annotations

from world.sim.contracts import Effect, LedgerVerdict, WorldView  # noqa: F401


def check(pre: WorldView, effects) -> LedgerVerdict:
    """Simulate `effects` against `pre` in-memory (no writes) and assert: material identity
    preserved; mass balanced (EXACT, integer grams; the sink absorbs legitimate losses);
    contamination/heat transfer consistent; provenance extended; separated pieces sum to the
    original. Returns a LedgerVerdict (ok=False ⇒ reject the transform as an engine bug). Implemented
    in roadmap P1. See conservation/README.md."""
    raise NotImplementedError("conservation.ledger.check — roadmap P1")


class EnvironmentSink:
    """The accountable pseudo-entity that absorbs mass/energy legitimately leaving the modeled world
    (smoke to air, heat lost). Tracks the total per channel and may only GROW; anomalous growth is
    reviewable and fails tests (DR-11). Implemented in roadmap P1."""
