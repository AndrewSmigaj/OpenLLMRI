# 01 — The premise and the world

## 1. Status

> **Status: the premise and Andrew's decisions reviewed 2026-09-17; the map (§3, §4.2–§4.12) redesigned
> by Claude 2026-10-02, for Andrew's review.** **Architecture counterpart:** none — this document is *what the world is*; how zones, edges
> and Scenes are represented lives in
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md)
> (DR-13a) and [`../architecture/perception-model.md`](../architecture/perception-model.md). The built
> zones are `game/world/scenarios/winter_survival/zones.py`.

This is the document you read to picture the whole world before anything else: what happened, when
and where it happened, what country the party is standing in, how big it is, what it costs to cross,
and every room in it. The valley's shape, its regions, its routes and its places
were redesigned by Claude on 2026-10-02 — **they are Claude's proposals**, for Andrew's review.

---

## 2. Decisions

### Andrew's decisions

- **The premise (June 2026, GDD §6).** A crash off the filed route, so the search starts in the wrong
  place: nobody is looking where you are yet. The wreck is unstable.
- **The pitch (June 2026; reworded with Andrew 2026-09-17 and 2026-09-27).** Survivors of a bush-plane
  crash improvise with a physically modelled world to stay alive against cold, injury, hunger and a
  season closing in, until they are rescued. The only endings are rescued or dead.
- **The data budget (June 2026, GDD §6).** One authored crash; the crash site and its near forest are
  the densest place in the valley, modelled to the hilt.
- **The bar for rooms (2026-09-07).** Rooms are living and interesting, never half-thought. The things
  in them serve the rescue goals (and not only them — 2026-09-28) — fixing and using the radio, then surviving until help arrives, which
  means finding food and warmth — and there are several ways of doing things: a lighter can be found by
  looking hard enough, and fire can be lit in other ways too. Things take the time they take, and, as in
  a MUD, the player sees messages while an attempt is under way.
- **The aircraft (2026-09-07, 2026-09-16, 2026-09-27).** A Cessna 206-class single with the honest
  four-seat interior: seats 1A, 1B, 2A, 2B and the right seat, a hat shelf, a cargo net and a jammed
  cargo door. The plane itself is fine. The plane's battery is in the
  nose, wired and fine.
- **The run (2026-09-07, 2026-09-17).** Roughly a week of game time in one sitting of two or three
  hours, which the players can pause and return to. An escalation ladder and no hard time barriers;
  there is no set arc.
- **The whole valley (2026-09-16, 2026-09-17).** Every region and its places are in the first complete
  run, and each region gets a reason to come back; the counts are floors. The size is judged by the travel
  table (§4.6), now that travel is an attended activity. If a region is ever cut, it is the muskeg.
- **The season (2026-09-26, 2026-09-27).** The first week of October in interior Alaska — Claude's
  choice, at Andrew's request, for more than ten hours of daylight. **No big storm** (2026-09-27): bare,
  icy ground at the start, berries and roots findable, skim ice on still water; snow on and off through
  the week, building to a couple of inches by the end, so a fire can be kept going outside and the world
  stays open; a heavier flurry on day 6 that clears for day 7. The sky is always at least partly cloudy:
  planes fly most days, but the wreck is hard to see from the air. The escalation comes from the cold
  and the land. The same weather every run. The numbers are document 13 §4.2's.
- **The party (2026-09-16, 2026-09-27).** Up to five play: four adults and the kid. A seat nobody plays
  is a dead character whose clothes and pockets can be searched; AI agents may play seats. No back
  stories — the characters differ in clothes, injuries and what they carry, and in how well and how fast
  they do things (document 16).
- **The pilot (2026-09-17, 2026-09-27).** He starts the run dead; the party does not need him to work out the rescue,
  and what he carries is what a real pilot would, and clues are what a realistic world holds, plus some added to help players, no set number (2026-09-27). His body is food,
  and eating it is taboo, not immoral (document 12).
- **What is aboard (2026-09-27).** There is no survival kit. The sleeping
  bag is buried with the tail wreckage; two blankets are hidden inside the plane; there is no firearm.
  Not too easy, not too hard.
- **Rescue (2026-09-17, 2026-09-27).** Three ways home — the radio, a signal a plane can see, surviving
  long enough — exactly as document 14 §3. **The ELT is broken.** Two radios: the plane's radio, on the plane's battery, with a
  loose wire; and a hand radio in Holt's cabin whose batteries are buried
  in a bag in the tail section.
- **Holt's cabin (2026-09-17, 2026-09-27).** The cabin is supplies — some trapline gear and modest
  stores, not piles of food. Walking out is not an ending, and no zone leads out of the valley.
- **The animals (2026-09-17, 2026-09-26, 2026-09-27).** The bear, some of the bigger animals and a few
  birds act — on the engine's behaviour rules, or played by a lightweight model, only a few at once; as
  many of an animal in a room as is realistic, and birds not constantly calling. The fish are scripted.
  Other wildlife shows as events and sign. No wolves, no wolverine, no moose (2026-10-01). What lives here is
  what realistically lives in an area of this size; food sources are not added just because they are
  possible (2026-09-18; document 23).
