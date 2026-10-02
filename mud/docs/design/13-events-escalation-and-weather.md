# 13 — Events, escalation and weather: the ladder, the event deck, weather, endings

> **Status: reviewed with Andrew 2026-09-28.** Architecture counterpart: none yet — no `docs/architecture/events.md`
> exists; the closest entries are DR-12 (determinism and seeding) and DR-15a (the week-long run, the
> escalation ladder, no hard time barriers) in
> [`implementation-architecture.md`](../architecture/implementation-architecture.md). **This document
> owns the week's weather and daylight numbers (§4.2); every other document refers here for them.**

## 2. Decisions

### Andrew's decisions
- **(2026-09-07)** A run is roughly a week. There are no hard time barriers: instead, the things that
  cause death increase over the days. There is no set arc; what to do is the players' decision. Events
  are planned.
- **(2026-09-17)** The pilot starts the run dead. The only endings are rescued or dead; walking out is
  not an ending and Holt's cabin is supplies. Rescue comes three ways (document 14 §3), and the flyover
  schedule is its clock. Dangerous places injure but never kill outright; fitness matters; a seeded
  dice roll, announced. No wolverine.
- **(2026-09-18, via document 08)** The night-one rule: night one is survivable inside the wreck in the
  clothes the party crashed in; from night two they need a heat source, better gear, conserving or
  huddling. The ladder's first rungs are tuned until both halves hold (document 08 §4.1a).
- **(2026-09-26)** A bear is in. The bear, some bigger animals and a few birds act, on the engine's behaviour rules or
  played by a lightweight model from outside, only a few at once; as many of an animal in a room as is
  realistic, and birds not constantly calling; no wolves (2026-10-01); the fish are scripted; other wildlife shows as events and sign. A combat system like a
  MUD's is in.
- **(2026-09-26, 2026-09-27)** The season is **the first week of October in interior Alaska** (Claude's
  choice, at Andrew's request, for more than ten hours of daylight; kept over an earlier date so every
  night stays below freezing). **No big storm** — sitting one out in the plane, unable to make a fire,
  would not be fun. Bare, icy ground at the start; snow on and off, building to a couple of inches by
  the end, so a fire can be kept going outside and the world stays open; **a heavier flurry the day
  before the end, which clears**. The sky is always at least partly cloudy: planes fly most days, but
  the wreck is hard to see from the air. **The same weather every run.**
- **(2026-09-27)** **The escalation comes from the cold and the land** — the nights colder through the week, the low
  forage covered a little at a time, the near wood used up, the body's own clocks, the bear growing
  bolder — and **the day-6 flurry is the finale**, telegraphed on day 5, clearing into the coldest
  night of the run before the day-7 plane (§4.2).
- **(2026-09-28)** **The event deck** is §4.3's, as proposed, with these: the bear's sign lies in its
  own area, not spread everywhere, and is plain on entering it — nobody has to examine the ground in
  every room; no claw marks on the wreck (the party would see and hear the bear); no snared hare found
  waiting; no chainsaw — nothing promises people within walking distance.
- **(2026-09-28)** **Weather is state** — real quantities that change every minute, one air mass over
  the valley, and each zone's snow, ice and frozen ground its own (§4.7).
- **(2026-09-28)** **How an event runs** is §4.4's, as proposed: a line crossed in the weather's
  state, an arrival, or a scheduled happening; danger warns first and physics decides; escape is never
  authored per danger.
- **(2026-09-28)** **The week's day-by-day numbers** are §4.2's table, as proposed: the cold rising
  steadily with one sharp drop after the day-6 flurry, and the search closing in day by day.
- **(2026-09-29)** **The game ends on day 7**: the rescuers find everyone still alive. The last 24 hours
  before it are the hardest of the run, so the early ways home are worth the work (§4.2, §4.5).
