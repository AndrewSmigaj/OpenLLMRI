# 01 — The premise and the world

## 1. Status

> **Status: reviewed with Andrew 2026-09-17** (created 2026-09-16; brought to the current decisions
> 2026-09-27 — the season, the pilot, the ELT, what is aboard, Holt's cabin, the animals — for Andrew's
> check). **Architecture counterpart:** none — this document is *what the world is*; how zones, edges
> and Scenes are represented lives in
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md)
> (DR-13a) and [`../architecture/perception-model.md`](../architecture/perception-model.md). The built
> zones are `game/world/scenarios/whiteout/zones.py`.

This is the document you read to picture the whole world before anything else: what happened, when
and where it happened, what country the party is standing in, how big it is, what it costs to cross,
and every room in it. The valley's shape, its regions, its routes and all fifty outdoor zone designs
came out of one overnight design run on 2026-07-15 — **they are Claude's proposals**, reviewed with
Andrew on 2026-09-17 and brought to the first week of October on 2026-09-27.

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
- **The whole valley (2026-09-16, 2026-09-17).** All fifty outdoor zones and all eleven regions are in
  the first complete run, and each region gets a reason to come back. The size is judged by the travel
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
  long enough — exactly as document 14 §3. **The ELT is broken.** The hand radio's batteries are buried
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
- **(2026-10-02)** Each region's roles are listed in the map data. Things cost what they really cost —
  there is no required number of costs.
- **(2026-09-27)** Holt, the trapper, does not come back during the week; the cabin is supplies, not a place to be
  rescued from. His traces say so (document 14, 2026-09-28) — his trapline gear gone from its pegs, and a
  calendar on the cabin wall with a date circled weeks after the week.

### Proposals (Claude)

Everything else in this document is a proposal — from the 2026-07-15 overnight design run, and, for
its October state, from 2026-09-27 (every October detail below is Claude's, for Andrew's check):

- the valley's geography, size and shape (an unnamed side valley in interior Alaska);
- the **eleven regions** ("Scenes") and the **fifty outdoor zones**, each with its purpose, resources,
  prices, hazards and story;
- the jobs the regions do for the three ways home (§4.3, §4.7);
- what things cost (§4.3);
- every **number**: distances, travel minutes, exposure bands, the object census;
- the **density gradient** (Ring 0 / Ring 1 / Ring 2 / the homestead) as the way GDD §6's dense scene
  is honoured across a big map (§4.11);
- the week's **re-pricing** of the map (§4.10);
- the **discovery chains** — no region is announced; each is found several ways (§4.9);
- **V. Holt**, the absent trapper whose homestead holds the valley's other supplies;
- the **October state** of every zone — open water, new ice, the snow as it comes and what it covers.

Every count here is a floor, per the open-world rule: fifty zones is where the valley starts, not
where it stops, and no zone is ever "finished."

---

## 3. In one paragraph

A mail plane crossing a low ridge in the first week of October clips the spruce, sheds a wing and its
tail, and slides to a stop at the east edge of a muskeg white with hoarfrost. The pilot
is dead in his seat. The beacon is broken; the hand radio is dead, and its batteries are somewhere in
the wreckage of the tail; the search is starting where the flight plan said the plane would be, not
where it is. Step out of the hull and the country opens up: west across the bog is a lake,
open water with skim ice at its edges, whose shore is the widest sightline in the valley and the
windiest place to stand; north is spruce forest with the fuel, the snares and the most sheltered
ground; northeast the plane's own scar climbs to a wing in the trees with avgas in its tank and, above
that, a knob you can see the whole valley from — the highest place to raise an antenna; east is birch,
whose bark is one of the best tinders; and south the lake drains into a creek that
runs, with fish in its open pools, past a beaver pond to a blazed trapline that ends at a stranger's
cabin with a wood stove, some trapline gear and modest stores, two and a half kilometres away — about
ninety minutes the first time, one way. Things lie where they really would — some in plain sight, more
in the brush, under the moss or the coming snow, up a tree or a long walk off — and every hazard tells
you what it is before it takes anything. Snow comes on and off all week and the nights grow colder,
until a heavier flurry on day 6 clears into the coldest night of the run.

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
- **The hand radio** is dead; its **batteries are buried in a bag in the tail section**, which each
  flurry hides a little more (document 14 §3.2).
