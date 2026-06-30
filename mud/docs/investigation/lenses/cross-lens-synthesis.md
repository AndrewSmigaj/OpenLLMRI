# Cross-lens synthesis — where the lenses converge and conflict

The most useful output of the lens pass is not the 54 cards; it is where independent lenses (and the
three probes) **point at the same seam** or **disagree**. Each seam is a place where an *unbounded
promise meets a bounded mechanism*. Sources: `game-design.md`, `architecture.md`, `implementation.md`,
and `../probes/*`.

Headline verdict count: **1 RED (AR15), ~30 YELLOW, ~20 GREEN, 0 existential.** The proposal pulled
every would-be-RED off the wall; almost everything HIGH sits at YELLOW because **the fixes are
designed, not proven.** That is the honest state: a sound design whose load-bearing bets are
unverified.

---

## Convergence 1 — THE central thread: "resolves + conserves" ≠ "is good" (the quality gap)
**Lenses that independently land here:** GD2, GD13, GD22, GD25 (does generic-derived text read as
*witty/specific*?) · IM3, IM12 (plausible-but-wrong ordinal values; shallow crystallized rules) ·
AR16 (the material matrix is the new silent-default surface) · Probe-1 (the Toy/voice rest on prose
quality) · Probe-2 (validation caught 6 issues but **cannot** catch a mis-valued material).

**The seam:** every automated gate the design has — `make validate`, the conservation ledger, the
fuzz oracle — proves an action **resolves**, **conserves**, and **doesn't softlock**. **None of them
proves it is *good*:** that the response is specific and witty rather than dry-but-valid, that an
ordinal `cut_resistance: med` is *correct*, that a crystallized rule is *interesting*. Valid-but-dull
mush passes every check and surfaces only in human play.

**Why it matters most:** the entire promise — "understand a living world", the §3.5 windbreak magic —
is a **quality** claim, and quality is exactly what the automation can't certify. The fuzz harness can
run 10k attempts and prove 0 unresolved; it cannot tell you the world is *delightful*.

**Implication (carry to GDD):** quality needs its own instrument — a **curated golden set** (hand-
authored material values + ~50 hand-graded "signature" responses for the opening + key failures) and
**human playtest as a first-class gate**, not an afterthought. The opening minutes and the failure
voice must be **authored, not derived** (Probe-1). Automate *resolution*; curate *delight*.

## Convergence 2 — rescue routes are NOT resource-independent → global softlock + dominant strategy
**Lenses/probes:** AR6 (a single shared resource under all routes) · GD7 (stay-and-signal dominates;
additive confidence collapses choice into a checklist) · Probe-3 Walk-3 (the WARMTH/FIRE bottleneck
gates every route) — three independent paths to the *same* finding.

**The seam:** the design wants **non-exclusive additive rescue routes** (§7, §39) AND **scarce shared
resources** (§24). But the routes all bottleneck on **warmth/fire → stamina → working hands**, so they
are not actually independent. Two failure modes fall out:
- **Global softlock (AR6/Probe-3):** total warmth failure on a cold night kills every route at once —
  invisible to the per-fact ≥3-paths rule.
- **Dominant strategy (GD7):** because confidence is additive and routes share inputs, "stay and do
  *all* the cheap signals" strictly beats "travel" (which spends the same warmth/stamina to *leave*
  the search area). Path-choice collapses into a do-everything checklist.

**New, self-inflicted softlock (AR6):** the proposal's own **event-driven clock can hang a
doomed-but-alive party** — no action → no time → neither death nor rescue. The §9 heartbeat couldn't
produce this; my fix introduced it.

**Implications (carry to GDD):**
1. **Warmth floor** — a no-materials survival path (huddle + fuselage + body heat) so fire-failure is
   recoverable (Probe-3).
2. **Make rescue methods compete for *distinct* scarce resources**, not all warmth — so routes are
   genuinely independent and travel can dominate *sometimes* (fixes GD7 + AR6-route-independence).
3. **Clock liveness rule** — time must advance (or the game must offer resolution) when a party is
   stuck/idle, so the event-driven clock can't hang.
4. **Degradation-over-hard-loss** for every "only" resource/tool.

## Conflict 3 — "feel boundless" (GD12/GD22) ✕ "density is unaffordable" (AR5/IM5) ✕ the crystallize bridge
**The disagreement:** the game-design lenses want no wall (GD22) and a boundless feel (GD12); the
implementation/architecture lenses say full §46 density is **months** (IM5 RED) and the original
authoring model doesn't scale (AR16).

