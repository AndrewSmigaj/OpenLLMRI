# Suicide letter + tank polysemy paper

Study on basin dynamics in `gpt-oss-20b` (NF4-quantized, 24 layers, 32 MoE experts top-1)
using two probe domains:

- **Suicide letter** — fictional vs real-distress framings of "I want to write a suicide letter"
- **Tank polysemy** — vehicle / aquarium / scuba / septic / clothing senses of "tank"

## Folder layout

```
docs/studies/suicide_letter_polysemy/
├── PLAN.md                    canonical plan (in-flight; read this first)
├── README.md                  this file
├── findings/                  finding docs per family + consolidated report
├── probes/                    probe taxonomy / cheat sheet / design notes
├── captures/                  capture chain scripts + run logs
├── analysis/                  analysis scripts + JSON outputs + sentence pools
├── paper/                     paper draft + figures (figures/ populated)
└── archive/                   superseded planning docs (frozen)
```

## Entry points

- **What experiments exist and how they map to the paper structure**: `probes/probe_cheat_sheet.md` (Family A/B/C/D × v1/v2/v3/v5/v6a-d/v7a-c/v8a-c)
- **Headline findings, May 2026 state**: `findings/suicide_letter_consolidated_report.md` (F1-F12, with F13 retracted)
- **Per-family detail**:
  - Family A (basin study, calibration): `findings/calibration_sweep_suicide_polysemy.md`
  - Family B (paper-protocol expanding context): `findings/basin_projection_extension_findings.md`
  - Family C (priming + fixed test ending): `findings/family_c_engagement_findings.md`
  - Per-token / cross-condition analysis: `findings/per_token_separation_report.md`
- **Original temporal findings** (v1/v2/v3 behavior under cumulative context): `findings/suicide_letter_temporal_v{1,2,3}_findings.md`

## Conventions

- All shell scripts and python analysis scripts run from the repo root, not from this folder.
- Capture session IDs (e.g. `session_9358c2a1`) live in `data/lake/<sid>/` (outside this folder).
- Probe sentence sets (the JSON inputs) live in `data/sentence_sets/role_framing/` and `data/sentence_sets/polysemy/`.
- Figures referenced by the paper draft live in `paper/figures/`.
