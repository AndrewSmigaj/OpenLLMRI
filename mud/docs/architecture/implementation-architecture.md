# Whiteout — Implementation Architecture

> **Status: v4 — current; a work in progress, amended through the DR register.** The full implementation blueprint for Whiteout, derived from
> `docs/scenarios/whiteout/GDD.md`. Supersedes the older sub-docs where they conflict
> (`overview.md`, `llm-integration.md`, `tick-and-scheduler.md`, `perception-model.md`, `testing.md`
> remain valid as focused views). **Current decisions: the engine is 100% deterministic and never calls a
> language model (models build the world and play from outside — GDD §3 rules 2 and 5; the radio
> voice's judgement is the one exception, DR-02); the world clock is a continuously running real-time clock;
> sessions are instanced, synchronous co-op runs; input is the taught grammar (§25a / DR-08).** The
> design each decision serves is in `docs/design/` (the index: `docs/design/README.md`); the current
> design decisions, all in one place, are `PLAN.md` §5. This document is scored in
> `review/30-certainty.md` against its **decisions register (§2)**.

## 0.5 Hardenings from the lens review (v2)
Six **additive hardenings** from `review/20-lens-findings.md` (none changes the design or goals — they
make stated guarantees *enforced*):
1. **One enforced, atomic, ledgered mutation path** (closes the lone RED, AR15). `apply()` is the *only*
   writer, behind a guarded choke-point + a lint forbidding raw `obj.db.x =` writes; **all** state change
   — including tick/`systems/*` — is expressed as **ledger-gated Effects**; apply is wrapped in
   `transaction.atomic`, updating the Attribute **and** its Tag mirror together. (DR-10, DR-11)
2. **Operations have one interface; verbs are plain Python** (AR8/AR13). Every verb is a Python handler
   behind the same interface, sharing one toolkit; the volume axis — objects, forms, materials,
   responses — is data in tables. There is no operation DSL. (DR-05, DR-05b)
3. **Determinism is an enforced contract** (IM10/AR4). All ids + random draws come from the per-run
   seeded RNG; **`dbid`/`uuid`/`datetime` are forbidden in `EntityState`** (lint); a double-run-same-seed
   property test guards it; fuzz/replay run on the pure core. (DR-12)
4. **Within-run debris policy + `Part.mass`** (IM8/AR11). Trivial derived objects are capped/merged
   (stackable scraps) and ignored debris auto-despawns; WorldView is zone-scoped; `Part` carries mass so
   removals balance. (DR-06)
5. **Accountable environment sink** (AR11). The sink tracks total mass/energy absorbed and may only grow;
   per-channel, reviewable — not a silent catch-all. (DR-11)
6. **The quality gate is named** (IM5/IM12). Physics/conservation/solvability are enforced gates;
   **delight is gated by the golden set + playtest**, and AI-authoring loops are bounded by it. (DR-18)

## 0.6 Refinements from the research (v3)
Six refinements from `review/40-research-notes.md` (Evennia source + Inform 7/TADS/PDDL/qualitative-
physics literature):
1. **Conserved quantities are REAL numbers, not ordinals (DR-11/DR-04 — the one correction).** Ordinals
   can't carry a balance. **Mass is a real integer count of grams (`mass_g: int`)** (kills float drift, à la
   Factorio/ONI); **ordinals are used only for intensive properties/gates**; **energy is a gate, not an
   ordinal balance.**
2. **Specificity dispatcher (DR-05).** Rule *precedence* is where declarative systems leak (Inform 7
   lesson): make it explicit/deterministic — **most-specific rule wins, ties broken by a declared
   priority.**
3. **Cache-invalidation-on-rollback (DR-10).** Evennia updates in-memory Attribute/Tag caches eagerly
   with no rollback hook; `apply()` must `reset_cache()` touched handlers on rollback, and the lint must
   catch in-place `SaverList/SaverDict` mutation.
4. **Recompute activity progress on `at_start` (DR-14)** from the persisted deadline + world clock,
   not a timer estimate.
5. **Instance from a prototype set; reaper sweeps tag-orphans (DR-15).** Pattern confirmed by the
   official **EvAdventure dungeon contrib** (near-identical) and Arx Shardhaven.
6. **Relations & gaps, not absolute thresholds (DR-04/DR-09).** Outcomes key off cross-factor rank
   relations + graded gaps; a failed attempt is answered with the physics of why, never a list of
   verbs (DR-08c).

---

## 1. Architectural principles
1. **Functional core / imperative shell.** All game *rules* are pure Python in `game/world/sim/**`
   (no Evennia/Django imports); Evennia is the shell that owns IO, persistence, sessions, and time.
2. **Deterministic runtime.** No model inference, no wall-clock dependence, no unseeded randomness in
   resolution. Same inputs + same seed → same result (so the fuzzer can replay).
3. **Data-driven content.** Materials, objects, forms and responses are **data**, not code branches;
   verbs are Python handlers behind one interface (DR-05b). Adding a material is a data edit; adding a
   verb is a new handler; neither edits the resolver.
4. **Single source of truth.** Persistent state lives in Evennia Attributes (Postgres). The pure core
   operates on *snapshots* and returns *Effects*; the shell is the only writer.
5. **One enforced mutation path.** State changes *only* via Effects applied by `apply()`, gated by the
   conservation ledger, wrapped in a DB transaction. This is **enforced, not conventional**: a single
   guarded choke-point, a lint/`engine-reviewer` rule forbidding raw `obj.db.x =` / `.attributes.add`
   anywhere else, and **all** state change — including tick/`systems/*` updates — routed through it as
   ledger-gated Effects. Nothing mutates state any other way.
6. **Everything resolves.** Every parsed action returns an `ActionResult` (success, partial, or the
   physics of why — DR-08c). Unhandled-but-sensible attempts log to the wall-sensor for build-time
   authoring.

## 2. Decisions register (the spine — each scored in `review/30-certainty.md`)
Each entry states the current decision. Lettered entries (DR-05b, DR-14b …) amend their parent and are
written out below the table or in the section that owns them.

