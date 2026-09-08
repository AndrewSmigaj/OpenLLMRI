# Events & escalation — the world moves, the cold closes in, and nothing is a barrier

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07, late).** Andrew's brief:
> heavy snow starts at some point; other events (a bear, or whatever); the game runs roughly a
> WEEK — rescue can come earlier, it can run longer until the food runs out — but it is not a
> permanent survival game: instead of hard time-window barriers, **increase the things that cause
> death** (temperature drops) so that a party that is not rescued dies honestly. **There is no set
> arc**: what to do is the players' decision. Events are seeded and deterministic (DR-12), so a run
> replays byte-for-byte. Promotes to `docs/architecture/events.md` + DR-30 on approval.

## 1. The two clocks (what "a week" means)
- **The world clock** runs continuously (DR-14) at 15 real-s per game-minute — ~1.6 real hours per
  game day when the party is active. **Sleep and `wait` advance it by consensus** (DR-14a, in
  `time-and-stakes.md` §9): when every connected player is resting, the heartbeat runs at 20× until
  a target time or an interrupting event. So a week of game time is a few sittings, and a party that
  keeps busy pays for it in cold.
- **The escalation calendar** is indexed by game day, not by real time: the world gets deadlier on
  its own schedule whether the party acts or sleeps.

## 2. The escalation ladder (the "should kill them" curve — deterministic, telegraphed, no barriers)
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
| **the pilot** | lucid windows, fragments | fading | dies | a body | — | information stops; the moral question starts |
Nothing here refuses a player; every line is a number that hurts more each day. A party that
does everything right can last past day ten; a party that does nothing dies by night three.

## 3. Endings (all honest, none a timer)
- **Rescued** — an overflight sees a signal inside a weather window and confidence is over the
  threshold: a helicopter on the ice by afternoon, or a plane drops a note. The recap (P7).
- **Walked out** — Holt's cabin: the stove, a radio or a snowmachine; "we can outlast this" is
  rescue confidence too.
- **Dead** — cold, starvation, a fall through ice, CO in a closed fuselage, the wreck sliding.
  Individually or all; the run ends when the last player dies. A dead player's body persists.
- **Still going** — no cutoff; the ladder guarantees an ending within ~two weeks of game time for
  any party, because cold and food only get worse.

## 4. The event menu (seeded; each fires when its preconditions hold and its day/hour arrives)
**Weather** (the storm system, P7 seam): first flurries · the heavy snow begins (Andrew's fixed
beat — day 2–3) · wind shift (the breach faces it now) · whiteout (visibility band 0 outside) ·
clear-cold night (aurora; −40) · sun break (the mirror window) · thaw-refreeze (overflow, black
ice) · the second storm.
**Wildlife** (all telegraphed by sign first — tracks, calls, the cold-shower gag):
ravens scout the wreck (they find the food cache before you do) · a fox trots the tussocks · a
**wolverine raids the cache** at night (fearless; the classic camp thief) · **wolves** howl the second
night, tracks circle the wreck by the fourth, they test a lone traveller on the ice (a real
danger, never a scripted kill) · a lynx print, never the lynx · ptarmigan flush (food if you're
quick) · a hare in the snare · a moose on the trail (a wall of meat that kills the careless; not
food unless the party can kill it, which they can't) · an owl at night · a snow load drops off a
bough onto whoever stands under it. **The bear:** Alaska bears den by early winter; a bear is
plausible only if the crash is late October (a hungry, late-denning grizzly drawn by the meat
smell) or if the tail section came to rest on a den. If Andrew wants the bear, set the calendar
to late October / early November and make it the rarest, loudest event in the deck — otherwise
the wolverine and the wolves are the honest antagonists of a December valley.
**Search & rescue** (the rescue system's own events): the day-1 overflight in the wrong area (heard,
not seen) · the day-2/3 search plane crossing the valley (seen if a signal is up: smoke, fire on the
ice, the mirror in sun, the ELT if an aircraft is overhead to hear 121.5) · a helicopter on a clear
day if confidence is high · a snowmachine on the lake at dusk (Holt? someone from upriver — a
chance to be seen, and a story) · a distant chainsaw (the upriver village exists).
**The wreck**: fuel drips and pools under the wing (a fire hazard and a fuel source) · the fuselage
shifts on the slope with a groan (things slide; the door jams) · a window pane falls in · the tail
section slides further down the scar · the battery freezes (the radio route's clock) · the
extinguisher's bracket lets go · ice seals the cargo door overnight (dig or pry).
**Bodies**: the pilot's lucid windows and his death · a wound infects · frostbite whitens a finger ·
snow blindness on the ice · hypothermia confusion (messages, not command hijacking) · dehydration
headaches · the hunger stages.
**Camp**: the fire dies on an untended watch · the drift buries the entrance · the ice booms at
night (harmless here, terrifying) · a bough dumps its snow on the lean-to · the creek overflows the
crossing · tracks in the morning that weren't there (the fox, the wolves, a moose).
**Mail & freight** (story beats, found not fired): the postmarks; the parcel addressed to Holt; the
child's letter; a parcel of candles; dog food in the freight.

## 5. How an event runs (the mechanism, for time & stakes)
An event is a **scheduled process** with preconditions: `Event{day, hour_window, seed_jitter,
preconditions(world) -> bool, effects, narration by band, interrupts: bool}`. The heartbeat
checks the due list each tick; fired events apply Effects through `apply()` (a drift is mass; a
wound is state), route their narration through the propagator by band (the wolves are heard from
the treeline, seen from the ice), and — if `interrupts` — wake sleepers and break activities. All
draws come from the run seed (DR-12): the same run replays the same week.

## 6. Lens pass
### Surprise (GD) — GREEN. The deck is large and seeded; no two parties see the same week in the
same order, and every event is telegraphed by sign the curious can read first.
### Challenge (GD) — GREEN. The ladder is the antagonist; it never stops and never cheats.
### Meaningful Choices (GD) — GREEN. No arc means every day is a choice: dig out, gather, signal,
travel, tend, sleep. The ladder prices each.
### Story Machine (GD) — GREEN. Tracks that circle, a plane that misses you, a wolverine in the
cache: these are stories the recap can name.
