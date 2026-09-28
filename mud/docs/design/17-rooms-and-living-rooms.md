# 17 — Rooms and living rooms: individuation, state that persists, the prose style, the crash rooms

> **Status: draft for review.** Architecture counterparts:
> [`../architecture/containment.md`](../architecture/containment.md) (DR-24, the reveal rule that
> `search`/`open`/`look under` all obey) and
> [`../architecture/presentation.md`](../architecture/presentation.md) §4 (Voice — the prose principle
> behind the style guide in §4.4).

---

## 2. Decisions

### Andrew's decisions

- **2026-09-07 — living rooms.** No half-thought rooms: living, interesting rooms — seats with cushions
  you can look under, labelled so you can look under different rows or cut different seats; the things
  in them serve the rescue goals, with several ways of doing things. This is the brief the rest of this
  document works from.
- **2026-09-16 — every room to real-world depth.** Every room is censused to real-world depth — any and
  all entities and relations, the natural world included: the ground and what is under it, rock, clay,
  bark, every substance and every relation a person would try — and grown without a ceiling by the
  loops. "Traversal terrain" means no forced puzzle hook per room; it is never a cap on entities. A
  class that yields individuals is still a full entity.
- **2026-09-16 — the four-seat interior** (document **16 — Players and kit** §4.6).
- **2026-09-18 — naming things apart.** Every pair of confusable things in reach needs a word that
  separates them in its authored prose (§4.7a).
- **2026-09-26 — the plane is an entity.** The plane is an entity itself, with openings that are open or
  closed and an internal heat that a fire inside raises; a fire generates heat in its area and residual
  heat in other areas; body parts have heat as part of their ontology. It is part of designing the fire
  and heat system. Rooms are therefore entities in the ontology like everything in them (§4.8).
- **2026-09-26, 2026-09-27 — the season** is the first week of October in interior Alaska (document 13
  §4.2).
- **2026-09-27 — what kills.** Nothing kills instantly: death comes by the body running down, on real
  clocks, with time to respond — carbon monoxide from a fire inside among them.

### Proposals (Claude)

Everything else is a proposal for review:

- The five properties of a "living" room (§4.1), density with purpose (§4.2), the seat exemplar and its
  finds (§4.3), the nine-rule prose style guide (§4.4), and the lens pass (§4.7).
- The "ontological Turing test" method (census first, then the built room, then the gaps) — from the
  `ontology-generator` skill.
- §4.8's mechanism — rooms as entities with air, light and ground; the plane's parts and openings; one
  air volume; the physics of its internal heat — stands as a proposal for Andrew's check.

---

## 3. In one paragraph

A room here is not a description with a noun list bolted on. The seat you are sitting in is not the
same as the one behind you — this one is wrenched off its rails with someone's laptop bag still
wedged under it, that one is thrown loose and could be dragged outside as a windbreak — and looking
under one tells you nothing about the others; you have to check each. Whatever you or the person
next to you does to a room stays true the next time either of you looks: the seat you stripped for
its cushion stays stripped, the drift you dug stays dug, the fire you built is still there, still
burning or still dead. Outdoors, nobody hands you a puzzle to solve at every tree; the woods are
exactly as thorough as the cabin was, but what they ask of you is movement, cold, and sightlines, not
a hook.

---

## 4. The design

### 4.1 What "living" means, mechanically (five properties)

1. **Individuation**: things a person would tell apart are told apart — seats by label (§4.3), trees by
   a notable feature; things they would not tell apart are a class that yields one on demand (tussocks,
   deadfall, snow). Rule: *individuate what a player would individuate; classify the rest; let classes
   yield individuals* (`take a branch` from "deadfall").
2. **State that persists and shows**: the stripped seat stays stripped ("bared clips showing where
   its cushion was hacked out"); the fire ring you built is there next look; the drift you dug has a
   hole. Every state-changing Effect has a scene/examine variant.
3. **Processes visible**: the fire's stage, the cold's band, the light failing, the pilot's body
   cooling and stiffening — the room changes while you stand in it.
4. **Other people's traces**: what a co-player did shows (the half-sawn branch, the scuffed rime, a
   dropped thing on the floor) — objects that land in a space render into that space's frame
   regardless of who dropped them.
