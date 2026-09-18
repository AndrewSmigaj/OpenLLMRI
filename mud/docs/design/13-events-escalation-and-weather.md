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

DR-15a's 2026-09-16 amendment also carries decisions that belong to other documents in this set (the
whole valley in the first run, the 206's four-seat interior, the kid, the watch rule, no lethal-consent
gate) — out of scope here; see docs 01, 06, 15, 16.

**Proposals (Claude).** Everything else below is a proposal from `events-and-escalation.md`, not yet
reviewed with Andrew: the escalation-ladder table and every number in it, the event deck's full
contents, the four endings (including "still going"), and the event-scheduling mechanism. The weather
section (§4.6) is not a proposal in the same sense — it is a collection of fragments that exist across
the GDD, the roadmap, and the architecture/perception code, none of which amount to a designed system;
that section says so plainly rather than inventing one.

## 3. In one paragraph

A run has no clock ticking down to failure and no scripted plot: the world clock keeps running while a
second, day-indexed calendar quietly turns colder, snowier, hungrier and more dangerous underneath it,
whether the party is asleep, working, or doing nothing. Nothing on the ladder ever refuses the party
outright — it just makes staying alive cost more every day — and the sign of what's coming (tracks,
calls, a groan from the fuselage) always arrives before the thing itself. A deck of seeded, telegraphed
events — weather beats, animals, the search moving on, the wreck settling, the pilot's body — fires
when its day and its preconditions line up, the same way every time the run is replayed from the same
seed. The run ends when rescue's confidence crosses its threshold, when the party walks out to Holt's
cabin, when the last player dies, or — if nobody does either — eventually anyway, because cold and
hunger never plateau.

## 4. The design

### 4.1 The two clocks (what "a week" means)
- **The world clock** runs continuously (DR-14) at 15 real-seconds per game-minute — roughly 1.6 real
  hours per game day while the party is active. Sleep and `wait` advance it by consensus (DR-14a): when
  every connected player is resting, the heartbeat runs at 20× until a target time or an interrupting
  event. A week of game time is a few sittings; a party that keeps busy pays for it in cold.
- **The escalation calendar** is indexed by game day, not by real time: the world gets deadlier on its
  own schedule whether the party acts or sleeps.

### 4.2 The escalation ladder (deterministic, telegraphed, no barriers)
The crash is in December — five hours of daylight; the ladder starts from a December valley. The
numbers below are proposals for review, tunable by probes, not locked.

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
| **the pilot** | scripted only — no talking to him: moaning heard in the cockpit, maybe a line; dies within the day | a body | — | — | — | the moral question starts on day one |

Nothing here refuses a player; every line is a number that hurts more each day. A party that does
everything right can last past day ten; a party that does nothing dies by night three.

### 4.3 The event deck (seeded; each fires when its preconditions hold and its day/hour arrives)
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
  wolves are the antagonists.
- **Search & rescue** (the rescue system's own events): the day-1 overflight in the wrong area (heard,
  not seen) · the day-2/3 search plane crossing the valley (seen if a signal is up: smoke, fire on the
  ice, the mirror in sun, the ELT if an aircraft is overhead to hear 121.5) · a helicopter on a clear
  day if confidence is high · a snowmachine on the lake at dusk (Holt? someone from upriver — a chance
  to be seen, and a story) · a distant chainsaw (the upriver village exists).
