# `world/sim/resolver/` — the §26 resolution tiers (DR-09)

`resolve(attempt, world)` walks tiers and returns the first hit; **everything resolves** (success /
partial / informative redirect) — never a hard "you can't do that".

| Tier | What | File |
|---|---|---|
| 1 | authored-special (puzzle-critical, e.g. radio FSM) | `tiers.py` |
| 2 | object-rule (rare per-object override) | `tiers.py` |
| 3 | **operation×material (the workhorse)** — index keyed `(verb, relation, material_of_X, material_of_Y)` | `index.py` |
| 4 | generic-physics (mass/temperature/containment defaults) | `tiers.py` |
| 5 | informative-redirect (ranked by smallest unmet-precondition gap; names the verb) | `redirect.py` |

Unhandled-but-sensible attempts → `wall_sensor.py` (the build-time authoring queue, DR-18). Specificity
dispatch: most-specific wins, ties by declared integer priority — never file order. Pure (reads
snapshots, returns Effects/Events, never writes). Built in roadmap **P1**.
