# 20 — Implementation / feasibility lens review (IM1–IM12)

**Artifact under review:** `docs/architecture/implementation-architecture.md` (v1, decisions register
DR-01…DR-22). **Question:** *can this architecture actually be built and run on Evennia* —
feasibility, not game design. **Primary evidence:** the decisions register (§2 of the target) and
`docs/investigation/research/evennia-interactive-worlds.md` (cited below as **EV-§N**, by its numbered
sections: EV-§1 perception/`return_appearance`, EV-§2 ticks/Scripts, EV-§3 parser, EV-§4 propagator,
EV-§5 Attributes/Tags/idmapper, EV-§6 LLM async seam, EV-§7 contribs, EV-§8 scaling). **Hard
constraint (GDD §0a.1, DR-02):** runtime is 100% deterministic; the LLM is build-time only.

## Triage (leverage = impact × uncertainty for THIS artifact)
- **HIGH:** IM1 (framework fit), IM2 (reactor), IM8 (perf), IM10 (replay determinism), IM9 (persistence).
- **MED:** IM5 (authoring throughput), IM6 (coverage), IM7 (test strategy), IM11 (tooling), IM12 (drift).
- **LOW / retired-by-design:** IM3 (build-time only, human-gated), IM4 (no runtime LLM at all).

---

### IM1 Framework Feasibility
- **Verdict:** GREEN (one YELLOW seam)
- **Evidence:** DR-01 core/shell split; DR-07 Tags-for-axes; DR-12/§12 per-action WorldView build;
  DR-13 per-observer `return_appearance` + propagator; DR-14/15 heartbeat & reaper Scripts; DR-08 parser.
  Cross-checked against EV-§1–§5, §7.
