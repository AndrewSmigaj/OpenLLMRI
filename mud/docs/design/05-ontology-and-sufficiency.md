# 05 — Ontology and sufficiency: what "anything reasonable" means, growing sets, the ontology store, the loops' scaffold, the viewer

> **Status: reviewed with Andrew 2026-09-18 — every question answered; finalized at the close.**
> **Architecture counterpart:** [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md)
> — the mechanism (forms, derived capabilities, fallback physics, the probe corpus). This document is
> the *what* and the *why*; that one is the *how*.

---

## 2. Decisions

### Andrew's decisions

- **Ontological sufficiency (2026-09-07, 2026-09-16).** A player — a person, or a language model
  whose behaviour is analysed and whose activations are captured — can do whatever is reasonable: if
  they want to cut something, they can break a mirror for a piece of glass, cut open a cushion for
  the stuffing, and then burn it. **In practice (2026-09-28): anything reasonable that follows the
  grammar works — basically anything a language model playing the game would think to do — whether or
  not it leads anywhere: throwing a snowball is as real as lighting a fire.**
- **The natural world is in scope (2026-09-16)**, not only the authored kit: take an axe and chop
  the log up; dig dirt; find a rock, maybe some clay.
- **What it is for (2026-09-16).** Two purposes, both first-class: a model world for research — a
  language model acts in it freely through the same taught grammar a person uses, and its behaviour
  and activations are studied — and a new kind of MUD for friends, a survival game where you can do
  anything within reason to solve it. Runs are for friends, for humans with agents, and for agents
  only.
- **The world is open-ended (2026-09-16).** Any entity or relation a person would reasonably try is
  in scope. The verbs, nouns, relations, materials and forms are growing sets, grown by evidence from
  the room censuses and from play, with no ceiling. Every count in any document is a floor. A room is
  never finished; it is "no walls found in the last N runs". Every goal has several ways, with no
  set number (2026-09-27).
- **Never a menu (2026-09-16, 2026-09-27).** The game never offers a set of actions, never lists
  what is reachable, never names a verb the player did not type. Feedback is a clarification
  (`Which can do you mean?`, `I don't understand 'X'`, a pointer to the grammar help) or the physics
  of why, and common sense is hinted in the world's voice (document 04 §3.3). Listing would give away
  the puzzles and, for an agent, constrain how it thinks.
- **The scale of the work (2026-09-16).** This is a massive side project with no finish line, grown
  mostly in overnight sessions where agents systematically flesh out the world — all the entities,
  relations and verbs.
- **The loops (2026-09-16).** The things and their synonyms are fleshed out *before anyone plays*.
  Sonnet writes descriptions; **both Sonnet and Opus build the ontology**, with a scaffold we give
  them for thinking about a room and what more it could turn into — entities and relations (the soil,
  a rock, clay…). Two models give better coverage; both have a good ontology to work with and need
  only the guidance, and the scaffold is adjusted as we learn. Sonnet especially is wanted for the
  fun, random things a person would notice or try. After the first fleshing-out, a second pass by
  reasoning: agents imagine being in the survival scenario, in different situations and rooms, and
  list everything they could do there toward survival and rescue, given **goal lenses** (tasks
  related to starting a fire, finding food, …) and other lenses. Some agents build the world; others
  think of all the things they would do in it.
- **The store and the viewer (2026-09-16, 2026-09-28).** Everything about the rooms and entities is
  stored where people can read it — `docs/ontology/`, as YAML — with a map. Sonnet 5 and Opus 5 build
  it as peers. **The viewer is a web app where Andrew reviews the rooms and the ontology and adds or
  deletes things** (2026-09-28), not only reads them.
- **Design first (2026-09-16).** Nothing is built and **no agent runs a loop until every design
  document is finalized**.
- **No moral tags (2026-09-16, 2026-09-28).** Acts are not tagged as immoral, neutral or taboo; a
  language model reads the playthrough after the run (document 15 rule 6). Other tags on actions can
  be ontology fields if research ever needs them.
- **The schema is designed in full, up front (2026-09-18)** — the pilot verifies it; it does not
  design it (§4.5).
- **The merge unions and never drops, and it is measured (2026-09-18)**: the models' outputs are
  kept, how often each row is found is tracked at every merge, and the results are analysed for what
  each model is doing and for patterns (§4.5).
- **The scaffold (2026-09-18):** the pilot runs on the draft briefs, and the briefs are rewritten
  from what the two models actually produce (§4.8).
