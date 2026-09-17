# Scene spaces — template-driven rooms, positioned objects, inner scenes

> **The design of record for this material is `docs/design/03-the-player-view.md` (2026-09-16).** This file
> stays as the detailed source (the zone-by-zone designs, the investigation notes) until the
> ontology store carries it; it is a scratchpad, not authoritative.

> **Status: SCRATCHPAD (investigation) — 2026-07-15.** Andrew's design, worked up for a read-through
> before any code moves. Supersedes the salience-tier bucketing of DR-23 and grounds the
> [`presentation-v3-plan`](presentation-v3-plan.md)'s "composition with a budget" in a physical model.
> Scope of the first pass: the plane (cockpit / mid cabin / rear cabin) and the ground immediately
> outside it (outside-nose / fuselage-top / outside-tail).

---

## 1. The model

**A scene is a set of SPACES. Each space holds objects. Each object, looked at closely, opens its
own scene.** Rooms and objects are the same shape at two scales — the only difference is the verb
that enters them: `go to` walks you into a zone's scene, `look at` opens an object's scene.

**Space** — an authored *area* of a zone. Not an entity: you cannot take it, open it, or carry it.
You *can* look at it. It owns a frame, an order, and a cap.

**Object** — an entity that rests *in* a space. Carries a noun phrase (how it reads inside a frame),
an examine body, and optionally its own spaces + parts (its inner scene).

**Container** — an object whose inner scene is *gated*: `open` / `search` / `dig` earn it. This is
the DR-24 rule, unchanged. A container hides; a space arranges what is already visible.

### The two rules that make it survive players

These are the load-bearing rules; everything else is authoring.

1. **A frame describes POSITION, never HISTORY.** "Lying in the aisle" is true forever. "Spilled
   down the aisle" is a claim about how things got there — and it becomes a lie the instant a
   player drops a can opener. The zone's own survey line already carries the history ("Buckled
   seat rows and spilled luggage crowd the aisle"), and it can, because the zone is authored and
   never mutates.
2. **An object's phrase carries its own character.** "a duffel bag, burst half-open" is about the
   duffel and stays true wherever it goes. History belongs to the object, not the space it sits in.

This split is why the scene can't degrade: every object — authored or player-dropped — always
lands inside a frame written by a human *for that position*, and says only what is true of itself.

**The bug this fixes today.** The live frame is `"The crash left its litter everywhere: {items}."`
It currently renders over the forward stowage bin (bolted in — the crash left nothing) and the
oxygen masks (a ceiling fixture). It is already false, before any player touches anything.

---

## 2. Rendering a scene

```
zone survey line                          (authored, static — zones.py, unchanged)
for each space, in order:
    anchors → each its own sentence       (the space's defining object, if it has one)
    frame.format(items = and_list(phrases[:cap]), be = is/are)
    + overflow phrase, if len(phrases) > cap
```

- **and_list**, not comma-join. `_and_list()` already exists in `presentation.py:213`. The current
  `", ".join()` at line 114 is the entire list-ness of the system.
- **Number agreement.** `{be}` → "is" for one item, "are" for many. Frames are authored with the
  slot: `"Lying in the aisle {be} {items}."`
- **An empty space renders NOTHING.** This is the omission the current system cannot do — it is
  structurally required to mention every object present. Here it falls out for free.
- **Anchors** are how a space's defining object keeps its own sentence (the pilot, the drift, seat
  11B). A space needs no anchor; most don't have one.

### Absorption — the cap

A space names at most `cap` items and absorbs the rest into its overflow phrase:

> Across the cockpit floor are a flight manual, splayed face-down, a sectional chart folded to this
> valley, **and a scatter of smaller debris**.

Absorption is **deferral, not deletion**. `look at the floor` renders the space uncapped; `look at
debris` is the same thing, because the overflow phrase registers as an alias of the space. No
phantom entity is invented, nothing needs conserving, and `look at floor` / `look at debris` both
land where a player would expect. Spaces become look-at-able — still not take-able or open-able.

