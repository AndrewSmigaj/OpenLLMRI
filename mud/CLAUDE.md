# CLAUDE.md — Whiteout

**Whiteout** is a systemic, multiplayer survival-puzzle MUD on Evennia: survivors of a
snowy plane crash improvise with the world to outlast cold, injury, hunger and a storm.
This repo hosts a reusable simulation engine (the "interaction system") plus authored
scenarios; Whiteout is the first.

This file is a pointer hub. Don't put design detail here — point to the docs.

## Stack
Evennia 6.0.0 · Python 3.13 · Django 6.0.6 · PostgreSQL 16.
**Everything runs via Docker.** Ports: 4000 telnet · 4001 website · 4002 websocket.
**Host carve-out:** the torch bot-agent (`agent/`) runs on the *host* — it needs the
user's model weights + GPU and is never containerized.

## Commands (all via Docker, through the Makefile)
| Target | Does |
|--------|------|
| `make build` | build the Evennia image |
| `make init` | one-time Evennia game-dir scaffold |
| `make migrate` | run DB migrations |
| `make accounts` | create admin (Account #1) + bot accounts (idempotent) |
| `make up` / `make up-d` | run the server (foreground / detached) |
| `make down` / `make restart` | stop / reload the server |
| `make logs` | follow the evennia logs |
| `make load-scenario SCENARIO=smoketest` | load a scenario |
| `make test` | pure `world.sim` unit tests (no DB, no boot) |
| `make test-int` | Evennia integration tests |
| `make validate SCENARIO=…` | §44 content-lint (hard gate) |
| `make verify` | compose config check + tests + validate |
| `make shell` | Evennia/Django shell |
| `make agent` | run the scripted bot from the host against a running server |

## Repo map
- `game/` — the **Evennia shell**: typeclasses, commands, settings. Owns state (Postgres
  Attributes) and IO. Marshals `world.sim.contracts` dataclasses and applies Effects.
- `game/world/sim/` — the **pure rules** (functional core), stdlib only, unit-tested
  without booting the server. *Not built yet* — see its README + the roadmap.
- `game/world/scenarios/` — authored **content** (objects/actions/workflows). Whiteout
  will live here. *Not built yet.*
- `game/tests/sim/` — fast pure pytest for `world.sim` (run by `make test`). *Empty until
  the engine exists.*
- `agent/` — the **bot harness** (host-side; scripted + torch brains).
- `scripts/` — host helpers (e.g. `create_superuser.py`).
- `docs/` — design, roadmap, architecture, authoring guides.
- `.claude/` — this tooling (agents, commands, hooks).

## Hard rules
- **`world/sim` imports no Evennia/Django — functional core, imperative shell.** Rules are
  pure Python in `game/world/sim/**`. Never put rules in typeclass methods; never import
  Evennia from `world/sim`. (ADR-0003)
- **The deterministic engine owns state; the LLM only proposes interpretation and prose
  (design §41).** The LLM never invents state, decides survival math, or grants impossible
  success. No LLM call in the deterministic core or blocking the Twisted reactor.
- **Conservation holds (design §24):** material, mass, temperature, wetness, contamination,
  damage, ownership and provenance survive every transformation. No prose-only state
  changes — if narration says it happened, an Effect made it happen.
- **Author from the §43 packets and pass `make validate` (design §44).** The validator is a
  hard gate at load / CI / `/verify`.
- **Read first before authoring or coding:** `VISION.md`, the scenario design
  (`docs/scenarios/whiteout/design.md`), and the relevant `docs/guides/`.

## Gotcha
Evennia's `createsuperuser` loops without a TTY. Account #1 is created over a pty by
`scripts/create_superuser.py` (host `pexpect`); `make accounts` runs it. The image
entrypoint word-splits args, so Make commands with quoted args use `--entrypoint`.

## Pointers
- `VISION.md` — the anchor: what we build and the non-negotiables.
- `docs/architecture/overview.md` — layering (functional core / imperative shell, ADRs).
- `docs/scenarios/whiteout/design.md` — full design (sections referenced as §N).
- `docs/scenarios/whiteout/roadmap.md` — §42 build order (Pass 1…10).
- `docs/guides/` — authoring guides (objects, actions, workflows).
- `game/world/sim/contracts.py` — the dataclasses every `sim` module speaks.
