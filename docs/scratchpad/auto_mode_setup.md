# Auto-Mode Setup — Context-Shift Dynamics Paper (v2 plan)

**Drafted:** 2026-08-27 (rev 3; STATUS 2026-08-27 EOD: mechanics verified, plan approved, Phase A items 0,2,3,4,5,7 done; design fully frozen 2026-08-28: tank carrier = Q1 meaning-question; predictions file made optional per Andrew — transition figure UNBLOCKED) · **Source of truth:** Research Plan v2 + `CLAUDE.md` §11.

**Rev 3 reframe (user correction):** the paper's empirical base is regenerated from scratch —
new sentence sets under the friend/foe-refined variation doctrine, all captures rerun under
current harmony format with per-token anchor spans. The existing lake's role is **archaeology
only** (trace table, findings-register verification, design priors). Rev 2 treated existing
coverage as the constraint; that was wrong. One exception by design: Phase 0's dual-trajectory
credibility figure is built on the existing May/harmony captures, because it must exist before
Sept 4 and the reruns are Phase 2 work.

---

## 1. Boundaries

`CLAUDE.md` §11 overrides auto mode: source is read-only without explicit "can change code".

**Green zone (runs without asking):** lake reads and heredoc measurement; `docs/research/**`,
`docs/scratchpad/**`, `docs/studies/**`, `docs/RECOMMENDATIONS.md`; **sentence sets and their
guides** (`data/sentence_sets/**`); clustering/categorization artifacts; server ops per `/server`;
captures via API; `.venv` package installs.

**Red zone (blocked):** `backend/src/`, `frontend/src/`, `evennia_world/`, `.claude/`,
top-level `scripts/`, configs.

---

## 2. Standing findings (survive the reframe)

**2.1 Instrument diagnosis (Phase 0 item 1 — answered).** No full-dimensional analysis mode
exists. Three projection implementations found: backend `get_temporal_lag_data`
(`temporal.py:289-437`; reduced-space centroid axis, UMAP up to 128 comps, `token_position==1`
hardcoded at `:337`/`:400`); study scripts (UMAP-6D refit + centroid axis + out-of-sample
`transform()` — source of existing paper-protocol numbers); and true raw-2880D
difference-of-means, in-repo only for lying_v4, never applied to tank or fiction/real. The
messiness critique: out-of-sample UMAP transform is loosest exactly on transition tokens, and a
linear axis in UMAP space has no guaranteed meaning — lens used as a model of geometry. The plan's
axis projection = port of lying_v4's method. `per_token_separation_report.md:181` already lists
raw-2880D readout as an open follow-up.

**2.2 Format split (hard evidence).** March captures = raw-text (bare sentence, e.g. 17 tokens);
May = harmony (~67-token scaffold, 84 tokens for same-length sentence). Chain log has separate
`polysemy` / `polysemy_h` families. Study findings already caveat cross-format projection
(v2/v3 findings vs `session_bca94762` centroids). No metadata records format anywhere → v2.1
requires recording it on all new runs (N4). For Phase 0's figure: usable harmony endpoint sets
are `session_9358c2a1` (fiction/real) and `session_e2be37dd` (tank).

**2.3 Capture machinery for the rerun standard.** `capture_static_substring` produces per-token
spans at semantic positions 2+ (`probe_processor.py:172`, `integrated_capture_service.py:200`).
Verified mapping for `"I want to write a suicide letter"`: pos 3 = ` want` (pre-lexical),
pos 8 = ` letter` (post-lexical); pos1 ≡ pos3 (60/60 probes, L14), cos(pos3,pos8)=0.751.
**Every new capture should pass a static substring spanning both anchors** — this is how the v2.1
anchor-site standard is met with zero code change. Tank needs its equivalent span chosen at
design time.

**2.4 Router observable is free.** `routing.parquet` ships per-token 32-expert weights and a
precomputed `gate_entropy` column on every capture. Tier 1 item 9 = analysis only, and applies
automatically to all reruns.

**2.5 Archaeology flags found so far.** README headlines the dropped engagement framing
(81%/80%, V=0.554) and pre-doctrine V=0.548; orphan result
`basin_proj_paper_protocol_results.txt` (want-vs-letter projection, axis 4.85 vs 15.58, no
committed script — an early sign the anchor contrast is large, and a provenance-rule flag).

