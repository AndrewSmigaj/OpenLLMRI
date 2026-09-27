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
- **The pitch (June 2026; reworded with Andrew 2026-09-17).** Survivors of a bush-plane crash improvise
  with a physically modelled world to stay alive against cold, injury, hunger and a worsening storm
  until they are rescued. The only endings are rescued or dead.
- **The data budget (June 2026, GDD §6).** One authored crash; the crash site and its near forest are
  the densest place in the valley, modelled to the hilt.
- **The bar for rooms (2026-09-07).** Rooms are living and interesting, never half-thought. The things
  in them serve the rescue goals — fixing and using the radio, then surviving until help arrives, which
  means finding food and warmth — and there are several ways of doing things: a lighter can be found by
  looking hard enough, and fire can be lit in other ways too. Things take the time they take, and, as in
  a MUD, the player sees messages while an attempt is under way.
- **The aircraft (2026-09-07, 2026-09-16, 2026-09-27).** A Cessna 206-class single with the honest
  four-seat interior: seats 1A, 1B, 2A, 2B and the right seat, a hat shelf, a cargo net and a jammed
  cargo door. The plane itself is fine; the crash supplies the difficulty. The plane's battery is in the
  nose, wired and fine.
- **The run (2026-09-07, 2026-09-17).** Roughly a week of game time in one sitting of two or three
  hours, which the players can pause and return to. An escalation ladder and no hard time barriers;
  there is no set arc.
- **The whole valley (2026-09-16, 2026-09-17).** All fifty outdoor zones and all eleven regions are in
  the first complete run, and each region gets a reason to come back. The size is judged by the travel
  table (§4.6), now that travel is an attended activity. If a region is ever cut, it is the muskeg.
- **The season (2026-09-26, 2026-09-27).** The first week of October in interior Alaska — Claude's
  choice, at Andrew's request, for more than ten hours of daylight. An inch of snow at the start, bushes
  dusted but visible, berries and roots findable, skim ice on still water; light snow on days 1–2, the
  storm on days 3–4, clearing after. The same weather every run. The numbers are document 13 §4.2's.
- **The party (2026-09-16, 2026-09-27).** Up to five play: four adults and the kid. A seat nobody plays
  is a dead character whose clothes and pockets can be searched; AI agents may play seats. No back
  stories — the characters differ in clothes, injuries and what they carry, and in how well and how fast
  they do things (document 16).
- **The pilot (2026-09-17, 2026-09-27).** He starts the run dead and carries no clues. His body is food,
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
  birds act — on the engine's behaviour rules, or played by a lightweight model; fewer than three birds
  in a room, and not constantly calling. The fish are scripted. Other wildlife shows as events and
  sign. No wolverine. Flora and fauna are
  filtered by ecology: this habitat, this month, real numbers (document 23).
- **Moving through the valley (2026-09-17).** Moving between areas is an attended activity with
  feedback and events: `walk`, `run` (less time, more sweat), `turn back`. Some stretches take longer to
  cross; weather lengthens every trip, so exploring early is rewarded a little. There is no escape by
  walking out.
- **What the party does outside (2026-09-16).** The party probably won't stay outside much, but it can
  make a fire and a lean-to if it wants. The outdoors is terrain to cross and work in, not a second home
  the design must force them into.
- **Dangerous places (2026-09-17).** They injure, never kill outright; fitness matters; the outcome is
  a seeded dice roll, and the player is told a roll was made.
- **Sweat (2026-09-17).** Sweat is wet clothing draining warmth, inside the warmth system (document 08).
- **Density (2026-09-17).** The density gradient (§4.11) is authoring order — a priority, never a cap.
- **(2026-09-27)** Holt, the trapper, does not come back during the week; the cabin is supplies, not a place to be
  rescued from. *(Proposed by Claude, for Andrew's check:* his traces say so — his trapline gear, and a calendar
  on the cabin wall showing he returns after the week.)

### Proposals (Claude)

Everything else in this document is a proposal — from the 2026-07-15 overnight design run, and, for
its October state, from 2026-09-27 (every October detail below is Claude's, for Andrew's check):

- the valley's geography, size and shape (an unnamed side valley in interior Alaska);
- the **eleven regions** ("Scenes") and the **fifty outdoor zones**, each with its purpose, resources,
  prices, hazards and story;
