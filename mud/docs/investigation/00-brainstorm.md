# Brainstorm — critical + creative re-read of the Whiteout design

Working notes, not a verdict. Reading `docs/scenarios/whiteout/design.md` (§1–49) with a
critical and creative eye, oriented to the user's stated goal: *a text world where as much
as possible can be done with everything, using LLMs to flesh out the ontology, one
data-dense scene, rescue conditions wired.*

Cross-refs use design §N and lens IDs (GD#/AR#/IM#, see `lenses/triage.md`).

---

## 0. One-paragraph take
The design's instincts are excellent and its spine — *the world is the puzzle; every attempt
resolves; understand-don't-guess* — is exactly right for the goal. Its weaknesses are an AI-spec
signature: it is **comprehensive instead of prioritized**, it **prescribes the expensive path as
the default** (deep authored packets), and it **under-resolves the three hardest tradeoffs**
(the multiplayer clock, the LLM↔determinism seam, and how "everything" survives a bounded
mechanism). The single highest-value reframe: treat the **~20 operation categories over a rich
material model (§5/§21/§24) as the actual engine**, and treat authored object-packets (§43) as
the *exception*, not the default — then make the LLM the bridge between unbounded intent and that
bounded physics, with a **resolve-then-crystallize loop** so play *is* authoring.

---

## 1. What's genuinely strong (keep, protect)
- **Resolution-not-success (§3.5, §25, GD25).** "You hold the shirt to the flame… it flaps too
  wildly… if you stretched it between branches it might work." This single example is the whole
  game's voice. Protect it as a hard invariant: no `You can't do that.` ever ships.
- **Perception ≠ reachability ≠ audibility ≠ direction (§10–15).** Genuinely novel for text. The
  best idea in the doc. It makes the world feel *physical* and is a perfect LLM-prose surface.
- **Conservation as first-class (§24).** Mass/temperature/wetness/contamination/provenance
  surviving transforms is what makes derived objects (§23) trustworthy and long chains possible.
  This is the structural backbone that lets "everything interacts" be coherent rather than ad hoc.
- **Multiplicity to avoid softlock (§39, §44): ≥3 solution paths / ≥3 clue paths.** Right
  instinct. (But see §6 below — it's per-*fact*, not per-*world-state*.)
- **Model-deep, requirement-light (§4).** The correct philosophy. The doc just then contradicts
  it operationally (see §3).

## 2. The central tension (and the resolution)
Three scaling models are in the doc and it never commits:
- **(a) Deep authored objects** — §22 parts/attachments, §43 packets, §46 density targets
  (60–100 primary + 300–800 derived, ≥50 attempts/object, 700+ tests). Does **not** scale; this
  is months of curation (IM5).
- **(b) Composable physics** — §5's ~20 operation categories over §21 materials + §24
  conservation. **Does** scale: rich materials × operations → object combinatorics for free.
- **(c) LLM-generated content** — §41's "draft templates / generate tests / brainstorm attempts."

**Resolution:** make (b) the engine, (a) the rare exception (radio/beacon/pilot only), and (c)
the *runtime* bridge between player intent and (b). A "seat" is a few part+material tags; ~90%
of its affordances *derive* from material properties; the LLM maps weird verbs → operation
compositions; the engine adjudicates feasibility from properties. This is the only configuration
where "everything with everything" is affordable. (GD12 ✕ AR5/IM5; GD22.)

## 3. The authoring-cost contradiction (the biggest practical problem)
§4 says "model everything plausible, require only core blockers," but §43 prescribes a ~60-line
YAML packet *per object* with parts, attachments, transformations, survival/non-survival uses,
failure modes, and tests, and §46 asks for hundreds of them. **You cannot have both** a
do-anything density target and a heavy per-object authoring path. Fixes:
- **Cheap-by-default objects:** an object = `{materials, parts?, size, mass, a few tags}`. Its
  affordances/failures are *derived* from material+operation rules, not authored.
- **Packets only for puzzle-critical objects** (radio, beacon, pilot, the one deep seat as a
  showcase). Everything else rides the generic physics.
- **Coverage is not enumeration (IM6).** You can never author/verify "everything." Redefine the
  target as: the bounded **operation × material matrix** is complete and tested, plus a fuzz
  sample of object×object attempts resolve. That is a *finite, checkable* definition of "done."

## 4. The interaction logic — how to make it *more powerful* (Q5)
§25's action model (`actor + action + target + tool + method + desired_result + time_budget`) and
§26's resolution tiers are good but can be much stronger:
- **Two-stage, LLM out of the core (already in our architecture).** Stage A: text → structured
  `ActionAttempt` (deterministic first; LLM fallback for odd phrasing). Stage B: pure resolver.
  Keep §26's "LLM tier" *out* of Stage B (it would destroy determinism + testability; GD21/AR4).
- **Reframe §26 around operations, not objects.** Tiers should be: authored-special → object-rule
  → **operation×material rule** (the workhorse) → generic-physics → informative-failure. Most
  resolution should happen at the operation×material tier, which is *generated/tunable*, not
  hand-written per object.
- **Add a third resolution mode: the constrained LLM judge (the missing middle).** §41 is binary
  (engine owns everything / LLM only prose). Reality has a huge middle of *soft adjudications*:
  "does this improvised contraption count as a windbreak ≥ 0.5? does this plea move morale?"
  Authoring each deterministically is infeasible; the right design is **the LLM returns a bounded
  verdict inside engine-defined rails, the engine clamps and records it, and the verdict is
  cached** so replay is deterministic (preserves §41's no-contradiction; AR3/AR4/AR15).
  → Three resolution modes: **hard mechanics** (engine, LLM never) · **soft adjudication**
  (LLM-judge-on-rails + clamp + cache) · **pure prose** (LLM free).
- **Resolve-then-crystallize (the headline idea).** §28 makes "brainstorm 50+ attempts/object" an
  *authoring* task — wrong time. Do it at **runtime**: unhandled attempt → LLM proposes a
  resolution constrained to operations + that object's material/part state → engine checks
  feasibility → resolves live → **logged and promoted to a deterministic rule** (optionally
  human-reviewed). Play becomes authoring; the ontology fleshes itself out through use. This is
  the strongest single answer to both "do anything" (GD22) and "LLM fleshes the ontology" (IM3).

## 5. The multiplayer clock (§9) — the riskiest subsystem, and the doc starts with it
The "10–20 real-seconds = 1 game-minute" global heartbeat + planning/live/fast-forward modes is
the most complex and least-fun-to-validate system (GD18/GD4), and §42 builds it *first*.
- **The wait problem:** a 90-game-minute shelter build = 15–30 real minutes; fast-forward needs
  *all* players idle/busy (§9.6), so one AFK player blocks everyone, or the active player waits in
  real time. §9.1 explicitly wants to avoid "losing daylight while reading room text," but the
  wall-clock coupling reintroduces exactly that.
- **Suggestion:** decouple *time pressure* from *wall-clock waiting*. Prefer an **event-driven
  clock that advances only when someone acts** (no idle drain), heavy compression, and
  *consensual* fast-forward. Or a turn/segment model. Whatever the choice, **prototype this first
  and be willing to redesign it** — it underpins everything and is the most likely to feel bad.
- **Session-model fork (unspecified, decides five other things; IM9):** persistent shard vs
  **instanced co-op runs**. The whole arc is "day 1" of a worsening storm ending in
  rescue/escape/collapse — that *screams* instanced runs of ~one in-game day. Committing to
  instanced runs simplifies the clock, persistence, logging-off mid-survival, and griefing
  (§27's sabotage/theft/cannibalism is fine among invited friends, fraught with strangers; AR10).
  **Recommend: instanced co-op runs, ~1 in-game day per run.**

## 6. Softlock: the ≥3-paths rule is necessary but not sufficient (AR6, Q3)
§44 enforces ≥3 paths *per critical fact*. But emergent **global** softlock is uncovered: the
group burns the only long-metal antenna material *and* spends all fuel *and* the pilot dies before
any clue path fired *and* everyone is hypothermic. No single fact is unreachable; the *world state*
is. The per-fact rule can't see this.
- **Fix:** an explicit **resource-exhaustion / world-state reachability** analysis, plus a
  **seeded fuzz harness** (IM10) that actually *drives* runs and flags dead-ends. This is the only
  way to give calibrated confidence on "smart players can always progress." Also: prefer
  *degradation over hard loss* (a burned antenna lead leaves a worse-but-usable stub; design §38.3
  already hints at "poor temporary conductor") so irreversibility rarely produces a true wall.

## 7. The LLM↔determinism seam — trust is the hidden requirement (GD21, AR3/AR4)
- A **silent Stage-A mis-parse** that does the wrong thing is worse than a clean "I didn't
  understand." Design needs an **intent-confirmation affordance** for low-confidence parses
  ("You try to *pry* the panel with the knife — yes?") rather than guessing.
- **Narration must never imply unmade state.** §41 forbids it; make it a **runtime assertion**
  (AR15): the narrator may only reference facts present in the post-Effect state. Prose that
  mentions a change with no backing Effect is a test failure, not a style note.
- **Determinism with an LLM in the loop** requires: seeded RNG, cached intent parses + cached
  soft-adjudication verdicts keyed by situation, and a deterministic timeout fallback so a slow
  model never stalls a turn (AR9/IM4). With those, transcripts replay identically and are testable.

## 8. Fun / pacing — depth is not enjoyment (GD4/GD10/GD18)
- **Chore audit:** 18-minute tick-saw tasks, stamina, cold-hands penalties — each must *dramatize
  desperation*, not just meter it. Tick messages (§9.4) should escalate stakes ("the wind shifts;
  your fingers won't close"), not just count minutes.
- **The Toy first (GD2):** the cabin must be fun to mess with in the first 2 minutes with zero
  rescue intent — lick the frozen latch, wear the seat cover as a cape, stack food trays. The §29
  first-minute list is the right material; the question is whether the *responses* are delightful.
- **Interest curve (GD10):** weather + pilot timer give a built-in rising curve; the danger is the
  mid-game "grind to survive the night" sag. Consider mid-run beats (a distant search plane that
  doesn't see you; the pilot's last lucid fragment) to re-spike interest.

## 9. Creative additions worth proposing
- **The run's auto-generated story (GD24).** Survival games live on the stories players retell.
  Summarize the deterministic event log into a *retrospective narrative* as the ending payoff
  (who you saved, what you burned, the cannibalism, how rescue came or didn't). Cheap, high
  emotional ROI, ideal LLM use.
- **LLM as the perception renderer (§14).** Don't hand-author degraded/directional variants —
  generate them from structured perception state. Scales infinitely; stays consistent because
  facts come from the engine.
- **Knowledge/uncertainty as a first-class mechanic.** §12 ("no longer confidently knows north")
  and §19.2/§38.8 clue-paths treat epistemics as a side-effect. Lean in: *believed* vs *true* (is
  that water safe? is the beacon actually transmitting? which way is the road?). Survival is mostly
  a knowledge game; text is the ideal medium; an LLM modeling "what this character knows" fits.
- **Invariants over enumerated tests (AR12/IM7).** Replace the 700+ enumerated tests (§46) with
  property tests on operations+materials (conservation always holds; no action softlocks; rescue
  confidence monotonic) + fuzz transcripts + a small golden set. Far fewer, far stronger.
- **A "wall sensor."** Instrument the resolver to log every attempt that fell through to
  generic-failure; that log is the prioritized authoring/crystallize queue *and* the GD22 wall
  detector.

## 10. Strategic: build order should be flipped
§42 starts with the tick engine (Pass 1) and perception (Pass 2) — the hardest systems, least able
to prove the game is fun. **Flip it: a single-room vertical slice of the ontology first** — the
cabin, ~4 objects (seat, knife, fire-makings, radio), the operation/material core, LLM
intent-parsing + crystallize, **single-player, no perception zones, no multiplayer clock.** Prove
*try-anything → resolves plausibly → feels alive* before investing in perception/multiplayer/
weather. If that core isn't magic, nothing downstream saves it; if it is, the rest is layering.

## 11. Open forks for the proposal to settle (with my lean)
1. Session model → **instanced co-op runs, ~1 in-game day.**
2. Clock → **event-driven (advance-on-action) + consensual fast-forward**, not a real-time heartbeat.
3. Runtime LLM → **resolve-then-crystallize with a deterministic fast-path + cached soft-adjudication.**
4. Build order → **vertical ontology slice first**, defer perception/multiplayer/clock.
5. Authoring model → **operation×material engine as default; packets as the exception.**
6. Coverage definition → **operation×material matrix complete + fuzz sample**, not enumerated "everything."

## 12. Seeds for the proposal (carry forward)
- The three resolution modes (hard / soft-judge-on-rails / prose) and the crystallize loop.
- The "cheap object, rich material" inversion of the authoring model.
- The wall-sensor + fuzz harness as the solvability/coverage instruments.
- Instanced runs + event-driven clock.
- Auto-generated retrospective story as the ending.
- Knowledge/uncertainty as a designed mechanic.
- Vertical-slice-first build order.
