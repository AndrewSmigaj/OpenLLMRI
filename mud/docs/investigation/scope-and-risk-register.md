# Scope & risk register

> **Update (decision):** runtime LLM removed (deterministic runtime, all interactions pre-built; LLM =
> build-time authoring only — `GDD.md` §0a). This **retires risk #9** (soft-adjudication cache leaks)
> and the runtime-LLM latency/mis-parse concerns. Risks #1 (quality), #2 (global softlock), #3
> (conservation ledger), #4 (density/scope), #5 (plausible-but-wrong values), #6 (dominant strategy),
> #7 (clock liveness), #8 (co-op), #11–15 all **still stand** — they're about authoring, content
> quality, Evennia, and solvability, none of which depended on runtime LLM. The make-or-break (risk #1,
> quality/fun) is unchanged.

Converts the lens findings into (1) a **buildable scope** (the vertical slice; what to cut) and (2) a
**risk register**. The certainty numbers (`certainty-assessment.md`) are "at this scope, with these
mitigations" — this file *is* that scope and those mitigations.

---

## Part 1 — The vertical slice (build this; prove the fun before anything else)

**Premise:** the make-or-break is whether *derived, validated* content feels *alive* (Convergence-1).
Build the smallest thing that tests that, and nothing else.

### In scope
| Area | Slice target |
|------|--------------|
| Players | **Single-player.** No multiplayer, no co-op, no shared clock. |
| Space | **One room** (cabin interior). **No perception zones, no direction, no sound propagation.** |
| Objects | **~5:** the aircraft seat (deep showcase), a multitool, fire-makings (tinder/fuel/lighter), the cockpit radio (the one authored special), the scripted pilot. |
| Materials | **~25 ordinal property vectors — hand-curated golden table** (not generated; this is the quality anchor). |
| Operations | **~15 declarative ops:** examine, cut, tear, pry, unbolt, bend, tie, wrap, wear, heat, dry, ignite, burn, extinguish, combine. |
| Action pipeline | Stage-A intent parse (deterministic + LLM fallback) → affordances-from-state → **informative redirect** → Stage-B pure resolve. |
| LLM | Local OSS-20B for intent + prose; **resolve-then-crystallize** loop + **wall-sensor** log; cached + clamped. |
| Invariants | **The conservation ledger (AR15)** + a closed model with an **environment sink (AR11)** — the flagship runtime assertion. |
| Quality | **~50 hand-authored "signature" responses** (the opening minute, the key failures incl. the windbreak) — curated, not derived. |
| Instruments | operation×material **matrix property tests** + the **`solvability-fuzz`** harness (seeded). |
| Rescue | a **stub**: the radio path only (power → antenna → contact), enough to have a goal. |

### Explicitly CUT for the slice (retire the §46 numbers)
- §46 density (60–100 primary, 300–800 derived, ≥50 attempts/object, **700+ tests**) → replaced by
  "the matrix + fuzz + golden set." **IM5 rated §46-as-written RED (person-months).**
- §9 multiplayer tick/clock modes, §10–15 perception/zones/sound, §8 weather arc, §39 full rescue
  routes, the auto-generated story, multiplayer/instancing. **All deferred until the slice proves fun.**

### The slice's single success test
> A new player, given no manual, spends 15 minutes in the cabin trying sensible, desperate, and silly
> things — and **comes away saying the world felt alive and reactive**, with **zero** "you can't do
> that," and at least one *delighted* "I can't believe that worked / that it told me *why* it didn't."

If that lands → green-light the layered build (proposal §10 steps 2–7). If it falls flat → the bet is
wrong and the depth is tedium; rethink before building perception/multiplayer.

---

## Part 2 — Risk register

Severity × Likelihood are for the **full vision**; the **mitigation/instrument** column is what de-risks
each, and most are exercised by the slice.

| # | Risk | Sev | Lik | Mitigation / instrument | Lens · status |
|---|------|-----|-----|--------------------------|---------------|
| 1 | **Derived content is dry, not delightful** (the quality gap — automation can't catch it) | High | Med | Curated golden set (materials + ~50 signature responses); **human playtest as a first-class gate**; opening/failure prose authored not derived | GD2/GD25/IM3 · Conv-1 · **the make-or-break** |
| 2 | **Global softlock** — rescue routes share warmth/fire/stamina, so total warmth failure kills all routes | High | Med | No-materials **warmth floor**; make routes draw on **distinct** scarce resources; **degradation-over-hard-loss**; `solvability-fuzz` standing oracle | AR6/GD7/Probe-3 · Conv-2 |
| 3 | **Conservation unenforced** — it's a doc line, not a runtime check; model doesn't close | High | High | Close model with an **environment sink (AR11)**; ship the **per-transform conservation ledger (AR15)** as the flagship invariant + property test | AR15(**RED**)/AR11 · Conv-4 |
| 4 | **§46 density unauthorable** — months of curation | High | High | **Cut to the vertical slice**; bounded coverage = matrix + fuzz; cheap-objects inversion | IM5(RED→YELLOW) · resolved by scope |
| 5 | **Plausible-but-wrong ordinal values** pass every automated gate | Med | High | Hand-curated **golden material table**; measured generation pilot (track repair rate); sampled human review | IM3/IM12 · Conv-1 |
| 6 | **Stay-and-signal dominant strategy** collapses path choice into a checklist | Med | Med | Rescue methods compete for **distinct** resources; make travel pay off *sometimes* | GD7 · Conv-2 |
| 7 | **Event-driven clock hangs** a doomed-but-alive idle party | Med | Med | **Clock-liveness rule**: time advances / game offers resolution when stuck | AR6 · Conv-2 (self-inflicted) |
| 8 | **Co-op is parallel labour**, not shared fun | Med | Med | Design **≥1 first-class interdependence** (hold antenna / relay scout's landmark while another transmits) | GD16 · Conv-5 |
| 9 | **Soft-adjudication cache leaks** (nondeterministic replays) | Med | Low | Key verdicts by situation; clamp to engine ranges; cache + replay tests (AR4) | AR3/AR4 |
| 10 | **"Do-anything" wall** found by persistent players | Med | Med | Reframe to bounded matrix; make the boundary a **delightful redirect**; wall-sensor → crystallize queue | GD22 · Conv-3 (mostly resolved) |
| 11 | **Activity progress lost on `@reload`** (Evennia) | Low | Med | Persist activities to Attributes, **not `.ndb`**; reload test | IM9 · Conv-5 |
| 12 | **No LLM per-turn call/token/GPU budget** set | Low | Med | State a budget; deterministic timeout fallback; cache hit-rate target | AR9 · Conv-5 |
| 13 | **Premature-abstraction bloat** — 9 validators / DSL before content | Low | Med | Build the slice's content first; add validators as invariants prove needed | AR13/AR16 |
| 14 | **Evennia primary NL parser** fights the matcher | Low | Low | One dominant `Command.parse()` / custom `COMMAND_PARSER` | IM1 · managed |
| 15 | **Concurrency ceiling** (~low-hundreds) | Low | Low | Instanced runs keep per-instance population tiny; `.ndb`/lazy traits avoid per-tick DB writes | IM1/IM9 |

### The three that must be addressed before/with the slice
- **#3 (conservation ledger)** — the lone RED; the slice's flagship invariant.
- **#1 (quality)** — the slice exists to test it; without curation + playtest there is no answer.
- **#2 (global softlock)** — fold the warmth-floor + distinct-resources + clock-liveness into the
  design now, and stand up the fuzz harness with the slice.

Everything else is a known, scoped fix to schedule into the layered build.
