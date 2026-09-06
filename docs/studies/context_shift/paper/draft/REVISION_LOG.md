# Revision Log — Multi-Lens Overnight Pass (2026-08-31)

Draft archived at `draft_v1/` (commit 137d7de) before any edit. Rule Zero in force:
writing-level changes applied; substance-level changes only proposed below.

## Substance proposals (NOT applied) — for Andrew's morning ruling

1. **"this study spent a year there deliberately" (04, closing).** Biographical
   duration I cannot verify from the repo. Left unchanged; confirm the "year" or give
   me the real figure.
2. **Single-author voice assumption.** Intro said "one of us studied these shifts";
   §3.6 said "one of us insisted... [provenance: A.S.]". I applied "the author" in the
   intro and rewrote the §3.6 sentence to keep the principle ("even a little
   off-manifold is off-manifold") without the bracket — the corrections record
   (Appendix A) still carries the named attribution. If coauthors are added, both
   should revert to "one of us (A.S.)" convention.
3. **Reasoning-traces clause (04, safety c2)** was not in FINDINGS_FINAL. I verified
   it against the committed worksheet (`analysis/r6_behavior_worksheet_fr_categorized.csv`
   — the model's analysis-channel text does weigh both framings before safe replies)
   and anchored the sentence to that artifact. If you want the paper strictly limited
   to frozen findings, cut the clause instead.
4. **Related-work gap (06).** Discussion's "same structure reported in the
   hallucination literature" had no anchor in the related-work spec. I added an
   internal-state anchor line (Azaria & Mitchell; Orgad et al.) to 06 — verify these
   are the citations you want at tex time.

## Number verification (pre-edit audit)

Seven draft values absent from FINDINGS_FINAL were traced before any editing:
drift ≈+1.0/≈0 and r = +0.75/−0.86 (v2 Gen-2); step-truth 0–2% (v2 §A4); D6 fitted
areas +14.3/+11.1 (v2 §B8); jump geometry 1.06×/1.12× (v2 three-worlds); marker
orthogonality −0.0052/−0.0065 (`s10_materialized.py`); reasoning traces (worksheet,
see proposal 3); "three retracted findings" = corrections 3/4/5, which fell to drift
and rotation combined — sentence re-attached to rules 3+4 jointly. Zero number
changes were needed; all edits below are wording.

---

## Round 1 findings and applied edits

### 00_abstract  [lenses L1 L3 L4 L5 ADV F60]
- **L5**: "jumps are triggered by the state, not by evidence strength" exceeded its
  evidence class (F4: state-dependence is the working interpretation; the measured
  fact is the negative). Rewritten: evidence strength does not predict jumps; trigger
  *appears* to lie in the state.
- **L5**: "no state leaves" → "no individual state leaves" (F10's per-state scope; the
  mean displacement is the marker claim that follows).
- **L1**: "the sense task committed silently" now carries its rate (52%) — the
  abstract's only unquantified behavioral claim, cheap precision.
- **F60**: title→abstract→contributions chain checked standalone: all three title
  words delivered; coin placed after the property list. No further finding.
- **L3, L4, ADV**: no additional finding.

### 01_intro  [lenses L1 L3 L4 L5 ADV F60]
- **L1**: cut "When an interpretation is unresolved, the model answers anyway — it
  goes with it." — restated the preceding sentence; "it goes with it" was
  conversational register.
- **L3**: 'tank' in quotes → *tank* italic (word-as-word convention used everywhere
  else).
- **L5**: contribution (6) "represents its own irresolution" overstated F10 (the
  marker marks *mixed context*); now "represents that its context is mixed."
- **STE-blacklist (applied early, structural)**: contribution (2)
  "permanent-within-range" was an invented compound → "with a residual persisting to
  the end of the tested horizon."
- **Voice**: "one of us" → "the author" (see substance proposal 2).
- **L4, ADV, F60**: opening hook (never-in-96) and three-worlds staging judged
  correct as-is; no additional finding.

### 02_methods  [lenses L1 L3 L4 L5 ADV]
- **L3**: §2.3 heading and Box 1 title both used "fooling yourself" — echo kept once
  (heading); Box retitled to a plain protocol name.
- **L1**: K=1 parenthetical compressed (tooling-facing aside, half the length).
- **L5**: "retracted three findings before adopting this rule" attributed all three
  retractions to rule 4; corrections 3/4/5 fell to drift+rotation jointly → sentence
  now attaches to rules 3 and 4 together.
- **L3**: glossary — semantic-metastability entry converted to pointer form per frame
  doctrine ("the name Discussion gives to..."); added *unresolved zone* (used in
  abstract/intro/results but never defined in the glossary).
- **L4, ADV**: Box-1 ordering and QA paragraph judged correct; no additional finding.

### 03_results  [lenses L1 L3 L4 L5 ADV, per R-unit]
- **R1/L4**: section now ends on the token-vs-utterance contrast (forward-pulling
  observation) instead of the trailing caveat; caveat folded into the figure
  parenthetical.
- **R2/L4**: "the study in one image" duplicated the intro verbatim → opener now
  states what is new at this point (both directions, one axis, against references).
- **R2/L2-early**: gap>1 explainer rewritten — the mixed unit systems (+2.16
  midpoint-referenced vs 1.09 amplitude-normalized) are now explicitly equated in one
  clause.
- **R2**: "Honesty requires one demotion" (self-regarding) → "One cell demotes under
  a stricter bootstrap."
- **R6/L3**: opener "the geometric question the title poses" mis-assigned the
  question → "the third of the introduction's three worlds" (resolves the intro's
  setup).
- **R6/L5**: calibration-state positive control "1.7–2.2×" spans two instruments
  (1.73× k-NN bundle; 1.9–2.2× subspace) — now says "across the two instruments."
- **R6**: provenance sentence rewritten without the bracket (substance proposal 2).
- **R3, R4, R5**: all numbers verified against FINDINGS_FINAL verbatim; no additional
  finding. ADV note: R5's misspecified-null disclosure and R3's identifiability
  framing are the section's strongest review-proofing — left intact.

### 04_discussion  [lenses L1 L3 L4 L5 ADV]
- **L3**: "ninety-six" → "96" (numeral convention for data counts).
- **L5**: reasoning-traces clause anchored to the committed worksheet (substance
  proposal 3).
- **Blacklist (structural)**: two "precisely" removed (para 1, safety c2).
- **L1**: "One disclaimer accordingly" → "One disclaimer."
- **ADV**: hallucination-literature sentence needed a citation anchor → 06 updated
  (substance proposal 4).
- **L4**: paragraph order (descriptive safety before interpreted safety;
  garden-path/pun after) judged correct; no additional finding.

### 05_limitations_future  [lenses L1 L3 L4 L5 ADV]
- All quantities verified (48% indeterminate; n=4 letter site; suggestive
  real→fictional). **No additional finding** — the section's candor-inventory
  structure is its strength; left intact pending Round-2 craft pass.

### 06_appendices  [correctness check only]
- All cross-references from body sections resolve (Appendix A ← intro/methods/
  discussion; Appendix C ← post-freeze s11/s12; Appendix D ← supplement citations).
- Figure partition (main vs supplement) consistent with body citations: fr fit
  gallery and fr D6 loop supplementary, tank versions main; fr secondary heatmap
  main, tank version supplementary. Verified against 03's citation list.
- Added internal-state related-work anchor (substance proposal 4).

---

## Round 2 findings and applied edits

### Linear read (L4 + OWN at paper level, + fascination check)
- **Echo**: intro's closing "Every number in this paper regenerates from committed
  code" duplicated §2.4 verbatim → intro version reworded and shortened.
- **§3.4 ending**: the correlational caveat was the section's last sentence, burying
  the 50→80→91 gradient → caveat moved to the head of the behavior paragraph; the
  section now ends on the gradient.
- **Deliberate echo KEPT**: "property of paths" closes both §3.5 and Discussion ¶1 —
  judged a functional thesis restatement (results states the finding; discussion
  anchors the term), not redundancy.
- **Fascination check**: surprise staging verified — stickiness death (§3.5, with the
  same-hour retraction told in place), failed jump prediction (§3.6, "we report it as
  failed"), challenged-verdict marker discovery (§3.6), plateau-on-the-midpoint
  (§3.2), 0/96 bolded at §3.4's center. No flattening found to restore.

### L2 + STE craft pass (with tic blacklist)
- **UNIT FIX (the pass's most important catch): the abstract labeled the residual
  range "0.4–1.1× the class separation"; the frozen values (F9) are amplitude
  fractions — 1.09/0.57/0.43/0.40× the no-shift reference amplitude, which is half
  the separation. The abstract overstated the residual by 2×. Fixed to "no-shift
  reference amplitude" in the abstract and mirrored in WRITEUP_SEPT3 (§3.2 already
  had the correct units). Caught before the Sept 3 submission.**
- Also fixed in §3.2: my own Round-1 rewording "the transition never half-completing"
  was wrong (a midpoint plateau half-completes exactly, never more) → "the transition
  stops at half-way."
- "deliberately" appeared 3× as an intensifier (intro design, methods axis, results
  claim) → kept once (methods, where it answers the too-simple objection).
- "unmistakable/unmistakably" (×2, §3.5/§3.6) and "demonstrably" (×2, §3.6/§4)
  removed or replaced with plain statements next to their numbers.
- "and critically," (§3.3) removed — the following sentence already lands the point.
- Idioms replaced with plain statements: "with and without a net" → "with and without
  a trained fallback"; "no writ" → "no trained behavior applies".
- One-meaning-per-word: "A model reading... maintains a reading" (intro) → "A model
  processing... maintains a reading."
- Dangling modifier (intro ¶2), "namely that" stack, "actually/exactly" fillers,
  spelled "ninety-six" → "96" (numeral convention), "single 20B model at one scale"
  redundancy (05) — all fixed.
- Precision: 2.1's "greedy forward passes" — greedy describes decoding, not capture
  passes → "deterministic forward passes"; greedy decoding now noted at the behavior
  cells in 2.2 where it applies.
- Abstract's final sentence split (three stats in one sentence); hysteresis sentence
  regrammared ("Order matters... but is fully explained" had a broken referent).

### OWN pass (final text, per section)
Signed: abstract, intro, methods, results, discussion, limitations. The paper says
what the study found, at the strength the evidence licenses, in scientific register,
and I would put my name on it. Remaining discomforts are logged as substance
proposals, not silently fixed.

### Mechanical sweep
- Number-trace automation: all 148 draft numerals ∈ FINDINGS_FINAL ∪ v2 ∪ logged
  post-freeze (s11/s12) ∪ committed-script output (s7 S1.4 percentile medians
  0.51/0.45/0.48/0.49; s10 orthogonality −0.0052/−0.0065) ∪ architecture facts
  (2,880 dims) ∪ the content-note 988. The 0.4–1.1 range is derived from frozen
  1.09/0.57/0.43/0.40.
- Terminology: one name per concept verified against the glossary (mixed-context
  marker, park, residual, unresolved zone, accumulation drift, axis rotation).
- Figure-reference style uniform (Fig. fig_name placeholders for tex); figure
  main/supplement partition consistent between body citations and Appendix D.
- Prose rewrapped to 88 columns; hyphenation artifacts repaired.

## Additional substance proposals (NOT applied) — appended for morning ruling

5. **The paper's last page is the freeze sentence.** Reading order is 04's scout
   close → 05 limitations → "...logged as such in Appendix C." Consider moving 04's
   Closing paragraph to a short §6 Conclusion after limitations so the paper ends on
   it. Structural move — not applied under Rule Zero.

## Budget — honest miss, explained

Paper sections (00–06): draft_v1 6,555 words → revised 6,614 (+0.9%). The 5–10%
shrink target was not met and I did not force it: dead phrasing and redundancy were
removed throughout, and the residual growth is entirely required additions — the
glossary's unresolved-zone entry, the internal-state citation anchor (06), the 52%
rate the abstract was missing, and the worksheet anchor for the analysis-channel
claim. The outline-disciplined draft had little fat; cutting further would have meant
cutting information, which the shrink guard forbids. Growth by section: 02 (glossary)
and 06 (anchor) as justified above; every other section is flat or smaller.

## Reviewing the diff

The prose was rewrapped to 88 columns in Round 2, so a plain line diff of `draft/`
vs `draft_v1/` is noisy. Use `git diff --word-diff --no-index draft_v1 draft` (or
`--word-diff=color`) — that view shows exactly the logged edits and nothing else.

---

## Morning rulings (2026-09-01) — snippet-material audit

Andrew's ruling: the voice snippet was topic orientation only; nothing from it may
appear as claims about the author or personal material. Full-paper sweep run.

- REMOVED: "spent a year there deliberately" + "or a scientist" (04 closing) — the
  duration was fabricated by Claude during drafting; proposal 1 resolved by deletion.
- REMOVED: "the author studied these shifts... cosine distance..." (01) — snippet
  anecdote had been converted into a formal prior-work claim; paragraph rebridged
  without biography. Proposal 2 (authorship voice) is moot: no first-person-history
  claims remain anywhere.
- STALE COMMENT fixed: 01's header said "Andrew's voice"; now "scientific register."
- AWAITING RULING: (a) the incident paragraph's "widely reported incident" (01) and
  WRITEUP's "a real incident" — unsourced by the repo; needs confirmation + citation
  decision, or reframing; (b) epigraph — approved with title, traditional joke, not
  biography; (c) closing cross-scale sentence ("what minds — artificial ones
  included —") — recommend narrowing to "what a model should do."
- Sweep result otherwise clean: no "one of us", no "(A.S.)", no other personal
  attributions in 00/02/03/05/06.

---

## Comprehension pass (2026-09-01) — cold-reader-driven rewrite

Method change after Andrew's challenge: two zero-context cold readers (report, never
author) read the full paper; 80 comprehension defects reported; all addressed or
consciously declined. The failure they exposed: the overnight reviewer was the
author, so the paper's structural vocabulary and coinages never read as cryptic.

**Three global renames (terminology only; all numbers unchanged, re-audited):**
- *residual* (finding) → **remnant**; "reconstruction residual" → "reconstruction
  error" — kills both collisions with "residual stream".
- *accumulation drift* → **accumulation offset** — kills the collision with the
  drift-plus-jumps mechanism (a cold reader genuinely wondered whether the headline
  finding was our own artifact).
- count-noun *probe* → **task** — kills the collision with linear probes; "tank
  task" / "fiction/real task" everywhere.
- Appendix C now carries a repository↔paper terminology map (repo keeps its names).

**Structural vocabulary now defined before use:** site (token+layer, in §2.1); arm,
cell, scene family, scene-held-out (new vocabulary paragraph, §2.2); carrier fronted
in the intro; checkpoint captures, mixture sweeps glossed in place; bands defined in
§3.4; time bands renamed time bins. The park and the mixed-context marker are now
christened by explicit naming sentences at their discovery points.

**Units and stats glossed at point of use:** amplitude defined twice (abstract,
§3.2); remnant-gap units spelled out; held-out numbers labeled as accuracy; the
±2.9 unit named (across-run standard deviations); slash-pairs labeled (§3.6 carries
a one-line pairing convention); the drift magnitude given its "half the class
separation" hand; r = +0.75/−0.86 explained; six domains named; the novelty
prediction stated before its refutation; 96-vs-108 counts reconciled;
safe-completion defined; the abstract's four conditions enumerated.

**Insider material removed or translated:** the K=1 parenthetical cut from §2.1
(now one line in Appendix C); "analysis-channel text"/"behavior worksheets" →
chain-of-thought text released with behavior data; "conceptual-operator battery" →
plain description; "blind generation batches" → plain; "remanence" glossed away;
authoring agents now identified as language-model agents (a fact the paper owed the
reader); the depth-ordering prediction's content stated ("ordering of crossing
times across layers"); "instrument doctrine" → "measurement protocol";
"interpretive irresolution" and "behavior-inert" uncoined.

**Judgment calls:** the closing now restates the title word and is scoped to "a
model" (the cross-scale "minds" flourish removed — my verdict under the
best-paper standard, logged for Andrew's review); "even a little off-manifold is
off-manifold" replaced by the plain statement of the shared-small-displacement
logic; "Incongruity, then resolution" kept with an anchor to §1. Figure references
keep placeholder ids until tex (numbering is a tex-time job).

Number-trace re-audit after all edits: identical missing-set to the pre-edit audit
(section refs, derived 0.4–1.1 range, model dims, hotline number, committed-script
outputs). Zero number changes.

STILL OPEN (Andrew): the incident paragraph — real, citable public case or not?

---

## Flourish-pattern sweep (2026-09-01, Andrew's "AI rhetorical flourish" ruling)

The named offender ("does not merely travel slowly — it stops") was an instance of
the "not X — it is Z" reveal pattern from this plan's own tic blacklist; it survived
because the sweep matched named lexical forms, not the structural pattern, in
sentences the author-reviewer wrote. Whole family swept (11 fixes):

- Negation-first reveals: park sentence → "stops rather than traveling slowly."
- Announcement throat-clearing: "And here is the descriptive fact..." → "One
  descriptive fact anchors this paper's framing:".
- Verdict theatrics: "The data return that verdict anyway" → "On the real runs the
  selector nonetheless returns hybrid"; "Answer: there is none." folded into its
  sentence.
- Poetic doubling: "it trails what the conversation has become" cut; "the study in
  one image" → "the central result" (intro + writeup caption); "the geometry our
  data forced on us" → "the geometry our data show"; "nothing needed to escape" →
  "no barrier to escape"; "nothing leaves." given its object.
- Fragments: "Incongruity, then resolution:" recast as a full sentence keeping the
  §1 tie; closing inversion "So, for now, is..." → "For now, so is...".

KEPT, deliberately (overrule if wrong): the intro's 96-completions hook; "The
failure surface this study maps needs no adversary" (a claim, not a reveal — it
positions the work against the jailbreak literature); §2.4 "outlived our own
attempts to kill them" (the corrections-as-method thesis); the bolded 0/96 sentence;
the simplified title-mirror close. Test applied: a declarative sentence carrying a
real claim stays; a construction whose only job is drama goes.

---

## Figure-vs-text audit + terminology settlement (2026-09-01, Andrew's challenges)

**Correction 18 (real numerical error, Andrew's catch).** The paper and FINDINGS §2
said readings "cross within 7–13 sentences"; Andrew eyeballed the fr collapse curves
crossing at ~4 and asked why the figure didn't match. Recomputed from committed data:
per-run median crossings tank 10.5/6.0 (1 run never crosses), fiction/real 4.0/5.0
(2 never); mean-curve crossings 13/8/4/4. The "7–13" matched no headline cell.
FINDINGS_FINAL §2 corrected + entry 18 appended; the paper now quotes per-cell
values; all "seventeen-entry" counts updated to eighteen.

**Single-site disclosure + depth structure.** §3.2 now states the collapse figure
shows each task's calibrated site only (layers 4 and 14) and adds the depth
paragraph from the B5 record: shallowest fr layers cross in 3–4 sentences (the
sudden flips visible in the heatmaps), mid-stack at medians 8–13; tank
aquarium→vehicle crosses at median 13 in every depth band with three deep layers
never crossing (the dwelling is stack-wide), reverse direction earliest at depth
(median 6); the half-failed layer-ordering prediction now appears in results, not
only in limitations.

**Terminology settled (Andrew's ruling, discussed not kneejerked):** no coined noun
for the stationary phenomenon. The paper says the trajectory "dwells within the
unresolved zone" (dwell as ordinary English verb), with "the stationary/dwelling
states" as the natural short form; "park" is gone from the paper (glossary entry
removed; Appendix C terminology map points repository readers from "park" to the
descriptive phrase). Horizon bounds applied at every dwelling claim: "on the
measured horizon, does not leave" (§3.4, with the shallow-late-slope caveat),
"to the end of the measured window" (abstract), "for the remainder of the tested
horizon" (discussion).

---

## Incident verified and corrected (2026-09-01)

The motivating incident is Raine v. OpenAI (Cal. Super. Ct., filed 2025-08-26;
16-year-old Adam Raine, died April 2025): months-long conversations; safeguards
triggered on direct requests; requests reframed as fiction received assistance (the
filing says the model's own reply suggested the creative-purposes route); the model
offered to draft the suicide note; OpenAI's moderation reportedly flagged 377
messages in real time; OpenAI's Nov 2025 answer denies causation. TWO corrections
to our text: (1) the arc was reversed — real circumstances were on record and the
FICTIONAL reframing unlocked assistance, not fiction drifting into disclosure; the
intro paragraph now matches the documented arc and attributes to filing+reporting
(contested litigation). (2) The real-time-flagging fact was added to the
discussion's "represented but not consulted" paragraph as the system-scale
instance of the same structure. Citation anchors added to 06 for tex time. The
last open item from the snippet audit is closed.

---

## Independent claims audit (2026-09-01, Andrew-commissioned) — 21/21 verified, all fixed

A fresh agent with no session context audited every claim against both findings
records, with license to disagree with the records' own confidence labels. All 21
findings verified by me against the sources; none rejected. Applied:

1. 91→50 safety gradient: abstract/discussion now carry n=4 endpoint +
   partly-scene-driven caveats; "tracks" → "co-varies with".
2. Dwelling scoped to tank (fr = n=4 paraphrase-carrier site, exploratory);
   hedging scoped to tank mid-band; abstract, intro (4), §3.4, §4, writeup.
3. Marker: "learned/represents/dedicated" → measured wording (systematic signal;
   pure ≈0 vs mixed ≈27%); the 1-of-8-uncorrected behavior tests now stated; the
   learned-representation vs input-consequence question explicitly left open;
   glossary entry updated.
4. "State-triggered" demoted everywhere to working interpretation (heading, intro,
   abstract, writeup); single-sentence-percentile limitation added to §3.3.
5. 0/96 scoped (tank, all bands) and reconciled with the 45% both-answers;
   "reports nothing" → "never asks or flags the ambiguity."
6. Intro's safeguard-default reading deferred to §4 instead of "turns out."
7. Chain-of-thought weighing marked qualitative/unquantified.
8. "Any smooth mechanism" → "any of the smooth mechanisms tested."
9. Abstract mechanism claim scoped to classifiable runs.
10. k∈{6,12} pooling flagged post-hoc, graded suggestive.
11. "Categorical frame detection" → saturation description.
12. "Information needed to flag the zone" → correlated signal, zone-flagging
    untested, monitor chance-compatible; "gating" → "testing whether... can be gated."
13. "Ordinary activations" → "matched no-shift states."
14. 3.6 context-token median misattribution FIXED (error introduced by the
    comprehension pass on 09-01 — my error, caught by the auditor in code).
15. Intro "neither ever reaches" → three-of-four robustly, window-bounded.
16. "Dedicated direction the no-shift world never occupies" → near-zero vs ≈27%.
17. Intro (5) "fully/nothing beyond recency" → "almost fully; mild γ difference."
18. "Full manual categorization" → regex + manual review of committed worksheet.
19. Rule 7 "every effect" → "every effect they are run on" + marker's own null.
20. Q1b replicate flagged in-sample.
21. Abstract "interpretation/means" tightened to reading/position language.

Auditor's solid-list covered all headline quantities; weakest-claim verdict (the
91→50 sentence) addressed by fix 1. Number-trace re-audit: unchanged, passes.

---

## Depth-scoping addendum (2026-09-01, Andrew's layer question)

The marker behavior-null and all behavior-link analyses are single-layer (tank L4,
fr L14; verified in s8_subspace_geometry.py) — now stated in §3.6/§4, with a
single-layer-readout limitation added to §5. New committed figure
fig_s13_collapse_layers (s13_collapse_by_layer.py): the collapse view at four
layers per task — sudden complete flips at fr's shallow layers, partial crossing
and dwelling at mid/deep layers, tank's dwell visible to L20 — cited from §3.2's
depth paragraph. Bonus from the r3 battery re-run: tank remnant gaps replicate at
L4/L8/L12/L16 (0.80–1.09 amp), so the tank dwell is depth-robust.

---

## Per-layer behavior check (2026-09-01, Andrew's depth-resolution hypothesis)

New committed s14_behavior_by_layer.py (post-freeze, exploratory): reading→behavior
association at every layer, joining the r3 projection cache with the categorized
behavior worksheets (family-clustered bootstrap). Result: curves roughly flat from
mid-stack to L23 in both tasks (fr peaks ≈0.69 at L6, ≈0.63 at L14 and L23; tank
peaks at its own site L4 ≈0.71) — no deep-layer advantage; instrument blunt
(band-level, imbalanced). The representational half of Andrew's hypothesis is
confirmed and now in §3.2: fr crosses to the destination side at depth (median 8)
in both directions while tank aq→vh stays origin-side through L23 — the dwelling
reaches the output-adjacent layers. Discussion c2 gains the depth-resolution
account as a second, compatible candidate (n=2, observation not test).
fig_s13_collapse_layers extended to include L23.

---

## Depth-claim correction (2026-09-01, Andrew's "explain that sentence" challenge)

"Remains on the origin side through the final layer — three deep layers never
cross" binarized trajectories that hover AT the midpoint: tank aq→vh late-window
dest-signed means are +0.12 (L3–12), 0.00 (L13–18), −0.10 (L19–23) — the honest
claim is midpoint-hovering, not origin-side. Worse, "fr crosses at depth in both
directions" was crossing-metric-true but materially wrong: fic→real's deepest band
ends at +0.08 (hovering), only real→fic settles (+0.48; tank vh→aq +0.42). §3.2
now carries the banded late-window means (regenerated by s13's new printout); c2's
depth-resolution candidate restated as weaker (fic→real's unresolved deepest band
is the direction where the safeguard engaged — depth-resolution cannot carry the
explanation alone).

---

## Early-trigger candidate (2026-09-01, Andrew's corrected heatmap reading)

Andrew's layer-order correction produced the strongest of the three safeguard
accounts: the shallowest fr layers resolve framing composition instantly and
completely with a surface-cue-tracker profile (D5's cue-only exclusion ran at L14
only), so a safeguard reading early would fire broadly on the alarming content and
be suppressed only by an established fictional frame — matching the 80% mid-band
hold and the fragile 50% fiction-side floor. Added to c2 as the third,
non-exclusive candidate (policy / downstream state / trigger locus), with the
saturation caveat explaining why s14 is blind to it, and patching named in §5 as
the decisive test.

---

## Shallow-lag observation (2026-09-01, Andrew)

Confirmed: fr's shallow band crosses at medians 3-4 and settles complete
(+0.99/+1.14); tank's shallow band crosses at 13/8 and settles partial toward
vehicle (+0.57). Added to section 3.2's depth paragraph. Andrew's RL-provenance
conjecture added to c2's early-trigger passage with its rival (pretrained register
statistics) and the unobservability caveat stated. Coherence note: the safeguarded
task is the one with the fast shallow detector (n=2, correlational).

---

## Methodology section + terminology + correction 19 (2026-09-01, Andrew)

- New §2.4 Analysis methods: midpoint decision rule for accuracies; the four model
  forms with the γ^age formula (uniform = γ→1 case, precisiating §3.3's "five
  models" vs the code's four BICs); BIC/ΔBIC≥2 with indeterminacy; remnant-gap
  definition; family-clustered bootstrap (2,000 seeded draws); categorization
  procedure. Reproducibility renumbered §2.5.
- "Fitted recency" now defined at every use; the abstract glosses it inline.
- "Arm" eliminated (transition runs vs no-shift arms was one object under two
  names): everything is a run; the D4s are no-shift control runs.
- "Cell" had grown three senses; now grid-cells only (mixture sweep). The four
  task×direction units are "conditions"; behavior units are completions/prompts;
  calibration items are sentences; "cell-level monitor" → monitor of individual
  readings.
- CORRECTION 19: "γ≈0.9–0.98 → effective memory 10–17 sentences" did not follow
  from the committed fits (r1_model_selection CSVs): per-cell median γ 0.90/0.90
  (fr), 0.94 (tank→aquarium), 0.985 (tank→vehicle) → weighted-mean ages ≈9/9/14
  and ~66, beyond the window. The near-uniform γ of the dwelling direction is the
  integrator fit's own dwell signature — now stated as such in §3.2; c1 updated;
  FINDINGS §2 + entry 19; writeup mirrored.

---

## "Mechanism" demoted to "form of the dynamics" (2026-09-01, Andrew)

Andrew: how is drift-plus-jumps "the mechanism"? It isn't — it is functional-form
selection at the trajectory level: a simulation-calibrated exclusion of smooth
integration plus the signature of discrete reorganization events, with no
implementational content (nothing identifies what inside the network produces a
jump). §3.3 heading and intro contribution (3) renamed; a status sentence added to
§3.3 stating exactly what the model selection does and does not license; writeup
heading mirrored. Same overreach family as "state-triggered"/"learned"/"park":
interpretation-loaded words standing where measured claims should.

---

## Kind audit — rulings applied (2026-09-01, discussed first)

Independent kind-of-claim audit (20 findings) verified item-by-item, then discussed
with Andrew before any edit. Applied (15): the two signpost headings (§3.6 → "The
geometry of irresolution"; §4 → "A signal behavior does not appear to use"); intro
contribution (6) de-escalated (cut "carries the information that"); "encodes" →
"elevates"; causal denial → predictive ("Jump timing is not predicted by evidence
strength"); "over-weights" → "the pattern a recency weighting would produce";
state-attribution → differentiating-property phrasing; "reorganization events" →
"changes in the reading"; "its integration window" → "the fitted recency timescale"
(×2); "would be" subjunctive in the typicality taxonomy; "carries no such default"
→ "showed no such default"; "content" → "what elevates it"; "safeguard must engage"
→ "safeguard behavior must appear"; "representational level" → "activation level";
intro's motivating question reworded per Andrew's approval ("internal state that
tracks whether the request is framed as fictional or real").

Declined with reasons (4): #10 (question-then-operationalization structure is
correct; §3.6's next sentence already fixes reference/measure/noise); #12 (Andrew's
argument: gpt-oss safeguards ARE trained, not scaffolding — "deployed" would
mislead; "trained" kept, model-card anchor added); #16 ("scene-driven" is
deterministic input causation, the audit's own licensed principle); #20 ("update" is
time-series idiom, frozen-record vocabulary).

Held: #15 awaiting Andrew's ruling (full before/after shown; the in-between
language is retained by the fix).

Audit's systematic lesson, logged for the tex pass: compression at the signpost
layer (headings, lists, topic sentences) strips the licensing devices — check
summaries run no hotter than the sentences they summarize.

---

## Methods restructure (2026-09-01, Andrew-approved after discussion)

§2.3 now opens with the actual computation: the projection formula
(r(h) = 2(h − m)·w/|w|², class means at ±1), the projection-not-distance sentence,
the explicit probe choice (diff-of-means over logistic probe: hyperparameter-free,
transparent geometry, comparable readout [CITE: mass-mean probing]), and the
midpoint accuracy rule (moved from §2.4). §2.4 restructured into labeled
paragraphs — Trajectory models (opening "no regression is involved in the
instrument; least squares enters only here"), The remnant gap, Uncertainty,
Behavior. Marks & Tegmark anchor extended for the probing precedent.

Process lesson (Andrew's criticism, valid): coherence/readability passes ran over
the pre-audit draft; every post-audit addition (§2.4 itself, depth paragraphs,
candidate accounts) skipped them. Rule going forward: new prose gets a read-through
before commit, and a hotspot linear re-read is owed now.

---

## Final revision batch (2026-09-01, applied on Andrew's go-ahead)

Readability: the abstract's long sentences were split and its duplicate 45% removed;
section 3.2 was re-cut into six short paragraphs; the discussion's interpretation
paragraph was split into three; the contributions are now a numbered list; smaller
fixes throughout (the real carrier quoted in the intro, a paragraph break in 3.4,
one redundant sentence cut in methods).

Register: the paper no longer tells the story of its own mistakes. The section-4
paragraph about our expectations was deleted; Appendix A now lists only corrections
that changed printed numbers, with the full record in the repository; Appendix B
(the synthesis-audit table) was removed from the paper; the remaining disclosures
(failed prediction, misspecified null, three retracted depth findings) stand as
single factual sentences where the evidence needs them.

Accuracy of wording: "fast" is gone (the transition is gradual; the two-phase claim
now says the data sit above the best fit early and below it late); "permanent" in
the 3.2 heading became "lingering"; the glossary bounds the remnant to the tested
window; "task-by-direction conditions" and similar constructions are plain English
now. Appendices renumbered (QA is B, supplementary figures C) with references
updated. No numbers changed.

## Rewrite, Step 0 — checks and freeze (2 September 2026)

Andrew's ruling: rewrite every section for a human reader, reordering first, nothing
left out, each section judged by an independent reviewer before moving on. Plan file:
`~/.claude/plans/review-this-make-sure-parallel-lynx.md`.

Set up before any text changes:
- `paper/WRITING_STANDARD.md`: the rules, the metric targets, and the reviewer's brief.
- `paper/tex/prose_metrics.py`: words per sentence, share over 35 words, numbers per
  paragraph, em-dashes and semicolons per 1,000 words, with PASS/FLAG against the
  targets. Baseline on the current draft: every section flags on dashes and
  semicolons; Results flags on all five targets (31 words per sentence, 35% over
  35, 6.6 numbers per paragraph).
- `paper/tex/number_check.py`: trace (every numeral in the draft appears in
  FINDINGS_FINAL, the v2 record, or `number_allowlist.md`) and preservation (every
  numeral in `draft_v2/` survives in the current draft). Both pass on the current
  draft. The allowlist records thirteen sources for values outside the findings
  documents (model width, bootstrap draws, s7/s10/s11/s12/s13 script outputs, the
  content-note number, and two derived ranges).
- Captions moved from `build.py` into `draft/captions.md`; `build.py` reads that
  file and converts captions like section prose. Caption text unchanged except
  "k ∈ {6,12}" written as "k of 6 and 12".
- `md2tex.py`: straight double quotes now convert to LaTeX quotes (the built PDF had
  been rendering both quotes of a pair as closing quotes).
- `draft/` copied to `draft_v2/` as the frozen pre-rewrite reference.
- One fix in the appendix assembly note: "3.2's" → "§3.2's" (a section reference,
  not a number).
- PDF rebuilt: 27 pages, zero errors. s13 re-run; the PNG regenerated byte-identical.

## Rewrite, Step 1 — structure pass (2 September 2026)

Reordering and splitting only; prose rewritten only where sections had to be stitched.
No number changed; `number_check.py` trace and preservation both pass.

- Methods reordered: 2.1 model and capture → 2.2 the instrument → 2.3 tasks, carriers,
  and corpora (each corpus introduced with the question it answers; "D3", "D4",
  "arms", and "reference ruler" removed; the vocabulary paragraph is now a list) →
  2.4 the protocol (Box 1 and the glossary, with *dwelling* defined) → 2.5 analysis
  methods (one sentence per trajectory model) → 2.6 reproducibility.
- Results: a roadmap paragraph at the top. Section 3.2 reordered: figure and crossing
  → the remnant gap (defined where it is first used) with Table 1 → the demotion,
  material, and permanence checks → the two-phase shape and the decay parameters →
  depth crossing → depth endpoints with Table 2 → asymmetry. Table 3 (model-selection
  counts and the selector calibration) added to 3.3. Old 3.4 split into 3.4 (the
  dwelling) and 3.5 (behavior); order and geometry renumbered 3.6 and 3.7. Repository
  labels "(R1)"–"(R6)" dropped from the headings. Cross-references updated in the
  introduction, discussion, and appendix.
- Table 1 carries all four reference-resampled intervals (source: the QA report, row
  C5), not only the one that demotes. Table 3 carries the five-model selector's
  full counts on real and synthetic runs (source: the s9 figure script, whose totals
  are in FINDINGS_FINAL F4). Allowlist entries added for both.
- Discussion grouped: what we found (the term; typicality versus commitment) → safety
  (descriptive → "A trained default for unresolved cases?" → "Why the safeguard held:
  three candidate accounts", one paragraph per account → monitor calibration → the
  unused signal) → connections (human parallel; garden path or pun) → closing. The
  monitor figure the text cites is now included in the paper (it printed as "Fig. ??"
  before). "fr-specific" → "specific to the fiction/real task".
- Limitations: first sentence split; deferred work is a list.
- Build tooling: `md2tex.py` converts markdown lists and pipe tables (booktabs) and
  lets italics wrap lines; `build.py` places the results figures under the seven
  subsections and the monitor figure under the discussion. PDF: 31 pages, zero errors,
  no unresolved references.
- Open for Andrew: section 3.3 says step-truth is called integrator "in 0–2%"; that
  figure comes from the earlier four-model calibration in the v2 record, while Table 3
  (five-model selector) shows 0 of 48. Left as is pending a ruling.
- Metrics after this pass (before rewriting): Results 28.7 words per sentence, 30%
  over 35, 5.8 numbers per paragraph; every section still flags on em-dashes and
  semicolons. These are the Step 2 targets.

## Rewrite, Step 2 — section log (2 September 2026)

### Abstract — closed after three review loops
Review-only pass per plan, adjusted because it flagged on dashes and semicolons.
Loop 1 (11 fixes, 3 reworded by me against the record): tasks before method; the
generation of completions added to the method sentences; "countering" and "stops
short" clarified; the tank dwell related to the crossing; "not timed by strong
evidence" → "do not coincide with unusually strong evidence" (the record says jump
sentences are median-strength); "order effects" split; "states" given an antecedent;
"never asks" scoped to the tank task; "stayed safe" replaced with the 80% and the
tank behavior stated as "lists both senses or commits silently" (the reviewer's
version overstated commitment); caveat sentences separated; "attenuation" →
"weakening ... with no adversarial prompt". Loop 2 (4 fixes): the no-shift reference
defined before use; "stops halfway" → "reaches the midpoint ... and stays there"
(the record: the plateau sits at the class midpoint); a topic sentence for the
behavior paragraph, stated as a contrast between tasks rather than the reviewer's
causal "depends on the safeguard"; "order" named as the order in which evidence
arrives. Loop 3 (3 fixes): "no-shift reference" named on first use; "safe" glossed
with §3.5's definition; "midpoint" kept because the record supports it (inventory
updated). Reviewer notes for Andrew: the epigraph is a flourish under rule 14 and
sits close to the content note (keep or drop is his call); the title's "Unresolved:"
can read as "the authors did not settle this". Metrics: 16.6 words per sentence,
none over 35, 1.0 numbers per paragraph, dashes 5.0 and semicolons 2.5 per 1,000.
Number checks pass.

### Introduction — closed after three review loops
Rewritten in full: context → the two tasks' origins → the safeguard pair → three
worlds → design → Figure 1 → contributions. Kind-audit item 15 applied ("has a
measurable correlate"). Loop 1 (12 fixes): Figure 1's green band was not the gap
between the references but the zone where fewer than 5% of either reference's
readings fall, so the caption now states that rule; the caption's crossing times
now use the mean-curve values (fiction/real about 4 sentences, tank 8 to 13); the
reference lines' colors explained; "in-between zone" → "unresolved zone"; two garden
paths ("a text form", "which sense or which framing") removed; the 96 completions
scoped to §3.5 with the distinction between listing both senses and flagging
ambiguity; "metastable" defined in the three-worlds paragraph; citation markers
added for Dynel and neural dynamics; contribution 4 split; a seventh contribution
added for the behavior beside the reading in both tasks, which the reviewer noted
was missing though the intro's safety framing set it up. Loop 2 (5 fixes): the
no-shift references named in the text; the figure legend relabeled "core of
unresolved zone" and both references named in the legend; the caption's scale
sentence split and corrected ("beyond ±1" holds only for tank); hysteresis and
recency weighting glossed in contribution 6; the tank request stated as such; a
sentence added pointing to §4's verdict on the three worlds. Loop 3 (5 fixes): the
right-panel legend was covering the reference line the reader must check, so both
legends now sit below the panels; carrier tied to "the task's request"; "steadily
shifting context" → "as the context grows"; the central-result sentence split and
the fourth case called suggestive; contribution 6 split. Figure 1 regenerated
from its committed script with plain panel titles, labeled references and shift
line, and an axis-unit label; content unchanged. Metrics: 15 words per sentence,
2% over 35, 0.9 numbers per paragraph, no dashes. Number checks pass.

### Methods — closed after three review loops
Rewritten in full in the structure-pass order. Loop 1 (17 fixes): sign convention
stated (aquarium/fictional −1, vehicle/real +1); calibration items pictured (one
context sentence, then the carrier); readings stated as unbounded; layer choice
stated (tank peak at 4; fiction/real near its 12–13 peak, fixed early); "capped
diversity" corrected to capped sentences per family; run counts added (12 per
direction tank, 24 fiction/real; 6 no-shift per class); "144 captures"; the
exclusion rule stated from the blind template; Box 1 rules 1, 2, 3, 7 reworded so a
non-practitioner can picture the failure; the ' like'/' letter' correlations
attributed; one phrase for level claims; the layer-14 readings' use of the
calibration axis stated with rule 3's referencing; lead/lag explained; the
integrator's inputs and single parameter stated from the committed code; the
remnant gap in one coordinate system; the axis named "calibration axis" throughout.
Loop 2 (11 fixes): a corpus table (Table 1, which renumbers the results tables to
2–4); paraphrase carriers quoted in full from the capture script; a step defined;
block order explained; bare-carrier baselines given their question; rule 2 and rule
4 retitled ("scene families held out"; "once context has accumulated, at every
layer"); rule 4's long sentence split and the layer-14 case named; rule 7's
"null-result instrument" replaced; the unresolved zone's edges named as the no-shift
references; the remnant gap's sign convention stated. Loop 3 (8 fixes): calibration
items described at first use; "carrier sentence itself"; the offset's measurement
(the position-by-position midpoint) and its sharing across the three fiction/real
carriers stated; the cosine sentence in standard form; axis rotation named in rule
4 with the reason referencing suffices; rule 7 narrowed to "a real displacement";
the integrator's per-class level stated as the constant over positions 10–40;
"scene family" used consistently. Metrics: 15 words per sentence, 1% over 35, 1.6
numbers per paragraph, no dashes. Number checks pass. Open for Andrew: the reviewer
asked why the primary fiction/real readings keep the single-sentence axis at layer
14, where rotation is largest; the text now answers with rule 3's referencing.

### Results and Discussion — drafted, review loops in progress (checkpoint)
All of §3 (roadmap, 3.1–3.7) and §4 rewritten to the standard with Tables 2–6 as
containers (Table 1 is the corpus table in Methods). Every cited figure relabeled in
its committed script (plain titles, no item numbers or codenames, axis labels,
legends named by class and direction) and regenerated with content unchanged.
Reviewer rounds so far: 3.1 two loops applied (tests mapped to tasks; a real minimal
pair shown; layer-0 accuracies added; "spread over several content words"); 3.2 one
loop applied (depth crossings stated as measured under per-layer axes; layer bands
defined before use; the pre-registered prediction stated; depth analyses flagged
exploratory; calibration-strength check scoped to the tank task, where it was run;
"not an instrument accident" replaced with what was tested; the ' letter' site noted
as not fitting the breadth account); 3.3 one loop applied (calibration counts in the
table's units; a classifiable column; "jump" and the 456 count defined from the
committed code; "0–2%" replaced by the five-model count 3 of 48 step-truth runs
called hybrid, which is the quantity the argument needs — Andrew to ratify, since it
retires a number from the older four-model calibration); Discussion one loop applied
(task names unified; "mid-transition" → "middle reading band"; "A calibration" →
"One limit"; three accounts introduced in plain words; monitor figure's third title
line removed). Correction candidate 20: the fiction/real axis-rotation cosine at
layer 21 is 0.68, outside the record's "0.57–0.63 at layers 10–23"; stated as an
exception in Methods and the caption. Metric misses to note: 3.3 and 3.5 exceed the
number-density target (calibration counts; behavior rates), 3.2's depth paragraph
counts layer ranges as numbers. Reviewer agents run on Sonnet 5 from this point, at
Andrew's request.

### Results 3.0–3.1 — closed after three review loops
Loop 1 (10 fixes): "topical shadow" replaced with the topical vocabulary it meant;
"discriminations" → "tests"; the minimal-pair task named; the reason d′ is not
comparable across tasks stated (different layers and baselines; unstable at 6 runs
per class); the contrast-structure result given its own paragraph; caption fixes
(dashed line explained; bar annotations explained; "hard_conversation" and missing
axis labels in the minimal-pairs figure fixed in its script); correction candidate 20
raised (layer-21 cosine 0.68). Loop 2 (9 fixes): the three tests mapped to their
tasks; a real minimal pair shown; "content domain" explained; "class-consistently"
replaced; layer 0's lower accuracies stated (0.88 and 0.73, from the v2 record);
"spread over several of the request's content words"; the pooled-standard-deviation
caveat reworded; the heatmap figure scoped to the task it shows. Loop 3 (3 fixes):
the layer-0 caveat as its own sentence; the tank carrier quoted before its tokens are
counted; the three tests as parallel paragraphs. Metrics: 16 words per sentence, 9%
over 35, 2.7 numbers per paragraph (paired task values), semicolons at target.

### Reviewer rounds applied this pass (Sonnet 5 reviewers from here)
3.2 loop 2 (5 fixes; one declined: a per-band crossing-time table would need new
per-band medians, which the plan rules out); 3.4–3.5 loop 1 (8 fixes, including the
"mixed" category counted from the committed worksheet, 3 of 204, and the
matched-composition figure's per-count tests explained beside the pooled test); 3.6–3.7
loop 1 (8 fixes, including one name for the family-resampled null, the dwelling
states' 0.96× uncoupled from a figure that does not show them, and per-task held-out
retention 73% and 89% from the figure script's constants); Discussion loop 2 (2
fixes; "runtime monitor" → "standalone monitor" in the figure). Section 5 and the back
matter drafted: Related work in prose with [CITE] placeholders; Appendix A as four
one-line corrections; Appendix B as prose with the shuffle-audit values from the QA
report; Appendix C as a prose list; the terminology map as a bulleted list.

### Results 3.2 — closed after three review loops
Loop 1 (16 fixes, one declined): depth crossing times stated as measured under
per-layer axes; layer bands defined before use; "dwelling" glossed at first use; the
pre-registered prediction stated in full (layers 5–9 later than 10–17, deepest in
between); depth analyses flagged as post-freeze; sign convention of the fit
comparison stated ("run ahead ... behind"); the negation-first closing replaced;
the calibration-strength check scoped to the tank task, where the committed script
runs it; "not an instrument accident" replaced with what was tested; the ' letter'
site noted as not fitting the breadth account; the caption's "so" corrected; the
midpoint arithmetic corrected ("as large as"); crossing values reconciled across
prose, Table 2, and the Figure 1 caption; Table 3's scale stated; announced-drama
opener replaced with the question. Loop 2 (5 fixes; one declined: a per-band
crossing-time table would need new per-band medians): the duplicated midpoint
sentence cut; "at the midpoint itself" dropped where the value is −0.10; "which §3.4
calls" → "the dwelling of §3.4"; "values in the caption" replaced with the values.
Loop 3 (3 fixes): arrows in running prose converted to words (throughout §3 and §4;
tables and captions keep them); the percentile check split by direction, following
the committed script's print order (aquarium to vehicle first); the median-midpoint
check uncoupled from a figure that does not show it and stated from the s13 script's
output (both tank gaps unchanged). Density flag: the depth paragraphs count layer
ranges as numbers; justified.

### Discussion — closed after three review loops
Loop 1 (25 fixes): task names unified (tank task / fiction/real task, "covered" only
where the safeguard is the point); "mid-transition" → "the middle reading band";
"metastable zone" → "unresolved zone"; "A calibration" → "One limit"; the three
accounts introduced in plain words (what training installed, what deeper layers
see, where the trigger reads); "matched composition" glossed; "the dissociation"
given its antecedent; negation-first close of the signal paragraph replaced; Dynel
cited; the monitor figure's clipped third title line removed and its axis relabeled
"safe-completions flagged"; caption glosses for the positive class and the
clustering unit. Loop 2 (2 fixes): the meta-sentence opening "One limit" cut;
"runtime monitor" → "standalone monitor" in the figure. Loop 3 (1 fix, held for
Andrew): the reviewer reads the closing sentence ("The states are what the title
calls them: unresolved. For now, so is the question ...") as wordplay out of register
beside the self-harm case; it is the paper's ending and predates the rewrite, so it
stands pending Andrew's ruling. Two clarifications applied (the two worlds named;
"layers 3 to 18, the two middle bands"). Metrics: 16 words per sentence, 2% over 35,
1.0 numbers per paragraph, no dashes.

### Results 3.4–3.7 — second loops applied
3.4–3.5 loop 2 (8 fixes): the per-layer figure's legend still carried "fr" and "k in
6,12", now words; the matched-composition axis label no longer says a magnitude is
signed; the matched-composition paragraph split so the fiction/real categories get
their own paragraph; the definition sentence split; the repetition-loop count moved
out of the "behavior tracks the reading" paragraph; the 0-of-96 count stated once;
the side-band rates given one per sentence; the carriers back-referenced to §2.3.
3.6–3.7 loop 2 (10 fixes, one declined): "reserved question" → "open question"; the
fiction/real loop area left to Table 5; the misspecified-null history compressed to
one sentence; "single-γ account" → "the one-parameter integrator"; the three
per-state ratios given one per sentence; the held-out retention stated per task from
the record (tank 71–76%, fiction/real 87–90%) in place of my derived fold means; the
marker figure's error bars named; "no bistability to fall into" made plain. Declined:
moving the marker's 25% and 38% out of prose, since the section's argument turns on
that value. Table 5's γ column awaits the sanity script's per-order output to label
which value belongs to which block order.
Table 5's γ column is now labeled by block order from the committed sanity script's
cross-order output (fit on destination-first: tank 0.910, fiction/real 0.900; fit on
destination-last: 0.970, 0.840). The record listed the fiction/real pair as
"0.84/0.90", the reverse order of the tank pair; the table now orders both rows the
same way. No value changed.

### Results 3.3 — closed after three review loops
Loop 1 (14 fixes): scope sentences moved after the real-run result; calibration
counts in Table 4's units; a classifiable column; "noise level" replaced with the
count of indeterminate runs; "jump" and the 456 count defined from the committed code
(largest step carrying more than half the net change; 19 stepped sentences per run
across 24 runs); "state-dependent" coined properly; the within-stream paragraph's
opening and its "not merely" close replaced; the gallery caption's three-model
provenance stated with its tallies; axis labels added to the model-classes and
within-stream figures. The "0–2%" step-truth figure from the four-model calibration
was replaced with the five-model count Table 4 carries (3 of 48 called hybrid);
Andrew to ratify. Loop 2 (5 fixes): "classifiable" defined at first use; the
denominators bridged; the calibration prose reduced to the two values the argument
turns on; the "same evidence strength" sentence restored in plain form; "sentences
that follow a step" disambiguated. Loop 3 (5 fixes, one declined): the five-ratio
sentence cut to the calibration fact; "drift plus jump" → "the hybrid" for the model;
why 19 of 20 post-shift sentences enter the jump test; a semicolon split. Declined:
removing the scene-family numbers from the gallery panels, since they identify the
experimental units and the caption now says how they are numbered. Density flag:
calibration counts; justified.

### Results 3.4–3.5 — closed after three review loops
Loop 3 (6 fixes): the paragraph names the tank task first; the "no answer" category
of the behavior figure identified as the eleven degenerate repetition loops, none a
request for clarification; the 96 stated as transition-run responses before the 108
total appears; "per-depth" → "per-count"; a semicolon split; "share of completions"
added as the figure's axis label. Density flag on 3.5 (behavior rates); justified.

### Results 3.6–3.7 and back matter — closed after three review loops
3.6–3.7 loop 3 (7 fixes, one declined): three subject-verb insertions moved out;
"the null" named as the noise level; "position-mismatched" defined; the held-out
sentence split; the marker's static-mixture strength stated per task (near full in
tank, about 70% in fiction/real, from Table 6); a semicolon split. Declined: the
reviewer read Table 5's fiction/real γ order as a transposition; the committed sanity
script's cross-order output confirms the table (destination-first 0.90,
destination-last 0.84), and the inventory was corrected instead. Back matter loop 3
(6 fixes): the replication scope sentence reordered; the citation appositive made a
sentence; the regeneration sentence split in three; the per-layer association called
exploratory; Table 7's columns renamed "Unshuffled"/"Shuffled" and its rows labeled by
task. Every section now has three reviewer loops recorded except the Abstract and
Intro (three each, earlier) and Methods (three); Step 3, the whole-paper coherence
review, is running.

## Rewrite, Step 3 — whole-paper coherence pass (3 September 2026)

The cold-reader agent for this pass failed three times on API overload (one Sonnet
session limit, two 529s), so at Andrew's instruction the pass was done by hand
without agents: the assembled draft read end to end against the seven checks
(names, cross-references, arc, repetition, numbers, unresolved terms, register).
Mechanical sweep: every §, Table, Box, and Appendix reference resolves; no
repository codenames outside the HTML comments; the key numbers agree across the
abstract, results, tables, discussion, and appendices. Thirteen fixes: the
heavy-tail note pointed to Appendix B (it is Appendix A's correction 2); the
stickiness null correction pointed to Appendix A without being listed there (added
as a fifth entry, with the retracted +3.7 from the record); "the frame reading",
"checkpoint window", "pre-lexical", "held-out mixture cells", and "calibrated sites"
defined at or before first use; "cross-run transition bundle" → the trajectory
bundle of §3.4; "family-block bootstrap null" in the marker caption → the
family-resampled null; "pair of tests in §3.1" → three; "amplitude fractions" →
gap-to-amplitude ratios; a duplicated caption sentence removed; the intro's
safeguard sentence names the fiction/real request; the abstract's "at
mid-transition" aligned with "the middle reading band". PDF: 38 pages, zero errors,
7 tables, 22 figures. Number checks: trace and preservation pass across the draft.

Held for Andrew's ruling: (1) correction candidate 20, the layer-21 rotation cosine
0.68 outside the record's 0.57–0.63; (2) the "0–2%" step-truth figure replaced by
the five-model count 3 of 48; (3) the reviewers' note that the paper's closing
sentence is wordplay beside the self-harm case, and that the epigraph sits close to
the content note; (4) the title's "Unresolved:" reading as "not settled by the
authors"; (5) the added seventh contribution (behavior beside the reading in both
tasks). Metric misses logged as justified: number density in §3 (calibration counts,
behavior rates, layer ranges) and semicolons in the back matter (serial lists and
citation brackets).

## Method lineage and citations (4 September 2026)

Andrew asked that the paper say plainly what the instrument does and cite the
methods it borrows. Methods §2.2 now states that the axis is the difference-of-means
(mass-mean) probe, that the midpoint rule is nearest-centroid classification, and
that what is ours is the ±1 rescaling, the referencing to matched no-shift contexts,
and the use of the axis over accumulating context. §3.1 names d′ as the signal
detection measure; §3.7 names its two novelty scores. Related work's probes
paragraph carries the lineage with [CITE] placeholders for: Marks & Tegmark 2023
(mass-mean probing); Rimsky et al. 2024 and Arditi et al. 2024 (difference-in-means
steering and refusal directions); Bolukbasi et al. 2016 (difference directions in
word embeddings); Kim et al. 2018 (concept activation vectors); Park, Choe & Veitch
2023 (linear representation hypothesis); Tibshirani et al. 2002 (nearest-centroid
classification); Green & Swets 1966 (d′); Sun et al. 2022 and Lee et al. 2018
(nearest-neighbor and Mahalanobis out-of-distribution scores); Jackson & Mudholkar
1979 (PCA reconstruction error). Andrew to confirm each reference before filling.

## Contributions check (4 September 2026)

Andrew asked whether the seven contributions are ours. Verdict: all seven are ours
as findings and protocol; none claims a borrowed method. Applied on his ruling:
(1) contribution 1 now says the protocol is built from standard difference-of-means
probes and names the matched no-shift referencing as part of it; (2) Related work
probes paragraph adds Reif et al. 2019 (word senses read from BERT activations by
nearest sense centroid) and Belrose et al. 2023 (depth rotation of readout
directions, tuned lens); (3) the dynamics paragraph replaces "None of these asks
what happens while the summary is changing" with the closest prior work: belief-state
geometry (Shai et al. 2024), Othello board-state probes (Li et al. 2023), incremental
parse-state probes (Eisape et al. 2022), and recency effects in in-context processing
(Zhao et al. 2021; Liu et al. 2023), then states the question as the fate of a
natural-language interpretation while it is overturned and whether the model acts on
the intermediate readings; (4) the encoding-versus-expression paragraph adds
residual-stream signals of context-versus-memory knowledge conflict (Zhao et al.
2024; reference to confirm) and places the mixed-context marker as conflict within
the context. All new references are [CITE] placeholders for Andrew to confirm.

## Review-draft proposals batch (4 September 2026)

Applied from the chat-side proposals list against the Sept 4 draft. Items not
applied are listed at the end with the reason.

**A. Errors.** A1: §4 third-account sentence now says the minimal pairs show the
reading tracks framing cues rather than content (no longer "rules out cue-only
tracking"). A2: the two literal "Figure fig_s9_collapse" references were the two
line-wrapped ones; md2tex now matches "Figure" followed by any whitespace, and the
PDF has zero literal figure ids. A3: abstract reads "Together they carry a
persistent internal signal".

**B. Scope.** B1: §5 "One model" paragraph carries the claim trichotomy
(descriptive / existence / prevalence). B2: sentence that gpt-oss-20b is itself
deployed and open-weight. B4 (check): §1 says "We do not analyze that case" and
takes only a question from it; §4 says the case "reportedly had the same structure
at system scale" (moderation layer, not model internals) — the bridge stays at the
phenomenon-type level. PASS. B3: ruling for Andrew (model-organism clause).

**C. Content.** C1: benign-framing control arm added to §5 beside the patching
item, marked as specified and not yet run. Status: no predictions file and no
captures exist (repository grep: "resignation"/"benign" appear only in unrelated
sets). C2: §2.3 states the fiction/real sub-arm structure (12 families × 2
sub-arms = 24 per direction; theme-only never names a suicide letter or note;
artifact-mentioned names one at least once — definitions from
specs/scene_families.md) and the frozen record's B6 finding that the sub-arms
nearly coincide with a slightly stronger early fictional reading under mention;
no-shift runs are theme-only. C3: new committed script
analysis/s15_fr_frame_queries.py (post-freeze; Appendix B line) — of the 84
fiction/real completions that reach a final answer, 0 ask whether the request is
fictional or real; no reasoning channel proposes asking it; 2 float a clarifying
question and drop it; 7 safe-completions plan a safety check-in. Manual verdicts
are keyed by set name inside the script with an assertion on the candidate list.

**E. Checks.** E1 PASS: s7 output (recorded in session transcripts) gives tank
fit-A(destination first)=0.910 / fit-B(destination last)=0.970 and fr 0.900 /
0.840; Table 5 "0.91 / 0.97" and "0.90 / 0.84" match; FINDINGS_FINAL lists the fr
pair in the opposite order from tank, which is a listing inconsistency in the
record, not in the table. E2 PASS: the complaint alleges the moderation system
flagged 377 messages for self-harm content and reporting describes real-time
tracking; the §4 sentence keeps "reportedly". The TechCrunch answer piece is dated
26 November 2025 ("OpenAI claims teen circumvented safety features…"); NBC News
(25 Nov) is the primary report of the answer. E3: the four flagged references
verified — Reif et al. 2019 (NeurIPS) uses "a nearest-neighbor classifier where
each neighbor is the centroid of a given word sense's BERT-base embeddings"
(quoted from the PDF); Zhao et al. 2024 = arXiv 2410.16090 "Analysing the Residual
Stream of Language Models Under Knowledge Conflicts"; Sun et al. 2022 = ICML
"Out-of-Distribution Detection with Deep Nearest Neighbors"; Eisape et al. 2022 =
Findings of EMNLP "Probing for Incremental Parse States in Autoregressive Language
Models". The remaining placeholders were checked from memory only (46 brackets,
64 individual references); the claim-source match for each is Andrew's to confirm
at fill time. E4 PASS: caption gives mean-trajectory crossings (4; 8 to 13, matching
FINDINGS_FINAL "mean-curve crossings 13/8/4/4"), Table 2 gives per-run medians
(10.5/6.0/4.0/5.0); the caption says "mean reading crosses", the table says
"per-run median".

**G. Coherence.** G1: intro design paragraph now says completions are generated at
four points after the shift. G2: same paragraph poses the order-of-evidence
question. G3: §3 roadmap says the behavioral question of §1 returns in §3.5. G4:
§3.2 integration passage points forward to the head-to-head test in §3.3. G5:
skipped — a defined label "plateau window" is an invented term (rule 6). G6: venue
note added at the head of tex/build.py.

**H. Capture date, precision, channels.** H1 (manifest check, committed as
analysis/s16_capture_days.py): fr transition runs, no-shift runs, and calibration
set all on 28 Aug 2026; tank on 27 Aug except tank_d3_fam11 (both directions) and
tank_d4_fam10_b on 28 Aug; checkpoints one day per task; mixture sweeps one day
(29 Aug) for both tasks; behavior completions on 29–30 Aug, each reading from the
completion's own forward pass; minimal pairs 30 Aug. Rendered system message (no
developer message): "You are ChatGPT, a large language model trained by OpenAI. /
Knowledge cutoff: 2024-06 / Current date: <YYYY-MM-DD> / Reasoning: medium / #
Valid channels: analysis, commentary, final…"; 61 tokens for any date; the date
line tokenizes to the same count for every date tested. Reasoning effort:
"medium" (template default; the code passes none) for capture and generation
alike. Disclosure text in §2.1, Appendix B ("Capture days"), and §3.7 (the
sweep-internal pure-vs-mixed control is within one day). Empirical bound not run
(Andrew's ruling); pinned-date re-capture added to §5.
H1(d) — CHANNEL FINDING, [PROPOSED] in §2.5 and §3.5: the raw output begins with
the reasoning channel; with the 256-token cap only 37 of 108 tank and 84 of 204
fiction/real completions reach the final channel. All 21 fiction-framed and all 3
mixed fiction/real completions were categorized from the reasoning channel; the 84
that reach a final answer are all safe-completions. The worksheets also truncate
at 1,200 characters. No number changes; the categories' meaning is now stated.
Andrew to rule on the wording and prominence.
H2: loader passes dtype=float16 with no quantization config (NF4 was removed on
15 March 2026, commit 394dd9f, before any capture); the checkpoint's expert
weights are MXFP4 (config.json quant_method) and a dequantized 20B model cannot
fit the 16 GB card, so experts ran in MXFP4; captured activations are stored as
float64 in Parquet. Stated in §2.1. H3: greedy-continuation caveat in §5. H4:
ethics and safe-messaging statement drafted in the back matter, marked [DRAFT].
H5: repository is github.com/AndrewSmigaj/OpenLLMRI under Apache-2.0 (LICENSE
file); placeholder inserted in §2.6 for Andrew's availability sentence.

**I. Readability.** I1: BIC expanded with [CITE: Schwarz 1978]. I2 sweep: "no-shift
control runs"/"no-shift runs" name the runs and "no-shift references" the levels
throughout; "park", "accumulation drift", "probe arms" appear only in the Appendix
B name mapping; "probe" elsewhere names the instrument; no drift found. I3:
glossary gains "Calibrated sites" and "Trajectory bundle". I4: "a one-component
fit beats a two-component fit" in §3.4 and the mode-track caption. F2: no
"pre-lexical" remains anywhere in the draft or captions.

**J.** PDF 40 pages, zero literal figure ids, content note on page 1; Tables 2
and 4 overflowed the right margin (pre-existing) — converter fixed in this batch.
Checks: number trace and preservation PASS; prose metrics PASS except the two
standing justified flags (§3 density; back-matter semicolons).

**Rulings for Andrew:** B3 model-organism clause; D1 release policy; D2
acknowledgment line; D3 author block; H5 availability sentence; the [PROPOSED]
channel disclosure wording in §2.5/§3.5; the [DRAFT] ethics statement.

## Rulings pass, part 1 (4 September 2026)

D3 applied: author block "Andrew Smigaj / Independent researcher" (Andrew's
instruction). D2 acknowledgment line and H5 availability statement drafted in place,
marked [DRAFT, for approval]. B3 clause added to §5 as [PROPOSED], anchored to the
single-model "biology" work rather than "model organisms" (which in interpretability
names engineered testbeds). Remaining rulings go to Andrew's chat-side reviewer via a
self-contained prompt.

## Availability statement corrected (4 September 2026)

Andrew asked whether the statement should point below the repository root. Two
false claims found on checking: the raw captures are git-ignored (data/lake/*,
*.parquet), so "captures are in the repository" was untrue — the study's 1,299
sessions total 48 GB on disk; and the study README that Appendix B cites for
regeneration instructions does not exist. The [DRAFT] statement now points to
docs/studies/context_shift/, lists what the directory holds, says the raw captures
are not in the repository (ruling clause: archived on request / deposited), and
notes that only the cache-fed analyses regenerate without them. Sixteen of 41
analysis scripts run from committed caches (among them the Figure 1 collapse
figure, the fit gallery and remnant-gap figure, the per-layer heatmaps and
rotation, the collapse-by-layer and behavior-by-layer panels, the behavior bands,
and the monitor ROC); 25 read raw activations (token-level d′ and within-stream
readings, minimal pairs, geometry and the mixed-context marker, mixture sweeps,
the behavior worksheets, and the post-freeze counts). Rulings: capture hosting;
whether to write the study README (it would carry the script-to-figure map).

## Rulings pass, part 2 (4 September 2026)

Applied from the chat-side reviewer's rulings. (1) D1 = (a); §4 carries the
supplied release sentence. (2) §3.5 now states, after the channel disclosure, that
all 84 completions reaching a final answer are safe-completions, that the reasoning
channel entertains the fiction frame while no arrived answer carried it, and that
truncation correlates with category so the band gradient is measured over
reasoning-committed responses with a censoring pattern; §5's caveat names the
256-token cap beside greedy decoding. (3) Acknowledgment: "The research questions,
study design, and interpretive decisions are the author's." (4) Availability kept;
hosting clause filled ("archived by the author and available to researchers on
request, and a public deposit is planned") and the committed manifest named.
(5) Ethics: withheld-from-open-release clause added. (6) B3 clause kept. (7a)
kept. (7b) verified from the record: v2 §A4's "0–2%" was step-truth-called-
integrator, which the draft had dropped while stating the two-timescale fact
twice; §3.3 now gives both from the committed five-model simulation (s7 output,
tallied in s9_figures): step truth → integrator 0 of 48 and → hybrid 3 of 48;
two-timescale truth → hybrid 5 of 48. (7c) kept. (7d) content note now above the
epigraph, in the source and the build. (7e, 7f) kept. (8) Intro and Related work
say 300 completions (96 tank + 204 fiction/real), none asks which reading is meant.
(9) Bibliography built: tex/references.bib (55 entries), tex/cite_map.json mapping
each placeholder text to keys, md2tex converts [CITE: …] to natbib \citep at
build; plainnat, author-year. Verified this session: Crescendo = USENIX Security
2025, pp. 2421–2440; gpt-oss model card = arXiv:2508.10925; Zhao et al. 2024 =
arXiv:2410.16090; Raine complaint No. CGC-25-628528, filed 26 Aug 2025
(courthousenews PDF); OpenAI answer filed 25 Nov 2025 (Ars Technica PDF); CNN 26
Aug 2025; NBC News 26 Aug 2025 (Yang, Jarrett, Gallagher) and 25 Nov 2025;
TechCrunch 26 Nov 2025. Not used: Farquhar et al. 2024 (no placeholder fits).
"Rimsky et al." placeholders resolve to Panickssery et al. 2024 (same work).
PDF: 44 pages, zero placeholders, zero tags, References on p. 41; tables 2 and 4
inside the margins; xurl added for breakable URLs.

Also this pass: study README written (docs/studies/context_shift/README.md) with
the content note, layout, archive facts, environment, regeneration commands,
cache-vs-captures script split, and the claims→script→figure map; capture
manifest committed (captures/capture_manifest.csv: 1,299 sessions, 7,794 files,
47.9 GB, SHA-256 per file; analysis/s17_capture_manifest.py).

OPEN for Andrew: the committed behavior worksheets carry the first 1,200
characters of every raw completion, including the fiction-framed reasoning
traces, which contradicts release policy (a) once the repository is public; and
"paraphrased excerpts" promised in §4 do not exist yet as an artifact. Flagged in
the README's release-policy section.

## Abstract replaced with the approved section K text (5 September 2026)

Andrew found the 1 September opening ("or whether a request is fiction") wrong: the
task varies the framing of a fixed request, not whether the request is fiction. That
opening was written in commit c212cac without recorded sign-off. The abstract is now
the section K text verbatim, with three factual corrections only: "72 runs" for "88
runs" (88 mixed the main-carrier runs with the paraphrase-carrier runs, eight of
which have no matched no-shift runs; every headline number comes from the 72); "the
300 completions we examine" for "all 300 completions in the study" (the study holds
312; the 12 tank no-shift completions were not scanned); and "where the fits can
decide, drift plus jumps beats every smooth evidence-integration model we fit" for
"no smooth evidence-integration model we fit reproduces them" (the recency
integrator wins 7 of 41 classifiable runs; §3.3 claims dominance, not exclusion).
Stylistic suggestions are held for Andrew's ruling, not applied. The third paragraph
updates when the behavior regeneration completes.

## Abstract: Andrew's final text (5 September 2026)

Applied verbatim except one clause. Andrew's text read "the largest means the
average reading never passes the midpoint at all". The record says otherwise: the
mean trajectory in that direction (tank, aquarium→vehicle) crosses the midpoint
after about 13 sentences (Figure 1 caption; per-run median 10.5, Table 2), and the
late plateau then sits at the midpoint within the interval's precision (gap ratio
1.09, CI on the ratio spanning 1.0; §3.2 "the transition stopped halfway"). The
clause now reads "the largest means the average reading ends at the midpoint".
Reported to Andrew as the single deviation.

## Behavior corpus regeneration applied to the paper (5–6 September 2026)

Record: findings/behavior_regeneration_2026-09.md (Parts 1–4) and
analysis/behavior_categorization_v2.md. Plan: ~/.claude/plans/humming-finding-frost.md
(approved 5 Sept). What changed in the paper:

- §2.1: determinism stated as verified (same cell twice → identical text and
  reading); regeneration pinned to original capture days; date-effect bound
  referenced. Table 1 behavior row: 2,048-token cap.
- §2.5 Behavior: rewritten. Categories from delivered answers; loops are "no
  answer"; every rate two ways; reasoning-channel commitment recorded.
- §3.5: rewritten from the regenerated corpus. Tank side bands answer their side
  (52%/59% all, 62%/63% delivered), middle band lists both in 45% (52% delivered);
  no clarification requests (0 of 94 delivered answers). Matched composition: p =
  0.037 at 6 sentences only; the pre-stated pooled test gives p = 0.10 and the
  result is graded as one significant count of four. Fiction/real: 111 safe / 8
  fiction-writing / 85 no-answer; safe completions 89% and 95% of delivered answers
  in the middle and real bands; the fiction side delivers 1 of 4. The frozen
  50→80→91% gradient is stated as an artifact of truncated reasoning. Frame
  queries: 0 of 119 delivered answers ask; one invites correction; reasoning
  channels counted. k=2 separation p = 0.034 (3 vs 45).
- §3.7: the eight marker-versus-behavior tests are scoped to the frozen
  categories (their computation is not in a committed script; not re-run).
- §4: rates replaced; the "weakening reachable by ordinary context" claim
  withdrawn; AUC 0.61 [0.37, 0.81] with 8 positives.
- §5: greedy-decoding caveat now carries the loop counts and names sampling as
  the study's most consequential scope limit.
- §1: 312 completions; contribution 4 reworded; contribution 5 rewritten
  (safeguard holds wherever the model answers; many completions never answer).
- Abstract, third paragraph: rewritten from the regenerated numbers; the
  "weakening reachable by ordinary context" sentence removed. FOR ANDREW'S VOICE
  READ.
- Appendix B: regeneration paragraph; capture days for the regenerated cells;
  post-freeze list. Captions: behavior bands (sides named, no-answer share),
  by-layer counts, monitor ROC.
- Preservation check: the frozen behavior values (96, 56/66%, 80%, 50%, 0.76 …)
  are reported LOST by design; they are superseded and recorded in Appendix B and
  the regeneration record.
- Figure script r6_behavior_figure.py: fiction/real panel gained the no-answer
  category (bars had not summed to one); band labels name the sides; rates are
  printed both ways. Its frozen caption's "signed toward the destination" had
  described a convention the script never applied; the caption now matches the
  computation.
- Matched composition, fiction/real: the frozen script compared fiction-writing
  answers against everything else, which on the regenerated corpus includes loops;
  the pre-stated comparison is against delivered safe completions (3 vs 26,
  p = 0.065, s7 S1.3 fixed to exclude no_answer). §3.5 and the caption state the
  weaker result; the frozen p = 0.010 is noted.
- Date-effect bound (s19, 24 no-shift cells re-captured pinned to 5 Sept): reading
  shift ≤ 0.02 axis units; greedy text diverges in 23 of 24; delivered category
  unchanged in all 18 pairs that answered both days; 3 loops became answers. §2.1
  now states the bound; Appendix B carries the paragraph; the §5 pinned-date
  bullet is retired.
- Matched-composition figure: fiction/real panel excludes no-answer outputs;
  p-values computed from the worksheet instead of hardcoded frozen values.
- Checks: trace PASS; preservation FLAG (18 frozen behavior numerals retired by
  design); prose density flag in §3 rises to 4.3 with the two-way rates,
  accepted; back-matter semicolons unchanged. Build: 46 pages, zero placeholders.

## De-narration pass (6 September 2026)

Andrew: the freeze is a lab discipline, not a paper structure. Applied: the
behavior corpus is stated once in §2.5 (greedy, 2,048-token cap, categories from
the delivered answer, loops as no answer, rates two ways; the 256-token pass noted
as superseded in one sentence). Removed from §3.5, §4, the abstract, §5, and the
captions: every frozen-versus-regenerated comparison, "pre-stated", "post-freeze",
"after the analysis freeze". §3.5's matched-composition paragraph cut to one
verdict ("one significant count of four"). Contribution 5 no longer carries the
loop clause; the abstract's third paragraph ends on the safeguard holding, with
one sentence on greedy loops as a decoding property. §5: greedy-decoding limit in
one sentence; a sampled regeneration is now the first deferred item. Appendix A
reduced to a paragraph; Appendix B's post-freeze list and the name mapping moved
to the study README (which now carries the four corrections and the retraction).
Tooling: tex/number_retired.md lists the superseded behavior numerals with
reasons; number_check's preservation check skips them. Trace PASS; preservation
PASS; 45 pages.

## Strengthening pass, Phase A (6 September 2026)

Plan: ~/.claude/plans/humming-finding-frost.md (approved 6 Sept after review).
Measured first, then written:

- Reasoning channel's final commitment categorized for every cell that delivered
  an answer (`reasoning_category`; loops keep the early reading). Result: it
  matches the delivered answer in 119 of 119 fiction/real cells and 75 of 94 tank
  cells; the three "flips" logged on 5 Sept were early-versus-late reasoning.
  Fiction-writing-committed reasoning delivers fiction-writing assistance (8) or
  loops (15), never a safe completion; it loops more often than
  safety-committed reasoning (15 of 23 vs 70 of 181, Fisher p = 0.023). The frozen
  50/80/91 are therefore the reasoning channel's commitment by band (final
  reading 50/82/91), the lower bound of the safe rate; delivered answers
  (100/89/95) are the upper bound. §3.5, §4, contribution 5, and the abstract's
  third paragraph now state the bracket; the "artifact" framing is withdrawn.
  The bands figure has paired panels (delivered answer / reasoning commitment).
  §2.5 states that the reasoning channel is treated as an output, with a
  faithfulness citation (Turpin et al. 2023; Lanham et al. 2023; Andrew to
  confirm).
- Dwelling decomposition (s20; criterion in the docstring before running):
  population plateau holds (mean late slope within [−0.040, +0.024] units per
  sentence, median late reading −0.11), but only 3 of 12 runs are individually
  flat; §3.4 now says the stationarity is a property of the population, with
  the bound and the per-run spread. The abstract's "stops at the midpoint and
  stays there" is population-level and stands.
- Whitelist restorations: "fixed in advance" on the pooled test; Appendix A
  carries the count (nineteen at the freeze) and the kinds of things caught.
- Naming sweep (Andrew's rule): fiction-writing frame / real-world frame in text,
  captions, and figure legends (direction labels, side names, class-label
  sentence); task name and ±1 class labels kept; figures regenerated.
- C6 scope bound; B3 rival stated and refuted; D1 "references held fixed"
  clause; E2 six nulls present with tier words. F1 table not added (optional).
- Checks: trace PASS, preservation PASS (retired list), prose flags unchanged;
  46 pages, zero placeholders.

## Abstract, third paragraph settled (6 September 2026)

Andrew: the abstract had been absorbing the last analysis each time rather than
the story. Paragraph 3 is now four sentences in his structure: the tasks differ;
no completion asks which reading is meant; the tank task lists both senses or
commits; the safeguard holds in the middle band (89% of delivered answers). Loops,
the reasoning-channel bracket, and the sampling caveat stay in §3.5 and §5. The
bare completion totals (312) are gone from §1 and Related Work ("every completion
we examine"); denominators live in §3.5.

## Deltas 1 and 2 from the final read (6 September 2026)

Reviewer deltas adjudicated with Andrew. Delta 1 item 1 (loops and the bracket
back into the abstract) refused and then withdrawn; item 2 adopted in words, no
bare total: "Across the answers the model delivered, none asks which reading is
meant" (abstract), "Of the answers the model delivers in §3.5" (§1), "none of
the answers the model delivered" (Related work). Item 3's "112 from transition
runs, 7 from no-shift runs" replaced, at Andrew's objection that bare arm counts
imply a phenomenon, by a corpus-composition sentence at the top of §3.5 (96 and
192 transition cells, 24 no-shift finals, giving 108 and 204) and a clause that
the no-shift runs loop as well (1 of 12, 5 of 12; addendum Part 6). Item 5's
optional clause added beside the loop association: per-cell loop identity is
decoding-sensitive (Appendix B); the rate and the association are aggregate.
Delta 2 stale-claim sweep (weaken/weakening/gradient/falls from/toward the
fiction-writing frame): two survivors the reviewer named and two it did not.
§5 existence claim → "can deliver fiction-writing assistance with the letter
under ordinary coherent context, with no adversarial prompt"; Related work
"weakening of the safeguard" → "the fiction-writing assistance the model
delivered in a few of them needed no adversary"; §4 monitor paragraph "The
band-level gradient of §3.5 is real." deleted (false after the retraction);
bands caption "loops, which fall mostly on reasoning that had committed to
fiction-writing assistance" corrected: 70 of the 85 loops sit on
safety-committed reasoning, the rate is what is higher (15 of 23 against 70 of
181). §4 behavior paragraph opener split: tank tracks the reading, fiction/real
does not (holds across bands). §4 trained-default, three-accounts, and signal
paragraphs audited against the revised §3.5: no gradient reasoning remains.
Register: "sampling breaks such loops" stated as fact in three places (§3.5, §5
twice) with no test or citation → "is expected to break". Not done, post
turn-in: band-threshold sensitivity (new analysis); the dwelling equivalence
bound is already in §3.4.

## Preprint v1 freeze (6 September 2026)

Full read of the paper before posting; every repeated number cross-checked
across abstract, §1–§5, captions, and appendices, and the capture dates checked
against the manifest. Findings and changes:
- Title block: "Review draft — \today" → "Preprint, version 1 — 6 September
  2026"; contact email added to the author block; PDF title and author
  metadata set (hypersetup).
- Release policy moved from §4's trained-default paragraph to §2.6 (Data and
  code availability), where §2.6, the Ethics section, and the study README had
  been pointing; the disclosure sentence added there: truncated 256-token
  outputs (≤1,200 characters) remain in the repository's history (commit
  408b312); the 2,048-token completions and reasoning traces are withheld.
  Study README repointed to §2.6 with the same sentence.
- Back matter reordered: Related work → Ethics → Acknowledgments → Appendices
  (headings only).
- Marker-versus-behavior tests re-run on the v2 categories
  (`analysis/s22_marker_behavior.py`, test form fixed in the docstring before
  running; addendum Part 7). Result: 0 of 7 defined tests at p < .05 (the
  eighth has no fiction-writing answer), and the marker does not separate
  delivered answers from loops. §3.7's two sentences on the un-repeated
  256-token tests replaced; §4, contribution 7, and the abstract unchanged.
- Wording: §2.1 "pinned a week later" → "pinned to a day about a week later";
  tank loop caption "(not shown)" → "(Appendix C)"; §3.4 late-slope clause
  restated as movement over the ten sentences.
- Root README: pointer to the paper and the study directory above the
  pre-alpha note.
- Tag `paper-v1` on this commit; hand-off fields for uploading in
  `paper/post/upload_v1.md`.