- **(2026-09-27)** The flyovers are the same every run; the rest
  of the flyover schedule is Claude's, at Andrew's request (§4.2's search row, kept 2026-09-28).
- **(2026-09-17, 2026-09-27)** The clock runs at 15 game-minutes per real minute; fast forward,
  proposed and agreed by the players, runs it at about 150×; awake players can stay in it and type a
  command to slow it. A player waking or any non-ambient event drops it back to 15×; ambient events
  do not (document 06).
- **(2026-09-27)** **Nothing kills instantly:** death comes by the body running down — blood loss, the
  cold, thirst and the rest — on real clocks, with time to respond; the bear kills through the bleeding
  it causes. Poison makes people very sick but never kills (document 11 §4.6). Dead players are ghosts; there
  is no recap.

### Proposals (Claude)
Every number is a real starting point, from the interior-Alaska sources under §4.2, and playtesting
tunes it. What is built first (§4.6) waits for the implementation plan.

## 3. In one paragraph

A run has no clock ticking down to failure and no scripted plot: the world clock keeps running while
a day-indexed calendar turns colder, snowier, hungrier and more dangerous underneath it, whether the
party is asleep, working or doing nothing. It starts gently — the first of October, bare ground white
with frost at dawn, the berries still on the bush, skim ice at the pond edges, a first night near
freezing — then snow on and off through the week, the nights colder through the week, the low forage going under a
little at a time and the near wood burnt, until a heavier flurry on day 6 that clears into the coldest
night of the run. Nothing on the ladder ever refuses the party outright — it just makes staying alive
cost more every day — and the sign of what is coming (a ring round the sun, tracks, calls, a groan
from the fuselage) arrives before the thing itself. The weather
and the flyovers are the same in every run. Events — the weather crossing a line, the search, the
wreck settling, the pilot's body changing — fire when their day and their preconditions line up; the
bear and the other animals that act do so on their own. The run ends two ways:
**rescued** — by the radio, by a signal a search plane sees, or on day 7, when the rescuers find
everyone still alive — or **dead**.

## 4. The design

### 4.1 The two clocks (what "a week" means)
- **The world clock** runs continuously (DR-14) at 15 game-minutes per real minute. Fast forward,
  proposed and agreed by the players, runs it at about 150×; awake players can stay in it, seeing
  events go by faster, and type a command to slow it when they want to act. A player waking or any
  non-ambient event drops it back to 15×; ambient events do not (document 06). A week of game time is
  one sitting of two or three hours, which the players can pause and return to. A party that keeps
  busy pays for it in cold.
- **The escalation calendar** is indexed by game day, not by real time: the world gets harder on its
  own schedule whether the party acts or sleeps.

### 4.2 The escalation ladder (the same every run, telegraphed, no barriers)

*(Andrew, 2026-09-27 and 2026-09-28 — the shape and the day-by-day numbers.)* The run
is the first week of October in an interior-Alaska side valley at about 64–65° N: **day 1 is
1 October and day 7 is 7 October.** The reference station is Fairbanks (64.8° N), the interior's long
record; every number below comes from real data first and is tuned by probes after. **The shape is
Andrew's: no big storm — bare, icy ground at the start, snow on and off building to a couple of inches
by the end, a heavier flurry on day 6 that clears for day 7, the sky always at least partly cloudy,
more than ten hours of daylight all week, and the same weather in every run.**

**What this week really is: a normal first week of October.** At Fairbanks the first trace of snow
comes on 21 September on average and the first inch on 9 October, about 4 cm has normally fallen by
7 October, and the snow that lasts the winter settles in on 16 October. So bare, frosty ground on
1 October, flurries through the week and a couple of inches by the 7th is simply what the week
usually is. The normal days are mild — a high of +7 °C and a low of −2 °C on 1 October, +4 °C and
−4 °C on the 7th — and every night is below freezing. A partly cloudy sky keeps the nights from the
deepest drops; the clearing after the day-6 flurry lets the ground lose its heat to the sky over fresh
snow and gives the coldest night of the run, coldest on the valley floor, where the cold air pools.

**The cold and the land are the escalation** (2026-09-27). Nothing pins the party in the plane: a fire
works outside all week, and the world stays open to them. What rises instead is the cold — the nights
colder through the week, a cloudy night a few degrees warmer than a clear one — and the land closing: each flurry covers more of the low forage, the near
deadfall is burnt, so every armful is a longer walk, and the ground freezes a little deeper each night.
The body's own clocks run underneath (wounds infect on days 2–4, hunger bites, sleep debt builds), and
the bear grows bolder as the camp starts to smell of food. **The heavier flurry on day 6 is the
finale**, telegraphed on day 5 by a ring round the sun and the altimeter in the dead cockpit creeping up
as the pressure falls, so the party has a goal: wood under cover, the plane sealed, the signal ready.
It snows most of day 6 and nothing flies; it clears overnight into the coldest night of the run; and
the day-7 plane flies in clear air over fresh snow, where only what the party has built stands out.

| what rises | day 1 | day 2 | day 3 | day 4 | day 5 | day 6 | day 7 | how it hurts |
|---|---|---|---|---|---|---|---|---|
| **daylight** | sunrise 07:59, sunset 19:21 (Alaska daylight time): 11 h 22 min; civil twilight adds about 45 minutes at each end, so nearly 13 hours to work by; the sun about 22° high at noon (13:40) | 11 h 15 min — about 6½ minutes less each day | 11 h 08 min | 11 h 02 min | 10 h 55 min | 10 h 48 min; the flurry makes midday dim | 10 h 42 min (sunrise 08:18, sunset 18:59); the noon sun about 20° | every job outside fits between first and last light |
| **cold** — the valley floor, day / night | +6 °C / −2 °C — partly cloudy; the first night near freezing | +4 / −6 — frost on everything | +2 / −4 — cloudier; the flurries hold the night up | +3 / −7 — a clearer night | +1 / −5 — the cloud thickening late | 0 / −11 — the flurry by day; it clears through the evening into the coldest night of the run, an inversion: the lake shore and the muskeg coldest, the bench and the ridge several degrees warmer | −2 / −9 — partly cloudy and calm over fresh snow | the warmth math (document 08): night one survivable inside the wreck in the clothes they crashed in; from night two, not without a heat source, better gear, conserving or huddling |
| **snow, wind and sight** | none; partly cloudy; a light wind | partly cloudy; a few wet flurries in the afternoon, a dusting in the shade by dusk | cloudier; flurries on and off through the day, about 1 cm, wet, melting where the sun reaches | partly cloudy; a morning flurry, then sun breaks | partly cloudy, then thickening high cloud late and a ring round the sun — heavier snow within a day; flurries by night | **the heavier flurry** (Andrew): steady snow from the early hours through the afternoon, about 3–4 cm; at its heaviest a few hundred metres of sight in the open; an east wind of 15–25 km/h; it clears through the evening | partly cloudy and calm — the best air of the week for being seen | wet flurries soak what they land on; wind multiplies exposure; on day 6 sight and sound close in (document 19's bands) and nothing flies; smoke and a mirror work best in the calm air after |
| **snow on the ground** | bare — hoarfrost at dawn, frozen puddles, the ground icy until the sun reaches it | a dusting in the shade; bare in the sun | about 1 cm in the open, wet; the first tracks | 1–2 cm, patchy: the sunny bench bare by afternoon, the spruce floor and the north slopes white | about 2 cm | about 5 cm by night — a couple of inches; the lowest mats (bog cranberry, bearberry) go under, and lowbush cranberry pokes through | about 5 cm, settling; crisp tracks — the best tracking snow of the run; the white wreck on white ground | forage goes under a little at a time; the fresh snow shows every track; after day 6 the wreck no longer stands out by itself — the signal has to |
| **ice** | frozen puddles; skim ice at the pond edges and in the lake's calm bays at dawn, gone by noon; the lake open; the creek running | the small ponds and the muskeg pools skin over at night (about 1 cm — it holds nothing; a skipped stone rings on it), melting back by day | the skin barely grows under cloud; slush in the creek's eddies | the clearer night thickens the pond skins; shelf ice at the creek's edges | pond ice about 2–3 cm | the flurry lies on the pond ice and slows it | the cold night grows it: about 3–5 cm on the small ponds; the lake skins over in its bays and along the shore, open in the middle and over the inlet and the outlet; the riffle stays open and steams | walking out on the ice breaks it (Andrew, 2026-09-27) — a plunge and the run-for-your-life clock (document 08 §4.5); the lake is not a place to stand this week — its shore, the gravel and the muskeg edge are the open ground |
| **the ground** | thawed under a skin frozen overnight; roots dig | frozen a centimetre or two at dawn, thawing in the sun | — | frozen a few centimetres | — | under the new snow the frost stops deepening (snow insulates) | a frozen crust, thawed below | digging roots, a pit, a grave costs more each day |
| **fuel** — deadfall within reach | bare ground: the treeline's deadfall in plain sight | — | the near wood's deadfall is used; wet wood smokes | a longer walk for each armful | — | the new snow covers the small deadfall; standing dead wood (a blade, a saw) and the far wood | a trail to the far wood, packed, is fast | daylight and sweat per armful rise; a fire and its wood have to be kept dry in the flurries |
| **food** — the country closing | the country at its richest: berries on the bush, grouse on the ground, hares turning white against the brown, open water with fish in it, roots in soft ground; the freight and people's bags | — | the first dusting on the low berries | — | — | the lowest mats go under; birds and hares sit tight in cover | fresh tracks lead to the hares and the grouse; fishing means the creek's open water, the riffle and the lake from its shore | a calorie debt each day → weakness → cold (document 10) |
| **the animals** — they act (document 23 owns which) | the bear, a male grizzly up all week, feeding hard before his den: its sign first (a torn-apart log, scat full of berries, tracks in the mud at the creek, ravens and jays gathered over something); an owl at night | the bear follows the smell — the pilot's body, the freight's food, the fuel and the oil | tracks in the first snow | the bear bolder as the camp smells of food | — | the flurry holds everything down | tracks circling the wreck in the fresh snow; ravens, jays and a fox work the camp | through the combat system and document 11's wounds; never a scripted kill |
| **injuries** — untreated wounds infect; cold injures | a cut | — | a dirty wound shows infection (24–72 hours, document 11) | fever costs warmth and water | untreated infection spreads | feet wet for days take non-freezing cold injury | frostbite through wet and contact after the coldest night | a body that can't work can't stay warm |
| **fatigue** — no sleep, or sleep in the cold | — | the first bad night's cost | judgment: slower activities | mistakes: the fire goes out on watch | — | — | collapse | sleep is a resource with a price |
| **the search** — document 14's flyover schedule, the same every run (Andrew) | overdue half an hour after the pilot's ETA; the alert out within about two hours; at dusk an aircraft flies the filed route high — heard far off, in the wrong place: the early pass, for the story (a party is unlikely to be ready) | the route search: engines along the filed route, across the ridge in the afternoon — a chance for a party with a signal ready | the search widens off the route: a pass heard in the next valley, lost in the cloud | a pass crosses the lake's far end, seen through a gap in the cloud — a real chance | the search narrows toward this valley: a pass low along the creek in the afternoon — a real chance | the flurry grounds the search; nothing flies | **the rescue of everyone still alive** (Andrew, 2026-09-29) — in clear air over fresh snow; the crew find each survivor wherever they are | before day 7, rescue needs a signal up, seen or heard, at the moment of a pass, or the radio; partial cloud and the trees hide the wreck, so what the party builds decides it; a party in radio contact that is not findable is told what to do by the voice |
| **the pilot's body** (he starts the run dead — 2026-09-17) | in the left seat, cooling in air near 0 °C, not freezing | stiff; the frosty nights freeze him from the skin inward | — | — | — | — | freezing through after the coldest night | the moral question from the first minute (documents 12, 15); a smell the bear and the ravens follow; food whose state the food system tracks |

**How the first rungs meet the night-one rule** (document 08 §4.1a). Night one is −2 °C under partial
cloud, calm, and the party is dry, fed and rested: survivable inside the wreck in the clothes they
crashed in, and miserable for anyone in denim — on night one the cold does not kill, and what it costs
shows on the warmth and rest meters (2026-09-28). Night two is −6 °C with frost on everything, and the
party meets it after a day of work, unfed and unslept: without a heat source, better gear, conserving
or huddling, they are in trouble. Both halves come from real early-October weather, and the probes tune
them until the acceptance test holds.

**Sources.**
- Daylight: sunrise-sunset.org, Fairbanks, October 2026 — 1 October: sunrise 07:59, sunset 19:21,
  11 h 22 min, civil twilight 07:13–20:07; 7 October: 08:18–18:59, 10 h 42 min, civil twilight
  07:31–19:46; 8 October: 10 h 35 min — about 6 minutes 40 seconds lost a day. The noon sun's height
  is 90° − 64.8° plus the sun's declination (about −3° on 1 October, −5° on the 7th).
- Temperatures and snow: NWS Fairbanks, *October Normals, Fairbanks, AK* (1981–2010) — 1 October high
  45 °F / low 28 °F (+7.2 / −2.2 °C), 7 October 40 / 24 °F (+4.4 / −4.4 °C); about 1.5 inches (4 cm)
  of snow normally fallen by 7 October, 10.8 inches (27 cm) in the month. NWS Fairbanks, *Fairbanks
  Climate Reference, October* (records since 1904) — record lows for 1–7 October from 14 °F to −1 °F
  (−10 to −18 °C); record daily snowfalls of 2.1–3.3 inches (5–8 cm) on 1–7 October.
- The first snow: NWS Fairbanks, *Fairbanks First Trace Snowfall* and *Fairbanks First 1" Snowfall*
  (1915–2015) — the first trace on 21 September on average, the first inch on 9 October. Ned Rozell,
  "Middle Alaska once again part of the cryosphere" (*Alaska Science Forum*, UAF Geophysical Institute,
  10 October 2019) — an inch or more of snow endures at Fairbanks from 16 October on average, and
  "snow cover encourages colder air temperatures by reflecting the sun's rays".
- Clear, calm nights: UAF Geophysical Institute, *Alaska Science Forum* ("Temperature inversions go to
  extremes") — under clear skies and calm air the valley bottoms are far colder than the hillsides.
- The halo: a 22° halo forms in the cirrostratus that leads a warm front, typically 12–24 hours before
  its snow — not a sure sign, since halos also appear without a front (Atmospheric Optics, "22° halo").
- Snow intensity by visibility (US surface-observation practice): heavy snow is a quarter mile (about
  400 m) or less. Fresh snow density ~50–150 kg/m³, wetter near 0 °C (UBC ATSC 113, "Density of
  newly-fallen snow").
- Ice: the modified Stefan equation of the US Army Corps of Engineers' ice-engineering guidance,
  thickness ≈ α √(accumulated freezing degree-days), with α ≈ 0.5–0.7 (inches, °F-days) for an
  average lake with snow and lower under snow; the ~10 cm (4 inch) guide for walking on new clear ice
  (*Anchorage Daily News*, 13 November 2021). Small lakes near Fairbanks froze over about 5 October
  2014 (NASA ABoVE, *Aerial Photographs of Frozen Lakes near Fairbanks, Alaska, October 2014*, taken on
  8 October, "three days after lake-ice formation"); the larger lakes ice up in late October (ADF&G,
  "Ice Fishing on the Big Three").
- Bears: ADF&G, "Where Sleeping Bears Lie" (black bears den in the latter part of October, among the
  roots of big spruce); ADF&G, "Grizzly Bear Denning" (all females denned by mid-October, about 80% of
  males by 1 November, on the North Slope); ADF&G, "Safety in Bear Country" (avoid carcasses and
  gathered scavengers — a bear may defend its cache).
- The search: AIM 6-2-6 and AOPA, "Rescue me!" (the overdue sequence); document 14 §3.5.

### 4.3 The event deck (each fires when its preconditions hold and its day and hour arrive)

Every card is a floor; the loops grow the deck (2026-09-28). Two
things differ in kind from a list of beats. **Weather cards are the moments the weather state (§4.7)
crosses a threshold** — the first flake, the wind swinging, the clearing — not beats laid on top of
it, and like the weather they are the same in every run. **Acting animals are not cards**: the deck
schedules when an animal comes into the valley and lays its sign ahead of it; after that its
behaviour rules (or a model playing it from outside) decide what it does, and the world's physics
and the combat system answer (§4.4).

- **Weather**: hoarfrost and frozen puddles at dawn on day 1 · the first wet flurries on day 2,
  melting into cotton · frost on everything, the stars through the gaps in the cloud, an aurora · the
  flurries of day 3, the first tracks in the morning · sun breaks on the dusting (day 4) · the halo
  late on day 5 — high cloud thickening, a ring round the sun: heavier snow within a day · the
  altimeter in the dead cockpit creeping upward (it is a barometer: at a fixed height its reading
  climbs as the pressure falls, about 30 feet for each hectopascal — for anyone who thinks to read it)
  · the heavier flurry begins (day 6, the early hours) · the wind rises and swings — the breach faces
  it now · the flurry easing (day 6 afternoon) · the clearing and the cold: the coldest night of the
  run, the lake shore and the muskeg coldest · steam fog over the open riffle in the cold · sun on the
  fresh snow (day 7: the mirror window).
- **The animals** (actors — document 23 owns which): **the bear**, a male grizzly up all week, feeding hard before his den — its
  sign before it, in its own area, not spread everywhere, and plain on entering that area without
  examining the ground (tracks in the new snow, a torn-apart log, scat full of berries, ravens and jays
  gathered over something) (2026-09-28); never a mark on the wreck the party would not have seen and
  heard being made; drawn by the pilot's body, the freight's food,
  the fuel and the oil; it may claim the body and defend it as a cache, and it may be driven off ·
  **a few birds** — as many as is realistic, and not constantly calling; wildlife comes and goes, met now and
  then and never ridiculously often (document 23 §4.1): a pair of ravens that find
  the food before you do; gray jays that will take it from a hand; a spruce grouse that sits and
  stares; a great horned owl calling at night · a fox trots the tussocks and the camp · a lynx print,
  never the lynx · a hare, half-white in its change of coat · a dead branch comes down in the
  wind. **No
  wolverine.**
- **Search & rescue** (document 14's flyover schedule): the early pass at dusk on day 1 (high over the
  filed route — heard, not seen) · the route search on day 2 · the search widening, then narrowing
  toward this valley on days 3–5 (the real chances) · the silence of the flurry day · airliners high
  above the weather, heard and never seen; a plane that rocks its wings has seen you · the day-7 rescue · a light plane that is not searching — someone flying supplies out to
  a trapline cabin before the season — a chance to be seen, and a story.
- **The wreck**: fuel drips and pools under the wing (a fire hazard and a fuel source) · the fuselage
  shifts on the slope with a groan (things slide; the door jams) · a window pane falls in · the tail
  section slides further down the scar · the extinguisher's bracket lets go · the day's meltwater
  refreezes the cargo door shut overnight · the day-6 snow lies on the wing and the fuselage, white on
  white ground, until the wreck no longer stands out from the air.
- **Bodies**: the pilot's body from the first minute — cooling, stiffening, freezing from the skin
  inward over the clear nights, a smell the bear and the ravens follow (document 12 §4.3a) · wet
  clothes from the wet flurries · a wound infects · frostbite whitens a finger after the coldest night
  · hypothermia's clumsiness and poor judgment
  (the body fails at acts; the engine never acts for a player — document 11 §4.11) · dehydration
  headaches · the hunger stages.
- **Camp**: the fire dies on an untended watch · the flurry soaks the woodpile left in the open · the new pond ice
  sings at night — thin ice cracking as it cools, high and strange (the deep booming belongs to thick
  ice, later in the winter) · a bough drops its snow on the lean-to · slush runs in the creek and the
  shelf ice grows · tracks in the morning that weren't there (the fox, a lynx, the bear).
- **Mail & freight** (story beats, found not fired): the postmarks; the parcel addressed to Holt; the
  child's letter; a parcel of candles; a small bag of dog food in the freight.

*Sources, beyond §4.2's:* ADF&G, "Safety in Bear Country"
(scavenging birds over a carcass are a warning sign); the altimeter-as-barometer relation is standard
(FAA, *Pilot's Handbook of Aeronautical Knowledge*, the altimeter: about 1,000 feet per inch of
mercury); singing thin ice (Minnesota Sea Grant, "Sounds of ice").

### 4.4 How an event runs (the mechanism)

An event is a **scheduled process** with preconditions (2026-09-28):
`Event{day, hour_window, preconditions(world) -> bool, effects, narration by band, ambient: bool,
interrupts: bool}`. The heartbeat checks the due list each tick; fired events apply Effects through
`apply()` (a drift is mass; a wound is state) and route their narration through the propagator by
band (an owl is heard from the treeline; the bear is seen across the shore). A **non-ambient** event drops fast
forward back to 15×; an **ambient** one — a raven calling, the wind in the tear — leaves it running
(Andrew, 2026-09-27); `interrupts` says whether it also wakes sleepers and breaks activities. The
weather and the flyovers are authored and the same in every run; every other draw comes from the run
seed (DR-12), so a run replays exactly.

Three kinds of thing ride this one mechanism, and they differ in what the event itself does:

- **A threshold crossed in continuous state.** Weather is state that changes every tick (§4.7); a
  weather "event" is the moment a value crosses a line that matters — snow starts, the wind swings
  past the breach, the sky clears — and its narration is that moment. The ice thickening, the snow
  settling and the body freezing work the same way on their own entities.
- **An arrival.** For an acting animal the event is only its entry into the valley and the sign laid
  ahead of it (tracks, scat, a torn log, the birds over a carcass). From then on it is an actor — its
  behaviour rules run each tick, or a model plays it from outside through the same grammar a person
  uses (GDD §3 rule 5) — and what it does resolves through the world's physics and the combat system,
  never through the card. *(The behaviour system and the combat system have no design document yet —
  `PLAN.md` A10.)*
- **A scheduled happening** with its own preconditions — the flyovers (document 14), the wreck
  settling.

**Danger is telegraphed the way it is in real country, and resolved by physics, never by a card.**
**The sign** is in each animal's ontology row — `sensed` carries its tracks, scat, calls and smell,
with cadence, and the world carries what it leaves: a torn log, a carcass with ravens and jays over it
(the sign ADF&G tells people to leave on). **The warning** is in its behaviour rules, as real animals
give it: a bear's huffing, jaw-popping and
a bluff charge before contact; a bear on a carcass defending it as a cache. **The outcome** is the
combat system's physics and document 11's wounds. A dead branch coming down in the wind is ordinary
physics on the tree. **Escape is never authored per danger**: it is
whatever the world allows — back off, group up, make noise, get into the wreck, leave the carcass,
fight. Running from a bear is the wrong answer: it chases, and it runs a person down; standing your
ground, looking big, staying together and, depending on the attack, playing dead are the real answers
(2026-09-27). The stakes are real: the bear can kill — through the bleeding it causes, never at once, so a mauled
person lies there bleeding and can still play dead (2026-09-27) — though in Alaska's own record a bear
injures far more often than it kills; dangerous places injure but never kill outright (2026-09-17;
document 11 §4.6).
Sources: ADF&G, "Safety in Bear Country".

### 4.5 Endings

Document 21 owns the endings and document 14 the rescue; this is what the ladder and the deck lead to.

- **Rescued** — by the radio, by a signal a search plane sees, or on day 7, when the rescuers find
  everyone still alive (documents 14 §3, 21 §4.3). Help comes when the weather lets it in; this week the lake never holds, so a
  helicopter sets down on the shore, the gravel or the muskeg.
- **Dead** — never at once: by the body running down — blood loss (the bear and a knife kill this
  way), the cold, thirst, a wound gone bad, carbon monoxide — on real clocks, with time to respond
  (2026-09-27; document 11 §4.6). Poison never kills, and a fall injures but never kills outright. The
  run ends when the last player dies. A dead player's body stays in the world, and the
  player is a ghost who moves freely and talks only out of character. There is no recap.

**The game ends on day 7** (Andrew, 2026-09-29): the rescuers find everyone still alive (document 21
§4.3). The early ways home get a party out sooner, and so **the last 24 hours before the day-7 rescue
are the hardest of the run** — the day-6 flurry, the coldest night, the wood and food running low — or
the early routes would not be worth the work when a party could simply wait one more day.

### 4.6 What is built first

*(Held for the implementation plan — `PLAN.md` §0, step 3 — where Andrew reviews how everything is
built; not part of the design sitting, 2026-09-28.)* An ordering by what each piece stands on, with nothing
dropped. (1) **The weather as state and the escalation calendar** (§4.7), because the warmth process
— step 3 of the decided build order (scheduler → fire → warmth → hunger and thirst → injury → the
pilot's body and `status`) — cannot run without air temperature, wind and falling snow. (2) **The
flyover schedule** (document 14), because two of the three ways home need a pass to happen. (3) **The
wreck's own events and the pilot's body**, which are state changes on entities that already exist.
(4) **The acting animals**, which wait on the behaviour system and the combat system (both still to
be designed — `PLAN.md` A10). (5) Everything else, and whatever the loops add.

### 4.7 Weather is state

Weather is not a label on the valley (2026-09-28). It is a set of real
quantities that change every tick, that other systems read, and that the things in the world answer
to. One air mass lies over the whole valley; each zone and each body of water does its own thing with
it.

**The valley's air** — one per run, advancing every game-minute:

| state | held as | what reads it |
|---|---|---|
| air temperature | °C, with a daily cycle; under a clear, calm sky an inversion pools the cold on the valley floor, so a zone's elevation and openness set how much colder it is | the heat system (to be written): bodies and their parts, fires, water, ice, food, the pilot's body |
| wind | speed (km/h) and the direction it comes from | each zone's exposure turns it into what reaches a body (document 08 §4.4); the openings of the wreck speak it (08 §4.8); drifting; smoke; fire (document 07's wind term) |
| precipitation | kind — none, snow, wet snow, freezing drizzle, rain — and rate (cm of snow, or mm of water, an hour) | wetting (08 §4.5), the snow on the ground, sight |
| visibility | metres | perception (document 19) — `visual_band` derives from it; whether a search crew can see anything |
| cloud | cover and ceiling height | whether search aircraft fly low (document 14's flyover schedule); whether the sun or the moon is out; how far a night falls |
| pressure | hectopascals | the altimeter in the cockpit, read as the barometer it is |
| sun and moon | height and bearing from the date, the hour and the latitude; the moon's phase | light — daylight, twilight, moonlight on snow; a mirror flash; focus fire (document 07) |

**Each zone and each water body:**

| state | held as | what reads it |
|---|---|---|
| snow on the ground | depth (cm), density (kg/m³), and whether it is fresh, settled, drifted, wind-slabbed or crusted | travel time (document 03 §4.1a: distance over pace × terrain × snow × load × fitness); what is buried — forage, deadfall, tracks, the wreck; digging; snow as water (document 09: ~10:1 loose, ~3:1 packed); snow blocks and walls (document 08) |
| ice on each water body | thickness (cm), clear or white, slush under the snow, open water over currents | whether it holds the weight on it; falling through; fishing through it |
| frost in the ground | depth (cm); and where there is permafrost — in patches under the black spruce, the muskeg and north-facing slopes — the depth to it, half a metre to a metre this week (document 23 §4.6) | digging roots, rocks, mud, a pit, a grave; a deep pit over permafrost hits ground frozen solid |

**How it advances.** The escalation calendar holds the week's weather as authored waypoints — when
the front arrives, when it peaks, when it clears — the same in every run (2026-09-27), with the
numbers of §4.2; every tick moves the air between them, with the daily cycle on top. Snow on the
ground grows by the snowfall rate over time, settles with time and warmth, and drifts in the wind
across open zones into their lees; ice grows with the freezing degree-days, slowed by the snow lying
on it and flooded to slush when that snow outweighs it (§4.2's sources); the ground freezes on the
clear nights and stops freezing once snow covers it. So the weather advances continuously, by the
calendar's authored shape, not by day-steps or dice; **the ladder's snow row and the deck's weather
cards are the same thing told twice** — the row is the state's shape over the days, the cards are the
moments it crosses a line (§4.4); **and one temperature curve governs — the real one.**

**The five shipped keys** (`WEATHER_BAND_STEP`: clear, light snow, steady snow, heavy snow, whiteout)
become what they really are: a perception band *derived* from visibility and precipitation, which
`visual_band` and `audible` keep using. They are not the weather.

**Who owns what.** This document owns the weather's state and its shape over the run. How heat moves
from the air into bodies, water, food and the plane is **the heat system's (design document to be
written — `PLAN.md` A10)**. The physics of the snow and ice on the ground — settling, drifting, ice
growth and slush, frost in the ground — is named here and wants its own design document (to be
written); until it exists, this section is its specification.

## 5. Interactions

**Depends on:**
- **Time, sleep and the clock** (`06-time-sleep-and-the-clock.md`; `tick-and-scheduler.md`) — the
  heartbeat that checks the due list, the activity and process model events interrupt, and fast
  forward, which non-ambient events drop back to 15×.
- **Warmth, clothing and shelter** (`08-warmth-clothing-and-shelter.md`) — the night-one rule (08
  §4.1a) that the cold row is tuned to; exposure, which the wind and the snow change.
- **Food and hunger** (`10-food-and-hunger.md`) — the food row.
- **Injury and first aid** (`11-injury-and-first-aid.md`) — the injuries row, and what kills.
- **The pilot and bodies** (`12-the-pilot-and-bodies.md`) — the body's states: cooling, rigor,
  freezing, smell (12 §4.3a).
- **Perception** (`perception-model.md`; `19-multiplayer-and-instances.md`) — event narration routed by
  band; visibility.
- **Rescue** (`14-rescue-paths.md`) — the flyover schedule in the search row, and whether a signal is
  seen, which reads this document's cloud, visibility, wind and light.
- **Flora and fauna** (`23-flora-and-fauna.md`) — which animals act, how many birds, what grows; the
  animal and forage rows read it. **Water** (`09-water.md`) — the open water, the creek's shelf ice and
  slush, the ice. **The premise and world** (`01-premise-and-world.md`) — the valley's zones, the lake
  open all week.
- **The moral and social layer** (`15-moral-and-social-layer.md`) — the bodies events overlap the
  pilot's body there.
- **Determinism** (DR-12, `implementation-architecture.md`) — every draw that is not authored comes
  from the run seed.
- **Systems with no design document yet** (`PLAN.md` A10): **the heat system** (how the air's
  temperature moves into bodies, water, food and the plane), **the behaviour of acting animals** (their
  senses, drives and warning behaviour, and how a model plays one), **combat** (how an animal's charge
  and a person's spear resolve), **snow and ice on the ground** (§4.7), and **food state and
  spoilage** (the body and the meat in a week that crosses from thaw to hard freeze).

**What depends on this:**
- **Every document that needs the week's weather or daylight** — 01, 02, 08, 09, 10, 14, 23 and the
  rest refer to §4.2 rather than restating its numbers.
- **Endings** (`21-endings.md`) — which ending fired, and the event log.
- **Rescue** (`14-rescue-paths.md`) — the flurry day that grounds the search, and the clear day after.
- **The world-building loops** (`22-the-world-building-loops.md`) — grow the deck by evidence, the
  same as everything else in the world.

## 6. Open questions

None open.

## 7. Review log

- **2026-09-18 (Andrew, via document 08):** the night-one rule constrains the ladder's first rungs.
- **2026-09-26 (Claude's self-review, for Andrew's check):** the ladder and the deck rebuilt from real
  interior-Alaska data; the animals act; how an event runs; what is built first; weather as state.
- **2026-09-27 (Andrew):** the same weather every run; the default rescue on day 7, with the same
  flyovers every run; nothing kills instantly.
- **2026-09-27 (Andrew):** the season is the first week of October, for more than ten hours of
  daylight; the ladder rebuilt for it from the Fairbanks record.
- **2026-09-27 (Andrew, at document 11's sitting):** no big storm — bare, icy ground at the start, snow
  on and off to a couple of inches, a heavier flurry on day 6 that clears for day 7; the sky always at
  least partly cloudy, planes flying most days and the wreck hard to see; the escalation from the cold
  and the land; the week stays the first of October. The ladder and the deck redrawn for it.
- **2026-09-28 (Andrew, the document's sitting):** the week's day-by-day numbers; the event deck, with
  the bear's sign in its own area and plain on entering, no claw marks on the wreck, no snared hare
  found waiting and no chainsaw; open-ended activities such as tending the fire through fast forward;
  how an event runs; weather as state. What is built first waits for the implementation plan.
  **Reviewed in full.**

## 8. What exists today

**Built:** nothing of the ladder, the deck or the weather.

**Designed, with types but no behaviour:** the `Event` / `EventKind` contract shape
(`game/world/sim/contracts.py`) and the `INTERRUPT_SIGNALS` set in `game/world/sim/events.py`
(`FIRE_STATE_CHANGE`, `SURVIVOR_WORSENS`, `WEATHER_CHANGE`, `SCRIPTED_TRIGGER`, `RESCUE_SIGNAL`,
`DANGER`, `PLAYER_STOP_REQUEST`). Nothing constructs a ladder or a deck from them yet, and
`events.should_interrupt()` raises `NotImplementedError`. There is no ambient / non-ambient flag yet.

**Nothing:**
- `game/world/sim/systems/weather.py` is a docstring only; it still describes a retired five-stage arc
  with −15 to −20 °C nights, and contains no function, class or state.
- `game/world/sim/systems/clock.py` advances world time and nothing else, and `scheduler.py` is a
  stub; no scheduler drives a due-events list.
- No probe or scenario table encodes the ladder or the deck — `game/world/scenarios/whiteout/probes/`
  holds only `census.py`, `chain.py`, `kit.py` and `phrasing.py`.
- No `docs/architecture/events.md` exists.
- The only place weather exists as running code is the perception stub: `visual_band()` and
  `audible()` in `game/world/sim/space/perception.py` and `sound.py` take a `weather` argument, and
  `sound.py`'s five-key `WEATHER_BAND_STEP` table is read — but every caller passes `"clear"` today.
