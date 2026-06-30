# Implementation / feasibility lenses — Whiteout

**Artifact under review:** the *intended* design of Whiteout = the original design
(`docs/scenarios/whiteout/design.md`, cited §N) **as amended by**
`docs/proposals/whiteout-engine-proposal.md`. Judgement is "as now intended": fixes in the
proposal are credited, residual risks flagged.
**Goal:** answer two questions — (a) *will the LLM actually generate enough correct, consistent
content, and how do you ever know coverage is enough?* and (b) *is the §46 density realistically
authorable, or must we cut to a vertical slice?*
**Primary evidence base:** `docs/investigation/research/evennia-interactive-worlds.md` (verdicts,
`contrib.rpg.llm`, ~low-hundreds concurrency ceiling, per-tick DB-write traps) and
`docs/investigation/research/prior-art.md` (LLM-at-three-edges, generate-then-validate,
ScienceWorld 25→200k, AI-Dungeon failure, action-chunking). Leverage per
`docs/investigation/lenses/triage.md`.
**Repo state (load-bearing):** `game/world/sim/` is a README only — the engine, the validators
(`docs/guides/validation-rules.md`), and the `make validate`/`verify` gates are **scaffolded but
unproven against generated content**. So every "the validator catches it" claim below is a
design promise, not an observed fact.

---

### IM1 Framework Feasibility (Evennia) — HIGH
- **Verdict:** GREEN (with one named YELLOW seam)
- **Evidence:** `evennia-interactive-worlds.md` §0/feasibility table — "5 of 7 Whiteout subsystems
  are idiomatic or near-idiomatic"; proposal §9 reuse list; design §10–15 (perception), §9 (clock),
  §40 (NL+MUD input).
- **Severity:** low–med (managed, not blocking)
- **What would change the verdict:** a primary free-text loop that fights `cmdparser` and produces
  frequent mis-routes (sentence starting with `s`/`l` consumed as `south`/`look` before
  `CMD_NOMATCH` fires); or reverting to a persistent shard that re-exposes the scale ceiling.
- **Note:** The research is unusually favourable: perception render (`get_display_*(looker)`,
  GREEN), tick/clock (Global Script + `TickerHandler`, GREEN), per-observer routing (`msg_contents`
  / `send_emote` propagator, GREEN), ontology-in-Attributes (YELLOW, resolvable via Tags), and the
  LLM async seam (GREEN — `contrib.rpg.llm` is a *copyable core reference*: `Agent` +
  `@inlineCallbacks`). Reuse covers a large fraction of the systemic surface off the shelf
  (rpsystem, extended_room, traits, crafting, clothing, prototypes). The single genuine
  "against-the-grain" point is a **primary NL parser**: Evennia's prefix-matcher pre-empts free
  text, so Whiteout needs one dominant NL `Command` with a rich `parse()` or a `COMMAND_PARSER`
  override (one heavy override, well-understood). The proposal's Stage-A "deterministic parser
  first, LLM fallback" maps onto this cleanly and reduces the fight. Override count is low and each
  has a blessed extension point; the proposal's single-scene + instanced choice *removes* the worst
  attribute-query/reachability tax (reachability over in-memory `room.contents`). Net: Evennia is a
  good fit; the parser is the one place to budget engineering, not a structural risk.

### IM2 Reactor / Concurrency Model — MED
- **Verdict:** YELLOW (managed)
- **Evidence:** `evennia-interactive-worlds.md` §6 (single-threaded Twisted reactor must never
  block), §8 ("the real per-tick trap: a fast ticker writing Attributes across many objects");
  design §9.3 (10–20s real = 1 game-minute heartbeat updating ~13 subsystems/tick); proposal §7
  (event-driven clock).
- **Severity:** low–med
- **What would change the verdict:** keeping the §9.3 wall-clock heartbeat that writes survival
  meters to Postgres Attributes every tick across all objects — that is the documented worst case.