- **The ELT is broken.**
- **The plane's battery** is in the nose, wired and fine.
- **The freight and the mail** — flour, coffee, a small bag of dog food, a toolbox, the mail sack with a parcel for
  V. Holt — are scattered through the wreck and along the scar (documents 10 and 16).

Realism supplies the inventory; the crash supplies the difficulty: the tail tore off two hundred
metres back up the scar, the hatchet's haft snapped, the nurse's matches damp, the sleeping bag took avgas.
Where each thing lies is decided case by case, by what makes the game better (2026-09-28): what would make the start too easy — the tools and supplies that solve the big problems — is not lying in plain sight in the first room, and no rule hides things away; everything else lies where it would really lie — a dead fish on the shore.

Conditions: the first week of October; daylight, temperature, snow and ice day by day are document 13
§4.2. The search starts in the wrong place, and search and rescue is searching (document 14 §3.5).

### 4.2 The valley

An unnamed side valley in interior Alaska. West of the wreck the muskeg opens onto a lake; the lake
drains from its south end into a creek that runs southeast past a beaver pond; from the pond an old
blazed trapline climbs southeast to V. Holt's homestead on a bench — the cabin the sectional chart
promises ("V. HOLT — CABIN, WOOD STOVE"). North of the wreck is spruce forest; northeast, the plane's
own scar climbs to a ridge; east, a south-facing toe of birch.

```
                                    N
                                    ▲
                    THE RIDGE OVERLOOK · 4 zones · 800 m NE, +120 m
                    krummholz ▸ boulder field ▸ the knob ▸ the lee slope
                    (the cabin found · the weather read · height for the radio)
                                   ╱
                 THE STRIKE PATH · 4 zones · 110–330 m NE
                 shear line ▸ the wing in the trees ▸ the gear gouge ▸ bench saddle
                 (the plane's own scar, walked backwards: salvage + orientation)
                                ╱
  THE NORTH WOOD · 6 zones      │        THE BIRCH STAND · 4 zones · 350 m E
  60–260 m N — fuel, protein,    │        bark ▸ punk ▸ chaga ▸ the game trail
  the forward camp, the bivvy ╲ │ ╱      (how you make fire without a lighter)
                            treeline  scar
 THE LAKE ◄── THE MUSKEG ◄───── ✈ THE CRASH SITE · 9 zones ─────────────────► E
 6 zones      5 zones             cockpit ▸ cabin ▸ breach ▸ 200 m of scar ▸ the tail
 500 m W      120–420 m W         (the pilot's body · the chart · the radio · the tail)
 shore ▸ open water ▸ mid-lake ▸ inlet ▸ outlet      — where a party stays and signals
    │
    ├── the far-shore burn: 1.5 km W across the lake (the fuel jackpot; the greed test)
    │
    │ S — the outlet, heard before it is seen
 THE CREEK · 5 zones · 0.8–1.1 km SE
 riffle ▸ willow bar ▸ overflow bend ▸ logjam ▸ the fishing pool
    │ S
 THE BEAVER POND · 5 zones · 1.7 km S
 dam ▸ pond flat ▸ the lodge ▸ food cache ▸ the old drowned set (wire; the trailhead)
     ╲  the blazes climb SE
      THE TRAPLINE · 4 zones — blaze gateway ▸ spruce tunnel ▸ marten set ▸ cabin gate
          ╲ SE
           HOLT'S HOMESTEAD · 7 zones · 2.4 km of travel (~90 min, the first time)
           dooryard ▸ porch ▸ the cabin (stove) ▸ loft ▸ cache ▸ woodshed ▸ water hole
```

Zone positions are authored per zone in metres from the wreck, y+ = north, matching `zones.py`'s
convention.

Straight-line distances from the wreck: lake shore 500 m W · ridge knob 800 m NE (+120 m) · birch stand
350 m E · creek riffle 800 m SW · beaver pond 1.7 km S–SE · homestead 2.4 km of travel SE. The far-shore
burn is 1.5 km W across the lake — farther round its shore.

### 4.3 How the map is built

