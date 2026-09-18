# 03 — The player view: the look, descriptions composed from state, arrival and events

> **Status: reviewed with Andrew 2026-09-17**
> **Architecture counterpart:** [`../architecture/presentation.md`](../architecture/presentation.md)
> — v1, implemented, and **superseded on two points** by Andrew's 2026-09-16 walk-through: its
> "object phrases only (the room desc stays static in v1)" default and its numbered disambiguation
> menu. A v2 of that document is pending and should be written *from* this one.
> **Sources.** The description-model walk-through with Andrew, 2026-09-16 (recorded in the session
> plan, "Part J — the description model", with the code facts verified at source the same day) ·
> [`../architecture/presentation.md`](../architecture/presentation.md) (v1, DR-23) ·
> [`../investigation/scene-spaces.md`](../investigation/scene-spaces.md) §1–§3, §5 (the space model)
> · [`../architecture/containment.md`](../architecture/containment.md) (DR-24, the tell/hide rule) ·
> [`../review/render-2026-09-07.md`](../review/render-2026-09-07.md) (what the looks read like
> today) · [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md)
> §2 (DR-23, DR-24, DR-08c) · code: `game/world/sim/presentation.py`,
> `game/typeclasses/rooms.py`, `game/typeclasses/propagator.py`,
> `game/world/scenarios/whiteout/{appearance,spaces,zones}.py`.

---

## 2. Provenance

### Andrew's decisions

**The look (2026-09-16, the walk-through).** *"The look: a title line (`The mid cabin`), the prose,
who is here, one `Exits:` line; compass outdoors, fore/aft/out inside; no item list, no hidden tags
on screen."* The room-name line is the marker of where you are. *"Descriptions are composed from
state, with the four composer extensions."*

**The same view for humans and agents (2026-09-16).** *"An agent sees exactly what a human sees;
per-step structure goes to the log only."* There is no agent-shaped observation block, no structured
sidecar on screen, no tag rendering for machine readers. Whatever the research log wants, it takes
from the log.

**Never a menu (2026-09-16).** *"The agent is not given a set of options to choose."* *"Giving
options changes how it thinks, it constrains it to those options."* *"If you give options for like
'pick up can' and then you list all the cans in the reachable area it would just give away all the
puzzles."* *"The only time you ask the user anything is if what object or action they can do is
ambiguous (two cans in a scene it will ask 'which can do you mean?')."* *"No you do not have numbered
nouns."* The consequence for this document: the look never lists the things in the room, and a tie
asks `Which can do you mean?` and prints nothing more.