Cap of **3** proposed as the default, per space, tunable per space.

---

## 3. Dropping — the space picker

`drop X` resolves a space, then sets it on the object (real state, one additive field, written via
a normal Effect through `apply()` — no new mutation path).

- Each object has a **default space** for the zone it's in (heavy things → the floor; nothing
  clever). The game states where it went rather than asking: *"You set the can opener down among
  the litter on the cockpit floor."*
- **Explicit wins**: `drop can in the footwell` / `put can on the seat` → that space.
- **Ask only on a genuine tie**, offering the zone's spaces by name.

Rationale for defaulting over asking: a five-way question on every `drop` is friction by the third
one. The ask is the fallback, not the interface. **← Andrew's feel call; easy to flip.**

Nesting falls out for free later: `put battery in the radio's battery well` is the same operation
one scale down. Not built day one; the model doesn't foreclose it.

---

## 4. The spaces — the plane and its immediate outside

Objects nested inside containers (the wire in the panel, the chocolate in the seat pocket, the
gloves in the drift) are **not** listed — they are inner scenes, earned by `open`/`search`/`dig`,
and unchanged by this design.

### `cockpit`
| space | frame | holds |
|---|---|---|
| `left_seat` | *(anchor: pilot)* "Slung over the seat back beside him {be} {items}." | jacket |
| `cradle` | *(anchor: radio)* "Below the cradle {be} {items}." | panel, extinguisher |
| `footwell` | "Down in the footwell, against the rudder pedals, {be} {items}." | flightbag, thermos |
| `floor` | "Across the cockpit floor {be} {items}." | manual, chart · **default** |

### `mid_cabin`
| space | frame | holds |
|---|---|---|
| `seat_rows` | *(anchor: seat 11B)* "Wedged into the row {be} {items}." | — |
| `overhead` | "Overhead {be} {items}." | bin_fwd, masks |
| `aisle` | "Lying in the aisle {be} {items}." | duffel · **default** |

### `rear_cabin`
| space | frame | holds |
|---|---|---|
| `rear_rows` | *(anchors: snowdrift, seat 12C)* "Against the rear rows {be} {items}." | — |
| `overhead` | "Overhead {be} {items}." | bin_aft |
| `floor` | "Across the floor {be} {items}." | bottle, blanket, enginecover · **default** |

### `outside_tail`
| space | frame | holds |
|---|---|---|
| `hull_side` | "Rolled against the hull {be} {items}." | jerrycan, oil quarts ×3 |
| `the_snow` | "Half-sunk in the snow {be} {items}." | ice · **default** |

