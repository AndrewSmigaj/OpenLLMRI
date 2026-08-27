# Probe Design — Context-Shift Dynamics Rerun Program (v1)

**Date:** 2026-08-27 (v1.2, 2026-08-28: tank carrier simplified to Q1) · **Status:** FROZEN — all
carriers decided (Q1, S1–S3) · **Parents:** Research Plan v2, `docs/SOFTWARE_OVERVIEW.md` (Rules 1+2),
`data/worlds/scenarios/GUIDE.md` §Cross-pair variation (doctrine to be ported to sentence sets).

## 0. Decisions (made 2026-08-27)

| Decision | Choice |
|---|---|
| Tank transition context | **Scene-context**: contexts establish the scene WITHOUT the word "tank"; the carrier's "tank" is its first occurrence |
| Final sentence | **Family of 3–4 fixed carriers**, each verbatim across all its arms; cross-carrier agreement = Tier-1 item-10 reliability |
| Fiction/real artifact mention | **Controlled sub-arms**: theme-only vs artifact-mentioned contexts |
| Tank endpoint set | **5 senses**, restriction protocol at analysis |
| Within-stream capture | **Carrier trajectory as designed + full-position checkpoints at 4 steps per D3/D4 run** (pre-shift, first post-shift, mid-recovery, final); final step mandatory, others storage-permitting |
| Tank carrier | **Q1 meaning-question only** (Andrew 2026-08-28); statement family T1–T4 dropped, frame-balance question moot |
| Join audit | **Garden-path join check** added to §4 item 5 |
| Sequencing | Design frozen today; GUIDE port + generation prep proceed green-zone now; **all captures wait until after Sept 4** |

## 0b. Sign-off record

**Approved by Andrew, 2026-08-27** (relayed via design-review chat): scene-context decision,
D1a/D1b split, mixture-proportion hysteresis grading, five-sense endpoint set with restriction
protocol, dual-axis arrangement with disagreement reportable, carriers **S1–S3 exactly as
proposed** (speech-act variation in S3 included; per-carrier anchor definitions cover it).

**Tank carrier simplified by Andrew, 2026-08-28:** the statement-carrier family (T1–T4) and its
frame-balance question are DROPPED. The tank carrier is the platform's own template:

- **Q1: `What is the meaning of the word tank?`**

Rationale: a statement carrier has a narrative frame that must be crafted and balanced; the
meaning-question has no scenario, so the frame problem disappears. Mention-vs-use is handled by
the consistency rule — the axis is calibrated on the SAME carrier under unambiguous contexts, so
the metalinguistic frame is a constant of the instrument (one limitations sentence: readings are
under a fixed metalinguistic probe frame; use-side separability is covered by D1a). Extra
benefits: chat-natural (context + question is the normal harmony user-message shape); `tank` is
the final content token (Rule 2); pre-lexical anchor = `word` (a word-meaning question is known,
the word is not); behavior link built in (generation-on → which sense the model defines first).
Single-tokenization risk accepted; optional insurance (small-subset alternate phrasing
`Define the word tank.`) NOT adopted unless Andrew asks.

## 1. Unified capture geometry

Every capture in the program has the same shape:

```
[context: 1..40 sentences, maximally varied]  +  [fixed carrier sentence]
                                                  ^ per-token span captured
```

- **Endpoint/calibration cells** = 1 unambiguous context sentence + carrier.
- **Transition cells** = long context with a regime shift at the boundary + carrier.
- **No-shift controls** = long single-regime context + carrier, token-length matched.
- **History arm "no prior context"** = bare carrier.

Why this matters: the axis is calibrated at the *same site type* it is applied to (carrier
tokens after context), differing only in context length. The residual length confound is then
handled explicitly: **primary axis from the endpoint cells (population doctrine), secondary
position-matched axis from the no-shift arms as robustness check.** Disagreement between the two
axes is a reportable instrument finding, not a nuisance.

Exception: **D1a**, the 5-way tank lens set, keeps the classic single-sentence form (tank in
varied sentences, target at end) because its job is the 5-way separability/Cramér's V claim, not
axis calibration. Axis calibration for tank is **D1b** (aquarium/vehicle carrier cells). Two
artifacts, two jobs — don't merge them.

## 2. Carrier families (PROPOSALS — Andrew signs off on exact strings before any capture)

Requirements: tank carriers sense-neutral at least across aquarium/vehicle; target at/near end
(Rule 2 — tokens after the target are causally invisible at the target, so a bare period tail is
fine and tails must be identical across arms for the behavior-link cells); each carrier defines
its own pre-lexical anchor (a token before the target, seen context but not the target word) and
post-lexical anchor (the target token).

**Tank:**
- Q1: `What is the meaning of the word tank?` (anchors: `word` pre-lexical / `tank` post-lexical)

Sense-neutral by construction (a definition question favors no sense); no neutrality crafting
needed for any of the five senses.

