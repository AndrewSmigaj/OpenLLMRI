# 05 — Ontology and sufficiency: what "anything reasonable" means, growing sets, the ontology store, the loops' scaffold, the viewer

> **Status: DRAFT FOR REVIEW (written 2026-09-16).**
> **Architecture counterpart:** [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md)
> — the mechanism (forms, derived capabilities, fallback physics, the probe corpus). This document is
> the *what* and the *why*; that one is the *how*.
> **Sources.** [`../../VISION.md`](../../VISION.md) ("What it is for", and the two non-negotiables
> added 2026-09-16) · [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md)
> §1 (including the two 2026-09-16 paragraphs), §2–§4, §6–§7 ·
> [`../investigation/design/00-provenance-audit.md`](../investigation/design/00-provenance-audit.md)
> §1 · the session plan of 2026-09-16 (§5.4 the world-building loops, §5.5 the scaffold, §13a the
> ontology store and the viewer) ·
> [`../investigation/world/objects.md`](../investigation/world/objects.md) (the per-zone census; its
> closing section on material-table candidates) · code: `game/world/sim/affordances.py`,
> `game/world/sim/testing/probes.py`, `game/world/scenarios/whiteout/probes/`.

---

## 2. Provenance

### Andrew's words

**The concept (2026-09-07, 2026-09-16).** An "ontologically sufficient" MUD: *"a user, or LLM when
we capture activations and analyze behavior, can do whatever is reasonable (if they want to cut
something they can break a mirror and get a piece of glass, then cut open a cushion for the stuffing
and then burn it)."*

**"Anything reasonable" (2026-09-16).** *"want to take an axe thing and chop the log up then sure.
want to dig dirt then yeah. find a rock, maybe some clay, whatever."* — the natural world is in
scope, not only the authored kit.

**What it is for (2026-09-16, quoted from [`../../VISION.md`](../../VISION.md)).** *"Two things, both
first-class: a **model world for serious research** — an LLM acts in it freely, through the same
taught grammar a person uses, and its behaviour and activations are studied (offering it options
would change how it thinks, so the world never does); and a **new kind of MUD** for friends — a
survival game where you can do anything within reason to solve it. Runs are for friends, for humans
and agents together, and for agents only. It is a massive side project, grown mostly in overnight
sessions where teams of agents systematically flesh out the world — every entity, relation and verb —
and it has no finish line."*

**The two non-negotiables added on 2026-09-16, quoted in full from
[`../../VISION.md`](../../VISION.md):**

> **The world is open-ended.** "Ontologically sufficient" means any and all entities and relations a
> player would reasonably try — chop the log with the axe, dig the dirt, find a rock, find clay, the
> natural world included. The verb set, the nouns, the relations, the materials and the forms are all
> growing sets, grown by evidence from room censuses and from play, without a ceiling. Every count in
> any doc is a floor. A room is never finished; it is "no walls found in the last N runs".

> **Never a menu.** The game never offers a set of actions, never lists what is reachable, never
> names a verb the player did not type. Feedback is a clarification (`Which can do you mean?`, `I
> don't understand 'X'`, a pointer to the grammar help) or the physics of why. Listing would give
> away the puzzles and, for an agent, constrain how it thinks.

**The scale of the work (2026-09-16).** *"This is not a small project, it is a massive side project
that will mostly run in overnight sessions as agents systematically 'flesh out' the world as in
building all the entities and relations and verbs."* *"We barely even touched this."*

**The loops, recorded in his words (2026-09-16).** The goal is to flesh out the things and the
synonyms *before anyone plays*. Sonnet writes descriptions; **both Sonnet and Opus do "ontology
building"**, using a scaffold we give them to think about a room and what more it could turn into —
entities and relations (the soil, a rock, clay…). Two models get better coverage; both have a good
ontology to work with, they just need the guidance, and we will adjust the scaffold as we learn.
Sonnet especially is wanted for the fun, random things a person would notice or try. **Everything
about the rooms and entities is stored where humans can look at it, with a simple app to view the
ontology as a whole and per room, with a map.** After the initial fleshing-out, a second pass by
reasoning: agents imagine being in the survival scenario, in different situations and rooms, and list
everything they could possibly do there toward the survival and rescue goals, given **goal lenses**
(*"tasks related to starting a fire"*, *"finding food"*, …) and other lenses — *"some agents build
the world, others think of all the things they would do in it."*

**Decided the same day.** The ontology store lives in `docs/ontology/` as YAML. Sonnet 5 and Opus 5
build it as peers. Nothing is built and **no agent runs a loop until every design document is
finalized**.