- the jobs the regions do for the three ways home (§4.3, §4.7);
- the **six currencies** every resource is priced in, and the anti-easy rule (§4.3);
- every **number**: distances, travel minutes, exposure bands, the object census;
- the **density gradient** (Ring 0 / Ring 1 / Ring 2 / the homestead) as the way GDD §6's dense scene
  is honoured across a big map (§4.11);
- the storm's **re-pricing** of the map (§4.10);
- the **discovery chains** — no region is announced; each is found several ways (§4.9);
- **V. Holt**, the absent trapper whose homestead holds the valley's other supplies;
- the **October state** of every zone — open water, new ice, the first snow and what the storm buries.

Every count here is a floor, per the open-world rule: fifty zones is where the valley starts, not
where it stops, and no zone is ever "finished."

---

## 3. In one paragraph

A mail plane crossing a low ridge in the first week of October clips the spruce, sheds a wing and its
tail, and slides to a stop at the east edge of a muskeg dusted with the first inch of snow. The pilot
is dead in his seat. The beacon is broken; the hand radio is dead, and its batteries are somewhere in
the wreckage of the tail; the search is starting where the flight plan said the plane would be, not
where it is. Step out of the hull and the country starts pricing you: west across the bog is a lake,
open water with skim ice at its edges, whose shore is the widest sightline in the valley and the
windiest place to stand; north is spruce forest with the fuel, the snares and the most sheltered
ground; northeast the plane's own scar climbs to a wing in the trees with avgas in its tank and, above
that, a knob you can see the whole valley from — the highest place to raise an antenna; east is birch,
which is how you make fire when your lighter is gone; and south the lake drains into a creek that
runs, with fish in its open pools, past a beaver pond to a blazed trapline that ends at a stranger's
cabin with a wood stove, some trapline gear and modest stores, two and a half kilometres away — about
ninety minutes the first time, one way. Nothing out there is lying loose: everything is under the
snow, inside the ice, up a tree or a long walk off, and every hazard tells you what it is before it
takes anything. Two days of light snow, then the storm, then the clear cold behind it — what you can
reach, and use, before the snow buries it is the game.

---

## 4. The design

### 4.1 The crash (the premise, made specific)

A 206-class piston single — the Alaska mail-and-freight workhorse, on big tundra tyres in October
(document 16 §4.5) — came in from the northeast over a low ridge shoulder, clipped the spruce crowns,
shed its right wing into the trees, bellied down the slope and slid southwest across the muskeg fringe,
shedding the tail, to stop at the muskeg's east edge. The pilot was stretching for the flat of the
muskeg and almost made it. He died in the crash: the run starts with his body in the left seat, and he
carries no clues (document 12).

What is aboard is the design's call, and it is set so the run is neither too easy nor too hard:

- **There is no survival kit.**
- **The sleeping bag** is buried with the tail wreckage; **two blankets** are hidden inside the plane;
  there is **no firearm** (document 16).
- **The hand radio** is dead; its **batteries are buried in a bag in the tail section**, under snow that
  deepens every day the party waits (document 14 §3.2).
- **The ELT is broken.**
- **The plane's battery** is in the nose, wired and fine.
- **The freight and the mail** — flour, coffee, a small bag of dog food, a toolbox, the mail sack with a parcel for
  V. Holt — are scattered through the wreck and along the scar (documents 10 and 16).

Realism supplies the inventory; the crash supplies the difficulty: the tail tore off two hundred
metres back up the scar, the hatchet's haft snapped, the matches soaked, the sleeping bag took avgas.
The more a thing solves, the farther, deeper or more broken the crash left it.

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
                    krummholz ▸ boulder field ▸ the knob ▸ the lee cornice
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

### 4.3 The three rules the map is built on

**Each region has a job in getting home.** The three ways home (document 14 §3) are laid on the map:
the lake's shore and the knob are the sightlines where a signal can be seen; the ridge and the
fuselage top are the heights where the radio's antenna goes; the crash site is where a party stays,
signals and keeps itself findable; and the creek–trapline–cabin line leads to the valley's other
supplies (distance and navigation). The forest ring between them is the survival economy every way
spends from.

