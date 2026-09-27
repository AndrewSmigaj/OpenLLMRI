# Events, escalation and weather: the ladder, the event deck, weather, endings

> **Status: draft for review.** Architecture counterpart: none yet — no `docs/architecture/events.md`
> exists; the closest architecture entries are DR-12 (determinism/seeding) and DR-15a (the week-long
> run, the escalation ladder, no hard time barriers) in
> [`implementation-architecture.md`](../architecture/implementation-architecture.md). Sources:
> `docs/investigation/design/events-and-escalation.md` (primary — its own banner names
> `docs/architecture/events.md` + a future DR-30 as its promotion path, which has not happened);
> `docs/scenarios/whiteout/GDD.md` §6/§8 and §0b; `docs/scenarios/whiteout/roadmap.md` P7;
> `implementation-architecture.md` (DR-12, DR-15a); `docs/architecture/perception-model.md`;
> `game/world/sim/space/sound.py` and `perception.py`; `game/world/sim/systems/weather.py`;
> `game/world/sim/events.py`; `docs/investigation/design/00-provenance-audit.md`.

> **The season was settled on 2026-09-26: October, at freeze-up.** The run starts with about an inch
> of snow, bushes dusted but visible, skim ice on the water, roots and berries still findable;
> the storm starts light and gets heavier over the days, and the snow piles up the way a real storm of
> that kind piles it up — part of the escalation ladder. A bear is in. Andrew, 2026-09-26: *"It starts
> with just an inch, you can still get to berries and such, with the storm it accumulates however much
> snow storms that start from light then get heavier over the days (part of the increasing challenge
> mechanic)"*; *"we can have a bear, that would be neat"*. The month is Claude's pick, at Andrew's
> request (*"you pick the month"*): freeze-up is October in interior Alaska — the first lasting snow,
> skim ice on still water, berries still on the bush, bears feeding hard before they den.
> **The December content in this document was revised to October on 2026-09-26** (Claude, `PLAN.md`
> task A8, from real interior-Alaska data with sources — the ladder §4.2, the deck §4.3, weather
> §4.6–§4.7; each December draft is kept below its revision, marked superseded), for Andrew's check
> at this document's sitting. `PLAN.md` §5 and task A8.

## 2. Provenance

**Andrew's decisions.**

- **2026-09-07.** Heavy snow starts at some point; other events are planned ("a bear, or whatever").
  The run is roughly a week — rescue can come earlier, it can run longer until the food runs out — but
  it is not a permanent survival game: instead of hard time-window barriers, the things that cause
  death increase. There is no set arc; what to do is the players' decision.
  (`events-and-escalation.md` banner; `implementation-architecture.md` DR-15a; `00-provenance-audit.md`
  §1.)
- **2026-09-16.** The crash is in December — no bear; wolves and a wolverine are the antagonists
  instead. (`implementation-architecture.md` DR-15a amendment; `events-and-escalation.md` §2 and §4.)
  *(superseded 2026-09-26: the season is October, at freeze-up, and a bear is in — the banner above;
  the wolverine was cut 2026-09-17.)*
- **2026-09-17.** The pilot starts the run dead. The only endings are rescued or dead; the walk-out
  is not an ending (the cabin is supplies); surviving long enough is the hardest rescue path, and
  the flyover schedule is the rescue clock (document 14 §3; document 21 §4). Wildlife as events and
  sign; no wolverine; lethal places injure, never kill outright; a seeded dice roll, announced.
  (`PLAN.md` §5.) *(The "events and sign" part is superseded 2026-09-26 for the bear, the bigger
  animals and a few birds, which act — next bullet.)*
- **2026-09-18 (via document 08).** The night-one rule: night one survivable inside the wreck in the
  starting clothes, with no fire and no huddle; from night two the cold climbs, and the ladder is
  tuned until both halves hold (document 08 §4.1a; the review log below).
- **2026-09-26.** October, at freeze-up; the storm starts light and builds over the days, "part of
  the increasing challenge mechanic"; a bear is in (the banner's quotes). The bear and some of the
  bigger animals are driven by behaviour rules the engine runs, or by a lightweight model playing
  them from outside when a run wants it; birds act too, a few rather than flocks: *"the bear can be
  controlled by either, birds have to be controlled by AI, we don't actually need flocks of them"*
  (`PLAN.md` §5). A combat system like a MUD's is in (`README.md`, writing rules).

DR-15a's 2026-09-16 amendment also carries decisions that belong to other documents in this set (the
whole valley in the first run, the 206's four-seat interior, the kid, the watch rule, no lethal-consent
gate) — they are designed there; see docs 01, 06, 15, 16.

**Proposals (Claude).** Everything else below is a proposal from `events-and-escalation.md`, not yet
reviewed with Andrew: the escalation-ladder table and every number in it, the event deck's full
contents, the four endings (including "still going"), and the event-scheduling mechanism. The weather
section (§4.6) is not a proposal in the same sense — it is a collection of fragments that exist across
the GDD, the roadmap, and the architecture/perception code, none of which amount to a designed system;
that section says so plainly rather than inventing one. *(Claude, 2026-09-26: the October revision
replaced the ladder's numbers and the deck's seasonal content with real interior-Alaska data — the
sources are listed under §4.2 and §4.7 — and §4.7 proposes weather as a state system; all of it
Claude's, for Andrew's check.)*

## 3. In one paragraph

A run has no clock ticking down to failure and no scripted plot: the world clock keeps running while a
second, day-indexed calendar quietly turns colder, snowier, hungrier and more dangerous underneath it,
whether the party is asleep, working, or doing nothing. It starts gently — an inch of snow, the
berries still on the bush, skim ice at the water's edge, a first night mild under cloud — and then
the storm comes in light and builds for days, burying the forage, the deadfall and the wreck itself,
and leaves a hard clear cold behind it *(Claude, 2026-09-26 — the October revision; for Andrew's
check)*. Nothing on the ladder ever refuses the party
outright — it just makes staying alive cost more every day — and the sign of what's coming (tracks,
calls, a groan from the fuselage) always arrives before the thing itself. A deck of seeded, telegraphed
events — weather beats, animals, the search moving on, the wreck settling, the pilot's body — fires
when its day and its preconditions line up, the same way every time the run is replayed from the same
seed; the bear, the moose and the wolves, once they are in the valley, act on their own.
~~The run ends when rescue's confidence crosses its threshold, when the party walks out to Holt's
cabin, when the last player dies, or — if nobody does either — eventually anyway, because cold and
hunger never plateau.~~ The run ends only two ways: **rescued** — the radio during a flyover, a
signal a search plane sees, or surviving until the late pass reaches a party that can be found — or
**dead**, of anything *(the endings decided 2026-09-17; rewritten by Claude 2026-09-26, for Andrew's
check)*.

## 4. The design

