# Slice 2: capture and jobs — a draft plan for Andrew's review (2026-10-09)

Related: docs/DESIGN.md (K slice 2; B12, C5, F6, G; L17), docs/research/read_site.md,
docs/RECOMMENDATIONS.md

**Andrew's answers (2026-10-11, DESIGN.md L17 and L19):** decisions 1, 2 (all three kinds of
position), 3, 4 and 6 as recommended. Decision 5 changed: the studies area becomes one of the new
app's first rooms (L17). He also set a new order of work (L21): this slice now follows the two
documents and the new app.

**Claude's notes on the answers (2026-10-11):** step 7 (the studies area) leaves this slice; the
four lens method changes adopted in L18 are proposed to join it (DESIGN.md C4); the MUD address
would go in the new app's top bar. The plan is rewritten from this draft when the slice is reached.

**2026-10-16:** the four method changes left this slice. Andrew moved them ahead, to be built while
the machine is shared with other work (ORDER-20; plan.md, "Work that needs no model").

The six decisions come first, each with Claude's recommendation; the steps after them follow the
recommendations, and say what changes if he picks otherwise.

## What slice 2 is for

DESIGN.md K, slice 2:
- **every capture records how it was made** (its recipe and the token ids it ran on), so any run
  can be replayed exactly (B12, G);
- **captures run as background jobs,** the way lens builds already do;
- **more token positions,** and states after generation starts for sentence sets too (C5, G);
- **entering your own MUD's address** (F6).

It comes before the sentence set builder (slice 3), which captures each new set as a background
job, and every capture records how it was made.

## What's true today (read at the source, 2026-10-09)

- **Captures hold the server up.** The capture route runs the whole capture before it answers
  (`api/routers/probes.py:236-325`), and meanwhile the backend answers nothing else: the job
  scheduler, the app's event stream and the health check all wait. On 2026-10-09 the captures of 524
  and 321 words held it for 3 minutes 9 seconds and 1 minute 27 seconds.
- **Nothing stops two captures from overlapping.** The agent loop runs as a task in the backend and
  allows one run at a time (`api/routers/agent.py:41-43, 73-78`), but a sentence capture can start
  beside it. Both share one set of hooks, which a generation or a finish on either removes
  (`services/probes/capture_orchestrator.py:34-43, 129-159`).
- **The model lives in the backend.** It loads in a thread when the backend starts
  (`api/dependencies.py:34-80`): 27 seconds alone, 4 to 10 minutes while CPU jobs run. Until it has
  loaded, the capture list fails (`GET /api/probes` depends on the loaded service,
  `api/routers/probes.py:88-95`), and the app's top bar shows no captures until the page is
  reloaded (`components/shell/TopBar.tsx:36-38`).
- **What a capture doesn't record:**
  - sentence captures: the pinned date, the decoding settings, the extra site
    (`capture_static_substring`) and the set file's hash. A lens on position 2 records only the
    number, not what position 2 is;
  - neither kind: the token ids it ran on, the model-identity line, the code's commit, or a run id.
- **Agent records carry the whole conversation as their text,** and the app's item list repeats the
  system prompt with every record: in `b629b6c5` (6,505 records) those are 21 MB and 10 MB of an
  item list of about 40 MB.
- **The writer rewrites each file in full at every flush** (`core/parquet_writer.py:75-86`): every
  1,000 rows, the file read back and written again. It's fine for today's sets; for every-position
  captures it grows with the square of the size.
- **Storage format doesn't need changing.** The stored values are exact 16-bit floats, and the
  files' encoding already removes the rest: the objects capture's residuals take 85.6 to 88.9 MB as
  64-bit lists, 32-bit fixed lists or 16-bit values alike (measured 2026-10-09). A token costs about
  280 KB over 24 layers (residuals, expert outputs and routing).
- **The hooks already copy every position of every layer** to the CPU
  (`services/probes/routing_capture.py:104-150`); a capture only chooses which positions to keep.
  A second fixed site already works (`capture_static_substring`, used for the read-site test).
- **The MUD's address is fixed when the backend and the app start:** `ws://localhost` and
  `MUD_WS_PORT` (`api/config.py:13-15`; `hooks/useEvennia.ts:21`).

## Andrew's decisions

### 1. Where GPU jobs run

