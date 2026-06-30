# `world/sim/systems/` — stateful subsystems (DR-14/16, §31–39)

Stateful logic that registers behind the **same** operation/resolver interface as any operation, as
plain Python (not the DSL). All pure.

| File | DR / § | Purpose | Roadmap |
|---|---|---|---|
| `clock.py` | DR-14 | the **continuously running real-time clock** (logical under the hood) | P4 |
| `scheduler.py` | DR-14 | the activity scheduler (timed tasks accrue on ticks; interrupts) | P4 |
| `fire.py` | §31 | fire state ladder + hazards | P5 |
| `warmth.py` | §32 | warmth/cold + the **no-materials warmth floor** | P5 |
| `water.py` | §33 | water safety gated by container state | P5 |
| `shelter.py` | §34 | shelter by properties (partial shelters count) | P5 |
| `injury.py` | §35 | systemic injury + improvised medicine | P5 |
| `rescue.py` | DR-16, §37–39 | additive-confidence rescue + the radio FSM | P5 |
| `weather.py` | §8 | the storm arc on the running clock | P7 |

The clock is **LOCKED**: it just runs (no modes, no fast-forward, nobody can stall it); the logical-clock
internals keep replay/fuzz deterministic (DR-12). See
[`docs/architecture/tick-and-scheduler.md`](../../../../docs/architecture/tick-and-scheduler.md).
