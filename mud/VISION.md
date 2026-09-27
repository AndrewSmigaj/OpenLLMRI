# VISION — Whiteout

> Anchor file. Short on purpose. Read this before any work session; it is the ground
> truth a loop returns to when work drifts. **Authoritative specs:**
> `docs/scenarios/whiteout/GDD.md` (the one game design document, over `docs/design/`) ·
> `docs/architecture/implementation-architecture.md` (architecture, the DR register) · `PLAN.md` (the
> order of work, and the current decisions in §5). Details live in `docs/`.

## What we are building
**Whiteout** — a text-forward, multiplayer, *systemic* survival-puzzle MUD on **Evennia**.
Survivors of a bush-plane crash in an Alaskan valley in the first week of October improvise with every object around them to
survive cold, injury, hunger and a worsening storm until they are rescued — the radio, a signal, or
simply surviving long enough — or die. The only endings are rescued or dead.

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
- **The engine is deterministic — no language model runs inside it.** The engine owns state and
  runs the whole game. Language models help build the world at build time, and they can play
  characters from outside, as players, through the same grammar a person uses — survivors,
  non-human characters, an animal such as the bear. A model never invents state, decides survival
  math, or grants success — except the radio voice's judgement of whether it has been told enough to find
  the party, by criteria the game gives it (Andrew, 2026-09-27; GDD §3 rules 2 and 5).
- **Input is a taught command grammar** (GDD §25a): `VERB X [RELATION Y] [WITH Z]`, at action
  granularity — not free-form NLP, not a canned verb list. Everything sensible that fits it resolves
  via the **generative** operation×material engine.
- **Multiplayer-first, on a continuously running real-time clock** (GDD §9). Time advances on its
  own; no player owns or can stall the clock; long actions schedule onto ticks rather than jumping
  it. It always runs faster than real time — 15 game-minutes per real minute — and fast forward, by
  the players' agreement, runs it at about 150×; awake players can stay in it and type a command to
  slow it, and a player waking or any non-ambient event drops it back (document 06). Sessions are
  **instanced, synchronous co-op**: roughly a week of game time inside one sitting of two or three
  hours that the players can pause and return to, with an escalation ladder and no hard time barriers.
- **Perception is graded, not binary** (design §10–15): visibility, audibility,
  reachability, direction and detail are separate and distance/weather/occlusion-aware.
- **Characters are players; the world runs itself** (GDD §3 rule 5). The pilot is authored content
  (he starts dead); animals act on behaviour rules the engine runs, and a lightweight model may play
  one; LLM-controlled *characters* are external **players**, not authored NPCs.
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
world-building loops have not run yet: the design documents in `docs/design/` are under review with
Andrew, one at a time, and nothing is built and no loop runs until they are finalized. The order of
work is [`PLAN.md`](PLAN.md); its Now slice is [`BACKLOG.md`](BACKLOG.md). *Fun is a continuous design judgment held throughout, not a test
a thin slice must pass* (friends see the finished game).