- **Note:** The async-LLM half is solved by a core reference (non-blocking `Agent`/`Deferred`), so a
  slow model never freezes other players. The remaining concurrency risk is the per-tick DB-write
  amplification, not CPU: an instanced ~4–6-player party over one scene on a 10–20s tick is trivial
  load (cf. the worst-case reference of 50 bots @ `look`/2s = ~45% CPU). The proposal's two fixes
  retire most of it — the **event-driven clock advances only on action** (no idle drain, no ticking
  empty instances) and **traits `.rate`** makes hunger/thirst/warmth lazy-computed-on-read (zero
  per-tick write). Residual: two players acting on one shared object within a tick (the AR17
  untested path) and the activity scheduler's partial-progress writes — both small at instanced
  scale but need an explicit ordering/locking rule.

### IM3 LLM Ontology-Authoring Throughput — HIGH  ·  *answers Q(a)*
- **Verdict:** YELLOW
- **Evidence:** `prior-art.md` §4H (GPT-4 ~**59.9%** whole-state transition accuracy, **49.7%** on
  environment-driven dynamics, error compounds), §4E/§5D (LIGHT/COMET: models *propose* structured
  content humans curate; ConceptNet **~15.5%** assertions false/vague, over half single-assertion),
  §4H/§5E (Guan et al.: LLM writes the symbolic model, validator+human correct once, planner runs
  it). Design §43 (heavy packet), §41 (good/bad LLM uses). Proposal §2/§3.2/§3.6/§4 (cheap objects,
  ordinal properties, generate-then-validate, resolve-then-crystallize).
- **Severity:** high (decisive for Q4)
- **What would change the verdict:** a measured pilot — generate the ~25-material property table +
  ~20 operation schemas, run them through `make validate`, and report two numbers: (1) the
  schema/conservation **reject rate** and (2) the human-judged **wrong-but-valid value rate** on a
  sample. A target like "<10% post-validate human correction on the material table" flips this to
  GREEN; no measurement yet means it stays YELLOW.
