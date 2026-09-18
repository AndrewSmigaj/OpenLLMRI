# 14 — Rescue paths: the goals, ≥3 paths per goal, the five channels, rescue confidence, the radio, the ELT, the walk-out

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
new — Andrew has not reviewed it yet — it collects and cross-checks what already exists.

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

**The whole valley is in the first complete run (2026-09-16).** All fifty outdoor zones — so the
travel/shelter and visual routes' anchor terrain (the lake, the ridge, the creek–trapline–homestead
line) is in scope for the first run, not a stretch goal, even though none of it is built yet (§7 below).

**The beacon/radio wire overlap is reviewed here, not asked separately (2026-09-16).** Per the
provenance audit §4: "the beacon/radio wire overlap is a note inside the rescue-paths design, reviewed
there." Reviewed in §3.4's distinctness check and flagged as open question 5.

**The watch rule and the clock (2026-09-07, amended 2026-09-16).** One acting player holds the running
clock at 1×; others wait for the next event; the clock may run 20× by consensus when everyone sleeps or
waits, and events interrupt it. This is what a rescue "weather window" (§3.5) actually runs against —
there is no separate planning-freeze for it.

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
  `two_way_no_location`. Harmless, but the two sources should agree on one spelling.
- **`roadmap.md` P5.** Sets the build-time exit-gate numbers: survive the first night via **≥3**
  warmth strategies, rescue reachable via **≥4** distinct combinations, the radio puzzle solvable **≥3**
  ways, the pilot's death never softlocks (his facts have **≥3** clue paths each per the GDD).

## 2. In one paragraph

At the start, the radio is dead and the beacon is weak — Andrew's own framing, carried since the first
seed doc. There is no single "real" way out: the party can stay near the wreck and make itself seen
(fire, smoke, a ground sign), fix the beacon and get its antenna clear, fix the radio and get useful
words through static, signal visually with a mirror or the plane's one flare, or walk out toward Holt's
homestead. Each of these draws on a different scarce thing — fuel, elevation, battery power and a
clear weather window, a flare or daylight, or the willingness to spend days walking — so no single
resource running out (cold, especially) can kill every route at once. None of it works instantly:
progress is layered and partial, reported by feedback that never says "you have solved it," and a
weak signal repeated stubbornly can still eventually matter. Meanwhile the same "several ways" rule
applies inside the survival goals that keep the party alive long enough to be found — warmth, water,
food, injury all have more than one path, and the paths cost different things so a party that is good
at one is not automatically good at all of them.

## 3. The design


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
> bands: a medium-difficulty mini game of piecing the message together, then the rescue ending if
> they survive the time it takes. One person can work the radio while another gets food. **Open for
> this document's sitting:** whether the ELT (the silent beacon you rig an antenna onto) stays as a
> second path or folds into the radio. The graph below is the September draft.

### 3.1 The goals

What "win" and "not lose" decompose into (`rescue-graph.md` §1):

- **Stay alive** — warmth, water, food, injury; each is its own goal with its own ≥3 paths (§3.2).
- **Be found** — rescue confidence, the sum of five channels, must clear a threshold inside a weather
  window; ≥4 winning combinations; no single object is required by every channel (`GDD.md` §37–39).
- **Keep the party alive** — the injured co-player: carry, bind, warm them. *(The pilot dies within the
  first day and cannot be talked to — Andrew, 2026-09-16; his body is a food path and a moral question,
  reviewed in [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md).)*

### 3.2 Stay alive — ≥3 paths per goal, each spending a different resource

From `rescue-graph.md` §3, the crash-cluster graph (v1). Every path also spends the common survival
economy (wood, food, daylight); what makes route choice real is the **key** resource column, which must
differ between a goal's siblings.

