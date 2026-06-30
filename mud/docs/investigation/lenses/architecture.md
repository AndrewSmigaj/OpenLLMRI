# Architecture lenses (AR1–AR17) — Whiteout finding cards

**Scope.** Reviewing the *intended* architecture of Whiteout = the original design
(`docs/scenarios/whiteout/design.md`, cited as §N) **as amended by** the engine proposal
(`docs/proposals/whiteout-engine-proposal.md`, cited as *proposal §N*). Goal: a deterministic,
testable, density-scalable simulation engine on Evennia where "everything interacts with
everything" is affordable and the LLM never owns state. Evidence on framework fit is drawn from
`docs/investigation/research/evennia-interactive-worlds.md` (*research §N*) and the current layering
(`docs/architecture/overview.md`, `docs/architecture/llm-integration.md`).

Verdicts judge the architecture **as now intended** — fixes the proposal lands are credited, residual
risks are flagged. Triage leverage (`triage.md`): HIGH lenses get a paragraph, MED a few sentences.

---

### AR1 Functional-Core Boundary
- **Verdict:** GREEN (holds)
- **Evidence:** ADR-0003 / `overview.md` "one idea": `world/sim/**` imports no Evennia/Django; the
  shell marshals Attributes → `contracts` dataclasses, calls pure `resolve()`, applies `Effect`s.
  Stage B is pure and the LLM is confined to Stage A + narrate + soft-judge (proposal §3.3, §4).
- **What would change the verdict:** a `time.time()`/RNG/network call discovered inside `world/sim`,
  or a soft-judge LLM call invoked *during* Stage-B resolution.
- **Note:** The split is well-specified and easy to enforce (uncertainty is low — triage MED). Two
  impurity vectors must be injected, not read: wall-clock time (`systems/clock.py` must take time as
  an argument, not call the clock; research §2 "derive time from a stored epoch" is shell-side) and
  RNG (proposal §4 seeded RNG). The one genuinely ambiguous boundary is **soft-judge-on-rails**
  (proposal §3.5): a verdict like "does this contraption count as a windbreak ≥ 0.5?" is logically a
  *resolution* decision, yet it calls an LLM. If that call lands inside Stage B, "Stage B is pure, no
  LLM ever" (`llm-integration.md`) leaks. The architecture survives only if soft-judge runs as a
  shell-side pre-pass whose clamped+cached verdict is fed *into* the pure resolver as an input — make
  that explicit.

### AR2 Coupling & Cohesion
- **Verdict:** YELLOW (at risk)
- **Evidence:** §9.3 lists ~13 things updated per tick (stamina, cold, injury, fire, smoke, weather,
  interruptions, noise, tracks, snow, rescue, visibility/audibility); `overview.md` maps these to
  separate `systems/*` modules. The perception propagator touches every event path (§11, §14).
- **Severity:** low
- **What would change the verdict:** evidence that the per-tick fan-out has a defined, tested update
  order and that systems communicate only via Events, not by reaching into each other's state.
- **Note:** Module cohesion is good (one file per system). The coupling hotspot is the **tick**: with
  the event-driven clock (proposal §7), one action advances time and cascades into all ~13 subsystems,
  so update *ordering* becomes load-bearing (it feeds AR4). Watch, don't redesign.

### AR3 Single Source of Truth / State Ownership
- **Verdict:** YELLOW (at risk)
- **Evidence:** Canonical store = Postgres Attributes; `overview.md` §7 makes the typeclass Effect
  applier "the *only* place that interprets Effects and writes Attributes" — one writer, good. But:
  the shell marshals Attributes → `EntityState` *snapshots* for actor/target/tool at Stage B
  (`overview.md` step 3); survival meters are recommended onto `.ndb` + lazy traits `.rate`
  (research §5/§8); soft-judge verdicts are cached "keyed by situation" (proposal §3.5); crystallized
  rules are promoted into the live rule set (proposal §3.6).
- **Severity:** high
- **What would change the verdict:** a documented optimistic-concurrency / re-validation check at
  Effect-apply time for *scheduled* actions, plus a cache-key invariant proving the soft-judge /
  crystallize key is a pure function of every state field the verdict reads.
