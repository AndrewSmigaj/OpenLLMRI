# Investigation scratchpad

Working notes for the pre-build design investigation of **Whiteout** (see the plan in
`docs/scenarios/whiteout/design.md` = the original AI seed). These are *little reports* —
evidence and reasoning, not polished docs. The polished output is the GDD
(`docs/scenarios/whiteout/GDD.md`, written last).

Read order (each was its own focused pass):
1. `lenses/triage.md` — leverage-rating of all 54 review lenses; picks the deep-dive set.
2. `00-brainstorm.md` — critical + creative re-read of the design.
3. `research/prior-art.md`, `research/evennia-interactive-worlds.md` — prior art + feasibility.
4. (skills built under `.claude/skills/` — `lenses`, `ontology-generator`, `solvability-fuzz`)
5. `lenses/{game-design,architecture,implementation}.md` — per-lens finding cards;
   `lenses/cross-lens-synthesis.md` — where the lenses disagree (the most useful output).
6. `probes/` — three empirical calibration probes (playtest, generation spike, softlock walk).
7. `certainty-assessment.md` + `scope-and-risk-register.md` — calibrated answers to the five
   questions, at an explicit scope.

Then: `docs/proposals/whiteout-engine-proposal.md` (my proposal) and the final
`docs/scenarios/whiteout/GDD.md` + `GDD-summary.md`.

Lens IDs (GD#/AR#/IM#) are defined in `.claude/skills/lenses/{game-design,architecture,implementation}.md`.
