"""world.sim.events — Event helpers + the activity-interrupt signal set (DR-10, DR-14).

The continuously running real-time clock NEVER stops. INTERRUPT_SIGNALS only break a player's pending
ACTIVITY (a danger event interrupts your sawing). Because interruption is driven by Event.kind, any
system that emits one of these automatically interrupts — no drift-prone list in the shell. Pure.
"""
from __future__ import annotations

from world.sim.contracts import Event, EventKind  # noqa: F401

# A pending activity (or a wait/rest) is interrupted the instant one of these occurs.
INTERRUPT_SIGNALS: frozenset[EventKind] = frozenset({
    EventKind.FIRE_STATE_CHANGE,
    EventKind.SURVIVOR_WORSENS,
    EventKind.WEATHER_CHANGE,
    EventKind.SCRIPTED_TRIGGER,
    EventKind.RESCUE_SIGNAL,
    EventKind.DANGER,
    EventKind.PLAYER_STOP_REQUEST,
})


def should_interrupt(events) -> bool:
    """True if any event in `events` is an interrupt signal (breaks a pending activity; the running
    clock itself never stops). Implemented in roadmap P4."""
    raise NotImplementedError("events.should_interrupt — roadmap P4")
