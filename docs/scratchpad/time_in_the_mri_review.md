# Review of "Time in the LLM MRI" (2026-10-07)

Status: a review of the design proposal `docs/scratchpad/time_in_the_mri.md` ("the design"), for
Andrew. The suggestions need his yes before they enter the design. The factual corrections in
§8 are already applied.

**How to read it:**
- **References:** "design §n" is a section of the design; a bare §n is a section of this review.
  A rule is one of the eight rules in design §2. Suggestions are numbered F1–F12
  (functionality, §4) and U1–U7 (UX, §5); stories are listed in §6. The design draft is the
  research-software draft in the one-MUD plan; E.n is one of its items.
- **Terms:** the design's Terms table defines carrier, site, replay, lens, reading, references,
  band, matched point, scripted run, free play, would-be action and censored. This review adds:

| Term | Meaning |
|---|---|
| **tick** | one agent turn: an observation, the model's reasoning, its action |
| **runner** | the backend's agent loop, which plays scenarios in the MUD and captures the model |
| **re-render** | rebuild a past tick's exact prompt from the run's log |
| **prefill** | text placed at the start of the model's own reply before it writes anything |
| **lane** | one row of a timeline, showing one kind of data |
| **study timeline** / **run timeline** | readings over time for a whole study, averaged by condition / for one run |
| **between the bands** | a reading that lies between the two classes' bands at that point: the design's "unresolved" |
| **lens kit** | the lenses a scenario declares for reading its runs (design draft E.4) |
| **node path** | a UMAP lens's node at each point of a run |
| **atlas** | the planned catalogue of nodes, experts and routes, each with a report |
| **the tank arm** | the paper's tank experiment: 40-sentence runs that switch from one sense of "tank" to the other |
| **crossing point**, **dwell** | where a run's reading crosses to the other class; how long it stays between the classes |
| **certainty** | my estimate, from the evidence listed, that a claim holds or a part is the best option |

## 1. Verdict and the decisions it asks for

| Part of the design | The best option? | Certainty |
|---|---|---|
| **The measurement core:** one saved lens, one fixed site, one ordering; readings compared with reference runs | Yes. Every alternative considered breaks one of the paper's rules (§7) | 85–90% |
| **Reading agent runs:** carriers read by replay; scripted runs for claims; free play for behaviour | Probably. Its open questions are real and are sent to experiments (design §13) | 60–75% |
| **Readings inside the reasoning** | Unknown until its experiment | 40% |
| **The UX (the Runs mode)** | Not yet. The design describes views but not how a person uses them; §4–§5 list the gaps | 60% |

**The change that would raise certainty most:** test the time view first on the paper's tank
sentence runs, whose answers are already known, and only then on agents (F1).

**Decisions:**
1. **F1:** test first on the paper's tank runs, copying a subset of those sessions from C:?
2. **F2–F12 and U1–U7:** which to take into the design? Each stands on its own.
3. **Stories:** add stories 7–11 (§6), and build story 3 first?

## 2. What I tested

- **Can a past tick be rebuilt exactly?**
  - Test: rebuild every tick's prompt from the log, for the three runs made since the runner
    changed on 2026-10-06 (10 ticks); add the re-encoded generation; compare with what the run
    recorded.
  - Result: the token count matched on all 10 ticks, and all 136 recorded target positions fell on
    the word " person". The design's claim (design §5.4) was reasoned before; now it is tested.
- **What does a reading cost?** From the backend log of the last agent run's first tick:
  - generation took about 9 seconds;
  - the capture pass, including writing every row and the MUD's reply, took about 6.7 seconds;
  - a replay point is one forward pass without those writes: roughly 1–3 seconds (an estimate);
  - so a study of 200 runs × 7 ticks needs about 25–70 minutes of GPU for its readings, and about
    3.5 more hours if each tick also generates a would-be action (1,400 generations);
  - readings must therefore be a background job (F5).
- **Does the paper have known answers to test against?** Yes.
  - `docs/studies/context_shift/analysis/tank_d3_metrics_L4.csv` gives, for each of the tank
    arm's 36 switching runs, its crossing point, where its reading settled, how far that is from
    the destination class, and its dwell.
  - These are the measures the design proposes as tools (design §11).
  - The runs are on the C: drive: 36 switching sessions (3.5 GB) and 18 non-switching ones
    (1.7 GB). A subset is enough for a test.

## 3. Suggestions: the order of work

**F1. Test on known answers first.**
- **What:** the first version reads the paper's tank runs, and its crossing points and dwell must
  match `tank_d3_metrics_L4.csv`. Agents come after.
- **Why:**
  - the agent version waits on scenarios that don't exist yet: friend/foe v3 pairs with and
    without a reveal;
  - the tank runs already store the carrier's state at every step, so this test needs no replay,
    no new capture code and no GPU;
  - matching published numbers shows the instrument works before it is used where nothing is
    known.
