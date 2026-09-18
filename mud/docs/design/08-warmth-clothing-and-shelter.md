# 08 — Warmth, clothing and shelter

> **Status: `draft for review` (2026-09-16). NEW — this system had no design document of its own;
> its content was scattered across six places and is gathered here for the first time.**
> **Architecture counterpart:** [`../architecture/clothing-warmth.md`](../architecture/clothing-warmth.md)
> (DR-25, the shipped v1). **Sources:** `docs/investigation/design/time-and-stakes.md` §4 (the warmth
> process, the bands, the floor; drying/wetting) · `docs/investigation/design/players-and-kit.md` §4
> (the clothing system v2 — the primary clothing content) · `docs/architecture/clothing-warmth.md`
> (v1 as built) · `docs/investigation/design/rescue-graph.md` §WARMTH (the four paths) ·
> `docs/investigation/design/events-and-escalation.md` §2 (the cold ladder) · GDD §31–§36 and §0a
> improvement 4 (the warmth floor) · the archived AI seed `design.md` §32 (warmth) and §34 (shelter),
> which GDD §31–§36 carries forward "unchanged" · `docs/investigation/world/rooms.md` (the per-zone
> exposure bands) · `docs/scenarios/whiteout/rooms/rear_cabin.md` §5 (block-the-breach) and
> `outside_nose.md` §5 (the exposure/shelter gap) · code: `game/world/sim/systems/warmth.py`,
> `shelter.py`.

---

## 2. Provenance

### Andrew's decisions

- **"you should be able to wear everything."** (2026-07-03, quoted in
  `docs/architecture/clothing-warmth.md` as the directive behind DR-25.) Clothing is a system, not
  flavour; wearability is derived from what a thing physically is, never from a list of approved
  garments.
- **Warmth comes in several ways — a blanket, jackets, other people (sharing a blanket); they can
  make a fire and a lean-to outside if they want.** (2026-09-07.) Fire is one path among several,
  and the social path — two bodies under one blanket — is named explicitly.
- **Clothing affects warmth loss.** (2026-09-07, decided; recorded in
  `docs/investigation/design/00-provenance-audit.md` §1.)
- **Each player starts with a different clothing draw** (and a different injury and pockets draw).
  (2026-09-07, decided.) What a player is wearing when the plane stops moving is not chosen.
- **Players can sleep**; the clock may run at 20× by consensus when everyone sleeps or waits, and
  events interrupt it. (2026-09-07, DR-14a.) Sleeping is where cold does its worst work.
- **The crash is in December**; **the whole valley is in the first complete run**; **the plane is a
  Cessna 206-class single** with the four-seat interior. (2026-09-16.) December sets the ambient
  temperatures the warmth clock spends, and the 206's thin skin and split hull set the shelter.
- **Descriptions are composed from state.** (2026-09-16.) "Your feet are soaked" is not a separate
  status screen; it is the scene and the self-view telling you what is true.

### Proposals (Claude)

Everything below is a proposal for this review. In particular:

- **The seed's warmth and shelter lists** (`design.md` §32, §34) are from the **archived AI-written
  seed**, not from Andrew — the file's own banner says "ARCHIVED — original AI seed". GDD §31–§36
  carries them "unchanged", so they have been sitting in an authoritative document wearing a
  provenance they do not have. They are good lists and this document keeps them; they are proposals.
- **The warmth floor** (GDD §0a improvement 4: a guaranteed no-materials warmth floor so
  fire-failure is recoverable) is likewise a GDD improvement, not a recorded decision of Andrew's.
  It is a proposal this document recommends keeping, because it is what makes fire failure a setback
  instead of an ending.
- **The clothing system v2** — coverage by body region, the shell's wind, waterproofing, the wet
  fraction, sweat, dexterity, movement, signal, sharing (`players-and-kit.md` §4).
- **The warmth clock** — core temperature as an integer, the per-tick equation, the bands
  (`time-and-stakes.md` §4).
- **Shelter as a property of a zone** — this document's own proposal; see §4.4. No shelter design
  existed anywhere before this page.
- **All numbers** — thresholds, bands, region shares, the December temperature ladder.

---

## 3. In one paragraph