- **Moving through the valley (2026-09-17).** Moving between areas is an attended activity with
  feedback and events: `walk`, `run` (less time, more sweat), `turn back`. Some stretches take longer to
  cross; weather lengthens every trip, so exploring early is rewarded a little. There is no escape by
  walking out.
- **What the party does outside (2026-09-07).** The party probably won't stay outside much, but it can
  make a fire and a lean-to if it wants.
- **Dangerous places (2026-09-17, 2026-10-02).** They injure, never kill outright; fitness matters; the
  outcome mixes chance with the character's stats, and it is never shown as a dice roll — the player
  reads what happened (*"your boot skids on the glazed rock and you go down hard"*); the tutorials
  explain that success is chance influenced by stats.
- **Sweat (2026-09-17).** Sweat is wet clothing draining warmth, inside the warmth system (document 08).
- **Density (2026-09-17).** The density gradient (§4.11) is authoring order — a priority, never a cap.
- **(2026-10-02)** Holt's cabin is secured the way a trapper leaves it in bear country, so it takes
  work: unlocked, but with bear boards over the windows and across the doorstep; the stovepipe capped;
  kindling laid and a few matches in a tin, found by searching the shelf (wood is still needed to keep
  the fire going); a bunk with wool bedding; the raised cache with its ladder stashed under the cabin,
  holding the axe and the stores; a modest woodshed stack and a freight sled. Not every place needs something interesting — ontologically
  sufficient is not fluff for its own sake.
- **(2026-10-02)** The wreck: the sleeping bag is buried with the tail (no avgas); no snowshoes in the
  tail; the plane is not falling apart — scripted events stay only where they are useful or add
  ambience; a few snapped branches on the shear line, the rest found or cut; the nurse's backpack wedged
  behind the rear seats under the crushed hat shelf.
- **(2026-10-02)** Each region's roles are listed in the map data. Things cost what they really cost —
  there is no required number of costs.
- **(2026-09-27)** Holt, the trapper, does not come back during the week; the cabin is supplies, not a place to be
  rescued from. His traces say so (document 14, 2026-09-28) — his trapline gear gone from its pegs, and a
  calendar on the cabin wall with a date circled weeks after the week.

### Proposals (Claude)

- **The whole map** (§3, §4.2–§4.12), redesigned by Claude on 2026-10-02 at Andrew's request — the
  regions and their roles, the places, the distances and travel times, where the ways home happen, the
  week on the map, the density order, and what the valley already holds. For Andrew's review; it rests
  on his decisions above, named where they apply.

Every count here is a floor: no region or place is ever "finished".

---

## 3. In one paragraph

A mail plane crossing a low ridge in the first week of October clips the spruce, sheds a wing and its
tail, and slides out onto the floor of a side valley at the east edge of a muskeg white with hoarfrost.
The pilot is dead in his seat. The beacon is broken; the plane's radio has power but will not work, and
the hand radio at a trapper's cabin down the valley has no batteries — they are in the wreckage of the
tail; the search is starting where the flight plan said the plane would be, not
where it is. Step out of the hull and the valley is all around: west across the bog, a lake, open water
under the widest sky in the valley, and an old burn on its far shore; north, spruce at the ridge's foot,
with the fuel, the hares and the shelter; north-east, the plane's own scar climbing past its wing to a
rocky knob that sees the whole valley — the highest place to raise an antenna; east, birch and aspen on
the ridge's warm toe; and south, the creek out of the lake, running past a fishing pool, the slopes and
gravel bench where a grizzly is feeding hard before winter, and a beaver pond, to a blazed trail and a
trapper's cabin two and a half kilometres away. Things lie where they really would. Snow comes on and
off all week and the nights grow colder, until a heavier flurry on day 6 clears into the coldest night
of the run, and on day 7 the rescuers come.

---

## 4. The design

### 4.1 The crash (the premise, made specific)

A 206-class piston single — the Alaska mail-and-freight workhorse, on big tundra tyres in October
(document 16 §4.5) — came in from the northeast over a low ridge shoulder, clipped the spruce crowns,
shed its right wing into the trees, bellied down the slope and slid southwest across the muskeg fringe,
shedding the tail, to stop at the muskeg's east edge. The pilot was stretching for the flat of the
muskeg and almost made it. He died in the crash: the run starts with his body in the left seat, and he
carries what a real pilot would (document 12).

What is aboard is the design's call, and it is set so the run is neither too easy nor too hard:

- **There is no survival kit.**
- **The sleeping bag** is buried with the tail wreckage; **two blankets** are hidden inside the plane;
  there is **no firearm** (document 16).
- **The plane's radio** has power from the plane's battery but a loose wire; **the hand radio in Holt's
  cabin** has no batteries — they are **buried in a bag in the tail section**, which each
  flurry hides a little more (document 14 §3.2).
- **The ELT is broken.**
- **The plane's battery** is in the nose, wired and fine.
- **The freight and the mail** — flour, coffee, a small bag of dog food, a toolbox, the mail sack with a parcel for
  V. Holt — are scattered through the wreck and along the scar (documents 10 and 16).

Realism supplies the inventory; the crash supplies the difficulty: the tail tore off two hundred
metres back up the scar, the hatchet's haft snapped, the nurse's matches damp, the sleeping bag buried with the tail.
Where each thing lies is decided case by case, by what makes the game better (2026-09-28): what would make the start too easy — the tools and supplies that solve the big problems — is not lying in plain sight in the first room, and no rule hides things away; everything else lies where it would really lie — a dead fish on the shore.

