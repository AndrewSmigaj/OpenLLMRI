# Certainty assessment — the five questions, calibrated

> **Update (decision):** runtime LLM was removed — the engine is now fully deterministic, all
> interactions pre-built; the LLM is a build-time authoring tool only (see `GDD.md` §0a). This
> **retires** the runtime-LLM risks this doc weighed (parser mis-parse from an LLM, runtime latency/
> cost, soft-adjudication cache determinism). Net effect: the picture is slightly *better* and cleaner.
> The headline numbers below still hold — **Q2 (fun) and Q4 (ontology) were never about runtime LLM**;
> they're about authoring quality + whether pre-built responses feel alive, which is unchanged. Q1/Q5
> tick up marginally (determinism is now free). The make-or-break remains the fun playtest.

Calibrated answers to the user's five questions, grounded in the lens cards
(`lenses/{game-design,architecture,implementation}.md`), the `cross-lens-synthesis.md`, and the
three probes (`probes/*`). Each: a **point estimate**, a **confidence band**, the **grounding**, and
**what would move it** — because an honest number says what evidence it rests on.

Estimates are for the design **as now intended** (design.md + the proposal), built to the proposal's
vertical-slice scope. They are *conditional on the named mitigations*; without those, each drops
materially. These are reasoned judgements, not measurements — the whole point of the vertical slice is
to replace them with data.

> Scale: the % is "probability this succeeds *at the stated scope, with the named fixes done*."

---

## Q1 — Will it WORK for what you want? (everything-interacts, one dense scene, rescue wired)
**Estimate: 72% · band 55–85% · trend ↑ with the slice.**
- **Grounding:** AR5/AR8/IM1 (GREEN) — the operation×material engine makes "everything interacts"
  a config problem and Evennia carries it; one dense scene is the *right* place to spend the data
  budget (Probe-2). Rescue-as-additive-confidence (§39) is sound. **But** GD22 + Convergence-3: the
  "everything" is *bounded* by the operation×material matrix; players will find graceful walls. And
  AR11/AR15 (Convergence-4): the data model must be *closed* (environment sink) and conservation
  enforced at runtime for "everything interacts" to be *trustworthy* rather than approximately true.
- **The honest split:** "works as a **bounded-but-large** world that *feels* like everything-with-
  everything inside the physics" → **~72%**. "Works as a literally **unbounded** do-anything world"
  → much lower (~40%) and not the right target — reframe to the bounded matrix.
- **What would move it:** ↑ closing the data model + shipping the conservation ledger; ↑ a working
  slice where 20 operations × 25 materials visibly produces hundreds of sensible interactions. ↓ if
  the matrix turns out to need per-pair tuning (the unproven "no per-object tuning" bet, IM5).

## Q2 — Will it be FUN?
**Estimate: 50% · band 30–70% · the make-or-break, and it is EMPIRICAL.**
- **Grounding:** the single most uncertain answer. Game-design lenses: GD2 (Toy), GD25 (voice),
  GD4/GD18 (chore loop) all sit YELLOW on the **same unproven bet** (Convergence-1): that *generic,
  derived, validated* responses read as **specific and witty** (the §3.5 windbreak magic) rather than
  dry-but-valid. Probe-1 found the fun beats are genuinely there (the Toy opening, the windbreak
  moment, weather/plane beats, co-op fire) **but** identified two cliffs: the long-task **tedium**
  (min 8–18) — survivable only if tick messages *escalate stakes* AND **action-chunking** ships — and
  **dominant-strategy collapse** of the pilot choice without a real cost to tending.
- **Why 50%, not higher:** no automated gate can certify delight; the fuzz harness proves "resolves",
  never "resolves *interestingly*". Fun rests on (a) the quality bet, (b) two specific tedium
  mitigations, (c) curated opening/failure prose. That is three conditional dependencies.
- **What would move it (most important line in this doc):** a **paper/Wizard-of-Oz playtest then a
  real single-player vertical-slice playtest** is the only thing that converts this from a guess to a
  number. ↑ sharply if curated signature responses + escalating ticks + action-chunking land well; ↓
  if early testers find the derived responses flat.

## Q3 — Can smart players always progress? (no impossible / softlocked states)
**Estimate: 80% · band 65–90% · conditional on three commitments + the fuzz instrument.**
- **Grounding:** per-fact solvability is **GREEN** (Walk-1: ≥3 independent clue paths for location;
  the redundancy is real). The risk is **global** softlock, found independently by AR6 **and**
  Probe-3 Walk-3: rescue routes are **not resource-independent** — warmth/fire → stamina → hands sits
  under all of them, so total warmth failure on a cold night kills every route at once, invisibly to
  the per-fact rule. Plus a self-inflicted one: the proposal's **event-driven clock can hang a
  doomed-but-alive party** (AR6).
