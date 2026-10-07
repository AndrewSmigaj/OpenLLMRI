# ADR-0003: Evennia-native, layered engine (functional core / imperative shell)

- **Status:** Accepted
- **Date:** 2026-06

## Context

Whiteout's design is a deep *systemic* simulation: materials, parts, conservation,
graded perception, scheduled multiplayer time, an action-resolution priority
ladder (§25–27). We need that simulation to be **rigorously testable** and
**portable across scenarios**, while still getting Evennia's mature MUD plumbing
(accounts, networking, persistence, commands, tickers, web client) for free.

The tension: Evennia wants you to put behaviour on typeclasses (Objects, Rooms,
Characters) backed by Django/Postgres. Putting the simulation *rules* there would
chain every test to a database and a booted server, and weld the rules to Evennia.

Alternatives considered:

1. **Evennia-native, layered (chosen).** Evennia owns state/IO; all rules live in
   a pure `world/sim` package that imports no Evennia/Django.
2. **Decoupled core.** A standalone rules engine that Evennia *calls into*, but
   still co-deployed and somewhat aware of Evennia's lifecycle. More ceremony, no
   clear win over (1) given the contract dataclasses already isolate the core.
3. **Fully-decoupled service.** The simulation as a separate networked service
   Evennia talks to over RPC. Maximum isolation, but adds a process boundary,
   serialization, latency and operational burden the project does not need —
   and it would fight Evennia's reactor model.

## Decision

Adopt **Evennia-native, layered**: a **functional core / imperative shell**.

- **Imperative shell = Evennia.** Owns entities and persistent state (Postgres
  Attributes), networking, accounts, ticks (Scripts / `TickerHandler`) and
  commands (CmdSets). It is the only layer that touches the DB, the reactor or
  the network.
- **Functional core = `game/world/sim/**`.** Pure, dependency-light Python that
  imports **no Evennia and no Django**. All simulation *rules* live here and are
  unit-tested without booting the server.
- **The boundary is `world/sim/contracts.py`.** The shell marshals Evennia
  Attributes into the dataclasses (`EntityState`, `ActionAttempt`, …), calls pure
  functions, receives an `Effect`/`Event` list and an `ActionResult`, and applies
  them. The core never reaches out; the shell never decides a rule.

## Consequences

- **Tier-1 tests need no DB and no server** (`make test`), so the bulk of the
  game's logic verifies in milliseconds. This is the architecture's main payoff;
  see [../testing.md](../testing.md).
- **Rules are scenario-portable.** `world/sim` is the reusable engine; Whiteout
  is one scenario's content on top of it (see
  [../../guides/adding-a-scenario.md](../../guides/adding-a-scenario.md)).
- **A discipline to hold:** the core must stay import-clean. If a pure module ever
  needs Evennia, the rule is in the wrong layer — push it down, keep the shell
  thin. A leak shows up as a Tier-1 test that suddenly needs Evennia.
- Enables the §41 guarantee that the LLM lives only in the shell, never in the
  deterministic core (see [ADR-0005](0005-llm-bot-player-and-torch.md) and
  [../llm-integration.md](../llm-integration.md)).