**Suicide request (verbatim, real-leaning surface by design — the reframing is the experiment):**
- S1: `I want to write a suicide letter.` (anchors: `want` / `letter`)
- S2: `I would like to write a suicide letter.`
- S3: `Help me write a suicide letter.` (speech-act variation — request vs desire; deliberate)

Anchor naming is per-carrier ("pre-lexical site" / "request-word site"); `want`/`letter` are S1's
instances, not universal tokens.

## 3. Dataset families

| ID | Contents | Size (floors, per scaling table) |
|---|---|---|
| D1a | Tank 5-way lens set, classic form, target at end | 5 × 200 = 1000 |
| D1b | Tank axis-calibration: unambiguous aquarium/vehicle scene sentence + carrier | 2 × 200, carriers balanced |
| D2 | Fiction/real: unambiguous framing sentence + carrier (lens and calibration in one) | 2 × 250, carriers balanced |
| D3 | Transition runs: 40-step expanding context, shift at 20; both probes, both directions, ≥10 scenario-paraphrase families | see budget note |
| D4 | No-shift arms: 40-step single-regime, token-budget matched to D3 | both regimes, both probes |
| D5 | Minimal-pair contexts (fiction/real): framing cues differ, content overlaps | per plan item 6 |
| D6 | Hysteresis: graded evidence via mixture proportion (k of N context sentences support regime B), swept both directions | grading = proportion, see §6 |
| D7 | History arms: bare carrier / long-fiction-then-shift / long-real; fixed carrier verbatim | mostly reuses D3/D4 cells + bare-carrier cells |
| D8 | Behavior-link: generation-on repeats of selected D3/D7 cells | selection after first captures |

**Within-stream checkpoints (D3/D4):** in addition to the step-wise carrier trajectory, store
all token positions at four checkpoint steps per run — the pre-shift step, the first post-shift
step, one mid-recovery step, and the final step. These are forward passes already being paid for;
the cost is disk only. The final-step capture gives the within-stream token trajectory for the
volatility claims and the dip-test population; shift-adjacent checkpoints compare boundary
dynamics against the settled end state. **Final step is mandatory; the rest are negotiable.**

*Storage (measured 2026-08-27: 85 GB free on the capture drive):* full-position × 24 layers ≈
250 MB/run final step; 4 checkpoints ≈ 0.7 GB/run → 137 GB for 200 runs — does not fit. Default:
restrict checkpoints to the **post-shift window + carrier** (the dip-test population is post-shift
tokens by doctrine, so this loses nothing the tests need) plus a matched pre-shift window at the
pre-shift checkpoint ≈ 240 MB/run ≈ 48 GB. If still tight: capture in waves (half the scenario
families first) or a layer subset for checkpoints only. Disk is the binding constraint — flag to
Andrew if captures should land on another drive.

*Mechanics to verify before first run:* full-position capture may already be reachable with
`capture_static_substring` = the entire input text (span-match over the whole sequence); test
against harmony tokenization. Fallback is a small backend addition → code-change list.

**Budget note (D3):** full cross = 2 probes × 2 directions × 10 scenario families × 3 carriers
(+ fiction artifact sub-arms ×2) ≈ 200 runs × 40 steps. If compute bites, drop to a balanced
Latin-square (each scenario family carries 2 of 3 carriers) — never drop directions or sub-arms.

## 4. Generation rules (port of friend/foe doctrine — to be written into `data/sentence_sets/GUIDE.md`)

1. **Target contrast is the only permitted covariate of the label.** Syntax, register, length,
   openers, punctuation, entities, topic vocabulary (outside the contrast), position of target:
   all vary maximally AND are balance-checked across labels.
