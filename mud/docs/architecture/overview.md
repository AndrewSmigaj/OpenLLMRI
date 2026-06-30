# Architecture Overview

> **Status: focused view.** The authoritative architecture is
> [`implementation-architecture.md`](implementation-architecture.md) (v4/FINAL, decisions register
> DR-01…DR-22) — defer to it on any conflict, and see its §11 for the full module layout. The
> authoritative *design* is [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md).

How the Whiteout *design* (`../scenarios/whiteout/GDD.md`) is realized on
**Evennia 6.0.0** (Python 3.13, Django 6.0.6, PostgreSQL 16), and where every
system lives in the repo.

Read [`../../VISION.md`](../../VISION.md) first for the non-negotiables. This
document is the map; the [ADRs](adr/0001-record-architecture-decisions.md)
record *why*.

## The one idea: functional core, imperative shell

Whiteout is built as a **functional core / imperative shell**
([ADR-0003](adr/0003-evennia-native-layered-engine.md)):

- **Imperative shell** — Evennia. It owns entities, persistent state (Postgres
  Attributes), networking, accounts, ticks (Scripts / `TickerHandler`) and
  commands (CmdSets). It is the only layer allowed to touch the database, the
  reactor or the network.
- **Functional core** — everything in `game/world/sim/**`. Pure, dependency-light
  Python that imports **no Evennia and no Django**. It encodes all the
  simulation *rules* and is unit-tested without booting the server.

The contract between them is the set of dataclasses in
[`game/world/sim/contracts.py`](../../game/world/sim/contracts.py). The shell
marshals Evennia Attributes into these structures, calls pure functions, gets
back a list of `Effect`s and `Event`s, and applies them. The core never reaches
out; the shell never decides a rule.

```
Evennia (shell)                     world.sim (pure core)
  Attributes  ──marshal──►  EntityState / ActionAttempt
                            pure resolve()
  apply ◄──Effect list───  ActionResult{effects, events, narration}
  route  ◄──Event list───
```

## System map: GDD.md → Evennia

| Design system (§) | Evennia mechanism (shell) | Pure core (`world/sim`) |
|---|---|---|
| Multiplayer time & activity ticks (§9) | one heartbeat `Script` + `TickerHandler` | `systems/clock.py`, `systems/scheduler.py`, `events.py` |
| Scene / zone / direction / perception (§10–15) | one Room per Scene; zone = Character Attribute; rooms/exits for scene transitions | `space/{zones,perception,direction,sound}.py` |
| Object / part / material model (§20–24) | Object typeclass ↔ Attributes | `contracts.py`, `materials.py`, `conservation.py` |
| Core action model & families (§25–27) | command shell parses (Stage A) | `actions/**` resolves (Stage B) |
| Effects & events (§25) | typeclass appliers + message propagator | `effects.py`, `events.py`, `narrator.py` |
| Survival systems: fire/water/warmth/shelter (§31–34) | Object/Character Attributes, tick hooks | `systems/{fire,water,warmth,shelter}.py` |
| Dying pilot (§19) | a scripted `Script` (no AI; see §3.3) | scenario data + condition track |
| Beacon / radio / rescue (§37–39) | scenario objects + tick hooks | `systems/rescue.py` |
| Authoring packets (§43) | — | `ObjectPacket`, `ActionFamilyPacket`, `WorkflowPacket` |
| Validation (§44) | content-lint at load/CI (`make validate`) | `validation/**` |
| LLM (§41) | external bot-player (a client) + build-time authoring | **never** in the core/runtime |

The design's §48 repo sketch is TypeScript-flavoured; the table above is the
authoritative Python realization.

## Repo layout