- **Note:** The architecture is right — the LLM is a **proposer into a constrained schema, gated by
  the same `make validate` content authored by hand passes** (the Guan/LIGHT/COMET winning pattern),
  and it reasons *qualitatively* (ordinal property direction, which LLMs do well) while the engine
  owns the numbers and conservation (the QPT split). The proposal's **inversion is the real
  throughput fix**: it collapses the consistency surface from ~800 derived objects × ~18 authored
  affordances (≈ thousands of independently-hallucinable cells, each a chance to contradict) to
  **~25 material property-vectors (~15 ordinal fields ≈ 375 cells) + ~20 operation schemas + ~5
  authored specials**. Drift/contradiction across thousands of bespoke packets is the original
  design's fatal IM3 exposure; the inversion makes it ~20× smaller and far more verifiable. **But two
  residual holes remain that no amount of architecture closes.** First, the validator catches
  *schema* and *conservation* violations — it cannot catch **plausible-but-wrong ordinal values**
  (the LLM asserting foam = high insulation, or steel cut-resistance below a pocketknife's edge):
  these pass every gate and only surface in playtest. Given ConceptNet's ~15.5% noise as a prior,
  expect a non-trivial fraction of proposed values to be wrong-yet-valid, requiring a human-curated
  **golden material table** as ground truth. Second, the **resolve-then-crystallize loop** is
  runtime generate-then-validate — strong for *do-anything*, but the validator can only check
  invariants, not "is this the *right/interesting* outcome," so crystallized rules can be
  valid-but-dumb and accumulate (ties to IM12). Bottom line on Q(a): *will it generate enough
  correct content?* — yes for **resolution** and **conservation**, **not provably** for
  **correctness/quality**, which must be human-sampled.

### IM4 Runtime LLM Latency/Cost Realism — MED
- **Verdict:** GREEN (with one deferral rule to enforce)
- **Evidence:** `evennia-interactive-worlds.md` §6 (non-blocking `Agent`+`Deferred`, `utils.delay`
  for a "thinking…" filler); proposal §3.3/§4 (deterministic parser first, cached parses,
  deterministic timeout fallback), §9 (local torch OSS-20B for cheap/frequent calls, stronger model
  for authoring); `prior-art.md` §4F (per-agent LLM cost/latency sinks multiplayer — budget hard).
- **Severity:** low–med
- **What would change the verdict:** a synchronous crystallize/author cycle on the interactive path
  — a runtime miss that blocks the player's turn for a multi-second author→validate round-trip.
- **Note:** The interactive LLM is off the hot path by design: deterministic parser handles the
  common case, LLM only on odd phrasing, parses cached, with a hard timeout → deterministic fallback
  so a slow model never stalls the turn. Local 20B on the host GPU makes intent-classify cheap
  (short output, ~sub-2s plausible) and marginal cost ~zero; the cloud authoring model is the only
  real $ and it's offline. Set p95 ≤ ~2s on the interactive path, fallback at ~3–4s with a filler
  message. **The one thing to make a hard rule:** the resolve-then-crystallize loop must **resolve
  now via generic-physics and crystallize the rule asynchronously/deferred** — never block the
  player on author+validate. Narration enrichment (a paragraph) is the latency wildcard (~2–5s);
  gate it behind the same timeout or render the deterministic fact-line first and enrich after.

### IM5 Authoring Throughput (human + AI) — HIGH  ·  *answers Q(b)*
- **Verdict:** YELLOW for the intended (inverted) scope; RED for §46-as-written
- **Evidence:** design §46 density targets — **60–100 primary objects, 300–800 derived,
  40–70 action families, 12–18 workflows, ≥50 brainstormed attempts/major object, ≥700 tests,
  15–25 zones**; §43 packet = ~60 lines, dozens of fields (perception ×8, affordances ×18,
  transformations, survival_uses ×9, non_survival_uses ×6, tests ×5). Proposal §2/§5/§10/§12 (cheap
  objects, invariants-not-700-tests, vertical slice, explicit cuts). `prior-art.md` §1A/§4B
  (BotW 3 rules; ScienceWorld 25 actions → ~200k pairs — few verbs × many objects is how density
  scales), §1B (imsim richness is "expensive to build against modest sales").
- **Severity:** high (forces the vertical-slice decision)
- **What would change the verdict:** an explicit re-scoping of §46 (so its numbers are not treated
  as build targets) + a per-item cost measurement on the inverted path (time to author one material
  vector and one operation schema, end-to-end through validate).
- **Note:** Do the multiplication on §43-as-written: even at an optimistic ~1–1.5h human+AI per heavy
  packet, **80 primary objects ≈ 100–120h** *before* 40–70 action-family packets, 12–18 workflows,
  ~1500 attempt-classifications (≥50 × ~30 major objects), and **700+ enumerated tests** — several
  person-months, the textbook IM5 wall. That is RED. **The proposal's inversion is the only
  affordable path** and it is the correct one (the BotW/ScienceWorld lesson literally quantified):
  author **~25 materials + ~20 operations + ~5 authored specials (radio/beacon/pilot/seat) + one
  dense scene**, let the other 95% of objects be *cheap* (~6 fields + state) riding the
  operation×material matrix, and replace 700 enumerated tests with invariants + fuzz + a golden set.
  That is weeks, not months — **authorable**. Hence YELLOW not GREEN: the inversion rests on an
  **unproven bet** that cheap objects deriving behavior from 25 materials × 20 operations produce
  *good enough* behavior without per-object tuning. If they don't, per-object tuning re-inflates cost
  toward the §43 packet and the schedule reverts to RED. The decision this lens forces: **commit the
  vertical slice and explicitly retire the §46 numbers**, or they will be mistaken for the plan.

### IM6 Coverage Verification — HIGH  ·  *answers Q(a) "how do you know"*
- **Verdict:** GREEN (the reframe is correct and checkable) with a YELLOW honesty caveat
- **Evidence:** proposal §5 (coverage = operation × material-property matrix complete and
  property-tested + a fuzz sample of object×object attempts all *resolve*; wall-sensor logs every
  generic-redirect as the boundary detector + authoring queue). `prior-art.md` §4C
  (ScienceWorld: 25 actions × ~200 object types → ~200k legal pairs — the bounded basis that
  *generates* the space), §5C/§5E (SHRDLU/PDDL: interpretability comes from a *closed, total* verb
  set over a fixed property schema). Design §44 (validator rules), §46 ("density exists so
  experimentation feels real" — but no completion definition).
- **Severity:** med (it is the answer to "how do you ever know," and the answer is good)
- **What would change the verdict:** a written, numeric pass-threshold for the fuzz oracle and an
  explicit statement that coverage = resolution+conservation+solvability, **not** correctness.
- **Note:** This lens is where the original design has no answer at all — "everything interacts" is
  unbounded and unverifiable — and the proposal supplies the one defensible reframe: **a bounded
  basis**. Make it concrete: **~20 operations × ~25 materials ≈ 500 cells**, each with a declared
  outcome class (works / partial / informative-fail) and a property test; that is finite and
  auditable. Object×object combinatorics (~60–100 objects → thousands of ordered pairs) are **not**
  authored — they are *derived* from the 500-cell matrix and **fuzz-sampled** (e.g. ≥10k seeded
  `(actor, operation, target, tool)` attempts over the scene) with an oracle: **0 unresolved (no
  `You can't do that.`), 0 conservation violations, rescue reachable from every reachable state, and
  the wall-sensor generic-redirect rate below a chosen X%**. The honest caveat (the YELLOW): this
  proves **resolution**, not **quality** — "all 500 cells resolve" is verifiable; "all 500 cells
  resolve *interestingly and correctly*" is not, and must be sampled by a golden set + playtest.
  Coverage must therefore be *defined* as resolution+conservation+solvability and never *claimed* as
  semantic completeness.

### IM7 Test Strategy — MED
- **Verdict:** GREEN (intended) — reframe the §45/§46 lists, don't delete them
- **Evidence:** design §46 ("explicit_tests: 700_plus"), §45 (enumerated example tests); proposal §5
  ("invariants over enumeration" — conservation always holds, rescue confidence monotonic, every
  operation resolves; + fuzz + small golden set). `prior-art.md` §4A (TextWorld: chain rules
  backward from a goal to *prove* a winnable quest — solvability as property, not hand-case).
- **Severity:** low–med
- **What would change the verdict:** treating 700 enumerated tests as the coverage strategy rather
  than as a curated regression anchor.
- **Note:** 700 enumerated tests is a smell — they can't cover an open space and they rot. The
  intended strategy is correct: **property/invariant tests + fuzz oracle (IM10) + a small golden
  set**. The right move is not to discard §45/§46 but to **demote the enumerated lists to the golden
  set** (curated regression anchors for the puzzle-critical specials and known-tricky materials),
  with the property+fuzz layer doing the coverage work. Follows directly from IM6/AR11/AR4.

### IM8 Performance — MED
- **Verdict:** GREEN at the intended scale
- **Evidence:** `evennia-interactive-worlds.md` §8 (single-process ceiling ~50–75 laptop / 150–250
  desktop; 50 bots `look`/2s = ~45% CPU, 100 = ~100%; idmapper keeps touched objects RAM-resident;
  "caching is king"); proposal §6 (instanced, single scene), §7 (event-driven clock). Design §10
  (perception O(objects × observers) per event).
- **Severity:** low
- **What would change the verdict:** a persistent shard with many concurrent objects/players, or
  reverting to a polling heartbeat writing meters to DB each tick.
- **Note:** Single dense scene + instanced small party + event-driven clock + lazy traits keeps every
  hot path far under the documented worst case. Perception runs per co-located observer per event —
  small N in one room. The only real performance disciplines are the ones the research already names
  and the proposal already adopts: **Tags for any value-query axis** (Attributes are unqueryable by
  value), **`.ndb`/lazy traits for hot state** (no per-tick write), **never block the reactor**.
  Memory (idmapper residency) is the quiet cost — relevant only if instances are never GC'd (see
  IM9).

### IM9 Persistence / Session Model — HIGH
- **Verdict:** YELLOW
- **Evidence:** design §3.2 (multiplayer-first, "never assume a single player owns the clock"), §9.6
  (clock modes), §9.1 (long tasks keep partial progress) — but the **instanced-vs-persistent fork is
  unspecified**. Proposal §6/§11 (instanced co-op runs, ~1 in-game day, advance-on-action clock +
  consensual fast-forward). `evennia-interactive-worlds.md` §8 (state persists in Postgres
  Attributes; `.ndb` is volatile across reload), §2 (`persistent=True` Script/Ticker survives
  shutdown). `prior-art.md` §2B (survival pacing as social, not a meter — favours session arc).
- **Severity:** med–high
- **What would change the verdict:** a written spec for (1) **activity-progress persistence** (the
  90-min shelter task surviving a server `@reload`, DB-backed not `.ndb`) with a test, and (2)
  **instance lifecycle** — creation, reconnect window, max duration, and GC so a single lingering
  player doesn't pin an instance resident forever.
- **Note:** The proposal resolves the existential fork correctly: **instanced co-op runs** sidestep
  the hardest persistence questions the design left open — "who owns time when the last awake player
  drops" simply doesn't arise, because the **event-driven clock advances only on action**, so an
  empty instance pauses rather than draining the party to death; griefing is bounded to the invited
  party (AR10); per-instance population stays small (helps the Evennia ceiling). This is a real fix.
  The residual YELLOW is the seam between two design rules: §9.1 says timed tasks **keep partial
  progress**, but the perf advice (and §8) pushes hot state to **`.ndb`, which is wiped on reload**.
  The activity scheduler is **custom code** and must serialize partial progress to the DB (or a
  reload mid-shelter-build silently loses it) — a direct tension that needs an explicit decision.
  Plus instance lifecycle (reconnect, end-condition, RAM GC) is entirely unspecified. None of this is
  hard, but it is unwritten, and persistence bugs are the classic silent data-loss class.

### IM10 Determinism / Fuzz Harness — HIGH  ·  *the oracle for Q3 (no dead-ends)*
- **Verdict:** GREEN (correctly specified and front-loaded) with a YELLOW determinism precondition
- **Evidence:** proposal §5 (seeded fuzz harness drives the ScriptedBrain over runs, flags dead-ends
  + unresolved attempts against an oracle; + global-state reachability/resource-exhaustion analysis
  on top of the per-fact ≥3-paths rule; degradation over hard loss so irreversibility rarely walls),
  §4 (determinism via seeded RNG, **cached** intent parses + soft verdicts keyed by situation,
  deterministic fallback), §10 step 2 (fuzz harness as a coverage instrument, built second). Repo:
  `.claude/skills/solvability-fuzz`, the host `agent/` ScriptedBrain. Design §44 ("critical goals
  have at least three solution paths" — per-*fact*, **not** global). `prior-art.md` §4A/§4C (TextWorld
  goal-chaining; Jericho fixed seeds + admissible-action detector for search/replay).
- **Severity:** med
- **What would change the verdict:** a cache-miss mid-replay (new phrasing) calling the live model
  and breaking reproducibility; or the "global reachability" analysis being merely per-fact
  path-counting (which AR6 already shows is insufficient for emergent global exhaustion).
- **Note:** This is the single most valuable instrument in the whole plan, and the proposal gets it
  right: a **scripted driver + seed + oracle** is "the only thing that empirically finds global
  softlock," and it is correctly front-loaded as build step 2 (you cannot ship the do-anything
  promise without it). Concrete oracle: every attempt resolves (no `You can't do that.`),
  conservation holds each step, rescue confidence monotonic where intended, and **≥1 rescue path
  reachable from every reachable state** — with "degradation over hard loss" keeping the reachable
  state space bounded and walls rare. The YELLOW is that **determinism is contingent**: the harness
  is only an oracle if the LLM seam is fully cached/clamped — so the deterministic regression core
  must run the **ScriptedBrain with canned intents (no live LLM)**, and LLM-phrasing robustness must
  be a *separate* fuzz mode, or replays diverge and regressions hide. Keep the per-fact ≥3-paths rule
  but treat global resource-exhaustion as a distinct analysis, since the two are not the same
  guarantee.