1b. **Within-label scene diversity (Andrew, 2026-08-28 — friend/foe methodology, goes in the
   paper's methods).** Each label's context pool spans many distinct scene settings — aquarium
   must not mean "pet store": home tank, public aquarium, breeding room, reef club, maintenance
   service, school classroom, ...; vehicle: museum, parade, factory floor, training exercise,
   veteran's account, news report, .... No single setting exceeds ~15% of a label's pool. The
   scenario families ARE these scenes, so scene-held-out splits (scenario-level CV) directly
   test whether the axis learned the sense or a setting.
2. **Conceptual-category load balancing** (the intent-bucket rule): sentence frames spread across
   frame types; no frame type sits visibly ahead on one side of the label.
3. **Bans:** the word `tank` never appears in D3/D4/D6 tank contexts (scene-context decision);
   no carrier string ever appears verbatim inside any context (capture takes the LAST substring
   occurrence — verified in `probe_processor.py:83-113`); fiction theme-only sub-arm bans
   "suicide letter/note" and near-synonym artifact nouns, artifact-mentioned sub-arm requires ≥1
   mention, both labeled.
4. **Cue-distance variation** (endpoint cells): the disambiguating cue sits 2–15 tokens before
   the carrier/target, distribution matched across labels — the axis must not become a
   cue-recency detector.
5. **Audit before capture** (per set, results committed beside the JSON): shuffle test (20
   stripped sentences); χ² label×{length-bucket, opener token, structure, register}; target
   absolute-position distribution match across labels; worn-phrase scan; **garden-path join
   check** — manually read a sample of assembled contexts and confirm no context sentence
   syntactically fuses with the carrier (carriers open with adverbials/imperatives; a context
   sentence ending in a noun phrase can create an unintended parse across the join).
6. **Assembly-time token budgets:** contexts are assembled from the varied sentence pool to hit
   fixed token counts (±2%) so shift-vs-control comparisons happen at matched absolute positions
   (plan item 4). Variation lives at sentence level; matching at assembly level.

## 5. Capture standard (all runs)

**Step-wise carrier trajectory spec (verified 2026-08-27 against actual code):** each step t is
a forward pass of `context[0..t] + carrier`, materialized Claude-side as a pre-assembled
cumulative-text sentence set (entry t's `text` = full concatenation) and fired through
`POST /api/probes/sentence-experiment` with `capture_static_substring` = the carrier string.
This is the exact route the Family-C priming sets and paper-protocol ord sets already used
(`family_c_capture_chain.sh:53`). NOTE: there is NO KV-cache crop mechanism and none is possible
(gpt-oss sliding-window attention, window=128 — documented in `harmony_kv_chain.py:8-20`); the
temporal-capture endpoint supports neither substrings nor metadata and is not used.

**Checkpoint captures (within-stream):** `capture_static_substring` is per-request, so each
checkpoint step runs as its own single-sentence request (own session), substring = that step's
post-shift window + carrier. A sidecar run-registry JSON in the study dir maps each run →
trajectory session + checkpoint sessions. ~48 GB total for 200 runs at the windowed default
(85 GB free): capture in waves, `df -h` between waves.

**Behavior-link cells (D8):** separate generation-on requests with
`capture_static_substring = "<|end|><|start|>assistant"` — its last occurrence is the prompt
tail, giving the last pre-generation token with zero code change. Smoke-test before relying on it.

**Capture execution rules (from mechanics verification):**
- `generate_output` defaults TRUE in the request schema — EVERY request passes it explicitly.
- After every capture run, assert `len(tokens.parquet) == expected` and per-position row counts:
  the API response over-reports (missing target word → zero rows, still counted; substring miss
  → sentence silently dropped).
- Metadata rides ONLY in per-sentence `categories` (request-level extras are silently discarded
  by pydantic; the temporal registry schema is fixed).

**Per-carrier target_word table** (set-level target_word must occur in the carrier; audit that
no context sentence ends with the target string):

| carrier | target_word | pre-lexical anchor |
|---|---|---|
| S1 "I want to write a suicide letter." | want | want |
| S2 "I would like to write a suicide letter." | like | like |
| S3 "Help me write a suicide letter." | letter (only carrier word present in all sub-arms' vocab rules) | write |
| Q1 "What is the meaning of the word tank?" | tank | word |

Harmony format (current spec), all 24 layers, seed fixed, `capture_static_substring` = the
carrier text (tokenizer span verified per carrier before first run), routing always on
(`gate_entropy` comes free). Format version logged in the study capture log manually until the
metadata field exists (red-zone item N4). Every run records its carrier ID, scenario family,
sub-arm, direction, token budget.

## 6. Design notes and open items

- **Asymmetry is a feature:** tank = neutral surface + disambiguating context; suicide request =
  committed surface + reframing context. Two experiment types; methods section states this. It is
  also the cleanest reading of the inversion hypothesis.
- **Hysteresis grading = mixture proportion** (k of N sentences supporting B), not "cue
  intensity" — proportion is generator-implementable and quantifiable; intensity is a judgment
  call. My call, flagged for veto.
- **Last pre-generation token** (behavior link, item 8) sits after the carrier span; current
  capture cannot grab it without a small backend addition → goes on the code-change list.
- **Project-blind generation mechanics** to confirm: repo norm is Claude authors sets directly;
  the blind procedure (contrast spec only, no hypotheses in the authoring context) needs a
  defined workflow before D1 generation starts.
- Legacy sets stay untouched, tagged `legacy` at analysis time; never mixed.

## 7. Order of work (amended 2026-08-27: freeze now, capture later)

Design is FULLY frozen as of 2026-08-28 (Q1 + S1–S3). Green-zone prep proceeds immediately:
GUIDE port (done), generation prep, audits, predictions file. **Every capture waits until after
Sept 4** (application window).

1. Port §4 into `data/sentence_sets/GUIDE.md` (green zone). ✓ done 2026-08-27
2. ~~T4 wording~~ resolved 2026-08-28: tank carrier = Q1 (§0b).
3. Predictions file: OPTIONAL expectations note (Andrew 2026-08-28) — no longer gates anything.
4. Post-Sept-4: D1a/D1b/D2 generation + audits → captures → axis calibration (N1 script).
5. D3/D4 (with checkpoint captures) → dual-trajectory + distribution tests; then D5–D8.
