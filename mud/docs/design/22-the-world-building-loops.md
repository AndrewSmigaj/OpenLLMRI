# 22 — The world-building loops

> **Status: reviewed with Andrew 2026-10-01** (the pilot plan approved). Nothing in it has run yet.
> **Owns:** how the world-building passes run — the pilot, the scaffolds, how a run works, triage,
> merging, the review web app, the queue and the firings. **Document 05 owns** what the ontology is:
> the schema, the store's rules and the measure (walls per run).
> **Architecture counterpart:** [`ontology-closure.md`](../architecture/ontology-closure.md) (§6 probes
> as the coverage measure; §7 the implementation loop, which is a different loop from these passes).

---

## 2. Decisions

### Andrew's decisions

- **The world is fleshed out before anyone plays** (2026-09-16): the things and their synonyms are
  written down first.
- **Both models build the ontology, as peers** (2026-09-16). Sonnet 5 and Opus 5 each do it, from a
  scaffold for thinking about a room and what more it could turn into. Two models give better coverage.
  Sonnet is wanted especially for the fun, random things a person would notice or try.
- **Sonnet writes the descriptions** (2026-09-16).
- **A scaffold is given, and it will be adjusted** (2026-09-16, 2026-09-18): it is piloted, then
  rewritten from what the models produce.
- **The store is human-browsable** (2026-09-16), as YAML in `docs/ontology/`, with a map; **the viewer
  is a web app** where Andrew reviews the rooms and the ontology and adds or deletes things
  (2026-09-28).
- **A second pass, by reasoning, with lenses** (2026-09-16): agents imagine being in the survival
  scenario, in different situations and rooms, and list everything they could do, given goal lenses
  (fire, food…) plus human lenses (2026-09-18).
