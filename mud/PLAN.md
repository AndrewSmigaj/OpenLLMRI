# PLAN — the program: every task, tracked

> **Status: LIVING — the single task list for the whole project (created 2026-09-17).** Every task we
> know of is here, with a status, the design document that owns it, and what it waits on. It is updated
> in the same commit as the work (the commit hook reminds). `BACKLOG.md` is only the *Now* slice of
> this file. `docs/scenarios/whiteout/roadmap.md` (the June P0–P7 arc) is history.
> Statuses: ☐ not started · ◐ in progress · ☑ done · ⊘ waiting on a decision (named).

## 0. RESUME HERE (last touched 2026-09-27)

**What we are in the middle of:** Phase A, the design review — a conversation over `docs/design/`, one
document at a time, until every one is finalized. Nothing is built and no agent runs a world-building
loop until then. The review page is **https://claude.ai/artifact/2Kyi7Cvxk2PovHthYRGayC** (regenerate
and republish it with `python3 tools/review_packet.py --current NN --out <scratchpad>/review-packet.html
--parked <scratchpad>/parked.md`). **The current decisions are §5** — every document is checked against
it.

**Where we are (2026-09-27):**
- Reviewed with Andrew: the GDD and documents 01–09. Documents 10–23 were re-reviewed by Claude against
  block 1 and real life (A9); Andrew answered the questions that were his, and the rescue was designed
  together (A13, document 14 §3).
- **Now: the cleanup (task A14).** Every document is made to show the current design only, in clean
  prose: no quotes of the conversation, no superseded material, every decision in §5 applied everywhere;
  the old seed design, the investigation scratchpads and the second GDD summary are removed. Document 13
  carries the first-week-of-October weather.

**Next, in this order:**
1. Finish A14, and answer the four items open with Andrew (§5, end).
2. **Document 15's rules**, presented one at a time — they have never been through a sitting.
3. **The sittings resume in index order**, checking the answers Claude proposed in each document, then
   finalizing at the close.
4. A10 — the missing systems' documents (combat, heat, hunting/trapping/fishing, food state, animal
   behaviour, scent, light, weather, snow and ice on the ground, physiology, the tutorial rooms); A11 — the
   GDD's vision, which Andrew finds too small.

**Standing corrections Claude owes the work** (in memory and in the writing rules): never quote the
conversation in the repository — it is public; show the current design only and carry every decision to
every document; never propose a cut for economy; never derive a world from a single answer; never ask
Andrew something he has already decided; be a design partner — real pushback, nothing added without
asking.

---

## 1. What we are building, and how this plan grows

Two things, both first-class: a **model world for serious research** — an LLM acts in it freely
through the same taught grammar a person uses, never offered options, and its behaviour is studied —
and a **new kind of MUD** for friends, where you can do anything within reason to solve the survival
game. Runs are for friends, for humans and agents together, and for agents only.

**The design has two halves, and this plan holds both.** The first half is *as designed as well as we
can to start*: the 22 documents in `docs/design/`, reviewed with Andrew one at a time until each is
finalized (Phase A). The second half is *what the loops add*: agents flesh out the world room by room
(Phase C), and an agent will put things in it nobody designed — a plant with a root you dig up, bugs
under bark, a use for clay. Every such addition flows back: into the ontology store, into the design
document of the system it touches (a new food source into `10-food-and-hunger.md`), and into **a new
task here** when it needs a verb, a material, a rule or a system that does not exist. The design is
never finished; it is finished *for now*, and this plan is where "for now" is kept honest.

**Rule:** nothing is built and no agent runs a world-building loop until the design documents are
finalized (Phase A). The machine that runs the loops (Phase B) is built in parallel because it touches
no design.

## 2. Done so far (so the plan starts from the truth)

- ☑ The engine core: the taught-grammar parser with tolerance, the operation×material resolver, the
  conservation ledger and single writer, zones and perception bands v1, scene spaces, containment,
  clothing v1 + v2 data, the crash draw (five slots, luggage), the probe corpus with its ratchet, the
  content validator, the render command, the four lint gates, CI. (June–September 2026.)
- ☑ The nine crash-site rooms built and playable; the fifty outdoor zones designed as documents.
- ☑ The provenance audit and corrections; the document system (22 design docs, the index, the GDD as
  umbrella); the branch pushed. (2026-09-16/17.)

## 3. The phases and the tasks