- **The lenses (2026-09-18):** the goal lenses as the backbone, plus a small set of human lenses
  (§4.8).
- **Walls per run (2026-09-18):** all five categories are counted, each separately (§4.5a).
- **Ambience comes from the things present (2026-09-18)** — each thing's `sensed` field carries its
  own cadence (document 06).
- **The store starts from the design, not the old tables (2026-09-30).** The engine's own vocabulary
  (materials, forms, capabilities, verbs, relations) is generated from code; the zone outlines come from
  document 01; each zone gets a brief of what the design says is there. The old runtime tables and the
  July room censuses describe an airliner-style cabin and are not imported — the runtime is only
  compared against. Nothing is reused just because it exists in the repo.
- **The schema refinements (2026-10-01, with the pilot plan):** flat parts with `part_of`; `states` as
  a list of axes; fixed `sensed` keys; provenance records the run and who; a `conflicts` list; a stable
  key on every sub-row; removals kept with a reason; every proposed command carries its intended target
  and tool; required fields checked per pass (§4.5).

### Proposals (Claude)

- The exact field names and value lists in §4.5, until the pilot verifies them (document 22 §4.7).
- The **scaffold's wording**, the lens lists and the situations — document 22, settled by the pilot.
- The **mechanism** counterpart in
  [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md): forms, derived
  capabilities, tier-4 fallback physics, the probe corpus as the coverage measure. Approved in
  outline (the closure chain is Andrew's own example, approved 2026-09-07); the specific form list,
  capability axes and numbers are proposals.
- Every count anywhere in this document. They are floors, and they are Claude's floors.

---

## 3. In one paragraph

"Ontologically sufficient" is the promise that if a survivor would reasonably try it, the world
answers physically — break the bottle, cut the cushion open with the shard, burn the stuffing; chop
the log, dig the dirt, find a rock, find clay. That promise is not a feature you finish; it is a
property you grow. So the world is built the way it is played: night after night, teams of agents
reason about one room at a time to real-world depth — what is there, what it is made of, what each
thing could turn into, every relation, everything a person would try — and write it down as YAML a
human can read, with a map and a viewer so Andrew can walk the whole world and any single room.
Other agents imagine *being* there, in a situation, with one goal in mind, and list every command
they would type. Everything either model finds becomes a candidate row; every candidate command
becomes a probe; every probe that fails becomes the next night's work. When agents finally play, every
wall they hit is logged and feeds the loop again. There is no finish line: a room is never "done", it
is "no walls found in the last N runs".

---

## 4. The design

### 4.1 What the property actually is

Sufficiency decomposes into axes that can each be worked on and measured
([`../architecture/ontology-closure.md`](../architecture/ontology-closure.md) §1):

| axis | means | where it is handled |
|---|---|---|
| **closure** | every output of an operation is a full entity: it has a form, derived capabilities, and prose | forms + capabilities (§4.2) |
| **fallback physics** | when no handler fires, the answer comes from mass / material / state, never from a verb list | §4.3 |
| **phrasing tolerance** | the taught grammar absorbs the phrasings people and agents actually type | [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) |
| **coverage, measured** | sufficiency is a number that only goes up | the probe corpus (§4.4) |
| **entity sufficiency** | scenery and elusive things (cold, draft, light, smell, sound) are addressable | pseudo-nouns; [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) |
| **time & stakes** | activities with feedback; fire, warmth, hunger, injury on the clock | [`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md) |

The gap this closed first was real and small: a shard minted by `break` used to carry only material,
mass and provenance, so `cut X with shard` counted as bare hands. Outputs were dead ends. Forms and
derived capabilities are what stopped that.

### 4.2 Growing sets, and why nothing here is a list

Three sets do the work, and none of them is closed.

- **Materials** say what a thing is made of. **Forms** say what shape that material is in. A
  **capability** — `edge`, `point`, `heft`, `leverage`, `abrasive`, `ignition`, `flame`, `cordage`,
  `sheet`, `vessel`, `insulating`, `absorbent`, `reflective` — is derived from material × form ×
  state. Verbs require a capability at a level; **a verb never names a tool**. That is the whole
  trick: anything the world mints is a full participant, so the sets can grow without touching the
  verbs.
- The starting forms are the code's 26 words, which are canonical (Andrew, 2026-09-18; document 07)
  — among them `shard`, `piece`, `scrap`, `strip`, `sheet`, `slab`/`board`, `rod`/`stick`,
  `spindle`, `point`/`stake`, `bow`, `shavings`, `bundle`, `cord`, `vessel`, `ember`/`ash`. The
  starting operation categories are ~40. **Both are floors** — where things start, never where they
  end (Andrew, 2026-09-16).
- **Authored wins, derived fills.** An explicit value on an object overrides the derived one, so the
  golden tools stay hand-tuned while everything minted still works. Derived levels are **capped** at
  min(material, form), so free composition cannot mint an exploit. **State degrades**: a wet match has
  no ignition; a frozen cord is stiff.
- **The signifier rule.** A capability nobody can see is the top complaint across every
  property-based game studied, so what a thing is like shows in its examine text as a couple of sensory cues — "a shard of glass, one edge wicked-sharp" — never what to do with it (2026-09-28; document 03 §4.6) — which is why this system and
  [`03-the-player-view.md`](03-the-player-view.md) are two halves of one thing.

### 4.3 The honest interim answer

The loop will always be behind the players. Tier-4 generic physics is what stands in the gap: when no
handler fires, the answer comes from properties — a soft thing *"gives — there is nothing to break"*;
a liquid *"parts around the blade"*; a heavy thing *"won't shift"*; a wet thing *"is too wet to
catch"*. Each is a physical reason and nothing else: **the game never names a verb the player did not
type** (Andrew, 2026-09-16). The wall sensor records the attempt either way, so the fallback is also
an input to the loop.

Fallback physics is the interim answer, **not the boundary**.

### 4.4 Coverage, measured

A **probe** is one typed command chain in one room with an expected outcome class, run through the
*real* parser against a pure in-memory world:

```python
{"id": "chain.shard_cuts_cover", "zone": "rear_cabin",
 "steps": ["break bottle", "take shard", "cut cover off 12c with shard"],
 "expect": "SUCCESS", "tier_prefix": "op:cut:free", "status": "pass",
 "source": "ontology-closure.md §1 (the example chain, step 2)"}
```

- `status: pass` probes are CI-enforced; `status: todo` probes **are the work queue**.
- `probes/BASELINE` holds the passing count and may never drop — the ratchet.
- Every probe cites its source: a census row, a phrasing-corpus line, a rescue path (document 14),
  or Andrew's approval. No self-graded probes.
- Coverage = the probe corpus's passing count plus the seeded fuzz (every attempt resolves, every
  effect conserves).

The corpus grows from four sources: the room censuses, the phrasing corpus (agent-generated
commands), the rescue paths (document 14), and the dilemma set (document 15). Once the loops run,
**every candidate command a scout writes is a future probe** — which is what connects §4.7 to this
number.

### 4.5 The ontology store

**Where.** `docs/ontology/`, as YAML (Andrew, 2026-09-16). Human-readable, diffable, reviewable, and
not the runtime.

**The schema is designed in full, up front (Andrew, 2026-09-18).** A schema is cheap to specify and
expensive to change once 59 zones of data exist: a field added later means either backfilling by
re-running passes or living with rows that disagree about their own shape. That is exactly the drift
waterfall exists to avoid, so the schema below is complete, and the pilot pass **verifies** it rather
than discovers it.

Two disciplines keep a full schema from becoming a half-filled one. **Every field is required,
conditional or derived** — if a world-builder standing in the room cannot fill it, it does not belong
in the ontology (it belongs in code, or in a later pass). And **every field names the pass that fills
it**, so a row is never "half empty", it is *complete for its phase*.

**Per zone** — `zones/<zone>.yaml`: the zone (id, name, aliases, region, position, terrain, exposure,
the survey line, and its **exits** — each with direction, mode `walk|climb|wade|crawl|enter`, travel
time, state) and its entities. **The zone is an entity too:** a zone row carries `materials`, `parts`
(its openings, the ground), `states` and `sensed` like any other entity, because the plane is an
entity with openings and an internal heat (Andrew, 2026-09-26), and the ground has a frost depth and a
snow depth (documents 17 §4.8, 23) *(the row shape proposed by Claude, 2026-09-26, for Andrew's
check)*. Each entity carries:

| field | what it holds | req. | filled by |
|---|---|---|---|
| `id` · `name` · `aliases` | how it is addressed; aliases are the nouns people try | required | census |
| `class` | `individual` · `class` (yields individuals: deadfall, snow, rocks) · `scenery` (addressable, not takeable) · `elusive` (cold, draft, light, smell, sound) | required | census |
| `count` | for a class or an aggregate: how many, and the mass of one | if `class`/aggregate | census |
| `materials` | what it is made of, in order | required | census |
| `mass_g` · `bulk` | integer grams; bulk derives from mass ÷ density unless authored | required · derived | census |
| `form` | the shape the material is in (`rod`, `sheet`, `vessel`…) | if it has one | census |
| `part_of` | the entity this is a part of, with its `attachment` (stitched, bolted, clipped, tied…). **Parts are entities in their own right, listed flat** — a part of a part points at its parent | if it is a part | census |
| `container` | `capacity_g`, `capacity_bulk`, `open`/`jammed`/`sealed`; what it contains is every entity located `in` it | if it holds things | census |
| `surfaces` | what things can sit *on* it | if it has any | census |
| `located` | `space`, and `relation` to a parent: on · in · under · against · attached | required | census |
| `states` | **a list of axes** this thing really has: `{axis, start, driver}` — e.g. `{axis: wet, start: dry, driver: wetness system}` (wet, frozen, temperature, burning, open, searched, damaged, lit…) | required | census |
| `could_become` | every transform: `{key, operation, needs: capability + level, yields: [{name, form, material, mass_g}], notes, support}` — cut, break, burn, dig, melt, shave… | required | census |
| `relations` | beyond containment: `{key, kind, target}` — blocks, supports, near, leads-to, owned-by | if any | census |
| `sensed` | **fixed keys** `look`, `smell`, `sound`, `touch`, `taste`, each `{text, cadence?}` — the cadence for things that speak on their own (a fire crackling, a creek running) and how it varies with state, since a room's ambience is the sum of its things (document 06) | required | census |
| `synonyms` | the words people use for it — written with the noun, not harvested (document 04 §3.7) | required | census |
| `actions` | candidate commands: `{key, command, intent, target, tool, lens, situation, expects, support, source}` — **`intent`, `target` and `tool` in plain words**, so triage can tell when the engine bound something else (a misread) | required | census · possibility |
| `goal_roles` | the goals this thing can serve a role in (ignition, fuel, vessel, binding…) — document 04 §3.9 | if any | possibility |
| `support` | on transforms and actions: what the agent thinks it would take — works now · content only · a synonym · a new operation · relation mechanics · a state system · a new mechanic | required on those rows | census · possibility |
| `numbers` | for each number given: `sourced` (with the source), `estimated` or `guessed` | required where numbers are | census |
| `status` | built · designed · candidate · removed | required | design pass |
| `removal` | when removed: `{by, on, reason}` — reason is not in this world · wrong · duplicate of · noise. The row is kept; the loops never add it back | if removed | design pass |
| `conflicts` | values two sources disagree on, each with its provenance, until the design pass settles it from reality | if any | merge |
| `notes` | anything the pass wants the next pass to know | optional | any |
| `provenance` | **a list**, one entry per pass that produced this row: `{model, agent, who, pass, run, date, source}` | required | every pass |

**Every sub-row has a stable `key`** (an action, a transform, a relation, a synonym), so a single one
can be removed or merged without touching the rest. **Required is checked per pass:** a row is
complete for the passes named in its provenance, never half empty for those.

**What the later systems need in these rows** (accepted 2026-10-01 with the pilot plan — so the
census can write what documents 10–23 define):

- **Temperature in `states`**, wherever the thing has one — body parts, food, water, stone, metal,
  the air of an enclosed space — because heat is a state on every entity, body parts included
  (Andrew, 2026-09-26).
- **Food-state axes in `states`** on anything edible: doneness, char, dryness, spoilage,
  contamination, and the hidden pathogens or parasites it may carry (documents 10 §4.6, 18 §4.8).
- **An ownership relation** in `relations` (`owned-by`), separate from holding — whose a thing is
  versus who has it (document 15 §4.6), with starting owners from documents 16 and 17.

**Shared files** — `materials.yaml` (every material with its axes, including `density` — document 18),
`verbs.yaml` (canonical verb, family, the relations it takes, the capability it needs, the forms it
yields), `synonyms.yaml`, `relations.yaml`, `goals.yaml` (the goal table, document 04 §3.9 — each row
lives in the system document that owns the goal, and this file collects them with that source). The
materials, forms, capabilities, verbs and relations the engine already has are generated from its
code, so the store starts from what the engine really does.

**The rules** (in `docs/ontology/README.md`): provenance is required on every row; status is never
overstated; **a row is never deleted, only superseded** — and when Andrew deletes something in the web
app, the row is marked removed by him with a reason and kept; the loops never add it back, and a
proposal of it again only adds to its provenance (2026-09-28, 2026-10-01). A "not in this world" removal
becomes a "not here" line in that zone's brief. The store is written in one canonical YAML form, with
no comments (notes go in `notes`). `make validate-ontology` checks the schema,
the cross-references, and the two disciplines above — a required field left empty is an error, a
field no pass owns is a schema bug.

**Merging, and measuring (Andrew, 2026-09-18).** Runs are experiments; Andrew merges the rows he
wants into the store, explicitly (2026-10-01; document 22 §4.6). The merge **unions, never drops**, and every row's `provenance` list gains an entry
per pass that found it. That makes agreement a number: a row found by both models carries two
entries, a row only one model saw carries one. Each firing then writes an **analysis report** beside
the merge: how many rows each model found, how many both found, what each found that the other did
not, broken down by kind (entity · part · state · transform · relation · action · synonym), and how
those counts move over time. That is what tells us what each model actually contributes, whether the
two-model premise pays, and how to change the briefs. Pruning is the design pass's, per zone, when it
reads the merge and its report.

**How the store starts (2026-09-30).** From the design, not from the old tables: the engine's own
vocabulary generated from code into the shared files; the 59 zone outlines from document 01 (with the
built zones' positions); and, for each zone the pilot works on, a **brief** (`briefs/<zone>.md`) — what
the design says is there, with its sources and a "not here" list — written by reading every document
that names the zone and fixing their contradictions first, then checked by Andrew. The old runtime
tables are what the S-world/R-world comparison measures against (document 22 §4.5); the July censuses
are not imported.

**Which one is the design of record.** The YAML is the design of record for the ontology; the Python
tables are the runtime. A converter (later) turns finalized YAML rows into object / material / zone /
space / appearance rows, run per zone when that zone's design is finalized.

### 4.5a Walls per run — the measure (Andrew, 2026-09-18)

A **wall** is a moment when someone tries something reasonable and the world cannot answer it
properly. **Walls per run** is the project's progress measure: it should fall as the loops flesh the
world out, and it never reaches zero — the world is open-ended, so there is always a next wall.

**All five categories are counted, and each is counted separately** (Andrew, 2026-09-18) — a blended
number would hide which axis is lagging, and this is the number read every morning:

| category | what happened | which gap it names | where it is logged |
|---|---|---|---|
| **unknown word** | they typed `chop`; no such verb | vocabulary | the parser's gaps log (document 04 §3.7) |
| **unknown noun** | they named something a real room would have and this one does not model (`the windscreen`, `the roots`) | the world | the parser's gaps log |
| **generic answer** | the verb fits and the thing exists, but the reply came from fallback physics rather than something specific | depth | the wall-sensor (tier-4 hit) |
| **wrong refusal** | the world said no to something a survivor could do | rules | the wall-sensor, flagged at review |
| **retry cluster** | the same intent tried three different ways in a row | anything — it is the player's own signal | derived from the per-step log (document 20) |

Each becomes a row in the morning report beside the ontology diff, with its own trend line. A
category that stops falling is the next pass's brief.

### 4.6 The web app

The viewer is **a web app** (Andrew, 2026-09-16, 2026-09-28): Andrew browses the world and any single
room, with a map, and adds, removes and edits things; what he changes is written back to the store
with his name as its provenance. It also shows the runs that build the store. Its design is document
22 §4.8.

### 4.7 The loops, the pilot and the scaffold

How the passes run — the pilot, the scaffolds, how a run works, triage, merging, the queue and the
firings — is document 22. This document owns what the ontology *is*: the schema, the store's rules and
the measure.

### 4.9 What the census already says the world needs

The per-zone census of the valley was written generous on purpose and is the closest thing to a dry
run of Phase 1. What it found is carried in the design documents: the materials the current table
does not have — rock and stone above all, then bone and antler, fur and hide, peat, lichen, punk wood,
rubber, kerosene, canvas, rawhide, grease and fat, mica, brass, paper (document 18 §4.7) — and the
detail the natural world demands: snow and ice are never one object — powder, wind-slab, drift,
spindrift, sugar snow, snow-cap, sastrugi, rime, hoarfrost, surface hoar, frost feathers; black ice,
white ice, shore ice, pressure slab, overflow, frazil, skim ice, glare ice. The variety is the ontology
exercise, and each behaves differently under the material table.

Its totals — **~59 zones, ~1,150 candidate objects, ambients and signs across the valley** (crash-site
builds excluded; document 01 §4.11) — are a floor from one pass by one model, before any loop has run.
That number is the honest scale of the work, and the reason the store and the viewer come before the
loops.

---

## 5. Interactions

**This depends on:**

- [`01-premise-and-world.md`](01-premise-and-world.md) — the zones the loops iterate over, and the
  map the viewer draws.
- [`18-materials-and-forms.md`](18-materials-and-forms.md) — the material table this grows; the forms
  vocabulary.
- [`22-the-world-building-loops.md`](22-the-world-building-loops.md) — the phases, the queue and the
  firing procedure in operational detail. This document owns *what the ontology is*; that one owns
  *how the nights are run*.

**Depends on this:**

- [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) — the verbs, relations and synonyms the
  grammar accepts are ontology rows; vocabulary grows here and the grammar absorbs it.
- [`03-the-player-view.md`](03-the-player-view.md) — every minted thing needs a phrase, and the
  state overlays key on material × form × state. A form with no prose is a thing nobody can see.
- [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) — acts are not tagged morally; a
  language model reads the playthrough after the run (Andrew, 2026-09-28).
- [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) — a room is individuated by its
  ontology; "a room is never finished" is this document's rule applied there.
- [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) — the walls an agent
  hits are the loop's input; the research value depends on the world answering everything reasonable.
- Every survival system (06–14): what is *there* to work with is whatever the ontology holds.

---

## 6. Open questions

None open. Every question this document asked was answered on 2026-09-18 and is written into §4.

---

## 7. Review log

- **2026-09-16** — the concept with Andrew: the world is open-ended and never a menu; the store as
  YAML in `docs/ontology/` with a viewer and a map; both models build the ontology as peers; the loops'
  two passes and the goal lenses; nothing runs until the design is finalized.
- **2026-09-18** — reviewed in full with Andrew: the schema designed in full up front, verified by the
  pilot; the merge unions, never drops, and is measured with an analysis report per firing; the
  scaffold piloted on the draft, then rewritten from the output; the goal lenses plus a small set of
  human lenses; all five wall categories counted separately; `sensed` carries a cadence, because
  ambience comes from the things present (document 06).
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).
- **2026-10-01 (Andrew, with the pilot plan):** the store starts from the design, not the old tables;
  the schema refinements (flat parts, states as axes, fixed senses, provenance with run and who,
  conflicts, stable keys, removals with a reason, the intended target on every command, required
  checked per pass); the viewer is the web app; how passes run moved wholly to document 22.

---

## 8. What exists today

**Nothing of the store, the viewer or the loops.** Verified absent: `docs/ontology/` (no directory),
`tools/ontology_seed.py`, `tools/ontology_view.py`, `docs/guides/world-building.md` (the scaffold),
the loop queue, and a `validate-ontology` target in the `Makefile`. No agent has ever run a
world-building or possibility pass. The mid-cabin pilot has not been run.

**Built — the closure mechanism's first step.**

- Forms and derived capabilities: `game/world/sim/affordances.py` — `derive(entity, materials)`
  computes capability levels from the primary material, `state["form"]` and state, with authored
  values winning, every factor capped, and every form a minting handler produces present as a key.
  Reached through `game/world/sim/operations/_helpers.py` (`capability`), so closure lands wherever a
  verb asks for an affordance.
- The runtime tables the store will be seeded from: `game/world/scenarios/whiteout/objects.py` (the
  object table), `game/world/scenarios/whiteout/materials/table.py`,
  `game/world/scenarios/whiteout/zones.py`, `game/world/scenarios/whiteout/spaces.py`,
  `game/world/scenarios/whiteout/appearance.py`.

**Built — the probe corpus.**

- The runner: `game/world/sim/testing/probes.py` (real parser, pure in-memory world, chained steps,
  outcome class and tier prefix compared).
- The corpus: `game/world/scenarios/whiteout/probes/` — `chain.py` (Andrew's own closure chain,
  approved 2026-09-07), `census.py` (candidate commands harvested from the nine room censuses, status
  measured, `todo` rows carrying the queue), `kit.py`, `phrasing.py`, and `BASELINE` (the ratchet).
- The entry points: `tools/probes.py`, `make probes`; the seeded solvability fuzz `tools/fuzz.py`,
  `make fuzz`.

**Designed, on paper.**

- The valley census's findings, carried into documents 01 (the zones, §4.5; the density gradient and
  the census totals, §4.11) and 18 (the missing materials, §4.7).
- The `census` probes (`game/world/scenarios/whiteout/probes/census.py`) — drawn from the July room
  censuses, the nearest thing to a Phase 1 output that exists.
- The mechanism spec: [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md).
