# 08 — Warmth, clothing and shelter

> **Status: reviewed with Andrew 2026-09-18.**
> **Architecture counterpart:** [`../architecture/clothing-warmth.md`](../architecture/clothing-warmth.md)
> (DR-25, the shipped clothing model).

---

## 2. Decisions

### Andrew's decisions

- **(2026-10-02)** The body's core temperature follows the real clinical staging of hypothermia —
  cold-stressed, mild, moderate, severe (§4.1) — felt in the text and the warmth meter, never shown as a
  number.
- **(2026-07-03)** A player can wear everything a body can wear. Clothing is a system, not flavour;
  wearability is derived from what a thing physically is, never from a list of approved garments (the
  directive behind DR-25).
- **(2026-09-07)** Warmth comes several ways — a blanket, jackets, other people (sharing a blanket);
  the party can make a fire, and a lean-to outside if they want. Fire is one way among several, and
  the social way — two bodies under one blanket — is named explicitly.
- **(2026-09-07)** Clothing affects warmth loss.
- **(2026-09-07)** Each player starts with a different clothing draw (and a different injury and
  pockets draw). What a player is wearing when the plane stops moving is not chosen.
- **(2026-09-16)** The plane is a Cessna 206-class single with a four-seat interior; its thin skin
  and split hull set the shelter. Descriptions are composed from state: "your feet are soaked" is the
  scene and the self-view telling you what is true.
- **(2026-09-17, 2026-09-27)** The clock runs at 15 game-minutes per real minute; a fast forward the
  players agree to runs it at about 150×, and a player waking or any non-ambient event drops it back to
  15× (document 06).
- **(2026-09-18)** There is no guaranteed warmth floor. Night one is not as cold: a party that stays
  inside the wreck survives it in the clothes they crashed in, without needing to huddle. Going out
  saps them without fire, food and better gear, though they can go out for a little while. After the
  first night it gets colder, and they need a heat source, better gear, conserving (anything they can
  use as a blanket included) or huddling — and huddling with someone conserves warmth too. Most parties
  will have fire by then if they spend the first day trying for it (§4.1a).
- **(2026-09-18)** Outdoors, shelter is two mutable numbers on the zone — wind exposure and roof —
  that built things write; shelters as objects with the full property block are the growth path (§4.4).
- **(2026-09-18, 2026-09-28)** **Clothing is layered**: extra layers go on over what someone wears, as
  long as they fit — a parka over a sweater, never a sweater over a parka, and the kid's jacket will not
  go on an adult. Layering adds linearly for now; whether stacking stops paying past some point is
  measured once the cold clock bites.
- **(2026-09-18, 2026-09-28)** The huddle: being close gives a small shared bonus; a shared covering
  gives the large one. **Two can huddle under one blanket, no more**; the others huddle together for
  warmth or put on extra layers.
- **(2026-09-28)** **On night one the cold does not kill.** The party will not have fire yet and not
  everyone has a blanket; the cold costs their warmth and their rest, by how well they manage it —
  staying in the wreck, huddling, layering, sealing the openings (§4.1a).
- **(2026-09-18)** The extremities — hands, feet, face — have their own cold, for frostbite.
- **(2026-09-28)** Being next to a fire is a real position — approach it, sit next to it — and the fire's
  radiant heat reaches those close to it (document 17 §4.8).
- **(2026-09-28)** An opening can be patched from outside as well as inside — a tarp lashed over the
  tear from outside, boughs or snow packed against it — and Holt's cabin holds warmth like the plane's
  cabin (document 17 §4.8).
- **(2026-09-18)** Covering and blocking are one generic `cover`/`block` operation over any opening,
  not a bespoke breach verb.
