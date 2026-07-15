# The rooms — every Scene and zone in the valley

> **Status: SCRATCHPAD (investigation) — 2026-07-15 overnight design run.** The complete room
> design for the Whiteout scenario, written as if the full room system (Scene transitions,
> durations, exposure, weather) were live. Macro geography, travel pricing and the design
> thesis live in [`map.md`](map.md); how these rooms are used in play lives in
> [`report.md`](report.md); the exhaustive per-room object lists live in
> [`objects.md`](objects.md).
>
> **Zone entry format.** Each zone gives: aliases · position (meters from the wreck, y+ =
> north, matching `zones.py`) · terrain tags · **exposure band** (the P5 warmth-drain input:
> `sheltered` < `broken` < `open` < `brutal`) · edges (walk/see; cross-Scene edges marked ⇄)
> · the authored look (the survey prose a player reads) · what's here and what it costs ·
> hazards (always: telegraph → consequence) · story, if the zone carries a beat.
>
> **Pricing discipline** (map.md §1): every resource costs ≥2 of daylight / warmth / sweat /
> tools / knowledge / risk. Every hazard is telegraphed. Every gate has ≥2 openings.

---

## S1 — The Crash Site (exists; retouch only)

The nine authored zones in `zones.py` stand. The wider world adds only **outward edges** and
**glimpses** — no interior redesign:

