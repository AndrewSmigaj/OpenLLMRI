# Implementation / feasibility lenses (IM1–IM12)

Feasibility, LLM-in-the-loop reality, and AI-assisted tooling. These ask "can it actually be
built and run, at the stated scope, by this team + AI?" Each: **key question** · *what to look
for* · applies-when.

**SCOPE & CONSTRAINTS.** These lenses review **feasibility of the execution** *within* the locked vision
and decisions (genre, premise, core promise, and any user-locked decisions; see `VISION.md` and the
GDD/plan "Decisions" lists). They do **not** recommend changing the vision or a locked decision because
it's hard to build. If a finding's only fix would alter one, reframe it as a *risk-within-the-vision*
(mitigations that keep the decision intact) or mark it *"outside scope — vision-level flag"* for the user
to decide — never "build something else." (See `SKILL.md` Protocol steps 2 & 4.)

---

### IM1 Framework Feasibility
**Does the chosen framework support the design idiomatically, or are we fighting it?**
*For each subsystem: is there a blessed extension point, or a hack? Count the overrides; flag any
"work against the grain".* — Applies when building on a framework/engine (here: Evennia).

### IM2 Reactor / Concurrency Model
**Does the runtime's concurrency model survive the load (ticks + many actors + async calls)?**
*Single-threaded reactors must never block; per-tick cost × entities; races on shared entities
within a tick.* — Applies to event-loop / actor / reactor runtimes.

### IM3 LLM Ontology-Authoring Throughput
**Will the LLM actually generate enough CORRECT, CONSISTENT content?**
*Drift/contradiction across many generations; hallucinated capabilities that violate invariants;
does generated content pass the validator without heavy human repair? Measure repair rate.* —
Applies to LLM-generated content/ontology.

### IM4 Runtime LLM Latency/Cost Realism
**Is the in-loop LLM fast and cheap enough per operation, with a safe fallback?**
*p95 latency budget on the interactive path; token cost; a deterministic timeout/fallback so a
slow model never stalls the user.* — Applies to runtime LLM features.

### IM5 Authoring Throughput (human + AI)
**Can the content targets be hit in realistic time by this team + AI?**
*Multiply the density targets by per-item cost; compare to a believable schedule. Usually forces a
vertical-slice scope cut.* — Applies to content-heavy projects.

### IM6 Coverage Verification
**How do you KNOW the content/ontology is complete when "everything" is unbounded?**
*Redefine coverage against a BOUNDED basis (operation × property matrix) + a fuzz sample, because
an unbounded total can never be verified.* — Applies to "do-anything"/open-content systems.

### IM7 Test Strategy
**Is the plan mostly property/invariant tests + a curated golden set + fuzz, not N hand cases?**
*Enumerated tests that can't cover the space; missing property tests for the invariants; no fuzz
oracle.* — Applies to large behavior spaces.

### IM8 Performance
**Do the hot paths stay within budget at target scale?**
*O(n²) recomputes, per-tick work, query/IO per action; caching/dirty-flagging where it matters.*
— Applies to interactive/real-time systems.

### IM9 Persistence / Session Model
**Is state correct across disconnect, reconnect, restart, and (if multiplayer) partial presence?**
*Who owns time/state when actors leave; partial-progress persistence; write contention; instanced
vs persistent.* — Applies to multiplayer / long-running stateful systems.

### IM10 Determinism / Fuzz Harness
**Can you replay seeded runs to FIND softlocks, unresolved attempts, and regressions automatically?**
*A scripted driver + a seed + an oracle (validator/invariants) that flags dead-ends and
"unresolved" outcomes. The only thing that empirically finds global softlock.* — Applies to
sim/progression systems.

### IM11 Tooling & AI-Assisted-Build Practices
**Is the build instrumented for AI-assisted authoring/review at scale (and is it SANE, not bloat)?**
*Generators, validators-as-gates, review subagents/skills, loops, hooks; do they compose, and is
each earning its place?* — Applies to AI-assisted development.

### IM12 Design-Intent Drift Control
**As AI generates/edits over many sessions, what keeps it true to the non-negotiables?**
*An anchor (VISION/spec) + an enforced gate (validator/tests) the AI must pass; risk of drift
toward shallow or over-scoped content across long loops.* — Applies to long-running AI-authoring.
