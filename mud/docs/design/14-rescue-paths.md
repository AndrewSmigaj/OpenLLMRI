# 14 — Rescue: the radio, the voice, signals, and surviving long enough

> **Status: reviewed with Andrew 2026-09-28.** Architecture counterpart:
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §8
> (DR-16). §3 was written on 2026-09-27 from the rescue conversation with Andrew (`PLAN.md` A13); he
> reads it whole at this document's sitting.

## 1. Decisions

### Andrew's decisions
- **(2026-09-07)** Every goal has several ways, with no set number — getting the radio working and
  using it, surviving until help arrives, finding food, finding warmth.
- **(2026-09-16)** The whole valley — every outdoor place — is in the first complete run.
- **(2026-09-17)** The only endings are **rescued or dead**. Walking out is not an ending, and Holt's
  cabin is supplies. Rescue comes **three ways** — the radio, a signal a search plane can see, and
  surviving long enough — and players never see a number. The flyover schedule is the rescue clock:
  a flyover is heard approaching, seen, passes over and leaves slowly, as planes do when they are
  searching, and there can be a few passes; an early flyover comes for the story, before a party is
  likely to be ready. Burning Holt's cabin down during a flyover brings a rescue. Searching the ground is
  an activity.
- **(2026-09-17)** The pilot starts the run dead; the party does not need him to work out the rescue.
- **(2026-09-18)** The radio's signal is continuous and heard as the world: a high screech of static
  with the antenna down, a low hum with it up, a faint voice as the dial turns, clearer as the signal
  improves; talking back gets broken answers asking you to repeat, and word to improve the signal.
  One person can work the radio while another gets food. The `make a signal` goal rows (§3.4).
- **(2026-09-26, 2026-09-27)** The season is the first week of October; the weather is the same every
  run (document 13 §4.2).
- **(2026-09-27)** Rescue is designed together with Andrew; nothing is added to it without asking him.
- **(2026-09-27)** **The ELT is broken.** The plane's battery is in the nose, wired and fine.
- **(2026-09-17, 2026-09-27) Two radios.** **The plane's radio** runs off the plane's battery, so power is
  not its problem; **a hand radio in Holt's cabin** has no batteries — they are buried in a bag or
  luggage in the plane's tail section, so a party finds the radio and must come back to search the tail
  for its batteries.
- **(2026-09-27) The plane's radio.** Something is needed to open it. Inside is a loose wire: a character
  with technical proficiency sees it on inspecting the inside; anyone else finds it more slowly, and
  the world hints that it may take them a while. The antenna is anything metal and long enough,
  raised — higher is better, a poor match only weakens the signal, and there is no finding the right
  length. A dial and a set of channel buttons, one of them the emergency channel: try them all, or
  find the frequency written down. Hold the button to talk; a player who does not is hinted. The
  power drains with use and the light dims; the cold does not stop a battery in a week. Contact comes
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

