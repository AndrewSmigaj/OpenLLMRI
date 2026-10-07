# Authoring Workflows — RETIRED (2026-09-07)

The §43.3 `WorkflowPacket` model was never used by the engine and is **retired** (DR-17a). What it was
for — goals as *conditions* with **several** solution paths and the clues a realistic world holds (no set
number, Andrew 2026-09-27), never recipes — now lives in the design documents (`docs/design/14-rescue-paths.md`
and the per-system documents): goals × paths × what each path costs × where in the valley it sits. Each path becomes a **probe
chain** (`scenarios/<scenario>/probes/graph.py`), and the ≥3-paths rule becomes a check the probe runner
can count. Puzzle-critical objects (the radio, the ELT, the pilot) get an authored rule in
`scenarios/<scenario>/authored.py` (the tier-1 seam), not a workflow packet.

The design intent is unchanged: **important goals are workflows, not recipes** (GDD §30, §49), and the
radio has one authored damage state and is never instant rescue (§38).

See [authoring-objects.md](authoring-objects.md) · [authoring-actions.md](authoring-actions.md) ·
[validation-rules.md](validation-rules.md).
