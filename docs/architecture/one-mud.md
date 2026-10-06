# One MUD in one app — architecture

> **Status: draft for Andrew's review, section by section (2026-10-06).** Nothing below is decided until
> he marks each section keep, change or cut. It replaces the MUD sections of
> [`../architecturemud.md`](../architecturemud.md). The research software (studies, lenses, tools,
> interventions, the AI scientists) gets its own design document later; this one covers the MUD and how
> it joins the app.

## 1. Purpose

Open LLMRI is an instrument for modelling how a Mixture-of-Experts language model — gpt-oss-20b first —
represents and processes meaning, with visualization first. The MUD is where agents act while their
activations and expert routing are captured, and where people visit the institute: its labs, its
simulator and, later, its AI scientists.

One MUD hosts three kinds of scenario:
- **free-form worlds**, with Whiteout the first;
- **staged multiple-choice situations**, such as friend/foe at the bus stop;
- **sentence-set probes**, run from a lab.

*Draft — awaiting Andrew.*

## 2. The pieces and where they run

| Piece | What it is | Where it runs |
|---|---|---|
| `backend/` | FastAPI: gpt-oss with capture hooks, the data lake, the analysis endpoints, the agent loop | the host, on the GPU; Python 3.10.12 from `backend/requirements.lock.txt` |
| `mud/` | the one MUD: Evennia 6 with Postgres, from Whiteout's foundation | Docker; Python 3.13 in a digest-pinned image |
| `frontend/` | the React app: the research view (terminal and visualizations), the labs | the browser, served by Vite |
| later | a workbench API (no GPU) for world building; the exploration engine | the host |

**Talking to each other:**
- the app talks to the backend over HTTP;
- the app and the backend's agent loop each talk to the MUD over its websocket;
- the backend never imports MUD code, and the MUD never imports backend code.

*Draft — awaiting Andrew.*

## 3. The target layout

```
OpenLLMRI/
  backend/                  FastAPI, gpt-oss, capture, lake, analysis + tests/
  frontend/                 React app
  mud/                      the one MUD: Evennia 6 game dir, Docker, its Makefile, docs, tools
    game/typeclasses/       plain shared bases + whiteout/ + staged/ + institute/
    game/commands/          the base command (sends the prompt) + whiteout/ + staged/ + institute/
    game/world/sim/         Whiteout's pure engine (unchanged, still gated)
    game/world/scenarios/whiteout/
    game/world/staged/      the staged-choice loader, schema and verb table
    game/world/institute/   hub, labs, simulator
    game/server/conf/inputfuncs.py   the control channel
    docs/                   Whiteout's design docs (its GDD) and the MUD's own architecture
  data/worlds/              situation YAML and world files: one copy, read by the MUD and the backend
  data/sentence_sets/
  data/lake/                kept sessions and new captures (git-ignored)
  data/models/gpt-oss-20b -> ~/models/gpt-oss-20b
  docs/architecture/one-mud.md
  .github/workflows/        mud.yml, backend.yml, frontend.yml (path-filtered)
  .githooks/                one pre-commit, per-area checks
  Makefile                  one entry point
```

The folder is `mud/`, not `whiteout/`, because the Evennia game becomes the institute's MUD and Whiteout
is one scenario in it. Whiteout keeps its history: it is imported with `git filter-repo`, so
`git log -- mud/<file>` shows every earlier commit.

*Draft — awaiting Andrew.*

## 4. Areas in one MUD

- **Every room belongs to one area:** the institute, Whiteout, or a staged situation.
- **The area decides which commands apply and how things are shown.** Each area's commands are an
  Evennia command set on its rooms. Evennia 6 merges a room's commands into everyone standing in it, so
  walking from one area to another changes what you can type.
- **The institute is plain Evennia.** Every institute room tells the app where you are with
  `room_entered {room_type, role}`, as the old prototype's rooms did; the app's toolbar uses both
  fields.
- **Whiteout's own rules hold inside Whiteout only:** the taught grammar, the world's feedback, never a
  menu. The simulator room is a menu on purpose.
- **Characters cross areas.** Their appearance asks their room's area which renderer applies, and
  Whiteout's body state applies only inside Whiteout.
- **Whiteout's code gates** (pure core, no raw writes, no raw output, doc consistency) cover Whiteout's
  own packages. The new institute and staged code has its own tests.

*Draft — awaiting Andrew.*

## 5. Staged choice, as it really is

