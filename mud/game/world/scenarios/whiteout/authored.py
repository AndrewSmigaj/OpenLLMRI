"""Whiteout — the tier-1 AUTHORED rules (DR-09 tier 1; the seam wired 2026-09-07).

`AUTHORED` maps a sim_id to `rule(attempt, world, materials) -> ActionResult | None`. The resolver
tries the rule for `attempt.X`'s entity BEFORE the generic handlers; `None` falls through. This is
the documented exception for puzzle-critical objects — the radio's state machine, the ELT, the
pilot — authored as goals with ≥3 paths in the rescue graph, never as recipes. Empty until the
rescue-graph design pass is promoted; the seam is live so content can land without plumbing.
"""
from __future__ import annotations

AUTHORED: dict = {}
