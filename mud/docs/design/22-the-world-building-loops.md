# 22 — The world-building loops

> **Status: draft for review (2026-09-16).** Never reviewed with Andrew. **No loop of this shape has
> ever run.**
> **Architecture counterpart:** [`ontology-closure.md`](../architecture/ontology-closure.md) §6–§7
> (probes as the coverage definition; the closure loop) · `harness.md` (pending) ·
> `docs/ontology/README.md` (pending, the store's schema).
> **Sources:** the plan file `plan-out-updating-the-lazy-pie.md` §1 (Andrew's words on the loops),
> §2 (the model policy), §5.4–§5.5 (the phases and the scaffold), §13a (the store and the viewer) ·
> [`build-queue.md`](../investigation/world/build-queue.md) (the July loop this replaces) ·
> [`ontology-closure.md`](../architecture/ontology-closure.md) §6–§7 ·
> [`loop-workflow.md`](../guides/loop-workflow.md) ·
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1 ·
> [`VISION.md`](../../VISION.md).

---

## 2. Provenance

### Andrew's decisions

**The loops, in his words (2026-09-16)** — as recorded in the plan file, which presents this
paragraph as his words rather than as a verbatim transcript; the itemised decisions under it are
each traceable to a second source. *"The goal is to flesh out the things and the synonyms
before anyone plays. Sonnet writes descriptions; both Sonnet and Opus do 'ontology building' using a
scaffold we give them to think about a room and what more it could turn into — entities and relations
(the soil, a rock, clay…). Two models get better coverage; both have a good ontology to work with,
they just need the guidance; we will adjust the scaffold. Everything about the rooms and entities is
stored where humans can look at it, with a simple app to view the ontology as a whole and per room,
with a map. After the initial fleshing-out, a second pass by reasoning: agents imagine being in the
survival scenario in different situations and rooms and list everything they could possibly do there
toward the survival and rescue goals, given goal lenses ('tasks related to starting a fire', 'finding
food', …) and other lenses — some agents build the world, others think of all the things they would
do in it. After the ontology is documented: one room first — the cabin, as one zone of the plane,
done right including the multi-zone connected perception (see and talk to people in adjacent zones) —
finalize its design, then plan implementation; then plan how to implement all the planned objects and
actions (some need new functionality; how easy new verbs are inside the grammar is untested; the
grammar may need expanding); finalize the grammar approach with its own document; every planned
architecture or approach gets its own document, plus a master document."*

The decisions that carries, itemised:

- **Both models build the ontology, as peers (2026-09-16).** *"Sonnet 5 and Opus 5 build the ontology
  as peers"* (audit §1). His reason, recorded with the model policy: **Sonnet is trained to be more
  conversational and less stuffy, so it thinks of fun, random things more often**; Opus is the
  systematic, exhaustive pass; together they cover more than either.
- **Descriptions are Sonnet's job.** *"Sonnet writes descriptions."*
- **A scaffold is given, and it will be adjusted.** *"a scaffold we give them to think about a room
  and what more it could turn into"* — and *"we will adjust the scaffold."* It is expected to change,
  not to be got right on paper.
- **The store is human-browsable, with a viewer (2026-09-16).** *"stored where humans can look at
  it, with a simple app to view the ontology as a whole and per room, with a map."* The store is
  decided: `docs/ontology/` as YAML (audit §1).
- **A second pass, by reasoning, with goal lenses.** Agents imagine being there and list everything
  they could do toward the survival and rescue goals. *"some agents build the world, others think of
  all the things they would do in it."*
- **All design is finalized before any of this runs (2026-09-16).** *"All design finalized in a
  conversation before rooms are built or any agent runs a loop."* This is the rule at the top of
  [`docs/design/README.md`](README.md).
- **Then the cabin, as one zone, done right** — including the multi-zone connected perception —
  *then* implementation planning, *then* the grammar finalized in its own document.
- **There is no ceiling and no finish line.** *"Every count in every doc is a floor. A room is never
  finished; it is 'no walls found in the last N runs'"* ([`VISION.md`](../../VISION.md)). And on how
  much has been done: *"We barely even touched this"* (audit §1).
- **Who does what (2026-09-16).** *"Fable plans; Opus 5 implements and grades its own work"*
  (audit §1); cheaper models take mechanical and prose work.

### Proposals (Claude)

Everything structural below. Specifically:

- **The phase structure** — a pilot pass, then Phase 1 (ontology), then Phase 2 (possibilities), and
  the rule that no implementation happens inside either.
- **The scaffold's actual wording** (§4.3) — his decision is that there *is* a scaffold and that it
  will be adjusted; the sentences are drafted.
- **The queue** — its file, its format (zone × phase × model), and its ordering.
- **The merge step** — that the two models' outputs are merged by a third pass, and that provenance
  is kept per row so each model's contribution stays visible.
- **The YAML schema** (§4.4), the seeding tool, the viewer's page structure, `make validate-ontology`.
- **The firing size**, the morning artifact, and the parallelism.
- **"Walls per run" as the measure** and the wall-sensor as the loop's input queue.

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
| 1 | A pilot pass by hand on one built room; read it together; fix the scaffold, the schema, the queue format from what we learn | proposal |
| 2 | **Phase 1 — ontology building** on every zone, both models as peers | **his** (the pass); proposal (the phase structure) |
| 3 | **Phase 2 — possibility passes** with goal lenses, both models | **his** |
| 4 | The cabin, as one zone of the plane, done right — including multi-zone connected perception; its design finalized | **his** |
| 5 | Implementation planning for the planned objects and actions, with a spike on how easy a new verb is inside the grammar | **his** |
| 6 | The grammar finalized in its own document | **his** |
| 7 | The play harness; then agents play freely and walls per run becomes the measure | proposal (document [20](20-the-agent-player-and-research.md)) |

Step 0 is a gate, not a preference: *"no agent runs in a loop before every design doc is finalized."*
Steps 2 and 3 write **no code** — that is the sharpest break from the July loop (§4.7).

### 4.2 Both models, as peers

Every room gets both passes. The two briefs differ on purpose, which is the entire reason for running
two:

| | the brief | the strength Andrew named |
|---|---|---|
| Sonnet 5 | *"what would a curious, playful person notice or try here?"* | conversational, less stuffy — thinks of the fun, random things |
| Opus 5 | *"everything a careful person would notice, part by part, substance by substance"* | the systematic, exhaustive sweep |

**Outputs are merged and never ranked** — neither model's list is the reference the other is graded
against. Every row carries provenance (agent, model, pass, date, and the source document or line it
came from), so which model found what stays visible and the briefs can be adjusted from evidence
rather than impression. A Sonnet merge step reconciles duplicates.

The same peer rule applies to the possibility pass, for the same reason: one model imagines the
unexpected tries, the other the thorough ones.

### 4.3 The scaffold (proposal — the wording is open question 1)

One guide, `docs/guides/world-building.md`, given to both models.

**For the ontology pass**, the frame is *"if this were the real world, not a MUD"*: every entity a
person would notice — objects, parts of parts, substances, surfaces, the ground and what is under it,
natural materials, sounds, smells, temperatures, light, wind, tracks, sign — what each is made of,
what each could turn into (cut, broken, burnt, dug, melted…), every relation to other things (on,
under, inside, attached, near), and every action a person would reasonably try on it **with the
command they would type**. Thorough, not the gist. No cap. Provenance on every row.

**For the possibility pass**, the model is handed a *situation packet* — the room, the day, the
weather, the party's state, what is known — and **one goal lens at a time**: fire · food · water ·
warmth · shelter · signals · rescue · injury · the pilot · the party, plus others as they are added.
The instruction is *"list everything you might try, as the command you would type"*, and explicitly
**not** to judge feasibility. An impossible attempt is as useful as a possible one: it is either a
gap to fill or a physical answer to author.

Plus an **exemplar** — the pilot room worked to the standard, and later an outdoor room (the birch
grove) as the calibration piece for terrain, which reads very differently from a cabin.

### 4.4 The store and the viewer

**`docs/ontology/`, YAML** (decided). `zones/<zone>.yaml` holds the zone — name, region, position,
edges, terrain, exposure, survey — and its entities. Per entity (proposal):

`id` · `name` · `aliases` · `class` (individuated | class-yields-individuals) · `materials` ·
`parts` (recursive) · `states` · `form` · `located` (the space, and the relation to its parent:
on / in / under / against) · `could_become` (the transforms and what each yields) · `relations` ·
`actions` (candidate commands, each with the goal lens that produced it) · `synonyms` · `status`
(built / designed / candidate) · `provenance` (agent, model, pass, date, source).

Shared files: `materials.yaml`, `verbs.yaml` (canonical verb, family, the relations it takes, the
forms it yields), `synonyms.yaml`, `relations.yaml`. `docs/ontology/README.md` holds the schema and
three rules: **provenance is required**, **status is never overstated**, and **a row is never
deleted, only superseded**. `make validate-ontology` checks the schema and the cross-references.

**Seeding without agents.** A converter turns what is already built — the object table, the
materials, the zones, the spaces, the appearance rows, and the nine room censuses — into the first
YAML files, marked built or designed with provenance *"converted from <file>"*. This matters for the
review: the store and the viewer exist and can be browsed **before any agent runs**, so the first
thing Andrew reads is the current world, not a model's guess at it.

**The viewer** generates a static site from the YAML: the world map (positions and edges drawn from
the zone files), a page per region and per room (entities, parts, relations, candidate actions,
synonyms, provenance, status), whole-world counts, and *what changed since the last firing*. It is
regenerated per firing and can be published as an artifact to browse from anywhere.

**The bridge to implementation (later):** a converter from YAML rows to the runtime tables, run per
zone when that zone's design is finalized. The YAML stays the design of record for the ontology; the
tables stay the runtime.

### 4.5 The queue and a firing

The queue is a file — `docs/investigation/world/loop-queue.md` — with a row per **zone × phase ×
model**. Order: the nine built rooms first (they can be checked against reality), then the fifty
designed zones. State lives in the file and in git, so a firing that dies mid-way loses nothing and
the next one resumes at the first unchecked row.

**A firing** (proposal): a bounded chunk — N zones in parallel — then **stop**. The morning artifact
is the regenerated viewer plus a diff summary, which is what gets read; nobody reads the YAML diff.
The bounding is the point, and it is the one piece of the July loop that proved itself: *"Doing a
small bounded chunk per firing is the entire point — it keeps each burst under the rolling token
budget so the work spreads across the night instead of exhausting one window and dying."*

### 4.6 Probes, and how coverage is counted

Nothing in Phase 1 or 2 produces code, but everything in them produces **probes**. A probe is one
typed command chain in one room with an expected outcome class, run by the real parser against a pure
in-memory world. Every candidate command a scout writes is a future probe.

The rules that already govern the corpus (`ontology-closure.md` §6) carry over unchanged:

- probes marked passing are enforced; probes marked todo **are the work queue**;
- the passing count is a ratchet that may never drop;
- **every probe cites its source** — a census row, a phrasing line, a rescue-graph node, or Andrew's
  approval. No self-graded probes.
- **Coverage** = the passing corpus + the seeded fuzz (every attempt resolves, every effect
  conserves). Not a matrix-filled percentage.

That last rule is what keeps the loops honest: an agent cannot generate its own evidence that the
world is finished.

### 4.7 What this replaces, and what survives from it

The July loop ([`build-queue.md`](../investigation/world/build-queue.md)) was **build-first**: per
room, *build it in code → census it → gap-analyse → verify and commit*, two rooms per firing. Its
successor inside that same file, the closure loop, changed the unit from a room to a probe cluster
and still ended each firing at a green gate and a commit.

The change now is not a refinement of either — it is the order. **Design is finalized first, then the
ontology is written down, and only then is anything built** (Andrew, 2026-09-16). Under the July
order, a room was implemented and then censused to see what had been missed; under this one, the room
is understood in full before a line of it exists. The July file's Phase 1 (the fifty outdoor rooms as
table rows) is history, and its gate never opened.

**What survives:** the bounded firing; state in a file plus git so the work resumes; the morning
artifact being *prose or a page a human reads*, never a diff; committing documents and code together;
the census standard itself (*"if this were the real world, not a MUD"* — every entity including the
elusive ones: air, wind, light, sound, cold, smell, damp — and for each, every action and relation
with a candidate command); and the probe corpus as the definition of coverage.

**On [`loop-workflow.md`](../guides/loop-workflow.md).** Its four beats — anchor, author, verify,
repeat — still describe the **implementation** loop, and driving it with `/loop` is unchanged. Two
things in it are superseded: its unit of work (*one object, one action family, one workflow stage,
ending at a green `make verify`*) does not describe Phases 1 and 2, whose unit is a room × a pass and
which run no gate because they produce no code; and its anchoring example still calls the slice's
exit *"the fun gate"*, which the roadmap has since replaced (fun is a continuous design judgment, not
a test a slice passes, and friends see the finished game). The guide needs a pointer to this document
for the world-building phases.

### 4.8 Walls per run

The end state, after the play harness exists: agents play freely, and every wall — every attempt the
world could not answer, unknown words included — becomes the next pass's input. **Walls per run is
the measure.** There is no finish line, and a room's completeness is expressed the same way:
*"no walls found in the last N runs."* What counts as a wall is open question 4 of document
[20](20-the-agent-player-and-research.md).

---

## 5. Interactions

**This depends on:**

- **Every other design document.** The gate is literal: no loop fires until all of them are
  finalized, because a changed room intent invalidates the ontology written against it.
- [05 — ontology and sufficiency](05-ontology-and-sufficiency.md): what the loops are producing, and
  the store and viewer they produce it into.
- [04 — grammar and feedback](04-grammar-and-feedback.md): candidate commands are written in the
  taught grammar; new verbs surfacing in Phase 2 feed the grammar's own finalization.
- [17 — rooms and living rooms](17-rooms-and-living-rooms.md): the census standard and the prose
  style the describer writes to.
- [18 — materials and forms](18-materials-and-forms.md): `could_become` rows are material × form
  claims and land in the shared material file.

**These depend on this:**

- [01 — premise and world](01-premise-and-world.md): the fifty outdoor zones get their content here.
- [20 — the agent player and research](20-the-agent-player-and-research.md): the walls loop is the
  last phase of this one; the phrasing sampling method is this loop's instrument for vocabulary.
- Implementation of anything world-shaped: the YAML → runtime-tables bridge is how a finalized zone
  becomes code.

---

## 6. Open questions

1. **The scaffold's wording.** §4.3 is a draft, and Andrew has already said it will be adjusted. The
   real question is what to change it from: a scaffold written on paper and a scaffold corrected after
   reading one room's output are different artifacts.
   *Options:* (a) review the draft wording now, in the sitting; (b) run the pilot pass on the draft
   and review the wording against its output; (c) both — glance now for anything obviously wrong,
   then fix properly from the pilot.
   *Recommendation:* (c). The text is cheap to change and the output is the only real evidence about
   it; the one thing worth settling on paper is whether the frame is *"if this were the real world,
   not a MUD"*, because everything else follows from that sentence.

2. **The lenses list.** Named so far: fire, food, water, warmth, shelter, signals, rescue, injury,
   the pilot, the party — *"and other lenses"*. Undecided: the full list, whether non-goal lenses are
   included (curiosity, fear, boredom, grief, keeping the kid occupied), and whether a lens is run
   per situation or per room.
   *Options:* (a) the ten goal lenses only; (b) the ten plus a small set of non-goal lenses;
   (c) goal lenses for the first sweep, then a second sweep of non-goal lenses once the gaps from the
   first are filled.
   *Recommendation:* (b). The goal lenses will find the rescue-relevant actions and miss most of what
   makes a room feel alive — nobody with a goal lens on thinks to look out of the window, and those
   are the attempts a real player makes in the first five minutes.

3. **The merge rule.** Two models produce overlapping lists with different words for the same thing.
   Undecided: who merges, what counts as a duplicate, what happens when the two disagree about a
   fact (one says the seat cover is vinyl, the other leather), and whether the merged row keeps both
   provenances or the first.
   *Options:* (a) a Sonnet merge step reconciling duplicates by name and keeping every provenance;
   (b) a mechanical merge on `id` with conflicts listed for a human; (c) no merge — keep both
   models' files side by side and let the viewer show the union.
   *Recommendation:* (a) with (b)'s conflict list: mechanical where the ids match, a model for the
   synonym judgments, and a short conflicts section per zone in the morning artifact, because a
   material disagreement is a real design question and should not be silently resolved by whichever
   pass ran second.

4. **The firing size.** The July loop's answer was two rooms per firing, tuned to the token budget.
   This loop's unit is bigger (a room's full ontology, twice over) and cheaper in one way (no code,
   no gates to run).
   *Options:* (a) two zones per firing, as before; (b) N zones in parallel, N tuned after the pilot;
   (c) one zone per firing but both models plus the merge, so a zone is always complete or untouched.
   *Recommendation:* (c) for the first several firings, then (b). A half-merged zone is the worst
   state to wake up to, and until the pilot has told us what one zone actually costs, any N is a
   guess.

5. **The pilot pass.** Proposed: the mid cabin, by hand, both models, under the draft scaffold, read
   together before anything runs unattended. Undecided: whether one room is enough evidence (a cabin
   and a snowfield are very different problems), and what specifically the pass is allowed to change
   afterwards.
   *Options:* (a) one interior room; (b) one interior and one outdoor room — the mid cabin and the
   birch grove; (c) one room per phase (an ontology pilot and a possibility pilot, possibly on
   different rooms).
   *Recommendation:* (b). The outdoor rooms are the bulk of the work (fifty of fifty-nine) and are
   known to behave differently — they are traversal terrain, where the systems are the content and a
   per-room hook is the wrong instinct ([`build-queue.md`](../investigation/world/build-queue.md),
   the fuselage-top census: *"outdoor rooms are traversal, systems > per-room hooks"*). Piloting only on a cabin would calibrate the scaffold on the
   easy nine.

6. **When is a zone's pass done?** There is no ceiling by decision, so "finished" cannot be the stop
   condition — but a firing has to stop somewhere, and a second pass over an already-rich room has
   to be worth more than a first pass over an empty one.
   *Options:* (a) one pass per model per zone, then move on and revisit only when play produces walls
   there; (b) repeat passes until a pass adds fewer than some number of new rows; (c) a fixed budget
   per zone, revisited on a schedule.
   *Recommendation:* (a). It matches "no walls found in the last N runs" — the world decides what
   needs more work by failing at it — and it avoids the trap of grinding the mid cabin to perfection
   while forty zones stay empty. A diminishing-returns threshold sounds principled but would be a
   count-based target, and the counts are floors.

---

## 7. Review log

*Not yet reviewed. This document has never been through a sitting with Andrew.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

## 8. What exists today

**Nothing of this loop exists, and it has never run once.**

- No ontology store: there is no `docs/ontology/` directory, no schema file, no YAML.
- No seeding tool (`tools/ontology_seed.py`), no viewer (`tools/ontology_view.py`), no
  `make validate-ontology`.
- No scaffold: `docs/guides/world-building.md` does not exist.
- No queue: `docs/investigation/world/loop-queue.md` does not exist.
- No world-builder, scout or describer agent has been run against a room under this design.

**What the July loop did produce** ([`build-queue.md`](../investigation/world/build-queue.md), still
the operational file until this replaces it): its foundation phase ran, and stopped there. The engine
core, the placement work and the authored prose for the crash cluster are done and ticked; the nine
crash rooms were censused into
[`docs/scenarios/whiteout/rooms/`](../scenarios/whiteout/rooms/) — one document per room, each with
its real-world entity census and a gap list. The live-verification box is **unticked**, and the gate
to the fifty outdoor rooms is **still closed** ("Andrew flips this after reviewing the foundation"),
so under that file a firing today would do nothing but re-verify. The closure loop's boxes in the
same file are all unticked.

**What exists to build on.** The probe corpus and its ratchet
([`game/world/scenarios/whiteout/probes/`](../../game/world/scenarios/whiteout/probes/)), which is
where every candidate command from a possibility pass will land; the wall-sensor writing
`server/logs/gaps.jsonl` from [`game/commands/cmd_act.py`](../../game/commands/cmd_act.py), which is
the walls-per-run input; the nine room censuses above; the runtime tables the seeder would read
(`objects.py`, `materials/table.py`, `zones.py`, `spaces.py`, `appearance.py`); and the content
validator that gates authored rows.