5. **Sensory layers**: smell, sound, cold, draft, light as addressable elusive nouns with sense
   verbs — the census's "entities a MUD usually forgets." *(Proposed by Claude, for Andrew's check:)*
   the decided schema is the mechanism, and rooms as entities complete it. Cold, draft, light, smoke and
   smell are **states of the room entity** (§4.8), each produced by the things that cause it — the tear
   makes the draft, the fire the smoke and the light, the pilot's body in a warming cabin the smell —
   and each of those things carries what it gives the senses, with its cadence, in its `sensed` field
   (document 05 §4.5; document 06). What is not an object at all — the wind, the cold itself — is a row
   of `class: elusive` (document 05 §4.5) that points at its source. So `feel the draft`, `smell the
   smoke` and `listen` address the room's own states and lead to what makes them, and every room has
   them because every room has air, light and things in it — no per-room hand-authoring and no special
   primitive. The loops still census each room's elusives, since that is what a room *is*.

### 4.2 Density with purpose (how a room earns its objects)

Every object is placed for one of two reasons, and the row says which:
- **a goal put it there** (a resource on one of its ways: the lighter, the wire, the hand radio's
  batteries, the manual);
- **realism put it there** (the census: the kneeboard, the airsickness bag, the headset).

Every room has obvious flavour that is tryable and honest; earned finds (inside things, per the reveal
rule, DR-24); things that connect to a goal's ways; and a trade-off (the fuel-soaked sleeping bag). The
**power ∝ cost** curve (also named in **16 — Players and kit** §4.3): the obvious is weak, the good
costs search, time, or a tool.

### 4.3 The seats — the exemplar

The 206's seats are the pilot's and the right seat up front, and **1A/1B/2A/2B** behind (Andrew,
2026-09-16; document 16 §4.6). Each is the same parts-machine — cover, cushion, belt, bolts — with
**different** damage and **different** finds. The damage, as document 16 §4.6 places it: 1A intact;
1B wrenched on its bolts (a laptop bag under it); 2A thrown loose — a movable seat, a windbreak, a sled
base; 2B thrown hard against the hull (under it, a life-vest pouch — vest fabric, straps, a whistle, a
signal object). Other damage a seat can carry: a cushion torn with the foam showing; a belt buckled; a
belt cut clean where someone freed themselves — the story.

The finds, placed across the seats, the hat shelf and the cargo net when the cabin zone is censused:
in the seat pockets, a safety card, a chocolate bar, an airsickness bag (paper), a boarding pass with a
name; under the seats, a AA battery, a penknife (the second blade), a hair clip, coins, a mitten.

`look under 1b` is the reveal act for seats; `search` covers pockets; `cut`/`pry`/`tear` the
parts-machine. Seats are addressable as a class: `look under the seats` composes what each hides once
revealed.

