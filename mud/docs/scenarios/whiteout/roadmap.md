# Whiteout — Implementation Roadmap

> **Status: FINAL — the waterfall build order.** Derived from `GDD.md` (§42) and
> [`../../architecture/implementation-architecture.md`](../../architecture/implementation-architecture.md)
> (DR-22 slice → layered build). **Supersedes** the older §42 "Pass 1–10" order, which built the
> multiplayer/clock engine first and assumed a runtime LLM — both wrong now (see *What changed* at the
> end).
>
> **Locked decisions this roadmap builds toward (never re-litigated):** runtime is **100% deterministic**
> (no runtime LLM — the LLM is a build-time authoring tool only); the world clock is a **continuously
> running real-time clock**; sessions are **instanced, synchronous co-op runs**; input is the **taught
> grammar** `VERB X [RELATION Y] [WITH Z]` (GDD §25a).
>
> **Doctrine.** Get the core *right* — the systemic mechanism works and the interaction *feels* right on the
> smallest real subset — before building breadth. (Fun is a **continuous design judgment** we make
> throughout, not a test the slice must pass.) Each phase has an **exit gate**; the next
> phase does not start until its gate passes. All rules are pure `game/world/sim/**` (Tier-1 tested
> without booting Evennia); the shell is thin. The empirical "joints" (the operation-DSL boundary, energy
> fidelity, fun-tuning) are deferred to where they're *proved* — P1 — not guessed up front.

> **This is the strategic arc.** What's actively being worked on now lives in
> [`../../../BACKLOG.md`](../../../BACKLOG.md) (Now / Next / Later).

## Phase overview
| Phase | Name | Builds | Exit gate (go/no-go) |
|---|---|---|---|
| **P0** | Repo prep + locked contracts | DR-21 tree · `contracts.py` · CI gates | `world.sim` imports with no Evennia; gates green; contracts **frozen** |
| **P1** | **Vertical slice (co-op)** | op×material core · ledger · taught parser · resolver · narrator · **shared-room co-op + basic clock**, behind seams | mechanism resolves everything + conserves; the interaction/format feels right (our call) |
| **P2** | Ontology breadth + coverage | full material/operation matrix · property tests · fuzz · bake | matrix complete; ≥10k fuzz, 0 unresolved / 0 conservation violations |
| **P3** | Perception & zones (§10–15) | `space/*` · per-observer rendering · propagator | crossing the scene fades detail through perception bands |
| **P4** | Full activity scheduler (basic clock ships in P1) | `systems/scheduler` + the durable Activity model | long activities accrue on ticks, interrupt-safe, `@reload`-durable |
| **P5** | Survival systems + rescue | `systems/{fire,warmth,water,shelter,injury,rescue}` · radio FSM · pilot | survive the night ≥3 warmth strategies; rescue reachable ≥4 ways; radio ≥3 paths; pilot death never softlocks |
| **P6** | Instanced runs + co-op interdependence (basic co-op ships in P1) | instance lifecycle/GC · authored interdependence | many instanced runs reset/GC cleanly; ≥1 real interdependence |
| **P7** | Weather arc + ending | `systems/weather` · recap generator | storm arc escalates on the clock; recap reads true; §47 end-to-end run plays |

---

## P0 — Repo prep + locked contracts
**Goal.** A dev-ready repo: the full DR-21 module tree (READMEs + interface stubs, *no behavior*), the
**frozen** `contracts.py`, and **mechanized CI gates**, so every later phase fills bodies behind stable
interfaces. *(This is Task 4 of the current finalize-and-prepare effort.)*
**Depends on.** Nothing — the infra (Docker/Postgres/Evennia/Makefile) already exists.
**Deliverables.**
- The `game/world/sim/**` tree per DR-21 (each package an `__init__.py` + a README citing its DR):
  `contracts.py`, `materials.py`, `conservation/ledger.py`, `effects.py`, `events.py`, `narrator.py`,
  `parser/`, `operations/interpreter.py`, `resolver/`, `space/{zones,perception,direction,sound}.py`,
  `systems/{clock,scheduler,rescue,fire,warmth,water,shelter,injury}.py`, `validation/`.
- **`contracts.py`** dataclasses (`EntityState`, `Part`, `Material`, `Operation` +
  `Predicate/Modifier/EffectSpec`, `ActionAttempt{actor,verb,X,relation,Y,tool,raw}`, `Effect`, `Event`,
  `ActionResult`, the §43 packets) + key signatures (`parse`, `resolve`, `ledger.check`, `apply`,
  operation `evaluate`) as `NotImplementedError` stubs with docstrings.