- **The wreck**: fuel drips and pools under the wing (a fire hazard and a fuel source) · the fuselage
  shifts on the slope with a groan (things slide; the door jams) · a window pane falls in · the tail
  section slides further down the scar · the battery freezes (the radio route's clock) · the
  extinguisher's bracket lets go · ice seals the cargo door overnight (dig or pry).
- **Bodies**: the pilot's moans (cockpit only) and his death within the first day · a wound infects ·
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

### 4.5 Endings (all honest, none a timer)
- **Rescued** — an overflight sees a signal inside a weather window and confidence is over the
  threshold: a helicopter on the ice by afternoon, or a plane drops a note.
- **Walked out** — Holt's cabin: the stove, a radio or a snowmachine; "we can outlast this" is rescue
  confidence too.
- **Dead** — cold, starvation, a fall through ice, CO in a closed fuselage, the wreck sliding.
  Individually or all; the run ends when the last player dies. A dead player's body persists.
- **Still going** — no cutoff; the ladder guarantees an ending within roughly two weeks of game time
  for any party, because cold and food only get worse.

### 4.6 Weather — an open section, gathered from fragments (not a designed system)
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
  seeded timed beats (a search plane that misses you, the pilot's last lucid line)"; plus the
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
as questions rather than deciding them.

## 5. Interactions

**Depends on:**
- **Time, sleep and the clock** (`06-time-sleep-and-the-clock.md`; `tick-and-scheduler.md`) — the
  heartbeat that would check the due list, the activity/process model events interrupt, and the 20×
  sleep-consensus advance the escalation calendar rides on top of.
- **Warmth, clothing and shelter** (`08-warmth-clothing-and-shelter.md`) — the cold row's numbers feed
  the warmth-floor math; storm bands change exposure.
- **Food and hunger** (`10-food-and-hunger.md`) — the food row.
- **Injury and first aid** (`11-injury-and-first-aid.md`) — the injuries row.
- **The pilot and bodies** (`12-the-pilot-and-bodies.md`) — the pilot's scripted moaning/death event;
  bodies persisting afterward.
- **Perception** (`perception-model.md`; `19-multiplayer-and-instances.md`) — event narration routed by
  band; the weather stub's visibility bands.
- **Rescue paths** (`14-rescue-paths.md`) — the search & rescue event category; the confidence threshold
  the "rescued" ending needs.
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

1. **Are the ladder's numbers final or starting points?** The source itself calls them "proposals for
   Andrew's review, tunable by probes." *Options:* lock them now vs. treat them as tunable starting
   points revisited once probes/playtest exist. *Recommendation:* starting points — tune by probes, as
   the source already intends.
2. **What ships in the event deck's first version — the full deck above, or a subset?** *Options:* ship
   everything listed now vs. ship a smaller first subset (e.g., weather + one wildlife thread) and grow
   the rest by evidence, matching the "every count is a floor" rule used everywhere else in this
   project. *Recommendation:* a first subset, named explicitly in the review conversation, with the
   remaining categories tracked as floors to build on.
3. **How are lethal cards (the moose, wolves testing a lone traveller, a snow load dropping on someone
   underneath) kept "telegraphed, never a scripted kill" in practice?** The source states the rule but
   not the mechanism. *Options:* rely on the sign-before-danger convention alone vs. require each lethal
   card to document its own escape/mitigation path when authored (echoing the rescue-graph's "≥3 paths"
   habit). *Recommendation:* the latter — document the escape path alongside each lethal card as it's
   authored, not after.
4. **Is "still going" truly endless, or does an agents-only research run need a practical ceiling?** The
   ladder's own claim is that any party gets an ending within roughly two weeks. *Options:* no cap for
   any run vs. a session-length ceiling for agent-only research runs specifically (a practical limit,
   not a narrative one). *Recommendation:* no cap for human/mixed runs; flag the agent-only case for
   `20-the-agent-player-and-research.md` rather than deciding it here.
5. **Which temperature curve governs — the GDD's §8 line (−15 to −20 °C) or the ladder's
   December-recalibrated column (−12 to −42 °C across ten days)?** The GDD's figure predates the
   December decision. *Options:* keep both as-is vs. correct the GDD to point here. *Recommendation:*
   the ladder's December numbers govern; the GDD should carry a corrective note once this document is
   reviewed.
6. **Does the ladder's storm-band row (§4.2) map onto the perception model's existing
   `WEATHER_BAND_STEP` keys (`clear`/`light_snow`/`steady_snow`/`heavy_snow`/`whiteout`), or does weather
   need richer state (visibility in meters, wind direction) than those five keys carry?** *Options:*
   reuse the five shipped keys as the v1 weather model vs. design a richer state now. *Recommendation:*
   reuse the five keys for v1 — they're already wired into `visual_band`/`audible` — and open a
   follow-up only if a specific mechanic needs more.

## 7. Review log
None yet — first draft, not yet reviewed with Andrew.

- **2026-09-18 (Andrew, via document 08):** the ladder's first rungs are constrained by the **night-one
  rule** — night one must be survivable inside the wreck in the starting clothes, with no fire and no
  huddle, and night two must not be. The day-1/day-3 temperatures are tuned until both are true
  (document 08 §4.1a).

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
