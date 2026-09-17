# VISION — Whiteout

> Anchor file. Short on purpose. Read this before any work session; it is the ground
> truth a loop returns to when work drifts. **Authoritative specs:**
> `docs/scenarios/whiteout/GDD.md` (game design, FINAL) · `docs/architecture/implementation-architecture.md`
> (architecture, v4/FINAL, the DR register DR-01…DR-28 + amendments) · `docs/scenarios/whiteout/roadmap.md` (build order).
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

**What it is for (Andrew, 2026-09-16).** Two things, both first-class: a **model world for serious
research** — an LLM acts in it freely, through the same taught grammar a person uses, and its
behaviour and activations are studied (offering it options would change how it thinks, so the world
never does); and a **new kind of MUD** for friends — a survival game where you can do anything within
reason to solve it. Runs are for friends, for humans and agents together, and for agents only. It is a
massive side project, grown mostly in overnight sessions where teams of agents systematically flesh
out the world — every entity, relation and verb — and it has no finish line.

## Non-negotiables (design §49)
- **The world is open-ended.** "Ontologically sufficient" means any and all entities and relations a
  player would reasonably try — chop the log with the axe, dig the dirt, find a rock, find clay, the
  natural world included. The verb set, the nouns, the relations, the materials and the forms are all
  growing sets, grown by evidence from room censuses and from play, without a ceiling. Every count in
  any doc is a floor. A room is never finished; it is "no walls found in the last N runs".
- **Never a menu.** The game never offers a set of actions, never lists what is reachable, never
  names a verb the player did not type. Feedback is a clarification (`Which can do you mean?`,
  `I don't understand 'X'`, a pointer to the grammar help) or the physics of why. Listing would give
  away the puzzles and, for an agent, constrain how it thinks.
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
  it. It may run fast by consensus — when every player is asleep or waiting it advances at 20× and
  events interrupt it; never 0× (DR-14a). Sessions are **instanced, synchronous co-op**; a run is
  roughly a week of game time with an escalation ladder and no hard time barriers (DR-15, amended
  DR-15a).
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
- **Author in the tables, validate as a gate.** Objects, materials, zones, spaces, appearance and
  responses are data tables (`docs/guides/`); `make validate` must pass (DR-17a). Verbs are Python
  handlers, and new ones are expected as the loops find them.
- **The loops are the main line of work.** Agents reason about each room to real-world depth — what
  is there, what it is made of, what it could turn into, everything a survivor might try — into a
  human-readable ontology; then the design is finalized and implemented, room by room; then agents
  play, every wall is logged, and the loop goes again. Run by teams of agents overnight.

## Current focus
The engine core and the crash-site rooms are built and playable; the closure loop's first steps
(forms, derived capabilities, the probe harness, parser tolerance) and the crash draw are in. The
world-building loops have not run yet: the design passes for time and stakes, fire, events, the moral
layer and living rooms are under Andrew's review, the ontology store and the loops' scaffold come
next, and the valley's outdoor zones are designed as documents that implement as data. The active
list is [`BACKLOG.md`](BACKLOG.md) (Now / Next / Later); the master document is
`docs/scenarios/whiteout/roadmap.md`. *Fun is a continuous design judgment held throughout, not a test
a thin slice must pass* (friends see the finished game).