### 4.1 The two clocks (what "a week" means)
- **The world clock** runs continuously (DR-14) ~~at 15 real-seconds per game-minute — roughly 1.6 real
  hours per game day while the party is active. Sleep and `wait` advance it by consensus (DR-14a): when
  every connected player is resting, the heartbeat runs at 20× until a target time or an interrupting
  event. A week of game time is a few sittings~~ *(superseded 2026-09-17, document 06: the clock runs
  at 15 game-minutes per real minute; `propose fast forward` raises it to 180× when every player
  agrees, and events drop it back; a week of game time is one sitting of two or three hours, halt
  and resume allowed — fixed by Claude, 2026-09-26)*; a party that keeps busy pays for it in cold.
- **The escalation calendar** is indexed by game day, not by real time: the world gets deadlier on its
  own schedule whether the party acts or sleeps.

### 4.2 The escalation ladder (deterministic, telegraphed, no barriers)

**The October ladder** *(Claude, 2026-09-26 — `PLAN.md` A8 and §6 Q1/Q5; for Andrew's check)*. The
crash is in mid-October in an interior-Alaska side valley at about 64–65° N — on or after 15 October,
the date from which Alaska's statute adds snowshoes, a sleeping bag and a wool blanket to every
aircraft's emergency kit (AS 02.35.110; the exact date is document 01's). The reference station is
Fairbanks (64.8° N), the interior's long record; every number below comes from real data first and
is tuned by probes after. Whether every run has this same week or draws its own inside the real
range is Andrew's (§6 Q7). **The shape is Andrew's: an inch of snow at the start, a storm that begins light and builds
over the days, and the snow piling up the way a real storm's does — the ladder's increasing
challenge.** The weather does the escalating: the normal cooling of mid-October is only about half a
degree a day, so what makes each day harder is the storm itself — what it buries, what it grounds,
and the hard clear cold it leaves behind.