### Phase A — Design, first pass: the review (exit: every `docs/design/` document is `finalized`)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ◐ | A1 | The review sittings (2026-09-17), one document at a time in index order; the five-step procedure; the review packet page; blocks 1–4 then the close. Rows below flip as each document finalizes. | Andrew + Fable | all | — |
| ◐ | A1.00 | GDD umbrella — reviewed in full 2026-09-17 (every section rewritten or struck as decided); finalized at the close | Andrew + Fable | GDD | — |
| ◐ | A1.01 | 01 premise and world — reviewed in full 2026-09-17 (fifty zones, eleven regions kept); finalized at the close | Andrew + Fable | 01 | — |
| ◐ | A1.02 | 02 the experience — reviewed 2026-09-17; the sample week regenerated after block 4 | Andrew + Fable | 02 | — |
| ◐ | A1.03 | 03 the player view — reviewed 2026-09-17 (exits as entities, groups, the block) | Andrew + Fable | 03 | — |
| ◐ | A1.04 | 04 grammar and feedback — reviewed in full 2026-09-18 (the forms, `make`, quantities, encumbrance, the naming rule, word-first vocabulary); finalized at the close | Andrew + Fable | 04 | — |
| ◐ | A1.05 | 05 ontology and sufficiency — reviewed in full 2026-09-18 (the full schema, the measured merge, the five wall categories); finalized at the close | Andrew + Fable | 05 | — |
| ◐ | A1.06 | 06 time, sleep and the clock — reviewed in full 2026-09-18; finalized at the close | Andrew + Fable | 06 | — |
| ◐ | A1.07 | 07 fire and shaping — reviewed in full 2026-09-18; finalized at the close | Andrew + Fable | 07 | — |
| ◐ | A1.08 | 08 warmth, clothing and shelter — reviewed in full 2026-09-18; finalized at the close | Andrew + Fable | 08 | — |
| ◐ | A1.09 | 09 water — reviewed in full 2026-09-18; finalized at the close | Andrew + Fable | 09 | — |
| ☐ | A1.10 | 10 food and hunger — reviewed and finalized | Andrew + Fable | 10 | — |
| ☐ | A1.11 | 11 injury and first aid — reviewed and finalized | Andrew + Fable | 11 | — |
| ☐ | A1.12 | 12 the pilot and bodies — reviewed and finalized | Andrew + Fable | 12 | — |
| ☐ | A1.13 | 13 events, escalation and weather — reviewed and finalized | Andrew + Fable | 13 | — |
| ☐ | A1.14 | 14 rescue paths — reviewed and finalized | Andrew + Fable | 14 | — |
| ☐ | A1.15 | 15 moral and social layer — reviewed and finalized | Andrew + Fable | 15 | — |
| ☐ | A1.16 | 16 players and kit — reviewed and finalized | Andrew + Fable | 16 | — |
| ☐ | A1.17 | 17 rooms and living rooms — reviewed and finalized | Andrew + Fable | 17 | — |
| ☐ | A1.18 | 18 materials and forms — reviewed and finalized | Andrew + Fable | 18 | — |
| ☐ | A1.19 | 19 multiplayer and instances — reviewed and finalized | Andrew + Fable | 19 | — |
| ☐ | A1.20 | 20 the agent player and research — reviewed and finalized | Andrew + Fable | 20 | — |
| ☐ | A1.21 | 21 endings — reviewed and finalized | Andrew + Fable | 21 | — |
| ☐ | A1.22 | 22 the world-building loops — reviewed and finalized | Andrew + Fable | 22 | — |
| ☐ | A1.23 | 23 flora and fauna — reviewed and finalized (new 2026-09-17) | Andrew + Fable | 23 | — |
| ☑ | A2 | The cross-document decisions the documents flagged — settled in the sittings and in §5 (2026-09-17 to 2026-09-27); new ones are raised at the sittings. | Andrew | all | A1 |
| ☐ | A3 | Record every review decision: the doc's review log, the DR register (amendments), `VISION.md` where a non-negotiable moves. | Fable | — | A1 |
| ☐ | A4 | Re-price the valley for a week-long run (travel, stay-or-go, the ladder): the July map assumed a five-hour day. | Fable → doc 01 + 13 | 01, 13 | A1.01, A1.13 |
| ◐ | A5 | First-pass numbers as proposals where the docs have none: **ignition weights + threshold + the fuel-to-heat curve (07, owed — Andrew asked for a draft)**, the warmth and bedding numbers (08, incl. 06's fatigue), food yields per source (10), water (09), injury clocks (11), the landmark list and its values for the radio voice (14). Drafted for Andrew's review, tunable by probes later. | Fable | 06–11, 14 | A1 |
| ☐ | A6 | Promote finalized mechanisms into their architecture counterparts: `architecture/grammar.md`, `presentation.md` v2, `events.md`, `time-and-stakes.md`, `moral-social-layer.md`, `fire-and-shaping.md`, `rescue.md`; DR-29/30 appended. | Fable | 03, 04, 06, 07, 13, 14, 15 | A1 |
| ☐ | A7 | The GDD's per-system sections pointed and corrected where the seed text is wrong (§31–36 came from the archived AI seed; §19; §9). | Fable | GDD | A1 |
| ☑ | A8 | The season revised everywhere to the first week of October, from real data (done in the A14 cleanup, 2026-09-27; weather and daylight in document 13 §4.2). | Fable | all | — |
| ☑ | A9 | **Claude's self-review of documents 10–23** (done 2026-09-26): every open question checked against block 1 and real life; answered where reality or the decided design answers, rewritten where wrong-headed, left for Andrew only where it is his. Andrew answered his on 2026-09-27. | Fable | 10–23 | — |
| ☐ | A10 | **New design documents for the systems the review found missing** — at least: combat (a MUD-like combat system, Andrew 2026-09-26); heat (heat as a state on every entity and body part; fire heating its area with residual heat around it; the plane as an entity with openings and an internal heat — Andrew 2026-09-26: part of designing the fire and heat system); hunting, trapping and fishing (snares from materials, throwing, casting vs dropping a line, stabbing, clubbing); food state and spoilage. A9 found these (2026-09-26): **combat** (blows as named wounds on body parts, clothing as protection, rounds vs single acts, fleeing, restraint, animals as fighters; `kill X` as an aim-verb with document 04); **heat** (every entity and body part; contact heat and cold; the plane's openings and internal heat; carbon monoxide and smoke; a body cooling and freezing); **hunting, trapping and fishing**; **food state and spoilage**; **animal behaviour** (the actors: senses, attack modes, caching and scavenging); **scent** as a perception channel carried on the wind; **light and darkness** (daylight by date, firelight, the phone); **weather** (document 13 §4.7 specifies it for now); **snow and ice on the ground** (settling, drifting, ice growth, slush, frost depth; falling through ice); **the body's physiology** (document 11 grows into it, or its own document); **two people acting on one thing** (a grammar form, documents 04 and 19). Each is its own document (Andrew: every system has its own design document). | Fable → Andrew | new | A9 |
| ☐ | A11 | **The GDD's vision is too small** (Andrew, 2026-09-26: it should include a combat system like a MUD's, and more besides) — the umbrella's pitch, scope and system list re-read against the open world and the systems A9/A10 name, and broadened. | Fable → Andrew | GDD | A10 |
| ☐ | A12 | **Corrections A9 found, for when the content is authored:** the pilot's materials (skin, fat, muscle, bone, blood, organs — not `flesh`); the 206's windscreen and windows are acrylic, not glass; `insulation_batting` is two materials; `conductivity` → `electrical_conductivity`; the radio is a hand radio with its batteries in a bag in the tail (document 14 §3; `objects.py` has a "field radio" in the cockpit cradle); ground signals and a piece of mirror (document 14 §3.4); the handbook with its ELT page, the flight-plan copy, the kneeboard, the logbook, the altimeter (document 16); document 05's schema change notes (§4.5); ground-to-air shapes through the `INTO` slot (document 04); document 01's lake (depth, connection to the creek). | Fable | 01, 04, 05, 14, 16, 18 | A1 |
| ☑ | A13 | **The rescue, redesigned with Andrew** (2026-09-27 — the conversation is done, and document 14 §3 is rewritten cleanly from it; Andrew reads §3 whole at document 14's sitting): no working ELT; the battery in the nose and fine; a loose wire inside the radio that a technically proficient character sees; then the rest of the scenario — what makes the radio hard, what a party without that character does, the flyovers, the signals, surviving long enough. A conversation: real design help, no additions without asking. | Andrew + Fable | 14 | — |
| ◐ | A14 | **The cleanup** (Andrew, 2026-09-27): every document shows the current design only, in clean prose — no quotes of the conversation (the repository is public), no superseded material, every §5 decision applied everywhere; `design.md`, `GDD-summary.md` and `docs/investigation/` removed; the writing rules and §5 rewritten; the first week of October. | Fable | all | — |

### Phase B — The machine: the harness, the front door, the store (parallel with A; touches no design)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | B1 | The agent roster pinned to models (`implementer`, `world-builder`, `scout`, `describer`, `engine-reviewer`, `requirements-reviewer`, `docs-editor`, `sim-test-writer`); the certainty skill's post-implementation mode; the constitution; all hooks consolidated into `.claude/settings.json`; the Opus-4.8 env pin removed. | Fable | 22 | — |
| ☐ | B2 | `docs/harness.md` — the inventory of every hook, gate, skill, agent, command and doc, what each returns to Claude, its cost, and how to change it. | Sonnet draft → Fable | 22 | B1 |
| ☐ | B3 | `README.md` rewritten: what it is for, no ceiling, never a menu, how it's built, how we work, built with Claude Code deliberately, where we are (no stats), the quickstart fixed. Andrew reads before the push. | Sonnet draft → Fable | — | — |
| ☐ | B4 | Anchors and quickstart config: `docs/README.md`, `Makefile` default scenario, `docker-compose.yml`, the `.claude/commands`, the guides' scenario names, `CLAUDE.md` commands table. | docs-editor | — | — |
| ☐ | B5 | Stale text: the code READMEs that still say "scaffolded / no tests"; the architecture views (tick-and-scheduler, testing, llm-integration, overview, clothing-warmth, presentation ident); GDD-summary; the Claude tooling (run-game, new-object, lenses); tools/README. | docs-editor | — | — |
| ☐ | B6 | Hygiene: delete `seed.md`, `tools/bake.py`, `tools/coverage.py`, the certainty draft, empty scenario dirs; gitignore the render output and the hook stamp; banners on unbannered authoritative files; fix `_TEMPLATE.md` links; move `mudlet-research.md`. | docs-editor | — | — |
| ☐ | B7 | The commit doc-reminder hook (`.claude/hooks/commit-doc-reminder.py`): a Bash `git commit` triggers a checklist of the docs the staged paths may need, incl. this file. The first test of the implement → self-grade → review process. | Opus implementer → Sonnet review → Fable | 22 | B1 |
| ☐ | B8 | Publish: fast-forward `main` to the branch, push, CI green. After Andrew's read of README + VISION + this file. | Fable | — | B3, B4 |
| ☐ | B9 | The ontology store: the **full** `docs/ontology/` YAML schema (document 05 §4.5 — every field required/conditional/derived and tagged with the pass that fills it) + `docs/ontology/README.md` (provenance a list; a row is never deleted, only superseded); `make validate-ontology` checks the schema, the cross-references, required-but-empty fields and fields no pass owns. | Fable (schema) → Opus | 05 | — |
| ☐ | B10 | The seed converter `tools/ontology_seed.py`: the built tables and the nine censuses → the first YAML files (✅ built / 📐 designed), so the store exists before any agent runs. | Opus | 05 | B9 |
| ☐ | B11 | The viewer `tools/ontology_view.py`: a static site — the world map, per-region and per-room pages, counts, what changed since last firing; publishable as an Artifact. | Opus | 05 | B10 |
| ☐ | B12 | The loop scaffold `docs/guides/world-building.md` (world-builder and scout briefs; the goal lenses) and the loop queue in `docs/ontology/` (zone × phase × model). | Fable | 22 | — |
| ☐ | B15 | The Mudlet write-up and a proposed Whiteout Mudlet setup (the research is done: `docs/client/mudlet-research.md`). | Fable | — | — |
| ☐ | B13 | The clarification-only feedback in code (DR-08c): no verb suggestions, no numbered menus, `help verbs` gone, `make`/bare `use` clarify, `use X on Y` silent, the near-miss hint gone, bare `go` no longer lists exits' targets beyond the Exits line, unknown words logged to the wall-sensor; **tier-4 physics answers from properties replace the verb-list redirect**; probes re-authored to name nouns. | Opus implementer | 04, 05 | A1.04 |
| ☐ | B14 | Shipped narration and binding bugs (found by running the sample week): the article doubler ("the the pilot", "a leather gloves"), `the fire` binding the extinguisher, bare `bin` binding the far bin, `cover X` folding to `wrap`. Bug fixes, not design. | Opus implementer | 03 | — |

### Phase C — The world-building loops: the design grows (exit: every zone has both passes; additions flowed back)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | C1 | The pilot pass: the mid cabin by the world-builder on Sonnet and on Opus, merged; the first viewer page; read together; the scaffold, schema and queue fixed from what we learned. | both models → Andrew + Fable | 22 | Phase A exit, B9–B12 |
| ☐ | C2 | Ontology passes over every zone (the nine built first, then the fifty): entities, materials, what each could turn into, relations, candidate commands; merged with provenance. | both models, overnight | 22, 05 | C1 |
| ☐ | C3 | Possibility passes: a survivor in a situation, one goal lens at a time (fire · food · water · warmth · shelter · signals · rescue · injury · the pilot · the party · others), everything they would try as commands. | both models, overnight | 22 | C2 |
| ☐ | C6 | The merge and its analysis: union the two models' files per zone, never drop; provenance as a list so agreement is a count; an analysis report per firing — rows per model, rows found by both, what each found alone, by kind, and the trend over firings. | Opus | 05 §4.5, 22 | B9 |
| ☐ | C4 | **The feedback rule, run after every firing:** each addition that names a new food source, material, verb, relation, hazard or system goes into the owning design document as a proposal AND becomes a task here (Phase E) if it needs code. Synonyms → the phrasing probes. | Fable (morning read) | all | C2 |
| ☐ | C5 | Walls per run, five categories counted separately (document 05 §4.5a): unknown word, unknown noun, generic answer, wrong refusal, retry cluster; each with its own trend line in the morning report; the parser gaps log and the wall-sensor wired to produce them. | Fable + Opus | 05 §4.5a, 20, 22 | B13, F1 |

### Phase D — The cabin zone done right (exit: one zone of the plane plays end to end to the finalized design)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | D1 | Finalize the cabin zone's design from its ontology (the mid cabin as the exemplar); the room-authoring rules for the loops. | Andrew + Fable | 17, 16 | C1 |
| ☐ | D2 | The implementation plan for the zone (plan mode): objects, verbs, phrases, probes; the new-verb spike (how easy is a new verb inside the grammar; does the grammar need expanding). | Fable → Opus | 04, 17 | D1 |
| ☐ | D3 | The description model v2: the four composer extensions (relations rendered on the parent; generic state overlays; zone/space state variants via an additive zone-facts effect; range conditions), the walked scenarios as failing probes first, a certainty audit, then built. | Opus | 03 | A1.03 |
| ☐ | D4 | The look: the title line, prose composed from state, people and animals as prose, exits as entities in prose (document 03). | Opus | 03 | D3 |
| ☐ | D5 | The 206 interior as content: seats 1A/1B/2A/2B + the right seat with their finds; the hat shelf; the cargo net; the jammed cargo door; the finds redistributed from the six-seat draft; `look under` as the seat reveal; the guide's and nurse's missing bag extras. | describer + Opus | 16, 17 | A1.16 |
| ☐ | D6 | Multi-zone perception verified against doc 19 (see and talk across zones; hear by loudness); the propagator's weather stub. | Opus | 19 | A1.19 |
| ☐ | D7 | The pilot starts the run dead (2026-09-17); the body afterwards (`cover` as reverence, search, `butcher`, buried, findable); the `pilot_body` dilemma probe. | Opus | 12, 15 | A1.12 |
| ☐ | D8 | Elusive nouns and sense verbs (cold, draft, light, smell, sound; smell/listen/feel) as a generic mechanism, proven on one room. | Opus | 17, 05 | D1 |
| ☐ | D9 | Render read and voice sign-off on the cabin (Andrew reads the rendered zone whole). | Andrew | 17 | D3–D8 |

### Phase E — The systems, built to the finalized designs (each item: probes first, certainty mode B, the reviewer pair)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | E28 | Openings as speaking entities: the hull tear, the torn tail, a missing pane, the unseated cargo door — each with a wind sound that varies with weather and with being blocked; blocking one makes the room quiet. The zone's wind and roof numbers are read through them. | Opus | 08 §4.8, 06, 05 | A1.08, E26 |
| ☐ | E26 | The three streams: activity emotes (start/tick/interrupt/complete), ambience from the things present (each thing's `sensed` cadence, varying with state; the sum is the room), and other people through the propagator. Under a fast forward the world runs fast for the awake watcher, rate-limited in real time to stay readable; interrupting events drop the clock to base pace. | Opus | 06, 05 | A1.06, E1 |
| ☐ | E1 | Time: the clock at 15 game-min per real min with a 4-second heartbeat; fast forward at about 150× by the players' agreement, a command to slow it, a player waking or any non-ambient event dropping it back to 15×; the activity scheduler (attended actions with start/tick/interrupt/complete; unattended processes; `responses/activities.py`); sleep and wait; halt and resume with the missing-member rule; travel durations actually spent per exit. | Opus | 06, 01, 19 | A1.06 |
| ☐ | E27 | Reconcile the forms list: the code's 26 words are canonical; correct `ontology-closure.md` §2's table and drop its "extend by evidence, never speculatively" comment (ceiling framing). Reconcile `systems/fire.py`'s older stage ladder to the design's. | Opus | 07, 18, 05 | A1.07 |
| ☐ | E29 | A latent `break` id collision: `_shatter` ids are `derived_id(parent, f"{piece_word}{i}")`, so breaking two parts of one entity would collide — give `break` the part-scoped id shape when it is next touched. | Opus | 18 | — |
| ☐ | E2 | Fire: the ignition model (source × receptivity × form thinness; a branch does not take from a lighter), fire as a process (the stage ladder; the stub's old ladder reconciled), the shaping family (`carve/split/shave/whittle/notch/string/bundle`), the seven methods as probe chains. | Opus | 07 | A1.07, E1 |
| ☐ | E3 | Warmth, clothing, shelter: the night-one rule as a property test (inside the wreck, starting clothes, no fire, no huddle → survives; nothing done by night two → in trouble); the cold clock (regions, wet fraction, wind), huddle, shelter as zone properties (per-zone exposure bands in `zones.py`; wind and roof numbers written by built things: `cover/block` an opening, snow walls, boughs), drying and wetting as grams, sweat and dexterity, heated stones, the warmth floor if kept. | Opus | 08, 01 | A1.08, E1 |
| ☐ | E4 | Water: **liquids measured in millilitres** (vessels with `capacity_ml`; an aggregate that splits when spent); `fill` as a transfer of as much as fits; `pour`, `drink from`; melting snow and ice over a fire (snow:water ~10:1 loose, ~3:1 packed, ~1.1:1 ice) and against the body; eating snow at ~120 kcal of core heat per litre; **thirst on a ~3-day clock** with ~3,000 ml/day cold-and-working; **no boiling gate**; contamination as fuel/oil carried by provenance, smellable, cleanable; **steam as an entity** so condensation works for anyone who reasons to it. | Opus | 09, 18 | A1.09, E2 |
| ☐ | E5 | Food and hunger: calories as a ledger; yields per source from document 23 §4.4's real figures (kit, freight, the country by zone, the body); the valley's carrying capacity as the spine of the week; the hare cycle as a seeded run variable; rabbit starvation (protein without fat); cooking as a heat state; `throw`, `set snare`, fishing; hunger's symptoms long before death. | Opus | 10, 23 | A1.10, E1 |
| ☐ | E6 | Injury and first aid: wounds as data with bleeding/infection/frostbite clocks, `press`, `bind/wrap`, `splint`, the med pouch, the starting draws' injuries as live processes. | Opus | 11 | A1.11, E1 |
| ☐ | E7 | Events, escalation and weather: the ladder by game day, the event deck (first version) as scheduled processes with a due list and band-routed narration, hazard triggers (the cornice, thin ice, snow load off a bough), tracks that persist and decay, weather bands wired to perception and fire, snow load and the drift, the acting animals (the bear, the moose, the wolves, a few birds) and wildlife as sign; dangerous places injure, never kill outright. | Opus | 13, 01 | A1.13, E1 |
| ☐ | E8 | Rescue, as document 14 §3: the hand radio (its batteries buried in a bag in the tail, something to open it, the loose wire, any long metal raised as the antenna, the channel buttons or the written frequency, push-to-talk, the draining light, contact once the antenna is fixed); the voice on the other end (a weak language model, scaffolded, judging landmarks by the game's criteria); signals seen by physics, the plane heard first; the same flyovers every run and the default rescue on day 7; findable after the storm takes work. The ELT is broken. | Opus | 14 | A1.14, E7 |
| ☐ | E9 | The moral and social layer: ownership live (`take X from <person>` witnessed; `give X to Y`), persons as targets (`hit`, `strike`, `push`, `bind`, `carry`), speech as acts with claims checked against world state, the event log `events.jsonl` with witness lists and action tags from the ontology, the two-lie check, the five dilemma probes. | Opus | 15 | A1.15, E5, E6 |
| ☐ | E10 | Materials: the natural world (stone, soil, clay, bone, hide, sinew, punk wood, lichen, rubber…) and the missing axes (edibility on flesh, liquid axes, hardness/spark); snow and ice as state on one material. | Opus | 18 | A1.18, C2 |
| ☐ | E11 | New verbs as the loops and the docs demand them (strike, press, tape, fill, arrange, blow, sit, scrape, cover/block, push/pull/drag, throw, unscrew, warm, climb, dig dirt…); `help grammar` finalized once the forms are final; the manual page. | Opus | 04 | D2 |
| ☐ | E12 | The converter YAML → tables, run per zone when its design is finalized; the fifty outdoor zones as data, rendered and read. | Opus | 05, 01 | C2, D9 |
| ☐ | E13 | Instances and co-op: a run as one sitting (lifecycle, halt/resume, the reaper), ghosts for dead players (free movement; ghosts hear ghosts, the living do not; anyone can use out-of-character chat), the missing player's character catatonic, seed-driven slot permutation at run start, the first-class interdependence as a general concurrent-state capability (the antenna hold first), the run modes incl. NHCs (and animals played by a lightweight model), and the agent pace: the speed of typing the command (Andrew, 2026-09-27). | Opus | 19, 16, 21 | A1.19 |
| ☐ | E14 | Endings: rescued (by the radio, a signal, or surviving to the day-7 rescue) or dead; ghosts; a fuzz that proves the day-7 rescue reaches every findable party. | Opus | 21 | A1.21, E7 |
| ☐ | E17 | Exits as entities with a mode, travel time and state; movement as an attended activity with events (`walk`, `run` = less time more sweat, `climb`, `enter`, `turn back`); the tutorial rooms teach it (E19). | Opus | 03, 01 | A1.03, E1 |
| ☐ | E18 | Groups: several things sharing a place and a kind form a described group ("a pile of clothes"); `look at the pile` lists them; taking dissolves it — the composer's fifth extension. | Opus | 03 | D3 |
| ☐ | E19 | The pre-scenario tutorial *(Andrew, 2026-09-27: a series of tutorial rooms, each one simple situation showing what sort of things players can do — it needs its own design document)*: the grammar forms with one example each, the time controls (`propose fast forward`), movement, `help`; taught once, never a menu. | describer + Opus | 04, 06 | A1.04, A1.06 |
| ☐ | E20 | `make` as the aim-bridge: the parse-time rewrite (like `use X to VERB Y`), the goal table loaded from content, role-filling by capability, the vague clarification, the honest edges (means that fill no role, half-filled roles, multi-step goals); the shipped recipe reply removed; what a fire wants moves to the survival manual's page. | Opus | 04 §3.9, 07 | A1.04, E2 |
| ☐ | E21 | Quantities as budgets: counts (`take two rocks`) and measures (`a handful of`, `an armful of`, `some`, `a few`, `all the`, `as much as I can carry`) resolved against what is there and what you can carry; the world reports what you actually got; aggregates (decided) with a count and a total mass that split when one is spent or stops being interchangeable. Needs E16 and E24. | Opus | 04 §3.11 | A1.04, E16, E24 |
| ☐ | E24 | Encumbrance (decided 2026-09-18): `density` on every material row, bulk derived (mass ÷ density, authored wins); `capacity_g` and `capacity_bulk` on containers — hands, pockets, bags, worn clothing, a dragged frame; exceeding capacity answered physically, never refused; the load feeds travel time. | Opus | 18, 16, 04 §3.11, 03 §4.1a | A1.18, A1.16 |
| ☐ | E22 | The distinguishable-names gate: `make validate` fails when two reachable things in a zone share a name with no separating adjective or label (there is no numbered menu to fall back on). | Opus | 04 §3.10, 17 | A1.04 |
| ☐ | E25 | Vocabulary authored word-first: every verb and noun ships with its synonym set written in the same pass, before the loops run; the gaps log stays as the backstop. A step in the authoring guide and a `make validate` warning for a word with no synonyms. | Opus | 04 §3.7 | A1.04 |
| ☐ | E23 | The missing everyday verbs the walk-through found: `give`, `sit`/`stand`/`lie`, `wait [duration\|until <event>]`, `stop`, `look under`, `listen`/`smell`/`feel`, **`status` (the body's report: injuries, cold, hunger, thirst, tiredness, wetness — band words, never numbers; document 08 §4.9)**, `propose fast forward`. | Opus | 04, 06, 17 | A1.04 |
| ☐ | E15 | Daylight and light: the day/night cycle on the clock (the first week of October, document 13 §4.2), darkness that changes what a look shows and what searching needs, light sources (fire, the flashlight, the phone, the headlamp) with batteries that drain; powered devices as processes (the phone's clock and light, the laptop's sparks). | Opus | 13, 03, 16 | A1.13, E1 |
| ☐ | E16 | Classes that yield individuals as an engine primitive: `take a branch from the deadfall`, `take snow`, a tussock from the tussocks — a class entity mints one member with the right material, form and mass; needed by every outdoor zone. | Opus | 17, 05 | A1.17 |

### Phase F — Play, and the loop closes
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | F1 | The pure-world play harness (`tools/play.py`): a brain drives parse → resolve → apply; the per-step log (two streams: ground truth, interpretation); seeded, replayable. | Opus | 20 | B10, D2 |
| ☐ | F2 | The telnet bot player (`agent/`): a normal account, the grammar guide given once, the same text a human sees. | Opus | 20 | F1 |
| ☐ | F3 | Research runs: how a run is started and seeded, the stopping rule, the artifacts; cross-family sampling if Andrew wants it. | Fable + Opus | 20 | F1, A1.20 |
| ☐ | F4 | Agents play; every wall becomes the next pass's input (back to C); walls per run reported each morning. | overnight | 20, 22 | F1 |
| ☐ | F5 | Friends' runs: the reveal is the finished game. | Andrew | — | everything |

### Cross-cutting (holds in every phase)
- X1 Gates, probes, the ratchet, the render read: every change green; every prose change read.
- X2 Documents updated in the same commit as the work; this file's statuses too (the hook reminds).
- X3 Certainty mode B on every implementation task; the requirements reviewer on every task; the engine reviewer on `game/**`.
- X4 Memory notes for durable decisions; never for what the repo already records.

## 4. Coverage — every gap the design documents name, mapped to a task

From the 2026-09-17 inventory of the 22 documents' "what exists today", open-question and ◌ items (190
things to build). **The rule:** anything a document says is missing maps to a task above, or is listed
under "no task yet" — which must stay empty. Three tasks were added by this pass (B14, E15, E16).

| doc | what it says is missing | tasks |
|---|---|---|
| 01 | the fifty zones as data; travel durations; exposure bands; hazard triggers; tracks; the timed-beat scheduler; `probe`, `climb`, `throw`, `drag/haul`, `set snare`, `fish`; the 206 recast; wolf sign; the cornice's outcome; live verification of the nine rooms | E12, E1, E3, E7, E11, E5, D5, D9 |
| 02 | daylight/darkness; the title + Exits renderer; `press`; the ignition check; shaping; fire as a process; `cover` a body; sleep/rest/wait + being on watch; fast forward and the slow command; the deck; the ladder; weather + snow load; band-routed event narration; calorie yields and a calorie number; interdependence; `butcher`; the event log with witnesses; claims checked; confidence + weather window; the article and binding bugs; DR-08c in code; `give`; wet as grams; hydration; the play harness; the four unbuilt fire methods; the `make fire` recipe removed | E15, D4, E6, E2, D7, E1, E7, E5, E13, E9, E8, B14, B13, E3, E4, F1 |
| 03 | the four composer extensions; the walked scenarios as probes; people-line phrasing; a length budget | D3, D4 |
| 04 | unknown-word logging; `architecture/grammar.md`; final `help grammar` + the manual page; tier-4 physics replacing the verb-list redirect | B13, A6, E11 |
| 05, 22 | the ontology store and shared tables; the seed converter; the viewer; `validate-ontology`; the scaffold; the queue; the pilot pass; the lenses; the merge step; the definition of a wall; the world-builder/scout/describer agents; the firing policy | B9, B10, B11, B12, C1, C3, C5, B1 |
| 06 | `scheduler.advance` + `Activity`; `should_interrupt`; `responses/activities.py`; bedding and fatigue numbers; `keep watch`; the whitelist; the chatter cadence | E1, A5 |
| 07 | the ignition numbers; the fuel→heat curve; pricing the seven methods; `probes/graph.py`; the stub's old stage ladder reconciled | E2, A5, E8 |
| 08 | the cold clock; sweat/dexterity/movement/signal; the cold ladder numbers (document 13 §4.2); shelter as zone numbers and building operations; `huddle`; `cover/block`; snow as building material; `sit`; per-region frostbite; heated stones; `status` (or its refusal) | E3, E7, E11, D4 |
| 09 | `water.py`; `fill`; `boil`/`gather`/`filter`/cleaning; volume in ml and `pour into`; the safety model; melt as a process | E4 |
| 10 | cooking as heat state; spoilage/storage/scavengers; `clean`/`prepare`; the bodies model; raven, fox and bear pressure; ration tuning | E5, E7, D7, A5 |
| 11 | the injury clock; `splint`/`stitch`/`clean`/`treat`; world-inflicted injuries; `carry`; wounds gating capability; painkiller masking; unreliable description; `examine <someone>` showing wounds | E6, E11 |
| 12 | the death clock + alive start; the moaning event; the clue fragments; tending; body states; the `authored.py` packet; the dilemma probe | D7 |
| 13 | `weather.py`; the ladder/deck as a probe table; `events.md` + DR-30; weather driving perception; an escape path per lethal card | E7, A6 |
| 14 | `rescue.py::confidence`; the radio machine; the ELT score; the weather-window gate; `rescue.def` + `AUTHORED`; the missing objects; `signal with`; the weights; the dooryard cable | E8, A5 |
| 15 | ownership live; persons-as-targets verbs; `moral.py`; `probes/dilemmas.py`; `architecture/moral-social-layer.md`; the five dilemmas; the two-lie check; tag fields on ontology rows | E9, A6, B9 |
| 16 | seed-driven slot permutation; the bag extras; the phone battery process | E13, D5, E15 |
| 17 | `look under`; the elusive sensory layer; the class-yields-individuals primitive; the authoring-rules promotion; the render read | D5, D8, E16, A6, D9 |
| 18 | natural materials (stone, soil, clay first); edibility on flesh; liquid axes; snow/ice as state; hardness/spark/ember/elasticity axes; the stale forms table | E10, A6 |
| 19 | the instance lifecycle and reaper; the interdependence capability; muffle edges; movement durations spent; a rate cap; the offline clock policy | E13, D6, E1 |
| 20 | `tools/play.py` + `agent/runner.py` + `client.py`; the brains; the log schema; replay; the research-run entry point; activation capture; the `@OBS` line removed from `bot-harness.md` | F1, F2, F3, B5 |
| 21 | the two endings (rescued or dead) as end conditions; deaths, persisting bodies and ghosts; the fuzz that every run ends | E14 |

**No task yet:** none.

## 5. The current decisions (the reference every document is checked against)

Andrew's decisions, in plain words, with the date each was made. Where Andrew left the choice to Claude,
it says so. When a decision changes, this list and every document it touches change together.

**What it is**
- Two purposes, both first-class: a model world for research — a language model acts in it freely through
  the same taught grammar a person uses, and its behaviour and activations are studied — and a new kind
  of MUD for friends. Runs are for friends, for humans with agents, and for agents only. (2026-09-16)
- The world is open-ended: any entity or relation a person would reasonably try; every count is a floor;
  the loops grow it. Every goal has **several ways**, with no set number; clues are what a realistic world
  holds, plus some added to help players. (2026-09-16, 2026-09-27)
- Never a menu: the game never lists options or names a verb the player did not type. Feedback is a
  clarification or the physics of why, and **common sense is hinted** in the world's voice. (2026-09-16,
  2026-09-27)
- The engine is deterministic and never calls a language model. Models play characters from outside, as
  players: survivors, non-human characters, animals, the voice on the radio. **One exception:** the
  radio voice judges whether it has been told enough to find the party, by criteria the game gives it.
  (2026-09-17, 2026-09-27)
- Design first: nothing is built and no loop runs until the design documents are finalized. The design is
  a work in progress; every system has its own document; **one GDD**. (2026-09-16, 2026-09-17, 2026-09-27)

**The setting**
- A Cessna 206-class single with a four-seat interior (1A, 1B, 2A, 2B and the right seat), a hat shelf,
  a cargo net and a jammed cargo door. The plane's battery is in the nose, wired and fine. (2026-09-16,
  2026-09-27)
- The whole valley — all fifty outdoor zones and all eleven regions, each with a reason to come back —
  is in the first complete run. (2026-09-16, 2026-09-17)
- **The season: the first week of October in interior Alaska** (Claude's choice, at Andrew's request,
  for more than ten hours of daylight). An inch of snow at the start, bushes dusted but visible, berries
  and roots findable, skim ice on still water; light snow on days 1–2, the storm on days 3–4, clearing
  after. **The same weather every run.** (2026-09-26, 2026-09-27)
- **The party:** up to five play (four adults and the kid). A seat nobody plays is a dead character whose
  clothes and pockets can be searched; AI agents may play seats. No back stories: characters differ in
  clothes, injuries and what they carry, and in how well and how fast they do things (a woodsman lights
  fires better; a technically proficient character sees a fault in a device). (2026-09-16, 2026-09-27)
- **The pilot starts the run dead.** He carries no clues. His body is food, and eating it is taboo, not
  immoral. (2026-09-17, 2026-09-27)
- **What is aboard:** the survival kit is not at hand — it is buried somewhere; the sleeping bag is
  buried with the tail wreckage; two blankets are hidden inside the plane; no firearm. Not too easy, not
  too hard. (2026-09-27)
- **Holt's cabin** is supplies: some trapline gear and modest stores, not piles of food. Walking out is
  not an ending. (2026-09-17, 2026-09-27)
- **Wildlife:** the bear, some bigger animals and a few birds act — on the engine's behaviour rules, or
  played by a lightweight model; fewer than three birds in a room, not constantly calling; the fish are
  scripted; other wildlife shows as events and sign; no wolverine. Claude proposes the list (document 23,
  for Andrew's check). Flora and fauna are filtered by ecology — this habitat, this month, real numbers.
  (2026-09-17, 2026-09-18, 2026-09-26, 2026-09-27)

**Time and the run**
- The clock runs continuously at **15 game-minutes per real minute**. **Fast forward** (proposed and
  agreed by the players) runs it at about **150×**; awake players can stay in it, seeing events faster,
  and type a command to slow it when they want to act. A player waking or any non-ambient event drops it
  back to 15×; ambient events do not. Sleeping players can chat out of character to pass the time. The
  numbers are tuned by playtesting. (2026-09-17, 2026-09-27)
- A run is one sitting of two or three hours — about a week of game time — which the players can pause
  and return to. A missing player's character goes catatonic, sits down and stares; the others can keep
  them alive, and they can die. (2026-09-17, 2026-09-27)
- Small attended jobs take one to three game-minutes; bigger ones take honest durations. Ambience comes
  from the things present, each with its own rhythm. Being awake is being on watch. The commands that
  don't interrupt an activity: look, examine, inventory, speech, help, status. Build order: scheduler →
  fire → warmth → hunger and thirst → injury → the pilot's body and `status`. (2026-09-18)
- **Endings: rescued or dead.** The run ends when they die, of anything. Dead players are ghosts: they
  move and use out-of-character chat; ghosts hear ghosts, the living cannot; anyone can use the
  out-of-character chat. **No recap.** (2026-09-17, 2026-09-26, 2026-09-27)

**What kills, and what hurts**
- **Death comes from blood loss, the bear and the cold.** Poison makes people very sick but never kills;
  other harms — infection, carbon monoxide and the rest — make them weak and sick. Dangerous places
  injure but never kill outright; fitness matters; a seeded dice roll, announced. (2026-09-17,
  2026-09-27)
- No gate on violence: it resolves with real physics, and there is a **combat system like a MUD's**.
  (2026-09-16, 2026-09-26)
- Hunger works as it does in real life. (2026-09-26)
- Water: liquids are measured in millilitres; eating snow costs body heat; there is no boiling gate;
  contamination means fuel and oil, carried as provenance; steam is an entity; `fill` moves as much as
  fits. (2026-09-18)
- Warmth: no guaranteed floor — night one is survivable inside the wreck in the clothes they crashed in;
  from night two they need a heat source, better gear, conserving or huddling. A `status` screen reports
  the body in words. The wreck's openings are heard (the wind through the tear). Layering, huddling, the
  extremities' own cold, covering openings, sweat, and heated stones are in. (2026-09-18)
- **Heat is a state system**: heat on every entity, body parts included; a fire heats its area and leaves
  residual heat around it; the plane is an entity with openings, open or closed, and an internal heat.
  Food changes with heat — raw, cooked, spoiled — and there is spoiled food and there are poisonous
  mushrooms. Hunting, trapping, fishing and killing are real operations, each variant its own.
  (2026-09-26)
- Fire: the code's 26 forms are canonical; the seven methods are priced by what they cost; the design's
  stage ladder stands; Claude drafts the ignition weights and the fuel-to-heat curve. (2026-09-18)

**The player's view and the grammar**
- The look: a title line, prose composed from state, people and animals as prose, exits as entities in
  prose; no item list; groups; a blank line before events; colour for human players only. An agent sees
  exactly what a human sees. (2026-09-16, 2026-09-17)
- `make` is the one aim-verb; `use X on Y` is silent; the forms are finalized before the loops run;
  vocabulary is written word-first with its synonyms; every line is in the world's voice; quantities are
  budgets (a handful, some, all); a gathered quantity is one aggregate; inventory is limited by weight and
  space, and bulk comes from density; distinguishable names are enforced. (2026-09-18)
- The tutorial is a series of rooms, each one simple situation that shows what sort of things players can
  do; nothing else is explained. (2026-09-27)

**The ontology and the loops**
- The store is `docs/ontology/` as YAML; the schema is designed in full up front; the two models build it
  as peers and the merge never drops; walls per run are counted in five categories; goal lenses plus human
  lenses. (2026-09-16, 2026-09-18)

**Rescue** (document 14 §3) — three ways: the radio, a signal a plane can see, surviving long enough.
- **The ELT is broken.** (2026-09-27)
- **The radio:** a hand radio in the plane's cabin; its batteries are buried in a bag in the tail section. You need
  something to open it; a loose wire inside is seen at once by a technical character and found more
  slowly by anyone else, with a hint. The antenna is anything metal and long enough, raised — higher is
  better, and a poor match only weakens the signal. Flip through the channel buttons or find the written
  emergency frequency; hold the button to talk. The batteries drain with use, and the light dims.
  Contact comes fairly quickly once the antenna is fixed — not only during flyovers. (2026-09-17,
  2026-09-18, 2026-09-27)
- **The voice:** a person at search and rescue, played by a weak language model — the same model every
  run, scaffolded with rules. It helps only as a real rescuer would, may hint (raise the antenna) through
  the bad signal, asks for landmarks and judges them by the game's list and values, says they will come
  once the storm dies down, and tells a party that cannot be found what it needs to do. A party that
  cannot say where it is can be homed in on, at a battery cost (Claude's choice). (2026-09-27)
- **Signals:** fire and smoke (rubber, oil, green boughs), a piece of mirror once clear of the trees,
  burning the cabin during a flyover. Whether a crew sees a signal follows physics — contrast, weather,
  how close the pass comes (Claude's choice). The plane is heard before it is seen; a party may not make
  it in time. (2026-09-17, 2026-09-27)
- **Surviving long enough:** search and rescue is searching; **the same flyovers every run**; **the
  default rescue is day 7**; being findable after the storm takes work. The rest of the schedule is
  Claude's (document 13 §4.2). No boats. (2026-09-17, 2026-09-27)

**Agents**
- An agent acts at the speed of typing its command; a slow model is simply slow. The models: a fast one
  (Haiku or Sonnet, low to medium reasoning) and Andrew's own open-weight model, which needs timing;
  activations may be collected in runs with humans if it is fast enough. (2026-09-26, 2026-09-27)

**Documents**
- One GDD; the old seed design and the investigation scratchpads are removed from the repository (git
  keeps them). Documents present the current design only, never quote the conversation, and every
  decision is carried to every document it touches. (2026-09-27)

### Open with Andrew
- **The trapper coming back** — on the fence; Claude recommends against it (the cabin would become a
  waiting room) and suggests his traces instead: gear, and a calendar showing he returns after the week.
- **Thirst** — decided 2026-09-18 as killing on a realistic three-day clock; the 2026-09-27 rule names
  blood loss, the bear and the cold as what kills. Does thirst kill, or weaken? Claude recommends it can kill: it is a slow clock with an answer always at hand (snow, the creek), not an accident like the mushroom (document 09 §6).
- **Document 15's moral rules** — to be presented, one at a time.
- **The other historical folders** (`docs/proposals/`, `docs/architecture/review/`, the June
  `roadmap.md`, the room censuses) — the same treatment as the investigation folder?

## 6. How this plan is maintained

- **One list.** A task exists here or it does not exist. `BACKLOG.md` shows the Now slice only.
- **Every commit** that changes status updates this file (the commit hook lists it when code is staged).
- **Every review decision** updates §5 and may add or remove tasks in §3.
- **Every loop firing** (Phase C) may add tasks via the feedback rule (C4): a new food source, material,
  verb or system named by an agent becomes a proposal in its design document and, if it needs code, a
  task in Phase E with the design doc named.
- **Nothing is built before its design document is finalized**, except Phase B (the machine).
- A task marked ⊘ names the decision it waits on; the decision is in §5 with the doc that holds it.
