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
