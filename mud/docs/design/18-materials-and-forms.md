# 18 — Materials and forms: the material table in plain words, forms, what is missing

> **Status: draft for review** (created 2026-09-16). **Architecture counterpart:**
> [`ontology-closure.md`](../architecture/ontology-closure.md) §2–§3 (forms, derived capabilities) and
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) §4 (DR-04, the
> material model).
> **Sources:** `game/world/scenarios/whiteout/materials/table.py` (the table itself — the content of
> this document) · `game/world/sim/affordances.py` (the shipped forms vocabulary and the derivation) ·
> [`authoring-objects.md`](../guides/authoring-objects.md) (how a row is authored) ·
> [`objects.md`](../investigation/world/objects.md) "New-material & system flags harvested by the
> census" · [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md).

## 1. Status

Draft for review. The table below is the real content of the game as it stands — it is not a
proposal in the sense the other documents use, it is a transcription of what is loaded at boot. What
*is* open is everything about its growth: which natural materials come next, which property axes are
missing, and who adds them.

## 2. Provenance

### Andrew's decisions

**The natural world is in scope** (2026-09-07 / 2026-09-16, recorded in the provenance audit §1):

> "want to take an axe thing and chop the log up then sure. want to dig dirt then yeah. find a rock,
> maybe some clay, whatever."

**Abstract the affordance away from the object** (2026-09-07, recorded in the provenance audit §2):

> "a shard can cut but so can a knife, abstract it"

That second quote is the whole reason materials and forms exist as a system: nothing in this game
asks "is this the knife?", it asks "does this thing hold an edge?", and the answer comes from what it
is made of and what shape it is in.

**The world is open-ended** (2026-09-16, VISION.md): materials and forms are growing sets grown by
evidence, without a ceiling. **Every count in this document is a floor**, including the 32 and the 26
below.

### Proposals (Claude)

The contents of the table — every material, every ordinal value, every tag — are authored content, not
Andrew's decisions; the table's own docstring says "This is world-building content — tune freely".
The forms vocabulary, the derived-capability axes and their form factors are equally proposals
(labelled as such in the provenance audit §2 under "ontology-closure"). So is every gap and
recommendation in §4.7 and §6.

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
| `conductivity` | carries current — the radio and beacon wiring axis |
| `rigidity` | holds its shape under load — the leverage and heft axis |
| `absorbency` | soaks up water (and so gets heavy, and stops insulating) |
| `edibility` | food value |
| `potability` | safe to drink |

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
| `glass` | the windscreen, instrument faces | hard to cut, will not bend at all, will not burn, rigid, brittle — the shard source |
| `insulation_batting` | the quilted engine cover, wall batting | insulates almost better than anything (`very_high`); burns well and takes some work to light; cuts and tears with no resistance |
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
| `flesh` | the pilot; any body | cuts easily, middling to tear, bends easily, barely burns and is hard to light, toxic smoke. **It declares no `edibility`** — see §4.7 |
| `bone` | a body; later, antler and game | hard to cut, `extreme` to tear, hard to bend, barely burns, rigid |
| `chocolate` | the emergency ration | very edible; burns poorly and is hard to light |
| `rations` | the survival kit's food | very edible; burns poorly; cuts easily |
| `fish` | a family's frozen catch in the cooler | very edible; cuts easily; burns poorly; middling rigidity — hard as a plank until thawed |

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

**A documentation mismatch to fix in review:** `ontology-closure.md` §2's table lists 15 rows
covering 20 form words and calls the set "~15"; the code carries 26. The doc is behind the code, not
the other way round. Neither number is a ceiling (Q3).

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
- **The signifier rule**: every load-bearing capability must show in the examine text — "a shard of
  glass, one edge wicked-sharp". A capability nobody can see is the standard failure of this kind of
  system.

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
masses must be integers, and a puzzle-critical object needs its authored rule and ≥3 solution paths in
the rescue graph. The validator prints the material count on every run.

### 4.7 What is missing (from the census)

The valley census (`objects.md`, "New-material & system flags harvested by the census") went looking
for what a real person would pick up out there and came back with a list the table does not have:

> rock/stone (boiling stones, anvils, flakes — **presently absent!**), bone/antler (billet, tine,
> scales), fur/hide (marten, hare — insulation values), peat (poor wet fuel), lichen (flash tinder +
> famine food), punk/rotten wood (ember medium — distinct from sound wood), rubber (tire, tube —
> black smoke + elastic), kerosene (lamp fuel class), canvas (pack, tarp), babiche/rawhide (lacing),
> grease/fat (bearing grease, lard — lamp fuel + waterproofing), mica (worthless glitter — the honesty
> material), brass (benchmark, shells), paper (newspaper, photographs, cards — burnable heartbreak
> class).

Three of them — `rubber`, `paper` and `bone` — are in the table. **Stone is not**, which is the
sharpest gap in the table: Andrew's own example of the natural world is "find a rock", a rock is the
oldest tool there is (an anvil, a hammer, a boiling stone, a spark against steel), and the game
currently has nothing to make one out of. Soil and clay — his other two examples — are equally absent.

