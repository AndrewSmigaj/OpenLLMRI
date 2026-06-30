# VISION — Whiteout

> Anchor file. Short on purpose. Read this before any work session; it is the ground
> truth a loop returns to when work drifts. Details live in `docs/`.

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
- **The deterministic engine owns state. The LLM only proposes interpretation and prose**
  (design §41). The LLM never invents state, decides survival math, or grants impossible
  success.
- **Multiplayer-first.** Long actions never jump the global clock; they schedule onto ticks
  (design §9). No player owns the clock, room, puzzle or camera.
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
Project scaffolding is complete and the stack boots a trivial smoketest scene. Next is the
§42 roadmap, starting with **Pass 1 (multiplayer tick engine)**. See
`docs/scenarios/whiteout/roadmap.md`.