- `game/world/scenarios/whiteout/` skeleton (`manifest.py`, `build.py`, `objects/`, `materials/`,
  `operations/`, `responses/`, `rescue.def`); `tools/` (`bake.py`, fuzz runner, coverage) stubs;
  `game/tests/{sim,integration}/`.
- **Mechanized gates** wired into `make verify` + the Stop hook + pre-commit: import-linter (no
  Evennia/Django under `world/sim`), a **no-raw-writes** lint (only `apply()` may touch Attributes/Tags),
  a **determinism** lint (no `dbid`/`uuid`/`datetime` in `EntityState`); plus a **`make test-host`** fast
  path (pure `world.sim` pytest without Docker).
**Tests.** A smoke test that `import world.sim.contracts` succeeds with no Evennia; the gates run green on
the stubbed tree.
**Exit gate.** DR-21 tree exists with READMEs; `world.sim` imports cleanly without booting Django;
`make verify` green (config + lint gates + suite); **contracts reviewed and FROZEN** — later changes need
an explicit contract-change note.

## P1 — Vertical slice (co-op, one shared room)
**Goal.** Prove **try-anything → resolves → feels alive** on the smallest real subset — get the mechanism
and the interaction *shape* right before building breadth.
**Depends on.** P0.
**Deliverables** (fill bodies behind P0 contracts):
- `materials.py` + **~25 hand-curated golden materials** (intensive ordinal props; real integer-gram
  mass).
- `operations/interpreter.py` + **~15 operations**, built **plain-Python-functions-first** — write 2–3 as
  functions and **extract the DSL only once repetition is undeniable** (DR-05; do *not* stand up the
  interpreter early).
- `resolver/` tiers **1/3/5** (authored-special stub for the radio, the op×material index keyed
  `(verb, relation, material_of_X, material_of_Y)`, the informative redirect ranked by smallest unmet-
  precondition gap) + the **wall-sensor**.
- `conservation/ledger.py` + the accountable **environment sink** (integer-gram mass, *exact* balance;
  energy as a gate).
- `parser/` — the **taught grammar** `VERB X [RELATION Y] [WITH Z]` + synonyms, possessive/`of`,
  adjective + disambiguation prompts → `ActionAttempt`.
- `effects.py` + the shell **`apply()`** (the single atomic, ledger-gated writer); `narrator.py` + **~50
  curated signature responses**; **~5 objects** (seat, multitool, fire-makings, radio stub, pilot body);
  a stub rescue.
- **Co-op: 2–3 players in one shared room.** All game output routed through the **message propagator**
  seam (trivially "everyone in the room" now; **no raw `msg`/`msg_contents` for game events** — a lint
  enforces it). Reachability via `WorldView.reachable()` (returns "everything in the one room"). Objects
  **tagged with a `run_id`** (one run for now).