You come to in a cold aluminium tube in December with whatever you happened to be wearing, and from
that minute the cold is spending you. It is not a meter you watch; it is the wind through the tear
in the hull, the snow melting into your sleeve, your fingers losing the knot you are trying to tie.
You get warmth back the way people actually do: you put more on — your own bag, someone else's
sweater, the quilted engine cover out of the aft bin — you get out of the wind, you block the hole
the wind is coming through, you get off the metal floor onto boughs, you light a fire if you can,
and when none of that is enough you sit shoulder to shoulder with the others under one blanket,
which is warmer than any of you alone and is also the moment the party becomes a party. The game
never tells you to do any of this. It tells you your hands are numb, that the wind is coming in
through the breach, that the cover would hold heat against metal all night — and lets you work out
the rest.

---

## 4. The design

### 4.1 The rules

1. **Warmth is a number on the body, surfaced as words.** One integer per character — core
   temperature in tenths of a degree Celsius (370 = 37.0). The player never sees the number; they
   see a band and, better, a composed sentence about their hands and their feet. *(Proposal;
   `time-and-stakes.md` §4.)*
2. **Every source is physical and additive.** There is no "warmth buff". The seed's list stands as
   the coverage target — *fire · windbreak · shelter · dry clothing · layering · insulation from the
   ground · huddling · heated stones · hot water containers · moving out of the wind · closing
   fuselage gaps · a snow trench · a snow wall · reduced sweating and exertion · sharing body heat*
   (`design.md` §32). Each is a thing you do to the world, and the world remembers it.
3. **The loss side accounts for** ambient temperature · wind exposure · wet clothing · clothing
   insulation · shelter insulation · ground contact · fatigue · calorie deficit · fire distance ·
   body condition (`design.md` §32). The per-tick form proposed in `time-and-stakes.md` §4:
   `Δ = −exposure(zone, weather, wind) + insulation(clothing, wet penalty) + fire_heat(distance)
   + activity_heat − wet_skin_penalty + huddle_bonus`.
4. **Bands, as proposed:** fine ≥ 360 · cold 350–359 · shivering 340–349 · impaired 320–339 ·
   dying < 320.
