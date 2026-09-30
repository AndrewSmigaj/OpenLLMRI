# 14 — Rescue: the radio, the voice, signals, and surviving long enough

> **Status: reviewed with Andrew 2026-09-28.** Architecture counterpart:
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §8
> (DR-16). §3 was written on 2026-09-27 from the rescue conversation with Andrew (`PLAN.md` A13); he
> reads it whole at this document's sitting.

## 1. Decisions

### Andrew's decisions
- **(2026-09-07)** Every goal has several ways, with no set number — getting the radio working and
  using it, surviving until help arrives, finding food, finding warmth.
- **(2026-09-16)** The whole valley — all fifty outdoor zones — is in the first complete run.
- **(2026-09-17)** The only endings are **rescued or dead**. Walking out is not an ending, and Holt's
  cabin is supplies. Rescue comes **three ways** — the radio, a signal a search plane can see, and
  surviving long enough — and players never see a number. The flyover schedule is the rescue clock:
  a flyover is heard approaching, seen, passes over and leaves slowly, as planes do when they are
  searching, and there can be a few passes; an early flyover comes for the story, before a party is
  likely to be ready. Burning Holt's cabin down during a flyover brings a rescue. Searching the ground is
  an activity.
- **(2026-09-17)** The pilot starts the run dead and carries no clues.
- **(2026-09-18)** The radio's signal is continuous and heard as the world: a high screech of static
  with the antenna down, a low hum with it up, a faint voice as the dial turns, clearer as the signal
  improves; talking back gets broken answers asking you to repeat, and word to improve the signal.
  One person can work the radio while another gets food. The `make a signal` goal rows (§3.4).
- **(2026-09-26, 2026-09-27)** The season is the first week of October; the weather is the same every
  run (document 13 §4.2).
- **(2026-09-27)** Rescue is designed together with Andrew; nothing is added to it without asking him.
- **(2026-09-27)** **The ELT is broken.** The plane's battery is in the nose, wired and fine; it does
  not power the hand radio.
- **(2026-09-27) The radio.** A hand radio in the plane's cabin; its batteries are buried in a bag
  or luggage in the plane's tail section. Something is needed to open it. Inside is a loose wire: a character
  with technical proficiency sees it on inspecting the inside; anyone else finds it more slowly, and
  the world hints that it may take them a while. The antenna is anything metal and long enough,
  raised — higher is better, a poor match only weakens the signal, and there is no finding the right
  length. A dial and a set of channel buttons, one of them the emergency channel: try them all, or
  find the frequency written down. Hold the button to talk; a player who does not is hinted. The
  batteries drain with use and the light dims; the cold does not weaken them. Contact comes
  relatively quickly once the antenna is fixed — not only during flyovers. The radio is interacting
  with the world, not a separate game: a bad signal that lets only some words through is part of the
  world. Common sense is hinted, in the world's voice.
- **(2026-09-27) The voice.** A person at search and rescue, played by a weak language model — the same
  model every run, scaffolded with rules. It helps only as a real rescuer would, and may hint (raise
  the antenna), heard through the bad signal, so it can take a few tries. It asks for landmarks and
  judges what it is told by criteria the game gives it — the list of landmarks and what each is
  worth; this is the one exception to the engine never calling a language model (GDD §3 rule 2). Once
  contact is made and it judges it can find the party, the pickup comes at the next daylight good for
  flying — the day-6 flurry is the only day nothing can land or fly. It tells a party it cannot find
  what it needs to do.
- **(2026-09-17, 2026-09-27) Signals.** Fire and smoke — rubber, oil, green boughs; a piece of mirror
  once clear of the trees; burning Holt's cabin during a flyover; the blue tarp laid in the open, which
  a plane can see — the same tarp that seals the plane's openings, so one tarp has two uses and the
  party chooses. The plane is heard before it is seen; a party may not make it in time.
- **(2026-09-17, 2026-09-27) Surviving long enough.** Search and rescue is searching — that is why
  planes come. The same flyovers every run. No big storm: snow on and off, and a heavier flurry on
  day 6 that grounds the search and clears for day 7; the sky is always at least partly cloudy, so
  planes fly most days, but the wreck is hard to see from the air (document 13 §4.2). **The default
  rescue is day 7.** Being findable takes work. No boats.