- **What it needs:** a copy, from C:, of some of those sessions and of the items the paper fitted
  its tank axis on, if those aren't among the sessions already kept. Copying data is your
  decision.

**F12. Run the reasoning experiment early.**
- You asked to see readings as the agent reasons. The design waits for its experiment (design
  §5.3). Put that experiment in the first batch, beside the carrier-placement experiment.
- Today's runs re-render exactly (§2), so it can start on runs that already exist.

## 4. Suggestions: functionality

Each is tagged: **[spec]** a gap in what the design specifies, **[feature]** something to add,
**[architecture]** how it is built.

- **F2. A study file sets up the study timeline [spec].**
  - The design never says how a study timeline is chosen: which runs, which references, which
    lens and layer, which event to align on, and how to split.
  - As on-screen controls, that would crowd the screen. The design draft already keeps studies
    as files in the repo (decided 2026-10-06), so the study file declares all of it.
  - In the app, you pick a study; Advanced overrides any setting for one look, without changing the
    file. The same file makes the view reproducible, and an analyst agent can read it.
- **F3. Show uncertainty, not just the number of runs [feature].**
  - Each condition's line gets a shaded confidence interval from a bootstrap over scene families
    (rule 6: statistics at the scene-family level).
- **F4. One lens per lane, several lanes [spec].**
  - The design allows one lens per timeline. People assessment needs several axes (intent, threat,
    honesty, need), and you want a lens per axis.
  - The rule that matters is never to mix lenses in one lane. The timeline opens with one lane,
    and "add lens" stacks another.
- **F5. Readings are background jobs [architecture].**
  - A study's readings are computed once, as a job on the GPU queue, and stored (costs in §2).
  - The study timeline shows the job's progress and fills in as results arrive. Opening a view
    never starts a computation.
- **F6. Choose the layer [spec].**
  - Each lens works at one layer, and the design never says which layer a timeline shows.
  - Default: the lens's best layer on held-out data, with a layer selector. The planned
    layer × time heatmap shows all layers at once.
- **F7. Lens kits make live readings automatic [spec].**
  - Live readings (story 5) need a lens chosen before the run starts. Each scenario declares its
    lens kit, so a run started from the MUD or the app is read with the kit, with nothing to choose.
- **F8. Link time and layers [feature].**
  - Click a point on a timeline to open that state in the layer view: its node at each layer, its
    route through the experts.
  - Click a node in the layer view to list the runs that pass through it, and when.
  - This joins the MRI's two views: how meaning forms through the layers, and how it changes over a
    run.
- **F9. Summary numbers per run, sortable [feature].**
  - The run list shows each run's ticks between the bands, its crossing tick, its final class and its
    outcome, and sorts on any of them.
  - Story 2 begins by finding a run that stayed between the bands; sorting finds it in one click.
- **F10. Export every view [feature].**
  - Each timeline exports its figure (SVG and PNG) and its data (CSV and JSON). Figures are paper
    assets, and the same data is what an analyst agent reads for the atlas.
- **F11. Say what is missing [spec].**
  - With no validated lens for a run's site, the view says so and links to where lenses are built.
  - With no references, it uses the calibration bands and warns about drift (the design already
    has this).
  - In free play, points reached by fewer than a set number of runs are drawn faded.

## 5. Suggestions: UX

- **U1. One timeline at a time in the main pane.** The sketch stacks the study timeline and a
  run timeline in one pane, which is cramped. Instead, the main pane shows the study timeline;
  clicking a run replaces it with that run's timeline and a breadcrumb back ("Study › run 07").
  The run list highlights the open run.
- **U2. Basic and Advanced, written down.**
  - Basic: the study (or run), the lens, the layer, the split, the event to align on.
  - Advanced:
    - the references and the matching rule (tick or context length);
    - the band width and the minimum number of runs;
    - per-run lines behind the averages;
    - censored ends and exploratory readings.
- **U3. Name the modes by what they show.** "Population" says little. Suggest **Layers** (how
  meaning flows through the layers) and **Runs** (how it changes over a run). A question for the
  UX pass.