- **Note:** The "Effects are the only writer over one canonical store" rule is a strong foundation and
  credits well. The divergence vectors the proposal has **not** closed: (1) **stale snapshot during
  timed work** — a long action (§9.3) marshals state at Stage B but applies Effects on a *later* tick;
  two actors who both snapshotted the same target then both commit will conflict (last-writer-wins
  silently). The snapshot is a denormalized copy that can diverge from canonical Attributes across the
  tick gap. (2) **Derived survival state** — hunger/stamina living as epoch + computed `.rate` (the
  perf win of research §8) is fine *only if* it is computed-only and never also written to `.db`, or
  "current stamina" has two authorities. (3) **Soft-judge / crystallize caches** become a second
  source of truth for facts like "is this a windbreak" — if the situation key omits a field the
  verdict depends on (the cloth later gets wet), the cache answers stale. Prose is safely downstream
  (state → narration, never the reverse) *iff* the AR15 assertion is actually enforced. Net: the
  ownership story is sound for instant actions and breaks at the timed-action / cached-verdict seams.

### AR4 Determinism & Reproducibility
- **Verdict:** YELLOW (at risk)
- **Evidence:** Proposal §4 lists the right tools — seeded RNG, cached intent parses + soft verdicts
  keyed by situation, deterministic fallback so a slow model never stalls a turn, pure Stage B,
  "transcripts replay identically and are testable." Proposal §7 replaces the §9.3 real-time heartbeat
  ("10–20 real seconds = 1 game-minute") with an event-driven, advance-on-action clock.
- **Severity:** high
- **What would change the verdict:** a written event-sequencing/replay spec + a fuzz harness (IM10)
  that asserts transcript-replay equality and fails on any divergence.
- **Note:** Two genuine wins to credit: pure Stage B removes the LLM from outcome decisions, and the
  event-driven clock makes game-time a function of *action count* rather than wall-clock, which is far
  more reproducible than the heartbeat. Three holes keep it YELLOW. (1) **Concurrent-action ordering:**
  the single-threaded Twisted reactor (research §0) serializes commands by arrival, giving *a* runtime
  order — but that order is wall-clock-arrival-dependent and is not reproducible from a transcript
  unless the exact interleaving is recorded and replayed; no event-sequence key is specified.
  (2) **LLM cache-as-authority in replay:** "replays identically" only holds if replay mode is
  *cache-only, no live call*, against a *version-pinned* model — a model bump silently changes any
  uncached parse/verdict. This is implied but not stated as a rule. (3) **The fallback is itself
  timing-dependent:** the same input yields different results depending on whether the model answered
  before the timeout, so the fallback/timeout decision must be recorded in the transcript or replay
  diverges. The pieces exist; "deterministic" is not yet an enforced property.

### AR5 Content-Density Scalability
- **Verdict:** GREEN (holds), trending YELLOW at the perception/object-count seams
- **Evidence:** Target density §46: 60–100 primary + 300–800 derived objects, 40–70 action families.
  Proposal §2/§3 inverts to cheap objects + ~25 material vectors + ~20 operations; behavior *derives*
  rather than being authored per object (the BotW / ScienceWorld lesson, proposal §1). Perception is
  graded per-observer over `room.contents` (§10–15; research §4 propagator loops observers).
- **Severity:** med
- **What would change the verdict:** a perception render budget/cache measured at 800 in-scene objects
  × party size, and an object-count bound (or strip-coalescing rule) measured under a "cut everything"
  fuzz run.
- **Note:** The operation×material inversion is the design's strongest scalability property and
  genuinely earns GREEN: authored content is O(operations × materials) ≈ 500 cells, *not* O(objects),
  so 10–100× more objects costs ~nothing to author. Instanced runs (proposal §6) keep per-instance
  population (and idmapper RAM — every touched object stays resident, research §5/§8) small. Two
  residual density risks the static "300–800" figure hides: (1) **per-`look` render cost** — one scene
  room holding hundreds of objects means each `look` scores every visible object per band per looker,
  O(objects) per look per player; single-scene sidesteps the cross-DB attribute tax (research §5) but
  not in-memory iteration, and no look-render cache is specified. (2) **Runtime object-count
  explosion** — matter separation (§23: seat cover → 5 strips → …) *creates* first-class objects;
  conservation (§24) bounds mass but **not object count**, so a fuzz run that cuts everything into
  strips can multiply the live object set well past 800. Bound it or coalesce strips.

