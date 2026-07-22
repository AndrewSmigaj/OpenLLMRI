# Outside the nose — real-world ontology census & gap analysis

> Official room doc. The first **exterior** zone censused, and the pattern flips: it holds **no built
> loose objects** — it is pure scenery + the elusive. That is exactly why it's valuable. Where the
> cabin censuses surfaced missing *content*, the exterior ones surface missing *systems*: the wings are
> the crash's real fuel tank, and stepping outside should mean losing the cabin's shelter. Gaps are
> recommendations; no code changed here.

---

## 1. The scene, if it were real

Out in the open, at the buried nose. The plane is driven in nose-first: the cowling and bent propeller
are half-swallowed by a drift, the windscreen crazed white above them. The wings spread out to either
side, low in the snow — and inside them, still, is fuel. Nothing breaks the wind here; the sky is the
whole ceiling. This is the coldest, most exposed spot at the crash, and it is where the fuel is.

## 2. Entity census — scenery & the elusive

### 2a. Structure / scenery (no built nouns yet)
| entity | note / latent affordance |
|---|---|
| crumpled nose cone | the buckled snout; a windbreak of last resort |
| bent propeller | aluminium blades — a lever, a digging tool, scrap metal |
| engine + cowling | the cowl the engine cover came off; oil; dead-cold now |
| **the wings** | **the fuel tanks** — avgas the fuel tester is literally built to draw ("the wing drains would answer to this") |
| wing sumps / fuel drains | the tap point for avgas |
| windscreen (from outside) | crazed glass; a shard source; sightline into the cockpit |
| landing gear / skis | how a bushplane sits on snow; steel + cable |
| pitot tube / antenna stubs / tie-down rings | small metal fittings |
| the drift against the nose | the room's `the_drift` default space (nothing buried today) |

### 2b. Substances
avgas (in the wings — the point of the room), engine oil, drifted snow, frost, broken windscreen glass.

### 2c. Elusive — the exterior DELTA (vs the cabin baseline in `cockpit.md §2d`)
| entity | built? | what changes *outside* |
|---|---|---|
| **exposure / no shelter** | ❌ (systemic gap) | the cabin's walls are gone; wind + cold act unbroken |
| **wind** (unblocked) | ~ prose only | direction + strength should bite harder here than inside |
| open sky / daylight | ~ (world clock) | full light; weather comes from here |
| **sightlines** (to the debris trail, treeline, tail) | ✅ perception bands | the exterior is where the far-view/§14 grading earns its keep |
| smell (avgas — STRONG at the wings) | ❌ | the fuel clue is loudest right here |
| sound (wind, the creaking hull) | ❌ | nothing damps it out here |

## 3. Actions & relations → candidate MUD command
| entity | real-world action | candidate command | built? |
|---|---|---|---|
| **the wings** | **draw / drain avgas** (with the tester or a can) | `drain wing`, `fill jerrycan from wing`, `pour fuel from wing into can` | ❌ **(high value)** |
| the wings | siphon into the sleeping bag / a rag (accelerant) | `pour fuel on X` | ~ pour exists, no wing source |
| propeller | break/bend a blade off for a tool | `break propeller`, `bend blade` | ❌ |
| engine cowling | already salvaged (engine cover) | — | ✅ elsewhere |
| windscreen | break for a glass shard | `break windscreen` → shard | ❌ (recurring glass gap) |
| nose cone / drift | shelter behind it from the wind | `shelter behind nose`, `hide from wind` | ❌ (exposure system) |
| the drift | dig / melt | `dig drift`, `melt snow` | ~ ops exist; nothing buried, but valid |
| this whole zone | feel how exposed/cold it is | (systemic warmth reading exposure) | ❌ **(systemic gap)** |
| adjacent wreck | look toward / go to | `look`, `go to the fuselage top / the tail` | ✅ (bands + walk) |

## 4. What's built today
Structurally: a walk/see hub (nose ↔ fuselage top ↔ outside tail; the cockpit *sees* it through the
windscreen), a default drop space (`the_drift`), and the **perception bands** that make the exterior
read as an exterior (you see the debris trail, treeline, tail fade by distance from here). No loose
objects — correct; nothing *fell* here, the plane *arrived* here.

## 5. Gap analysis → recommendations (none applied; logged)

### High payoff — systemic, and this zone is the reason to build them
1. **The wings as the fuel source (`drain`/`siphon` avgas).** The fuel tester's own examine text
   promises it ("the wing drains would answer to this"), and there is no wing to drain. Avgas is the
   crash's real accelerant (for signal fires, the sleeping bag is deliberately fuel-soaked). → a `wing`
   scenery-container holding `fuel`, tapped by `drain wing with tester` / `fill can from wing`. **The
   single highest-value exterior gap.**
2. **Exposure / shelter as a systemic axis.** Standing outside should cost more warmth than the cabin —
   wind unbroken, no walls. If `warmth` doesn't already weight `terrain_tags` (exterior/exposed) and a
   wind factor, this is *the* survival tension (in vs. out) and it's missing. → have warmth read zone
   exposure; pairs with the `block-the-draft` gap from rear_cabin (shelter is the same system from both
   sides). **Recommend a design spike jointly with block-the-draft.**

### Medium / low
3. **Propeller / gear as salvage** (aluminium lever, steel cable) — cheap scenery-objects. Low.
4. **Shelter behind the nose cone** — a lightweight form of exposure mitigation; folds into #2.

### Recurring votes (cross-room)
- **sense verbs `smell`/`listen`** — avgas is loudest here; wind is the sound. (vote 4)
- **broken glass as a blade** — the windscreen again. (vote 3)
- **examinable scenery nouns** — nose, prop, wings, gear, windscreen: the whole zone is scenery, so the
  need is sharpest here. (vote 4)

> **Emerging thesis:** the exterior zones don't need more *objects* — they need the **shelter/exposure
> system** and the **wing-fuel source**. Two builds would transform all six outdoor-adjacent zones.

---

*Pair: `fuselage_top.md` (the antenna-stub zone — the ELT rig puzzle) next.*
