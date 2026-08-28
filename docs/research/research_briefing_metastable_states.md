# Research Briefing: Representational Transition Dynamics and Metastable States (v2)

**Program:** Scaffold Dynamics / OpenLLMRI
**Status:** Active. This document is the shared context for AI collaborators on this project.
**Version:** v2, 2026-08-28. Supersedes the 2026-08-27 original. Additions: superseded-framings section, population doctrine as a standing section, unresolved-zone test battery, decisions register for drift assessment. The repo copy may contain further iterations made on the repo side; reconcile via the decisions register below, flagging conflicts rather than silently rewriting.

## What we study

We study how an LLM's contextual understandings form, shift, and fail to consolidate, as read from the residual stream. When context changes (aquarium tank to vehicle tank; friend to foe; fictional framing to real framing), the representation of the relevant concept moves. Our prior observations: before a shift, representations sort into high-purity groups under our lenses; after a shift, tokens drift, bounce, linger between groups, and often never fully consolidate into the new one. The alignment stakes: we have a motivating case where a safety-relevant behavior failed after a long fictional context shifted to a real one, and we hypothesize the lag (hysteresis) in the frame representation is part of why. What we know for certain is only that the safeguards failed on certain models; the representational account is the hypothesis under test.

## Vocabulary (operational definitions)

- **Lens:** a dataset-defined contrast. Datasets are constructed (by a project-blind LLM) so that everything varies as much as possible except one target opposition. The dominant structure the lens reveals is, by design, that opposition.
- **Conceptual separation space:** the UMAP-reduced space plus clustering computed per layer for a given lens. Not a model of raw geometry; a detector of separation.
- **Transition / confusion zone:** the region and period after a context shift where tokens read between the two groups.
- **Hysteresis:** the state depending on history, not just current input. Same final sentence, different context history, different reading.
- **Metastable state:** a candidate stable-ish intermediate region between two opposing understandings. Existence not yet established. Central object of the current inquiry.
- **Unresolved band:** the middle region of the calibrated axis between the two understandings. Defined only by a rule fixed in advance whose numbers come from data (see battery below). Behavior labels never enter its definition.

## Superseded framings (read before touching older material)

Older drafts, docs, code comments, and variable names in this repo predate the August 2026 redesign. Where they conflict with this briefing, this briefing wins. Specifically:

- **"Attractor basin" as an established framing: retired.** The descriptive term is now hysteresis. Basin-like structure is one *possible outcome* of the hysteresis loop experiment (direction-dependent crossing points), never an assumption or a background fact. Do not write new prose, docstrings, or names that present basins as established.
- **"Engagement capture" / persona persistence / Waluigi framing: dropped.** AI-originated in an earlier session, provenance untraceable, unverified. Do not carry it forward in any form.
- **KV-cache material: cut from this paper.** Lives in the ideas file only.
- **UMAP-space measurements: demoted to discovery.** Any existing metric computed in UMAP coordinates, including the +1/-1 centroid trajectory, is discovery-instrument output. Do not quote its numbers as quantitative claims; the raw-axis projection replaces it for all measurement.
- **Legacy dataset recipes: tagged, not used.** Data generated before the friend/foe-era pipeline is legacy; new claims come only from current-pipeline data on the harmony format.

When you find occurrences of the retired framings in existing files, flag them in a list for Andrew; do not silently rewrite them.

## The central open question

When a token reads "between" the two concept groups, which world are we in?

1. **Learned intermediate state:** the model has a genuine, reusable representation for the mixed/uncertain condition. Predictions: the middle is a recurring, stable region across runs and datasets; a third mode appears in properly measured distributions; middle-occupancy has its own downstream behavioral signature.
2. **Transitional passage:** the middle is merely traversed. Predictions: fast crossings, low dwell time, thin occupancy, no stable third mode.
3. **Off-manifold or projection artifact:** the between-ness is a byproduct of the input pushing activations off the learned manifold, or an artifact of the reduction itself. Predictions: between-ness in the projection without corresponding structure in raw space; high distance from the training-like activation distribution; instability across projection hyperparameters.