### IM11 Tooling & AI-Assisted-Build Practices — HIGH  ·  *the user's explicit ask*
- **Verdict:** GREEN (the instrumentation is sane and composes) with a YELLOW "unproven + watch for
  bloat" caveat
- **Evidence:** Repo — `make validate` (hard gate at load/CI/`verify`), `make verify`
  (compose+tests+validate), `make test` (pure `world.sim`), `.claude/skills/{lenses,
  ontology-generator, solvability-fuzz}`, the host `agent/` ScriptedBrain, ADR-0003 (functional-core
  boundary), CLAUDE.md hard rules. Proposal §3.4/§3.6/§4 (wall-sensor as boundary detector +
  authoring queue; resolve-then-crystallize = play-becomes-authoring; "LLM proposes, validator
  disposes — nothing enters without passing the same gate"). Design §44 (validator rules), §48 (9
  validator files + 12 test files). `prior-art.md` §4E/§4H/§5D (generate-then-validate is the proven
  shape). **Caveat evidence:** `game/world/sim/` is README-only — the gates are unbuilt.
- **Severity:** low–med
- **What would change the verdict:** the validators staying aspirational (never run against real
  generated content, so they themselves drift), or §48's 9-validator/12-test scaffold being built in
  full before one content pass stresses it (the AR13 "framework before content" smell → bloat).
