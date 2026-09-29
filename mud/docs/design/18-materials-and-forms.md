# 18 — Materials and forms: the material table in plain words, forms, what is missing

> **Status: draft for review** (created 2026-09-16). **Architecture counterparts:**
> [`ontology-closure.md`](../architecture/ontology-closure.md) §2–§3 (forms, derived capabilities) and
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) §4 (DR-04, the
> material model). The table in §4.3 is a transcription of what is loaded at boot
> (`game/world/scenarios/whiteout/materials/table.py`; the forms and the derivation in
> `game/world/sim/affordances.py`; how a row is authored in
> [`authoring-objects.md`](../guides/authoring-objects.md)). What *is* open is everything about its
> growth: which natural materials come next, which property axes, and who adds them.

## 2. Decisions

### Andrew's decisions

- **2026-09-07, restated 2026-09-16 — the natural world is in scope.** Taking an axe to a log and
  chopping it up, digging dirt, finding a rock, maybe some clay — all of it is in.
- **2026-09-07 — abstract the affordance away from the object.** A shard can cut, and so can a knife.
  That decision is the whole reason materials and forms exist as a system: nothing in this game asks
  "is this the knife?", it asks "does this thing hold an edge?", and the answer comes from what it is
  made of and what shape it is in.
- **2026-09-16 — the world is open-ended** (`VISION.md`): materials and forms are growing sets grown by
  evidence, without a ceiling. **Every count in this document is a floor**, including the 32 and the 26
  below.
- **2026-09-18 — density is in.** Every material carries its real density; bulk derives from mass ÷
  density, and an authored bulk wins (§4.7a).
- **2026-09-18 — the code's 26 forms are canonical** (document 07), and `ontology-closure.md` §2 is
  corrected to match — one list, floors everywhere.
- **2026-09-18 — the ontology store's schema is designed in full, up front** (document 05).
- **2026-09-26 — heat and the rest are state systems.** Heat, wetness, spoilage, cooking and freezing
  are states on every entity that really has them, changed by systems: snow melts into water, food
  changes with heat, and that is part of the implementation of each object; body parts have heat as
  part of their ontology.
- **2026-09-26, 2026-09-27 — the season** is the first week of October in interior Alaska (document 13
  §4.2).

- **2026-09-28 — real numbers on every material** (§4.8): the physical axes the heat, water and food
  systems read are real numbers in real units, each with a source; the word scales stay for the
  judgement axes (cut, tear, bend, ignition, smoke).
- **2026-09-28 — the missing materials go in** (§4.7): stone above all, soil and clay, fur and hide,
  bone and antler, lichen, punk wood, peat, canvas, rawhide, grease and fat, kerosene, mica, brass;
  snow and ice as states of one substance, water; the six body materials in place of `flesh`; real
  freezing points, flash points and burn heat for every liquid aboard.

### Proposals (Claude)

The contents of the table — every material, every ordinal value, every tag — are authored content, not
Andrew's decisions; the table's own docstring says "This is world-building content — tune freely".
The forms vocabulary, the derived-capability axes and their form factors are equally proposals. So is
every gap in §4.7, the axes and materials of §4.8, and the order and growth of §4.9 — all for Andrew's
check.

## 3. In one paragraph

The player never meets "materials" — they meet a seat cushion that burns fast and stinks, a wool
blanket that is warm and hard to light, a windscreen that will not bend but will shatter into
something that cuts, a down parka that is the warmest thing in the valley until it gets wet. All of
that is two small tables and one function: what a thing is *made of* (its resistances, how it burns,
how it insulates) and what *shape* it is in (a shard, a rod, a strip, a sheet), and from the pair the
engine works out what the thing can do — hold an edge, take a point, give leverage, serve as cordage,
catch a spark. That is why a glass shard cuts and a foam cushion in the same shape does not, and why
nobody had to write a rule for "glass shard".

## 4. The design

### 4.1 What a material is (DR-04)

A material is an **ordinal property vector**: a set of named properties whose values are words on one
seven-step scale.

```
none < very_low < low < med < high < very_high < extreme
```

The engine maps those words to numbers at load (`world/sim/materials.load_materials`;
`none 0.0 · very_low 0.15 · low 0.3 · med 0.5 · high 0.7 · very_high 0.85 · extreme 1.0`). Words are
the authoring surface because they are fast to write and hard to get subtly wrong; numbers are what
the rules compare.

**Intensive, never summed.** A material's properties are *intensive* — they describe the stuff, not
the amount of it — so they are used only as **gates and rank relations** (`tool.edge −
target.cut_resistance`), never added together. The conserved *extensive* quantity is **mass in
integer grams**, and it lives on the object and its parts, not here (DR-04/DR-11).

**A property that is not listed is `none`.** `affordances.derive` reads every axis with a default of
0.0, so leaving an axis off a row is a decision, not an omission — see §4.7.

### 4.2 The axes, in plain words

Twelve axes are in use across the table today. Two of them read backwards from the intuition, which
is worth saying out loud to anyone editing a row:

| axis | what a **high** value means |
|---|---|
| `cut_resistance` | hard to cut — steel is `extreme`, foam is `very_low`. *(It is also what lets a material hold an edge: a thing must resist cutting to cut.)* |
| `tear_resistance` | hard to tear apart by hand |
| `bend_resistance` | hard to bend. **Glass is `extreme`** — it does not bend, it breaks |
| `burnability` | burns readily and hot once lit |
| `ignition_difficulty` | **hard to light.** Low is the tinder end: dry grass and paper are `very_low` |
| `smoke_toxicity` | the smoke will hurt you in a closed fuselage |
| `insulation` | keeps heat in — the warmth system's axis |
| `conductivity` | carries current — the radio and battery wiring axis |
| `rigidity` | holds its shape under load — the leverage and heft axis |
| `absorbency` | soaks up water (and so gets heavy, and stops insulating) |
| `edibility` | food value |
| `potability` | safe to drink |