- **Severity:** low (the friction is confined and already mitigated).
- **What would change the verdict:** the parser turning out to need a `settings.COMMAND_PARSER` override
  (EV-§3's heaviest option) rather than one dominant told-format `Command`; or the propagator proving to
  need framework-fighting beyond the `send_emote` pattern.
- **Note:** This design is unusually *with-the-grain* because it deliberately avoids both of EV's YELLOW
  areas. Count the integrations and their blessed extension points: **(1)** WorldView built per action
  from `room.contents` + Attributes/Tags is idiomatic — idmapper makes those reads dict-fast (EV-§5),
  and the single-scene design keeps it over a small in-memory set rather than cross-DB queries (EV-§5
  "Whiteout-specific relief"). **(2)** Per-looker render via `get_display_*(looker)` on `ObjectParent`
  is *the designed extension point*, GREEN in EV-§1. **(3)** The push propagator (DR-13) copies the
  in-core `rpsystem.send_emote` reference — bespoke but proven (EV-§4), and deferred past the slice
  (DR-22) so it carries no slice risk. **(4)** Heartbeat = Global Script, reaper = Script with
  `at_repeat()`/`is_valid()` — blessed (EV-§2). **(5)** Tags for queryable axes is the *documented fix*
  for Attributes-not-queryable-by-value (EV-§5). The **one seam:** DR-08's parser. EV-§3 rates a
  *primary NL* loop YELLOW because Evennia's prefix matcher pre-empts free text — but DR-08 explicitly
  rejects NL ("deterministic told-format + synonym tables; no NL model; richness from rule coverage").
  A verb-first told format maps cleanly onto Evennia Commands. The unpinned detail: whether ~15–20
  operation verbs become individual `Command`s (risk: single-letter aliases collide with `look`/`north`
  via abbreviation, EV-§3) or one dominant `Command` with a rich `parse()` (EV-§3's recommended path).
  Recommend the latter and disable abbreviation for the family. No subsystem fights the framework at the
  slice scope.

### IM2 Reactor / Concurrency Model
- **Verdict:** GREEN (two YELLOW sub-notes)
- **Evidence:** Principle 1/2 + DR-02 (no IO/LLM/wall-clock in `resolve()`); §12 (WorldView built once
  per action); DR-10 (effects as atomic DB writes); DR-11 (in-`apply()` ledger `simulate`); DR-14
  (activities). EV-§2 (per-tick DB-write trap), EV-§6 (reactor must never block), EV-§8 (write load).
- **Severity:** med (the sub-notes are correctness/scaling, not blockers).
- **What would change the verdict:** choosing the real-time clock option (DR-14) without adopting
  `traits.rate` lazy meters (EV-§7/§8); or activity steps caching a start-of-activity snapshot instead of
  re-reading live state.
- **Note:** The headline is a *win*: because `resolve()` + the ledger do **no IO and call no model**
  (DR-02), the #1 general Evennia hazard — a slow in-loop LLM blocking the single-threaded reactor and
  freezing every player (EV-§6) — is eliminated at runtime. Per-action work is pure Python over a
  small snapshot: build WorldView over `room.contents` (idmapper dict-reads, EV-§5), an O(1)
  operation×material index lookup (DR-09), and `simulate(pre, effects)` over the *touched* entities — all
  µs-to-low-ms, never blocking. Write amplification (DR-10): a single "cut" can emit ~5–15 Attribute
  writes (remove_part + create_object + state/provenance), but actions are human-paced (≪1/s), far below
  EV-§8's "bottleneck only when reading **and** writing many times per second." **Sub-note A — per-tick
  writes:** EV-§2/§7/§8 name the real trap as a *fast ticker writing Attributes across many objects*, and
  name `traits.rate` (lazy, compute-on-read, **zero per-tick DB write**) as the fix for survival meters.
  The event-driven clock (recommended, DR-14) sidesteps this entirely (meters recompute on action); but
  if the real-time option is taken, the doc does **not** yet adopt `traits.rate` for hunger/thirst/
  warmth — it should, explicitly. **Sub-note B — multi-tick activity races:** single actions are atomic
  on the reactor thread (no interleave), so no intra-action race. But a long Activity (DR-14) spans many
  ticks; in instanced co-op (DR-15) another player can mutate the activity's target between ticks (burn
  the beam being sawed). Each activity *step* must rebuild its WorldView from live state and re-validate
  preconditions, not operate on a frozen start-snapshot. The doc says steps "accrue progress" but does
  not state the re-read/re-validate rule — pin it.

### IM3 LLM Ontology-Authoring Throughput
- **Verdict:** YELLOW
- **Evidence:** DR-02 (build-time only), DR-05 (closed expression language), DR-17 (generate → validate
  + ledger → bake; golden table extended-not-overwritten), DR-11 (ledger as physics gate).
- **Severity:** med (slows authoring; not a build/run blocker — humans + a hard gate stand between the
  LLM and runtime).
- **What would change the verdict:** a measured slice repair-rate (fraction of generated ops/materials
  passing `validate`+ledger without human rework). None exists yet.
- **Note:** Structurally this is the right shape to keep drift/hallucination low: the **closed DSL**
  (DR-05, "a handful of node types") bounds what generated content can even express, so a hallucinated
  capability that violates physics fails the conservation ledger at build time (DR-11/DR-17), and the
  hand-curated golden material table (DR-04/DR-17) is the anchor the generator *extends, never
  overwrites*, bounding cross-generation contradiction. The residual risk is purely empirical and
  build-time: the repair rate is unproven until the slice is authored. Because it is human-gated and
  never reaches the runtime (DR-02), the worst case is "authoring is slower than hoped," not "unsafe at
  runtime." Hence YELLOW, not RED.

### IM4 Runtime LLM Latency / Cost Realism
- **Verdict:** GREEN (retired by design)
- **Evidence:** DR-02 (no model inference at runtime); GDD §41 table; GDD §49 ("removing runtime LLM
  retires the determinism/latency/mis-parse risks"). EV-§6 (the async seam is the general blocking risk).
- **Severity:** n/a.
- **What would change the verdict:** any reintroduction of an in-loop model call (e.g. a runtime
  narration-enricher) — which the hard constraint forbids.
- **Note:** The entire class of in-loop-LLM p95/timeout/fallback risk is eliminated, not mitigated. This
  is arguably the single biggest feasibility advantage of the design: EV-§6 marks the LLM async seam as
  GREEN-but-bespoke and reactor-blocking as the dominant general hazard; Whiteout removes it from runtime
  wholesale. The only runtime latency budget is pure compute (covered under IM8).

### IM5 Authoring Throughput (human + AI)
- **Verdict:** GREEN at slice scale (YELLOW at full scale)
- **Evidence:** DR-22 slice scope (~25 materials, ~15 operations, ~5 objects, ~50 curated responses);
  DR-03/DR-05 (operations-as-data + closed DSL); DR-17 (generator + validator gate); DR-18 ("validator
  cannot certify delight"). GDD §5 ("few operations × many materials"), §49 (~50% confidence on fun).
- **Severity:** med (the bottleneck is the project's own central uncertainty, not a blocker).
- **What would change the verdict (to GREEN at full scale):** evidence that the redirect/template
  fallback (DR-09 tier 5) carries the long tail without per-interaction curation, *and* a measured rate
  at which curated "signature" responses can be produced.
- **Note:** The mechanics authoring scales as **O(operations + materials)**, not O(ops × materials):
  you author ~15 ops + ~25 materials and the interpreter *derives* the ~375 interaction cells (DR-05,
  GDD §5) — this is the throughput engine and it makes the slice a days-to-weeks budget, not months.
  The closed DSL + validator+ledger gate (DR-17) makes LLM-drafted operations viable because every draft
  is machine-checkable. The genuine bottleneck is **delight, not physics**: the GDD's success test is a
  player saying "I can't believe that worked," and the witty/specific *signature responses* that produce
  it are O(interesting-interactions), hand-curated, and explicitly **un-certifiable by the validator**
  (DR-18). ~50 responses for the slice is realistic; keeping a *full* dense scene feeling witty
  everywhere is the open-ended cost the GDD itself rates at ~50% (§49). The architecture is honest about
  this (quality = curated + playtested), so the verdict is GREEN-for-slice / YELLOW-for-scale.

### IM6 Coverage Verification
- **Verdict:** GREEN
- **Evidence:** DR-18 (coverage = operation×material matrix complete + property-tested **plus** ≥10k
  seeded fuzz with 0 unresolved / 0 conservation violations / rescue reachable); DR-09 (wall-sensor);
  GDD §44/§0a.6 (replaces 700+ enumerated tests).
- **Severity:** low.
- **What would change the verdict:** discovering that the higher-order interaction space
  (op × target-material × tool-material × state-modifiers) has failure modes the pairwise matrix + fuzz
  sample systematically miss.
- **Note:** This is textbook-correct for a "do-anything" system: it replaces the **unbounded** "everything
  interacts" with a **bounded** basis (≈20 ops × 25 materials ≈ 500 enumerable cells) + a fuzz sample +
  an explicit solvability oracle. The one honest caveat to name: the bounded basis is *pairwise*
  (operation×material), while real interactions are higher-dimensional (tool material, frozen/wet/
  contaminated state, modifiers). Pairwise enumeration + fuzz sampling of the combinations is the right
  compromise (standard n-wise testing), but the doc should *call it that* — the matrix proves each
  (op, material) cell resolves; the ≥10k fuzz is what samples the tool/state/modifier cross-product, and
  the wall-sensor (DR-09) is the empirical gap detector that turns unbounded into a worklist.

### IM7 Test Strategy
- **Verdict:** GREEN
- **Evidence:** DR-19 (Tier-1 pure pytest + Tier-2 Evennia integration; property/invariant tests:
  conservation, narration↔Effect, rescue-monotonic, every-attempt-resolves, replay determinism, clock
  liveness, warmth floor); DR-01/DR-21 (pure core, no evennia imports; CLAUDE.md ADR-0003).
- **Severity:** low.
- **What would change the verdict:** a leak of Evennia/Django into `world/sim` (an `EntityState` carrying
  a live Evennia object ref, or a global `random`/`datetime` in the core) breaking Tier-1 purity.
- **Note:** The shape is exactly right — property/invariant tests + a curated golden set + fuzz, not N
  hand cases (the GDD §0a.6 delta). **Tier-1 purity is genuinely achievable and enforceable:** the
  contracts (`EntityState`, `Effect`, etc.) are plain dataclasses of str/float/list (DR-06), the
  WorldView is the only read boundary (§12), and `world/sim/**` is forbidden Evennia imports
  (DR-01/DR-21). That claim is *testable*, so make it an enforced gate: an import-boundary test asserting
  no `evennia`/`django` symbol is reachable from `world/sim` (proposable as a `make validate` rule). The
  invariants listed map one-to-one to property tests; this review's IM10 finding adds one more
  (seed-double-run determinism).

### IM8 Performance
- **Verdict:** GREEN (YELLOW on DR-06 proliferation)
- **Evidence:** §12 (WorldView built per action, "discarded after Effects apply" — no caching/dirty-flag);
  DR-09 (O(1) op×material index); DR-11 (`simulate(pre, effects)`); DR-06 (part removal → first-class
  derived object); DR-15 (instanced GC). EV-§5 (idmapper dict-fast reads + RAM cost), EV-§8 (low-hundreds
  concurrency, per-tick traps, "caching is king").
- **Severity:** med.
- **What would change the verdict:** a long run accumulating thousands of derived objects in one scene
  (pushing WorldView build and idmapper RAM up), or a `simulate()` that deep-copies the *whole* WorldView
  per action rather than the touched subset.
- **Note:** **The hot-path compute is comfortably within budget at realistic scale.** Order-of-magnitude:
  an idmapper Attribute read ≈ a Python dict access (~50–100 ns, EV-§5); building one `EntityState` (~10
  attrs + dataclass) ≈ 1–5 µs; so a WorldView over N objects ≈ N×(1–5 µs). Slice N≈5 → ~25 µs; N=100 →
  ~0.5 ms; N=1000 → ~5 ms. A `look`/action exceeds the ~100 ms budget only around **N ≈ 10k–20k objects
  in a single scene**, which an instanced ~1-in-game-day run with end-of-run GC (DR-15) should never
  approach. The index lookup is O(1) (DR-09) and `simulate` touches the affected subset, so neither
  scales with N. Even against EV-§8's concurrency ceiling (50 bots `look`/2 s ≈ 45% CPU; ~low-hundreds
  players), instanced co-op of ~1–6 human-paced players per run sits far under it — the heavier
  per-action compute (resolve + ledger) is still ms-scale, dwarfed by network/parse overhead. **The one
  real risk is DR-06 object proliferation:** every part-removal mints a *first-class* derived object, so
  a player who cuts/separates repeatedly multiplies `room.contents` within one run — each new object is
  idmapper-resident (EV-§5 RAM cost), each lengthens every subsequent O(N) WorldView build and every Tag
  query, and all must be bulk-deleted at teardown. It is bounded only by the ~1-day run + GC, with no
  within-run debris cap. Two cheap fixes: coalesce identical loose scraps, and demote non-interactive
  debris to a count rather than N live objects. Separately, §12's "build per action, discard" has **no
  caching/dirty-flagging** — fine at single-scene N, but it is an explicit O(N)-per-action with no reuse;
  worth a note if N ever grows.

### IM9 Persistence / Session Model
- **Verdict:** GREEN
- **Evidence:** DR-15 (instanced run = objects tagged `run_id`; create on start, persist in Postgres,
  reset by deleting the tagged set, GC via a reaper Script for runs with no connected sessions); DR-14
  (activities persisted to **Attributes, not `.ndb`**, to survive `@reload`). EV-§2 (Script persistence,
  the `persistent=False`-comes-back-stopped trap), EV-§5 (`.ndb` cleared on reload; Tags as the
  queryable primitive), EV-§7 (prototypes/spawner as the data-driven instantiation backbone).
- **Severity:** low.
- **What would change the verdict:** the reaper failing to map `run_id`→characters→sessions correctly
  (orphaning or premature-GCing a run), or an activity heartbeat built on a `persistent=False` ticker
  (EV-§2's "timers vanished after shutdown" bug).
- **Note:** The lifecycle is idiomatic on every axis. Tagging the run's object set with `run_id` and
  querying/deleting by Tag is exactly the queryable-primitive use case (EV-§5; "find all objects in run
  X" = `search_tag`). The reaper is a Global Script with `at_repeat()`/`is_valid()` — blessed (EV-§2).
  Fresh-world-per-run instantiation should use prototypes/spawner (EV-§7). **The DR-14 activity-durability
  decision is exactly right and matches the Evennia facts:** `.ndb` is wiped on `@reload` (EV-§5), so
  persisting in-progress activities to **Attributes** (Postgres) on a **persistent** Script (default
  `persistent=True`, EV-§2) is correct — the doc explicitly avoids the `.ndb` trap. Partial-presence is
  handled: the run lives in Postgres and the activity runs on the Script (not a player session), so a
  disconnect doesn't lose the run, and GC fires only when *no* session remains (after a timeout) — the
  clock/state is owned by the Script, cleanly decoupled from any one player. Minor watch-items, none
  blocking: the reaper's `run_id`→session mapping; bulk teardown cost when DR-06 debris is large; and the
  first action after `@reload` rebuilding WorldView from a cold (idmapper-flushed) cache.

### IM10 Determinism / Fuzz Harness
- **Verdict:** YELLOW
- **Evidence:** DR-12 (per-run seed; resolution pure; "stochastic elements draw from a per-run seeded RNG
  passed through the snapshot — never `random`/`time`"); §12 ("`WorldView`: read-only … built from
  Evennia per action"); DR-18 (≥10k seeded fuzz + the solvability oracle; replay); DR-06 (`create_object`
  mints derived objects); DR-01/DR-19 (pure core; Tier-1 "milliseconds"). EV-§5 (idmapper/dbid/timestamp
  surfaces), EV-§8.
- **Severity:** med-high — the *entire* verification edifice (the solvability oracle, coverage,
  regression replay) rests on bit-exact replay, and two determinism leaks are currently unpinned.
- **What would change the verdict (to GREEN):** the doc stating that (1) the fuzz/replay harness runs on
  the **pure core with an in-memory WorldView** (never through Evennia's DB/idmapper/clock), and (2) all
  object-id minting and any "random" draw come from the **per-run seeded RNG** (a deterministic counter
  for ids), with `EntityState` forbidden from carrying `dbid`/`uuid`/`datetime`; plus a property test
  that runs the same seed twice and asserts **identical Effect *and* Event streams**.
- **Note:** The *core* is architecturally replayable — `resolve()` is a pure `f(attempt, world,
  seed_state)` (DR-12), ordered collections use `list` not hash-randomized `set` (DR-06: `materials`/
  `tags`/`parts` are lists), and the ledger's ± per-channel tolerance (DR-11) absorbs float-summation
  order drift. But two traps sit *between the core and Evennia* and the doc does not close them.
  **Trap 1 — the replay path.** Replay/fuzz must run on the pure core with a synthetic in-memory
  WorldView; if it replays through the imperative shell, Evennia injects nondeterminism (auto-incrementing
  `dbid`s, attribute `date` stamps, idmapper identity, EV-§5). DR-01 + DR-19's "milliseconds" *imply* a
  pure harness, but it is never stated — and the determinism guarantee depends on it. **Trap 2 — id
  minting.** DR-06's `create_object` mints a *first-class* derived object per part-removal; if its id (or
  provenance string) comes from an Evennia `dbid`, `uuid4()`, or wall-clock, two runs of the same seed
  diverge on object identity and the replay/oracle goes flaky. Ids must be minted from the seeded RNG /
  a deterministic counter. Until both are pinned and guarded by a double-run property test, "the fuzzer
  replays runs exactly" (DR-12) is an aspiration, not a proven property — and it is the foundation the
  whole DR-18 coverage/solvability story stands on.

### IM11 Tooling & AI-Assisted-Build Practices
- **Verdict:** GREEN
- **Evidence:** DR-17 (author → validate (+ledger) → bake → runtime loads baked; golden table extended-
  not-overwritten); DR-18 (`solvability-fuzz` → wall-sensor as the prioritized authoring queue); DR-11
  (single ledger used at both build-validate and runtime-apply); §9; CLAUDE.md (validate is a hard gate
  at load/CI/`verify`). Skills: `ontology-generator`, `solvability-fuzz`.
- **Severity:** low.
- **What would change the verdict:** the baked artifact drifting out of sync with authored source (a
  stale index loaded at runtime), or the build-time validator ledger forking from the runtime ledger.
- **Note:** The pipeline is a clean, non-bloated DAG — generate → validate → **bake** → load — with a
  genuinely good feedback loop: the fuzzer's **wall-sensor** (DR-09/DR-18) empirically names exactly which
  attempts hit the generic redirect, turning the unbounded "what's left to author" into a prioritized
  worklist. Each tool earns its place (generator drafts, validator+ledger gate, fuzz finds gaps + proves
  solvability, bake transforms ordinals→numbers + builds the O(1) index). Two design choices avoid classic
  traps: bake *separates* the human-readable canonical source (`materials.table`) from the runtime form so
  the golden table stays the quality anchor (DR-17), and there is **one** ledger
  (`world/sim/conservation/ledger.py`) used at both build-validate and runtime-apply (DR-11), so content
  that passes the build cannot fail a *different* runtime check. The only discipline to enforce is the
  standard build-artifact one: re-bake in CI / `make verify` so a stale index never ships.

### IM12 Design-Intent Drift Control
- **Verdict:** YELLOW
- **Evidence:** Anchor = VISION.md / GDD + the §2 decisions register; enforced gate = validator +
  conservation ledger as a hard gate (DR-11, DR-17, CLAUDE.md) + the DR-19 property tests (conservation,
  narration↔Effect, determinism, every-attempt-resolves, import-boundary). DR-18 ("validator cannot
  certify delight").
- **Severity:** med.
- **What would change the verdict:** an enforced (even proxy) gate on *depth/non-shallowness* of authored
  content, or a measured "delight rate" from the slice playtest, so the soft axis stops relying solely on
  human vigilance.
- **Note:** Drift control on the **hard invariants is strong and enforced** — the AI must pass the
  conservation ledger, narration↔Effect, determinism, and the import boundary, not merely produce
  plausible prose; these are property-tested gates, not vibes (the right anchor + enforced-gate shape).
  The remaining drift exposure is the same seam IM5/IM3 surface: the validator certifies physics,
  conservation, and resolution but **not** delight or depth (DR-18). Over long AI-authoring loops, content
  can drift toward mechanically-valid-but-shallow responses and still pass every gate. Human curation +
  playtest is the only guard, and it is exactly where long loops erode. Hence YELLOW: bulletproof on the
  non-negotiables, unguarded on the soft quality axis the GDD itself flags as the make-or-break (§49).

---

## Top findings

**Three biggest feasibility risks**

1. **Replay determinism is unpinned at the Evennia seam (IM10, med-high).** The whole DR-18 verification
   story — the solvability oracle, coverage, regression replay — rests on bit-exact seeded replay (DR-12),
   but two leaks are open: the replay/fuzz path is not stated to run on the **pure core with an in-memory
   WorldView** (going through the shell injects `dbid`s/timestamps/idmapper identity, EV-§5), and DR-06
   `create_object` id/provenance minting is not pinned to the seeded RNG (a `dbid`/`uuid4`/clock id makes
   two runs of one seed diverge). Until both are closed and guarded by a double-run property test,
   "the fuzzer replays runs exactly" is an aspiration.

2. **DR-06 derived-object proliferation (IM8/IM2/IM9, med).** Minting a *first-class* object per
   part-removal lets `room.contents` balloon within a run — idmapper RAM (EV-§5), linear WorldView-build
   and Tag-query growth (the only per-action cost that scales with N), and bulk-teardown load — bounded
   only by the ~1-day instanced run + GC, with no within-run debris cap. Compute stays under the ~100 ms
   budget until ~10k objects in one scene, but RAM and build cost creep before that. Coalesce identical
   scraps; demote non-interactive debris to a count.

3. **The soft-quality / delight axis has no enforced gate (IM5/IM3/IM12, med).** The validator + ledger
   certify physics, conservation, and resolution but explicitly **cannot certify delight** (DR-18) — yet
   the GDD's success criterion *is* delight ("I can't believe that worked"), and signature-response
   authoring is O(interesting-interactions), human-gated, and the only guard against AI drift toward
   mechanically-valid-but-shallow content. This is the project's own central uncertainty (GDD §49, ~50%
   on fun); the architecture is honest about it but offers no instrument to measure or hold it.

**The single most important "build this differently"**

Make **determinism an enforced contract, not an aspiration.** Concretely: (a) state that the fuzz/replay
harness runs on the **pure core with an in-memory WorldView**, never through Evennia's DB/idmapper/clock;
(b) mint every object id and every "random" draw from the **per-run seeded RNG** (a deterministic counter
for ids), and forbid `EntityState` from carrying any `dbid`/`uuid`/`datetime`; (c) enforce both with a
property test that double-runs a seed and asserts identical **Effect *and* Event** streams, plus the
import-boundary test that `world/sim` imports no `evennia`/`django`. This converts DR-12/DR-18 from
"should replay" to "provably replays" — the foundation the entire solvability-oracle and coverage
edifice depends on, and cheap to lock in before the slice is authored.

---

## Summary (6 lines)
1. **Verdict spread:** GREEN IM1, IM2, IM4, IM6, IM7, IM8, IM9, IM11; YELLOW IM3, IM5(scale), IM10, IM12; no REDs.
2. **Biggest win:** DR-02's no-runtime-LLM constraint *eliminates* the dominant Evennia hazard — a slow in-loop model blocking the single-threaded reactor (EV-§6, IM4) — and keeps every hot path pure ms-scale Python.
3. **Framework fit is unusually good (IM1):** the design avoids both of EV's YELLOW areas by choosing a told-format parser (not NL, EV-§3) and a single scene + Tags (not cross-DB attribute queries, EV-§5).
4. **Top risk (IM10):** seeded replay — the basis of the whole DR-18 oracle/coverage story — is not yet pinned at the Evennia seam (replay path + DR-06 id minting); close it with a double-run property test.
5. **Scaling watch-item (IM8):** DR-06's first-class derived objects can proliferate within a run (idmapper RAM + linear WorldView build); bounded by instanced GC but needs a debris cap.
6. **Honest soft spot (IM5/IM12):** physics/conservation/resolution are enforced gates, but *delight/depth* — the GDD's make-or-break (~50%) — has none; it stays human-curated and is where long AI-authoring loops drift.