Measured over the 252 situation files in `data/worlds/scenarios/`:
- **250 are friend/foe.** Each has one room, one stage and four actions. Each action carries the text
  the agent types, a message, and an ending with `{action_id, outcome}`. There are also objects, the
  person, inventory, and a planning prompt.
- **Two are old dialogue demos** (the herbalist and the blacksmith); they are not ported.
- **Actions are matched as text, not as commands.** The agent's actions use 385 different verbs, and a
  fallback matches the typed text against the situation's actions.
- **The old verbs collapse into a table.** 34 of the old prototype's 42 verb commands only print a "you"
  line, show a line to others in the room, and pass the action on, so one table replaces them: the
  verb, the "you" line, the "others see" line.
- **Port the behaviour exactly,** so new captures stay comparable with old ones.
  - A replay check plays every recorded situation from session `b629b6c5` and compares every line the
    agent saw, byte for byte. Differences are listed, then fixed or documented.
  - The 13 situations whose names appear twice are left out; the old prototype sent the agent to the
    wrong room for them. The new loader keys every situation by its file, so that can't happen again.
  - *Open:* redesigning the situations instead, and re-capturing.

*Draft — awaiting Andrew.*

## 6. The MUD ↔ backend protocol

**The game text the agent sees:**
- text arrives as `["text", [...], {}]`, with the client asking for raw text (`client_options raw`);
- a prompt message after every command marks the end of the output. Every command sends it, because the
  MUD's base command class is Evennia's `COMMAND_DEFAULT_CLASS`, and a test walks every reachable
  command to check;
- `[SCENARIO_COMPLETE]` stays in the text, as the agent saw it in the recorded data.

**A separate control channel,** a custom message handler that Evennia loads from
`server.conf.inputfuncs`:
- `scenario {load | end | status}` replies with `{ok, error, room, logged_in}`;
- `scenario_complete {action_id, outcome}` reports the end of a situation and its labels as structured
  data, not by matching strings.

**Why the split:**
- the agent can't type its way out of a situation;
- the backend can always move it on to the next one;
- login is confirmed by `status`, not by matching a welcome banner.

The simulator's console command calls the same function a person uses.

*Draft — awaiting Andrew.*

## 7. Fresh instances

- **One fresh instance per load.** It is removed at the next load or on leaving, never inside the action
  that ends it, so no move text leaks into the agent's reply.
- **Items made by an instance leave with it.**
- **Whiteout from the menu** loads the existing world for now. Per-session Whiteout instances are
  designed later.

*Draft — awaiting Andrew.*

## 8. The GPU queue

**The constraint:** one RTX 5070 Ti (16 GB) holds one copy of the model, about 14 GB. Agent runs,
sentence captures, later AI-scientist studies and live views all want it.

**The rule:** one queue on the backend, one job on the GPU at a time. Each job records what it ran.
Jobs that need no GPU, such as clustering, sweeps and reports, run beside it.

It is built when Whiteout agents arrive; until then the backend's existing one-at-a-time behaviour
stands.

*Draft — awaiting Andrew.*

## 9. Rules carried over

- **Whiteout's gates** apply to Whiteout's code (section 4).
- **The repo is public:** no secrets in it; decisions written in plain prose, never quoting
  conversations.
- **One source of truth:** this document for the MUD's architecture, Whiteout's GDD for Whiteout's
  design.
- **Code changes follow the approved plan;** anything outside it is asked first.

*Draft — awaiting Andrew.*

## 10. What's retired, and when

- **`evennia_world/`, the Evennia 4.5 prototype with SQLite,** is deleted once staged choice, the
  simulator and the polysemy lab run in the new MUD and the end-to-end check passes. Evennia then leaves
  the backend's environment.
- **The new MUD moves to ports 4000–4002 at that point;** it uses 14000–14002 until then.
- **The old C: checkout stays** while the context-shift paper runs from it, until the lake moves to an
  external drive.

*Draft — awaiting Andrew.*

## 11. Open questions

1. **Section 5:** port the friend/foe situations exactly (recommended), or redesign them and re-capture.
2. **The polysemy lab's clustering:** its world file names `polysemy_explore`, which doesn't exist. Pick
   one of `polysemy_default_k5_n16` or `tank_polysemy_k6_n{8,15,20,30}`; Claude suggests
   `tank_polysemy_k6_n20`.
3. **Anything in sections 1–10** marked change or cut.
