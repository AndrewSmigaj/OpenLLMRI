# 03 — The player view: the look, descriptions composed from state, arrival and events

> **Status: reviewed with Andrew 2026-09-17**
> **Architecture counterpart:** [`../architecture/presentation.md`](../architecture/presentation.md)
> — v1, implemented. It differs from this document on two points: v1 keeps the room description
> static and prints a numbered disambiguation menu. A v2 of that document is pending and is to be
> written *from* this one.

---

## 2. Decisions

### Andrew's decisions

- **The look (2026-09-16, 2026-09-17).** A title line naming where you are — the marker of where you
  are; a paragraph of prose composed from state; the people and animals present, as prose, by what
  they are doing (standing or sitting when idle); then the exits, as prose. No item list, no hidden
  tags on screen. Exits are named by compass direction outdoors and fore / aft / out inside the plane.
- **(2026-09-28)** Between Scenes, a person who stops walking is *"between the birch grove and the
  plane"*, with whatever is near them and no room description beyond that; a journey gives an estimate
  of how long it will take (document 19 §4.3).
- **(2026-09-28)** A person can approach a thing and be next to it — `sit next to the fire` — and the
  room's prose says so ("Cal sits close by the fire"); the position is real (document 17 §4.8).
- **(2026-10-02)** **Moving is ontologically sufficient.** Any reasonable way of saying it that follows
  the grammar works: the directions and their synonyms, up and down, `go to` or `walk to` a place
  (`walk to the grove`), and the exit's own verb — `climb the tree` leads to a separate place up the
  tree, `climb onto the plane` to the top of the fuselage.
- **(2026-09-28)** A serious condition shows in a person's line in the room; the body's signs (a
  cough, a wince, shivering) arrive as emotes; examining or looking at the person reveals the smaller
  things (§4.1, §4.7; document 11 §4.12).
  People are coloured slightly differently, and colour is for human players only.
- **Descriptions are composed from state (2026-09-16)**, with the four composer extensions of §4.4,
  which Andrew walked against the shipped renderer and approved as the way to get there.
- **The same view for humans and agents (2026-09-16).** An agent sees exactly what a human sees;
  per-step structure goes to the log only. There is no agent-shaped observation block, no structured
  sidecar on screen, no tag rendering for machine readers. Whatever the research log wants, it takes
  from the log.
- **Never a menu (2026-09-16).** The player — person or agent — is never given a set of options:
  options change how an agent thinks and constrain it to those options, and listing, say, every can
  in reach would give away the puzzles. The only question the game asks is which thing is meant when
  a name is ambiguous (two cans in a scene: `Which can do you mean?`). There are no numbered nouns.
  So the look never lists the things in the room, and a tie asks `Which can do you mean?` and prints
  nothing more.
- **The tell/hide rule (2026-07; DR-24; 2026-09-28).** Scenes read as scenes, not manifests. What is
  inside a closed or unsearched thing is honestly absent from the prose, from the parser's pool and
  from reach until `open` / `search` / `dig` earns it. No hidden flags — the hiding is physical. No rule
  puts useful things inside others: where each thing lies is decided case by case, for the game.
- **The unified renderer (2026-07-02).** Bare `look` **is** the room survey — there is no separate
  "look around" verb. `look at X` / `look X` ≡ `examine X`: one detailed description, one renderer,
  identical output on both paths.
- **The v1 defaults (2026-07-03, approving DR-23).** Three salience tiers; identical derived objects
  aggregate at two or more; no authored hiding (DR-24 then made the hiding physical); moderate
  property hints in examine; frames as a small per-room set rather than authored per room.
- **Exits are entities (2026-09-17).** Each exit has its own name, synonyms, verb and sentence in the
  prose; the tutorial gives a brief guide and an example of the movement forms (§4.1a).
- **Groups (2026-09-17).** Several things of one kind in one place form a described group; this is
  also how a crowded zone keeps its paragraph short (§4.1b).
- **Events (2026-09-17).** A blank line comes before an event, so a player who is mid-activity
  notices it.
- **Frames and survey lines (2026-09-17).** A space's frame may have state variants — describing the
  condition of the place, never the history of the things in it; a zone's survey line changes only
  through a small authored set of variants (§4.2, §4.4).
- **Examine and search (2026-09-17).** `examine` reveals features you would not otherwise see;
  `search` goes through a container — the ones it makes sense to search.
