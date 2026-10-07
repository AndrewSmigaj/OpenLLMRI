"""game.typeclasses.winter_survival.heartbeat — the world-clock Script (DR-14). Shell.

A persistent global Script that fires every `interval` real-seconds and advances each active run's
LOGICAL clock by a fixed `dt` via the pure `world.sim.systems.clock` (through the allowlisted `apply`
writer). The wall-clock decides WHEN; `clock.tick` decides WHAT (deterministic). P1 minimal — time
advances; no survival ticks yet (P5). `at_repeat` receives no elapsed-time (verified), so we pass a
fixed dt.
"""
from __future__ import annotations

from typeclasses.scripts import Script


class HeartbeatScript(Script):
    """The Winter Survival running world clock."""

    def at_script_creation(self):
        self.key = "winter_survival_heartbeat"
        self.desc = "Winter Survival running world clock (DR-14)"
        self.interval = 15          # real seconds per tick (the tunable real->game pacing)
        self.persistent = True
        self.start_delay = True

    def at_repeat(self, **kwargs):
        from evennia import search_tag

        from typeclasses.winter_survival.apply import advance_clock
        from typeclasses.winter_survival.propagator import propagate

        for room in [r for r in search_tag("slice", category="run_id") if r.location is None]:
            events = advance_clock(room, dt=1)       # +1 game-minute per tick
            if events:
                propagate(room, events, actor=None)