- `treeline` ⇄ **North Wood `forest_edge`** (walk N; the existing zone becomes the doorway).
- `outside_nose` ⇄ **Muskeg `tussock_flat`** (walk W; the clearing simply opens out).
- `tail_section` ⇄ **Strike Path `shear_line`** (walk NE, upslope — the gouge line is the
  path; following the wreck's own scar uphill is the natural first expedition).
- `fuselage_top` gains cross-Scene **see** glimpses: the lake's sky-glare W, the ridge notch
  NE, and — only if lit — fire or smoke on the lake ice. The climbable spine becomes the
  site's watchtower, which it already wants to be (the antenna stub lives there).
- `debris_trail` gains a see edge NE to `shear_line` (the scar is one continuous line).
- **New salvage note (the early sled)**: the engine cowling half-buried at `outside_nose`
  is a drag-toboggan blank — punch two holes, lash paracord (all hour-1 materials), and
  hauling gameplay exists from the first fuel ferry. It is slow, tippy, and plows in soft
  snow (honest limits) — the woodshed's freight sled later arrives as the UPGRADE to a
  logistics game the party already plays, not as its introduction.

**Exposure**: interiors `broken` (windbreak but unheated), exteriors `open`, fuselage_top
`brutal` (the wind owns the bare spine).

---

## S2 — The Muskeg (W of the wreck)

The frozen bog the pilot almost cleared. Flat, white, deceptively open — the walking is
miserable and everything useful is at ankle height, under snow, priced in sweat and
knowledge. Five zones.

### `tussock_flat` — the tussock flat
*aliases:* muskeg, tussocks, bog, the flat · *pos:* −120, −10, 0 · *terrain:* exterior, snow,
muskeg · *exposure:* open
*edges:* walk ⇄ crash `outside_nose` E; walk `labrador_thicket` NW; walk `drifted_channel` W;
see all S2 zones, see crash-site hulk E, see `lake_gate_willows` W.
> Cottongrass tussocks stud the snow like buried heads, each one an ankle-trap under its
> white cap. The flat runs west toward a grey shine of lake ice, and the wind has nothing to
> say to it but one long vowel.
**Resources & pricing.** *Cottongrass seed-heads* (first-rate tinder): visible as tufts only
if examined — knowledge + a few minutes' picking per handful (daylight). *Lowbush cranberries*,
frozen hard at the tussock bases: knowledge (the manual's forage page or plain curiosity) +
sweat (digging bare-handed chills; digging gloved is slow); a real but marginal calorie
trickle — priced honestly low so it can't replace hunting.
**Hazards.** Tussock walking: hurried movement (running, hauling) risks a wrenched ankle —
telegraphed by the look and by the first stumble narration. Slow pace is safe.

### `labrador_thicket` — the labrador-tea thicket
*aliases:* thicket, labrador tea, dwarf birch, brush · *pos:* −160, 40, 0 · *terrain:*
exterior, snow, brush · *exposure:* broken
*edges:* walk `tussock_flat` SE; walk `tamarack_island` W.
> Knee-high brush claws out of the snow here, dwarf birch and something evergreen-leaved
> that survives the cold out of pure stubbornness. The wind combs across the top of it and
> leaves the ankle-height world alone.
**Resources & pricing.** *Labrador tea* (leathery leaves persist all winter): knowledge to
recognize + a container + fire to brew — a warm drink is real warmth-band help and morale,
gated behind the whole fire-water-vessel chain. *Dwarf-birch twigs*: dense, resinous
kindling bundles — free to snap by hand, but a useful ARMLOAD costs time and gloved fingers
(daylight + warmth). The honest lesson: kindling is everywhere; *quantity* is the cost.

### `tamarack_island` — the tamarack island
*aliases:* tamarack, island, the lone tree, snag · *pos:* −240, 60, 1 · *terrain:* exterior,
snow, trees · *exposure:* broken
*edges:* walk `labrador_thicket` E; walk `drifted_channel` S; see `lake_gate_willows` W.
> A single old tamarack holds a low rise, dead lower limbs spidered out stiff and grey. Under
> the snow at its base, ravens have been working at something; the tracks come and go from
> the direction of the wreck.
**Resources & pricing.** *Dead tamarack limbs*: bone-dry, off the ground, snap or saw free —
the best easy fuel west of the treeline, but a load worth carrying wants a saw or hatchet
(tools) and a sled or many trips (daylight). *The ravens' find*: dig where they dug
(knowledge — reading tracks) → a mail bundle flung from the breach: nothing to eat, one more
letter (story). The ravens teach the real skill: **tracks point at calories**; here the
answer is a red herring with a heart.
**Story.** The ravens found the crash before anyone else did. They'll appear again wherever
food is mishandled — the world's first scavenger pressure, played gently.

### `drifted_channel` — the drifted channel
*aliases:* channel, slough, drift, hollow · *pos:* −300, 0, −1 · *terrain:* exterior, snow,
deep-drift · *exposure:* open
*edges:* walk `tussock_flat` E; walk `tamarack_island` NE; walk `lake_gate_willows` W.
> An old slough crosses the flat here, brim-full of wind-packed drift. The snow looks like
> more of the same and is not: one stride in, the bottom is somewhere around your thigh.
**Resources & pricing.** None. This zone is the tuition zone: it exists to teach snow.
**Hazards.** *Deep drift*: crossing costs double time and real sweat (wet clothing debt);
floundering with a heavy load is worse. Telegraphed by the look ("is not") and by probing
with anything pole-shaped (a probe — knowledge — reveals depth and finds the firm line the
old slough bank makes; clever players cross dry). The storm refills it first of anywhere.

### `lake_gate_willows` — the willows at the lake gate
*aliases:* willows, willow fringe, lake shore brush, the gate · *pos:* −420, 10, 0 ·
*terrain:* exterior, snow, brush · *exposure:* broken
*edges:* walk `drifted_channel` E; walk ⇄ lake `shore_apron` W; see `tussock_flat`,
`tamarack_island` E, lake `ice_flat` W.
> Head-high willows crowd the last ground before the lake, whips clattering softly in the
> wind. Down at snow level the bark is nibbled white in patches, and narrow packed runs
> thread the stems like someone's small commute.
**Resources & pricing.** *Willow withes*: cut green (blade — tools) for lashings, snare
loops, a fish-jig rod, sled repair — the valley's cordage-adjacent plant, everywhere along
water and only along water (knowledge: willow means water). *The hare runs*: the nibbled
bark and packed runs are the sign; a snare (wire or cord + knowledge) set ON a run and
**left to work** may hold a hare hours later — protein priced in wire, know-how, and the
discipline to leave and come back (daylight structuring). A snare set off-run catches wind.
**Story.** The commute line is the first invitation to read the world as inhabited.

---

## S3 — The Lake

The pilot's runway that almost was. The biggest open space in the valley: the visual-rescue
stage, the wind's kingdom, the ice hazard family, and the one place the world can SEE you.
Six zones.

### `shore_apron` — the shore apron
*aliases:* shore, lakeshore, apron, shore ice · *pos:* −520, 0, 0 · *terrain:* exterior,
ice, shore · *exposure:* open
*edges:* walk ⇄ muskeg `lake_gate_willows` E; walk `ice_flat` W; walk `outlet_narrows` S;
see `ice_flat`, `pressure_ridge`, `inlet_mouth` N, `far_shore_burn` W (clear weather only).
> Grounded shore ice runs in a pale apron along the willows, solid as a floor and grumbling
> to itself when the temperature moves. Out west the lake is one flat page; far across it a
> smudge of burnt black sticks stands against the snow. Half-buried at the tide line of some
> old autumn storm lies a bleached drift log the length of the plane.
**Resources & pricing.** *The drift log*: a season of fuel in one object — utterly immune to
bare hands. A saw or axe (tools, the good ones from Holt's) plus real labor (sweat +
daylight) buys rounds; without them it's a bench and a windbreak (still worth something —
partial success). *Blue shore-ice chunks*: cleaner and denser than snow for melting (water
efficiency — knowledge from the manual's water page); pry free with any lever.
**Hazards.** None. The apron is the lake's honest zone — grounded ice can't drop you. The
look says so ("solid as a floor") to teach the contrast the other zones will spend.

### `ice_flat` — the open ice
*aliases:* lake ice, the flat, open ice, middle of the lake · *pos:* −900, 0, 0 · *terrain:*
exterior, ice, open · *exposure:* brutal
*edges:* walk `shore_apron` E; walk `pressure_ridge` W; walk `inlet_mouth` N; walk
`outlet_narrows` S; see everything on the lake, the ridge knob NE, the sky.
> Out here there is no *here* — just wind-burnished ice under a skin of driven snow, and
> more sky than one pair of eyes can be responsible for. Anything standing on this would be
> visible for miles. So would you.
**Night/storm look.** *In near-whiteout the flat is the map's most dangerous room:* "White
above, white below, and the wind erasing the difference. Your own trail is gone within
plane-lengths. Somewhere is the shore; the wind knows which way it was, if you marked the
wind." (The design intent authored plainly: after dark or in whiteout, the flat is
navigable ONLY by wind-bearing, a rigged rope line, or the fire itself as beacon.)
**Resources & pricing.** *Visibility itself* — the zone's only resource, and the visual
rescue route's whole foundation. A signal fire out here is seen by any air search on the
drainage line; a fire out here also fights the wind for its life. Making one work costs
engineering: a windbreak (snow-block wall — see below; or hauled wreck paneling), a dry
platform (green boughs from the strike path), fuel HAULED from shore (daylight + sweat),
and timing (lit and smoking when the beat plane passes, not an hour after). *Wind-slab
snow-blocks*: the flat's hard-packed snow cuts into blocks with any long blade or the
shovel (tools + knowledge from the manual's shelter page) — windbreak or emergency
snow-shelter stock, the one shelter material the treeless ice provides.
**Hazards.** *Exposure*: the flat drains warmth faster than anywhere but the knob;
everything done here is done on a countdown the zone announces plainly ("So would you" —
the look cuts both ways: seen by planes, flayed by wind).

### `pressure_ridge` — the pressure ridge
*aliases:* ice ridge, pressure ridge, heave, ice blocks · *pos:* −1300, 60, 1 · *terrain:*
exterior, ice, jumbled · *exposure:* open
*edges:* walk `ice_flat` E; walk `far_shore_burn` W; see `ice_flat`, `far_shore_burn`.
> The lake's two plates meet here in a frozen argument — a ridge of upthrust slabs shoulder
> high, blue in their broken faces. On the lee side the wind goes suddenly, blessedly stupid.
**Resources & pricing.** *The lee* — free windbreak mid-crossing, the resting ledge that
makes the burn run survivable in worsening weather (knowledge: cross VIA the ridge, not the
shortest line). *Clear blue ice*: the cleanest melt-water stock on the map, already broken
into liftable slabs (a container and a fire still gate the payoff).
**Hazards.** *The jumble*: climbing through loaded (hauling wood back) risks a slip and a
dropped load — cross the low gap at its south end instead (visible on approach; the ridge
telegraphs its own door).

### `inlet_mouth` — the inlet mouth
*aliases:* inlet, north end, feeder brook, bad ice · *pos:* −1000, 350, 0 · *terrain:*
exterior, ice, thin-ice · *exposure:* open
*edges:* walk `ice_flat` S; see `ice_flat`, `pressure_ridge`.
> A feeder brook comes in under the ice at the lake's north end, and the lake shows it: the
> snow cover thins to a stained grey ring, the ice beneath goes dark as bottle glass, and
> every third footfall out there answers with a drumhead note that no sane animal ignores.
> In along the shore, where the brook actually arrives, a narrow lead stands open against
> the gravel — real water, moving, close enough to smell — with all that dark glass lying
> between it and anywhere sensible to stand.
**Resources & pricing.** *The shore lead*: the NORTH's liquid water — the signal-camp
party's answer to the riffle, so the lake day has real logistics instead of a fuel-melting
tax (assessment I-2). Priced exactly as the zone's own curriculum demands: the safe draw is
the LONG way — around by the grounded shoreline gravel, prone, with a lashed dipper
(daylight + knowledge that grounded beats short) — while the short way is forty feet of
drum-note glass. The zone thus graduates from pure tuition to a real trade: the lesson and
the temptation are the same forty feet.
**Hazards.** *Thin ice*: proceeding onto the dark ring past the drum warnings = through the
ice — soaked to the waist, the run-for-your-life clock, gear on the bottom. Never random:
every step of escalation is announced, and probing (pole, axe tap) reads the danger safely.
The shore lead's undercut lip is the second, subtler exam: the gravel is safe, the last
yard of overhanging ice-shelf is not, and the difference is visible to a look that has
learned anything at all here.

### `outlet_narrows` — the outlet narrows
*aliases:* outlet, narrows, south end, lake outlet · *pos:* −700, −350, 0 · *terrain:*
exterior, ice, current · *exposure:* open
*edges:* walk `shore_apron` N; walk `ice_flat` N; walk ⇄ creek `outlet_riffle` S (the bank
route — safe); see `ice_flat`, creek `outlet_riffle` S.
> The lake gathers itself and leaves through a stone-pinched gap at the south end. Current
> keeps the ice honest here — thin, flexing, snow-free in a long tongue — and from somewhere
> past the gap comes a sound the whole frozen valley has forgotten: running water.
**Resources & pricing.** *The sound* — the discovery chain to open water (map.md §4),
audible from the south shore and the forest edge. The water itself is downstream in the
creek Scene; this zone's job is to advertise it and to gate the direct route.
**Hazards.** *Current-thinned ice*: the snow-free tongue is the tell (wind strips what
current thins — knowledge). The safe way down to the riffle is the west BANK, dry-shod,
obvious once looked for. Walking the tongue because it's shortest is the classic paid lesson.

### `far_shore_burn` — the burn on the far shore
*aliases:* burn, burnt shore, dead trees, far shore · *pos:* −1900, 0, 1 · *terrain:*
exterior, snags, burned · *exposure:* broken
*edges:* walk `pressure_ridge` E; see `pressure_ridge`, `ice_flat`.
> An old fire took this shore down to black bones — acres of standing dead spruce, barkless,
> silver-grey, dry as paper and ringing hard when knocked. Enough seasoned firewood to keep
> a family alive all winter, an easy hour from the wreck. The hour is the problem.
**Resources & pricing.** *Standing-dead spruce*: the fuel jackpot — dry, dense, already
seasoned; push-over or one-tool felling for the small stems (some yield to determined
bare-handed rocking — a real freebie, priced instead in distance). The price is the map's
plainest: 1.5 km of open ice EACH WAY (daylight + brutal-exposure transit + the storm
roulette — heavy-band weather strands or kills the overloaded). The burn pays best to
parties who scout early, cross light, and ferry via the pressure-ridge lee — logistics as
gameplay.
**Story.** Lightning, years ago. Fireweed under the snow. The valley has burned and healed
before; the world is older than the emergency.

---

## S4 — The North Wood (the spruce forest beyond the treeline)

The survival economy's heart: fuel, shelter, protein, and the forward camp the GDD's dense
core wants. Sheltered, dim, and generous only to players who look up, look down, and read
bark instead of grabbing at snow. Six zones.

### `forest_edge` — the forest edge
*aliases:* edge, treeline in the wood, first trees · *pos:* 0, 60, 2 · *terrain:* exterior,
trees, cover · *exposure:* broken
*edges:* walk ⇄ crash `treeline` S; walk `big_spruce_hollow` N; walk `deadfall_tangle` NE;
see crash-site hulk S (a broken glimpse), `big_spruce_hollow` N.
> The spruce close ranks a few steps in and the wind drops to a rumor overhead. Snow lies
> deep and unbothered between the trunks, printed here and there with the neat stitchwork
> of small feet. Back south through the boughs, the wreck shows in pieces — a glint, a rib
> of white metal — like something the forest is already growing over.
**Resources & pricing.** *Green spruce boughs*: cut low limbs (blade) — bedding, bough-bed
insulation (the ground steals more heat than the air — manual knowledge), shelter thatch,
the signal-fire smoke-maker (green = white smoke). Free-ish by design: boughs are the
gateway resource that teaches cutting the world.
**Story.** The stitchwork tracks (voles, a weasel's paired dots) are the wood introducing
its cast. Nothing here hunts the players; the cold does that.

### `big_spruce_hollow` — the big-spruce hollow
*aliases:* hollow, big spruce, cathedral grove, camp grove · *pos:* −20, 140, 2 · *terrain:*
exterior, trees, sheltered · *exposure:* sheltered
*edges:* walk `forest_edge` S; walk `grouse_thicket` N; walk `hare_runs` NE; walk
`tree_well_hollow` W; see `forest_edge`, `grouse_thicket`.
> Half a dozen white spruce stand grandfather-large here, and under them the snow thins to
> a firm blue dusk. Dead twigs skirt every big trunk from knee height down, grey and
> brittle and bone-dry under the living boughs — a fact worth more than it looks. The wind
> passes overhead without stopping.
**Resources & pricing.** *Squaw wood* (the dry dead twig-skirts): THE reliable fire starter
of the entire valley — always dry regardless of weather, snaps free bare-handed. Priced
purely in knowledge: the look hints ("worth more than it looks"), the manual's fire page
names it, and once learned it changes every fire the party ever builds. *Spruce pitch*:
amber seams on scarred trunks — fire helper (burns wet), glue for repairs (the hatchet
haft, the sled runner) — pry with any blade, melt with fire (tool chain). *The campsite
itself*: flat, sheltered, wood-adjacent, water-adjacent (creek S) — the designed forward
camp; choosing it is the reward for evaluating terrain (exposure bands make it mechanical).
**Story.** This is the "camp + near-forest" of the GDD's dense core. If the party builds a
home outside the fuselage, the world has quietly argued for here.

### `deadfall_tangle` — the deadfall tangle
*aliases:* deadfall, blowdown, windthrow, tangle · *pos:* 80, 160, 2 · *terrain:* exterior,
trees, obstacle · *exposure:* sheltered
*edges:* walk `forest_edge` SW; walk `hare_runs` N; see `hare_runs`.
> A winter gale laid a whole family of spruce over each other here years ago, and the wood
> has been drying in the wind ever since. It is a fortune in fuel and a bear to get at:
> trunks crossed like dropped matchsticks, every one of them shin-high, hip-high, wrong.
> One widow-maker hangs half-fallen overhead, caught in a neighbor's crown, creaking.
**Resources & pricing.** *Seasoned deadfall*: the near fuel-mother-lode (the burn is richer
but 2 km away) — limbing and bucking want saw/axe/hatchet (tools) and sweat; bare hands can
snap the small stuff endlessly (partial success always available). Priced in labor and
barked shins, not distance.
**Hazards.** *The widow-maker*: named, creaking, visible — working under it is the risk;
pulling it down first with cord from a distance (knowledge + rope) is the professional
move and free physics lesson.

### `grouse_thicket` — the grouse thicket
*aliases:* thicket, young spruce, roost · *pos:* −40, 240, 3 · *terrain:* exterior, trees,
dense · *exposure:* sheltered
*edges:* walk `big_spruce_hollow` S; walk `hare_runs` E.
> Young spruce grow shoulder-to-shoulder here, dense as a hedge, dim as a closet. Fat dark
> shapes sit puffed and motionless in the low branches — spruce grouse, wintering on
> needles, watching you with the total unconcern of a bird that has never been wrong about
> anything.
**Resources & pricing.** *Spruce grouse*: real protein, comically tame (true to life) — but
the gate is the WEAPON and the follow-through: a throwing stick (any straight billet —
free) thrown from close range (approach slowly: rushing flushes the flock one zone away for
hours — patience priced in daylight), then plucking/cleaning (blade + knowledge + the
stomach for it) and cooking (the whole fire chain). Missed throws are honest: the birds
relocate branch by branch, unconcern degrading with each attempt.
**Story.** "Fool hen." The first player to club dinner out of a tree will tell that story
at the reveal table, which is the point.

### `hare_runs` — the hare runs
*aliases:* runs, alder alley, snare alley, hare highway · *pos:* 60, 260, 3 · *terrain:*
exterior, brush, trees · *exposure:* broken
*edges:* walk `deadfall_tangle` S; walk `grouse_thicket` W; see `deadfall_tangle`.
> Alder and young willow thread the spruce here, and the snow between the stems is
> stitched with packed runs — a whole commuter network of them, dotted with sign, nibbled
> white at the bark line. Something small and fast owns this block after dark.
**Resources & pricing.** *The snare line*: the valley's best protein-per-effort — IF the
party has wire (avionics panel, the drowned set, the marten sets) or serviceable cordage,
reads which runs are FRESH (knowledge: sharp-edged tracks, fresh droppings — examine
teaches), sets loops right (hand-width, hand-high — manual knowledge), and **leaves**. The
run pays on return visits, hours later; camping on it pays never. Snaring is the game's
purest test of the plan-ahead muscle, and its yield (a hare or two by dusk) is priced to
matter without trivializing food.
**Hazards.** None. The zone's risk is spent daylight on badly-set snares — tuition, not
punishment.

### `tree_well_hollow` — the tree-well hollow
*aliases:* tree well, well, spruce hollow, bivvy tree · *pos:* −120, 180, 2 · *terrain:*
exterior, trees, hollow · *exposure:* sheltered
*edges:* walk `big_spruce_hollow` E.
> The grandmother spruce of the whole wood stands here, boughs sweeping to the snow like a
> pitched roof, and around her trunk the snow falls away into a deep dry well — a room,
> almost, floored with needles, walled with white, already warmer than the air by the
> width of a held breath.
**Resources & pricing.** *The natural bivvy*: the no-materials warmth floor (GDD §-locked)
given a terrain form — a party caught out overnight survives HERE with boughs and body
heat and nothing else. Free to use; costs knowledge to trust (the manual's shelter page
describes exactly this) and nerve to choose over a desperate night march (the design's
mercy door, and the storm chapter's best-kept promise).
**Hazards.** *The flip side*: blundering into an unseen well while trail-breaking under
load = a floundering, sweat-soaking extraction (telegraphed: boughs-to-the-snow trees
announce wells; the look models the reading).

---

## S5 — The Strike Path (NE upslope)

The crash rewound: follow the wreck's own scar uphill through everything the plane hit,
shed, and started. Salvage country — the plane's last gifts, priced in climbing, prying,
and one genuinely dangerous liquid. Four zones.

### `shear_line` — the shear line
*aliases:* sheared crowns, strike path, cut line, the scar · *pos:* 90, 60, 6 · *terrain:*
exterior, trees, debris · *exposure:* broken
*edges:* walk ⇄ crash `tail_section` SW (down the gouge); walk `wing_in_the_trees` NE; walk
`gear_gouge` E; see crash `debris_trail` SW, `wing_in_the_trees` NE.
> The forest is beheaded in a dead-straight line here — crowns sheared at one height and
> flung downhill in a wreckage of green. The cut points back up the slope as plainly as a
> drawn arrow, and the air still smells of resin, bright and raw, as if the wound were
> minutes old.
**Resources & pricing.** *Sheared green boughs, everywhere*: the crash pre-cut a shelter's
worth of thatch and bedding — free material, but bulk-hauling it anywhere useful costs
trips (daylight) or the sled. *The arrow*: aligning the shear line with the gouge below is
the valley's free compass — the orientation knowledge that makes the ridge findable and
"which way did we come from" answerable forever after.
**Story.** Resin-smell as fresh wound: the crash happened to the forest too.

### `wing_in_the_trees` — the wing in the trees
*aliases:* wing, hung wing, the right wing, wing tree · *pos:* 170, 120, 12 · *terrain:*
exterior, trees, wreckage · *exposure:* broken
*edges:* walk `shear_line` SW; walk `bench_saddle` NE; see `shear_line`, `gear_gouge`.
> The missing wing hangs twenty feet up a big spruce, speared through the crown and canted
> like a diving board, groaning when the wind leans on it. Beneath it the snow is stained
> in a spreading blue-white rot and the air stings of avgas. Nothing about the
> arrangement looks finished.
**Resources & pricing.** *Avgas, in the tip tank*: the valley's fire accelerant and its
most dangerous convenience. Three openings, all priced: CLIMB the leaning neighbor spruce
and work the drain valve one-handed over a drop (risk + a container rigged to catch);
CHOP/FELL the carrier tree (Holt's axe + an hour of labor + the wing comes down where
physics says, not where you'd like); or RIG a catch under the existing slow drip
(container + paracord + patience — slowest, safest, cleverest: the stained snow shows
exactly where). *Wing skin & spar*: sheet aluminum (windbreak paneling, a fire platform,
a snow shovel blank) and structural tube — pry/cut work (tools + sweat) once it's down.
**Hazards.** *The groan*: the wing IS coming down someday — working directly beneath it is
announced foolishness; the stain marks the fall shadow. *Avgas near flame*: a flare-up
lesson the material system already knows how to teach — the manual says accelerant, the
first careless splash-and-light says WHOOMPF (singed, scared, schooled — survivable by
design at splash quantities).
**Story.** "Nothing about the arrangement looks finished" — the crash isn't over; the
world has unexploded parts.

### `gear_gouge` — the gear gouge
*aliases:* gouge, landing gear, wheel crater, gear leg · *pos:* 150, 40, 5 · *terrain:*
exterior, snow, wreckage · *exposure:* broken
*edges:* walk `shear_line` W; see `shear_line`, `wing_in_the_trees`.
> The right landing gear tore off here and ploughed its own small crater — a bent strut, a
> fat black tire on a bent axle, hydraulic line coiled like a cut vein, all of it half
> re-buried in kicked snow. A wheel in a forest: the eye keeps refusing it.
**Resources & pricing.** *The tire*: the visual-rescue route's secret weapon — rubber burns
with thick BLACK smoke, the one column that reads as man-made against snow-white weather
(knowledge: the manual's signals page). Getting it off the axle: unbolt (multitool +
patience + cold fingers) or cut the sidewall for strips (blade + sweat). Hauling it to the
lake: the sled or a miserable roll-and-carry (daylight). *Hydraulic line & fittings*: hose,
clamps, a threaded steel rod — repair stock (tools to strip). *The strut*: a pry bar
better than anything in the kit, if freed (unbolt/lever — a bootstrapping puzzle: use the
weak pry to free the strong one).
**Story.** "The eye keeps refusing it" — wrongness as landmark.

### `bench_saddle` — the bench saddle
*aliases:* saddle, bench, shoulder, the notch trail · *pos:* 260, 200, 25 · *terrain:*
exterior, snow, slope · *exposure:* open
*edges:* walk `wing_in_the_trees` SW; walk ⇄ ridge `krummholz_band` NE (the climb); see
`wing_in_the_trees` SW, ridge `krummholz_band` NE, a first grey glimpse of the lake W.
> The slope gathers itself into a bench here, the last easy ground before the ridge
> shoulder climbs in earnest. Uphill the trees begin to shrink and lean, all combed the
> same direction by a wind you can already hear working the high ground. Downhill, the
> whole strike path lies readable in one look — the beheaded trees, the gouge, the small
> broken cross of the plane at the bottom of its long arithmetic.
**Resources & pricing.** *The reading*: the mid-station where the climb's cost becomes
informed consent — the wind is audible, the shrinking trees show what's ahead, and the
view back is the crash's story told whole (story + orientation). No material resources:
the bench charges nothing and sells nothing; it is the place you decide.
**Hazards.** Beyond here the exposure bands go `open` → `brutal` and the look has already
said so twice. The design rule: nobody reaches the cornice unwarned.

---

## S6 — The Ridge Overlook

Elevation: the radio/beacon route's scarce resource, the map's grand reveal, and the
valley's most honest exposure math. You cannot linger, and everything up here is designed
around that clock. Four zones.

### `krummholz_band` — the krummholz band
*aliases:* krummholz, stunted trees, last trees, wind trees · *pos:* 420, 380, 70 ·
*terrain:* exterior, trees, stunted · *exposure:* open
*edges:* walk ⇄ strike `bench_saddle` SW; walk `boulder_field` N; see `bench_saddle` SW,
`boulder_field`, `the_knob` N.
> The trees give up by degrees here — spruce bent into hags and hedges, grown sideways,
> kneeling away from the wind. What little of them is dead is dry as chalk and hard as
> horn. This is the last cover on the hill and it says so.
**Resources & pricing.** *Krumm-wood*: wind-killed limbs — the driest small fuel on the
map, kept in the worst place to need it (an emergency fire HERE is possible: that's the
zone's mercy). *The last cover*: the staging shelf — leave packs, add layers, eat
something (knowledge: summit habits; the manual's exposure page) before the open ground.
**Hazards.** The look's job is the warning: past here is commitment.

### `boulder_field` — the boulder field
*aliases:* boulders, talus, rock field · *pos:* 460, 470, 95 · *terrain:* exterior, rock,
snow · *exposure:* brutal
*edges:* walk `krummholz_band` S; walk `the_knob` N; see `krummholz_band`, `the_knob`.
> Snow lies thin and lying over a shoulder of jumbled talus — every third step booms
> faintly hollow, and the spaces between the boulders are exactly ankle-shaped. Someone
> has been here before: a knee-high cairn stands against the sky with the patience of its
> kind, one grey survey stake still wedged in its crown.
**Resources & pricing.** *The cairn*: a survey benchmark — orientation (the map suddenly
has a fixed, official point; with the chart, players can place themselves in the wider
world — story: people measured this country once) and a bundle of *dry survey stakes*
wedged in and around it: straight seasoned poles — probe sticks, snare springs, splint
stock — the summit's small practical prize.
**Hazards.** *The talus*: hollow-boom telegraph; hurrying or descending loaded risks the
ankle-shaped gaps (the same lesson tussocks taught, at higher stakes). The safe line
follows the cairn-side rib — visible once looked for.

### `the_knob` — the knob
*aliases:* knob, summit, overlook, the top · *pos:* 480, 560, 120 · *terrain:* exterior,
rock, summit · *exposure:* brutal
*edges:* walk `boulder_field` S; walk `lee_cornice` NE; see — everything: the whole valley
(all Scenes' glimpse lines), the notch NE, and weather incoming from the W a full band
early.
> The hill ends in a bald rock knob and the world arrives all at once: the lake a grey
> coin westward, the wreck a matchstick cross on the white flat, the creek a stitched
> seam running south through the timber — and there, southeast on a bench above the
> creek, one right angle in a country with no others. A roof. The wind up here does not
> gust; it leans, with its whole weight, steadily, like something that has decided, and
> it is not going to get tired before you do.
**Resources & pricing.** *The view*: the cabin DISCOVERED (the map's biggest single
knowledge payout — a bearing, "follow the creek, climb at the pond"), the weather read
(storm bands visible early — the party that summits knows the afternoon's shape before
anyone else), and the whole valley placed in one legible frame. *Line-of-sight*: the
radio/ELT route's terrain — up here the handheld's static opens into voices on a lucky
band, and the §38 puzzle's elevation clue becomes physical. Priced in the climb (an hour),
the exposure clock (minutes of working time, the look promises the wind wins), and the
carry (the radio or rigged ELT hauled up the hill — the 12 kg arithmetic suddenly a
mountaineering question).
**Storm-phase beat (assessment I-1 — the second climb).** If the party ever raised
static-voices up here (or rigged the ELT), then mid-afternoon — heavy band, the worst
possible moment — the handheld crackles ONCE at valley level during a clear pocket:
"…any traffic… section… the creek…" and dies. The knob suddenly has a late-game price
tag: a second climb, in weather, against the §14 ladder closing — the northeast's
risk/reward decision staged exactly when it is priced worst. It is genuinely winnable
(the krummholz stages it, the clock is honest) and genuinely declinable (the beat adds
radio confidence, it doesn't gate rescue — GDD: no single required path).
**Hazards.** The clock IS the hazard. The design guarantee: the knob never kills anyone it
didn't warn twice on the way up.

### `lee_cornice` — the lee cornice
*aliases:* cornice, the lip, snow lip, northeast lip · *pos:* 520, 620, 118 · *terrain:*
exterior, snow, cornice · *exposure:* brutal
*edges:* walk `the_knob` SW; see `the_knob`, the notch NE (the tempting shortcut line).
> Beyond the knob the ridge runs on toward the notch under a smooth white promenade of
> snow — inviting, level, and attached to nothing. The cornice curls over the northeast
> face like a held wave; near its root a blue crack runs, and twice while you watch, the
> whole shelf answers your weight from ten feet away with a soft dropped-pillow *whumpf*.
**Resources & pricing.** None. The promenade is the shortcut that isn't: the notch (and an
imagined faster way home from the summit) lies straight ahead, across snow that is a roof
over air.
**Hazards.** *The cornice*: crack + whumpf + the look's plain anatomy ("attached to
nothing") = three telegraphs before a step is taken. Stepping out anyway is the map's one
plainly lethal choice, and it is entirely, fairly, loudly optional. The rock-line detour
back through the boulder field is always available and says so.

---

## S7 — The Birch Stand (E, the south-facing toe)

The fire-craft chapter. Birch is the north's match-book, and everything in this stand
serves ignition, ember-craft, or the reading of trees. Four zones.

### `aspen_fringe` — the aspen fringe
*aliases:* aspens, fringe, pale trees · *pos:* 300, −40, 8 · *terrain:* exterior, trees ·
*exposure:* broken
*edges:* walk toward crash `debris_trail` W (⇄ S1); walk `birch_grove` E; see `birch_grove`.
> Aspen take the toe of the slope in a pale crowd, bark green-white and cold-tight,
> printed all over at knee height with the neat double-cut of browsing teeth. A few
> standing dead among them have gone grey and light as paper lanterns.
**Resources & pricing.** *Dead-standing aspen saplings*: push-over poles — light, straight,
hand-harvestable (the ONE freely-generous wood, priced in its own softness: burns fast,
worth little as fuel — honest material math). *Punk wood*: the grey "paper lantern" snags
are dry-rotted through — soft punk that takes and HOLDS a coal for hours cupped in a tin:
the ember-carrier. FIRE BECOMES PORTABLE — the mid-game logistics unlock that changes camp
math (knowledge: the manual's fire page, or noticing a knocked-open snag smoulder). *The
browse sign*: a pointer only — the runs here thread back toward `hare_runs`; one snare
venue per wood is enough, and the fringe's job is poles and punk.

### `birch_grove` — the birch grove
*aliases:* birches, grove, paper birch · *pos:* 380, −20, 12 · *terrain:* exterior, trees ·
*exposure:* broken
*edges:* walk `aspen_fringe` W; walk `chaga_tree` NE; walk `game_trail_crossing` SE; see
`aspen_fringe`, `chaga_tree`.
> Paper birch stand through the snow in white columns, bark curling off the trunks in
> pale scrolls that shiver without wind. One big trunk lies fallen and half-buried, its
> upturned side peeling in sheets you could read by.
**Resources & pricing.** *Birch bark*: the north's fire-starter royalty — burns hot, long,
and WET (material table: ignition easy even soaked — the storm-proof flame). The fallen
trunk peels by hand in sheets (the freebie that teaches the resource); standing trunks
give more and better with a blade (tools), and stripping a full girdle kills the tree —
the world doesn't punish it, it just stays true (provenance + a scar, and the grove
remembers in prose). The grove keeps ONE job — bark, the storm-proof flame — and does it
in three grades: hand-peeled scrolls (free), blade-cut sheets (tools), and the standing
trunks' thick jacket (tools + the tree's life). The ember-carrier moved to the aspen
fringe where punk actually grows (assessment I-6); together the two zones split fire-craft
cleanly: the fringe carries flame FORWARD, the grove starts it ANYWHERE.
**Story.** Fire you can carry, fire you can start in the rain: the stand is where the
party stops re-solving ignition and starts managing flame as a supply line.

### `chaga_tree` — the chaga birch
*aliases:* chaga, conk tree, black growth, old birch · *pos:* 430, 40, 15 · *terrain:*
exterior, trees · *exposure:* broken
*edges:* walk `birch_grove` SW; see `birch_grove`.
> The oldest birch in the stand carries a black burl the size of a bread loaf ten feet up
> its trunk — crusted, charcoal-dark, wrong against all that white bark, and exactly out
> of reach.
**Resources & pricing.** *Chaga*: tinder-fungus — catches a spark (flint-and-steel class
ignition without the lighter — the backup-fire insurance policy) and smolders for hours
(the OTHER ember-carrier), plus the hot-drink loop (chaga tea — morale + warmth). Priced
as a reach puzzle with open solutions: climb (risk — birch limbs are honest but iced),
knock it down (thrown billet — the grouse skill transfers), pole it (aspen sapling +
lashed blade — the tool-making chain), or chop the trunk (axe + the tree's life —
possible, costly, remembered). Then processing: the crust yields to a blade or a rock's
edge (tools, minimal).
**Story.** The item that rewards LOOKING UP — planted after every early resource taught
looking down.

### `game_trail_crossing` — the game-trail crossing
*aliases:* game trail, moose trail, crossing · *pos:* 420, −80, 10 · *terrain:* exterior,
snow, trail · *exposure:* broken
*edges:* walk `birch_grove` NW; walk toward creek `gravel_bar_willows` SW (⇄ S8); see
`birch_grove`.
> A trench of a trail crosses the stand here, punched stride-deep by something with more
> mass than patience — willow tops browsed off man-high, and in the lee of a spruce a
> single melted-down oval of packed snow where the animal has been lying up warm through
> the storms. In the bed's packed floor, one half-buried curve of grey: bone or antler.
**Resources & pricing.** *The shed antler* (dig it from the bed — sweat, minor): a billet,
a club, a digging tine, knife-handle scales — the valley's premium tool-stock organic,
free once found (priced in the noticing). *The moose bed lesson*: heat conservation
written in terrain (bed in the lee, mass warms its floor — the same physics as the
bough-bed, taught by a better survivor). *The trail itself*: a packed, walkable seam
toward the creek — moose engineering, free to reuse (knowledge: game trails go somewhere
sensible, usually water).
**Hazards.** *The owner*: the trail is FRESH. The design keeps the moose forever offstage
(no combat system wanted) but the sign is real and the prose says *be elsewhere when it's
home* — atmosphere doing a hazard's job without mechanics.

---

## S8 — The Creek (the lake's outlet, running SE)

The travel corridor and the water chapter: liquid water, fish under ice, willow economy,
and the overflow hazard that gates the whole southern map. Five zones.

### `outlet_riffle` — the outlet riffle
*aliases:* riffle, open water, rapids, the lead · *pos:* −650, −450, −2 · *terrain:*
exterior, water, ice-edge · *exposure:* broken
*edges:* walk ⇄ lake `outlet_narrows` N (the bank route); walk `gravel_bar_willows` SE;
see `outlet_narrows` N, `gravel_bar_willows`.
> The creek comes out of the lake shallow and quick here, and quick water is stubborn: a
> black lead runs open down the middle of the riffle, smoking faintly in the cold,
> chattering over stones like the only voice left in the valley. Ice shelves lean over it
> from both banks, thin as biscuit at their lips.
**Resources & pricing.** *Liquid water, free-running*: the melting-fuel bypass — a full
container without spending a stick of firewood (the efficiency prize that funds every
other fire). Priced in approach and wet-risk: the shelf lips are announced ("thin as
biscuit"); the safe draw is prone from the gravel spit with a lashed-pole dipper or a
sleeve rolled and a held breath (knowledge + cold hands + purification still applies —
manual: even wild water wants boiling; the giardia line is authored).
**Hazards.** *The shelf lips*: kneeling on them = a plunge to the knee and the wet-boot
clock. Every telegraph is in the look.

### `gravel_bar_willows` — the willow bar
*aliases:* willow bar, gravel bar, the bar · *pos:* −500, −600, −2 · *terrain:* exterior,
brush, gravel · *exposure:* broken
*edges:* walk `outlet_riffle` NW; walk `overflow_bend` SE; walk ⇄ birch
`game_trail_crossing` NE; see `outlet_riffle`, `overflow_bend`.
> A long gravel bar splits the creek under a head-high standing crop of willow, and the
> willows are busy: runs stitched through the stems, bark nibbled to white wood, and — sit
> still a moment — small explosive bursts of snow down the bar where fat white birds
> detonate out of drifts and resettle, invisible the instant they land.
**Resources & pricing.** *Willow, in quantity*: the lashing/withe/wicker mother-lode
(blade + time — sled-load quantities exist here and only here). *Ptarmigan*: the bar's
protein — white-on-white (the perception system's showcase prey: they are VISIBLE only
when they move or to a deliberate slow examine — patience priced in cold minutes), then
the grouse rules apply (throwing stick, close approach, cleaning chain). *Rose hips*:
shriveled red-orange on thorned canes along the bar's spine — vitamin/morale food, free
but thorn-priced and never filling (honest calories again).
**Story.** The exploding-snow birds are the valley showing off: the perception ladder as
delight instead of danger.

### `overflow_bend` — the overflow bend
*aliases:* overflow, the bend, bad bend, steaming bend · *pos:* −380, −750, −3 ·
*terrain:* exterior, ice, overflow · *exposure:* broken
*edges:* walk `gravel_bar_willows` NW; walk `logjam_crossing` SE; see `gravel_bar_willows`,
`logjam_crossing`.
> The creek elbows under a cut bank here and the ice has been cheating: yellow-grey
> stains bloom through the snow cover in long tongues, a thin breath of steam stands off
> the surface in the cold, and the fresh snow over the stained patches sags, just
> slightly, like frosting over a soft spot. Under that snow is water, standing on top of
> good ice, going nowhere, waiting.
**Night/storm look.** "Dark takes the stains first. What is left is the steam — faint
grey feathers standing in your light where the bad snow breathes — and the sag underfoot
arriving a half-second after it would have helped." (Design intent: two of the three
telegraphs survive darkness; the probe still answers; the night crossing is harder, not
unfair.)
**Resources & pricing.** None — the second tuition zone, and the southern map's toll gate.
*Overflow* is the north's sneakiest hazard (water trapped ATOP solid ice, hidden under
powder — boots soak with no plunge, no drama, just wet feet a mile from fire).
**Hazards.** *Overflow*: three telegraphs (stain, steam, sag) + the probe answer (a pole
comes up WET — the definitive test, teachable). Crossing anyway = soaked boots and the
map's most instructive misery: the wet-cold debt clock, survivable exactly if the party
treats it as the emergency it is (fire NOW or the cabin FAST). The dry line: the cut-bank
shelf upslope, narrow and obvious once probed for. GDD honesty: the hazard never
randomizes — the same reads always give the same answers.

### `logjam_crossing` — the logjam crossing
*aliases:* logjam, jam, crossing, wood pile · *pos:* −260, −900, −3 · *terrain:* exterior,
wood, obstacle · *exposure:* broken
*edges:* walk `overflow_bend` NW; walk `confluence_pool` SE; see `overflow_bend`,
`confluence_pool`; the trapline's blaze tree stands on the E bank (see — the second
discovery chain to S10).
> Some old flood folded half a forest into the bend below the bluff, and the creek has
> been wearing it like a brooch ever since: a heaped silver jam of barkless trunks,
> bridging the channel bank to bank, dry as bones above the waterline and booby-trapped
> with voids below. It is a woodpile pretending to be a bridge, and both halves of that
> are true.
**Resources & pricing.** *The jam as fuel*: barkless flood-cured wood, endless, saw/axe
priced (tools + sweat) — the southern camp's fuel depot. *The jam as bridge*: the only
dry crossing between the riffle spit and the beaver dam — free, IF stepped with care.
**Hazards.** *The voids*: hollow footing under snow — the talus lesson recurring (probe,
test, unweight); a leg-through costs a wrench and a scare, not a death — the jam is
loud ("booby-trapped") and its floor is wood, not water.

### `confluence_pool` — the confluence pool
*aliases:* pool, confluence, deep pool, fishing hole · *pos:* −140, −1050, −4 · *terrain:*
exterior, ice, pool · *exposure:* broken
*edges:* walk `logjam_crossing` NW; walk ⇄ pond `dam_crossing` SE; see `logjam_crossing`,
pond `dam_crossing` SE.
> A feeder brook slides in under the east bank and the creek pauses here into a long
> black-ice pool, snow-scoured, deep enough that the light gives up halfway down. Shapes
> hang in that dark sometimes and adjust themselves — slow, deliberate, alive. The ice
> is thick, clear, and drum-tight: a floor over an aquarium.
**Resources & pricing.** *The fishery*: winter fish concentrate in pools (knowledge —
manual's fishing page or the visible shapes); the kit's line-and-hooks (AS 02.35.110
canon) + a chopped hole (hatchet/axe + honest labor through 40 cm — sweat + tool edge) +
a jig rod (willow) + bait (ration crumbs, gristle, a hare's eye — the economy composts)
+ patience (daylight in cold minutes) = burbot and grayling: the valley's only SCALING
food source — the thing that turns "surviving today" into "provisioned for the storm."
Priced accordingly: the longest tool-and-knowledge chain on the map, every link earnable.
**Hazards.** Thick ice here (the look promises: "drum-tight... floor") — the pool is safe
BECAUSE the current pauses; the reading rule (current thins / stillness thickens) pays
consistently across lake, creek, and pond by design.
**Story.** The adjusting shapes under clear ice: the valley's second wonder-beat. The
world is alive below the emergency too.

---

## S9 — The Beaver Pond

Another engineer already winters here, and did the party's woodcutting years in advance.
The pond is a masterclass zone-set: infrastructure to reuse, a larder to misunderstand,
wire to salvage, and the trailhead that makes the cabin walkable. Five zones.

### `dam_crossing` — the dam crossing
*aliases:* dam, beaver dam, crossing, the causeway · *pos:* 0, −1250, −4 · *terrain:*
exterior, wood, dam · *exposure:* broken
*edges:* walk ⇄ creek `confluence_pool` NW; walk `pond_flat` E; walk `drowned_set` S; see
`pond_flat`, `the_lodge`, `drowned_set`.
> A beaver dam holds the feeder brook in a pond here — a woven causeway of mud and
> gnawed poles, chest-high, snow-capped, solid as government work. Below its downstream
> toe the spill keeps one black slot of water open all winter; above it the pond lies
> flat and white to the far bank. The dam top is packed with prints: everything in the
> valley crosses here.
**Resources & pricing.** *The causeway*: the dry bridge to the trapline side — free
passage, the pond's gift (and everything-crosses-here is snare intelligence for the
reading player). *Dam poles*: pre-cut, pre-peeled, tug-or-hack free (minor tools) —
BUT pulling structure from the dam's working face drains the pond by degrees (the world
stays systemic: the spill slot widens, the prose registers the vandalism, the lodge's
vent goes quiet — consequences in provenance and story, not fines). The polite harvest
is the loose tail of poles below the spillway.
**Hazards.** *The spill slot*: open black water, plainly visible, undercutting the snow
lip nearest the toe — announced, avoidable, the pond's one wet mistake.

### `pond_flat` — the pond flat
*aliases:* pond, pond ice, the flat white · *pos:* 120, −1300, −4 · *terrain:* exterior,
ice, pond · *exposure:* open
*edges:* walk `dam_crossing` W; walk `the_lodge` NE; walk `food_cache_margin` N; see all
S9 zones.
> The pond lies still under cleaner ice than the lake ever manages — black glass in
> wind-swept panes, and locked into it a museum of small silver bubble-trails, each one
> the frozen breath-line of something that swam here after freeze-up and knew where it
> was going.
**Resources & pricing.** *The bubble-trails*: pure wonder, and a map — the trails
converge on the lodge and the food cache (knowledge: the pond explains its own
residents to anyone who reads the ice).
**Hazards.** Margins near inflow and spill are thinner (the standing rule: current
thins); the centre is sound. The lake's ice-reading lessons transfer verbatim — by now,
mid-map, the party is expected to know, and the prose stops repeating the tutorial.

### `the_lodge` — the lodge
*aliases:* lodge, beaver lodge, the mound · *pos:* 220, −1260, −3 · *terrain:* exterior,
ice, lodge · *exposure:* open
*edges:* walk `pond_flat` SW; see `pond_flat`, `food_cache_margin`.
> The lodge humps out of the ice like a shaggy kiln — a fortress of mud and crossed
> sticks frozen to the hardness of poured concrete, vented at the crown by one small
> chimney of frost-feathered breath-steam, rising, pulsing faintly. Somebody is home,
> and their walls are better than yours.
**Resources & pricing.** *The steam-vent lesson*: warmth made visible — mass + insulation
+ bodies = a livable core at −20°, the whole shelter chapter taught by a rodent
(knowledge, free, and the design's thesis miniaturized). *The temptation*: hacking in is
POSSIBLE (axe + an hour against frozen masonry) and designed to be a bad trade — a
wrecked wall, scattered residents, a handful of nothing (the lodge stores food in the
water, not the walls) — the world's one deliberate anti-loot lesson: not every
interactable is a resource, and the prose will remember the vandalism all game.
**Story.** The valley's best shelter belongs to its calmest resident. Players who get it
laugh; players who don't get a wall's worth of nothing, honestly priced.

### `food_cache_margin` — the food-cache margin
*aliases:* food cache, green butts, feed pile, larder margin · *pos:* 180, −1180, −4 ·
*terrain:* exterior, ice, cache · *exposure:* open
*edges:* walk `pond_flat` S; see `the_lodge`, `pond_flat`.
> Off the lodge's doorstep a raft of green cut brush stands frozen into the ice, butt
> ends up — willow and aspen jammed downward in businesslike rows, the whole thing the
> size of a hay wagon. It is a larder: somebody spent all autumn laying in groceries
> under a lid of glass.
**Resources & pricing.** *Green pole stock*: chop the exposed butts free (axe/hatchet +
sweat) — withes and poles in quantity WITHOUT touching the dam (the ethical harvest the
dam zone hinted at). *The green-wood lesson*: it barely burns (material truth — hissing,
smoking failure, authored honestly) — its value is structure, lashings, and bait, and
the party learns fuel-vs-material as a distinction with a hiss. *Bark bait*: fresh
aspen inner-bark — the snare-line's upgrade bait (knowledge: bait a run, double the
take).
**Hazards.** The cache sits over the pond's second-thinnest ice (the residents keep
their pantry near deep water on purpose) — chop from the flat side, not the lodge side;
the bubble-map already drew the line for anyone who read it.

### `drowned_set` — the old drowned set
*aliases:* drowned set, old trap, wire set, trapline end · *pos:* −40, −1350, −4 ·
*terrain:* exterior, ice, bank · *exposure:* broken
*edges:* walk `dam_crossing` N; walk ⇄ trapline `blaze_gateway` SE; see `dam_crossing`,
the blazed shore tree SE.
> Under the dam's toe, half in the frozen spill-pool, a human thing: a slide-pole set,
> years old — a lever of grey lumber, a rusted jaw of a trap on a chain staple, and
> yards of good snare wire wrapped and rewrapped up the pole with a trapper's tidy
> impatience. On the bank spruce above it, two old axe blazes stacked like a colon,
> pointing away southeast into the timber.
**Resources & pricing.** *Snare wire, in yards*: the protein economy's missing tool,
free of the plane (players who hated cannibalizing the avionics get their reward here) —
unwrap it (cold fingers + patience), and the snare-line game opens fully. *The trap*:
rusted solid — a chain, a staple, steel plate stock (parts, not a working trap: the
mechanism is honestly dead). *The blazes*: THE TRAPLINE DISCOVERED — the second and most
practical chain to the cabin (map.md §4).
**Story.** First human sign beyond the wreck. Someone works this country, competently,
and went home. The colon of blazes is a sentence that continues.

---

## S10 — The Trapline

Holt's commute: a blazed, wind-proof corridor through black spruce — the storm-safe route
SE, the navigation tutorial, and the map's quietest storytelling. The trail only works if
you learn to read it, and the storm will examine you on it later. Four zones.

### `blaze_gateway` — the blaze gateway
*aliases:* blazes, trailhead, gateway, shore tree · *pos:* 60, −1420, −2 · *terrain:*
exterior, trees, trail · *exposure:* broken
*edges:* walk ⇄ pond `drowned_set` NW; walk `spruce_tunnel` SE; see `drowned_set`, the
next blaze SE.
> The doubled blaze on the shore spruce has healed to grey lips around bright old wood,
> and once your eye takes the pattern the forest quietly reorganizes: there, at the
> edge of seeing, another tree wears the same two pale marks, and the snow between runs
> just faintly dished, a seam of old passage under the fresh white. It isn't a trail so
> much as a sentence in a language of exactly one word, repeated all the way to
> somewhere.
**Resources & pricing.** *The system itself*: blazes face the walker; each is visible
from the last (knowledge — the zone look TEACHES the protocol, because the storm will
later test it closed-book). Nothing material. The gateway's job is to install a skill.
**Story.** "A sentence... repeated all the way to somewhere" — the trail as promise.

### `spruce_tunnel` — the spruce tunnel
*aliases:* tunnel, black spruce, dark stretch, the corridor · *pos:* 260, −1560, 4 ·
*terrain:* exterior, trees, dense · *exposure:* sheltered
*edges:* walk `blaze_gateway` NW; walk `marten_set_tree` SE; see one blaze back, one
blaze ahead (deliberately: the tunnel's see-range IS the blaze interval).
> Black spruce close over the trail here in a dark, snow-stuffed nave — trees thin as
> fence posts and packed like them, boughs meshed overhead so the day arrives
> secondhand. The wind, for once, is somewhere else entirely; snow stands on every
> twig, unbothered, in absolute administrative silence. One blaze glimmers behind you.
> One waits ahead. Between them the world is twelve feet wide.
**Night/storm look.** "The tunnel does not know about the storm. Snow sifts through the
mesh overhead in single flakes, one blaze soaks up your light and gives back a wet grey
gleam, and somewhere above the boughs the wind is tearing the valley apart in another
country." (Design intent: the corridor's exposure stays `sheltered` at every weather
band — the trapline is the storm's one open road, and its night prose should feel like
being indoors in a hallway of the outside.)
**Resources & pricing.** *Shelter-in-motion*: the corridor is `sheltered` for its whole
length — the ONLY long move on the map that stays cheap in heavy weather (the
storm-phase ace, priced in advance: you must have LEARNED the trail while learning was
easy). *Dry black-spruce twigs*: fence-post trees die standing here — kindling picked
in passing, an armload per transit (the commuter's habit, taught by mention).
**Hazards.** *Losing the thread*: leave the blaze interval (a shortcut urge, a dropped
mitten chase) and the tunnel's sameness closes like water — the one zone where being
lost is modeled INSIDE the zone (finding the dished seam or backtracking your own prints
recovers it; panic walking does not). A drifted blowdown mid-tunnel forces the one
detour — around it, the next blaze is NOT visible until the trail is refound (the test,
placed mid-course, with the answer one careful circle away).

### `marten_set_tree` — the marten-set tree
*aliases:* marten set, leaning pole, set tree, the box · *pos:* 420, −1680, 10 ·
*terrain:* exterior, trees, trail · *exposure:* sheltered
*edges:* walk `spruce_tunnel` NW; walk `cabin_gate` SE; see the trail both ways.
> A pole leans against a big spruce at a careful angle, and halfway up it a little
> roofed box is nailed — a marten set, baited and wired with the same tidy impatience
> as the drowned set below. Ice has sealed the box mouth shut; a fan of frost feathers
> grows on the wire. In the box's dark, a small shape, hunched, still, weeks past
> caring.
**Resources & pricing.** *The marten*: frozen in the set — a rich fur scrap (mitt
liners, a hood ruff — a real, small warmth upgrade) behind a chain of small gates:
notice the box (perception), free the iced mouth (pry/thaw — minor), then skin it
(blade + knowledge + stomach — the cleaning skill's advanced exam; botching it wastes
the fur honestly). *More set wire*: each set on the line carries yards (the line has
three sets; the design places one on-trail, hints the others off it for completionists).
*The read*: ice-sealed = untended for weeks = the cabin is EMPTY — the trail tells you
what you'll find before you arrive (knowledge as spoiler-mercy, so the cold hearth
lands as confirmation, not ambush).
**Story.** Holt's craft, twice now. The player arrives at the cabin already knowing the
man — tidy, impatient, competent, gone.

### `cabin_gate` — the cabin gate
*aliases:* bench top, trail top, the gate, clearing edge · *pos:* 560, −1780, 22 ·
*terrain:* exterior, trees, edge · *exposure:* broken
*edges:* walk `marten_set_tree` NW; walk ⇄ homestead `dooryard` SE; see homestead
`dooryard`, the cabin roof, the cache poles.
> The trail climbs the last of the bench and stops being a wilderness thing: the
> timber opens on a small cleared shoulder of land, stumps under snow-caps in mown
> rows, and across the clearing a low log cabin sits shuttered under a foot of
> unbroken white. No light. No tracks. And over the roof, from a stovepipe crooked as
> a beckoning finger — no smoke. The word you have been carrying up the whole trail
> arrives anyway, and it is *empty*.
**Resources & pricing.** None — the threshold zone. Its whole cargo is the beat.
**Story.** Hope, correction, and a door anyway: the storm chapter's shelter is real
even if the rescue-fantasy version of it (lights, smoke, a radio, a person) is not.
The marten set threw this punch in slow motion; here it lands.

---

## S11 — Holt's Homestead

The second dense node: the endgame's shelter, the map's biggest material payoff, and a
portrait of its absent owner in tool-marks and habits. Everything here is EARNED —
drifted, latched, cached, or up a pole — but the earning is craft, not cruelty. Seven
zones.

### `dooryard` — the dooryard
*aliases:* yard, clearing, dooryard, front of the cabin · *pos:* 700, −1850, 24 ·
*terrain:* exterior, snow, clearing · *exposure:* broken
*edges:* walk ⇄ trapline `cabin_gate` NW; walk `porch` E; walk `woodshed` S; walk
`cache` SE; walk `water_hole_path` N; see everything in S11.
> The dooryard lies under snow that nobody has argued with all winter: one smooth
> blank page from stump-row to door. Shapes wait under it — a long mound here, a
> squat one there — and a wire runs post-to-post across the yard at knee height,
> humming very slightly in the wind, going nowhere anyone can see. The whole place
> has the held-breath tidiness of a room left by someone who expected to be back.
**Night/storm look.** "The yard at night is shapes and the memory of shapes: the cabin a
harder black, the cache on its legs against the sky like a wading bird asleep, your own
trench of tracks the only line the storm hasn't finished arguing with. The door is twenty
steps of wind away." (Design intent: arrivals AFTER dark — the likeliest case for
first-time expeditions — get an approach that is findable [the trapline delivers you to
the gate, the yard is small] but earns its relief; the porch dune by lamplight is the
night's last honest labor.)
**Resources & pricing.** *The buried shapes*: a chopping block (the long mound: a
sawbuck) — infrastructure, not loot; dig to use (sweat, minor). *The dog-run wire*:
yards of braided cable between posts (unwind: patience + cold fingers) — heavier stock
than snare wire: hanging chains, sled tow-line, the ELT antenna's best donor (the
radio route reaches even here — the map's economies interlock at the far end too).
**Story.** "Expected to be back." The yard is the note before the note.

### `porch` — the porch
*aliases:* porch, door, front door, stoop · *pos:* 730, −1850, 24 · *terrain:* exterior,
wood, porch · *exposure:* broken
*edges:* walk `dooryard` W; walk `cabin_interior` E (once cleared); see `dooryard`.
> The porch is a cave of drift: snow packed shoulder-deep against the door in one
> smooth wind-built dune, hard enough to hold a boot-print like plaster. Under the
> eave, out of the weather, a pair of empty nails wait at shovel height — the shape
> of the tool that should hang there, and doesn't.
**Resources & pricing.** *Entry, the front way*: dig the dune — bare-handed or with
improvised scoops it is a LONG sweaty job (the sweat debt made vivid: strip layers or
soak them — the manual said so); with the woodshed's shovel it is ten minutes (the
design's loop: the yard rewards a lap of scouting before brute force — the empty nails
are the hint, aimed at the shed). *Entry, the side way*: a shuttered window (pry —
tools; smaller, faster, and it BREAKS something the storm will want intact — a real
trade, priced in later drafts and the prose's memory).
**Story.** The empty nails: Holt's habits keep teaching even in absence.

### `cabin_interior` — the cabin
*aliases:* cabin, inside, one room, Holt's cabin · *pos:* 760, −1850, 24 · *terrain:*
interior, wood · *exposure:* sheltered (with the stove lit: the map's ONLY `warm`)
*edges:* walk `porch` W; walk (ladder) `loft` up; see `loft` (open joists).
> One room, and the room is a man: a bunk boxed in the corner under a mounded quilt,
> a plank table wiped clean, a shelf of tins squared to the edge like soldiers, traps
> and spare hinges on wall nails in size order — and holding the centre of everything,
> a squat black wood stove on a gravel pad, door shut, dead cold, with kindling
> already split and laid in the box beside it. The cold in here is different from
> outside: still, patient, museum cold. The stove is the argument the whole room is
> making.
**Resources & pricing.** *THE STOVE*: shelter's endgame — a contained, chimney-drafted,
cook-topped fire that turns the storm into weather (fuel still wanted: the shed's
wood is the other half of the promise; lighting it is the whole fire chain one last
time, indoors, almost easy — the game's earned victory lap). *The shelf*: flour, salt,
lard, tea, a few tins — real staples (the mouse tax has opened two packets — honest
attrition); ONE bulged can among the good ones (botulism — the examine-gated poison
lesson: the manual's food page names the bulge; eating it unexamined is the map's one
slow self-inflicted wound). *The lamp*: kerosene, half a jug — LIGHT after dark, the
night-phase resource nothing else provides (priced: finite, and the jug is also the
avgas-safe fire helper). *The note on the table*: "Gone to Galena til breakup. Wood
in the shed, leave the box full. — V.H." — story, permission, and the country's law
of the open cabin in one breath (and "leave the box full" is quietly a QUEST: the
world's etiquette asking to be honored by players who have taken everything else).
**Story.** The GDD's "cabin + wood stove" promise, kept — and the room characterizes
rescue itself: survival out here has always been people leaving doors unlocked for
each other.

### `loft` — the sleeping loft
*aliases:* loft, upstairs, sleeping loft · *pos:* 760, −1850, 27 · *terrain:* interior,
wood, loft · *exposure:* sheltered
*edges:* ladder `cabin_interior` down; see `cabin_interior`.
> The loft is a triangle of trapped air under the ridgepole, floored with rough
> boards and one narrow tick mattress. A cedar trunk sits at the gable end with a
> horse blanket folded on its lid — and from a nail on the king post hangs a rifle
> with its bolt drawn and carried away to town, which out here is not distrust, just
> housekeeping.
**Resources & pricing.** *The trunk*: wool — union suits, socks, a sweater with mouse
holes (grading: warmth values reduced but real — the clothing system's jackpot,
priced by distance and the whole journey here). *Quilts/blankets*: bedding for the
storm night, or cloak-class wearables (DR-25 covers them). *The boltless rifle*:
story furniture ONLY (the bolt is in Galena — firearms stay out of scope by the
owner's own habit; a box of .22 shells on the sill is flagged for Andrew: powder as
fire-starter lore vs. cutting it — decide at content pass).
**Story.** The drawn bolt: competence and trust in one image; the design dodges the
weapon system diegetically.

### `cache` — the raised cache
*aliases:* cache, food cache, the little house on legs · *pos:* 800, −1880, 28 (floor
+4 m) · *terrain:* exterior, wood, cache · *exposure:* broken
*edges:* walk `dooryard` NW; see `dooryard`, `woodshed`.
> Behind the cabin a miniature house stands on four peeled poles a man's reach and a
> half off the ground, each pole wearing an upturned tin skirt — flashing to break a
> marten's stride, or a squirrel's, or anything's with claws and ambition. The ladder
> that belongs to it is nowhere in sight; the little door up there is latched with a
> simple wooden toggle, ten feet of empty air below it, laughing quietly.
**Resources & pricing.** *The climb problem*: the ladder is stashed UNDER THE CABIN
(classic practice — visible as pole-ends from the dooryard with a stoop and a look:
perception pays again); alternatives all work and all cost — shoulder-stand (co-op's
signature move: this cache opens EASIER with two people, by design), pole-and-toggle
fishing (the chaga skill transfers), or building a stump-stack (sweat + time).
*Inside*: the deep stores — beans, rice, a slab of dry fish, candles, a tarp, a coil
of good rope, AND the two crown jewels: **snowshoes** (the mobility upgrade — map.md's
travel table third column turns on) and **a full-size felling axe, sharp, hafted,
oiled** (the tool that re-prices the drift log, the deadfall, the burn — the fuel
economy's endgame key). Priced in: the whole journey, the climb, and the going-back
(everything up here must come DOWN the same ten feet and 2.4 km home — logistics to
the last).
**Story.** The tin skirts: Holt versus every climbing thief in the country, and now
versus the players — who win only by being cleverer than a marten, which the game
should absolutely narrate if a shoulder-stand collapses.

### `woodshed` — the woodshed
*aliases:* shed, woodshed, wood pile · *pos:* 740, −1900, 24 · *terrain:* exterior,
wood, shed · *exposure:* broken
*edges:* walk `dooryard` N; see `dooryard`, `cache`.
> Three walls, a shed roof, and wealth: split spruce and birch stacked to the eaves
> in courses straight enough to check a level against, a chopping stump with an
> orange-handled splitting maul left buried mid-swing, a bucksaw hung on pegs, a
> long-handled shovel — and leaning in the corner, a freight sled with one runner
> split and wired badly, waiting for a better repair than its owner had time for.
**Resources & pricing.** *Dry split wood, a WINTER of it*: the fuel problem solved —
at 2.4 km's distance (the hauling problem IS the puzzle: burn it here in the stove
[the shelter answer] or move mass to the crash/lake [the signal answer] — the sled
decides which futures are affordable). *The shovel*: the porch dune's ten-minute key,
the snow-block tool, the dig-everything upgrade. *The bucksaw + maul*: the processing
suite (the maul's mass also frees the strut, cracks the lodge — the map's heavy
argument). *THE SLED*: one split runner — the repair loop's masterpiece (splint stock
[survey stakes / aspen], lashing [wire / withes / paracord], glue [spruce pitch,
warmed] — three economies converge); repaired, it moves 10× a back-load and makes
the wood, the tire, the batteries, the stores all PORTABLE. The map's last lock, and
every key for it was planted somewhere behind.
**Story.** The maul mid-swing: the whole homestead in one image — interrupted, not
abandoned.

### `water_hole_path` — the water-hole path
*aliases:* water hole, creek path, water trail · *pos:* 700, −1800, 20 · *terrain:*
exterior, snow, path · *exposure:* broken
*edges:* walk `dooryard` S; see `dooryard`.
> A packed path — the only made thing under all the yard's snow — drops off the
> bench's north lip toward creek-sound, ending at a low plank lid weighted with a
> stone. Under the lid, a chopped basin in the creek ice, skinned over thin from
> disuse, and hanging from a lean-pole above it, a dented dipper can turning slowly
> on its wire like a small patient moon.
**Resources & pricing.** *The water hole*: Holt's infrastructure — break the thin
skin (trivial) and the homestead has bucket-water without the riffle's risks (the
reward for the cabin route made concrete in chores). *The path itself*: the lesson
that a homestead is a SYSTEM — wood, water, food, warmth in a fifty-yard circle —
the design's closing statement of everything the crash site wasn't.
**Story.** The dipper turning on its wire: the last image of the man who isn't here,
still handing you the cup.

---

## Cross-cutting design tables

### Exposure bands (P5 seam input)
`sheltered`: big_spruce_hollow, tree_well_hollow, deadfall_tangle, grouse_thicket,
spruce_tunnel, marten_set_tree, cabin_interior (+stove → `warm`), loft ·
`broken`: most forest/brush/bank zones (see entries) · `open`: muskeg flats, lake
apron/ridge/inlet/outlet, pond flats, krummholz, bench_saddle ·
`brutal`: ice_flat, boulder_field, the_knob, lee_cornice, fuselage_top.

### The hazard family audit (every one telegraphed ≥2 ways)
tussock ankles (look + stumble) · deep drift (look + probe) · thin ice (stain + dark
ice + drum) · current ice (snow-free tongue + knowledge rule) · overflow (stain +
steam + sag + wet probe) · logjam voids ("booby-trapped" + hollow foot) · talus
(hollow boom + ankle-gaps line) · cornice (crack + whumpf + anatomy in prose) ·
widow-maker (named + creaking) · wing fall-shadow (groan + stain) · avgas flare
(smell + manual) · botulism can (bulge + manual) · exposure clocks (every look on
the brutal zones says so).

### The ≥2-openings audit (every gate)
avgas (climb / fell / rig-catch) · cache (ladder-hunt / shoulder-stand / pole-toggle
/ stump-stack) · porch (dig hard / shovel easy / shutter pry) · chaga (climb / throw
/ pole / chop) · fish (only long chain — but its links each have multiple sources:
hole [hatchet or axe or maul], rod [willow or stake], bait [three+ sources]) · sled
runner (stakes/aspen × wire/withes/cord × pitch) · cabin discovery (chart / knob /
blazes / pilot) · water (riffle / melt / blue ice / shore lead / water hole) ·
fire-start (lighter / matches-dried / birch bark / chaga-spark / avgas-assist).

### Timed beats as WORLD events (assessment I-4 — never a silent no-op)
The GDD's 2–3 timed beats must land on every party, wherever it stands:
- **The search plane (midday band)**: the engine-drone is audible VALLEY-WIDE
  (AUDIBLE_ONLY at minimum, with direction — "an engine, small and high, west") in
  every exterior zone and, muffled, inside the wreck and the cabin. Parties on the
  lake with smoke up get the confidence event; parties elsewhere HEAR their
  allocation choice cost them, in the moment, with a bearing — the gut-punch teaches
  only if it is witnessed.
- **The radio voice (heavy band)**: one valley-level crackle (the knob's second-climb
  invitation — see `the_knob`) — audible to whoever carries the handheld, wherever
  they carry it.
- **The pilot's last lucid line (timing set by the medicine loop)**: delivered
  wherever HE is — and the design assumes parties may move him (a drag litter of
  paneling and cord: possible, priced in sweat and gentleness). The line reaches
  whoever stayed close; care is rewarded with information, absence with silence.

No beat requires standing in the right room; every beat is perceivable from every
room; the difference in what you can DO about it is the game.