**WARMTH** (the antagonist is cold; the GDD's warmth floor guarantees a fire-less night is survivable):

| path | key resource | rooms | probe chain (seed) |
|---|---|---|---|
| fire (7 methods — doc 07, fire-and-shaping) | fuel + an ignition source | treeline / north wood (fuel); the source's room | lighter path; bow-drill path; battery path |
| insulation salvage | tools (to strip) + time | mid/rear cabin (foam, batting, blanket, engine cover, clothes) | `wear blanket` · `cut cushion` → stuff jacket · `wear engine cover` |
| shelter / windbreak | sweat + tools | rear cabin (block the breach with the sheet), outside (snow wall, boughs) | `cover breach with sheet` · `put boughs on floor` |
| huddle + fuselage + body heat (the floor) | nothing but proximity | any enclosed zone | `huddle with agent-2` (P6) |

Softlock guard: the floor path needs no object; the fire paths need ≥2 different ignition sources
present at start (the lighter and the flare and the battery and the friction kit are all in the crash
cluster).

**WATER:**

| path | key resource | rooms | chain |
|---|---|---|---|
| the canteen / thermos as found | knowledge (search) | cockpit, rear cabin | `search backpack` → `drink from canteen` |
| melt snow/ice by fire in a vessel | fuel + a vessel | anywhere + fire | `put snow in thermos` → `put thermos by fire` → `drink` |
| melt by body heat (slow, costs warmth) | warmth | any | `put snow in canteen` → wear it under the jacket (time) |
| the lake lead / the seep (valley) | risk + daylight | inlet_mouth, shore | `fill canteen from lead` |

Eating snow is always possible and always costs heat (the manual's lesson; a redirect with a
consequence, never a refusal).

**FOOD:**

| path | key resource | rooms | chain |
|---|---|---|---|
| the kit (rations ×2, chocolate, flour, coffee tin) | search | seat pocket, survival duffel, crate | `open tin` → `eat rations` |
| the country (grubs, cranberries, hare snare, fish) | knowledge + tools + daylight | tamarack, tussocks, willows, the lead | `set snare with paracord at willows` (P5) |
| the pilot's body | the moral price (doc 15, moral and social layer) | cockpit | `butcher pilot with knife` |
| Holt's cache | travel | homestead | the travel route's reward |

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
| **Daylight** | travel and work both burn the ~5 h light budget; the storm shortens it further |
| **Warmth** | every zone has an exposure band; open ice and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt |
| **Tools** | blade, chopper, saw, container, cordage — each unlocks a different shelf of the world |
| **Knowledge** | reading sign: tracks, ice colour, blaze marks, squaw wood; `examine` is the tutor |
| **Risk** | thin ice, overflow, the cornice, the climb — always telegraphed, never random |

`map.md`'s own thesis: **each region anchors one rescue route** — the lake anchors the visual route
(open sightlines), the ridge anchors radio/beacon (elevation), the creek–trapline–cabin line anchors
travel/shelter (distance and navigation), and the crash site anchors stay-and-signal (the known point
searchers will eventually grid). The forest ring in between is the survival economy every route spends
from.

### 3.4 Be found — the five channels

From `rescue-graph.md` §3: each channel is a separate confidence account; ≥4 combinations should reach
the threshold.

| channel | key resource | rooms | clue paths (≥3 each) | chain |
|---|---|---|---|---|
| stay-and-signal (fire on the ice; the tire's black smoke; a ground sign) | fuel logistics + wind engineering | ice_flat, gear_gouge, crash site | the manual's SIGNALS page · the chart's search grid note · the reflector's glint (examine) | `put oil quart on fire` (smoke) · `put boughs on ice` (SOS) |
| beacon (ELT) | conductor + elevation | tail_section (ELT), cockpit panel (wire) or dooryard cable, fuselage_top / the_knob | the manual's 121.5 page · examine the ELT ("antenna sheared") · the sheared base on fuselage_top | `take elt` → `tie wire to elt` → `go to fuselage top` → `tie wire to antenna base` |
| radio | carry logistics + weather windows (the battery is 12 kg in the nose cowling) | cockpit, outside_nose (battery), the_knob | static-but-powered implies antenna · the pilot's fragment · the chart's ridge bearing | `pry cowling` → `take battery` → `tie wire to radio` → `talk to radio` (the FSM: §3.5) |
| visual (mirror, reflector, flare) | the flare's one shot / sun for the mirror | crash site, ice_flat, fuselage_top | the reflector's glint · the manual · the survival mirror (census: under the seat) | `light flare` (spends the fire source) · `examine reflector` → `signal with reflector` |
| travel/shelter (the cabin) | navigation + daylight | creek → trapline → homestead | the chart (V. HOLT) · blaze marks (knowledge) · the pilot's "ridge" | the walk, priced by the P4 durations |

**Distinctness check** *(a design note for this document's review, not a decision already asked of
Andrew)*: wire — beacon and radio share the conductor, "the ONE deliberate overlap the GDD flags"; the
dooryard cable is a second conductor so it is not a single point of failure — elevation, fuel/wind, the
flare, and navigation are otherwise separate accounts. No object is required by every channel; the
flare is fire OR signal (a genuine risk/reward triangle). Reviewed further as open question 5.

`report.md` §2 restates this as room itineraries and gives the same routes a slightly different shape
— see open question 1.

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

`implementation-architecture.md` §8 (DR-16):

- **Additive confidence:** `RescueState{channels:{beacon,radio,landmark,visual,smoke,stay}: 0..1}`;
  `confidence = Σ weight·value` capped at 1; `rescued = weather_window AND confidence ≥ threshold`.
- **Distinct resources:** each channel's authored requirements draw on different scarce inputs (not
  all warmth/fire) so route choice is real and global softlock is avoidable.
- Enforced invariants (`GDD.md` §44/45): rescue confidence is **monotonic** (an action never lowers it
  behind your back) and **always reachable** from every sampled state (the solvability oracle,
  `roadmap.md` P5 exit gate; `rescue-graph.md` §4).

The exact weights, the threshold, and the ≥4-combinations count are not locked by Andrew anywhere this
document found — see open question 2.

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

**Radio feedback** must name signal quality explicitly so players can reason about the antenna
(`design.md` §38.4): `"... unidentified aircraft ... signal weak ... repeat ..."`,
`"... hearing you faintly ... improve your antenna if you can ..."`,
`"... we have partial transmission ... need location ... landmarks ..."`. With power but no usable
antenna, results are mostly static, with occasional broken fragments getting through — persistence is
never hard-blocked forever, but antenna repair stays the better path (§38.5).

**The six-state ladder** (`design.md` §38.6; renamed slightly by the architecture doc and `roadmap.md`
— see the naming-drift note in §1):

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

**Location information** (`design.md` §38.8) can come from: the pilot's fragment before he dies, the
cockpit nav log, a torn map mark, a visible red ridge before whiteout, river direction, landmark
alignment, a weather-relay sign, a description of the basin/wreck orientation/ridge shape, the beacon
signal combined with partial radio contact, or a visual signal spotted during a weather break. The
radio supports imperfect communication — fragments, not coordinates; the rescue system aggregates
confidence from them.

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

### 3.8 The walk-out (travel/shelter)

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

### 3.10 Keep the party alive

The injured co-player: carry, bind, warm them (`rescue-graph.md` §1). This overlaps entirely with the
INJURY paths in §3.2 and the warmth paths in §3.2 — it is not a sixth independent system, just the same
survival paths applied to a teammate instead of yourself.

### 3.11 What the graph still asks of the world

`rescue-graph.md` §4, kept as a design note (also cross-referenced in §7, "what exists today"):

- **Missing objects:** the survival mirror (cockpit, under the seat), the tire (the smoke column), the
  aircraft battery (outside_nose, in the cowling), the wing drains (fuel), a rock (spark).
- **Missing verbs:** press (wound), cover/block (an opening), signal (with a reflector), set (a snare),
  fill/pour-into (vessels), carry (a person), butcher.
- **Missing systems:** the fire process, warmth/hunger/injury numbers, drying; the rescue-confidence
  arithmetic itself, the ELT/radio state machines, the pilot's clock.
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

## 4. Interactions

**Depends on:**
- Doc 06 (time, sleep and the clock) and doc 13 (events, escalation and weather) — the weather window
  the confidence threshold is gated by, and the 20× consensus clock the watch rule runs it against.
- Doc 07 (fire and shaping) — ignition for stay-and-signal and for warmth's fire path.
- Doc 08 (warmth, clothing and shelter) — the no-materials warmth floor that keeps a fire-less night
  survivable, feeding the "stay alive" side of this system.
- Docs 09–11 (water, food, injury) — the WATER/FOOD/INJURY tables in §3.2 are this document's copy of
  those systems' rescue-relevant paths, not a separate design.
- Doc 12 (the pilot and bodies) — the pilot's scripted lines/clues and the tending opportunity cost,
  linked in §3.9, not repeated.
- Doc 15 (the moral and social layer) — prices the pilot's body as food (§3.2, §3.9).
- Doc 16 (players and kit) — the luggage contents that supply antenna material, wire, and tools.
- Doc 17 (rooms and living rooms) — the room censuses this graph's itineraries are built from.
- Doc 18 (materials and forms) — the `conductivity` ordinal the antenna-quality rule needs (§3.6, §7).
- Doc 01 (premise and world) — the valley regions each route anchors to (§3.3).
- DR-13/DR-14 (perception/zones, clock/scheduler) and DR-18 (the solvability fuzz) — the machinery the
  monotonic/always-reachable invariants and the global-softlock check (§3.11) run on.

**Depended on by:**
- Doc 21 (endings and recap) — "rescued" as an ending is exactly this system's confidence threshold
  being crossed; "walked out" may or may not be the same event (open question 4).
- Doc 20 (the agent player and research) — an agent must reach these goals from the same clues a human
  gets, with no menu and no hint that names a step (the "never a menu" rule applies to every clue path
  in §3.4 and §3.6 as much as to any other verb).
- Doc 03 (the player view) — how a rising or falling confidence, a radio-state change, or a beacon
  ladder step gets narrated (never as a raw number, never as a list of what is reachable).

## 5. Open questions

1. **Is the five-channel model right?** `rescue-graph.md` (2026-09-07) treats stay-and-signal, beacon,
   radio, visual, and travel/shelter as five separately-accounted channels. `report.md` §2 (2026-07-15,
   three weeks earlier) lists only four routes and does not carry "visual" as its own account.
   *Options:* (a) keep five — the flare and the mirror spend a genuinely distinct resource (a one-shot
   item, or daylight/sun) that neither fire logistics nor navigation touch, so folding it into
   stay-and-signal would blur the distinctness check; (b) fold visual back into stay-and-signal per the
   older four-route table. *Recommendation:* keep five, and update `report.md`'s table to match — it is
   the older pass and is now out of step with the doc that superseded it.
2. **The confidence threshold and weather-window arithmetic.** `confidence = Σ weight·value` capped at
   1, gated by a weather window, is the model everywhere it appears, but no source sets the actual
   weights, the threshold, or ties the "≥4 winning combinations" number to anything Andrew said (it
   appears first in `GDD.md`, not in `design.md`, which only lists nine *example* combinations).
   *Options:* (a) leave the model as additive-linear and set the numbers empirically once P5's
   solvability fuzz exists to test them against; (b) reconsider the model itself if additive-linear
   proves too easy to game (stack several weak signals to clear the threshold with no single strong
   one). *Recommendation:* (a) — the model is cheap to reason about and matches Andrew's "several ways,"
   "layered efforts" framing; treat every number attached to it as a tunable placeholder, not a
   decision, until the fuzz harness can check it.
3. **The radio state machine.** The six states in §3.6 are detailed enough to build against, and the
   antenna-quality-from-material rule is exactly the kind of "several ways" mechanism Andrew asked for.
   Two things need a call before P5 authors `authored.py`: the naming drift between `design.md`'s
   `two_way_contact_no_location` and the architecture doc/roadmap's `two_way_no_location`; and whether
   the ladder is really six discrete states or a continuous quality score like the beacon's (§3.7 uses
   numeric values 0–85, the radio uses named states — an inconsistency between two systems built by the
   same June pass). *Recommendation:* keep the six named states (the radio's feedback text in §3.6 is
   written to name a state, not a number) but pick one spelling for state 5.