- **Design first** (2026-09-16): no agent runs a loop until every design document is finalized.
- **There is no ceiling and no finish line** (2026-09-16). Every count is a floor; a room is never
  finished *(Claude's measure, not yet decided: "no walls found in the last N runs")*.
- **Who does what** (2026-09-16): Fable plans; Opus implements and grades its own work; Sonnet and Opus
  are peers for building the ontology.
- **The schema is designed in full, up front; the pilot verifies it** (2026-09-18; document 05 §4.5).
- **The merge unions and never drops**, and it is measured (2026-09-18).
- **Walls per run counts five categories, separately** (2026-09-18; document 05 §4.5a).
- **Ecology** (2026-09-18): what is here is what realistically lives in an area of this size; food
  sources are not added just because they are possible.
- **Real life is the default answer; state systems, not shortcuts; never make the world less
  interactive** (2026-09-26) — carried to the agents by every scaffold (§4.3).
- **Balancing from play** (2026-09-28): after agents play, other language models analyse their
  playthroughs and the agents answer a brief questionnaire; what they find feeds the loops, including
  where a hint is needed.
- **The pilot is an experiment** (2026-09-29/30): hand-run and read together, set up so we can see what
  works, what is missing, what must change and what challenges appear — including what the agents
  assume and which things the engine already handles versus which need new mechanics. Several
  scaffolds are compared. It is analysed at length and followed by more tests and pilots; smoke tests
  along the way are welcome.
- **The pilot runs after the design review, before the missing system documents** (2026-09-30; `PLAN.md`
  A10), as an input to them. Its output is never merged automatically; the full loops still wait for
  every document.
- **The store starts from the design, not the old tables** (2026-09-30; document 05 §4.5). Nothing is
  reused just because it exists in the repo. Quality over speed; there is no deadline.
- **The web app gets pages for runs**, and later a way to launch runs from it with `claude -p`
  (2026-09-29).
- **The pilot plan** (2026-10-01): the changes in §4.1, the experiment in §4.7, the web app in §4.8.

### Proposals (Claude)

- The wording of every scaffold, the lens and situation lists, and every number here (run counts,
  thresholds, budgets) — settled by the pilot's evidence.

---

## 3. In one paragraph

Before anyone plays, the world has to contain what a person would expect to find in it. Agents build
it, one zone at a time, in two kinds of pass. In an **ontology pass** (the census), an agent lists every
thing in the zone: its parts, what it is made of, its states, what it could turn into, what it relates
to, what each sense gets from it, and the commands a person would type at it. In a **possibility pass**,
an agent imagines being a survivor there, in one situation, with one goal in mind, and lists every
command it would try. Every proposed command is fed straight through the real game engine, so we learn
at once which ones the engine already answers and which need new words, new content or new mechanics.
Each run is kept as an experiment; Andrew reviews it in a web app, asks the agent why it did what it
did, and merges the rows he wants into the store. A hand-run pilot comes first, to find out what works
before anything runs on its own.

---

## 4. The design

### 4.0 Terms

- **Pass**: one kind of work on one zone. An **ontology pass** (the census) writes the zone's things; a
  **possibility pass** writes the commands a survivor would try.
- **Scaffold**: a run's written instructions — the system prompt, the task, the output format.
  Versioned; a version is frozen once it has been run.
- **Run**: one model, one scaffold version, one zone, one pass — with its inputs, outputs and costs.
- **Packet**: the exact files a run is given.
- **Triage**: feeding each proposed command through the real parser and resolver.
- **R world**: the game as built today (the runtime tables). **S world**: a test world built from the
  store — the design.
- **Brief**: a zone's design truth — what the documents say is there, with sources and a "not here"
  list (`docs/ontology/briefs/<zone>.md`).

### 4.1 What changed from the first draft, and why

| # | Problem | Change |
|---|---|---|
| 1 | Sonnet always got the "playful" instructions and Opus the "careful" ones, so model and instructions could not be told apart | Instructions and models are crossed: each brief runs on each model |
| 2 | Proposed commands were not tested until play | Every proposed command is triaged at once, in the S world and the R world (§4.5) |
| 3 | The engine silently misreads some commands ("go aft" bound to the aft overhead bin; "sit on the seat" became *put*) | Every command carries its intended target and tool in plain words; triage flags a misread when the engine bound something else |
| 4 | Nothing recorded what the agent assumed | Each run returns its assumptions and questions; each row its support estimate; after a run the agent can be asked why (§4.4) |
| 5 | A whole-zone census as one answer hits output limits, and nested parts cannot be validated | The census is written one entity per file, then validated and repaired; small possibility outputs come back as structured JSON |
| 6 | Runs started in the repo would inherit its instructions, hooks and settings, and the user's | Runs execute outside the repo, isolated, with the model, effort and tools pinned, and are checked from their first event (§4.4) |
| 7 | Outputs were to be merged automatically | Runs are experiments; Andrew merges rows explicitly (§4.6) |
| 8 | A full possibility grid is about 19,000 runs | New commands per extra run are measured, and runs are scheduled by yield — an order of work, never a finish line (§4.9) |
| 9 | This document and document 05 repeated each other and disagreed | Document 05 owns the schema and store; this one owns how passes run |
| 10 | The loops find what players try, not the engine that answers it | The mechanics report ranks the engine work by how often commands need it (§4.7) |

### 4.2 The two passes

**Ontology pass (the census).** The frame is *"if this were the real world, not a MUD"*. Every thing a
person would notice — objects, parts of parts, substances, surfaces, the ground and what is under it,
natural materials, sounds, smells, temperatures, light, wind, tracks, sign — with what each is made
of, its states, what it could turn into, every relation, what each sense gets, its synonyms, and the
commands a person would type at it. Thorough, not the gist; no cap. Output: one YAML file per entity,
in document 05's schema.

**Possibility pass.** The agent is given what a survivor there would see and know, one situation (day
one on bare, frosty ground; the day-6 flurry; night; injured; alone; with the party; the bear near…)
and **one lens at a time**. It lists everything it would try, as the command it would type, with what
it means by it. It does **not** judge whether a command will work — an impossible try is as useful as a
possible one.

**Briefs and models are crossed.** Each scaffold's brief (for example "careful, part by part" and
"curious, playful") runs on both Sonnet and Opus, so what each model and each brief contributes can be
seen separately.

### 4.3 What every scaffold carries

- **Real life is the answer.** When the agent does not know what a thing is made of, how it breaks or
  what it weighs, it finds out how it is in reality and cites the source; every number is marked
  sourced, estimated or guessed.
- **Every state a thing really has** — heat, wetness, frozen, spoilage, damage, open or closed — and
  every transform as a real process (heat melts, cooks and chars; time and warmth spoil).
- **Every real distinction a survivor would act on**, and every meaningfully different act as its own
  command — cast a line out, or drop one through a hole; stab, club, throw.