- A **basic running clock** (world-time advances + cold ticks) on a heartbeat Script; the *full* activity
  scheduler is deferred. **Defer (behind the seams above, so they're clean extensions — not refactors):**
  perception zones, instanced-run lifecycle, interdependence, weather.
**Tests.** Tier-1 pure pytest (operation interpreter, ledger balances, resolver tiers, redirect ranking);
a small seeded fuzz run (every attempt resolves; 0 conservation violations); the **seeded-replay
determinism** property; **golden-master narration snapshots** (narration↔Effect); a **Tier-2 2-session
integration test** (two players act on the shared room; each sees the other via the propagator).
**Exit gate:**
- **Mechanical:** 0 unresolved attempts in the slice fuzz; ledger balances on every transform; replay is
  byte-identical; the boundary / no-raw-write / **no-raw-output (propagator)** / determinism lints green.
- **Feasibility + format (our call):** the systemic mechanism resolves *everything* tried and conserves,
  and the interaction/presentation is in a shape we like — proving the core is buildable, consistent, and
  extensible behind the seams, so breadth is worth investing in.

*Fun is a **continuous design judgment** we hold throughout — "are we designing toward something fun?" —
not a functional test the slice must pass, and not a friends-playtest (friends see the finished game). We
keep checking it as depth accumulates.*

## P2 — Ontology breadth + coverage
**Goal.** Scale from "fun on a few" to "complete and trustworthy" across the full operation×material space.
**Depends on.** P1 **pass**.
**Deliverables.** The full scene material table; all **~20 operation categories**; property tests per
operation family; the **`solvability-fuzz`** harness (ScriptedBrain: greedy / reckless / random-within-
affordances) + the **coverage definition**; the wall-sensor → authoring-queue loop; the **bake pipeline**
(`ontology-generator` drafts → validate + run the ledger over each transform → bake to the numeric/indexed
runtime form). If DR-05 repetition is now undeniable, **extract the operation DSL** (the deferred joint).
**Tests.** Coverage = the op×material matrix populated + property-tested **plus** a **≥10k-attempt seeded
fuzz corpus** with **0 unresolved, 0 conservation violations, rescue reachable from every sampled state**.
**Exit gate.** Coverage definition met; the bake pipeline produces loadable data; **no silent
truncation** — the wall-sensor queue is drained or its remainder explicitly logged.

## P3 — Perception & zones (§10–15)
**Goal.** The single scene becomes a perceptual space: overlapping zones with separate visibility /
audibility / reachability / direction / detail.
**Depends on.** P2 (object/material core + events).
**Deliverables.** `space/{zones,perception,direction,sound}.py` (pure); Room/Character per-observer
`return_appearance`/`get_display_*(looker)`; reachability gates manipulation (the resolver only binds
reachable nouns); the **message propagator** (rpsystem `send_emote` pattern) rendering each Event per
observer by perception band × loudness × weather-stub.
**Tests.** Tier-1 perception/direction/sound math; Tier-2 per-observer rendering; the reachability gate.
**Exit gate.** Crossing the scene fades camp through perception bands; one action's Event is perceived
differently by near vs far observers; manipulation is blocked beyond reach.

## P4 — Full activity scheduler (+ clock hardening) — LOCKED clock model
**Goal.** The **basic running clock shipped in P1** (world-time + cold ticks). P4 adds the **full activity
scheduler** for timed tasks (durable across `@reload`, partial progress) and hardens the clock.
**Depends on.** P1 (the basic clock), P3 (events/propagator for tick feedback).
**Deliverables.**
- `systems/clock.py` — harden the P1 clock: the **continuously running real-time clock** at a fixed
  real→game pace (~10–20 real-sec per game-minute); a **deterministic logical clock under the hood**
  (time is an input); **no modes, no planning freeze, no fast-forward**; nobody can stall or yank it.
- `systems/scheduler.py` — a long action = an **Activity** persisted to Attributes (survives `@reload`),
  accrues progress per tick, emits tick feedback, routes degraded messages, keeps **partial progress** on
  interrupt; `events.INTERRUPT_SIGNALS` break a pending activity (the running clock itself never stops);
  recompute elapsed from the world clock **on `at_start`** after a reload.
- The **heartbeat Script** (gathers state → calls pure `clock`/`scheduler` → applies ledgered Effects →
  routes events).
**Tests.** Tier-1 `clock.tick`/`scheduler.advance` (pure); the wall-clock-fires-vs-deterministic-tick
property (fuzz drives **logical** ticks, byte-reproducible); Tier-2 `@reload`-durable activities.
**Exit gate.** The clock runs continuously and **cannot be stalled or yanked by any player**; a long
activity accrues on ticks while others act; an interrupt keeps partial progress; activities survive
`@reload`; logical-tick replay is deterministic.

## P5 — Survival systems + rescue + authored packets (radio / beacon / pilot)
**Goal.** The survival loop *and* the win condition — the deep puzzles that make the clock matter.
**Depends on.** P2 (op×material), P3 (perception for signals), P4 (the running clock — cold/warmth/
injury and signaling are all time-driven).
**Deliverables — survival systems (§31–36).** `systems/{fire,warmth,water,shelter,injury}.py`: the fire
state ladder + hazards; warmth as fire **plus** windbreak/shelter/insulation/huddling/body-heat, incl.
the **no-materials warmth floor** (a competent party survives one night without fire, so fire-failure is
recoverable); water safety gated by container state; shelter by properties (partial shelters count);
systemic improvised injury/medicine.
**Deliverables — rescue.** `systems/rescue.py` — additive confidence, channels drawing on **distinct** scarce
resources, `rescued = weather_window AND confidence ≥ threshold`, **monotonic & always-reachable**; the
**radio FSM** packet (`dead → powered_static → weak_receive → weak_transmit → two_way_no_location →
useful_contact`, gated by power, an improvised-antenna quality from material/length/placement, and
location info with ≥3 clue paths); the beacon; the **pilot** (condition-scripted, deteriorating info
source; tending has a real opportunity cost; every fact ≥3 clue paths; death → a body, never a softlock).
**Tests.** Survival property tests (the warmth floor guarantees a survivable night; bad fire ideas fail
informatively); rescue arithmetic (monotonic, reachable); the **solvability oracle** (rescue reachable
from every sampled state); radio ≥3 solution paths; pilot ≥3 clue paths per fact; the **global-softlock
check** (no spend/burn into an unwinnable state).
**Exit gate.** A competent party survives the first night via **≥3 warmth strategies**; rescue reachable
via **≥4 distinct combinations**; no single object required for all endings; the radio puzzle solvable ≥3
ways; the pilot's death never softlocks.

## P6 — Instanced runs + co-op interdependence (LOCKED model)
**Goal.** **Basic shared-room co-op shipped in P1.** P6 makes it **instanced** (many parties, each its own
run that resets) and adds **first-class co-op interdependence**.
**Depends on.** P1 (basic co-op + run-tagging), P3 (the graded propagator), P4 (the full scheduler/clock),
P5 (full scenario).
**Deliverables.** The **instance lifecycle** (spawn from a prototype set, tag `run_id`, persist in
Postgres, reset by deleting tagged objects via `search_object_by_tag`, a reaper Script sweeping tag-
orphans — the **EvAdventure dungeon-contrib** pattern); concurrent action handling on the shared running
clock; **≥1 first-class co-op interdependence** (one holds/raises the antenna or relays a scout's landmark
while another transmits); the graded propagator across players.
**Tests.** Tier-2 instance create/persist/reset/GC; multi-session concurrent actions on one clock; the
interdependence path; the decision-trace (DR-20) still resolves a wrong narration under multiplayer.
**Exit gate.** 2+ players act concurrently in one instanced run on the shared running clock; ≥1
interdependence genuinely **requires** cooperation; instances reset cleanly and orphans GC.

## P7 — Weather arc + auto-generated ending
**Goal.** The dramatic curve and the closing story.
**Depends on.** P4 (the clock drives the arc), P5 (rescue); P6 optional.
**Deliverables.** `systems/weather.py` (light → steady → heavy → near-whiteout → night, degrading
visibility/audibility/fire/tracks/rescue; 2–3 seeded timed beats — a search plane that misses you, the
pilot's last lucid line); the **auto-generated end-of-run recap** (deterministic, from the run's event log
— the optional nice-to-have).
**Tests.** Weather-arc property (monotonic escalation; degrades the right channels); the recap matches the
actual event log (narration↔Effect at the story level).
**Exit gate.** A full session shows the storm escalating on the running clock and pressuring rescue; the
recap reads true to what happened; the **§47 minimal end-to-end run** plays through (wake → free yourself
→ meet the pilot → salvage a seat → make a fire → improvise a radio antenna → survive / get rescued).

---

## Cross-cutting (holds in every phase)
- **One enforced mutation path:** all state change is ledger-gated Effects via `apply()` (atomic); the
  no-raw-write lint stays green.
- **Determinism:** seeded RNG for all ids/draws; no `dbid`/`uuid`/`datetime` in `EntityState`; the
  seeded-replay property stays green.
- **Validation gate (§44):** `world/sim/validation` content-lint at load / CI / `make verify`.
- **NO runtime LLM, ever:** the LLM is build-time authoring only (`ontology-generator` → validate →
  bake). Gaps from the wall-sensor are filled **at build time**, never by a runtime call.
- **Authoring discipline (§43):** puzzle-critical objects authored from packets as *goals with ≥3
  clue/solution paths*; everything else from cheap-object + materials + operations.
- **Vision guardrail:** lenses/reviews optimize *within* the locked vision; they never re-open a locked
  decision (clock, session model, no-runtime-LLM, taught grammar).

## What changed from the old §42 "Pass 1–10"
The previous order built the **multiplayer tick engine first** and listed a runtime **"server-side LLM"**
— both now wrong. This roadmap is **slice-first** (prove fun before breadth), puts the **running real-time
clock** at **P4** (not first), **instanced synchronous co-op** at **P6**, and has **no runtime LLM
anywhere**.