### Left to Claude, at Andrew's request (for his check)
- A party that cannot say where it is can be **homed in on**, at a battery cost (§3.3) — accepted,
  realism first: it takes far longer than flying to a named landmark (2026-09-28).
- **Whether a crew sees a signal follows physics** — what the signal is and how it contrasts, the
  weather, how close the pass comes (§3.4) — accepted (2026-09-28).
- **The rest of the flyover schedule** (§3.5; document 13 §4.2) — accepted with document 13's numbers
  (2026-09-28).
- **(2026-09-27)** Holt, the trapper, does not come back during the week; the cabin is supplies, not a place to be
  rescued from. **His own traces tell it** (2026-09-28), and nothing else does: the gear he carries on
  the line is gone from its pegs (spare snares and traps stay); a calendar on the wall has the days
  crossed off to late September and a date circled weeks after this week; the stores are modest and
  the stove cold, the way someone leaves a place for a while. A careful reader works it out; a careless
  one waits.

### Proposals (Claude)
None left: the `make a signal` rows' marker and flare roles were accepted (2026-09-28, §3.4).

## 2. In one paragraph

Nobody is looking where you are yet, but search and rescue is searching. There are three ways home.
**The radio** — a hand radio sits in the plane's cabin, dead, its batteries somewhere in a bag in the
tail section, which gathers a little more snow with every flurry you wait; you find something to open it
and a loose wire inside, fix the antenna and get it high, and work the dial and the channel buttons
until, through the screech and the hum, a faint voice answers — a person who wants to know where you
are, and who will come at the next daylight good for flying. **A signal a search plane can see** — you
hear the engines first, and have that long to get smoke up dark against the snow or white against the
spruce, or the blue tarp spread in the open; you might not make it. **Surviving long enough** — on the
seventh day the search comes for a party it can find, and under a half-clouded sky, with the trees
around the wreck and the white plane on white ground after the sixth day's snow, being findable is work.
None of it shows a number, and nobody tells you what to do — except the voice on the radio, who talks
like a rescuer. Meanwhile staying alive has its own several ways, in documents 08–11. *(Written
2026-09-27 from Andrew's decisions, for his check.)*

## 3. The design

### 3.1 Three ways home (Andrew, 2026-09-17)

The only endings are **rescued or dead**; walking out is not an ending, and Holt's cabin is supplies. Rescue
comes three ways: **the radio**, **a signal a search plane can see**, or **surviving long enough** for the
search to reach a party it can find. **The ELT is broken** (2026-09-27). Players never see a number.

### 3.2 The radio (Andrew, 2026-09-17, 2026-09-18, 2026-09-27)

- **What and where.** A **hand radio in the plane's cabin**. Its **batteries are buried in a container — a bag or
  luggage — in the tail section**; the tail lies on bare, frosty ground at the start and gathers a
  little snow with each flurry, a couple of inches by the end (document 13 §4.2), so the longer a party
  waits, the more there is to brush off and the colder the hands that sort through it. Finding them is
  searching the ground and sorting through the wreckage, as on 2026-09-17.
- **Getting it working.** You need **something to open it**. Inside is **a loose wire**: a character
  with technical proficiency sees it on inspecting the inside; anyone else finds it more slowly, and the
  world says so when they look inside — the wiring means little to them, and this may take a while —
  the same way fire is slower for some (characters differ in how well and how fast they do things,
  2026-09-27). **Fix the antenna and raise it**: anything metal and long enough serves, higher is
  better, and a poor match only weakens the signal — there is no finding the right length of wire.
- **Using it.** A **dial and a set of channel buttons**, one of them the emergency channel: try them all,
  or find the frequency written down (where it is written is content, in the plane). **Hold the button
  while you talk**; a player who talks without it is told why nothing went out, in the world's voice.
- **The signal is the world.** Static — a high screech with the antenna down, a low hum with it up — and
  a faint voice as you turn the dial, clearer as the antenna goes up. A bad signal lets only some words
  through; that is the world, like everything else in it.
- **Power.** The batteries **drain with use, and it shows** — the radio's light starts to dim. The cold
  does not weaken them.
- **Contact.** Not tied to flyovers: **once the antenna is fixed, contact comes relatively quickly.**
  One person can work the radio while another gets food.

### 3.3 The voice on the other end (Andrew, 2026-09-27)

- A person at search and rescue, **played by a weak language model** — the same model in every run,
  scaffolded with rules; a character played from outside like any other, and the one exception in GDD §3
  rule 2. It is a fixed condition in research runs (document 20).
- It **helps only as a real rescuer would**: stay with the plane, keep warm, save your battery, a fire we
  can see when you hear us. It **may hint** — *"you're breaking up — can you get your antenna higher?"* —
  heard only as far as the signal lets it through, so it can take a few tries.
- It **asks where you are** and **judges what it is told by the game's criteria — the landmarks and what
  each is worth**: a party that says it is next to a river is told there are a lot of rivers; another
  landmark narrows it.
- A party that cannot say where it is can be **homed in on** (2026-09-28): it has to keep
  transmitting while a search plane flies around taking bearings on it, and bearings give only a
  general area, so the plane circles to narrow it — far longer than flying straight to a named
  landmark, and longer still if the party moves. Every minute on the air drains the batteries. The
  chart in the cockpit names landmarks, so a party that works out where it is gets home sooner.
- **The pickup comes at the next daylight good for flying** (2026-09-27), once contact is made and the
  voice judges it can find the party; the day-6 flurry is the only day nothing can land or fly, and the
  voice says when they will come.
- A party in contact that is not findable is **told what it needs to do**.

### 3.4 Signals a plane can see (Andrew, 2026-09-17, 2026-09-27)

- Fire and smoke — rubber, oil, green boughs, whatever really makes smoke — a piece of mirror once clear
  of the trees, **burning Holt's cabin down during a flyover**, which brings a rescue, and **the blue
  tarp laid in the open** (2026-09-27): bright blue against brown ground or new snow is something a crew
  can see. It is the same tarp that seals the plane's openings (document 16 §4.5), so one tarp has two
  uses — keep the plane warm or signal — and the choice is the party's.
- **Whether a crew sees a signal comes from physics** (2026-09-28): what it is and how it contrasts — dark smoke from rubber or oil against snow, white smoke
  from green boughs against dark forest, fire at night, the tarp's blue, the white wreck against brown
  ground until the day-6 snow makes it white on white, signs laid out on the ground or scraped through
  the snow to the dark ground beneath, three fires in a triangle — the weather (wind flattens smoke;
  cloud hides the ground from a pass; the day-6 flurry hides everything and grounds the planes), the
  trees between the signal and the sky, and how close the pass comes.
- **The plane is heard before it is seen** — a window to light a fire laid ready, which a party may
  miss.

**The `make a signal` rows (Andrew, 2026-09-18).** The goal table's rows for this system; the form and
the dispatch rule are document 04 §3.9. Vague, `make` asks how; given the means it performs the act
they imply and this system answers.

| field | a signal |
|---|---|
| `goal` | a signal · smoke · to be seen |
| `vague` | "How are you going to signal?" |
| `roles` | **fire** (lit) · **smoke-maker**: rubber, oil, green boughs · or **reflector**: the mirror, the landing-light reflector, in sun |
| `realize` | `put <smoke-maker> on <fire>` · `signal with <reflector>` — and whether anyone sees it is the flyover clock's answer, not the command's |

The row set is a floor — the loops add goals and means from what people and agents type (2026-09-28).

**roles** also (2026-09-28) **marker** — anything that contrasts with the
ground, laid or tramped large: the blue tarp, boughs, dark cloth, luggage, wreckage on snow, or lines
stamped or scraped through the fresh snow to the dark ground; three of anything, or SOS, is the
international distress sign · **pyrotechnic** — the flare, one shot, fire or signal, never both. **realize** also `put <marker> on <snow>`, `light <flare>`, `tramp <snow>`. Which
smoke-maker suits depends on the background, which the world already knows: rubber and oil make dark
smoke that shows against snow; green boughs make white smoke that shows against dark spruce.

### 3.5 Surviving long enough, and the flyovers (Andrew, 2026-09-17, 2026-09-27)

- **Why planes come:** search and rescue is searching for the plane. A flyover is heard approaching,
  seen, passes over and leaves slowly, as planes do when they are searching (2026-09-17).
- **The same weather and the same flyovers every run.** No big storm: snow on and off, the sky always
  at least partly cloudy, so planes fly most days; **a heavier flurry on day 6** grounds the search and
  clears overnight for day 7 (document 13 §4.2).
- **The game ends on day 7** (2026-09-29) — the survived-long-enough rescue: the crew find everyone
  still alive, wherever they are, and a rescuer entering a room rescues whoever is in it (document 21
  §4.3). The early ways home bring the helicopter sooner.
- *(The rest of the schedule is Claude's, at Andrew's request, for his check:)* day 1 at dusk the early
  pass, high along the filed route — heard far off, for the story; day 2 the route search, across the
  ridge in the afternoon — a chance for a party with a signal ready; day 3 the search widening off the
  route, a pass heard in the next valley and lost in the cloud; day 4 a pass across the lake's far end,
  seen through a gap in the cloud — a real chance; day 5 the search narrowing toward this valley, a pass
  low along the creek in the afternoon — a real chance; day 6 the flurry grounds the search and nothing
  flies; **day 7 the rescue of everyone still alive**, in clear air over fresh snow.
- **Findable takes work — for the early passes** (days 2–5): partial cloud and the trees hide the wreck from the air, and after day 6's
  snow the white plane is white on white, so what the party builds decides it — smoke kept going, the
  tarp laid out, a sign laid or scraped in the open; the chimney smoke at Holt's cabin is a sign by
  itself. A party in radio contact that is not findable is
  told what to do.

### 3.6 Staying alive meanwhile

Warmth, water, food and injury each have their own document (08, 09, 10, 11) and their own several
ways.

### 3.7 Not in the design (decided)

A working ELT · the walk-out as an ending · a wire-length puzzle · a wet radio · the pilot as a clue
source (he starts dead) · a rescue-confidence number · boats · the plane's battery powering the hand
radio (the battery is in the nose, wired and fine).

### 3.8 Content this needs (not questions — work for when the zone is built)

Where the emergency frequency is written; which characters are technically proficient (document 16's
slots); the landmark list and what each is worth, for the voice's criteria; the voice's scaffold rules;
what opens the radio. Each is written with Andrew when its document or zone is designed.

## 4. Interactions

**Depends on:**
- **06 Time, sleep and the clock** — the flyovers and the voice run on the world clock; a flyover is
  not an ambient event, so it drops fast forward back to 15×; searching the ground and working the
  radio are activities, and one person can do one while another does something else.
- **13 Events, escalation and weather** — the day-6 flurry that grounds the search, the partial cloud
  that hides the ground from a pass, and the snow that gathers on the tail and turns the wreck white on
  white; the weather state (13 §4.7) — cloud, visibility, wind, light — that decides whether a
  plane flies low and whether a signal is seen; the flyover schedule in 13 §4.2's search row.
- **07 Fire and shaping** — the fire under every smoke signal, and Holt's cabin burning.
- **08–11 (warmth, water, food, injury)** — staying alive until one of the ways home comes through;
  an injured party digs, climbs and carries less.
- **16 Players and kit** — which characters are technically proficient; what the party carries that can
  open the radio or serve as an antenna; the luggage in the tail that holds the batteries; the blue
  tarp, a seal or a signal.
- **18 Materials and forms** — what is metal and long enough to be an antenna; what burns into dark or
  white smoke.
- **01 Premise and world** and **17 Rooms and living rooms** — the plane's cabin, where the radio is,
  and its tail section; Holt's cabin; the landmarks the voice judges; the open ground a signal can be
  seen from.
- **04 Grammar and feedback** — holding the button to talk; the `make a signal` rows (04 §3.9); hints in
  the world's voice, never a list.
- **GDD §3 rule 2** and **20 The agent player and research** — the voice's judgement is the rule's one
  exception, and the voice is a fixed condition in research runs.
- **19 Multiplayer and instances** — the plane heard before it is seen, by whoever is in earshot.

**Depended on by:**
- **21 Endings** — "rescued" is this system's outcome.
- **13** — the ladder's search row and the deck's search cards.
- **03 The player view** — the static's screech and hum, the voice through the noise, engines heard and a
  plane seen: all in prose, never a number.
- **20 The agent player** — an agent reaches rescue from the same world a human does, with the same
  hints and no menu.

## 5. Open questions

None open.

## 6. Review log

- **2026-09-17 (Andrew, ahead of this document's sitting):** the endings, rescued or dead; the three ways;
  the flyover schedule as the rescue clock; searching the ground as an activity.
- **2026-09-18 (Andrew):** the radio's continuous signal, heard as the world; the `make a signal` goal rows.
- **2026-09-26 (Claude's self-review):** the rescue checked against real small-aircraft search and rescue;
  the findings were taken into the rescue conversation.
- **2026-09-27 (Andrew, the rescue conversation):** the ELT is broken; the plane's battery in the nose;
  the hand radio in the plane's cabin and its batteries in the tail; the loose wire; the antenna; the channels;
  holding the button to talk; the draining light; contact not tied to flyovers; the voice; signals seen by
  physics, the plane heard first; the default rescue on day 7. §3 written from it.
- **2026-09-27 (Andrew)** — the trapper does not come back; not a way to be rescued.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2); the tarp is also a ground signal.
- **2026-09-28 (Andrew, the document's sitting):** the flyover schedule with document 13's numbers;
  homing in on a party that cannot name a landmark — far slower than naming one, and it drains the
  batteries; being seen follows physics, with markers (three of anything, or SOS) and the flare; Holt's
  own traces tell the party he is not coming back. **Reviewed in full.**

## 7. What exists today

**Designed, not built:** everything in §3 exists only as prose. No probe chain exists for any of it:
`game/world/scenarios/whiteout/probes/` holds `census.py`, `chain.py`, `kit.py` and `phrasing.py`, and
none of them walks a way home. The valley the rescue relies on — Holt's cabin, the lake shore, the ridge
— exists only as design: `game/world/scenarios/whiteout/zones.py` holds the nine crash-site zones
(cockpit, mid_cabin, rear_cabin, outside_nose, fuselage_top, outside_tail, debris_trail, tail_section,
treeline). Building the fifty outdoor zones is tracked separately (`PLAN.md`).

**Built, but carrying the retired model** (rewritten when the rescue is built):
- `game/world/sim/systems/rescue.py` holds one function, `confidence(channels)`, which raises
  `NotImplementedError`; its docstring describes the retired additive-confidence model and a radio
  state machine. `game/world/scenarios/whiteout/rescue.def` is a comment-only placeholder describing
  the same.
- `game/world/scenarios/whiteout/authored.py` — the authored-rule seam is live (the resolver consults
  `AUTHORED` before the generic handlers), but the dict is empty, and its docstring still names the
  ELT.
- `objects.py` authors `radio` as a field radio in the cockpit (`plastic`/`copper_wire`, `state:
  {powered: False, fixed: True}`) and `elt` in the tailcone (`state: {armed: True, antenna:
  'sheared'}`), each with a description in `appearance.py`. The design puts a hand radio in the plane's
  cabin with its batteries in a bag in the tail, and the ELT is broken.

**Built, and a foothold:** a generic `wire` object; the guitar's strings yield `loose_wire` when
removed; the material table carries a `conductivity` ordinal on metals and `copper_wire` — the start of
"anything metal and long enough". In the probe corpus, `census.py` records the radio as something to
take and listen to, marked `todo`; `phrasing.py` checks that sentences like "turn on the radio" parse,
which tests the parser only.

**Nothing:** the batteries' bag in the tail, the written frequency, a mirror or a tire as objects; any
radio signal, voice, flyover, detection or weather gating; any probe or fuzz coverage of the ways home.