### Left to Claude, at Andrew's request (kept 2026-09-28)
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
**The radio** — two of them. The plane's own radio has power from the plane's battery but will not
work: you find something to open it and a loose wire inside, fix the antenna and get it high, and work the dial and the channel buttons
until, through the screech and the hum, a faint voice answers — a person who wants to know where you
are, and who will come at the next daylight good for flying. And in Holt's cabin, a long walk away, a hand
radio sits without its batteries, which are buried somewhere in a bag in the plane's tail. **A signal a search plane can see** — you
hear the engines first, and have that long to get smoke up dark against the snow or white against the
spruce, or the blue tarp spread in the open; you might not make it. **Surviving long enough** — on the
seventh day the rescuers find everyone still alive (2026-09-29); before then, under a half-clouded sky
and with the trees around the wreck, being found by an early pass is work.
None of it shows a number, and nobody tells you what to do — except the voice on the radio, who talks
like a rescuer. Meanwhile staying alive has its own several ways, in documents 08–11. (Written from Andrew's decisions.)

## 3. The design

### 3.1 Three ways home (Andrew, 2026-09-17)

The only endings are **rescued or dead**; walking out is not an ending, and Holt's cabin is supplies. Rescue
comes three ways: **the radio**, **a signal a search plane can see**, or **surviving long enough**: on day 7 the
rescuers find everyone still alive (2026-09-29). **The ELT is broken** (2026-09-27). Players never see a number.

### 3.2 The radio (Andrew, 2026-09-17, 2026-09-18, 2026-09-27)

- **Two radios** (2026-09-17, 2026-09-27). **The plane's radio**, powered by the plane's battery in the
  nose (wired and fine), whose fault is a loose wire; and **a hand radio in Holt's cabin**, without its
  batteries. **Holt's radio's batteries are buried in a container — a bag or luggage — in the plane's tail
  section**: a party has to find the radio and come back to search the tail. The tail lies on bare, frosty ground at the start and gathers a
  little snow with each flurry, a couple of inches by the end (document 13 §4.2), so the longer a party
  waits, the more there is to brush off and the colder the hands that sort through it. Finding them is
  searching the ground and sorting through the wreckage, as on 2026-09-17.
- **Getting the plane's radio working.** You need **something to open it**: its case is screwed shut, and anything
  that can turn a screw serves — a knife's tip, the multitool, a coin, a key, a seat-belt buckle's steel
  tongue (2026-10-02; document 18 §4.5). Inside is **a loose wire**: a character
  with technical proficiency sees it on inspecting the inside; anyone else finds it more slowly, and the
  world says so when they look inside — the wiring means little to them, and this may take a while —
  the same way fire is slower for some (characters differ in how well and how fast they do things,
  2026-09-27). **Fix the antenna and raise it**: anything metal and long enough serves, higher is
  better, and a poor match only weakens the signal — there is no finding the right length of wire.
  *(Open since 2026-10-03: whether the loose wire stays inside the radio, which gives players no sign it is
  there, or moves somewhere with a visible symptom. The placeholder at the end of this section answers it
  for now — under seat 1B — and flags that as a change for Andrew's ruling.)*
- **Holt's hand radio** works once its batteries are in. *(Claude's reading, not yet decided: it is used
  the same way — the dial, the channels, the voice — and, being a hand radio, it can be carried up high.)*
- **Using a radio.** A **dial and a set of channel buttons**, one of them the emergency channel: try them all,
  or find the frequency written down (where it is written is content, in the plane). **Hold the button
  while you talk**; a player who talks without it is told why nothing went out, in the world's voice.
- **The signal is the world.** Static — a high screech with the antenna down, a low hum with it up — and
  a faint voice as you turn the dial, clearer as the antenna goes up. A bad signal lets only some words
  through; that is the world, like everything else in it.
- **Power.** It **drains with use, and it shows** — the radio's light starts to dim. A week of cold
  does not stop a battery.
- **Contact.** Not tied to flyovers: **once the antenna is fixed, contact comes relatively quickly.**
  One person can work the radio while another gets food.

#### The plane's radio, stage by stage — placeholder

> **Placeholder — Claude's choice, 2026-10-04; to be replaced by the puzzle chosen from the swarm.**
> Andrew chose to let Claude's full version stand in until then (2026-10-04). Nothing here is his decision
> except where it repeats the decisions above. **It changes two of them**, flagged where they occur: the
> battery drains from the crash onward (stage 0), and the loose wire sits under seat 1B, not inside the
> radio (stage 1). Both wait for his ruling; until then the decisions above stand.

The plane's radio is meant as the opposite of Holt's: Holt's is simple to work out but costs a long walk
there and back; the plane's is right there in the wreck but takes thinking, testing and teamwork. Its
sound is the progress bar — every fix changes what players hear: silence → crackles → a high screech → a
low hum with voices in it → someone answering. There are four problems; each shows itself, each needs
things found around the wreck, and each has more than one way to fix it.

- **Stage 0 — waking up.** The dashboard is faintly lit and a little dimmer every hour: the pilot never
  got to switch the main power off, so the battery is slowly draining. *(Flagged change: the battery is
  fine but draining, not simply fine.)* A party can switch it off now to save the battery, or leave it on
  while they work things out; either way every later try costs power and the radio's light dims, as
  decided. A careful party gets everything ready before switching on to talk. If the battery runs flat,
  the plane's radio is gone and Holt's radio is the way left. *(Starting point, tuned in play: flat by the
  evening of day 2 if nobody ever switches it off.)*
- **Stage 1 — power to the radio.** The dashboard is lit but the radio is dark. Now and then the speaker
  in the ceiling spits a burst of static — when someone shifts in or bumps the wrecked seat 1B, or when
  the plane settles with a groan. The radio's power wire runs under the floor, and the wrenched seat has
  crushed it, so it touches only when the seat moves. *(Flagged change: this is the loose wire, moved
  from inside the radio to under seat 1B, where it has a symptom.)* The clue is that the crackle follows
  the seat.
  - **Reaching it:** unbolt the seat (pliers, a wrench, or the kid's multitool); pry it off its rails with
    something long and strong, which takes two people to lift; or leave it and cut through the floor
    covering beside it with a knife. Under it is a floor panel held by screws, which anything that turns
    a screw opens (document 18 §4.5).
  - **The fix:** light, because it is dark under there — the pilot's weak flashlight (the loose AA battery
    under a seat fits it), the guide's headlamp, a phone, or daylight through the hull's tear; something
    sharp to strip the wire, then twist the ends together; something to wrap the join — tape from the
    toolbox, medical tape from the nurse's pouch, or a strip of cloth bound tight.
  - **The difficulty:** with the main power on it sparks — a scorched wire end and stung fingers,
    nothing worse — so stage 0's switch matters: off to work, on to test. Fine work needs bare hands, and
    the cold numbs them (document 08). Two people help: one holds the light while the other works.
  - **What the world says:** a technically proficient character examining the dashboard learns that
    power reaches the dashboard but not the radio, and that a bundle of wires runs down under the floor
    toward the seats; anyone else is told the wiring means little to them and this may take a while, as
    decided.
  - **The reward:** the radio's small screen lights up, and it gives the high screech of the antenna
    being down, as decided.
- **Stage 2 — the antenna** (as decided, with two people). On the roof is a torn stub with a cable end
  sticking out where the antenna sheared off. Any metal long enough, joined to the cable end and raised —
  higher is better: a wire coat hanger from a suitcase (a new object), seat tubing, the wing's control
  cables, wire from the dashboard, guitar strings; lashed to a branch or a pole to get it high.
  - **Warmer, colder:** one person moves the antenna around on the roof while another, inside, hears the
    screech soften into a hum or come back, and calls out through the hull. Alone it just takes longer:
    climb down to listen, then go back up.
  - **The reward, the puzzle's biggest surprise:** as the dial turns, the hum fills with voices — the
    robot voice of a weather station somewhere, reading wind and temperature, which never answers; an
    airliner talking to Anchorage; and the search planes talking to each other, searching the planned
    route, nowhere near. The party hears itself being looked for in the wrong place, and learns roughly
    where and when the planes will fly (the flyover schedule, §3.5).
- **Stage 3 — being heard.** They talk, and nobody answers; a small light on the radio that should come
  on when you talk stays dark. The plane's hand microphone was smashed in the crash and hangs from its
  hook in pieces.
  - **The pilot's headset, still on his head:** it plugs into the sockets beside his seat — one plug to
    listen, one to talk. Taking it off him gets harder the longer they wait, as he stiffens and freezes;
    this gives the dead pilot a real part in the radio.
  - **The right-hand seat's headset, its cord cut:** strip and join tiny wires with numb fingers —
    slower, but no need to touch the body.
  - The hint for talking without holding the button still applies, as decided.
- **Stage 4 — who to talk to.** The radio is still set to the last frequency the pilot used, and there is
  only hum on it (the ridge blocks it). The right channel: try them one by one, as decided; read the
  pilot's notepad, strapped to his leg, with that frequency, a few others along the route and the
  emergency one (a new object); or read the frequencies printed on the chart. Later, once they reach
  someone, the voice tells them part of the pilot's mayday was heard — which is why the search is only
  roughly in the right area.
- **Stage 5 — the first answer: the airliner window.** Contact comes fairly quickly once the antenna is
  fixed, as decided, and the real reason it can is airliners: jets crossing Alaska listen on the
  emergency channel and, from 11 km up, can hear a weak radio in a valley. A crew answers — they hear
  the plane weakly and ask for its position. The airliner is passing over, so the party has about an
  hour of game time (a few real minutes at 15×) to say where it is before it is out of range; then the
  crew hands it to the search-and-rescue voice (§3.3), and the decided design takes over — landmarks,
  homing in if the party cannot say, the pickup at the next daylight good for flying, the battery dimming
  all the while. Two people help again: one on the fuselage top or up the knob calls out what they can
  see while the other relays it on the radio.
  - **For the ambitious:** unbolt the radio and the battery (about 11 kg together) and carry both up the
    knob for a much stronger signal — a two-person job; wiring them back together is easier for the
    technically proficient character.

**Keeping it possible.** The crackle can't be missed, because the plane's own groans set it off. Every
stage has at least two ways, and the technically proficient character gets clearer clues at each.
Everything happens in or on the plane apart from the tools, and the toolbox and the multitool are in the
tail. Rough length: one to two hours of real play across the stages, split among the party — longer to
work out than Holt's radio, but with no long walk.

**New things it needs, if it stands:** on the dashboard, the main power switch, the speaker in the
ceiling and the radio's small talk light; for talking, the smashed hand microphone, the pilot's headset
(on him) and the right-hand seat's headset with its cut cord; for the wire, the crushed wire and the
screwed floor panel under seat 1B; on the pilot, the notepad strapped to his leg; in a suitcase, a coat
hanger; on the radio, the search planes' chatter, the weather robot and the airliner's lines.

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
  chart in the cockpit names landmarks — on the redesigned map (document 01, for Andrew's review), the
  lake, the creek, the knob with its survey marker, the old burn and Holt's cabin — so a party that works
  out where it is gets home sooner.
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

**The `make a signal` rows** (the goal chosen 2026-09-18; its rows kept 2026-09-28). The goal table's rows for this system; the form and
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
- (The rest of the schedule is Claude's, at Andrew's request, kept 2026-09-28:) day 1 at dusk the early
  pass, high along the filed route — heard far off, for the story; day 2 the route search, across the
  ridge in the afternoon — a chance for a party with a signal ready; day 3 the search widening off the
  route, a pass heard in the next valley and lost in the cloud; day 4 a pass across the lake's far end,
  seen through a gap in the cloud — a real chance; day 5 the search narrowing toward this valley, a pass
  low along the creek in the afternoon — a real chance; day 6 the flurry grounds the search and nothing
  flies; **day 7 the rescue of everyone still alive**, in clear air over fresh snow.
- **Findable takes work — for the early passes** (days 2–5): partial cloud and the trees hide the wreck from the air, so what the party
  builds decides it — smoke kept going, the
  tarp laid out, a sign laid or scraped in the open; the chimney smoke at Holt's cabin is a sign by
  itself. A party in radio contact that is not findable is
  told what to do.

### 3.6 Staying alive meanwhile

Warmth, water, food and injury each have their own document (08, 09, 10, 11) and their own several
ways.

### 3.7 Not in the design (decided)

A working ELT · the walk-out as an ending · a wire-length puzzle · a wet radio · a rescue-confidence number · boats · the plane's battery powering the hand
radio (the plane's battery powers the plane's radio).

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
  two radios — the plane's radio on the plane's battery, with the loose wire, and a hand radio in Holt's
  cabin whose batteries are in the tail; the antenna; the channels;
  holding the button to talk; the draining light; contact not tied to flyovers; the voice; signals seen by
  physics, the plane heard first; the default rescue on day 7. §3 written from it.
- **2026-09-27 (Andrew)** — the trapper does not come back; not a way to be rescued.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2); the tarp is also a ground signal.
- **2026-09-28 (Andrew, the document's sitting):** the flyover schedule with document 13's numbers;
  homing in on a party that cannot name a landmark — far slower than naming one, and it drains the
  batteries; being seen follows physics, with markers (three of anything, or SOS) and the flare; Holt's
  own traces tell the party he is not coming back. **Reviewed in full.**
- **2026-10-04 (Andrew):** the plane's radio puzzle in full is Claude's placeholder (§3.2) until the puzzle
  chosen from the swarm replaces it; its two changes to the decisions — the battery draining from the
  crash, and the loose wire under seat 1B — are flagged there and wait for his ruling.

## 7. What exists today

**Designed, not built:** everything in §3 exists only as prose. No probe chain exists for any of it:
`game/world/scenarios/whiteout/probes/` holds `census.py`, `chain.py`, `kit.py` and `phrasing.py`, and
none of them walks a way home. The valley the rescue relies on — Holt's cabin, the lake shore, the ridge
— exists only as design: `game/world/scenarios/whiteout/zones.py` holds the nine crash-site zones
(cockpit, mid_cabin, rear_cabin, outside_nose, fuselage_top, outside_tail, debris_trail, tail_section,
treeline). Building the outdoor places is tracked separately (`PLAN.md`).

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
  'sheared'}`), each with a description in `appearance.py`. The design has two radios — the plane's
  radio on the plane's battery, with a loose wire, and a hand radio in Holt's cabin whose batteries are in a
  bag in the plane's tail — and the ELT is broken.

**Built, and a foothold:** a generic `wire` object; the guitar's strings yield `loose_wire` when
removed; the material table carries a `conductivity` ordinal on metals and `copper_wire` — the start of
"anything metal and long enough". In the probe corpus, `census.py` records the radio as something to
take and listen to, marked `todo`; `phrasing.py` checks that sentences like "turn on the radio" parse,
which tests the parser only.

**Nothing:** the batteries' bag in the tail, the written frequency, a mirror or a tire as objects; any
radio signal, voice, flyover, detection or weather gating; any probe or fuzz coverage of the ways home.