5. **The warmth floor.** Huddle + the fuselage + body heat, with no materials at all, keeps a
   competent party at or above *shivering* through one night — held as a property test, not a hope
   (GDD §0a #4; `time-and-stakes.md` §4). Fire failure must be survivable or the fire stops being a
   choice and becomes a gate.
6. **Wearability is derived, never whitelisted.** Anything flexible/fabric/soft/insulating and light
   enough to drape around a body wears: the blanket as a cloak, a freed seat cover, the engine
   cover, socks on hands. Refusals are physical ("it doesn't bend around a body"), never a list of
   what does work. *(Shipped, DR-25.)*
7. **Shelter is evaluated by properties, never by recipes, and partial shelters count.** A half-built
   windbreak reduces heat loss before it is anything you would call a shelter (`design.md` §34;
   GDD §31–§36). There is no build menu and no recipe list; see §4.4.
8. **Wet is a quantity, not a flag** — grams of water in a thing. It rises in snow and falls by a
   fire; wet insulation counts for a fraction that falls with wetness, to nothing for soaked down.
   *(Proposal; the shipped `wet_fraction` already implements the curve.)*
9. **Never a menu.** The game does not suggest huddling, does not list shelter types, does not say
   "you could block the breach". The breach is described as what it is — the wind's door — and the
   engine cover is described as holding heat against metal all night. The player joins them.

### 4.2 The clothing system

Each wearable declares: `covers` (head · torso · arms · hands · legs · feet), `insulation` (from its
material), `wind` (0–1: a shell stops wind, a sweater does not), `waterproof` (0–1), mass in grams;
and inherits `wet` (grams of water) and damage state. *(Proposal, `players-and-kit.md` §4; the fields
are shipped in `characters.py` and read by `warmth.py`.)*

What derives from that:

| derived | rule | source |
|---|---|---|
| **warmth by region** | the body loses heat per region by exposure × (1 − that region's coverage); a bare head is about a fifth of the loss, bare hands and feet drive frostbite | `players-and-kit.md` §4; the shipped region shares are head .20 · torso .35 · arms .10 · hands .10 · legs .15 · feet .10 |
| **layering** | layers add; the outer shell's `wind` multiplies the whole stack | `players-and-kit.md` §4 (v1 ships unlimited linear layering — "wear everything"; diminishing curves are an open question) |
| **wet** | wet insulation counts for a fraction that falls with wetness, to zero for soaked down; wool forgives, down does not | `players-and-kit.md` §4; `warmth.py::wet_fraction` |
| **sweat** | hard work in a heavy stack puts water into the inner layer — the deferred cold debt | `players-and-kit.md` §4 |
| **dexterity** | bare hands in the cold lose fine work by the minute (knots, a match, the drill); thick mittens cannot do fine work at all — take them off and pay the warmth | `players-and-kit.md` §4; `warmth.py::fine_work_ok` |
| **movement** | snow boots against sneakers changes wet-feet rate and speed; snowshoes double speed on snow; dress shoes on ice is a fall | `players-and-kit.md` §4 |
| **signal** | a bright jacket on the wing is visual rescue confidence; a dark one is not | `players-and-kit.md` §4 |
| **sharing** | `give X to Y`, wearing something from another's hand, the blanket over two — the huddle bonus is real physics: two bodies, one blanket, shared loss | `players-and-kit.md` §4 |

**The score, as built (DR-25):** each worn item contributes `round(insulation × min(mass_g, 3000))`
"insulation-grams" — an intensive material property scaled by an extensive mass — summed, then
banded: *bare to the wind → thinly covered → adequately dressed → well bundled → swaddled*. v2
multiplies each item by its wet fraction and distributes it over the regions it covers. Status words,
never numbers: "your hands are numb", "your feet are soaked", "you are sweating in the parka".

### 4.3 The draws (what the party starts with)

The starting clothing draw is Andrew's decision (2026-09-07); the specific slots are proposals from
`players-and-kit.md` §1 and are the subject of document 16. The warmth-relevant shape: a guide in a
down parka, wool base layer, insulated boots, gloves and a wool hat; a townie in a denim jacket,
cotton hoodie, jeans and sneakers with **no gloves**; a nurse in fleece and hiking boots with thin
gloves; a salesman in a wool overcoat and **dress shoes**; a kid in a full ski outfit and mittens.
*What a player wears at the crash is the largest single determinant of the first night* — and the
spread is what makes giving away your gloves an act rather than a transaction.

### 4.4 Shelter (proposal — no design existed before this page)

Nothing in the repo designed shelter. `game/world/sim/systems/shelter.py` is a docstring and an
import. Two room censuses independently arrived at the same missing system from opposite sides —
`rear_cabin.md` §5 ("block / cover the hull breach — the single most natural survival act here has
no affordance… it would light up the whole warmth loop") and `outside_nose.md` §5 ("standing outside
should cost more warmth than the cabin — wind unbroken, no walls… pairs with the block-the-draft
gap; shelter is the same system from both sides"). What follows is the proposal that answers both.

**Shelter is a property of a zone, not an object you own.** Every zone carries, as authored data:

- **wind exposure** — how much of the weather's wind reaches a body standing in it. The valley
  design already authored this for all fifty outdoor zones as four bands (`rooms.md`, "Exposure
  bands"): `sheltered` (the big-spruce hollow, the tree well, the deadfall tangle, the grouse
  thicket, the spruce tunnel, the marten set, the cabin, the loft) · `broken` (most forest, brush
  and bank zones) · `open` (the muskeg flats, the lake apron and ridge and inlet and outlet, the
  pond flats, the krummholz, the bench saddle) · `brutal` (the open ice, the boulder field, the
  knob, the lee cornice, the fuselage top). The cabin with its stove lit is the map's only `warm`.
  The crash cluster: interiors `broken` (a windbreak but unheated), exteriors `open`, the fuselage
  top `brutal`.
- **a roof score** — how much sky is over you: bough cover, hull, a lean-to's thatch, the tree
  well's snow-laden skirt. A roof cuts radiant loss and stops falling snow wetting you.

**Both are mutable.** Blocking the breach raises the rear cabin's wind exposure one band; a snow
wall on the ice raises the fire's survival and the body's; a lean-to raises the roof score of the
patch of outdoors you built it on. This is what makes shelter a *verb* and not a *building*.

**The seed's property block** (`design.md` §34) is the fuller target once partial shelters are
objects in their own right: `wind_blocking · insulation · waterproofing · structural_stability ·
fire_safety · capacity · smoke_ventilation`. The proposal is that the zone-level pair (wind exposure,
roof) is the v1 that everything reads, and a built shelter is a thing that *writes* those two
numbers plus capacity — so partial work counts automatically and nothing needs a recipe.

**The shelters Whiteout's own world already implies** (all proposals; each is a floor, not a set):

| shelter | what it is | where the world already says so |
|---|---|---|
| **the fuselage as a windbreak with a hole** | the crash's default shelter: walls, no heat, and a tear in the rear hull that the wind owns. It is the warmth floor's physical half | `rear_cabin.md` §2e ("the tear is the way outside, the wind's door, and the reason this room is colder"); the manual's SHELTER page backs "the warmth floor (fuselage)" |
| **block the breach** | cover the tear with the engine cover, a wing panel, a suitcase wall, plexiglass. The first real shelter act, available in the first hour, needing nothing the party does not have | `rear_cabin.md` §5.1; `rescue-graph.md` §WARMTH ("shelter / windbreak — cover breach with sheet") |
| **the lean-to** | Andrew's own example (2026-09-07): poles and thatch against the weather, outside, by choice. Boughs are pre-cut for it on the shear line and free at the forest edge | `design.md` §34; `rooms.md` (`shear_line`: "the crash pre-cut a shelter's worth of thatch and bedding"; `forest_edge`: bough beds, shelter thatch) |
| **a snow trench / snow wall / snow blocks** | the treeless ice's only shelter material: wind-slab snow cuts into blocks with any long blade or the shovel — a windbreak for a signal fire, or emergency shelter stock | `design.md` §32, §34; `rooms.md` (`ice_flat`: "wind-slab snow-blocks… the one shelter material the treeless ice provides") |
| **the tree well** | a natural bivvy: a grandmother spruce's skirt to the snow, a dry needle floor, already warmer than the air. The warmth floor given a terrain form — a party caught out overnight survives there with boughs and body heat and nothing else | `rooms.md` (`tree_well_hollow`) |
| **ground insulation** | boughs, foam, luggage, the seat cushions — the ground steals more heat than the air | `rooms.md` (`forest_edge`); `design.md` §32; `time-and-stakes.md` §8 (the bedding score) |
| **the stove** | Holt's cabin, the map's only `warm` zone: a contained, chimney-drafted fire that turns the storm into weather — the walk-out path's reward | `rooms.md` (`cabin_interior`) |

**Graceful degradation.** Until a build operation exists, the zones are still authored with their
bands and the prose still says which places are cold; a party can still get out of the wind by
*going somewhere else*, which is itself the first shelter decision.

### 4.5 Drying and wetting

Wet is grams of water in a thing. By a fire it falls; in snow it rises; a soaked matchbox dries by
heat, which is the fire bootstrap (`time-and-stakes.md` §4). Three authored ways to get wet that the
world already carries: snow driving in through the breach; overflow on the creek (water standing on
top of good ice under fresh powder — "boots soak with no plunge, no drama, just wet feet a mile from
fire"); and going through thin ice at the inlet, which is the run-for-your-life clock. Sweat is the
fourth and the one nobody expects — the deferred cold debt of working hard in a heavy stack.

### 4.6 The four warmth paths (the rescue graph's own check)

Every survival goal must have at least three paths spending different key resources
(`rescue-graph.md` §2–3). Warmth's:

| path | key resource it spends | where |
|---|---|---|
| **fire** | fuel + an ignition source | the treeline and the north wood for fuel; the ignition source's own room |
| **insulation salvage** | tools (to strip) + time | mid and rear cabin: foam, batting, the blanket, the engine cover, clothes |
| **shelter / windbreak** | sweat + tools | the rear cabin (block the breach); outside (snow wall, boughs) |
| **huddle + fuselage + body heat — the floor** | nothing but proximity | any enclosed zone |

The softlock guard: the floor path needs no object at all, and the fire paths need at least two
different ignition sources present at the start.

### 4.7 The cold ladder (December)

The antagonist's schedule, indexed by game day, not by real time (`events-and-escalation.md` §2 —
proposals, tunable): ambient about −12 °C by day and −20 °C at night on day 1, falling to −24/−32 by
day 5 and −34/−42 by day 10, with storm bands over the top of it (first heavy snow around day 2–3, a
two-day near-whiteout blow, then clear-cold nights that are colder still — the aurora and the
temperature drop arrive together, and the design says so). Wind chill multiplies exposure. Nothing
here refuses a player; every line is a number that hurts more each day.

---

### The `make shelter` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | shelter |
|---|---|
| `goal` | shelter · a lean-to · a windbreak |
| `vague` | "How are you going to make a shelter?" |
| `roles` | **cover**: boughs, a sheet, a seat frame, the hull · **support**: a rigid thing or the wreck itself · **site**: the zone |
| `realize` | the first act the means imply — `lean <cover> against <support>`, `cover <opening> with <cover>` — which writes the zone's wind and roof numbers; a shelter is never one command |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

## 5. Interactions

**This depends on:**
- **06 Time, sleep and the clock** — warmth is an unattended process on the heartbeat; sleeping cold
  costs warmth per hour at a rate the bedding score sets; the 20× consensus advance is where a cold
  night actually gets spent, and "you wake shivering" is one of the interrupts.
- **07 Fire and shaping** — fire is one warmth path and the only drying source that works fast.
- **13 Events, escalation and weather** — supplies ambient temperature, wind and the storm bands;
  wind shift ("the breach faces it now") and ice sealing the cargo door are shelter events.
- **16 Players and kit** — the clothing draw, the luggage, the 206's interior; the engine cover, the
  blanket, the sleeping bag.
- **17 Rooms and living rooms** — zones carry the exposure band and the roof score; blocking a
  breach is state the room must remember and describe.
- **18 Materials and forms** — insulation, wind resistance and soak behaviour come from materials.

**These depend on it:**
- **09 Water** — eating snow costs heat; melting by body heat costs warmth.
- **10 Food and hunger** — calorie deficit is a warmth input; being cold burns calories.
- **11 Injury and first aid** — frostbite is a warmth failure with a location; hypothermia's
  confusion is a warmth band; a bleeding wound costs warmth.
- **14 Rescue paths** — a bright jacket is visual confidence; the walk-out is priced in warmth;
  distinct-resource routing exists so total warmth failure does not kill every rescue route at once.
- **15 Moral and social layer** — who gets the good coat, the blanket for the dying man, and whether
  you strip a body. Sharing warmth is the first co-op act, hours before the antenna.
- **19 Multiplayer** — the huddle is only meaningful with other bodies in the zone.

---

## 6. Open questions

1. **Is the warmth floor kept?** *(a)* Keep it — a competent party survives one fire-less night by
   huddle + fuselage + body heat, held by a property test. *(b)* Drop it — no fire on night one is
   death. **Recommendation: keep.** It is what lets the fire be a choice rather than a gate, and it
   makes the huddle — the social act — mechanically load-bearing. It needs Andrew's word because the
   provenance audit does not record him deciding it.
2. **Does shelter live on the zone or on an object?** *(a)* Two mutable numbers on the zone (wind
   exposure, roof) that built things write to. *(b)* Shelters as entities with the seed's full
   seven-property block. **Recommendation: (a) first**, because partial shelters then count for free
   and nothing needs a recipe; (b) as the growth path when built shelters need capacity and smoke
   ventilation of their own.
3. **Does layering stay linear?** v1 is "wear everything", unlimited and linear, per Andrew's
   directive. *(a)* Keep linear. *(b)* Diminishing returns past a coverage threshold.
   **Recommendation: keep linear until the cold clock bites**, then measure — the directive is about
   never refusing a wearable, which (b) does not violate, but stacking eleven shirts should probably
   stop paying at some point.
4. **What exactly does the huddle require, and what does it give?** Options range from proximity in
   the same zone, to an explicit shared act, to a shared covering (the blanket over two).
   **Recommendation: proximity gives a small shared bonus; a shared covering gives the large one** —
   it makes the blanket the object the party argues over, which is the point.
5. **Do we model body regions in the cold clock, or only in the clothing score?** v2 computes an
   exposure fraction per region already. *(a)* One core temperature, regions only shading the
   message. *(b)* Per-region cold that can frostbite a hand while the core is fine.
   **Recommendation: (b) for the extremities only** (hands, feet, face) — that is where frostbite
   lives and it costs one extra number, not six.
6. **Is there a `status` command at all?** `time-and-stakes.md` §5 proposes one; the never-a-menu
   rule makes any always-on readout suspect. **Recommendation: no separate status screen** — the
   self-view (`examine me`) and the composed scene already carry it, and the inventory footer
   carries the band. Bring `status` back only if playtests show players losing the thread.
7. **How does blocking the breach express itself in the grammar?** `cover breach with cover`,
   `block hull`, `stuff hole with jacket` are all in the census as attempts. **Recommendation: a
   `cover`/`block` operation over any opening** (the censuses voted it up from three rooms), not a
   bespoke breach verb.
8. **Sweat: in or out of v1?** It is the most-cited real lesson (never sweat in the cold) and the
   least visible mechanic. *(a)* Ship it with the first cold clock. *(b)* Defer.
   **Recommendation: ship it**, but only surfaced through the clothing line ("you are sweating in
   the parka") and the later cost — never as a warning.
9. **What is the honest cost of sleeping without shelter?** The bedding score is proposed but
   unnumbered. **Recommendation: a night on bare metal or bare snow should be survivable but
   expensive** — roughly the cost of a day's work — so that gathering boughs before dark is the
   obviously right thing nobody tells you to do.
10. **Do heated stones and hot water containers make v1?** They are in the seed's source list and
    they are real. **Recommendation: yes** — both fall out of existing operations (heat a thing by a
    fire, carry it) and they reward the fire you already built.

---

## 7. Review log

*Not yet reviewed. This document is the first pass gathering a scattered system; everything in §4
except the items marked as Andrew's is open for cutting.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18:** the `make shelter` goal rows added (document 04 §3.9 owns the form and the dispatch rule).

## 8. What exists today

**Built**
- `game/world/sim/systems/warmth.py` — the whole clothing model as data and derivation: derived
  wearability from material tags, insulation-grams with the mass cap, the five warmth bands, the wet
  fraction per material, per-region coverage with the shell's wind, an exposure fraction (the number
  a cold clock would multiply the weather by), bare-region reporting, and the mitten fine-work gate.
- `game/world/sim/operations/handlers/wear.py` — `wear`/`don` (auto-takes from the floor),
  `remove`/`doff`/`shed`, "take X off" routing, worn things refusing drop, stripping the dead.
- `game/world/sim/operations/handlers/wrap.py` — `wrap`/`bandage`/`insulate`/`swaddle`; wrapping with
  an insulating material sets `insulated`.
- `game/world/scenarios/whiteout/characters.py` — the five slots' worn rows carrying `covers`,
  `wind`, `waterproof` and the mittens' `fine_work: False`.
- The self-view: `worn_summary` / `self_view` in `warmth.py` — what you wear, the band, what is bare,
  what is soaked, behind both `look at me` and `examine me`.
- `game/tests/sim/test_warmth.py` and `game/tests/sim/test_kit.py` cover derivation, the band ladder,
  wear/shed, regions/wind/wet and the exposure fraction's ordering.
- Probes: `probes/kit.py` (each slot's self-view and pockets; mittens off) and `probes/census.py`
  (`rear_cabin.wear_cover`, `rear_cabin.wear_blanket`, `mid_cabin.wear_socks` all measured passing).

**Designed, not built**
- The cold clock itself: core temperature, the per-tick equation, the bands, the floor
  (`time-and-stakes.md` §4; the roadmap's step 3). `systems/clock.py` says so in as
  many words: its exposure tick "emits nothing consequential".
- Sweat, dexterity decay, movement effects and the signal value of a bright jacket
  (`players-and-kit.md` §4) — the fields exist, nothing reads them.
- Wetness as a quantity written by the world (snow, overflow, a plunge). `wet` exists only as a
  boolean today: authored on the soaked matchbox and written by `pour`. `warmth.py::wet_fraction`
  already reads grams and treats a bare `wet: True` as half-soaked, so the curve is waiting for the
  world to start writing numbers.
- The December cold ladder and the storm bands (`events-and-escalation.md` §2;
  `systems/weather.py` is a docstring).
- The per-zone exposure bands for all fifty outdoor zones (`rooms.md`) — authored as design data, not
  yet in `zones.py`, which carries only `terrain_tags` (one crash zone is tagged `exposed`).

**Nothing**
- **Shelter.** `game/world/sim/systems/shelter.py` contains a docstring and `from __future__ import
  annotations`. No zone carries a wind-exposure or roof value; no operation builds, blocks or covers
  anything.
- **Huddle.** No operation, no verb; `huddle` appears once in the parser vocabulary (mapped to `put`)
  and once as a `todo` phrasing probe from the agent corpus.
- **Blocking the breach.** `probes/census.py` carries `rear_cabin.cover_breach_with_cover`,
  `rear_cabin.block_hull`, `cockpit.block_windscreen`, `cockpit.stuff_hole_with_jacket` and
  `outside_nose.shelter_behind_nose` — all `todo`. There is no `cover`/`block` operation in the
  handler set.
- **Snow as a building material.** `rear_cabin.pack_snow` and `rear_cabin.build_wall_from_snow` are
  `todo` probes; `snow` is a material with insulation and potability, and nothing packs it.
- **Sitting, resting, bedding.** `sit on seat` is a `todo` probe in two rooms; there is no bedding
  score and no ground-contact term.
