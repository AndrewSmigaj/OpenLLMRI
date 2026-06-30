# 60 — Independent self-review & verification

Much of the architecture review was done by subagents, and **agents can be confidently wrong** — so this
is my own verification pass: checking the load-bearing factual claims against ground truth, reading the
product for internal consistency, checking the certainty math, and giving my *own* certainty assessment
(not just inheriting the agents'). Done by the main agent, 2026-06-30.

## 1. What I verified against ground truth (not the agents' word)

### Evennia claims — checked against the INSTALLED Evennia 6.0.0 source (the research agent read 4.5.0)
This was the highest-risk area (the agent flagged a 4.5.0 vs 6.0.0 version gap). I ran the actual
package in our container and grepped the real source. Results:

| Claim (research) | Verified on 6.0.0? | Evidence |
|---|---|---|
| EvAdventure **dungeon contrib** implements our instancing pattern (DR-15) | ✅ **REAL** | `evennia/contrib/tutorials/evadventure/dungeon.py` exists with `EvAdventureDungeonBranch` (L169), `EvAdventureDungeonBranchDeleter` (L396), `search_object_by_tag` (L257/270), `last_updated` (L219/284/418) — matching the agent's cited locations. The single biggest confidence-raiser (DR-15 +15) is genuine. |
| `reset_cache()` on attr/tag handlers (DR-10 rollback fix) | ✅ | `def reset_cache` present in `typeclasses/attributes.py` (×2) and `tags.py` (×1). |
| `TickerHandler.restore` (DR-14) | ✅ | `def restore` at `scripts/tickerhandler.py:435`. |
| Attributes pickled / not value-queryable → Tags for queries (DR-07) | ✅ (known Evennia fact) | consistent with docs; it's *why* the dungeon contrib uses tags. |
| `search_object_by_tag` API | ⚠️ **nuance** | exists, but **not** at top-level `evennia.` — it's under `evennia.search`/`evennia.utils.search`. Doc updated to say so. Not an error, a path detail. |
| `prototypes.spawner.spawn` (DR-15 improvement) | ◻️ couldn't import in a bare shell (needs Django settings) | standard, well-known Evennia API; low risk. Not independently confirmed here. |

**Verdict:** the agent's Evennia findings are **trustworthy** — verified on the correct version. No
hallucinated APIs found; the one discrepancy (the `evennia.search_object_by_tag` import path) is cosmetic
and now fixed in the doc. The version caveat is resolved (it holds on 6.0.0).

### Certainty arithmetic — recomputed by hand
v2 Σ(C·K)=4278, Σ(K)=53 → 80.7. Research deltas, K-weighted: DR-04 +15, DR-05 +21, DR-07 +9, DR-09 +24,
DR-10 +6, DR-11 +24, DR-13 +6, DR-14 +16, DR-15 +30 = **+151**. 4278+151 = **4429**; 4429/53 = **83.6 ≈
84**. ✅ The math in `50-final-changes.md` is correct.

### Design-research conclusions — sanity-checked against my own knowledge
The Inform 7 / TADS "are themselves hybrids," PDDL precondition/effect ladder, and the **qualitative-
physics result that ordinals can't carry a conservation balance** are all things I independently know to
be true. The two worked balances (foam-burn → ash + smoke-to-sink; 1 sheet → 5 strips) are trivially
sound. I did **not** independently re-fetch every citation, but the conclusions are correct and the one
that mattered (real-mass, not ordinal-mass) is a genuine and important correction.

## 2. What I found wrong in the PRODUCT (and fixed)
Reading the architecture doc end-to-end caught internal inconsistencies from layering v2/v3 hardening
onto v1 text:
1. **§4.2 opening contradicted the hardened DR-05.** It still said an operation is "a declarative schema
   … *not* a bespoke Python function per verb" — the opposite of the agreed "plain Python functions
   first; extract the DSL later." **Fixed:** reworded to the hybrid (one interface; data for common
   cases, Python for complex; functions-first).
2. **Ledger pseudocode said "± tolerance"** while the v3 text says mass balances *exactly* (integer
   grams). **Fixed** the comment.
3. **Stale closing line** ("Next: A3 applies the lenses…") as if the review hadn't happened. **Fixed:**
   replaced with a Review-status section.
4. **`search_object_by_tag` import path** — added the correct namespace note.

None of these was a *design* flaw — they were documentation drift. But they're exactly what a careful
human review is for, and they'd have confused an implementer.

## 3. My own certainty assessment (independent)
I **agree** with ≈84/100 for *architectural soundness* — and the Evennia verification nudges me slightly
*up* on the Evennia-dependent rows (they're now confirmed on our actual version, not assumed). I'd put my
independent number at **~83–85/100 for "is this correct, sound, buildable architecture."** Reasons I'm
confident: the core/shell + deterministic + operation×material design is well-precedented; the one RED
(unenforced conservation) is closed with a concrete, standard mechanism (transaction + choke-point +
lint + ledger); and the riskiest Evennia bet (instancing) turns out to match an official contrib.

**Two honest caveats I'd attach to that number:**
- **"Good architecture" ≠ "fun game."** The ≈84 is about engineering. It does **not** change the GDD's
  make-or-break, empirical question — *will pre-authored content feel alive?* — which sits at ~50% until
  a playtest. Don't let the architecture confidence bleed into game-confidence.
- **DR-05 (operations) is still the one I'd watch hardest.** "Plain functions first, extract the DSL
  later" is the right instinct, but teams routinely build the interpreter too early, or find the closed
  expression language too limiting so everything escapes to plain Python (wasting the DSL). 72/100 is
  fair; I would *not* build the DSL until ≥5–6 operations exist as functions and the repetition is
  undeniable. This is a build-discipline risk, not a paper-design risk.

**One residual I'll name that the agents underweighted:** running the conservation ledger over *every*
action **and every tick effect** adds real code ceremony and a little overhead. Reads are cheap
(verified), and the ledger is in-memory/pre-commit, so it's fine for correctness — but "every stamina
tick is a ledgered Effect" is more machinery than it sounds. Worth keeping the ledger *fast and simple*
(integer mass only; energy as a gate, as decided) so it doesn't become a tax on every heartbeat.

## 4. Bottom line
The review trail is **sound and, where it matters most (Evennia), independently verified true**. The
product had a handful of documentation inconsistencies, now fixed. My independent confidence in the
*architecture* is **~84/100** — the same ballpark the process produced, which I now trust more because I
checked its load-bearing claims rather than inheriting them. The remaining uncertainty is correctly
located in the **vertical slice** (DR-05 and the fun question), which is exactly where the plan already
sends the first build.
