# PLAN — the program: every task, tracked

> **Status: LIVING — the single task list for the whole project (created 2026-09-17).** Every task we
> know of is here, with a status, the design document that owns it, and what it waits on. It is updated
> in the same commit as the work (the commit hook reminds). `BACKLOG.md` is only the *Now* slice of
> this file. `docs/scenarios/whiteout/roadmap.md` (the June P0–P7 arc) is history.
> Statuses: ☐ not started · ◐ in progress · ☑ done · ⊘ waiting on a decision (named).

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
| ☐ | A1.00 | GDD umbrella — reviewed and finalized | Andrew + Fable | GDD | — |
| ☐ | A1.01 | 01 premise and world — reviewed and finalized | Andrew + Fable | 01 | — |
| ☐ | A1.02 | 02 the experience — reviewed and finalized | Andrew + Fable | 02 | — |
| ☐ | A1.03 | 03 the player view — reviewed and finalized | Andrew + Fable | 03 | — |
| ☐ | A1.04 | 04 grammar and feedback — reviewed and finalized | Andrew + Fable | 04 | — |
| ☐ | A1.05 | 05 ontology and sufficiency — reviewed and finalized | Andrew + Fable | 05 | — |
| ☐ | A1.06 | 06 time, sleep and the clock — reviewed and finalized | Andrew + Fable | 06 | — |
| ☐ | A1.07 | 07 fire and shaping — reviewed and finalized | Andrew + Fable | 07 | — |
| ☐ | A1.08 | 08 warmth, clothing and shelter — reviewed and finalized | Andrew + Fable | 08 | — |
| ☐ | A1.09 | 09 water — reviewed and finalized | Andrew + Fable | 09 | — |
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
| ☐ | A1.21 | 21 endings and recap — reviewed and finalized | Andrew + Fable | 21 | — |
| ☐ | A1.22 | 22 the world-building loops — reviewed and finalized | Andrew + Fable | 22 | — |
| ☐ | A2 | The cross-document decisions the docs flag (see §5): the walk-out as ending vs channel (14/21); four routes vs five (01/14); the forms list (07/18); the warmth floor (08); the run's food yields (10); the event deck's first version (13); "still going" (13/21). | Andrew | 01, 07, 08, 10, 13, 14, 18, 21 | A1 |
| ☐ | A3 | Record every review decision: the doc's review log, the DR register (amendments), `VISION.md` where a non-negotiable moves. | Fable | — | A1 |
| ☐ | A4 | Re-price the valley for a week-long run (travel, stay-or-go, the ladder): the July map assumed a five-hour day. | Fable → doc 01 + 13 | 01, 13 | A1.01, A1.13 |
| ☐ | A5 | First-pass numbers as proposals where the docs have none: food yields per source (10), water paths (09), injury clocks (11), the warmth/bedding numbers (06/08), the ignition and fire-ladder numbers (07), rescue confidence weights (14). Proposed in the sittings, tunable by probes later. | Fable | 06–11, 14 | A1 |
| ☐ | A6 | Promote finalized mechanisms into their architecture counterparts: `architecture/grammar.md`, `presentation.md` v2, `events.md`, `time-and-stakes.md`, `moral-social-layer.md`, `fire-and-shaping.md`, `rescue.md`; DR-29/30 appended. | Fable | 03, 04, 06, 07, 13, 14, 15 | A1 |
| ☐ | A7 | The GDD's per-system sections pointed and corrected where the seed text is wrong (§31–36 came from the archived AI seed; §19; §9). | Fable | GDD | A1 |

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
| ☐ | B9 | The ontology store: `docs/ontology/` YAML schema + `docs/ontology/README.md` (provenance required; a row is never deleted, only superseded); `make validate-ontology`. | Fable (schema) → Opus | 05 | — |
| ☐ | B10 | The seed converter `tools/ontology_seed.py`: the built tables and the nine censuses → the first YAML files (✅ built / 📐 designed), so the store exists before any agent runs. | Opus | 05 | B9 |
| ☐ | B11 | The viewer `tools/ontology_view.py`: a static site — the world map, per-region and per-room pages, counts, what changed since last firing; publishable as an Artifact. | Opus | 05 | B10 |
| ☐ | B12 | The loop scaffold `docs/guides/world-building.md` (world-builder and scout briefs; the goal lenses) and the queue `docs/investigation/world/loop-queue.md` (zone × phase × model). | Fable | 22 | — |
| ☐ | B13 | The clarification-only feedback in code (DR-08c): no verb suggestions, no numbered menus, `help verbs` gone, `make`/bare `use` clarify, `use X on Y` silent, the near-miss hint gone, bare `go` no longer lists exits' targets beyond the Exits line, unknown words logged to the wall-sensor; **tier-4 physics answers from properties replace the verb-list redirect**; probes re-authored to name nouns. | Opus implementer | 04, 05 | A1.04 |
| ☐ | B14 | Shipped narration and binding bugs (found by running the sample week): the article doubler ("the the pilot", "a leather gloves"), `the fire` binding the extinguisher, bare `bin` binding the far bin, `cover X` folding to `wrap`. Bug fixes, not design. | Opus implementer | 03 | — |

