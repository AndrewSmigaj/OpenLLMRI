"""world.sim.validation.content_lint — the §44 content-lint (DR-17). Pure.

A HARD GATE at load / CI / `make validate`. Checks authored content: ≥3 solution paths for critical
goals, ≥3 clue paths for critical facts, timed actions have tick feedback + interruptibility, derived
objects have capabilities or explicit non-uses, perception routing on major activity, the global-
softlock check, and that the conservation ledger balances every authored transform. Built in roadmap
P2 (load-time hook earlier). Returns a list of findings (empty = clean).
"""
from __future__ import annotations


def validate(scenario) -> list:
    """Lint an authored scenario against the §44 checklist; return findings (empty = clean). Roadmap
    P2."""
    raise NotImplementedError("validation.validate — roadmap P2")
