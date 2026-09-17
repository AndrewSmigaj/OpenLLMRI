# 01 — The premise and the world

## 1. Status and sources

> **Status: draft for review** (created 2026-09-16). **Architecture counterpart:** none — this
> document is *what the world is*; how zones, edges and Scenes are represented lives in
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md)
> (DR-13a) and [`../architecture/perception-model.md`](../architecture/perception-model.md).
> **Sources:** [`../investigation/world/map.md`](../investigation/world/map.md) ·
> [`../investigation/world/rooms.md`](../investigation/world/rooms.md) ·
> [`../investigation/world/report.md`](../investigation/world/report.md) ·
> [`../investigation/world/objects.md`](../investigation/world/objects.md) ·
> [`../investigation/world/build-queue.md`](../investigation/world/build-queue.md) ·
> [`../investigation/plane-interior.md`](../investigation/plane-interior.md) ·
> [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md) §6/§8 ·
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §2
> (Andrew's amendments) · `game/world/scenarios/whiteout/zones.py` (the built zones).
> Provenance audit: [`../investigation/design/00-provenance-audit.md`](../investigation/design/00-provenance-audit.md).

This is the document you read to picture the whole world before anything else: what happened, when
and where it happened, what country the party is standing in, how big it is, what it costs to cross,
and every room in it. The valley's shape, its regions, its routes and all fifty outdoor zone designs
came out of one overnight design run on 2026-07-15 — **they are Claude's proposals, and they are what
this review is judging: interesting, or not.**

---

## 2. Provenance

### Andrew's decisions

- **The premise (GDD §6, his original design text, June 2026).** "Off-route winter crash, wrong search
  area, dead radio, weak beacon, unstable wreck, ~5h daylight." The search grid is in the wrong place:
  nobody is coming to where you are.
- **The pitch (GDD §1 / `VISION.md`, June 2026).** "Survivors of a snowy plane crash improvise with a
  physically-modeled world to outlast cold, injury, hunger, and a worsening storm until rescue, escape,
  or collapse."
- **The data budget (GDD §6, June 2026).** "One authored crash. One **dense scene** (cabin + camp +
  near-forest) gets the whole data budget — modeled to the hilt — rather than spread thin."
- **The bar for rooms (2026-09-07, verbatim).** "we dont want half thought rooms we want living
  interesting rooms - but at the same time the things will facilitate completing the various rescue
  goals (fix radio, use radio, then survive until help arives so find food, find warmth, etc) and
  there should be several ways of doing things - you could find a lighter if you look hard enough but
  can light it in various other ways, and of course a lot of things have time it takes, like a MUD you
  will see 'attempting to X' with appropriate messages that fire."
- **The weather arc (GDD §8, June 2026).** Weather escalates "light → steady → heavy → near-whiteout →
  night (−15 to −20 °C), degrading visibility/audibility/fire/tracks/rescue," with "2–3 timed beats (a
  search plane that misses you; the pilot's last lucid line) so the curve doesn't sag."
- **The aircraft (2026-09-07, recorded in architecture §2).** "The aircraft is the 206-class single
  (plane-interior §1) with the honest interior (cargo net + hat shelf + jammed cargo door; seats
  1A/1B/2A/2B + the right seat)." The plane itself is fine — it is the crash that supplies the
  difficulty.
- **The run length (2026-09-07, DR-15a).** Roughly a week of game time, persisting across sittings;
  rescue can come earlier, it can run longer until the food runs out; an escalation ladder, and "**no
  hard time-window barriers**." There is **no set arc**.
- **The whole valley is in scope (2026-09-16, architecture §2).** "The whole valley (all fifty outdoor
  zones, the walk-out included) is in the first complete run."
- **December (2026-09-16, architecture §2).** "The crash is in December — no bear (wolves and a
  wolverine)." Alaska bears are denned by December; the valley's predators are wolves and a wolverine.
- **The party (2026-09-16).** "The kid is in (a party of four or five)."
- **What the party will actually do outside (2026-09-16, said in conversation; not yet written into any
  document).** The party probably won't stay outside much — but they can make a fire and a lean-to if
  they want to. The outdoors is terrain to cross and work in, not a second home the design must force
  them into.

### Proposals (Claude)

Everything below that is not quoted above is a proposal from the 2026-07-15 overnight design run, in
`docs/investigation/world/`. Specifically, **all of this is proposed, not decided**:

- the valley's geography, size and shape (an unnamed side valley in interior Alaska);
- the **eleven regions** ("Scenes") and the **fifty outdoor zones**, each with its authored look,
  resources, prices, hazards and story beat (`rooms.md`);