- **The ecology filter** (document 23).
- **The zone's brief**, including its "not here" list.
- **The lenses** — a growing set: fire · water · food (hunting, trapping, fishing) · warmth · shelter
  · signals · rescue · injury · the pilot's body · the party · danger (the bear, the ice, a fall, the
  cold, the day-6 flurry, violence) · moving · and the human lenses: curiosity, boredom, fear, grief,
  spite, tidying up, keeping the kid busy, play. Which lens produced a command is recorded on it.
- **The grammar** (document 04): commands are written as a player would type them.
- **One worked example** of a correct entity row.
- **No rules that constrain the world** (2026-09-28): a zone holds not only things that are there for a
  reason; anything reasonable that follows the grammar works, whether or not it leads anywhere.

### 4.4 How a run works

1. **The packet.** A fresh workspace outside the repo gets: the scaffold's system prompt and task, the
   zone's brief, the output format with one worked example, the grammar forms, the season, the writing
   rules, the engine's vocabulary, and the document sections the scaffold lists. A possibility run also
   gets the survivor's view of the zone and the situation. Every file's hash goes in the run's manifest.
2. **The launch.** `claude -p` runs in that workspace with: safe mode (no project or user instructions,
   skills, plugins, hooks or memory); the scaffold as the whole system prompt; an explicit tool list
   (read, write, edit, search, web search and fetch, so it can cite real sources); no permission
   prompts; the full model id and an explicit effort, the same for both models; streamed output with
   hook events; a saved session id; a spend cap, a turn cap and a wall-clock timeout; a clean
   environment.
3. **The check.** The run is rejected unless its first event reports the requested model and tools and
   no hook fired.
4. **Validate and repair.** The output is validated against the schema; errors go back to the same
   session for at most two repair turns.
5. **Triage** (§4.5).
6. **The report.** A short report and the manifest: the model reported, effort, versions and hashes,
   tokens, estimated cost, time, turns, outputs by kind, validation results, triage totals, and later
   the merge and review records.
7. **Asking the agent why.** Any question can be put to the run's saved session afterwards ("why did
   you put a life vest here?"); the answer is kept with the run.

### 4.5 Triage

Every proposed command is fed through the real parser and resolver, with the game's responses loaded,
in the S world and in the R world. Each gets one category:

| What happened | Wall category (document 05 §4.5a) | What it would take |
|---|---|---|
| the verb is not known | unknown word | a synonym, or a new operation |
| the noun is not in the design | unknown noun | a census gap |
| the engine bound a different thing than intended | misread | naming things apart, or parser work |
| two things answer to the name | ambiguity | naming things apart (document 17 §4.7a) |
| in the design, not in the built game, and the S world answers | — | content only |
| a relation (on, under, behind) the operation ignores | — | relation mechanics |
| the generic fallback answered | generic answer | depth, or a new mechanic |
| refused where success was expected | wrong refusal (to review) | review |
| it works in the built game | answered | works now |

Some needs only a person or a model can tag: a state system (heat, spoilage), two people, position,
quantity. They map onto the missing system documents. Triage is trusted only after it agrees with
hand labels on at least 85% of a test set (§4.7, S3).

### 4.6 Merging

- **Runs are experiments.** Nothing reaches the store unless Andrew merges it.
- **Matching** rows across runs: the same id; then the same zone, parent and a shared name or synonym;
  then near-matches, which Andrew confirms. One matcher is used everywhere, and its decisions are shown
  and reversible.
- **The merge unions and never drops.** Lists union by key; provenance lists join, so agreement is a
  count; a disagreement of fact goes into the row's `conflicts` until it is settled from reality.
- **Removed rows stay removed.** A row Andrew removed is never added back; a new proposal of it only
  adds to its provenance. "Not in this world" removals become "not here" lines in the zone's brief.
- **Every merge writes an analysis report**: rows found by each model and each brief, by both, by only
  one, by kind, and how those counts move.

### 4.7 The pilot

**The questions it answers, and what each decides:**