Captures, agent runs and generation become jobs either way, with the same kinds, requests and
progress; the question is only what runs them.
- **(a) A GPU lane inside the backend.** The model stays where it is. One thread in the backend runs
  GPU jobs one at a time, so captures never overlap and the server keeps answering while one runs.
  The capture's own Python work still shares the process, so requests may slow a little during a
  capture; a hard crash in a capture would take the backend down; every backend restart reloads the
  model, as today.
- **(b) A GPU worker process.** A separate, long-lived process loads the model once and claims GPU
  jobs from the job store; the backend never loads the model. A crash ends only the worker, capture
  work never slows the app, and when a change doesn't touch capture code the backend could restart
  alone. Costs: one more process to start, watch and stop (the server skill's full restart includes
  it), and a worker running older code than the backend has to be noticed (each job records its
  commit).

**Claude's recommendation: (a),** the simpler design that meets the requirements. The failures that
(b) would isolate haven't happened, and with the job kinds the same either way, a worker can take
the lane over later if they do.

### 2. Which extra positions sentence sets capture

Three kinds, each named in the capture's recipe:
- **named sites:** any fixed text in the message, such as a carrier's words or the end marker:
  today's one extra site generalised to several, each with its name;
- **every position of the message,** opt-in, with the size shown before the capture starts (about
  280 KB a token: 600 sentences of 25 tokens is about 4 GB);
- **states after generation starts:** one pass over the prompt and the generated text, as agent
  runs already do, keeping named words in the generated text and the first token of the answer.

**Claude's recommendation:** all three, with every-position opt-in. A lens then chooses its site by
name, and says what it reads.

### 3. Entering a MUD's address

The MUD chip in the app's top bar opens a small form; the backend stores the address as one
setting, which the terminal and agent runs both use; before saving, the backend checks that the
server answers the control channel's status. The default stays localhost until Scaffold Dynamics is
hosted (F6).

**Claude's recommendation:** as described.

### 4. What an agent record keeps as its text

Records keep the tick's observation as their text, and the whole conversation lives once per tick
in the run's token ids. The app's Members tab then shows the observation, with the conversation one
click away.

**Claude's recommendation:** yes, with the system prompt sent once per run instead of with every
record. Together they remove about 28 of the 40 MB in `b629b6c5`'s item list (the observations
that stay average 533 characters), and nothing is lost: the token ids hold each conversation
exactly.

### 5. The studies area's place (L17)

- **(a) At the end of slice 2:** a first version that lists the studies and shows each one's
  question, sets, captures, lenses, findings and ledger, read only. The studies already exist as
  files, and `GET /api/studies` already serves them.
- **(b) With Study's timelines in slice 4** (slice 5 since 2026-10-11).

Editing a study's design would come with the builder (slice 3), whose authoring agent already
designs sets.

**Claude's recommendation: (a).** It is small, and every slice since 1 has added a study.

### 6. The leftovers (one yes or no for the list)

