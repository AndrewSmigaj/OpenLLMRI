# A5 — Architecture certainty analysis (numeric system)

Scores every decision in the `implementation-architecture.md` register (DR-01…DR-22) for **whether it
is good design**, using an explicit numeric system, then ranks the weakest for A6 research. These are
the **v2 (lens-hardened)** scores; A7 re-scores after research.

## The numeric system
Each decision gets three values:

- **Confidence `C` (0–100):** probability this is a *good* architectural choice for Whiteout.
  | Band | Meaning |
  |------|---------|
  | 90–100 | **Proven** — a standard, battle-tested pattern; little could go wrong |
  | 75–89 | **Sound** — strong reasoning + supporting evidence; minor unknowns |
  | 60–74 | **Plausible** — reasoned but unproven here; a real chance it needs change |
  | 40–59 | **Uncertain** — material risk; could be wrong |
  | <40 | **Weak** — likely needs rework |
- **Criticality `K` (1–3):** 3 = load-bearing (failure sinks the project) · 2 = important · 1 = minor.
- **Evidence basis:** `Proven` (established pattern) · `Research` (backed by our prior-art/Evennia
  research) · `Reasoned` (sound argument, no external proof) · `Speculative`.

Derived:
- **Overall architecture confidence** = Σ(C·K) / Σ(K) — criticality-weighted mean.
- **Risk score `R` = (100 − C) · K** — what A6 should attack first (high R = uncertain *and* important).

---

## Scores (v2)
| DR | Decision | C | K | Basis | R | Note |
|----|----------|---|---|-------|---|------|
| DR-01 | Core/shell split | 90 | 3 | Proven | 30 | Functional-core/imperative-shell is standard; already works in the scaffold. |
| DR-02 | No runtime LLM | 95 | 3 | Proven | 15 | Clearly right; removes the dominant Evennia hazard. The safest decision here. |
| DR-03 | Content as data | 75 | 2 | Reasoned | 50 | Sound *as hybrid*; "all data" would be lower (see DR-05). |
| DR-04 | Material ordinal vectors + golden table | 80 | 3 | Research | 60 | QPT/ordinal reasoning backs it; the open Q is whether ordinals are *expressive enough* for good outcomes. |
| DR-05 | Operation model (hybrid DSL) | 65 | 3 | Reasoned | **105** | The biggest bet. Hybrid + "plain-Python-first" de-risks it, but the DSL envelope is undrawn until content stresses it. |
| DR-06 | Object model + debris + Part.mass | 78 | 2 | Reasoned | 44 | Cheap-objects sound; debris policy added; needs the cap/merge actually built. |
| DR-07 | Attributes + Tags single truth | 82 | 3 | Research | 54 | Evennia-idiomatic; the Tag-in-same-transaction sync needs verification (DR-10). |
| DR-08 | Deterministic parser | 85 | 2 | Proven | 30 | Classic IF/MUD parser; well-trodden. Richness is in rules, not parsing. |
| DR-09 | Resolver tiers + index + redirect | 80 | 3 | Research | 60 | Sound; the redirect "nearest operations" quality is the unproven part. |
| DR-10 | Enforced atomic mutation path | 80 | 3 | Proven | 60 | The pattern is standard, but **`transaction.atomic` over Evennia Attributes+Tags needs verifying** (A6). |
| DR-11 | Conservation ledger + accountable sink | 70 | 3 | Reasoned | **90** | Novel-ish; can the model truly *close* (mass/energy balance with the sink) across all transforms? |
| DR-12 | Determinism (enforced) | 85 | 3 | Proven | 45 | Seeded RNG + lint + double-run test is a known-good recipe. |
| DR-13 | Perception/zones | 80 | 2 | Research | 40 | Evennia `return_appearance` GREEN; rpsystem propagator exists. Deferred. |
| DR-14 | Clock/scheduler + @reload durability | 75 | 2 | Research | 50 | Event-driven is sound; activity persistence across `@reload` needs an Evennia check (A6). |
| DR-15 | Instanced sessions lifecycle | 68 | 2 | Reasoned | **64** | Tags + reaper Script plausible; how real Evennia games instance is unverified (A6). |
| DR-16 | Rescue model + radio FSM | 78 | 2 | Reasoned | 44 | Additive confidence is standard; the FSM is small and authored. |
| DR-17 | Build pipeline (author→validate→bake) | 80 | 2 | Proven | 40 | A normal asset/content pipeline. |
| DR-18 | Coverage/fuzz oracle | 82 | 3 | Research | 54 | Property tests + fuzzing are proven; the coverage *definition* is the clever part and it's sound. |
| DR-19 | Test strategy (two tiers) | 88 | 2 | Proven | 24 | Already demonstrated in the scaffold (19 pure tests ran with no DB). |
| DR-20 | Observability (decision trace) | 85 | 1 | Proven | 15 | Standard structured tracing. |
| DR-21 | Module/file layout | 88 | 1 | Proven | 12 | Conventional; mirrors the working scaffold. |
| DR-22 | Vertical slice scope | 88 | 3 | Reasoned | 36 | Slice-first is a strongly-validated de-risking move; the scope is well-drawn. |

## Aggregate
- **Σ(C·K) = 4278 · Σ(K) = 53 → Overall architecture confidence ≈ 81 / 100** (high end of "Sound").
- Interpretation: the architecture is **sound and buildable**, with a small number of load-bearing
  uncertainties concentrated in three places.

## Ranked A6 research targets (by Risk R)
1. **DR-05 — the operation model / DSL envelope (R=105).** *Is hybrid-DSL-with-plain-Python-fallback the
   right structure, and where exactly is the data/code boundary?* Research: how Inform 7 (rulebooks),
   TADS, and systemic sims structure verbs/operations; qualitative-physics rule representations; when a
   mini-DSL pays off vs. plain functions.
2. **DR-11 — conservation ledger closure (R=90).** *Can the model actually balance mass/energy across
   burn/melt/boil/dry/cut with the environment sink?* Research: how sims/qualitative-physics do
   conservation accounting; whether per-channel ordinal conservation is tractable; a worked balance for
   the chair + fire.
3. **DR-15 — instanced sessions on Evennia (R=64).** *How do real Evennia games implement instanced/
   per-party worlds and GC them?* Research: Evennia docs (rooms/zones/tags, `@reload`), Arx and other
   open games, contrib patterns.
4. **DR-10 — `transaction.atomic` over Attributes+Tags (R=60).** *Does Evennia support wrapping Attribute
   + Tag writes in a Django transaction, and a write choke-point/lint?* Research: Evennia/Django
   Attribute internals.
5. **DR-09 / DR-04 (R=60 each).** Redirect quality + ordinal expressiveness — partly empirical (slice),
   partly research (affordance/redirect patterns; ordinal vs continuous in sims).
6. **DR-14 — activity durability across `@reload` (R=50).** Evennia Script/Attribute persistence
   specifics.

These six are A6's agenda. Everything else is ≥75 confidence and standard; A6 will spot-check, not deep-
dive, those.

## Honest framing
~81/100 means: *a sound architecture with three real load-bearing unknowns (DR-05, DR-11, DR-15) and a
few Evennia-specifics to verify (DR-10, DR-07, DR-14).* None is a likely-fatal flaw; each is a "prove it
or adjust it" item. A6 exists to convert those from reasoned to evidenced — and to lower R where the
evidence is good, or change the decision where it isn't.