**The country is the difficulty engine.** Indoors, the crash supplied the difficulty. Outdoors, the
season does: the first snow and then the storm bury, water that is open in the first days freezes
too thin to trust, distance taxes, cold punishes idleness, and the storm closes the world one band at a
time. Nothing needed adding — only honest pricing. Every resource out here costs at least two of six
currencies:

| Currency | What spends it |
|---|---|
| **Daylight** | travel and work both burn the day's light (document 13 §4.2); the storm makes the useful part shorter |
| **Warmth** | every zone has an exposure band; the lake shore and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt, carried as wet clothing inside the warmth system (document 08) |
| **Tools** | blade, chopper, saw, container, cordage — each unlocks a different shelf of the world |
| **Knowledge** | reading sign: tracks, ice colour, blaze marks, dead spruce twigs. `examine` is the tutor |
| **Risk** | thin ice, the cold creek, the cornice, the climb — always telegraphed; a fall is a seeded roll, announced, that injures and never kills outright |

**The anti-easy rule.** Nothing usable lies loose on the surface anywhere in the valley except what the
crash itself scattered (which is already priced). Everything else is under snow, inside ice, up a tree,
behind a blaze you have to follow, or 2.4 km away. Fair, not generous: every hazard telegraphs, every
gate has several openings, `examine` always pays.

### 4.4 The regions

| Region | Zones | What it is for | From the wreck |
|---|---|---|---|
| **S1 The Crash Site** | 9 ✅ | the wreck: the pilot's body, the chart, the hand radio and its batteries in the tail, what the crash scattered; where a party stays and signals | — |
| **S2 The Muskeg** | 5 📐 | the bog the pilot almost reached: the travel tutorial, a tinder and berry trickle, the gate to the lake | 120–420 m W |
| **S3 The Lake** | 6 📐 | the widest sightline in the valley and the wind's home; the ice curriculum as the lake freezes; open water at its edges | 500 m W |
| **S4 The North Wood** | 6 📐 | the survival economy's heart: fuel, shelter, protein, the forward camp, the most sheltered ground | 60–260 m N |
| **S5 The Strike Path** | 4 📐 | the crash rewound — salvage, orientation, and one genuinely dangerous liquid | 110–330 m NE |
| **S6 The Ridge Overlook** | 4 📐 | height: the radio's scarce resource, the map's reveal, the honest exposure math | 800 m NE, +120 m |
| **S7 The Birch Stand** | 4 📐 | the fire-craft chapter: ignition, ember-craft, reading trees | 350 m E |
| **S8 The Creek** | 5 📐 | the travel corridor and the water chapter: running water, fish, willow, the thin-ice toll gate | 0.8–1.1 km SW→SE |
| **S9 The Beaver Pond** | 5 📐 | another engineer's infrastructure to reuse, wire to salvage, a larder to misunderstand, the trailhead | 1.7 km S |
| **S10 The Trapline** | 4 📐 | Holt's commute: the storm-safe route, the navigation tutorial, the quietest storytelling | 1.7–2.4 km SE |
| **S11 Holt's Homestead** | 7 📐 | the second dense node: supplies — trapline gear and modest stores — a stove, and a portrait of its absent owner | 2.4 km SE |

### 4.5 The fifty-nine zones

✅ = built in `zones.py` today · 📐 = designed in this document, not built.

**S1 — The Crash Site** *(built; the wider world adds only outward edges and glimpses — no interior
redesign)*

| Zone | What it is for | Status |
|---|---|---|
| `cockpit` | the panel, the pilot's body in the left seat, the chart and the flight manual; the wire behind the panel | ✅ |
| `mid_cabin` | the crafting heart: seats as a parts-machine, the tool caches, the luggage | ✅ |
| `rear_cabin` | the torn hull: blown-in snow, the engine-cover warmth prize, the draft to block | ✅ |
| `outside_nose` | the nose in the snow; the plane's battery, wired and fine; the wings' fuel; the cowling that becomes the party's first sled | ✅ |
| `fuselage_top` | the watchtower: the torn antenna base, the valley's sightlines, a high place to raise an antenna, the worst exposure on site | ✅ |
| `outside_tail` | the breach exit — the hub between hull, scar and treeline | ✅ |
| `debris_trail` | the scatter: the mail sack, the freight, the hatchet under the snow | ✅ |
| `tail_section` | the tail wreckage: the broken ELT, snowshoes, the sleeping bag buried with it and soaked in avgas, and the bag holding the hand radio's batteries | ✅ |
| `treeline` | the supply room and the forest gateway: deadfall, boughs, dry grass | ✅ |

