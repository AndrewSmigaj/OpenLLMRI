# Power-ups & the Claude-Code-assisted build

Two things the user asked for in the polish pass: (1) **what makes the interaction logic more
powerful** (refined by the lens review), and (2) **how this looks built *with* Claude Code** — the
sane skill set + loop, not bloat. Plus the concrete **new invariants** the review says must become
enforced gates.

---

## Part 1 — Interaction-logic power-ups (refined by the review)

Beyond the proposal's core (operation×material engine, two-stage actions, three resolution modes,
resolve-then-crystallize), the lens pass surfaced these upgrades:

1. **The conservation ledger is the power-up, not a chore (AR15/AR11).** Making conservation a
   *runtime* assertion with an explicit **environment sink** is what turns "objects interact" into
   "objects interact *trustably*." It is the difference between approximate physics that drifts and a
   world players can *reason about* — which is the whole pitch. Build it first; it makes every later
   interaction free to trust.

2. **Name the expressiveness honestly: the operation × material matrix.** "Everything" = "every
   physical operation applicable to these materials in this state." That's bounded *and large* (a
   ~500-cell matrix yields tens of thousands of object×object interactions, à la ScienceWorld's 25
   actions → 200k pairs). Design and market to *that*, and the "wall" becomes a **delightful
   redirect** ("you can't dissolve it, but you could cut, burn, or pry it") instead of a hidden cage
   (GD22).

3. **Two extension paths, kept distinct.** *Composition* (new combinations of existing operations) is
   handled at runtime by **crystallize** — cheap, automatic, validated. *New primitives* (a genuinely
   novel verb the matrix can't express) are an **authoring event** with a human in the loop, surfaced
   by the **wall-sensor** queue. Conflating them is the trap; separating them makes the system both
   safe and growable.

4. **Affordances computed from state → intent parsed against them (Versu/Jericho lesson).** The parser
   doesn't guess in a vacuum; it matches intent to the operations *actually possible* on what's
   reachable, then redirects to the nearest possible ones. This is what makes "try anything" *legible*
   (GD20/GD21) instead of a slot machine.

5. **Knowledge / uncertainty as a first-class mechanic (reinforced).** Track *believed* vs *true* (is
   the water safe? is the beacon transmitting? which way is the road?). It is the richest unmined vein
   in the design, the ideal text+LLM surface, and it multiplies the interaction space without new
   objects — a pure power-up.

6. **Distinct-resource rescue routes + the warmth floor (solvability power-up, Conv-2).** Making each
   rescue method draw on *different* scarce resources is not just anti-softlock plumbing — it is what
   makes the strategic choice between routes *real* (GD7), which is where the replay value lives.

7. **First-class cooperative interdependence (GD16).** One designed dependency — hold the antenna /
   relay the scout's landmark while another transmits — converts co-op from parallel solitaire into a
   shared-story engine. One is enough to change the texture.

8. **The run's auto-generated retrospective story (GD24).** Summarizing the deterministic event log
   into an ending narrative *captures* the emergent play the engine produces — it is the payoff that
   makes a systemic survival run *memorable*, and it is almost free (the log already exists).

## Part 2 — The new invariants to enforce (the review's "enforced outcomes")

Findings that imply invariants → these become `make validate` rules and/or property tests (hand to
`sim-test-writer`). This is how the review yields enforcement, not just prose:

| Invariant (new) | Kind | From |
|-----------------|------|------|
| **Per-transform conservation ledger** — post-state balances pre-state on material/mass(±sink)/contamination/heat/provenance/length-count, else reject | runtime assert + property test | AR15/AR11 |
| **Narration↔Effect**: no narrated state change without a backing Effect | runtime assert | AR15/§41 |
| **Rescue-confidence monotonic** under additive evidence; **rescue always reachable** from any live state | property + fuzz oracle | AR6/Q3 |
| **Every attempt resolves** (0 generic-dead-ends across the fuzz corpus) | fuzz oracle | GD25/IM10 |
| **Soft-adjudication determinism**: same situation key → same clamped verdict on replay | property test | AR3/AR4 |
| **Clock liveness**: time advances or resolution is offered when a party is stuck/idle | runtime rule | AR6 |
| **Warmth floor**: a no-materials survival path exists from any non-terminal state | design invariant + fuzz check | Conv-2/Probe-3 |
| **Activity durability**: in-progress activities survive `@reload` (persisted, not `.ndb`) | integration test | IM9 |

## Part 3 — Building it *with* Claude Code (the sane loop)

The skills are in place; here is how they compose into an authoring loop that is instrumented but not
bloated.

### The skill set (each earns its place)
- **`/lenses`** (built) — design-level pressure-testing; produced this whole review.
- **`ontology-generator`** (built) — the LLM-at-the-authoring-edge: generate materials/operations/
  cheap objects, generate-then-validate.
- **`solvability-fuzz`** (built) — the standing softlock + unresolved-attempt oracle.
- **`whiteout-world-builder`** (upgraded) — authoring agent, now operation-first, wired to the
  generator + validator.
- **`engine-reviewer`** (exists) — guards the functional-core boundary, conservation, LLM placement.
- **`sim-test-writer`** (exists) — turns invariants into property tests.

### The loop (one focused pass per turn — `/loop`-friendly)
```
Anchor   → re-read VISION + the GDD + roadmap pass (what am I building?)
Generate → ontology-generator drafts content (qualitative, schema-bound)
Validate → make validate + the conservation ledger (the hard gate)
Fuzz     → solvability-fuzz: 0 unresolved, rescue reachable, no global softlock
Sense    → read the wall-sensor log (attempts that hit redirect)
Crystallize → propose missing operation×material rules from the log; validate; promote
Curate   → HUMAN: golden material values + signature responses (quality — automation can't)
Playtest → HUMAN: is it alive and fun? (the only Q2 instrument)
```
Automate the left half (resolution/conservation/solvability); **a human owns the right half**
(quality/fun/intent). That boundary is the "sane" part — the AI builds the world that *runs*; the
human certifies the world that *delights*.

### Drift control (IM12)
Every loop must pass the **validator + the conservation ledger + the fuzz oracle**, and is anchored to
**VISION.md** + the GDD. Long autonomous runs can't drift shallow (validator rejects unresolved/
unconserved) or off-intent (VISION + golden set are the reference). The `/lenses` skill is re-run on
the GDD and on major content batches as a periodic deeper check.

### What we deliberately did NOT build (sane, not bloat)
- No speculative validators/DSL before there is content to stress them (AR13) — invariants are added
  as the review proves them needed (Part 2), not pre-emptively.
- No per-object packet tooling — the cheap-object/operation inversion makes it unnecessary.
- No multiplayer/perception/clock tooling yet — those wait until the vertical slice proves fun.
- Lenses are **triaged**, not all-applied-equally — effort follows leverage.

### The one-line build doctrine
> **Automate what can be *proven* (resolution, conservation, solvability); curate what can only be
> *judged* (quality, fun, intent). Build the single-player vertical slice first, and let the playtest —
> not the validator — decide whether the world is alive.**