Distinguishing these is the research program. Do not assume any of them in write-ups.

## Two-instrument doctrine

- **Discovery instrument:** UMAP + clustering (the lens), color blending for secondary variance, Sankey routing, expert-selection pipelines. Use freely to explore, flag anomalies, find unexpected structure, and tell the story. Between-cluster and outlier points get flagged, never force-assigned.
- **Measurement instrument:** raw-activation-space projections. For each lens, compute the difference-of-class-means axis (or a logistic-regression probe) from labeled unambiguous endpoint data, using all dimensions with no neuron thresholding. Project every token onto this axis. All quantitative claims about discreteness, intermediacy, dwell time, and transition dynamics are computed here. Dimensions orthogonal to the axis contribute zero, so this is the noise-suppressed raw-space lens.
- **Rule:** UMAP evidence licenses separation, context-driven formation, and shift detection. It does not license claims about discreteness vs continuum or about raw-space between-ness. Those require the measurement instrument.

## Population doctrine (governs every distribution claim)

- **Endpoint sets** (designed, unambiguous, bimodal by construction): they CALIBRATE. They define the axis, pin the +1/-1 normalization, and establish separability. They NEVER feed a discreteness or modality test; their bimodality was installed at generation time, so finding it proves only that the generator worked.
- **Transition-window occupancy** (post-shift tokens from long-context runs): this population's positions were produced by the model's dynamics, not by our labels. ALL discreteness, modality, and habitability claims are tested here.
- **Graded-evidence inputs:** used ONLY in the hysteresis sweep, where evidence strength is the independent variable.

## Unresolved-zone test battery (added 2026-08-28)

Two extensions, both pre-registered in the predictions file before any capture. Pre-registration fixes procedures, not numbers; the data supplies every number through the fixed rule. The one forbidden ingredient anywhere in zone definition is the behavior labels.

**1. Off-manifold vs unresolved learned structure.** For transition-window tokens, alongside the dip/trimodality test:

- (a) Distance from the on-manifold reference distribution (endpoint plus no-shift activations), per layer: Mahalanobis or kNN distance.
- (b) Reconstruction error against a low-rank subspace fit on on-manifold activations.
- (c) Recurrence check: whether the middle region reappears in the same place across paraphrase families and seeds.
- (d) Router signatures: expert-routing distribution and entropy through the transition.

Learned structure predicts: normal manifold distance, low reconstruction error, recurring location, a distinctive stable third routing pattern. Off-manifold predicts: elevated distance and reconstruction error, scattered location, routing entropy spikes / flickering / fallback-expert behavior.

**2. Unresolved-zone occupancy and behavior.** Primary endpoint is the continuous output-probability measure (probability mass toward compliance vs refusal at generation start), available on every run and immune to event rarity: regress it on the probe reading at the last pre-generation token, scenario-clustered statistics. Pre-registered hypothesis: compliance probability rises as the reading approaches the middle of the axis. The binary safeguard outcome is secondary and gated: the predictions file fixes a minimum failure-event count before the binary test runs (heuristic: roughly ten events per predictor for logistic regression, counted at scenario level). Secondary, for figures and crisp claims: a band defined by a rule fixed in advance, width supplied by data. Rule options, in order of preference: (a) probe-posterior uncertainty region, cutoff set so that at most 5% of endpoint tokens fall inside; (b) the interval between the inner 95th percentiles of the two endpoint distributions; (c) if the trimodality test finds a middle mode, the middle mixture component's support. Sensitivity sweep over the cutoff reported alongside any band result.

**Honesty guard and reporting tiers (fixed in advance):** what we know is that safeguards failed on certain models, under conditions that are hard to replicate and likely conjunctive. Outcomes report as exactly one of:

