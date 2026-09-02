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
