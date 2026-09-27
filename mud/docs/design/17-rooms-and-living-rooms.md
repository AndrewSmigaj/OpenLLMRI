# 17 — Rooms and living rooms: individuation, state that persists, the prose style, the crash rooms

> **Status: `draft for review` (2026-09-16).**
> **Architecture counterparts:** [`../architecture/containment.md`](../architecture/containment.md)
> (DR-24, the reveal rule that `search`/`open`/`look under` all obey) and
> [`../architecture/presentation.md`](../architecture/presentation.md) §4 (Voice — the prose
> principle behind the style guide in §4.4).
> **Sources:** `docs/investigation/design/living-rooms.md` (primary — the five properties, density
> with purpose, the seat-row exemplar, the style guide, the individuation rule) · the nine room
> censuses, `docs/scenarios/whiteout/rooms/*.md` · `docs/architecture/implementation-architecture.md`
> (DR-23, DR-24) · `docs/investigation/design/00-provenance-audit.md` §1–§2 · code:
> `game/world/scenarios/whiteout/zones.py`, `spaces.py`, `appearance.py`, `objects.py`;
> `game/world/scenarios/whiteout/probes/census.py`.

> **2026-09-26 (Claude, for Andrew's check).** Two things arrived after this draft. **The season is
> October, at freeze-up** (`README.md`): the fifty outdoor zones in §8 were designed in July for
> December, and their census changes with an inch of snow, open ground and skim ice (§4.5). And
> **rooms are entities, the plane among them** (Andrew, 2026-09-26 — §2, §4.8).

---

## 2. Provenance

### Andrew's decisions

- **"we don't want half thought rooms we want living interesting rooms — seats with cushions you
  can look under, labeled so you can look under different rows or cut different seats; the things
  facilitate the rescue goals, with several ways of doing things."** (2026-09-07.) This is the
  brief the rest of this document works from.
- **Every room is censused to real-world depth — any and all entities and relations, the natural
  world included; "traversal terrain" means no forced puzzle hook per room, not fewer entities.**
  (2026-09-16, clarifying §4.5.) In his own words, recorded in `living-rooms.md` §5: *"'traversal
  terrain' is about not forcing a puzzle hook per room. It is NOT a cap on entities: every outdoor
  room is censused to real-world depth — the ground and what is under it, rock, clay, bark, every
  substance and every relation a person would try — and grown without a ceiling by the loops. A
  class that yields individuals is still a full entity."*
- **The four-seat interior is a go.** (2026-09-16, recorded in document **16 — Players and kit**
  and the DR-14a/DR-15a amendment.) This supersedes the six-seat rows this document's §4.3 keeps —
  see that section for what is superseded and what is kept.
- **The plane is an entity itself, with openings that are open or closed and an internal heat that a
  fire inside raises; fire heats its area and leaves residual heat in other areas; body parts have heat
  as part of their ontology.** (2026-09-26, in document 10's review log, answering its Q3.) In his
  words: *"we will have the plane as an entity itself with flags for open or closed and a fire source
  rule which uses it's heat amount to change it's internal heat calue, so this would all be part of
  planning the design and implementation of the fire and heat system"*; *"fire would generate heat in
  that area and residual heat in other areas"*. Rooms are therefore entities in the ontology like
  everything in them (§4.8). *(Recorded here by Claude, 2026-09-26.)*

### Proposals (Claude)

Everything else is a proposal for review:

- The five properties of a "living" room (§4.1), density with purpose (§4.2), the seat-row exemplar
  and its table of finds (§4.3), the nine-rule prose style guide (§4.4), and the lens pass (§4.7) —
  all from `living-rooms.md`, listed as Claude's addition in the provenance audit's own table
  ("living-rooms — individuation rule, state that persists, the style guide").
- The nine room-census documents themselves (`docs/scenarios/whiteout/rooms/*.md`) — the
  "ontological Turing test" method (census first, then the built room, then the gaps) is named in
  the `cockpit.md` banner as coming from the `ontology-generator` skill, not from Andrew directly.

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

1. **Individuation**: things a person would tell apart are told apart — seats by label (the seat
   rows, §4.3), trees by a notable feature; things they would not tell apart are a class that yields
   one on demand (tussocks, deadfall, snow). Rule: *individuate what a player would individuate;
   classify the rest; let classes yield individuals* (`take a branch` from "deadfall").
2. **State that persists and shows**: the stripped seat stays stripped ("bared clips showing where
   its cushion was hacked out"); the fire ring you built is there next look; the drift you dug has a
   hole. Every state-changing Effect has a scene/examine variant.
3. **Processes visible**: the fire's stage, the cold's band, the light failing, the pilot's body
   cooling and stiffening — the room changes while you stand in it. *(Claude, 2026-09-26: "the
   pilot's breathing" is superseded — he starts the run dead, Andrew 2026-09-17; document 12 §4.3a.)*
4. **Other people's traces**: what a co-player did shows (the half-sawn branch, the scuffed rime, a
   dropped thing on the floor) — objects that land in a space render into that space's frame
   regardless of who dropped them.
5. **Sensory layers**: smell, sound, cold, draft, light as addressable elusive nouns with sense
   verbs — the census's "entities a MUD usually forgets."

### 4.2 Density with purpose (how a room earns its objects)

Every object is placed for one of two reasons, and the row says which:
- **the rescue graph put it there** (a path's resource: the lighter, the wire, the ELT, the manual);
- **realism put it there** (the census: the kneeboard, the airsickness bag, the headset).

Every room has: obvious flavour that is tryable and honest; two or three earned finds (inside
things, per the reveal rule below); at least one thing that connects to a goal path; and one
trade-off (the fuel-soaked sleeping bag). The **power ∝ cost** curve (also named in
**16 — Players and kit** §4.3): the obvious is weak, the good costs search, time, or a tool.

### 4.3 The seat rows — the exemplar (recast to four seats)

> **Recast 2026-09-16** — the 206's four-seat interior (**16 — Players and kit** §4.6: seats
> 1A/1B/2A/2B plus the right seat; a hat shelf and a cargo net instead of overhead bins) is now the
> approved layout. The six-seat rows below are the earlier draft, kept for their FINDS, which
> redistribute across the four seats, the hat shelf, and the cargo net — the layout itself is
> superseded.

A bush plane carries six to nine seats. The earlier draft proposed rows 11A/11B/11C (mid) and
12A/12B/12C (rear), each the same parts-machine (cover, cushion, belt, bolts) with **different**
damage and **different** finds:

| seat | state | under / in it (the seat pocket, and what a look-under reveals) |
|---|---|---|
| 11A | intact, belt buckled | pocket: safety card; under: a AA battery |
| 11B | wrenched on its bolts (as now) | pocket: chocolate bar; under: the penknife (the second blade) |
| 11C | cushion torn, foam showing | pocket: an airsickness bag (paper); under: a hair clip, coins |
| 12A | thrown loose — a movable seat (a windbreak, a sled base) | under: nothing; it is the loose frame that matters |
| 12B | belt cut clean (someone freed themselves — the story) | pocket: a boarding pass with a name; under: a mitten |
| 12C | thrown hard against the hull (as now) | under: a life-vest pouch — vest fabric, straps, a whistle (a signal object) |

`look under 11b` becomes the reveal verb for seats; `search` covers pockets; `cut`/`pry`/`tear` the
parts-machine. Rows are addressable as a class: `look under the seats` composes what each hides once
revealed. Recast to four seats (**16 — Players and kit** §4.6), the same different-damage-different-
find principle applies to 1A/1B/2A/2B and the right seat; only the count and the labels change.

### 4.4 The prose style guide (rules first, then words — from the v3 retrospective)

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

### 4.5 The individuation rule for the valley (traversal terrain)

Outdoor rooms do not get a puzzle hook each; they get the systems (movement effort, exposure,
sightlines) and a class-yielding census (deadfall, willow, snow types). Individuate the landmarks
(the drift log, the erratic boulder, the tamarack) and the graph's resources; classify the rest.
Clarified by Andrew, 2026-09-16 (quoted in full in §2): this is about not forcing a hook per room,
never about a ceiling on what a room contains — every outdoor room is censused to the same
real-world depth as the crash rooms, and grown without a ceiling by the loops.

**At freeze-up the census is deeper, not shallower** *(Claude, 2026-09-26 — the season; for Andrew's
check)*. An inch of snow leaves the ground readable: fallen birch and aspen leaves, moss and lichen,
berries still on the bush, mushrooms frozen where they stood, mud stiffening in the ruts, the creek
running, skim ice on still water, tracks printed sharp in the new snow. None of it holds still for the
week — the storm lays snow down day by day, each clear night drives frost deeper into the ground and
thickens the ice. So snow depth and type, the depth of frozen ground, ice thickness and what is buried
are **states on the room** (§4.8), changed by the weather system, and the same zone reads and plays
differently on day one and day six: berries you picked on Monday are under a foot of snow by Friday,
and the lake skim you could not stand on may, by the end of a cold week, bear a person (document 18
§4.8 has the ice arithmetic).

### 4.6 The nine crash-room censuses

A **census** is the "ontological Turing test" the `cockpit.md` banner names it: for one room, ask
what is *here* if it were real, what a real person could *do* with each thing, and whether the game
already lets them — before anything is built or changed. Each census walks the same shape: the scene
as if it were real; an entity census (structure, loose kit, substances, and the "elusive" entities a
MUD usually forgets — cold, draft, sound, smell, light, time); the candidate commands each entity
invites; what is built today; and a flat, unranked gap analysis (recommendations only — no code
changes from the census itself). The nine rooms, one line each:

- **`cockpit.md`** — the EXEMPLAR the other eight follow; the pilot, the radio, the six-pack
  instruments, the manual and chart; the shared cabin baseline (structure and elusive entities) that
  `mid_cabin.md` and `rear_cabin.md` both point back to instead of repeating.
- **`mid_cabin.md`** — the crafting heart of the crash: the wrenched seat, the jammed overhead bin,
  the burst duffel, the oxygen masks — where a survivor *harvests* foam, fabric, webbing, tools.
- **`rear_cabin.md`** — the cold room and the warm one at once: the hull is open here, so snow and
  wind come in, but the aft bin behind it holds the engine cover, the game's warmth prize.
- **`outside_nose.md`** — the first exterior censused, and the pattern flips: no built loose
  objects, pure scenery plus the elusive; the coldest, most exposed spot, and where the fuel is.
- **`outside_tail.md`** — the breach exit: the torn stump where the tail tore away, one way back
  into the rear cabin, the other out along the crash scar.
- **`fuselage_top.md`** — one of the few outdoor rooms with a genuine hook: the highest, most
  exposed point, where the antenna was, so it anchors the ELT-rig puzzle; a deliberate exception to
  the traversal-terrain rule, named as such in its own banner.
- **`debris_trail.md`** — the scatter: the gouge the plane tore on its way in, shedding a burst
  survival duffel, a wind-packed drift, a spilled mail sack — found by looking *through* the mess,
  not at a glance.
- **`tail_section.md`** — the expedition cache: the severed tail rode out here with the baggage bay,
  sealed inside a crushed tail cone and a nailed freight crate that both want a lever and real anger.
- **`treeline.md`** — the survival core's supply room and the gateway to the wider woods: wood,
  tinder, and shelter material, earning its keep as a resource-plus-gateway rather than a unique
  hook — exactly what the traversal-terrain rule asks of an outdoor zone.

*(Claude, 2026-09-26: the nine censuses predate the 206 interior and the season. Their overhead bins
are the hat shelf and the cargo net now — document 16 §4.6, the finds redistributed as §4.3 says — and
their December snow and cold are October's inch of snow and freeze-up; the censuses are re-run at the
cabin zone's census, with the plane as an entity (§4.8).)*

### 4.7 Lens pass

- **The Toy** (GD — is it fun to poke without a goal?) — YELLOW → GREEN once the four-seat recast's
  finds and the deeper physics resolver are in place. Seats with different guts are a toy; identical
  ones are a puzzle with one answer.
- **Curiosity** (GD) — GREEN. Look-under, pockets, labels: every seat asks "and this one?"
- **Surprise** (GD) — GREEN. A cut belt and a boarding pass with someone's name on it: a story you
  find, not a note you're handed.

---

### Naming things apart — a rule the loops must follow (Andrew, 2026-09-18)

There is no numbered menu (DR-08c): when two things a player can plausibly confuse are in reach, the
game asks `Which seat do you mean?` and nothing more. So every pair of confusable things in a room
needs **a word that separates them** in its authored prose — the *wrenched* seat and the *thrown*
seat, seat *1a* and *1b*, the *forward* bin and the *aft* bin. Identical things (three glass shards)
never ask, because it does not matter which one you take. **A room that can ask an unanswerable
question is a bug in the room**, and `make validate` should catch it (document 04 §3.10, Q10).

### 4.8 Rooms are entities — and the plane is one (Andrew, 2026-09-26; the mechanism is Claude's, for Andrew's check)

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
  shelf and the baggage bay (document 16 §4.6); the wings with fuel in them; the engine and its
  battery. The tail section out on the trail is a separate entity now, with the tail cone and the ELT.
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
  a promise. At mid-October's night lows of about −8 °C (Fairbanks normals, document 16 §4.9) a closed
  wreck with the party inside is survivable in the clothes they crashed in; every opening they close,
  every lining they put up and every body adds degrees; the colder nights at the end of the week take
  them away again.

**A fire inside is real, and so is its price.** A fire needs air: in a closed cabin it starves and
smokes, so an opening must stay open, and the openings do double duty — shut to keep heat in, open to
breathe. It makes carbon monoxide; burning seat foam makes the most poisonous smoke in the material
table (document 18); aluminium melts in the coals (from about 600 °C); and warming the shell turns the
frost that everyone's breath has laid on the inside of the cold skin into drips, which is how the
inside of a heated wreck gets wet. How dangerous the carbon monoxide may be is Andrew's (Q6).

**Outdoors, a zone is an entity too**: its ground (soil, moss, rock — frozen to a depth that grows every
clear night at freeze-up), its snow cover (depth and type, document 18 Q4), its air (temperature and
wind from the weather, sheltered or exposed as document 08 §4.4 bands it), its light. A fire outdoors
warms mostly by radiation, which falls off steeply with distance: it warms a body a metre or two away,
and a reflector behind it (rock, stacked logs, a sheet of hull) sends back part of what would be lost.
The heat that stays is in thermal mass — the hearth stones, the thawed ground under the ashes (where
roots can now be dug, document 23 Q3), the embers for hours. So Andrew's *"residual heat in other
areas"* is, outdoors, the warmed ground, the stones and the lee of the fire; inside the plane, the
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
  the aggregation of identical objects (§8) is a presentation mechanism, not a room one.
- **16 — Players and kit** — the seats carry each slot's luggage and injuries; the seat labels in
  §4.3 are the ones that document proposes.
- **Ontology closure** (`../architecture/ontology-closure.md`, DR-26) — forms, derived capabilities,
  and the probe corpus are the census method's engine-side counterpart: a census gap is only real if
  no existing material/operation precondition already covers it.
- **14 — Rescue paths** — density with purpose's "the rescue graph put it there" half depends on
  the rescue graph existing to point at.
- **06 — Time, sleep and the clock** — property 3 (processes visible) needs the activities/processes
  system to have something to show.
- **The heat system** (no design document yet — to be written; *Claude, 2026-09-26*) — the room's and
  the plane's internal heat, heat flowing between connected spaces, the openings, carbon monoxide
  (§4.8).
- **13 — Events, escalation and weather** — the storm laying snow down, frost driving into the ground,
  ice thickening: the states that make a room on day six differ from day one (§4.5).
- **05 — Ontology and sufficiency** — the per-zone schema (§4.5 there) is where a room's own
  materials, parts, states and `sensed` live once rooms are entities (§4.8 here).

**These depend on it:**
- **22 — The world-building loops** — the room-authoring rules this document proposes (§4.1, §4.4,
  §4.5) are meant to promote into `docs/guides/authoring-objects.md` and govern how the fifty
  outdoor zones get authored (open question 3).
- **02 — The experience** — a sample week reads as prose only if the rooms it moves through hold to
  this style.
- **15 — Moral and social layer** — property 4 (other people's traces) is part of how a co-player's
  action becomes something a third party can witness.
- **08 — Warmth, clothing and shelter** — inside the plane, the wind exposure and the warmth a body
  feels are read off the plane's openings and internal heat (§4.8), not a band on the zone.

---

## 6. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9) against block 1, the season and rooms as entities.**
Q1, Q2, Q4 and Q5 are answered by the decided design, each marked for Andrew's check; Q3 is rewritten
(it assumed the loops could start before the design is finalized); Q6 is new and his. The original
wording of every question is kept as the record.

~~1. The prose voice needs a render read, not a text approval.~~ **Claude's answer (2026-09-26), for
   Andrew's check:** already decided by this document's own rule 9 (§4.4: render every scene, then read
   the zone whole) and by `presentation.md` §4 (the voice is Andrew's to rewrite). The nine rooms are
   rendered with `make render-scenes` and read together at the sitting; the reading, and any rewrite,
   is his. One caution: what renders today is the six-seat, December wreck, so the reading judges the
   *voice*, not the content — the content changes with the four-seat plane entity (§4.8) and October
   (§4.5).

   *(The original, kept as the record:)* **The prose voice needs a render read, not a text approval.** `living-rooms.md`'s own rule 9 is
   "read it" — render every scene and read the zone whole before committing — and `presentation.md`
   §4 leaves Voice open for Andrew to rewrite freely. *Options:* (a) sign off on the style guide from
   this document's text alone; (b) render the nine crash rooms and read them together at the review
   sitting before signing off. *Recommendation then:* (b) — a style guide is a hypothesis about prose
   until it is read.

~~2. Which presentation leftovers survive?~~ **Claude's answer (2026-09-26), for Andrew's check:**
   each of the four was tested against the ground the removals used — does it name a verb, list what is
   reachable, or hint at a solution? — and against document 03's review (2026-09-17). **Masses** (one
   authored sentence folding the rest of a space) are superseded by **groups** (document 03 §4.1b): the
   room shows "a pile of clothes", and `look at the pile` lists its members. **Three-form phrases** (a
   thing's `scene`, `item` and `glance` wording for near, listed and far) survive: how a thing reads
   depends on how far away you are, which is perception, not a hint. **Glimpse lines** (what you can
   make out in the next zone) survive for the same reason — they say what is really visible from where
   you stand (document 03 §4.2; document 19's perception). **Look-under** survives: hiding is physical,
   things are inside and under things (document 03 review, 2026-09-17), and looking under something is
   an act on the world. None names a verb or lists what is in reach.

   *(The original, kept as the record:)* **Which presentation leftovers survive?** Masses (identical objects aggregating into one
   sentence), three-form phrases, glimpse lines, and look-under are all named across the sources,
   but the provenance audit records several removals elsewhere (the verb-list redirect, the sibling
   near-miss hint) on grounds that would apply here too if any of these turn out to hint at a
   solution. *Options:* (a) treat all four as still-live conventions until told otherwise; (b) audit
   each one explicitly at this sitting. *Recommendation then:* (b) — a five-minute check against the
   same "does this give something away" question the removals used, done once, in this review.

~~3. The room-authoring rules for the loops — start the loops now, promote the guide later?~~
   **Rewritten (Claude, 2026-09-26):** the question offered starting the loops before this document is
   finalized, which Andrew ruled out — no agent runs a loop until every design document is finalized
   (document 05 §2, 2026-09-16). **The answer:** when this document is finalized, its rules — the five
   properties (§4.1), density with purpose (§4.2), the style guide (§4.4), the outdoor census rule and
   October's changing ground (§4.5), naming things apart, and rooms as entities (§4.8) — go into the
   world-builder's scaffold, `docs/guides/world-building.md` (document 05 §4.8), which is what the
   loops actually read, and into `docs/guides/authoring-objects.md` for anyone authoring rows by hand.
   Both happen before the pilot pass on the mid cabin.

   *(The original, kept as the record:)* **The room-authoring rules for the loops.** `living-rooms.md`'s banner says this promotes into
   `docs/guides/authoring-objects.md` "on approval"; nothing has been added there yet.
   *Options:* (a) let the fifty-outdoor-zone loops start from this document's rules now, behind the
   existing content seams, and promote the guide afterward; (b) wait for the promotion before any
   loop authors a new room. *Recommendation then:* (a) — the promotion is a paperwork step, not a gate
   on content; the rules are already specific enough to build from.

~~4. `look under` is still unbuilt.~~ **Claude's answer (2026-09-26), for Andrew's check:** it is
   designed; it is not yet built, like every other part of the design. `under` is one of the relations
   things really stand in — the containment modes on · under · against · inside of document 03 §4.4
   (extension 1) and the `located.relation` of document 05 §4.5 — and hiding is physical. The
   variants that do different things are each their own operation, within the grammar's
   `VERB [RELATION] thing` forms: **`look under`** (sight — it needs light, and it shows what is there
   to be seen), **`feel under`** / **`reach under`** (touch — it works in the dark and finds what the eye
   cannot, and it can find the sharp thing the hard way), **`look behind`**. It is built with
   extension 1 when the cabin zone is implemented — before any outdoor zone is built, since the valley
   hides things under logs and in hollows the same way.

   *(The original, kept as the record:)* **`look under` is still unbuilt.** The seat-row exemplar (§4.3) names it as the reveal verb for
   seats, but no operation, handler, or probe anywhere in the codebase implements or even tests for
   it. *Options:* (a) build it before any of the fifty outdoor zones start populating landmarks,
   since this document's own exemplar depends on it; (b) leave seats reachable only through `search`
   and `cut`/`pry` until a later pass. *Recommendation then:* (a) — the exemplar this document points
   to for "how a room is living" cannot fully demonstrate its own point without it.

~~5. The "elusive" sensory layer has no generic mechanism.~~ **Claude's answer (2026-09-26), for
   Andrew's check:** the decided schema is the mechanism, and rooms as entities complete it. Cold,
   draft, light, smoke and smell are **states of the room entity** (§4.8), each produced by the things
   that cause it — the tear makes the draft, the fire the smoke and the light, the pilot's body in a
   warming cabin the smell — and each of those things carries what it gives the senses, with its
   cadence, in its `sensed` field (document 05 §4.5; document 06). What is not an object at all — the
   wind, the cold itself — is a row of `class: elusive` (document 05 §4.5) that points at its source.
   So `feel the draft`, `smell the smoke` and `listen` address the room's own states and lead to what
   makes them, and every room has them because every room has air, light and things in it — no per-room
   hand-authoring and no special primitive. The loops still census each room's elusives, since that is
   what a room *is*. Option (c), "defer", was a cut dressed as ordering and is struck.

   *(The original, kept as the record:)* **The "elusive" sensory layer has no generic mechanism.** Property 5 and every census's own
   "elusive" section name cold, draft, sound, smell, light, and time as things a person would sense
   and try to act on; none are addressable objects anywhere in `objects.py` or `appearance.py`.
   *Options:* (a) a generic sense-noun primitive in the ontology that every room inherits; (b)
   hand-author sensory nouns per room as ordinary content rows; (c) defer until a dedicated pass.
   *Recommendation then:* (a), proven on one room first — it is the single build that unblocks all nine
   censuses' elusive sections at once, and matches the outdoor rule's preference for systems over
   per-room authoring.

~~6. asked:~~ **Answered 2026-09-27 (Andrew):** *"bear can kill, poison should make them really sick but not kill we dont want to just kill a character off because they ate a mushroom - they can die from blood loss, the bear, the cold, other things make them weak and sick"* *The question as it was asked:* **How dangerous is a fire inside the plane allowed to be?** *(New, Claude, 2026-09-26 — raised by
   §4.8; the numbers will belong to the heat-system design.)* Reality is plain: a fire in an enclosed
   space makes carbon monoxide, which has no smell and kills sleepers; burning seat foam adds cyanide
   to the smoke; the warnings a real person gets are a headache, dizziness, nausea, confusion, and a
   fire that burns poorly for want of air. Andrew's standing rule is that lethal places injure, never
   kill outright, with a seeded roll announced (2026-09-17) — and a gas that kills in the night is
   exactly the unannounced death that rule was written against. What he is deciding is how that rule
   meets an invisible hazard the party creates themselves. *Options:* (a) fully real — carbon monoxide
   accumulates by the physics and can kill sleepers who closed every opening; (b) real harm, bounded by
   the rule — it builds by the physics and injures (headache, nausea, confusion, collapse, a lost
   night), its symptoms and the choking fire are the telegraph, and whoever is awake on watch
   (document 06) notices; it kills only someone who stays in it after it has spoken; (c) no carbon
   monoxide. **Recommendation: (b)** — every real distinction stays (open an opening, bank the fire,
   put someone on watch), the danger is honest, and the death it can cause is one the party walked
   into with warnings, which is what the lethal-places rule protects.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18:** the distinguishable-names rule added as an authoring requirement for the loops.

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-checked against block 1, the October season and
  Andrew's 2026-09-26 decision that the plane is an entity with openings and an internal heat.
  **Design text:** that decision recorded in §2; §4.8 added — rooms are entities with the full schema
  plus air, light and ground; the plane as one entity whose parts include every opening (area and
  state) and whose cockpit, mid cabin and rear cabin share one air volume and one internal heat; the
  physics of that heat in first figures (bodies, candle, fire in; aluminium skin and openings out; the
  air holds almost nothing), the price of a fire inside, and a zone outdoors as an entity with residual
  heat in the ground and stones. §4.5 gains October's changing ground; the pilot's breathing (§4.1) and
  the censuses' overhead bins (§4.6) marked superseded. **Answered for Andrew's check:** Q1 (rule 9
  already says render and read; the voice is his), Q2 (groups replace masses; three-form phrases,
  glimpses and look-under are perception or physical acts, not hints), Q4 (`look under` is the `under`
  relation, with `feel under`/`reach under` and `look behind` as their own operations), Q5 (the room
  entity's states plus `sensed` and `class: elusive`; "defer" struck). **Rewritten:** Q3 (the loops
  cannot start before finalization; the rules go into the world-builder scaffold). **New for Andrew:**
  Q6 (how dangerous carbon monoxide from a fire inside may be — recommended: real harm bounded by the
  lethal-places rule). **Needs a design document:** the heat system (room and plane heat, openings,
  heat between spaces, carbon monoxide).

- **2026-09-27 (Andrew):** Q6 — what kills: blood loss, the bear, the cold; *"other things make them weak and sick"* — carbon monoxide from a fire inside the plane is one of the other things.

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
- The nine census documents themselves: `docs/scenarios/whiteout/rooms/*.md`.
- A probe corpus over the censuses: `game/world/scenarios/whiteout/probes/census.py` (97 lines,
  mixed `pass`/`todo` status per candidate command); the coverage floor at
  `game/world/scenarios/whiteout/probes/BASELINE`.

**Designed, not built**
- The fifty outdoor zones for the whole valley: designed as docs only —
  `docs/investigation/world/map.md`, `rooms.md`, `objects.md`, `report.md`, `build-queue.md` (a
  2026-07-15 overnight design run covering the full valley, exposure bands, and travel pricing).
  `zones.py` carries exactly the nine crash-cluster zones above and nothing else; none of this is in
  code.
- `look under` (open question 4) — the seat-row exemplar's own reveal verb — unbuilt: no handler,
  operation, or probe anywhere references it.
- The "elusive" sensory-noun layer (property 5, open question 5) — none of the nine censuses'
  elusive entities (cold, draft, smell, sound, light, darkness, time) exist as addressable objects;
  nothing in `objects.py` or `appearance.py` represents them.
- A generic class-that-yields-individuals primitive (property 1's "let classes yield individuals," e.g.
  "take a branch from the deadfall") — not built as a mechanism; today's deadfall is two authored
  instances that merely display as an aggregate (above), not an unbounded source a player can keep
  drawing from.
- The four-seat interior recast (§4.3) — see **16 — Players and kit** §8 for the full gap: the seat
  objects in `objects.py` are still the six-seat draft's `11B`/`12C`, not `1A`/`1B`/`2A`/`2B`/the
  right seat.
- Rooms and the plane as entities (§4.8; *Claude, 2026-09-26*) — nothing in code: a zone in
  `zones.py` carries position, terrain tags, adjacency and a survey line, with no states, parts or
  heat; the plane is not an entity, and its openings are not parts with states.

**Nothing**
- The room-authoring rules promoted into a guide: `docs/guides/authoring-objects.md` does not yet
  mention individuation, state persistence, or the style guide — this document's rules stand only
  here until reviewed and promoted (open question 3).
