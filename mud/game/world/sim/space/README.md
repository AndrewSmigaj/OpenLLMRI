# `world/sim/space/` — perception & space (DR-13, §10–15)

Overlapping perceptual zones, not chunky rooms. A Scene is one space; a character's **zone** is a
position within it; **visibility, audibility, reachability, direction, detail are separate**, each
distance/weather/occlusion-aware (§14 bands).

| File | Purpose |
|---|---|
| `zones.py` | zone = coords + terrain tags within the one Scene |
| `perception.py` | the separate visibility/audibility/reachability/detail bands |
| `direction.py` | relative direction between zones |
| `sound.py` | loudness × distance × weather → audibility (speech ranges, §15) |

Pure functions; the shell wires them to per-observer `return_appearance`/`get_display_*` and the message
propagator. Reachability gates manipulation. Built in roadmap **P3** (deferred past the slice).
