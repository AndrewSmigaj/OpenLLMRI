"""world.sim.narrator — deterministic prose from real post-Effect state (DR-09, §25/§40).

Pre-written templates filled from current state. **NO LLM, ever** — the runtime is deterministic.
Golden-master snapshots guard narration in tests (narration↔Effect). Pure.
"""
from __future__ import annotations

from world.sim.contracts import ActionResult, EntityState  # noqa: F401


def narrate(template_id: str, state: dict) -> str:
    """Render a pre-written template against real state into the player-facing line. Implemented in
    roadmap P1."""
    raise NotImplementedError("narrator.narrate — roadmap P1")