**The tell/hide rule (2026-07, Andrew's directive; DR-24).** Scenes read as scenes, not manifests.
Load-bearing things live *inside* things and are honestly absent from the prose, from the parser's
pool and from reach until `open` / `search` / `dig` earns them. No hidden flags — the hiding is
physical.

**The unified renderer (2026-07-02).** Bare `look` **is** the room survey — there is no separate
"look around" verb. `look at X` / `look X` ≡ `examine X`: one detailed description, one renderer,
identical output on both paths.

**The v1 defaults (2026-07-03).** Approving DR-23, Andrew took the recommended answers: **three
salience tiers**, **identical derived objects aggregate at ≥2**, **no authored hiding** (deferred to
the perception work — DR-24 then made the hiding physical), **moderate property hints in examine**,
and **frames as a small per-room set** rather than authored per room. The space model (below)
superseded the first of these inside a zone; the rest stand.

**The four composer extensions (walked with Andrew, 2026-09-16)** — listed in §4.4 below; the
scenarios he walked are §4.5. He walked each of them against the shipped renderer and approved the
four extensions as the way to get the rest.

### Proposals (Claude)

Everything below that is not quoted above:

- The space model itself — frames, anchors, caps, absorption, the drop picker
  ([`../investigation/scene-spaces.md`](../investigation/scene-spaces.md), 2026-07-15; built and
  shipped, never reviewed line by line with Andrew).
- The cap of **3** items per space before the overflow phrase, the survey order of spaces, and every
  authored frame in `spaces.py`.
- Replacing the (Andrew-approved) salience tiers with spaces inside a zone — tiers are now vestigial
  there (see §8) and survive only to grade what is visible in an *adjacent* zone.
- The generic form-keyed prose for minted things, and the aggregate phrasing itself (the ≥2
  threshold is Andrew's).
- Every phrase quoted in §4.5 as "after" text that is not already in `appearance.py` today.
- The rendering order inside the block (survey sentence before the scene prose; who-is-here before
  exits), the `With you:` phrasing, and the direction-framed lines for people in adjacent zones.
- The event line shapes, and the proposal that events print as single lines.

---

## 3. In one paragraph

You type `look` and get four things and nothing else: a line naming where you are, a short paragraph
of prose, who is with you, and one line of exits. The paragraph is not authored per room — it is
*built* every time from what is actually there: the zone's survey sentence, then each area of the
room in turn (the footwell, the overhead, the aisle), each naming what rests in it in a sentence
written for that position. Nothing is listed. Nothing is tagged. If you take the duffel out of the
aisle, the aisle stops being mentioned; if you put it on the seat, it becomes a clause on the seat's
sentence; if you set it alight, both its own phrase and the room's survey change, because smoke is a
fact about the room now. What is inside a closed thing is simply not in the text — you earn it by
opening, searching or digging. An agent playing reads exactly this, byte for byte, because a
different view would be a different world.

---

## 4. The design

### 4.1 The block

Every arrival and every `look` prints the same block, in this order:

```
The mid cabin                                          ← title line: where you are
Buckled seat rows and spilled luggage crowd the aisle.  ← the zone survey sentence
An aircraft seat — 1B stencilled on the frame — sits wrenched sideways on its bolts.
Luggage lies thrown across the floor.                   ← the composed scene (groups form)

Mara is going through the duffel; Cal sits against the hull.   ← people and animals, as prose
                                                         (colored for human players)
Forward, the cockpit; aft, the rear cabin; the split hull opens onto the snow.
                                                         ← the exits, as prose (they are entities)
```

*(Andrew, 2026-09-17: exits are listed below the room as prose, not as an `Exits:` line; people and
animals sit between the description and the exits, as prose by what they are doing, standing or sitting
when idle, colored slightly differently for human players; the description holds the interactables.)*

What is **not** in it: no `You see:` list, no item inventory of the room, no counts-first phrasing,
no salience labels, no tags, no ident brackets, no per-step structure, no numbered anything. The
title line and the exits line are the only two structural lines the player reads; everything else is
prose.

**The exits line.** One line. Outdoors it is compass (`Exits: north, east, southwest`); inside the
plane it is `fore`, `aft`, `out` (Andrew, 2026-09-16). Exits are geography, not affordances, so
naming them is not a menu: the line says where the world continues, never what to do. The commands
are `go <direction>` and `go to <place>`.

**Why a title line at all.** The zones of the crash site live inside one Evennia room, so moving
from the cockpit to the mid cabin changes no room header on its own. The title line is the marker
that you moved.

### 4.2 

### 4.1a Exits are entities (Andrew, 2026-09-17)

An exit is a thing in the world with a name, synonyms, a direction, a mode and a state, and its own
sentence in the room's prose ("a trail leads north into the spruce"; "the scar climbs east toward the
ridge, drifted knee-deep"). You act on it with the verb its mode calls for: `walk west`, `walk to the
birch grove`, `run to the treeline` (less time, more sweat), `climb up` the rock face, `enter the tail`,
`turn back` mid-way. Moving is an attended activity with feedback and events (something passes; a wolf
tests you); its time is distance over pace, times terrain, snow depth, load and fitness, so weather
lengthens it and early exploration is rewarded. The first exit a player takes shows the forms once (the
tutorial), never a menu. *(Proposal for the mechanism: an exit row carries `mode`, `travel_time`,
`state`; its sentence composes from state like every other thing.)*

### 4.1b Groups (Andrew, 2026-09-17)

When more than one thing shares a place and a kind, a group forms with its own descriptor — "a pile of
clothes", "luggage thrown across the floor" — and the room shows the group, not the members.
`look at the pile` lists what is in it (uncapped); taking things apart dissolves it. Groups are
relations with descriptors, like containers that form on their own. This is how a crowded room stays
readable without ever listing what is reachable: you have to look. *(Proposal: groups form by place +
kind with an authored descriptor per kind; the composer's cap/overflow phrases become named groups.)*
Composed from state — the pipeline

Nothing in the block is a hand-written variant of a whole room, and no room owns a state machine.
On every look the composer runs:

1. **The zone survey sentence** — authored, selected by zone state (extension 3).
2. **The spaces of that zone, in survey order** — each space's authored frame, filled with the
   phrases of the things resting in it. An **empty space renders nothing**.
3. **Each visible thing's phrase** — the authored state-keyed variant if it has one; otherwise a
   generic phrase keyed by material × form, with a state overlay (extension 2).
4. **Relation clauses** — a thing that is *on* / *under* / *against* / *inside (when open)* another
   thing does not get its own sentence; its phrase hangs as a clause on the parent's (extension 1).
5. **People** — those here, then those visible in adjacent zones, direction-framed.
6. **The exits line.**

Three rules keep this honest as players move things around
([`../investigation/scene-spaces.md`](../investigation/scene-spaces.md) §1):

- **A frame describes POSITION, never HISTORY.** "Lying in the aisle" stays true forever; "spilled
  down the aisle" becomes a lie the moment a player drops a can opener there. The *zone's* survey
  line carries the history, and it can, because the zone is authored and never mutates.
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
deterministic — search and dig find exactly what is physically there, never a roll.

This is what lets the look be short and still fair. The scene shows the *flavour* — the things a
person would see from the doorway — and the load-bearing kit is inside things, earned.

### 4.4 The four composer extensions

These are the four Andrew walked on 2026-09-16. Nothing about them is built (§8); all four sit
behind seams that already exist.

| # | extension | what it does |
|---|---|---|
| 1 | **Relations rendered on the parent** | `on` / `under` / `against` / `inside (when open)` as containment modes. The child renders as a clause on the parent's sentence — *"…, a duffel bag dumped on it"* — not as its own sentence in the space's frame. |
| 2 | **Generic state overlays** | A table keyed by material × form × state (searched, open, wet, frozen, burning, burnt, half-sawn, dug…) that modifies any thing's phrase, authored or minted. Authored phrases stay for the places where the voice earns it. |
| 3 | **Zone and space state variants** | The `(condition, phrase)` mechanism objects already use, now driven by *zone facts* written by Effects: smoke, light, a fire present, a breach blocked, drift depth. **This supersedes v1's "the room desc stays static."** |
| 4 | **Range conditions in the phrase matcher** | The matcher today is an equality-subset test; ranges let a phrase key on `drift_depth > 40` or `temperature_c <= -20` instead of an exact value. |

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

The baseline for all six is the mid cabin as it renders today
([`../review/render-2026-09-07.md`](../review/render-2026-09-07.md)):

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

…and the dug ground reads as dug, via the same state overlay, with the drift depth keyed through a
range condition (4).

### 4.6 The thing renderer — `look at X` ≡ `examine X`

One renderer, two entry points, identical output (Andrew, 2026-07-02). It prints: the authored
state-conditioned prose; the systemic condition woven as a clause, never as data (`It's alight,
soaked.` — never `(foam, clipped)`); revealed contents when open or searched; parts as physical
sentences with their names intact, so the player learns what to type, and attachments as phrases.
Idents survive here (`aircraft seat [11B]`) because the grammar needs an addressable tag — that is a
tag the player can *say*, not a hidden marker on the scene.

Property hints, not affordance lists: at most a couple of sensory cues ("the fabric is thin; the foam
beneath is dense and dry"). Naming a verb here would be a menu.

`look at <space>` renders that space uncapped — every loose thing in it, no overflow. Spaces are
look-at-able but never take-able or open-able.

### 4.7 Arrival and events

- **Arrival prints the block.** Moving into a zone re-prints the whole look (MUD convention), and
  that is what makes the title line a marker. This is shipped behaviour (`game/commands/cmd_act.py`,
  the `MOVE_ZONE` branch).
- **Events print as single lines** (proposal): one line, in the same voice as the prose, no block, no
  header. What another person's action looks like to you is graded by distance and loudness and is
  routed per observer — a full third-person line here, a direction-framed line from the next zone
  ("To the south, Mara is moving about."), a shape or a sound further out, nothing beyond. The actor
  never sees the propagated line; they already got their own narration.
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
  extension (3) renders (smoke, light, drift, weather) are written by those systems' Effects.
- [`19-multiplayer-and-instances.md`](19-multiplayer-and-instances.md) — the perception bands that
  decide who and what you can see from an adjacent zone
  ([`../architecture/perception-model.md`](../architecture/perception-model.md)).

**Depends on this:**

- [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) — the look is what teaches the nouns.
  Anything the prose does not name is a noun the player has no reason to type; anything it names must
  parse. The clarification-only rule and this document's "no list" rule are the same rule seen twice.
- [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) — the agent's entire
  observation is this block; the structured per-step record goes to the log.
- [`07-fire-and-shaping.md`](07-fire-and-shaping.md), [`09-water.md`](09-water.md),
  [`18-materials-and-forms.md`](18-materials-and-forms.md) — every minted output needs a phrase, or
  the world grows things nobody can see.
- [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) — "witnessed" means the propagated
  line reached another player; what the witness reads is decided here.

---

## 6. Open questions

1. **Exit naming inside the plane.** Andrew decided `fore` / `aft` / `out`. The 206's interior is
   four seats and a cargo area, and the crash-site zones include `fuselage_top` and `outside_nose`,
   which are not on a fore/aft axis. Options: (a) `fore`/`aft`/`out` only, and anything else is
   reached by `go to <place>` without appearing on the exits line; (b) add `up` / `down` where a
   zone is genuinely above or below; (c) name the destination on the line (`Exits: fore (cockpit),
   out (the tail breach)`). **Recommendation: (b).** `up` for the fuselage top is physical, not a
   hint, and (c) starts to read like a menu.
2. **How people present are phrased.** Today it is `With you: Mara, Cal.` — a label and a list, the
   one list left in the block. Options: (a) keep it, on the grounds that people are not puzzle
   content and a survivor always knows who is next to them; (b) prose them like everything else
   ("Mara is here, working at the bin."), which costs a per-person activity phrase and risks leaking
   what they are doing; (c) prose for people who are doing something, the plain line otherwise.
   **Recommendation: (c)** — it reads as a scene and the activity is already public (the propagator
   sends it live anyway).
3. **How events print.** One line each is decided in shape but not in voice. Options: (a) plain
   sentences inline with everything else; (b) a leading marker for events that interrupt (a blank
   line, or `—`), so a player who is mid-activity notices; (c) a distinct colour. **Recommendation:
   (b) with a blank line** — colour does not survive an agent's transcript, and interruptions that go
   unnoticed are a real failure at 20×.
4. **What a space is allowed to say.** The position/history rule is clear; the grey area is *state*.
   May a frame say "Across the smoke-blackened floor…"? That is position-shaped but state-keyed, and
   with extension (3) it becomes possible. Options: (a) frames stay pure position, all state goes on
   the zone survey or the object phrases; (b) frames get state variants like everything else.
   **Recommendation: (b)**, with the rule kept: a frame variant may describe the *condition of the
   place*, never the *history of the things in it*.
5. **How much a zone's survey sentence may change.** Extension (3) makes the survey line
   state-keyed, which is exactly what "the room desc stays static" forbade. The risk is a room that
   reads differently every look and stops being recognisable. Options: (a) a small closed set of
   survey variants per zone (dark / lit / smoke / storm), authored; (b) free composition of clauses
   onto the base sentence. **Recommendation: (a)** — authored variants keep the voice, and the
   recognisable opening line is how a player knows where they are.
6. **Whether the composed paragraph needs a length budget.** Nine loose things in the cockpit already
   produce five sentences; the outdoor zones are being designed with far more. Options: (a) per-space
   caps only (today); (b) a whole-block budget that tightens the caps when the zone is crowded.
   **Recommendation: (b) eventually**, measured on the rendered zones rather than guessed now —
   record it as the first thing to check when the fifty outdoor zones render.

---

## 7. Review log

*(Nothing yet — this document has not been reviewed with Andrew.)*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-17 (Andrew, block 1):** Q1 — exits are entities, listed below the description as prose, each with
  its own name, synonyms and verb; a brief guide and example in the tutorial. Q2 — people and animals as
  prose above the exits and below the description, by what they are doing; colored for human players.
  Q3 — a blank line before interrupting events; color only for humans. Q4, Q5 — as recommended (state
  variants on frames; a small authored set of survey variants). Q6 — solved by granularity: groups.
  `examine` reveals features you would not otherwise see; `search` goes through a container (the
  appropriate ones only). §4.1 rewritten; §4.1a and §4.1b added.

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
- The rendered-prose review artifact: `make render-scenes` →
  [`../review/render-2026-09-07.md`](../review/render-2026-09-07.md).

**Designed, not built.**

- The title line and the `Exits:` line as specified here. The zone edges already know `walk` and
  `see`, so the line has its data; nothing renders it.
- All four composer extensions. Relations-on-the-parent, state overlays, zone/space state variants
  and range conditions are **nothing** in code today.
- The walked scenarios as `todo` probes with expected text — not yet written.

**Carrying superseded behaviour.**

- The numbered disambiguation menu still ships (`game/commands/cmd_act.py`,
  `game/commands/cmd_items.py` print `Which X do you mean?` followed by a numbered list). DR-08c
  retires it; the removal lands with this document's v2.
- Bare `go` still orients by naming where you can walk
  (`game/world/sim/operations/handlers/move.py`) — a list of options, made redundant by the exits
  line and retired by DR-08c.
- DR-23's three salience tiers are vestigial inside a zone: `_render_space` orders by `anchor` and
  `order`, and `salience` is now read only when grading what is visible in an *adjacent* zone.
  `appearance.py` still carries a `salience` on nearly every row.
- `presentation.md` v1 still states "the room desc stays static in v1" and describes the numbered
  menu; both are superseded by Andrew's 2026-09-16 decisions above.