### Phase C — The world-building loops: the design grows (exit: every zone has both passes; additions flowed back)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | C1 | The pilot pass: the mid cabin by the world-builder on Sonnet and on Opus, merged; the first viewer page; read together; the scaffold, schema and queue fixed from what we learned. | both models → Andrew + Fable | 22 | Phase A exit, B9–B12 |
| ☐ | C2 | Ontology passes over every zone (the nine built first, then the fifty): entities, materials, what each could turn into, relations, candidate commands; merged with provenance. | both models, overnight | 22, 05 | C1 |
| ☐ | C3 | Possibility passes: a survivor in a situation, one goal lens at a time (fire · food · water · warmth · shelter · signals · rescue · injury · the pilot · the party · others), everything they would try as commands. | both models, overnight | 22 | C2 |
| ☐ | C4 | **The feedback rule, run after every firing:** each addition that names a new food source, material, verb, relation, hazard or system goes into the owning design document as a proposal AND becomes a task here (Phase E) if it needs code. Synonyms → the phrasing probes. | Fable (morning read) | all | C2 |
| ☐ | C5 | Walls per run defined and measured once agents play (Phase F); the categories kept separate. | Fable | 20, 22 | F1 |

### Phase D — The cabin zone done right (exit: one zone of the plane plays end to end to the finalized design)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | D1 | Finalize the cabin zone's design from its ontology (the mid cabin as the exemplar); the room-authoring rules for the loops. | Andrew + Fable | 17, 16 | C1 |
| ☐ | D2 | The implementation plan for the zone (plan mode): objects, verbs, phrases, probes; the new-verb spike (how easy is a new verb inside the grammar; does the grammar need expanding). | Fable → Opus | 04, 17 | D1 |
| ☐ | D3 | The description model v2: the four composer extensions (relations rendered on the parent; generic state overlays; zone/space state variants via an additive zone-facts effect; range conditions), the walked scenarios as failing probes first, a certainty audit, then built. | Opus | 03 | A1.03 |
| ☐ | D4 | The look: the title line, people present, the `Exits:` line (compass outdoors; fore/aft/up/out inside). | Opus | 03 | D3 |
| ☐ | D5 | The 206 interior as content: seats 1A/1B/2A/2B + the right seat with their finds; the hat shelf; the cargo net; the jammed cargo door; the finds redistributed from the six-seat draft; `look under` as the seat reveal; the guide's and nurse's missing bag extras. | describer + Opus | 16, 17 | A1.16 |
| ☐ | D6 | Multi-zone perception verified against doc 19 (see and talk across zones; hear by loudness); the propagator's weather stub. | Opus | 19 | A1.19 |
| ☐ | D7 | The pilot as a process: alive at first light, mumbling a clue fragment or two (each fact with ≥3 other paths), heard only in the cockpit, dies within the first day; tending as costed acts; the body afterwards (`cover` as reverence, search, `butcher`, buried, findable); the `pilot_body` dilemma probe. | Opus | 12, 15 | A1.12 |
| ☐ | D8 | Elusive nouns and sense verbs (cold, draft, light, smell, sound; smell/listen/feel) as a generic mechanism, proven on one room. | Opus | 17, 05 | D1 |
| ☐ | D9 | Render read and voice sign-off on the cabin (Andrew reads the rendered zone whole). | Andrew | 17 | D3–D8 |

