# 20 — Architecture lens findings (AR1–AR17)

**Artifact under review:** `docs/architecture/implementation-architecture.md` v1 — specifically its
**decisions register §2 (DR-01…DR-22)** and the engine internals (§3–§13).
**Goal of the review:** judge the *software architecture itself* — sound, buildable, scalable,
testable, low-debt? — **not** the game design (that is `10-design-polish.md` / the GDD lens pass).
**Lens library:** `.claude/skills/lenses/architecture.md` (AR1–AR12 design-integrity + AR13–AR17
code-smell/debt). **Stance:** adversarial — each card hunts the failure, and every GREEN says *why
it is certain*. Cards are anchored to the DR-row(s) they judge.

> **Standing caveat (applies to every card):** *no code exists yet* (CLAUDE.md: `world/sim`,
> `world/scenarios`, `tests/sim` are "Not built yet"). So every verdict is a judgement on the
> **document's design**, not on an implementation. That fact alone is load-bearing for AR13.

## Triage (leverage = how-much-it-could-change-the-design × how-uncertain-now)
| Lens | Leverage | Verdict |
|------|----------|---------|
| AR15 Missing invariants | **HIGH** | **RED** |
| AR11 Data-model soundness | **HIGH** | YELLOW (med→high) |
| AR8 Extensibility | **HIGH** | YELLOW (med) |
| AR13 Premature abstraction | **HIGH** | YELLOW (med) |
| AR3 Single source of truth | **HIGH** | YELLOW (med) |
| AR4 Determinism | MED | YELLOW (low) |
| AR5 Density scalability | MED | YELLOW (low) |
| AR16 Over-configuration | MED | YELLOW (low–med) |
| AR14 God object | MED | YELLOW (low–med) |
| AR17 Untested critical path | MED | YELLOW (med) |
| AR2 Coupling & cohesion | MED | YELLOW (low) |
| AR10 Griefing surface | LOW | YELLOW (low) |
| AR1 Functional-core boundary | LOW | GREEN |
| AR6 Softlock analysis | LOW | GREEN |
| AR7 Observability | LOW | GREEN |
| AR9 LLM latency/cost | LOW | GREEN |
| AR12 Testability | LOW | GREEN |

---

## AR1 Functional-Core Boundary
- **Verdict:** GREEN
- **Evidence:** DR-01 (pure `world/sim` ⟷ Evennia shell via dataclass contracts), DR-12 (seed passed
  *through the snapshot*, never `random`/`time`), §11 layout ("no evennia imports; Tier-1 tested"),
  §12 contracts (`WorldView` is the read boundary; "the pure core never touches Evennia objects").
- **Severity:** low (caveat only).
- **What would change the verdict:** finding a framework/`time`/RNG import inside `world/sim`, or a
  resolver path that reads an Evennia object directly instead of a `WorldView`.
- **Note:** The split is drawn cleanly and the determinism rule (DR-02/DR-12) reinforces it — no
  inference, no wall-clock, no unseeded RNG in resolution; RNG is threaded through the snapshot. The
  de-facto enforcement is real: Tier-1 pytest (§10) runs without booting Evennia, so an accidental
  `import evennia` in `world/sim` fails at test collection. **Caveat:** the boundary is asserted as a
  *principle* (P1) and backed by a test tier, but the document specifies **no explicit lint** (e.g. an
  import-graph check) as a hard gate; CLAUDE.md cites ADR-0003 as the rule but the arch doc doesn't
  wire a `make validate` rule for it. Cheap to add; recommend it so the boundary can't rot silently.

## AR2 Coupling & Cohesion
- **Verdict:** YELLOW
- **Evidence:** DR-21 module layout (parser / resolver / operations / materials / conservation /
  effects / events / narrator / space / systems); DR-10 Effect taxonomy; §12 `contracts.py` as the
  shared kernel.
- **Severity:** low.
- **What would change the verdict:** an Effect taxonomy that is genuinely closed and stable (adding
  operations never adds Effect kinds), or registered per-Effect handlers so a new kind is local.
