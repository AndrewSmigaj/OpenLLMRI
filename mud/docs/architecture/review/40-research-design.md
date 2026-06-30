# A6 — Design research: the three load-bearing software-design bets

> **Purpose.** Deep, cited prior-art research on the three highest-risk *software-design* decisions in
> `implementation-architecture.md`, to confirm, improve, or challenge them before build. Targets the top
> three by Risk `R` in `review/30-certainty.md`: **DR-05** (operation model, R=105), **DR-11**
> (conservation closure, R=90), and **DR-04/DR-09** (ordinal expressiveness + redirect quality, R=60
> each). The companion doc on Evennia-specific verification (DR-10/14/15) lives elsewhere; this file is
> the *design* half of A6.
>
> Each section gives: the **findings** (cited inline), a **CONFIRM / IMPROVE / CHALLENGE** verdict, a
> **recommended approach**, and a **confidence delta**. A summary table closes the doc. All three bets
> survive the research; two are improved, none is challenged at the level of "rework the design."

---

## DR-05 — How should "operations" be represented? (mini-DSL vs plain Python vs hybrid)

**The v2 decision under test:** a *hybrid* — a small declarative DSL (precondition/effect schema,
interpreted at runtime) for the common stateless operation×material cases, plain Python for
stateful/complex logic (FSMs, multi-step systems), all behind one `Operation`/tier interface, built
"plain functions first, extract the DSL only once repetition is proven."

### Findings

