# Whiteout — Implementation Architecture

> **Status: v4 — FINAL (design-frozen).** The full implementation blueprint for Whiteout, derived from
> `docs/scenarios/whiteout/GDD.md`. Supersedes the older sub-docs where they conflict
> (`overview.md`, `llm-integration.md`, `tick-and-scheduler.md`, `perception-model.md`, `testing.md`
> remain valid as focused views). **Hard constraints (LOCKED): runtime is 100% deterministic and the
> LLM is a build-time authoring tool only; the world clock is a continuously running real-time clock;
> sessions are instanced, synchronous co-op runs; input is the taught grammar (§25a / DR-08).** This
> document is scored in `review/30-certainty.md` against its **decisions register (§2)**.

## 0.5 v2 review hardening (what the lens pass changed)
Six **additive hardenings** from `review/20-lens-findings.md` (none changes the design or goals — they
make stated guarantees *enforced*):
1. **One enforced, atomic, ledgered mutation path** (closes the lone RED, AR15). `apply()` is the *only*
   writer, behind a guarded choke-point + a lint forbidding raw `obj.db.x =` writes; **all** state change
   — including tick/`systems/*` — is expressed as **ledger-gated Effects**; apply is wrapped in
   `transaction.atomic`, updating the Attribute **and** its Tag mirror together. (DR-10, DR-11)
2. **Operations-as-data has an explicit envelope** (AR8/AR13). The DSL covers common op×material cases;
   **stateful/complex logic (FSMs, multi-step systems) is plain Python** behind the same interface. Build
   2–3 operations as plain functions **first**; extract the DSL only once repetition is proven. (DR-05)
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

## 0.6 v3 research refinements (what the deep research changed)
Six refinements from `review/40-research-notes.md` (Evennia source + Inform 7/TADS/PDDL/qualitative-
physics literature). All raised confidence; none reversed a decision (overall ≈81 → ≈84/100):
1. **Conserved quantities are REAL numbers, not ordinals (DR-11/DR-04 — the one correction).** Ordinals
   can't carry a balance. **Mass is a real integer count of grams (`mass_g: int`)** (kills float drift, à la
   Factorio/ONI); **ordinals are used only for intensive properties/gates**; **energy is a gate, not an
   ordinal balance.**
2. **Specificity dispatcher (DR-05).** Rule *precedence* is where declarative systems leak (Inform 7
   lesson): make it explicit/deterministic — **most-specific rule wins, ties broken by a declared
   priority.** DSL stays internal + capped; plain Python beyond it.
3. **Cache-invalidation-on-rollback (DR-10).** Evennia updates in-memory Attribute/Tag caches eagerly
   with no rollback hook; `apply()` must `reset_cache()` touched handlers on rollback, and the lint must
   catch in-place `SaverList/SaverDict` mutation.
4. **Recompute activity progress on `at_start` (DR-14)** from the persisted deadline + world clock,
   not a timer estimate.
5. **Instance from a prototype set; reaper sweeps tag-orphans (DR-15).** Pattern confirmed by the
   official **EvAdventure dungeon contrib** (near-identical) and Arx Shardhaven.
6. **Relations & gaps, not absolute thresholds (DR-04/DR-09).** Outcomes key off cross-factor rank
   relations + graded gaps; the redirect ranks by smallest unmet-precondition gap (same target first,
   cap 2–3, name the verb).

---

## 1. Architectural principles
1. **Functional core / imperative shell.** All game *rules* are pure Python in `game/world/sim/**`
   (no Evennia/Django imports); Evennia is the shell that owns IO, persistence, sessions, and time.
2. **Deterministic runtime.** No model inference, no wall-clock dependence, no unseeded randomness in
   resolution. Same inputs + same seed → same result (so the fuzzer can replay).
3. **Data-driven content.** Materials and operations are **data**, not code branches. Adding a material
   or operation is editing data + a property test, never editing the resolver.
4. **Single source of truth.** Persistent state lives in Evennia Attributes (Postgres). The pure core
   operates on *snapshots* and returns *Effects*; the shell is the only writer.