- **(2026-09-18)** Sweat is in, surfaced only through the clothing line ("you are sweating in the
  parka") and its later cost — never as a warning.
- **(2026-09-28)** Getting wet is how the cold hurts most — the whole body, not only hands and feet:
  breaking through the ice, the wet flurries, the creek, and sweat, which keeps a body warm while it
  works and chills it once the work stops.
- **(2026-09-18)** Sleeping without shelter is survivable but expensive *(Claude's starting point, not
  yet decided: roughly the cost of a day's work)*.
- **(2026-09-18)** Heated stones and a warm vessel are in.
- **(2026-09-18)** There is a `status` screen: injuries such as frostbite or a break, and anything a
  person can sense about themselves — hunger, cold, tiredness — in band words, on request (§4.9).
- **(2026-09-18)** You hear your shelter leaking: the tail wreckage and the torn-open parts of the
  plane give feedback, such as hearing the wind blow in (§4.8).
- **(2026-09-26)** Heat is a state system: heat on every entity, body parts included; a fire heats its
  area and leaves residual heat around it; the plane's cabin is rooms like any others, with openings,
  open or closed, and a shared internal heat (2026-09-28; document 17 §4.8).
- **(2026-09-27)** The season is the first week of October in interior Alaska, with the same weather
  every run; the temperatures, wind and snow by day are document 13 §4.2.
- **(2026-09-27)** Aboard: the sleeping bag is buried with the tail wreckage; two blankets are hidden
  inside the plane; there is no survival kit. Up to five play, and a seat nobody plays is
  a dead character whose clothes and pockets can be searched.
- **(2026-09-27)** Nothing kills instantly: death comes by the body running down — blood loss, the
  cold, thirst and the rest — on real clocks, with time to respond.
- **(2026-09-27)** Players see **meters** for what a person can sense about their own body — people
  are not cut off from their own senses: seven bars with no numbers in the prompt line — hunger,
  thirst, warmth, rest, pain, stamina and blood. The `status` screen stays (§4.9).
- **(2026-09-27)** A tarp is aboard, to help seal the openings the crash tore in the plane; branches
  and anything else that covers serve too, and a lean-to is in (document 16). Carbon monoxide builds
  only where the space does not breathe enough for its fire (document 11 §4.4).

### Proposals (Claude)

- **The warmth-source list and the shelter property block**, carried from the first AI-written seed
  through GDD §31–§36. They are good lists and this document keeps them, as proposals.
- **The clothing model's mechanism** — coverage by body region, the shell's wind, waterproofing, the
  wet fraction, sweat, dexterity, movement, signal, sharing (with document 16 §4.4).
- **The warmth clock** — core temperature as an integer, the per-tick equation, and the bands, which
  follow the clinical staging of hypothermia (§4.1).
- **Shelter's mechanism** — the exposure bands and roof score per zone and what writes them (§4.4).
- **All numbers** — thresholds, bands, region shares.

---

## 3. In one paragraph

You come to in a cold aluminium tube in the first week of October with whatever you happened to be
wearing, and from that minute the cold is spending you. It is not a stat you manage; it is the wind
through the tear in the hull, the snow melting into your sleeve, your fingers losing the knot you are
trying to tie. You get warmth back the way people actually do: you put more on — your own bag,
someone else's sweater, the quilted engine cover from behind the rear seats — you get out of the wind, you
block the hole the wind is coming through, you get off the metal floor onto boughs, you light a fire
if you can, and when none of that is enough two of you share the blanket and the rest press close or
layer up (2026-09-28), which is warmer than any of you alone. The
game never tells you to do any of this. It tells you your hands are numb, that the wind is coming in
through the breach, that the engine cover is thick and quilted — and lets you work out the rest.

---

## 4. The design

### 4.1 The rules

1. **Heat is a state on the body, surfaced as words.** Heat is a state on every entity, body parts
   included (Andrew, 2026-09-26). A body carries its core temperature — an integer in tenths of a
   degree Celsius (370 = 37.0) — and the extremities (hands, feet, face) cool on their own, which is
   where frostbite lives (Andrew, 2026-09-18). The player never sees a number; they see a band, the
   meters (§4.9) and, better, a composed sentence about their hands and their feet. *(The integer and its unit are a
   proposal.)*
2. **Every source is physical and additive.** There is no "warmth buff". The seed's list stands as
   the coverage target — *fire · windbreak · shelter · dry clothing · layering · insulation from the
   ground · huddling · heated stones · hot water containers · moving out of the wind · closing
   fuselage gaps · a snow trench · a snow wall · reduced sweating and exertion · sharing body heat*
   (GDD §31–§36). Each is a thing you do to the world, and the world remembers it. This week lays only
   a couple of inches of snow (document 13 §4.2), too little for a trench or a wall; a windbreak of
   boughs, logs, rocks or the wreck's panels does that work (§4.4). Heated stones and a warm vessel
   are in (Andrew, 2026-09-18).
3. **The loss side accounts for** ambient temperature · wind exposure · wet clothing · clothing
   insulation · shelter insulation · ground contact · fatigue · calorie deficit · fire distance ·
   body condition. The per-tick form proposed:
   `Δ = −exposure(zone, weather, wind) + insulation(clothing, wet penalty) + fire_heat(distance)
   + activity_heat − wet_skin_penalty + huddle_bonus`, with the fire's heat read from the heat state
   around the body (document 07 §4.5).
4. **The bands follow the clinical staging of hypothermia** (2026-10-02; Wilderness Medical Society,
   2019): cold-stressed but not hypothermic at 35–37 °C (cold and
   shivering, the mind clear); mild hypothermia at 35–32 °C (shivering hard, clumsy); moderate at
   32–28 °C (impaired consciousness, and the shivering stops); severe below 28 °C (unconscious; the
   risk of the heart stopping rises, high below 24 °C). The band words and the exact thresholds are
   drafted with the warmth numbers (`PLAN.md` A5); document 11 §4.6 carries the same thresholds. The
   cold kills on its real clock, never at once (2026-09-27).
5. **The night-one rule** (§4.1a): the first night is survivable *inside the wreck, in the clothes
   you crashed in*, with no fire and no huddle. After that the cold takes it away.
6. **Wearability is derived, never whitelisted.** Anything flexible/fabric/soft/insulating and light
   enough to drape around a body wears: a blanket as a cloak, a freed seat cover, the engine cover,
   socks on hands. Refusals are physical ("it doesn't bend around a body"), never a list of what does
   work. *(Shipped, DR-25.)*
7. **Shelter is evaluated by properties, never by recipes, and partial shelters count.** A half-built
   windbreak reduces heat loss before it is anything you would call a shelter (GDD §31–§36). There is
   no build menu and no recipe list; see §4.4.
8. **Wet is a quantity, not a flag** — grams of water in a thing. It rises in snow and falls by a
   fire; wet insulation counts for a fraction that falls with wetness, to nothing for soaked down.
   *(Proposal; the shipped `wet_fraction` already implements the curve.)*
9. **Never a menu.** The game does not suggest huddling, does not list shelter types, does not say
   "you could block the breach". The breach is described as what it is — the wind's door — and the
   engine cover as what it is: thick, quilted, padded. The player joins them.

### 4.1a The first night, and what comes after (Andrew, 2026-09-18)

There is no guaranteed floor. There is a **first night that is survivable inside**, and a cold that
removes it.

**Night one.** It is not as cold yet, and **the cold does not kill on night one** (2026-09-28). A party
that stays in the wreck survives it in the clothes they crashed in — no fire, no huddle, nobody doing
anything clever. It will not be pleasant, and the townie in denim will feel it, but nobody dies of it:
what night one costs shows on the warmth and rest meters, by how well the party manages it. *This is the teaching night: the lesson it
teaches is that the wreck is shelter.*

**Going outside on night one** saps you — without fire, food and better gear the cold takes warmth
steadily. You can be out there for a while, and short trips are fine and expected. A whole night out
without a heat source costs dearly — deep into the warmth meter, a night with no real rest — though on
night one it still does not kill.

**Night two onward it gets colder** (document 13 §4.2), and the wreck alone stops being enough.
Now you need at least one of:

| answer | what it is |
|---|---|
| **a heat source** | a fire, and everything document 07 says about getting one; hot stones, a warm vessel |
| **better gear** | what the wreck gives up — the engine cover, the two blankets hidden in the plane, the sleeping bag buried with the tail wreckage, salvaged foam and batting, another person's spare coat, the clothes of a seat nobody plays |
| **conserving** | block the breach, get off the metal floor onto boughs, close the space you are heating, and gather anything that will serve as a blanket |
| **huddling** | shared body heat, and more of it under one covering — a real answer, not the only one |

**Most parties will have fire by then**, because most parties spend day one trying for it — which is
exactly the intent: night one buys them the day to earn it.

**The acceptance test:** *a party that stays in the wreck on night one survives without fire, in the
starting draws; a party that has done nothing more by night two is in trouble.* Document 13's numbers
are tuned until both halves are true.

### 4.2 The clothing system

Each wearable declares: `covers` (head · torso · arms · hands · legs · feet), `insulation` (from its
material), `wind` (0–1: a shell stops wind, a sweater does not), `waterproof` (0–1), mass in grams;
and inherits `wet` (grams of water) and damage state. *(Proposal, with document 16 §4.4; the fields
are shipped in `characters.py` and read by `warmth.py`.)*

What derives from that:

| derived | rule | source |
|---|---|---|
| **warmth by region** | the body loses heat per region by exposure × (1 − that region's coverage); a bare head is about a fifth of the loss, bare hands and feet drive frostbite | proposal; the shipped region shares are head .20 · torso .35 · arms .10 · hands .10 · legs .15 · feet .10 |
| **layering** | layers add, as long as each fits over what is under it — size and order are real (a parka over a sweater, not the reverse; the kid's jacket will not go on an adult); the outer shell's `wind` multiplies the whole stack | Andrew, 2026-09-18 and 2026-09-28: linear for now, wearing everything that fits; diminishing returns are measured once the cold clock bites |
| **wet** | wet insulation counts for a fraction that falls with wetness, to zero for soaked down; wool forgives, down does not | proposal; `warmth.py::wet_fraction` |
| **sweat** | hard work in a heavy stack puts water into the inner layer — the deferred cold debt; the player hears of it only through the clothing line and pays for it later | Andrew, 2026-09-18 |
| **dexterity** | bare hands in the cold lose fine work by the minute (knots, a match, the drill); thick mittens cannot do fine work at all — take them off and pay the warmth | proposal; `warmth.py::fine_work_ok` |
| **movement** | snow boots against sneakers changes wet-feet rate and speed; snowshoes pay only in deep snow, which this week never lays, and on a couple of inches over tussocks they slow you; dress shoes on ice or frost-glazed rock make a fall far likelier | proposal |
| **signal** | a bright jacket spread on the wing is something a search crew can see; a dark one is not | proposal; document 14 §3.4 |
| **sharing** | `give X to Y`, wearing something from another's hand, the blanket over two — the huddle is real physics: two bodies, one blanket, shared loss; two fit under a blanket, no more, and the rest huddle close or layer up; being close gives a small shared bonus, a shared covering the large one | Andrew, 2026-09-18 and 2026-09-28 |

**The score, as built (DR-25):** each worn item contributes `round(insulation × min(mass_g, 3000))`
"insulation-grams" — an intensive material property scaled by an extensive mass — summed, then
banded: *bare to the wind → thinly covered → adequately dressed → well bundled → swaddled*. The region
model (DR-25a, live in `warmth.py`) multiplies each item by its wet fraction and distributes it over
the regions it covers. Status words, never numbers: "your hands are numb", "your feet are soaked",
"you are sweating in the parka".

### 4.3 The draws (what the party starts with)

The starting clothing draw is Andrew's decision (2026-09-07); the specific slots are document 16's
proposals. Up to five play, and a seat nobody plays is a dead character whose clothes and pockets can
be searched (2026-09-27). The warmth-relevant shape: a guide in a down parka, wool base layer,
insulated boots, gloves and a wool hat; a townie in a denim jacket, cotton hoodie, jeans and sneakers
with **no gloves**; a nurse in fleece and hiking boots with thin gloves; a salesman in a wool overcoat
and **dress shoes**; a kid in a light insulated jacket, jeans and sneakers, his snow gear packed in a duffel out in the tail wreckage — and everyone boarded in a coat, some lost in the crash (2026-09-28). Giving away your gloves is a real act.

### 4.4 Shelter

The room censuses found the same missing system from opposite sides: in the rear cabin, covering the
hull breach is the most natural survival act there is; outside the nose, standing in the
open should cost more warmth than the cabin, with the wind unbroken and no walls. Shelter answers both.

**Outdoors, shelter is a property of a zone, not an object you own** (Andrew, 2026-09-18). Every zone
carries, as authored data *(Claude's, not yet decided: the bands, their names and which zone gets which)*:

- **wind exposure** — how much of the weather's wind reaches a body standing in it, in four bands
  over document 01's zones: `sheltered` (the big-spruce hollow, the tree well, the deadfall tangle,
  the grouse thicket, the spruce tunnel, the marten set, the cabin, the loft) · `broken` (most forest,
  brush and bank zones) · `open` (the muskeg flats, the lake shore, inlet and outlet, the pond flats,
  the krummholz, the bench saddle) · `brutal` (the boulder field, the knob, the lee slope, the
  fuselage top). The crash cluster: exteriors
  `open`, the fuselage top `brutal`.
- **a roof score** — how much sky is over you: bough cover, hull, a lean-to's thatch, a big
  spruce's skirt. A roof cuts radiant loss and stops falling snow wetting you.

**Inside the plane, shelter comes from the cabin's rooms** (Andrew, 2026-09-26, 2026-09-28). Each opening is
a part with an area and a state — open · partly blocked · blocked · closed · jammed · iced shut — and
the cabin is one air volume with one internal heat, which bodies and a fire raise and the skin and the
open openings lose (document 17 §4.8). The wind and roof a body feels inside are read off the
openings and the internal heat. The heat system's own document (`PLAN.md` A10) owns the numbers for
both.

**Both are mutable.** Blocking the breach changes the opening's state, and the cabin's wind and heat
follow; a windbreak in the open raises the fire's survival and the body's; a lean-to raises the roof
score of the patch of outdoors you built it on. This is what makes shelter a *verb* and not a
*building*.

**The seed's property block** (GDD §31–§36) is the fuller target once built shelters are objects in
their own right: `wind_blocking · insulation · waterproofing · structural_stability · fire_safety ·
capacity · smoke_ventilation`. Until then a built shelter is a thing that *writes* the zone's two
numbers plus capacity — so partial work counts automatically and nothing needs a recipe.

**The shelters Whiteout's own world already implies** (all proposals; each is a floor, not a set):

| shelter | what it is | where |
|---|---|---|
| **the fuselage, a windbreak with holes** | the crash's default shelter: walls, no heat, and openings the wind owns — the tear in the rear hull first. It is night one's physical half (§4.1a) | the rear cabin — the tear is the way outside, the wind's door, and the reason the room is colder (`rear_cabin.md` §2e) |
| **block the breach** | cover the tear with the engine cover, a wing panel, a suitcase wall, a sheet of acrylic — the generic `cover`/`block` over any opening. The first real shelter act, available in the first hour, needing nothing the party does not have | the rear cabin (`rear_cabin.md` §5.1) |
| **the lean-to** | Andrew's own example (2026-09-07): poles and thatch against the weather, outside, by choice. A few branches the crash snapped lie on the shear line; the rest are found or cut at the forest edge (2026-10-02) | `shear_line` (a few branches the crash snapped); `forest_edge` (bough beds, shelter thatch) |
| **a windbreak in the open** | boughs, logs, rocks and the wreck's panels stacked against the wind — for a signal fire, or a night caught out. The week lays only a couple of inches of snow (document 13 §4.2): too little to cut into blocks or pile into a wall, though scraped up and packed along a windbreak's foot it seals the gap at the ground | open ground: the muskeg, the lake shore, the bench saddle |
| **under a big spruce** | a natural bivvy: a big spruce's skirt of low branches down to the ground, a dry needle floor that stays bare while the open ground whitens, out of the wind and the open sky. A party caught out overnight survives there with boughs and body heat and nothing else | `tree_well_hollow` |
| **ground insulation** | boughs, foam, luggage, the seat cushions — the ground steals more heat than the air. A night on bare metal, frozen ground or snow is survivable but expensive, *(roughly the cost of a day's work — Claude's starting point)*, so gathering boughs before dark is the obviously right thing nobody tells you to do | `forest_edge`; the bedding score (document 06) |
| **the stove** | Holt's cabin: a contained, chimney-drafted fire that turns the coldest night into weather | `cabin_interior` |

**Graceful degradation.** Until a build operation exists, the zones are still authored with their
bands and the prose still says which places are cold; a party can still get out of the wind by
*going somewhere else*, which is itself the first shelter decision.

### 4.5 Drying and wetting

Wet is grams of water in a thing. By a fire it falls; in snow it rises; a damp book of matches dries by
heat, which is the fire bootstrap. The ways to get wet that the world already carries: snow driving in
through the breach; wet snow near freezing, which soaks what it lands on (document 13 §4.2); the
creek, which still runs — a slip at the riffle or a wade soaks boots and legs a long way from a fire;
and still water whose skim ice holds nothing, which is a plunge and the run-for-your-life clock. Sweat
is the one nobody expects — the deferred cold debt of working hard in a heavy stack.

### 4.6 The ways to stay warm

Every goal has several ways, with no set number. Warmth's:

| way | key resource it spends | where |
|---|---|---|
| **fire** | fuel + an ignition source | the treeline and the north wood for fuel; the ignition source's own room |
| **insulation salvage** | tools (to strip) + time | mid and rear cabin: foam, batting, the two hidden blankets, the engine cover, clothes; the sleeping bag, dug out of the tail wreckage |
| **shelter / windbreak** | sweat + tools | the rear cabin (block the breach); outside (boughs, logs, the wreck's panels) |
| **the wreck itself, night one** | nothing at all | inside the fuselage — enough for the first night only (§4.1a) |
| **huddling** | nothing but proximity; more under a shared covering | any enclosed zone — one answer among several, from night two |

The softlock guard: night one needs no object at all, and the fire ways never hang on a single
ignition source — so a party that loses one can still earn the heat source night two asks for.

### 4.7 The cold, day by day

The antagonist's schedule is document 13 §4.2: temperature, wind and snow by game day, the same every
run — bare, icy ground at the start, snow on and off through the week, the nights growing colder (the
partial cloud keeps them from the deepest drops), and a heavier flurry on day 6 that clears into the
coldest night of the run, coldest on the valley floor where the cold air pools. Wind chill multiplies
exposure. Nothing here refuses a player; every line is a number that hurts more each day.

### The `make shelter` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | shelter |
|---|---|
| `goal` | shelter · a lean-to · a windbreak |
| `vague` | "How are you going to make a shelter?" |
| `roles` | **cover**: boughs, a sheet, a seat frame, the hull · **support**: a rigid thing or the wreck itself · **site**: the zone |
| `realize` | the first act the means imply — `lean <cover> against <support>`, `cover <opening> with <cover>` — which writes the zone's wind and roof numbers (inside the plane, the opening's state); a shelter is never one command |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

### 4.8 You hear your shelter leaking (Andrew, 2026-09-18)

A shelter's quality is never a number on screen. **You learn it through your senses**, because the
holes in it are things, and things speak (document 06: ambience comes from what is present, carried
in each row's `sensed` cadence).

The wreck is full of them. The hull tear in the rear cabin, the torn-open tail section, a window
pane gone, the cargo door that will not seat, a seam the impact opened. Each one is an entity with a
wind sound that varies with the weather and with whether anything has been done about it:

| the opening's state | what you hear |
|---|---|
| open, wind rising | "The wind comes through the tear in long cold breaths." |
| open, gusting | "A gust drives snow through the tear and across the floor." |
| partly blocked | "The wind worries at the edge of the sheet over the tear." |
| blocked | nothing — and the quiet is the reward |

So the loop closes without a tutorial: you hear the cold getting in, you find the hole, you cover it,
and the room goes quiet. The same holds outdoors — a lean-to that does not meet the ground tells you
so on a gusty night. **Ambient lines are how shelter (§4.4) is read**, and `examine` on the opening
gives the detail.

### 4.9 `status` and the meters — what your body reports (Andrew, 2026-09-18, 2026-09-27)

There **is** a status screen. It is not a menu of anything: it is your own body answering when you
ask, in the same words the prose uses, never in numbers.

```
> status
You are shivering, and your feet are soaked through.
Two fingers on your left hand are white and hard — frostbitten.
Your left forearm is bandaged; the bleeding has stopped.
You are hungry. You have not slept.
```

It carries everything a person can sense about themselves: **injuries** (each named wound and its
state — frostbite, a break, a burn, what is bound and what is not), **cold**, **hunger**, **thirst**,
**tiredness**, **wetness**, and anything else the body has to say. Bands, not numbers (§4.1), and the
same band words the narration uses, so the screen never teaches a second vocabulary.

`status` is one of the commands that does **not** interrupt what you are doing (document 06) — asking
how you feel is free. It is a command, not part of the room block (document 03): the look tells you
about the world, `status` tells you about you.

**The meters** (Andrew, 2026-09-27). People are not cut off from their own senses — you know you are
hungry without stopping to ask yourself — so players see meters for what a person can sense about their
own body, all the time, without typing anything. There are seven — **hunger, thirst, warmth, rest,
pain, stamina** (how out of breath you are: running, fighting and hauling spend it, and a breather
gives it back) and **blood** (it drains as you bleed, and the world says so too — you feel faint,
light-headed, cold) — each a short bar with no digits, because that is how a person feels it: very
hungry, not 38 %. Each bar is full when all is well and empties as the body runs down; pain fills as
it hurts more. They sit in the prompt line under each
response, the way a MUD shows its bars:

```
Hunger [###--]  Thirst [####-]  Warmth [##---]  Rest [####-]  Pain [##---]  Stamina [#####]  Blood [####-]
```

A client such as Mudlet can draw the same line as gauges, and an agent sees the line a human sees. The
bars read the same body numbers the band words do, so the meters and the words never disagree. A wound
is never a meter: it is named, in `status` and in `examine me` (document 11 §4.1).

## 5. Interactions

**This depends on:**
- **06 Time, sleep and the clock** — warmth is an unattended process on the heartbeat; sleeping cold
  costs warmth by the hour, by what a person lies on and under; a fast forward is where a cold night actually
  gets spent, and "you wake shivering" is one of the interrupts that drops the clock back to 15×.
- **07 Fire and shaping** — fire is one way to stay warm and the only drying source that works fast;
  its heat reaches bodies through the heat state of its area.
- **13 Events, escalation and weather** — supplies temperature, wind and snow (§4.2); a wind
  shift ("the breach faces it now") and ice sealing the cargo door are shelter events.
- **16 Players and kit** — the clothing draw, the luggage, the 206's interior; the engine cover, the
  two hidden blankets, the sleeping bag buried with the tail wreckage; the clothes of a seat nobody
  plays.
- **17 Rooms and living rooms** — zones carry the exposure band and the roof score; the plane is an
  entity with openings and one internal heat (§4.8); blocking a breach is state the room must remember
  and describe.
- **18 Materials and forms** — insulation, wind resistance and soak behaviour come from materials.
- **The heat system** (`PLAN.md` A10) — heat on every entity and body part, and its flow between the
  fire, the air, the plane and the body.

**These depend on it:**
- **09 Water** — eating snow costs heat; melting by body heat costs warmth.
- **10 Food and hunger** — calorie deficit is a warmth input; being cold burns calories, and
  shivering runs on the body's glycogen.
- **11 Injury and first aid** — frostbite is a warmth failure with a location; hypothermia's
  confusion is a warmth band, on the same thresholds (§4.1); a bleeding wound costs warmth.
- **14 Rescue paths** — a bright jacket on the wing is something a crew can see; the walk to the
  cabin costs warmth.
- **15 Moral and social layer** — who gets the good coat and the blanket, and whether you strip a
  body. Sharing warmth is the first co-op act, hours before the antenna.
- **19 Multiplayer** — the huddle is only meaningful with other bodies in the zone.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-16** — first draft, gathering the scattered warmth, clothing and shelter material.
- **2026-09-18 (Andrew)** — the `make shelter` goal rows; the night-one rule in place of a guaranteed
  floor; shelter as two mutable numbers on the zone; linear layering for now; the huddle's two sizes;
  the extremities' own cold; a generic `cover`/`block`; sweat; sleeping without shelter survivable but
  expensive; heated stones and a warm vessel; a `status` screen; the openings heard. Reviewed in full.
- **2026-09-26 (Andrew)** — heat as a state on every entity and body part; the plane as an entity with
  openings and an internal heat, which is how shelter works inside it. Claude proposed hypothermia
  bands that follow the clinical staging, for Andrew's check.
- **2026-09-27 (Andrew, at document 11's sitting)** — meters for what the body feels, beside the
  `status` screen: seven bars with no numbers, in the prompt line, blood among them (§4.9).
- **2026-09-27** — the first week of October carried in (the cold, day by day, is document 13 §4.2);
  what is aboard (the two hidden blankets, the sleeping bag with the tail wreckage); the unplayed seat;
  what kills.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

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
- The cold clock itself: core temperature, the extremities, the per-tick equation, the bands, the
  night-one rule (the roadmap's step 3). `systems/clock.py` says so in as many words: its exposure
  tick "emits nothing consequential".
- Heat as a state on every entity and body part, and the plane's openings and internal heat
  (document 17 §4.8) — there is no heat system yet.
- Sweat, dexterity decay, movement effects and the signal value of a bright jacket — the fields
  exist, nothing reads them.
- Wetness as a quantity written by the world (snow, the creek, a plunge). `wet` exists only as a
  boolean today: authored on the soaked matchbox and written by `pour`. `warmth.py::wet_fraction`
  already reads grams and treats a bare `wet: True` as half-soaked, so the curve is waiting for the
  world to start writing numbers.
- The cold and the snow by day (document 13 §4.2; `systems/weather.py` is a docstring).
- The per-zone exposure bands for the outdoor zones (document 01) — design data, not yet in
  `zones.py`, which carries only `terrain_tags` (one crash zone is tagged `exposed`).

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