- **The tutorial (2026-09-27)** is a series of rooms, each one simple situation that shows what sort
  of things players can do; nothing else is explained.

### Proposals (Claude)

- The space model itself — frames, anchors, caps, absorption, the drop picker (built and shipped
  2026-07-15, never reviewed line by line with Andrew).
- Spaces replacing the salience tiers inside a zone — the tiers are now vestigial there (§8) and
  survive only to grade what is visible in an *adjacent* zone.
- The cap of **3** items per space before the overflow phrase, the survey order of spaces, and every
  authored frame in `spaces.py`.
- The generic form-keyed prose for minted things, and the aggregate phrasing itself.
- Every phrase quoted in §4.5 as "after" text that is not already in `appearance.py` today.
- The rendering order inside the block (the survey sentence before the scene prose) and the
  direction-framed lines for people in adjacent zones.
- Events printing as single lines, and their line shapes.
- The mechanism for exits and groups (§4.1a, §4.1b).

---

## 3. In one paragraph

You type `look` and get a line naming where you are, a short paragraph of prose, who is with you and
what they are doing, and where the world goes on from here — and nothing else. The paragraph is not
authored per room — it is *built* every time from what is actually there: the zone's survey
sentence, then each area of the room in turn (the footwell, the overhead, the aisle), each naming
what rests in it in a sentence written for that position. Nothing is listed. Nothing is tagged. If
you take the duffel out of the aisle, the aisle stops being mentioned; if you put it on the seat, it
becomes a clause on the seat's sentence; if you set it alight, both its own phrase and the room's
survey change, because smoke is a fact about the room now. Where several things of a kind lie
together, you read "a pile of clothes", and you have to look at the pile to see what is in it. What
is inside a closed thing is simply not in the text — you earn it by opening, searching or digging.
An agent playing reads exactly this, byte for byte, because a different view would be a different
world.

---

## 4. The design

### 4.1 The block

Every arrival and every `look` prints the same block, in this order:

```
The mid cabin                                          ← title line: where you are
Wrenched seats and spilled luggage crowd the narrow cabin.  ← the zone survey sentence
An aircraft seat — 1B stencilled on the frame — sits wrenched sideways on its bolts.
Luggage lies thrown across the floor.                   ← the composed scene (groups form)

Mara is going through the duffel; Cal sits against the hull.   ← people and animals, as prose
                                                         (coloured for human players)
Forward, the cockpit; aft, the rear cabin; the split hull opens onto the muskeg.
                                                         ← the exits, as prose (they are entities)
```

The description holds the things you can interact with; the people and animals sit between the
description and the exits, as prose by what they are doing, standing or sitting when idle. **A serious
condition shows in the person's line** (2026-09-28) — what anyone would see from across the room:
*Cal sits against the hull, his sleeve soaked dark with blood*; *Mara stands on one foot, pale and
shaking*. Smaller things wait for a closer look — `look at Mara`, `examine Mara` (document 11 §4.12).
**A hiding person is left out of the line** (2026-09-28) until someone looks where they are hiding or
a small sound gives them away; from then on they are in that person's line (document 15 §4.7).

What is **not** in it: no `You see:` list, no item inventory of the room, no counts-first phrasing,
no salience labels, no tags, no ident brackets, no per-step structure, no numbered anything. The
title line is the only structural line the player reads; everything else, the exits included, is
prose.

**The exits.** Below the people, each exit in prose — its own sentence or clause, composed from its
state like any other thing (§4.1a). Outdoors they are named by compass direction; inside the plane,
fore / aft / out, and `up` / `down` wherever a place really is above or below. Every direction has its
synonyms, and moving is ontologically sufficient (2026-10-02): `go to` or `walk to` a place, or the
exit's own verb — `climb the tree` leads to a separate place up the tree, `climb onto the plane` to the
top of the fuselage. Exits are geography, not affordances, so naming them is not
a menu: the prose says where the world continues, never what to do. The commands are `go <direction>`,
`go to <place>`, and the exit's own verb.

**Why a title line at all.** The zones of the crash site live inside one Evennia room, so moving
from the cockpit to the mid cabin changes no room header on its own. The title line is the marker
that you moved.

### 4.1a Exits are entities (Andrew, 2026-09-17)