*(Proposed by Claude, for Andrew's check:)* `under` is one of the relations things really stand in —
the containment modes on · under · against · inside of document 03 §4.4 (extension 1) and the
`located.relation` of document 05 §4.5 — and hiding is physical. The variants that do different things
are each their own operation, within the grammar's `VERB [RELATION] thing` forms: **`look under`**
(sight — it needs light, and it shows what is there to be seen), **`feel under`** / **`reach under`**
(touch — it works in the dark and finds what the eye cannot, and it can find the sharp thing the hard
way), **`look behind`**. They are built with extension 1 when the cabin zone is implemented — before
any outdoor zone is built, since the valley hides things under logs and in hollows the same way.

### 4.4 The prose style guide (rules first, then words)

1. A frame describes POSITION, never history.
2. An object's phrase carries its own CHARACTER, not its position.
3. Persons get their own sentence, never a list item.
4. No internal commas in a noun phrase that will sit in a list.
5. Show functional flavour; hide load-bearing things inside containers.
6. Examine prose names what the thing AFFORDS (the signifier rule): "one edge wicked-sharp," "would
   tie, bind or wrap."
7. State variants are written for every state an Effect can set.
8. Repeated lines (frames, ticks) are plain; objects carry the colour.
9. Read it: render every scene, then read the zone whole before committing.

This is the content-side companion to the architecture's own **Voice** principle
(`presentation.md` §4): phrasing must be *specific-and-witty* or it fails its purpose — a
derived-dry "the shirt is too light to block wind" satisfies the physics and loses the game's
identity. Both agree on who owns the words: Claude (or whichever model is drafting) writes under
these rules; Andrew owns the voice and rewrites freely.

*(Proposed by Claude, for Andrew's check:)* **the voice is judged by reading.** Rule 9 and
`presentation.md` §4 already say how: the crash rooms are rendered with `make render-scenes` and read
together at this document's sitting; the reading, and any rewrite, is Andrew's. What renders today
predates the four-seat plane and the season, so that reading judges the *voice*, not the content.

*(Proposed by Claude, for Andrew's check:)* **what the prose may use.** Each device was tested against
the rule the game's feedback follows — does it name a verb, list what is reachable, or hint at a
solution? — and against document 03. **Groups** (document 03 §4.1b) fold identical or gathered things:
the room shows "a pile of clothes", and `look at the pile` lists its members. **Three-form phrases** (a
thing's `scene`, `item` and `glance` wording for near, listed and far) are in: how a thing reads depends
on how far away you are, which is perception, not a hint. **Glimpse lines** (what you can make out in
the next zone) are in for the same reason — they say what is really visible from where you stand
(document 03 §4.2; document 19's perception). **Look-under** is in: hiding is physical, things are
inside and under things (document 03), and looking under something is an act on the world. None names
a verb or lists what is in reach.

### 4.5 The individuation rule for the valley (traversal terrain)

Outdoor rooms do not get a puzzle hook each; they get the systems (movement effort, exposure,
sightlines) and a class-yielding census (deadfall, willow, snow types). Individuate the landmarks
(the drift log, the erratic boulder, the tamarack) and the goals' resources; classify the rest. This is
about not forcing a hook per room, never about a ceiling on what a room contains (Andrew, 2026-09-16):
every outdoor room is censused to the same real-world depth as the crash rooms, and grown without a
ceiling by the loops.

**In early October the census is deeper, not shallower** *(proposed by Claude, for Andrew's check)*. An
inch of snow leaves the ground readable: fallen birch and aspen leaves, moss and lichen, berries still
on the bush, mushrooms frozen where they stood, mud stiffening in the ruts, the creek running, skim ice
on still water, tracks printed sharp in the new snow. None of it holds still for the week — the storm
lays snow down day by day, each clear night drives frost into the ground and thickens the ice. So snow
depth and type, the depth of frozen ground, ice thickness and what is buried are **states on the room**
(§4.8), changed by the weather system, and the same zone reads and plays differently on day one and day
six: berries you picked on the first day are under the storm's snow by the fifth, and the lake skim you
could not stand on may, by the end of a cold week, bear a person (document 18 §4.8 has the ice
arithmetic).

### 4.6 The nine crash-room censuses

A **census** is the "ontological Turing test" the `cockpit.md` banner names: for one room, ask what is
*here* if it were real, what a real person could *do* with each thing, and whether the game already lets
them — before anything is built or changed. Each census walks the same shape: the scene as if it were
real; an entity census (structure, loose kit, substances, and the "elusive" entities a MUD usually
forgets — cold, draft, sound, smell, light, time); the candidate commands each entity invites; what is
built today; and a flat, unranked gap analysis (recommendations only — no code changes from the census
itself). The nine rooms, one line each:

- **`cockpit.md`** — the EXEMPLAR the other eight follow; the pilot's body, the six-pack instruments,
  the manual and chart; the shared cabin baseline (structure and elusive entities) that `mid_cabin.md`
  and `rear_cabin.md` both point back to instead of repeating.
- **`mid_cabin.md`** — the crafting heart of the crash: the wrenched seat, the burst duffel, the
  hat shelf and the cargo net — where a survivor *harvests* foam, fabric, webbing, tools.
- **`rear_cabin.md`** — the cold room and the warm one at once: the hull is open here, so snow and
  wind come in, but the stowage behind it holds the engine cover, the game's warmth prize.
- **`outside_nose.md`** — the first exterior censused, and the pattern flips: no built loose
  objects, pure scenery plus the elusive; the coldest, most exposed spot, and where the fuel is.
- **`outside_tail.md`** — the breach exit: the torn stump where the tail tore away, one way back
  into the rear cabin, the other out along the crash scar.
- **`fuselage_top.md`** — the highest, most exposed point, where the plane's antenna was; one of the
  few outdoor rooms with a genuine hook, a deliberate exception to the traversal-terrain rule, named as
  such in its own banner. Its census was written around rigging the ELT; the ELT is broken (Andrew,
  2026-09-27; document 14 §3).
- **`debris_trail.md`** — the scatter: the gouge the plane tore on its way in, a spilled mail sack and
  what else the crash shed along it — found by looking *through* the mess, not at a glance.
- **`tail_section.md`** — the expedition cache: the severed tail rode out here with its load, sealed
  inside a crushed tail cone and a nailed freight crate that both want a lever and real anger.
- **`treeline.md`** — the survival core's supply room and the gateway to the wider woods: wood,
  tinder, and shelter material, earning its keep as a resource-plus-gateway rather than a unique
  hook — exactly what the traversal-terrain rule asks of an outdoor zone.

The nine censuses predate the 206 interior and the season: their overhead bins are the hat shelf and
the cargo net (document 16 §4.6), and their snow and cold are the first week of October's (document 13
§4.2). They are re-run at the cabin zone's census, with the plane as an entity (§4.8).

### 4.7 Lens pass

- **The Toy** (GD — is it fun to poke without a goal?) — YELLOW → GREEN once the four seats' finds
  and the deeper physics resolver are in place. Seats with different guts are a toy; identical ones
  are a puzzle with one answer.
- **Curiosity** (GD) — GREEN. Look-under, pockets, labels: every seat asks "and this one?"
- **Surprise** (GD) — GREEN. A cut belt and a boarding pass with someone's name on it: a story you
  find, not a note you're handed.

### 4.7a Naming things apart — a rule the loops must follow (Andrew, 2026-09-18)

There is no numbered menu (DR-08c): when two things a player can plausibly confuse are in reach, the
game asks `Which seat do you mean?` and nothing more. So every pair of confusable things in a room
needs **a word that separates them** in its authored prose — the *wrenched* seat and the *thrown*
seat, seat *1a* and *1b*. Identical things (three glass shards) never ask, because it does not matter
which one you take. **A room that can ask an unanswerable question is a bug in the room**, and `make
validate` should catch it (document 04 §3.10).

### 4.8 Rooms are entities — and the plane is one (Andrew, 2026-09-26; the mechanism proposed by Claude, for Andrew's check)

**What Andrew decided** (§2): the plane is an entity with openings that are open or closed and an
internal heat that a fire inside raises; a fire heats its area and leaves residual heat in other areas;
body parts have heat. So a room is not a backdrop things sit in. It is an entity of the ontology with
the same schema as everything in it (document 05 §4.5) — materials, parts, states, `sensed` with its
cadence, relations, `could_become`, synonyms — plus what only a place has: its **air** (volume,
temperature, wind, smoke, damp), its **light**, its **floor or ground**, and its exits (document 03
§4.1a).

**The plane.** One entity, and the crash rooms inside it are its interior.
- *Its parts:* the fuselage skin (aluminium sheet under a millimetre thick, over a frame), the
  windscreen and windows (acrylic — document 18 §4.8), the pilot's door, the right door, the double
  cargo door, the breach where the tail tore away, the seams the impact opened; the seats, the hat
  shelf and the baggage bay (document 16 §4.6); the wings with fuel in them; the engine, and the
  battery in the nose. The tail section out on the trail is a separate entity, with the tail cone and
  the broken ELT.
- *Each opening is a part with an area and a state* — open · partly blocked · blocked · closed ·
  jammed · iced shut. The state is what its wind sound speaks from (document 08 §4.8), what lets the
  wind and the snow in, and what lets the heat out.
- *One air volume.* In a 206 the cockpit, the two passenger rows and the baggage area are one cabin
  with no bulkhead between them — about 3.7 m long, 1.1 m wide and 1.3 m high (12 ft 1 in × 3 ft 8 in ×
  4 ft 2 in, Cessna Flyer Association), some 4–5 m³ of air. The cockpit, the mid cabin and the rear
  cabin stay separate places for where things sit and how the prose reads (document 03), but they
  share **one internal heat**, warmest near whatever is heating it.

**The internal heat, physically** *(first figures, for the heat-system design to redo properly)*.
- *Heat in:* bodies, about 100 W each at rest and several times that working or shivering; a candle,
  about 80 W; a fire or a stove, kilowatts.
- *Heat out:* through the skin — thin aluminium is almost no barrier; the U.S. Army's survival manual
  says that in extreme cold a metal fuselage conducts away what little heat you make, and what holds
  heat is the still air against the walls and whatever lines them (foam, batting, the engine cover) —
  and through every open opening, because the wind changes the air.
- *The air itself holds almost nothing* — roughly 6 kJ per degree for the whole cabin, about a minute
  of one person's heat — so the inside temperature settles within minutes to the balance of those two
  flows, and moves when an opening changes state or a source starts or stops. Roughly: four or five
  people resting in a closed cabin keep it a few degrees above outside; with the breach open, barely
  above; a small fire of a few kilowatts, with an opening for draught, can hold it fifteen to twenty
  degrees above.
- *What that does for the design:* the night-one rule (document 08 §4.1a) becomes physics rather than
  a promise. At the week's night lows (document 13 §4.2) a closed wreck with the party inside is
  survivable in the clothes they crashed in; every opening they close, every lining they put up and
  every body adds degrees; the colder nights later in the week take them away again.

**A fire inside is real, and so is its price.** A fire needs air: in a closed cabin it starves and
smokes, so an opening must stay open, and the openings do double duty — shut to keep heat in, open to
breathe. It makes carbon monoxide; burning seat foam makes the most poisonous smoke in the material
table (document 18); aluminium melts in the coals (from about 600 °C); and warming the shell turns the
frost that everyone's breath has laid on the inside of the cold skin into drips, which is how the
inside of a heated wreck gets wet. Carbon monoxide builds by the physics — headache, dizziness, nausea, confusion, a fire that burns
poorly for want of air — and, left to build, kills over hours, never at once (2026-09-27; document 11
§4.4). Opening an opening,
banking the fire and keeping someone awake on watch (document 06) are the real answers to it.

**Outdoors, a zone is an entity too**: its ground (soil, moss, rock — frozen to a depth that grows every
clear night), its snow cover (depth and type — states of water, document 18 §4.8), its air (temperature
and wind from the weather, sheltered or exposed as document 08 §4.4 bands it), its light. A fire outdoors
warms mostly by radiation, which falls off steeply with distance: it warms a body a metre or two away,
and a reflector behind it (rock, stacked logs, a sheet of hull) sends back part of what would be lost.
The heat that stays is in thermal mass — the hearth stones, the thawed ground under the ashes (where
roots can now be dug, document 23), the embers for hours. So the residual heat in other areas that
Andrew named is, outdoors, the warmed ground, the stones and the lee of the fire; inside the plane, the
connected air carrying heat forward and aft.

**Who owns what.** This document owns that rooms and the plane are entities with these parts and
states. The numbers — heat flow between connected spaces, the openings' areas, the sources' outputs,
the carbon monoxide — belong to the **heat-system design, to be written**. Document 08 §4.4's
wind-exposure and roof numbers stand outdoors; inside the plane they are read off the openings (a
reconciliation for document 08).

## 5. Interactions

**This depends on:**
- **Containment** (`../architecture/containment.md`, DR-24) — the ONE reveal rule (`open` OR
  `searched`) is what "look under," pockets, and every earned find in §4.2–§4.3 actually run on.
- **Presentation** (`../architecture/presentation.md`, DR-23, §4 Voice) — the scene-as-prose `look`
  and the unified `look at X` / `examine X` renderer are what §4.4's style rules are written for;
  groups of identical objects (§4.4) are a presentation mechanism, not a room one.
- **16 — Players and kit** — the seats carry each slot's luggage and injuries; the seat labels in
  §4.3 are that document's.
- **Ontology closure** (`../architecture/ontology-closure.md`, DR-26) — forms, derived capabilities,
  and the probe corpus are the census method's engine-side counterpart: a census gap is only real if
  no existing material/operation precondition already covers it.
- **14 — Rescue** — density with purpose's "a goal put it there" half points at the ways home.
- **06 — Time, sleep and the clock** — property 3 (processes visible) needs the activities/processes
  system to have something to show.
- **The heat system** (no design document yet — to be written) — the room's and the plane's internal
  heat, heat flowing between connected spaces, the openings, carbon monoxide (§4.8).
- **13 — Events, escalation and weather** — the storm laying snow down, frost driving into the ground,
  ice thickening: the states that make a room on day six differ from day one (§4.5).
- **05 — Ontology and sufficiency** — the per-zone schema (§4.5 there) is where a room's own
  materials, parts, states and `sensed` live once rooms are entities (§4.8 here).

**These depend on it:**
- **22 — The world-building loops** — *(proposed by Claude, for Andrew's check:)* when this document is
  finalized, its rules — the five properties (§4.1), density with purpose (§4.2), the style guide
  (§4.4), the outdoor census rule and early October's changing ground (§4.5), naming things apart
  (§4.7a), and rooms as entities (§4.8) — go into the world-builder's scaffold,
  `docs/guides/world-building.md` (document 05 §4.8), which is what the loops read, and into
  `docs/guides/authoring-objects.md` for anyone authoring rows by hand. Both happen before the pilot
  pass on the mid cabin; no loop runs before the design documents are finalized (Andrew, 2026-09-16).
- **02 — The experience** — a sample week reads as prose only if the rooms it moves through hold to
  this style.
- **15 — Moral and social layer** — property 4 (other people's traces) is part of how a co-player's
  action becomes something a third party can witness.
- **08 — Warmth, clothing and shelter** — inside the plane, the wind exposure and the warmth a body
  feels are read off the plane's openings and internal heat (§4.8), not a band on the zone.

---

## 6. Open questions

None open. Claude's answers — the sensory layer (§4.1), the look-under family (§4.3), reading the voice
and what the prose may use (§4.4), and the room rules reaching the loops (§5) — and §4.8's mechanism
are for Andrew's check at this document's sitting.

---

## 7. Review log

- **2026-09-07 (Andrew):** living, interesting rooms — labelled seats to look under and cut, things that
  serve the goals, several ways of doing things.
- **2026-09-16 (Andrew):** every room censused to real-world depth; traversal terrain is no forced hook,
  never fewer entities; the four-seat interior.
- **2026-09-18 (Andrew):** the distinguishable-names rule, an authoring requirement for the loops.
- **2026-09-26 (Andrew, in document 10's review):** the plane is an entity with openings and an internal
  heat; a fire heats its area and leaves residual heat in others; body parts have heat.
- **2026-09-26 (Claude, self-review):** rooms and the plane as entities (§4.8); the season's changing
  ground (§4.5); the sensory layer as room states; look-under as the `under` relation with its own
  family of acts; reading the voice; groups, three-form phrases, glimpses and look-under in the prose;
  the room rules into the loops' scaffold — all for Andrew's check.
- **2026-09-27 (Andrew):** nothing kills instantly; death comes by the body running down, carbon
  monoxide from a fire inside among the ways.

## 8. What exists today

**Built**
- The nine crash rooms, as zones with position, terrain tags, and adjacency:
  `game/world/scenarios/whiteout/zones.py` (`cockpit`, `mid_cabin`, `rear_cabin`, `outside_nose`,
  `fuselage_top`, `outside_tail`, `debris_trail`, `tail_section`, `treeline` — all nine, and nothing
  beyond them).
- Their scene-spaces (property 1's "where things sit"), one `SPACE_TABLE` entry per zone:
  `game/world/scenarios/whiteout/spaces.py` (e.g. `mid_cabin`'s `seat_rows` / `overhead` / `aisle`).
- State that persists and shows (property 2), live today: the seat's `residue_cushion: "clipped"`
  state variant renders "Seat 11B stands half-stripped, bared clips showing where its cushion was
  hacked out" — `game/world/scenarios/whiteout/appearance.py`.
- The aggregation of identical objects into one sentence (part of property 4's "other people's
  traces," and a presentation mechanism, DR-23): two authored `deadfall` branches render as "{count}
  snow-crusted deadfall branches" when both are present — `appearance.py`.
- A probe corpus over the censuses: `game/world/scenarios/whiteout/probes/census.py` (mixed
  `pass`/`todo` status per candidate command); the coverage floor at
  `game/world/scenarios/whiteout/probes/BASELINE`.

**Designed, not built**
- The fifty outdoor zones for the whole valley (document 01): `zones.py` carries exactly the nine
  crash-cluster zones above and nothing else.
- `look under` and its family (§4.3) — the seat exemplar's own reveal act — unbuilt: no handler,
  operation, or probe anywhere references it.
- The sensory layer (property 5, §4.1) — none of the nine censuses' elusive entities (cold, draft,
  smell, sound, light, darkness, time) exist as addressable objects; nothing in `objects.py` or
  `appearance.py` represents them.
- A generic class-that-yields-individuals primitive (property 1's "let classes yield individuals," e.g.
  "take a branch from the deadfall") — not built as a mechanism; today's deadfall is two authored
  instances that merely display as an aggregate (above), not an unbounded source a player can keep
  drawing from.
- The four-seat interior (§4.3) — see **16 — Players and kit** §8 for the full gap: the seat objects in
  `objects.py` are still `11B`/`12C`, not `1A`/`1B`/`2A`/`2B`/the right seat.
- Rooms and the plane as entities (§4.8) — nothing in code: a zone in `zones.py` carries position,
  terrain tags, adjacency and a survey line, with no states, parts or heat; the plane is not an entity,
  and its openings are not parts with states.

**Nothing**
- The room-authoring rules promoted into a guide: `docs/guides/authoring-objects.md` does not yet
  mention individuation, state persistence, or the style guide — this document's rules stand only
  here until reviewed and promoted (§5).