**S2 — The Muskeg**

| Zone | What it is for | Status |
|---|---|---|
| `tussock_flat` | cottongrass tinder, and lowbush and bog cranberries frost-sweetened under the first snow until the storm buries them; hurrying wrenches an ankle | 📐 |
| `labrador_thicket` | kindling in quantity and the hot-drink plant: kindling is free, an armload costs | 📐 |
| `tamarack_island` | bone-dry dead limbs, the best easy fuel west of the treeline | 📐 |
| `drifted_channel` | the travel tuition zone: a wet channel under skim ice and the first snow, drifted deep after the storm; no resources; a probe finds the firm line | 📐 |
| `lake_gate_willows` | withes for lashings and the first hare runs to snare; the gate to the lake | 📐 |

**S3 — The Lake**

| Zone | What it is for | Status |
|---|---|---|
| `shore_apron` | the lake's honest zone: the drift log (a season of fuel behind a saw) and open water at the edge under a skin of ice at dawn; no hazards, deliberately | 📐 |
| `ice_flat` | the open lake: visibility is the resource, wind is the bill; open water at first, new ice later that holds nobody until it thickens (document 13 §4.2); the map's most dangerous room in the storm | 📐 |
| `pressure_ridge` | the lake's middle, reached only over the ice. Its winter design — a pressure ridge as a windbreak mid-crossing, with the cleanest blue ice — needs thick ice the first week of October does not have; in October this is open water, then the thinnest new ice | 📐 |
| `inlet_mouth` | the ice curriculum as the lake freezes — skim ice, new ice, the current that keeps it thin — and running water at the inflow | 📐 |
| `outlet_narrows` | running water heard before it is seen: the discovery chain south, its border ice thin over the current | 📐 |
| `far_shore_burn` | the fuel jackpot on the far shore: the long way round the lake while it is open, across it only once the ice holds — the greed test | 📐 |

**S4 — The North Wood**

| Zone | What it is for | Status |
|---|---|---|
| `forest_edge` | green boughs for bedding, thatch and white signal smoke; the wood's first tracks | 📐 |
| `big_spruce_hollow` | dead spruce twigs — the always-dry fire starter — and the forward camp of the dense core | 📐 |
| `deadfall_tangle` | the near fuel mother-lode, tool-priced, under a named widow-maker | 📐 |
| `grouse_thicket` | tame protein you must approach slowly and throw at | 📐 |
| `hare_runs` | the snare line: the best protein per effort, gated on wire and on reading which runs are fresh in the new snow | 📐 |
| `tree_well_hollow` | shelter given by terrain: the dry ground under a big spruce — a tree well once the storm's snow is down — a night on boughs and body heat | 📐 |

**S5 — The Strike Path**

| Zone | What it is for | Status |
|---|---|---|
| `shear_line` | the crash pre-cut a shelter's worth of boughs; the scar as an arrow back up the hill | 📐 |
| `wing_in_the_trees` | avgas in the tip tank: the valley's accelerant and its most dangerous convenience, several ways to reach it | 📐 |
| `gear_gouge` | the torn-off tyre — black smoke that reads as man-made against snow | 📐 |
| `bench_saddle` | the mid-station where the climb's cost becomes informed consent | 📐 |

**S6 — The Ridge Overlook**

| Zone | What it is for | Status |
|---|---|---|
| `krummholz_band` | the driest small fuel on the map, kept in the worst place to need it; the staging shelf | 📐 |
| `boulder_field` | the survey cairn (a fixed point on the chart) and dry stakes; hollow talus underfoot | 📐 |
| `the_knob` | height: the cabin discovered, the weather read early, the highest place to raise the radio's antenna | 📐 |
| `lee_cornice` | the shortcut that isn't: a steep lee slope, and after the storm a new cornice — a roof over air; a fall injures and never kills outright | 📐 |

**S7 — The Birch Stand**

