# Trace Table — Claim Archaeology (Provenance Rule)

**Started:** 2026-08-27 · **Rule:** any claim that cannot be traced to a specific dataset and
number Andrew personally recognizes is UNVERIFIED. Untraceable rows are FLAGGED, not carried
forward. Living document — rows added/resolved through Phase 1.

Verdicts: **TRACEABLE** (dataset+script+number all recovered) · **PARTIAL** (number and dataset
recovered, no committed script) · **FLAGGED** (provenance gap or doctrine violation) ·
**DROPPED** (per plan).

| # | Claim (where) | Number | Dataset | Script | Space | Verdict |
|---|---|---|---|---|---|---|
| 1 | Tank clusters covary with continuation sense (paper §Results, README:33) | V=0.548, χ²(25)=750.63, p<0.001 | tank polysemy capture, March era (presumed session_1434a9be, raw-text format) | none committed — platform insights path | UMAP-reduced clustering, K=6 @ L23 | **PARTIAL** — recomputation pending (scenario-level, restriction protocol, harmony data) |
| 2 | Tank per-cluster purity (paper:164) | C4 98% vehicle, C5 92% aquarium, C2 94% clothing | same as #1 | none committed | same | **PARTIAL** |
| 3 | Suicide basins covary with engage/refuse (paper:205,239) | V=0.554, χ²(2)=60.68; fictional→engage 81%, distress→refuse 80% | suicide letter capture, March (presumed session_bca94762, raw-text) | none committed | UMAP-reduced clustering, K=3 @ L23 | **PARTIAL** — and output-categorization provenance unverified |
| 4 | "Engagement basin predicts engagement" framing (README:33) | 81%/80% | as #3 | — | — | **DROPPED** — persona/engagement framing removed per plan; paper §naming already renames to fictional/distress; README still carries it → fix in README pass |
| 5 | Single-sentence separation purity (paper:225,294; README:55) | 99% cluster purity | as #3 | none committed | UMAP-reduced | **PARTIAL** |
| 6 | Suicide temporal collapse, both orderings, no visible transition at switch (paper:225,245) | qualitative + Fig | paper-protocol temporal runs (chain-log `suicide` family, 20 runs) | `paper_protocol_basin_projection.py` (committed) reproduces the trajectory points | UMAP-6D refit + centroid axis, out-of-sample transform | **PARTIAL→TRACEABLE for points; FLAGGED for interpretation** — instrument critique applies (out-of-sample UMAP transform); raw-axis revalidation is the plan's central pending item |
| 7 | Polysemy noisy-but-real transition after switch (paper:245) | qualitative + Fig | chain-log `polysemy`/`polysemy_h` families (20+20 runs) | same script | same | same as #6; NOTE `polysemy` family is raw-text (legacy), `polysemy_h` harmony — figure must state which |
| 8 | Want-vs-letter basin projection (unpublished working result) | axis len 4.85 (want) vs 15.58 (letter) | 6 'expanding' per-token sessions | **no committed script** (orphan: `basin_proj_paper_protocol_results.txt`) | UMAP-6D + centroid axis | **FLAGGED** — number without script; superseded by N1 axis work |
| 9 | v2/v3 temporal findings absolute basin positions | various | v2/v3 temporal sessions (harmony) projected on session_bca94762 centroids (raw-text) | study findings docs | cross-format projection | **FLAGGED** — cross-format axis application; findings docs themselves caveat this; v2.1 doctrine now bans it |
| 10 | Generation-quality claim (paper:145) "Claude Sonnet 4 ... matched length ±20 tokens ... prompts archived" | — | generation prompts | claimed archived | — | **UNVERIFIED** — locate archived prompts during Phase 1; if absent, soften paper text |

## Notes
- #1-#5: "presumed" session attributions to be pinned during Phase 1 by matching cluster
  schemas in `data/lake/*/clusterings/` to the paper's K/layers; the schema-space inventory
  (companion doc) feeds this.
- README currently leads with #4's dropped framing — README pass (plan Phase A item 7) rewrites
  around surviving rows only.
- The paper's own §limitations already handles correlation-vs-causation for #3 correctly.
