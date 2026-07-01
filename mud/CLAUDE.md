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
| `make test` | pure `world.sim` unit tests in Docker (no DB, no boot) |
| `make test-host` | **host-fast** pure tests + gates (no Docker; the tight inner loop) |
| `make lint` | the pure-core boundary/determinism + no-raw-writes gates (host, ms) |
| `make test-int` | Evennia integration tests |
| `make validate SCENARIO=…` | §44 content-lint (hard gate) |
| `make bake` / `make fuzz` | build-time: bake authored data / solvability-fuzz |
| `make verify` | gates + compose config check + tests |
| `make shell` | Evennia/Django shell |
| `make agent` | run the scripted bot from the host against a running server |

**Skills over these:** use the **`run-game`** skill to boot / load a scenario / smoke the live
server, and the **`run-tests`** skill to run and interpret the checks (which layer to run when).
The test strategy is documented in [docs/architecture/testing.md](docs/architecture/testing.md).

**One-time dev setup** (per clone): `cp .env.example .env`, then
`git config core.hooksPath .githooks` to enable the pre-commit gate (runs the 4 host-fast lints
before each commit). **Auto-checks:** every push to GitHub runs the gates + Tier-1 + Tier-2 via
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) — a green ✓ / red ✗ per commit. The Docker
image is pinned by digest (`docker/evennia/Dockerfile`) so local, CI and any clone build identically.

## Repo map  (the full module layout lives in ONE place: architecture §11 / DR-21)
- `game/` — the **Evennia shell**: typeclasses, commands, settings. Owns state (Postgres
  Attributes) and IO. Marshals `world.sim.contracts` dataclasses and applies Effects via `apply()`
  (the **only** writer).
- `game/world/sim/` — the **pure functional core**, stdlib only, unit-tested without booting the
  server. **Scaffolded (P0):** a frozen `contracts.py` + interface stubs (`NotImplementedError`, no
  behavior); bodies filled per roadmap phase. See its README.
- `game/world/scenarios/whiteout/` — authored **content** (skeleton + `_template/`); authored P1+.
- `game/world/llm/` — **build-time** authoring seams only (never runtime).
- `game/tests/{sim,integration}/` — the two test tiers; `sim/test_contracts.py` locks the contracts.
- `tools/` — build-time + CI: `bake/fuzz/coverage` (stubs) + `lints/` (the host-fast gates).
- `agent/` — the **bot harness** (host-side; scripted + torch brains; a *client*, not the engine).
- `scripts/` — host helpers (e.g. `create_superuser.py`).
- `docs/` — design, roadmap, architecture, authoring guides (authoritative sources: see Pointers).
- `.claude/` — this tooling: **skills** (`run-game`, `run-tests`, lenses, ontology, fuzz), agents,
  commands, hooks. Reach for `run-game` to operate the server and `run-tests` for the checks.

## Hard rules (LOCKED — do not relitigate; see VISION.md / GDD §0b / the architecture DRs)
- **`world/sim` imports no Evennia/Django — functional core, imperative shell.** Rules are
  pure Python in `game/world/sim/**`. Never put rules in typeclass methods; never import Evennia
  from `world/sim`. Enforced by `tools/lints/check_pure_core.py`. (ADR-0003, DR-01)
- **Runtime is 100% deterministic — NO runtime LLM.** The LLM is a **build-time authoring tool
  only** (GDD §41) — it helps build the world, it is never in the world. It never invents state,
  decides survival math, or interprets input at runtime. (DR-02)
- **The world clock is a continuously running real-time clock** (GDD §9) — it just runs; nobody can
  stall or yank it. Event-driven/turn-based time, a planning-freeze and fast-forward were all rejected.
  A deterministic logical clock under the hood keeps replay/fuzz reproducible. (DR-14)
- **Sessions are instanced, synchronous co-op** (~1 in-game day, then reset). (DR-15)
- **Input is the taught grammar** `VERB X [RELATION Y] [WITH Z]` → `ActionAttempt{verb,X,relation,
  Y,tool}` — not free-form NLP, not a canned verb list; resolution is the generative
  operation×material engine. (DR-08, GDD §25a)
- **One enforced mutation path:** state changes ONLY via Effects applied by `apply()` (atomic,
  ledger-gated). No raw `obj.db.x=` / `.attributes.add` elsewhere — enforced by
  `tools/lints/check_no_raw_writes.py`. (DR-10)
- **Conservation holds (GDD §24):** material, mass (**real integer grams**), temperature, wetness,
  contamination, damage, ownership and provenance survive every transformation. No prose-only state
  changes — if narration says it happened, an Effect made it happen. (DR-11)
- **Author from the §43 packets and pass `make validate` (GDD §44).** The validator is a hard gate
  at load / CI / `make verify`.
- **Read first before authoring or coding:** `VISION.md`, then the authoritative spec for the task
  (`docs/scenarios/whiteout/GDD.md` for design · `docs/architecture/implementation-architecture.md`
  for architecture), the relevant `docs/scenarios/whiteout/roadmap.md` phase, and `docs/guides/`.

## Gotcha
Evennia's `createsuperuser` loops without a TTY. Account #1 is created over a pty by
`scripts/create_superuser.py` (host `pexpect`); `make accounts` runs it. The image
entrypoint word-splits args, so Make commands with quoted args use `--entrypoint`.

## Pointers (authoritative sources — check these before coding; don't trust memory)
- `VISION.md` — the anchor: what we build + the locked non-negotiables.
- `docs/scenarios/whiteout/GDD.md` — **the authoritative game design** (FINAL; §N anchors; §0a
  improvements + §0b locked decisions). `design.md` beside it is the **archived original seed — not
  authoritative**.
- `docs/architecture/implementation-architecture.md` — **the authoritative architecture** (v4/FINAL;
  decisions register DR-01…DR-22). `overview.md` / `perception-model.md` / `tick-and-scheduler.md` /
  `llm-integration.md` / `testing.md` are focused views kept consistent with it.
- `docs/scenarios/whiteout/roadmap.md` — the **slice-first waterfall** build order (P0…P7; P1 = the
  co-op vertical slice → the fun gate).
- `docs/guides/` — authoring guides (objects, actions, workflows).
- `game/world/sim/contracts.py` — the **frozen** dataclasses every `sim` module speaks.
- `docs/investigation/**` + `docs/architecture/review/**` — historical record (how decisions were
  reached); NOT authoritative for current state.
