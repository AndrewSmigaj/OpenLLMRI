# `world/sim/` — the simulation engine (pure functional core)

The **functional core**: deterministic, dependency-light Python that imports **no Evennia/Django** and
touches no database. The Evennia typeclasses/commands are the *imperative shell* that owns state
(Postgres Attributes), marshals these dataclasses, runs these pure functions, and applies the returned
Effects (the only writer).

> **Status: scaffolded (P0).** The package tree, the **frozen** `contracts.py`, and interface stubs
> (`NotImplementedError`, no behavior) are in place. Bodies are filled per phase in
> [`docs/scenarios/whiteout/roadmap.md`](../../../docs/scenarios/whiteout/roadmap.md). The authoritative
> spec is
> [`docs/architecture/implementation-architecture.md`](../../../docs/architecture/implementation-architecture.md)
> (decisions register DR-01…DR-22).

## The boundary rule (ADR-0003, enforced by lint)
> `world/sim/**` imports **no** Evennia/Django and touches no DB. It speaks plain dataclasses
> (`contracts.py`). No `dbid`/`uuid`/`datetime` in `EntityState` (determinism, DR-12). Mass is **real
> integer grams**; ordinals are **intensive properties only** (gates / rank-relations), never summed.

## Module layout (DR-21)
| Path | DR / § | Purpose | Roadmap |
|---|---|---|---|
| `contracts.py` | DR-01 | the **FROZEN** backbone dataclasses both layers speak | P0 |
| `materials.py` | DR-04 | `Material` + ordinal→numeric map + baked-table loader | P1 |
| `operations/` | DR-05 | the op interpreter (closed expr language); **functions-first** | P1/P2 |
| `resolver/` | DR-09 | §26 tiers + the `(verb,relation,matX,matY)` index + redirect + wall-sensor | P1 |
| `conservation/` | DR-11 | the pre-commit ledger + the accountable environment sink | P1 |
| `parser/` | DR-08 | the taught grammar `VERB X [RELATION Y] [WITH Z]` → `ActionAttempt` | P1 |
| `effects.py` `events.py` `narrator.py` | DR-10 | Effects; Events + interrupt signals; deterministic prose | P1 |
| `space/` | DR-13 | zones, perception, direction, sound | P3 |
| `systems/` | DR-14/16, §31–39 | running clock, scheduler, survival, rescue, weather | P4–P7 |
| `validation/` | DR-17 / §44 | content-lint over authored scenarios | P2 |

The key signatures (`parse`, `resolve`, `ledger.check`, operation `evaluate`; and the shell-side
`apply`) are stubbed with docstrings. See
[`docs/architecture/overview.md`](../../../docs/architecture/overview.md).