| # | Question | Measured by | Decides |
|---|---|---|---|
| Q1 | Do agents produce valid, useful rows in the schema? | validation errors, how often each field is filled, repair turns | schema changes before the loops |
| Q2 | Which scaffold gives the most real, design-faithful content per cost? | yield by kind per 1,000 output tokens; unique finds by model and by brief | the scaffold; which model does what |
| Q3 | Do agents stay faithful to the design, and what do they assume? | contradictions against the brief; assumptions; answers to "why" | the brief format; what every packet carries |
| Q4 | What does the engine already handle, and what does it need? | triage by category and by what it would take | the mechanics report → the missing system documents and implementation planning |
| Q5 | Do matching and merging work? | 60 matched and unmatched pairs checked by hand | the merge procedure |
| Q6 | How much do possibility passes add, by situation and by lens? | new commands per extra situation and per extra lens | the sampling rule (§4.9) |
| Q7 | Does the scaffold transfer to outdoor terrain? | the same measures on the birch grove | whether terrain needs its own scaffold |
| Q8 | What does a zone cost — tokens, time, Andrew's reading? | run reports; reading time per run | firing size; whether loops can run unattended |
| Q9 | What would turn design rows into answers? | which S-world commands fail for lack of a mechanism | the bridge from the store to the runtime |
| Q10 | Does the web app make review easy? | Andrew's notes after each session | web app changes |

**Before the first real run — the spikes:**
- **S1 — isolation.** A trivial run with the exact command line, from outside the repo: the model,
  tools, effort and thinking settings reported, zero hooks, no project or user instructions visible.
- **S2 — output.** A census of about 80 entities written as files, and a structured output of about 30
  commands: truncation, tokens, time. Decides whether a census runs in one go or in stages.
- **S3 — triage.** About 40 hand-written mid-cabin commands, each with its intended target, labelled by
  hand and by the tool: at least 85% agreement before the totals are trusted.
- **S4 — the schema on paper.** Five mid-cabin entities written by hand (a seat and its parts, the cargo
  net, the hole in the hull, the cold, the floor): they validate, read clearly in the web app, and
  become every packet's worked example.
- **S5 — the S world.** An S world built from those rows, fed the S3 commands: what the bridge cannot
  express yet (on, under, the cold as a thing).
- **S6 — review walk-through.** Andrew uses the web app on the hand-written rows, so its problems are
  found on known content.

**Preparation:** the mid-cabin brief and its reference list (the design's named items and its ruled-out
ones), checked by Andrew; the rule for choosing between scaffolds, agreed before the first run.

**Round 1:**
- **Session 1 — the mid cabin, ontology pass.** 2 briefs × 2 models × 2 repeats = 8 runs; read
  together; agents asked why on their most surprising choices.
- **Session 2 — scaffold v2** from what session 1 showed; rerun; Andrew merges the rows he wants.
- **Session 3 — the mid cabin, possibility pass.** 3 situations × 3 lenses × 2 models, from the
  survivor's view; one run with all lenses in one session; one with the full ontology visible.
- **Session 4 — the birch grove**, both passes.
- **The analysis:** a plain-English report per question, the mechanics report, and the decisions.

**Optional smoke tests**, when they would clarify something: an agent playing against the S world one
command at a time (retries and the real wall rate); Sonnet writing the `sensed` text for merged rows,
read against document 17's rules; three merged rows turned into runtime rows and probed; the same
scaffold at a different effort or with a smaller or larger packet.

**Round 2 and after**, as the analysis calls for: other zones, other scaffolds, other models.

**The findings notebook** (`docs/ontology/pilot/findings.md`, also a web app page): each finding, the
runs that show it, and what was decided.

### 4.8 The web app

Local only, one worker (`make ontology-web`). Every action is also a command-line tool.

- **Browse:** home (counts, uncommitted changes, a map of the zones); a zone page (its things as a
  tree, filters by status and by who produced them); a page per thing; the shared tables; the
  validator's report.
- **Edit:** remove with a reason, restore, promote, add a synonym, action or note, edit a thing's YAML
  directly (validated on save). A **Commit** button commits only the store; nothing commits by itself.
- **Probe console:** type a command on a zone page and see what the S world and the R world do.
- **Runs:** the list; a run page (prompt, packet, outputs, assumptions, questions, triage, a diff
  against the store, merge selected rows); **ask this run**; a compare page; scaffold versions with a
  diff; the findings notebook.
- **Later:** a form that launches a run in the background, live progress and a stop button; the queue;
  the morning report.

### 4.9 After the pilot: the queue and the firings

- **The queue** is a file of zone × pass × scaffold × model rows. State lives in the file and in git,
  so a firing that dies loses nothing.