An exit is a thing in the world with a name, synonyms, a direction, a mode and a state, and its own
sentence in the room's prose ("a trail leads north into the spruce"; "the scar climbs east toward the
ridge under a skin of new snow"). You act on it with the verb its mode calls for: `walk west`,
`walk to the birch grove`, `run to the treeline` (less time, more sweat), `climb up` the rock face, `enter the tail`,
`turn back` mid-way. Moving is an attended activity with feedback and events (something passes; a hare
bolts; the bear's fresh sign); its time is distance over pace, times terrain, snow depth, load and fitness, so weather
lengthens it and early exploration is rewarded. The tutorial gives a brief guide and an example of
these forms; the game never lists them. *(Proposal for the mechanism: an exit row carries `mode`,
`travel_time`, `state`; its sentence composes from state like every other thing.)*

### 4.1b Groups (Andrew, 2026-09-17)

When more than one thing shares a place and a kind, a group forms with its own descriptor — "a pile of
clothes", "luggage thrown across the floor" — and the room shows the group, not the members.
`look at the pile` lists what is in it (uncapped); taking things apart dissolves it. Groups are
relations with descriptors, like containers that form on their own. This is how a crowded room stays
readable without ever listing what is reachable: you have to look. It is also what keeps a crowded
zone's paragraph short — the room names a few groups rather than many things. *(Proposal: groups form
by place + kind with an authored descriptor per kind; the composer's cap/overflow phrases become named
groups.)*

### 4.2 Composed from state — the pipeline

Nothing in the block is a hand-written variant of a whole room, and no room owns a state machine.
On every look the composer runs:

1. **The zone survey sentence** — authored, selected by zone state (extension 3).
2. **The spaces of that zone, in survey order** — each space's authored frame, filled with the
   phrases of the things resting in it. An **empty space renders nothing**.
3. **Each visible thing's phrase** — the authored state-keyed variant if it has one; otherwise a
   generic phrase keyed by material × form, with a state overlay (extension 2).
4. **Relation clauses** — a thing that is *on* / *under* / *against* / *inside (when open)* another
   thing does not get its own sentence; its phrase hangs as a clause on the parent's (extension 1).
5. **People and animals** — those here, by what they are doing; then those visible in adjacent zones,
   direction-framed.
6. **The exits**, in prose.

Three rules keep this honest as players move things around (the prose style guide, document 17
§4.4):

- **A frame describes POSITION, never HISTORY.** "Lying in the aisle" stays true forever; "spilled
  down the aisle" becomes a lie the moment a player drops a can opener there. The *zone's* survey
  line carries the history, and it can, because the zone is authored and never mutates.
  A frame may have **state variants** that describe the *condition of the place* — "across the
  smoke-blackened floor…" — but never the history of the things in it (Andrew, 2026-09-17).
- **An object's phrase carries its own character.** "a duffel bag, burst half-open" is about the
  duffel and stays true wherever the duffel goes.
- **Absorption is deferral, not deletion.** A space names at most `cap` things (proposed default 3)
  and folds the rest into an overflow phrase — *"and a scatter of smaller debris"* — which is itself
  an alias of the space, so `look at debris` and `look at floor` both render the space uncapped.
  Nothing is invented and nothing disappears.

### 4.3 The tell/hide rule (DR-24)