| Zone | What it is for | Status |
|---|---|---|
| `aspen_fringe` | push-over poles and punk wood: the ember you can carry | 📐 |
| `birch_grove` | bark in three grades: fire that starts wet | 📐 |
| `chaga_tree` | the spark-catching fungus ten feet up — lighterless insurance, and the reward for looking up | 📐 |
| `game_trail_crossing` | an old shed antler (tool stock) and a moose bed's heat lesson; the moose itself may be on the trail (document 23 §4.1a) | 📐 |

**S8 — The Creek**

| Zone | What it is for | Status |
|---|---|---|
| `outlet_riffle` | free-running water: a full container without burning a stick, priced in wet-boot risk | 📐 |
| `gravel_bar_willows` | willow in sled-load quantity, rose hips, and ptarmigan turning white that hide on snow and show against bare brush | 📐 |
| `overflow_bend` | the southern toll gate: the creek running fast under thin shelf ice that the first snow hides — telegraphed, and a probe finds the edge | 📐 |
| `logjam_crossing` | the only dry crossing and the southern fuel depot, over booby-trapped voids | 📐 |
| `confluence_pool` | the fishery, open at the start of the run: the longest chain on the map and the one calorie source that scales | 📐 |

**S9 — The Beaver Pond**

| Zone | What it is for | Status |
|---|---|---|
| `dam_crossing` | the causeway to the trapline side, and pre-cut poles you *could* pull from the working face | 📐 |
| `pond_flat` | the bubble-trails under the new ice: wonder that doubles as a map of who lives here | 📐 |
| `the_lodge` | the shelter chapter taught by a rodent — mass, insulation and bodies make a livable core in the cold | 📐 |
| `food_cache_margin` | the beavers' winter larder, being built now; the ethical harvest (green poles without touching the dam) and the green-wood lesson | 📐 |
| `drowned_set` | snare wire in yards, free of the plane; the first human sign beyond the wreck | 📐 |

**S10 — The Trapline**

| Zone | What it is for | Status |
|---|---|---|
| `blaze_gateway` | the navigation tutorial: each blaze visible from the last. It installs a skill and holds no loot | 📐 |
| `spruce_tunnel` | sheltered for its whole length: the only long move that stays cheap in heavy weather | 📐 |
| `marten_set_tree` | Holt's old marten set behind a chain of small gates, empty — the trapping season has not opened; his craft, read a second time | 📐 |
| `cabin_gate` | the threshold beat: hope, correction, and a door anyway | 📐 |

**S11 — Holt's Homestead**

| Zone | What it is for | Status |
|---|---|---|
| `dooryard` | the yard's infrastructure and the dog-run cable; the note before the note | 📐 |
| `porch` | the door: after the storm, a drift against it — dig it bare-handed and soak your layers, or ten minutes with the shed's shovel | 📐 |
| `cabin_interior` | the stove, with the first move pre-paid — laid kindling and a match tin; Holt's shelf of modest stores | 📐 |
| `loft` | wool in a cedar trunk, and the photograph that names the absent man's reason | 📐 |
| `cache` | ten feet of air as a puzzle: trapline gear (snowshoes, the felling axe) and modest stores, behind a ladder stashed under the cabin | 📐 |
| `woodshed` | a winter of split dry wood 2.4 km from where it is needed; the freight sled with a split runner | 📐 |
| `water_hole_path` | Holt's water infrastructure: bucket-water without the riffle's risks | 📐 |

### 4.6 Travel is the price tag

At the start of the run the snow is an inch deep and the going is the ground's own — tussocks, bog,
deadfall. After the storm, unbroken snow is the tyrant: knee-deep trail-breaking moves at about
1.5 km/h and costs sweat. Your own broken trail is twice as fast — until the next snow refills it. The
creek's bank is a highway with a toll (thin ice and cold water). Snowshoes — in the tail wreckage and
in Holt's cache — roughly double open-country speed once the snow is deep, which is why the mobility
upgrade is treasure: the map is big.

| Leg (one way) | First time | Broken trail | On snowshoes |
|---|---|---|---|
| wreck → lake shore | 20 min | 12 min | 8 min |
| wreck → big spruce hollow | 15 min | 8 min | 6 min |
| wreck → birch stand | 25 min | 15 min | 10 min |
| wreck → ridge knob | 55 min | 40 min | 35 min (wind, not depth) |
| wreck → creek riffle | 30 min | 18 min | 12 min |
| wreck → beaver pond | 55 min | 35 min | 25 min |
| wreck → homestead | ~90 min | ~60 min | ~40 min |
| across the lake to the burn, once the ice holds | 25 min | — (wind erases the trail) | 15 min |

