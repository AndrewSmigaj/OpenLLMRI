# Lens triage — leverage rating of all 54 lenses

**Purpose:** rate every lens by how much *signal* it yields for THIS design, so the deep
dives go where the decisions are and we don't spend equal effort on low-leverage lenses.
Every lens still gets a finding card in `lenses/{game-design,architecture,implementation}.md`
(per the user's "for each lens"); the **HIGH** set gets paragraphs + evidence, **MED** gets a
few sentences, **LOW** gets a line.

Leverage = (how much it could change the design) × (how uncertain the answer is now).
A lens whose answer is obviously "fine" is LOW even if important; a lens probing a load-bearing
unknown is HIGH.

Lens IDs are defined in the three skill libraries under `.claude/skills/lenses/`.

---

## Game-design lenses (25)

| ID | Lens | Lev | Why for Whiteout |
|----|------|-----|------------------|
| GD1 | Essential Experience | MED | The "understand a living world under pressure" feeling is clear; risk is delivery, covered better by GD2/GD4. |
| GD2 | The Toy | **HIGH** | Is it fun to poke the world *before* a goal? If the cabin isn't a great toy in 2 min, nothing downstream saves it. |
| GD3 | Curiosity | MED | Examine-hints driving "could I…?" — important but downstream of GD2/GD20. |
| GD4 | Fun (chore audit) | **HIGH** | Tick-saw/stamina/cold-hands are the exact places depth becomes tedium. Decisive for Q2. |
| GD5 | Endogenous Value | MED | Do tinder/charge/lucidity feel valued — likely yes if survival stakes land; lower uncertainty. |
| GD6 | Problem Solving | MED | Multi-route rescue posed; whether routes are *honestly different* is really AR6/GD7. |
| GD7 | Meaningful Choices | **HIGH** | Dominant-strategy collapse (always-loot-pilot, always-stay) would gut the design. |
| GD8 | Triangularity | **HIGH** | Risk/reward spine (fuel ignition, leaving search area, cannibalism) — core of replay tension. |
| GD9 | Skill vs Chance | MED | Deterministic lean is right; only the few stochastic bits (radio fragments, pilot timer) need a look. |
| GD10 | Interest Curve | **HIGH** | Built-in curve from weather+pilot timer, but the mid-game "survive the night" sag is a real risk. |
| GD11 | Failure | MED | "Every attempt resolves" is the antidote; whether failure teaches is downstream of GD25. |
| GD12 | Freedom / Indirect Control | **HIGH** | Making the bounded ~20-operation ceiling feel boundless is the whole illusion. |
| GD13 | Imagination | MED | Text leans on it; asset only if prose is evocative+consistent — consistency is GD23. |
| GD14 | Accessibility | MED | Onboarding a "do-anything" world is hard; overlaps GD20/GD21 which carry more signal. |
| GD15 | Story–Mechanic Harmony | MED | Tick-grind must dramatize desperation; really a restatement of GD4 for narrative. |
| GD16 | Cooperation | **HIGH** | If co-op: is shared play *fun* or just logistics? Also gates the session-model decision (IM9). |
| GD17 | Goals | MED | No quest log → "what do I do" risk; mitigated by pilot/radio cues; medium uncertainty. |
| GD18 | Time / Pressure | **HIGH** | The clock as drama-not-punishment is the riskiest felt-experience question (ties to the tick model). |
| GD19 | Reward | MED | "Reward deeper work" legibility — important, but a tuning problem more than a design unknown. |
| GD20 | Affordance Discoverability | **HIGH** | The tightrope between guess-the-verb and checklist; decisive for Q3 (can smart players progress). |
| GD21 | Parser / Intent Legibility | **HIGH** | A silent LLM mis-parse doing the wrong thing breaks trust worse than "didn't understand." |
| GD22 | "Do-Anything" Expectation Mgmt | **HIGH** | The existential risk: the wall where a sensible attempt can't be represented. |
| GD23 | Systemic Consistency | **HIGH** | Same rule everywhere, or the imm-sim contract leaks at authored special-cases (§26 tier 1). |
| GD24 | Emergent Narrative | **HIGH** | Do simple actions combine into unscripted stories? The payoff of the whole bet. |
| GD25 | Resolution-Not-Success | **HIGH** | Generating *informative physical failure* at scale without hand-authoring each — the game's voice. |

## Architecture lenses (17)

| ID | Lens | Lev | Why for Whiteout |
|----|------|-----|------------------|
| AR1 | Functional-Core Boundary | MED | Central bet, but already well-specified (ADR-0003) and easy to enforce; uncertainty is low. |
| AR2 | Coupling & Cohesion | MED | clock↔scheduler↔weather↔survival cross-talk + perception touching every message path; watch, not decide. |
| AR3 | Single Source of Truth | **HIGH** | Postgres Attributes vs in-memory snapshot vs LLM prose — divergence is the classic, likely bug. |
| AR4 | Determinism & Reproducibility | **HIGH** | RNG seeding, tick ordering across concurrent actions, cached LLM intent — required for testing *and* trust. |
| AR5 | Content-Density Scalability | **HIGH** | Does the architecture hold at 100 objects / 800 derived / O(objects×observers) perception? |
| AR6 | Softlock / Failure-Mode | **HIGH** | The ≥3-paths rule is per-*fact*; emergent *global* exhaustion is uncovered. Decisive for Q3. |
| AR7 | Observability / Debuggability | MED | Decision traces for §26 tiers/perception/ticks matter for live debugging; build concern, low design risk. |
| AR8 | Extensibility | **HIGH** | Files-touched per new object/material — determines whether "more powerful" is cheap or a rewrite (Q5). |
| AR9 | LLM Latency & Cost | **HIGH** | Stage-A on the player's turn + authoring cost across hundreds of objects; a real envelope, currently unbudgeted. |
| AR10 | Griefing Surface | MED | fast-forward consent, irreversible shared-resource destruction; gated by the (likely instanced) session model. |
| AR11 | Data-Model Soundness | **HIGH** | Does object/part/material/conservation actually *close*? If not, "everything interacts" is aspirational. |
| AR12 | Testability (invariants) | MED | Property tests over 700 hand-cases — important method choice, but follows from AR4/AR11. |
| AR13 | Premature Abstraction (smell) | **HIGH** | 20 operations + packets + validator designed before one pass shipped — a framework no content has stressed. |
| AR14 | God Object (smell) | MED | The resolver/Narrator/propagator are natural sinks; watch during build, not a design-time decision. |
| AR15 | Leaky Abstraction / Missing Invariants (smell) | **HIGH** | Conservation must be a *runtime assertion*, not a doc line, or "no prose-only change" is unenforced. |
| AR16 | Over-Configuration (smell) | **HIGH** | Dozens-of-fields packets + silent defaults = invisible content bugs; directly threatens LLM-authoring. |
| AR17 | Untested Critical Path (smell) | MED | LLM timeout mid-turn, two players one object, validator-passes-yet-unreachable — covered by AR6/AR4/IM10. |

## Implementation / feasibility lenses (12)

| ID | Lens | Lev | Why for Whiteout |
|----|------|-----|------------------|
| IM1 | Evennia Feasibility | **HIGH** | Does the framework carry scene/zone/perception/tick without fighting it? Gates "will it work" (Q1). |
| IM2 | Reactor / Concurrency | MED | Single-thread Twisted + ticks + async LLM; real, but a known pattern — engineering, not unknown design. |
| IM3 | LLM Ontology-Authoring Throughput | **HIGH** | Will the LLM actually produce enough *correct, consistent* content? Decisive for Q4. |
| IM4 | Runtime LLM Latency/Cost | MED | Per-turn fallback budget; overlaps AR9; mostly a "needs a deterministic timeout" answer. |
| IM5 | Authoring Throughput (human+AI) | **HIGH** | §46 density is months of curation; forces the vertical-slice scope decision. |
| IM6 | Ontology Coverage Verification | **HIGH** | You can't verify "everything"; must redefine coverage as bounded operation×material + fuzz. Reframes Q4. |
| IM7 | Test Strategy | MED | invariants vs 700 enumerated — important, but follows from AR4/AR11/IM6. |
| IM8 | Performance | MED | Perception O(objects×observers); caching matters at density; tuning, not a design unknown. |
| IM9 | Persistence / Session Model | **HIGH** | Who owns the clock when the last awake player drops; the unspecified instanced-vs-persistent fork. |
| IM10 | Determinism / Fuzz Harness | **HIGH** | The only thing that *finds* global softlocks + unresolved attempts; the oracle for Q3. |
| IM11 | Tooling / Claude-Code Practices | **HIGH** | Whether the AI-assisted build is instrumented at scale — the user's explicit ask. |
| IM12 | Design-Intent Drift Control | MED | VISION + validator as anchor against long AI loops; important, but a process answer. |

---

## Deep-dive set (the HIGH lenses — 26)

Grouped by the decision each most informs:

- **Is the "everything" promise real? (Q1, Q5)** — GD12, GD22, GD23, GD24, GD25 · AR11, AR8 · IM1.
- **Is it fun, not tedious? (Q2)** — GD2, GD4, GD7, GD8, GD10, GD16, GD18.
- **Can smart players progress without dead-ends? (Q3)** — GD20, GD21 · AR6 · IM10.
- **Can the ontology actually be built (by LLMs at density)? (Q4)** — IM3, IM5, IM6 · AR5, AR13, AR16.
- **Will the LLM seam stay trustworthy/deterministic?** — AR3, AR4, AR15 · AR9 · IM9.
- **Is it instrumented for an AI-assisted build?** — IM11.

> 26 HIGH is more than the ~15 the Plan agent suggested, because the user asked for maximal
> thoroughness. To keep signal up, the apply-lenses pass (P5) runs three parallel group
> agents and the HIGH lenses get the paragraph treatment while MED/LOW get proportionally
> less. The single most valuable artifact will be `cross-lens-synthesis.md`, which surfaces
> where HIGH lenses *conflict* (notably **GD12 "feel boundless" vs AR5/IM5 "density won't
> scale" vs GD22 "the wall"** — the central tension of the project).

## Notable a-priori conflicts to watch (seed the synthesis)
1. **GD12/GD22 (boundless / no wall) ✕ AR5/IM5 (density is unaffordable).** More authored depth
   = fewer walls but slower to build. The resolve-then-crystallize loop is the proposed bridge;
   the lenses must judge whether it actually closes the gap.
2. **GD23 (systemic consistency) ✕ §26 tier-1 authored special-cases.** Every bespoke rule is a
   place the "same rule everywhere" contract leaks. How many specials before players stop trusting?
3. **GD18/GD4 (clock as drama, not chore) ✕ the multiplayer real-time tick (§9).** The tick model
   is simultaneously the fun-pressure source and the tedium/wait risk.
4. **AR4 (determinism) ✕ runtime LLM (crystallize loop, Stage-A fallback).** Caching + clamping is
   the proposed reconciliation; AR3/AR15 judge whether it holds.