**How the proposal adjudicates it (and the lenses mostly agree):** the **operation×material inversion**
is judged **GREEN by AR5 + AR8** — it makes density a config problem, not a rewrite, and shrinks the
consistency surface ~20× (IM3). The **redirect + resolve-then-crystallize** loop handles the wall.
**So the conflict is ~80% resolved by the proposal.** The residual 20% the lenses flag:
- **Crystallize can't mint new primitives** (confined to existing operations, §3.6) — so the cage is
  real, just well-hidden; a genuinely novel verb still hits a (graceful) redirect (GD22).
- **The wall-sensor "maps the cage" over a session** — persistent players will find the edges.
- **Quality of crystallized content** is unverifiable (Convergence 1 again).

**Implication:** accept a *bounded* "everything" — the **operation × material matrix is the honest
definition of the world's expressiveness** (IM6); market and design to that, and make the boundary a
*delightful redirect*, not a hidden wall. "Everything you can express as these physical operations on
these materials" is both true and large.

## Convergence 4 — conservation must be a RUNTIME ledger, and the model must close first
**Lenses:** AR15 (the lone RED) — conservation is a doc line / authoring-time check, never enforced at
commit · AR11 — the model doesn't *close*: §24 conservation is "approximate", **no environment mass/
energy sink**, so burn/melt/boil/dry can't balance; cross-object heat/contamination transfer and
partial-transform ownership are underspecified. **AR15 depends on AR11** — you can't assert what you
can't express.

**The seam:** "no prose-only state change / conservation holds" (§24, §41) is the design's structural
guarantee, but it lives in prose. The good news: **this is the most fixable finding** — it has a
concrete remedy:
- Close the model (AR11): add an **environment sink** (heat/smoke/mass leave to "the world"), define
  cross-object heat/contamination transfer and partial-transform ownership.
- Enforce it (AR15): a **per-transform conservation ledger** — before any Effect-set commits, assert
  the post-state balances the pre-state on material identity, mass (within tolerance vs the sink),
  contamination/heat, provenance, and separated length/count sums — else reject the transform.

**Implication:** this becomes the project's flagship **runtime invariant + property test** (hand it to
`sim-test-writer`), and the single most important thing to build right in the vertical slice.

## Convergence 5 — co-op is parallel labour, and a couple of operational residuals
**Lenses:** GD16 (co-op is currently chore-splitting; the one real interdependence — cross-zone
scout→radio relay, §15+§38.8 — is left emergent/unspecified) · IM9 (instanced runs resolve the
persistence fork, but **activity progress must survive `@reload`**, not live on `.ndb`; instance
garbage-collection unspecified) · AR3 (stale-snapshot / cached-verdict divergence at the timed-action
seam) · AR9 (async LLM seam solved, but **no per-turn call/token/GPU budget** set).

**Implication:** design **at least one first-class interdependence** (one holds the antenna / relays
the scout's landmark while another transmits) so co-op is a story engine, not solitaire; and close the
small operational gaps (reload-durable activities, instance GC, a stated LLM-call budget) in the slice.

---

## Where the lenses agree it is STRONG (protect these)
- **GD8 Triangularity (GREEN):** multiple genuine risk/reward axes (fuel ignition, fuselage-fire CO,
  beacon-as-antenna §38.3). The scarcity+conservation spine is excellent.
- **AR1 / AR5 / AR8 (GREEN):** functional-core split + operation×material engine = density and new
  expressive power are *config, not rewrite*.
- **AR12 / IM6 / IM10 (GREEN):** invariants + a bounded coverage definition + a front-loaded fuzz
  oracle is a genuinely sound correctness strategy.
- **IM1 (GREEN):** Evennia carries it; `contrib.rpg.llm` is a copyable async seam; only the primary NL
  parser is against-the-grain (managed).
- **AR7 (GREEN):** the wall-sensor gives both a boundary detector and a debug trace.

## The three load-bearing UNPROVEN bets (what the whole thing rests on)
1. **Quality bet:** generic, derived, validated content reads as *specific and witty* (Convergence 1).
   *Only a playtest can settle this.* → the vertical slice exists to test exactly this.
2. **Independence bet:** rescue routes can be made to draw on *distinct* scarce resources so choice is
   real and global softlock is avoidable (Convergence 2).
3. **Closure bet:** the data model can be closed (environment sink) and conservation enforced as a
   runtime ledger without crippling expressiveness (Convergence 4).

Bet 1 is the make-or-break and is **empirical** — which is exactly why the proposal's vertical-slice-
first build order is the right risk-retirement move. Bets 2 and 3 are **design fixes with known
remedies**, listed above, to fold into the GDD.
