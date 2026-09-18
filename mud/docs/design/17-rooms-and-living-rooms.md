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
3. **Processes visible**: the fire's stage, the cold's band, the light failing, the pilot's breathing
   — the room changes while you stand in it.
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

**These depend on it:**
- **22 — The world-building loops** — the room-authoring rules this document proposes (§4.1, §4.4,
  §4.5) are meant to promote into `docs/guides/authoring-objects.md` and govern how the fifty
  outdoor zones get authored (open question 3).
- **02 — The experience** — a sample week reads as prose only if the rooms it moves through hold to
  this style.
- **15 — Moral and social layer** — property 4 (other people's traces) is part of how a co-player's
  action becomes something a third party can witness.

---

## 6. Open questions

1. **The prose voice needs a render read, not a text approval.** `living-rooms.md`'s own rule 9 is
   "read it" — render every scene and read the zone whole before committing — and `presentation.md`
   §4 leaves Voice open for Andrew to rewrite freely. *Options:* (a) sign off on the style guide from
   this document's text alone; (b) render the nine crash rooms and read them together at the review
   sitting before signing off. **Recommendation: (b)** — a style guide is a hypothesis about prose
   until it is read.
2. **Which presentation leftovers survive?** Masses (identical objects aggregating into one
   sentence), three-form phrases, glimpse lines, and look-under are all named across the sources,
   but the provenance audit records several removals elsewhere (the verb-list redirect, the sibling
   near-miss hint) on grounds that would apply here too if any of these turn out to hint at a
   solution. *Options:* (a) treat all four as still-live conventions until told otherwise; (b) audit
   each one explicitly at this sitting. **Recommendation: (b)** — a five-minute check against the
   same "does this give something away" question the removals used, done once, in this review.
3. **The room-authoring rules for the loops.** `living-rooms.md`'s banner says this promotes into
   `docs/guides/authoring-objects.md` "on approval"; nothing has been added there yet.
   *Options:* (a) let the fifty-outdoor-zone loops start from this document's rules now, behind the
   existing content seams, and promote the guide afterward; (b) wait for the promotion before any
   loop authors a new room. **Recommendation: (a)** — the promotion is a paperwork step, not a gate
   on content; the rules are already specific enough to build from.
4. **`look under` is still unbuilt.** The seat-row exemplar (§4.3) names it as the reveal verb for
   seats, but no operation, handler, or probe anywhere in the codebase implements or even tests for
   it. *Options:* (a) build it before any of the fifty outdoor zones start populating landmarks,
   since this document's own exemplar depends on it; (b) leave seats reachable only through `search`
   and `cut`/`pry` until a later pass. **Recommendation: (a)** — the exemplar this document points
   to for "how a room is living" cannot fully demonstrate its own point without it.
5. **The "elusive" sensory layer has no generic mechanism.** Property 5 and every census's own
   "elusive" section name cold, draft, sound, smell, light, and time as things a person would sense
   and try to act on; none are addressable objects anywhere in `objects.py` or `appearance.py`.
   *Options:* (a) a generic sense-noun primitive in the ontology that every room inherits; (b)
   hand-author sensory nouns per room as ordinary content rows; (c) defer until a dedicated pass.
   **Recommendation: (a)**, proven on one room first — it is the single build that unblocks all nine
   censuses' elusive sections at once, and matches the outdoor rule's preference for systems over
   per-room authoring.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18:** the distinguishable-names rule added as an authoring requirement for the loops.

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

**Nothing**
- The room-authoring rules promoted into a guide: `docs/guides/authoring-objects.md` does not yet
  mention individuation, state persistence, or the style guide — this document's rules stand only
  here until reviewed and promoted (open question 3).