- **Link supported:** effect estimate with confidence interval, on whichever endpoints were testable.
- **Powered null:** event floor met, precision adequate, interval tight around zero. Only this tier may use the word "dissociation."
- **Untestable here:** event floor not met. Report the observed event count and rate with its interval; no dissociation language. An underpowered null is absence of evidence, not evidence of absence.
- **Out of reach on this model:** if the study model's safeguards fail at no measurable rate, the binary link is not null, it is untested on this model; the claim narrows to the continuous gradient and says so.

All behavior designs are enriched toward the failure-prone regime by construction (long fiction-to-real contexts), so conditional associations are estimable and base rates are not; never quote a failure rate from these samples as a base rate. The previously observed dissociation (frame reading collapsed while refusal held) stays on record as a finding from that run, not as a prior that any new null automatically confirms.

## Current work queue

1. Diagnostic: determine exactly what the existing raw-space mode computes. If it is full-dimensional distance-to-centroid, replace with axis projection before drawing any conclusions from its messiness.
2. Build the per-layer diff-in-means axis from existing labeled endpoints; renormalize endpoints to +1/-1 to preserve our coordinate convention.
3. Produce the dual-trajectory figure: the same transition plotted in UMAP coordinate and raw-axis coordinate. This is the key credibility artifact.
4. Distribution tests along the axis: Hartigan dip test for unimodality; check for trimodality (candidate metastable middle mode). Per layer. Population doctrine applies: transition-window occupancy only.
5. Statistics at scenario level, never token level (tokens within a scenario are correlated; cross-validation splits never share a scenario).
6. Maintain a log of which datasets produce island-like separations vs split-spread separations in the lens; this variation is itself data for the central question.

## Decisions register (late Aug 2026, for drift assessment)

Reconcile the repo against this list. Anything in the repo that conflicts gets flagged, not silently rewritten. Pointers name where each decision lives in full.

