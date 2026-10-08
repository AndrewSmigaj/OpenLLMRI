# One MUD in one app — architecture

> **Status: reviewed by Andrew, round 1 (2026-10-06).**
> - **Kept, with round 1's changes applied:** sections 1–4 and 6–10.
> - **Rewritten from his review:** section 5.
> - **Answered:** the open questions (section 11).
> - **New:** section 12, the end state. It records his decisions and marks Claude's proposals that still
>   wait for his ruling.
>
> This document replaces the MUD sections of [`../architecturemud.md`](../architecturemud.md). The
> research software (studies, lenses, tools, interventions, the AI scientists) is designed in
> [`../DESIGN.md`](../DESIGN.md) (approved 2026-10-08), which also holds this document's user-facing
> parts: what the MUD is for, its rooms and its commands (Part F). This one covers how the MUD is
> built and how it joins the app.

## 1. Purpose

Open LLMRI is an instrument for modelling how Mixture-of-Experts language models represent and process
meaning, with visualization first. It always works with MoE models: gpt-oss-20b first, others later.

**The MUD is the instrument's engine for multi-step processes.** Evidence arrives over steps, the model
reasons and acts, and the ground truth is known at every step, so you can watch internal
representations change, not only read them from a single sentence. It is also where people visit the
institute: its labs, its simulator and, later, its AI scientists.

One MUD hosts three kinds of scenario:
- **free-form worlds,** each with its own goals. Winter Survival is the first of many; it was called
  Whiteout until 2026-10-06.
- **staged scenarios,** such as the friend/foe situations at the bus stop;
- **sentence-set probes,** run from a lab.

The MUD is one tool among many. Sentence sets, and even single words fed to the model, stay first-class
ways to study it.

## 2. The pieces and where they run

| Piece | What it is | Where it runs |
|---|---|---|
| `backend/` | FastAPI: gpt-oss with capture hooks, the data lake, the analysis endpoints, the agent loop | the host, on the GPU; Python 3.10.12 from `backend/requirements.lock.txt` |
| `mud/` | the one MUD: Evennia 6 with Postgres, from Winter Survival's foundation | Docker; Python 3.13 in a digest-pinned image |
| `frontend/` | the React app: the research view (terminal and visualizations), the labs | the browser, served by Vite |
| later | a workbench API (no GPU) for world building; the exploration engine | the host |

**How the pieces talk:**
- the app talks to the backend over HTTP;
- the app and the backend's agent loop each talk to the MUD over its websocket;
- the backend never imports MUD code, and the MUD never imports backend code.

## 3. The target layout

```
OpenLLMRI/
  backend/                  FastAPI, gpt-oss, capture, lake, analysis + tests/
  frontend/                 React app
  mud/                      the one MUD: Evennia 6 game dir, Docker, its Makefile, docs, tools
    game/typeclasses/       plain shared bases + winter_survival/ + staged/ + institute/
    game/commands/          the base command (sends the prompt) + winter_survival/ + staged/ + institute/
    game/world/sim/         the free-form worlds' pure engine (unchanged, still gated)
    game/world/scenarios/winter_survival/
    game/world/staged/      the staged engine: loader, schema, multi-stage rooms
    game/world/institute/   hub, labs, simulator
    game/server/conf/inputfuncs.py   the control channel
    docs/                   Winter Survival's design docs (its GDD) and the MUD's own architecture
  data/scenarios/<set_id>/  the scenario library (section 5): one copy, read by the MUD and the backend
  data/sentence_sets/
  data/labs/                lab presets, e.g. the polysemy lab's view
  data/lake/                kept sessions and new captures (git-ignored)
  data/models/gpt-oss-20b -> ~/models/gpt-oss-20b
  docs/architecture/one-mud.md
  .github/workflows/        mud.yml, backend.yml, frontend.yml (path-filtered)
  .githooks/                one pre-commit, per-area checks
  Makefile                  one entry point
```

**Why `mud/`, not `winter_survival/`:** the Evennia game becomes the institute's MUD, and Winter
Survival is one world in it. It is imported with `git filter-repo`, so `git log -- mud/<file>` shows
every earlier commit.

## 4. Areas in one MUD