- **Note:** Within-module cohesion is good — each `world/sim/**` module does one job. The coupling
  **hotspot is the Effect contract** (DR-10): one new `Effect` kind ripples across *four* sites — the
  operation interpreter (which `EffectSpec` emits it), `effects.py`, the ledger's `simulate()` (DR-11,
  which must know its mass/heat/provenance semantics to balance it), and the shell's `apply()` writer
  (which must translate it to Attribute/Tag writes), plus `narrator.py`. That is "N systems all touch
  one path." Not broken — it's the price of a single mutation channel — but the Effect set must be
  treated as a deliberately-frozen kernel, and new kinds should be the rare exception, not the way you
  add content.

## AR3 Single Source of Truth / State Ownership
- **Verdict:** YELLOW
- **Evidence:** DR-04 / P4 (Attributes are the single source of truth), DR-07 (Attributes for payload
  **+ Tags mirror the queryable axes**; `EntityState` is "a transient snapshot built from them per
  resolution and discarded"), DR-10 (shell `apply()` is "the only writer", atomic), §12 (`WorldView`
  built from Evennia "once per action").
- **Severity:** med (escalates to high under DR-15 multiplayer).
- **What would change the verdict:** (a) a stated rule that `apply()` updates Tags **in the same
  atomic write** as the Attributes they mirror, with a property test asserting Tag/Attribute coherence;
  (b) an optimistic-concurrency/version check at commit for the snapshot path.
- **Note (high-leverage focus).** The single-*writer* discipline is sound (one `apply()`, P4/DR-10),
  and within a single turn-based action the snapshot→resolve→apply→discard lifecycle has no divergence
  window. **Two real risks remain.** (1) **Tag/Attribute is a denormalized duplicate (DR-07).** Each
  queryable fact (material, zone, affordance) lives *twice*: in the Attribute payload *and* as a Tag.
  The doc names Attributes as truth and Tags as "mirror" but **specifies no mechanism that updates the
  mirror transactionally with every state-changing Effect.** Any Effect that changes a queryable axis
  (a `remove_part` that changes an object's material set, a `move_zone`, a contamination that flips an
  affordance) must re-sync Tags or the indexed query ("find all metal things in the cabin," DR-07/DR-09
  tier-3 candidate gathering) returns **stale results** — a divergence between the two stores. (2)
  **Snapshot staleness under concurrency (DR-15).** `WorldView` is read at resolve-time and `apply()`
  commits later; the ledger checks `pre`(snapshot) vs `post`, *not* the live DB at commit. In an
  instanced co-op run two players each snapshot, A commits, B's resolve was computed against a
  now-stale world (B "cuts a cover" A already removed). This is a textbook TOCTOU; the per-action
  atomicity (DR-10) does not address cross-action contention. Both are deferred-but-asserted: the SSOT
  claim is made globally (P4) while DR-15 is in the register, so the architecture currently *claims*
  more consistency than it specifies.

## AR4 Determinism & Reproducibility
- **Verdict:** YELLOW
- **Evidence:** DR-02 (no runtime LLM — end-to-end deterministic), DR-12 (per-run seed; resolution a
  pure function of `(attempt, world, seed_state)`; replayable), DR-10 (atomic apply), DR-18 (≥10k
  seeded fuzz "replays runs exactly"), DR-08 (deterministic parser, no NL model).
- **Severity:** low.
- **What would change the verdict:** (a) a spec for how the **new** `seed_state` is returned in
  `ActionResult` and persisted atomically with effects (so the next action and any replay consume the
  same stream); (b) a rule that every iteration over an Evennia query/`set` is explicitly ordered
  (`order_by` / sorted) before it can affect resolution.
- **Note (focus).** Killing the runtime LLM (DR-02) retires the single biggest nondeterminism source —
  this is the architecture's strongest determinism move and it's genuine. Two things are **still
  hiding**, both fixable: (1) **RNG state round-trip is underspecified (DR-12).** "Draws from a
  per-run seeded RNG passed through the snapshot" tells us inputs are seeded, but *not* how the
  advanced RNG state is threaded back and persisted between actions. If `apply()` mutates a live RNG
  object, that state must be committed atomically with the effects or a crash/replay diverges; if the
  shell re-derives state from `(run_seed, action_index)` it's clean — the doc doesn't say which.
  (2) **Collection-ordering leakage.** `EntityState` uses lists (deterministic), but tier-3 candidate
  gathering and the "nearest possible operations" redirect (DR-09) draw from Evennia **Tag queries
  (QuerySets, unordered without `order_by`)** and possibly Python `set`s of reachable entities. If
  iteration order over an unordered query can change which entity binds or which redirect text is
  chosen, replay diverges across runs/platforms. Neither is fatal, but the answer to "is anything
  nondeterministic still hiding?" is *yes, two things*, and both deserve an explicit invariant.