```
MUDExperiments/
  game/                      # the Evennia game dir (bind-mounted into Docker)
    server/conf/             # Evennia settings, at_initial_setup, etc.
    typeclasses/             # Object / Character / Room / Script SHELL classes
    commands/                # CmdSets — Stage A parsing -> ActionAttempt
    world/
      sim/                   # ===== PURE FUNCTIONAL CORE — no Evennia/Django =====
        contracts.py         #   the dataclasses both layers speak
        materials.py         #   §21 material properties
        conservation.py      #   §24 conservation checks
        effects.py           #   Effect constructors + the canonical effect kinds
        events.py            #   Event queue + activity-interrupt signals (§9)
        narrator.py          #   deterministic prose from real state (§25)
        space/               #   §10–15 perception: zones, perception, direction, sound
        systems/             #   §9 clock/scheduler; §31–34 survival; §39 rescue (roadmap)
        actions/             #   §25–27 Stage-B resolver + families/ (roadmap)
        validation/          #   §44 content-lint (roadmap)
      scenarios/<name>/      # authored content per scenario (Whiteout is one of many)
  agent/                     # external LLM bot-PLAYER harness — runs on the HOST
    brains/                  #   TorchBrain / ClaudeBrain / ScriptedBrain
  docker/evennia/Dockerfile  # extends evennia/evennia:latest (+psycopg2, pytest)
  docker-compose.yml         # evennia + postgres:16
  scripts/                   # create_superuser.py (pty), bootstrap_accounts.py
  Makefile                   # build/init/migrate/accounts/up/load-scenario/test/...
  docs/                      # you are here
```

The folders under `world/sim/` marked *(roadmap)* are introduced by their
[roadmap](../scenarios/whiteout/roadmap.md) pass; `space/`, `contracts.py`,
`effects.py`, `events.py`, `narrator.py`, `materials.py` and `conservation.py`
exist today.

## Data flow for one action

Example: `cut the seatbelt off the seat with the pocketknife` (design §25; the
taught grammar `VERB X [RELATION Y] [WITH Z]`, GDD §25a).

1. **Text → `ActionAttempt` (Stage A, shell).** An Evennia command matches the verb
   against the synonym table and binds the grammar slots, resolving object
   references in the speaker's scene, to fill an
   [`ActionAttempt`](../../game/world/sim/contracts.py)
   (`actor`, `verb`, `X`, `relation`, `Y`, `tool`, `raw`). Unknown phrasing → a help
   nudge showing the format (**no runtime LLM** — the engine never calls a model
   during play; see [llm-integration.md](llm-integration.md)).
2. **Reachability gate.** Because everyone in a scene shares one Evennia room,
   the command first checks the target is *reachable* from the actor's zone (the
   reachability tax — [perception-model.md](perception-model.md)).
3. **Marshal.** The shell builds `EntityState` snapshots for actor, target and
   tool from their Attributes.
4. **`ActionAttempt` → pure resolver (Stage B, core).** `world/sim/actions`
   resolves deterministically through the design §26 tiers **minus the LLM**:
   authored → object → part → material → generic physics → informative failure
   (`Resolution` enum). It returns an `ActionResult`.
5. **`ActionResult`.** Carries `success`, `resolution`, deterministic
   `narration`, `effects: list[Effect]`, `events: list[Event]`, and
   `duration_minutes` for timed work.
6. **Schedule or apply.** Timed work is handed to the scheduler so it accrues on
   ticks without jumping the clock ([tick-and-scheduler.md](tick-and-scheduler.md));
   instant actions apply now.
7. **Effects → Attributes.** The Object/Room typeclass is the *only* place that
   interprets `Effect`s (`set_attr`, `remove_part`, `create_object`,
   `move_zone`, …) and writes Postgres Attributes. No prose-only changes (§44).
8. **Events → perception-routed messages.** The message propagator turns each
   `Event` into per-observer text by perception band and loudness, replacing a
   plain `msg_contents` ([perception-model.md](perception-model.md)).

## Where to go next

- [perception-model.md](perception-model.md) — §10–15 on Evennia.
- [tick-and-scheduler.md](tick-and-scheduler.md) — §9 clock modes & ticks.
- [llm-integration.md](llm-integration.md) — the two LLM seams and the §41 rule.
- [testing.md](testing.md) — the two test tiers.
- [ADRs](adr/0001-record-architecture-decisions.md) — the decisions of record.
- [Guides](../guides/docker-workflow.md) — how to build, author and run.