`conductivity` here is electrical and is renamed `electrical_conductivity` so the heat system's
`thermal_conductivity` is not mistaken for it; `edibility` and `potability` become answers the food and
water systems derive from real axes and the entity's states, and `absorbency` gains a real number,
`holds_water` — §4.8 (2026-09-28).

Beside the properties each material carries **tags** — 27 in use, among them `flammable`, `fuel`,
`tinder`, `fabric`, `flexible`, `metal`, `conductive`, `cordage`, `wire`, `rigid`, `brittle`, `soft`,
`insulating`, `absorbent`, `liquid`, `organic`, `edible`, `food`, `frozen_water`, `windproof`,
`waterproof`, `extinguisher`. Tags are the categorical half: `flexible` is what lets a strip become
cordage, `metal` is what makes a sheet reflective.

### 4.3 The table today — 32 materials in plain words

*(`game/world/scenarios/whiteout/materials/table.py`, read 2026-09-16. A floor, not a target.)*

**Aircraft and cabin**

| material | where it is | what the table says |
|---|---|---|
| `synthetic_fabric` | the seat covers | cuts and tears easily, bends freely; burns well and lights easily, with toxic smoke; middling insulation and absorbency |
| `foam` | the seat cushions | almost no resistance to a blade or a tear; burns fiercely, lights at once, and has the most toxic smoke in the table; insulates well; no rigidity; soaks up water |
| `nylon_webbing` | the seatbelts | middling to cut, hard to tear, bends easily; burns moderately and takes work to light; poor insulation. Tagged `cordage` — the lashing of first resort |
| `steel` | frame, bolts, the multitool blade | the toughest thing here: `extreme` to cut and tear, very hard to bend; will not burn; conducts well; very rigid |
| `aluminum` | the hull skin, fittings | hard to cut, bends at middling effort, will not burn, conducts well, rigid |
| `plastic` | cases, the radio shell, the lighter | middling to cut, bends easily, burns moderately with toxic smoke, takes some work to light, middling rigidity |
| `rubber` | tyres, hose, insulation | middling to cut, bends at a touch, burns moderately with toxic smoke, insulates well, and conducts **nothing** — the one insulator against current |
| `copper_wire` | the panel loom, the antenna run | middling to cut, bends at a touch, conducts better than anything else in the table (`extreme`), not rigid |
| `glass` | instrument faces | hard to cut, will not bend at all, will not burn, rigid, brittle — the shard source. *(The 206's windscreen and windows are acrylic, not glass — §4.8, proposed by Claude.)* |
| `insulation_batting` | the quilted engine cover, wall batting | insulates almost better than anything (`very_high`); burns well and takes some work to light; cuts and tears with no resistance. *(Proposed by Claude: two materials — the fuselage's wall batting is fibreglass, which does not burn; the engine cover's polyester fill does — §4.8.)* |
| `fuel` | avgas from a ruptured line or a jerry can | burns as hot as anything and catches at a spark, with toxic smoke. Declares no `potability` and no extinguishing tag — it is not a drink and not a douser |

**Fibre, cloth and clothing** *(the kit's materials — players-and-kit, DR-25a)*

| material | where it is | what the table says |
|---|---|---|
| `wool` | the blanket | cuts easily, middling to tear; burns moderately but is **hard to light**; insulates well; absorbs water readily. Warmth, bandages, and fuel of last resort |
| `cotton_cloth` | shirts, rags | cuts with nothing, tears easily, burns well and lights easily, poor insulation, absorbs water readily |
| `leather` | the pilot's flight jacket, boots | middling to cut and tear, burns poorly, middling insulation |
| `down` | a parka's fill | the warmest thing in the valley (`extreme` insulation) and the thirstiest (`very_high` absorbency) — worthless soaked; burns well; no cut or tear resistance |
| `nylon_shell` | a parka's or ski jacket's outer skin | barely insulates on its own but absorbs nothing and is tagged `windproof` and `waterproof` — it stops wind, not cold; burns moderately with toxic smoke |
| `denim` | jeans, a jacket | poor insulation, cuts easily, middling tear resistance, burns well, absorbs water readily — cold when wet |
| `fleece` | a synthetic mid-layer | insulates well and stays warm damp (`low` absorbency); no cut resistance, tears easily; burns well and lights easily with toxic smoke — it melts near a flame |

**Fire and the woods**

| material | where it is | what the table says |
|---|---|---|
| `wood` | deadfall, branches, the drill board | middling to cut and bend, burns well, takes some work to light, middling insulation, rigid |
| `dry_grass` | tinder from the tussocks | no resistance to anything; burns as hot as the table goes and lights at the first spark; little smoke |
| `paper` | the flight manual, mail, photographs | no resistance to cut, tear or bend; burns very readily and lights at once with little smoke — excellent tinder |
| `cardboard` | freight cartons | cuts and tears easily, bends easily, burns well, takes some work to light, barely rigid |
| `wax` | lip balm, a candle | burns well and lights easily; no cut resistance; barely rigid — a slow, hot fuel |
| `alcohol` | the flask, hand sanitiser | burns very readily and catches at a spark; `low` potability — drinkable in the sense that it will not kill you, and it cleans a wound |

**Water, snow and ice**

| material | where it is | what the table says |
|---|---|---|
| `water` | melt, the lead, the thermos | fully potable; absorbs nothing; tagged `liquid` and `extinguisher` |
| `snow` | everywhere | middling insulation (the snow-shelter axis); middling potability; `low` edibility — you can eat it, and the heat cost lives in the water system, not here |
| `ice` | the lake, the overflow | low cut resistance, rigid, brittle, middling potability |

**Bodies and food**

| material | where it is | what the table says |
|---|---|---|
| `flesh` | the pilot; any body | cuts easily, middling to tear, bends easily, barely burns and is hard to light, toxic smoke. **It declares no `edibility`** — see §4.7. *(Proposed by Claude: it becomes the six body materials — skin, fat, muscle, bone, blood, organs — document 12 §4.3a; §4.8.)* |
| `bone` | a body; later, antler and game | hard to cut, `extreme` to tear, hard to bend, barely burns, rigid |
| `chocolate` | the emergency ration | very edible; burns poorly and is hard to light |
| `rations` | packaged ration food | very edible; burns poorly; cuts easily |
| `fish` | a family's frozen catch in the cooler | very edible; cuts easily; burns poorly; middling rigidity — hard as a plank until thawed, though a knife still shaves it |

### 4.4 Forms

A **form** is the shape a quantity of material is in. Materials say what a thing is made of; forms say
what shape it is in; capabilities fall out of the pair (`ontology-closure.md` §2).

The shipped vocabulary (`affordances.FORMS`) is **26 words**: `blade`, `shard`, `flake`, `piece`,
`scrap`, `strip`, `sheet`, `slab`, `board`, `rod`, `stick`, `bar`, `pole`, `spindle`, `point`,
`stake`, `bow`, `shavings`, `bundle`, `cord`, `block`, `vessel`, `ember`, `ash`, `liquid`, `cloth`.

Where they come from and what they lend (`ontology-closure.md` §2): `shard` from breaking glass or
ice — edge and point; `piece` from breaking a thing in two — heft if rigid; `scrap` from hacking a
part off a mechanical fastener — little, but fuel if it burns; `strip` from tearing cloth or bark —
cordage if flexible, tinder if thin; `sheet` from tearing hull skin — cover, wrap, windbreak, and an
edge if metal; `slab`/`board` from splitting wood — the drill board; `rod`/`stick` from a branch —
leverage and the drill spindle; `spindle` from carving a stick — rotation; `point`/`stake` from
whittling — a point; `bow` from stringing a springy stick — the thing that drives a spindle;
`shavings` from shaving wood — thin tinder; `bundle` from bundling grass — the tinder nest; `cord`
from paracord or a twisted strip — cordage; `vessel` from a can or a hollowed thing — it holds
liquid; `ember`/`ash` from friction or burning — ignition, and nothing.

**Forms are minted, not declared.** The handlers that mint objects (break, cut, tear, pry, and the
shaping family: `carve`, `split`, `shave`, `whittle`, `notch`, `string`, `bundle`) name the form they
produce and `apply()` copies it into the new object's state. Authored objects may declare one too —
the multitool is a `blade`, the whisky bottle is a `vessel`, a branch is a `rod`. The shaping grammar
is `VERB X into <form> [with Z]`, where the form word sits in the Y slot as a pseudo-noun
(`form:spindle`) exactly as zones do.

**One list** (Andrew, 2026-09-18): the code's 26 forms are canonical, and `ontology-closure.md` §2 —
which still lists about fifteen — is corrected to match; so is the stale "extend by evidence, never
speculatively" comment in `affordances.py`. Neither number is a ceiling.

*(Proposed by Claude, for Andrew's check:)* §4.8's materials bring forms of their own into the floor: a
carcass's quarters and fillets, a hide, a clay lump and coil, a snow block and ball, a coal. Snaring,
fishing and trapping (document 10 §4.8) bring three more: **`noose`** (a running loop of wire or cord —
the snare), **`hook`** (a bent pin or wire, or a carved bone or wood gorge that lodges crosswise in the
throat — the oldest fish hook), and **`net`** / **`mesh`** (cordage knotted into a grid — a gill net, a
dip net, a carrying bag). Each is a shape a material takes, with capabilities that follow from material
× form: a wire noose tightens and holds, a cord noose frays on a gnawing hare, a mesh strains water and
holds fish.

### 4.5 What the pair derives

`affordances.derive(entity, materials)` computes a thing's **capabilities** — named, levelled
affordances that verbs ask for by name, so no verb ever names a tool. The axes it produces today:
`edge`, `point`, `leverage`, `heft`, `abrasive`, `cordage`, `sheet`, `vessel`, `reflective`,
`insulating`, `absorbent`, `ignition`, `flame`, `ember`, `tinder`.

The rules, in plain words:

- **Edge** needs a material that resists cutting (≥ `high`) *and* a sharp form: a blade keeps all of
  it, a shard or flake most of it, a sheet some, a piece little. Foam in any shape has none.
- **Point** comes from a point, stake, shard, blade, flake or spindle, on either hardness or rigidity.
- **Leverage** and **heft** need rigidity *and* mass: a bar or a pole gives the most leverage, a rod
  or stick nearly as much — but a rigid thing under 100 g gives none at all (the toothpick gate), and
  heft rises with mass to a full value at 800 g.
- **Cordage** comes free with a `cordage` or `wire` tag, otherwise from a flexible material in `cord`
  or `strip` form. **Sheet** from a flexible material in `sheet` or `cloth` form (half value from a
  strip). **Vessel** from a `vessel` form that is not floppy.
- **Reflective** from a sheet, shard, flake or blade that is metal, glass or ice.
- **Insulating** and **absorbent** pass straight through from the material, so a verb can ask the
  thing rather than the table.
- **Fire** is state, not material: `ignition` and `flame` come from an object's own state (and a wet
  thing has no ignition), while **tinder** is material burnability gated on form — shavings, a
  bundle, a strip or a scrap, dry.
- **Capped**: a derived level never exceeds the lower of the material's and the form's own ceiling —
  free composition must not mint an exploit. **Authored wins**: an explicit `state["edge"]` on an
  object overrides the derivation, which is how the golden tools stay hand-tuned.
- **The signifier rule**: what a thing is like shows in its examine text as a couple of sensory cues — "a shard of glass, one edge wicked-sharp" — never what to do with it (2026-09-28; document 03 §4.6). A capability nobody can see is the standard failure of
  this kind of system; naming its uses is a menu.

### 4.6 How a row is authored

Materials are where the heavy authoring goes; objects are cheap (`authoring-objects.md`). A row is:

```python
"wool": {
    "props": {"cut_resistance": "low", "tear_resistance": "med", "burnability": "med",
              "ignition_difficulty": "high", "insulation": "high", "absorbency": "high"},
    "tags": ("fabric", "flexible", "insulating", "flammable"),
},
```

An object then names material ids, a mass in integer grams, and — when the shape matters — a
`state["form"]`. `make validate` gates it: every material id an object names must exist in the table,
and masses must be non-negative integers; a puzzle-critical object also has its authored rule
(`authored.py`). The validator prints the material count on every run.

### 4.7 What is missing (from the census — accepted 2026-09-28)

The valley census went looking for what a real person would pick up out there and came back with a
list the table does not have: rock and stone (boiling stones, anvils, flakes); bone and antler (billet,
tine, scales); fur and hide (marten, hare — insulation values); peat (poor wet fuel); lichen (flash
tinder and famine food); punk or rotten wood (an ember medium, distinct from sound wood); rubber (tyre,
tube — black smoke and elastic); kerosene (lamp fuel); canvas (pack, tarp); babiche and rawhide
(lacing); grease and fat (bearing grease, lard — lamp fuel and waterproofing); mica (worthless glitter —
the honesty material); brass (a survey benchmark); paper (newspaper, photographs, cards — burnable
heartbreak).

Three of them — `rubber`, `paper` and `bone` — are in the table. **Stone is not**, which is the
sharpest gap in the table: Andrew's own example of the natural world is finding a rock, a rock is the
oldest tool there is (an anvil, a hammer, a boiling stone, a spark against steel), and the game
currently has nothing to make one out of. Soil and clay — his other two examples — are equally absent.

The census also notes that snow and ice are one word each in the table and about twenty in the world
(powder, wind-slab, drift, spindrift, sugar snow, sastrugi, rime, hoarfrost; black ice, shore ice,
pressure slab, overflow, skim ice, glare ice), each wanting at least a behaviour note. §4.8 makes them
states of one substance, water.

Two gaps are visible in the table itself rather than the census:

- **`flesh` declares no `edibility`.** With the default-to-`none` rule that means a body is not food,
  which contradicts the pilot's body as food (Andrew, 2026-09-27; document 12) and the `pilot_body`
  dilemma (document 15). §4.8 replaces `flesh` with the six body materials of document 12 §4.3a, each
  with its food energy and its state-driven hazards.
- **Liquids are nearly propertyless.** `water`, `fuel` and `alcohol` carry two or three axes between
  them. Nothing expresses viscosity, freezing point, or what a liquid does to a fire beyond the
  `extinguisher` tag — and in the first week of October, when the air crosses 0 °C most days, "does it
  freeze, and when" matters. §4.8 gives freezing points, flash points and heats of combustion
  for every liquid aboard.

### 4.7a Density, and the bulk it gives (Andrew, 2026-09-18)

Inventory is limited by **weight and space**, and only weight exists today. A down sleeping bag is
light and enormous; the aircraft battery is small and crushing; a bundle of dry grass weighs nothing
and fills your arms. Without a second axis they all cost the same to carry.

**Decided 2026-09-18 (Andrew):** add **`density`** to the material table (grams per litre, the real
number for each material), and derive **bulk = mass ÷ density**, with an authored `bulk` on an object
winning — the same derive-then-override shape the capabilities already use (§4.5). One axis,
physically true, and it makes the sleeping bag and the battery behave differently for free. Every
material row therefore gains a density; the loops add one with every new material.

It also pays for itself elsewhere: density is what decides whether a thing floats in the lead, how
much a snow block weighs when you cut one, and how far a thrown stone carries. Capacity, the other
half, lives on containers (document 16); the grammar side is document 04 §3.11.

### 4.8 What the state systems need from a material (accepted 2026-09-28)

Heat, wetness, spoilage and the rest are states on every entity that really has them, changed by
systems; snow melts into water, food changes with heat, and body parts have heat as part of their
ontology (Andrew, 2026-09-26). A state lives on the entity: this log's temperature, this fish frozen
hard, this meat's spoilage. **The material says how that state changes** — how much heat it takes to
warm, how fast heat passes through it, when it melts, what it gives when it burns, what it feeds and what
in it can hurt you. That is what the table must carry.

**How the numbers are written.** The physical axes are real numbers in real units, with a source on
every row, exactly as `density` already is (grams per litre, the real number for each material —
Andrew, 2026-09-18). The ordinal words (§4.1) stay the authoring surface for the axes that are
judgements a gate compares — cut, tear and bend resistance, ignition difficulty, smoke toxicity —
because nothing adds them up over time. A system that moves heat, water or calories over time needs the
real quantity.

**The axes the state systems read**

| axis | unit | what it decides | read by |
|---|---|---|---|
| `density` *(decided 2026-09-18)* | g/L | bulk (mass ÷ density), floating, the weight of a cut snow block. For anything porous — foam, down, batting, cloth, grass, snow — it is the **as-found** density, and compression is a state: a stuffed sleeping bag and a lofted one are the same mass in a quarter of the space, and the lofted one is the warm one | carrying (04 §3.11, 16), heat |
| `specific_heat` | J/g·K | how much heat it takes to warm it, and gives back cooling: a stone stores heat, a blanket does not, water most of all | heat |
| `thermal_conductivity` | W/m·K | how fast heat moves through it: aluminium drains a hand; still air, snow and wool hold heat | heat, warmth (08) |
| `emissivity` | 0–1 | how much heat it radiates and takes in: bright metal and foil throw a fire's heat back and keep a body's in; dark cloth drinks the sun | heat; the `reflective` capability |
| `melts_at` · `latent_fusion` | °C · J/g | when a solid turns liquid, and the heat that takes with no change in temperature — snow sits at 0 °C until the last of it has melted | heat, water (09), food |
| `boils_at` · `latent_vaporisation` | °C · J/g | boiling, steam (09), drying | heat, water |
| `softens_at` · `chars_at` | °C | plastics sag and drip, fleece melts onto skin, leather shrinks | heat, fire |
| `heat_of_combustion` | MJ/kg | the heat a kilogram gives burning — a fire's output is this times the mass it burns a minute | fire (07), heat |
| `ignites_at` | °C | how hot it must get before a flame takes it; the physical ground under the ordinal `ignition_difficulty` | fire |
| `flash_point` | °C | for liquids: below it there is not enough vapour to catch from a spark or a passing flame | fire |
| `holds_water` | g per g dry | how much water it takes up and holds — the number behind `absorbency`; with the moisture state it decides wet weight, wet warmth and whether it will burn | wetness, warmth, fire |
| `electrical_conductivity` | ordinal | the existing `conductivity` axis, renamed so the heat system's conductivity is not mistaken for it | the radio and the battery (14) |
| `hardness` | Mohs | what scratches what; a stone harder than steel, with an edge, throws sparks off carbon steel | fire (07, method 6), shaping |
| `elasticity` · `shrinks_drying` | ordinal | rubber and green willow spring back; rawhide and sinew shrink tight as they dry — a lashing that tightens itself | shaping, binding |

**For food**, the materials of things that are eaten also carry, per 100 g:

| axis | what it decides | where the numbers come from |
|---|---|---|
| `energy`, with `protein` · `fat` · `carbohydrate` | calories, and what kind: hare and ptarmigan are protein with almost no fat, which is how rabbit starvation happens (document 23 §4.4) | USDA FoodData Central |
| `water_fraction` | the freezing point, the heat of freezing and thawing, how much it shrinks when dried | ASHRAE, "Thermal properties of foods" |
| `cooked_at` | the core temperature at which it is cooked and safe: bear and any ground meat 71 °C (160 °F); whole cuts of other game 63 °C (145 °F) with a rest; birds 74 °C (165 °F); fish 63 °C (145 °F) | USDA FSIS safe minimum temperatures; ADF&G for bear |
| `cooking_gain` | cooked meat and starch give more usable energy than raw — the body spends less digesting them | Carmody, Weintraub and Wrangham 2011, *PNAS* |
| `hazards` | what in it can hurt you, and what kills that: the trichinosis worm in bear meat survives freezing and dies only to cooking at 71 °C; rabbit fever (tularemia) in snowshoe hares, killed by cooking; botulinum toxin in a bulged can; poisons cooking does not touch — water hemlock's cicutoxin, the liver-destroying toxins of the deadly mushrooms | ADF&G, "Trichinosis in Alaska's species"; CDC; established toxicology |
| `spoils` | how fast it spoils at a temperature: bacteria double as fast as every 20 minutes between 4 °C and 60 °C, grow slowly below 4 °C and stop below freezing; fish goes faster than red meat; an ungutted carcass spoils from the gut outward | USDA FSIS, "Danger Zone" |

The states these drive live on the entity, each changed by a system (document 05 §4.5, `states`):
**temperature** on everything, body parts included; **moisture**; **phase** (frozen · thawing · thawed);
**cooked** (raw · cooking · cooked · charred); **spoilage** (fresh · going off · spoiled · rotten);
**dried** and **smoked** — this country's real preservation, dried fish strips and smoked meat, which
stop spoilage by taking the water out; **gutted**, for a carcass. `edibility` and `potability` become
answers the food and water systems derive from these, not one word on the material: a raw bear steak is
food *and* a hazard; the same steak cooked through is food. *The heat numbers belong to the heat-system
design and the rest to the food-state and spoilage design — both to be written.*

**One substance, water — snow and ice are its states.** Snow and ice are both solid water. What
separates powder from wind-slab is how much air is in it, which is a number, and how its grains are
bonded, which weather and people change. So the table carries **water**, with the constants of all
three phases, and the entity carries the states: phase (ice · liquid · vapour — steam is document 09's
entity), density, grain and crust, liquid-water content (October snow near 0 °C is wet, sticky and
packs; cold snow is dry and does not), temperature, and for ice its thickness and clarity. The twenty
names — powder, wind-slab, sugar snow, rime, skim ice, black ice… — are words the prose and the
synonyms key on those states (document 03, extensions 2 and 4), not twenty materials. The existing
`snow` and `ice` rows are how the code says this today; in the store they become states of `water`.
It follows Andrew's rule that snow melts into water as part of the object's own implementation
(2026-09-26), and the same density is what the snow shelter reads (conductivity rises with it) and what
document 09's melt ratios already are.

| water as | density (g/L) | what it does |
|---|---|---|
| new snow, fallen calm | 50–70 | ~14–20 L of it to melt one litre; warm to lie under, useless to build with |
| damp new snow | 100–200 | packs into snowballs, and into walls where there is enough of it — the first snows of October |
| settled snow | 200–300 | three to five litres of it per litre of water |
| wind-packed snow | 350–400 | cuts into blocks; about 3 L per litre (document 09's figure) |
| ice | 917 | ~1.1 L per litre; floats; bears a walking person at about 10 cm of clear ice |

(Cuffey and Paterson, *The Physics of Glaciers*, Table 2.1.) Snow's thermal conductivity rises with its
density — about 0.05 W/m·K for new snow, about 0.13 at 300 g/L, about 0.25 at 400 (Sturm and others
1997, *Journal of Glaciology*) — against 2.2 for ice and 0.024 for still air: loose snow insulates like
a quilt, packed snow like wood, ice hardly at all. That is how a snow shelter and a snow wall work, from
one axis — though this week's couple of inches is never enough snow to build with (document 13 §4.2).
The first ice of the season is the other half: **10 cm (4 in) of clear ice to walk on** is the rule
Alaskans are given; white snow-ice is weaker than clear; skim ice a few millimetres thick holds nothing.
Ice thickens roughly with the square root of the cold it has accumulated, and a blanket of new snow on
top slows it (Stefan's ice-growth law; a first figure for the weather system). This week it gets the
small ponds to a few centimetres and skins the lake's calm bays, so no ice holds a person: walking out
on any of it breaks it (document 13 §4.2).

**Every material, first physical figures** *(handbook values, rounded; ranges where the real thing
varies; each row's pass confirms its figure at source when it writes the row — the sources are listed
below)*

| material | density g/L (as found) | specific heat J/g·K | thermal cond. W/m·K | heat of combustion MJ/kg | the temperature, or the fact, that matters |
|---|---|---|---|---|---|
| synthetic_fabric (polyester or nylon upholstery) | 300–500 folded (fibre 1,140–1,380) | 1.2–1.7 | ~0.05 as cloth | 24–31 | melts 220–260 °C and drips |
| foam (flexible polyurethane) | 20–50 | ~1.4 | 0.03–0.04 | 24–27 | lights at ≈300 °C; its smoke carries carbon monoxide and hydrogen cyanide |
| nylon_webbing | 600–900 | 1.7 | 0.25 solid | ~31 | melts 220–260 °C |
| steel — carbon / stainless | 7,850 | 0.49 | ~50 / ~16 | — | carbon steel throws sparks off a hard stone; stainless barely does |
| aluminum (airframe alloy) | 2,780 | 0.88 | ~120 | — | melts 500–640 °C — in a fire's coals; with water in it, a pot holds |
| plastic (ABS trim) | 1,050 | ~1.4 | ~0.17 | ~36 | softens near 100 °C |
| rubber (tyre) | ~1,150 | ~1.9 | 0.15–0.2 | 32–37 | burns with black, oily smoke — a signal |
| copper_wire | 8,960 | 0.39 | ~400 | — | melts 1,085 °C |
| glass (instrument faces) | 2,500 | 0.84 | ~1.0 | — | cracks when heated unevenly |
| insulation_batting — two materials (below) | fibreglass 10–30 · polyester 10–20 | 0.84 · 1.3 | 0.035–0.045 | none · ~24 | fibreglass does not burn |
| fuel (100LL avgas) | 720 | ~2.0 | ~0.13 | 43.5 | flash point near −40 °C; stays liquid to at least −58 °C; its vapour is heavier than air and pools low |
| wool | 100–300 folded (fibre 1,310) | 1.36 | ~0.04 as cloth | ~20.5 | chars and puts itself out; holds 13–16% of its weight as water without feeling wet |
| cotton_cloth · denim | 200–500 (fibre 1,540) | 1.3 | ~0.04–0.06 dry, far more wet | 16–17 | holds 7–8% as vapour and a great deal of liquid water; cold when wet |
| leather | 850–1,000 | ~1.5 | ~0.15 | ≈18–20 | shrinks and hardens heated wet |
| down | 3–15 lofted; far denser stuffed | ~1.3 | 0.02–0.03 lofted | ≈20 | collapses wet — the loft is the warmth |
| nylon_shell | 400–600 as cloth | 1.7 | — | ~31 | melts near 220 °C |
| fleece (polyester) | 50–100 | 1.3 | 0.04–0.05 | ~24 | melts near 250 °C and drips; holds under 1% water |
| wood (white spruce at 12% moisture) | ~420–460; green wood carries up to its own dry weight again in water | 1.2 dry, more wet | 0.10–0.13 across the grain | ~20 dry | a flame takes it near 300 °C; green wood hisses until dried |
| dry_grass | 20–60 loose | ~1.2 | 0.04–0.07 | 15–17 | lights at ≈250–300 °C |
| paper | 700–1,100 | 1.34 | 0.05–0.1 as a stack | 15–17 | lights at 220–250 °C |
| cardboard | 100–150 corrugated | 1.3 | 0.05–0.07 | 15–16 | lights about as paper does (≈) |
| wax (paraffin; lip balm is waxes and oils) | 900 | ~2.1 | 0.25 | 42–46 | melts 46–68 °C — a candle is a wick drinking melted wax |
| alcohol — sanitizer (62–70% ethanol) · whisky (40%) | ~880 · ~950 | ~3 · ~3.8 | — | only the ethanol burns (26.8 for pure) | flash point ~23 °C · ~26 °C: **cold, it will not catch** until warmed or given a wick; whisky freezes near −25 °C |
| water | 1,000 | 4.18 | 0.56 | — | freezes at 0 °C (334 J/g to do it); boils at 100 °C at sea level, about a degree less per 300 m up |
| snow · ice | the table above | 2.1 | the paragraph above | — | melts at 0 °C |
| flesh — the body materials below | ~1,050 | ~3.5 | 0.4–0.5 | — | tissue freezes just below 0 °C |
| bone | 1,700–2,000 | ~1.3 | 0.3–0.6 | burns poorly | calcines white in a hot fire |
| chocolate | ~1,250 | ~1.6 | ~0.2 | — | melts near 34 °C; 535 kcal per 100 g |
| rations (ration bars, Pilot Bread) | ~1,000 | ~1.5 | — | — | 430–500 kcal per 100 g |
| fish (salmon) | ~1,050 | 3.6 thawed · 1.9 frozen | 0.5 thawed · ~1.5 frozen | — | freezes near −2 °C; coho 146 kcal per 100 g; thaws more slowly than it froze, because the thawed outside conducts worse |

**What the valley, the season and the state systems add.** Every one is in the design, each with the
axes above, and each gives a survivor a real distinction to act on:

| material | where | the real distinction |
|---|---|---|
| **the body materials** — skin, fat, muscle, bone (with marrow), blood, organs | every body: the pilot's (document 12 §4.3a), every kill | `flesh` becomes these six, the same for a person, a hare or a bear, each species with its own figures. Muscle is about 1,300 kcal a kilogram and fat about 5,700 (Cole 2017, *Scientific Reports*); blood freezes; marrow is mostly fat |
| stone (the Interior's schist, granite and quartz, in bedrock and creek gravel) | the ridge, the creek bar, the erratic | 2,600–2,750 g/L, 0.79 J/g·K, 2.5–3.5 W/m·K; quartz is hardness 7. It stores heat — a kilogram at 400 °C holds enough above boiling to warm a litre of water by about 55 °C (stone-boiling; a hot stone in a sock warms a bed); it strikes sparks off carbon steel; **wet creek stones can burst in a fire** as the water in them turns to steam |
| soil (silt and loam) | everywhere underfoot | 1,100–1,600 g/L; thawed, it digs; frozen, it is nearly rock, and it carries heat better than thawed soil because ice conducts four times better than water. In early October it is a frozen crust over soft ground, thicker every cold night until snow covers it; a fire thaws it |
| clay | the creek cut, the pond edge | plastic only at the right water content (a state), crumbling dry, rock-hard frozen; fired above about 600 °C — which a hot fire reaches — it becomes pottery: a vessel |
| sphagnum and peat | the muskeg | sphagnum holds many times its dry weight in water and was a wound dressing in the First World War; dry peat burns slowly (~20 MJ/kg dry), wet peat not at all |
| lichen | the ridge, the spruce | reindeer lichen and the hair lichens on spruce: flash tinder dry; famine food only after boiling out its acids |
| punk wood, chaga | the old birch, rotten logs | hold an ember and smoulder for hours — the way to carry fire |
| birch bark | the birch stand | rich in betulin and oils: it lights even damp; it peels in sheets — a container, a torch |
| spruce pitch | any wounded spruce | sticky warm, brittle cold; burns hot and sooty; antiseptic on a wound |
| fat — tallow, lard, bear fat, fish oil | kills, Holt's shelf | 900–920 g/L, ~39 MJ/kg, ~900 kcal per 100 g (USDA); melts between 30 and 50 °C (fish oil stays liquid) — food, lamp fuel on a wick, waterproofing for leather |
| hide, fur, rawhide, sinew | kills, the marten set | fur insulates by its loft; a snowshoe hare's skin is paper-thin and tears; rawhide and sinew shrink and harden as they dry; boiled hide is the food of last resort |
| feathers | birds | a ptarmigan's down is down |
| berries, roots, mushrooms — one material per species | the tussocks, the bars, the marsh edge | fresh berries run 40–60 kcal per 100 g (USDA: cranberries 46, blueberries 57), rose hips far more (162); baneberry and water hemlock carry their poisons, and cooking does not help |
| acrylic | the 206's windscreen and windows | `glass` in the table is wrong for them — general-aviation windscreens are acrylic (LP Aero Plastics makes the 206's). 1,180 g/L; softens near 105 °C; burns bright with little smoke (~25 MJ/kg); cracks rather than bends; scores and snaps along a line |
| fibreglass batting | the fuselage walls and ceiling | light aircraft are usually lined with it: it does not burn, it itches and cuts skin, it insulates dry and lofted. The engine cover's polyester fill does burn — `insulation_batting` is two materials |
| lead | the battery's plates, the tackle's sinkers | 11,340 g/L; melts at 327 °C — a fire melts it into sinkers or weights |
| battery electrolyte (sulfuric acid) | the aircraft battery | burns skin; a charged battery's freezes near −60 °C, a flat one's near −7 °C — a dead battery cracks on an October night |
| kerosene | Holt's lamp | ~800 g/L, ~43 MJ/kg; flash point 38–72 °C — safe to handle, needs a wick |
| canvas (cotton duck) | the work coats, a tarp | cotton's behaviour; windproof tight and dry |
| charcoal, wood ash | what a fire leaves | charcoal burns hot with no flame and no smoke (~30 MJ/kg); ash wetted makes lye — it scours a vessel and stings a wound |
| brass, mica | fittings and shells; the schist | mica is glitter in the schist — worthless, as the census says, except where a book of it splits into clear sheets that stand a fire's heat |

*Sources for §4.8:* The Engineering ToolBox and the CRC *Handbook of Chemistry and Physics* (densities,
specific heats, conductivities, melting points) · USDA Forest Products Laboratory, *Wood Handbook*
(FPL-GTR-282, 2021), chapters 4–5 · Babrauskas, *Ignition Handbook* (2003) · ASTM D910 (aviation
gasoline) · FAA Technical Note DOT/FAA/TC-TN10/19 (Cavage 2010, alcohol-based hand sanitizer — the 62%
gel's flash point near 23 °C; chilled sanitizer failed to ignite) · textile standard moisture regain
(ASTM D1909) · Cuffey and Paterson, *The Physics of Glaciers* (4th ed.), Table 2.1 · Sturm, Holmgren,
König and Morris 1997, "The thermal conductivity of seasonal snow", *Journal of Glaciology* 43(143) ·
Alaska's News Source, 2025-11-14, on measuring ice (4 in of clear ice) · ASHRAE *Handbook —
Refrigeration*, "Thermal properties of foods" · USDA FoodData Central · USDA FSIS, safe minimum
internal temperatures and "Danger Zone" · ADF&G, "Trichinosis in Alaska's species" and "Parasite
reminds hunters: bear meat…" · Carmody, Weintraub and Wrangham 2011, *PNAS* 108(48) · Cole 2017,
*Scientific Reports* 7:44707 · LP Aero Plastics (206 acrylic windscreens) · IFLScience, "Why you should
never use river rocks in a campfire" · U.S. Army FM 21-76 (the metal fuselage in the cold).

### 4.9 The order materials go in, and how the table grows *(proposed by Claude, for Andrew's check)*

**The order.** Every material named in §4.7 and §4.8 is in the design: the ontology store's
`materials.yaml` carries each, with its axes and a source for every number, and the loops add more
(document 05 §4.5). The only order is the runtime table's, and it follows the system build order
(document 06: scheduler → fire → warmth → hunger and thirst → injury → the pilot's body and `status`):
each material lands with the first system that reads it. **With fire** — stone (the hearth ring, sparks
off carbon steel, heated stones), birch bark, punk wood and chaga, lichen, spruce pitch, charcoal and
ash, kerosene, and the heat axes on every row. **With warmth** — fur and hide, feathers, canvas, the
batting split in two, acrylic. **With water** — water's phases and snow's states. **With hunger** — the
six body materials, fat, fish and game species, berries, roots and mushrooms with their hazards. **With
injury** — sphagnum, spruce pitch as an antiseptic, willow bark. **Soil and clay** come with the first
`dig`, which the season brings forward: in early October the ground is bare or under a few
centimetres of snow, and roots are there to be dug (document 23). Stone leads, because fire needs it.

**How the table grows.** By document 05's store: the loops write material rows into `materials.yaml` as
candidates, with provenance; the merge unions and never drops; nothing reaches `table.py` until the
zone that uses it is finalized and the converter writes it; a row is never deleted, only superseded;
`make validate-ontology` checks the schema. What stops drift is that real life is the default answer
(`README.md`): every physical number on a row carries its source, and the validator treats a physical
axis without one as an error — so an agent can add a material or a value freely, and cannot add an
unsourced one.

## 5. Interactions

**Depended on by:** almost everything. Fire and shaping (07) reads `burnability`, `ignition_difficulty`
and the tinder derivation; warmth and clothing (08) reads `insulation` and `absorbency` (warmth is
insulation × capped mass, DR-25); water (09) reads `potability`; food and hunger (10) reads
`edibility`; the grammar (04) and the ontology (05) rest on capabilities rather than verb-to-tool
lists; rooms (17) and the player view (03) render derived objects through form-keyed prose; the pilot
and bodies (12) needs the body to be food. The **heat system** and the **food-state and spoilage
system** — neither has a design document yet, both to be written — read the physical axes of §4.8; the
rooms and the plane (17 §4.8) read the aluminium, the acrylic and the batting.

**Depends on:** the ontology and sufficiency document (05) for how the sets grow, and the world-building
loops (22), which are the mechanism that grows them.

## 6. Open questions

None open. Claude's proposals — the new forms (§4.4), the axes and materials of §4.8, and the order and
growth of §4.9 — are for Andrew's check at this document's sitting.

## 7. Review log

- **2026-09-16 (Claude):** written by reading the shipped table and the closure spec; §4.3 is a
  transcription, §4.7 the honest gaps.
- **2026-09-18 (Andrew):** `density` is in — bulk derives from mass ÷ density, authored wins; inventory
  is limited by weight and space (document 04 §3.11).
- **2026-09-26 (Andrew, in document 10's review):** heat, spoilage, cooking and freezing are state
  systems on every entity that really has them, body parts included.
- **2026-09-26 (Claude, self-review):** the physical axes the state systems read, as real numbers with
  sources; water as one substance with snow and ice as its states; first physical figures for every
  row; the materials the valley, the season and the systems add; the windscreen is acrylic,
  `insulation_batting` is two materials, `conductivity` is renamed; the forms `noose`, `hook` and
  `net`/`mesh`; the order materials go in and how the table grows — all for Andrew's check.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built.**
- `game/world/scenarios/whiteout/materials/table.py` — **32 materials** (the count at the top of §4.3),
  using **12 property axes** and **27 tags**. A floor.
- Loaded at boot: `game/world/scenarios/whiteout/content.py` calls
  `world.sim.materials.load_materials(MATERIAL_TABLE)` at import and `content.load()` runs from
  `game/server/conf/at_server_startstop.py`; the same `MATERIALS` map is what the commands
  (`cmd_act.py`, `cmd_items.py`) and the pure tests use, so the shell and the probes cannot drift.
- `game/world/sim/materials.py` — the ordinal→number map and the loader (it raises on an unknown
  ordinal word, so a typo in a row fails loudly).
- `game/world/sim/affordances.py` — `FORMS` (**26** words) and `derive()` producing the fifteen
  capability axes in §4.5, with the caps, the mass gates and the authored-override rule.
- `game/world/sim/validation` — `make validate` checks that every material id an object names exists,
  and prints the material count.
- Coverage (counted 2026-09-16): the 99 authored objects in `objects.py` plus the kit outfits in
  `characters.py` draw on **31 of the 32** rows, and every material they name exists in the table.
  `bone` is the one row authored ahead of an object that uses it.

**Designed, not built.** The correction of `ontology-closure.md` §2's forms table (it still says about
fifteen) and of the comment in `affordances.py`; every material in §4.7 (stone, soil, clay, fur and
hide, peat, lichen, punk wood, kerosene, canvas, rawhide, grease, mica, brass); snow and ice as states of
water; the body materials in place of `flesh`; any liquid axis beyond potability. `density` — decided
2026-09-18 — is not yet in `table.py`; nor is any axis of §4.8, or any of the materials §4.8 adds.

**Nothing.** No process adds materials automatically; there is no bake pipeline yet (the ordinal→number
mapping in `materials.py` *is* the bake for now, as its docstring says), and no loop has yet proposed
a material row.