- **Why 80% and not lower:** every one of these has a **known fix** (Convergence-2): a no-materials
  **warmth floor**, making rescue methods draw on **distinct** scarce resources, a **clock-liveness**
  rule, **degradation-over-hard-loss**, and the **`solvability-fuzz`** harness as the standing
  instrument that *finds* the next one. With those, "smart players always progress" is defensible.
- **What would move it:** ↑ implementing the four fixes + a fuzz harness reporting 0 unresolved /
  rescue-always-reachable across 10k seeded reckless runs. ↓ if the warmth floor proves impossible to
  balance (too generous = no tension; too harsh = softlock).

## Q4 — Is the workflow + ontology-building thorough enough that the LLMs generate everything needed?
**Estimate: 68% · band 50–80% · conditional on the bounded-coverage reframing.**
- **Grounding:** IM6 (GREEN-with-caveat) gives the reframing that makes the question *answerable*:
  you can never verify "everything", so define coverage as a **bounded ~500-cell operation×material
  matrix (property-tested) + a ≥10k-attempt fuzz oracle** (0 unresolved, 0 conservation violations,
  rescue reachable). IM3 (YELLOW): proposer-into-schema + generate-then-validate is the right
  architecture and shrinks the consistency surface ~20×; Probe-2 measured **6 first-pass repairs on
  one object, 4 of them eliminable by schema defaults**, suggesting ~1–2 real repairs/object with a
  good schema — *plausible at slice scale*.
- **The caveat that caps it (Convergence-1):** the validator proves content **resolves + conserves**,
  **never that an ordinal value is correct or a rule is interesting**. So "LLMs generate everything
  that *runs*": ~68%. "LLMs generate everything that is *good*": needs a **human-curated golden
  material table** + playtest — automation can't close it.
- **What would move it:** ↑ a measured generation pilot (real repair rate) + a golden material table
  authored by hand; ↑ cutting §46's hundreds-of-objects/700-tests (IM5 RED) to the slice. ↓ if repair
  rate is high or plausible-but-wrong values pollute the matrix unnoticed.

## Q5 — Does the interaction logic make sense / can it be MORE powerful?
**Estimate: 76% · band 60–88%.**
- **Grounding:** the proposal's model is judged **sound and more powerful** than the original §26:
  declarative operations over materials (AR8/AR5 GREEN = adding power is config, not rewrite), the
  **three resolution modes** (hard / soft-judge-on-rails+clamp+cache / prose) fill the expressive
  middle the original lacked, **affordances-from-state + informative redirect** handle the wall, and
  **resolve-then-crystallize** turns play into authoring (GD24). This is a real power increase.
- **Residual (why not higher):** crystallize **can't mint new primitives** (confined to existing
  operations) so novel verbs still hit a graceful redirect (GD22); the soft-judge cache must be keyed
  and clamped correctly to stay deterministic (AR3/AR4); and AR15 — conservation as a runtime ledger —
  is the prerequisite that makes the whole thing trustworthy.
- **What would move it:** ↑ a slice demonstrating a long emergent chain (webbing→tourniquet→splint, or
  battery+wire→ignition→fire→smoke-signal) resolving cleanly with conservation held; ↑ the conservation
  ledger live. ↓ if soft-adjudication caching proves leaky (nondeterministic replays).

---

## Overall read
The design is **structurally sound and, with the proposal, genuinely buildable** — the architecture
lenses largely pass, the operation×material inversion is the right engine, and the correctness strategy
(invariants + bounded coverage + fuzz) is solid. **One RED (AR15, conservation-as-runtime-ledger) is
fixable and should be the flagship invariant.** The two design-fix bets (route resource-independence;
model closure) have known remedies.

**The make-or-break is Q2 (fun), and it is empirical, not analyzable.** Everything points to the same
move: **build the single-player vertical slice and playtest it.** That one experiment retires the
biggest risk (does derived content feel alive?), exercises the conservation ledger, lets you measure
the real LLM repair rate, and runs the fuzz harness for softlocks. Until it exists, Q2 is a coin-flip
with a good story; after it, every number above sharpens.

**Confidence in the *plan to find out* is high (~90%); confidence in the *game being fun* is ~50%.**
Those are different things, and the vertical slice is precisely the bridge between them.