- **U4. One visual grammar:**
  - a band is a shaded area, labelled with its class;
  - the reading is a line whose points are coloured by where they fall (one class, between the
    bands, the other class);
  - the reveal, or any event, is a vertical rule;
  - each action is coloured by its type in the scenario file (friend or enemy in today's set);
  - the number of runs is a thin strip under the axis;
  - a run that ends without leaving a state ends in an open marker (censored);
  - the legend is always on.
- **U5. Reasoning collapsed by default.** Each tick shows one point. Opening a tick shows its
  reasoning text, and later its reasoning readings, below it; they never join the next tick.
- **U6. Show the MUD pane only while watching.** The terminal matters during a live run.
  Otherwise it folds away, and its space goes to the run's text or the behaviour table.
- **U7. One run list, whatever started the run.** Runs started in the MUD (`agent run`) and in the
  app appear in the same list, marked with how they were started. The UX pass decides where runs
  start.

## 6. The user stories

| Story | Verdict | What to change |
|---|---|---|
| 1. An agent study | The right goal, but the hardest to build first | List your steps (pick the study; its settings load). Name its prerequisites: v3 scenario pairs, the scripted entry point, would-be actions (about 3.5 hours of GPU for 200 runs, §2) |
| 2. One run | Right: the behaviour analysis you asked for | Start by finding the run: sort by ticks between the bands (F9). Readings inside the reasoning come later (F12) |
| 3. A sentence study | Too vague now, but the best first story | Make it specific and first: the paper's tank runs, checked against its saved results (F1) |
| 4. The atlas | Right, but later | Needs the node path, long sequences and exports (F10) |
| 5. Watching live | Right | Needs lens kits (F7); the timeline grows one tick at a time |
| 6. Steering | Right, later | — |

**Stories to add:**
- **7. Check the instrument:** reproduce a published result in the Runs mode (F1). Every later
  story rests on this.
- **8. Compare the reading methods:** the first experiment as a view. For the same runs, the
  carrier and the model's own words in two lanes (F4).
- **9. Follow the reasoning:** where in its reasoning the agent's reading shifts. You asked for
  this, so it should be written down as a goal even while its lane waits (F12).
- **10. From a moment to the layers:** from a tick, see the state's route through the layers and
  experts (F8).
- **11. Hand a study to an analyst:** export a study's readings and events; a `claude -p` analyst
  writes the report, and its numbers are re-checked (F10).

## 7. Certainty: is this the best design?

**The alternatives for the core, and why each loses:**

| Alternative | Why it loses |
|---|---|
| Repair the old panel | It still measures against a separately fitted UMAP map (rule 7), in the retired basin vocabulary, and has no reference runs |
| Time as its own instrument, with a new fit for each sequence | Nodes from separate fits can't be matched (rule 7) |
| Store every token's state for every run, and choose sites later | About 280 KB per token per run. Readings away from the calibrated site carry no information (rule 1), and replay can still read any carrier later |
| Read only live, during runs | Past runs couldn't be re-read with a new lens; replay also covers live reading |
| Put the prefill into the real run | It changes the agent's behaviour; replay reads the same prefill without touching the run |
| UMAP timelines first | "Between the bands" needs a position on one axis, or soft membership; the UMAP node path comes second (design §12) |

**The claims the design depends on:**

| Claim | Evidence | Certainty |
|---|---|---|
| Readings over time need one fixed site and one saved lens | the paper's Box 1 (each rule learned from a failure); the app's broken panel; the friend/foe figure's moving site (checked) | 95% |
| "Between the bands" needs reference runs at matched points, held out by scene family | the paper's measured drift (half the class distance within twenty sentences); held-out bands are standard practice | 90% |
| Replay gives the state the run would have had with the carrier appended | each token depends only on the tokens before it; the paper's method; one full pass, no cache cropping (checked in transformers 5.4.0) | 90% |
| Ticks from today's runner re-render exactly | 10 of 10 ticks, 136 of 136 positions (§2) | 93% |
| Scripted runs give matched ticks | the staged engine has no randomness; the runner's seam for scripts exists (checked); the entry point and would-be actions aren't built | 85% |
| Readings are affordable as background jobs | about 9 s per generation and at most 6.7 s per capture step, measured; the replay cost itself is an estimate | 80% |
| A mass-mean lens is the right first lens | "between the bands" is a position along one contrast | 85% |
| Free play can be compared with references at equal context length | an assumption, not yet tested (design §13) | 50% |
| Carrier readings track the agent's own assessment | the first experiment decides | 60% |
| Readings inside the reasoning can be made valid | its experiment decides | 40% |
| The Runs mode as sketched is the right UX | a sketch only; §4–§5 list its gaps | 60% |

**The weakest claims the design depends on:**
- As written: comparing free play at equal context length (50%), and the UX (60%).
- With F1, the first version depends on neither. What remains is a decision, copying the
  sessions, rather than a risk.

## 8. Corrections already applied to the design

- **Design §0** said "time is a dimension of readings, not a separate tab" and then proposed a
  Runs mode. It now says that time is read with the same saved lenses as the rest of the app, and
  has its own mode in the app.
- **Design §5.4** now records the re-rendering test (10 ticks) and the measured costs, with what
  follows from them: readings are a background job.