Conditions: the first week of October; daylight, temperature, snow and ice day by day are document 13
§4.2. The search starts in the wrong place, and search and rescue is searching (document 14 §3.5).

### 4.2 The valley

*(The whole map, §4.2–§4.12, was redesigned by Claude on 2026-10-02 at Andrew's request — he had not
reviewed the July version. Everything here is Claude's, not yet decided, until he reviews it; what it
rests on is his decisions, named where they apply.)*

An unnamed side valley in interior Alaska, about six square kilometres, running north-west to
south-east. Its two sides are the two faces of every interior valley: the **north side** is a ridge
whose south-facing slope gets the sun — dry ground, white spruce, and birch and aspen on its warm
toe; the **south side** is a lower slope facing north — black spruce, deep moss, and permafrost under
it. Between them the floor is muskeg, a lake and the creek that drains it.

The plane came in from the north-east over the ridge, clipped the spruce, shed its right wing into
the trees, bellied down the slope and slid out onto the valley floor at the east edge of the muskeg,
leaving its tail two hundred metres back up the scar (§4.1). So the wreck sits where the ridge meets
the floor, and almost everything in the valley is a direction from it:

- **up the scar, north-east** — the wing, the torn-off wheel, and the climb to the ridge and its rocky
  knob, the highest place for the radio's antenna and the one place that sees the whole valley;
- **north** — the spruce wood at the ridge's foot: fuel, hares, grouse, shelter;
- **east** — the birch and aspen on the ridge's warm toe: bark, punk, chaga, the friction woods;
- **west** — the muskeg, and beyond it the lake, the valley's widest open sky; across the lake, an old
  burn full of standing dead wood;
- **south** — the creek out of the lake's south end, running south-east down the valley: open water
  all week, fish in its pool, the bear's berry slopes and root bench along it, a beaver pond, and from
  the pond Holt's blazed trail up onto a bench to his homestead.

```
                                     N
                     the lee slope ╮  ▲
                 THE RIDGE · the knob (granite tor, +120 m) · the boulder field
                       │ the ridge top (wind-stunted spruce, lichen)
                       │ the bench saddle
     THE NORTH WOOD    │ THE SCAR — the gear gouge · the wing in the trees · the shear line
     forest edge ·     │      ╲
     big spruce ·      │       the tail section (200 m up the scar)
     hare runs ·       │      ╱
     grouse · deadfall │    ╱                         THE BIRCH SLOPE · 350 m E
                       ✈ THE CRASH SITE ─────────────  aspen · birch grove · the old birch · game trail
 THE BURN ── THE LAKE ── THE MUSKEG ◄─┘
 (far shore,  shore · marsh edge ·   tussocks · Labrador tea ·
  1.5 km W)   inlet · outlet         tamarack · wet channel · willows
                         │
                         ▼ S — the outlet, heard before it is seen
              THE CREEK · riffle · willow bars · the bend · the logjam · the pool
                         │
              THE BEAR'S COUNTRY · the berry slope · the root bench · torn ground
                         │
              THE BEAVER POND · the dam · the pond · the food pile · the old drowned set
                         ╲ the blazes climb SE
                          HOLT'S TRAIL · blazes · spruce tunnel · marten set · the gate
                           ╲
                            HOLT'S HOMESTEAD · dooryard · porch · the cabin · loft · cache · woodshed · water hole
```

Zone positions are authored per zone in metres from the wreck, y+ = north, matching `zones.py`'s
convention. Straight-line distances from the wreck: the north wood 60–300 m N · the birch slope 350 m E ·
the ridge's knob 800 m NE (+120 m) · the lake shore 500 m W · the burn 1.5 km W across the lake (about
2.5 km round its shore) · the creek's riffle 800 m SW · the pool 1.1 km S · the bear's country
1.2–1.5 km S · the beaver pond 1.7 km S–SE · the homestead 2.4 km of travel SE.

**What it rests on** (Andrew): the whole valley in the first complete run, each region with a reason
to come back (2026-09-16, 2026-09-17); the lake about 1.5 km long and 6–8 m deep, joined to the creek
(2026-10-02); Holt's cabin as supplies, 2.4 km off (2026-09-17, 2026-09-27); the bear's sign in its own
area, plain on entering it (2026-09-28); what lives here is what realistically lives in an area this
size (2026-09-18); each region's roles listed in the map data (2026-10-02); if a region is ever cut, it
is the muskeg (2026-09-17).

### 4.3 How the map is built

**Each region has roles**, and they are listed in the map data (2026-10-02): what a party comes to it
for — the ways home (document 14 §3) and the survival every way spends from. The roles are §4.4's
second column. A region is a Scene (document 19 §4.3): a connected group of places, sight working
within it and, across open land, case by case.

**The week gets harder** (the escalation, PLAN §5): the nights grow colder, each flurry covers more of
the low forage, the near deadfall burns away so every armful is a longer walk, the still water skins
over too thin to trust, and on day 6 a heavier flurry closes the world in for a day (document 13 §4.2).

**Things cost what they really cost** (2026-10-02) — the kinds of cost, with no number of them
required (a rock on the creek bar costs a short walk):