The census also flags that snow and ice are one word each in the table and about twenty in the world
(powder, wind-slab, drift, spindrift, sugar snow, sastrugi, rime, hoarfrost; black ice, shore ice,
pressure slab, overflow, skim ice, glare ice), and notes that "each wants at least a behavior note in
the table".

Two gaps are visible in the table itself rather than the census:

- **`flesh` declares no `edibility`.** With the default-to-`none` rule that means a body is not food,
  which contradicts the food path in the rescue graph and the `pilot_body` dilemma (design 12). Either
  the axis is added or the butchered output is a different material (`meat`) that carries it.
- **Liquids are nearly propertyless.** `water`, `fuel` and `alcohol` carry two or three axes between
  them. Nothing expresses viscosity, freezing point, or what a liquid does to a fire beyond the
  `extinguisher` tag — and in a December valley, "does it freeze, and when" is load-bearing.

## 5. Interactions

**Depended on by:** almost everything. Fire and shaping (07) reads `burnability`, `ignition_difficulty`
and the tinder derivation; warmth and clothing (08) reads `insulation` and `absorbency` (warmth is
insulation × capped mass, DR-25); water (09) reads `potability`; food and hunger (10) reads
`edibility`; the grammar (04) and the ontology (05) rest on capabilities rather than verb-to-tool
lists; rooms (17) and the player view (03) render derived objects through form-keyed prose; the pilot
and bodies (12) needs `flesh` to be food.

**Depends on:** the ontology and sufficiency document (05) for how the sets grow, and the world-building
loops (22), which are the mechanism that grows them.

## 6. Open questions

**Q1 — Which natural materials go in first?**
Options: (a) the three Andrew named — stone, soil, clay — plus what they obviously imply (a stone
holds no edge but takes a flake off, soil is a fire base on snow, clay holds water and takes a shape);
(b) the whole census list at once; (c) wait for the loops to hit walls and add by evidence.
*Recommendation:* (a) now — the absence of stone is a hole in his own example — then (c) continuously.
(b) authors properties for objects nobody has placed yet.

**Q2 — What property axes are missing, and which do we add before content needs them?**
Known candidates: `edibility` on flesh (or a `meat` material); a freezing point and a viscosity for
liquids; hardness/friability and a spark axis for stone; a wetness interaction for fuels that are
poor *because* they are wet (peat); an ember-medium axis distinguishing punk wood from sound wood;
`elasticity` for rubber and sinew. Options: (a) add an axis only when an operation reads it; (b) add
the obvious set now.
*Recommendation:* (a), with the `flesh`/`meat` fix taken immediately because a designed path already
depends on it.

**Q3 — The two forms lists.**
The doc says ~15 forms, the code has 26, and the code's comment still says "extend by evidence, never
speculatively" — phrasing the provenance audit removed from the docs as ceiling framing. Options:
(a) make the closure doc's table match the code and delete the stale comment; (b) treat the doc's 15
as the taught set and the code's 26 as the internal set.
*Recommendation:* (a). One list, floors everywhere, no ceilings in the comments.

**Q4 — Snow and ice sub-types: material rows, or state on one material?**
Options: (a) rows per sub-type (twenty-odd materials for snow alone); (b) one `snow` material plus a
state axis (density, crust, wetness) that the prose and the operations read; (c) the current single
row plus authored prose.
*Recommendation:* (b) — the difference between powder and wind-slab is a number, not a different
substance, and it is the same axis a snow shelter needs.

**Q5 — How do the loops add materials, and what stops the table drifting?**
The table is the hand-curated quality anchor (DR-04/DR-17), and the overnight loops are meant to grow
the world. Options: (a) agents propose rows, a person reviews each one before it lands; (b) agents add
rows freely and the validator plus probes are the only gate; (c) agents may add *tags and axes to
existing rows* freely but new materials need review.
*Recommendation:* (c). New materials are where the quality anchor actually matters; extending an
existing row is the cheap, safe half.

## 7. Review log

*Not yet reviewed. 2026-09-16: written by reading the shipped table and the closure spec; §4.3 is a
transcription, §4.7 and §6 are the honest gaps.*

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
- Coverage today (counted 2026-09-16): the 99 authored objects in `objects.py` plus the kit outfits in
  `characters.py` draw on **31 of the 32** rows, and every material they name exists in the table.
  `bone` is the one row authored ahead of an object that uses it.

**Designed, not built.** The stale "~15" forms table in `ontology-closure.md` §2; every material in
§4.7 (stone, soil, clay, fur/hide, peat, lichen, punk wood, kerosene, canvas, rawhide, grease, mica,
brass); the snow and ice sub-type behaviour; `edibility` on flesh or a `meat` material; any liquid
axis beyond potability.

**Nothing.** No process adds materials automatically; there is no bake pipeline yet (the ordinal→number
mapping in `materials.py` *is* the bake for now, as its docstring says), and no loop has yet proposed
a material row.
