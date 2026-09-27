# 22 — The world-building loops

> **Status: draft for review.** No loop of this shape has ever run.
> **Architecture counterpart:** [`ontology-closure.md`](../architecture/ontology-closure.md) §6–§7
> (probes as the coverage definition; the closure loop) · `docs/harness.md` (pending, `PLAN.md` B2) ·
> `docs/ontology/README.md` (pending, the store's schema).
> **Sources:** document [05](05-ontology-and-sufficiency.md) (the store, the scaffold, the loops) ·
> [`ontology-closure.md`](../architecture/ontology-closure.md) §6–§7 ·
> [`loop-workflow.md`](../guides/loop-workflow.md) · [`VISION.md`](../../VISION.md).

---

## 2. Decisions

### Andrew's decisions

- **The world is fleshed out before anyone plays** (2026-09-16): the things and their synonyms are
  written down first.
- **Both models build the ontology, as peers** (2026-09-16). Sonnet 5 and Opus 5 each do ontology
  building, using a scaffold for thinking about a room and what more it could turn into — its entities
  and relations (the soil, a rock, clay…). Two models give better coverage; both have a good ontology
  to work with and need only the guidance. Sonnet is more conversational and less stuffy, so it thinks
  of fun, random things more often.
- **Sonnet writes the descriptions** (2026-09-16).
- **A scaffold is given, and it will be adjusted** (2026-09-16) — it is expected to change, not to be
  got right on paper. It is piloted on the draft and rewritten from what the two models produce
  (2026-09-18, document 05).
- **The store is human-browsable, with a viewer** (2026-09-16): everything about the rooms and
  entities is stored where people can look at it, with a simple app to view the ontology as a whole
  and per room, with a map. The store is `docs/ontology/`, as YAML.
- **A second pass, by reasoning, with lenses** (2026-09-16): agents imagine being in the survival
  scenario, in different situations and rooms, and list everything they could do there toward the
  survival and rescue goals, given goal lenses (tasks related to starting a fire, to finding food, …)
  and other lenses. Some agents build the world; others think of all the things they would do in it.
  The goal lenses are the backbone, plus human lenses (2026-09-18, document 05).
- **Design first** (2026-09-16): all design is finalized in conversation before rooms are built or any
  agent runs a loop — the rule at the top of [`docs/design/README.md`](README.md).
- **Then the cabin, as one zone of the plane, done right** (2026-09-16) — including the multi-zone
  connected perception (seeing and talking to people in adjacent zones) — with its design finalized;
  then implementation planning for it; then planning how to implement all the planned objects and
  actions (some need new functionality; how easy new verbs are inside the grammar is untested; the
  grammar may need expanding); then the grammar approach finalized in its own document. Every planned
  architecture or approach gets its own document, plus a master document.
- **There is no ceiling and no finish line** (2026-09-16). Every count in every document is a floor; a
  room is never finished — it is "no walls found in the last N runs" ([`VISION.md`](../../VISION.md)).
  What exists so far barely begins it.
- **Who does what** (2026-09-16): Fable plans; Opus 5 implements and grades its own work; cheaper
  models take mechanical and prose work.
- **The schema is designed in full, up front; the pilot verifies it** (2026-09-18) — document 05 §4.5:
  every field required, conditional or derived, and tagged with the pass that fills it.
- **The merge unions and never drops** (2026-09-18): `provenance` is a list, so agreement is a count,
  and every firing writes an analysis of what each model found (document 05 §4.5).
- **Walls per run counts five categories, separately** (2026-09-18) — document 05 §4.5a.
- **Ecology is a real filter** (2026-09-18): a species is in the valley only if it lives in this
  habitat, this month, in numbers that matter.
- **Real life is the default answer; state systems, not shortcuts; never make the world less
  interactive** (2026-09-26) — the writing rules in [`docs/design/README.md`](README.md), which the
  scaffold carries to the world-builders and scouts (§4.3).

### Proposals (Claude)

- **The phase structure** — a pilot pass, then Phase 1 (ontology), then Phase 2 (possibilities), and
  the rule that no implementation happens inside either (§4.1).
- **The scaffold's wording** (§4.3) — the sentences are drafted and piloted.
- **The merge mechanics** under Andrew's union rule (§4.2).
- **The queue** — its file, its format (zone × phase × model), and its ordering; the firing unit; when
  a pass is done and when a zone returns to the queue (§4.5).
- **The seeding tool, the viewer's page structure, `make validate-ontology`**, and the bridge to the
  runtime tables (§4.4).
- **The pilot's scope** — both phases, and the birch grove calibrated before the fifty outdoor zones
  (§4.1).

---

## 3. In one paragraph

Before anyone plays — human or model — the world has to actually contain what a person would expect
to find in it, and right now it does not. So the building is done by agents overnight, in passes, on
one room at a time. Two models go at each room as equals: one asks *what would a careful person
notice here, part by part, substance by substance*, the other asks *what would a curious, playful
person notice or try*, and both write down every entity, what it is made of, what it could turn into,
how it relates to everything else, and the command someone would type at it. Their two answers are
merged, with a note of which model found what, into a YAML file a human can open and a viewer that
draws the whole valley as a map with a page per room. Then a second kind of pass: agents imagine
being a survivor standing in that room — day one, dusk, injured, snowing — and, one goal at a time
(fire, water, food, a signal), list everything they would try, each as the command they would type.
Every one of those is a future probe and a candidate for the vocabulary. In the morning there is a
regenerated viewer and a diff to read. None of this writes code; building the code comes after, one
finalized zone at a time. And once the world is playable, agents play it, and every place the world
failed to answer becomes the next night's list — which is why the measure is walls per run and not a
percentage complete.

---

## 4. The design

### 4.1 The order

Andrew's sequence, with the steps that are his marked, and the rest proposals:

| # | step | whose |
|---|---|---|
| 0 | Every design document finalized in conversation | **his** |
| 1 | A pilot pass by hand; read it together; fix the scaffold, the queue format and the firing procedure from what we learn | proposal |
| 2 | **Phase 1 — ontology building** on every zone, both models as peers | **his** (the pass); proposal (the phase structure) |
| 3 | **Phase 2 — possibility passes** with goal lenses, both models | **his** |
| 4 | The cabin, as one zone of the plane, done right — including multi-zone connected perception; its design finalized | **his** |
| 5 | Implementation planning for the planned objects and actions, with a spike on how easy a new verb is inside the grammar | **his** |
| 6 | The grammar finalized in its own document | **his** |
| 7 | The play harness; then agents play freely and walls per run becomes the measure | proposal (document [20](20-the-agent-player-and-research.md)) |

Step 0 is a gate, not a preference: no agent runs in a loop before every design document is
finalized. Steps 2 and 3 write **no code**.

*(Proposed by Claude, for Andrew's check.)* Step 0 includes the system documents the review found
missing (`PLAN.md` A10) — at least combat; heat as a state on every entity and body part, with fire
heating its area and the plane's openings and internal heat; hunting, trapping and fishing; food state
and spoilage. The world-builders write every entity's `states` and `could_become`, and those
documents are what say which states and transforms exist; a zone written before them would be
rewritten after.

**The pilot** *(proposed by Claude, for Andrew's check; its outline is document 05 §4.7–§4.8)*. The
pilot is the mid cabin, by both models, read together. **Both phases are piloted** — an ontology pass
and a possibility pass — because both briefs are drafts. **The birch grove is calibrated the same
way, by hand and read, before the fifty outdoor zones run**: the queue takes the nine built rooms
first, so the calibration falls exactly where the terrain begins, and the outdoor rooms are the bulk
of the work and read nothing like a cabin — they are traversal terrain, where the systems are the
content. **What the pilot may change:** the scaffold, the queue format and the firing procedure
(document 05 §4.7); the schema only where it fails verification — the pilot verifies the schema, it
does not design it (document 05, Andrew 2026-09-18) — so a field found missing is a deliberate change
recorded in document 05, not drift.

### 4.2 Both models, as peers

Every room gets both passes. The two briefs differ on purpose, which is the entire reason for running
two:

| | the brief | the strength |
|---|---|---|
| Sonnet 5 | *"what would a curious, playful person notice or try here?"* | conversational, less stuffy — thinks of the fun, random things (Andrew, 2026-09-16) |
| Opus 5 | *"everything a careful person would notice, part by part, substance by substance"* | the systematic, exhaustive sweep |

**Outputs are merged and never ranked** — neither model's list is the reference the other is graded
against. Every row carries provenance (agent, model, pass, date, and the source document or line it
came from), so which model found what stays visible and the briefs can be adjusted from evidence
rather than impression. **The merge unions and never drops** (Andrew, 2026-09-18, document 05 §4.5):
a row both models found carries two provenance entries, and agreement is a count.

**The merge mechanics** *(proposed by Claude, for Andrew's check)*: mechanical where ids match; a
model's judgment (Sonnet's) where two rows are one thing under different words. A duplicate is the
same entity in the same place, whatever each model called it, and **both names survive** as
`synonyms`, because a second word for a thing is vocabulary (document 04 §3.7), not noise. A
disagreement of fact (vinyl or leather on the seat) keeps both values on the row with their
provenance and goes in the zone's conflicts list in the morning report; the design pass settles it
from reality, with a source (what the 206's seats are actually covered with), and the other value is
marked superseded on the row, never deleted.

The same peer rule applies to the possibility pass, for the same reason: one model imagines the
unexpected tries, the other the thorough ones.

### 4.3 The scaffold (proposal — piloted, then rewritten)

One guide, `docs/guides/world-building.md`, given to both models.

**For the ontology pass**, the frame is *"if this were the real world, not a MUD"* — which is
Andrew's writing rule that real life is the default answer (2026-09-26): every entity a person would
notice — objects, parts of parts, substances, surfaces, the ground and what is under it, natural
materials, sounds, smells, temperatures, light, wind, tracks, sign — what each is made of, what each
could turn into (cut, broken, burnt, dug, melted…), every relation to other things (on, under,
inside, attached, near), and every action a person would reasonably try on it **with the command
they would type**. Thorough, not the gist. No cap. Provenance on every row.

**For the possibility pass**, the model is handed a *situation packet* — the room, the day, the
weather, the party's state, what is known — and **one goal lens at a time**. The instruction is
*"list everything you might try, as the command you would type"*, and explicitly **not** to judge
feasibility. An impossible attempt is as useful as a possible one: it is either a gap to fill or a
physical answer to author.

Plus an **exemplar** — the pilot room worked to the standard, and the birch grove as the calibration
piece for terrain, which reads very differently from a cabin.

**What both briefs carry** *(proposed by Claude, for Andrew's check; the wording itself is piloted,
not settled here)*:

- **Real life is the answer.** When the world-builder does not know what a thing is made of, how it
  breaks or what it weighs, it finds out how it is in reality and cites the source; numbers come from
  real data first.
- **Every state a thing really has.** Each entity's `states` lists the axes it really has — heat
  (body parts included), wetness, frozen, spoilage, damage, open or closed — and each `could_become`
  is a real transform driven by a system (heat melts, cooks and chars; time and warmth spoil), never a
  shortcut.
- **Every real distinction a survivor would act on**, and every ontologically significant variant of
  an act as its own candidate command — cast a line out and drop one through a hole; stab, club,
  throw.
- **The ecology filter.** A living thing goes into a zone only if it lives in that habitat, in the
  first week of October, in numbers that matter (document 23).
- **The lenses** — a growing set, the list a floor: fire · water · food, which takes in hunting,
  trapping and fishing, many ways each · warmth · shelter · signals · rescue · injury · the pilot's
  body · the party · **danger** (the bear and the other acting animals, the ice, a fall, the storm —
  and violence, since a MUD-like combat system is in) · **moving** (exits are entities with modes and
  honest travel times; the outdoors is traversal terrain whose systems are the content); and the human
  lenses — curiosity, boredom, fear, grief, spite, tidying up, keeping the kid busy, play. Which lens
  produced a command is a field on every action row, so the analysis report shows what each lens
  finds.
- **One room, one situation and one lens at a time** (document 05 §4.8), with each room walked
  through the situations the week really has: day one in an inch of snow with skim ice on the water;
  the storm on days 3–4; deep snow after it; night; injured; alone; with the party; the bear near.

### 4.4 The store and the viewer

**`docs/ontology/`, YAML** (decided). The schema — per zone, per entity, the shared files and the
store's rules — is document 05 §4.5, designed in full up front (Andrew, 2026-09-18).
`make validate-ontology` checks the schema and the cross-references.

**Seeding without agents** *(proposal)*. A converter turns what is already built — the object table,
the materials, the zones, the spaces, the appearance rows, and the nine room censuses
([`docs/scenarios/whiteout/rooms/`](../scenarios/whiteout/rooms/)) — into the first YAML files,
marked built or designed with provenance *"converted from <file>"*. This matters for the review: the
store and the viewer exist and can be browsed **before any agent runs**, so the first thing Andrew
reads is the current world, not a model's guess at it.

**The viewer** *(proposal; document 05 §4.6)* generates a static site from the YAML: the world map
(positions and edges drawn from the zone files), a page per region and per room (entities, parts,
relations, candidate actions, synonyms, provenance, status), whole-world counts, and *what changed
since the last firing*. It is regenerated per firing and can be published as an artifact to browse
from anywhere.

**The bridge to implementation (later):** a converter from YAML rows to the runtime tables, run per
zone when that zone's design is finalized. The YAML stays the design of record for the ontology; the
tables stay the runtime.

### 4.5 The queue and a firing *(proposal)*

The queue is a file — `docs/ontology/loop-queue.md` — with a row per **zone × phase × model**. Order:
the nine built rooms first (they can be checked against reality), then the fifty designed zones.
State lives in the file and in git, so a firing that dies mid-way loses nothing and the next one
resumes at the first unchecked row.

**A firing** is a bounded chunk, then **stop**. The bounding is the point: a small chunk per firing
keeps each burst under the rolling token budget, so the work spreads across the night instead of
exhausting one window and dying. The unit inside a firing is a **whole zone for one phase** — both
models, the merge and its analysis report — so a zone is always complete for its phase or untouched
(document 05 §4.5: a row is complete for its phase, never half empty). How many zones one firing takes
is part of the firing procedure, which document 05 §4.7 fixes from what the pilot measures. A night
is many firings, and the morning artifact covers the night: the regenerated viewer, a diff summary,
each firing's analysis report, the conflicts list (§4.2), and — once agents play — the walls. The
artifact is what gets read; nobody reads the YAML diff.

**When a pass is done.** A *pass* is done when both models have run it on the zone and the merge is
written; "done" belongs to a pass, never to a room (a room is never finished). Every zone gets its
first passes before any zone gets a second — ordering, not a limit — and a zone goes back on the queue
on evidence: walls from play there (document 05 §4.5a); a new lens (every zone gets *danger* once it
exists); a new system document whose states and transforms its rows must carry (`PLAN.md` A10); a
design change that makes rows untrue (a change of season); or the analysis report showing a kind of
row one model keeps missing, which changes a brief and re-runs it. A diminishing-returns threshold
would be a count target, and counts are floors.

### 4.6 Probes, and how coverage is counted

Nothing in Phase 1 or 2 produces code, but everything in them produces **probes**. A probe is one
typed command chain in one room with an expected outcome class, run by the real parser against a pure
in-memory world. Every candidate command a scout writes is a future probe.

The rules that already govern the corpus (`ontology-closure.md` §6) carry over unchanged:

- probes marked passing are enforced; probes marked todo **are the work queue**;
- the passing count is a ratchet that may never drop;
- **every probe cites its source** — a census row, a phrasing line, a node of the rescue design
  (document 14), or Andrew's approval. No self-graded probes.
- **Coverage** = the passing corpus + the seeded fuzz (every attempt resolves, every effect
  conserves). Not a matrix-filled percentage.

That last rule is what keeps the loops honest: an agent cannot generate its own evidence that the
world is finished.

### 4.7 The order of work, and what carries into it

**Design is finalized first, then the ontology is written down, and only then is anything built**
(Andrew, 2026-09-16): a room is understood in full before a line of it exists.

Carried into these loops from the earlier build loop: the bounded firing; state in a file plus git so
the work resumes; the morning artifact being *prose or a page a human reads*, never a diff; committing
documents and code together; the census standard itself (*"if this were the real world, not a MUD"* —
every entity including the elusive ones: air, wind, light, sound, cold, smell, damp — and for each,
every action and relation with a candidate command); and the probe corpus as the definition of
coverage.

The implementation loop keeps its four beats — anchor, author, verify, repeat — and is still driven
with `/loop` ([`loop-workflow.md`](../guides/loop-workflow.md)). Phases 1 and 2 are not that loop:
their unit is a zone × a pass, and they run no gate because they produce no code.

### 4.8 Walls per run

The end state, after the play harness exists: agents play freely, and every wall — every attempt the
world could not answer, unknown words included — becomes the next pass's input. **Walls per run is
the measure.** There is no finish line, and a room's completeness is expressed the same way: no walls
found in the last N runs. What counts is Andrew's (2026-09-18, document 05 §4.5a): unknown word,
unknown noun, generic answer, wrong refusal and retry cluster, each counted separately with its own
trend line in the morning report.

---

## 5. Interactions

**This depends on:**

- **Every other design document.** The gate is literal: no loop fires until all of them are
  finalized, because a changed room intent invalidates the ontology written against it.
- [05 — ontology and sufficiency](05-ontology-and-sufficiency.md): what the loops are producing, the
  store and viewer they produce it into, the schema, the pilot and the scaffold's outline.
- [04 — grammar and feedback](04-grammar-and-feedback.md): candidate commands are written in the
  taught grammar; new verbs surfacing in Phase 2 feed the grammar's own finalization.
- [17 — rooms and living rooms](17-rooms-and-living-rooms.md): the census standard and the prose
  style the describer writes to.
- [18 — materials and forms](18-materials-and-forms.md): `could_become` rows are material × form
  claims and land in the shared material file.
- [23 — flora and fauna](23-flora-and-fauna.md): the ecology filter every living row passes, and the
  animals that act.
- The system documents still to be written (`PLAN.md` A10 — combat; heat; hunting, trapping and
  fishing; food state and spoilage): they define the states and transforms the world-builders write
  onto every entity.

**These depend on this:**

- [01 — premise and world](01-premise-and-world.md): the fifty outdoor zones get their content here.
- [20 — the agent player and research](20-the-agent-player-and-research.md): the walls loop is the
  last phase of this one; the phrasing sampling method is this loop's instrument for vocabulary.
- Implementation of anything world-shaped: the YAML → runtime-tables bridge is how a finalized zone
  becomes code.

---

## 6. Open questions

None open. The scaffold's wording is settled by the pilot, not on paper (document 05).

---

## 7. Review log

- **2026-09-16 (Andrew):** the loops' shape — both models as peers, a scaffold to be adjusted, a
  human-browsable store with a viewer, a possibility pass with goal lenses, design first, then the
  cabin zone done right.
- **2026-09-18 (Andrew, in document 05's sitting):** the schema designed in full up front and verified
  by the pilot; the merge unions and never drops; the scaffold piloted on the draft; goal lenses plus
  human lenses; walls counted in five categories.
- **2026-09-26 (Claude, self-review):** answered for Andrew's check — the frame and what both briefs
  carry (§4.3), the lenses including *danger* and *moving* (§4.3), the merge mechanics (§4.2), the
  firing unit and when a pass is done (§4.5), the pilot's scope (§4.1).

---

## 8. What exists today

**Nothing of this loop exists, and it has never run once.**

- No ontology store: there is no `docs/ontology/` directory, no schema file, no YAML.
- No seeding tool (`tools/ontology_seed.py`), no viewer (`tools/ontology_view.py`), no
  `make validate-ontology`.
- No scaffold: `docs/guides/world-building.md` does not exist.
- No queue: `docs/ontology/loop-queue.md` does not exist.
- No world-builder, scout or describer agent has been run against a room under this design.

**What the earlier build loop produced.** The engine core, the placement work and the authored prose
for the crash cluster; and the nine crash rooms censused into
[`docs/scenarios/whiteout/rooms/`](../scenarios/whiteout/rooms/) — one document per room, each with
its real-world entity census and a gap list. Its step into the fifty outdoor rooms never began.

**What exists to build on.** The probe corpus and its ratchet
([`game/world/scenarios/whiteout/probes/`](../../game/world/scenarios/whiteout/probes/)), which is
where every candidate command from a possibility pass will land; the wall-sensor writing
`server/logs/gaps.jsonl` from [`game/commands/cmd_act.py`](../../game/commands/cmd_act.py), which is
the walls-per-run input; the nine room censuses above; the runtime tables the seeder would read
(`objects.py`, `materials/table.py`, `zones.py`, `spaces.py`, `appearance.py`); and the content
validator that gates authored rows.

**A correction owed.** [`loop-workflow.md`](../guides/loop-workflow.md) describes only the
implementation loop — its unit of work is one object, one action family or one workflow stage, ending
at a green `make verify` — and its anchoring example still calls the slice's exit "the fun gate",
which the roadmap has replaced (fun is a continuous design judgment, and friends see the finished
game). The guide needs a pointer to this document for the world-building phases.