## AR5 Content-Density Scalability
- **Verdict:** YELLOW
- **Evidence:** DR-09 (operation×material index, "O(1)" dict keyed by `(operation_id, material_id)`),
  DR-07 (Tags for value-queries), §4.6 (cheap objects; behavior derives from generic operations),
  §12 (`WorldView` "built from Evennia once per action"); research §5/§8 (single-scene relief;
  Attribute pickling cost grows with structure).
- **Severity:** low–med.
- **What would change the verdict:** a measured per-action `WorldView`-build cost at target scene
  density (e.g. 100+ objects with parts) and a decision on whether/how to cache or incrementally
  update it across actions.
- **Note (focus).** The **content** axis scales well *by design*, and this is the architecture's best
  idea: generic op×material rules (DR-09) mean adding entities does **not** add per-item rules — ~20
  operations × ~25 materials covers a huge space with a tiny indexed table (~500 entries), exactly the
  BotW/ScienceWorld argument. That defeats the per-item-authored-rules failure mode the lens warns
  about. The **cost** axis is the open question: every action **rebuilds `WorldView` from Evennia**
  (§12) — O(N_scene) construction that unpickles each reachable object's Attribute payload (research
  §8: pickle cost grows with structure) and re-derives `EntityState`s including parts→derived objects.
  Single-scene reachability over in-memory `room.contents` (research §5) keeps N bounded, so this is
  *probably* fine at one-dense-scene scale — but it is repeated **every action**, with no specified
  caching/incremental-rebuild (and it can't trivially cache because Attributes are truth and mutate).
  Under DR-15 multiplayer (a party generating many actions/sec) the full-scene marshal per action is
  the thing that will bite first. Hold it as a measurement target, not an assumption.

## AR6 Softlock / Failure-Mode Analysis
- **Verdict:** GREEN
- **Evidence:** DR-16 (additive confidence; **distinct-resource** routes so no single exhaustion kills
  every route), GDD §0a#4 / §44 (global-resource softlock check + **no-materials warmth floor**),
  DR-18 (solvability oracle: "rescue reachable from every sampled state").
- **Severity:** low (caveat).
- **What would change the verdict:** a soft-lock that the fuzz sampler *misses* because the dangerous
  state requires a specific irreversible-action *sequence* the `ScriptedBrain` never explores.
- **Note:** The design directly answers the lens's core trap — *per-item ≥3-paths misses global
  exhaustion of shared resources*. DR-16's distinct-resource routing and the warmth floor are exactly
  the global guarantees the lens asks for, and DR-18 turns "rescue reachable" into a checked oracle.
  Honest caveat: the oracle is a **sampler, not a proof** — ≥10k seeded fuzz over greedy/reckless/
  random brains gives strong evidence but cannot certify *no* irreversible-action sequence strands a
  party; and the warmth-floor / rescue-reachable invariants are enforced at *build* time (property
  tests, §10), not as a runtime gate. Acceptable, because the floor is a designed structural guarantee
  rather than a probabilistic one.

## AR7 Observability / Debuggability
- **Verdict:** GREEN
- **Evidence:** DR-20 (every `resolve()` emits a structured decision trace: tier hit, precondition
  results, ledger verdict, events — behind a debug flag), DR-11 (ledger rejection logged), DR-09
  (wall-sensor logs unresolved attempts), DR-12 (seeded replay reconstructs any run).
- **Severity:** low (caveat).
- **What would change the verdict:** a wrong **perception** output (DR-13) that the trace can't explain
  because perception scoring isn't in the trace.
- **Note:** For a rule engine this is well above average — the trace covers the whole resolution
  decision (which tier fired, which predicate failed, what the ledger said), so a wrong narration is
  traceable to the producing rule, and seeded replay (DR-12) means even a prod bug (trace off by
  default) is reconstructable from the seed. **Gaps:** the trace as specified covers resolution +
  ledger + events but **not** the per-observer perception scoring (DR-13 band/loudness/weather math),
  so a future "why did this observer see *that*?" multiplayer bug has no equivalent trace; and the
  Tag-mirror sync (AR3) has no observability hook. Add perception to the trace when DR-13 lands.

## AR8 Extensibility
- **Verdict:** YELLOW
- **Evidence:** P3 / DR-03 ("adding a material or operation is editing data + a property test, never
  editing the resolver"), DR-05 (the closed `Predicate`/`Modifier`/`EffectSpec` expression language,
  "a handful of node types," "the closed set is deliberate"), §4.6 (radio/beacon/pilot are an
  **authored packet** exception), §11 layout (`systems/{clock,scheduler,rescue,fire,warmth,water,
  shelter,injury}.py` — eight bespoke Python systems).
- **Severity:** med.
- **What would change the verdict:** (a) the actual **enumerated node-type list** of the expression
  language, plus (b) a demonstration that the slice's ~15 operations (DR-22) all express within it
  *without* interpreter edits, and (c) a triage of which survival behaviours are data (op×material) vs.
  hand-coded `systems/` — i.e. earn the "config not code" claim with content.
- **Note (high-leverage focus).** "Add a material/operation = data edit, not resolver edit" is the
  architecture's central extensibility promise, and it is **true only inside the closed language's
  expressive envelope — and the document never draws that envelope.** Two concessions already mark the
  wall: (1) the radio FSM is "the documented exception," an authored packet *because* a stateful
  multi-step machine can't be a stack of `Predicate/EffectSpec` nodes (§4.6, DR-16); (2) the layout
  carries **eight bespoke `systems/*.py`** (fire ladder, injury, warmth, water…), so the continuous
  survival dynamics are **hand-coded Python, not data** — adding a new hazard or a frostbite curve is a
  code edit, not an `.op` edit. What else can the closed set likely *not* express, by construction?
  **Cross-entity / relational transforms** (weld A to B → one object; pour A into B → proportional
  wetness/contamination transfer; tie rope → an attachment constraint) — if `EffectSpec` nodes are
  per-target (`separate`, `conserve`, `set_attr`), n-ary mixtures and topology changes have no obvious
  node. So extensibility is genuinely excellent for the *common* single-target op×material case and a
  **framework edit** (touching interpreter + ledger + validator + bake) for anything relational,
  stateful, or continuous. That's a defensible boundary — but the doc asserts the friendly half of it
  and is silent on where the wall sits, which is exactly the uncertainty AR13 flags.

## AR9 LLM Latency & Cost Budget
- **Verdict:** GREEN
- **Evidence:** DR-02 (runtime LLM: **none**; deterministic end-to-end), P2, §9 (LLM is build-time,
  offline, "never at runtime"), DR-17 (author→validate→bake pipeline).
- **Severity:** low.
- **What would change the verdict:** any LLM call sneaking onto the runtime path (e.g. a "redirect
  generator" that calls a model) — there is none specified.
- **Note:** This lens is essentially *retired by the determinism constraint*. There is **no
  per-operation LLM latency/cost on the player's critical path**, no async/timeout/fallback to design,
  no runtime caching strategy needed — the hardest part of the lens evaporates. The residual LLM cost
  is **build-time authoring throughput** (the `ontology-generator` over ~25 materials + ~20 operations
  + response text for one scene, replenished by the wall-sensor queue, DR-09/DR-18) — bounded,
  offline, and a *tooling* concern for the implementation-lens pass, not a runtime budget. Cleanest
  card in the set, and it's clean *because* of DR-02.

## AR10 Security / Griefing Surface
- **Verdict:** YELLOW
- **Evidence:** DR-15 (instanced co-op runs; a run = a `run_id`-tagged shared world-state), DR-10
  (irreversible Effects: `consume`, `remove_part`, burn), DR-08/DR-02 (deterministic parser, **no
  runtime NL model**), DR-14 (event-driven clock + liveness rule + consensual fast-forward).
- **Severity:** low.
- **What would change the verdict:** a stated intra-party authorization / undo / rate-limit model on
  shared run-state, or an explicit "co-op is trusted small-group, griefing out of scope" decision.
- **Note (mostly deferred to the multiplayer phase).** Two halves. **Closed (GREEN aspect):** the
  classic LLM-parser injection vector is **gone** — DR-08's deterministic told-format parser with no
  runtime model means there is no NL prompt to inject through (a real benefit of DR-02). **Open:** in a
  shared instanced run (DR-15) all party members can act on any reachable object with no per-player
  ownership/authorization, and the mutation set (DR-10) includes **irreversible** acts on **finite
  shared resources** — a malicious or careless co-op member can burn the antenna or eat the food. The
  global solvability floor (DR-16/AR6) keeps the *world* winnable but does not stop *teammate* griefing
  or denial-of-fun (e.g. withholding consent to fast-forward — DR-14's liveness rule handles the *idle*
  party but not a *present-but-obstructive* one). Low stakes if co-op is friends-only; the architecture
  should *say* that scope rather than leave shared-state authorization unspecified.

## AR11 Data-Model Soundness
- **Verdict:** YELLOW (med→high)
- **Evidence:** DR-11 (the ledger: `material_identity_preserved`, `balanced(mass, sink=ENVIRONMENT)`,
  `contamination_and_heat_transfer_consistent`, `provenance_extended`, `separated_sums`; per-channel
  tolerances; the explicit **environment sink**), DR-06 (`EntityState`: `mass_kg`, `state{}`,
  `parts:[Part]`, `provenance`; `Part{id, material, attachment, outputs_when_removed}`), DR-04.
- **Severity:** med (high for the conservation claim).
- **What would change the verdict:** (a) **bound the sink** — make each Effect declare *typed* sink
  contributions (smoke-mass, lost-heat) so the sink can't silently absorb authoring error; (b) route
  **every** state change including tick/`systems` updates through ledger-gated Effects (see AR15);
  (c) give `Part` a `mass` (or state the invariant `object.mass_kg == Σ part.mass + loose`).
- **Note (high-leverage focus).** The model **largely closes for active transforms**: `separate→
  outputs` + `separated_sums` makes cut-pieces-sum-to-original checkable, `provenance:list[str]` +
  `provenance_extended` closes provenance, partial success is just a `state{}` progress field
  (conservation-neutral until pieces are produced). **Three soundness gaps keep it off GREEN.**
  (1) **The environment sink is an unbounded catch-all (DR-11).** It "absorbs mass/energy that
  legitimately leaves the modeled world" — but the ledger cannot distinguish *legitimate* loss from an
  *authoring bug that lands within tolerance*. A sink that absorbs whatever remainder is needed weakens
  the flagship invariant from "mass is conserved" to "mass is conserved ± whatever the sink ate." Per-
  channel tolerances bound the magnitude but not the *category* of error. (2) **Passive, time-driven
  state change may live outside the schema the ledger sees.** Heat loss, drying, fire burning fuel down
  over minutes are inherently *continuous and relational*, and the layout puts them in
  `systems/{warmth,water,fire}.py` — the ledger runs "inside `apply()`" on the **action** path, so the
  question "is the cooling/drying/burning ledgered?" is unanswered, and if those systems write state
  directly the conservation books are only balanced for player actions, not for the survival sim that
  most needs them (overlaps AR15). (3) **`Part` carries no mass.** The schema has `object.mass_kg`
  (one float) and parts with no mass field; when a part becomes a derived object, its mass comes from
  `outputs_when_removed`, so there is **no schema-level invariant that parts' masses sum to the
  object's** — `separated_sums` leans entirely on authored output specs being right. The model is
  computable, but only if the sink is typed, the tick path is ledgered, and part/object mass is
  reconciled — three things the schema doesn't yet enforce.

## AR12 Testability (invariants vs enumeration)
- **Verdict:** GREEN
- **Evidence:** DR-18 / DR-19 / §10 / GDD §0a#6: replace 700 enumerated tests with **invariants +
  fuzz** — conservation balances, **narration↔Effect**, rescue-confidence monotonic & reachable,
  every-attempt-resolves, **seeded-replay determinism**, clock liveness, warmth floor; Tier-1 pure
  pytest (ms) over the whole core; the solvability fuzz oracle (≥10k).
- **Severity:** low (caveat).
- **What would change the verdict:** discovering that a named invariant ("conservation balances")
  silently *doesn't cover* a real state-change path (the tick/systems bypass — AR15) and so passes
  while the world is unconserved.
- **Note:** Textbook-correct for a large open behaviour space: properties + a seeded, **replayable**
  fuzz oracle (enabled by DR-12/DR-02), a pure core testable in milliseconds without a DB, and honest
  scoping ("quality cannot be certified — curated + playtested"). The one caveat is *coverage of the
  invariants, not their form*: each property is only as strong as the path it observes. "Conservation
  balances" is asserted over `apply()`; if survival `systems/` mutate state outside `apply()` (AR15),
  the property is green while conservation is actually violated on the continuous path. Make the
  invariants enforce the *boundary* (all state change is a ledgered Effect), and this stays GREEN.

## AR13 Premature Abstraction
- **Verdict:** YELLOW
- **Evidence:** DR-05 (the operation interpreter + closed `Predicate`/`Modifier`/`EffectSpec`
  expression language), the whole **22-decision register settled before any code** (CLAUDE.md:
  `world/sim` / scenarios / tests "Not built yet"), §4.5 ("the BotW 3-rules / ScienceWorld 25-actions"
  analogy as justification), DR-22 (the vertical slice as the antidote).
- **Severity:** med.
- **What would change the verdict:** build the DR-22 slice (~15 operations, tiers 1/3/5) and show the
  interpreter's node set expressed all of them with **zero interpreter edits** — i.e. the abstraction
  is earned by content, not by analogy.
- **Note (high-leverage focus).** This is a **framework-first design**: a generalized interpreter, a
  bespoke closed DSL, an op×material index, a conservation engine with an environment sink, a
  bake/fuzz toolchain, and 22 interlocking decisions — **authored before a single operation or
  material exists to stress them.** The central abstraction (the closed expression language, DR-05) is
  justified by *post-hoc analogies to other games* (BotW, ScienceWorld) rather than by Whiteout content
  proving its node types fit; the node set is described as "a handful" and **not enumerated**, so the
  claim "this DSL can express our operations" is asserted, not demonstrated — and §4.6/§11 already show
  the FSM and the survival dynamics escaping it. The strong **mitigation** is that DR-22 puts the slice
  *first* and explicitly frames it as "prove the core before building the rest," which is the right
  de-risking order. But the *document* scores DR-05 as a settled decision in the register (to be
  certainty-graded in `30-certainty.md`) when it is in fact the highest-uncertainty bet in the system:
  if the first 15 operations need 8 new node types, or half of them turn out to be `systems/`/packet
  code, the "data not code" thesis and several downstream decisions move together. Treat DR-05 as
  *provisional pending the slice*, not settled.

## AR14 God Object
- **Verdict:** YELLOW
- **Evidence:** DR-09 (the resolver, 5 tiers), DR-05 (the operation interpreter,
  `operations/interpreter.py`), DR-11 (the conservation ledger, `conservation/ledger.py`), §12
  (`contracts.py` as the shared dataclass kernel).
- **Severity:** low–med.
- **What would change the verdict:** the interpreter evaluating node types via a **registry of
  per-node handlers** and the ledger running **per-channel checks as registered plugins**, so each
  grows by adding a small handler, not by fattening a central switch.
- **Note.** The **resolver is well-defended** against god-objecthood — the tiers + the O(1)
  op×material index (DR-09) keep per-operation logic in *data*, so the resolver stays thin by
  construction (its job is dispatch, not physics). The two natural **growth sinks** are elsewhere:
  (1) `operations/interpreter.py` (DR-05) must evaluate *every* node type the expression language ever
  gains — and AR8/AR13 show pressure to grow that set — so it tends toward "the module that knows how
  to evaluate everything." (2) `conservation/ledger.py` (DR-11) accretes one check per conserved
  channel (mass, heat, contamination, provenance, length-count, …); it is by design "the module that
  knows all of the world's physics," and every new physical quantity adds to it. Neither is a problem
  *yet* (no code), but the design concentrates two unbounded responsibilities; specify them as
  open-for-extension (handler registries) now, while it's free.

## AR15 Leaky Abstraction / Missing Invariants
- **Verdict:** **RED**
- **Evidence:** P4/P5 + DR-10 ("the shell's `apply()` is the **only writer**," "nothing mutates state
  except an applied Effect that passed the ledger"), DR-11 (the ledger "runs **inside `apply()`**,
  before commit"), §11 (`systems/{fire,warmth,water,injury,…}.py`), §7 (activities persisted to
  **Attributes**), research §8 (the Evennia perf rule: drive survival meters with **lazy traits /
  `.ndb`** to **avoid per-tick DB writes** — i.e. *outside* the Attribute/Effect path).
- **Severity:** high.
- **What would change the verdict:** (1) a **runtime write-guard** that makes `apply()` the *enforced*
  sole mutator of game-state Attributes/Tags (e.g. a single `Object.apply_effects()` choke-point + a
  `make validate`/test that forbids direct `obj.db.<state>` writes outside it); (2) an explicit rule
  that **all** state change — including every tick/`systems` update — is a **ledger-gated Effect**;
  (3) `apply()` wrapped in `django.db.transaction.atomic` covering the Attribute writes **and** the
  Tag mirror so "atomic, all-or-nothing" is mechanized, not asserted.
- **Note (THE finding).** The flagship invariant — *conservation holds at runtime*, the GDD's #3
  binding decision — is, as architected, **documented but not enforced on the path that matters most.**
  Three leaks compound: (1) **"`apply()` is the only writer" is a convention, not a boundary.** Evennia
  gives every typeclass public `obj.db.x = …` write access; nothing structural stops a command or a
  system from mutating state directly and skipping the ledger. The lens's exact smell: *"a rule that's
  only a doc line with no runtime assertion is unenforced; boundaries callers can bypass."* (2) **The
  survival sim is the path most pressured to bypass it.** Continuous heat/water/fire/injury dynamics
  live in `systems/*.py`; the *Evennia performance guidance the project itself cites* (research §8)
  says to keep per-tick meters on lazy traits / `.ndb` to avoid per-tick DB writes — i.e. **off** the
  Attribute/Effect/ledger path. So the very physics conservation most needs to govern (fuel burning
  down, heat lost, water freezing) is the physics steered *around* the ledger, and the doc never
  reconciles "everything is a ledgered Effect" with "don't write Attributes every tick." (3)
  **Atomicity is claimed without a mechanism.** "Applied atomically, all-or-nothing" (DR-10) needs a DB
  transaction spanning the multi-Attribute write *and* the Tag mirror (AR3); none is cited, so a
  mid-apply failure or an `@reload` between writes can leave a half-mutated, unconserved world. Until
  the mutation boundary is *enforced* (one guarded choke-point), *total* (ticks included), and *atomic*
  (transactional, Tags included), the conservation ledger is a gate on the front door of a building with
  the back wall missing.

## AR16 Over-Configuration
- **Verdict:** YELLOW
- **Evidence:** DR-05 (operations = declarative records: `preconditions`/`modifiers`/`effects`/
  `duration`/`partial`/`failure` — logic encoded as expression-node data), DR-04 (materials = ~25-field
  ordinal property vectors), DR-03/DR-17 (content authored as data, validated, **baked** to a numeric/
  indexed form the runtime loads), DR-20 (the decision trace), §9 (validator / content-lint).
- **Severity:** low–med.
- **What would change the verdict:** a validator rule requiring **every** material property explicitly
  present (no silent default to `none`/0), a **baked-form-matches-source** check, and confirmation the
  DR-20 trace names the *specific failing `.op` node*.
- **Note (focus).** The design *is* logic-as-data — preconditions and effects are an expression tree in
  a `.op` file, and a wrong resolution means reading data + the interpreter, not a Python function. That
  is inherently harder to debug than code, and the wide material vectors (~25 ordinal fields each) are
  the classic **under-filled-and-silently-defaulted** content-bug surface: an omitted `conductivity`
  defaulting to `none` reads as "safe to grab the live wire," an invisible bug. **But this is better
  mitigated than the typical over-config case:** the **ordinal scheme bounds the value space** to seven
  named tokens (DR-04), a **validator gates content** at build *and* load (DR-17/§9), and crucially the
  **DR-20 decision trace surfaces which precondition failed** — turning logic-as-data from a black box
  into something traceable. So the verdict is YELLOW not RED chiefly on two unspecified guarantees: the
  doc does **not** state the validator enforces material-vector *completeness* (the silent-default risk
  is live), and the **bake step** (authored→numeric/indexed) is a second representation that can drift
  from source without the proposed equivalence check. Specify both and this trends GREEN.

## AR17 Untested Critical Path & Error-Handling Gaps
- **Verdict:** YELLOW
- **Evidence:** DR-18 (≥10k fuzz over the resolution/conservation/solvability space), DR-11 (a runtime
  ledger **rejection** "fails the action as an engine error, logged"), DR-14 (activities persisted to
  Attributes, partial progress on interrupt, `@reload`-durable), DR-15 (instance create/reset/**GC**
  reaper), DR-10 ("atomic" apply).
- **Severity:** med.
- **What would change the verdict:** a defined **player-facing behaviour for a runtime ledger
  rejection** (graceful "that didn't work" + log, never a stack trace to the player), a specified
  `apply()` transaction so an `@reload` mid-apply can't half-mutate, and contention/GC-race tests when
  DR-14/15 land.
- **Note.** The *happy-and-space* path is **exceptionally** covered — seeded fuzz + property tests +
  replay (DR-18/DR-12) are exactly right for an open behaviour space. The **rare-but-catastrophic**
  paths are under-specified: (1) **Runtime ledger rejection (DR-11).** "A rejection is a bug, logged"
  describes build-time; if unphysical baked content reaches production, a player's reasonable action
  *fails as an engine error* with **no defined player-facing experience** — the catastrophic path isn't
  designed for the player. (2) **`apply()` atomicity under `@reload`/failure.** Claimed atomic (DR-10)
  but with no transaction mechanism (AR15) — a reload between Attribute writes can strand a half-applied
  world; the durable-activity invariant (§10) tests the *activity*, not a torn `apply()`. (3)
  **Multiplayer contention (DR-15)** — the snapshot TOCTOU (AR3) is an untested concurrent-writer path.
  (4) **Instance GC races (DR-15)** — the reaper deleting `run_id`-tagged objects vs. an in-flight
  action or a reconnect is unaddressed. The slice (DR-22, single-player, no clock) legitimately
  sidesteps 2–4 — which is *why* they're untested — but they are the paths that bite when DR-14/15
  arrive, and the runtime-rejection UX (1) is live even in the slice.

---

## Top findings

**The three most important RED/YELLOW:**

1. **AR15 (RED, high) — the conservation ledger is an unenforced convention, and the survival sim is
   steered around it.** DR-10/DR-11 make `apply()`+ledger the "only writer," but Evennia Attributes are
   directly writable (the boundary is a doc line, not a guard), the cited Evennia perf guidance pushes
   per-tick survival state *off* the Attribute/Effect path, and "atomic" apply has no transaction
   mechanism. The flagship runtime invariant (GDD binding decision #3) is enforced on the action path
   and open on the continuous-physics path that needs it most.

2. **AR8 + AR13 (YELLOW, med) — the closed expression language / interpreter is an unvalidated
   framework, and "data not code" is true only inside an undrawn envelope.** DR-05 settles a bespoke DSL
   + interpreter + 21 dependent decisions *before any operation exists to stress them*; the node set is
   "a handful," unenumerated, and FSMs (radio) and continuous dynamics (eight `systems/*.py`) already
   escape it. The DR-22 slice is the right antidote but hasn't run, so DR-05 is the system's
   highest-uncertainty bet dressed as a settled decision.

3. **AR3 (YELLOW, med) — the Tag mirror of the Attribute truth has no specified transactional sync.**
   DR-07 duplicates every queryable axis (material/zone/affordance) as a Tag *and* an Attribute but
   names no mechanism keeping them coherent across a state-changing Effect, so indexed queries (DR-09)
   can go stale; under DR-15 the same read-snapshot-then-write-later shape becomes a multiplayer TOCTOU.

**The single most important architectural fix:** *make `apply()` + the ledger the one **enforced**,
**total**, **atomic** state-mutation path.* Concretely: (a) a single guarded mutation choke-point plus a
`make validate`/test forbidding direct game-state Attribute writes outside it (enforce P4/P5/DR-10);
(b) a rule that **every** state change — including all tick/`systems` updates — is a ledger-gated Effect,
reconciled against the per-tick-write perf guidance via batched/coalesced Effects rather than
ledger-bypass (close AR15 + AR11's tick gap); (c) wrap `apply()` in one `transaction.atomic` covering
Attributes **and** the Tag mirror (close AR3's sync + AR17's torn-apply + DR-10's atomicity claim). This
one change converts the project's headline invariant from *documented* to *enforced* and resolves the
core of four findings (AR15, AR11, AR3, AR17) at once.
