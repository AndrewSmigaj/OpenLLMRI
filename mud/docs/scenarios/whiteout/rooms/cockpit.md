# Cockpit — real-world ontology census & gap analysis

> **Official room doc — the EXEMPLAR** (the other eight crash rooms follow this shape). Status:
> scratchpad-authoritative, 2026-07. The test this doc runs is the **ontological Turing test**: if a
> real person stood in this cockpit, what is *here*, what could they *do*, and does the MUD let them?
> Census first (the real world), then the built room, then the gaps. Gaps are **recommendations** —
> code is not changed from this doc without Andrew's review (design-first; the Phase-1 gate ethos).
>
> Method note (from the `ontology-generator` skill): affordances derive from **materials × operations**,
> not per-object verb lists. A gap is only real if a real person could do it AND no existing
> material-property / operation precondition already covers it. Grounded gaps become recommendations to
> extend a material, an operation, or the scenery-noun surface — never a one-off hack.

---

## 1. The scene, if it were real

A single-engine bushplane, nose-down and canted in deep snow. The windscreen is crazed to white and
punched open on one side; cold air pours through it. The instrument panel is shattered — dials starred,
needles dead. The pilot is slumped dead against the forward bulkhead, jacket zipped to the chin, one
hand fallen from the radio. Frost furs every metal surface; the whole cabin ticks and creaks as it
cools. It smells of avgas, cold aluminium, and — incongruously — coffee, still warm in a thermos wedged
by the rudder pedals. Grey daylight, no more. Everything that isn't bolted down has slid forward.

---

## 2. Entity census — everything that is *here*

### 2a. Structure (fixed / scenery)
| entity | note |
|---|---|
| fuselage skin / bent aluminium | the shell; a source of sheet metal if torn free |
| forward bulkhead | the pilot leans on it |
| windscreen (crazed, holed) | the cold's way in; glass shards; sightline out |
| instrument panel + shattered instruments | altimeter, ASI, compass, gauges — dead, glass-faced |
| glareshield | shelf above the panel |
| control yoke / column | between the seats |
| rudder pedals | down in the footwell |
| throttle quadrant / trim wheel | side console |
| circuit breakers + master switch + battery | the electrical bus (radio power lives here) |
| avionics stack + the radio's cradle | the radio sits in it |
| antenna lead / wiring loom | behind the avionics panel (the copper wire) |
| pilot & copilot seats + rails + harness | two seats, belts |
| the deck / floor | where loose things settle |
| door / hatch | the way in and out |