### Proposals (Claude)

- The YAML **schema** — every field named in §4.5, the shared files, the status vocabulary, the
  provenance requirement, the never-delete rule, `make validate-ontology`.
- The **viewer** as a generated static site, its pages, and the "what changed since last firing"
  summary.
- The **scaffold's wording** — the world-builder brief and the scout brief in §4.8 — and the choice
  of the mid cabin as the first exemplar and the birch grove as the outdoor calibration piece.
- The **seeding** step (converting what is already built into the first YAML files).
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
- The starting forms (~15) are `shard`, `piece`, `scrap`, `strip`, `sheet`, `slab`/`board`,
  `rod`/`stick`, `spindle`, `point`/`stake`, `bow`, `shavings`, `bundle`, `cord`, `vessel`,
  `ember`/`ash`. The starting operation categories are ~40. **Both are floors** — "where things
  start, never where they end" (Andrew, 2026-09-16).
- **Authored wins, derived fills.** An explicit value on an object overrides the derived one, so the
  golden tools stay hand-tuned while everything minted still works. Derived levels are **capped** at
  min(material, form), so free composition cannot mint an exploit. **State degrades**: a wet match has
  no ignition; a frozen cord is stiff.
- **The signifier rule.** A capability nobody can see is the top complaint across every
  property-based game studied. Every load-bearing derived capability must show in the examine text —
  *"a shard of glass, one edge wicked-sharp"* — which is why this system and
  [`03-the-player-view.md`](03-the-player-view.md) are two halves of one thing.

### 4.3 The honest interim answer

The loop will always be behind the players. Tier-4 generic physics is what stands in the gap: when no
handler fires, the answer comes from properties — a soft thing *"gives — there is nothing to break"*;
a liquid *"parts around the blade"*; a heavy thing *"won't shift"*; a wet thing *"is too wet to
catch"*. Each is a physical reason and nothing else: **the game never names a verb the player did not
type** (Andrew, 2026-09-16 — this retires the older verb-list redirect and the sibling near-miss
hint). The wall sensor records the attempt either way, so the fallback is also an input to the loop.

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
- Every probe cites its source: a census row, a phrasing-corpus line, a rescue-graph node, or
  Andrew's approval. No self-graded probes.
- Coverage = the probe corpus's passing count plus the seeded fuzz (every attempt resolves, every
  effect conserves).

The corpus grows from four sources: the room censuses, the phrasing corpus (agent-generated
commands), the rescue graph, and the dilemma set. Once the loops run, **every candidate command a
scout writes is a future probe** — which is what connects §4.7 to this number.

### 4.5 The ontology store

**Where.** `docs/ontology/`, as YAML (Andrew, 2026-09-16 — "stored where humans can look at it").
Human-readable, diffable, reviewable, and not the runtime.

**Per zone** — `zones/<zone>.yaml`: the zone itself (name, region, position, edges, terrain, exposure,
survey) and its entities. Each entity carries:

| field | what it holds |
|---|---|
| `id`, `name`, `aliases` | how it is addressed |
| `class` | individuated, or a class that yields individuals |
| `materials` | what it is made of |
| `parts` | recursive — parts of parts |
| `states` | the states it can be in |
| `form` | the shape its material is in |
| `located` | its space, and its relation to a parent: on / in / under / against |
| `could_become` | the transforms and what they yield |
| `relations` | to other things |
| `actions` | candidate commands, each with the goal lens that produced it |
| `synonyms` | the words people use for it |
| `status` | ✅ built · 📐 designed · ◌ candidate |
| `provenance` | agent, model, pass, date, source doc and line |

**Shared** — `materials.yaml`, `verbs.yaml` (canonical verb, family, the relations it takes, the
forms it yields), `synonyms.yaml`, `relations.yaml`.

**The rules** (in `docs/ontology/README.md`): provenance is required on every row; status is never
overstated; **a row is never deleted, only superseded**. `make validate-ontology` checks the schema
and the cross-references.