### AR6 Softlock / Failure-Mode Analysis
- **Verdict:** YELLOW (at risk)
- **Evidence:** §44 guarantees are per-fact ("critical goals ≥ 3 solution paths", "critical hidden
  facts ≥ 3 clue paths"). Proposal §5 explicitly names the gap and adds (a) global-state reachability /
  resource-exhaustion analysis, (b) a seeded fuzz harness, and (c) "degradation over hard loss (a
  burned antenna lead leaves a worse-but-usable stub)". Instanced ~1-day runs end in "rescue / escape /
  collapse" (proposal §6). Shared finite resources exist: battery (radio power + drain on each attempt,
  §38.5; "keep the radio powered", §38.7), aviation fuel, firewood/tinder, the one sharp tool, the
  beacon. §7 already accepts "a good beacon but no shelter may still fail if everyone freezes."
- **Severity:** high
- **What would change the verdict:** a global resource-reachability invariant (from any reachable
  state, at least one rescue route's gating resources remains attainable) verified by the fuzz harness,
  plus a clock floor / deadman that guarantees a run terminates even with zero player action.
- **Note:** This answers the user's sharp question — **yes, a global softlock can occur despite the
  per-fact ≥3-paths rule**, by two routes. (1) **Shared-resource exhaustion underpins all rescue
  routes:** the ≥3 routes are counted independently, but they share gating resources — every route
  needs the party *alive*, which needs warmth, which needs firewood/fuel; the radio route needs
  battery; the travel route needs stamina/warmth. Burn the firewood for heat and you simultaneously
  starve the signal-fire and the survive-to-rescue routes. A single shared resource sitting under all
  routes is a global exhaustion vector the per-route count cannot see. (2) **The event-driven clock can
  *hang* a doomed-but-alive party** — this is a softlock the proposal's own §7 clock *introduces*: if
  the party is alive but every rescue route's resource is spent and they stop acting, the
  advance-on-action clock never ticks, so they neither die nor get rescued — a true no-path-forward
  hang. The §9 heartbeat would at least drain them to a (valid) death ending. Strong credits: framing
  loss as a legitimate *run ending* (collapse) means most "stuck" states resolve rather than hang, and
  degradation-over-loss shrinks irreversibility — but degradation is a design discipline, not an
  enforced invariant (nothing checks every irreversible transform leaves a usable residue).

### AR7 Observability / Debuggability
- **Verdict:** GREEN (holds)
- **Evidence:** Resolution returns a `Resolution` enum naming which §26 tier fired (authored → object →
  part → material → generic → informative; `overview.md` step 4). Proposal §3.4 adds a **wall-sensor**
  logging every attempt that reaches generic-redirect (boundary detector + authoring queue), and §8 a
  deterministic event log summarized into the run story — a full decision trace.
- **What would change the verdict:** nothing to hold GREEN; add the two traces below before
  multiplayer.
- **Note:** Tier and boundary tracing are well covered (triage MED). The two gaps for live
  (multiplayer) debugging: **per-observer perception decisions** (why did observer X not receive event
  Y? — needs the band/visibility computation logged) and **soft-judge verdicts** (what did the LLM
  return, what did the clamp change it to? — async + clamped values are otherwise irreproducible from
  the log alone).

### AR8 Extensibility
- **Verdict:** GREEN (holds)
- **Evidence:** Proposal §2: "an object is cheap" — `{id, name, materials, parts?, size, mass, tags,
  state}`, no bespoke affordance list; behavior derives from operations over materials. A new material
  is one ~20-property vector (proposal §3.2) that instantly interacts with all operations; a new
  operation is one declarative precondition/effect schema (proposal §3.1). Authored packets (§43.1)
  are demoted to the exception (proposal §12).
- **What would change the verdict:** nothing to hold GREEN — but budget property-schema changes as the
  expensive class.
- **Note:** This is the architecture's other standout property: the common extensions — new object,
  new material, new operation — are each ~1 record / 1 schema, so "more powerful" is config, not a
  rewrite (the Q5 answer). The one non-O(1) seam: an operation that needs a *new property axis* (e.g.
  `magnetize` → a `ferromagnetic` property) forces an edit across all ~25 materials, so the **property
  schema** is the real extensibility bottleneck — adding an axis is O(materials), not O(1). Two minor
  taxes: authored specials (radio/beacon/pilot) stay multi-file (acceptable, they're few — but each is
  a GD23 consistency leak), and every queryable axis must be mirrored as a Tag *and* an Attribute
  (research §5, "Attributes are unqueryable by value → use Tags").

### AR9 LLM Latency & Cost Budget
- **Verdict:** YELLOW (at risk)
- **Evidence:** LLM at four edges (proposal §4): Author (offline, strong model), Parse (Stage-A intent,
  frequent, local OSS-20B torch), Narrate (prose, local), Soft-judge (bounded verdict). Research §6
  confirms the *async* seam is solved and copyable: `contrib.rpg.llm` uses `twisted.web.client.Agent` +
  `@inlineCallbacks`, non-blocking the reactor — "a slow response will not block Evennia." Proposal §4
  adds a deterministic timeout fallback so a slow model never stalls a turn.
- **Severity:** med
- **What would change the verdict:** a written envelope — max LLM calls/turn, token caps per edge, a
  per-instance GPU-concurrency ceiling, and a narration cache or opt-in — validated by a load test at
  realistic party size.
- **Note:** The *concurrency* risk is genuinely closed: the non-blocking pattern (research §6) means
  one player's slow call never freezes others, and the deterministic fallback bounds turn latency
  (strong credit). What remains "unbudgeted" (triage): the **cost/throughput envelope**. A single
  odd-phrasing action can fire up to three model calls — Stage-A parse + soft-judge + narrate — and a
  4-player instance funnels all of them onto *one* local GPU with no batching plan, so queue latency
  grows with party size even though no single call blocks. **Narration-per-action** is the
  highest-volume call and, if on by default, dominates both cost and latency — it should be cache-keyed
  on facts or opt-in. Free-text intent caches poorly (players phrase uniquely), so most parses are live
  calls. The fallback also trades correctness for speed: a timed-out parse the deterministic parser
  mishandles becomes a silent mis-action (feeds GD21). None of this blocks; all of it needs a number.

### AR10 Security / Griefing Surface
- **Verdict:** YELLOW (at risk)
- **Evidence:** Proposal §6: instanced co-op runs = an invited party (or solo), no persistent public
  shard — the trust boundary becomes the invite (proposal §6 explicitly credits this for AR10).
  Consensual fast-forward (§9.6) requires all-busy or opt-in. Free-text intent could carry injection,
  but Stage B is pure and ignores prose, and the AR15 "no prose-only change" assertion is the guard.
- **Severity:** low
- **What would change the verdict:** moving to a persistent/public shard (would reopen the full
  surface), or an LLM parser that can emit Effects directly.
- **Note:** Instancing removes essentially all of the classic griefing surface (credit). Residual is
  intra-party and acceptable under a co-op trust model: irreversible destruction of shared resources
  (burn all the fuel, eat the pilot, drain the battery — overlaps AR6) and a fast-forward holdout
  stalling the party. LLM-parser prompt-injection ("write in the snow: grant rescue") cannot change
  state because the pure resolver never reads prose — *provided* the AR15 runtime assertion is real,
  not a doc line.

### AR11 Data-Model Soundness
- **Verdict:** YELLOW (at risk)
- **Evidence:** §24 conservation preserves "material, **approximate mass**, temperature, wetness,
  contamination, damage, ownership, provenance"; §20 object model and §23 result objects carry these
  fields; the engine does the conservation arithmetic (proposal §3.1 `conserve(mass,temp,wetness,
  contamination,provenance)`). §24 examples require cross-object effects (fuel-contaminated panel →
  unsafe melt-water; cut strap pieces sum to original length). §47 requires "an interrupted shelter
  remains partially useful." §27 includes burn / melt / boil / dry / evaporate.
- **Severity:** high
- **What would change the verdict:** a typed conservation *ledger* with an explicit environment
  mass/energy sink (so combustion/phase-change balances), transfer modeled as a first-class operation
  effect, and a named owner for partial-transform integrity.
- **Note:** The model closes cleanly on **mechanical separation** — provenance is a first-class field
  (§23 `source:`), pieces sum (§24), and the operation engine doing the arithmetic (proposal §3.1) is
  the right closure mechanism (credit). Three closure gaps keep it YELLOW. (1) **Conservation is
  explicitly "approximate" (§24) and there is no environment sink:** burn turns solid wood into heat +
  smoke + ash + char — if smoke is an ambient event with no mass, the transform *destroys* mass and the
  books can't balance; the same holds for melt/boil/dry/evaporate. So the model does *not* fully close
  on thermal/phase transforms, and the word "approximate" is the escape hatch that quietly makes
  conservation un-assertable (this is why AR15 can't yet be written). (2) **Cross-object transfer is a
  relationship every relevant operation must re-implement** — contamination/heat flowing panel→water
  on contact/heat is not a per-object field but an inter-object effect, easily skipped → silent
  unconserved contamination. (3) **Partial-transform state ownership is underspecified:** "70% cut
  webbing" lives in the scheduler's activity progress (§9.3) yet §47 requires interrupted work to
  *persist usefully* on the object — the object schema (§20) has `damage` but no partial-transform
  integrity field, so where partial state crystallizes is undefined. Minor: attachments (§22) are
  binary attached/detached, with no representation of a partially-detached part.

### AR12 Testability (invariants vs enumeration)
- **Verdict:** GREEN (holds)
- **Evidence:** Proposal §5 replaces the §46 "700+ explicit tests" with property tests (conservation
  always holds; rescue confidence monotonic; every operation resolves) + a seeded fuzz sample + a small
  golden set; coverage is redefined as "the operation × material-property matrix is complete and
  property-tested" (the only checkable definition of done, IM6).
- **What would change the verdict:** discovering that a headline invariant can't be expressed (see
  AR11) and so degrades back to enumerated cases.
- **Note:** The method is exactly right for an open behavior space — invariants + fuzz oracle beat 700
  hand cases (triage MED). The dependency to flag: the flagship invariant "conservation always holds"
  is only assertable once AR11's ledger closes with a tolerance + environment sink; until then it's a
  property test that can't be written truthfully.

### AR13 Premature Abstraction (smell)
- **Verdict:** YELLOW (at risk)
- **Evidence:** The original design specifies a full apparatus — ~20 operations, ~50-field object
  packets (§43.1), an 18-rule validator (§44), the entire §20–27 ontology, "700+ explicit tests"
  (§46) — before a single object resolves; `CLAUDE.md` confirms `world/sim` is "Not built yet" and
  `game/tests/sim` is "Empty until the engine exists." The proposal counters with a **vertical slice
  first** (proposal §10 step 1: single-player, one room, ~4 objects — seat, knife, fire-makings, radio
  — + the operation×material core + Stage-A parse + crystallize loop + wall-sensor; "the make-or-break
  experiment") and cuts heavy packets-as-default + the 700 tests (proposal §12).
- **Severity:** med
- **What would change the verdict:** shipping the §10 slice and confirming the operation×material
  factoring + the crystallize loop on concrete content before building breadth.
- **Note:** The original is a textbook framework-first artifact — maximal machinery, zero stressed
  content. The proposal's slice-first reordering + demoting packets to the exception is the correct,
  explicit antidote (strong credit): build one thing that resolves, then generalize. The residual smell
  is that the proposal *introduces its own* unstressed abstractions: the **resolve-then-crystallize
  loop** (proposal §3.6, "play becomes authoring, the ontology fleshes itself") and **soft-judge-on-
  rails** are elegant but speculative — no concrete run has shown the crystallize queue *converges*
  (the LLM may propose rules that mostly fail `make validate`, so the wall-sensor backlog grows faster
  than crystallization drains it). It is to the proposal's credit that §10 step 1 routes exactly these
  into the make-or-break slice, so they will be stressed first — ship that before betting the ontology
  on them.

### AR14 God Object (smell)
- **Verdict:** GREEN (holds)
- **Evidence:** Functional core split into per-system modules (`systems/{fire,water,warmth,rescue}`,
  `space/*`, `actions/*`; `overview.md`); operations are declarative *data* schemas (proposal §3.1) so
  the resolver is a generic interpreter, not a growing switch.
- **What would change the verdict:** the Effect applier or perception propagator drifting toward a
  thousand-line "knows everything" module during build.
- **Note:** Declarative operations keep Stage B thin (triage MED — a build-time watch, not a
  design-time decision). The two natural accretion sinks to watch: the typeclass **Effect applier**
  ("the only place that interprets Effects", `overview.md` §7) grows with every effect kind, and the
  **perception propagator** concentrates visibility + audibility + reachability + direction + detail +
  weather (§11 rule) — keep both factored.

### AR15 Leaky Abstraction / Missing Invariants (smell)
- **Verdict:** RED (broken / unaddressed)
- **Evidence:** The load-bearing laws are stated as prose or as *authoring-time* checks, not *runtime*
  assertions: "Conservation holds" (§24, `CLAUDE.md` hard rule) and "no prose-only state changes",
  "≥ 3 solution/clue paths", "conservation rules are followed", "LLM-generated rules cannot override
  core physics" all live in the §44 **content validator**, which lints authored content at load/CI —
  it does **not** guard a live transform. The proposal *does* convert two laws to runtime assertions:
  "no prose referencing state with no backing Effect" (proposal §4 Narrate guardrail, explicitly tagged
  AR15) and the soft-judge clamp.
- **Severity:** high
- **What would change the verdict:** implement a **per-transform conservation ledger assertion** that
  rejects any Effect-set that doesn't balance the conserved quantities against the pre-state, wired as
  both a runtime guard and a property test.
- **Note:** This is the most actionable architecture finding. The proposal earns real credit for naming
  AR15 and making the *narration* law a runtime assertion (state → prose can no longer invent state)
  and for clamping soft-judge verdicts. But the **single most important law — conservation — remains
  unenforced at runtime**: §44 lints authored packets, nothing checks that an *applied* Effect-set
  conserves mass/material/contamination/provenance against the pre-transform state. Worse, per AR11 it
  is currently *un-writable*, because §24's "approximate mass" plus the missing environment sink mean
  the books don't close on burn/melt/evaporate — so "everything is physical, no prose-only change" is,
  for thermal transforms, an aspiration the engine cannot presently verify. A doc line that says
  "conservation holds" with no runtime check is exactly the leaky-abstraction smell this lens exists to
  catch. (See Top findings for the exact assertion.)

### AR16 Over-Configuration (smell)
- **Verdict:** YELLOW (at risk)
- **Evidence:** The original design is configuration-heavy: §43.1 object packet ~50 fields, §21
  material template ~22 fields, §27 action_family ~18 fields, §43.3 workflow ~17 fields — with silent
  defaults the obvious failure mode (an unfilled `burnability` → a seat that should burn doesn't,
  invisibly). The proposal inverts this (proposal §2): cheap objects, behavior derived from ~25
  shared material vectors; "the operation × material-property matrix is complete and property-tested"
  is the coverage definition (proposal §5).
- **Severity:** med
- **What would change the verdict:** hard "no silent default" validation that fails load on any
  unfilled material×property cell, plus a real type-checker for the operation precondition/effect DSL.
- **Note:** The cheap-object inversion collapses the worst over-configuration — hundreds of 50-field
  packets become cheap records + ~25 shared material vectors, dropping the surface from O(objects × 50)
  to O(materials × 20) + thin records (strong credit), and proposal §5's matrix-completeness check is
  the right guard *if enforced*. Two residuals. (1) The ~25 × ~20 **material matrix becomes the new
  high-leverage silent-default surface**: one unfilled ordinal cell misbehaves across *every* object of
  that material, so completeness must be a hard load gate, not a documented aim — "ordinals are fast to
  fill" (proposal §3.2) helps authors but does not enforce that they did. (2) The **declarative
  operation schemas are logic-as-data** — preconditions like `tool.edge >= material.cut_resistance -
  slack` (proposal §3.1) are a precondition/effect mini-language embedded in YAML; without its own
  type-checker/validator that is precisely the "logic that should be code, hidden as weakly-validated
  data" smell, just relocated from packets to operations.

### AR17 Untested Critical Path & Error-Handling Gaps (smell)
- **Verdict:** YELLOW (at risk)
- **Evidence:** Proposal §4 gives a deterministic timeout fallback (LLM-timeout path) and §5 a seeded
  fuzz harness for "validator passes yet goal unreachable" (IM10). Not addressed: the concurrent-writer
  path (AR3's stale snapshot) and a soft-judge call timing out *mid* multi-tick timed action.
- **Severity:** med
- **What would change the verdict:** tests for two players acting on one object across a tick boundary,
  and for a soft-judge/parse timeout occurring partway through a scheduled action.
- **Note:** Two catastrophic paths are covered (LLM timeout → deterministic fallback; reachable-state
  exhaustion → fuzz oracle) — credit. The untested ones are the **concurrent-writer reconciliation**
  (AR3) and **timeout-mid-timed-action** (what partial state persists if the soft-judge that gates a
  long action never returns?). Both are the "rare but catastrophic" cases this lens targets.

---

## Top findings

The three most important RED/YELLOW cards, then the one invariant that must become a runtime assertion.

1. **AR15 — Conservation is a doc line, not a runtime law (RED, high).** The flagship contracts
   ("conservation holds", "no prose-only state change") live in the §44 *authoring-time* validator and
   in prose; nothing guards a *live* transform. The proposal commendably makes the narration law a
   runtime assertion, but the central law — conservation — stays unenforced. This is existential for
   the "everything is physical" thesis: if it isn't asserted at commit, prose-implied or LLM-implied
   state changes can slip through undetected.

2. **AR11 — The data model does not fully close (YELLOW, high).** §24 conservation is explicitly
   "*approximate*" and the schema has **no environment mass/energy sink**, so burn / melt / boil / dry
   (§27) cannot balance; cross-object contamination/heat transfer and partial-transform ownership are
   underspecified. AR15 and AR11 are joined: you cannot *assert* conservation (AR15) until the model
   can *express* a closed ledger (AR11). Fix AR11 first.

3. **AR6 — A global softlock can occur despite the per-fact ≥3-paths rule (YELLOW, high).** Yes, via
   two routes: (a) a **single shared resource** (firewood/warmth, then battery, then stamina) sits
   under *all* rescue routes, so the routes are not resource-independent and exhausting the shared
   resource locks every path at once; and (b) the proposal's own **event-driven clock can hang a
   doomed-but-alive party** — no action → no time → neither death nor rescue — a true no-path-forward
   state the §9 heartbeat could not produce. The instanced "always ends in collapse/rescue" model and
   degradation-over-loss are strong mitigations, but neither is yet an enforced invariant.

   *Runners-up:* **AR3** (stale snapshot + cached-verdict divergence at the timed-action seam) and
   **AR4** (concurrent-action ordering / replay-mode-cache-only / recorded-fallback unspecified) are
   both YELLOW-high and would be cards 4–5; **AR9** (no per-turn LLM call/token/GPU budget) is the
   leading MED.

### The one invariant that MUST become a runtime assertion (AR15)

> **Per-transform conservation ledger.** On every Effect-set, before commit, assert that the
> post-transform world balances the pre-transform world on each conserved quantity —
> **material identity, mass (within a declared tolerance against an explicit *environment* sink),
> contamination and heat (transfers accounted, not vanished), provenance carried, and separated
> lengths/counts summing to the source** — or **reject the transform**. Concretely:
> `assert conserves(pre_state, effects, environment_sink)` in the Effect applier, mirrored as a
> property test (`conservation_holds` over fuzzed operation × material × object) and a new `make
> validate` *runtime* rule. This is the assertion that turns "no prose-only state change" and
> "everything is physical" from documentation into law, and its prerequisite is AR11 giving the ledger
> an environment sink so combustion and phase-change can actually balance.

---

## Summary

1. The intended architecture (design + proposal) is strong on its two headline bets: the functional
   core / imperative shell (AR1) and the operation×material engine that makes density (AR5) and
   extensibility (AR8) cheap — config, not rewrites — credited as GREEN.
2. The proposal lands real fixes the lenses credit: pure Stage B + event-driven clock (AR4), cheap
   objects collapsing over-configuration (AR16), invariants+fuzz over 700 enumerated tests (AR12), the
   wall-sensor trace (AR7), and slice-first build order against framework-first premature abstraction
   (AR13).
3. The decisive weakness is a chain: the data model doesn't fully close (AR11 — "approximate" mass, no
   environment sink), so conservation can't be expressed, so it stays a doc line not a runtime
   assertion (AR15, RED).
4. A **global** softlock is reachable (AR6) — shared-resource exhaustion under all rescue routes, plus
   the event-driven clock hanging a doomed-but-alive party — so the per-fact ≥3-paths rule is
   necessary but not sufficient; a global resource-reachability invariant + a clock deadman are needed.
5. Determinism and single-source-of-truth (AR4, AR3) are achievable with the named tools but not yet
   enforced: concurrent-action ordering, replay-cache-only mode, and stale snapshots at the timed-
   action seam are the open holes; the async LLM seam itself is solved (research §6) but unbudgeted
   (AR9).
6. Required next step: implement the per-transform conservation ledger (AR15) on top of a closed AR11
   model, and add the global-reachability + clock-termination invariants (AR6) to the fuzz harness —
   these convert the design's strongest *promises* into enforced *laws*.