- **Note:** This is a genuinely well-instrumented AI-assisted build, and the pieces **compose into
  one loop**: the LLM **proposes** schema-constrained content → **`make validate` disposes** (the
  anchor gate, identical for hand- and machine-authored content) → the **fuzz harness** (IM10) finds
  dead-ends/unresolved attempts → the **wall-sensor** logs every generic-redirect as both the GD22
  boundary metric and the prioritized authoring queue → **crystallize** fills the gap under the same
  gate → the **functional-core ADR** structurally keeps the LLM out of state. That is exactly the
  research's winning pattern (Guan/LIGHT/COMET), instrumented end-to-end, plus review skills (lenses,
  sim-test-writer) and `verify` for CI. **SANE-not-bloat check:** mostly yes, but two trims are
  warranted. (1) The gates are **unproven** — none has run against generated content, and a validator
  that never sees real LLM output is itself a drift risk; the first deliverable should be running the
  ontology-generator → validate → fuzz loop on the ~25-material slice to *exercise* the gates. (2)
  §48 lists **nine** validator files (conservation, solvability, coverage, perception, direction,
  soundPropagation, rescueRoute, sillyInteraction) and twelve test files — building all of them
  before the vertical slice has content is premature (AR13). **Load-bearing now:** conservation,
  solvability, coverage, wall-sensor. **Defer until their content exists:** direction / sound /
  rescue-route / silly validators. Each should earn its place by gating content that actually exists.