- **A firing** is one bounded chunk, then stop — a whole zone for one pass, so a zone is always
  complete for that pass or untouched. How many zones one firing takes is set by what the pilot
  measures.
- **Order** *(Claude's, not yet decided — settled after the pilot)*: the built crash-site zones first,
  then the designed ones; every zone gets its first passes before any gets a second. Possibility passes are scheduled by yield — the situations and lenses that
  still find new commands go first. This is an order of work, never a finish line.
- **A zone goes back on the queue** on evidence: walls from play there; a new lens; a new system
  document whose states and transforms its rows must carry; a design change; a kind of row a model
  keeps missing.
- **The morning report** covers the night: what changed, each run's report, the conflicts, the triage
  totals, and — once agents play — the walls.

### 4.10 Probes and coverage

Nothing in these passes writes code, but every proposed command is a future probe. A command becomes a
probe in `game/world/scenarios/whiteout/probes/` when its zone is finalized for implementation; until
then it stays a row with its triage result. The probe rules (`ontology-closure.md` §6) hold: passing
probes are enforced, the passing count never drops, every probe cites its source, and no agent grades
its own evidence.

### 4.11 Walls per run

Once agents play, every wall becomes the next pass's input. Walls per run is the measure, in document
05 §4.5a's five categories, each with its own trend.

---

## 5. Interactions

**This depends on:**
- **Every other design document** — no loop fires until all are finalized; the pilot may run before
  the missing system documents, as their input.
- [05 — ontology and sufficiency](05-ontology-and-sufficiency.md): the schema, the store, the measure.
- [04 — grammar and feedback](04-grammar-and-feedback.md): commands are written in the taught grammar.
- [17 — rooms and living rooms](17-rooms-and-living-rooms.md): the census standard and the prose rules.
- [18 — materials and forms](18-materials-and-forms.md): transforms are material × form claims.
- [23 — flora and fauna](23-flora-and-fauna.md): the ecology filter, and the animals that act.

**These depend on this:**
- [01 — premise and world](01-premise-and-world.md): the fifty outdoor zones get their content here.
- [20 — the agent player and research](20-the-agent-player-and-research.md): the walls loop is the last
  phase of this one.
- The missing system documents (`PLAN.md` A10) and implementation planning: the pilot's mechanics report.

---

## 6. Open questions

None open. The scaffold's wording, the lists and the numbers are settled by the pilot.

---

## 7. Review log

- **2026-09-16 (Andrew):** the loops' shape — both models as peers, a scaffold to be adjusted, a
  human-browsable store, a possibility pass with goal lenses, design first.
- **2026-09-18 (Andrew, at document 05's sitting):** the schema designed in full and verified by the
  pilot; the merge unions and never drops; goal lenses plus human lenses; walls in five categories.
- **2026-09-26 (Claude, self-review):** what every scaffold carries; the danger and moving lenses.
- **2026-09-27** — the no-storm week carried in.
- **2026-09-29 to 2026-10-01 (Andrew):** the pilot as an experiment, run after the review and before the
  missing system documents; the store starts from the design; nothing reused because it exists; the
  web app with run pages and, later, launching runs; the pilot plan approved — briefs crossed with
  models, triage with misreads, assumptions and asking the agent why, isolated runs, explicit merges,
  scheduling by yield, the spikes, the rounds and the findings notebook. Rewritten in plain technical
  English. **Reviewed in full.**

---

## 8. What exists today

**Nothing of these passes exists, and none has ever run.** No store (`docs/ontology/`), schema file,
validator, briefs, scaffolds, runner, triage, web app or queue.

**What they build on:** the probe machinery (`game/world/sim/testing/probes.py`, `pure_world.py`),
which already feeds a command through the real parser and resolver on an in-memory world — the basis
of triage and of the S world; the probe corpus and its ratchet; the wall-sensor writing
`server/logs/gaps.jsonl`; and the engine's tables, which the R world reads.

**Retired:** the old `whiteout-world-builder` agent and the `ontology-generator` skill (they write
Python content under the old model), and the July room censuses (an airliner-style cabin).

**A correction owed:** [`loop-workflow.md`](../guides/loop-workflow.md) describes only the
implementation loop; it needs a pointer here for the world-building passes, and its "fun gate" wording
is out of date.