| what rises | day 1 | day 2 | days 3–4 | day 5 | days 6–7 | days 8–10 | how it kills |
|---|---|---|---|---|---|---|---|
| **daylight** | about 9 h 45 min, sunrise ~08:45, sunset ~18:30 (Alaska daylight time); civil twilight adds ~45 min at each end, so ~11 h 20 min to work by; the sun no higher than ~16° at noon | 7 minutes less | 7 minutes less each day; storm cloud makes midday dim | about 9 h 15 min | about 9 h; the noon sun ~14° | about 8 h 40 min | every job outside fits between first and last light; the storm shortens the useful part |
| **cold** — the valley floor, day / night | +1 °C / −4 °C — overcast; the cloud holds the first night up | −1 / −12 — the first clear night: frost on everything, the cold falling out of the sky | −3 / −8 — cloud and snow hold it up | −5 / −9 — the storm's peak | −12 / −20 — clearing behind the storm, calm, an inversion: the lake and the muskeg coldest, the bench and the ridge several degrees warmer | −14 / −22, or milder under a second system | the warmth math (document 08): night one survivable inside the wreck; from night two, not without a heat source, better gear, conserving or the huddle |
| **the storm** — snow, wind, sight | dry and overcast; wet flurries from dusk near 0 °C, which melt into what they land on | the flurries end by midday; clearing, calm; late in the day a halo round the sun in thickening high cloud — snow within a day | day 3: light snow from the afternoon (under 1 cm an hour), light wind from the east. Day 4: steady snow all day (1–2 cm an hour), wind 15–25 km/h, a kilometre or two of sight | heavy snow for hours at 2–4 cm an hour: under 400 m of sight in the open and almost none on the ice and the ridge; wind 25–40 km/h in the open, gusting past 50 on the ridge; possibly freezing drizzle at the onset (seeded) | day 6: the low passes, the wind swings north and colder, flurries; blowing and drifting on open ground. Day 7: clear and still | clear cold holds, or a second, smaller system (seeded) | wind multiplies exposure; wet snow soaks what it lands on; sight and sound collapse (document 19's bands); smoke and mirrors fail in snow and wind; search aircraft do not fly low |
| **snow on the ground** | ~2–3 cm (the inch): bushes dusted, berries visible, deadfall visible, every track crisp | ~3–4 cm — the best tracking snow of the run | 10–20 cm, ankle to mid-calf: lowbush cranberry and crowberry go under; deadfall becomes humps; the breach drifts in | 30–40 cm fresh, knee-deep drifts in the lee of the fuselage; breaking trail costs sweat; the wreck's white skin disappears from the air | settles to ~25–30 cm; wind-packed drifts of 60–80 cm against the hull and the treeline; the cargo door drifted shut each morning; wind slab on open ground | stays; each system adds | work costs sweat (the deferred cold debt); the entrance must be kept; forage and fuel go under; the wreck stops being a signal by itself |
| **ice** | skim ice at the pond edges and the lake margin at dawn, gone by noon; the lake open; the creek running, rimmed with shelf ice | the clear night skins the ponds over (~2 cm — it holds nothing; a skipped stone rings on it) | the lake skins over on a calm night; snow on new ice insulates it, and snow deeper than about 0.8 of the ice's thickness pushes it under and floods it with slush; frazil slush runs in the creek | ~5 cm under snow and slush — it looks like a snowfield and holds nobody | the cold grows it fast: ~7–15 cm on the lake by day 7 (thinner where snow lies deep, none over the inlet and outlet currents); the riffle stays open and steams | the lake holds a careful person in most places | thin ice is a plunge and the run-for-your-life clock (document 08 §4.5); the lake as a signal platform arrives late, and is a gamble when it does |
| **the ground** | thawed under a skin frozen overnight; roots dig | frozen a few centimetres after the clear night | under the snow the frost stops deepening (snow insulates) | — | a frozen crust under the snow | — | digging roots, a pit, a grave costs more each day |
| **fuel** — deadfall within reach | lies on an inch of snow; the treeline is enough | — | the near wood's visible deadfall is used; new snow hides the rest | deadfall under 30 cm: standing dead wood (a blade, a saw) and the north wood | a trail to the far wood, once broken and packed, is fast | — | daylight and sweat per armful rise |
| **food** — the country closing | the country at its richest: berries on the bush, grouse on the ground, hares half-white against the brown, open water with fish in it, roots in soft ground; the kit and the freight | — | the low berries go under; the ground crusts | birds and hares sit tight in cover; fishing means the creek's open water | a hole through the lake ice, once it holds; the wreck's food is what is left | starvation math | a calorie debt each day → weakness → cold (document 10) |
| **the animals** — they act (document 23 owns which) | the bear, feeding hard before its den: its sign in the new snow first (tracks, a torn-apart log, scat full of berries, ravens and jays gathered over something); a bull moose at the rut's end in the willows, still quick to charge; wolves heard at night | the bear follows the smell — the pilot's body, the freight's food, the fuel and the oil | the storm holds everything down | the bear likely dens as the snow deepens — unless it has claimed a carcass | wolves travel the packed trails and the lake edge and come to any carcass; ravens, jays and a fox work the camp | a bear still about now is a hungry one (seeded, rare) | through the combat system and document 11's wounds; never a scripted kill |
| **injuries** — untreated wounds infect; frostbite deepens | a cut | — | infection risk rises (dirty wound) | fever costs warmth and water | gangrene without care; frostbite in the cold behind the storm | — | a body that can't work can't stay warm |
| **fatigue** — no sleep, or sleep in the cold | — | the first bad night's cost | judgment: slower activities | mistakes: the fire goes out on watch | collapse | — | sleep is a resource with a price |
| **the search** — document 14's flyover schedule | overdue half an hour after the pilot's ETA; the alert out within about two hours; at dusk an aircraft flies the filed route high, listening on 121.5 — heard far off, in the wrong place: the early pass, for the story | the route search, in good weather: engines across the ridge — a real chance only for a party with a signal ready by the clear afternoon | the storm grounds the visual search; only traffic high above the weather, which can hear 121.5 and nothing else | nothing flies low | the clearing: the search widens off the route into the valleys beside it — the real chances; calm, clear cold is the best smoke weather there is | scaled back toward suspension; the late pass — the endurance rescue for a party that can still be found | rescue needs a signal up, seen or heard, at the moment of a pass — or the late pass finding the party |
| **the pilot's body** (he starts the run dead — 2026-09-17) | in the left seat, cooling, not yet frozen at 0 °C | stiff; freezing from the skin inward on the clear night | — | — | frozen hard | — | the moral question from the first minute (documents 12, 15); a smell the bear and the ravens follow; food whose state the food system tracks |

**How the first rungs meet the night-one rule** (document 08 §4.1a). Night one is −4 °C under
cloud, calm, and the party is dry, fed and rested: survivable inside the wreck in the clothes they
crashed in, miserable for the townie in denim. Night two is the first clear night, −12 °C on the
valley floor, and the party meets it after a day of work in wet snow, unfed and unslept: without a
heat source, better gear, conserving or the huddle, they are in trouble. Both halves come from real
October weather — a cloudy night holds near the day's temperature and a clear calm night falls far
below the normal low — and the probes tune them until the acceptance test holds.

**The storm is the escalation.** It telegraphs itself (the halo, the thickening cloud, the altimeter
in the dead cockpit creeping up as the pressure falls), buries in turn the berries, the deadfall, the
tracks and the wreck, grounds the search for its whole length, and leaves the clearest, calmest,
coldest days of the run behind it — which are also the search's best days. A party that does nothing
more than sit in the wreck is in trouble from night two; the cold behind the storm finds out every
party that has not built warmth by then. *(Proposal, tuned by probes.)*

**Sources.** Daylight: sunrise-sunset.org, Fairbanks, October 2026 (15 October: sunrise 08:42,
sunset 18:31, 9 h 48 min, civil twilight 07:55–19:18; 22 October: 9 h 01 min, 08:15–18:55 — about
6.7 minutes lost a day); the noon sun's height from the latitude and the sun's declination (about
−9° on 16 October, −11° on the 22nd). Temperatures: NWS Fairbanks, *October Normals, Fairbanks, AK*
(1981–2010): 15 October high 33 °F / low 18 °F (+0.6 / −7.8 °C), 22 October 27 / 12 °F (−2.8 /
−11.1 °C), 31 October 19 / 4 °F; October's normal snowfall 10.8 inches (27 cm). Clear calm nights and
the inversion: University of Alaska Geophysical Institute, *Alaska Science Forum* ("Temperature
inversions go to extremes"; "Live higher, stay warmer") — valley bottoms far colder than hillsides
under clear skies and calm air. Real October storms in the interior: 20–21 October 2024, 10–25 cm of
snow across the region with freezing rain, and Fairbanks's third-wettest day on record (1.99 inches
of water — *The Watchers*, 22 October 2024; Alaska Public Media, 21 October 2024); 1–3 October 2021,
17 cm in three days at Fairbanks (*Fairbanks Daily News-Miner*); October 2023, the snowpack set on
6 October and 36 cm by late October (Rick Thoman, *Alaska & Arctic Climate*, October 2023 summary).
The halo: a 22° halo forms in the cirrostratus that leads a warm front, typically 12–24 hours before
its snow (it is not a sure sign — halos also appear without a front; Atmospheric Optics, "22° halo").
Snow intensity by visibility
(US surface-observation practice): heavy snow is a quarter mile (about 400 m) or less. Ice growth:
the modified Stefan equation of the US Army Corps of Engineers' ice-engineering guidance, thickness
≈ α √(accumulated freezing degree-days), with α ≈ 0.5–0.7 (inches, °F-days) for an average lake
with snow and lower under heavy snow; the ~10 cm (4 inch) guide for walking on new clear ice
(*Anchorage Daily News*, 13 November 2021); the slush threshold from buoyancy (ice floats with about
8% of its thickness above water; snow at ~100 kg/m³ deeper than ~0.8 of the ice's thickness sinks it).
Fresh snow density ~50–150 kg/m³, wetter near 0 °C (UBC ATSC 113, "Density of newly-fallen snow").
Bears: ADF&G, "Where Sleeping Bears Lie" (black bears den in the latter part of October, among the
roots of big spruce); ADF&G, "Grizzly Bear Denning" (all females denned by mid-October, about 80% of
males by 1 November, on the North Slope); ADF&G, "Safety in Bear Country" (avoid carcasses and
gathered scavengers — a bear may defend its cache). Moose: ADF&G, "Aggressive Moose" (bulls may be
aggressive in the rut, late September and October; moose injure more Alaskans than bears do). The
search: AIM 6-2-6 and AOPA, "Rescue me!" (the overdue sequence); document 14 §3.5a.

#### The December draft (superseded 2026-09-26 by the October ladder above; kept as the record)

The crash is in December — five hours of daylight; the ladder starts from a December valley. The
numbers below are proposals for review, tunable by probes, not final.

| what rises | day 1 | day 3 | day 5 | day 7 | day 10 | how it kills |
|---|---|---|---|---|---|---|
| **cold** — ambient by day, colder at night (coldest before dawn) | −12 °C / −20 night | −18 / −26 | −24 / −32 | −30 / −38 | −34 / −42 | warmth math: without fire + insulation + shelter the core drops below the floor |
| **storm bands** — snowfall, wind, whiteout | light flurries | the first heavy snow (a day) | a two-day blow, near-whiteout | clear-cold behind it (aurora, brutal night) | the second storm | wind chill multiplies exposure; visibility bands collapse; travel and signals shut |
| **snow load** — drifts bury the wreck, the wood, the tracks | ankle | knee at the doors; the breach drifts in | the cargo door needs digging out each morning | the wing is a hump | — | work costs sweat; the entrance must be kept; wood gets farther away |
| **fuel radius** — deadfall within reach is used up | treeline | the near wood is picked clean | the north wood (a walk with the sled) | — | — | daylight and sweat per armful rise |
| **food** — the kit's rations for three run out | rations | the freight (flour, coffee) | the country (snares, grubs, bark) or the pilot | — | starvation math | calories/day debt → weakness → cold |
| **injuries** — untreated wounds infect; frostbite deepens | a cut | infection risk rises (dirty wound) | fever costs warmth and water | gangrene without care | — | a body that can't work can't stay warm |
| **fatigue** — no sleep, or sleep in the cold | — | judgment: slower activities | mistakes: the fire goes out on watch | collapse | — | sleep is a resource with a price |
| **the search** — rescue confidence decays as the grid moves away | the first overflight (wrong area) | a search plane crosses the valley (seen only if a signal is UP) | the search shifts north | the search is scaled back | occasional traffic only | rescue needs a signal in the air at the moment of a pass |
| **the pilot** | scripted only — no talking to him: moaning heard in the cockpit, maybe a line; dies within the day *(superseded 2026-09-17: he starts the run dead — the October ladder's body row)* | a body | — | — | — | the moral question starts on day one |

Nothing here refuses a player; every line is a number that hurts more each day. A party that does
everything right can last past day ten; a party that does nothing dies by night three.

### 4.3 The event deck (seeded; each fires when its preconditions hold and its day/hour arrives)

**The October deck** *(Claude, 2026-09-26 — `PLAN.md` A8; for Andrew's check)*. Every card is a
floor; the loops grow the deck. Two things changed in kind, not only in season. **Weather cards are
the moments the weather state (§4.7) crosses a threshold** — the first flake, the wind swinging, the
clearing — not beats laid on top of it. **Acting animals are not cards**: the deck schedules when an
animal comes into the valley and lays its sign ahead of it; after that its behaviour rules (or a
model playing it from outside, `PLAN.md` §5) decide what it does, and the world's physics and the
combat system answer (§4.4).

- **Weather**: the first wet flurries at dusk on day 1, melting into cotton · the first clear night
  (day 2): frost on everything, the stars, often an aurora (seeded), the cold · the halo — high cloud
  thickening, a ring round the sun or the moon: snow within a day · the altimeter in the dead cockpit
  creeping upward (it is a barometer: at a fixed height its reading climbs as the pressure falls,
  about 30 feet for each hectopascal — for anyone who thinks to read it) · the snow begins (day 3) ·
  the wind rises and swings — the breach faces it now · the heavy-snow peak (day 5): near-whiteout in
  the open · freezing drizzle at the storm's onset (seeded): a glaze on the wreck, the rocks and the
  antenna · the wind shift behind the low (day 6), drifting · the clearing and the cold: the inversion
  night, the lake and the muskeg coldest (days 6–7) · steam fog over the open riffle in the cold ·
  sun break on fresh snow (the mirror window, and snow blindness) · a second, smaller system (seeded,
  days 8–10).
- **The animals** (actors — document 23 owns which, and how many birds): **the bear**, feeding hard
  before its den — its sign before it (tracks in the new snow, a torn-apart log, scat full of berries,
  claw marks on the fuselage, ravens and jays gathered over something); drawn by the pilot's body,
  the freight's food, the fuel and the oil; it may claim the body and defend it as a cache, it may be
  driven off, and it most likely dens as the snow deepens · **the moose**: a bull at the rut's end in
  the willow flats, a cow with a calf; the wall of meat that injures the careless · **wolves**: howls
  at night; tracks circling the wreck the morning after the storm; they come to any carcass; testing
  a lone traveller is rare in real Alaska and rare here · **a few birds, never flocks**: a pair of
  ravens that find the food before you do; Canada jays that will take it from a hand; a spruce grouse
  that sits and stares; a great horned owl calling at night · a fox trots the tussocks and the camp ·
  a lynx print, never the lynx · a hare in the snare, half-white in its change of coat · a snow load
  drops off a bough — October's wet snow is heavy, and a dead branch can come down with it. **No
  wolverine** (2026-09-17).
- **Search & rescue** (document 14's flyover schedule): the early pass at dusk on day 1 (high over
  the filed route, listening on 121.5 — heard, not seen) · the route search on day 2 · the silence of
  the grounded storm days · traffic high above the weather (it can hear 121.5 and nothing else) · the
  widened search in the clearing (the real chances); a plane that rocks its wings has seen you ·
  a helicopter once a sighting is confirmed and the weather lets it in · the late pass · a distant
  chainsaw (the upriver village exists) · a light plane that is not searching — someone flying
  supplies out to a trapline cabin before the season — a chance to be seen, and a story.
- **The wreck**: fuel drips and pools under the wing (a fire hazard and a fuel source) · the fuselage
  shifts on the slope with a groan (things slide; the door jams) · a window pane falls in · the tail
  section slides further down the scar · the battery loses capacity in the cold (warmed, it gives
  some back; run flat, it freezes a few degrees below zero, while a charged one will not freeze in
  any October cold) · the extinguisher's bracket lets go · the day's meltwater refreezes the cargo
  door shut overnight (early), the drift seals it (later) · snow loads the wing and the fuselage
  until the wreck vanishes from the air.
- **Bodies**: the pilot's body from the first minute — cooling, stiffening, freezing from the skin
  inward over the clear nights, a smell the bear and the ravens follow (document 12 §4.3a) · wet
  clothes from the first wet snow · a wound infects · frostbite whitens a finger in the cold behind
  the storm · snow blindness in the low sun on fresh snow · hypothermia confusion (messages, not
  command hijacking) · dehydration headaches · the hunger stages.
- **Camp**: the fire dies on an untended watch · the drift buries the entrance · the new ice sings at
  night — thin ice cracking as it cools, high and strange (the deep booming belongs to thick ice,
  later in the winter) · a bough dumps its snow on the lean-to · slush runs in the creek and the shelf
  ice grows · tracks in the morning that weren't there (the fox, the wolves, the bear, a moose).
- **Mail & freight** (story beats, found not fired): the postmarks; the parcel addressed to Holt; the
  child's letter; a parcel of candles; dog food in the freight.

*Sources, beyond §4.2's:* ADF&G, "Findings related to the March 2010 fatal wolf attack near Chignik
Lake" (the one confirmed fatal wolf attack in modern Alaska); ADF&G, "Safety in Bear Country"
(scavenging birds over a carcass are a warning sign); the altimeter-as-barometer relation is standard
(FAA, *Pilot's Handbook of Aeronautical Knowledge*, the altimeter: about 1,000 feet per inch of
mercury); singing thin ice (Minnesota Sea Grant, "Sounds of ice").

#### The December deck (superseded 2026-09-26 by the October deck above; kept as the record)

- **Weather** (the storm system, P7 seam): first flurries · the heavy snow begins (day 2–3) · wind
  shift (the breach faces it now) · whiteout (visibility band 0 outside) · clear-cold night (aurora;
  −40) · sun break (the mirror window) · thaw-refreeze (overflow, black ice) · the second storm.
- **Wildlife** (all telegraphed by sign first — tracks, calls, the cold-shower gag): ravens scout the
  wreck (they find the food cache before you do) · a fox trots the tussocks · a **wolverine raids the
  cache** at night (fearless; the classic camp thief) · **wolves** howl the second night, tracks circle
  the wreck by the fourth, they test a lone traveller on the ice (a real danger, never a scripted kill)
  · a lynx print, never the lynx · ptarmigan flush (food if you're quick) · a hare in the snare · a
  moose on the trail (a wall of meat that kills the careless; not food unless the party can kill it,
  which they can't) · an owl at night · a snow load drops off a bough onto whoever stands under it.
  **No bear** — the crash is in December; Alaska bears den by early winter. The wolverine and the
  wolves are the antagonists. *(superseded: no wolverine, 2026-09-17; October and a bear, 2026-09-26.)*
- **Search & rescue** (the rescue system's own events): the day-1 overflight in the wrong area (heard,
  not seen) · the day-2/3 search plane crossing the valley (seen if a signal is up: smoke, fire on the
  ice, the mirror in sun, the ELT if an aircraft is overhead to hear 121.5) · a helicopter on a clear
  day if confidence is high · a snowmachine on the lake at dusk (Holt? someone from upriver — a chance
  to be seen, and a story) · a distant chainsaw (the upriver village exists).
- **The wreck**: fuel drips and pools under the wing (a fire hazard and a fuel source) · the fuselage
  shifts on the slope with a groan (things slide; the door jams) · a window pane falls in · the tail
  section slides further down the scar · the battery freezes (the radio route's clock) · the
  extinguisher's bracket lets go · ice seals the cargo door overnight (dig or pry).
- **Bodies**: the pilot's moans (cockpit only) and his death within the first day *(superseded
  2026-09-17: he starts the run dead)* · a wound infects ·
  frostbite whitens a finger · snow blindness on the ice · hypothermia confusion (messages, not command
  hijacking) · dehydration headaches · the hunger stages.
- **Camp**: the fire dies on an untended watch · the drift buries the entrance · the ice booms at night
  (harmless here, terrifying) · a bough dumps its snow on the lean-to · the creek overflows the crossing
  · tracks in the morning that weren't there (the fox, the wolves, a moose).
- **Mail & freight** (story beats, found not fired): the postmarks; the parcel addressed to Holt; the
  child's letter; a parcel of candles; dog food in the freight.

### 4.4 How an event runs (the mechanism)
An event is a **scheduled process** with preconditions: `Event{day, hour_window, seed_jitter,
preconditions(world) -> bool, effects, narration by band, interrupts: bool}`. The heartbeat checks the
due list each tick; fired events apply Effects through `apply()` (a drift is mass; a wound is state),
route their narration through the propagator by band (the wolves are heard from the treeline, seen from
the ice), and — if `interrupts` — wake sleepers and break activities. All draws come from the run seed
(DR-12): the same run replays the same week.

*(Claude, 2026-09-26 — §6 Q3 and Q6; for Andrew's check.)* Three kinds of thing ride this one
mechanism, and they differ in what the event itself does:

- **A threshold crossed in continuous state.** Weather is state that changes every tick (§4.7); a
  weather "event" is the moment a value crosses a line that matters — snow starts, the wind swings
  past the breach, the sky clears — and its narration is that moment. The ice thickening, the snow
  settling and the body freezing work the same way on their own entities.
- **An arrival.** For an acting animal the event is only its entry into the valley and the sign laid
  ahead of it (tracks, scat, a torn log, the birds over a carcass). From then on it is an actor — its
  behaviour rules run each tick, or a model plays it from outside through the same grammar a person
  uses (`PLAN.md` §5; GDD §3 rule 5) — and what it does resolves through the world's physics and the
  combat system, never through the card. *(The behaviour system and the combat system have no design
  document yet — `PLAN.md` A10.)*
- **A scheduled happening** with its own preconditions — the flyovers (document 14), the wreck
  settling, the chainsaw upriver.

### 4.5 Endings (all honest, none a timer)

*(Superseded 2026-09-17 — Andrew: the only endings are **rescued or dead**; the walk-out is not an
ending (the cabin is supplies); "still going" is gone, because surviving long enough is itself the
hardest rescue path — the late pass of the flyover schedule reaches a party that can be found. Kept as
the record; document 21 owns the endings and document 14 the rescue.)*

- **Rescued** — an overflight sees a signal inside a weather window and confidence is over the
  threshold: a helicopter on the ice by afternoon, or a plane drops a note. *(Claude, 2026-09-26: the
  additive confidence and its threshold are replaced by document 14 §3.5a — a pass sees or hears a
  signal, or the late pass finds the party; in October the helicopter lands on the shore, the gravel
  or the muskeg, since the ice holds only late.)*
- ~~**Walked out** — Holt's cabin: the stove, a radio or a snowmachine; "we can outlast this" is rescue
  confidence too.~~ *(superseded 2026-09-17.)*
- **Dead** — cold, starvation, a fall through ice, CO in a closed fuselage, the wreck sliding.
  Individually or all; the run ends when the last player dies. A dead player's body persists. *(And
  anything else that really kills — a bear, a moose, bleeding, thirst; dead players are ghosts,
  2026-09-17.)*
- ~~**Still going** — no cutoff; the ladder guarantees an ending within roughly two weeks of game time
  for any party, because cold and food only get worse.~~ *(superseded 2026-09-17.)*

### 4.6 Weather — an open section, gathered from fragments (not a designed system)

*(Claude, 2026-09-26 — §6 Q5 and Q6; for Andrew's check: the fragments below are kept as the record
of what existed. The October ladder (§4.2) reconciles their numbers — real climate governs, and both
the GDD's June line and the December column are superseded — and §4.7 designs weather as state,
which answers the three open points in the paragraph after the list.)*

Weather has no design pass of its own anywhere in this project. What exists is scattered across four
places that don't yet agree with each other, and none of them say *how* the storm actually advances:

- **The GDD's one-line arc (§6/§8, unchanged since the original design):** "Weather (§8) escalates
  light → steady → heavy → near-whiteout → night (−15 to −20 °C), degrading visibility/audibility/fire/
  tracks/rescue." This predates the December decision (2026-09-16) and its temperatures are much
  milder than the ladder's December-recalibrated cold column (§4.2) — the two have not been
  reconciled.
- **The ladder's own "storm bands" row (§4.2):** light flurries → the first heavy snow (day 3) → a
  two-day blow / near-whiteout (day 5) → clear-cold behind it (day 7, aurora) → the second storm
  (day 10). This is the closest thing to a day-by-day weather schedule that exists, and it is a Claude
  proposal, not a system.
- **The event deck's Weather category (§4.3):** the same five-stage language (first flurries, heavy
  snow begins, whiteout, clear-cold night at −40, sun break, thaw-refreeze, the second storm) recast as
  individually-fired deck entries rather than a continuous arc.
- **The roadmap's P7 deliverable** (`docs/scenarios/whiteout/roadmap.md`): `systems/weather.py` — "light
  → steady → heavy → near-whiteout → night, degrading visibility/audibility/fire/tracks/rescue; 2–3
  seeded timed beats (a search plane that misses you, the pilot's last lucid line — *superseded
  2026-09-17: the pilot starts the run dead and has no lines*)"; plus the
  auto-generated end-of-run recap. Its exit gate wants weather-arc property tests (monotonic escalation;
  degrades the right channels) and a recap that matches the actual event log. None of this is built —
  see §8.
- **The perception model's weather stub** (`docs/architecture/perception-model.md`; confirmed in
  `game/world/sim/space/sound.py` and `perception.py`): `visual_band()` and `audible()` both take a
  `weather` argument that every caller today passes as `"clear"`; `sound.py` defines
  `WEATHER_BAND_STEP = {"clear": 0, "light_snow": 0, "steady_snow": 1, "heavy_snow": 2, "whiteout": 3}`
  — five keys, no code yet setting anything past `"clear"`. `perception-model.md` says this plainly:
  "Weather is a stub." `game/world/sim/systems/weather.py` itself is a docstring naming the same §8 arc
  and citing roadmap P7 — no function, no class, no state.

There is no answer here for how a band advances (by day? by dice? by both?), how the ladder's storm-band
row and the deck's Weather category relate to each other (are they the same beats told twice, or two
independent things that need to be merged?), or which temperature figures govern. §6 below opens these
as questions rather than deciding them. *(Answered in §4.7 and §6 Q5–Q6, Claude, 2026-09-26.)*

### 4.7 Weather is state (Claude, 2026-09-26 — §6 Q6; for Andrew's check)

Weather is not a label on the valley. It is a set of real quantities that change every tick, that
other systems read, and that the things in the world answer to. One air mass lies over the whole
valley; each zone and each body of water does its own thing with it.

**The valley's air** — one per run, advancing every game-minute:

| state | held as | what reads it |
|---|---|---|
| air temperature | °C, with a daily cycle; under a clear, calm sky an inversion pools the cold on the valley floor, so a zone's elevation and openness set how much colder it is | the heat system (to be written): bodies and their parts, fires, water, ice, food, the pilot's body |
| wind | speed (km/h) and the direction it comes from | each zone's exposure turns it into what reaches a body (document 08 §4.4); the openings of the wreck speak it (08 §4.8); drifting; smoke; fire (document 07's wind term) |
| precipitation | kind — none, snow, wet snow, freezing drizzle, rain — and rate (cm of snow, or mm of water, an hour) | wetting (08 §4.5), the snow on the ground, sight |
| visibility | metres | perception (document 19) — `visual_band` derives from it; whether a search crew can see anything |
| cloud | cover and ceiling height | whether search aircraft fly low (document 14's flyover schedule); whether the sun or the moon is out; how far a night falls |
| pressure | hectopascals | the altimeter in the cockpit, read as the barometer it is |
| sun and moon | height and bearing from the date, the hour and the latitude; the moon's phase | light — daylight, twilight, moonlight on snow; a mirror flash; focus fire (document 07); snow blindness |

**Each zone and each water body:**

| state | held as | what reads it |
|---|---|---|
| snow on the ground | depth (cm), density (kg/m³), and whether it is fresh, settled, drifted, wind-slabbed or crusted | travel time (document 03 §4.1a: distance over pace × terrain × snow × load × fitness); what is buried — forage, deadfall, tracks, the wreck; digging; snow as water (document 09: ~10:1 loose, ~3:1 packed); snow blocks and walls (document 08) |
| ice on each water body | thickness (cm), clear or white, slush under the snow, open water over currents | whether it holds the weight on it; falling through; fishing through it; the lake as a place to signal from |
| frost in the ground | depth (cm) | digging roots, a pit, a grave |

**How it advances.** The escalation calendar holds the storm's shape as a few seeded waypoints — when
the front arrives, when it peaks, when it clears — inside the real ranges of §4.2, and every tick moves
the air between them, with the daily cycle and small seeded variation on top. Snow on the ground
grows by the snowfall rate over time, settles with time and warmth, and drifts in the wind across open
zones into their lees; ice grows with the freezing degree-days, slowed by the snow lying on it and
flooded to slush when that snow outweighs it (§4.2's sources); the ground freezes on the clear nights
and stops freezing once snow covers it. So the three open points of §4.6 are answered: **the weather
advances continuously, by the calendar's seeded shape, not by day-steps or dice alone; the ladder's
storm row and the deck's weather cards are the same thing told twice** — the row is the state's shape
over the days, the cards are the moments it crosses a line (§4.4); **and one temperature curve
governs — the real one.**

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
  heartbeat that would check the due list, the activity/process model events interrupt, and the 20×
  sleep-consensus advance the escalation calendar rides on top of. *(Superseded 2026-09-17: 15
  game-minutes per real minute, `propose fast forward` to 180×.)*
- **Warmth, clothing and shelter** (`08-warmth-clothing-and-shelter.md`) — the cold row's numbers feed
  the warmth-floor math; storm bands change exposure. *(Now the night-one rule, 08 §4.1a; 08 §4.7's
  December cold ladder is superseded by §4.2 here.)*
- **Food and hunger** (`10-food-and-hunger.md`) — the food row.
- **Injury and first aid** (`11-injury-and-first-aid.md`) — the injuries row.
- **The pilot and bodies** (`12-the-pilot-and-bodies.md`) — the pilot's scripted moaning/death event;
  bodies persisting afterward. *(Superseded 2026-09-17: he starts the run dead; his body's states —
  cooling, rigor, freezing, smell — are document 12 §4.3a.)*
- **Perception** (`perception-model.md`; `19-multiplayer-and-instances.md`) — event narration routed by
  band; the weather stub's visibility bands.
- **Rescue paths** (`14-rescue-paths.md`) — the search & rescue event category; the confidence threshold
  the "rescued" ending needs. *(Now the flyover schedule and the detection model, 14 §3.5a, which
  read this document's cloud, visibility, wind and light.)*
- *(Added by Claude, 2026-09-26.)* **Flora and fauna** (`23-flora-and-fauna.md`) — which animals act,
  how many birds, what grows; the ladder's animal and forage rows read it. **Water** (`09-water.md`) —
  open water early, ice late; the creek's shelf ice and slush. **The premise and world**
  (`01-premise-and-world.md`) — the lake is open water and skim ice at the start, not a frozen plain.
  **Systems with no design document yet** (`PLAN.md` A10): **the heat system** (how the air's
  temperature moves into bodies, water, food and the plane), **the behaviour of acting animals** (their
  senses, drives and warning behaviour, and how a model plays one), **combat** (how an animal's charge
  and a person's spear resolve), **snow and ice on the ground** (§4.7), and **food state and
  spoilage** (the body and the meat in a week that crosses from thaw to hard freeze).
- **The moral and social layer** (`15-moral-and-social-layer.md`) — the "bodies" event category
  overlaps the pilot_body dilemma there.
- **Determinism** (DR-12, `implementation-architecture.md`) — every draw in the deck comes from the
  per-run seed.

**What depends on this:**
- **Endings & recap** (`21-endings-and-recap.md`) — reads which ending fired and the event log to build
  the recap.
- **The world-building loops** (`22-the-world-building-loops.md`) — grow the deck's categories by
  evidence, the same as everything else in the world.

## 6. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9 with the October revision A8), for Andrew's check:**
Q1, Q2 and Q5 are answered from real data and the decided design; Q3, Q4 and Q6 were wrong-headed (a
card mechanism for animals that now act, an ending that no longer exists, a shortcut for weather) and
are rewritten and answered; **Q7 is new and Andrew's** — whether every run is the same week of
weather. The originals are kept, struck, as the record.

~~1. **Are the ladder's numbers final or starting points?** The source itself calls them "proposals for
   Andrew's review, tunable by probes." *Options:* lock them now vs. treat them as tunable starting
   points revisited once probes/playtest exist. *Recommendation:* starting points — tune by probes, as
   the source already intends.~~ **Claude's answer (2026-09-26), for Andrew's check:** starting points
   taken from real data, then tuned by probes — never invented and never "final" (the design is a work
   in progress). The October ladder (§4.2) takes its daylight from the sun tables, its temperatures and
   snow from the Fairbanks record, and its storm from real interior October storms, with the sources
   listed; the probes then tune it against document 08's acceptance test (night one survivable inside,
   night two not for a party that has done nothing). The writing rule decides it: real life is the
   default answer.
~~2. **In what order is the event deck built?** *(Reframed 2026-09-18: the earlier version asked what to
   cut from the deck, which is scarcity reasoning — nothing is dropped, only queued.)* Every event
   listed is in the design. The question is only what gets built first, since they cannot all be
   built at once. *Options:* (a) the weather spine and the fixed beats first (the heavy snow, the
   flyovers, the pilot), then the wildlife threads, then the rest; (b) a different order — name it.
   *Recommendation:* (a), with everything else queued rather than dropped, and the loops adding more
   events as they flesh the world out.~~ **Claude's answer (2026-09-26), for Andrew's check:** by what
   each piece stands on — an ordering, with nothing dropped. (1) **The weather as state and the
   escalation calendar** (§4.7), because the warmth process — step 3 of document 06's decided build
   order (scheduler → fire → warmth → hunger and thirst → injury → the pilot and `status`) — cannot run
   without air temperature, wind and falling snow. (2) **The flyover schedule** (document 14), because
   two of the three rescue ways need a pass to happen. (3) **The wreck's own events and the pilot's
   body**, which are state changes on entities that already exist. (4) **The acting animals**, which
   wait on the behaviour system and the combat system (both still to be designed — `PLAN.md` A10).
   (5) Everything else, and whatever the loops add. The old option (a) named "the pilot" as a fixed
   beat; he starts the run dead (2026-09-17), so his place in the order is his body's states.
~~3. **How are lethal cards (the moose, wolves testing a lone traveller, a snow load dropping on someone
   underneath) kept "telegraphed, never a scripted kill" in practice?** The source states the rule but
   not the mechanism. *Options:* rely on the sign-before-danger convention alone vs. require each lethal
   card to document its own escape/mitigation path when authored (echoing the rescue-graph's "≥3 paths"
   habit). *Recommendation:* the latter — document the escape path alongside each lethal card as it's
   authored, not after.~~ *(Rewritten 2026-09-26: there are no lethal cards — the bear, the moose and
   the wolves became actors, and a per-card escape path is an authored menu of outs.)* **Claude's
   answer (2026-09-26), for Andrew's check:** danger is telegraphed the way it is in real country,
   and resolved by physics, never by a card. **The sign** is in each animal's ontology row — `sensed`
   carries its tracks, scat, calls and smell, with cadence, and the world carries what it leaves: a
   torn log, a carcass with ravens and jays over it (the sign ADF&G tells people to leave on). **The
   warning** is in its behaviour rules, as real animals give it: a moose's ears laid back and hackles
   up before it charges; a bear's huffing, jaw-popping and a bluff charge before contact; a bear on a
   carcass defending it as a cache. **The outcome** is the combat system's physics and document 11's
   wounds (combat has no design document yet — `PLAN.md` A10). A snow load or a dead branch coming
   down under October's heavy wet snow is ordinary physics on the tree. **Escape is never authored per
   danger**: it is whatever the world allows — back off, group up, make noise, get into the wreck,
   leave the carcass, fight. And the stakes are real: violence resolves with real physics
   (2026-09-16), so a bear or a moose can kill, though in Alaska's own record both injure far more
   often than they kill; the rule that lethal *places* injure and never kill outright (2026-09-17)
   covers places, as document 11 §6 Q2 answers. Sources: ADF&G, "Safety in Bear Country"; ADF&G,
   "Aggressive Moose".
~~4. **Is "still going" truly endless, or does an agents-only research run need a practical ceiling?** The
   ladder's own claim is that any party gets an ending within roughly two weeks. *Options:* no cap for
   any run vs. a session-length ceiling for agent-only research runs specifically (a practical limit,
   not a narrative one). *Recommendation:* no cap for human/mixed runs; flag the agent-only case for
   `20-the-agent-player-and-research.md` rather than deciding it here.~~ *(Rewritten 2026-09-26:
   "still going" was cut on 2026-09-17.)* **Claude's answer (2026-09-26), for Andrew's check:** no run
   needs a cap to end. The only endings are rescued or dead, and surviving long enough is itself a
   rescue path: the late pass of the flyover schedule reaches a party that can be found — at the
   wreck, at the cabin, or under a signal (document 14). A findable party is ended by the late pass or
   by the cold; a party that has made itself unfindable is ended by the ladder — the cold behind the
   storm and the empty larder. Whether an agents-only research run wants a practical session limit is
   document 20's question, not this one's.
~~5. **Which temperature curve governs — the GDD's §8 line (−15 to −20 °C) or the ladder's
   December-recalibrated column (−12 to −42 °C across ten days)?** The GDD's figure predates the
   December decision. *Options:* keep both as-is vs. correct the GDD to point here. *Recommendation:*
   the ladder's December numbers govern; the GDD should carry a corrective note once this document is
   reviewed.~~ **Claude's answer (2026-09-26), for Andrew's check:** neither — the real October
   governs (§4.2). The Fairbanks normals fall about half a degree a day through mid-October (+0.6 /
   −7.8 °C on the 15th, −2.8 / −11.1 on the 22nd), and the weather bends them: a cloudy night holds
   near the day's temperature, a clear calm night falls far below the normal low, and the valley floor
   is colder than the slopes. Both the GDD's June line and the December column are superseded; the
   GDD's §6/§8 needs a pointer here (a cross-document note, not edited from this pass).
~~6. **Does the ladder's storm-band row (§4.2) map onto the perception model's existing
   `WEATHER_BAND_STEP` keys (`clear`/`light_snow`/`steady_snow`/`heavy_snow`/`whiteout`), or does weather
   need richer state (visibility in meters, wind direction) than those five keys carry?** *Options:*
   reuse the five shipped keys as the v1 weather model vs. design a richer state now. *Recommendation:*
   reuse the five keys for v1 — they're already wired into `visual_band`/`audible` — and open a
   follow-up only if a specific mechanic needs more.~~ *(Rewritten 2026-09-26: "reuse the five keys"
   collapsed a real process into a label — the writing rule is state systems, not shortcuts.)*
   **Claude's answer (2026-09-26), for Andrew's check:** weather is state (§4.7): air temperature with
   its daily cycle and the inversion, wind speed and direction, the kind and rate of precipitation,
   visibility in metres, cloud cover and ceiling, pressure, the sun and the moon — and, per zone and
   per water body, the snow on the ground (depth, density, drifted, crusted), the ice (thickness,
   slush, open leads) and the frost in the ground. Every one of them is read by something a survivor
   acts on: exposure, wetting, travel, what is buried, whether the ice holds, whether smoke rises,
   whether a mirror flashes, whether a plane flies low. The five shipped keys stay as what they really
   are — a perception band derived from visibility and precipitation.
7. **Is every run the same week of weather, or does each run draw its own inside the real range?**
   Andrew is deciding how much a second run should be able to lean on memory of the first — whether
   his friends, playing again, know that the storm peaks on day five. The shape itself is his and does
   not change: an inch at the start, a storm that builds, the cold behind it. *Options:* (a) **one
   authored week** — every run has the same storm on the same days; (b) **the shape fixed, the timing
   and amounts drawn per run** from the real range — the peak somewhere on days four to six, 15–45 cm
   of new snow, the coldest night between −15 and −28 °C, the second system or not — seeded, so a
   replay of the same run matches exactly; (c) **a real week** — each run replays an actual
   interior-Alaska October week from the station record that fits the shape. *Recommendation:* (b),
   with its ranges taken from (c)'s records: every run is true to a real October, the escalation is
   always there, and no one can count on day five.

## 7. Review log
None yet — first draft, not yet reviewed with Andrew.

- **2026-09-18 (Andrew, via document 08):** the ladder's first rungs are constrained by the **night-one
  rule** — night one must be survivable inside the wreck in the starting clothes, with no fire and no
  huddle, and night two must not be. The day-1/day-3 temperatures are tuned until both are true
  (document 08 §4.1a).

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-reviewed against block 1 (03–09), the
  decisions since (October at freeze-up, the bear and the acting animals, no wolverine, the pilot dead
  from the start, rescued-or-dead, the flyover clock, combat) and real data, with sources. **The
  October revision (A8):** the ladder rebuilt from Fairbanks normals, the sun tables and real interior
  October storms (§4.2) — its first rungs meet the night-one rule (night one −4 °C under cloud; night
  two the first clear night, −12 °C), the storm builds over days 3–5 and leaves the clear cold of days
  6–7, and new rows carry daylight, snow on the ground, ice, the ground, the animals and the pilot's
  body; the deck rewritten for October with the bear, the moose, the wolves and a few birds as actors
  and no wolverine (§4.3); the December ladder and deck kept below each, marked superseded. **Added**
  §4.4's three kinds of event (threshold, arrival, scheduled) and **§4.7, weather as state**. The clock
  numbers (§4.1), the one-paragraph summary and the endings (§4.5) corrected to the 2026-09-17
  decisions, marked. **Answered** Q1, Q2, Q5; **rewrote and answered** Q3 (no lethal cards — animals
  act), Q4 ("still going" is gone), Q6 (weather is state, not five keys); **left for Andrew:** Q7, the
  same week every run or drawn per run. **Systems with no design document** named in §5: heat,
  animal behaviour, combat, snow and ice on the ground, food state and spoilage.

## 8. What exists today

**Built:** nothing.

**Designed:** the ladder, the event deck, the endings, and the event-scheduling mechanism
(`docs/investigation/design/events-and-escalation.md`); the weather arc's five-stage description (GDD
§8) and its roadmap slot (`docs/scenarios/whiteout/roadmap.md` P7); the `Event`/`EventKind` contract
shape and the `INTERRUPT_SIGNALS` set (`game/world/sim/contracts.py` — `EventKind` enum and `Event`
dataclass; `game/world/sim/events.py` — `INTERRUPT_SIGNALS = frozenset({FIRE_STATE_CHANGE,
SURVIVOR_WORSENS, WEATHER_CHANGE, SCRIPTED_TRIGGER, RESCUE_SIGNAL, DANGER, PLAYER_STOP_REQUEST})`); the
types exist but nothing constructs a ladder or a deck from them yet, and `events.should_interrupt()`
raises `NotImplementedError` (roadmap P4, confirmed by reading the file).

**Nothing:**
- `game/world/sim/systems/weather.py` is a docstring only — confirmed by reading the file: it names the
  §8 arc and cites roadmap P7, and contains no function, class, or state.
- No scheduler drives a due-events list; `clock.py` and `scheduler.py` in the same directory are
  themselves P4 work.
- No probe or scenario table encodes the ladder or the deck — `game/world/scenarios/whiteout/probes/`
  holds only `census.py`, `chain.py`, `kit.py`, `phrasing.py`.
- No `docs/architecture/events.md` and no DR-30 exist — `events-and-escalation.md`'s own banner names
  that promotion path, and it hasn't happened.
- The only place "weather" exists as running code is the perception stub: `visual_band()` /
  `audible()` in `game/world/sim/space/perception.py` and `sound.py`, and the five-key
  `WEATHER_BAND_STEP` table in `sound.py` — every caller passes `"clear"` today.