- **Every room belongs to one area:** the institute, a free-form world, or a staged scenario.
- **The room a character stands in decides three things, through three hooks** (DR-29 in Winter
  Survival's register):
  - **which commands apply:** a room names its area's character command set (`character_cmdset`),
    and the character makes it its default while there, so walking from one area to another changes
    what you can type. A room can also pick the set per character (`character_cmdset_for`): a staged
    scenario's room gives its player the scenario's commands and anyone else a watcher's. A
    room-carried command set merged over the stock one does not work: Evennia treats commands as
    duplicates only when their keys match, so stock commands that share only an alias (`get`,
    `examine`) stay beside the area's;
  - **how a character looks:** the room's `render_character`;
  - **which typed lines it claims first:** before any command runs, the room may claim the line
    (`claim_input`). A staged scenario's room claims a line that is one of the open actions, so an
    action wins over a command that shares its verb (`give`, `help`, …). Every other line runs as a
    command.
- **The institute is plain Evennia.** Every institute room tells the app where you are with
  `room_entered {room_type, role}`, as the old prototype's rooms did; the app's toolbar uses both
  fields. Arriving sends it, and so does logging in inside the room; leaving sends `room_left
  {room_type}`. The role is `researcher` for Builder accounts and `visitor` otherwise.
  - **the hub** (`room_type: hub`) is the start room, with exits to the polysemy lab and the
    simulator;
  - **a lab** (`micro_world`, the app's name for a room that fixes the session shown) adds its preset
    from `data/labs/<name>.yaml`: `session_id`, `clustering_schema` and `viz_preset`, read on every
    entry. The polysemy lab shows `tank_polysemy_k6_n20` of `session_1434a9be`;
  - **the simulator** (`simulator`): `simulator` lists the library's sets, or one set's scenarios;
    `simulate <set>[/<subset>] [<scenario>]` loads a staged scenario and shows what the agent sees at
    its start, the room, the inventory and the choices (`leave` comes back); or it enters a world
    through its package's `build.start_room()`. `agent run <set>[/<subset>] [<scenario>]` asks
    the backend to play scenarios with the model, and `agent stop` stops it (section 6). Visitors
    browse; researchers load and run agents.
  - `world/institute/build.py` builds them, idempotently: `make institute`, and on a new database's
    first start.
- **Guests** (`connect guest`) are visitors and arrive in the hub.
- **Watching.** In any institute room, `watch <name>` follows a character into each scenario
  instance it loads and back out; `unwatch` returns to where watching started. In a scenario's room a
  watcher can look, examine and list the actions, and reads every line the player types. It can't
  act or speak there: only the player's typed lines are claimed as actions, and anything said in the
  room would reach the player's observation, an agent's prompt. Following into a world waits for a
  world observer mode.
- **A world's own rules hold inside that world only.** For Winter Survival: the taught grammar, the
  world's feedback, never a menu. The simulator room is a menu on purpose.
- **Characters cross areas,** so a world's body state applies only inside it.
- **The engine's gates** (pure core, no raw writes, no raw output, doc consistency) cover the world
  code they were written for. The institute and staged code have their own tests.

## 5. Scenario sets and the staged engine

**The library.** Scenarios are datasets, like sentence sets. A set is designed for a study by varying
some things and holding others fixed. Other studies reuse a set, or build their own.
- **Each set has its own folder,** `data/scenarios/<set_id>/`, holding:
  - `set.yaml`: id, version, kind, purpose, the axes it varies, its invariants (target words, planning
    prompt), named subsets, provenance, and which studies and sessions used it;
  - the set's guide;
  - its logs;
  - `scenarios/*.yaml`.
- **The generic scenario format** is in `data/scenarios/README.md`.
- **Studies refer to a set as `set_id@version`.** A set a finished study used is never edited; changes
  go into a new version.

**Kinds of set:**
- **staged:** scenarios as data, run by the staged engine;
- **world:** points at a free-form world's code in `mud/` and lists its run configurations and goals;
- **mini-worlds:** world configurations with a starting situation, designed axes and exit conditions,
  played on a world's engine. Example: a stranger arriving at the cabin, which ends when the party has
  dealt with them.

**The friend/foe set as it stands.** The 250 friend/foe files are the set `bus_stop_friend_foe_v2`,
with its rewrite log. It is tied to the session it fed, `b629b6c5`, and kept as it is. Its guide
records what that session's data holds (checked against its tick log, 2026-10-06):
- **the two runs of a scenario are two versions of it.** The files were revised between the two run
  days; most first-day runs used earlier versions, whose actions often named the person by role
  (`block extortionist`), so the prompt gave the label away;
- **12 scenarios were played in the wrong room.** 13 room names are each used by two files; the old
  prototype found rooms by name, so 12 scenarios got the other file's room with their own person and
  actions (the 13th pair's second file came later);
- **the sample is 479 captures from 249 scenarios.** Its statistics are counted per scenario.

The two "subsets" (clean, diverse) name the earlier 52-scenario set's files, so they are kept in the
set's logs, not as subsets.

The two old dialogue demos (the herbalist and the blacksmith) are parked.

**The staged engine is generic and multi-stage.** The format already has states and transitions.
- **Each stage has:**
  - what the agent sees;
  - what can be examined;
  - actions: typed text, matched against the stage's actions after article stripping;
  - effects: a message, the next stage, or the end with an outcome.
- **Each stage declares its ground-truth labels,** so a scenario can shift: a reveal at stage 3 turns a
  friend into a foe. That is the context-shift question asked of an agent that acts.
- **Every scenario is keyed by `set_id/file`,** never by room name.
- **Watchers in the room** read each line the player types (section 4).
- **Nothing is ported byte for byte,** because the friend/foe probes may be redone (Andrew,
  2026-10-06).

**Friend/foe v3 becomes people assessment** (Andrew, 2026-10-06). It is a study that comes after lens
slice 1:
- not only friend or foe, but the type of foe, intent, threat, honesty, need;
- a lens for each axis;
- played as staged scenarios and as mini-worlds with exit conditions;
- re-captured.

## 6. The MUD ↔ backend protocol

**The game text the agent sees:**
- text arrives as `["text", [...], {}]`, with the client asking for raw text (`client_options raw`);
- a prompt message after every command marks the end of the output. Every command sends it, because the
  MUD's base command class is Evennia's `COMMAND_DEFAULT_CLASS`, and a test walks every reachable
  command to check;
- `[SCENARIO_COMPLETE]` stays in the text, as before.

**A separate control channel,** a custom message handler that Evennia loads from
`server.conf.inputfuncs`:
- `scenario {load | end | status}` replies with `{ok, error, room, logged_in}`;
- `stage_entered {stage, labels}` reports each stage's ground truth as structured data;
- `scenario_complete {action_id, outcome}` reports the end and its labels;
- free-form worlds emit **state events** from their engine (for Winter Survival, its Effects: cold,
  injured, fire lit, and so on), recorded as labels.

**Why the split:**
- the agent can't type its way out of a scenario;
- the backend can always move it on to the next one;
- login is confirmed by `status`, not by matching a welcome banner.

**The structured messages** carry their payload as the first argument, like `room_entered`:
`["scenario", [{…}], {}]`, `["stage_entered", [{scenario, set, file_hash, stage, labels}], {}]` and
`["scenario_complete", [{scenario, set, file_hash, action_id, outcome, action_type, correct, canary,
labels}], {}]`. A load is silent apart from `stage_entered`; the runner decides what the agent reads next.

**What every run records:** `set_id@version`, the scenario id and the scenario file's hash.

The simulator's console command calls the same function a person uses.

**The other direction:** the simulator's `agent` command calls the backend's HTTP API
(`/api/agent/start`, `/api/agent/stop`; `BACKEND_URL`, the host as seen from the MUD's container),
off the server's thread. The backend still owns the GPU and refuses a second run.

## 7. Fresh instances

- **One fresh instance per load.** It is removed at the next load or on leaving, never inside the action
  that ends it, so no move text leaks into the agent's reply.
- **Loads and ends are silent moves:** no announcements and no arrival look, but the rooms' enter and
  leave hooks run, so an institute room the player leaves or returns to tells the app.
- **Items made by an instance leave with it.**
- **Winter Survival from the menu** loads the existing world for now. Per-session world instances are
  designed later.

## 8. The GPU queue

**The constraint:** one RTX 5070 Ti (16 GB) holds one copy of the model, about 14 GB. Agent runs,
sentence captures, later AI-scientist studies and live views all want it.

**The rule:** one queue on the backend, one job on the GPU at a time. Each job records what it ran.
Jobs that need no GPU, such as clustering, sweeps and reports, run beside it.

It is built when world agents arrive; until then the backend's existing one-at-a-time behaviour stands.

## 9. Rules carried over

- **The engine's gates** apply to the world code they were written for (section 4).
- **The repo is public:** no secrets in it; decisions written in plain prose, never quoting
  conversations.
- **One source of truth:** this document for the MUD's architecture; each world's GDD for that world's
  design.
- **Code changes follow the approved plan;** anything outside it is asked first.

## 10. What's retired, and when

- **`evennia_world/`, the Evennia 4.5 prototype with SQLite, was deleted on 2026-10-07,** once
  these held:
  - the new staged engine plays the v2 set end to end with the right completion labels
    (`make scenario-check`: every scenario once per opening action, scripted, no GPU);
  - the simulator works;
  - the polysemy lab works;
  - everything the prototype was used for can be done in the new MUD: watching an agent play, guest
    login, and starting and stopping agent runs from inside the MUD (section 4).

  Evennia and the 29 packages only it needed left the backend's environment with it.
- **The MUD uses Evennia's standard ports, 4000–4002.** The ports are one setting in the root
  `.env` (`MUD_TELNET_PORT`, `MUD_WEB_PORT`, `MUD_WS_PORT`), read by compose, Evennia's web client,
  the backend and the app's terminal.
- **The old C: checkout stays** while the context-shift paper runs from it, until the lake moves to an
  external drive.

## 11. Decisions from review round 1 (Andrew, 2026-10-06)

1. **Friend/foe** may be redesigned and re-captured; nothing is ported byte for byte (section 5).
2. **The polysemy lab** shows the clustering `tank_polysemy_k6_n20`. Its old preset named
   `polysemy_explore`, which doesn't exist.
3. **Lens slice 1,** the first piece of the research software, comes before the Winter Survival
   world-building pilot. Friend/foe v3 comes after lens slice 1.
4. **Whiteout is renamed Winter Survival** (`winter_survival`). The weather condition "whiteout" inside
   the engine keeps its name.

## 12. Where the MUD is heading

The MUD stays thin: it supplies experiences and shows them, and never measures. The measuring belongs
to the backend's instrument.

**1. The library:** sentence sets, staged scenario sets, free-form worlds and mini-worlds, all
versioned, with manifests, guides and provenance (section 5).

**2. Lens kits** (Andrew, 2026-10-06):
- each scenario has the lenses designed for it, built for it or reused from another scenario's kit. For
  Winter Survival that might be danger, cold, injury, and trust in the other survivors;
- a world's lenses are calibrated on runs the world labels itself through its state events, then
  checked on held-out runs;
- lenses are built from deliberately varied data, so anything carrying the understanding lands in one
  of their clusters, or at its place on a mass-mean axis.

**3. The runner** (the backend's agent loop plus the control channel):
- it runs any scenario under a recorded condition: model, scaffold, steering, decoding, seed, pinned
  date;
- each tick it records what the agent saw, its reasoning, its action, and the scenario's stage and
  labels;
- **it captures at three kinds of site:**
  - the observation's sites, before generation;
  - the generated tokens, through one forward pass after generation over prompt plus output. This is
    the same values the generation produced, and the agent loop already does it;
  - lens readings.
- **Storage:** generation-time capture is selective (named sites and lens readings), because all
  positions cost about 280 KB per token.

**Reading lenses on an agent** (compared on friend/foe runs, where the right answer is known):
- **side-pass probes** (Claude's recommendation for the main reading):
  - each tick, the agent's context is copied, the lens's probe words are appended, and one forward pass
    runs with nothing generated;
  - the agent never sees the probe, so its run isn't disturbed, and no measuring instruction enters the
    context the lens reads;
- **words in the agent's own reasoning,** natural or scaffolded (Andrew, 2026-10-06): the agent is
  asked to use certain words, and lenses calibrated on reasoning text read at them. The scaffold is
  recorded as a condition;
- **scans** of the context and reasoning against a neutral baseline, for exploring.

**4. The instrument** (backend; never inside the MUD):
- lenses, compared first as classifiers, UMAP against raw space; UMAP is preferred where it holds up;
- population flows through nodes, and expert pipelines and hubs;
- token-over-time views, as in the context-shift paper;
- steering a node, with the downstream view: from the steered layer on, baseline flows beside steered
  flows, and the expert pipelines beside each other;
- the atlas.

**The atlas** (Andrew, 2026-10-06) is three catalogues, built from populations:
- **nodes:** the clusters of validated lenses, per layer;
- **experts:** all of them, each the same unit in every capture, so each entry grows with every probe
  set;
- **routes:** pipes through sequences of experts, and hubs.

Each entry carries an LLM-written report. Every node split also comes with four things:
- attention's share of the split against the experts' share (from the residual and MoE outputs already
  captured);
- which token the split appears at first;
- what the node pushes toward in the output vocabulary;
- a check that surface features don't explain it.

*Claude's proposal, awaiting Andrew:* routes built from all four experts per layer, weighted by their
real gate weights, not only the strongest.

**The paradigm** is the accepted findings: claims from the reports, reviewed and accepted by Andrew,
with votes from several models. A key finding gets the steering-a-node check before it is accepted.

**5. The observatory** (MUD + app):
- watch or replay any run;
- labs, one per lens family or study;
- the simulator, which browses the library;
- steered and baseline runs side by side.

The AI scientists' work shows in the institute as events.