### `outside_nose`, `fuselage_top`
No loose objects today — they render their survey line alone, correctly. Each still needs one
**default space** so player drops have somewhere to land: `the_drift` ("Half-sunk in the drift
{be} {items}.") and `the_spine` ("On the bare aluminium {be} {items}.").

---

## 5. Read it — before and after

The cockpit is the showcase, because it is the worst case today: nine loose objects, three tiers.

**NOW** (what the composer actually emits — note the chart's internal commas colliding with the
joining commas, the exact "sectional chart, folded to this valley, the pilot" bug from the v3
retrospective):

> Shattered instruments and a crazed windscreen; cold air knifes in off the snow.
> The pilot lies still against the forward bulkhead. A field radio sits dark in its cradle beside
> the pilot. The crash left its litter everywhere: the pilot's spare flight jacket, a flight manual
> splayed face-down, a sectional chart, folded to this valley, an avionics panel, crumpled at one
> corner, the pilot's leather flight bag, wedged by the rudder pedals. Half-buried in the mess: a
> steel thermos, upright against the pedals, a small fire extinguisher in its bracket.

**WITH SPACES:**

> Shattered instruments and a crazed windscreen; cold air knifes in off the snow.
> The pilot lies still against the forward bulkhead. Slung over the seat back beside him is his
> spare flight jacket. A field radio sits dark in its cradle. Below the cradle are an avionics
> panel, crumpled at one corner, and a small fire extinguisher in its bracket. Down in the footwell,
> against the rudder pedals, are the pilot's leather flight bag and a steel thermos, standing
> upright. Across the cockpit floor are a flight manual, splayed face-down, and a sectional chart
> folded to this valley.

**`mid_cabin`, with spaces** (against the transcript Andrew read on Jul 10):

> Buckled seat rows and spilled luggage crowd the aisle.
> An aircraft seat — 11B stencilled on the frame — sits wrenched sideways on its bolts. Overhead are
> the forward stowage bin, latched shut, and a sprung ceiling panel with oxygen masks swaying from
> it. Lying in the aisle is a duffel bag, burst half-open.

**`rear_cabin`, with spaces:**

> The hull splits open here; snow sifts through the tear with every gust.
> Snow has drifted in through the split hull, banking white against the rear rows. A second
> passenger seat — 12C on the frame — lies thrown hard against the hull. Overhead the aft stowage
> bin is buckled shut in its track. Across the floor are an unbroken whisky bottle, a wool blanket
> half-spilled from it, and the quilted engine cover, folded fat as a mattress.

**`outside_tail`, with spaces:**

> The fuselage ends in torn metal here — the tail itself is GONE, and a scar of gouged snow runs
> away northeast.
> Rolled against the hull are a jerry can on its side and three quarts of engine oil. Half-sunk in
> the snow is a chunk of ice, broken off the wing root.

**And the same cockpit after a player drops three things on the floor** — the cap earning its keep,
and the frame staying honest about objects it was never authored for:

> Across the cockpit floor are a flight manual, splayed face-down, a sectional chart folded to this
> valley, and a scatter of smaller debris.

---

## 6. The code this needs

Small, and all of it additive behind the existing seam. `compose_scene()` is ~55 lines; this
replaces the bucketing half of it.

1. **`spaces.py`** (new, `world/sim/` — pure): the space table per zone; `id`, `aliases`, `order`,
   `frame`, `cap`, `overflow`, `default`. Mirrors `zones.py` — same shape, same load path.
2. **`presentation.compose_scene()`**: group by `state["space"]` instead of salience tier; render
   anchors, then `frame.format(be=…, items=_and_list(…))`; emit nothing for an empty space. The
   `perceived`/banding path (§14 distance grading) is untouched — it already groups by direction,
   which is the same idea one scale up.
3. **`appearance.py`**: each entry gains `space` (its home) and keeps `scene` as its noun phrase;
   `anchor: True` marks the few that lead a space with a full sentence. The tier fields
   (`salience`/`order`/`promote`) come out — order is now a property of the space.
4. **`drop`**: resolve a space (explicit → default → ask), set `state["space"]` via an Effect.
5. **`look at <space>`**: resolve space aliases + overflow aliases; render the space uncapped.

**Not changed:** containment (DR-24), the ledger, conservation, the zone/banding model, `describe()`.

### The open question this parks

`describe()` renders an object's parts today as one woven sentence
(`presentation.py:206` — *"You can make out its faceplate held by stitching"*). Under this model
that IS an inner scene with no spaces and no frame. Giving the radio real inner spaces is the
natural next step and the same code — **but it is a separate pass**, after the room scale is proven.

---

## 7. For Andrew

- **Read §5.** That is the whole proposal. If the voice is wrong, the model is still right and the
  frames are one file to retune.
- **The feel call in §3**: default-and-tell vs ask-on-every-drop.
- **Cap of 3** — a taste number, tunable per space.
- Voice check on the frames themselves: they are deliberately plain ("Overhead are…", "Lying in
  the aisle is…") because they repeat every single look. The *objects* carry the colour. An
  ornate frame gets old on the fourth read of the same room — but that is a judgement call, and
  it's yours.