1. Hysteresis replaces basin language; metastable = tested hypothesis; three worlds never assumed (this doc).
2. Engagement capture / persona persistence / Waluigi dropped; KV-cache out of this paper (this doc; Plan v2 out-of-scope list).
3. UMAP metrics demoted to discovery; all measurement on the raw axis (this doc; Plan v2).
4. Population doctrine: endpoints calibrate, transition windows testify, graded inputs only in the hysteresis sweep (this doc; Plan v2).
5. Predictions file dated and committed before any Phase 2 capture (Plan v2 Step 0).
6. Hysteresis loop: graded evidence via mixture proportion (k of N context sentences supporting regime B), swept both directions, loop area = stickiness (Plan v2 item 5; Probe Design D6).
7. Router/expert entropy logged as second observable through every transition (Plan v2 item 9).
8. Scenario-level statistics everywhere; CV splits never share a scenario (Plan v2 item 1).
9. Anchor sites: per-carrier pre-lexical and request-word sites plus the full position scan (Plan standards; Probe Design section 2).
10. Data standards: friend/foe-era generation pipeline only, legacy data tagged and never mixed; harmony format everywhere; calibration and applied data share identical format/tokenization, recalibration on any format change (Plan standards; Probe Design section 5).
11. Polysemy target analysis restricted to aquarium/vehicle clusters via the transparent restriction protocol: labels from dataset construction, out-of-target fraction reported, other clusters described as discovered secondary structure (Plan v2 item 2).
12. Probe Design v1 decisions (2026-08-27 doc, in repo): scene-context rule (the word "tank" never appears in tank transition contexts; the carrier's occurrence is first), D1a/D1b split (5-way lens vs aquarium/vehicle axis calibration), unified capture geometry (varied context plus fixed verbatim carrier), carrier strings pending Andrew's sign-off.
13. Probe Design review outcomes (2026-08-27, this conversation), MANDATORY: at the final step of every D3/D4 run, capture ALL token positions in that pass, not just the carrier span; the within-stream token trajectory is the population for the volatility claims and the dip test, while the step-wise carrier curve measures frame evolution, a different thing. Also: add a fourth non-chore tank carrier (T1-T3 all share the maintenance frame); add the garden-path join audit (manual reads to catch accidental syntactic fusion at assembly joins) to the pre-capture audits.
14. Unresolved-zone test battery and continuous-first behavior analysis with data-driven band rules; behavior labels never enter zone definitions (this doc, 2026-08-28).
15. Layer-by-position heatmap = Tier 2; dense-model replication = stretch (Plan v2 items 12-13).

## Scaffold Dynamics line of inquiry

The conceptual exploration operators (including frame collisions) deliberately induce shifts and collisions between framings. Working hypotheses, to be tested later, not asserted now: productive out-of-the-box generation may correspond to controlled visits to intermediate regions; scaffolding may act as an external resolution mechanism the architecture lacks, shortening confusion zones and re-routing to appropriate behavior (including safeguards). Prerequisite for all of this is the measurement capability above: we cannot study visits to metastable states until we can establish whether and where they exist.

## Ground rules

- Sloppy in generation, strict in measurement. Hypotheses and metaphors flow freely in exploration; every published number comes from the measurement instrument.
- Anomalies (between points, third clusters, purity asymmetries between probes) are flagged and logged as hypotheses, not folded into conclusions.
- When the two instruments disagree, that disagreement is a result to investigate, not a nuisance to hide.
- Claims calibrate to evidence. "The lens shows X" and "the raw axis confirms X" are different sentences; use the right one.
- Endpoint sets calibrate; transition windows testify. Behavior labels never enter any zone or band definition.

---
# REPO-SIDE RECONCILIATION ADDENDUM (2026-08-28, appended by the repo-side collaborator)

In-session decisions by Andrew that supersede or extend register items above. The other AI's
copy should converge on these; conflicts flagged in `briefing_reconciliation.md`.

- **Register 12/13 carriers — superseded:** the T1–T4 statement family is DROPPED (Andrew,
  2026-08-28). Tank carrier is **Q1: "What is the meaning of the word tank?"** (frame-balance
  question moot; Q1 doubles as the behavior carrier). Sensitivity gated empirically: 20-sentence
  scene contexts (word "tank" absent) give perfect held-out separation, ~10× tighter than
  single-sentence cells. S1–S3 unchanged as signed off.
- **Register 5 — modified:** Andrew rejected mandatory pre-registration (exploratory analysis is
  first-class). Convergence: battery PROCEDURES (band rules, tiers, event floor) commit before
  new behavior captures; outcome calls remain optional forever.
- **Standing baseline (new, post-reassessment):** all transition dynamics stated relative to a
  recency-weighted evidence-integrator null (uniform null reading(t)=2(k−20)/(20+k); observed
  runs ahead of it in both directions). Hysteresis in this doc's operational sense is
  demonstrated; "stickiness" = D6 loop area beyond a FITTED one-parameter recency model.
- **Instrument doctrine (new, empirically forced):** same-site calibration is mandatory.
  Cross-position projection collapses to a constant; cross-token projection is dominated by
  token-identity offsets (~16k window tokens all read −1.7 regardless of content). For the
  within-stream population (register 13), the proposed instrument is an axis calibrated from
  D4 no-shift WINDOWS (matched token-position mix cancels identity offsets) — pending the
  other AI's sanity check.
- **Register 13 storage stratification — resolved:** Andrew approved the full final-step
  all-positions backfill (36 requests, ~9 GB) after the suicide chain completes; interim
  checkpoint captures were post-shift-window-only.
- **First-token logprob capture** approved as a backend addition (the battery's continuous
  behavior endpoint).
- **Design review round 2 additions (2026-08-28):** carrier-replicate arm ("Define the word
  tank.", 8 runs); extended-tail arm (20 pre + 40 post, subset); fitted-γ integrator; D6 third
  (interleaved) ordering; behavior token-sets derived from classified outputs and frozen in
  procedures.