| ID | Decision | Choice (one line) |
|----|----------|-------------------|
| DR-01 | Core/shell split | pure `world/sim` ⟷ Evennia shell via dataclass contracts |
| DR-02 | Runtime LLM | the engine never calls a language model; deterministic end-to-end. Models play characters from outside, as players, through the grammar (GDD §3 rules 2 and 5). One exception: the radio voice judges whether it has been told enough to find the party, by criteria the game gives it — its act, logged like a player's (2026-09-27; document 14 §3.3) |
| DR-03 | Content as data | objects, forms, materials and responses are tables, loaded at boot (DR-17a) |
| DR-04 | Material model | ~25 ordinal property vectors for intensive properties (gates and rank relations only); conserved quantities are real numbers — mass in integer grams; hand-curated golden table; ordinal→numeric map at load |
| DR-05 | Operation model | one interface; **verbs are Python handlers** sharing one toolkit; the volume axis (objects, forms, materials, responses) is data; no DSL (DR-05b); deterministic specificity dispatch |
| DR-06 | Object model | cheap objects; parts (with **mass**) → derived objects; provenance; **within-run debris cap/merge** |
| DR-07 | State in Evennia | Attributes for payload + **Tags** for queryable axes; single source of truth; Tag mirror updated in the same transaction as the Attribute |
| DR-08 | Parser | deterministic taught grammar `VERB X [RELATION Y] [WITH Z]` + synonym tables → `ActionAttempt{verb,X,relation,Y,tool}`; the RELATION slot makes two-object actions first-class; no NL model; tolerance for how people type (DR-08b); feedback is clarification only, never a menu (DR-08a, DR-08c) |
| DR-09 | Resolver | resolution tiers + an operation×material index keyed by `(verb, relation, material-of-X, material-of-Y)` + tier-4 generic physics + the physics of why, never a list of verbs (DR-08c) + wall-sensor |
| DR-10 | Effects/Events + apply | **the one enforced, total, atomic mutation path**: guarded choke-point + lint; `transaction.atomic`; tick/systems updates are Effects too |
| DR-11 | Conservation ledger | pre-commit balance gate inside apply(); **accountable** environment sink (tracked, monotonic) |
| DR-12 | Determinism/seeding | per-run seeded RNG for all ids + draws; `dbid/uuid/datetime` forbidden in `EntityState`; double-run-same-seed test; pure replay |
| DR-13 | Perception/zones | zone = attribute in a Scene-Room; per-observer `return_appearance`; propagator (built in a first version, DR-13a) |
| DR-14 | Clock/scheduler | **continuously running real-time clock** at 15 game-minutes per real minute; fast forward at about 150× by the players' agreement (DR-14b); activity scheduler; activities persisted (not `.ndb`); deterministic logical clock under the hood |
| DR-15 | Session/instance | **instanced, synchronous co-op runs** — one sitting of two or three hours covering about a week of game time (DR-15a/15b); explicit lifecycle (create/persist/reset/GC) |
| DR-16 | Rescue | as document 14 §3: three ways home — the radio, a signal a plane can see, surviving long enough; the radio, its signal and the searchers' flyovers are world state and scheduled processes; no rescue number is shown or kept as a score (§8) |
| DR-17 | Build pipeline | author in the tables → validate (`make validate`, + the ledger) → load at boot; no bake step (DR-17a) |
| DR-18 | Coverage/fuzz | the probe corpus (every `pass` probe green, the passing count never drops) + the seeded fuzz; the solvability oracle (DR-18a) |
| DR-19 | Test strategy | Tier-1 pure pytest + Tier-2 Evennia integration; property tests for invariants |
| DR-20 | Observability | a per-resolution decision trace (tier hit, ledger result, events) |
| DR-21 | Module/file layout | `world/sim` pure core, `game/` shell, `world/scenarios` content, build tools (§11) |
| DR-22 | Vertical slice and its seams | the slice (built June–July 2026) and every system after it are built behind seams — the message propagator, `WorldView`, the logical clock, the run tag — so each deferred system is an extension, not a refactor (§13) |
| DR-23 | Presentation | scene-as-prose `look` (salience weights what is VISIBLE — amended by DR-24); `look at X` ≡ `examine X` via ONE pure renderer (`presentation.py`); appearance is state-conditioned scenario content; attachments render physically (DR-09a phrases), never as data — full spec: [`presentation.md`](presentation.md) |
| DR-24 | Containment & discovery | loot lives INSIDE things (Evennia nesting = honest hiding); ONE reveal rule (`open` OR `searched`, recursive through revealed); deterministic finds; `TRANSFER` effect (additive) relocates via hook-free `move_to`; taught `take/get` owns acquisition — full spec: [`containment.md`](containment.md) |
| DR-25 | Clothing & warmth | wearability DERIVED from materials (never a whitelist); worn = `state["worn_by"]`, stays in inventory; warmth = Σ round(insulation × capped mass) in insulation-grams (intensive×extensive, not ordinal-summing) → banded words on `inventory`/self-examine; unlimited linear layering v1 — full spec: [`clothing-warmth.md`](clothing-warmth.md) |
| DR-26 | Ontology closure | **forms** on every minted object + **derived capabilities** (material × form × state, capped, authored wins) + tier-4 generic physics + the **probe corpus** as the coverage definition — full spec: [`ontology-closure.md`](ontology-closure.md) |
| DR-27 | Activities & processes | *(designed 2026-09 in `docs/design/06-time-sleep-and-the-clock.md`; promoted here when that document is finalized)* attended activities with start/tick/interrupt/complete feedback + unattended processes (fire, drying, cold), both driven by the single persistent heartbeat; deadlines in world-time, progress in Attributes |
| DR-28 | Moral & social logging | *(designed 2026-09 in `docs/design/15-moral-and-social-layer.md`; promoted here when that document is finalized)* ownership + spatial witness in the event log; no moral tags — a language model reads the playthrough after the run (2026-09-28); observational only, never a reward; no run-level consent flag — the engine never gates physics (2026-09-16) |