### Phase E — The systems, built to the finalized designs (each item: probes first, certainty mode B, the reviewer pair)
| status | id | task | owner | design doc | waits on |
|---|---|---|---|---|---|
| ☐ | E1 | Time: the activity scheduler on the heartbeat (attended actions with start/tick/interrupt/complete; unattended processes; `responses/activities.py`), sleep and wait, the 20× consensus advance with event interrupts, the watch; travel and movement durations actually spent per edge. | Opus | 06, 01 | A1.06 |
| ☐ | E2 | Fire: the ignition model (source × receptivity × form thinness; a branch does not take from a lighter), fire as a process (the stage ladder; the stub's old ladder reconciled), the shaping family (`carve/split/shave/whittle/notch/string/bundle`), the seven methods as probe chains. | Opus | 07 | A1.07, E1 |
| ☐ | E3 | Warmth, clothing, shelter: the cold clock (regions, wet fraction, wind), huddle, shelter as zone properties (per-zone exposure bands in `zones.py`; wind and roof numbers written by built things: `cover/block` an opening, snow walls, boughs), drying and wetting as grams, sweat and dexterity, heated stones, the warmth floor if kept. | Opus | 08, 01 | A1.08, E1 |
| ☐ | E4 | Water: vessels and liquids (fill / pour / drink from), melting, boiling, contamination, eating snow costs heat. | Opus | 09 | A1.09, E2 |
| ☐ | E5 | Food and hunger: calories as a ledger, yields per source (kit, freight, the country by zone, the body), cooking as heat state, `throw`, `set snare`, fishing; hunger's symptoms before death. | Opus | 10 | A1.10, E1 |
| ☐ | E6 | Injury and first aid: wounds as data with bleeding/infection/frostbite clocks, `press`, `bind/wrap`, `splint`, the med pouch, the starting draws' injuries as live processes. | Opus | 11 | A1.11, E1 |
| ☐ | E7 | Events, escalation and weather: the ladder by game day, the event deck (first version) as scheduled processes with a due list and band-routed narration, hazard triggers (the cornice, thin ice, snow load off a bough), tracks that persist and decay, weather bands wired to perception and fire, snow load and the drift, wildlife as sign and pressure (ravens, the wolverine, wolves), an escape path documented per lethal card. | Opus | 13, 01 | A1.13, E1 |
| ☐ | E8 | Rescue: confidence arithmetic and the weather window, the radio state machine and antenna quality, the ELT score, signals (smoke, the mirror, the flare, a ground sign; `signal with <reflector>`), the missing objects (the survival mirror, the tire, the aircraft battery, the wing drains, a spark rock; the dooryard cable as a real second conductor), the walk-out, the rescue graph as probe chains (`probes/graph.py`), the solvability oracle. | Opus | 14 | A1.14, E7 |
| ☐ | E9 | The moral and social layer: ownership live (`take X from <person>` witnessed; `give X to Y`), persons as targets (`hit`, `strike`, `push`, `bind`, `carry`), speech as acts with claims checked against world state, the event log `events.jsonl` with witness lists and action tags from the ontology, the two-lie check, the five dilemma probes. | Opus | 15 | A1.15, E5, E6 |
| ☐ | E10 | Materials: the natural world (stone, soil, clay, bone, hide, sinew, punk wood, lichen, rubber…) and the missing axes (edibility on flesh, liquid axes, hardness/spark); snow and ice as state on one material. | Opus | 18 | A1.18, C2 |
| ☐ | E11 | New verbs as the loops and the docs demand them (strike, press, tape, fill, arrange, blow, sit, scrape, cover/block, push/pull/drag, throw, unscrew, warm, climb, dig dirt…); `help grammar` finalized once the forms are final; the manual page. | Opus | 04 | D2 |
| ☐ | E12 | The converter YAML → tables, run per zone when its design is finalized; the fifty outdoor zones as data, rendered and read. | Opus | 05, 01 | C2, D9 |
| ☐ | E13 | Instances and co-op: instanced runs persisting across sittings (lifecycle, the reaper), the empty-instance and disconnect clock rules, seed-driven slot permutation at run start, the first-class interdependence as a general concurrent-state capability (the antenna hold first), the run modes and an agent action-rate cap. | Opus | 19, 16 | A1.19 |
| ☐ | E14 | Endings and the recap: the four endings, dead players, the recap from the event log; a fuzz that proves no party survives past day N unrescued. | Opus | 21 | A1.21, E7 |
| ☐ | E15 | Daylight and light: the day/night cycle on the clock (December's five hours), darkness that changes what a look shows and what searching needs, light sources (fire, the flashlight, the phone, the headlamp) with batteries that drain; powered devices as processes (the phone's clock and light, the laptop's sparks). | Opus | 13, 03, 16 | A1.13, E1 |
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
| 01 | the fifty zones as data; travel durations; exposure bands; hazard triggers; tracks; the timed-beat scheduler; `probe`, `climb`, `throw`, `drag/haul`, `set snare`, `fish`; the 206 recast; wolf/wolverine sign; the cornice's outcome; live verification of the nine rooms | E12, E1, E3, E7, E11, E5, D5, D9 |
| 02 | daylight/darkness; the title + Exits renderer; `press`; the ignition check; shaping; fire as a process; `cover` a body; sleep/rest/wait + the watch; the 20× advance; the deck; the ladder; weather + snow load; band-routed event narration; calorie yields and a calorie number; interdependence; `butcher`; the event log with witnesses; claims checked; confidence + weather window; the article and binding bugs; DR-08c in code; `give`; wet as grams; hydration; the play harness; the four unbuilt fire methods; the `make fire` recipe removed | E15, D4, E6, E2, D7, E1, E7, E5, E13, E9, E8, B14, B13, E3, E4, F1 |
| 03 | the four composer extensions; the walked scenarios as probes; people-line phrasing; a length budget | D3, D4 |
| 04 | unknown-word logging; `architecture/grammar.md`; final `help grammar` + the manual page; tier-4 physics replacing the verb-list redirect | B13, A6, E11 |
| 05, 22 | the ontology store and shared tables; the seed converter; the viewer; `validate-ontology`; the scaffold; the queue; the pilot pass; the lenses; the merge step; the definition of a wall; the world-builder/scout/describer agents; the firing policy | B9, B10, B11, B12, C1, C3, C5, B1 |
| 06 | `scheduler.advance` + `Activity`; `should_interrupt`; `responses/activities.py`; bedding and fatigue numbers; `keep watch`; the whitelist; the chatter cadence | E1, A5 |
| 07 | the ignition numbers; the fuel→heat curve; pricing the seven methods; `probes/graph.py`; the stub's old stage ladder reconciled | E2, A5, E8 |
| 08 | the cold clock; sweat/dexterity/movement/signal; the December ladder numbers; shelter as zone numbers and building operations; `huddle`; `cover/block`; snow as building material; `sit`; per-region frostbite; heated stones; `status` (or its refusal) | E3, E7, E11, D4 |
| 09 | `water.py`; `fill`; `boil`/`gather`/`filter`/cleaning; volume in ml and `pour into`; the safety model; melt as a process | E4 |
| 10 | cooking as heat state; spoilage/storage/scavengers; `clean`/`prepare`; the bodies model; raven/wolverine pressure; ration tuning | E5, E7, D7, A5 |
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
| 21 | the four endings as end conditions; deaths and persisting bodies; the recap; the survive-past-day-N fuzz | E14 |

**No task yet:** none.

## 5. Decisions Andrew must make (tracked; each with the doc and status)

| status | decision | doc | note |
|---|---|---|---|
| ☑ | The pilot: alive at first light, mumbles a clue fragment or two, dies within the first day. | 12 | 2026-09-17 |
| ☑ | The run was always a week; the one-day wording struck everywhere live. | 19, GDD | 2026-09-17 |
| ⊘ | The walk-out to the cabin: its own ending, or one way of being found? | 14, 21 | at the sitting |
| ⊘ | Four routes or five channels (visual as its own account)? | 01, 14 | at the sitting |
| ⊘ | The forms list: the code's 26 words canonical, the closure table updated? | 07, 18 | at the sitting |
| ⊘ | The warmth floor: keep (a fire-less night is survivable by huddle + fuselage) or drop? | 08 | at the sitting |
| ⊘ | The event deck's first version: full or a subset? "Still going" with no cutoff? | 13, 21 | at the sitting |
| ⊘ | Which regions earn their place; the muskeg; the density gradient. | 01 | at the sitting |
| ⊘ | Player count per run; the first-class interdependence; the empty-instance clock. | 19 | at the sitting |
| ⊘ | What is logged per step; cross-family sampling; the stopping rule for agent runs. | 20 | at the sitting |
| ⊘ | The non-interrupting command whitelist; the step-3 build order (defaults proposed). | 06 | at the sitting |
| ⊘ | Which fire stage ladder (the design's, or the stub's older one); which temperature curve (the December ladder over the GDD's June line); the radio state's spelling — mine to reconcile, his to confirm. | 07, 13, 14 | at the sittings |
| ⊘ | Per-goal path minimums (≥3 everywhere vs the roadmap's ≥4 for rescue); the nurse's knowledge (nothing mechanical vs a skill). | 14, 11 | at the sittings |
| ⊘ | Every other open question in the 22 documents, in their order (130 in the 2026-09-17 inventory). | all | at the sittings |

## 6. How this plan is maintained

- **One list.** A task exists here or it does not exist. `BACKLOG.md` shows the Now slice only.
- **Every commit** that changes status updates this file (the commit hook lists it when code is staged).
- **Every review decision** updates §5 and may add or remove tasks in §3.
- **Every loop firing** (Phase C) may add tasks via the feedback rule (C4): a new food source, material,
  verb or system named by an agent becomes a proposal in its design document and, if it needs code, a
  task in Phase E with the design doc named.
- **Nothing is built before its design document is finalized**, except Phase B (the machine).
- A task marked ⊘ names the decision it waits on; the decision is in §5 with the doc that holds it.