One rule decides whether a thing is in the text at all: **an object's contents enter the prose, the
parser's pool and reach if and only if the object is `open` or `searched`** (or the child is worn by
the parent — a worn jacket is the visible layer). Recursive through revealed containers only:
opening the bin shows the duffel; the duffel's insides wait for their own search. Discovery is
deterministic — search and dig find exactly what is physically there, never a roll. Searching is an
activity (2026-09-28): it goes through a body, a pile, a container or the wreckage a pocket, a
compartment or a layer at a time, a line for each find, and it can be stopped with what was searched
kept; searching a bag turns up the clothes in it, and each garment's pockets are searched in turn; a search aimed at one place (`search the pilot's pockets`) goes straight there (document 06).

This is what lets the look be short and still fair. The scene shows what a person would see from the
doorway; what is inside things waits for opening or searching. Where each thing lies is decided case
by case, for the game (2026-09-28).

### 4.4 The four composer extensions

These are the four Andrew walked on 2026-09-16. Nothing about them is built (§8); all four sit
behind seams that already exist.

| # | extension | what it does |
|---|---|---|
| 1 | **Relations rendered on the parent** | `on` / `under` / `against` / `inside (when open)` as containment modes. The child renders as a clause on the parent's sentence — *"…, a duffel bag dumped on it"* — not as its own sentence in the space's frame. |
| 2 | **Generic state overlays** | A table keyed by material × form × state (searched, open, wet, frozen, burning, burnt, half-sawn, dug…) that modifies any thing's phrase, authored or minted. Authored phrases stay for the places where the voice earns it. |
| 3 | **Zone and space state variants** | The `(condition, phrase)` mechanism objects already use, now driven by *zone facts* written by Effects: smoke, light, a fire present, a breach blocked, snow depth. A zone's survey line has **a small authored set of variants** — dark, lit, smoke, falling snow — rather than clauses composed freely onto it, so the voice holds and the opening line stays recognisable (Andrew, 2026-09-17). |
| 4 | **Range conditions in the phrase matcher** | The matcher today is an equality-subset test; ranges let a phrase key on `snow_depth >= 5` or `temperature_c <= -10` instead of an exact value. |

**What each needs (verified at source, 2026-09-16 — this raises the design's certainty; it is not a
substitute for the certainty audit that precedes implementation).**

- **(1)** touches containment and reach, so it is the one that gets a full audit first. `resolve_put`
  (`game/world/sim/operations/handlers/take.py`) redirects unless the destination is a container;
  `TRANSFER` (`apply.py`) already relocates into any object; the worldview marshals `state["in"]`;
  `Room.get_display_things` gathers direct children only. So "on" needs a surface property (authored,
  or derived from form and size), `rel: "on"` on the child, the parser pool walk and the room's
  things-gathering to include the `on`-children of visible things, and `_render_space` to attach the
  child's phrase as a clause. All additive.
- **(2)** `_entry` already falls through to form-keyed generics; an overlay table keyed by state flags
  slots in after `_pick`.
- **(3)** `SET_ATTR` targets a real entity, and zone pseudo-entities are synthesized on the fly, so
  zone facts need a home: `room.db.zone_state[zone]`, written by an additive `SET_ZONE_ATTR` effect
  (a contract change, additive, with a change note), marshalled into the zone entity's state and read
  by the survey selector. The zone's `look` becomes a variants list like any object's.
- **(4)** a two-line extension to `_pick`.

**Discipline.** The walked scenarios below become `todo` probes *with their expected rendered text*
before the composer is touched — they fail first. A Mode-A certainty audit of extension (1) precedes
the implementation brief.

**A knock-on to expect.** The probe runner defaults a mid-chain ambiguity to the first option, and no
probe names a pick. When the numbered menu becomes a bare clarification (DR-08c), any probe that
silently relied on that default fails and has to be re-authored with an unambiguous noun. How many is
only knowable by running.

### 4.5 The worked examples

The baseline for all six is the mid cabin as it renders today (`make render-scenes`). Today's built content is
still the old airliner cabin — overhead bins, oxygen masks, seat rows and an aisle — and labels the
seats with airliner rows (11B, 12C); the design is the 206 interior, with no overhead bins, and these
examples are redone when that content is re-authored; the 206's seats are 1A, 1B, 2A, 2B and the right seat
(document 16), and the labels change when that content is re-authored.

> **The mid cabin**
> Buckled seat rows and spilled luggage crowd the aisle.
> An aircraft seat — 11B stencilled on the frame — sits wrenched sideways on its bolts. Overhead are
> the latched forward overhead bin and oxygen masks swaying from a sprung panel. Lying in the aisle
> is a duffel bag burst half-open.

**1. `take duffel` — works today.** The aisle is now empty, and an empty space renders nothing. The
whole line goes; no "nothing here", no hole in the prose.

> …Overhead are the latched forward overhead bin and oxygen masks swaying from a sprung panel.

**2. `put duffel on seat` — needs (1).** Today the duffel either stays in its home space or is
refused, because the seat is not a container. With relations on the parent, it becomes a clause:

> An aircraft seat — 11B stencilled on the frame — sits wrenched sideways on its bolts, a duffel bag
> dumped on it.

**3. `search duffel` — needs (2).** The search is what reveals the contents (DR-24), and the duffel
itself should read as turned out from then on. The overlay supplies that without a new authored
variant per bag:

> Lying in the aisle is a duffel bag burst half-open, its contents turned out across the floor.

…and what was inside now has phrases of its own in the aisle.

**4. `cut cover off seat` — the authored variant works today; (1) carries the freed cloth.** The
seat's own state-keyed variant is already in `appearance.py` and fires:

> Seat 11B stands half-stripped, bared clips showing where its cushion was hacked out.

The freed fabric is a minted thing with a form; it lands in the aisle (or, with (1), as a clause on
whatever it was dropped onto).

**5. `light duffel` — needs (2) and (3).** Two things change at once, which is the whole point of
(3): the duffel's phrase, and the *room*, because a fire is a fact about the room.

> **The mid cabin**
> Smoke rolls along the ceiling and the light is orange and moving.
> An aircraft seat — 11B stencilled on the frame — sits wrenched sideways on its bolts. Overhead are
> the latched forward overhead bin and oxygen masks swaying from a sprung panel. Lying in the aisle
> is a duffel bag well alight, flame licking up its open seam.

**6. `dig dirt` / `chop log` outdoors — spaces, minted forms and aggregation, with (2) and (3).**
Outdoors the same machinery does the natural world: the ground is a space, digging mints spoil and a
hole (state on the space), chopping mints pieces that aggregate rather than list.

> Across the trampled snow are a spruce log, half through, and three split billets.

…and the dug ground reads as dug, via the same state overlay, with the snow depth keyed through a
range condition (4).

### 4.6 The thing renderer — `look at X` ≡ `examine X`

One renderer, two entry points, identical output (Andrew, 2026-07-02). It prints: the authored
state-conditioned prose; the systemic condition woven as a clause, never as data (`It's alight,
soaked.` — never `(foam, clipped)`); revealed contents when open or searched; parts as physical
sentences with their names intact, so the player learns what to type, and attachments as phrases.
`examine` reveals the features you would not see from a glance at the room (Andrew, 2026-09-17).
No ident brackets (2026-10-03): the seat's label is in the prose ("1B stencilled on the frame"), and the player
can say it — `examine 1B`.

Property hints, not affordance lists: at most a couple of sensory cues ("the fabric is thin; the foam
beneath is dense and dry"). Naming a verb or a use here would be a menu — players know what a sharp
thing can do (2026-09-28). Where players really struggle, a hint is added case by case (document 04).

`search` goes through a container — the ones it makes sense to search — and is what reveals their
contents (§4.3).

`look at <space>` renders that space uncapped — every loose thing in it, no overflow. Spaces are
look-at-able but never take-able or open-able.

### 4.7 Arrival and events

- **Arrival prints the block.** Moving into a zone re-prints the whole look (MUD convention), and
  that is what makes the title line a marker. This is shipped behaviour (`game/commands/cmd_act.py`,
  the `MOVE_ZONE` branch).
- **The body's own signs arrive as emotes** (2026-09-28): a cough, a wince, teeth chattering, a limp as
  someone moves — single event lines now and then, not every tick, routed by distance like any other
  (document 11 §4.12).
- **Events print as single lines** *(Claude's)*, **after a blank line** (Andrew, 2026-09-17): one line,
  in the same voice as the prose, no block, no header; colour, where it is used, is for human players
  only, since it does not survive an agent's transcript. What another person's action looks like to
  you is graded by distance and loudness and is routed per observer — a full third-person line here,
  a direction-framed line from the next zone ("To the south, Mara is moving about."), a shape or a
  sound further out, nothing beyond. The actor never sees the propagated line; they already got their
  own narration.
- **The clock's own events** (weather turning, a fire dying, someone worsening) interrupt a pending
  activity and print the same way. What exactly each one says is document
  [`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md)'s to decide; that it
  is one line, in prose, with no structure, is this document's rule.