**2.6 Environment.** `.venv` ok (+matplotlib; `diptest` missing, installable). Model + tokenizer
local. Backend/frontend down. Lake: 204 sessions — henceforth archaeology material.

---

## 3. The generation standard (port of the friend/foe doctrine)

The current recipe lives in `data/worlds/scenarios/GUIDE.md` §Cross-pair variation; sentence-set
`GUIDE.md` predates it. The port, applied to every new set:

- **The target contrast is the only permitted axis of covariation.** Everything else — syntax,
  register, length, opener tokens, topic vocabulary, named entities, punctuation — varies
  maximally and is balanced across labels. Any feature shared by most members of one label is a
  feature the model can learn instead of the contrast.
- **Conceptual-category load balancing**, not just surface-string diversity (the scenario guide's
  intent-bucket rule, applied to sentence frames).
- **Audit recipes** written alongside each set (label × structure/register/length χ² checks — the
  shuffle-test discipline already proposed in RECOMMENDATIONS 2026-05-01).
- **Project-blind generation** per v2.1: generator sees the contrast spec, not the hypotheses.
  Mechanics to confirm with Andrew (blind sub-session vs external LLM — repo norm is that Claude
  authors sets directly; see feedback_no_subagents_for_authoring).
- Legacy sets stay for archaeology, tagged `legacy` in metadata, never silently mixed.

First green-zone deliverable of the program: **update `data/sentence_sets/GUIDE.md`** with this
doctrine (sentence-set guides are exempt from code-change mode), so every set generated after it
follows one written recipe.

## 4. The rerun program (dataset → capture map)

All new, all harmony, all per-token anchor spans, seed fixed, format version logged in the study
log until N4 lands. Per plan Tier 1:

| # | Dataset family | Purpose (plan item) |
|---|---|---|
| D1 | Tank polysemy endpoint set (5 senses, restriction protocol at analysis) | calibration + separability (1,2) |
| D2 | Fiction/real endpoint set | calibration + separability (1,2) |
| D3 | Transition sequences, both probes, both directions, ≥paraphrase families | transition metrics + distribution tests (3,4,10) |
| D4 | Length-matched no-shift control arms | control (6) |
| D5 | Minimal-pair contexts, fiction/real | control (6) |
| D6 | Graded-evidence sweep sets, A→B and B→A | hysteresis loop (5) |
| D7 | History design: fixed verbatim request × 3 arms | safety-setting hysteresis (7) |
| D8 | Behavior-link runs (generation on) | last-token → behavior (8) |

Captures for D1–D8 are green zone (API); they wait on the **predictions file** (Phase 2 Step 0 —
committed before results exist) and on Phase 0 closing Sept 4.

## 5. Phase 0 queue (now → Sept 4)

1. **A1 Trace table** (`docs/research/trace_table.md`) — archaeology, seeded from §2.5.
2. **A2 Schema/format inventory** — which prior results rest on which space + format; `legacy` list.
3. **A3 Anchor-site + capture-standard doc** in `docs/ANALYSIS.md` (§2.3 table, recovered substring).
4. **N1 Axis projection** — difference-of-class-means, 2880D, per layer, endpoints renormalized
   ±1; calibrated on the May/harmony sets. *Home decision:* committed study script
   (`docs/studies/.../analysis/`, established pattern) first; backend port under code-change mode.
5. **N3 Dual-trajectory figure** — same transition, study-standard UMAP-6D lens beside raw axis.
6. **A4 README/repo presentability** — after A1, so the front page only claims what survives.
7. Nothing else (no steering, no SAE, no new features).

## 6. Implementation list awaiting "can change code"

- **N2** anchor-site request parameter (`temporal.py:337`/`:400` hardcode `token_position==1`).
- **N4** format/tokenizer version recorded in capture metadata (v2.1 requirement).
- **N1-backend** axis-projection endpoint + frontend raw-axis panel, after script validation.
- **N7** scenario-level grouped CV for linear probes (upgrade of the 5-fold template in
  `representation_output_gap.md`) — Phase 2, script-level.

## 7. Cadence

Work §5 in order; checkpoint after A2 and after N1. Stop and ask before anything red-zone.
Session-end: append to `docs/RECOMMENDATIONS.md`, update this file.