> **DR-14a / DR-14b — the clock (2026-09-07, 2026-09-17, 2026-09-27; design: document 06).** The
> clock runs continuously and never freezes, at **15 game-minutes per real minute**. **Fast forward**,
> proposed and agreed by the players, runs it at about **150×**; awake players can stay in it, seeing
> events faster, and type a command to slow it when they want to act. A player waking or any
> non-ambient event drops it back to 15×; ambient events do not. Sleeping players can chat out of
> character. The numbers are tuned by playtesting. Being awake is being on watch. Time controls are
> taught in the pre-scenario tutorial.
>
> **DR-15a / DR-15b — the run (2026-09-07, 2026-09-17, 2026-09-27; design: documents 13, 19, 21).**
> A run is **one sitting of two or three hours** covering about a week of game time; the players can
> pause it and return. An **escalation ladder** makes each day harder (document 13), with **no hard
> time-window barriers** and **no set arc** — what to do is the players' call. Up to five play; a seat
> nobody plays is a dead character whose clothes and pockets can be searched; agents may play seats. A
> missing player's character goes catatonic, sits down and stares; the others can keep it alive, and it
> can die.
> **The only endings are rescued or dead**; the run ends when the party is dead, of anything. **A dead or
> rescued player goes to the Warming Hut** and can go back in as a silent watcher (a ghost): unseen and
> unheard by the living, hearing other watchers; anyone can use the out-of-character chat. There is no recap.
>
> **The design decisions that shape the engine** (all in `PLAN.md` §5, each designed in its document):
> the aircraft is the 206-class single with the four-seat interior — seats 1A/1B/2A/2B and the right
> seat, a hat shelf, a cargo net and a jammed cargo door — and each player starts with a different
> clothing, injury and pockets draw; luggage has real contents (document 16). The whole valley — every outdoor
> place — is in the first complete run (document 01). The season is the first week of
> October (document 13 §4.2). The pilot starts the run dead (document 12). An agent sees exactly what
> a human sees; structure goes to the log only (document 20). The look is a title line, the prose,
> who is here and the exits as entities in prose (document 03). **Exits are entities**, each with its
> own name, synonyms and verb (`walk west`, `walk to the birch grove`, `climb up`, `enter the tail`),
> travel time and state; movement is an attended activity with events. **Groups** ("a pile of
> clothes") form when several things share a place and a kind; `look at the pile` lists them; taking
> dissolves them (document 03). The bear, some bigger animals and a few birds act, on engine behaviour
> rules or played by a lightweight model from outside; other wildlife is events and sign (GDD §3 rule
> 5, document 23). Dangerous places injure, never kill outright; the seeded dice are never shown — the player reads
> what happened (2026-10-02).
> Sweat is not a meter: it is wet clothing draining warmth later. **No moral tags:** acts are
> not tagged; a language model reads the playthrough after the run (2026-09-28).
>
> **DR-05b (2026-09-07) — verbs stay Python; there is no operation DSL.** Verbs are a small set at any
> moment (~40 physical operation categories today — grown by evidence without a ceiling, never a fixed
> list), each with real physics, and the handlers share one toolkit (`_helpers`). The volume axis —
> objects, forms, materials, responses — is DATA (tables), and that is where authoring scales.
> `operations/interpreter.py` stays a stub; no interpreter will be built. Handlers may read small
> tuning tables; that is not a DSL. Specificity dispatch: authored > handler > tier-4 physics > the
> physics of why.
>
> **DR-17a (2026-09-07) — no bake step.** `load_materials` maps ordinals to numbers at boot; the tables
> (`objects.py`, `materials/table.py`, `zones.py`, `spaces.py`, `appearance.py`, `responses/`) load
> directly. The pipeline is author → **validate** (`make validate`, real content lint over the tables)
> → load. The §43 packet dataclasses in `contracts.py` remain (frozen contract, additive rule) but are
> not part of the authoring model; the four authoring guides describe the tables. (`tools/bake.py`
> is deleted by PLAN B6.)
>
> **DR-18a (2026-09-07) — coverage is the probe corpus + the fuzz.** Every `status: pass` probe green
> (CI), the passing count never drops (`probes/BASELINE`), plus the seeded fuzz (every attempt
> resolves, every effect conserves). Probes cite a census row, a room document, a phrasing-corpus
> line, or Andrew's approval — never self-graded. The wall-sensor is persisted (`gaps.jsonl`) and
> feeds the queue.

---

## 3. System overview

```
                         ┌─────────────────────────── Evennia shell (game/) ──────────────────────────┐
 player text ──telnet──► │ Command (cmdset)                                                            │
                         │   └─ Parser ──► ActionAttempt ──► resolve(attempt, world_snapshot) ─────────┼──┐
                         │ Object/Room typeclasses  ◄── apply(effects) ◄── ActionResult ◄──────────────┼─ │
                         │ Attributes (Postgres)  •  Tags (queryable axes)  •  heartbeat Script         │  │
                         └────────────────────────────────────────────────────────────────────────────┘  │
                                                                                                           │
   ┌──────────────────────── pure core (game/world/sim/**, no Evennia) ─────────────────────────────────┐ │
   │ parser/   resolver/ (§26 tiers, op×material index)   operations/ (handlers)      materials/         │◄┘
   │ conservation/ (the ledger + environment sink)   effects/ events/   narrator/ (templates)           │
   │ space/ (perception)   systems/ (clock, scheduler, rescue, fire, ...)   validation/                 │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                   ▲ loads
   ┌──────────────── content tables (game/world/scenarios/whiteout/, loaded at boot) ──────────────────┐
   │ objects.py   materials/table.py   zones.py   spaces.py   appearance.py   responses/   rescue.def   │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                   ▲ built by
   ┌──────────────── build-time tools (offline; LLM-assisted; never at runtime) ───────────────────────┐
   │ ontology-generator → validate (+ ledger);   probes;   solvability-fuzz;   golden-table curation    │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Runtime data flow (one action):** text → Parser → `ActionAttempt` → `resolve()` (pure) →
`ActionResult{effects, events, narration}` → shell applies effects (ledger-gated) → routes events →
prints narration. No IO or LLM inside `resolve()`.

---

## 4. Content & data model

### DR-04 Materials
A material is an **ordinal property vector**. Ordinals (`none < very_low < low < med < high < very_high
< extreme`) make authoring fast and LLM reasoning reliable; the engine maps ordinals → a fixed numeric
scale for arithmetic.
```python
# pure: world/sim/materials.py
ORDINAL = {"none":0.0,"very_low":0.15,"low":0.3,"med":0.5,"high":0.7,"very_high":0.85,"extreme":1.0}
@dataclass(frozen=True)
class Material:
    id: str
    props: dict[str, float]      # loaded: ordinals mapped to numbers at boot
    # cut_resistance, tear_resistance, bend_resistance, burnability, ignition_difficulty,
    # smoke_toxicity, insulation, conductivity, edibility, potability, absorbency, ...
```
The **canonical source** is the hand-curated `materials/table.py` (the quality anchor); `load_materials`
maps its ordinals to numbers at boot (DR-17a). The table grows by evidence without a ceiling.

**Intensive (ordinal) vs extensive (real) — v3 correction (DR-04/DR-11).** A material's `props` are
**intensive** properties (resistances, burnability, insulation) — these are the **ordinal** values, used
only as *gates and rank-relations*, never summed. **Conserved extensive quantities — mass above all —
are real **integer grams** and live on `EntityState.mass_g` /
`Part.mass_g` (ints — no float mass), **not** as ordinals. Outcomes are driven by **rank relations and graded gaps** between
intensive properties (e.g. `tool.edge − target.cut_resistance`), not by arithmetic on ordinals
(measurement theory: ordinals don't support true addition/distance). This split is what lets the ledger
balance (real mass) while authoring stays fast (ordinal properties).

### DR-05 Operations (the heart)
An operation is a unit of behavior registered behind **one interface**. **Verbs are Python handlers**
(`operations/handlers/`, DR-05b), each with real physics, sharing one toolkit (`operations/_helpers.py`)
and free to read small tuning tables; the volume axis — objects, forms, materials, responses — is data
in tables, and that is where authoring scales. There is no operation DSL and no interpreter. The
`Operation` dataclass and its `Predicate`/`Modifier`/`EffectSpec` parts stay in `contracts.py` as part of
the frozen contract (additive rule):
```python
@dataclass(frozen=True)
class Operation:
    id: str                      # "cut"
    verbs: tuple[str, ...]       # synonyms feed the parser: cut, saw, slice
    roles: tuple[str, ...]       # ("actor","target","tool?")
    preconditions: tuple[Predicate, ...]   # over EntityState/Material/zone
    modifiers: tuple[Modifier, ...]        # qualitative: harder if frozen; slower if cold_hands
    effects: tuple[EffectSpec, ...]        # separate(target)->outputs; conserve(...)
    duration: DurationSpec                 # f(resistance, tool, modifiers) -> minutes
    partial: PartialSpec                   # budget<required -> progress
    failure: FailureSpec                   # which physical explanation to emit
```
Stateful or multi-step logic — the radio, the `systems/*` (fire, warmth, water, injury, weather) — is
plain Python behind the same interface.
**Deterministic specificity dispatch (v3 — DR-05).** When several rules could fire, precedence is the
classic failure point (the Inform 7 leaky-rule-ordering lesson). Resolution is therefore **explicit and
deterministic: the most-specific rule wins** (authored > handler > tier-4 generic physics > the physics
of why), **ties broken by a declared integer priority** — never by file/registration order. This makes
"which rule fired" predictable, traceable (DR-20), and replayable (DR-12).

> **DR-05a (attachment honesty, 2026-07) — destructive extraction.** In the D12 cut rule, **a part's
> attachment gates HOW its material comes free, never WHETHER** (the material gate stays first — a dull
> blade is still dull). Cut/tear on a part whose material the tool defeats
> but whose attachment is mechanical (pryable-class) now SUCCEEDS destructively: the part is removed
> and its full mass minted as `{material}_scrap` ×3 (part-scoped derived ids like
> `seat:cushion_scrap0:loose`; the ledger balances exactly; a `residue_{part}` state attribute
> records the wrecked fastener so the aftermath narration is a recorded fact — DR-11). **Pry keeps
> its exclusive value**: the only intact single-piece removal off a mechanical fastener
> (`outputs_when_removed`) — intact-vs-scrap matters for later content (insulation area, whole
> covers); no uses built yet. **`fixed`/unknown attachments stay integral** — refuse-with-
> explanation; authors opt INTO extractability by naming a real attachment. Nothing narrates damage
> that no Effect recorded. `break` intentionally unchanged (extraction defers to cut/tear/pry);
> destructive-is-slower is future tuning once durations land (PLAN E1).
>
> **DR-09a (attachment honesty, 2026-07) — explain the physics.** Attachment-mismatch refusals explain
> WHY in physical terms via a content-tunable phrase map in the scenario responses
> (`attachment.explain.*` / `attachment.residue.*` — Andrew owns the voice; the pure helper
> `_helpers.attachment_phrase` reads it through `narrator.get`). The answer names the thing and its
> physical state, never another part to try, a method or a tool (DR-08c). The shipped code still
> appends a sibling near-miss (`_helpers.sibling_hint`, the `attachment.hint.*` phrases) and a coarse
> `generic_redirect`; PLAN B13 removes the first and replaces the second with the tier-4 physics.

### DR-06 Objects
Cheap by default; behavior derives from operations over materials.
```python
@dataclass
class EntityState:               # the snapshot the pure core sees (mirrors an Evennia Object)
    id: str; name: str
    materials: list[str]
    parts: list[Part]            # Part{id, material, mass_g, attachment, outputs_when_removed}
    tags: list[str]
    mass_g: int                  # extensive: integer grams (DR-11)
    state: dict                  # temperature_c, wetness, contamination{}, damage, ...
    provenance: list[str]        # GDD §24: where it came from
    owner: str | None
```
Removing a part yields a **first-class derived object** built from the part's `outputs_when_removed`,
with conserved state and mass (`Part.mass_g` lets the ledger balance the removal, DR-11). An object
that needs more than the shared operations — the radio — carries authored rules on top, resolved at
tier 1 (DR-09); there are no per-object packets (DR-17a).

**Within-run debris policy (v2 hardening — DR-06).** Because salvage mints objects, a run's
`room.contents` could balloon (idmapper RAM + linear WorldView/Tag-query growth). Mitigations: trivial
identical derivatives are **stackable** (a heap of fabric scraps is one object with a count, not twenty),
ignored debris **auto-despawns** after a grace period (with a "you could still grab the scraps" hint so
nothing vanishes mid-use), and the **WorldView is built per zone, not per whole scene**. Instanced GC
(DR-15) is the backstop, not the only bound.

### DR-07 Where state lives in Evennia
- **Attributes** hold each object's payload (`materials`, `state{}`, `parts`, `provenance`). Great for
  per-object data; **idmapper-cached**.
- **Tags** mirror the **queryable axes** (each material, current zone, key affordances) because Evennia
  Attributes are *not queryable by value* (Evennia research). "Find all metal things in the cabin" = a
  Tag query, not an Attribute scan.
- Attributes are the **single source of truth**; `EntityState` is a transient snapshot built from them
  per resolution and discarded after Effects apply.

---

## 5. The runtime engine (deterministic)

### DR-08 Parser (the taught grammar)
A classic IF/MUD parser, no model. Input is the **taught command grammar** (GDD §25a),
`VERB  X  [RELATION  Y]  [WITH Z]`, pitched at action granularity. Pipeline: tokenize → match verb
against the **synonym table** (built from every operation's `verbs`) → bind slots by the grammar: **X**
the primary target (a thing *or a part*; possessive and `of` both parse), an optional **RELATION**
preposition (`off`, `onto`, `against`, `between`, `into`, `from`…) binding a **second object Y**, and an
optional **WITH** tool **Z** → resolve each noun phrase to **reachable** entities (name/alias/tag match,
adjective + disambiguation prompts on ties) → emit `ActionAttempt{actor, verb, X, relation, Y, tool,
raw}`. **The RELATION slot is what makes two-object actions first-class** (`cut … off …`, `wedge …
against …`, `tie … between …`), rather than single-target-only commands. An unknown word or an unseen
noun gets a clarification, never a hard error and never a list (DR-08c). Richness comes from *rule
coverage* and the **generative** operation×material engine — not parser cleverness or an enumerated
command list.

> **DR-08a (2026-07, restated by DR-08c) — disambiguation.** A multi-hit noun returns
> `Disambiguation{term, options}`; each `DisambigOption` carries its concrete `entity_id`/`part_id`
> (**ADDITIVE** contract change; pinned by `test_contracts.py`). Ties are resolved silently first
> (DR-08b); a true tie asks `Which X do you mean?` and nothing more (DR-08c). The shipped code still
> answers a true tie with a numbered menu — `cmd_act.py` (a module-level pending map, re-parsing the
> whole line with `parse(..., bindings={term: (entity_id, part_id)})` when `CmdNoMatch` catches a bare
> number) and `cmd_items.py` (stock `get`/`drop`) — until PLAN B13 replaces it with the question.

> **DR-08b (parser tolerance, 2026-09-07) — the grammar absorbs how people type.** Measured
> against the real parser, taught-condition agent phrasings parsed 32–58%; the six mechanical fixes
> below lift that into the 90s without free-text NLP (`ontology-closure.md` §5): (1) verb + PARTICLE
> forms resolved positionally (`cut open X`, `pick up X`, `put on X` → wear — a relation word right
> after the verb is a particle only if the pair is listed, else it stays a relation); (2) multi-word
> relations matched greedily (`out of`, `on top of`) + the missing single ones (over, through, across,
> behind, beside); (3) a first-token SYNONYM table seeded from the samples; (4) **state the act, not
> the aim** — purpose clauses (`… to VERB …`, `for …`, `so …`), meta prefixes (`try to`, `see if`)
> and adverbs are dropped; `use X to VERB Y` rewrites to `VERB Y with X`; (5) body parts → the actor,
> `it` → the last bound noun (an ephemeral per-caller binding); (6) nouns bind the
> WHOLE phrase before the possessive split (`canteen of water`), then the longest known prefix.
> **Disambiguation is resolved silently first**: exact matches beat partial ones, three identical
> shards pick the first (a tie that doesn't matter — Inform's "does the player mean"), a held thing
> wins the tool slot; a question only for a true tie (two different seats). **Failures are told
> apart**: an unknown word, an unseen noun (X=None — the resolver says so), and a verb that doesn't fit
> a thing (the tier-4 physics); what each says is DR-08c. `use X on Y` dispatches through capabilities
> to the real verb. `and`/`then` split a line into acts. Contract: `ParseError.kind` and
> `Reachable.held` added (ADDITIVE).
>
> **DR-08c (Andrew, 2026-09-16 and 2026-09-27) — feedback is clarification only; the game never offers
> options.** The game never offers a set of actions, never lists what is reachable, never names a verb
> the player did not type: an unknown word → `I don't understand 'X'.` plus a pointer to `help
> grammar` (if the game could suggest the word it already knows it — the synonym table absorbs it;
> every unknown word is logged to the wall-sensor); an unseen noun → `You don't see any 'X' here.`
> (never naming what IS here); a verb that doesn't fit → the tier-4 physics, never another verb; a true
> tie → `Which X do you mean?` and nothing more (no list — listing the reachable candidates would give
> away hidden things); silent disambiguation first still holds. `use X on Y` resolves silently as the
> real operation. `make` is the one aim-verb: vague, it asks how; given the means, it performs the act
> they imply (document 04 §3.9). `help grammar` shows the forms with one example each; there is no
> `help verbs`. **Common sense is hinted** (2026-09-27): when a player misses what any person would
> know, the world says why in its own voice — a reason, never a list of options. Why: listing gives
> away the puzzles, and for an LLM agent offering options changes how it thinks (Andrew's LLM-MRI
> finding). The shipped parser nudge, the verb-list redirect, the numbered menus and `help verbs` are
> still in the code until PLAN B13 lands.

### DR-09 Resolver (`resolve(attempt, world) -> ActionResult`, pure)
```
resolve(attempt, world):
    candidates = tiers in order:
      1 authored-special   (an object's authored rule, e.g. the radio)
      2 object-rule        (rare per-object override)
      3 operation×material (THE WORKHORSE — indexed lookup: (verb, relation, material_of_X, material_of_Y))
      4 generic-physics    (fallbacks: mass/temperature/containment defaults)
      5 the physics of why (DR-08c — never another verb, never a list)
    for tier in candidates:
        r = tier.try(attempt, world)
        if r is not None: 
            trace(tier, r)                 # DR-20 observability
            return r
    log_wall_sensor(attempt, world)        # DR-18 build-time queue
    return generic_redirect(attempt, world)
```
The **operation×material index** is a dict keyed by `(operation_id, relation, material_of_X,
material_of_Y)` → the operation schema + any material-specific tuning; lookup is O(1). For single-object
actions `relation` and `material_of_Y` are `None`, so the common case is effectively `(operation_id,
material_of_X)`; **two-object (relational) actions** — `cut … off …`, `wedge … against …` — key on the
full tuple, which is how the engine *generates* outcomes for **pairs** of materials (the seat's fabric
*against* the door's steel) instead of treating the second object as scenery. Partial success returns
`ActionResult(partial=True, duration_minutes=budget)`. The resolver is pure: it reads `world` (snapshots)
and returns Effects/Events — it never writes.

**When no rule fires (DR-08c).** The answer is the physics of why the attempt does not work, drawn
from the things' properties — never another verb, never a list of what is reachable — and the attempt
is logged to the wall-sensor.

### DR-10 Effects & Events
- **Effect** = the only state-mutation instruction (`set_attr`, `adjust_attr`, `create_object`,
  `remove_part`, `consume`, `move_zone`, `set_owner`). The shell's `apply(effects)` is the **single
  enforced writer** — and "enforced" is mechanical, not conventional (v2 hardening, C1):
  - a **guarded choke-point**: only `apply()` touches Attributes/Tags; an `engine-reviewer` lint rejects
    any raw `obj.db.x =` / `.attributes.add` / `.tags.add` elsewhere in the codebase;
  - **`transaction.atomic`** wraps the whole Effect set (all-or-nothing; no torn world on failure), and
    each Effect updates the Attribute **and** its Tag mirror **together** inside that transaction (closes
    the DR-07 stale-Tag race);
  - **tick/`systems/*` updates are Effects too** (stamina, cold, fire) — batched per tick and ledgered —
    so no survival state escapes conservation (closes the AR11 tick gap).
  - **cache-invalidation-on-rollback (v3 — Evennia footgun):** Evennia updates its in-memory
    Attribute/Tag caches *eagerly with no rollback hook*, so the ledger must run **before** any write
    (it does), and on a rolled-back transaction `apply()` calls `reset_cache()` on every touched handler;
    the lint additionally treats in-place `SaverList`/`SaverDict` mutation as a write it must reject.
- **Event** = a perceivable happening (`speech`, `impact`, `activity_tick`, `fire_state_change`, …)
  routed to observers by perception band × loudness (DR-13) and used as activity-interrupt signals (DR-14).

### DR-11 The conservation ledger (flagship invariant)
Runs **inside `apply()`, before commit**. Given the pre-state and the proposed Effects:
```
ledger.check(pre, effects):
    post = simulate(pre, effects)                 # in-memory, no writes
    assert material_identity_preserved(pre, post)
    assert balanced(mass, pre, post, sink=ENVIRONMENT)      # EXACT: mass is integer grams; sink absorbs legitimate losses (smoke/heat)
    assert contamination_and_heat_transfer_consistent(pre, post)
    assert provenance_extended(pre, post)
    assert separated_sums(pre, post)              # cut pieces sum to original length/mass
    else: REJECT (raise; action fails as an engine error, logged) 
```
The **environment sink** is an explicit pseudo-entity that absorbs mass/energy that legitimately leaves
the modeled world (smoke to air, heat lost) so burn/melt/boil/dry *balance*. It is **accountable** (v2
hardening, AR11): the sink **tracks the total it has absorbed per channel and may only grow** — it is
not a silent catch-all into which imbalance can disappear; anomalous sink growth is reviewable and
fails tests. **Mass balances *exactly*** (it's integer-quantized — grams as ints — so there are no
float tolerances to drift; the only "tolerance" is the sink absorbing legitimate losses). **Energy is
modeled as a *gate*** (enough heat to ignite/melt? enough force to bend?), **not a balanced channel** —
qualitative-physics research (de Kleer/Forbus) shows ordinal energy can't be conserved unambiguously, so
we don't try; we gate on it and route lost heat to the sink. Worked checks (foam-burn → ash + smoke-to-
sink; one sheet → five strips summing to the original grams) both close exactly.
A rejection is a *bug*, not a player failure — it means authored content is unphysical; it's logged and
must be fixed (and in tests it fails the build).

### DR-12 Determinism & seeding (an *enforced contract*, v2 hardening — C2)
Each run carries a seed; **every** stochastic element *and every minted id* (derived-object ids, the
seeded dice, radio fragment selection) draws from the **per-run seeded RNG** passed through the
snapshot — never `random`/`time`/`uuid`/the DB's `dbid`. Resolution is a pure function of
`(attempt, world, seed_state)`. Enforcement:
- **Lint:** `EntityState` and the pure core may not contain `dbid`/`uuid`/`datetime`/wall-clock values
  (they'd leak nondeterminism into snapshots); ids in the pure layer are seeded logical ids, mapped to
  Evennia dbrefs only in the shell at apply time.
- **Property test:** *double-run-same-seed* — running a scripted transcript twice from one seed yields
  byte-identical effect/event streams. This guards the entire DR-18 fuzz/coverage story.
- Fuzz/replay run on the **pure core with an in-memory `WorldView`** (no DB), so replay is exact and
  fast.

### Worked sequence — "cut the cover of the seat with the multitool"
1. **Parser:** verb `cut` (synonym table) → `ActionAttempt{verb:cut, X:seat.seat_cover, relation:None,
   Y:None, tool:multitool}` (the possessive "cover of the seat" binds X to the part; nouns matched to
   reachable entities). *(The two-object form `cut cover off seat` would set `relation:off, Y:seat`.)*
2. **Resolver:** tier 3 lookup `(cut, synthetic_fabric)` → operation schema. Preconditions: `tool.edge ≥
   fabric.cut_resistance − slack` → `0.8 ≥ 0.3` ✓. Modifier: `target.frozen` → +resistance, +duration.
   Duration f(...) = 6 min; actor budget 20 → full success.
3. **Effects:** `remove_part(seat, seat_cover)` + `create_object(loose_fabric, from=seat_cover)` with
   conserved `temperature/wetness/contamination/provenance`. **Event:** `impact(loudness=0.35)`.
4. **Ledger:** pre vs post — fabric mass moved from part to new object, sums match, provenance extended
   → ✓ commit.
5. **Narrate:** template `cut.success` filled from state → *"You saw the cover free of its stitching — a
   ragged sheet of frost-stiff fabric."* Event routed to same-zone observers.
*(Contrast: `cut the steel bolt` → `(cut, steel)` precondition `0.8 ≥ 0.99` ✗ → the physics of why:
"the blade just skates off the steel.")*

---

## 6. Perception & space (DR-13; built in a first version — DR-13a below)
Scene = one Evennia Room; a character's **zone** is an Attribute (coords + terrain tags). Per-observer
rendering overrides `return_appearance`/`get_display_*(looker)` to compute, from the looker's zone:
visibility/audibility/reachability/direction/detail (pure functions in `world/sim/space`). A **message
propagator** (built on the rpsystem `send_emote` pattern) replaces plain `msg_contents`: each Event is
rendered per observer by perception band × loudness × weather. Reachability gates manipulation
(DR-09 only binds reachable nouns). The single-scene design keeps this O(observers×nearby), cheap.

> **DR-13a (shipped 2026-07) — the first version.** Zone storage: `state["zone"]`
> on characters AND objects (marshalled free through the existing Attribute schema; precedent:
> `ident`) with a zone tag mirror written by the `apply()` MOVE_ZONE branch; carried objects track
> their carrier dynamically; minted objects inherit the actor's zone; a dropped object re-zones
> through the single writer; a room `default_zone` covers the unassigned. The zone map is
> loaded-once scenario content (`zones.load_zones` — the narrator/appearance registry pattern):
> zones carry name/coords/elevation/terrain/aliases/survey-prose + undirected edges flagged
> `walk`/`see`/`muffle`. **v1 band math = see-edge hops** (0→SAME_ZONE … 4→BARELY_VISIBLE; no
> path→OUT_OF_SIGHT) + the §15 weather band-steps as a `"clear"`-defaulting parameter (the weather
> seam, PLAN E7); walls are absent see-edges (the v1 occlusion model); planar-distance banding and finer
> occlusion are the recorded refinement. **The one-zone compat rule:** entities/observers without
> zone data are SAME_ZONE — a zone-less world is a one-zone world, keeping every pre-P3 fixture
> and scenario byte-identical. **Moves are single-hop and instant** (durations/auto-pathing: PLAN E17;
> `duration_minutes` already plumbed). **The reachables/reachable split:** the worldview's
> `reachables()` = the perception-VISIBLE set (+ zone pseudo-nouns so destinations parse);
> `reachable()` = the manipulable same-zone set; the resolver's central reach gate answers
> visible-but-far attempts with the §17 "too far to {verb} from here" redirect (excluded from the
> wall-sensor). The reachability tax is paid by that gate + the stock-get pre-flight +
> `return_appearance` — no mixin. Muffle edges ship tested but the crash-site map authors none
> (openings are edges, walls are absences); a closed hatch/door zone makes them real later.
> The frozen `Event(kind, source_id, loudness, data)` carries perception: the shell derives the
> source zone from `source_id` (`data["zone"]` optional override).

## 7. Time & multiplayer (DR-14, DR-15)
- **Clock (DR-14):** a **continuously running real-time clock** — game time advances on its own
  at **15 game-minutes per real minute**, and at about **150×** in a fast forward the players agree to
  (DR-14b), on a global heartbeat Script (`tick-and-scheduler.md`, the canonical model). It is never
  advanced by player actions or chat and cannot be stalled or yanked by one player; the world moves
  whether or not the party acts. Event-/turn-based time is **rejected** (clunky in multiplayer). **Determinism reconciliation
  (DR-12):** the wall-clock only decides *when* a tick fires; *what* a tick does is a pure, deterministic
  function of `(state, dt)` with every draw from the seeded RNG — so the fuzzer/replay drive **logical**
  ticks directly (no real clock) and stay byte-reproducible. A running clock is live by construction.
  The built clock is the **basic** version (world-time advances + cold ticks); the full activity
  scheduler is PLAN E1 (DR-27), behind the §13 seams.
- **Activity scheduler:** a long action returns `duration_minutes`; the shell registers an **Activity**
  persisted to **Attributes** (not `.ndb`, so it survives `@reload` — IM9) on a global heartbeat/own
  Script; each step accrues progress, emits tick feedback, routes degraded messages, and keeps **partial
  progress** on interrupt. A pending activity is interrupted on `events.INTERRUPT_SIGNALS` (danger,
  fire/weather/rescue changes); the running clock itself never stops. **v3:** persist each
  Activity's start/deadline/progress and **recompute elapsed from the world clock on `at_start`** after a
  reload, rather than trusting the timer's elapsed estimate (Evennia research).
- **Session/instance (DR-15):** a **synchronous, small-party instanced run** = a fresh world-state spawned from a **prototype
  set** (Evennia spawner) and tagged with a `run_id`, created on party start, persisted in Postgres
  during play, **reset** by deleting the run's tagged objects (`search_object_by_tag`) at end, and
  **GC'd** by a reaper Script that **sweeps tag-orphans** (objects whose run has no connected sessions
  past a timeout), not just iterating live runs. Solo = a one-player instance. *This is near-identical to
  the official **EvAdventure dungeon contrib** (and Arx Shardhaven) — a confirmed idiomatic pattern, not
  an invented one (research, DR-15 confidence 68→83).*

## 8. Rescue (DR-16)
The design is document 14 §3; the engine design is written when that document is finalized (PLAN A6,
`rescue.md`). What the engine has to carry, from the design:
- **Three ways home** — the radio, a signal a search plane can see, surviving long enough — and two
  endings, rescued or dead (DR-15b). Players never see a number, and the engine keeps no rescue score.
- **The radios are world state**, not a packet: the plane's radio on the plane's battery, and Holt's hand radio whose batteries are separate objects, buried
  in a bag in the tail section; a loose wire inside; an antenna that is any metal long enough, and how
  high it is raised (higher is better; a poor match only weakens the signal); the channel buttons and
  the written emergency frequency; push-to-talk; a charge that drains with use, shown as a dimming
  light. The signal follows from that state and reaches the players as the world's sound — a screech, a
  hum, a faint voice, words lost. Contact does not wait for a flyover.
- **The voice** on the radio is a character played from outside by a language model — DR-02's one
  exception: its judgement of what it is told, by the game's list of landmarks and their values, is its
  act, logged like a player's.
- **The flyovers** are a fixed schedule, the same every run (document 13 §4.2), run as scheduled
  processes on the escalation calendar, with the default rescue on day 7 for a party that can be found.
  Whether a crew sees a signal is decided by physics at the moment of a pass — contrast, weather, how
  close the pass comes — deterministically from the seeded state (DR-12). Being findable is world state
  too: partial cloud and the trees hide the wreck, and after the day-6 snow it is white on white, so
  what the party builds decides it — smoke kept going, the tarp or a sign laid out.
- **The ELT is broken.**

---

## 9. Build-time toolchain (DR-17, DR-18) — offline, LLM-assisted, never at runtime
**Pipeline (DR-17a):** content is authored in the tables (`objects.py`, `materials/table.py`,
`zones.py`, `spaces.py`, `appearance.py`, `responses/`) — by hand, or drafted by `ontology-generator`
and the world-building loops from the ontology store (`docs/ontology/`, document 05) → **validate**
(`make validate`: content lint over the tables, plus the conservation ledger over each transform's
pre/post) → loaded at boot. The **golden material table** is hand-curated and is the canonical input the
generator extends, never overwrites.

**Coverage (DR-18a):** every `status: pass` probe green and the passing count never dropping, plus the
seeded fuzz — **0 unresolved attempts, 0 conservation violations, rescue reachable from every sampled
state**. The **`solvability-fuzz`** harness drives the `ScriptedBrain` (greedy / reckless /
random-within-affordances) over seeded runs; its **wall-sensor** output (attempts answered only by the
generic fallback) is the prioritized build-time authoring queue. This verifies *resolution +
conservation + solvability*; **quality is judged by reading the rendered scenes** (`make
render-scenes`; the validator cannot certify delight).

## 10. Testing & observability (DR-19, DR-20)
- **Tier 1 — pure pytest** over `world/sim/**` (no DB, no Evennia): the operation handlers, the ledger,
  perception/direction/sound math, resolver tiers, the systems. Milliseconds.
- **Tier 2 — Evennia integration** (`evennia test`, test DB): Attribute↔EntityState marshalling,
  parser+reachability, the propagator, `@reload`-durable activities, instance lifecycle.
- **Property/invariant tests** (the enforced findings): conservation ledger balances; narration↔Effect
  (no narrated change without an Effect); rescue reachable from every state; every-attempt-resolves
  over the fuzz corpus; seeded-replay determinism; the night-one rule (document 08 §4.1a).
- **Observability (DR-20):** every `resolve()` emits a structured **decision trace** (tier hit,
  precondition results, ledger verdict, events) behind a debug flag, so a wrong narration in a live
  (later multiplayer) session is traceable to the rule that produced it.

## 11. Module & file layout (DR-21)
```
game/
  world/sim/                      # PURE CORE (no evennia imports; Tier-1 tested)
    contracts.py                  # EntityState, ActionAttempt, Effect, Event, ActionResult, Material, Operation, Part
    parser/                       # tokenizer, synonym table, role binding  (pure given a vocab)
    operations/                   # handlers/ (one per verb), _helpers.py (the shared toolkit), registry.py; interpreter.py a stub (DR-05b)
    resolver/                     # tiers, the (operation×material) index, the generic fallback (redirect.py), wall-sensor
    materials.py                  # Material + ordinal map + loader of the material table
    conservation/ledger.py        # the pre-commit ledger + environment sink
    effects.py events.py narrator.py
    space/{zones,spaces,perception,direction,sound}.py
    systems/{clock,scheduler,rescue,fire,warmth,water,shelter,injury,weather}.py
    validation/                   # content-lint (build-time + load-time)
  typeclasses/                    # SHELL: Object(bridge to/from EntityState, apply effects),
                                  #        Room(=Scene, perception return_appearance),
                                  #        Character(zone attr), Script(heartbeat/instance-reaper)
  commands/                       # cmdset: parse entry, the verbs, the propagator hook, `observe`
  world/scenarios/whiteout/       # CONTENT TABLES (loaded at boot, DR-17a): objects.py, materials/table.py, zones.py, spaces.py, appearance.py, responses/, probes/, rescue.def, build.py
tools/                            # BUILD-TIME (offline): probes.py, fuzz.py, render_scenes.py, lints/
game/tests/{sim,integration}/     # the two tiers
```

## 12. Key interfaces (contracts)
```python
# parser (shell-side, pure given vocab):     parse(text, vocab, reachable) -> ActionAttempt | ParseError
# resolver (pure):                            resolve(attempt: ActionAttempt, world: WorldView) -> ActionResult
# ledger (pure):                              check(pre: WorldView, effects: list[Effect]) -> LedgerVerdict
# apply (shell, only writer):                 apply(result: ActionResult) -> None   # ledger-gated, atomic
# WorldView: read-only access to EntityStates by id + reachability/zone queries (built from Evennia per action)
```
`WorldView` is the read boundary: the shell builds it from Evennia (Attributes/Tags/contents) once per
action; the pure core never touches Evennia objects.

## 13. The seams (DR-22)
The first vertical slice (built June–July 2026) proved *try-anything → resolves → feels alive* **as
co-op**, because Whiteout is a MUD on Evennia (multiplayer is the premise, and Evennia gives shared
rooms/sessions nearly free; the single-threaded reactor serializes commands, so shared-object mutation
can't race). It, and every system after it, is built behind seams — this is what makes each system
still to come a clean extension, not a refactor:
- **All game output goes through the message propagator** (`Event` → per-observer render). **No raw
  `msg`/`msg_contents` for game events** — enforced by a lint (mirrors the no-raw-writes gate). Adding
  perception (DR-13) = swap that one implementation; commands/resolver/narrator untouched.
- **Reachability/visibility go through `WorldView.reachable()`/`in_zone()`.** Adding zones = change the
  WorldView builder only.
- **The clock is the deterministic logical clock** (DR-14); real-time is a pacing layer. The basic clock
  and the full scheduler share the same `tick(state, dt)`.
- **Run state is tagged with a `run_id` from day one**; instanced co-op (DR-15) = lifecycle/GC code, not
  a data-model migration.

## 14. Decided, not yet fully built
- **Clock** (DR-14) and **sessions** (DR-15) are **decided** — a continuously running real-time clock
  and instanced, synchronous co-op (GDD §9/§16). The built versions are basic (a running clock; one
  shared co-op room with run-tagging); the **full** versions (the activity scheduler; the instanced-run
  lifecycle + GC + interdependence) land **behind the §13 seams**, so adding them is extension, not
  refactor (PLAN E1, E13). *Deferred ≠ undecided, and deferred ≠ fragile.*
- **Perception zones** (DR-13) are built in a first version (DR-13a); planar-distance banding and finer
  occlusion are the recorded refinement, a drop-in behind the propagator seam.
- **Weather** and **rescue** (DR-16) land behind the same seams (PLAN E7, E8).
- **Bot-player** (`agent/`) is an orthogonal external client (build/test tool), not part of the engine.

---
## Review status
This document has been through a lens analysis (`review/20-lens-findings.md`, 1 RED found and closed),
the numeric certainty system (`review/30-certainty.md`), deep research (`review/40-research-notes.md`),
and a final re-score and independent self-verification (`review/50-final-changes.md`,
`review/60-self-review.md`). The residual unknown is DR-11's energy fidelity, an empirical item. The
Evennia-dependent decisions (DR-07/10/14/15) were verified against the installed Evennia **6.0.0**
source. **v4** folds in Andrew's decisions — the taught input grammar (§25a / DR-08), the continuously
running real-time clock (DR-14) and instanced synchronous co-op (DR-15) — and the register carries every
amendment since.

> *Implementation note:* `search_object_by_tag` lives under `evennia.search` / `evennia.utils.search`
> (not the top-level `evennia.` namespace) — see `evennia/contrib/tutorials/evadventure/dungeon.py` for
> the reference instancing usage.