### 2b. Loose kit & the pilot (the takeable world)
| entity | built? | note |
|---|---|---|
| the pilot (body, dead) | ✅ `pilot` | wears a jacket; a lighter in a pocket; boots/gloves/watch (not modelled) |
| flight jacket | ✅ `jacket` | worn on the body |
| brass lighter | ✅ `lighter` | in the jacket pocket — found by frisking/searching the body |
| field radio (RT-220) | ✅ `radio` | dark, powered:false, fixed in its cradle |
| avionics panel | ✅ `panel` | jammed container; a coil of copper wire behind it |
| coil of copper wire | ✅ `wire` | inside the panel — pried out |
| flight manual | ✅ `manual` | readable (GUARD 121.5 clue) |
| sectional chart | ✅ `chart` | readable (Holt's cabin clue) |
| flight bag | ✅ `flightbag` | container: flashlight, fuel tester |
| flashlight | ✅ `flashlight` | powered:true |
| fuel tester (sump cup) | ✅ `fueltester` | for drawing avgas a swallow at a time |
| thermos of coffee | ✅ `thermos` | still warm — drinkable |
| fire extinguisher | ✅ `extinguisher` | steel, sealed |
| pilot's boots | ❌ | real: strip the body for footwear/leather |
| pilot's gloves | ❌ | real: warmth |
| pilot's watch / wallet / ID | ❌ | flavour + fire-starter paper (wallet) |
| headset | ❌ | copper + foam ear cups |
| kneeboard / pen | ❌ | paper + a hard edge |

### 2c. Substances
| entity | built? | note |
|---|---|---|
| broken glass (windscreen + instrument faces) | ❌ | a real improvised blade; today only the whisky bottle yields shards |
| avgas (in the wings / lines) | ~ (`fueltester`, `jerrycan`) | smellable clue; drawable with the tester |
| coffee (in the thermos) | ✅ via `thermos` | drinkable, warm |
| frost / rime on surfaces | ❌ | scrapeable → water; a cold-transfer surface |
| blown-in snow | ~ (`snowdrift` is rear) | not present in the cockpit specifically |
| the pilot's blood (dried stain) | ❌ (examine prose only) | narrative, non-interactive |
| grease / oil / hydraulic fluid | ❌ | burns black; flavour |
| dust / cold | — | see elusive |

### 2d. Elusive — the entities a MUD usually forgets
| entity | built? | what a real person does with it |
|---|---|---|
| **cold air** (the ambient temperature) | ✅ systemic (warmth) | you feel it; you act to keep heat |
| **the draft / wind through the windscreen** | ❌ | you'd feel *where* it comes from and try to block it |
| **light** (grey daylight; the flashlight beam; the radio lamp) | ~ (`flashlight` powered) | see by it; conserve the battery; signal with it |
| **darkness** (behind the panel, in the footwell) | ❌ | you'd want a light to search the dark |
| **sound** (creaking metal, wind, radio static, silence) | ~ (radio state) | you'd *listen* — for the radio, for engine tick, for anything outside |
| **smell** (avgas, coffee, blood, cold metal, leather) | ❌ | avgas smell is a real fuel *clue*; you'd *sniff* to find it |
| **your own breath / body heat** | ✅ systemic (warmth) | fogs in the cold; the thing the cold is eating |
| **time / the cooling airframe** | ✅ (world clock) | the ticking-cold is the pressure |

---

## 3. Actions & relations → candidate MUD command

Ontology verbs, **monadic** (act on one thing) and **polyadic** (relate two/three), each with the
taught-grammar command `VERB X [RELATION Y] [WITH Z]` and whether the built room answers it.

### Universal, per takeable entity (all ✅ built)
`examine X` / `look at X` · `take X` / `get X` · `drop X` · `put X on/in <space-or-container>` ·
`search X` (containers) · read for the paper items. These resolve for every object above.

### Entity-specific
| entity | real-world action (relation) | candidate command | built? |
|---|---|---|---|
| pilot (body) | frisk / search the body | `search pilot` → lighter | ✅ |
| pilot | strip his jacket / boots / gloves | `remove jacket from pilot`, `take boots` | ~ jacket only; boots/gloves ❌ |
| pilot | close his eyes / cover him | `cover pilot with blanket` | ❌ (no reverence affordance) |
| pilot | check for a pulse | `examine pilot` (says dead) | ✅ (prose) |
| radio | power it / key the mic / tune it | `open panel`→wire→antenna chain (ELT) | ✅ (systemic puzzle) |
| radio | pull it from the cradle | `take radio` (fixed) | ~ fixed; real: salvageable |
| panel | pry it open | `pry panel`, `open panel` | ✅ |
| wire | bend / cut / tie it | `bend wire`, `tie wire to X` | ✅ |
| manual / chart | read it | `read manual`, `read chart` | ✅ |
| manual / chart | burn it (tinder) | `burn manual`, `light chart` | ✅ (paper is flammable) |
| thermos | drink from it | `drink coffee` / `drink from thermos` | ✅ |
| thermos | pour it out / warm hands on it | `pour thermos on X` | ~ pour exists; "warm hands" ❌ |
| lighter | strike it / light something | `light tinder with lighter` | ✅ |
| flashlight | turn it on/off; shine it | `light`/`douse flashlight`; `examine X with flashlight` | ~ powered flag; on/off toggle ❌ |
| extinguisher | discharge it | `open extinguisher` / `pour extinguisher on fire` | ~ sealed; discharge ❌ |
| fuel tester | draw avgas with it | `pour fuel into tester` / `use tester on wing` | ~ item present; draw-fuel op ❌ |
| jacket | wear it / wrap something | `wear jacket`, `wrap X in jacket` | ✅ |
| windscreen | look out / block the hole / take a shard | `look out`, `cover windscreen with jacket`, `take glass` | ❌ all three |
| instruments | read the altimeter/compass | `read altimeter`, `examine compass` | ❌ (scenery, not nouns) |
| frost | scrape it → water | `scrape frost` → water | ❌ |
| cold air / draft | find & block the draft | `block windscreen`, `stuff hole with jacket` | ❌ |
| smell | sniff for the fuel clue | `smell`, `smell fuel` | ❌ (no sense verb) |
| sound | listen for the radio / outside | `listen`, `listen to radio` | ❌ (no sense verb) |
| darkness | light the dark to search | `search footwell` (needs light?) | ~ search works, light not required |

---

## 4. What's built today (the honest baseline)
13 entities (§2b), all reachable through the taught grammar and the space model (box A–C): 4 spaces
(left_seat, cradle, footwell, floor), the radio/pilot anchors, two readable clues, one drink, one
container chain (panel→wire) and one body-frisk (pilot→lighter). The systemic layers already present:
**warmth/cold** (elusive-cold is modelled), the **world clock** (time pressure), **containment/discovery**
(DR-24 — the wire and lighter are earned), **read** (§38 clues), and **material operations** (paper
burns, wire bends, leather wears).

## 5. Gap analysis → recommendations

Ranked by ontological payoff. **None applied to code this firing** (documentation pass; each is logged
for deliberate, seam-respecting implementation and Andrew's review).

### High payoff — sensory verbs the whole game wants (not cockpit-only)
1. **`smell` / `sniff`** — a first-class sense op. Grounds the avgas *clue* ("it reeks of fuel — the
   wings still hold some"), coffee, blood, smoke. Cross-cutting: every zone has a smell. → new operation
   category, state-conditioned narration; no conservation impact (read-only sense).
2. **`listen`** — the radio's faint static, the ticking airframe, wind direction, sounds from adjacent
   zones (ties into the perception/sound-hop model already in `space/sound.py`). → new sense op, reuses
   sound-hops.
3. **`feel` / `touch`** — warmth of the thermos, the source of the draft, frost texture. Lower priority
   (examine covers much of it).

### Medium — the cockpit's missing physical affordances
4. **Broken glass as a real blade** — the crazed windscreen and instrument faces should yield a
   `glass shard` on `break`/`take` (today only the whisky bottle does). A shard is an early improvised
   knife; the cockpit is the first room, so this matters. → a `windscreen` scenery-container that
   yields shards, or a `break instruments` → shards rule (glass material already exists).
5. **Strip the body** — boots (leather, warmth), gloves (warmth), watch/wallet (wallet = dry paper =
   fire). Reinforces the grim survival loop already started by frisking for the lighter. → 2–3 cheap
   objects on `pilot`, worn/pocketed.
6. **Block the draft** — `cover windscreen with jacket` / `stuff hole` to cut the cold in-zone. A real
   survival move that would interact beautifully with the warmth system. → needs a "cover an opening"
   operation + a per-zone `draft` the cover suppresses. Bigger; log as a design spike.

### Low — scenery legibility & toggles
7. **Examinable scenery nouns** — `windscreen`, `instruments`, `bulkhead`, `rudder pedals`,
   `control yoke` return "you don't see that" today. A lightweight **scenery-noun** surface (examine-only
   pseudo-nouns per zone, like the existing zone pseudo-nouns) would let a player look at what the room
   description names. Cross-cutting; would serve every room. → recommend a `scenery` table beside the
   space table.
8. **Flashlight on/off + battery drain** — `powered:true` is static; a real flashlight is a resource
   you ration. → toggle op + a slow drain on the world clock.
9. **Discharge the extinguisher / draw fuel with the tester** — both are items whose *characteristic
   action* isn't wired. Niche; log.

### Cross-cutting note
Items 1, 2, 7 recur in **every** room census — they are engine/surface features, not cockpit content.
Recommend they graduate to the roadmap as their own tasks rather than being solved per-room. The
per-room censuses (this and the next eight) should keep *counting* how often each recurs — that vote is
the prioritisation.

---

*Next: `mid_cabin.md` (the seat-foam / first-aid / duffel room) follows this template.*