- **one region per rescue route**, and the four routes as room itineraries (`report.md` §2);
- the **six currencies** every resource is priced in, and the anti-easy rule (`map.md` §1);
- every **number**: distances, travel minutes, exposure bands, the ~1,150-object census (`objects.md`);
- the **density gradient** (Ring 0 / Ring 1 / Ring 2 / the homestead) as the way GDD §6's "one dense
  scene" is honoured across a big map (`map.md` §6);
- the storm's **spatial re-pricing** of the map (`map.md` §5) as the application of GDD §8;
- the **discovery chains** (no region is announced; each is found at least two ways);
- the cast: ravens, spruce grouse, hare, ptarmigan, marten, an offstage moose, the beavers — and
  **V. Holt**, the absent trapper whose homestead is the endgame shelter;
- the three assessment sweeps in `report.md` §8–§10 and everything they changed.

Every count here is a floor, per the locked open-world rule: fifty zones is where the valley starts,
not where it stops, and no zone is ever "finished."

---

## 3. In one paragraph

A mail plane going over a low ridge in December clips the spruce, sheds a wing and its tail, and slides
to a stop at the east edge of a frozen muskeg; the pilot is dying, the radio is dead, the beacon is
screaming into a sheared antenna, and the search grid is a hundred miles off. You have about five hours
of light. Step out of the hull and the country starts pricing you: west across the bog is a frozen lake
wide enough that anything burning on it can be seen for miles, and cold enough that standing on it
costs you; north is spruce forest with the fuel, the snares and the only free warmth on the map;
northeast the plane's own scar climbs to a wing in the trees with avgas in its tank and, above that, a
knob you can see the whole valley from; east is birch, which is how you make fire when your lighter is
gone; and south the lake drains into a creek that runs, with liquid water and fish under the ice, past
a beaver pond to a blazed trapline that ends at a stranger's cabin with a wood stove in it, two and a
half kilometres away — half a day of light, round trip, the first time. Nothing out there is lying
loose on the snow; everything is under it, inside ice, up a tree, or a long walk off, and every hazard
tells you what it is before it takes anything. What you can afford to reach, before the snow gets
heavy and the light goes, is the game.

---

## 4. The design

### 4.1 The crash (the premise, made specific)

A 206-class piston single on wheel-skis — the Alaska mail-and-freight workhorse — came in from the
northeast over a low ridge shoulder, clipped the spruce crowns, shed its right wing into the trees,
bellied down the slope and slid southwest across the muskeg fringe, shedding the tail, to stop at the
muskeg's east edge. *(Proposal — `map.md` §2.)* The pilot was stretching for the lake ice and almost
made it. He is alive and dying; he dies within the first day and nobody can talk to him (doc 12).

The plane was legal under Alaska Statute AS 02.35.110, which requires an emergency kit aboard every
in-state flight — a week of rations per occupant, an axe, a first-aid kit, sealed signalling devices,
and, from 15 October to 1 April, snowshoes, a sleeping bag and a wool blanket per occupant. *(Sourced
fact, `plane-interior.md` §7.)* **That single statute justifies the entire survival economy without
inventing anything** — and the crash then decides where the kit is and what shape it is in: the tail
tore off two hundred metres back up the scar, the duffel split, the hatchet's haft snapped, the matches
soaked, the sleeping bag took avgas, the ELT's antenna sheared. Realism supplies the inventory; the
crash supplies the difficulty. *(`plane-interior.md` §8b — proposal, shipped in the built content.)*

Conditions: December, roughly −15 °C falling to −20 °C after dark, about five hours of usable light,
weather on GDD §8's ladder. The search grid is in the wrong area.

### 4.2 The valley

An unnamed side valley in interior Alaska. West of the wreck the muskeg opens onto a lake; the lake
drains from its south end into a creek that runs southeast past a beaver pond; from the pond an old blazed
trapline climbs southeast to V. Holt's homestead on a bench — the cabin the sectional chart promises
("V. HOLT — CABIN, WOOD STOVE"). North of the wreck is spruce forest; northeast, the plane's own scar
climbs to a ridge; east, a south-facing toe of birch. *(Proposal — `map.md` §2, `rooms.md`.)*

