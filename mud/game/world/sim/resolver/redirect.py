"""world.sim.resolver.redirect — the informative redirect (DR-09). Pure.

When no rule fires, rank candidate operations by the SMALLEST unmet-precondition gap (the action you
were closest to being able to do), prefer the same target, cap at 2-3, and NAME THE VERB, not the
solution ("you could *cut* or *pry* it" — not "use the knife to free the strap"). The convergent lesson
from affordance theory, parser-IF practice, and precondition-error-correction research.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, ActionResult, WorldView  # noqa: F401


def generic_redirect(attempt: ActionAttempt, world: WorldView) -> ActionResult:
    """Build the ranked informative redirect (Resolution.REDIRECT). Roadmap P1."""
    raise NotImplementedError("resolver.redirect.generic_redirect — roadmap P1")
