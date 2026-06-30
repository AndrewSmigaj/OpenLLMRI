# Testing

Whiteout has **two test tiers**, and the functional-core boundary
([overview.md](overview.md)) is precisely what makes the fast tier possible.

## Tier 1 — Fast pure tests (`make test`)

Plain **pytest** over `game/world/sim/**`. **No Postgres, no Evennia boot, no
Twisted reactor.** Because the core imports no Evennia/Django, these tests
import the pure modules directly, build the
[contract dataclasses](../../game/world/sim/contracts.py) by hand, call pure
functions and assert on the returned `Effect`/`Event`/`PerceptionResult`
structures.

```
make test        # docker compose run --rm --no-deps evennia pytest -q tests/sim
```

`--no-deps` skips even starting Postgres — the point is that this tier needs
nothing but Python. These tests cover the §45 strategy: material/cutting rules,
conservation (§24), perception bands & direction (§10–15), clock & scheduler
(§9), sound propagation, action resolution tiers. They are the fast inner loop
during authoring and the gate the agentic
[loop](../guides/loop-workflow.md) runs every iteration.

> **This tier is the payoff of the architecture.** Keeping all *rules* pure means
> the bulk of the game's logic is verified in milliseconds without a database or
> a server. If a test here needs Evennia, the boundary has leaked — move the rule
> into `world/sim`.

## Tier 2 — Evennia integration tests (`make test-int`)

These run through **Evennia's own test runner** against a **throwaway test DB**.
They verify the *shell*: typeclasses marshalling Attributes into `EntityState`
and applying `Effect`s back, command parsing (Stage A → `ActionAttempt`), the
reachability gate, the heartbeat `Script`, and the message propagator routing
per observer.

```
make test-int    # docker compose run --rm evennia evennia test --settings settings tests.integration
```

This tier needs the full stack (hence no `--no-deps`); Evennia stands up a test
database, builds objects from typeclasses, and exercises the seams the pure tests
deliberately cannot reach.

## What goes where

| Concern | Tier 1 (pure) | Tier 2 (integration) |
|---|---|---|
| Material / cutting / conservation rules | ✅ | |
| Perception bands, direction, sound | ✅ | |
| Clock tick, scheduler, activity interrupts | ✅ | |
| Action resolution tiers (§26 minus LLM) | ✅ | |
| Attribute ↔ `EntityState` marshalling | | ✅ |
| Command parsing & reachability gate | | ✅ |
| Heartbeat Script & message propagator | | ✅ |
| Content lint (authored packets) | see below | |

## Content validation is not a test tier

The §44 validation checklist runs as **content-lint**, not as runtime or as a
unit test: `make validate` (and `make verify`, which adds a compose config check
plus `make test`). It checks authored scenario content — solution-path counts,
conservation, perception routing, tick feedback, etc. See
[../guides/validation-rules.md](../guides/validation-rules.md).

```
make verify      # docker compose config -q  +  make test  +  make validate
```

## Related

- [overview.md](overview.md) — the functional-core boundary that enables Tier 1.
- [../guides/docker-workflow.md](../guides/docker-workflow.md) — the full command set.
- [../guides/loop-workflow.md](../guides/loop-workflow.md) — `make verify` in the loop.