```
                                    N
                                    ▲
                    THE RIDGE OVERLOOK · 4 zones · 800 m NE, +120 m
                    krummholz ▸ boulder field ▸ the knob ▸ the lee cornice
                    (the cabin found · the weather read · elevation for the radio)
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
 500 m W      120–420 m W         (the kit · the ELT · the pilot · the chart)
 shore ▸ open ice ▸ pressure ridge ▸ inlet ▸ outlet       — the signal stage
    │
    ├── the far-shore burn: 1.5 km W across open ice (the fuel jackpot; the greed test)
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

*(Adapted from `map.md` §2, which carries the original diagram; zone positions in metres from the
wreck, y+ = north, are authored per zone in `rooms.md` and match `zones.py`'s convention.)*

Straight-line distances from the wreck: lake shore 500 m W · ridge knob 800 m NE (+120 m) · birch stand
350 m E · creek riffle 800 m SW · beaver pond 1.7 km S–SE · homestead 2.4 km of travel SE. The far-shore
burn is 1.5 km W **across open lake ice**.

### 4.3 The three rules the map is built on *(proposals — `map.md` §1)*

**Each region anchors one rescue route.** GDD §37–39 asks for additive rescue confidence with several
winning combinations drawing on *distinct* scarce resources. The map is that design made geographic:
the lake anchors the visual route (open sightlines), the ridge anchors radio and beacon (elevation),
the creek–trapline–cabin line anchors travel and shelter (distance and navigation), and the crash site
anchors stay-and-signal. The forest ring between them is the survival economy every route spends from.

**The country is the difficulty engine.** Indoors, the crash supplied the difficulty. Outdoors, winter
does: snow buries, ice gates, distance taxes, cold punishes idleness, and the storm closes the world
one band at a time. Nothing needed adding — only honest pricing. Every resource out here costs at least
two of six currencies:

| Currency | What spends it |
|---|---|
| **Daylight** | travel and work both burn the ~5 h light budget; the storm shortens it further |
| **Warmth** | every zone has an exposure band; open ice and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt |
| **Tools** | blade, chopper, saw, container, cordage — each unlocks a different shelf of the world |
| **Knowledge** | reading sign: tracks, ice colour, blaze marks, squaw wood. `examine` is the tutor |
| **Risk** | thin ice, overflow, the cornice, the climb — always telegraphed, never random |

**The anti-easy rule.** Nothing usable lies loose on the surface anywhere in the valley except what the
crash itself scattered (which is already priced). Everything else is under snow, inside ice, up a tree,
behind a blaze you have to follow, or 2.4 km away. Fair, not generous: every hazard telegraphs, every
gate has at least two openings, `examine` always pays.

### 4.4 The regions

| Region | Zones | What it is for | From the wreck |
|---|---|---|---|
| **S1 The Crash Site** | 9 ✅ | the wreck: the kit, the ELT, the chart, the pilot; the stay-and-signal anchor | — |
| **S2 The Muskeg** | 5 📐 | the frozen bog the pilot almost cleared: the snow-travel tutorial, a tinder and forage trickle, the gate to the lake | 120–420 m W |
| **S3 The Lake** | 6 📐 | the visual-rescue stage, the wind's kingdom, the ice-hazard curriculum, the one place the world can see you | 500 m W |
| **S4 The North Wood** | 6 📐 | the survival economy's heart: fuel, shelter, protein, the forward camp, the free warmth floor | 60–260 m N |
| **S5 The Strike Path** | 4 📐 | the crash rewound — salvage, orientation, and one genuinely dangerous liquid | 110–330 m NE |
| **S6 The Ridge Overlook** | 4 📐 | elevation: the radio/beacon route's scarce resource, the map's reveal, the honest exposure math | 800 m NE, +120 m |
| **S7 The Birch Stand** | 4 📐 | the fire-craft chapter: ignition, ember-craft, reading trees | 350 m E |
| **S8 The Creek** | 5 📐 | the travel corridor and the water chapter: liquid water, fish, willow, the overflow toll gate | 0.8–1.1 km SW→SE |
| **S9 The Beaver Pond** | 5 📐 | another engineer's infrastructure to reuse, wire to salvage, a larder to misunderstand, the trailhead | 1.7 km S |
| **S10 The Trapline** | 4 📐 | Holt's commute: the storm-safe route, the navigation tutorial, the quietest storytelling | 1.7–2.4 km SE |
| **S11 Holt's Homestead** | 7 📐 | the second dense node: the endgame shelter, the material payoff, a portrait of its absent owner | 2.4 km SE |

### 4.5 The fifty-nine zones

✅ = built in `zones.py` today · 📐 = designed as a document, not built.

**S1 — The Crash Site** *(built; the wider world adds only outward edges and glimpses — no interior
redesign)*

| Zone | What it is for | Status |
|---|---|---|
| `cockpit` | the panel, the radio set, the dying pilot; the wire prize behind the panel | ✅ |
| `mid_cabin` | the crafting heart: seats as a parts-machine, the tool caches, the luggage | ✅ |
| `rear_cabin` | the torn hull: indoor snow, the engine-cover warmth prize, the draft to block | ✅ |
| `outside_nose` | the nose in the drift; the wings' fuel; the cowling that becomes the party's first sled | ✅ |
| `fuselage_top` | the watchtower: the sheared antenna base, the valley's sightlines, the worst exposure on site | ✅ |
| `outside_tail` | the breach exit — the hub between hull, scar and treeline | ✅ |
| `debris_trail` | the scatter: the torn survival duffel, the drift-buried hatchet, the mail sack | ✅ |
| `tail_section` | the expedition cache: the ELT screaming into a sheared antenna, snowshoes, the avgas-soaked bag | ✅ |
| `treeline` | the supply room and the forest gateway: deadfall, boughs, dry grass | ✅ |

**S2 — The Muskeg**

| Zone | What it is for | Status |
|---|---|---|
| `tussock_flat` | cottongrass tinder and frozen cranberries at ankle height; hurrying wrenches an ankle | 📐 |
| `labrador_thicket` | kindling in quantity and the hot-drink plant: kindling is free, an armload costs | 📐 |
| `tamarack_island` | bone-dry dead limbs, the best easy fuel west of the treeline; the ravens teach that tracks point at calories | 📐 |
| `drifted_channel` | the snow-travel tuition zone: thigh-deep drift, no resources, a probe finds the dry line | 📐 |
| `lake_gate_willows` | withes for lashings and the first hare runs to snare; the gate to the lake | 📐 |

**S3 — The Lake**

| Zone | What it is for | Status |
|---|---|---|
| `shore_apron` | the lake's honest zone: the drift log (a season of fuel behind a saw) and blue melt-ice; no hazards, deliberately | 📐 |
| `ice_flat` | the visual route's stage — visibility is the resource, wind is the bill; the map's most dangerous room in a whiteout | 📐 |
| `pressure_ridge` | the free windbreak mid-crossing and the cleanest blue ice: cross via the ridge, not the short line | 📐 |
| `inlet_mouth` | the ice curriculum in three telegraphs — and the north's liquid water at the shore lead | 📐 |
| `outlet_narrows` | running water heard before it is seen: the discovery chain south, gated by current-thinned ice | 📐 |
| `far_shore_burn` | the fuel jackpot 1.5 km across open ice: the greed test | 📐 |

**S4 — The North Wood**

| Zone | What it is for | Status |
|---|---|---|
| `forest_edge` | green boughs for bedding, thatch and white signal smoke; the wood's first tracks | 📐 |
| `big_spruce_hollow` | squaw wood — the always-dry fire starter — and the forward camp of the dense core | 📐 |
| `deadfall_tangle` | the near fuel mother-lode, tool-priced, under a named widow-maker | 📐 |
| `grouse_thicket` | tame protein you must approach slowly and throw at | 📐 |
| `hare_runs` | the snare line: the best protein per effort, gated on wire and on reading which runs are fresh | 📐 |
| `tree_well_hollow` | the no-materials warmth floor given terrain: the night you survive on boughs and body heat | 📐 |

**S5 — The Strike Path**

| Zone | What it is for | Status |
|---|---|---|
| `shear_line` | the crash pre-cut a shelter's worth of boughs; the scar as an arrow back up the hill | 📐 |
| `wing_in_the_trees` | avgas in the tip tank: the valley's accelerant and its most dangerous convenience, three ways to reach it | 📐 |
| `gear_gouge` | the tire — black smoke, the one column that reads as man-made against snow | 📐 |
| `bench_saddle` | the mid-station where the climb's cost becomes informed consent | 📐 |

**S6 — The Ridge Overlook**

| Zone | What it is for | Status |
|---|---|---|
| `krummholz_band` | the driest small fuel on the map, kept in the worst place to need it; the staging shelf | 📐 |
| `boulder_field` | the survey cairn (a fixed point on the chart) and dry stakes; hollow talus underfoot | 📐 |
| `the_knob` | elevation: the cabin discovered, the weather read a band early, the radio/beacon multiplier | 📐 |
| `lee_cornice` | the shortcut that isn't — a roof over air; the map's one deliberately lethal opt-in | 📐 |

**S7 — The Birch Stand**

| Zone | What it is for | Status |
|---|---|---|
| `aspen_fringe` | push-over poles and punk wood: the ember you can carry | 📐 |
| `birch_grove` | bark in three grades: fire that starts wet | 📐 |
| `chaga_tree` | the spark-catching fungus ten feet up — lighterless insurance, and the reward for looking up | 📐 |
| `game_trail_crossing` | the shed antler (premium tool stock) and the moose bed's heat lesson; the owner stays offstage | 📐 |

**S8 — The Creek**

| Zone | What it is for | Status |
|---|---|---|
| `outlet_riffle` | free-running water: a full container without burning a stick, priced in wet-boot risk | 📐 |
| `gravel_bar_willows` | willow in sled-load quantity, and ptarmigan that are visible only when they move | 📐 |
| `overflow_bend` | the southern toll gate: water atop the ice under dry powder — three telegraphs and a probe | 📐 |
| `logjam_crossing` | the only dry crossing and the southern fuel depot, over booby-trapped voids | 📐 |
| `confluence_pool` | the fishery: the longest chain on the map and the one calorie source that scales | 📐 |

**S9 — The Beaver Pond**

| Zone | What it is for | Status |
|---|---|---|
| `dam_crossing` | the causeway to the trapline side, and pre-cut poles you *could* pull from the working face | 📐 |
| `pond_flat` | the bubble-trails: wonder that doubles as a map of who lives here | 📐 |
| `the_lodge` | the shelter chapter taught by a rodent — mass + insulation + bodies = a livable core at −20 °C | 📐 |
| `food_cache_margin` | the ethical harvest (green poles without touching the dam) and the green-wood lesson | 📐 |
| `drowned_set` | snare wire in yards, free of the plane; the first human sign beyond the wreck | 📐 |

**S10 — The Trapline**

| Zone | What it is for | Status |
|---|---|---|
| `blaze_gateway` | the navigation tutorial: each blaze visible from the last. It installs a skill and holds no loot | 📐 |
| `spruce_tunnel` | sheltered for its whole length: the only long move that stays cheap in heavy weather | 📐 |
| `marten_set_tree` | a fur scrap behind a chain of small gates; Holt's craft, read a second time | 📐 |
| `cabin_gate` | the threshold beat: hope, correction, and a door anyway | 📐 |

**S11 — Holt's Homestead**

| Zone | What it is for | Status |
|---|---|---|
| `dooryard` | the yard's buried infrastructure and the dog-run cable; the note before the note | 📐 |
| `porch` | the drift dune: dig it bare-handed and soak your layers, or ten minutes with the shed's shovel | 📐 |
| `cabin_interior` | the stove — shelter's endgame — with the first move pre-paid: laid kindling and a match tin | 📐 |
| `loft` | the wool jackpot in a cedar trunk, and the photograph that names the absent man's reason | 📐 |
| `cache` | ten feet of air as a puzzle: snowshoes, the felling axe and food, behind a ladder stashed under the cabin | 📐 |
| `woodshed` | a winter of split dry wood 2.4 km from where it is needed; the freight sled with a split runner | 📐 |
| `water_hole_path` | Holt's water infrastructure: bucket-water without the riffle's risks | 📐 |

### 4.6 Travel is the price tag *(proposal — `map.md` §3)*

Unbroken snow is the tyrant: knee-deep trail-breaking moves at ~1.5 km/h and costs sweat. Your own
broken trail is twice as fast — until the storm refills it. Creek ice is a highway with a toll
(overflow). Snowshoes, in Holt's cache, roughly double open-country speed — which is why the mobility
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
| lake crossing to the burn | 25 min | — (wind erases the trail) | 15 min |

Against a five-hour light budget the homestead is a **commitment**: the first trip eats half the usable
day, round trip. That is the stay-or-go tension, made of minutes instead of dialogue.

### 4.7 The four routes, as room itineraries *(proposal — `report.md` §2)*

No two routes compete for their key resource; every route crosses the shared survival economy.

| Route | Rooms | Its distinct scarce resource |
|---|---|---|
| **Stay-and-signal** | crash site, `ice_flat`, `gear_gouge`, the north wood's fuel zones | fuel logistics + wind engineering |
| **Beacon (the ELT)** | `tail_section` (the ELT), the cockpit's wiring or the dooryard's cable, `fuselage_top` or `the_knob` | conductor + elevation |
| **Radio (the deep puzzle)** | the cockpit set, the wreck's batteries, `the_knob` | carry logistics + weather windows |
| **Travel / shelter** | the creek run, the trapline, the homestead | navigation skill + daylight |

### 4.8 The economies the routes spend from *(proposal — `report.md` §3)*

Each is a crude-to-mastery arc, and each is a network of rooms rather than a stat:

- **Fuel** — squaw wood (starter) → dwarf birch and krummholz twigs (kindling, priced in armloads) →
  deadfall and the logjam (bulk, tool-priced) → the drift log, the far burn, the woodshed (jackpots,
  distance- and tool-priced). Fire is always possible; scale is always earned.
- **Water** — melt (anywhere, plus a fuel tax) → blue ice (efficiency) → the inlet's shore lead (north,
  nerve-priced) → the riffle and Holt's water hole (south, travel-priced).
- **Food** — rations (finite) → cranberries and rose hips (a trickle) → grouse and ptarmigan (skill
  shots) → snare lines (planning + wire) → the fishery (the source that scales) → the cabin's stores
  (the depot, farthest away). Calories scale with commitment, never with luck.
- **Warmth and clothing** — crash clothing → the pilot's jacket → covers and blankets → marten fur →
  the loft trunk; plus the terrain layer, where *where you work* is itself a clothing decision.
- **Mobility and hauling** — boots → the cowling drag (hour one) → your own broken trails → the game
  trails, the causeway and the tunnel (the world's own roads) → snowshoes → the repaired freight sled.
- **Fire-craft** — lighter → squaw wood → birch bark (a weatherproof start) → punk-cupped embers
  (portable flame) → chaga and a spark (lighterless insurance) → avgas (a dangerous shortcut).
- **Information** — the chart, the manual's pages, the pilot's line, the knob, the blaze protocol,
  ice-reading, track-reading. The only massless economy, which is why the knob — pure information —
  justifies the map's hardest climb.

### 4.9 How the world teaches, and how the party finds it *(proposal — `report.md` §4/§6, `map.md` §4)*

No region is announced; each is discovered at least two independent ways, so a party that misses a clue
is never locked out. The cabin is found by the chart, or from the knob's line of sight, or by the blaze
at the drowned set, or from the pilot's last lucid line. The lake is visible as sky-glare west from the
fuselage top, and the muskeg simply opens onto it. The ridge is pointed at by the plane's own gouge.
Open water at the outlet is **audible** before it is visible.

The knowledge currency is paid back the same way every time: a cheap tutorial zone, a zone where the
lesson pays, and an exam — usually the tutorial's own room revisited at night or in the storm. The
drifted channel teaches snow; the inlet teaches ice; the overflow bend teaches overflow; the blaze
gateway teaches the trail the near-whiteout will later test closed-book. Behind every knowledge price
stands an in-game teacher, and most of them are **the survival manual**: its eight read-pages (fire,
water, shelter, signals, food, fishing, SAR/ELT, exposure) are therefore first-class content, ranked
equal with the zone looks, under one authoring rule — the manual may simplify, but it must never lie.

### 4.10 The storm re-prices the map *(proposal — `map.md` §5, applying GDD §8)*

Each weather phase doesn't just dim the world, it changes what things cost:

1. **Light snow** — the whole map is open. Scouting is cheap; the far burn and the ridge are
   affordable. Everything learned now (broken trails, blaze positions) is capital for later.
2. **Steady** — sight-bands tighten a step; the search plane's pass happens somewhere in here, over the
   lake line, following the drainage as real search pilots do. You are either ready with smoke on the
   ice, or you eat the near-miss.
3. **Heavy** — open country turns hostile: the lake crossing and the knob become gambles, and your
   morning trail is filling in. The sheltered routes (the spruce tunnel, the creek under its banks)
   keep working.
4. **Near-whiteout** — navigation collapses to handrails: the creek, the blazes, a rope line you
   rigged, the wind's one constant direction. Zones shrink to arm's length.
5. **Night (−20 °C)** — the world is three lit rooms: a fire you built, the fuselage huddle, or Holt's
   stove. Everything else is a mistake.

Every timed beat is a **world** event, never a silent no-op: the search plane's drone is audible in
every exterior zone with a bearing, so the party a day's walk south *hears* what its allocation cost;
the heavy-band radio crackle reaches whoever carries the handheld, wherever they are; and once, deep in
the storm night, the overcast tears open for a few minutes and the north gets the aurora — beauty
honestly priced, because clearing skies mean plunging cold.

### 4.11 The density gradient *(proposal — `map.md` §6, honouring GDD §6)*

GDD §6 gives the dense scene the whole data budget. The map keeps that promise across a big valley by
spending unevenly on purpose:

- **Ring 0** — the crash site and the big-spruce forward camp: modelled to the hilt.
- **Ring 1** — muskeg, strike path, birch stand, near creek: full interaction, leaner object counts.
- **Ring 2** — lake, ridge, pond, trapline: purposeful terrain. Each zone exists for one decision, one
  resource, one hazard, one story beat.
- **The homestead** — the second dense node; it is the "cabin + camp" of the endgame.

The object census (`objects.md`) scoped the authoring bill behind this: **~1,150 candidate objects,
ambients and signs across the valley**, excluding what is already built at the crash site, with Ring-0
and homestead zones keeping most of their census and Ring-2 zones keeping the load-bearing half. The
census also flagged what the material table still lacks for any of this to be buildable — **rock and
stone are absent today**, along with bone/antler, fur/hide, punk wood, rubber, kerosene, canvas,
rawhide, grease, brass and paper — and it distinguishes fifteen-odd snow and ice sub-types (powder,
wind-slab, drift, sastrugi, rime, hoarfrost, black ice, shore ice, overflow, frazil…), each of which
wants its own behaviour note. Those are doc 18's to settle; they are named here because the valley
cannot be built without them.

### 4.12 What the valley is about

One story is told by every room regardless of route order: **the crash is not the first thing that ever
happened here.** Ravens already commute to the wreck; the burn already regrew; the beavers already
solved winter; a surveyor already measured the ridge; Holt already blazed the way out and left his door
unlocked and his kindling laid. The emotional argument is competence-before-you and
indifference-without-malice — which is the argument that the players' own competence is possible.

---

## 5. Interactions

**This document depends on:**

- **06 (time, sleep and the clock)** — travel minutes and work durations are meaningless without the
  running clock and the activity model; the whole map is priced in minutes.
- **08 (warmth, clothing and shelter)** — every zone carries an authored exposure band
  (`sheltered` < `broken` < `open` < `brutal`); the bands are inert until warmth drain exists.
- **13 (events, escalation and weather)** — the storm ladder is what re-prices the map; the search
  plane, the radio crackle and the aurora are its beats.
- **18 (materials and forms)** — the census's missing materials (stone above all) gate the build.
- **05 (ontology and sufficiency)** and **17 (rooms and living rooms)** — individuation, the prose
  style, and the state a room remembers.
- **19 (multiplayer and instances)** — sight and sound across zones is what makes a split party work:
  voices carry zones, not kilometres; the knob sees everything; smoke reads for miles.

**These depend on this document:**

- **14 (rescue paths)** — the four routes *are* the four regions; the walk-out's geography is here.
- **10 (food and hunger)**, **09 (water)**, **07 (fire and shaping)** — every economy's sources are
  zones on this map.
- **02 (the experience)** — the sample week walks this map.
- **22 (the world-building loops)** — the build queue is this document's fifty zones in build order.

---

## 6. Open questions

1. **Is the valley the right size?** Fifty outdoor zones over roughly four kilometres of country —
   the far-shore burn 1.5 km west across the ice, the homestead 2.4 km of travel southeast, ~90 minutes
   away the first time. *Options:* (a) keep the fifty as designed; (b) trim Ring 2 to the
   zones that carry a route or an economy (roughly 35 outdoor zones); (c) grow it. **Recommendation:**
   keep the fifty — you decided the whole valley ships in the first complete run — but judge the *size*
   by the travel table in §4.6 rather than by the zone count, because a week-long run makes distance
   much cheaper than the table's one-day assumptions imply (see question 3).

2. **Which regions earn their place?** Tested by "does this region anchor a route or an economy, and is
   there a reason to go back a second time?", the strongest are the lake, the north wood, the ridge, the
   creek and the homestead. The two weakest are **the muskeg** (a five-zone tutorial corridor whose
   material payoff is a calorie trickle and some willow) and **the birch stand** (a fire-craft chapter
   that a party usually reaches *after* it has solved fire). *Options:* (a) keep all eleven; (b) fold
   the muskeg into the lake approach at two zones; (c) keep both, but give each a second-visit reason.
   **Recommendation:** (c) — the muskeg is the road west and the road west gets walked every day
   anyway; the birch stand needs a reason that survives the lighter (ember transport is one, and it is
   already there). If you want a cut, the muskeg is the cut.

3. **A one-day map under a week-long run.** The map, the travel table and the storm phases were all
   designed against a single five-hour day (`report.md` opens "a session is ~5 hours of daylight plus
   the storm night"). Your 2026-09-07 decision made the run **roughly a week**. Over a week, the
   homestead stops being a gamble and becomes day two, and the "stay or go" argument the map is built
   around loses most of its pressure. *Options:* (a) re-price the map for a week (distances get longer
   or the ladder gets meaner); (b) keep the day-scale pricing and let the week be repeating days, each
   worse than the last; (c) let the escalation ladder carry it — the party can reach everything by day
   three, but by then the weather, the food and the injuries decide whether they can *use* it.
   **Recommendation:** (c), and doc 13 owns the ladder that makes it true. This is the biggest
   unresolved tension in the world design and it should be settled before any outdoor zone is built.

4. **The four routes.** Each is anchored in its own region on its own scarce resource. But "travel /
   shelter" is not rescue — reaching Holt's cabin means you *outlast*, it does not mean anyone comes.
   *Options:* (a) keep it as a fourth rescue route; (b) rename it what it is (an outlast path) and
   require it to convert into rescue by some other channel; (c) make the cabin a rescue channel in its
   own right (Holt's own gear, a second radio, a route out). **Recommendation:** (b) — doc 14 owns the
   conversion; the world is happy either way.

5. **The walk-out.** You said the walk-out is in the first complete run, but the fifty zones end at the
   homestead: no zone leads out of the valley. *Options:* (a) the walk *to the cabin* is the walk-out,
   and the ending is "shelter secured, storm outlasted"; (b) a further chain of zones beyond the
   homestead (the river, a road, a village) — new design that grows the fifty; (c) the walk-out is
   narrated off-map once the party has snowshoes, food and a working navigation plan.
   **Recommendation:** (a) with (c) as the ending text — otherwise the map needs a twelfth region.

6. **The density gradient.** Ring 2 keeps "the load-bearing half" of its object census. *Options:* (a)
   keep the gradient with a per-ring quota; (b) keep the gradient as *authoring order* only, and let
   evidence decide — build what players and probes actually reach for, in ring order.
   **Recommendation:** (b). A quota contradicts the open-world rule; ring order is a priority, not a
   ceiling.

7. **The fauna, after December.** You decided no bear — wolves and a wolverine. The July zones cast
   ravens, spruce grouse, hare, ptarmigan, marten, an offstage moose and the beavers; no wolverine
   appears anywhere in the fifty, and the only wolf is a single trot-line of tracks crossing the lake
   ice in the object census. *Options:* (a) put them in the world as *sign* (wolf
   trot-lines crossing the lake ice, a wolverine's raids on the cache and on snare lines) and leave the
   encounters to doc 13; (b) design them as full presences here; (c) leave them entirely to events.
   **Recommendation:** (a) — sign in the world, pressure in the event ladder. A wolverine that robs
   snares is a systems antagonist the economy already has a slot for.

8. **The one lethal opt-in.** The lee cornice is designed as the map's single deliberately lethal place,
   and there is no lethal-consent gate. The sources telegraph it three ways but never say what
   happens. *Options:* (a) a fall that kills; (b) a fall that buries and injures, so the party fights
   the cold clock for a rescue; (c) survivable but crippling. **Recommendation:** (b) — it keeps the
   physics honest, keeps the party playing, and makes the one lethal zone a co-op emergency rather than
   an execution. Doc 11 prices the injury.

9. **Sweat as its own currency.** The six currencies treat sweat as separate from warmth. *Options:*
   (a) keep six for design talk and implement it as wetness inside the warmth system; (b) collapse to
   five. **Recommendation:** (a) — the deferred-debt shape is the point of naming it, and doc 08 owns
   the implementation.

---

## 7. Review log

| Date | Decided | Cut | Sent back |
|---|---|---|---|
| — | *(awaiting the review with Andrew)* | | |

---

## 8. What exists today

**Built** — nine zones, all at the crash site, in `game/world/scenarios/whiteout/zones.py`: `cockpit`,
`mid_cabin`, `rear_cabin`, `outside_nose`, `fuselage_top`, `outside_tail`, `debris_trail`,
`tail_section`, `treeline`. Each has a position, edges (walk/see), terrain tags and a survey line;
each has authored spaces in `game/world/scenarios/whiteout/spaces.py` and objects in
`objects.py` / `objects/`; each has an official room document with its real-world ontology census and
gap list under `docs/scenarios/whiteout/rooms/` (nine files, one per zone); the probe corpus
(`game/world/scenarios/whiteout/probes/`) is drawn from those censuses and names those nine zones and
no others. The crash-site content
includes the ELT, the sectional chart naming V. Holt's cabin, the scattered survival kit, the snapped
hatchet and the soaked matchbox.

**Designed, not built** — the fifty outdoor zones. They exist as documents only:
`docs/investigation/world/rooms.md` (every zone's look, resources, prices, hazards, story),
`map.md` (geography, travel pricing, the currencies, the density gradient), `report.md` (how the rooms
are used in play, plus the three assessment sweeps), `objects.md` (the ~1,150-object census). No
outdoor zone id appears anywhere under `game/` — verified. The build order for all fifty is
`docs/investigation/world/build-queue.md`, which is gated behind a foundation phase whose last box
(live verification of the nine crash rooms) is still open, and behind the closure loop's clusters.

**Nothing yet** — the ontology store `docs/ontology/` does not exist. Nor does any of the machinery the
outdoor world assumes: travel durations, exposure/warmth drain, weather bands, hazard triggers,
forage/snare/fish operations, track persistence and decay, the timed-beat scheduler. `report.md` §9-D
enumerates the ten operations the map assumes (`probe` — the map's signature verb — plus `climb`,
`throw`, `drag/haul`, snare-setting, `fish`, and the rest), each with the degraded behaviour that keeps
its zone playable until the operation ships.

**One known discrepancy to fix.** The built crash-site content still carries the pre-206 airliner
fiction: `objects.py` defines a "forward overhead bin" and an "aft overhead bin", and seats identified
as `11B` and `12C`. Your 2026-09-16 decision is the honest 206 interior — a hat shelf, a netted cargo
bay and a jammed cargo door, with seats 1A/1B/2A/2B plus the right seat. The re-skin is small (names,
aliases and prose; a `cargo net` object already exists) and belongs to the next crash-site pass.
