# Presentation — scene-as-prose, salience, and the unified look/examine (DR-23)

> **Status: AUTHORITATIVE (promoted 2026-07-03; v1 IMPLEMENTED).** Approved by Andrew with the
> recommended defaults on the open questions: **three salience tiers** · **identical deriveds
> aggregate at ≥2** · **no authored hiding in v1** (deferred to the P3 perception work) · **object
> phrases only** (the room desc stays static in v1) · **moderate property hints** · **frames are a
> small per-room set** (`_frames`). Implementation: pure `game/world/sim/presentation.py`
> (composer + `describe`), content in `game/world/scenarios/whiteout/appearance.py` (Andrew-tunable
> voice), shell seams `Room.get_display_things` / `Object.return_appearance`. Reconstructed from
> the archived seed (§11/§13/§17/§38.2), lenses GD3/GD20/GD25, and prior-art. **Orthogonal to
> item-interaction** and **NOT** the P3 multi-zone perception system (DR-13 stays deferred) — this
> is what text a player reads inside one zone.

## The problem (what the play run showed)

1. Bare `look` renders the authored room prose, then Evennia's stock contents list — **"You see:
   aircraft seat, canteen of water, coil of copper wire, …"** — a checklist that spoils discovery.
   GD3: the list "closes curiosity by spoiling the answer before the player wonders the question."
   A player who reads "coil of copper wire" in a list thinks *"oh, I have to use a wire"* instead
   of discovering it.
2. **`look at X` and `examine X` diverge.** `look seat` hits stock Evennia (no desc authored →
   "You see nothing special"); `examine seat` hits the sim handler (a data dump). In MUD
   convention they are the same command.
3. **`examine` is the worst spoiler in the game**: `cushion (foam, clipped)` prints the solution
   as data — GD20's "checklist" failure mode, and the opposite of the §49 bet that responses read
   *specific and witty*.
4. **No object has any prose at all.** 17 objects, zero descriptions.

## Locked conventions (Andrew, 2026-07-02)