| Cost | What spends it |
|---|---|
| **Daylight** | travel and work both burn the day's light (document 13 §4.2) |
| **Warmth** | the open places drain you while you work — the lake shore and the ridge most (document 08) |
| **Sweat** | hard effort dampens clothing, which chills once the work stops (document 08) |
| **Tools** | a blade, a hatchet or axe, a saw, a container, cordage — each makes different work possible |
| **Knowledge** | reading tracks, ice, blazes, which wood is dry — `examine` shows what is there; reading it is the player's |
| **Risk** | thin ice, the cold creek, the glazed lee slope, the bear's country |

**Where things lie** is decided case by case (2026-09-28): what would make the start too easy is not in
plain sight in the first room; everything else lies where it really would. Not every place has
something interesting in it — a stretch of muskeg is a stretch of muskeg (2026-10-02).

### 4.4 The regions

| Region | Its roles | Places | From the wreck |
|---|---|---|---|
| **The crash site** | shelter, the kit in the bags, the plane's radio, and in the tail the batteries for Holt's hand radio; where a party stays, signals and keeps itself findable for the early passes | 9 ✅ | — |
| **The scar** | salvage from the wreck (the wing's fuel, the wheel and tyre, wire, aluminium); the way up to the ridge; an arrow pointing back up the hill | 4 | 100–450 m NE |
| **The ridge** | height for the radio's antenna; the view over the whole valley (the lake, the creek, Holt's clearing); a named landmark (the knob, on the chart); signals seen from far off; exposure and the glazed lee slope | 4 | 650–900 m NE, +100–120 m |
| **The north wood** | fuel, boughs, shelter; spruce grouse, hares, red squirrel middens, porcupine | 5 | 60–300 m N |
| **The muskeg** | the way to the lake (slow, wet going); berries, Labrador tea, sphagnum moss, cottongrass, tamarack | 5 | 120–450 m W |
| **The lake** | the widest open sky — signals and the sound of the planes; water; fishing from the shore; the marsh edge's cattails, and its water hemlock; swans resting on their way south | 4 | 500 m W and along the shore |
| **The burn** | standing dead spruce, the biggest fuel supply, far off; open ground a plane can see; berries and hares in the regrowth | 3 | 1.5 km W across the lake |
| **The birch slope** | fire: birch bark, punk wood, chaga; the friction woods (aspen); rose hips and highbush cranberries; ruffed grouse | 4 | 350 m E |
| **The creek** | running water all week; fish in the pool; willow; ptarmigan; the way south | 5 | 0.8–1.1 km SW–S |
| **The bear's country** | the richest berry slope and root bench in the valley — and the grizzly's home ground, its sign plain on entering | 3 | 1.2–1.5 km S |
| **The beaver pond** | Holt's old trap set and its wire; the beavers and their food pile; poles; where Holt's blazed trail starts | 4 | 1.7 km S–SE |
| **Holt's trail** | the way to the cabin, sheltered in any weather; Holt's traces (an empty marten set) | 4 | 1.7–2.4 km SE |
| **Holt's homestead** | supplies — the stove, a bunk, modest stores, the axe, the woodshed; a hand radio without its batteries; chimney smoke a plane can see | 7 | 2.4 km SE |

### 4.5 The places

✅ = built in `zones.py` today · 📐 = designed here, not built. Each row is what is really there; the
loops grow every one (document 22), and every count is a floor.

**The crash site** *(built; to be re-authored to the current decisions — §8)*

| Place | What is there | Status |
|---|---|---|
| `cockpit` | the panel and the panel compass, the pilot's body in the left seat, the chart and the flight manual, the hand flare in the door pocket; the wire behind the panel | ✅ |
| `mid_cabin` | the four seats and what is under them, the luggage | ✅ |
| `rear_cabin` | the torn hull, frost on the metal, the hat shelf and the bags behind the rear seats, the quilted engine cover, the cargo net and the jammed cargo door | ✅ |
| `outside_nose` | the nose in the frozen moss; the plane's battery, wired and fine; the cowling | ✅ |
| `fuselage_top` | the torn antenna base, the widest view from the wreck, a high place to raise an antenna, the wind | ✅ |
| `outside_tail` | the breach — the way between the hull, the scar and the treeline | ✅ |
| `debris_trail` | what the crash shed: the mail sack, the freight, the cooler in the brush, the hatchet with its cracked haft | ✅ |
| `tail_section` | the tail wreckage, two hundred metres up the scar: the broken ELT, the kid's duffel with the sleeping bag buried in it, the bag holding the batteries for Holt's hand radio, the toolbox in the crushed tail cone | ✅ |
| `treeline` | deadfall, boughs, dry grass under the spruce; the way into the north wood | ✅ |

**The scar**

| Place | What is there | Status |
|---|---|---|
| `shear_line` | where the plane came through the spruce: snapped trunks and crowns, some branches the crash broke off | 📐 |
| `wing_in_the_trees` | the right wing hung in the spruce, avgas still in its tank, aluminium, control cables and wire | 📐 |
| `gear_gouge` | the furrow where the landing gear dug in, and the torn-off wheel and tundra tyre (rubber burns with thick black smoke) | 📐 |
| `bench_saddle` | a saddle halfway up the climb, out of the worst wind | 📐 |

**The ridge**

