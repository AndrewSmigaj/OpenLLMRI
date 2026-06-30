# Architecture lenses (AR1–AR17)

Design-integrity lenses (AR1–AR12) + a code-smell / code-debt subset (AR13–AR17).
Each: **key question** · *what to look for* · applies-when.

**SCOPE & CONSTRAINTS.** These lenses review the **execution** of the architecture *within* the locked
vision and decisions (genre, premise, core promise, and any user-locked decisions; see `VISION.md` and
the GDD/plan "Decisions" lists). They do **not** recommend changing the vision or a locked decision. If a
finding's only fix would alter one, reframe it as a *risk-within-the-vision* (mitigations that keep the
decision intact) or mark it *"outside scope — vision-level flag"* for the user to decide — never "build
something else." (See `SKILL.md` Protocol steps 2 & 4.)

---

### AR1 Functional-Core Boundary
**Is pure logic cleanly separated from IO/framework/DB/time, and does anything leak across?**
*Hunt hidden impurity in the "pure" core: imports of the framework, `time.now()`, RNG, network,
global state. One leak erodes testability.* — Applies to layered / hexagonal designs.

### AR2 Coupling & Cohesion
**Can each system change independently, and does each module do one thing?**
*Cross-talk hotspots where N systems all touch one path; modules that know too much about each
other.* — Always.

### AR3 Single Source of Truth / State Ownership
**Is there exactly one authority for each piece of state?**
*Caches/snapshots/denormalized copies that can diverge from the canonical store; two writers to
one fact.* — Applies to stateful systems, esp. with caches or in-memory mirrors.

### AR4 Determinism & Reproducibility
**Given the same inputs, does the system produce the same result — including with RNG / async / LLM?**
*Unseeded randomness, ordering races, wall-clock dependence, uncached nondeterministic calls.
Required for testing and for trust.* — Applies to sims, anything testable, LLM-in-loop.

### AR5 Content-Density Scalability
**Does the architecture hold as content/entities grow 10–100×?**
*Per-item authored rules vs generic rules; O(n²) recompute (e.g. perception over objects×observers);
load/validate cost at target density.* — Applies to content-heavy / sim worlds.

### AR6 Softlock / Failure-Mode Analysis
**Can the system reach a state with no path forward?**
*Per-item guarantees (≥3 paths per fact) miss GLOBAL exhaustion (resources consumed across the
whole world-state). Look for irreversible actions + finite shared resources.* — Applies to
progression/survival/puzzle systems.

### AR7 Observability / Debuggability
**When output is wrong, can you trace which rule/branch produced it?**
*Decision traces for resolution tiers, routing, scheduling; without them, live (esp. multiplayer)
bugs are untraceable.* — Applies to rule engines, distributed/concurrent systems.

### AR8 Extensibility
**How many files must change to add one new entity/rule/feature?**
*The cost of "one more object/material/scenario." High cost = adding power is a rewrite, not a
config.* — Applies to platforms/engines meant to grow.

### AR9 LLM Latency & Cost Budget
**What is the per-operation and per-batch latency/$ envelope for every LLM call?**
*Calls on the user's critical path (need async + timeout + deterministic fallback); authoring cost
across thousands of generations; caching strategy.* — Applies to any LLM-integrated system.

### AR10 Security / Griefing Surface
**What can a malicious or careless actor do to shared/critical state?**
*Irreversible destruction of shared resources, denial-of-fun (spam, clock control), injection via
an LLM parser, privilege of one user over others.* — Applies to multiplayer/shared/untrusted-input.

### AR11 Data-Model Soundness
**Does the core data model actually close — can it represent every required state without contradiction?**
*Conservation/accounting that must balance; partial states; provenance; relationships the schema
can't express; "where does X live" gaps.* — Applies to sim/domain-model-heavy systems.

### AR12 Testability (invariants vs enumeration)
**Can correctness be asserted as invariants/properties rather than enumerated cases?**
*Open spaces can't be covered by hand cases; look for invariant candidates (conservation,
monotonicity, symmetry) and a fuzz oracle.* — Applies to large/open behavior spaces.

---
## Code-smell / code-debt subset

### AR13 Premature Abstraction
**Are abstractions earning their keep, or speculative frameworks no concrete case has stressed?**
*Generalized machinery built before a real user; config/plugin systems with one implementation;
"we'll need it later."* — Applies to young codebases / framework-first designs.

### AR14 God Object
**Is any module accreting unrelated responsibilities?**
*Natural sinks (a resolver, a "manager", a world-state) growing toward thousands of lines that
"know everything."* — Always (during build).

### AR15 Leaky Abstraction / Missing Invariants
**Do boundaries hold at RUNTIME, and are the laws enforced rather than documented?**
*A "rule" that's only a doc line (e.g. "conservation holds", "no prose-only state change") with no
runtime assertion is unenforced. Boundaries that callers can bypass.* — Applies to rule/contract
systems.

### AR16 Over-Configuration
**Is behavior buried in sprawling data/YAML with weak validation and silent defaults?**
*Dozens-of-fields records, under-filled + silently defaulted → invisible content bugs; logic that
should be code hidden as data.* — Applies to data-driven / authored-content systems.

### AR17 Untested Critical Path & Error-Handling Gaps
**Are the rare-but-catastrophic paths (failure, timeout, contention, recovery) actually tested?**
*LLM/endpoint timeout mid-operation; concurrent writers; "validator passes yet goal unreachable";
empty/exhausted states.* — Applies to systems with external deps / concurrency / progression.
