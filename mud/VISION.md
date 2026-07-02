# VISION — Whiteout

> Anchor file. Short on purpose. Read this before any work session; it is the ground
> truth a loop returns to when work drifts. **Authoritative specs:**
> `docs/scenarios/whiteout/GDD.md` (game design, FINAL) · `docs/architecture/implementation-architecture.md`
> (architecture, v4/FINAL, decisions DR-01…DR-22) · `docs/scenarios/whiteout/roadmap.md` (build order).
> `design.md` is the **archived original seed — not authoritative**. Details live in `docs/`.

## What we are building
**Whiteout** — a text-forward, multiplayer, *systemic* survival-puzzle MUD on **Evennia**.
Survivors of a snowy plane crash improvise with every object around them to survive cold,
injury, hunger and a worsening storm until rescue, escape or collapse.

The central promise (design §2):
> The player survives by **understanding the world**, not by guessing the author's
> intended verb-object pair.

This repo (`MUDExperiments`) hosts a reusable **simulation engine** (the "interaction
system") plus **multiple authored scenarios**. Whiteout is the first scenario.

## Non-negotiables (design §49)
- **The world is the puzzle.** Model everything plausible; require only the core authored
  blockers. Model-deep, requirement-light.
- **Everything physical is tryable, and every attempt *resolves*.** Never "You can't do
  that." Desperate, silly and wasteful attempts get a real, physical answer.
- **Runtime is 100% deterministic — there is NO runtime LLM.** The deterministic engine owns
  state and runs the whole game; the **LLM is a build-time authoring tool only** (GDD §41) — *it
  helps build the world; it is never in the world.* It never invents state, decides survival math,
  or grants success at runtime.
- **Input is a taught command grammar** (GDD §25a): `VERB X [RELATION Y] [WITH Z]`, at action
  granularity — not free-form NLP, not a canned verb list. Everything sensible that fits it resolves
  via the **generative** operation×material engine.
- **Multiplayer-first, on a continuously running real-time clock** (GDD §9). Time advances on its
  own; no player owns or can stall the clock; long actions schedule onto ticks rather than jumping
  it. Sessions are **instanced, synchronous co-op** (~1 in-game day, then reset).
- **Perception is graded, not binary** (design §10–15): visibility, audibility,
  reachability, direction and detail are separate and distance/weather/occlusion-aware.
- **No autonomous in-scenario NPCs** (design §3.3). The dying pilot is scripted, not an AI.
  LLM-controlled *characters* are external bot **players**, not authored NPCs.
- **Conservation holds** (design §24): material, mass, temperature, wetness, contamination,
  damage, ownership and provenance survive every transformation.
- **No prose-only state changes.** If the story says it happened, the simulation made it
  happen.

## How we build (engineering stance)
- **Evennia-native, layered.** Evennia owns entities/state (Postgres)/IO; all *rules* are
  pure dependency-light Python in `game/world/sim/**` that unit-tests without booting the
  server. (ADR-0003)
- **Everything via Docker** (the MUD). The torch bot-agent runs on the host. (ADR-0002)
- **Author from packets, validate as a gate.** Objects/actions/workflows follow the §43
  templates; the §44 validator must pass. See `docs/guides/`.

## Current focus
Design is FINAL (GDD + architecture v4) and **P0–P1 are built**: the frozen contracts, the pure
`world/sim` engine (operations×materials, ledger, taught-grammar parser, resolver, narrator), the thin
Evennia shell (WorldView → `apply()` → propagator), and the enriched co-op slice — 14 verbs, 16
objects, live on the running clock. Current work: **finishing the item-interaction slice** until the
interaction format feels right — the active list is [`BACKLOG.md`](BACKLOG.md) (Now / Next / Later).
*Fun is a continuous design judgment held throughout, not a test a thin slice must pass* (friends see
the finished game). The strategic arc onward (P2–P7): `docs/scenarios/whiteout/roadmap.md`.
