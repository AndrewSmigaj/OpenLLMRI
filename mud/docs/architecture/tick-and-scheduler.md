# Tick & Scheduler

> **Status: canonical (LOCKED).** This is Whiteout's clock: a **continuously running real-time clock**
> — the decided model (GDD §9 / DR-14). Game time advances on its own at a fixed real→game pace; it is
> never advanced by player actions or chat, and no one can stall or yank it. Event-/turn-based time was
> considered and **rejected** as clunky for multiplayer. The single-player vertical slice needs no clock
> at all; this lands in the post-slice clock phase.

Design §9 (multiplayer time and activity ticks) realized on Evennia. The clock
and scheduler *rules* are pure functions in
[`game/world/sim/systems/`](../../game/world/sim/); the heartbeat is one Evennia
`Script`.

> Core rule (§9.1): **long actions never jump the global clock.** A player who
> starts a 90-minute task does not jump the clock for everyone else; the task
> is scheduled onto ticks and accrues progress while others keep acting.

## One heartbeat, pure delegation

A single Evennia `Script` (via the `TickerHandler`) is the only thing that
"beats." On each tick it does no game logic itself — it gathers state, calls the
pure `systems/clock` and `systems/scheduler` functions, and applies what comes
back (the same functional-core boundary as everywhere else; see
[overview.md](overview.md)).

```
heartbeat Script (shell)        world.sim.systems (pure core)
   gather active activities ─►  scheduler.advance(activities, dt)
   apply progress / effects ◄─  progress, completions, Effects, Events
   route tick messages      ◄─  Events (by perception band; §14)
   advance world clock      ─►  clock.tick(dt, world_time)
```

Tick pace: **1 game-minute per ~10–20 real seconds** (a tunable constant) while the
run is live. Each tick updates activity progress, stamina, cold exposure, injury,
fire/smoke, weather, interruptions, noise events, snow accumulation, rescue search
state and visibility/audibility.

## The clock just runs (no modes)

`systems/clock` is deliberately **not** a mode machine. The global clock advances
**continuously**, at a fixed real→game pace, whenever the run is live — it does
**not** freeze while players read/plan/chat, and it does **not** compress when they
are idle. Reading, planning and talking happen *while the world keeps moving*: the
storm, the dying pilot and the fires don't wait for the party. That pressure is the
survival gameplay, not a tax to be optimized away.

This trivially satisfies the VISION non-negotiable that **no single player can seize
or stall the clock for the others** — because *no one* controls it; it is just wall
time at a fixed scale. A player who wants to pass time issues a normal `wait`/`rest`
**activity** and the clock runs as usual. There is **no planning-mode freeze and no
consensus fast-forward** — both were the event-driven flavour we rejected (GDD §9).

## Activity scheduling

Starting a timed action does **not** block. The resolver returns an
`ActionResult` with `duration_minutes` (and `partial`); the shell registers it as
an activity. Each tick the scheduler accrues progress, emits the actor's tick
feedback (*"You saw at the frozen webbing. A few more nylon fibers part. Progress:
7 / 18 minutes."*, §9.4) and routes a degraded message to nearby observers by
perception band. Activities can be **interrupted** and keep **partial progress**
(§9.5) — an interrupted shelter is still partially useful. Validation requires
every timed action to have tick feedback and to be interruptible or explicitly
marked otherwise (§44; see [../guides/validation-rules.md](../guides/validation-rules.md)).

## Activity-interrupt signals

A player engaged in a long activity (or a `wait`/`rest`) should be **interrupted**
the instant something meaningful happens. The pure set of interrupt signals lives in
[`game/world/sim/events.py`](../../game/world/sim/events.py) as `INTERRUPT_SIGNALS`,
with `should_interrupt(events)`:

```
fire_state_change · survivor_worsens · weather_change
scripted_trigger · rescue_signal · danger · player_stop_request
```

Because interruption is driven by `Event.kind`, any system that emits one of these
events (fire, pilot condition, weather, rescue) automatically breaks a pending
activity and hands control back to the player — there is no separate, drift-prone
list to maintain in the shell. **The running clock itself never stops; only the
player's *current activity* is interrupted.**

## Why this shape

- **Multiplayer-fair.** Progress lives on ticks, not in a single player's
  command, so no one's long action steals time from others (§9.1).
- **Testable.** `clock.tick` and `scheduler.advance` are pure: roadmap P4's
  acceptance test (90-minute task doesn't jump the clock; another player keeps
  acting; progress + interrupt + partial progress) runs as fast pytest with no DB
  and no Evennia boot. See [testing.md](testing.md).

## Related

- [overview.md](overview.md) · [perception-model.md](perception-model.md)
- Roadmap **P4** is the clock/scheduler milestone
  ([roadmap](../scenarios/whiteout/roadmap.md)).