### IM12 Design-Intent Drift Control — MED
- **Verdict:** YELLOW
- **Evidence:** Anchor — `VISION.md`, CLAUDE.md hard rules (conservation, "LLM never owns state,"
  "author from §43 packets and pass `make validate`"), ADR-0003. Gate — `make validate` at
  load/CI/`verify`. Proposal §3.6/§4 (crystallize: "LLM proposes; validator disposes; nothing enters
  without passing the same gate," + optional human review on promotion), §12 (explicit cuts list).
  `prior-art.md` §4G (AI Dungeon: no ground truth → drift — the failure mode crystallize must not
  reproduce in slow motion).
- **Severity:** low–med
- **What would change the verdict:** a "no auto-promotion" rule (crystallized rules stay
  cached/per-instance until a human reviews) + a periodic content-quality audit (golden-set
  regression + playtest sampling), so *quality/scope* drift is caught, not just invariant violations.
- **Note:** A real anchor (VISION + ADR + hard rules) and a real enforced gate (`make validate`)
  exist, and the crystallize loop is correctly structured so nothing enters the rule set without
  passing the same gate — bounding the AI-Dungeon failure (every fact reconstructable from the
  store). The residual is precise: the gate enforces **invariants** (conservation, schema,
  solvability), **not design intent** (depth-that-teaches, no shallow content, stay-in-slice). So
  over long crystallize loops, content can drift toward **valid-but-shallow** (and the AI can
  over-scope past the vertical slice) without tripping any gate — the same quality gap IM3/IM6 name.
  Human curation on crystallize-promotion + a quality audit are the only catches, and they must be
  written into the loop, not assumed.

---

## Top findings

**1. The realistic buildable scope (what to cut).** Build the proposal's **vertical slice**: one
data-dense scene; **~25 materials** (ordinal property vectors) × **~20 operations** (declarative
precondition/effect schemas) as the workhorse engine; **~5 authored specials** (radio §38, beacon
§37, dying pilot §19, plus the one showcase aircraft seat §22); cheap (~6-field) objects for
everything else; **single-player first**, then instanced co-op. **Cut / retire:** the §46 density
numbers as targets (60–100 hand-packeted objects, 300–800 hand-authored derived, 40–70 packeted
action families, **700+ enumerated tests**); the §43 heavy packet as the *default* object path; the
§9.3 real-time wall-clock heartbeat (→ event-driven clock); the persistent shard (→ instanced
runs); and the not-yet-needed §48 validators (direction / sound / rescue-route / silly) until their
content exists. Replace 700 enumerated tests with **invariants + fuzz + a golden set** (the §45/§46
lists become the golden set). Decision forcing function: §46 must be explicitly re-scoped, or its
numbers will be mistaken for the plan (IM5).

**2. The single biggest feasibility risk.** It is **not** Evennia (IM1 GREEN), **not** throughput
*given* the inversion, and **not** the LLM stepping state (structurally prevented). After every fix
the proposal lands, the residual existential risk is the **unproven core bet plus an unclosable
quality gap**: that cheap objects deriving behavior from ~25 materials × ~20 operations actually
produce *enough correct, non-dumb* behavior **without per-object tuning** — *and* that the validator,
which checks **resolution + conservation + solvability but never correctness or quality**, can only
tell you when content *resolves*, never when it is *good*. Plausible-but-wrong ordinal values (IM3)
and valid-but-shallow crystallized rules (IM12) pass every automated gate and surface only in
playtest. If per-object tuning turns out necessary, authoring cost re-inflates toward §43 and the
schedule reverts to RED (IM5). **Mitigation:** a measured pilot (generate the 25-material table + 20
operations, report schema-reject rate *and* human-judged wrong-value rate, target <10% post-validate
correction) + a **human-curated golden material table as ground truth** + playtest quality sampling +
no auto-promotion of crystallized rules.

**3. How to define and verify "ontology coverage."** Never against "everything" (unverifiable).
Define it against a **bounded basis** (IM6): the **operation × material matrix ≈ 20 × 25 = ~500
cells**, each with a declared outcome class (works / partial / informative-fail) and a property
test — finite and auditable. Object×object combinatorics are *derived* from the matrix and
**fuzz-sampled**, not authored: run **≥10k seeded `(actor, operation, target, tool)` attempts** over
the scene with an oracle of **0 unresolved (no `You can't do that.`), 0 conservation violations,
rescue reachable from every reachable state, and wall-sensor generic-redirect rate below a chosen
threshold**. **Coverage = resolution + conservation + solvability is verifiable and is the
definition of "done"; semantic correctness/quality is *sampled* (golden set + playtest) and must
never be claimed as complete.** The wall-sensor's redirect-rate is the live boundary metric and the
prioritized authoring/crystallize queue — it is how you *empirically* watch the do-anything wall
recede.