**Each region has a job in getting home**, and each region's roles are listed in the map data
(2026-10-02) — the store's region and zone rows (document 05 §4.5, document 22). The three ways home
(document 14 §3) are laid on the map:
the lake's shore and the knob are the sightlines where a signal can be seen; the ridge and the
fuselage top are the heights where the radio's antenna goes; the crash site is where a party stays,
signals and keeps itself findable; and the creek–trapline–cabin line leads to the valley's other
supplies (distance and navigation). The forest ring between them is the survival economy every way
spends from.

**The week gets harder** (the escalation, PLAN §5): the nights grow colder, each flurry covers more of the low forage, the near
deadfall burns away so every armful is a longer walk, water that is open in the first days freezes
too thin to trust, distance and the cold cost more, and on day 6 a heavier flurry closes the
world in for a day. Things cost what they really cost, in
these kinds of cost (2026-10-02 — no count of them is required; a rock on the creek bar costs a short walk):

| Cost | What spends it |
|---|---|
| **Daylight** | travel and work both burn the day's light (document 13 §4.2); the days shorten, and the day-6 flurry makes the useful part shorter |
| **Warmth** | every zone has an exposure band; the lake shore and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt, carried as wet clothing inside the warmth system (document 08) |
| **Tools** | blade, chopper, saw, container, cordage — each makes different work possible |
| **Knowledge** | reading sign: tracks, ice colour, blaze marks, dead spruce twigs. `examine` shows what is there; reading it is the player's |
| **Risk** | thin ice, the cold creek, the frost-glazed lee slope, the climb — always telegraphed; a fall is chance mixed with fitness, told as what happened, and it injures and never kills outright |

**Where things lie is decided case by case** (2026-09-28): there is no rule that hides things away.
What would make the start too easy is not in plain sight in the first room; everything else lies where
it really would — rocks on the creek bar and the ridge, a dead fish on the shore, deadfall in the
brush, a cache up a tree, a cabin 2.4 km off (§4.1).

### 4.4 The regions

| Region | Zones | What it is for | From the wreck |
|---|---|---|---|
| **S1 The Crash Site** | 9 ✅ | the wreck: the pilot's body, the chart, the hand radio and its batteries in the tail, what the crash scattered; where a party stays and signals | — |
| **S2 The Muskeg** | 5 📐 | the bog the pilot almost reached: tussocks and wet channels, tinder and berries, the way to the lake | 120–420 m W |
| **S3 The Lake** | 6 📐 | the widest sightline in the valley and the wind's home; open water all week, skim ice at its edges | 500 m W |
| **S4 The North Wood** | 6 📐 | fuel, shelter, game, the most sheltered ground | 60–260 m N |
| **S5 The Strike Path** | 4 📐 | the crash's scar up the hill — salvage, orientation, and avgas in the wing | 110–330 m NE |
| **S6 The Ridge Overlook** | 4 📐 | height for the radio's antenna, the view over the valley, and exposure to the wind | 800 m NE, +120 m |
| **S7 The Birch Stand** | 4 📐 | birch bark, punk wood, chaga | 350 m E |
| **S8 The Creek** | 5 📐 | the way south along running water: fish, willow, thin ice over the current | 0.8–1.1 km SW→SE |
| **S9 The Beaver Pond** | 5 📐 | the beavers' dam, lodge and food pile, and where Holt's trail starts | 1.7 km S |
| **S10 The Trapline** | 4 📐 | Holt's blazed trail: sheltered in any weather, each blaze in sight of the last | 1.7–2.4 km SE |
| **S11 Holt's Homestead** | 7 📐 | the second dense node: supplies — trapline gear and modest stores — a stove, and a portrait of its absent owner | 2.4 km SE |

### 4.5 The fifty-nine zones

✅ = built in `zones.py` today · 📐 = designed in this document, not built.

**S1 — The Crash Site** *(built; to be re-authored to the current decisions — §8)*