| Place | What is there | Status |
|---|---|---|
| `ridge_top` | open ground: wind-stunted spruce and dwarf birch, lichen, bearberry; dry small fuel in a windy place | 📐 |
| `boulder_field` | talus that shifts underfoot, rock tripe on the boulders | 📐 |
| `the_knob` | a granite tor, the valley's highest point: the view over the whole valley, a survey marker set in the rock and named on the chart, the highest place for the antenna, the worst wind | 📐 |
| `lee_slope` | the steep north side of the knob: frost-glazed rock, worse once new snow hides the glaze; a fall injures and never kills outright | 📐 |

**The north wood**

| Place | What is there | Status |
|---|---|---|
| `forest_edge` | green boughs, the wood's first tracks | 📐 |
| `big_spruce_hollow` | big white spruce: dead twigs dry under them in any weather, a bare needle floor out of the wind, a red squirrel's midden | 📐 |
| `deadfall_tangle` | a tangle of deadfall, much of it needing a tool, under a dead tree leaning over it | 📐 |
| `grouse_thicket` | young spruce where spruce grouse sit, tame enough to approach | 📐 |
| `hare_runs` | willow and alder brush threaded with hare runs, the fresh ones plain in the new snow | 📐 |

**The muskeg**

| Place | What is there | Status |
|---|---|---|
| `tussock_flat` | tussocks with lowbush and bog cranberries, cottongrass, sphagnum in the hollows; hurrying can turn an ankle | 📐 |
| `labrador_thicket` | Labrador tea, its leaves leathery all winter | 📐 |
| `tamarack_island` | a rise of tamarack and black spruce, the tamaracks' needles gold and falling; dry dead limbs | 📐 |
| `wet_channel` | a wet channel under skim ice, its edges hidden by the thin new snow as the week goes on; water, sedge, mud; a probe finds the firm line | 📐 |
| `lake_gate_willows` | willow where the muskeg meets the lake, the first hare runs | 📐 |

**The lake** — about 1.5 km long and 6–8 m at its deepest, deep enough for fish to winter in it;
fed by its inlet and drained south by the creek at the outlet (2026-10-02). Open water all week; its
surface is water, seen and fished from the shore — walking out on any ice breaks it (2026-09-27).

| Place | What is there | Status |
|---|---|---|
| `shore_apron` | a gravel shore with a drift log on it (a big supply of fuel for a saw), open water at the edge under a skin of ice at dawn, the widest open sky in the valley | 📐 |
| `marsh_edge` | the lake's shallow south-east bay: a stand of cattails, water hemlock among them, a muskrat's house of cattail and sedge; the mud never frozen | 📐 |
| `inlet_mouth` | the north end: running water at the inflow, skim ice and new ice forming at its sides | 📐 |
| `outlet_narrows` | the south end: running water heard before it is seen, its border ice thin over the current; the way to the creek | 📐 |

**The burn** — the far shore, burned some fifteen years ago; reached the long way round the lake.

| Place | What is there | Status |
|---|---|---|
| `burn_edge` | where the green forest stops: fireweed stalks, young aspen and birch | 📐 |
| `snag_stand` | standing dead spruce, silver and dry — the most fuel in the valley, and a long way from the wreck | 📐 |
| `burn_regrowth` | open regrowth with blueberries (dried on the bush), hare runs and their sign; open ground a plane can see | 📐 |

**The birch slope**

| Place | What is there | Status |
|---|---|---|
| `aspen_fringe` | aspen poles, dead and standing, punk wood that carries an ember; ruffed grouse | 📐 |
| `birch_grove` | birch bark, which burns even damp; birch polypore and tinder conk | 📐 |
| `chaga_tree` | an old birch with chaga ten feet up — it catches a spark and holds an ember | 📐 |
| `game_trail_crossing` | an old shed antler; rose hips and highbush cranberries along the trail | 📐 |

**The creek**

| Place | What is there | Status |
|---|---|---|
| `outlet_riffle` | running water — a full container without melting snow, at the risk of wet boots | 📐 |
| `gravel_bar_willows` | willow in quantity, rose hips, highbush cranberries; ptarmigan turning white | 📐 |
| `overflow_bend` | the creek running fast under thin shelf ice that the first snow hides; a probe finds the edge | 📐 |
| `logjam_crossing` | a dry crossing and a lot of wood, over real voids between the logs | 📐 |
| `confluence_pool` | a deep pool where a side stream joins: grayling and burbot, open all week | 📐 |

**The bear's country** — the grizzly's home ground this week (document 23 §4.1a): its sign lies here
and is plain on entering (2026-09-28). The bear itself can be anywhere food is (document 23).

| Place | What is there | Status |
|---|---|---|
| `berry_slope` | an open south-facing slope above the creek: the valley's best lowbush cranberries and crowberries, bearberry — and berry-filled scat, flattened patches where the bear fed | 📐 |
| `root_bench` | a gravel bench along the creek with wild potato in it — dug up in swathes, the bear's diggings fresh | 📐 |
| `torn_ground` | a rotten log ripped open for grubs, a torn-up stump, tracks in the mud at the water's edge | 📐 |

**The beaver pond**

