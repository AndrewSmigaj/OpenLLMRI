"""world.sim.narrator — deterministic prose from real post-Effect state (DR-09, §25/§40).

Pre-written templates filled from state. **NO LLM, ever** — the runtime is deterministic; golden-master
snapshots guard narration in tests. Pure. The operation handlers call `narrate(template_id, state)` with
the projected post-state (D7), so narration is produced inside the pure resolver and is testable.

`_RESPONSES` is loaded-once content (immutable after `load_responses`), not mutable runtime state.
"""
from __future__ import annotations

_RESPONSES: dict[str, str] = {}


class _SafeDict(dict):
    """A format mapping that leaves unknown `{placeholders}` literal instead of raising."""
    def __missing__(self, key):
        return "{" + key + "}"


def load_responses(responses: dict) -> None:
    """Install the response template registry (`template_id -> template`). Replaces any prior set."""
    _RESPONSES.clear()
    _RESPONSES.update(responses)


def render(template: str, state: dict) -> str:
    """Fill a template string from `state` (deterministic; unknown placeholders are left literal)."""
    return str(template).format_map(_SafeDict(state or {}))


def narrate(template_id: str, state: dict) -> str:
    """Render the registered template for `template_id` against `state`. Never blank — falls back to a
    generic line if the template id is missing (a missing template is a build-time content gap to fill,
    not a runtime crash)."""
    template = _RESPONSES.get(template_id)
    if template is None:
        return _RESPONSES.get("__fallback__", "Something gives way.")
    return render(template, state)
