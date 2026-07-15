# The object inventory — every room, everything in it

> **Status: SCRATCHPAD (investigation) — 2026-07-15 overnight design run.** The per-zone
> object census Andrew asked for: for every room, as many objects as possible — snow,
> breeze, rock, whatever — to feed the eventual flesh-out (§43 packets, the appearance
> registry, the materials table). Companions: [`map.md`](map.md) · [`rooms.md`](rooms.md)
> · [`report.md`](report.md).
>
> **How to read it.** Five lines per zone: **Terrain & fixtures** (the big immovables) ·
> **Harvest & loose** (takeable/workable as found) · **Hidden / contained / buried**
> (earned by dig/search/open/climb/pry — the DR-24 layer) · **Ambient** (air, light,
> sound, smell — perceivable, mostly untakeable, all addressable: the examine-rich layer)
> · **Sign & trace** (fauna/flora/human evidence — the knowledge economy's raw text).
> Everything listed is a CANDIDATE: the census errs generous on purpose; the content
> pass prunes against the density gradient (map.md §6). New-material needs are collected
> at the end.
>
> Snow and ice are never one object: the census distinguishes powder, wind-slab, drift,
> spindrift, sugar snow (depth hoar), snow-caps, rime, hoarfrost, black ice, white ice,
> overflow, shore ice, pressure slab, frazil, icicles — the variety IS the ontology
> exercise, and each behaves differently under the material table.

---

## S1 — The Crash Site (additions beyond build.py's ~40 built objects)

### cockpit
**Terrain & fixtures:** instrument panel (crazed gauges individually: airspeed, altimeter, fuel, oil temp), yoke (bent), rudder pedals, pilot seat (frame sprung), windscreen shards in frame, magnetic compass (whiskey compass, fluid frozen — reads true, story-tool), circuit-breaker rows, throttle/mixture knobs, cabin-heat lever (cruel joke, authored), sun visor, door pillar.
**Harvest & loose:** chart pencil, kneeboard clip, headset (one earcup crushed, cord = wire), checklist card, seat-rail bolts, broken toggle switches, instrument glass discs.
**Hidden / contained / buried:** behind-panel wiring loom (the wire prize, pry-gated), map pocket (spare fuses, a candy bar wrapper — empty, story), under-seat survival mirror (signal mirror — the visual route's pocket ace), defrost duct hose.
**Ambient:** cold-metal smell, faint avgas whiff, wind keening through the windscreen hole, frost feathers on every glass face, blue morning light through crazing, the compass card's slow wobble.
**Sign & trace:** blood smear on the yoke (the pilot's), scuffed rudder pedal ice, a thumb-worn shine on the throttle knob (a man who flew this plane for years).

### mid_cabin
**Terrain & fixtures:** seat rows 11A–12C (frames, tracks, armrests), overhead rack rails, cabin windows (two starred, one popped), floor tie-down rings, headliner (torn, batting exposed — DR-24 wall salvage), bulkhead placards.
**Harvest & loose:** seat cushions/covers/belts (built), scattered magazines, an airsickness bag, a child's crayon (mail-letter rhyme, story), luggage straps, a shoe (one), seat-pocket safety cards.
**Hidden / contained / buried:** under-seat penknife (11B, planned DR-24b), under-seat mitten (12C, planned), boarding pass in 11B's cover (planned reveal-by-removal), floor-track debris (coins, a hair clip, a AA battery), life-vest pouches under seats (vests: fabric/straps/whistle! — the whistle is a signal object).
**Ambient:** snow sifting at the tear, luggage-leather smell, the hull's tick and groan in gusts, dim slatted light, breath-fog hanging.
**Sign & trace:** impact scatter pattern (everything thrown forward-left — physics as narration), frost growing on the aisle carpet.

### rear_cabin
**Terrain & fixtures:** cargo net mounts, hull tear (the breach — edges: torn aluminium, sharp), floor D-rings, aft bulkhead (buckled).
**Harvest & loose:** cargo straps, bungee cords, a tarp corner (torn free), mail sack (built), loose envelopes, twine bundles.
**Hidden / contained / buried:** between-frames void (a rolling flashlight — dead, bulb good; battery corrosion puzzle), under-floor inspection hatch (control cables, a spare cotter-pin tin).
**Ambient:** the gust-driven snow-sift, flapping envelope corner, the tear's harmonica moan at certain wind angles (authored sound event), diesel-y hydraulic smell.
**Sign & trace:** drag marks where the tail tore away, mail postmarks (villages upriver — the world beyond, story).

### outside_nose
**Terrain & fixtures:** crumpled nose cone, propeller (one blade bent back, one buried), engine cowling (the drag-toboggan donor), nose gear collapsed under, drift bank against the hull.
**Harvest & loose:** cowling fasteners, prop-tip fragment, oil-stained snow (contaminated — the melt-water lesson), blown-out landing-light lens + bulb + reflector (the reflector: fire-by-sun lore flag, signal aid).
**Hidden / contained / buried:** engine bay via sprung cowling gap (dipstick, oil filler, battery! — heavy, the radio route's power option, 12kg arithmetic), exhaust stubs (steel tube).
**Ambient:** engine-oil smell, ticking of cooling metal long gone silent (authored as absence), drift's smooth wind-carved flank, spindrift running off the cone.
**Sign & trace:** the prop's single strike-gouge in frozen ground (it wasn't turning hard — story detail: engine had already died).

### fuselage_top
**Terrain & fixtures:** aluminium spine, antenna base (torn, cable stub — ELT route), rivet lines, VOR blade (bent flat).
**Harvest & loose:** antenna cable stub (conductor), a static wick, loose rivets in a seam.
**Hidden / contained / buried:** none — the zone is a lookout, not a locker (design intent).
**Ambient:** full wind (brutal band), rime on the windward skin, the whole valley's soundscape unmuffled, sun-glare or spindrift by band, the metal's hum in gusts.
**Sign & trace:** boot-scuffs in rime (yours — the map's first own-trace mirror), the skin's oil-canning dents underfoot.

### outside_tail / debris_trail / tail_section / treeline
(Existing builds carry these; census adds:) heavier gauge scatter along the trail — hull rib sections, window frame, insulation batts (snagged on stubs, wind-strewn), a wheel chock, cargo-door hinge half; treeline adds: first spruces (bough/pitch/squaw-wood bearing), snow-caps on boughs (dumpable — the cold shower gag that teaches canopy snow), a wind-tipped leaner to push over (starter deadfall), snowshoe-hare crossing tracks (the FIRST sign object, pointing north into the wood), raven flyover + kronk (ambient, points at the tamarack cache), the wreck-glint view SW (glimpse object).

---

## S2 — The Muskeg

### tussock_flat
**Terrain & fixtures:** the tussock field itself (hundreds, individually steppable/examinable as a class), frozen bog surface beneath, a lone bleached snag pole (old, leanable — probe donor), the lake-glare horizon line W.
**Harvest & loose:** cottongrass seed-heads (tinder), dead sedge stems (poor kindling, abundant), tussock grass wads (boot insulation — the dry-grass-in-boots trick, manual EXPOSURE page).
**Hidden / contained / buried:** cranberries at tussock bases (dig), a snow-buried ptarmigan roost hollow (flushes if stepped — startle event + a feather), frost-cracked bog surface plates (pryable peat slabs — burns poorly wet, dries slow: the peat lesson, LATER-flag).
**Ambient:** the one long wind vowel, ground-blizzard streamers at boot height, flat white light (contrast-killing — the whiteout preview), the squeak of cold powder underfoot, distant raven pair.
**Sign & trace:** vole tunnels collapsed in lines (the under-snow world), fox trot-line stitching tussock to tussock (a hunter's straight commute — contrast with hare panic-loops: track grammar), wind-scalloped sastrugi rims.

### labrador_thicket
**Terrain & fixtures:** the brush stand (dwarf birch + labrador tea as harvestable classes), one granite erratic boulder (waist-high — windbreak, anvil stone, landmark).
**Harvest & loose:** labrador-tea leaves (rusty-backed, aromatic when crushed — the crush-and-sniff identify), dwarf-birch twig bundles, dead brush stems, the boulder's exfoliated flakes (crude scraper stock).
**Hidden / contained / buried:** under-boulder cavity (an old fox cache: bones, a frozen vole — grim, story, bait stock), snow-pillowed brush pockets (grouse sometimes — flush event).
**Ambient:** wind combing the brush tops (a dry rattling), the crushed-leaf resin smell, snow-caps on every twig fork, chickadee dee-dee-dee (life persisting — morale ambient).
**Sign & trace:** hare browse line (nipped twig angles — 45° clean cut = hare, ragged = moose: the browse forensics lesson), fox scat on the boulder top (marking — the country is owned).

### tamarack_island
**Terrain & fixtures:** the tamarack (climbable lower whorls, dead-limb skirt), the rise itself (dry ground under snow — camp-grade, flag), a second fallen tamarack (log seat / fuel).
**Harvest & loose:** dead limbs (premium dry small fuel), tamarack twig tips, bark plates (kindling), cone litter under snow.
**Hidden / contained / buried:** the ravens' dig (the flung mail bundle — story), a woodpecker-drilled limb (grubs frozen in galleries — survival protein, stomach-gated, real), the rise's dry duff layer under snow (fire-base material).
**Ambient:** raven pair overhead (kronk, wing-whuff — audible before visible: the sound-first design showcase), the tree's creak, needle-less winter silhouette lattice light.
**Sign & trace:** raven tracks + wing-brush marks at the dig, ancient axe stump on the rise (someone cut here decades ago — the country's long memory, pre-Holt).

### drifted_channel
**Terrain & fixtures:** the drift body (deep, wind-packed lid over sugar snow — the two-layer trap), the old slough's cutbank line (the firm crossing, probe-findable), one drowned willow clump tips showing.
**Harvest & loose:** willow tips (meager withes), the drift's wind-slab surface (snow-block quarry #2 — closer than the lake, smaller blocks).
**Hidden / contained / buried:** under-drift slough ice (black, air-pocketed — hollow knock), a snow-buried fuel jug (BLOWN FROM THE PLANE — the debris field's westernmost orphan: half-gallon of avgas, cracked cap, quarter left; the "how did that get HERE" find that teaches debris-scatter logic).
**Ambient:** spindrift snakes crossing the lid, the hollow drum note over pockets, wind-sculpted cornice-lets along the cutbank.
**Sign & trace:** a moose's old post-holed crossing (thigh-deep holes, frozen — even the big ones pay the toll here: the price telegraphed by a better athlete), your own first crossing's flounder-pit (the map's most honest mirror).

### lake_gate_willows
**Terrain & fixtures:** the willow stand (whip classes by thickness), the shore hinge line (grounded ice begins), a driftwood tangle knot at the high-water line.
**Harvest & loose:** withes (snare/lash/jig grades), dry driftwood sticks, willow bark strips (emergency cordage — inner bark, the two-ply twist, manual page), catkin buds (famine nibble, authored honest: near-zero calories).
**Hidden / contained / buried:** snare-height runs through the stems (the set sites), a preserved wasp gall cluster (tinder curio), under-tangle void (a weathered wooden boat oar — half — the lake's human past, story + paddle-blade tool blank).
**Ambient:** whip-clatter percussion in gusts, hare-run shadow lines raking in low sun, the ice sheet's first long boom rolling in from the W (the lake announcing itself before you step on it — sound as threshold).
**Sign & trace:** fresh hare pellets (green-brown = hours old: freshness forensics), a single lynx round print (the predator that explains the hares' architecture — never seen, always implied), nibble-barked stems in bands.

---

## S3 — The Lake

### shore_apron
**Terrain & fixtures:** the grounded apron (safe class ice), the drift log (the fuel boss), shore gravel in wind-scoured patches, the willows behind (edge reference).
**Harvest & loose:** blue shore-ice chunks (pry), gravel handfuls (fire-base ballast, boiling-stone stock — hot-rock water warming, manual-flagged), driftwood splits off the log's checked end (bare-hand slabs — the log's freebie fringe), frozen spray beads.
**Hidden / contained / buried:** under-log void (dry punky underside + a wasp nest paper sheet — tinder), gravel-frozen fishing lure with rusted treble (the lake's human past #2 — hook salvage).
**Ambient:** ice grumble/boom series (thermal cracking — harmless HERE, teaching the sound), wind at half-throttle (the willows' shadow), long low light lanes W, the burn's black smudge visible on clear bands.
**Sign & trace:** otter slide groove down the bank into a (refrozen) hole (joy as sign — and a former hole = future hole: fishing intel), old fire ring stones under snow at the log's lee (humans have signaled from this shore before — confidence + a ready ring).

### ice_flat
**Terrain & fixtures:** the sheet (wind-burnished, snow-skinned in panes), sastrugi ribs, the wind itself (addressable — always-on force object), shore bearings (the four edges as glimpse objects).
**Harvest & loose:** wind-slab blocks (quarry with long blade/shovel — windbreak/shelter stock), drifted snow-skin (bad water source vs. blue ice — the purity ladder), surface hoar plates on calm mornings (glitter — beauty ambient, also the WORST fire snow: flags the snow-type ontology).
**Hidden / contained / buried:** under-snow old pressure crack (refrozen, safe, but a black seam that TESTS the ice-reading lesson — a false positive to reward probing over panic), a wind-freed weather balloon fragment + mylar streamer frozen in (the outside world's litter — mylar: signal streamer salvage).
**Ambient:** full wind (brutal), ground blizzard at shin height, the sheet's whale-song booms and cracks radiating underfoot (loud HERE — the same sound grammar as the inlet, in safe context), sun dogs on cold clear morning (parhelia — the north's sky jewelry), your shadow at noon pointing the compass (navigation ambient).
**Sign & trace:** wolf trot-line crossing mid-lake, dead straight for the far shore (the country's confidence walking past your caution — story + a proven crossing line the brave may follow), old snowmachine track ghost-ridges (weeks old, drifted — humans DO come through: rescue-plausibility seed).

### pressure_ridge
**Terrain & fixtures:** the ridge (slab classes: tilted, stacked, cathedral), the low south gap (the door), the lee pocket (windbreak room).
**Harvest & loose:** clear blue slabs (the melt-water premium), shatter shards (ice-glass — a cutting curiosity: works once, melts in the hand — authored honesty for the "ice knife" attempt someone WILL make).
**Hidden / contained / buried:** inter-slab caves (bivvy-grade pockets — the mid-lake emergency shelter nobody expects to need), a wind-drifted ptarmigan flock shelter (they burrow the lee too — flush event + the shared-shelter story beat).
**Ambient:** the ridge's active groans (it is still MOVING, slowly — awe + honest warning), wind-shadow quiet in the lee (the contrast object), blue light inside the slab caves.
**Sign & trace:** fresh shear faces (the lake breathes), fox prints threading the gap (everything uses the door — the gap is the valley's advice, printed).

### inlet_mouth
**Terrain & fixtures:** the stained ring (grey slush halo), the dark glass zone (thin class ice), the shore lead (open water strip), the brook's under-ice channel (current object), gravel shore arc (the safe approach).
**Harvest & loose:** the lead's water (the north's liquid — dipper-gated), frazil slush at the lead edge (ice-making in realtime — examine wonder), brook-polished pebbles (smooth boiling-stones).
**Hidden / contained / buried:** under-gravel seep spring (never freezes — the backup draw if the lead skins over: reward for exploring the arc), a silt-frozen moose skull with one antler (the country's dead — story, antler stock #2, grim beauty).
**Ambient:** the drum notes (three-telegraph choir: stain, dark ice, drum), the brook's under-ice gurgle (water audible through the sheet — eerie, load-bearing sound), steam wisp off the lead at dawn bands.
**Sign & trace:** otter feed remains at the lead edge (fish scales, a tail — the lead FEEDS things: fishing intel #2), wing-tip snow-brush of a swooping eagle (something else fishes here too).

### outlet_narrows
**Terrain & fixtures:** the stone pinch (bedrock knuckles — the map's only exposed rock at water level), the snow-free ice tongue (current-thinned class), the west-bank route (the safe way down), the gap's wind funnel.
**Harvest & loose:** frost-shattered rock flakes at the knuckles (scraper/anvil stock), stunted gap-willows (tough withes).
**Hidden / contained / buried:** a bedrock pothole under snow (river-ground stones — perfect boiling stones, geology's gift), wedged flood-log across the pinch (a bridge IF tested — probe exam).
**Ambient:** the funnel wind's whistle keys (pitch rises with weather bands — the gap as barometer, authored), the riffle's chatter arriving from below (the discovery sound), ice-tongue flex creaks.
**Sign & trace:** water-ouzel (dipper) bobbing at the tongue's edge (the bird that walks underwater — wonder object, and where a dipper winters, water stays open: knowledge), old ring-bolt leaded into the knuckle rock (a boat was once winched here — human past #3).

### far_shore_burn
**Terrain & fixtures:** standing dead spruce (snag classes: sound, punky, leaning), fire-hollowed stump chimneys, the burn's edge line (live/dead boundary), deadfall crisscross.
**Harvest & loose:** dry snags (push-over class + saw class), bark-free silver branches (bone-dry kindling in any weather), fire-hardened spike stubs (tool: awl/spike stock), charcoal chunks at old root boles (water-filter lore flag + pigment — the mark-making object: charcoal on aluminium = the message system nobody built yet).
**Hidden / contained / buried:** hollow stump caches (red squirrel middens — cone stores: FOOD, real, small, raidable with the guilt authored), a fire-glazed glass insulator half-buried (a line ran through here once?? no — lightning-fused sand lump [fulgurite]: rarity wonder), under-deadfall grouse roosts.
**Ambient:** the burn's particular silence (no needles to catch wind — a DIFFERENT quiet than the tunnel's: the ontology of silences), woodpecker knock echoes (life in the dead wood), fireweed stalks rattling above snow (the healing signature), black-on-white starkness (the map's strongest visual).
**Sign & trace:** fireweed + willow regrowth in the old heat scars (succession as story), lynx kill-site snow-angel (wing-sweep + blood flecks + hare tufts — the food web's receipts, reading exam).

---

## S4 — The North Wood

### forest_edge
**Terrain & fixtures:** edge spruces (bough-bearing class), the wind-shear line (canopy lean), snow-depth step (shallower inside — visible threshold).
**Harvest & loose:** green boughs (bedding/thatch/smoke), cone litter, dead lower twigs (starter squaw wood — the teaser before the hollow's lesson).
**Hidden / contained / buried:** bough-pillow pockets (dumpable snow-caps), an edge-tree's pitch scar (first pitch, small).
**Ambient:** the wind dropping to rumor (the threshold ambient — the map's most repeated mercy, first felt here), grouse wing-thunder somewhere deeper (invitation sound), needle-sift.
**Sign & trace:** the wreck's glint back S (orientation anchor), hare tracks entering (the commute continues), squirrel cone-shred middens at trunk bases.

### big_spruce_hollow
**Terrain & fixtures:** the six grandfather spruces (each an object: squaw-wood skirt, pitch seams, bough tiers, windward moss), the firm blue-dusk floor, the flat camp shelf, a nurse log (moss-topped, punky).
**Harvest & loose:** squaw wood in armloads (THE resource), pitch globs (amber classes: fresh-soft, aged-hard), bough tiers, nurse-log punk (ember bed stock), old-man's-beard lichen streamers (flash tinder — catches from spark, burns in seconds: the tinder ladder's top rung).
**Hidden / contained / buried:** under-skirt dry cones (stove-grade), a rusted tin cup wedged in a root crotch (someone camped here before — human past #4, and a CUP), boughs concealing a grouse dust-bowl hollow.
**Ambient:** cathedral hush, resin-sweet air, shafted light columns, chickadee flock working through (the wood's citizens), snow-sift ticking down through tiers.
**Sign & trace:** old blaze-like bark scar (natural, a TEST of the blaze lesson — false positive that makes players verify doubles), squirrel highway prints trunk-to-trunk, the cup's decades of patina (date the visitor).

### deadfall_tangle
**Terrain & fixtures:** the crossed trunks (classes: bridge-height, waist, shin), the widow-maker (hung, creaking — the named hazard), root-plate walls (windbreak discs with gravel-and-stone freight), the under-tangle crawl spaces.
**Harvest & loose:** snap-off branch stubs (bare-hand endless), bark slabs (sheeting), root-plate stones (hearth stock), dry trunk-top splits where checks opened (axe-free slab pry points).
**Hidden / contained / buried:** under-trunk voids (a marten's feather-and-bone larder; a preserved winter-kill hare — freezer find, edibility examine-gated), the oldest trunk's hollow core (bone-dry punk cylinder — the ember bank).
**Ambient:** the creak (the widow-maker's metronome — loudens with wind bands: the hazard has a VOLUME), snow-muffled clatter when anything shifts, kinglets seething in the tops.
**Sign & trace:** fresh spruce-splinter scatter (the hang is RECENT — urgency), marten twin-print bounds along a bridge trunk (the arboreal highway), your own barked-shin snow-scuffs (the tangle keeps receipts).

### grouse_thicket
**Terrain & fixtures:** the young-spruce hedge walls, roost branches (droppings-whitened — findable BEFORE the birds: hunt-craft), the dust-bowl clearings (summer relics under snow).
**Harvest & loose:** the grouse themselves (3–5, the huntable class), molted feathers (fletching/insulation/lure), needle-clump browse (what they eat — bait irrelevant, knowledge relevant), straight young-spruce wands (throwing-stick + wand stock).
**Hidden / contained / buried:** snow-roost burrows (grouse dive-bomb INTO powder to sleep — the second, weirder huntable state, dawn-gated + the eruption startle), a roost-tree's base cache of wing feathers (the molt pile).
**Ambient:** wing-thunder flushes, the birds' dumb calm regard (authored personality), croplike clucking, hedge-dimmed light.
**Sign & trace:** droppings piles under roosts (the FIND-them object), wing-drag takeoff fans in snow, tracks like tiny dinosaurs.

### hare_runs
**Terrain & fixtures:** the run network (main lines + branch loops — mappable), form hollows (hare beds under low boughs), the alder/willow stem field.
**Harvest & loose:** withes, alder rounds (smoking-wood flag — alder smoke = fish-cure lore, LATER), shed white fur snags on stems (fur wisps — lure/tinder).
**Hidden / contained / buried:** the forms (a hare AT HOME sometimes — the flush), pellets in freshness grades, a previous owner's rusted snare (STILL SET, empty, half-grown into a stem — Holt's or older: the lesson that snares outlive intent, and free wire #3).
**Ambient:** dusk-and-dawn run traffic (the zone has HOURS — activity schedule as ambient), stem-clatter, the lynx's absence (authored as felt silence — "something owns the night shift").
**Sign & trace:** run freshness grades (the exam), lynx ambush bed at a run crossing (packed oval + long wait marks — the competitor's tactics, readable), blood-fleck memory of an old kill.

### tree_well_hollow
**Terrain & fixtures:** the grandmother spruce (the map's biggest single organism), the well room (needle floor, snow walls, bough roof), the bough door.
**Harvest & loose:** needle duff (dry floor stock + slow-smolder fuel), her dead skirt (a family's worth of squaw wood — the reserve bank), pitch mother-lode seams.
**Hidden / contained / buried:** a previous occupant's layer (compressed old bough bed, a wax-paper twist with three fish hooks and a wine cork — the bivvy has SAVED someone before: hope archaeology), deep-duff warmth (measurably warmer floor — the thermal object).
**Ambient:** the held-breath warmth (air object with a temperature), her trunk's slow deep creak (a different, older voice than the tangle's), total wind-shadow.
**Sign & trace:** the old bed's outline, a carved initial + date grown half-shut in the bark ("R.T. '61" — the valley's guestbook), ermine investigation prints at the door (the landlord checks on tenants).

---

## S5 — The Strike Path

### shear_line
**Terrain & fixtures:** beheaded trunks (fresh-cut class — the crash's stump field), flung crown wreckage (bough mass), the cut's sight-line (the arrow object), sap-bleeding stubs.
**Harvest & loose:** pre-cut boughs in shelter quantity, splintered spar-wood (resin-rich lighterwood — fire premium), crown-top cones (seed-rattle curio), bark shrapnel.
**Hidden / contained / buried:** under-crown voids (a flung cabin-door — THE PLANE'S, torn off at strike: a ready sled-deck/litter/table — the crash's best furniture, buried in green), sap icicles (spruce-sugar curiosity, lickable, authored).
**Ambient:** raw resin sharpness (the wound smell), creak of half-attached tops, the arrow's up-slope pull (composition object — the look aims the player).
**Sign & trace:** the height-consistent shear (physics forensics: altitude + descent angle readable — the crash reconstructible by a thoughtful examine chain, PILOT'S STORY told by trees), squirrels already working the downed cones (the wood wastes nothing).

### wing_in_the_trees
**Terrain & fixtures:** the hung wing (fuel tank, aileron, strut stub, nav-light lens), the carrier spruce (climbable class, iced), the fall-shadow (stained ground zone — the marked hazard), neighbor climb-tree.
**Harvest & loose:** dripped avgas ice-slush (the stained snow — CONTAMINATED class, burnable-slush curiosity), popped rivets, aileron cable end (frayed steel — wire brush stock), the nav lens (red glass — signal color filter, curio).
**Hidden / contained / buried:** the tip tank's remaining avgas (gallons — the prize, triple-gated: climb/fell/rig), wing-root lodged duffel (a passenger's? — NO: the plane flew cargo... a TOOL ROLL flung from the cargo door: wrenches, a hacksaw blade! — the mechanical route's missing teeth, hidden in plain groan range), leaf-spring door hinge in the debris.
**Ambient:** the groan cycle (wind-load metronome — the hazard's voice, banded like the widow-maker), avgas sting, drip-tick on crust ice.
**Sign & trace:** the drip-line blue stain (the teacher), scorch-absence (it DIDN'T burn — the mercy that made the game possible, examine-readable), gray-jay pair already investigating (camp robbers cameo — they'll follow the players' food forever after, authored recurring ambient).

### gear_gouge
**Terrain & fixtures:** the crater (impact bowl), the strut (pry-bar class, pinned), the wheel + tire (the smoke bomb), the hydraulic line coil, frozen spray-arc of thrown earth (dirt over snow — the anomaly object).
**Harvest & loose:** brake-line tube, fittings (threaded stock), bearing grease in the hub (waterproofing/lamp-fat substitute — materials flag), scattered lug bolts, the thrown-earth clods (mineral soil — fire-base premium on snow).
**Hidden / contained / buried:** under-crater the sheared axle stub (steel billet), the tire's inner tube (INTACT — rubber sheet, straps, slingshot lore flag, water-carrier patch stock: the census's sneaky-best multi-tool), crater-wall frozen mud (chinking stock — LATER flag).
**Ambient:** the wrongness ambient (a wheel in a forest — authored dissonance), grease-and-earth smell (the only non-snow smell on the path), crater's wind-eddy quiet.
**Sign & trace:** the bounce-and-drag scar sequence (more crash forensics), ermine den entrance IN the crater wall (the world moves into wreckage within days — story law).

### bench_saddle
**Terrain & fixtures:** the bench shelf, the leaning wind-combed tree line (the anemometer object — permanent wind-direction record: navigation), the up-route and down-view.
**Harvest & loose:** wind-cured dead branches (dry, abundant, LAST fuel before krummholz), a quartz vein knuckle in an outcrop nub (striker-spark rock — flint-and-steel lore flag, examine reward).
**Hidden / contained / buried:** lee-side old wind shelter ring (stacked stones, decades old — climbers before you: the route is proven, the cairn's promise starts here), under-outcrop pika hay cache (a stranger's harvest — LATER-latitude flag; swap: red squirrel midden, safe).
**Ambient:** the wind's first real voice (the audition before the ridge), both worlds visible (valley behind, climb ahead — the decision ambient), cloud shadows running the muskeg below.
**Sign & trace:** the combed trees' unanimous lean (the prevailing story), old stone ring lichen (dating by growth — deep time), your party's whole day readable below (tracks, trails, smoke if any — THE self-audit object, unique on the map).

---

## S6 — The Ridge Overlook

### krummholz_band
**Terrain & fixtures:** the hag-spruce hedges (crawl-shelter class), wind-pruned flag trees, the last-cover line.
**Harvest & loose:** krumm dead-wood (chalk-dry, iron-hard — top-shelf kindling), flag-tree lee moss pads, snow-slab quarry pockets.
**Hidden / contained / buried:** hedge-tunnel voids (ptarmigan again + a wind-mummified hare carcass — sky-burial still-life, bait/fur), under-hedge bare ground pockets (the only snowless earth up high).
**Ambient:** wind in ascending keys, the roar above (the knob audible before visible), cloud-tatter light, spindrift plumes off the boulder field.
**Sign & trace:** every tree a wind-vane (unanimous testimony), ptarmigan burrow-pops, an old weathered wand stub with a rag scrap (a ROUTE MARKER — someone flagged this line: the cairn's second promise).

### boulder_field
**Terrain & fixtures:** the talus (hollow-booming class rocks, ankle gaps), the cairn + benchmark disk (brass, stamped 1958 — the country's coordinates), the safe rib line, the stake bundle.
**Harvest & loose:** survey stakes (straight dry poles), lichen sheets off boulders (black tripe-de-roche — famine-food lore flag + fire-extender), frost-split rock flakes.
**Hidden / contained / buried:** under-talus voids (a rusted tobacco tin under the cairn's base — THE SUMMIT REGISTER: three names, 1958–1974, pencil stub; players may ADD THEIRS — the map's quietest co-op ritual, zero mechanics, pure meaning), marmot-free (winter) burrow mouths (empty — the mountain sleeps).
**Ambient:** the boom-notes underfoot (the talus xylophone — hazard as instrument), wind-scour hiss, the disk's cold brass glint.
**Sign & trace:** the benchmark's stamped elevation (the map GIVEN a number), wand-line remnants toward the knob, generations of lichen on the cairn (built long before the disk).

### the_knob
**Terrain & fixtures:** the bald rock crown, the view (each glimpse a composed object: lake coin, wreck cross, creek seam, THE ROOF), the wind (at full authority), the west weather window.
**Harvest & loose:** nothing — the knob GIVES information and CHARGES warmth; its emptiness is authored (design: the summit is not a container).
**Hidden / contained / buried:** a lightning-scarred crack with a wedged, bleached caribou antler shed (how did it get up here — the mystery object, pure story; also the best antler on the map for the party that earns the summit).
**Ambient:** the lean of the wind (the rewritten line — its whole weight, steadily), radio static opening into voice-ghosts (the §38 ambient), the aurora on ITS night, sun dogs, the storm's western wall visible a band early (the oracle object).
**Sign & trace:** rime feathers growing WINDWARD off every edge (the wind's fingerprints — ice that points), no tracks but yours (the loneliest sign on the map, authored).

### lee_cornice
**Terrain & fixtures:** the cornice wave (the trap), the blue root-crack, the promenade illusion (level snow object, attached to nothing), the rock-line detour (the answer, visible).
**Harvest & loose:** nothing on the shelf (by design — no bait on the trap: the census's one deliberately empty larder).
**Hidden / contained / buried:** nothing findable — what is under the cornice is AIR, and the design never rewards testing it.
**Ambient:** the whumpf (the mountain clearing its throat), the crack's slow blue light, wind-plume streaming off the lip like a flag of exactly where not to stand.
**Sign & trace:** old fracture scars down the NE face (previous collapses — the cornice's rap sheet, readable from the safe rock), a raven riding the lip updraft (the only local that can afford the shortcut).

---

## S7 — The Birch Stand

### aspen_fringe
**Terrain & fixtures:** the aspen colony (live class + dead-standing punk class), browse-line topiary, the paper-lantern snags.
**Harvest & loose:** push-over poles, punk chunks (the ember-carriers), aspen bark strips (bitter — moose winter food, bait stock), catkin twigs.
**Hidden / contained / buried:** snag-heart punk cylinders (the premium cores), a bear-clawed trunk's healed scars (claw-groove ladder — HIBERNATING-elsewhere reassurance authored: sign without threat), under-colony connected root story (one organism — examine wonder).
**Ambient:** the pale colonnade light, dead-leaf flags rattling (aspens keep a few — winter's castanets), snow-plop from sprung branches.
**Sign & trace:** the browse height line (moose reach — measure the neighbor), hare girdling collars (killing the colony's edge — the world eats itself honestly), the healed bear ladder (years old, readable).

### birch_grove
**Terrain & fixtures:** the white columns (bark classes: curl-fringe, sheet, jacket), the fallen reader trunk, the canopy's pen-stroke lattice.
**Harvest & loose:** bark scrolls (hand class), bark sheets (blade class), birch twig bundles (fine kindling), a tinder-conk shelf (false chaga — the identification test: hoof-shaped ≠ chaga, still an ember conk: both PAY, differently — kind misidentification design).
**Hidden / contained / buried:** the fallen trunk's punk heart + under-trunk vole city (tunnels, nests — bedding-material theft option with authored guilt), sap-well rows drilled by sapsuckers (the tree's old wounds in dotted lines — bird forensics).
**Ambient:** bark-curl shiver (movement without wind — the grove's signature), white-on-white column depth (the perception showcase), woodpecker knock.
**Sign & trace:** old blaze — REAL this time — on the grove's south edge (Holt came HERE for bark too: the trapline's outlier mark, a breadcrumb toward the creek crossing), moose-barked scrape panels (antler rub history).

### chaga_tree
**Terrain & fixtures:** the elder birch (half its crown dead — the conk's slow victory), the conk (the black loaf, 3 m up), the reach problem's furniture (climb limbs iced, throw-range clearing, pole-length aspens nearby — the solutions PLANTED in the terrain).
**Harvest & loose:** ground-fallen conk crumbs (spark-catcher samples — the free taste that teaches the value), dead-crown twigs.
**Hidden / contained / buried:** the conk's interior grades (rust-orange punk core = the spark bed; black crust = the coal shell — internal anatomy as loot table), a second smaller conk on the BACK of the trunk (the examine-the-far-side reward — perception pays twice here).
**Ambient:** the tree's split personality (live side sighs, dead side clatters — authored), conk's faint sweet-rot smell up close.
**Sign & trace:** knock-marks on the trunk below the conk (someone tried before with a stick and gave up too low — a FAILED attempt as hint: aim higher, bring more pole).

### game_trail_crossing
**Terrain & fixtures:** the trench trail (packed class — the walkable seam), the moose bed oval (melt-formed, iced glaze), the lee spruce, browse-line sculpting.
**Harvest & loose:** the shed antler half (dig from the bed), trail-packed snow (fast walking — the mobility freebie), willow tops within moose-reach only (browse shadow: what's LEFT tells what was eaten).
**Hidden / contained / buried:** bed-floor treasures (compressed shed hair mat — insulation wad; a second antler point broken off deeper — the pairing lure that makes players re-dig), trail-side red-backed vole runs (the small parallel economy).
**Ambient:** the trail's pull (a made path in pathless country — composition object), lee-quiet, hair-and-musk ghost smell at the bed (occupancy WARNING ambient, honest).
**Sign & trace:** stride-length post-holes (mass calculable — respect taught by arithmetic), FRESH browse nips at the far end (he was here TODAY — the be-elsewhere clock, renewed each visit), the trail's destination logic (toward water — the knowledge object).

---

## S8 — The Creek

### outlet_riffle
**Terrain & fixtures:** the black lead (open water — the prize object), ice shelves (biscuit-lip class), the gravel spit (the safe draw platform), boulder teeth in the current.
**Harvest & loose:** water (liquid, moving, boil-gated), polished pebbles, shelf-ice panes (window-glass curio — and a cutting-board), waterlogged stick jam bits.
**Hidden / contained / buried:** under-shelf air gap (the shelf's anatomy examinable — WHY lips break: education object), spit-gravel gold flecks?? NO — mica flakes (fool's glitter, authored wink: the country tests greed in small ways too), a stranded frozen grayling in a shrinking side-pocket pool (the free fish — ONE, found not caught: the fishery's advertisement).
**Ambient:** the chatter (the valley's only running-water voice — audible two zones out), steam smoke on cold mornings, dipper-splash.
**Sign & trace:** otter rose-holes along the lead (breathing line), mink prints hugging the waterline (the little fisherman's beat), ice-rim growth rings (cold nights recorded in shelf layers).

### gravel_bar_willows
**Terrain & fixtures:** the bar spine, the willow crop (harvest classes by gauge), rose canes (thorned), the ptarmigan drifts.
**Harvest & loose:** withes in sled-load quantity, rose hips (vitamin trickle), ptarmigan (the huntable flock), bar gravel (hearth + boiling stones), grass tussock wads at the bar tail.
**Hidden / contained / buried:** drift-burrowed ptarmigan (the eruption), under-gravel frost-free seep (side-channel water backup), flood-buried log with iron spike (a RAFT once? — human past #5, spike = steel stock), willow-root wads (the toughest lashings, dig-gated).
**Ambient:** whip-clatter, the birds' detonations, hip-red points of color in a white world (the map's only warm color north of the cabin — authored), creek mutter beneath.
**Sign & trace:** ptarmigan wing-trenches and roost pits, browse bands, an old drowned snare loop on a willow (Holt fished this bar for hares too — wire #4, and the trail's second breadcrumb).

### overflow_bend
**Terrain & fixtures:** the cutbank (the dry shelf route), the stained tongues (the trap field), the steam breath line, sound-under-snow (water's muffled voice — the fourth telegraph, sound).
**Harvest & loose:** cutbank frost-fallen blocks (silty — poor), exposed root ladders on the bank face (handholds + root cordage), nothing else — the zone charges, it doesn't pay.
**Hidden / contained / buried:** bank-swallow burrow colony holes in the cutbank face (summer's empty apartments — curiosity + a wren wintering in one: tiny life beat), the overflow's own layered anatomy (probe-readable strata: powder / slush / ice — the exam object).
**Ambient:** steam feathers, the sag underfoot (tactile ambient), the muffled gurgle, dusk making the stains invisible (the night-look's honest warning).
**Sign & trace:** a moose's overflow crossing — steaming post-holes REFROZEN into casts (even he got wet; even he chose the shortest line — companionship in error), old wet-exit scramble marks up the bank (someone's bad afternoon, preserved).

### logjam_crossing
**Terrain & fixtures:** the jam (bridge-class trunks, void-class underdeck), the bluff behind, the east-bank blaze tree (the trapline's front door, visible), snow-caps on every crossing log (the sweep-before-step lesson).
**Harvest & loose:** flood-cured limbs (saw class), bark-stripped poles, jam-top dry wisps (kindling cache in any weather — under the caps).
**Hidden / contained / buried:** underdeck voids (an intact glass bottle — sealed, empty, cork sound: the message-bottle INVITATION, pure player-imagination fuel), a wedged aluminum canoe rib section (human past #6 — the creek has eaten boats), winter-stash muskrat feed bed at the water gap.
**Ambient:** water-gurgle through the jam's throat (the structure BREATHES sound), log-boom knock when stepped, the blaze visible across (the pull object).
**Sign & trace:** the doubled blaze (colon punctuation — the trail SPEAKS from here), mink slide under the deck, high-water wrack lines in the jam's teeth (flood history — how the jam was BUILT, readable).

### confluence_pool
**Terrain & fixtures:** the pool sheet (drum-tight class — the safe thick), the feeder mouth, the black depth (the aquarium object), the chop-hole site (flat, bankside).
**Harvest & loose:** clear pool ice (premium melt), bank alders (jig-rod + smoke-wood).
**Hidden / contained / buried:** the fish (burbot lie-in-wait shapes, grayling drift shapes — VISIBLE through clear ice as moving shadows: the census's only self-advertising food), bottom-snagged spoon lure (glinting through the ice — retrievable ONLY by fishing over it: the map teaching tackle recovery), feeder-mouth spring seep (the pool's warm secret, why fish gather).
**Ambient:** the shapes adjusting below (wonder + larder in one), ice-boom rolls, the feeder's whisper.
**Sign & trace:** otter feed-hole (refrozen thin — BOTH intel and hazard: the pool's one soft spot, marked by feed remains), fish-scale glitter at the otter's table, an old auger-hole scar refrozen (someone fished HERE, with equipment — the world keeps validating the plan).

---

## S9 — The Beaver Pond

### dam_crossing
**Terrain & fixtures:** the dam (causeway class — mud-and-stick masonry), the spill slot (open black water, the marked edge), the downstream pole tail (the polite harvest), the crossing top (print highway).
**Harvest & loose:** loose spill-side poles (pre-cut, peeled), dam-face mud chunks frozen (chinking stock), cattail-analog sedge fringe (bedding wads).
**Hidden / contained / buried:** in-dam woven structure (pull-gated, consequence-priced), spill-pool trout minnows (bait-size — dip-gated), the dam's spring seep line.
**Ambient:** the spill's small waterfall voice, print-map underfoot (the census of everyone), pond-flat white silence beyond.
**Sign & trace:** every local species' prints in one meter (the crossroads guest-book — tracking's final exam sheet), fresh gnaw chips floating frozen in the slot (the engineers are AWAKE down there).

### pond_flat
**Terrain & fixtures:** the black-glass panes (bubble-trail archive), snow-pane patchwork, margin willow palisade.
**Harvest & loose:** pane ice (the clearest on the map — lens-grade: the ice-lens fire-starting lore flag, sunny-day-only, delightful), margin withes.
**Hidden / contained / buried:** the bubble-map (trails converge on lodge + cache — the readable infrastructure diagram), under-ice weed beds (muskrat feed — and muskrat push-up domes at the margin: the SECOND rodent economy, small protein flag).
**Ambient:** bubble-trails silver under boots (walking on the archive), pane-crack star patterns, the lodge's steam thread NE.
**Sign & trace:** push-up domes (muskrat breathe-holes roofed in frozen weed — count the population), the trails' braided logic (who went where, all season, in one look).

### the_lodge
**Terrain & fixtures:** the mound (frozen masonry class), the vent chimney (steam thread — the life signal), underwater door (implied, examine-taught).
**Harvest & loose:** shed gnaw-poles at the base ring, frost-feather crystals at the vent (beauty macro).
**Hidden / contained / buried:** the interior (axe-hour-gated, DESIGNED disappointment — wet sticks, musk, scattered kits' bedding: the anti-loot lesson holds), vent-warmth (hand-warming at the chimney — tiny real heat, free, weird, memorable: the lesson's consolation prize).
**Ambient:** the vent's pulse (breath of the house), under-ice thumps and mutters (the family heard through the floor — the census's most alive ambient), musk trace.
**Sign & trace:** generations of repair layers in the mound's anatomy (readable masonry — the oldest continuously-inhabited structure in the valley, older than Holt's cabin: authored fact), tail-slap memory (none in winter — the silence that proves the season).

### food_cache_margin
**Terrain & fixtures:** the feed raft (butt-up rows, ice-locked), the thin-margin warning arc (bubble-marked), the chop-friendly flat side.
**Harvest & loose:** exposed butt poles (chop-gated), bark-strip flotsam frozen in.
**Hidden / contained / buried:** the raft's under-ice mass (green tonnage — visible, mostly untakeable: the abundance-behind-glass object), inner-bark sheets (bait premium, peel-gated).
**Ambient:** the raft's ordered rows (husbandry made visible — the design's thesis in sticks), gnaw-chip smell of fresh aspen.
**Sign & trace:** the rows' businesslike angles (somebody's pantry discipline), drag-furrows from the far shore (the harvest routes — where the aspen came FROM: follow them to standing aspen stands, knowledge bonus).

### drowned_set
**Terrain & fixtures:** the slide-pole set (lever, chain, staple), the rusted trap jaw (seized class), the spill-pool edge, the blazed shore spruce (the gateway's other half).
**Harvest & loose:** the snare-wire wrap (yards, the prize), chain + staple (hardware), the pole itself (seasoned lumber).
**Hidden / contained / buried:** under-pool second set (a submerged conibear glimpsed through ice — retrievable at spring, i.e., NEVER: the country holds some tools back, authored), wire-wrap inner layers (the deeper you unwind, the better the wire — patience-graded loot).
**Ambient:** the set's tidy-impatience craftsmanship (character in knots), spill-pool gurgle, the blazes' pull SE.
**Sign & trace:** the wraps' weathering gradient (years of re-visits — Holt's calendar in wire), drowned-set engineering itself (the trapper's method readable: humane-kill physics as grim education).

---

## S10 — The Trapline

### blaze_gateway
**Terrain & fixtures:** the doubled blaze tree (the teacher), the corridor mouth, the dished seam (old-passage class snow), the next-blaze sightline.
**Harvest & loose:** trailside dead twigs (commuter kindling), blaze-chip scars' pitch weep (fire dabs).
**Hidden / contained / buried:** under-seam packed old trail (probe-confirmable — the trail EXISTS below the season), a trailside stump-top tobacco tin (trail cache #1: waxed matches, three, and a pencil stub — Holt's habit of leaving himself supplies: the trail TEACHES cache ethics).
**Ambient:** the reorganizing forest (the look's pattern-snap authored), corridor pull, first-blaze glow in low light (axe-cut wood catches light — findable at dusk, authored mercy).
**Sign & trace:** blaze heal-lips (dated by rollover growth — the trail's age), the seam's discipline (a straight man in crooked country).

### spruce_tunnel
**Terrain & fixtures:** the nave (post-spruce walls, mesh roof), the drifted blowdown (the detour test), blaze pairs at interval, the twelve-foot world.
**Harvest & loose:** standing-dead posts (fence-wood fuel, snap class), beard lichen swags (tinder streamers, abundant HERE — the tunnel's one gift).
**Hidden / contained / buried:** blowdown's under-arch crawl (the short way through the test — probe + crawl vs. the circling detour: two answers, both fair), a mid-tunnel side-blaze pair (a SPUR — to the line's second set, off-trail: completionist hook, storm-inadvisable, authored warning in spacing).
**Ambient:** administrative silence (kept — it read aloud true), secondhand daylight, needle-sift ticks, your own heartbeat loud (authored interiority — the tunnel is the map's quietest room).
**Sign & trace:** marten prints OWNING the trail (the line's quarry commutes on the line — irony as sign), grouse wing-marks where the tunnel's grouse exploded through the mesh (even the roof has traffic).

### marten_set_tree
**Terrain & fixtures:** the leaning set-pole, the box (iced mouth), the bait wire, the frozen marten (the find), trail continuing both ways.
**Harvest & loose:** set wire (yards #5), the box nails (pull-gated), bait-bone remnant.
**Hidden / contained / buried:** the marten (fur + the skinning exam), box-back maker's marks (stenciled "V.H." — the initials that close the chart's loop BEFORE the cabin: the name becomes a person mid-trail), under-pole snow void (a dropped belt-axe head, rusted — Holt LOST tools too; hafting it is the player's first full repair if they never fixed the hatchet).
**Ambient:** frost feathers on wire (cold made visible at wire-gauge), the box's small dark (a coffin-sized examine — tone authored gentle), trail-quiet.
**Sign & trace:** ice-seal thickness (weeks — the away-calendar), the set's habits (height, angle, bait style — craft as characterization, third instance: by now players could DESCRIBE Holt).

### cabin_gate
**Terrain & fixtures:** the bench lip, the stump rows (mown order class), the clearing frame, THE VIEW (cabin, cache, shed as composed distance objects), the crooked stovepipe (the no-smoke object).
**Harvest & loose:** stump-top snow caps (nothing — the zone is a threshold; its poverty is composition).
**Hidden / contained / buried:** gate-post mail box — a coffee can nailed to the first stump, lid frozen ("MAIL" in paint — the bush joke: nearest post 40 miles; inside, a plane-dropped newspaper from October: the DATE object — the world has a calendar, and winter has been long).
**Ambient:** opening-sky relief after the tunnel, the empty-word arrival (the look's beat), held-breath yard silence below.
**Sign & trace:** stump rows' seasons of work (years counted in cuts), no tracks anywhere in the clearing (the confirmation, land-wide), the pipe's cold crook (hope's punctuation mark).

---

## S11 — Holt's Homestead

### dooryard
**Terrain & fixtures:** the blank-page yard, the buried chopping block + sawbuck mounds, the dog-run wire + posts, the flagpole? no — the cache-ladder stash under the cabin (pole-ends visible at a stoop), path traces to all doors.
**Harvest & loose:** the run-wire cable (unwind-gated), post staples, yard-edge kindling stubs.
**Hidden / contained / buried:** under-snow yard archaeology (a dog dish, a chew-scarred axe handle blank — the dog made real; a horseshoe nailed over the door frame, points up — luck kept), the ladder (the cache key, stooped-for), buried path stones (the yard's skeleton — dig-mapped).
**Ambient:** held-breath tidiness, the wire's faint hum, night's shape-yard (authored), aurora wash on ITS night.
**Sign & trace:** the mown-stump discipline everywhere, wind-scoured door-drift asymmetry (which way storms come — sited to the weather: bush architecture readable), NO cabin tracks (the third confirmation).

### porch
**Terrain & fixtures:** the drift dune (plaster class snow), the door (latched, unlocked — bush law), the empty shovel nails, the eave's dry strip, a porch bench mound.
**Harvest & loose:** dune snow-blocks (dig spoil → windbreak stock — even the obstacle composts), eave-hung dried grass bundle (boot-stuffing, pre-harvested — Holt's habit #7).
**Hidden / contained / buried:** under-bench boot-jack + a stiff pair of work gloves (leather, mouse-nibbled — REAL find, entry-adjacent by design: the porch pays the digger before the door opens), door-frame key nail (empty — the door was never locked: the key's absence IS the culture, examine-taught).
**Ambient:** dune-muffled quiet, the door's waiting plainness, dig-sweat steam (the player's own breath as object — the sweat debt visible).
**Sign & trace:** the nails' shovel silhouette (tool-shaped absence #2), autumn's last boot prints fossilized in porch mud under the drift (Holt LEAVING, preserved — walk-out direction readable: toward the trail, calm strides — no emergency: closure).

### cabin_interior
**Terrain & fixtures:** the stove (+ warming shelf, damper, pipe), the bunk, the plank table + two chairs, the shelf rows, wall tool-nails (size-ordered, half empty), the window shutters (inside bars), the door's draft-snake sausage, floor boards (one loose — see hidden), the kindling box, wash basin + bench.
**Harvest & loose:** the laid kindling, the match tin, flour/salt/lard/tea/beans tins, the bulged can (the marked danger), kerosene lamp + jug, candle stubs, the note, a deck of cards (soft with use — the storm-night object, authored: co-op's smallest gift), sewing kit tin (needles thread buttons — repair economy), a wall calendar (October's grouse print, days crossed to the 19th — the date's second witness), cast-iron pan + pot, dish shelf, a slush lamp shell (the pre-kerosene backup: fat + wick + tin — the lamp the players can COPY: bearing grease + rag: the census closing a loop planted at the gouge).
**Hidden / contained / buried:** loose floor-board cache (a coffee can of cash?? no — of .22 shells + a spare stove-door spring + a whetstone: the practical trinity), bunk-under trunk overflow (winter boots, felt liners — the footwear jackpot, size-lottery authored), behind-stove warming niche (dried boot liners left hanging — usable NOW), the mouse dynasty's wall-void nest (thieved batting, a chewed mitten thumb — where the shelf losses WENT: the world's books balance).
**Ambient:** museum cold, mouse-must + kerosene + old woodsmoke (the smell triad of every real cabin), the stove's argument (authored), lamp-light possibility (the night resource), storm heard as WEATHER (walls change the storm's voice — the payoff ambient).
**Sign & trace:** wear shine on chair arms and axe nails, the note's steady hand, days-crossed calendar discipline, boot-heel arcs worn into the floor at the stove door (years of mornings, printed).

### loft
**Terrain & fixtures:** the ridgepole triangle, the tick mattress, the cedar trunk, the king-post rifle nail, the gable vent (a fist of daylight).
**Harvest & loose:** the horse blanket, quilts (mouse-graded), the boltless .22 (story furniture), sill shell box (flagged for Andrew), a moth-paper bundle of cedar blocks (why the wool survived — preservation as detail).
**Hidden / contained / buried:** trunk contents (union suits, socks, sweater, a wool watch cap, long wool scarf — the clothing jackpot, graded), trunk-bottom photograph tin (a woman on a riverboat deck, 1970s; "Vi & me, Galena" penciled — V. HOLT is VIOLET?? — no: "V." stays Holt, "Vi" is the wife: the cabin's second person, the reveal that reframes the note's "til breakup" as going-to-HER: the map's warmest secret, found only by full search), rafter-hung snowshoe NEEDLE and babiche coils (snowshoe REPAIR stock — the cache's shoes have a spare-parts story).
**Ambient:** trapped-air stillness (the warmest cold room), cedar + wool smell, vent-light beam with dust motes even in winter.
**Sign & trace:** one side of the mattress more worn (which side he sleeps), the rifle's oil shadow on the log wall (decades in one place).

### cache
**Terrain & fixtures:** the four skirted poles, the box house, the toggle latch, the ten feet of air (the problem object), the ladder's ABSENCE.
**Harvest & loose:** (post-solve) beans, rice, dry fish slab bundle, candles, the tarp, the rope coil, THE SNOWSHOES, THE FELLING AXE, a tin of tea, a sealed pail of dog kibble (the dog again — and emergency calories with authored dignity-check humor).
**Hidden / contained / buried:** back-wall hung canvas pack (EMPTY — the carry-it-home solution included: Holt thinks of everything, including the players), floor-corner mouse-proof tin (sourdough starter, dormant — the deepest lore object on the map: some things you save even from mice; useless to players, PRICELESS to Holt: the one thing the note's "leave the box full" is really about, for those who read).
**Ambient:** the skirts' tin shimmer, the box's swaying creak in gusts (ten feet of leverage), the toggle's simple patience.
**Sign & trace:** claw-frustration grooves on a pole below a skirt (the system WORKS — audited by a marten), the poles' draw-knife peel marks (built by hand, alone, readable strokes).

### woodshed
**Terrain & fixtures:** three walls + roof, the courses of split wood (spruce rows, birch rows — btu-sorted: fuel literacy displayed), the chopping stump + buried maul, the bucksaw pegs, the shovel corner, THE SLED (split runner), a workbench slab + vise? (no vise — a shave-horse: period-true), wall pegs of hung tools' absences.
**Harvest & loose:** split dry wood (the jackpot, haul-priced), the maul, the bucksaw, the shovel, kindling bin sweepings, a box of wooden matches on a high joist (shed-local fire backup — Holt's redundancy habit #8), sled-repair leavings (old runner half — the pattern to copy).
**Hidden / contained / buried:** under-course bottom rows (driest wood — first-in seasoning logic, take-from-the-top taught by collapse risk: even the WOODPILE has technique), joist-top long stock (two spare axe hafts, a peavey pole — handle economy), shave-horse drawer slot (draw-knife, wrapped — the tool that makes tools).
**Ambient:** wood-order perfume (split spruce sweetness), the courses' checked-end music when pulled, roof-load creak.
**Sign & trace:** the maul mid-swing (the interruption, kept), splitting-technique in the billet scars (one-stroke splits — strength or skill, readable either way), the wood's ring-count (the country's climate diary in every round).

### water_hole_path
**Terrain & fixtures:** the packed path (made-thing class), the bench lip steps (cut treads under snow), the plank lid + stone, the chopped basin (skinned over), the lean-pole + dipper can, creek-sound below.
**Harvest & loose:** the dipper (a CUP again — the census's recurring humblest treasure), lid-stone (anchor stock), basin skim-ice discs.
**Hidden / contained / buried:** basin-bottom settled bucket (galvanized, sound, sunk on purpose below freeze line — retrieve by reach: Holt's winter storage trick TEACHING water-hole craft), path-edge stored pole-spare for the lean (redundancy habit #9).
**Ambient:** the path's underfoot difference (made vs. wild — feet can read), the dipper's slow turn (the closing image, kept), creek voice below the lip.
**Sign & trace:** path re-cut history (widened over years), the treads' wear-polish, the lid-stone's lichen ring matching its seat (undisturbed all season — the yard's fourth confirmation, and the last).

---

## New-material & system flags harvested by the census

**Material table candidates:** rock/stone (boiling stones, anvils, flakes — presently absent!), bone/antler (billet, tine, scales), fur/hide (marten, hare — insulation values), peat (poor wet fuel), lichen (flash tinder + famine food), punk/rotten wood (ember medium — distinct from sound wood), rubber (tire, tube — black smoke + elastic), kerosene (lamp fuel class), canvas (pack, tarp), babiche/rawhide (lacing), grease/fat (bearing grease, lard — lamp fuel + waterproofing), mica (worthless glitter — the honesty material), brass (benchmark, shells), paper (newspaper, photographs, cards — burnable heartbreak class).
**Snow/ice sub-types used:** powder, wind-slab, drift, spindrift, sugar snow, snow-cap, sastrugi, plaster-drift, rime, hoarfrost, surface hoar, frost feathers; black ice, white ice, shore/grounded, pressure slab, candle—(no: spring only), overflow, frazil, skim/skin ice, glare ice panes. Each wants at least a behavior note in the table.
**Recurring habit-objects (authoring shorthand):** Holt's redundancy caches (matches ×3 locations, poles, hafts), CUPS (tin cup, dipper, bucket — the humble-treasure motif), wire sources (×5, all earned), human-past artifacts (×9, dating the valley), the gray-jay pair (recurring ambient thieves), the raven pair (recurring pointers).
**Census totals:** ~59 zones · ~1,150 candidate objects/ambients/signs across the valley (crash-site builds excluded). The density gradient (map.md §6) prunes: Ring-0/homestead zones keep most; Ring-2 zones keep the load-bearing half.
