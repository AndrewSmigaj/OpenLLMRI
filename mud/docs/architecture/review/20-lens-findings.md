# A3 — Architecture lens analysis: synthesis

Consolidates the two lens passes over `implementation-architecture.md` v1:
`20-lens-arch.md` (AR1–AR17) and `20-lens-impl.md` (IM1–IM12). Verdicts: **1 RED, ~15 YELLOW, ~13
GREEN, 0 existential** — a sound, buildable architecture with a small set of high-leverage fixes. The
two passes **converge** on the same core issues.

## Verdict at a glance
- **Strong GREENs (keep):** DR-02 no-runtime-LLM (removes the dominant Evennia hazard — a model blocking
  the single-threaded reactor) · DR-09 generic op×material rules · DR-18 invariant+fuzz testing · the
  told-format parser + single-scene+Tags (sidesteps both of the Evennia research's YELLOW areas) · IM1
  framework feasibility · AR9 latency · AR12 testability.
- **1 RED:** AR15 — conservation is documented, not *enforced* at runtime.

## The convergences (where both passes point at the same seam)

### C1 — The mutation path is convention, not enforcement (the RED) — AR15 · AR3 · AR11 · AR17 · DR-10/11
Both passes independently: "engine owns state / conservation holds / apply() is the only writer / atomic"
are **stated, not mechanized.** Evennia Attributes are directly writable, so any code *can* bypass
`apply()`; there's no transaction behind "atomic apply"; Evennia perf guidance pushes per-tick survival
state (stamina, cold) *off* the ledgered path; and the Attribute-truth → Tag-mirror (DR-07) has no
transactional sync, so DR-09 can read stale Tags.
**Fix (the single most important in the whole review):** make **`apply()` + the ledger the one
enforced, total, atomic mutation path** —
  (a) a single guarded choke-point in the shell + a lint/`engine-reviewer` rule forbidding raw
      `obj.db.x =`/`.attributes.add` outside it;
  (b) **all** state change — including tick/`systems/*` updates — expressed as **ledger-gated Effects**
      (batched per tick), so nothing escapes conservation;
  (c) wrap apply in `django.db.transaction.atomic`, updating the Attribute **and** its Tag mirror
      together.
This one fix closes AR15 (enforcement), AR11's tick-state gap, AR3's Tag sync, and AR17's torn-apply.

### C2 — Determinism is assumed, not contracted — IM10 · AR4 · DR-06/12
Seeded replay underpins the entire DR-18 solvability/coverage story, but the replay/fuzz path isn't
stated to run on the pure core, and DR-06 mints a derived object per part-removal — a place `dbid`/
`uuid`/clock nondeterminism can leak into `EntityState`.
**Fix:** make determinism an **enforced contract** — fuzz/replay run on the pure core with an in-memory
`WorldView`; **all ids and random draws come from the per-run seeded RNG**; **forbid `dbid`/`uuid`/
`datetime` in `EntityState`** (lint); guard with a **double-run-same-seed property test** + the existing
`world/sim` import-boundary test.

### C3 — "Operations as data" is the biggest bet, dressed as settled — AR8 · AR13 · AR16 · IM5 · DR-05
The closed `Predicate/Modifier/EffectSpec` DSL + interpreter is a **framework no content has stressed**;
"add a verb = data edit, not resolver edit" is true only inside an **undrawn envelope**, and the radio
FSM + eight `systems/*.py` **already escape** the DSL. Logic-as-data can become a debugging nightmare
(AR16).
**Fix:** stop pretending it's all data. **Draw the envelope explicitly:** the DSL expresses the common
operation×material cases; **complex/stateful logic (FSMs, multi-step systems) is plain Python**, behind
the same `Operation`/tier interface. Pick the boundary deliberately, document what the DSL can't express,
and — critically — **build 2–3 real operations as plain functions first, extract the DSL only once the
repetition is proven** (avoid the premature-abstraction trap). DR-05 is the #1 thing to validate in the
slice.

### C4 — Object proliferation within a run — IM8 · IM2 · IM9 · AR11 · DR-06
Per-part-removal mints a first-class object, so `room.contents` balloons within a run (idmapper RAM +
linear WorldView-build/Tag-query growth), bounded only by end-of-run GC.
**Fix:** a **within-run debris policy** — cap/merge trivial derived objects (a pile of identical fabric
scraps is one stackable object), auto-despawn ignored debris, and keep the WorldView build scoped to the
zone, not the whole scene. Also: **`Part` must carry mass** (AR11) so the ledger can balance removals.

### C5 — Quality has no enforced gate (by design) — IM5 · IM12 · DR-18
Physics/conservation/solvability are enforced; **delight/depth is not** — it stays human-curated, exactly
where long AI-authoring loops drift. This is correct (automation can't certify delight) but must be
**named in the architecture**: the golden set + playtest *is* the quality gate, and AI-authoring loops
must be bounded by it.

## AR11 data-model gaps to close (smaller, concrete)
- The **environment sink** is an unbounded catch-all → make it **accountable per channel** (track total
  mass/energy it absorbs; assert it only grows; review anomalies) so it can't silently hide imbalance.
- **`Part.mass`** missing → add it.
- **Tick-driven state** (stamina/cold) must be **ledger-gated Effects**, not direct writes (C1).

## Prioritized fix list for A4 (update the doc)
1. **C1 — the enforced atomic ledgered mutation choke-point** (closes the RED + three YELLOWs). *Highest.*
2. **C3 — the DSL envelope + "plain Python first, extract DSL later"** (de-risks the #1 bet).
3. **C2 — determinism as an enforced contract** (lint + seeded ids + double-run test).
4. **C4 — within-run debris policy + `Part.mass`.**
5. **AR11 — accountable environment sink; tick-state as Effects.**
6. **C5 — name the quality gate (golden set + playtest) and bound AI loops by it.**

All six are **additive hardening** — none changes the design or the goals. They move the architecture
from "sound on paper" toward "sound and enforced."