1. **Inform 7 is itself a hybrid: declarative rule *heads* dispatching to arbitrary imperative
   *bodies*.** A rule has a declarative head (`Before/Instead/Check/Carry out/After/Report` + a
   condition pattern) but its body is ordinary procedural code — `say`, `now X is Y`, `silently try
   taking the noun`, control flow `stop the action`/`continue the action`. The "DSL" is only a dispatch +
   precedence skeleton over imperative logic, *not* a data-only effect language.
   (https://ganelson.github.io/inform-website/book/WI_7_3.html)
2. **Inform 7's rulebook precedence is automatic specificity-ordering — and documented as *leaky*,
   requiring manual override.** Rules sort most-specific-first and run in order until one ends in
   success/failure (and rulebooks differ in default outcome: Instead→failure, After→success,
   Before/Check/Carry-out→no-decision). The manual concedes Inform "will sometimes get it wrong … or
   place them in an order which does not suit us" and ships explicit overrides — *listed before/after*,
   *listed first/last*, *listed instead of*, *not listed*. Lesson: automatic resolution is a usability
   win but needs a deterministic manual escape hatch.
   (https://ganelson.github.io/inform-website/book/WI_19_9.html ;
   https://ganelson.github.io/inform-website/book/WI_19_4.html ;
   https://inform-7-handbook.readthedocs.io/en/latest/chapter_4_actions/rulebooks_%26_stop_the_action/)
3. **TADS 3 models verbs as objects with a fixed multi-phase pipeline + reusable precondition objects —
   logic lives in overridable methods, not data.** The cycle is parse → resolve → *verify* → *check
   preconditions* → *check* → *action* → *report*; `PreCondition` objects (`objVisible`, `touchObj`, …)
   can fire *implicit actions* to satisfy themselves (auto-open a door), and per-object behaviour is plain
   code in `verifyDobjX`/`checkDobjX`/`actionDobjX`. Both leading IF engines converge on the engine's
   exact shape: a *structured precondition/phase interface wrapping arbitrary code*.
   (http://www.tads.org/t3doc/doc/techman/t3cycle.htm ; http://www.tads.org/t3doc/doc/gsg/precond.htm)
4. **PDDL cleanly separates declarative action schemas from the solver, but pure STRIPS is expressively
   thin — and the family had to escalate past it for exactly our "stateful" cases.** STRIPS allows only
   conjunctive preconditions + add/delete effects; ADL adds disjunctive/quantified/negative preconditions
   and *conditional effects* `(when C E)`; PDDL 2.1 / PDDL+ add *numeric fluents* and *durative actions*
   (separate start/over-all/end conditions + duration) and *processes/events* for continuous change —
   things instantaneous schemas "cannot represent." This is direct prior-art that a thin declarative tier
   covers the common conjunctive case and a *second tier* (our "plain Python for FSMs/timed/multi-step
   systems") is unavoidable, not a smell.
   (https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume28/coles07a-html/node14.html ;
   https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume27/fox06a-html/node31.html)
5. **Forward-chaining rule engines (Rete/Drools) pay off for declarative pattern-matching but carry
   documented maintainability costs — and are the *wrong* tool for coupled, stateful logic.** Drools'
   own docs warn it is "not really intended to handle workflow or process executions," that learning-
   curve overhead must be factored in, and that *strongly coupled* rules (one rule's firing directly
   triggering another) "will turn out to be inflexible … a rule engine is overkill." Sequential operation
   logic is exactly that coupled case where a data engine becomes a debugging trap.
   (https://docs.jboss.org/drools/release/5.5.0.Final/drools-expert-docs/html/ch01.html ;
   https://en.wikipedia.org/wiki/Rete_algorithm)
6. **The "rule of three" directly endorses "plain functions first, extract the DSL later."** Fowler's
   heuristic: two copies don't justify abstraction, extract on the third; "premature refactoring risks
   selecting a wrong abstraction" that must later be re-refactored. The build rule is a textbook
   application. (https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))
7. **The "configuration complexity clock" + Greenspun's rule warn an over-eager content DSL reinvents a
   worse language.** Hadlow's clock runs hard-code → config → rules-engine → DSL → *back to hard-code*;
   by "9 o'clock" you've built a custom language with no IDE/debugger support and are "back where we
   started … except now in a much crappier language." Greenspun names the failure: complex programs grow
   "an ad hoc, informally-specified, bug-ridden, slow implementation of half of Common Lisp." Both argue
   for a *deliberately small, capped* DSL. (http://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html [blog] ;
   https://en.wikipedia.org/wiki/Greenspun%27s_tenth_rule)
8. **ECS/data-driven design is the right model for the *stateless* operation×material matrix; Fowler
   recommends an *internal* DSL to keep host tooling.** ECS systems "act globally over all entities that
   have the required components," naturally ignoring non-matching entities — the natural encoding for
   "operation = system selecting entities by material tag." Fowler frames an internal DSL as "a particular
   form of API in a host general-purpose language," grown from an ordinary library, so you keep the
   debugger and tests (vs. a parsed external language → the clock's 9-o'clock trap).
   (https://en.wikipedia.org/wiki/Entity_component_system ; https://martinfowler.com/books/dsl.html)

### Verdict: **CONFIRM (and modestly IMPROVE)**

Convergent, independent evidence backs the hybrid. The two most mature deterministic IF engines (Inform 7,
TADS 3) are *themselves* hybrids — a declarative precondition/phase/precedence skeleton wrapping arbitrary
imperative code — and neither encodes stateful operation logic as pure data (Findings 1–3). The planning-
languages lineage proves the tier *boundary* is real: a STRIPS-level schema covers the common stateless
matrix, but disjunction/conditional-effects/numeric/temporal/stateful behaviour provably forces escalation
to Python-equivalent expressiveness (Findings 4–5). Three SE principles independently endorse deferring the
DSL and keeping it small (Findings 6–8). The only reason this isn't a *stronger* confirmation: no source is
a survival-sim (transfer is by analogy), and Inform 7's documented *leaky-specificity* problem is a concrete
hazard you must engineer around in the precedence layer.

### Recommended approach — one interface, two implementations

- **Operation protocol (both tiers register identically):** `selector` (verb + material/tag match driving
  candidacy) · `specificity` (explicit deterministic precedence key) · `can_apply(ctx) -> success /
  failure(reason) / no_decision` · `apply(ctx) -> [Effect|Event]`.
- **Tier A — declarative data ops (the matrix):** records keyed by `(verb, material/tags)`, each a
  *conjunctive* precondition list over named predicates + a *closed primitive-effect set*
  (`set_state`, `change_material`, `consume`, `spawn`, `emit`, `damage`). One evaluator interprets all.
  No branching beyond the flat list, no loops, no numeric integration, no multi-turn state. Keep it an
  **internal** DSL (Python dataclasses/decorators interpreted in-process), not a parsed external language.
- **Tier B — Python ops:** same interface, arbitrary code (radio FSM, the eight `systems/*`, cross-object
  cascades), registered under the same `(verb, selector)` keys so dispatch is uniform.
- **Single deterministic dispatcher (the I7/TADS lesson):** gather candidates, sort by explicit
  `specificity` then registration order (stable tie-break), run until one returns success/failure
  (I7's "stop the action"); ship `force_first/last/replace/disable` overrides from day one (Finding 2).
- **Write the DSL's *exclusion list* using PDDL's escalation ladder** as the tier boundary spec: anything
  needing disjunction/quantification, conditional `when`-effects, numeric integration, time/duration,
  structured randomness, or multi-turn state goes to Tier B (Findings 4–5).

### Confidence delta: **+6 to +9 (DR-05 65 → ~71–74)**

Multiple independent authoritative lines (two shipping hybrid IF engines; the STRIPS→ADL→PDDL+ escalation
ladder marking the exact tier boundary; three convergent SE principles) all point the same way. Held below
+10 because transfer is by analogy (no survival-sim source) and I7's leaky-precedence problem is a real,
unsolved-until-built risk in *our* dispatcher.

---

## DR-11 — Can runtime conservation actually *close*, with an environment sink?

**The v2 decision under test:** a pre-commit ledger inside `apply()` asserts per-channel balance
(mass/energy/material-identity/contamination) before any mutation commits; an explicit **accountable**
environment sink (tracks total absorbed per channel, monotonic non-decreasing, reviewable) absorbs
legitimate losses (smoke to air, heat lost) so burn/melt/boil/dry *balance*.

### Findings

1. **The "environment sink" is exactly the textbook control-volume / system+surroundings method — the
   design is principled, not ad hoc.** Engineering conservation draws a control-volume boundary and
   balances flows across it: mass `dm_CV/dt = Σṁ_in − Σṁ_out`; energy = stored-energy change equals net
   transfer via heat, work, and mass flow; systems are classed by what crosses the boundary
   (isolated/closed/open). Our sink *is* the surroundings; per-channel balance *is* the control-volume
   balance.
   (https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Introduction_to_Engineering_Thermodynamics_(Yan)/05%3A_The_First_Law_of_Thermodynamics_for_a_Control_Volume/5.03%3A_Mass_and_energy_conservation_equations_in_a_control_volume ;
   https://www.engr.colostate.edu/CBE101/topics/material_balances.html)
2. **Mass conservation is *additive bookkeeping over real, extensive quantities* — atoms in = atoms out,
   total mass in = total mass out.** Balancing a chemical equation *is* enforcing conservation of mass;
   for combustion you draw O₂ *in* from the environment and send gases *out* — both real-valued, never
   ordinal. (https://www.engr.colostate.edu/CBE101/topics/material_balances.html ;
   https://www.solubilityofthings.com/law-conservation-mass/)
3. **Qualitative Process Theory represents amounts *ordinally* (a "quantity space" of landmark values +
   inequalities), not as numbers.** Forbus 1984 ("Qualitative Process Theory," *Artificial Intelligence*
   24:85–168): a value is known only by `< = >` against landmarks, with no magnitude; quantities change
   only via processes' direct influences `I+`/`I-`.
   (https://www.qrg.northwestern.edu/papers/Files/QPT-PHD(searchable).pdf ;
   https://www.qrg.northwestern.edu/ideas/qptidea.htm)
4. **The crux: qualitative/ordinal *arithmetic is ambiguous* when opposing influences combine — the
   formal reason ordinals cannot close a balance.** In QPT, with influences in both directions "the net
   change is ambiguous." In de Kleer & Brown's confluences, variables carry only sign `[+]/[0]/[-]`, and
   `[+] + [-]` "produces an ambiguous outcome — the system cannot determine whether the result is
   positive, negative, or zero," and that ambiguity "spreads throughout most of the network." A ledger
   that must *prove* `in = out + sink` cannot tolerate `?`.
   (https://dekleer.org/Publications/Scanned%20AIJ.pdf ; https://arxiv.org/pdf/1212.2445 ;
   http://cse.unl.edu/~choueiry/Documents/Kuipers-QualPhysics.pdf)
5. **Qualitative/naive physics is the "rule out the impossible" tool, not the "compute the balance"
   tool.** de Kleer's qualitative physics "excels at ruling out impossible scenarios but struggles with
   competing plausible outcomes," needing extra constraints/measurements to resolve; Hayes's *Naive
   Physics Manifesto* / *Ontology for Liquids* models the world in discrete qualitative terms
   (containment, flow, histories) for *ontology and causal direction*, not numeric ledgers.
   (https://dekleer.org/Publications/Scanned%20AIJ.pdf ; https://en.wikipedia.org/wiki/Pat_Hayes)
6. **Cautionary baseline: real material-flow games *do not* strictly conserve.** Oxygen Not Included
   "does not fully ensure the conservation of energy or mass" and runs hard-coded transitions (a Space
   Heater draws 120 W but emits ~18,000 W; the game "does not care about conservation of energy between
   heat, electrical, and food forms"), which players exploit to delete heat/germs. Conservation is easy
   to *claim* and hard to *hold*. (https://oxygennotincluded.fandom.com/wiki/Hidden_Mechanics)
7. **Floating-point material flow *leaks* — Factorio knowingly loses fluid to float error** ("100 units
   go in and 99.9 come out"), an accumulating error the devs decline to fix. This is precisely the failure
   a pre-commit ledger with exact units prevents. (https://wiki.factorio.com/Fluid_system)
8. **Dwarf Fortress uses *threshold/gate* semantics for energy, not an energy balance — and does not
   mass-balance either.** It tracks material temperature in "degrees Urist" with
   `[MELTING_POINT]/[BOILING_POINT]/[IGNITE_POINT]/[SPEC_HEAT]`, moving toward ambient each tick; fire is
   injected non-conservingly and burning items "take damage … before disappearing" rather than balancing
   to ash+smoke. DF treats ignition/melt/boil as *gates* (cross a landmark → change state) — exactly the
   ordinal-as-gate pattern that *does* work. (https://dwarffortresswiki.org/index.php/DF2014:Temperature)
9. **Exact conservation is achievable by *quantizing to integer/fixed-point units* — kills drift, gives
   determinism.** Fixed-point sims "treat values as integers scaled by a fixed factor" so results are
   bit-identical everywhere (how deterministic lockstep RTS avoid float indeterminism); integer "units"
   make a sum balance *exactly* (no epsilon). Integers balance exactly; ordinal buckets do not.
   (https://www.gamedeveloper.com/programming/cross-platform-rts-synchronization-and-floating-point-indeterminism)

### Two worked balances (per-channel, with sink entries)

Both use the engine's existing real `mass_kg` / `Part.mass_kg`. Numbers are illustrative material
constants (polyurethane foam ≈25 MJ/kg, ≈5% char residue).

**A. Foam cushion burned — `mass_kg = 0.40`.**

| Channel | IN | OUT (stays in world) | OUT → SINK | Balance |
|---|---|---|---|---|
| Mass (kg) | foam 0.40 | ash/char 0.02 | smoke+volatiles 0.38 (`SINK[air]`) | 0.40 = 0.02 + 0.38 ✓ |
| Energy (MJ) | chemical released ≈9.50 | ash thermal ≈0.05 | heat ≈9.45 (`SINK[heat]`) | 9.50 = 0.05 + 9.45 ✓ |
| Contamination (units) | 3 retardant units | 1 → ash | 2 → `SINK[air]` | 3 = 1 + 2 ✓ |

For a *true atom* balance you'd also draw O₂ *in* from `SINK[air]` (≈1.5–2 kg per kg fuel) and emit
CO₂+H₂O+soot *out* — both real-valued. For object material-identity accounting the split above already
closes. **The energy channel needs real numbers:** "burnability = high" supplies no MJ — it can *gate*
ignition and *rank* rate, but cannot produce the 9.50.

**B. Fabric sheet cut into 5 strips — `mass_kg = 0.20`, length 1.00 m.**

| Channel | IN | OUT (5 strips) | OUT → SINK | Balance |
|---|---|---|---|---|
| Mass (kg) | sheet 0.20 | 5 × 0.03996 = 0.19980 | dust/kerf 0.00020 | 0.20 = 0.19980 + 0.00020 ✓ |
| Length (m) | 1.00 | 5 × 0.20 (cross-cut) | ≈0 | 1.00 = 1.00 ✓ |
| Energy (MJ) | mech. work ≈0 | — | ≈0 | trivial |
| Contamination | surface units | partition with mass across 5 | ≈0 | exact (integer split) |

With a zero-kerf idealization, `0.20 = 5 × 0.04`, sink = 0. This balance is pure addition of like-signed
contributions → no qualitative ambiguity, exact under reals or integer units.

### Can ordinals conserve, or do you need real numbers?

**You need real-valued *extensive* quantities to conserve; ordinals cannot carry a balance — but ordinals
remain correct for *intensive* properties, gates, and rate-ranking.** Two independent reasons from the
sources: (1) conservation must sum contributions and check the total; ordinal addition of opposing terms
gives `[+] + [-] = ?` and the ambiguity propagates (Finding 4), so a balance over ordinals is unsound.
(2) Bucketing destroys the residue: even mapped to fixed numbers, `low + low` is not reliably `med`, and
re-bucketing throws away the exact remainder a ledger must track. So keep **ordinals for material
*properties*** (burnability, hardness, brittleness, toxicity tier) and for **gates** (ignite/melt/boil
landmarks — DF's pattern, Finding 8); carry the **conserved channels (mass, contaminant amount, and
energy-in-Joules if you want a real balance) as real numbers** — which the engine *already does* via
`mass_kg`/`Part.mass_kg`. This is the prompt's expected answer, **confirmed** (not corrected) by sources.

### Verdict: **CONFIRM (with refinement → IMPROVE)**

Per-channel conservation with an accountable, *monotonic* sink is sound and standard — literally the
control-volume / system+surroundings method (Finding 1). The monotonic (absorb-only) sink is what keeps it
*tractable*: because every contribution enters the sink with the same sign, you never hit de Kleer's
`[+] + [-] = ?` ambiguity. It is tractable for **mass, material-identity, and contamination** across
burn/melt/boil/cut, because each transform is mass-additive (melt/boil conserve material mass exactly —
state is intensive, latent heat is the energy term; burn splits mass into ash+smoke, drawing O₂ from the
air-sink). It becomes intractable/ambiguous *only if* you (a) run the balance over ordinal arithmetic, or
(b) demand a strict numeric energy balance from invented ordinal numbers.

### Recommended simplifications

1. **Conserve mass exactly with real kg, preferably integer/quantized units** (e.g. milligram-units) for
   the committed ledger, so the balance is bit-exact and deterministic — explicitly to avoid
   Factorio/ONI float leakage (Findings 6, 7, 9). Pairs with the DR-12 determinism contract.
2. **Make the sink strictly monotonic per channel (absorb-only).** Not just hygiene — it is what
   guarantees unambiguous, sound addition (sidesteps Finding 4) and makes anomalous growth reviewable.
3. **Treat energy as a *gate* or a *real-Joule budget*, not an ordinal balance.** Use ordinal
   burnability/ignite-point to decide *whether* a transform fires and to rank its rate (DF-style
   threshold); if you want energy to truly balance, carry it in real Joules. **Do not balance energy with
   ordinals.** For the slice, an energy *gate* (does it ignite? does the budget cover the cut?) is
   sufficient; a full Joule balance is optional polish.
4. **Tolerance policy:** integer units → zero tolerance; if any float remains, fix an epsilon and route
   the rounding remainder *explicitly to the sink* so it stays accounted.

### Confidence delta: **+7 (range +6 to +10), DR-11 70 → ~77–80**

Bump because (a) the sink/per-channel design maps onto an authoritative method (control volume), (b)
quantized-unit practice confirms exact drift-free conservation is achievable, and (c) QPT/de Kleer pin the
one real constraint — keep conserved quantities real-valued (already true via `mass_kg`), confine ordinals
to intensive properties/gates. Held below higher because energy-channel fidelity (gate vs. true Joule
balance), contamination-channel semantics, and multi-output reactions that pull mass from the air-sink are
still under-specified, and the real-game baselines show conservation is easy to claim and hard to hold.

---

## DR-04 / DR-09 — Ordinal expressiveness + "nearest operations" redirect

**The v2 decisions under test.** DR-04: ~25 materials as ordinal property vectors
(`none<very_low<low<med<high<very_high<extreme`) mapped to fixed numbers (0.0…1.0) — *expressive enough*
for good, non-degenerate outcomes? DR-09: when an action can't resolve, pick the "nearest operations" and
emit an informative redirect that tells the player what they *can* do without spoiling puzzles.

### Findings — DR-04 (ordinal expressiveness)

1. **BotW's "chemistry engine" is strong evidence that *few discrete types + consistent rules* yield
   combinatorial depth.** A handful of elements (fire/water/ice/electricity/wind) act on materials
   (wood/rock/metal/Link) under ~3 simple consistent rules; the designers call it "an extremely simple
   [model] but allows for the expression of all sorts of events," and note players trust a ruleset "as
   long as [the rules] are consistent, and importantly, clever." Discrete categories, not continuous
   stats, drive the emergence. (https://www.gamedeveloper.com/design/video-designing-i-zelda-breath-of-the-wild-i-s-unconventional-mechanics ;
   https://www.thumbsticks.com/gdc-17-breath-of-the-wild-science-lies/)
2. **Immersive sims confirm the pattern at genre scale:** consistent systemic rules over *typed* objects +
   a broad verb set produce "emergent gameplay beyond what has been explicitly designed," explicitly
   avoiding scripted one-offs (Deus Ex/Dishonored/Prey). (https://en.wikipedia.org/wiki/Immersive_sim)
3. **Measurement-theory caveat — the real risk.** An ordinal scale licenses ranking, order, median, and
   `>`/`<` comparison but *not* addition/mean or meaningful distances: "the real difference between ranks
   1 and 2 … may be more or less than the difference between ranks 5 and 6." Mapping `none…extreme` →
   fixed numbers and doing arithmetic/Euclidean "distance" silently *promotes* ordinal data to interval,
   which Stevens' framework says isn't strictly valid. (https://en.wikipedia.org/wiki/Level_of_measurement)
4. **Resolution of the tension:** fixing the numbers is a legitimate *designer choice* (you assert an
   interval scale by fiat and tune it by playtest feel) — but treat the numbers as *tunable
   ordering/relations, not measurements*, and never claim the gaps are "real." Decide outcomes from rank
   *relations across material × tool × operation* (e.g. `tool_hardness exceeds material_hardness by ≥2
   levels`), not one global threshold — that's what kills bland ties and threshold cliffs.
5. **Keep 7 levels, not 3:** more rungs give more distinct relational results and push ties/cliffs apart;
   ~25 materials × ~20 ops easily absorbs 7 levels without degeneracy.
6. **Resolver should compare *gaps*, not pass/fail:** rank-gap magnitude (how far over/under requirement)
   lets you grade outcomes (partial / slow / clean / overkill) instead of a binary cliff — the analogue of
   BotW's graded interactions, and it directly feeds the DR-09 redirect metric below.

### Findings — DR-09 (nearest-operation redirect)

7. **Affordance theory frames the problem.** Gibson: affordances are *relational*, existing in the fit
   between object and the actor's capabilities. Norman adds *signifiers* — perceptible cues that
   *communicate* which affordances exist ("affordances determine what actions are possible, signifiers
   communicate where/that the action should take place"). The redirect is literally a signifier for a real
   affordance. (https://en.wikipedia.org/wiki/Affordance)
8. **Parser-IF names the exact failure being avoided.** Emily Short: the bare command prompt "*is a lie*"
   — it implies any input works; "guess the verb" is the canonical novice wall. The fix is to *separate
   discovering what's possible from solving the puzzle*: reveal that a verb exists without revealing
   *when/how* to apply it. (https://emshort.blog/2010/06/07/so-do-we-need-this-parser-thing-anyway/ [blog])
9. **Proven low-spoiler UX from IF:** clickable/interactive nouns (Bronze, Blue Lacuna) and *noun-then-verb
   menus* that surface only verbs applicable to the selected object — Short notes this "eliminate[s]
   guess-the-verb while still preserving puzzle difficulty, since knowing a verb exists differs from
   knowing *when* to apply it." That sentence is the design north star.
   (https://emshort.blog/2010/06/07/so-do-we-need-this-parser-thing-anyway/ [blog])
10. **Graceful failure should *teach the verb set*, not just say "you can't do that"** — a failed action is
    the best moment to surface adjacent affordances (the IF/im-sim "every dead-end teaches the system"
    ethic). (https://en.wikipedia.org/wiki/Immersive_sim)
11. **Precondition-gap ranking has direct precedent.** The CAPE method formats *precondition-error* info
    into a corrective suggestion and ranks actions by how close they are to satisfiable (fewest/smallest
    unmet preconditions) — exactly the "nearest operations" selector, showing precondition-gap ranking is
    a recognized technique. (https://arxiv.org/html/2211.09935v3)

### Concrete ranking recipe for "nearest operations"

1. Enumerate operations whose target *type* matches the object; discard zero-overlap ops (avoid nonsense).
2. For each, compute an **unmet-precondition gap** = sum of rank-distances on the conditions that currently
   fail (reuse the DR-04 gap metric).
3. Sort ascending by gap; **tie-break by preferring the same target object** the player just acted on
   (locality = relevance, matching Gibson's actor-object relation).
4. **Cap at 2–3** suggestions (avoid "lawnmowering" / choice paralysis; IF and UX both favour a short
   signifier set).
5. **Name the VERB, not the solution:** *"You could burn, pry, or wet this"* — never the missing material,
   the threshold value, or the sequence. This is Short's "verb exists ≠ when to apply it," preserving the
   puzzle.

### Verdicts

- **DR-04 → IMPROVE.** Discrete/ordinal is demonstrably expressive enough (BotW + im-sims), but stop
  treating the fixed numbers as arithmetically "true": drive outcomes from cross-factor rank *relations*
  and *graded gaps*, and keep 7 levels. Confidence **80 → 85** (expressiveness strongly confirmed; small
  deduction for the arithmetic-validity caveat to engineer around).
- **DR-09 → CONFIRM.** Precondition-gap ranking + same-target preference + 2–3 cap + name-the-verb-not-the-
  solution is well-supported by affordance theory, parser-IF practice, and precondition-error correction
  research. Confidence **80 → 88** (multiple independent traditions converge on this exact recipe).

*Source flags: emshort.blog is an expert-practitioner blog; Wikipedia pages used for definitional/consensus
claims; CAPE is an arXiv preprint; BotW claims rest on second-hand GDC-2017 coverage (the primary "Change
and Constant" talk is GDC-Vault video, not directly fetchable).*

---

## Summary table

| Decision | Question | Verdict | Recommended change | Confidence delta |
|---|---|---|---|---|
| **DR-05** | Operation model: DSL vs Python vs hybrid | **CONFIRM + IMPROVE** | Keep hybrid + "plain-functions-first." Make the DSL *internal* (Python data/decorators); cap it at the STRIPS boundary using PDDL's escalation ladder as the written exclusion list; ship a deterministic specificity dispatcher with `force_first/last/replace/disable` overrides from day one (the I7 leaky-precedence lesson). | **+6 to +9** (65 → ~71–74) |
| **DR-11** | Can conservation close, with an environment sink? | **CONFIRM + IMPROVE** | Keep per-channel ledger + accountable sink (= control-volume method). Conserve mass with real, *integer/quantized* kg-units (bit-exact, no float leak); make the sink strictly monotonic/absorb-only (kills qualitative ambiguity); treat **energy as a gate or a real-Joule budget, never an ordinal balance**; keep ordinals for intensive properties/landmarks only. | **+7** (70 → ~77–80) |
| **DR-04** | Are ordinal material properties expressive enough? | **IMPROVE** | Discrete/ordinal is enough (BotW/im-sim evidence). Keep 7 levels; drive outcomes from cross-factor rank *relations* + graded *gaps*, not single thresholds; treat the fixed numbers as tunable orderings, not measurements (Stevens caveat). | **+5** (80 → 85) |
| **DR-09** | "Nearest operations" redirect quality | **CONFIRM** | Rank candidates by smallest unmet-precondition gap; tie-break to the same target object; cap at 2–3; **name the verb, not the solution** (Emily Short: "verb exists ≠ when to apply it"). | **+8** (80 → 88) |

**Net:** all four design bets survive the research. Two are confirmed-and-improved (DR-05, DR-11), one is
improved (DR-04), one is confirmed and strengthened (DR-09). None is challenged at "rework the design."
The residual risks are now narrow and buildable: the DR-05 deterministic-precedence layer, the DR-11
energy-channel fidelity choice (gate vs. Joules), and the DR-04 "relations/gaps, not thresholds" resolver
discipline — each a *prove-it-in-the-slice* item, not a redesign.
