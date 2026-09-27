# 14 — Rescue paths: the goals, ≥3 paths per goal, the flyover clock, the radio, the ELT, signals, surviving long enough

> **Status: draft for review.** Architecture counterpart:
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md) §8
> (DR-16). Sources: [`../investigation/design/rescue-graph.md`](../investigation/design/rescue-graph.md)
> (primary — the graph); [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md) §37–39, §19;
> `docs/scenarios/whiteout/design.md` §7, §37–39 (the archived AI seed — where the additive-confidence
> model and the radio/beacon workflows first appear, plain path, not linked — see the doc-consistency
> gate); [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md)
> §7–8 (DR-16); [`../scenarios/whiteout/roadmap.md`](../scenarios/whiteout/roadmap.md) P5;
> [`../investigation/world/map.md`](../investigation/world/map.md) §1;
> [`../investigation/world/report.md`](../investigation/world/report.md) §2; the code
> (`game/world/scenarios/whiteout/rescue.def`, `authored.py`, `objects.py`, `zones.py`,
> `game/world/sim/systems/rescue.py`) and the probe corpus
> (`game/world/scenarios/whiteout/probes/`). Provenance method:
> [`../investigation/design/00-provenance-audit.md`](../investigation/design/00-provenance-audit.md).

This is spread across five places today (a scratchpad, the GDD, the archived seed, the architecture
doc, and the code). This document is the one place it lives from here on. It does not decide anything
new — Andrew has not reviewed it yet — it collects and cross-checks what already exists. *(Since
written: Andrew's answers of 2026-09-17 — the box at the head of §3 — and Claude's self-review of
2026-09-26, which answers what real search and rescue and the decided design answer, in §3.5a and §5,
for Andrew's check.)*

## 1. Provenance

### Andrew's decisions (quoted, with dates)

**The rescue goals (2026-09-07).** Andrew set them directly: fix the radio, use the radio, then
survive until help arrives, find food, find warmth — with several ways of doing each; his own example
was fire: "you could find a lighter if you look hard enough but can light it other ways." *(This
document could not find a verbatim transcript of this exact phrasing in the repo; it is relayed by the
task that produced this document and is consistent with the paraphrase in the provenance audit §1,
"The world and the run (2026-09-07)": "things facilitate the rescue goals; several ways of doing
things"; "Fire is made *somehow*: rubbing sticks fails and the game says so; a bow drill works; a
lighter lights tinder, not a branch." Flagged here so a reviewer with the original transcript can
confirm the exact words.)*

**No lethal-consent gate; `use X on Y` resolves silently (2026-09-16).** Directly relevant to two
rescue paths below: butchering the pilot's body (a food path) and any violence among survivors resolve
with real physics, not an engine refusal — "violence resolves with real physics."

**The pilot dies within the first day; nobody can talk to him (2026-09-16, amended the same day).**
"No language model behind him" — scripted things only: "moaning heard only in the cockpit, maybe a
line." His body then persists (a food path and a moral question). What his lines carry as clues is
reviewed in [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md), not here (§19 of the GDD stands
until that review; provenance audit §4: "my earlier 'not a clue source' was wrong and is corrected").
*(Superseded 2026-09-17: **the pilot starts the run dead** — he has no lines, so he carries no clues;
every fact he would have carried is reached by paths in the world instead (§3.4, §3.6, §3.9).
`PLAN.md` §5; document 12.)*

**The whole valley is in the first complete run (2026-09-16).** All fifty outdoor zones — so the
travel/shelter and visual routes' anchor terrain (the lake, the ridge, the creek–trapline–homestead
line) is in scope for the first run, not a stretch goal, even though none of it is built yet (§7 below).

**The beacon/radio wire overlap is reviewed here, not asked separately (2026-09-16).** Per the
provenance audit §4: "the beacon/radio wire overlap is a note inside the rescue-paths design, reviewed
there." Reviewed in §3.4's distinctness check and flagged as open question 5.

**The watch rule and the clock (2026-09-07, amended 2026-09-16).** One acting player holds the running
clock at 1×; others wait for the next event; the clock may run 20× by consensus when everyone sleeps or
waits, and events interrupt it. This is what a rescue "weather window" (§3.5) actually runs against —
there is no separate planning-freeze for it. *(Superseded 2026-09-17: the clock runs at 15
game-minutes per real minute and `propose fast forward` raises it to 180× when every player agrees,
events dropping it back; "watch rule" was Claude's label and is dropped — being awake is being on
watch (document 06).)*

**Rescue, the endings and the radio (2026-09-17).** The only endings are rescued or dead; the
walk-out is closed and the cabin is supplies; rescue comes three ways, each harder than the last — the
radio during a flyover, a signal a search plane can see, surviving long enough; the flyover schedule
is the rescue clock and players never see a number; the radio (no "mini game" — the world, Andrew 2026-09-27) and the battery in the tail
wreckage under the snow; searching the ground as an activity. In full in the box at the head of §3
and in the review log.

**October, and a bear (2026-09-26).** The season is October at freeze-up: an inch of snow at the
start, and a storm that starts light and gets heavier over the days (the banner quotes in documents
13 and 23; `PLAN.md` §5). *(What that means for rescue — Claude's, for Andrew's check: about ten
hours of light; the lake open or skimmed with new ice until late in the week (document 13 §4.2); and
a storm that grounds the search while it lasts and leaves behind it the clear, calm cold that is the
search's best weather.)*

**Andrew's standing complaint, applied here.** "Most of them are just half thoughts, half attempts to
just put something there not well thought out design." Where a source below is thin (the confidence
threshold, the ≥4 count), this document says so as an open question rather than inventing a number to
fill the gap.

### Proposals (Claude)

Everything else in this document is a proposal, not a decision, layered across four passes:

- **`design.md` §7, §37–39 (first AI seed, dated by file — 2026-06-29).** This file is explicitly
  labelled "the first AI-written design," archived, superseded by the GDD. It is the origin of: the
  idea that rescue confidence is *additive and partial* ("players can be rescued through different
  combinations"), the beacon workflow and its six-step signal-quality ladder, and the authored radio
  workflow with its own six-state progress ladder, the antenna-quality-from-material/length/connection/
  height/placement/snow/weather rule, and the list of where location information can come from. None of
  this is Andrew's verbatim words; it is Claude's first attempt to operationalize his rescue goals.
- **`GDD.md` §37–39, §19 (2026-09-16).** Promotes the above, keeping it "your additive-confidence
  model" in tone but adding one explicit improvement — routes must draw on **distinct** scarce
  resources — and a concrete number, **≥4 winning combinations**, that does not appear in `design.md`
  (which lists nine *example* combinations but never states a minimum).
- **`rescue-graph.md` (2026-09-07 investigation pass).** Reorganizes the above into **five** named
  channels (splitting `design.md`'s blended beacon/radio/visual/travel list into stay-and-signal,
  beacon, radio, visual, travel/shelter as coequal accounts), introduces the **six currencies**, and
  produces the per-goal (warmth/water/food/injury) path tables with rooms and probe-chain seeds — the
  "several ways of doing things, checkable" the provenance audit credits to this pass.
- **`map.md` / `report.md` (2026-07-15 investigation pass, world design).** Anchors each route to a
  valley region and restates the routes as room itineraries. Notably, `report.md` §2's own route table
  lists only **four** routes (stay-and-signal, beacon, radio, travel/shelter) — it does not carry
  "visual" as a fifth, separately-accounted route the way `rescue-graph.md` (written three weeks later)
  does. That is flagged as open question 1, not silently resolved here.
- **`implementation-architecture.md` §8 (DR-16).** Formalizes the above into a schema
  (`RescueState{channels: {...}: 0..1}`, `confidence = Σ weight·value` capped at 1) and a radio FSM.
  One naming drift, worth fixing before P5 authors it: `design.md` §38.6 names the fifth radio state
  `two_way_contact_no_location`; the architecture doc and `roadmap.md` both shorten it to
  `two_way_no_location`. Harmless, but the two sources should agree on one spelling. *(Moot since
  2026-09-17: the radio's signal is continuous, not a state machine — §5 Q3; and the additive
  confidence is replaced by §3.5a — §5 Q2. Claude, 2026-09-26.)*
- **`roadmap.md` P5.** Sets the build-time exit-gate numbers: survive the first night via **≥3**
  warmth strategies, rescue reachable via **≥4** distinct combinations, the radio puzzle solvable **≥3**
  ways, the pilot's death never softlocks (his facts have **≥3** clue paths each per the GDD).

## 2. In one paragraph

At the start the radio is dead, the beacon in the tail is shouting on 121.5 into a sheared antenna,
and nobody is looking where you are: the pilot filed a route and left it, and the search will fly
that route first. There are three ways home, each harder than the last. **The radio** — find the
battery in the tail wreckage under the snow, get an antenna up and high, and while a plane is
overhead turn the dial through the screech and the hum to a faint voice, and piece its words together
until it knows where you are. **A signal a search plane can see** — a smoke column dark against the
snow on a calm, clear day, three fires in a triangle at night, a mirror flash in the low October sun,
a flare, a V tramped big into fresh snow — up at the moment a plane passes, which mostly means after
the storm, when the air is still and the wreck itself has vanished under the snow. **Surviving long
enough** — staying alive and findable until the search's late pass reaches you. None of it is
instant and none of it shows a number: you hear engines, you see a plane rock its wings, a voice asks
you to repeat. Meanwhile staying alive has its own several ways — warmth, water, food, injury — each
spending something different, so a party good at one is not automatically good at all of them.
*(Claude, 2026-09-26 — rewritten to Andrew's 2026-09-17 decisions and to October; for Andrew's check.)*

*The September draft of this paragraph — five routes, the walk-out, the plane's one flare — is
superseded by the 2026-09-17 decisions and kept as the record:*

> At the start, the radio is dead and the beacon is weak — Andrew's own framing, carried since the first
> seed doc. There is no single "real" way out: the party can stay near the wreck and make itself seen
> (fire, smoke, a ground sign), fix the beacon and get its antenna clear, fix the radio and get useful
> words through static, signal visually with a mirror or the plane's one flare, or walk out toward Holt's
> homestead. Each of these draws on a different scarce thing — fuel, elevation, battery power and a
> clear weather window, a flare or daylight, or the willingness to spend days walking — so no single
> resource running out (cold, especially) can kill every route at once. None of it works instantly:
> progress is layered and partial, reported by feedback that never says "you have solved it," and a
> weak signal repeated stubbornly can still eventually matter. Meanwhile the same "several ways" rule
> applies inside the survival goals that keep the party alive long enough to be found — warmth, water,
> food, injury all have more than one path, and the paths cost different things so a party that is good
> at one is not automatically good at all of them.

## 3. The design

> **Reopened with Andrew, 2026-09-27 — rescue is designed together, and nothing is added to it without
> asking him.** *"this whole rescue scenario will need thought please dont just blindly agree it pisses me
> off I want help designing this, i just dont want you to add things without explicitely asking me."*
> Decided the same day: **no working ELT** (*"otherwise this wouldnt even be a game"*); **the battery is
> in the nose, wired up and fine** (the tail battery of 2026-09-17 is superseded); **the radio has a loose
> wire inside**, which a character with technical proficiency sees on inspecting it. Everything below that
> is not Andrew's words — the channels, the arithmetic, §3.5a's search model, the ELT section — is the
> record of what was weighed, not a design he has accepted (`PLAN.md` A13).
>
> **The radio so far (Andrew, 2026-09-27, the rescue conversation):** a **hand radio in the cabin**; its
> **batteries are buried in a container — a bag or luggage — in the tail section**. You need something to
> open the radio; it has **a loose wire inside**, which a technically proficient character sees on
> inspecting it, and anyone else finds more slowly (*"you are not technically proficient so this might
> take awhile"*). You **fix the antenna and raise it** — higher is better; there is no finding the right
> length of wire. It has **a dial and a set of channel buttons**, one of them the emergency channel: try
> them all, or find the frequency written down. The batteries **drain with use, and it shows** (*"the
> light starts to dim, perhaps the radio is draining"*). Not in: a wet radio; a wire-length puzzle.
> Search and rescue is searching — that is why planes come. **Answered the same day:** someone can answer
> **not just during a flyover — once the antenna is fixed, contact is relatively quick** (supersedes the
> 2026-09-17 "usable only during flyover events"); the cold does **not** weaken the batteries — only use
> drains them.
>
> **After contact (Andrew, 2026-09-27):** the pickup waits on the weather — the voice on the radio can say
> they will come *"once the storm dies down"*. **The person on the other end is played by a weak language
> model**, because players will want to talk to them — a character played from outside, like any other
> (GDD §3 rules 2 and 5): the engine decides when the rescue flies; the voice only speaks it. Players
> hold the button while they talk into the mic; if they don't, the world hints. *"a lot of things might
> need hints i dont want users figuring out common sense things."* **Where they are — Claude's choice
> (2026-09-27), at Andrew's request, for his check:** the voice asks; whatever the party can tell —
> the lake, the ridge, the burn, the chart — narrows the search; if they can tell nothing, a search plane
> homes in on their transmissions when it is in the area, which costs battery.
>
> **The radio is the world, not a mini game (Andrew, 2026-09-27):** *"there is no such things as a 'mini
> game' there is interacting with the world and certain steps would need to be taken to get to a rescue
> condition. so when the signal is bad and they can only hear certain words thats just part of the
> world."* **The voice is scaffolded not to help too much** — only what a real rescuer says (stay with the
> plane, keep warm, save your battery, a fire they can see when you hear them). It asks for a landmark:
> *"you can tell them you are next to a river and they would be like 'there are a lot of rivers' and you
> can give them another landmark - the llm can make a judgment on if the information is good enough."*
> **Settled the same day:** *"i need one because they are talking to someone. the someone can hint at
> things like needing to raise the antenna though it might take a few tries given we only show certain
> words. yes we will keep the same model and scaffold it with rules."* and *"the llm can judge based on
> criteria we give it such as the list of landmarks and their value."* The voice may hint as a rescuer
> would (*"you're breaking up — can you get your antenna higher?"*), heard only as far as the signal lets
> it through; the game gives it the landmarks and what each is worth; the same model plays it every run.
> GDD §3 rule 2 carries this as its one exception.


> **Decided with Andrew, 2026-09-17:** the only endings are **rescued or dead**; walking out is not an ending
> and the cabin is supplies. Rescue comes three ways, each harder than the last: **the radio** during a
> flyover; **a signal** a search plane can see (a smoke column — rubber, oil, green boughs — past a
> threshold; or the cabin burning during a flyover); or **surviving long enough** for the search to
> reach a findable party (at the wreck, at the cabin, or under a signal). The flyover schedule is the
> rescue clock and players never see a number: an early pass for the story (too early to succeed),
> then real chances, then the late pass that is the endurance rescue. **The radio, as Andrew designed
> it:** it needs the battery, which is in the tail wreckage under the snow (light snow on day one,
> more by the second morning), found by searching the ground — an activity that lists things slowly,
> which then appear in the description — and by sorting through the wreckage, prying where needed. It
> works only during a flyover; otherwise static (a possible "air traffic" label as a hint, or let them
> work it out). Signal quality is continuous — battery, antenna up or down and how high, the plane's
> nearness — mapped to prose: a high screech with the antenna down, a low hum with it up, a faint
> voice as you turn the dial, clearer as it improves. Talking back gets snippets — "can't hear you,
> repeat", in variants — and the words *improve your signal* and *adjust antenna* ride on the better
> bands: ~~a medium-difficulty mini game~~ piecing the message together from what the signal lets through *(Andrew, 2026-09-27: "there is no such things as a 'mini game' there is interacting with the world")*, then the rescue ending if
> they survive the time it takes. One person can work the radio while another gets food. **Open for
> this document's sitting:** whether the ELT (the silent beacon you rig an antenna onto) stays as a
> second path or folds into the radio. The graph below is the September draft. *(Claude, 2026-09-26:
> the ELT question is sharpened with the real device's facts as §5 Q7; §3.5a replaces the September
> draft's confidence arithmetic with how a real search finds a party, for Andrew's check.)*

### 3.1 The goals

What "win" and "not lose" decompose into (`rescue-graph.md` §1):

- **Stay alive** — warmth, water, food, injury; each is its own goal with its own ≥3 paths (§3.2).
- **Be found** — rescue confidence, the sum of five channels, must clear a threshold inside a weather
  window; ≥4 winning combinations; no single object is required by every channel (`GDD.md` §37–39).
  *(Superseded: rescue comes Andrew's three ways (2026-09-17), and being found is a pass seeing or
  hearing a signal, or the late pass reaching a findable party — §3.5a and §5 Q1, Q2, Q6.)*
- **Keep the party alive** — the injured co-player: carry, bind, warm them. *(The pilot dies within the
  first day and cannot be talked to — Andrew, 2026-09-16; his body is a food path and a moral question,
  reviewed in [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md).)* *(Superseded
  2026-09-17: he starts the run dead.)*

### 3.2 Stay alive — ≥3 paths per goal, each spending a different resource

From `rescue-graph.md` §3, the crash-cluster graph (v1). Every path also spends the common survival
economy (wood, food, daylight); what makes route choice real is the **key** resource column, which must
differ between a goal's siblings.

**WARMTH** (the antagonist is cold; the GDD's warmth floor guarantees a fire-less night is survivable
*— superseded 2026-09-18 by the night-one rule: night one survivable inside the wreck in the starting
clothes, and from night two the cold climbs (document 08 §4.1a); the "floor" row below is night one
only*):

| path | key resource | rooms | probe chain (seed) |
|---|---|---|---|
| fire (7 methods — doc 07, fire-and-shaping) | fuel + an ignition source | treeline / north wood (fuel); the source's room | lighter path; bow-drill path; battery path |
| insulation salvage | tools (to strip) + time | mid/rear cabin (foam, batting, blanket, engine cover, clothes) | `wear blanket` · `cut cushion` → stuff jacket · `wear engine cover` |
| shelter / windbreak | sweat + tools | rear cabin (block the breach with the sheet), outside (snow wall, boughs) | `cover breach with sheet` · `put boughs on floor` |
| huddle + fuselage + body heat (the floor) | nothing but proximity | any enclosed zone | `huddle with agent-2` (P6) |

Softlock guard: the floor path needs no object; the fire paths need ≥2 different ignition sources
present at start (the lighter and the flare and the battery and the friction kit are all in the crash
cluster). *(Claude, 2026-09-26: "the floor" is now night one only — document 08 §4.1a; the battery
is in the tail wreckage, Andrew 2026-09-17.)*

**WATER:**

| path | key resource | rooms | chain |
|---|---|---|---|
| the canteen / thermos as found | knowledge (search) | cockpit, rear cabin | `search backpack` → `drink from canteen` |
| melt snow/ice by fire in a vessel | fuel + a vessel | anywhere + fire | `put snow in thermos` → `put thermos by fire` → `drink` |
| melt by body heat (slow, costs warmth) | warmth | any | `put snow in canteen` → wear it under the jacket (time) |
| the lake lead / the seep (valley) | risk + daylight | inlet_mouth, shore | `fill canteen from lead` |

Eating snow is always possible and always costs heat (the manual's lesson; a redirect with a
consequence, never a refusal). *(Claude, 2026-09-26 — October: open water is easier than the
December draft assumed. The creek runs all week behind a rim of shelf ice, the lake is open or
skimmed with new ice until late, and the riffle never closes — each a `fill` source (document 09
§4.6), priced in wet feet and thin ice rather than in fuel; document 13 §4.2's ice row.)*

**FOOD:**

| path | key resource | rooms | chain |
|---|---|---|---|
| the kit (rations ×2, chocolate, flour, coffee tin) | search | seat pocket, survival duffel, crate | `open tin` → `eat rations` |
| the country (grubs, cranberries, hare snare, fish) | knowledge + tools + daylight | tamarack, tussocks, willows, the lead | `set snare with paracord at willows` (P5) |
| the pilot's body | the moral price (doc 15, moral and social layer) | cockpit | `butcher pilot with knife` |
| Holt's cache | travel | homestead | the travel route's reward |

*(Claude, 2026-09-26 — October: the country is richest at the start — berries still on the bush,
grouse on the ground, fish in open water, roots in soft ground — and closes as the storm buries it
(document 13 §4.2's food row; documents 10 and 23 own the rows and the numbers). The pilot's body is
there from the first minute, since he starts the run dead.)*

**INJURY** (the cut forearm; frostbite; a co-player's break):

| path | key resource | rooms | chain |
|---|---|---|---|
| the first-aid kit (bandage, tape) | search | mid cabin bin | `press wound` → `wrap arm with bandage` |
| improvised (spare shirt strips, whisky as antiseptic, paracord + a rod as a splint) | tools + knowledge | rear cabin, duffel | `tear shirt` → `pour whisky on wound` → `wrap arm with strip` |
| warmth for frostbite (skin-to-skin, no rubbing — the manual) | warmth | any | `wrap hands in socks` · sit by fire |

### 3.3 The six currencies

`map.md` §1: a path must spend a *different* key account from its siblings; every path also spends the
common economy (wood, food, daylight):

| Currency | What spends it |
|---|---|
| **Daylight** | travel and work both burn the ~~about 5 h~~ light budget — *October: about 9 h 45 min sunrise to sunset on day 1, ~11 h 20 min with civil twilight, falling about 7 minutes a day (document 13 §4.2; Claude, 2026-09-26)*; the storm shortens it further |
| **Warmth** | every zone has an exposure band; open ice and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt |
| **Tools** | blade, chopper, saw, container, cordage — each unlocks a different shelf of the world |
| **Knowledge** | reading sign: tracks, ice colour, blaze marks, the dead lower branches of a spruce *(renamed by Claude, 2026-09-26 — the old woodsman's term for them is a slur)*; `examine` is the tutor |
| **Risk** | thin ice, overflow, the cornice, the climb — always telegraphed, never random *(October: thin ice is the risk of the whole week; overflow belongs to midwinter, once the ice is thick; the cornice builds only after the storm's wind — Claude, 2026-09-26)* |

`map.md`'s own thesis: **each region anchors one rescue route** — the lake anchors the visual route
(open sightlines), the ridge anchors radio/beacon (elevation), the creek–trapline–cabin line anchors
travel/shelter (distance and navigation), and the crash site anchors stay-and-signal (the known point
searchers will eventually grid). The forest ring in between is the survival economy every route spends
from. *(Claude, 2026-09-26 — October: the lake is open water and skim ice at the start and holds a
careful person only late in the week (document 13 §4.2), so its shore, the gravel and the muskeg
edge are the open sightline until then; travel/shelter is no longer a rescue route — the cabin is
supplies, and being there keeps a party findable (2026-09-17).)*

### 3.4 Be found — the five channels

*(Superseded as a structure 2026-09-17: rescue comes Andrew's three ways — the radio during a
flyover, a signal a search plane can see, surviving long enough. The channels map onto them: the
radio is the radio; stay-and-signal, visual and — if Andrew keeps it — the beacon are the means of
"a signal"; travel/shelter is no longer a rescue way (the cabin is supplies, and a party there is
findable for the late pass). The table is kept for its clue paths and chains, corrected below where
a decision or the season moved them. §5 Q1.)*

From `rescue-graph.md` §3: each channel is a separate confidence account; ≥4 combinations should reach
the threshold.

| channel | key resource | rooms | clue paths (≥3 each) | chain |
|---|---|---|---|---|
| stay-and-signal (fire on the ice; the tire's black smoke; a ground sign) | fuel logistics + wind engineering | ice_flat, gear_gouge, crash site | the manual's SIGNALS page · the chart's search grid note · the reflector's glint (examine) | `put oil quart on fire` (smoke) · `put boughs on ice` (SOS) *(October: the ice holds only late in the week — the shore, the gravel and the muskeg edge until then; Claude, 2026-09-26)* |
| beacon (ELT) | conductor + elevation | tail_section (ELT), cockpit panel (wire) or dooryard cable, fuselage_top / the_knob | the manual's 121.5 page · examine the ELT ("antenna sheared") · the sheared base on fuselage_top | `take elt` → `tie wire to elt` → `go to fuselage top` → `tie wire to antenna base` *(its place among the three ways is Andrew's — §5 Q7)* |
| radio | carry logistics + weather windows ~~(the battery is 12 kg in the nose cowling)~~ *(superseded 2026-09-17: the battery is in the tail wreckage under the snow — Andrew)* | cockpit, ~~outside_nose (battery)~~ the tail wreckage (battery), the_knob | static-but-powered implies antenna · ~~the pilot's fragment~~ the aircraft's own handbook, which must be aboard — its ELT page says 121.5, save the battery until a plane is in sight, and switch the beacon off to talk *(replaced by Claude, 2026-09-26: the pilot starts the run dead)* · the chart's ridge bearing | ~~`pry cowling` →~~ `search the snow` / `sort through the tail` → `take battery` → `tie wire to radio` → `talk to radio` (~~the FSM: §3.5~~ the continuous signal, §3.6) |
| visual (mirror, reflector, flare) | the flare's one shot / sun for the mirror | crash site, ice_flat, fuselage_top | the reflector's glint · the manual · the survival mirror (census: under the seat) | `light flare` (spends the fire source) · `examine reflector` → `signal with reflector` |
| travel/shelter (the cabin) *(no longer a rescue way — 2026-09-17; the cabin is supplies, and these paths are how it is found)* | navigation + daylight | creek → trapline → homestead | the chart (V. HOLT) · blaze marks (knowledge) · ~~the pilot's "ridge"~~ the view from the knob — the homestead's clearing on its bench, seen from the valley's highest point *(replaced by Claude, 2026-09-26: the pilot starts the run dead)* | the walk, priced by the P4 durations |

**Distinctness check** *(a design note for this document's review, not a decision already asked of
Andrew)*: wire — beacon and radio share the conductor, "the ONE deliberate overlap the GDD flags"; the
dooryard cable is a second conductor so it is not a single point of failure — elevation, fuel/wind, the
flare, and navigation are otherwise separate accounts. No object is required by every channel; the
flare is fire OR signal (a genuine risk/reward triangle). Reviewed further as open question 5.
*(Claude, 2026-09-26: the dooryard cable is at Holt's homestead, 2.5 km away — a trip, not a
spare; and Alaska's statute requires **two** signalling devices in every in-state aircraft, "colored
smoke bombs, railroad fuses, or Very pistol shells, in sealed metal containers" (AS 02.35.110), so
the kit carries two unless the crash took one — document 16's to author. §5 Q5.)*

`report.md` §2 restates this as room itineraries and gives the same routes a slightly different shape
— see open question 1. *(Superseded with the channels, 2026-09-17; `report.md` is the investigation
record and is not maintained.)*

| Route | Rooms | Scarce resource | Confidence events |
|---|---|---|---|
| Stay-and-signal | crash site, ice_flat, gear_gouge, north-wood fuel zones | fuel logistics + wind engineering | fire visible on ice; the tire's black smoke column; maintained through the plane beat |
| Beacon | tail_section (the ELT), dooryard (cable) or avionics (wire), fuselage_top or the_knob | conductor + elevation | antenna rigged; elevation multiplier; the 121.5 manual clue closes the loop |
| Radio (the deep puzzle) | cockpit (the set), the wreck's batteries, the_knob | carry logistics + weather windows | static → voices on the knob; the heavy-band crackle; a working exchange in a clear pocket — the storm-phase second climb is this route's climax |
| Travel/shelter | creek run, trapline, homestead | navigation skill + daylight | the stove lit — survival secured buys the SECOND weather window; "we can outlast this" is rescue confidence too |

`report.md` §3 (the economies as room networks) restates fire, water, food, warmth/clothing, mobility,
fire-craft and information as full progressions across the valley, and calls information "the only
massless economy — which is why the_knob, pure information, justifies the map's hardest climb."

### 3.5 Rescue confidence — the arithmetic

*(Superseded 2026-09-26 by §3.5a, for Andrew's check: a real search is not a sum of weights against
a threshold — it is where the search flies and whether a pass sees or hears the party. The September
arithmetic is kept below as the record; DR-16 in the architecture register wants the same update.)*

`implementation-architecture.md` §8 (DR-16):

- **Additive confidence:** `RescueState{channels:{beacon,radio,landmark,visual,smoke,stay}: 0..1}`;
  `confidence = Σ weight·value` capped at 1; `rescued = weather_window AND confidence ≥ threshold`.
- **Distinct resources:** each channel's authored requirements draw on different scarce inputs (not
  all warmth/fire) so route choice is real and global softlock is avoidable.
- Enforced invariants (`GDD.md` §44/45): rescue confidence is **monotonic** (an action never lowers it
  behind your back) and **always reachable** from every sampled state (the solvability oracle,
  `roadmap.md` P5 exit gate; `rescue-graph.md` §4).

The exact weights, the threshold, and the ≥4-combinations count are not decided by Andrew anywhere this
document found — see open question 2.

### 3.5a How a real search finds a party — the flyover schedule and the pass (Claude, 2026-09-26 — §5 Q2; for Andrew's check)

Andrew set the shape on 2026-09-17: the flyover schedule is the rescue clock; players never see a
number; an early pass for the story, then real chances, then the late pass. Underneath it, a real
search answers two separate questions, and neither is a sum of weights.

**Where the search flies — what the searchers know.**

- **The flight plan starts it.** A VFR flight is overdue half an hour after its ETA; Flight Service
  sends an information request (INREQ) along the filed route at about an hour and an alert notice
  (ALNOT) at about two, and in Alaska the Rescue Coordination Center at Joint Base
  Elmendorf-Richardson launches the search (AIM 6-2-6; AOPA, "Rescue me!"). With no flight plan an
  Air Force review found about 36 hours pass before a family's worry starts one (AIM 6-2-6); which
  it was is written in the cockpit — the kneeboard, a copy of the plan (document 16 to author).
- **It flies the filed route first**, then widens into the ground beside it by probability. The
  pilot left his route to stretch for the lake (document 01 §4.1), so the early passes are in the
  wrong place — the premise's "wrong search area", made real.
- **Clues move it.** Anything that reaches the searchers shifts where the later passes fly: the ELT
  heard on 121.5 by any aircraft, a fragment of the party's radio call, smoke reported by a passing
  pilot, a landmark named on the radio. What the searchers know only grows — a clue once received
  is not unlearned — which is the old "monotonic" invariant made physical.
- **Weather gates it** (document 13 §4.7's cloud and visibility): search aircraft fly low only under
  a high enough ceiling and in enough visibility, so the storm's days are grounded and the clear, calm
  cold behind it carries the week's heaviest searching.
- **It ends.** Without new clues the search is scaled back and suspended as the planners' estimate of
  survival falls; the late pass is its last sweep over the widened area.

**Whether a pass finds you — computed at that moment, from what is physically there.**

- **What is up.** A smoke column — dark smoke (rubber, an oil-soaked rag) against snow, white smoke
  (green boughs smothering a fire) against dark spruce; smoke is "effective only on comparatively
  calm, clear days — high winds, rain, or snow disperse smoke" (FM 3-05.70, ch. 19). Three fires in a
  triangle about 25 m apart, the international distress signal (ibid.). A fire's light at night. A
  mirror flash — only in sun and only aimed; pilots have reported them from up to 160 km in ideal
  conditions (ibid.). A flare — a pen flare climbs about 150 m (ibid.) — one shot, spent at the
  right moment or wasted. A ground pattern in the international ground-to-air code — V (need
  assistance), X (need medical help), an arrow (going this way), Y, N — at least 6 m long and 4 m
  wide (FM 3-05.70; the AIM says at least 10 feet), tramped as trenches into snow or laid in boughs,
  dark on white, and in the low October sun its shadow is half the signal. A bright coat spread on
  the wing (document 08 §4.2). The wreck itself, which trees hide and, after the storm, snow buries.
  And, heard rather than seen, the ELT or the radio on 121.5 — line of sight to the aircraft, the
  antenna and its height (§3.6–§3.7).
- **The pass itself**: its track (how close it comes), its height (a Civil Air Patrol visual search
  flies about 1,000 feet above the ground), the visibility, the light, the sun's angle.
- **The odds without a signal are poor.** CAP's own worked example gives about 15 % for one pass over
  hilly tree cover at a one-mile track spacing and 25 % after a second, against up to 85 % over open,
  flat ground (CAP *Mission Aircrew Reference Text*, vol. II, §6.3) — which is why the signal is the
  game.

**What the party learns, without a number.** A crew that has seen you **rocks its wings** — the
AIM's signal for "message received and understood" (a flashing green light by night) — and circles,
or drops a message, or a voice on the radio asks you to repeat. Then help comes when the weather lets
it in — a helicopter within hours in clear weather, the next clear day if it closes — and the party
has to survive the time it takes (Andrew, 2026-09-17). Every number — each pass's chance of seeing
them, the shape of the search area — goes to the log only.

**The invariants, restated.** "Rescue always reachable" becomes: the late pass reaches any party that
is findable — at the wreck, at the cabin, or under a signal. "Monotonic" becomes: what the searchers
know never shrinks. The weights, the threshold and the "≥4 winning combinations" retire with the
additive model (§5 Q2, Q6).

### 3.6 The radio — the one authored deep puzzle

`design.md` §38 (the origin) and `GDD.md` §37–39 ("the radio is the one authored deep puzzle"). The
radio is part of the single authored crash scene, not procedurally generated, and deliberately does not
require repairing every subsystem:

> The radio has no power. The outside antenna is broken. The rescuers need useful location information.

That is the core route, not the whole interaction space — the microphone, speaker, frequency knob and
internal transceiver are damaged-looking but working enough for gameplay; players can still inspect,
test, damage or misuse them.

**Antenna quality** is computed from material, length, connection to the antenna lead, height,
placement, snow/ice coverage, surrounding wreckage and weather — not a per-object whitelist, so any
sufficiently long, metal, elevated, unburied, well-connected thing can work. `design.md` §38.3 lists
example materials: aircraft wire, copper cable, an aluminium seat frame, a metal pole, a strip of
fuselage metal, seat-frame tubing, a metal luggage handle, wire salvaged from electronics, the beacon's
own antenna (a costly tradeoff), or a knife/tool as a poor temporary conductor. The material table
already carries a `conductivity` ordinal property (`none`/`high`/`extreme`) on metals and `copper_wire`
— a real foothold for this rule, not just a placeholder (§7 below).

**The physics that rule computes** *(Claude, 2026-09-26 — §5 Q3; for Andrew's check)*. Aviation VHF
(121.5 MHz is the emergency frequency) travels in straight lines: the radio reaches a plane only if
nothing solid stands between them, so the valley's walls block it and height clears them. The radio
horizon is about 4.1 × (√h₁ + √h₂) km with the two heights in metres — an antenna at head height
reaches an aircraft 300 m up out to roughly 75 km over open ground, and far less where a ridge is in
the way; a 1978 Cessna 206 handbook puts its own ELT's range at "up to 100 miles at 10,000 feet". A
conductor radiates best near a quarter of the wavelength long — about 62 cm at 121.5 MHz (the speed
of light ÷ the frequency ÷ 4) — standing upright, joined at its base to the radio's antenna lead,
clear of the hull and the snow; much longer or shorter, bent, lying flat, buried, or touching the
metal, it radiates less. That is Andrew's "antenna up or down and how high" in the physics: *up* is
upright and clear, *how high* is the line of sight. The material table's `conductivity` says whether
a thing can be an antenna at all; its length, posture, connection and height say how good it is.

**The aircraft's own procedure** — the Cessna U206G handbook's ELT supplement, a document that must be
aboard the airplane: *"Prior to sighting rescue aircraft — conserve airplane battery. Do not activate
radio transceiver. After sighting rescue aircraft — place ELT function selector switch in the OFF
position, preventing radio interference. Attempt contact with rescue aircraft with the radio
transceiver set to a frequency of 121.5 MHz. If no contact is established, return the function
selector switch to ON immediately."* This is Andrew's radio exactly — the battery is the thing to
spend, and the radio is worth using only while a plane is near — and it adds one real coupling:
the beacon's tone on 121.5 swamps the party's own call, so someone has to switch it off to be heard
and on again after. *(Claude, 2026-09-26; for Andrew's check.)*

**Where the battery really is** *(flagged once, for Andrew — his 2026-09-17 decision stands)*. The
same handbook places the 206's 24-volt battery "on the upper left forward portion of the firewall" —
in the nose — while the ELT sits behind the baggage wall in the tailcone with its antenna on top of
the tail. A battery in the tail is real in Cessna singles (Cessna's own 1979 TR182 carries its 24-volt
battery in the tailcone, and moving it aft is a known weight-and-balance change), so the decision is
kept true to the airplane if this 206 is one that had its battery moved aft — something the
aircraft's logbook in the cockpit can say (document 16 to author).

**Radio feedback** must name signal quality explicitly so players can reason about the antenna
(`design.md` §38.4): `"... unidentified aircraft ... signal weak ... repeat ..."`,
`"... hearing you faintly ... improve your antenna if you can ..."`,
`"... we have partial transmission ... need location ... landmarks ..."`. With power but no usable
antenna, results are mostly static, with occasional broken fragments getting through — persistence is
never hard-blocked forever, but antenna repair stays the better path (§38.5).

**The six-state ladder** (`design.md` §38.6; renamed slightly by the architecture doc and `roadmap.md`
— see the naming-drift note in §1): *(superseded 2026-09-17 — Andrew: "signal quality is continuous —
battery, antenna up or down and how high, the plane's nearness — mapped to prose"; the six names
survive only as landmarks along that continuous quality for whoever writes the prose bands, and the
spelling drift no longer matters — §5 Q3)*

| state | description | rescue effect |
|---|---|---|
| `dead` | no lights, no sound | none |
| `powered_static` | the radio lights up and hisses | confirms power works |
| `weak_receive` | broken voices come through static | players may learn searchers are looking in the wrong area |
| `weak_transmit` | rescuers may hear a distress call but not enough to locate the crash | search confidence increases slightly |
| `two_way_contact_no_location` *(design.md) / `two_way_no_location` (architecture, roadmap)* | rescuers answer, but ask where the crash is | players need landmarks, route clues or beacon support |
| `useful_contact` | rescuers have enough information to narrow the search | rescue becomes likely when weather allows |

**Not instant rescue** (`design.md` §38.7): even useful contact does not end the run. Players may still
need to keep the radio powered, repeat contact during a weather window, keep the beacon or visual
signal active, stay near the known rescue area, survive cold/injury/nightfall, and prepare/clear
extraction signals.

**Location information** (`design.md` §38.8) can come from: ~~the pilot's fragment before he dies~~
the flight plan copy and the pilot's kneeboard — the filed route, and so how far off it the wreck lies
*(replaced by Claude, 2026-09-26: the pilot starts the run dead)*, the
cockpit nav log, a torn map mark, a visible red ridge before whiteout, river direction, landmark
alignment, a weather-relay sign, a description of the basin/wreck orientation/ridge shape, the beacon
signal combined with partial radio contact, or a visual signal spotted during a weather break. The
radio supports imperfect communication — fragments, not coordinates; the rescue system aggregates
confidence from them. *(Claude, 2026-09-26: in §3.5a's terms each fragment that gets through is a
clue that moves where the later passes fly — no confidence is summed.)*

The resolver's authored-rule seam for exactly this kind of object exists and is wired
(`game/world/scenarios/whiteout/authored.py`), but carries no radio content yet (§7 below).

### 3.7 The ELT (the beacon)

`design.md` §37: the beacon is one rescue path, not the only one. It improves search confidence and
starts or strengthens rescue progress; the group still has to survive, keep it transmitting, and make
themselves discoverable. Workflow: find the beacon, notice weak/intermittent behaviour, access the
casing, diagnose a power/antenna/switch/moisture issue, find or improvise a tool, secure the connection,
warm or insulate the battery, improve antenna placement, test the signal, protect it from snow, survive
while the search narrows.

**Beacon signal ladder** (`design.md` §37):

| state | value |
|---|---|
| `off` | 0 |
| `intermittent_weak` | 15 |
| `weak_but_stable` | 35 |
| `stable_at_crash_site` | 55 |
| `stable_with_clear_antenna` | 70 |
| `elevated_on_ridge_or_tree` | 85 |

Beacon success does not instantly win — it narrows the search, especially paired with visual signals,
radio contact, smoke, firelight, or staying near the wreck. In `rescue-graph.md`'s room terms: the ELT
itself sits in the tail section, its conductor is either the cockpit-panel wire or a dooryard cable, and
elevation comes from the fuselage top or the_knob.

**What the real device is** *(Claude, 2026-09-26 — the facts §5 Q7 turns on; for Andrew's check)*.
Whatever Andrew decides about its place among the three ways, the ELT is in the world as the real
thing it is — an entity with a switch (off · on · armed), a battery that runs down, an antenna socket,
a sound on 121.5 that anyone with a receiver can hear — because a real device a survivor would act on
is never taken out (writing rule: never make the world less interactive).

- **Two kinds exist.** The older kind (TSO-C91/C91a) transmits a swept tone on 121.5 MHz (and 243.0),
  about 75 mW; a 1978 Cessna 206's handbook gives 48 continuous hours between −40 and +55 °C, "line-of-
  sight transmission up to 100 miles at 10,000 feet", mounted "behind the baggage compartment wall in
  the tailcone", its antenna "mounted on top of tailcone". The newer kind (TSO-C126) sends a 5-watt
  digital burst on 406 MHz every 50 seconds for at least 24 hours at −20 °C, carrying the aircraft's
  identity, plus a 121.5 homing tone for 48 hours (manufacturers' specifications, e.g. the ACK E-04).
- **Since 1 February 2009 satellites listen only to 406.** Cospas-Sarsat stopped processing 121.5 and
  243 MHz; a 121.5-only ELT is still legal in a US aircraft, but only an aircraft within line of
  sight that is listening on 121.5 can hear it (Cospas-Sarsat; AOPA, "Answers for pilots: 406 MHz
  ELTs"; CAP, "The phaseout of 121.5 MHz beacons"). Airliners, search aircraft and many pilots monitor
  121.5; the AIM asks pilots to.
- **ELTs often fail in crashes, and the antenna is the classic failure.** NTSB data for 1983–87 found
  88 % of ELT failures crash-related — the g-switch, fire, impact, and the antenna broken or
  disconnected (NASA CR-4330, 1990). The design's sheared antenna and "weak beacon" are the
  commonest real story.
- **It is fixable in the ways the design already imagines.** A conductor about 62 cm long (a quarter
  wave at 121.5 MHz; about 18 cm at 406) joined to the socket's centre pin, upright and high, restores
  much of what the sheared whip lost; warming the battery gives some of its cold-lost capacity back;
  switching it off saves hours for when the planes are flying; and it must be switched off for the
  party's own radio call on 121.5 to be heard (§3.6).

### 3.8 The walk-out (travel/shelter)

*(Superseded 2026-09-17 — Andrew: the walk-out is not an ending and the cabin is supplies. Walking
to the homestead is travel priced as below; what it buys is Holt's stove, cache and water hole, and a
party at the cabin is findable for the late pass (§3.5a). Open question 4 is answered. Kept as the
record.)*

Rooms: creek run → trapline → homestead (`rescue-graph.md`, `report.md` §2). Priced by navigation
knowledge (blaze marks) and daylight, and by the P4 travel durations once those exist. `report.md`
frames reaching the homestead and lighting its stove as itself raising rescue confidence — "'we can
outlast this' is rescue confidence too" — rather than as an escape from the rescue system. Whether it
should instead (or also) be its own separate ending is open question 4; this document does not resolve
it, only surfaces the tension between the two framings that already exist in the sources.

### 3.9 The pilot

Scripted, dies within the first day (Andrew, 2026-09-16); nobody can talk to him — no language model
behind him, scripted things only: moaning softly, heard only in the cockpit, maybe a line. The earlier
(June) design held every fact he carries reachable by ≥3 other paths — the ridge bearing by chart,
blaze, and the wreck's scar; 121.5 by the manual, the ELT placard, and the radio's dial detent. What his
lines carry, and whether tending him has a real opportunity cost, is designed and reviewed in
[`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md) — linked here, not repeated. Death within the
first day produces a body: a food path (§3.2) and a moral question (doc 15).

*(Superseded 2026-09-17: **the pilot starts the run dead** — a body from the first minute, with no
lines, so he carries no fact at all. Every fact the June design gave him keeps its paths in the world
(Claude, 2026-09-26): **the ridge bearing** — the chart, the blazes, the wreck's scar, and the knob's
view; **121.5** — the survival manual, the ELT placard, the radio's dial detent, and the handbook's
ELT page; **where the search is looking** — the flight plan copy and the kneeboard (the filed route),
the broken voices on the radio when a plane is near (§3.6), and the passes themselves, heard far off
in the wrong place; **the cabin** — the chart ("V. HOLT"), the blazes, and the knob's view of the
homestead's clearing. His body is a food path (§3.2), a moral question (document 15) and a smell the
bear and the ravens follow (document 13 §4.3; document 12 §4.3a).)*

### 3.10 Keep the party alive

The injured co-player: carry, bind, warm them (`rescue-graph.md` §1). This overlaps entirely with the
INJURY paths in §3.2 and the warmth paths in §3.2 — it is not a sixth independent system, just the same
survival paths applied to a teammate instead of yourself.

### 3.11 What the graph still asks of the world

`rescue-graph.md` §4, kept as a design note (also cross-referenced in §7, "what exists today"):

- **Missing objects:** the survival mirror (cockpit, under the seat), the tire (the smoke column), the
  aircraft battery (~~outside_nose, in the cowling~~ *the tail wreckage under the snow — Andrew,
  2026-09-17*), the wing drains (fuel), a rock (spark). *(Added by Claude, 2026-09-26: the aircraft's
  handbook with its ELT page; the flight plan copy and the pilot's kneeboard; the aircraft logbook;
  the altimeter, readable as a barometer; the second statutory signalling device (AS 02.35.110) —
  document 16 authors them.)*
- **Missing verbs:** press (wound), cover/block (an opening), signal (with a reflector), set (a snare),
  fill/pour-into (vessels), carry (a person), butcher. *(Added by Claude, 2026-09-26: tramping or
  stamping snow, and laying things out, into a ground-to-air shape — whether the shape (a V, an X, an
  arrow) is named through the grammar's `INTO` slot, as a form is, is document 04's to settle;
  switching a device off and on; wave.)*
- **Missing systems:** the fire process, warmth/hunger/injury numbers, drying; the rescue-confidence
  arithmetic itself, the ELT/radio state machines, the pilot's clock. *(Claude, 2026-09-26: the
  confidence arithmetic becomes §3.5a's search and detection model; the radio is a continuous signal
  (§3.6); the pilot has no clock — he starts dead; and rescue now reads the weather state of document
  13 §4.7 — cloud, visibility, wind, light.)*
- **The solvability oracle (DR-18):** every goal's ≥3 chains pass from the start state; no chain's
  consumption makes another goal's last chain unreachable (the global softlock check) — a fuzz over the
  graph, not just the movement grid.

### 3.12 The lens pass

`rescue-graph.md` §5 (the Book of Lenses, as it stands — not re-graded here):

- **Economy — GREEN.** Six currencies, every path priced in a different key account, the common economy
  (wood, daylight) shared: spend here, can't spend there.
- **Meaningful Choices — GREEN, conditional.** Route choice is real only once durations (P4) and the
  weather window (P7) price travel against staying; until then the graph is a promise the probes hold
  open.
- **Triangularity — GREEN.** The flare; the battery walk; the pilot's body; eating snow; the thin-ice
  shortcut.
- **Problem Solving — GREEN.** Every goal ≥3 paths; every fact ≥3 clues; the counts are what
  `make probes` reports once a probe chain for the rescue graph exists (§7 — it does not yet).

### The `make a signal` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | a signal |
|---|---|
| `goal` | a signal · smoke · to be seen |
| `vague` | "How are you going to signal?" |
| `roles` | **fire** (lit) · **smoke-maker**: rubber, oil, green boughs · or **reflector**: the mirror, the landing-light reflector, in sun |
| `realize` | `put <smoke-maker> on <fire>` · `signal with <reflector>` — and whether anyone sees it is the flyover clock's answer, not the command's |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

*(Added by Claude, 2026-09-26, from the real signals of §3.5a — more means for the same goal, for
Andrew's check:)* **roles** also **marker** — anything that contrasts with the ground, laid or tramped
large: boughs, dark cloth, luggage, wreckage on snow, or trenches stamped into fresh snow · **pyrotechnic**
— the signalling devices in the kit (a flare, a smoke) · **sound on 121.5** — the radio, and the ELT if
§5 Q7 keeps it a signal. **realize** also `put <marker> on <snow>`, `light <flare>`, `tramp <snow>`.
Which smoke-maker suits depends on the background, which the world already knows: rubber and oil make
dark smoke that shows against snow; green boughs make white smoke that shows against dark spruce.

## 4. Interactions

**Depends on:**
- Doc 06 (time, sleep and the clock) and doc 13 (events, escalation and weather) — the weather window
  the confidence threshold is gated by, and the 20× consensus clock the watch rule runs it against.
  *(Claude, 2026-09-26: now the weather state of 13 §4.7 — cloud ceiling, visibility, wind, light —
  that decides whether search aircraft fly and whether a signal can be seen, and 13 §4.2's search row;
  the clock is 15 game-minutes per real minute with `propose fast forward` to 180×, decided
  2026-09-17.)*
- Doc 07 (fire and shaping) — ignition for stay-and-signal and for warmth's fire path.
- Doc 08 (warmth, clothing and shelter) — the no-materials warmth floor that keeps a fire-less night
  survivable, feeding the "stay alive" side of this system. *(Superseded 2026-09-18: the night-one
  rule, 08 §4.1a.)*
- Docs 09–11 (water, food, injury) — the WATER/FOOD/INJURY tables in §3.2 are this document's copy of
  those systems' rescue-relevant paths, not a separate design.
- Doc 12 (the pilot and bodies) — the pilot's scripted lines/clues and the tending opportunity cost,
  linked in §3.9, not repeated. *(Superseded 2026-09-17: he starts the run dead — no lines, no
  tending; his facts reach the party by other paths, §3.9.)*
- Doc 15 (the moral and social layer) — prices the pilot's body as food (§3.2, §3.9).
- Doc 16 (players and kit) — the luggage contents that supply antenna material, wire, and tools.
- Doc 17 (rooms and living rooms) — the room censuses this graph's itineraries are built from.
- Doc 18 (materials and forms) — the `conductivity` ordinal the antenna-quality rule needs (§3.6, §7).
- Doc 01 (premise and world) — the valley regions each route anchors to (§3.3). *(And the pilot's
  filed route and where he left it — the search's first, wrong place — Claude, 2026-09-26.)*
- DR-13/DR-14 (perception/zones, clock/scheduler) and DR-18 (the solvability fuzz) — the machinery the
  monotonic/always-reachable invariants and the global-softlock check (§3.11) run on.

**Depended on by:**
- Doc 21 (endings and recap) — "rescued" as an ending is exactly this system's confidence threshold
  being crossed; "walked out" may or may not be the same event (open question 4). *(Answered
  2026-09-17: rescued or dead only; "rescued" is a pass seeing or hearing the party, or the late pass
  finding it — §3.5a.)*
- Doc 20 (the agent player and research) — an agent must reach these goals from the same clues a human
  gets, with no menu and no hint that names a step (the "never a menu" rule applies to every clue path
  in §3.4 and §3.6 as much as to any other verb).
- Doc 03 (the player view) — how a rising or falling confidence, a radio-state change, or a beacon
  ladder step gets narrated (never as a raw number, never as a list of what is reachable). *(Claude,
  2026-09-26: now engines heard and their bearing, a plane rocking its wings, the radio's screech,
  hum and voice — all prose, by band.)*

## 5. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9), for Andrew's check:** Q3, Q4 and Q6 are answered by
his 2026-09-17 decisions and by real radio physics; Q1, Q2 and Q5 were wrong-headed (a channel count
written before his three ways, an arithmetic no real search uses, a scarcity worry about wire) and
are rewritten and answered from how real small-aircraft search and rescue works; **Q7 is Andrew's,
sharpened** — what hearing the ELT does. His 2026-09-17 answers stand throughout. The originals are
kept, struck, as the record.

~~1. **Is the five-channel model right?** `rescue-graph.md` (2026-09-07) treats stay-and-signal, beacon,
   radio, visual, and travel/shelter as five separately-accounted channels. `report.md` §2 (2026-07-15,
   three weeks earlier) lists only four routes and does not carry "visual" as its own account.
   *Options:* (a) keep five — the flare and the mirror spend a genuinely distinct resource (a one-shot
   item, or daylight/sun) that neither fire logistics nor navigation touch, so folding it into
   stay-and-signal would blur the distinctness check; (b) fold visual back into stay-and-signal per the
   older four-route table. *Recommendation:* keep five, and update `report.md`'s table to match — it is
   the older pass and is now out of step with the doc that superseded it.~~ *(Rewritten 2026-09-26:
   the channels were an accounting of the September confidence model, and Andrew replaced the model
   with three ways on 2026-09-17.)* **Claude's answer (2026-09-26), for Andrew's check:** the structure
   is Andrew's three ways — **the radio** during a flyover, **a signal** a search plane can see (or,
   per Q7, hear), and **surviving long enough** for the late pass. The old channels fold in without
   losing a thing a survivor could do: stay-and-signal and visual are means of *a signal* — smoke,
   fire, three fires, a mirror, a flare, a ground pattern, a bright coat, and whatever else the world
   allows (never a closed list); the beacon's place is Q7; travel/shelter stops being a rescue way,
   and the cabin's stove, cache and water hole are supplies, a party there findable for the late
   pass. What made "visual" distinct — the flare's one shot, the mirror's need of sun — survives as
   what those means cost, not as separate accounts. `report.md` is the investigation record and is
   not updated.
~~2. **The confidence threshold and weather-window arithmetic.** `confidence = Σ weight·value` capped at
   1, gated by a weather window, is the model everywhere it appears, but no source sets the actual
   weights, the threshold, or ties the "≥4 winning combinations" number to anything Andrew said (it
   appears first in `GDD.md`, not in `design.md`, which only lists nine *example* combinations).
   *Options:* (a) leave the model as additive-linear and set the numbers empirically once P5's
   solvability fuzz exists to test them against; (b) reconsider the model itself if additive-linear
   proves too easy to game (stack several weak signals to clear the threshold with no single strong
   one). *Recommendation:* (a) — the model is cheap to reason about and matches Andrew's "several ways,"
   "layered efforts" framing; treat every number attached to it as a tunable placeholder, not a
   decision, until the fuzz harness can check it.~~ *(Rewritten 2026-09-26: a sum of weights against a
   threshold is a shortcut no real search resembles — the writing rule is state systems, not
   shortcuts.)* **Claude's answer (2026-09-26), for Andrew's check:** replace the arithmetic with how a
   real search finds a party (§3.5a). **Where the search flies** is state the searchers hold: it
   starts from the pilot's filed flight plan (overdue half an hour after his ETA, the alert notice
   within about two hours, Alaska's Rescue Coordination Center launching — AIM 6-2-6), flies the filed
   route first — the wrong place, because he left it — then widens by probability; every clue that
   reaches them (the ELT heard on 121.5, a radio fragment, reported smoke, a landmark named) moves the
   later passes toward the valley; weather grounds the low search while the storm lasts. **Whether a
   pass finds the party** is computed at that moment from what is physically up (smoke — only on calm,
   clear days; fire at night; a mirror in sun; a flare; a ground pattern at least 6 m long; the wreck,
   which snow buries — FM 3-05.70), the pass's track and height, and the light and visibility — real
   odds without a signal are poor, about 15 % for one pass over hilly forest (CAP *Mission Aircrew
   Reference Text*). A crew that sees them rocks its wings (the AIM's acknowledgement); help comes when
   the weather lets it in, and they must survive the wait (Andrew). Players never see a number; the
   log carries them all. "Always reachable" becomes the late pass reaching any findable party, and
   "monotonic" becomes what the searchers know never shrinks. The weights, the threshold and "≥4
   winning combinations" retire; DR-16 in the architecture register wants the same change.
~~3. **The radio state machine.** The six states in §3.6 are detailed enough to build against, and the
   antenna-quality-from-material rule is exactly the kind of "several ways" mechanism Andrew asked for.
   Two things need a call before P5 authors `authored.py`: the naming drift between `design.md`'s
   `two_way_contact_no_location` and the architecture doc/roadmap's `two_way_no_location`; and whether
   the ladder is really six discrete states or a continuous quality score like the beacon's (§3.7 uses
   numeric values 0–85, the radio uses named states — an inconsistency between two systems built by the
   same June pass). *Recommendation:* keep the six named states (the radio's feedback text in §3.6 is
   written to name a state, not a number) but pick one spelling for state 5.~~ **Claude's answer
   (2026-09-26), for Andrew's check:** answered by Andrew on 2026-09-17 — signal quality is
   **continuous** (the battery's charge, the antenna up or down and how high, the plane's nearness),
   mapped to prose: a screech with the antenna down, a hum with it up, a faint voice as the dial turns,
   clearer as it improves. So there is no six-state machine and the spelling question dissolves; the
   six names are at most landmarks for whoever writes the prose bands. What the quality is made of is
   real radio physics (§3.6): line of sight between the antenna and the aircraft (the radio horizon,
   the valley walls), an antenna near a quarter wave long (about 62 cm at 121.5 MHz), upright,
   connected and clear, the battery's charge falling with use and cold, and the ELT switched off so
   its tone does not swamp the call — the procedure in the aircraft's own handbook.
~~4. **Does the walk-out to Holt's homestead count as rescue?** `report.md` §2 frames arriving and
   lighting the stove as raising rescue confidence ("'we can outlast this' is rescue confidence too").
   The design-doc index's own description of doc 21 lists endings as "rescued / walked out / dead /
   still going" — four distinct outcomes, which reads as "walked out" being separate from "rescued."
   *Options:* (a) travel/shelter is purely a confidence channel like the other four — walking to the
   homestead only ever helps you get found, it is never itself the win; (b) reaching the homestead and
   surviving there under your own power is its own ending, distinct from "rescued," matching doc 21's
   four-way split. *Recommendation:* (b), explicitly — but this document cannot decide it alone; doc 21
   needs to agree with whatever this settles on, or the two documents will describe different games.~~
   **Answered by Andrew, 2026-09-17:** no — the only endings are rescued or dead, the walk-out is
   closed and the cabin is supplies. *(Claude, 2026-09-26:)* a party at the cabin is findable, so
   the late pass can reach it there; its stove, cache and water hole are what the walk buys (§3.8).
~~5. **The shared-conductor overlap (beacon/radio).** Andrew's 2026-09-16 note asked for this to be
   reviewed here rather than as a separate question. `rescue-graph.md`'s distinctness check calls the
   wire "the ONE deliberate overlap the GDD flags," mitigated by the dooryard cable as a second
   conductor. *Recommendation:* accept it as a deliberate, priced overlap (not a flaw) — but at
   authoring time, verify the dooryard cable is a genuinely separate physical object from the
   tail-section/cockpit wire pair, not secretly the same item under two names, or the mitigation is
   fictional.~~ *(Rewritten 2026-09-26: treating one wire as a flaw to mitigate is scarcity reasoning —
   the world is not short of conductors.)* **Claude's answer (2026-09-26), for Andrew's check:** there
   is nothing to mitigate. Whether a thing can be an antenna is physics — `conductivity` from its
   material, then its length against the quarter wave, its posture, its connection and its height
   (§3.6) — so every conductor in the valley qualifies: the avionics wire, the guitar's strings,
   seat-frame tubing, a strip of skin, the ELT's own stub, Holt's dooryard cable 2.5 km away, and
   whatever the loops find. When the party has one good wire and two antennas to make, choosing is a
   real decision, not a design fault — and the two are coupled anyway, since both speak on 121.5 and
   the beacon must be switched off for the radio to be heard. The authoring requirement is the
   ordinary one: every conductor is its own entity with its own name (document 04 §3.10).
~~6. **Which goals get which minimum number of paths?** §3.2's four survival goals each get "≥3 paths" in
   `rescue-graph.md`; `roadmap.md`'s P5 exit gate instead states per-goal numbers that are not uniformly
   3: ≥3 warmth strategies specifically, ≥4 distinct rescue combinations, ≥3 radio solution paths, ≥3
   pilot clue paths per fact. *Options:* (a) treat the roadmap's per-goal numbers as authoritative since
   they are the closer-to-build-time source; (b) normalize everything to a single ≥3 floor and treat
   "≥4" for rescue as the one deliberate exception (it is the win condition, so it gets one more).
   *Recommendation:* (a) — keep the roadmap's numbers as given; they already read as deliberate, not
   copy drift, and every count here is a floor regardless of which is chosen.~~ **Claude's answer
   (2026-09-26), for Andrew's check:** every count is a floor, never a target, and the floor is the
   same everywhere — at least three paths per goal, each spending something different (Andrew,
   2026-09-07: "several ways of doing things"). Rescue has Andrew's three ways, and each has several
   means (the radio: the battery found by searching the ground or sorting the tail, any conductor as
   the antenna, several ways to get it high; a signal: every means in §3.5a). "≥4 winning
   combinations" retires with the additive model (Q2); "≥3 pilot clue paths per fact" becomes ≥3 paths
   per fact *in the world*, since he starts the run dead — §3.9 lists them. `roadmap.md` is the June
   history (`PLAN.md`'s header), not a source of numbers.
~~7. asked:~~ **Answered 2026-09-27 (Andrew):** *"no working ELT meter otherwise this wouldnt even be a game"* *The question as it was asked:* **The ELT: what does hearing it do for the party?** Andrew is deciding the beacon's place among his
   three ways — not whether it exists: US rules put an ELT in nearly every small airplane (14 CFR
   91.207), and it stays a real, working device the party can switch, warm, rig and raise (§3.7). The
   facts that decide it: the design's ELT is the older 121.5 MHz kind (what a 1970s 206 left the
   factory with, and still legal); since 2009 no satellite listens to 121.5, so only an
   aircraft within line of sight that is listening can hear it; its 48-hour battery runs down faster in
   the cold; its antenna — the part crashes break most — is sheared; and its tone swamps the party's
   own radio call until someone switches it off. *Options:* (a) **a signal, heard rather than seen** —
   part of the second way: a pass within line of sight hears the tone, which moves the search onto the
   valley and lets the crew home in; a ~62 cm conductor stood upright and carried high widens that
   reach; the battery is a clock the party spends or saves by switching it off until the planes fly;
   (b) **the modern 406 MHz kind** — satellites hear it within minutes once its antenna works, so a
   rigged ELT calls the rescue by itself, whatever the flyover schedule says: true to a newer aircraft,
   but a fourth way home that bypasses the rescue clock and outranks the radio and every other signal;
   (c) **parts and interference only** — it works and can be heard, but hearing it brings no pass; its
   rescue value runs through the radio (its whip and socket, its battery, and the switch that silences
   it). *Recommendation:* (a) — it is what this airplane most plausibly carries, it keeps Andrew's three ways
   and the flyover schedule as the clock, and it adds real decisions (rig it, raise it, save its
   battery, switch it off to talk) without a new way home. This is the "second silent path" of the
   2026-09-17 note, made exact.

## 6. Review log



- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** endings rescued or dead; the walk-out
  closed; surviving long enough is the hardest rescue path; the flyover schedule as the rescue clock; the
  radio as the ~~mini game~~ interaction above; the battery in the tail under the snow; searching the ground as an
  activity. Open: the ELT — keep as a second silent path (Claude's recommendation) or fold in.

- **2026-09-18:** the `make a signal` goal rows added (document 04 §3.9 owns the form and the dispatch rule).

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-reviewed against block 1 (03–09), Andrew's
  2026-09-17 answers (which stand), the decisions since (October, the pilot dead from the start) and
  real small-aircraft search and rescue, with sources. **Added §3.5a** — how a real search finds a
  party: the filed flight plan and the overdue sequence, the route search in the wrong place, clues
  that move the passes, weather that grounds them, and per-pass detection from what is physically up
  (smoke, fire, mirror, flare, the ground-to-air code, the wreck, 121.5), with the wing-rock as the
  sign of being seen; the additive confidence (§3.5) is kept as the record, superseded. **Added to
  §3.6** the radio's real physics (line of sight, the quarter-wave antenna) and the aircraft
  handbook's own procedure (save the battery until a plane is in sight; switch the ELT off to talk),
  and flagged once that a real 206 keeps its battery on the firewall — Andrew's tail battery kept, made
  true by a battery moved aft. **Added to §3.7** the real ELT (121.5 vs 406, satellites since 2009,
  crash failures, the battery clock). The title, the one-paragraph summary, the pilot (starts dead —
  his clue paths replaced by paths in the world, §3.4 and §3.9), the clock, the warmth floor, the
  battery's place, daylight and the lake's ice (October) corrected and marked; a slur in §3.3
  renamed. **Answered** Q3, Q4, Q6; **rewrote and answered** Q1 (three ways, not five channels), Q2
  (the search model replaces the arithmetic), Q5 (no conductor scarcity); **left for Andrew:** Q7, the
  ELT's place among the three ways, sharpened with the real device's facts.

- **2026-09-27 (Andrew):** Q7 — no working ELT. The battery is in the nose, wired up and fine; the radio has a loose wire inside that a character with technical proficiency sees on inspecting it. *"this whole rescue scenario will need thought please dont just blindly agree … I want help designing this, i just dont want you to add things without explicitely asking me."* Rescue is reopened as a design conversation with Andrew (`PLAN.md` A13); Claude's additions here are not accepted design.

- **2026-09-27 (Andrew, the rescue conversation, first round):** the radio — *"you need to find something to open the radio, you need to fix the antenna, you need to adjust the antenna, never said you had to wait for a flyover you just have to try different channels"*; and *"What would you add to make it harder? a disconnected battery? what?"* A party without a technical character: *"it would just be slower just like making fire. it would hint at this 'you are not technically proficient so this might take awhile' when inspecting the inside."* Why planes come: *"they are searching for it, search and rescue you know."* Claude showed the 2026-09-17 words (*"the hand radio is also usable only during flyover events otherwise it is static"*) — which of the two stands is open in the conversation.

- **2026-09-27 (Andrew, the rescue conversation, second round):** *"would a battery really stop working in a week of cold? it could drain down with indicators 'the light starts to dim, perhaps the radio is draining'. b) absolutely not making the user find the right length wire, putting it higher is ok c) we have a dial and a set of buttons for different channels only one of which is the emergency one they can try all the channels or find the written down frequency d) no, as for the fork you suggested a hand radio in the cabin but it needs batteries buried in a container like luggage or bag in the tail section."* Written into the §3 banner.

- **2026-09-27 (Andrew, the rescue conversation, third round):** *"1. no 2. not just during a flyover, once you fix the antenna it is relatively quick"* — the cold does not weaken the radio's batteries; contact does not wait for a flyover, and comes relatively quickly once the antenna is fixed (supersedes 2026-09-17's "usable only during flyover events").

- **2026-09-27 (Andrew, the rescue conversation, fourth round):** *"a. sure, they can say once the storm dies down on the radio, i want the radio person controlled by a weak llm as the user might want to talk to them, i think the user might want to press the button while talking into the mic but if they dont it will hint. a lot of things might need hints i dont want users figuring out common sense things b. you choose, i thought we already decided but i dont care"* — no earlier decision on location was found in the record; Claude's choice is in the §3 banner, for his check.

- **2026-09-27 (Andrew, the rescue conversation, fifth round):** no "mini game" — the radio is interacting with the world, and a bad signal letting through only some words is part of the world; the voice is scaffolded to help only as a real rescuer would, asks for landmarks, and judges whether what it is told is good enough (§3 banner). The "mini game" wording is struck here, in the GDD, the design index and `PLAN.md`.

- **2026-09-27 (Andrew, the rescue conversation, sixth round):** the model's judgement stays — *"i changed my mind. i need one because they are talking to someone"*; the voice may hint (raise the antenna), heard through the bad signal; the same model every run, scaffolded with rules; it judges by criteria the game gives it — the landmarks and their value. GDD §3 rule 2, `VISION.md` and `CLAUDE.md` carry the exception.

## 7. What exists today

**Designed, not built:**
- The whole graph in §3.2–§3.4 (`rescue-graph.md`) and the radio/beacon workflows in §3.6–§3.7
  (`design.md` §37–38) exist only as prose and tables. No probe chain exists for any of it: there is no
  `probes/graph.py` anywhere in the repository (checked directly — `find . -iname "graph.py"` returns
  nothing), even though `rescue-graph.md`'s own header promises one and
  `game/world/scenarios/whiteout/probes/__init__.py`'s docstring lists "the rescue graph" among the
  corpus's sources. The actual `PROBES` union in that file only imports `census`, `chain`, `phrasing`,
  and `kit` — the rescue graph is not wired into the probe corpus at all.
- The wider valley terrain each route (other than stay-and-signal) anchors to — the lake/ice_flat, the
  ridge/the_knob, the creek–trapline–homestead line — is entirely `map.md`/`report.md` design. None of
  it exists in `game/world/scenarios/whiteout/zones.py`, which currently holds only the nine crash-
  cluster zones (cockpit, mid_cabin, rear_cabin, outside_nose, fuselage_top, outside_tail, debris_trail,
  tail_section, treeline). Building the fifty outdoor zones is separately tracked (see the memory note
  on the outdoor room build) and is a precondition for the visual and travel/shelter channels having
  anywhere to run.
- The rescue-confidence arithmetic itself: `game/world/sim/systems/rescue.py` contains exactly one
  function, `confidence(channels)`, and its body is `raise NotImplementedError("systems.rescue.
  confidence — roadmap P5")`. Nothing computes a confidence value anywhere in the running game.
- `game/world/scenarios/whiteout/rescue.def` is a seven-line comment block — a reserved placeholder
  that says the format will be finalized when the rescue system is authored in P5. It defines nothing.
- The authored-rule seam for puzzle-critical objects (the documented exception for the radio/beacon/
  pilot) is real and live: `game/world/scenarios/whiteout/authored.py` defines the `AUTHORED` dict the
  resolver already consults before generic handlers. But the dict itself is `{}` — empty. This is a
  built seam with no rescue content behind it yet, exactly as its own docstring says: "Empty until the
  rescue-graph design pass is promoted; the seam is live so content can land without plumbing."
- The weather system (`game/world/sim/systems/weather.py`) that the rescue formula's `weather_window`
  term depends on is the same kind of stub — a docstring and nothing else, built in roadmap P7.

**Built:**
- The radio and the ELT/beacon exist as authored objects today, with prose: `objects.py` defines
  `sim_id: 'radio'` (a field radio, `plastic`/`copper_wire`, in the cockpit, `state: {powered: False,
  fixed: True}`) and `sim_id: 'elt'` (aliases `elt`/`transmitter`/`beacon`, in the tailcone,
  `state: {armed: True, antenna: 'sheared'}` — matching `design.md`'s broken-antenna clue exactly).
  `appearance.py` gives both a description (the radio dark in its cradle beside the pilot; the sheared
  antenna base on the fuselage top). A generic `wire` object exists, and the guitar's strings yield
  `loose_wire` when removed — a real, if incidental, second antenna-material source matching
  `design.md` §38.3's "wire from electronics." The material table already carries a `conductivity`
  ordinal (`none`/`high`/`extreme`) on metals and `copper_wire`, which is the real hook the
  antenna-quality rule (§3.6) would compute from — a foothold, not a placeholder.
- `rescue-graph.md`'s "missing objects" list (§3.11) is still accurate as of this reading: no survival
  mirror, no tire, no aircraft battery, no wing drains, and no dedicated spark-rock exist in
  `objects.py` (checked directly).
- The probe corpus has a small number of "todo"-status entries that touch this system without
  resolving anything: `probes/census.py` records that the cockpit panel should open, the radio should
  be takeable and listenable-to, and wire should tie to the fuselage-top cable/ELT — all marked `todo`,
  meaning recorded as needed, not yet passing. `probes/phrasing.py` has a larger set of probes asking
  whether sentences like "turn on the radio" or "fix the radio using the screwdriver" *parse* — some
  pass, some are `todo` — but these test the parser only, not whether the radio resolves or advances its
  state.

**Nothing:** any tracked rescue-confidence value on a running instance; any radio- or beacon-state
transition logic; any weather-window gating; any probe or fuzz coverage of the graph as a whole.