| Zone | What it is for | Status |
|---|---|---|
| `cockpit` | the panel, the pilot's body in the left seat, the chart and the flight manual; the wire behind the panel | ✅ |
| `mid_cabin` | the seats and what can be stripped from them, the luggage | ✅ |
| `rear_cabin` | the torn hull: frost on the metal and the flurries blowing in, the quilted engine cover, the draft to block | ✅ |
| `outside_nose` | the nose in the frozen moss; the plane's battery, wired and fine; the wings' fuel; the cowling | ✅ |
| `fuselage_top` | the watchtower: the torn antenna base, the valley's sightlines, a high place to raise an antenna, the worst exposure on site | ✅ |
| `outside_tail` | the breach exit — the hub between hull, scar and treeline | ✅ |
| `debris_trail` | the scatter: the mail sack, the freight, the hatchet in the brush, a little more hidden by each flurry | ✅ |
| `tail_section` | the tail wreckage: the broken ELT, the sleeping bag buried with it, and the bag holding the hand radio's batteries; *(Claude's, not yet decided: snowshoes here, and the sleeping bag soaked in avgas)* | ✅ |
| `treeline` | the supply room and the forest gateway: deadfall, boughs, dry grass | ✅ |

**S2 — The Muskeg**

| Zone | What it is for | Status |
|---|---|---|
| `tussock_flat` | cottongrass tinder, and lowbush and bog cranberries frost-sweetened on the bare mats; each flurry covers more, and the day-6 snow buries the bog cranberries while the lowbush cranberries poke through; hurrying can turn an ankle | 📐 |
| `labrador_thicket` | kindling in quantity and the hot-drink plant: kindling is free, an armload costs | 📐 |
| `tamarack_island` | bone-dry dead limbs, the best easy fuel west of the treeline | 📐 |
| `drifted_channel` | a wet channel under skim ice, its edges hidden under the thin new snow as the week goes on; water, sedge and mud; a probe finds the firm line | 📐 |
| `lake_gate_willows` | withes for lashings and the first hare runs to snare; the gate to the lake | 📐 |

**S3 — The Lake** — about 1.5 km long and 6–8 m at its deepest, deep enough for fish to winter in it;
fed by its inlet and drained south by the creek at the outlet, so grayling come down from the creek to
winter in it, and burbot, whitefish and pike live in it (document 23, 2026-10-02).