| Place | What is there | Status |
|---|---|---|
| `dam_crossing` | the dam, a causeway to the trapline side; poles in its face | 📐 |
| `pond_flat` | the pond skinning over at night, bubble trails under the new ice showing where the beavers swim; the lodge | 📐 |
| `food_cache_margin` | the beavers' winter food pile, being built now: green poles that can be taken without touching the dam | 📐 |
| `drowned_set` | Holt's old beaver set, its wire on a pole — yards of snare wire; the first sign of a person beyond the wreck | 📐 |

**Holt's trail**

| Place | What is there | Status |
|---|---|---|
| `blaze_gateway` | the first blazes from the pond, each in sight of the last | 📐 |
| `spruce_tunnel` | the trail under close spruce, sheltered for its whole length | 📐 |
| `marten_set_tree` | Holt's old marten set, empty — the trapping season has not opened | 📐 |
| `cabin_gate` | the gate to Holt's yard | 📐 |

**Holt's homestead** — secured the way a trapper leaves a cabin in bear country (2026-10-02).

| Place | What is there | Status |
|---|---|---|
| `dooryard` | the yard and the dog-run cable | 📐 |
| `porch` | the door, unlocked as trapline cabins are; bear boards — plywood studded with nails, points out — across the doorstep and over the windows, to be pried off with a tool or slow care | 📐 |
| `cabin_interior` | the stove with kindling laid, its pipe capped against squirrels and birds (light it unnoticed and the cabin fills with smoke); Holt's shelf of modest stores, a bulged can among the tins; a hand radio without its batteries (they are in the plane's tail); a tin with a few matches on the shelf, found by searching; wood is needed to keep the fire going | 📐 |
| `loft` | a bunk with wool bedding | 📐 |
| `cache` | a raised cache, its ladder stashed under the cabin as trappers do against bears: trapline gear (snowshoes, the felling axe) and modest stores | 📐 |
| `woodshed` | a modest stack of split dry wood — a few nights', since Holt is still cutting his winter's in early October — and a freight sled with a split runner | 📐 |
| `water_hole_path` | the path down to the creek where Holt draws his water | 📐 |

### 4.6 Travel takes time

All week the going is the ground's own — tussocks, bog, deadfall, ground frozen hard at dawn — because
the snow never gets deep: a couple of inches by the end (document 13 §4.2). What the snow does is hide
the footing: frost-glazed rock and roots on the first mornings, then the holes between the tussocks and
the thin ice on the channels once it lies over them. Your own trail is faster than the first time — the
firm line through the bog found, the brush broken — and after a flurry it is plain to follow back.
Snowshoes, in Holt's cache, are for deep snow the week never lays.

| Leg (one way) | First time | Known trail |
|---|---|---|
| wreck → north wood (big spruce) | 15 min | 8 min |
| wreck → birch slope | 15 min | 10 min |
| wreck → tail section (up the scar) | 10 min | 6 min |
| wreck → the knob | 55 min | 40 min |
| wreck → lake shore | 25 min | 15 min |
| wreck → the burn (round the lake) | ~100 min | ~75 min |
| wreck → creek riffle | 30 min | 18 min |
| wreck → the pool | 40 min | 25 min |
| wreck → bear's country | 45 min | 30 min |
| wreck → beaver pond | 55 min | 35 min |
| wreck → homestead | ~90 min | ~60 min |