4. **Does the walk-out to Holt's homestead count as rescue?** `report.md` §2 frames arriving and
   lighting the stove as raising rescue confidence ("'we can outlast this' is rescue confidence too").
   The design-doc index's own description of doc 21 lists endings as "rescued / walked out / dead /
   still going" — four distinct outcomes, which reads as "walked out" being separate from "rescued."
   *Options:* (a) travel/shelter is purely a confidence channel like the other four — walking to the
   homestead only ever helps you get found, it is never itself the win; (b) reaching the homestead and
   surviving there under your own power is its own ending, distinct from "rescued," matching doc 21's
   four-way split. *Recommendation:* (b), explicitly — but this document cannot decide it alone; doc 21
   needs to agree with whatever this settles on, or the two documents will describe different games.
5. **The shared-conductor overlap (beacon/radio).** Andrew's 2026-09-16 note asked for this to be
   reviewed here rather than as a separate question. `rescue-graph.md`'s distinctness check calls the
   wire "the ONE deliberate overlap the GDD flags," mitigated by the dooryard cable as a second
   conductor. *Recommendation:* accept it as a deliberate, priced overlap (not a flaw) — but at
   authoring time, verify the dooryard cable is a genuinely separate physical object from the
   tail-section/cockpit wire pair, not secretly the same item under two names, or the mitigation is
   fictional.
6. **Which goals get which minimum number of paths?** §3.2's four survival goals each get "≥3 paths" in
   `rescue-graph.md`; `roadmap.md`'s P5 exit gate instead states per-goal numbers that are not uniformly
   3: ≥3 warmth strategies specifically, ≥4 distinct rescue combinations, ≥3 radio solution paths, ≥3
   pilot clue paths per fact. *Options:* (a) treat the roadmap's per-goal numbers as authoritative since
   they are the closer-to-build-time source; (b) normalize everything to a single ≥3 floor and treat
   "≥4" for rescue as the one deliberate exception (it is the win condition, so it gets one more).
   *Recommendation:* (a) — keep the roadmap's numbers as given; they already read as deliberate, not
   copy drift, and every count here is a floor regardless of which is chosen.

## 6. Review log



- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** endings rescued or dead; the walk-out
  closed; surviving long enough is the hardest rescue path; the flyover schedule as the rescue clock; the
  radio as the mini game above; the battery in the tail under the snow; searching the ground as an
  activity. Open: the ELT — keep as a second silent path (Claude's recommendation) or fold in.

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