| Zone | What it is for | Status |
|---|---|---|
| `shore_apron` | the drift log (a big supply of fuel for a saw) and open water at the edge under a skin of ice at dawn | 📐 |
| `ice_flat` | *(Claude's, from the July winter design, not yet decided — the lake is open all week and walking out on any ice breaks it, so whether this stays a place, or becomes the open water seen from the shore, is open)* | 📐 |
| `pressure_ridge` | the lake's middle, reached only over the ice. Its winter design — a pressure ridge as a windbreak mid-crossing, with the cleanest blue ice — needs thick ice the first week of October does not have; in October this is open water, then the thinnest new ice | 📐 |
| `inlet_mouth` | skim ice and new ice forming, the current that keeps it thin, and running water at the inflow | 📐 |
| `outlet_narrows` | running water heard before it is seen: the way south, its border ice thin over the current | 📐 |
| `far_shore_burn` | a burn full of dead standing wood on the far shore: the long way round the lake — walking out on the ice breaks it (Andrew, 2026-09-27) | 📐 |

**S4 — The North Wood**

| Zone | What it is for | Status |
|---|---|---|
| `forest_edge` | green boughs for bedding, thatch and white signal smoke; the wood's first tracks | 📐 |
| `big_spruce_hollow` | dead spruce twigs, dry under the big spruce in any weather; *(Claude's, not yet decided: a forward camp here)* | 📐 |
| `deadfall_tangle` | a tangle of deadfall near the wreck, much of it needing a tool, under a dead tree leaning over it | 📐 |
| `grouse_thicket` | spruce grouse, tame enough to approach | 📐 |
| `hare_runs` | the hares' runs, the fresh ones plain in the new snow — where snares catch (document 10 §4.8) | 📐 |
| `tree_well_hollow` | shelter given by terrain: the dry ground under a big spruce's skirt, bare while the open ground whitens around it — a night on boughs and body heat | 📐 |

**S5 — The Strike Path**

| Zone | What it is for | Status |
|---|---|---|
| `shear_line` | the crash pre-cut a shelter's worth of boughs; the scar as an arrow back up the hill | 📐 |
| `wing_in_the_trees` | the sheared wing caught in the trees, avgas in its tank | 📐 |
| `gear_gouge` | the torn-off tyre (rubber burns with thick black smoke) | 📐 |
| `bench_saddle` | a saddle halfway up the climb | 📐 |

**S6 — The Ridge Overlook**

| Zone | What it is for | Status |
|---|---|---|
| `krummholz_band` | wind-stunted spruce and dwarf birch on the exposed ridge (a 120 m ridge is far below treeline): dry small fuel in a windy place | 📐 |
| `boulder_field` | hollow talus underfoot; *(Claude's, not yet decided: a survey cairn marked on the chart, and dry stakes)* | 📐 |
| `the_knob` | height: the cabin discovered, the weather read early, the highest place to raise the radio's antenna | 📐 |
| `lee_cornice` | the shortcut that isn't: a steep lee slope of frost-glazed rock, worse once the new snow hides the glaze; a fall injures and never kills outright | 📐 |

**S7 — The Birch Stand**

| Zone | What it is for | Status |
|---|---|---|
| `aspen_fringe` | dead aspen poles and punk wood, which carries an ember | 📐 |
| `birch_grove` | birch bark, which burns even damp | 📐 |
| `chaga_tree` | chaga ten feet up a birch — it catches a spark and holds an ember | 📐 |
| `game_trail_crossing` | an old shed antler (tool stock) | 📐 |

**S8 — The Creek**

| Zone | What it is for | Status |
|---|---|---|
| `outlet_riffle` | running water — a full container without melting snow, at the risk of wet boots | 📐 |
| `gravel_bar_willows` | willow in sled-load quantity, rose hips, and ptarmigan turning white that hide on snow and show against bare brush | 📐 |
| `overflow_bend` | the creek running fast under thin shelf ice that the first snow hides; a probe finds the edge | 📐 |
| `logjam_crossing` | a dry crossing and a lot of wood, over real voids between the logs | 📐 |
| `confluence_pool` | the fishing pool, open all week | 📐 |

**S9 — The Beaver Pond**

| Zone | What it is for | Status |
|---|---|---|
| `dam_crossing` | the causeway to the trapline side, and pre-cut poles you *could* pull from the working face | 📐 |
| `pond_flat` | bubble trails under the new ice, showing where the beavers swim | 📐 |
| `the_lodge` | the beavers' lodge — mud, sticks and bodies keeping a warm core in the cold | 📐 |
| `food_cache_margin` | the beavers' winter food pile, being built now: green poles that can be taken without touching the dam, and green wood that burns badly | 📐 |
| `drowned_set` | *(Claude's, not yet decided: an old drowned trap set with yards of snare wire, the first human sign beyond the wreck)* | 📐 |

**S10 — The Trapline**

| Zone | What it is for | Status |
|---|---|---|
| `blaze_gateway` | the start of Holt's blazed trail: each blaze in sight of the last | 📐 |
| `spruce_tunnel` | sheltered for its whole length — a long walk that stays easy in heavy weather | 📐 |
| `marten_set_tree` | Holt's old marten set behind a chain of small gates, empty — the trapping season has not opened | 📐 |
| `cabin_gate` | the gate to Holt's yard | 📐 |

**S11 — Holt's Homestead**

| Zone | What it is for | Status |
|---|---|---|
| `dooryard` | the yard and the dog-run cable | 📐 |
| `porch` | the door, unlocked; *(Claude's, not yet decided: swollen in its frame, and frozen to the sill by meltwater once the snow comes)* | 📐 |
| `cabin_interior` | the stove; Holt's shelf of modest stores; *(Claude's, not yet decided: kindling laid in the stove and a match tin)* | 📐 |
| `loft` | *(Claude's, not yet decided: wool in a cedar trunk, and a photograph that tells why Holt is away)* | 📐 |
| `cache` | a raised cache: trapline gear (snowshoes, the felling axe) and modest stores; *(Claude's, not yet decided: its ladder stashed under the cabin)* | 📐 |
| `woodshed` | *(Claude's, not yet decided: a winter of split dry wood, and a freight sled with a split runner)* | 📐 |
| `water_hole_path` | Holt's water infrastructure: bucket-water without the riffle's risks | 📐 |

### 4.6 Travel takes time

All week the going is the ground's own — tussocks, bog, deadfall, and ground frozen hard at dawn —
because the snow never gets deep: a couple of inches by the end (document 13 §4.2). What it does is
hide the footing: frost-glazed rock and roots on the first mornings, then the holes between the
tussocks and the thin ice on the channels once the snow lies over them. Your own trail is faster than
the first time — the firm line through the bog found, the brush broken, the deadfall stepped round — and
after a flurry it is plain to follow back. The creek's bank is quick going, at the risk of thin ice and cold
water. Snowshoes — in Holt's cache *(and, not yet decided, in the tail wreckage)* — are for deep snow the week never lays; on
a couple of inches over tussocks they only slow a walker. The map is big, and what speeds a party
across it is knowing it.

| Leg (one way) | First time | Known trail |
|---|---|---|
| wreck → lake shore | 20 min | 12 min |
| wreck → big spruce hollow | 15 min | 8 min |
| wreck → birch stand | 25 min | 15 min |
| wreck → ridge knob | 55 min | 40 min |
| wreck → creek riffle | 30 min | 18 min |
| wreck → beaver pond | 55 min | 35 min |
| wreck → homestead | ~90 min | ~60 min |

**The journey itself** (Andrew, 2026-09-28; document 19 §4.3). A Scene is a connected group of places — a
multi-place zone, bigger or smaller — and going to another one is a journey, not a step: you head off
in its direction and the world gives an estimate (*"You head off toward the birch grove; you reckon it
will take about twenty minutes."*). The walk is an attended activity with its own emotes, and on a
long one you may pass things along the way. You can stop walking, and then you are between Scenes —
*"You are between the birch grove and the plane"* — with whatever is near you, and no room description
beyond that. Moving from place to place inside a Scene takes time too, with the right emotes.

The minutes are placeholders, re-priced for the week-long run and the October ground by `PLAN.md`
task A4. Moving is an attended activity whose time is distance over pace, times terrain, snow depth,
load and fitness (document 03 §4.1a). Against the October day (document 13 §4.2) the first round trip
to the homestead is about three hours of walking before any work there — a commitment, and a bigger
one each day as the light shortens and the nights harden. That is the stay-or-go tension, made of
minutes instead of dialogue.

### 4.7 The three ways home, on the map

The ways home are document 14 §3's; this is where they happen.

| Way home | Rooms | Its scarce resource |
|---|---|---|
| **The radio** | the hand radio; its batteries in a bag in `tail_section`; anything metal and long enough for the antenna (the panel's wire, seat tubing, the dooryard's dog-run cable); a height to raise it — `fuselage_top`, `the_knob` | the batteries, dug out of the tail wreckage, and height |
| **A signal a plane can see** | the crash site; the lake shore's sightline; `gear_gouge` (the tyre's black smoke); the north wood's green boughs; the knob in clear air | fuel logistics, wind, and being ready when the engines are heard |
| **Surviving long enough** | everywhere — on day 7 the rescuers find everyone still alive (2026-09-29); before then, being found by an early pass takes work: partial cloud and the trees hide the wreck, so what the party builds decides it — a sign laid out on the ground, the wreck brushed clear, smoke | staying alive; for the early passes, the work of being findable |

**Holt's homestead is not a way home.** The creek run, the trapline and the homestead are the road to
the valley's other supplies — navigation skill and daylight are its price — and the cabin's chimney
smoke is a sign a search plane can see (document 14 §3.5).

### 4.8 The economies every way spends from

Each is a crude-to-mastery arc, and each is a network of rooms rather than a stat:

- **Fuel** — dead spruce twigs (starter) → dwarf birch and stunted spruce twigs (kindling, by the
  armload) → deadfall and the logjam (bulk, needing tools) → the drift log, the far burn, the woodshed
  (big supplies, far off or needing tools). The near
  deadfall is burnt first, so every armful is a longer walk, and the day-6 snow covers the small
  deadfall and pushes the work to standing dead wood and the far wood.
- **Water** — open water at the lake's edge and in the creek from the start, under a skin of ice at
  dawn; snow and ice melted by a fire anywhere, for a fuel tax; the riffle and Holt's water hole, still
  open when the still water has frozen. Eating snow costs body heat; water tainted by fuel or oil
  carries it (document 09).
- **Food** — the wreck's food (the pockets, the luggage, the freight) →
  cranberries, rose hips and roots (a trickle) → grouse and ptarmigan → snare lines
  (planning and cordage) → the fishery → Holt's modest stores (farthest away) → the
  bear (the richest food and the most dangerous, through the combat system) — and the
  pilot's body, which is food and taboo (document 12). Effort pays, eventually (document 10 §4.8).
- **Warmth and clothing** — crash clothing → the pilot's jacket and the unplayed seats' clothes → seat
  covers, the two blankets hidden in the plane, the sleeping bag buried with the tail →
  the loft trunk; plus the terrain layer, where *where you work* is itself a clothing decision.
- **Mobility and hauling** — boots → the cowling drag → your own trails → the game trails, the
  causeway and the tunnel (the world's own roads) → a sled *(Claude's, not yet decided: Holt's freight sled)*. Snowshoes wait for deep
  snow the week never lays. A dragged load snags on bare tussocks and slides easier over frozen ground
  under a skin of snow, but the tussocks still stand through a couple of inches.
- **Fire-craft** — lighter → dead spruce twigs → birch bark (a weatherproof start) → punk-cupped embers
  (portable flame) → chaga and a spark (lighterless insurance) → avgas (a dangerous shortcut).
- **Information** — the chart, the knob, the blaze protocol, ice-reading,
  track-reading, and the voice on the radio once it answers.

### 4.9 How the world teaches, and how the party finds it

No region is announced; each is discovered several independent ways, so a party that misses a clue
is never locked out. The cabin is found by the chart, from the knob's line of sight, or by the blaze at
the drowned set. The lake shows west from the fuselage top, and the muskeg simply opens onto it. The
ridge is pointed at by the plane's own gouge. Open water at the outlet is **audible** before it is
visible.

The muskeg's wet channel shows how the footing goes; the inlet, ice as it forms; the creek's bend,
thin ice over running water; the blazes, a trail that dusk or the flurry makes harder to follow. What
players learn, they learn in the world: the tutorial rooms, each one simple
situation (2026-09-27); what the world shows, and the physics of why an attempt fails; and hints added
case by case where something is very unobvious or players struggle (document 17). **There is no
survival manual in the world** (2026-10-02).

### 4.10 The week re-prices the map

The weather is the same every run (document 13 §4.2). Each part of it doesn't just dim the world, it
changes what things cost:

1. **The open days (days 1–5)** — bare, icy ground at the start, then snow on and off: the whole map
   is open, and the ground is readable — berries on the bush, deadfall in sight, and after each flurry
   a morning of crisp tracks. Scouting is cheap; the far burn round the shore and the ridge are
   affordable. Everything learned now — trails found, blazes followed, where the deadfall lies — is
   capital for later. Underneath, the country closes a little each day: the nights colder, each flurry
   covering more of the low forage, the near deadfall burnt so every armful is a longer walk, the
   ground freezing deeper. The search flies most days — the filed route, then the route, then wider,
   then narrowing toward this valley — but partial cloud and the trees make the wreck hard to see
   (document 14 §3.5). On day 5 a ring round the sun and the altimeter creeping up say heavier snow is
   coming.
2. **The flurry (day 6)** — steady snow from the early hours through the afternoon, and an east wind.
   Open country turns hostile: the lake shore and the knob become gambles, sight closes to a few
   hundred metres at its heaviest, and the morning's tracks fill in. Navigation shrinks to handrails —
   the creek, the blazes, a rope line you rigged, the wind's one direction. The sheltered routes (the
   spruce tunnel, the creek under its banks) keep working. Nothing flies. The lowest berry mats and the
   small deadfall go under, and the wreck turns white.
3. **The clearing (day 6 night and day 7)** — it clears through the evening into the coldest night of
   the run, coldest on the lake shore and the muskeg, where the cold air pools. Day 7 is calm over fresh
   snow: the best tracking of the week, and the day the rescuers find everyone still alive
   (2026-09-29; document 14 §3.5).

Every timed beat is a **world** event, never a silent no-op: a search plane's engines carry as far as the
sound really does, heard before it is seen, so a party far down the creek hears the pass it missed; and on a clearer night the north gets the aurora through the gaps in the cloud
(document 13 §4.3) — and a clearing sky means falling cold.

### 4.11 The density gradient

GDD §6 gives the dense scene the most modelling. The map keeps that promise across a big valley by
spending unevenly on purpose — as authoring order, a priority and never a cap:

- **Ring 0** — the crash site and the big spruce near it: modelled to the hilt.
- **Ring 1** — muskeg, strike path, birch stand, near creek: full interaction.
- **Ring 2** — lake, ridge, pond, trapline — and each grows by evidence like every other.
- **The homestead** — the second dense node.

The July object census counted **about 1,150 candidate objects, ambients and signs across the valley**,
beyond what is built at the crash site. It also named what the material table lacks for any of this
to be buildable — **rock and stone are absent today**, along with bone and antler, fur and hide, punk
wood, rubber, kerosene, canvas, rawhide, grease, brass and paper — and it distinguished fifteen-odd
snow and ice sub-types (powder, wind-slab, drift, sastrugi, rime, hoarfrost, black ice, shore ice,
skim ice, frazil, overflow…), each of which wants its own behaviour note. Those are document 18's to
settle; they are named here because the valley cannot be built without them.

### 4.12 What the valley is about *(Claude's, from the July design — not yet decided)*

One story is told by every room regardless of route order: **the crash is not the first thing that
ever happened here.** Ravens already commute to the wreck; the burn already regrew; the beavers are
already laying in their winter; a surveyor already measured the ridge; Holt already blazed his trail
and left his door unlocked and his kindling laid. The emotional argument is competence-before-you and
indifference-without-malice — which is the argument that the players' own competence is possible.

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
- **22 (the world-building loops)** — the queue builds this document's fifty zones.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-17 (block 1):** reviewed in full. Travel is an attended activity (`walk`, `run`, `turn
  back`) that weather lengthens; walking out is not an ending and the cabin is supplies; the density
  gradient is authoring order, never a cap; wildlife as events and sign, no wolverine and no moose; dangerous places
  injure, never kill outright (chance never shown as dice — 2026-10-02); sweat is wet clothing inside the warmth
  system; keep the fifty zones and all eleven regions, each with a reason to come back. Follow-ups in
  `PLAN.md`: A4 (re-price the valley for the week-long run), E17 (exits as entities, travel as an
  activity).
- **2026-09-27 (Andrew)** — Holt does not come back during the week.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built** — nine zones, all at the crash site, in `game/world/scenarios/whiteout/zones.py`: `cockpit`,
`mid_cabin`, `rear_cabin`, `outside_nose`, `fuselage_top`, `outside_tail`, `debris_trail`,
`tail_section`, `treeline`. Each has a position, edges (walk/see), terrain tags and a survey line;
each has authored spaces in `game/world/scenarios/whiteout/spaces.py` and objects in
`objects.py` / `objects/`; the probe corpus (`game/world/scenarios/whiteout/probes/`) names those nine
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
- **The radio** is built as a field radio in a cradle in the cockpit; the design's radio is the hand
  radio whose batteries are buried in a bag in the tail section (document 14 §3.2).
- **The survival kit** is built as a torn duffel lying on the debris trail; the design has no survival
  kit.
- **The snow.** The built crash site is authored deep in snow: a knee-deep `snowdrift` in the rear
  cabin, a `wind-packed drift` (`drift2`) holding the cooler and a duffel on the debris trail, the
  `the_drift` and `the_snow` spaces outside the nose and the tail, and survey lines and zone names to
  match. The design's week starts on bare, frosty ground and never lays more than a couple of inches
  (document 13 §4.2).

**Designed, not built** — the fifty outdoor zones. They exist as this document's tables; the fuller
zone-by-zone write-ups of the July run are in git history. No outdoor zone id appears anywhere under
`game/` — verified 2026-09-27. The build order is document 22's queue (§4.5), behind the crash-site
foundation and the closure loop's clusters.

**Nothing yet** — the ontology store `docs/ontology/` does not exist. Nor does any of the machinery the
outdoor world assumes: travel durations, exposure and warmth drain, weather, hazard triggers, forage,
snare and fishing operations, track persistence and decay, ice growth, the timed-beat scheduler. The
map assumes operations that do not exist yet — `probe` (the map's signature verb), `climb`, `throw`,
`drag` and `haul`, setting a snare, `fish`, and more — and each zone needs a degraded behaviour that
keeps it playable until its operation ships.