5. **One enforced mutation path.** State changes *only* via Effects applied by `apply()`, gated by the
   conservation ledger, wrapped in a DB transaction. This is **enforced, not conventional**: a single
   guarded choke-point, a lint/`engine-reviewer` rule forbidding raw `obj.db.x =` / `.attributes.add`
   anywhere else, and **all** state change — including tick/`systems/*` updates — routed through it as
   ledger-gated Effects. Nothing mutates state any other way.
6. **Everything resolves.** Every parsed action returns an `ActionResult` (success, partial, or an
   informative redirect). Unhandled-but-sensible attempts log to the wall-sensor for build-time
   authoring.

## 2. Decisions register (the spine — each scored in `review/30-certainty.md`)
| ID | Decision | Choice (one line) |
|----|----------|-------------------|
| DR-01 | Core/shell split | pure `world/sim` ⟷ Evennia shell via dataclass contracts |
| DR-02 | Runtime LLM | none; deterministic end-to-end |
| DR-03 | Content as data | operations + materials are declarative data, loaded at boot |
| DR-04 | Material model | ~25 ordinal property vectors; hand-curated golden table; ordinal→numeric map |
| DR-05 | Operation model | **hybrid**: common cases as declarative data (DSL); stateful logic as plain Python behind one interface; extract DSL only after repetition is proven |
| DR-06 | Object model | cheap objects; parts (with **mass**) → derived objects; provenance; **within-run debris cap/merge** |
| DR-07 | State in Evennia | Attributes for payload + **Tags** for queryable axes; single source of truth; Tag mirror updated in the same transaction as the Attribute |
| DR-08 | Parser | deterministic taught grammar `VERB X [RELATION Y] [WITH Z]` + synonym tables → `ActionAttempt{verb,X,relation,Y,tool}`; the RELATION slot makes two-object actions first-class; no NL model |
| DR-09 | Resolver | §26 tiers + an operation×material index keyed by `(verb, relation, material-of-X, material-of-Y)` + informative redirect + wall-sensor |
| DR-10 | Effects/Events + apply | **the one enforced, total, atomic mutation path**: guarded choke-point + lint; `transaction.atomic`; tick/systems updates are Effects too |
| DR-11 | Conservation ledger | pre-commit balance gate inside apply(); **accountable** environment sink (tracked, monotonic) |
| DR-12 | Determinism/seeding | per-run seeded RNG for all ids + draws; `dbid/uuid/datetime` forbidden in `EntityState`; double-run-same-seed test; pure replay |
| DR-13 | Perception/zones | zone = attribute in a Scene-Room; per-observer `return_appearance`; propagator |
| DR-14 | Clock/scheduler | **continuously running real-time clock (LOCKED)** + activity scheduler; activities persisted (not `.ndb`); deterministic logical clock under the hood |
| DR-15 | Session/instance | **instanced, synchronous co-op runs (LOCKED)**; explicit lifecycle (create/persist/reset/GC) |
| DR-16 | Rescue | additive-confidence model; distinct-resource routes; radio FSM |
| DR-17 | Build pipeline | author → validate (+ ledger) → **bake** → runtime loads baked data |
| DR-18 | Coverage/fuzz | operation×material matrix + ≥10k seeded fuzz; the solvability oracle |
| DR-19 | Test strategy | Tier-1 pure pytest + Tier-2 Evennia integration; property tests for invariants |
| DR-20 | Observability | a per-resolution decision trace (tier hit, ledger result, events) |
| DR-21 | Module/file layout | `world/sim` pure core, `game/` shell, `world/scenarios` content, build tools |
| DR-22 | Vertical slice | **co-op** in one shared room + a basic running clock, the §22 subset; built behind seams (propagator, WorldView, logical clock, run-tag); defer perception zones / full scheduler / instances / interdependence |
| DR-23 | Presentation | scene-as-prose `look` (salience weights what is VISIBLE — amended by DR-24); `look at X` ≡ `examine X` via ONE pure renderer (`presentation.py`); appearance is state-conditioned scenario content; attachments render physically (DR-09a hint phrases), never as data — full spec: [`presentation.md`](presentation.md) |
| DR-24 | Containment & discovery | loot lives INSIDE things (Evennia nesting = honest hiding); ONE reveal rule (`open` OR `searched`, recursive through revealed); deterministic finds; `TRANSFER` effect (additive) relocates via hook-free `move_to`; taught `take/get` owns acquisition — full spec: [`containment.md`](containment.md) |
| DR-25 | Clothing & warmth | wearability DERIVED from materials (never a whitelist); worn = `state["worn_by"]`, stays in inventory; warmth = Σ round(insulation × capped mass) in insulation-grams (intensive×extensive, not ordinal-summing) → banded words on `inventory`/self-examine; unlimited linear layering v1 — full spec: [`clothing-warmth.md`](clothing-warmth.md) |

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
   │ parser/   resolver/ (§26 tiers, op×material index)   operations/ (interpreter)   materials/         │◄┘
   │ conservation/ (the ledger + environment sink)   effects/ events/   narrator/ (templates)           │
   │ space/ (perception)   systems/ (clock, scheduler, rescue, fire, ...)   validation/                 │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                   ▲ loads
   ┌──────────────── content data (game/world/scenarios/whiteout/, BAKED at build time) ───────────────┐
   │ materials.table   operations/*.op   objects/*.obj   responses/*.txt   rescue.def                   │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                   ▲ built by
   ┌──────────────── build-time tools (offline; LLM-assisted; never at runtime) ───────────────────────┐
   │ ontology-generator → validate (+ ledger) → bake;   solvability-fuzz;   golden-table curation       │
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
    props: dict[str, float]      # baked: ordinals already mapped to numbers
    # cut_resistance, tear_resistance, bend_resistance, burnability, ignition_difficulty,
    # smoke_toxicity, insulation, conductivity, edibility, potability, absorbency, ...
```
The **canonical source** is a hand-curated `materials.table` (the quality anchor, DR-17); the baked form
has numbers. ~25 materials for the first scene.

**Intensive (ordinal) vs extensive (real) — v3 correction (DR-04/DR-11).** A material's `props` are
**intensive** properties (resistances, burnability, insulation) — these are the **ordinal** values, used
only as *gates and rank-relations*, never summed. **Conserved extensive quantities — mass above all —
are real **integer grams** and live on `EntityState.mass_g` /
`Part.mass_g` (ints — no float mass), **not** as ordinals. Outcomes are driven by **rank relations and graded gaps** between
intensive properties (e.g. `tool.edge − target.cut_resistance`), not by arithmetic on ordinals
(measurement theory: ordinals don't support true addition/distance). This split is what lets the ledger
balance (real mass) while authoring stays fast (ordinal properties).

### DR-05 Operations (the heart)
An operation is a unit of behavior registered behind **one interface**. *Common, stateless* cases are
expressed as a **declarative schema** (data) run by a shared interpreter; *stateful/complex* ones are
plain Python — both register identically, and the resolver doesn't care which a given operation is (see
**the DSL envelope** below). The declarative form is what lets *most* "add a verb" be a data edit and
keeps the bulk of the resolver small; the schema shape below is that declarative form.
```python
@dataclass(frozen=True)
class Operation:
    id: str                      # "cut"
    verbs: tuple[str, ...]       # synonyms feed the parser: cut, saw, slice
    roles: tuple[str, ...]       # ("actor","target","tool?")
    preconditions: tuple[Predicate, ...]   # declarative, over EntityState/Material/zone
    modifiers: tuple[Modifier, ...]        # qualitative: harder if frozen; slower if cold_hands
    effects: tuple[EffectSpec, ...]        # separate(target)->outputs; conserve(...)
    duration: DurationSpec                 # f(resistance, tool, modifiers) -> minutes
    partial: PartialSpec                   # budget<required -> progress
    failure: FailureSpec                   # which authored redirect/explanation to emit
```
`Predicate`/`Modifier`/`EffectSpec` are a tiny, closed expression language (a handful of node types:
compare a property, check a tag, require a tool quality, etc.) evaluated deterministically. The closed
set is deliberate — it bounds what authored/generated content can express and makes it all checkable.

**The DSL envelope (v2 hardening — DR-05 is the system's biggest bet, so draw its limits honestly).**
The DSL covers the *common, stateless* operation×material cases (cut/burn/pry/tie/wear…), which are the
bulk. **Stateful or multi-step logic is plain Python**, not data: the radio FSM, the eight `systems/*`
(fire ladder, warmth, rescue confidence), and any operation the DSL can't express implement the same
`Operation`/tier interface as a normal function. Both kinds register identically; the resolver doesn't
care which a given operation is. **Build order matters:** write the first 2–3 operations as **plain
Python functions first**, and **extract the DSL only once the repetition is real** — this avoids
standing up an interpreter that no content has stressed (the premature-abstraction trap). What the DSL
*cannot* express is documented alongside it, so authors know when to drop to Python.
**Deterministic specificity dispatch (v3 — DR-05).** When several rules could fire, precedence is the
classic failure point (the Inform 7 leaky-rule-ordering lesson). Resolution is therefore **explicit and
deterministic: the most-specific rule wins** (authored-special > object > (operation,material) >
generic), **ties broken by a declared integer priority** — never by file/registration order. This makes
"which rule fired" predictable, traceable (DR-20), and replayable (DR-12).

> **DR-05a (appended, attachment-honesty 2026-07) — destructive extraction.** The D12 cut rule is
> amended: **a part's attachment gates HOW its material comes free, never WHETHER** (the material
> gate stays first — a dull blade is still dull). Cut/tear on a part whose material the tool defeats
> but whose attachment is mechanical (pryable-class) now SUCCEEDS destructively: the part is removed
> and its full mass minted as `{material}_scrap` ×3 (part-scoped derived ids like
> `seat:cushion_scrap0:loose`; the ledger balances exactly; a `residue_{part}` state attribute
> records the wrecked fastener so the aftermath narration is a recorded fact — DR-11). **Pry keeps
> its exclusive value**: the only intact single-piece removal off a mechanical fastener
> (`outputs_when_removed`) — intact-vs-scrap matters for later content (insulation area, whole
> covers); no uses built yet. **`fixed`/unknown attachments stay integral** — refuse-with-
> explanation; authors opt INTO extractability by naming a real attachment. The old
> slash-without-effect branches (`cut.slash_fixed`, `tear.attached`) are **retired** — they narrated
> damage no Effect recorded. `break` intentionally unchanged (extraction defers to cut/tear/pry);
> destructive-is-slower is future tuning once durations land (P4).
>
> **DR-09a (appended, attachment-honesty 2026-07) — explain the physics + one sibling near-miss.**
> Attachment-mismatch refusals explain WHY in physical terms via a content-tunable phrase map in the
> scenario responses (`attachment.explain.*` / `attachment.hint.*` / `attachment.residue.*` — Andrew
> owns the voice; the pure helper `_helpers.attachment_phrase` reads it through `narrator.get`).
> Handlers may append at most ONE near-miss: the first sibling part of the SAME entity where the
> attempted verb genuinely works *with the held tool* (`_helpers.sibling_hint`), phrased naming the
> part and its physical state ("The cover, though, is only held by stitching.") — never the method
> or tool (name-the-verb-not-the-solution holds). Hints use the short neutral `hint` phrase kind,
> not the failure explanations. Not a spoiler: `examine` already lists every part's attachment.
> `generic_redirect` stays coarse by design; its precision upgrade remains P2.

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
    provenance: list[str]        # design §24: where it came from
    owner: str | None
```
Removing a part yields a **first-class derived object** built from the part's `outputs_when_removed`,
with conserved state and mass (`Part.mass_g` lets the ledger balance the removal, DR-11). Puzzle-
critical objects (radio/beacon/pilot) additionally carry an authored packet (a small state machine +
clue/solution paths); they are the documented exception.

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
against …`, `tie … between …`), rather than single-target-only commands. Unknown verb / no match → a help
nudge showing the format (never a hard error). Richness comes from *rule coverage* and the **generative**
operation×material engine — not parser cleverness or an enumerated command list.

> **DR-08a (appended, slice-fix 2026-07) — the numbered disambiguation menu.** A multi-hit noun returns
> `Disambiguation{term, options}`; each `DisambigOption` now carries its concrete `entity_id`/`part_id`
> (**ADDITIVE** contract change — defaults preserve the prior shape; locked in `test_contracts.py`). The
> shell prints a **numbered menu** and parks it as ephemeral UI state (a module-level pending map in
> `cmd_act.py`, deliberately NOT an Attribute — DR-10's single-writer rule guards *world* state; a menu
> is a question, not a fact). A bare number (caught by the deterministic unmatched-input command,
> `CmdNoMatch` in `cmd_act.py` — digits match no verb; NO LLM anywhere near it, DR-02 holds) re-runs the
> **whole original raw line** through `parse(..., bindings={term: (entity_id, part_id)})` — the pick
> pins that slot on re-parse, so RELATION/Y/WITH survive **by construction**, and identical objects
> ("glass shard" ×3) are picked by identity, immune to reordering. A **stale** pick (its entity no
> longer among the live hits) is ignored and degrades to a fresh menu / the lone survivor / `X=None` →
> the informative redirect — never an error ("ambiguity prompts a clarification, never a flat refusal",
> GDD §25a). Accepted edges: a future command literally named "2" would shadow a pick; the same term
> ambiguous in two slots pins both to one entity (bindings are per-term and ephemeral — per-slot keys
> are a safe later upgrade); `@reload` clears pending menus.
>
> **(appended, stock-items 2026-07)** Stock `get`/`drop` share the numbered menu: thin subclasses
> (`game/commands/cmd_items.py`) pre-flight a quiet search — a true multimatch (not a leading-count
> stack of identical keys) shows the same menu; single/none/stacked defer to stock behavior
> untouched. A pick re-issues the original command using the manager's stable, id-ordered `name-N`
> ordinal recomputed at pick time (`#dbref` re-issue rejected — Builder-gated in the pinned
> Evennia), so picks are reorder-immune and a stale pick degrades to an informative message or a
> fresh menu. The pending map gains a `kind` discriminator dispatched by the unmatched-input
> command (`CmdNoMatch`); one pending menu per caller — **the latest question wins**. `give` is
> deferred until a third use case.

### DR-09 Resolver (`resolve(attempt, world) -> ActionResult`, pure)
```
resolve(attempt, world):
    candidates = tiers in order:
      1 authored-special   (puzzle-critical object rule, e.g. the radio FSM)
      2 object-rule        (rare per-object override)
      3 operation×material (THE WORKHORSE — indexed lookup: (verb, relation, material_of_X, material_of_Y))
      4 generic-physics    (fallbacks: mass/temperature/containment defaults)
      5 informative-redirect (authored "can't do X here; you could cut/burn/pry…")
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

**Informative-redirect ranking (v3 — DR-09).** When no rule fires, the redirect ranks candidate
operations by the **smallest unmet-precondition gap** (the action you were *closest* to being able to
do), **prefers the same target**, **caps at 2–3 suggestions**, and **names the verb, not the solution**
("you could *cut* or *pry* it" — not "use the knife to free the strap"). This is the convergent lesson
from affordance theory, parser-IF practice, and precondition-error-correction research.

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
Each run carries a seed; **every** stochastic element *and every minted id* (derived-object ids, pilot
timer jitter, radio fragment selection) draws from the **per-run seeded RNG** passed through the
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
*(Contrast: `cut the steel bolt` → `(cut, steel)` precondition `0.8 ≥ 0.99` ✗ → authored failure
redirect: "the blade just skates off — you'd need to unbolt it.")*

---

## 6. Perception & space (DR-13; SHIPPED v1 — see DR-13a below)
Scene = one Evennia Room; a character's **zone** is an Attribute (coords + terrain tags). Per-observer
rendering overrides `return_appearance`/`get_display_*(looker)` to compute, from the looker's zone:
visibility/audibility/reachability/direction/detail (pure functions in `world/sim/space`). A **message
propagator** (built on the rpsystem `send_emote` pattern) replaces plain `msg_contents`: each Event is
rendered per observer by perception band × loudness × weather. Reachability gates manipulation
(DR-09 only binds reachable nouns). The single-scene design keeps this O(observers×nearby), cheap.

> **DR-13a (appended, P3 shipped 2026-07) — the v1 realization.** Zone storage: `state["zone"]`
> on characters AND objects (marshalled free through the existing Attribute schema; precedent:
> `ident`) with a zone tag mirror written by the `apply()` MOVE_ZONE branch; carried objects track
> their carrier dynamically; minted objects inherit the actor's zone; a dropped object re-zones
> through the single writer; a room `default_zone` covers the unassigned. The zone map is
> loaded-once scenario content (`zones.load_zones` — the narrator/appearance registry pattern):
> zones carry name/coords/elevation/terrain/aliases/survey-prose + undirected edges flagged
> `walk`/`see`/`muffle`. **v1 band math = see-edge hops** (0→SAME_ZONE … 4→BARELY_VISIBLE; no
> path→OUT_OF_SIGHT) + the §15 weather band-steps as a `"clear"`-defaulting parameter (the P7
> seam); walls are absent see-edges (the v1 occlusion model); planar-distance banding and finer
> occlusion are the recorded refinement. **The one-zone compat rule:** entities/observers without
> zone data are SAME_ZONE — a zone-less world is a one-zone world, keeping every pre-P3 fixture
> and scenario byte-identical. **Moves are single-hop and instant** (durations/auto-pathing = P4;
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
- **Clock (DR-14, LOCKED):** a **continuously running real-time clock** — game time advances on its own
  at a fixed real→game pace (a tunable constant, ~10–20 real-seconds per game-minute) on a global
  heartbeat Script (`tick-and-scheduler.md`, now the canonical model). It is never advanced by player
  actions or chat and cannot be stalled or yanked by one player; the world moves whether or not the party
  acts. Event-/turn-based time is **rejected** (clunky in multiplayer). **Determinism reconciliation
  (DR-12):** the wall-clock only decides *when* a tick fires; *what* a tick does is a pure, deterministic
  function of `(state, dt)` with every draw from the seeded RNG — so the fuzzer/replay drive **logical**
  ticks directly (no real clock) and stay byte-reproducible. The old "event-driven + clock-liveness rule"
  is **retired** (a running clock is live by construction). The **slice gets the *basic* version** (a
  running clock: world-time advances + cold ticks); the full activity scheduler is deferred (DR-22).
- **Activity scheduler:** a long action returns `duration_minutes`; the shell registers an **Activity**
  persisted to **Attributes** (not `.ndb`, so it survives `@reload` — IM9) on a global heartbeat/own
  Script; each step accrues progress, emits tick feedback, routes degraded messages, and keeps **partial
  progress** on interrupt. A pending activity is interrupted on `events.INTERRUPT_SIGNALS` (danger, fire/weather/rescue changes); the running clock itself never stops. **v3:** persist each
  Activity's start/deadline/progress and **recompute elapsed from the world clock on `at_start`** after a
  reload, rather than trusting the timer's elapsed estimate (Evennia research).
- **Session/instance (DR-15, LOCKED):** a **synchronous, small-party instanced run** = a fresh world-state spawned from a **prototype
  set** (Evennia spawner) and tagged with a `run_id`, created on party start, persisted in Postgres
  during play, **reset** by deleting the run's tagged objects (`search_object_by_tag`) at end, and
  **GC'd** by a reaper Script that **sweeps tag-orphans** (objects whose run has no connected sessions
  past a timeout), not just iterating live runs. Solo = a one-player instance. *This is near-identical to
  the official **EvAdventure dungeon contrib** (and Arx Shardhaven) — a confirmed idiomatic pattern, not
  an invented one (research, DR-15 confidence 68→83).*

## 8. Rescue (DR-16)
- **Additive confidence:** `RescueState{channels:{beacon,radio,landmark,visual,smoke,stay}: 0..1}`;
  `confidence = Σ weight·value` capped at 1; `rescued = weather_window AND confidence ≥ threshold`.
- **Distinct resources:** each channel's authored requirements draw on *different* scarce inputs (not
  all warmth/fire) so route choice is real and global softlock is avoidable (Conv-2).
- **Radio (authored exception):** a small **FSM** — `dead → powered_static → weak_receive →
  weak_transmit → two_way_no_location → useful_contact`; transitions gated by power, an improvised
  long-metal antenna (quality computed from material/length/placement), and location info (≥3 clue
  paths). Implemented as a puzzle-critical packet, not generic physics.

---

## 9. Build-time toolchain (DR-17, DR-18) — offline, LLM-assisted, never at runtime
**Pipeline:** authored source (`materials.table`, `*.op`, `*.obj`, response text) →
`ontology-generator` drafts candidates (qualitative) → **validate** (content-lint + run the conservation
ledger over each transform's pre/post) → **bake** into the numeric/indexed form the runtime loads →
commit. The **golden material table** is hand-curated and is the canonical input the generator extends,
never overwrites.

**Coverage definition (DR-18):** done = the **operation × material matrix** is populated + property-
tested, **plus** a **≥10k-attempt seeded fuzz corpus** with **0 unresolved attempts, 0 conservation
violations, rescue reachable from every sampled state**. The **`solvability-fuzz`** harness drives the
`ScriptedBrain` (greedy / reckless / random-within-affordances) over seeded runs; its **wall-sensor**
output (attempts that hit generic-redirect) is the prioritized build-time authoring queue. This verifies
*resolution + conservation + solvability*; **quality is curated + playtested** (the validator cannot
certify delight).

## 10. Testing & observability (DR-19, DR-20)
- **Tier 1 — pure pytest** over `world/sim/**` (no DB, no Evennia): operation interpreter, the ledger,
  perception/direction/sound math, resolver tiers, rescue arithmetic. Milliseconds.
- **Tier 2 — Evennia integration** (`evennia test`, test DB): Attribute↔EntityState marshalling,
  parser+reachability, the propagator, `@reload`-durable activities, instance lifecycle.
- **Property/invariant tests** (the enforced findings): conservation ledger balances; narration↔Effect
  (no narrated change without an Effect); rescue-confidence monotonic & reachable; every-attempt-
  resolves over the fuzz corpus; seeded-replay determinism; warmth floor.
- **Observability (DR-20):** every `resolve()` emits a structured **decision trace** (tier hit,
  precondition results, ledger verdict, events) behind a debug flag, so a wrong narration in a live
  (later multiplayer) session is traceable to the rule that produced it.

## 11. Module & file layout (DR-21)
```
game/
  world/sim/                      # PURE CORE (no evennia imports; Tier-1 tested)
    contracts.py                  # EntityState, ActionAttempt, Effect, Event, ActionResult, Material, Operation, Part
    parser/                       # tokenizer, synonym table, role binding  (pure given a vocab)
    operations/interpreter.py     # evaluates Predicate/Modifier/EffectSpec; the closed expr language
    resolver/                     # tiers, the (operation×material) index, redirect, wall-sensor
    materials.py                  # Material + ordinal map + loader of the baked table
    conservation/ledger.py        # the pre-commit ledger + environment sink
    effects.py events.py narrator.py
    space/{zones,perception,direction,sound}.py
    systems/{clock,scheduler,rescue,fire,warmth,water,shelter,injury}.py
    validation/                   # content-lint (build-time + load-time)
  typeclasses/                    # SHELL: Object(bridge to/from EntityState, apply effects),
                                  #        Room(=Scene, perception return_appearance),
                                  #        Character(zone attr), Script(heartbeat/instance-reaper)
  commands/                       # cmdset: parse entry, the verbs, the propagator hook, `observe`
  world/scenarios/whiteout/       # BAKED CONTENT: materials.table, operations/, objects/, responses/, rescue.def, build.py
tools/                            # BUILD-TIME (offline): bake.py, fuzz runner, coverage report
game/tests/{sim,integration}/     # the two tiers
```

## 12. Key interfaces (contracts)
```python
# parser (shell-side, pure given vocab):     parse(text, vocab, reachable) -> ActionAttempt | ParseError
# resolver (pure):                            resolve(attempt: ActionAttempt, world: WorldView) -> ActionResult
# ledger (pure):                              check(pre: WorldView, effects: list[Effect]) -> LedgerVerdict
# apply (shell, only writer):                 apply(result: ActionResult) -> None   # ledger-gated, atomic
# operation interpreter (pure):               evaluate(op: Operation, attempt, world) -> ActionResult | None
# WorldView: read-only access to EntityStates by id + reachability/zone queries (built from Evennia per action)
```
`WorldView` is the read boundary: the shell builds it from Evennia (Attributes/Tags/contents) once per
action; the pure core never touches Evennia objects.

## 13. The vertical slice architecture (DR-22 — build this first)
A reduced subset proving *try-anything → resolves → feels alive* — **as co-op**, because Whiteout is a
MUD on Evennia (multiplayer is the premise, and Evennia gives shared rooms/sessions nearly free; the
single-threaded reactor serializes commands, so shared-object mutation can't race).
- **In:** `contracts`, `materials` (~25, golden table), `operations/interpreter` + ~15 operations,
  `resolver` (tiers 1/3/5 only — authored-special for the radio stub, op×material, redirect),
  `conservation/ledger` + sink, `parser`, `effects/apply`, `narrator` templates + ~50 curated signature
  responses, the wall-sensor, ~5 objects (seat, multitool, fire-makings, radio stub, pilot), a stub
  rescue. **2–3 players co-op in one shared room.** A **basic running clock** (world-time + cold ticks).
  Tier-1 tests + a small fuzz run + a 2-session integration test.
- **Built behind seams — this is what makes the deferred systems clean extensions, not refactors:**
  - **All game output goes through the message propagator** (`Event` → per-observer render); the slice's
    propagator is trivially "render the same line to everyone in the room." **No raw `msg`/`msg_contents`
    for game events** — enforced by a lint (mirrors the no-raw-writes gate). Adding the overlapping
    perception zones (DR-13) later = swap that one implementation; commands/resolver/narrator untouched.
  - **Reachability/visibility go through `WorldView.reachable()`/`in_zone()`**; the slice returns
    "everything in the one room." Adding zones = change the WorldView builder only.
  - **The clock is the deterministic logical clock** (DR-14); real-time is a pacing layer. Basic now,
    full scheduler later — same `tick(state, dt)`.
  - **Run state is tagged with a `run_id` from day one** (one run in the slice); instanced co-op (DR-15)
    later = lifecycle/GC code, not a data-model migration.
- **Out (deferred, behind the seams above):** the graded perception zones (DR-13), the full activity
  scheduler (DR-14), instanced-run lifecycle (DR-15), authored co-op interdependence, weather, the full
  rescue graph.
- **Success test (from the GDD):** a couple of friends, no manual, ~15 min co-op — "the world felt alive
  (and fun to poke at together)", zero "you can't do that", one delighted "I can't believe that worked."
  Pass → layer DR-13 / DR-14(full) / DR-15 / DR-16.

## 14. Deferred-in-the-slice (decided, not open)
- **Clock** (DR-14) and **sessions** (DR-15) are **decided and locked** — a continuously running
  real-time clock and instanced, synchronous co-op (GDD §9). The slice ships their **basic** form (a
  running clock; one shared co-op room with run-tagging); the **full** versions (the activity scheduler;
  instanced-run lifecycle + GC + interdependence) land post-slice, **behind the §13 seams** so adding
  them is extension, not refactor. *Deferred ≠ undecided, and deferred ≠ fragile.*
- **Overlapping perception zones** (DR-13) are deferred but **critical**; the propagator seam (§13) is
  exactly what keeps them a clean drop-in rather than a rewrite.
- **Bot-player** (`agent/`) is an orthogonal external client (build/test tool), not part of the engine.

---
## Review status
This document has been through the full review: lens analysis (`review/20-lens-findings.md`, 1 RED
found and closed), the numeric certainty system (`review/30-certainty.md`), deep research
(`review/40-research-notes.md`), and a final re-score + **independent self-verification**
(`review/50-final-changes.md`, `review/60-self-review.md`). **Overall architecture confidence ≈ 84/100**,
nothing below 72; the two residual unknowns (DR-05 operation-DSL boundary, DR-11 energy fidelity) are
empirical "prove-it-in-the-slice" items. The Evennia-dependent decisions (DR-07/10/14/15) were verified
against the installed Evennia **6.0.0** source.
>
> **v4 (FINAL)** folds in the user's locked decisions — the taught input grammar (§25a / DR-08), the
> continuously running real-time clock (DR-14), and instanced synchronous co-op (DR-15) — plus the GDD
> finalization. These are vision/decision locks the design is built *toward*, not changes the review
> proposed; DR-14's earlier "event-driven (recommended)" framing is retired accordingly.

> *Implementation note:* `search_object_by_tag` lives under `evennia.search` / `evennia.utils.search`
> (not the top-level `evennia.` namespace) — see `evennia/contrib/tutorials/evadventure/dungeon.py` for
> the reference instancing usage.