**The journey itself** (Andrew, 2026-09-28; document 19 §4.3). Going to another region is a journey: you
head off in its direction and the world gives an estimate (*"You head off toward the birch slope; you
reckon it will take about fifteen minutes."*). The walk is an attended activity with its own lines, and
on a long one you may pass things along the way. You can stop, and then you are between Scenes —
*"You are between the birch slope and the plane"* — with whatever is near you. Moving between places
inside a region takes time too.

The minutes are starting points for the week-long run on the October ground, tuned in play (`PLAN.md`
A4); moving is an attended activity whose time is distance over pace, times terrain, snow, load and
fitness (document 03 §4.1a). The first round trip to the homestead is about three hours of walking
before any work there, and the light shortens each day.

### 4.7 The three ways home, on the map

The ways home are document 14 §3's; this is where they happen.

| Way home | Where | What it needs |
|---|---|---|
| **The radio** — two (document 14 §3.2) | **the plane's radio** in the cockpit, on the plane's battery: something to open it (anything that turns a screw), the loose wire, an antenna mended and raised — the fuselage top, or higher; **Holt's hand radio**, in his cabin, without batteries — they are in a bag in `tail_section` | height; landmarks to tell the voice where you are — the lake, the knob and its survey marker, the burn, the creek, Holt's cabin on the chart |
| **A signal a plane can see** | the open places — the lake shore, the ridge and the knob, the muskeg, the burn's open ground; smoke from the wreck's clearing; the tarp laid out; Holt's chimney | fire and fuel ready when the engines are heard; something that stands out from the air |
| **Surviving long enough** | everywhere — on day 7 the rescuers find everyone still alive (2026-09-29); before then, being found by an early pass takes work, since partial cloud and the trees hide the wreck | staying alive |

**Holt's homestead is not a way home** (2026-09-17). It is supplies, and its chimney smoke is a sign a
search plane can see (document 14 §3.5).

### 4.8 What each kind of thing comes from

- **Fuel** — dead spruce twigs under the big spruce (dry in any weather) → dwarf birch and stunted
  spruce twigs, Labrador tea stems, by the armload → deadfall and the logjam (bulk, needing tools) →
  standing dead: the burn's snags, Holt's woodshed, the drift log (big supplies, far off or needing
  tools). The near deadfall is burnt first, so every armful is a longer walk; the day-6 snow covers the
  small deadfall. What is dry this week, and which woods serve friction fire, is document 23 §4.2a.
- **Water** — the creek's riffle and the lake's edge, open all week; Holt's water hole; snow and ice
  melted by a fire anywhere. Eating snow costs body heat (document 09).
- **Food** — what is aboard (the pockets, the bags, the freight) → berries, rose hips, roots (the best
  of them in the bear's country) → grouse and ptarmigan → snare lines on the hare runs, in the north
  wood and the burn → the pool's fish → a porcupine, a beaver → Holt's modest stores → the bear, through
  the combat system — and the pilot's body, which is food and taboo (document 12). The numbers are
  document 23 §4.4 and document 10 §4.8.
- **Warmth and clothing** — what people wore → the coats lost in the crash, found again → the unplayed
  seats' clothes → the two blankets in the plane and the sleeping bag in the tail → the engine cover,
  seat cushions, boughs, sphagnum stuffed in boots → Holt's bunk; and where you work is itself a
  warmth decision.
- **Hauling** — hands and bags → the cowling dragged → your own trails → the game trails, the dam and
  the spruce tunnel → Holt's freight sled, once its runner is mended.
- **Fire-craft** — the matches, the lighters, the ferro rod, the flare, the convex glasses → dead spruce
  twigs and birch bark → punk wood that carries an ember → chaga that holds one → friction on the right
  dry wood → avgas, a dangerous accelerant (documents 07, 12).
- **Information** — the chart (Holt's cabin, the lake, the creek, the knob and its survey marker), the
  view from the knob, the blazes, the ice, the tracks, and the voice on the radio once it answers.

### 4.9 How the party finds its way

No region is announced; each is found more than one way, so a party that misses one never loses it.
The lake shows west from the fuselage top, and the muskeg simply opens onto it. The ridge is up the
plane's own scar. The outlet is heard before it is seen. Holt's cabin is on the chart, is seen from the
knob as a clearing (and as smoke, once its stove is lit), and is reached by the blazes from the beaver
pond. The bear's country announces itself by its sign. What players learn, they learn in the world: the
tutorial rooms, each one simple situation (2026-09-27); what the world shows, and the physics of why an
attempt fails; and hints added case by case where something is very unobvious (document 17). There is no
survival manual in the world (2026-10-02).

### 4.10 The week on the map

The weather is the same every run (document 13 §4.2):

1. **Days 1–5** — bare, icy ground at the start, then snow on and off: the whole map is open and
   readable — berries on the bush, deadfall in sight, and after each flurry a morning of crisp tracks.
   Everything learned now — trails, blazes, where the deadfall lies, where the bear feeds — is worth it
   later. The country closes a little each day: colder nights, more of the low forage covered, the near
   deadfall burnt, the ground freezing deeper, the bear bolder as the camp smells of food. The search
   flies most days — the filed route, then wider, then narrowing toward this valley — and partial cloud
   and the trees make the wreck hard to see (document 14 §3.5). On day 5 a ring round the sun and the
   altimeter creeping up say heavier snow is coming.
2. **Day 6, the flurry** — steady snow from the early hours through the afternoon, and an east wind. The
   lake shore and the knob become hard places to be, sight closes to a few hundred metres, and the
   morning's tracks fill in. The creek, the blazes and the spruce tunnel still lead somewhere. Nothing
   flies. The lowest berry mats and the small deadfall go under.
3. **Day 6 night and day 7** — it clears into the coldest night of the run, coldest on the lake shore
   and the muskeg, where the cold air pools. Day 7 is calm over fresh snow: the best tracking of the
   week, and the day the rescuers find everyone still alive (2026-09-29).

Every timed beat is a world event: a search plane's engines carry as far as the sound really does,
heard before it is seen; and on a clearer night the aurora shows through the gaps in the cloud — and a
clearing sky means falling cold.

### 4.11 The density gradient

The crash site and its near forest are the densest place in the valley (the data budget, June 2026),
and the homestead is the second. The rest is authored in order — a priority, never a cap (2026-09-17):

- **Ring 0** — the crash site and the north wood's edge: modelled to the hilt.
- **Ring 1** — the scar, the muskeg, the birch slope, the near creek.
- **Ring 2** — the lake and the burn, the ridge, the bear's country, the pond, Holt's trail.
- **The homestead** — the second dense node.

Each grows by evidence like every other (document 22). What the material table still needs for the
outdoors — stone above all, bone and antler, fur and hide, punk wood, rubber, canvas, rawhide, grease —
and the snow and ice of this week are document 18's.

### 4.12 What the valley holds already

The crash is not the first thing that happened here. Ravens already work the valley; the far shore burned
some fifteen years ago and has grown back in aspen and fireweed; the beavers are laying in their winter;
a surveyor set a marker on the knob; Holt blazed his trail, set his traps, and left his cabin secured
against bears with kindling laid in the stove. The party is not the first people in the valley, and the
traces of the ones before are there to be read.

---

## 5. Interactions

**This document depends on:**

- **06 (time, sleep and the clock)** — travel minutes and work durations are meaningless without the
  running clock and the activity model; the whole map is priced in minutes.
- **08 (warmth, clothing and shelter)** — every zone carries an authored exposure band
  (`sheltered` < `broken` < `open` < `brutal`); the bands are inert until warmth drain exists.
- **13 (events, escalation and weather)** — the weather, day by day, is what re-prices the map; the
  flyovers and the aurora are its beats.
- **16 (players and kit)** and **12 (the pilot and bodies)** — who is aboard, what they carry, and the
  pilot's body.
- **18 (materials and forms)** — the census's missing materials (stone above all) gate the build.
- **23 (flora and fauna)** — what lives in each zone in October, and which animals act.
- **05 (ontology and sufficiency)** and **17 (rooms and living rooms)** — individuation, the prose
  style, and the state a room remembers.
- **19 (multiplayer and instances)** — sight and sound across zones is what makes a split party work:
  voices carry as far as they really do; sight works within a Scene and across open land case by case; smoke reads for miles.

**These depend on this document:**

- **14 (rescue paths)** — the three ways home happen on this map (§4.7): the heights for the antenna,
  the sightlines for signals, the wreck to keep findable.
- **10 (food and hunger)**, **09 (water)**, **07 (fire and shaping)** — every economy's sources are
  zones on this map.
- **02 (the experience)** — the sample week, rewritten once the design is finalized, walks this map.
- **22 (the world-building loops)** — the queue builds this document's places.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-17 (block 1):** reviewed in full. Travel is an attended activity (`walk`, `run`, `turn
  back`) that weather lengthens; walking out is not an ending and the cabin is supplies; the density
  gradient is authoring order, never a cap; wildlife as events and sign, no wolverine and no moose; dangerous places
  injure, never kill outright (chance never shown as dice — 2026-10-02); sweat is wet clothing inside the warmth
  system; keep the whole valley (then fifty zones and eleven regions), each region with a reason to come back. Follow-ups in
  `PLAN.md`: A4 (re-price the valley for the week-long run), E17 (exits as entities, travel as an
  activity).
- **2026-09-27 (Andrew)** — Holt does not come back during the week.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).
- **2026-10-02 (Claude, at Andrew's request)** — the whole map redesigned: thirteen regions with their
  roles, the lake's ice places gone (it is open all week), the lake's marsh edge, the burn as a region,
  the bear's country, the ridge's granite knob with its survey marker; for Andrew's review.

## 8. What exists today

**Built** — nine zones, all at the crash site, in `game/world/scenarios/winter_survival/zones.py`: `cockpit`,
`mid_cabin`, `rear_cabin`, `outside_nose`, `fuselage_top`, `outside_tail`, `debris_trail`,
`tail_section`, `treeline`. Each has a position, edges (walk/see), terrain tags and a survey line;
each has authored spaces in `game/world/scenarios/winter_survival/spaces.py` and objects in
`objects.py` / `objects/`; the probe corpus (`game/world/scenarios/winter_survival/probes/`) names those nine
zones and no others. Their full census is the ontology store's work (document 05 §4.5). The crash-site content includes the pilot's body, the sectional chart naming V. Holt's
cabin, the torn survival duffel, the snapped hatchet, the soaked matchbox, the sleeping bag, the
snowshoes and the ELT.

**Where the built crash site differs from the design** — content to change at the next crash-site
pass:

- **The airliner fiction.** `objects.py` defines a "forward overhead bin" and an "aft overhead bin", and
  seats identified as `11B` and `12C`. The design is the honest 206 interior — a hat shelf, a netted
  cargo bay and a jammed cargo door, with seats 1A/1B/2A/2B plus the right seat. The re-skin is small
  (names, aliases and prose; a `cargo net` object already exists).
- **The ELT** is built as an armed beacon whose antenna is sheared; the design's ELT is broken.
- **The radio** is built as a field radio in a cradle in the cockpit; the design has two radios — the plane's radio
  on the plane's battery, with a loose wire, and a hand radio in Holt's cabin whose batteries are in the
  tail (document 14 §3.2).
- **The survival kit** is built as a torn duffel lying on the debris trail; the design has no survival
  kit.
- **The snow.** The built crash site is authored deep in snow: a knee-deep `snowdrift` in the rear
  cabin, a `wind-packed drift` (`drift2`) holding the cooler and a duffel on the debris trail, the
  `the_drift` and `the_snow` spaces outside the nose and the tail, and survey lines and zone names to
  match. The design's week starts on bare, frosty ground and never lays more than a couple of inches
  (document 13 §4.2).

**Designed, not built** — the outdoor places. They exist as this document's tables. No outdoor zone id appears anywhere under
`game/` — verified 2026-09-27. The build order is document 22's queue (§4.5), behind the crash-site
foundation and the closure loop's clusters.

**Nothing yet** — the ontology store `docs/ontology/` does not exist. Nor does any of the machinery the
outdoor world assumes: travel durations, exposure and warmth drain, weather, hazard triggers, forage,
snare and fishing operations, track persistence and decay, ice growth, the timed-beat scheduler. The
map assumes operations that do not exist yet — `probe` (the map's signature verb), `climb`, `throw`,
`drag` and `haul`, setting a snare, `fish`, and more — and each zone needs a degraded behaviour that
keeps it playable until its operation ships.
