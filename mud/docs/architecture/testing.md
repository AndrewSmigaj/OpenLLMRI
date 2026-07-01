# Testing

Whiteout's checks come in **layers, fast → slow**, and the functional-core boundary
([overview.md](overview.md)) is precisely what makes the fast layers possible. Day to day you
drive them through the **`run-tests`** skill (`.claude/skills/run-tests/`); this doc is the
authoritative record of *what each layer proves* and *when to run what*.

| Layer | Command | Proves |
|---|---|---|
| 4 structural gates (host-fast) | `make lint` | the functional-core boundary + determinism, the single `apply()` writer, the single output path (propagator), doc-consistency |
| Tier 1 — pure unit | `make test-host` (host) / `make test` (Docker) | the pure `world/sim` engine: materials, conservation, resolver, parser, clock |
| Tier 2 — Evennia integration | `make test-int` | the shell: Attribute↔`EntityState` marshalling, commands, the propagator, the heartbeat Script |
| Solvability fuzz | `make fuzz` | every attempt resolves + every effect conserves mass; seeded-replay is byte-identical |

### When to run what
| Moment | Runs | Command |
|---|---|---|
| Editing (inner loop) | gates + Tier-1 pure | `make test-host` |
| On Stop (auto, wired) | 4 gates + compose config | `.claude/hooks/verify.sh` |
| Before each local commit | 4 gates | `.githooks/pre-commit` — enable once: `git config core.hooksPath .githooks` |
| Before a push / full local pass | gates + compose + Tier-1 | `make verify` |
| Shell / integration check | Tier-2 Evennia | `make test-int` |
| Every GitHub push | all of the above | `.github/workflows/ci.yml` (auto) |

The two detailed tiers follow.

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
| Action resolution tiers (§26 minus LLM) | ✅ | |
| Basic clock tick (P1) | ✅ | |
| Attribute ↔ `EntityState` marshalling | | ✅ |
| Command parsing & reachability gate | | ✅ |
| Heartbeat Script & message propagator | | ✅ |
| Perception bands / direction / sound | ✅ *(roadmap P5+, not built yet)* | |
| Scheduler / activity interrupts | ✅ *(roadmap P5+, not built yet)* | |
| Content lint (authored packets) | see below | |

## Content validation is not a test tier

The §44 validation checklist runs as **content-lint**, not as runtime or as a
unit test: `make validate` checks authored scenario content — solution-path counts,
conservation, perception routing, tick feedback, etc. See
[../guides/validation-rules.md](../guides/validation-rules.md). It is **engine-stage
(roadmap)** — a stub today — so it is not yet wired into `make verify`.

`make verify` is the full local gate to run before a push:

```
make verify      # make lint  +  docker compose config -q  +  make test
```

## Related

- [overview.md](overview.md) — the functional-core boundary that enables Tier 1.
- [../guides/docker-workflow.md](../guides/docker-workflow.md) — the full command set.
- [../guides/loop-workflow.md](../guides/loop-workflow.md) — `make verify` in the loop.
- `.claude/skills/run-tests/` — drive + interpret these checks (which to run when).
- `.claude/skills/run-game/` — boot + smoke the live server for a manual playtest.
- `.github/workflows/ci.yml` — the same gates + Tier-1 + Tier-2 run on every GitHub push.