**Seeding, before any agent runs.** `tools/ontology_seed.py` converts what is already built — the
object table, the materials table, the zones, the spaces, the appearance rows, and the nine censuses'
entity lists — into the first YAML files (status ✅ built or 📐 designed, provenance "converted from
&lt;file&gt;"). So the store and the viewer exist, and Andrew can browse the *current* world during
the design review, before a single loop fires.

**Which one is the design of record.** The YAML is the design of record for the ontology; the Python
tables are the runtime. A converter (later) turns finalized YAML rows into object / material / zone /
space / appearance rows, run per zone when that zone's design is finalized.

### 4.6 The viewer

`tools/ontology_view.py` generates a static site (`docs/review/ontology/`, gitignored, regenerated
after every firing; also publishable so Andrew can browse it from anywhere):

- **the world map** — positions and edges, taken from the zone files;
- **per-region and per-room pages** — entities, parts, relations, candidate actions, synonyms,
  provenance, status;
- **whole-world counts**, and **what changed since the last firing**.

Kept simple on purpose. Its job is that a person can read the world.

### 4.7 The loops

**A pilot pass, by hand, first.** After the schema exists and after the design review — no agent runs
in a loop before every design document is finalized — one built room (the mid cabin) is done by the
world-builder on Opus 5 and again on Sonnet 5, under the draft scaffold; the two outputs are merged
into `docs/ontology/zones/mid_cabin.yaml`; Andrew and Claude read it and the first generated viewer
page together. **The scaffold, the schema, the queue format and the firing procedure are fixed from
what that teaches, not designed on paper.** Only then do the loops run unattended.

**Phase 1 — ontology building.** Unit: a room × a pass. The world-builder reasons about the room to
real-world depth — what is there, what it is made of, what each thing could turn into, every relation,
and (Sonnet especially) the fun, random things a person would notice or try — and writes YAML rows
with provenance. **Both models run every room**, as peers; which model found a row is kept, so we can
see what each contributes and adjust the briefs. Duplicates are reconciled by a merge step; synonyms
are collected as they appear.

**Phase 2 — possibility passes.** The scout imagines being a survivor in that room in a *situation*
(day 1 dusk, injured, the storm…) with **one goal lens at a time**, and lists everything they would
try, as the command they would type. New verbs, relations and entities surface here and go back into
the YAML. Every candidate command is a future probe.

**A firing** is one overnight run: N zones in parallel; the morning artifact is the regenerated viewer
plus a diff summary Andrew reads. The queue is a plain table of zone × phase × model rows — the nine
built rooms first, then the fifty designed zones.

**No implementation happens in either phase.** Design and implementation stay separate: the cabin
zone is finalized from its ontology first (including the multi-zone connected perception), then an
implementation plan is written for the planned objects and actions across the world, with a spike on
how easy new verbs are inside the grammar.

**Then play, and the walls.** Once the play harness exists, agents play freely, and every wall — an
attempt with no answer, an unknown word, a thing that should have been there — is logged and becomes
the next pass's input. **"Walls per run" is the measure.** There is no finish line.

### 4.8 The scaffold (what the agents are given)

`docs/guides/world-building.md` — one guide, two briefs. Wording is a proposal; it is expected to
change after the pilot.

**For world-builders — "if this were the real world, not a MUD":** every entity a person would notice
(objects, parts of parts, substances, surfaces, the ground and what is under it, natural materials,
sounds, smells, temperatures, light, wind, tracks, sign); what each is made of; what each could turn
into (cut, broken, burnt, dug, melted…); every relation to other things (on, under, inside, attached,
near); every action a person would reasonably try on it, **with the command they would type**.
Thorough, not the gist. **No cap.** Provenance on every row.

**For scouts:** the situation packet (room, day, weather, the party's state, what is known); **one
goal lens at a time** — fire · food · water · warmth · shelter · signals · rescue · injury · the
pilot · the party, plus lenses we add; "list everything you might try, as the command you would
type"; **never judging feasibility** (judging is what a probe is for).

**The exemplars:** the mid cabin from the pilot pass, and later the birch grove at real-world depth as
the outdoor calibration piece.

### 4.9 What the census already says the world needs

The per-zone census ([`../investigation/world/objects.md`](../investigation/world/objects.md)) was
written generous on purpose and is the closest thing to a dry run of Phase 1. Its closing section is
the concrete shape of "growing sets" — the materials the current table does not have:

> rock/stone (boiling stones, anvils, flakes — **presently absent**), bone/antler, fur/hide, peat,
> lichen, punk/rotten wood (ember medium — distinct from sound wood), rubber, kerosene, canvas,
> babiche/rawhide, grease/fat, mica ("the honesty material" — worthless glitter), brass, paper.

And the detail the natural world demands: snow and ice are never one object — powder, wind-slab,
drift, spindrift, sugar snow, snow-cap, sastrugi, rime, hoarfrost, surface hoar, frost feathers;
black ice, white ice, shore ice, pressure slab, overflow, frazil, skim ice, glare ice — *"the variety
IS the ontology exercise"*, and each behaves differently under the material table.

Its totals — **~59 zones, ~1,150 candidate objects, ambients and signs across the valley** (crash-site
builds excluded) — are a floor from one pass by one model, before any loop has run. That number is
the honest scale of the work, and the reason the store and the viewer come before the loops.

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
- [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) — moral tags, and other tags on
  actions, **are ontology fields** (Andrew, 2026-09-16), assigned in their own pass.
- [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) — a room is individuated by its
  ontology; "a room is never finished" is this document's rule applied there.
- [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) — the walls an agent
  hits are the loop's input; the research value depends on the world answering everything reasonable.
- Every survival system (06–14): what is *there* to work with is whatever the ontology holds.

---

## 6. Open questions

1. **The schema fields.** §4.5 is a first cut, never used in anger. Risks both ways: too few fields
   and the loops produce prose nobody can convert; too many and every row is expensive and half
   empty. Options: (a) take the field list as drafted into the pilot; (b) cut it to a minimum
   (`id`, `materials`, `could_become`, `relations`, `actions`, `provenance`) and let the pilot show
   what is missing; (c) design it further on paper first. **Recommendation: (b)** — the pilot exists
   precisely to fix the schema from evidence, and a thin schema that grows is cheaper than a wide one
   that is half-filled.
2. **The scaffold text.** The world-builder and scout briefs are the single biggest lever on output
   quality, and are currently one paragraph each. Options: (a) run the pilot on this draft and rewrite
   from what the two models actually produce; (b) write a long, worked brief first, with a full
   exemplar room. **Recommendation: (a) then (b)** — draft in, pilot, then promote the mid cabin's
   output as the exemplar, which is worth more than more instructions.
3. **The goal lenses.** The list (fire · food · water · warmth · shelter · signals · rescue · injury ·
   the pilot · the party) is Claude's, from Andrew's two examples. Open: whether non-goal lenses
   belong too — boredom, fear, grief, curiosity, spite, tidying up, keeping the kid busy — since a lot
   of what a person would try has no survival goal at all, and those are exactly the "fun, random
   things" Andrew wants from Sonnet. **Recommendation: keep the goal lenses as the backbone, and add
   a small set of human lenses**, tried in the pilot and kept only if they produce commands the goal
   lenses missed.
4. **How merges between the two models are reconciled.** Two models on every room will disagree on
   naming, granularity and plausibility. Options: (a) a Sonnet merge step that unions everything and
   flags only exact-id collisions; (b) a stricter merge that judges plausibility and drops rows; (c)
   keep both models' rows side by side, with provenance, and let the design pass prune. **Recommendation:
   (a) with (c) as the fallback** — dropping rows loses the evidence we are running two models to get,
   and "a row is never deleted, only superseded" already says which way to lean. The real question for
   the review is who prunes, and when.
5. **What counts as "a wall".** The measure of the whole programme is "walls per run", and it is
   undefined. Candidates: any tier-4 fallback; any unknown word; any clarification the player did not
   resolve; any attempt whose answer the player retried three different ways; only an attempt a
   reasonable person would expect to work. Options: (a) count the broad set and accept a noisy number
   that trends; (b) count only the narrow set and accept that it undercounts. **Recommendation: (a),
   with the categories kept separate** — the trend per category is what tells us which axis is
   lagging, and a single blended number would hide it. This needs Andrew's call, because it is the
   number he will be shown every morning.

---

## 7. Review log

*(Nothing yet — this document has not been reviewed with Andrew.)*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

## 8. What exists today

**Nothing of the store, the viewer or the loops.** Verified absent: `docs/ontology/` (no directory),
`tools/ontology_seed.py`, `tools/ontology_view.py`, `docs/guides/world-building.md` (the scaffold),
the loop queue under `docs/investigation/world/`, and a `validate-ontology` target in the `Makefile`.
No agent has ever run a world-building or possibility pass. The mid-cabin pilot has not been run.

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

**Designed, on paper, as scratchpads.**

- The per-zone census of the whole valley:
  [`../investigation/world/objects.md`](../investigation/world/objects.md), with
  [`map.md`](../investigation/world/map.md), [`rooms.md`](../investigation/world/rooms.md) and
  [`report.md`](../investigation/world/report.md).
- The nine built rooms' censuses: `docs/scenarios/whiteout/rooms/*.md` — the source of the `census`
  probes and the nearest thing to a Phase 1 output that exists.
- The mechanism spec: [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md).
