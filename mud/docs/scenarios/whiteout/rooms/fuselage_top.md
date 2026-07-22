# Top of the fuselage — real-world ontology census & gap analysis

> Official room doc. An exterior zone — and one of the FEW with a genuine hook: the high point of the
> wreck, and where the antenna was, so it is the physical anchor of the ELT-rig puzzle.
>
> **Calibration (Andrew, 2026-07):** most outdoor rooms will NOT have a hook like this — they're
> traversal terrain, and the outdoors' real content is *systems* (movement effort/time, snow-slowing,
> 2–3-zone sightlines, exposure), not per-room gimmicks. This zone earns its keep; the coming 50 mostly
> won't, and shouldn't be forced to. No built objects; gaps logged, none applied.

---

## 1. The scene, if it were real
Up on the bare aluminium spine — the highest, most exposed point at the crash. Wind scours it clean.
Where the antenna should be there is only a torn metal base and a short feed cable, hanging loose and
rimed with ice. From up here you can see farther than anywhere else.

## 2. Entity census
### 2a. Scenery / the hook
| entity | note / latent affordance |
|---|---|
| aluminium spine | the roof you stand on; exposed metal |
| **antenna base (torn stub)** | **the mount point** — where a new antenna is rigged (the ELT puzzle) |
| **feed cable (rimed, hanging)** | the lead the antenna joins; de-ice, splice wire to it |
| the elevation (3 m vantage) | the high point — best sightlines; where a signal is *seen from* |
| rime ice on the cable | thaw it to work the connection |

### 2b. Elusive — exterior DELTA (worst exposure of any zone)
Elevated + `exposed` terrain: the wind bites hardest here (warmth should weight it). Best sightlines (a
vantage). Same missing sense verbs (wind = sound; only cold metal to smell).

## 3. Actions & relations → candidate MUD command
| entity | real-world action | candidate command | built? |
|---|---|---|---|
| antenna base | mount / attach a new antenna | `attach antenna to base`, `tie wire to base` | ❌ (the puzzle's top anchor) |
| feed cable | splice wire / connect the ELT lead | `tie wire to cable`, `connect cable to elt` | ❌ |
| rime ice | thaw the connection | `melt ice on cable` | ~ melt op exists, no target |
| the spine | signal from the high point | `signal`, `wave`, `light fire here` | ❌ (vantage/signal) |
| the vantage | see farther than below | elevation-boosted sightlines | ~ bands use see-hops, not elevation |
| adjacent | go / look along the spine | `go`, `look` | ✅ |

## 4. What's built today
A see-hub along the spine (sightline to outside_tail; walk/see to outside_nose), a default drop space
(`the_spine`), the perception bands. The antenna base + cable are **zone prose, not nouns** — so the
ELT-rig puzzle's *top-side half* has no interactable anchor yet.

## 5. Gap analysis → recommendations (none applied; logged)

### High — the puzzle's missing half
1. **The antenna mount as an interactable.** The ELT (in the tail) needs "a real antenna, and wire
   enough to reach one." Down there it's a noun; up here, where the antenna *goes*, there is nothing to
   attach to. Rigging the antenna is a headline puzzle and its top anchor doesn't exist as an object. →
   an `antenna_base` object you tie/attach wire to, which then feeds the ELT. **The key gap in this zone.**
2. **Vantage / signalling.** The high point should matter — a signal fire or mirror here is seen from
   farther, and elevation should widen sightlines (the §14 band model uses see-hops, not elevation — a
   recorded deferral). Ties to the eventual rescue-signal system. Medium.

### Systemic (the outdoors' real content — these outrank per-room hooks)
- **exposure / shelter** — worst here (elevated + exposed). (systemic, vote 2 with outside_nose)
- **movement effort/time + snow-slowing** — the reason the outdoors exists: traverse, at a cost, slower
  as snow deepens. Not a gap this zone invents; the census keeps flagging it as *the* outdoor system.
- **2–3-zone sightlines for social play** — already delivered by the bands; elevation should enhance it.

### Recurring votes
sense verbs (wind = sound) — vote 5 · examinable scenery nouns (spine, base, cable) — vote 5.

> **Carried forward:** `outside_nose` + `fuselage_top` establish the exterior model — **two systems
> (exposure, movement) + the occasional puzzle anchor** are the whole outdoor content picture. The
> remaining outdoor rooms get censused fast against that, not mined for hooks they don't need.

---
*Next: `outside_tail.md`, then the debris trail / severed tail / treeline.*