---

## 5. Interactions

**This depends on:**

- [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) — the spaces, frames and authored
  voice this composes; the crash rooms.
- [`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md) — forms and materials, which is
  what the generic phrases and state overlays key on. A minted thing has no prose unless the form is
  in the table.
- [`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md) and
  [`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md) — the zone facts that
  extension (3) renders (smoke, light, snow, weather) are written by those systems' Effects.
- [`19-multiplayer-and-instances.md`](19-multiplayer-and-instances.md) — the perception bands that
  decide who and what you can see from an adjacent zone
  ([`../architecture/perception-model.md`](../architecture/perception-model.md)).

**Depends on this:**

- [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) — the look is what teaches the nouns.
  Anything it names must parse, and a player can also name what a real place would hold (document 05
  §4.1). The clarification-only rule and this document's "no list" rule are the same rule seen twice.
- [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) — the agent's entire
  observation is this block; the structured per-step record goes to the log.
- [`07-fire-and-shaping.md`](07-fire-and-shaping.md), [`09-water.md`](09-water.md),
  [`18-materials-and-forms.md`](18-materials-and-forms.md) — every minted output needs a phrase, or
  the world grows things nobody can see.
- [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) — "witnessed" means the propagated
  line reached another player; what the witness reads is decided here.

---

## 6. Open questions

None open. Everything this document asked was settled on 2026-09-17 and is written into §4.

---

## 7. Review log

- **2026-09-16** — the description-model walk-through with Andrew: the look, descriptions composed
  from state, the four composer extensions, the same view for agents, no item list and no numbered
  menu.
- **2026-09-17** — reviewed with Andrew: exits as entities, in prose below the description, with a
  guide and an example in the tutorial; people and animals as prose by what they are doing, coloured
  for human players; a blank line before events, colour for humans only; state variants on frames; a
  small authored set of survey variants per zone; groups, which also keep a crowded zone's paragraph
  short; what `examine` and `search` reveal.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

---

## 8. What exists today

**Built.**

- The composer: `game/world/sim/presentation.py` — `compose_scene` groups a zone's entities into
  spaces and renders each space's frame in survey order, omitting empty spaces, with serial-`and`
  joining, number agreement (`{be}`), per-space caps and overflow phrases; `look_space` renders a
  named space uncapped; `describe` is the one renderer for `look at X` / `examine X`, weaving the
  condition flags and the parts; `_entry` falls back from sim-id to display name to a form-keyed
  generic.
- The space and zone tables: `game/world/scenarios/whiteout/spaces.py` (the plane and its immediate
  outside — frames, aliases, caps, overflow), `game/world/scenarios/whiteout/zones.py` (positions,
  `walk` / `see` edges, the authored survey line per zone), `game/world/sim/space/`.
- The appearance table: `game/world/scenarios/whiteout/appearance.py` — per-object `scene` and
  `examine` variant lists, `space` homes, anchors, ordering, aggregates. State-keyed variants work
  today (seat 11B's stripped variant is in there and fires).
- Containment and the tell/hide rule: `game/world/sim/` + the worldview marshalling described in
  [`../architecture/containment.md`](../architecture/containment.md); contents stay out of the prose,
  the pool and reach until `open` / `search` / `dig`.
- Arrival re-printing the look: `game/commands/cmd_act.py` (the `MOVE_ZONE` branch).
- Per-observer event lines graded by perception band and loudness:
  `game/typeclasses/propagator.py`.
- The shell seams: `Room.get_display_things` / `get_display_desc` / `get_display_characters` in
  `game/typeclasses/rooms.py`.
- The rendered-prose review artifact: `make render-scenes` writes it to `docs/review/`.

**Designed, not built.**

- The title line, people and animals as prose, and the exits as entities in prose. The zone edges
  already know `walk` and `see`, so the exits have their data; nothing renders them this way.
- Groups.
- All four composer extensions. Relations-on-the-parent, state overlays, zone/space state variants
  and range conditions are **nothing** in code today.
- The walked scenarios as `todo` probes with expected text — not yet written.

**Built, but not matching the design.**

- The numbered disambiguation menu still ships (`game/commands/cmd_act.py`,
  `game/commands/cmd_items.py` print `Which X do you mean?` followed by a numbered list). DR-08c
  retires it; the removal lands with `presentation.md` v2.
- Bare `go` still orients by naming where you can walk
  (`game/world/sim/operations/handlers/move.py`) — a list of options, which the exits in prose make
  redundant and DR-08c retires.
- DR-23's three salience tiers are vestigial inside a zone: `_render_space` orders by `anchor` and
  `order`, and `salience` is now read only when grading what is visible in an *adjacent* zone.
  `appearance.py` still carries a `salience` on nearly every row.
- `presentation.md` v1 still states that the room description stays static and describes the
  numbered menu; this document differs on both.