| Item | Why it goes | Needed? | Replaced by |
|---|---|---|---|
| `GET /api/experiments/health` and its router file | reports on a retired service (`expert_route_analysis`); no callers | no | `/health` |
| seven client methods with no callers (getSessionStatus, pollSessionUntilComplete, getTrajectoryEmbedding, archiveClustering, deleteClustering, runSentenceExperiment, listClusterings) and the unused `ExecutionResponse` schema | dead since the window views retired (rechecked 2026-10-09: still no callers) | no | the capture job's client call arrives with the builder |
| the session-start reminder "Temporal captures always need generate_output: false" (a settings file) | the temporal route retired on 2026-10-08 | no | the rest of the reminder stays |
| the test lens `lab-k4-n15` in `session_1434a9be` | built by a throwaway check of the lab's `lens build` | no | — |
| the README findings' "basin" wording | the design retired the vocabulary | — | "metastable states", as the README's own note says |
| 13 images in `docs/images/` that nothing in the repo references (the old tour's among them) | unused | not by the repo; posts outside it may link to them | — |

## The steps

| # | Step | Ends with |
|---|---|---|
| 0 | The design record | DESIGN.md B12, C5, F6, G, K and the appendix from the answers; marks audited; page republished |
| 1 | What a capture records | the recipe in every session file; token ids for every pass; absolute positions and site names on every record; agent records' text (4); lenses say what they read; a parity check |
| 2 | The writer | flushes append a part instead of rewriting; readers take a file or its parts |
| 3 | The GPU lane and capture jobs | (1a) a lane in the backend; captures, agent runs and generation as jobs; sessions never left "active"; the app's capture list follows jobs |
| 4 | More positions | named sites, every position (opt-in, size shown first), states after generation starts; lenses choose a site by name |
| 5 | The MUD address | the setting, its check, the top bar's form, the terminal and agent runs using it |
| 6 | Small fixes and the leftovers | the capture list without the model; the session details' counts; the leftovers list |
| 7 | The studies area | (5a) the list and each study's page, read only |
| 8 | Showcase and docs | "where the signal is"; docs and skills; push |

### 1. What a capture records

- **The recipe,** in every session file (sentence and agent captures alike):
  - the model: name, dtype, quantisation, the weights' index hash, library versions;
  - the prompt: the chat template's hash (recorded today), the model-identity line, the reasoning
    effort, the developer message (agents), the pinned date;
  - decoding: whether it generated, the token cap, sampling, temperature, top-p, seed;
  - sites: the target rule (the word, its last occurrence, a split word at its last token) and
    every extra site with its name and text; logit token sets;
  - the set: name, file and sha256 (scenario sets: `set@version` and each file's hash, as today);
  - the code: commit and whether the tree was dirty; who started it, and the job.
- **Token ids for every pass,** in `sequences.parquet`: one row per item (sentence sets) or per tick
  (agent runs), with its run, step, token ids and prompt length. Records point to their row and keep
  absolute positions, the extra sites' included (lost today).
- **Agent records' text** becomes the tick's observation, and the app's item list sends the system
  prompt once per run (decision 4).
- **Lenses say what they read:** a lens's site carries the site's name and text from the recipe,
  for example "position 2: `<|end|>`".
- **Checks:**
  - a parity capture: the smoke set's states equal `a644abd9`'s bit for bit, as in Phase 1;
  - replaying a row of `sequences.parquet` gives the same states bit for bit;
  - older sessions read as before.

### 2. The writer

- Each flush writes a new part (`residual_streams/part-00012.parquet`) instead of reading the file
  back and writing it again; a part is either complete or absent, so a crash loses at most the
  unflushed rows, as today.
- Every reader takes a session's single file (older sessions) or its parts.
- **Checks:** a capture written in parts reads back identical to one written whole; the lens tests
  pass on both layouts.

### 3. The GPU lane and capture jobs (decision 1a)

- **The lane:** a `gpu` lane with one slot, run by a thread in the backend instead of a worker
  process: it waits for the model, runs each job with the loaded capture service, writes its
  progress, and stops at the job's cancel flag between items or ticks (never by killing a process).
  A backend restart ends the thread, so a GPU job that was running is marked interrupted, as a lens
  job is today when its worker dies.
- **Job kinds:**
  - `capture_sentences`: the sentence route's work. `POST /api/probes/sentence-experiment` returns
    202 and the job at once;
  - `agent_run`: the agent loop, through its existing actions seam (`ModelActions`).
    `POST /api/agent/start` queues it, `stop` cancels it, and the MUD's `agent run` works as before;
  - `generate`: `/api/agent/generate`.
- **Sessions are never left "active":** a session belongs to its job; when the job ends, fails or
  is interrupted, the session file says so. Resuming a sentence capture skips the items already
  written.
- **The app** shows capture jobs with the lens jobs, and a finished capture refreshes the capture
  list (a `capture` event).
- **Skills:** `/probe` and `/agent` (captures and runs return jobs), `/app` (capture events),
  `/server` (the lane's status in the health check).
- **If Andrew picks (1b)** instead: the same job kinds, claimed by a long-lived worker process that
  loads the model; the backend stops loading it, and the server skill starts and stops the worker.
- **Checks:** with a fake model service, jobs run, cancel and resume; two GPU jobs never run
  together; a restart leaves a running job and its session interrupted; live, a capture runs while
  the app's other requests answer within a second.

### 4. More positions (decision 2)

- **Named sites:** `sites: [{name, text}]` in the capture request; each site's tokens are kept at
  their last occurrence in the message.
- **Every position:** `all_positions: true`, for short inputs; before starting, the route answers
  with the size it would write and the free disk.
- **After generation starts:** with `generate_output`, one pass over the prompt and the output; named
  words in the output and the answer's first token are kept, marked `generation`.
- **Lenses** choose a site by name (the build form lists the capture's sites), and keep reading
  `token_position` on older captures.
- **Checks** with the real tokenizer: sites found at the right tokens; every-position counts equal
  the message's length; generated-word positions point into the output.

### 5. The MUD address (decision 3)

- `GET` and `PUT /api/settings/mud`: the address, checked with the control channel's `status`
  before it's saved; `wss://` for a remote server.
- The top bar's MUD chip opens the form; the terminal reconnects to the new address; agent runs use
  it.
- **Checks:** a bad address is refused with the reason; the local MUD on 4002 passes; a run started
  after a change goes to the new address.

### 6. Small fixes and the leftovers

- The capture list and a capture's details stop depending on the model.
- `GET /api/probes/{id}`: its count and layers come from the session (agent captures show 0 and
  `[0, 1, 2]` today).
- The leftovers list (decision 6), as answered.

### 7. The studies area (decision 5a)

- A Studies workspace: the list from `GET /api/studies` (status, question, sets, captures, lenses,
  findings), and each study's page with its ledger; links open its lenses in Layers and its notes.
- Read only; editing a design comes with the builder.

### 8. Showcase and docs

- **"Where the signal is":** the tank calibration set (aquarium against vehicle, `29a80932`'s 600
  items) captured again as a job with every position; its mass-mean axis fitted at each position and
  layer and scored on held-out scenes: a positions × layers map of where the contrast can be read
  (C5's "other token positions that carry the same signal"). Beside it, a replay from token ids
  matching the capture bit for bit.
- **Docs:** DESIGN.md's Built marks and its page; CLAUDE.md, README, PIPELINE.md, PROBES.md; the
  `/server`, `/probe`, `/agent` and `/app` skills; RECOMMENDATIONS.md.
- **Push,** then CI checked.

## What changes or goes

| Item | Dropped or changed on purpose? | Still needed? | Replaced by |
|---|---|---|---|
| The sentence route answering when the capture ends | changed, on purpose | no | 202 with the job at once; the job's progress and the `capture` event |
| The agent loop running as its own task in the backend | changed, on purpose (1a) | no | an `agent_run` job on the GPU lane |
| Agent records' text holding the whole conversation | changed, on purpose (4) | no | the observation; the conversation in the run's token ids |
| The writer rewriting each file | changed, on purpose | no | parts |
| The leftovers (decision 6) | dropped, on purpose | no | as listed |

## How sure

| Claim | Evidence | Certainty |
|---|---|---|
| The GPU lane can run every GPU job | the agent loop already takes its model through one seam (`ModelActions`, `api/routers/agent.py:93-106`) and runs in the backend today; the sentence route's work is a loop over items calling `generate` and `capture_step`; the job store already records progress and cancel flags | 90% |
| Captures stop holding the server up | the capture runs on the lane's own thread; the model's computation leaves the backend free, and building records between passes shares its time (requests may slow a little, never wait minutes) | 90%: measured live in step 3 |
| Records can be replayed exactly | Phase 1's parity capture matched bit for bit with a pinned date; the token ids remove the template and date from the question | 93% |
| The storage format can stay | measured: 85.6 to 88.9 MB for every format on the objects capture | 95% |
| Parts fix the rewrite | each flush writes only its own rows; readers already scan in batches | 95% |
| The MUD check works | the control channel's `status` answers today (`evennia_client`) | 90% |

## Risks

- **A big slice:** each step ships on its own; steps 1 and 2 change no behaviour the app sees.
- **One slow job holds the lane:** a long agent run or a large every-position capture delays the next
  GPU job; the lane shows its queue, and any job can be cancelled.
- **Clients of the old synchronous capture route:** the skills, PROBES.md and PIPELINE.md change in
  the same step; the MUD calls only `/api/agent/start`, whose request stays the same.

## Not in this slice

- the sentence set builder and its capture form (slice 3);
- time on sentence runs, Study's timelines, references and bands (slice 5);
- hosting Scaffold Dynamics for others (F6, before other researchers are invited);
- interventions (slice 8).