The table was drawn for deep snow; it is re-priced for the week-long run and the October ground by
`PLAN.md` task A4. Moving is an attended activity whose time is distance over pace, times terrain,
snow depth, load and fitness (document 03 §4.1a). Against the October day (document 13 §4.2) the first
round trip to the homestead is about three hours of walking before any work there — a commitment, and
a bigger one once the storm has filled the trail. That is the stay-or-go tension, made of minutes
instead of dialogue.

### 4.7 The three ways home, on the map

The ways home are document 14 §3's; this is where they happen. No two compete for their key resource,
and every one of them spends from the shared survival economy.

| Way home | Rooms | Its scarce resource |
|---|---|---|
| **The radio** | the hand radio; its batteries in a bag in `tail_section`; anything metal and long enough for the antenna (the panel's wire, seat tubing, the dooryard's dog-run cable); a height to raise it — `fuselage_top`, `the_knob` | the batteries, digging for them as the snow deepens, and height |
| **A signal a plane can see** | the crash site; the lake shore's sightline; `gear_gouge` (the tyre's black smoke); the north wood's green boughs; the knob in clear air | fuel logistics, wind, and being ready when the engines are heard |
| **Surviving long enough** | everywhere — and after the storm, keeping the party findable: digging the wreck out, a sign stamped in the snow, smoke | staying alive, and the work of being findable |

**Holt's homestead is not a way home.** The creek run, the trapline and the homestead are the road to
the valley's other supplies — navigation skill and daylight are its price — and the cabin's chimney
smoke is a sign a search plane can see (document 14 §3.5).

### 4.8 The economies every way spends from

Each is a crude-to-mastery arc, and each is a network of rooms rather than a stat:

- **Fuel** — dead spruce twigs (starter) → dwarf birch and krummholz twigs (kindling, priced in
  armloads) → deadfall and the logjam (bulk, tool-priced) → the drift log, the far burn, the woodshed
  (jackpots, distance- and tool-priced). Fire is always possible; scale is always earned. The storm
  buries the deadfall and pushes the work to standing dead wood.
- **Water** — open water at the lake's edge and in the creek from the start, under a skin of ice at
  dawn; snow and ice melted by a fire anywhere, for a fuel tax; the riffle and Holt's water hole, still
  open when the still water has frozen. Eating snow costs body heat; water tainted by fuel or oil
  carries it (document 09).
- **Food** — the wreck's food (the pockets, the luggage, the freight) →
  cranberries, rose hips and roots (a trickle) → grouse and ptarmigan (skill shots) → snare lines
  (planning + wire) → the fishery (the source that scales) → Holt's modest stores (farthest away) → the
  bear and the moose (the richest food and the most dangerous, through the combat system) — and the
  pilot's body, which is food and taboo (document 12). Calories scale with commitment, never with luck.
- **Warmth and clothing** — crash clothing → the pilot's jacket and the unplayed seats' clothes → seat
  covers, the two blankets hidden in the plane, the sleeping bag buried with the tail →
  the loft trunk; plus the terrain layer, where *where you work* is itself a clothing decision.