- Bare **`look`** IS the room survey. There is **no separate "look around" verb.** (The archived
  seed's `look around` split is retired by this decision.)
- **`look at X` / `look X` ≡ `examine X`** — one detailed description, one renderer, identical
  output on both paths.

## The design

### 1. One renderer per level, everything through prose

```
look                     → the SCENE: authored room prose + composed object prose (no list)
look at X / examine X    → the THING: authored object prose + state line + woven part names
examine <part> (or looking at a part) → the PART: its prose + physical attachment description
```

Progressive disclosure IS the look-tree: each level names the things the next level can address —
which is exactly what the taught grammar needs ("use `examine <thing>` to see what you can name").

### 2. Scene-as-prose `look`

The stock contents list is suppressed (`Room.get_display_things` override — the single Evennia
seam that produces the "You see:" line). In its place, a **scene composer** builds 1–3 prose
sentences from per-object **scene phrases**:

- Every object carries authored `scene_phrases`: how it appears *in the room description*, keyed
  by state — e.g. the wire: unbent *"a coil of copper wire glints under the frost near the radio
  rack"*; bent *"a bent length of copper wire lies where someone worked it"*. Selection is a pure
  function of `EntityState` (sim side); composition happens in the shell override.
- **Salience weights what is VISIBLE.** *(AMENDED 2026-07-03 by Andrew — DR-24 supersedes the
  original "weighting, never hiding" default: contents of unrevealed containers are honestly
  absent from the scene, the parser and the pool; `open`/`search`/`dig` earn them. See
  [`containment.md`](containment.md).)* Among the things that ARE visible, salience decides
  *order and prominence*:
  - **prominent** — leads the prose with its own sentence (the pilot, a lit fire, the radio).
  - **ordinary** — grouped into shared clauses: *"Scattered around the cabin: a whisky bottle, a
    flight manual, a wool blanket."* (grouping still reads like a scene, not a menu — no "You
    see:" header, no counts-first phrasing).
  - **subtle** — folded into an aggregate mention: *"a tangle of salvage — wire, cord, a jerrycan
    — heaped by the bulkhead."*
  - State promotes salience: a lit fire is always prominent; the radio crackling to life jumps a
    tier. Authored **hiding** (not mentioned at all until found) stays possible as an explicit
    per-object flag, but is never the default (open question 3).
- Derived objects group naturally: three glass shards → *"broken glass glitters near the seat"*
  (one aggregate phrase for N identical deriveds), not three list entries. `look at glass` /
  `get shard` then use the existing numbered menu when it matters which one.
- The room's own desc can carry state variants too (fire lit → the frost line changes) — the
  Extended-Room `$state` pattern, kept as authored variants in scenario content (open question 4).

### 3. The unified thing renderer (`look at X` ≡ `examine X`)

One pure function — `describe(EntityState, …) → prose` — used by BOTH paths: the sim `examine`
handler keeps its verb (events, resolver trace), and `Object.return_appearance` delegates to the
same function, so stock `look at` output is byte-identical. Shape:

- **Authored prose first** (the object's `examine_prose`, state-conditioned like scene phrases).
- **State woven, not listed**: today's `_condition` flags become prose clauses ("Soot streaks its
  base; it is still warm.").
- **Parts woven as prose with their names intact**: *"Its fabric cover is stitched over a thick
  foam cushion — the cushion sits snapped into a metal frame — and a nylon seatbelt hangs from a
  bolted anchor."* Part names (cover, cushion, seatbelt) appear naturally so the player learns
  what to type; **attachments render physically** via Workstream B's `attachment.hint.*` phrase
  map — never `(foam, clipped)`.
- **Property hints, not affordance lists** (GD20): at most a couple of sensory property cues
  ("the fabric is thin; the foam beneath is dense and dry") — never an enumeration of verbs.
- Idents stay: *"aircraft seat [11B]"* — the grammar needs addressable tags.

### 4. Voice

Specific-and-witty (GD25) or it fails its purpose: a derived-dry "the shirt is too light to block
wind" satisfies the invariant and loses the game's identity. All phrases are **content** in the
scenario (`responses/` or a sibling `appearance.py`), Andrew-tunable; Claude drafts the full set
for the 17 objects + parts + state variants, Andrew rewrites freely.

### 5. Explicitly out of scope

- Multi-zone perception bands, distance fading, the propagator rework — P3/DR-13, untouched.
- Any runtime LLM (narration stays template-rendered from state — DR-02).
- Per-observer differences beyond reachability (everyone in the zone reads the same scene for now).

## Mechanism sketch (feasibility only — details get their own certainty pass after approval)

- `Room.get_display_things(looker)` override → gathers contents' `EntityState`s via the existing
  worldview marshalling → pure `compose_scene(states, phrases) → str`. Pure side new module:
  `world/sim/presentation.py` (selection + composition, stdlib only). Shell stays thin.
- `Object.return_appearance(looker)` override → `describe(to_entity_state(self), …)`; the examine
  handler calls the same `describe`. One renderer, two entry points.
- Content: `scene_phrases` / `examine_prose` / `salience` live as object attributes set by
  `build.py` (same pattern as `sim_id`/`materials`), with the phrase text in a scenario content
  module for tunability. §44 validator later grows a "has scene phrase + examine prose" check.
- Tests: golden-master scene render for the crash cabin (seeded, deterministic); describe() unit
  tests per state variant; Tier-2 look/examine equality test (`look at seat` == `examine seat`).

## Open questions — RESOLVED 2026-07-03 (answers stamped in the status banner; kept for the record)

1. **Salience tiers**: are three (prominent / ordinary / subtle) right, or two enough?
2. **Derived-object aggregation**: always aggregate identical deriveds ("broken glass glitters…"),
   or only above a count (≥3)?
3. **Authored hiding**: keep a per-object "hidden until discovered" flag at all in v1, or defer
   hiding entirely to the perception work (P3)?
4. **State-conditioned room desc**: worth doing in v1 (fire-lit cabin reads differently), or
   object phrases only?
5. **Property hints in examine**: how bold may they be? ("the foam is dense and dry — it would
   burn ugly" vs just "dense and dry")
6. **The scene composer's connective tissue** (the "Scattered around the cabin:" framing lines):
   authored per-room, or a small reusable set?

## Sources
`design.md` §17 (prose look examples), §11/§13 (evocative-sparse, perception-honest prose), §38.2
(state-as-clue: the broken antenna); lenses GD3 (curiosity), GD20 (affordance discoverability —
"hints at properties and a couple of verbs, never the full set"), GD25 (specific-and-witty);
prior-art: Inform's Report stage, Curveship's simulator/teller split, Short's "knowing a verb
exists ≠ knowing when to apply it", Extended-Room `$state` conditioning; pinned Evennia seams:
`get_display_things` / `return_appearance`.