- **Mobility and hauling** — boots → the cowling drag → your own broken trails → the game trails, the
  causeway and the tunnel (the world's own roads) → snowshoes → the repaired freight sled. A dragged
  load snags on an inch of snow over tussocks and runs once the storm has filled the hollows.
- **Fire-craft** — lighter → dead spruce twigs → birch bark (a weatherproof start) → punk-cupped embers
  (portable flame) → chaga and a spark (lighterless insurance) → avgas (a dangerous shortcut).
- **Information** — the chart, the manual's pages, the knob, the blaze protocol, ice-reading,
  track-reading, and the voice on the radio once it answers. The only massless economy, which is why
  the knob — pure information — justifies the map's hardest climb.

### 4.9 How the world teaches, and how the party finds it

No region is announced; each is discovered several independent ways, so a party that misses a clue
is never locked out. The cabin is found by the chart, from the knob's line of sight, or by the blaze at
the drowned set. The lake shows west from the fuselage top, and the muskeg simply opens onto it. The
ridge is pointed at by the plane's own gouge. Open water at the outlet is **audible** before it is
visible.

The knowledge currency is paid back the same way every time: a cheap tutorial zone, a zone where the
lesson pays, and an exam — usually the tutorial's own room revisited at night or in the storm. The
drifted channel teaches footing; the inlet teaches ice as it forms; the creek's bend teaches thin ice
over running water; the blaze gateway teaches the trail the storm will later test closed-book. Behind
every knowledge price stands an in-game teacher, and most of them are **the survival manual**: its
read-pages (fire, water, shelter, signals, food, fishing, search and rescue, exposure) are
first-class content, ranked equal with the zone looks, under one authoring rule — the manual may
simplify, but it must never lie.

### 4.10 The storm re-prices the map

The weather is the same every run (document 13 §4.2). Each part of it doesn't just dim the world, it
changes what things cost:

1. **Light snow (days 1–2)** — the whole map is open, and the ground is still readable: berries on the
   bush, deadfall in sight, every track crisp. Scouting is cheap; the far burn round the shore and the
   ridge are affordable. Everything learned now — trails broken, blazes found, where the deadfall lies —
   is capital for later. The search flies the filed route, then the route between showers (document 14
   §3.5).
2. **The storm (days 3–4)** — steady snow building to heavy, and wind. Open country turns hostile: the
   lake shore and the knob become gambles, sight bands collapse, and the morning's trail fills in.
   Navigation shrinks to handrails — the creek, the blazes, a rope line you rigged, the wind's one
   direction. The sheltered routes (the spruce tunnel, the creek under its banks) keep working. Nothing
   flies. The low berries, the deadfall and the wreck's outline go under.
3. **The clearing (day 5 on)** — the snow ends and the cold falls in behind it. Every trip now breaks
   trail through deep snow, forage and fuel are under it, and the wreck has vanished from the air —
   but these are the clearest days of the run, and the search's best (document 14 §3.5).

**Night** is always the same argument: the world is three lit rooms — a fire you built, the fuselage
huddle, or Holt's stove. Everything else is a mistake.

Every timed beat is a **world** event, never a silent no-op: a search plane's engines are audible in
every exterior zone with a bearing, heard before it is seen, so a party a day's walk south *hears*
what its choices cost; and on a clear night the north gets the aurora (document 13 §4.3) — beauty
honestly priced, because clear skies mean falling cold.

### 4.11 The density gradient

GDD §6 gives the dense scene the most modelling. The map keeps that promise across a big valley by
spending unevenly on purpose — as authoring order, a priority and never a cap:

- **Ring 0** — the crash site and the big-spruce forward camp: modelled to the hilt.
- **Ring 1** — muskeg, strike path, birch stand, near creek: full interaction, leaner object counts.
- **Ring 2** — lake, ridge, pond, trapline: purposeful terrain. Each zone exists for a decision, a
  resource, a hazard or a story beat — and grows by evidence like every other.
- **The homestead** — the second dense node.

The July object census counted **about 1,150 candidate objects, ambients and signs across the valley**,
beyond what is built at the crash site. It also named what the material table lacks for any of this
to be buildable — **rock and stone are absent today**, along with bone and antler, fur and hide, punk
wood, rubber, kerosene, canvas, rawhide, grease, brass and paper — and it distinguished fifteen-odd
snow and ice sub-types (powder, wind-slab, drift, sastrugi, rime, hoarfrost, black ice, shore ice,
skim ice, frazil, overflow…), each of which wants its own behaviour note. Those are document 18's to
settle; they are named here because the valley cannot be built without them.

### 4.12 What the valley is about

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
  voices carry zones, not kilometres; the knob sees everything; smoke reads for miles.

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
  gradient is authoring order, never a cap; wildlife as events and sign, no wolverine; dangerous places
  injure, never kill outright, by an announced seeded roll; sweat is wet clothing inside the warmth
  system; keep the fifty zones and all eleven regions, each with a reason to come back. Follow-ups in
  `PLAN.md`: A4 (re-price the valley for the week-long run), E17 (exits as entities, travel as an
  activity).
- **2026-09-27 (Andrew)** — Holt does not come back during the week.

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
