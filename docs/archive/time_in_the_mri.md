# Time in the LLM MRI — design proposal

> **Superseded (2026-10-08).** Andrew ruled on this proposal while reviewing
> [`docs/DESIGN.md`](../DESIGN.md), approved 2026-10-08, whose Part D now holds the design of time.
> This file stays as the record of the proposal.

Status: a proposal for Andrew's ruling (2026-10-07). Nothing here is decided. It replaces the
"temporal tab" question in the one-MUD plan's Phase 7 notes and, once ruled on, feeds the
research-software design (Phase 10, now the one design document). Two independent reviews
checked this version, and every claim it relies on was re-checked at source. A further review,
with suggestions for the functionality, the UX and the user stories and a certainty table, is in
`time_in_the_mri_review.md` (2026-10-07).

**References used below:**
- §n is a section of this document. A rule is in §2, a story in §3 and a decision in §14.
- **The paper** is the context-shift paper (`docs/studies/context_shift/`).
- **The briefing** is `docs/research/research_briefing_metastable_states.md`.
- **The design draft** is the research-software draft in the one-MUD plan. E.n is one of its
  items. A slice is a step of its build order: slice 1 is the lens core, slice 5 agent readings,
  slice 6 the transition and trajectory views.

## Terms

| Term | Meaning |
|---|---|
| **ordering** | what a sequence of readings steps through: context steps, agent ticks, or reasoning steps inside one tick (§1) |
| **site** | the one token a reading is taken at, for example " person" in a fixed sentence |
| **carrier** | a fixed text containing the site's token, appended to a context so that token can be read |
| **replay** | one forward pass over a recorded run's exact context plus a carrier, with no generation, to read the carrier's token |
| **lens** | a saved, validated way to read the residual stream at one site, of one of two kinds (the two *instruments*): a **UMAP lens** (a per-layer map whose clusters are *nodes*) or a **mass-mean lens** (an *axis*: the direction from one class's mean state to the other's) |
| **reading** | what a lens gives for one state: a node (UMAP), or a position along the axis (mass-mean, scaled so the class means sit at −1 and +1) |
| **calibration items** | the labelled items a lens is fitted on, for example single scenario observations with the carrier |
| **scene family** | items that share one setting. Held-out validation withholds whole families, so a lens can't pass by learning settings instead of classes |
| **drift** | a change in readings that grows with the amount of context, whatever the class (the paper's *accumulation drift*) |
| **reference runs** | runs whose label never changes (no reveal), read with the same lens: they show where each class's readings sit at each point, drift included |
| **band** | the range holding most (for example 90%) of one class's reference readings at one point |
| **matched point** | a point in a run and a point in the references that are comparable: the same tick in scripted runs, the same context length in free play (§6) |
| **scripted run** | an agent run whose actions follow a fixed script through the MUD, so every run of a scenario has the same stages at the same ticks |
| **free play** | an agent run in which the model chooses its own actions |
| **would-be action** | in a scripted run, the action the model generates at a tick: recorded, not played |
| **censored** | a stay in a state that the end of the run cut off, so its true length is unknown |
| **regime** | the kind of context a reading is taken in: prompt format, carrier and amount of accumulated context |
| **condition** | what a set of runs varies: a reveal or none, a scaffold, steering, a model |
| **observatory** | the MUD and app views for watching runs live (one-MUD doc §12) |

## 0. In one screen

**The question.** The app has a "Temporal Analysis" panel from the basin era. The paper later
moved its time measurements to mass-mean axes read against reference runs. What should time mean
in this software, whose purpose is to model how gpt-oss-20b processes meaning, and which runs
studies and agents?

**The answer, briefly.**
- **Time is read with the same saved lenses as the rest of the app,** not with an instrument of
  its own. A saved lens is read at one declared site at each point of a sequence. The app already
  shows how a token's state changes through the layers; the same lenses, read along a sequence,
  show how it changes as evidence arrives and as the model acts. In the app, time has its own
  mode (§10).
- **Three orderings are time:** context steps, agent ticks, and reasoning steps inside one tick.
  Each tick's reasoning is a branch the next tick never sees (the runner keeps only the action),
  so readings are compared within one ordering, never across a tick.
- **The main way to read a run is a carrier, by replay.** The run itself is untouched. The second
  way reads the model's own words: the target word where it naturally occurs, and words the agent
  is asked to use (design draft E.4). Comparing the two is the first experiment.
- **"Unresolved" means between the class bands at a matched point.** The bands come from reference
  runs of scene families the lens wasn't fitted on. The need is general, not the paper's: readings
  drift as context grows, whatever the class.
- **Agent studies come in two kinds.**
  - *Scripted runs* have the same ticks every time. They support claims about dynamics.
  - *Free play* shows behaviour, read against the references, with the number of runs at each
    point always shown.
- **Time feeds the atlas:** how long runs stay in a node, and what comes before and after it, come
  from sequences long enough to show them. This is how the briefing's question (a learned
  intermediate state, a passage, or an off-manifold state) gets answered, node by node.
- **In the app this is a second mode, Runs,** beside today's Population mode. The first version is
  small: one mass-mean lens, the events, a run timeline and a study timeline.
- **What's retired:** the old temporal panel, its endpoints and the old sequence-capture route.

**Decisions for Andrew** are in §14.

## 1. What "time" means here

**Orderings that are time** (something the model receives or produces changes between points):

| Ordering | What changes between points | Example |
|---|---|---|
| Context step | the input grows by one unit; the same carrier is re-read | the paper's 40-step runs |
| Tick | an agent turn: a new observation, then reasoning, then an action | a friend/foe episode |
| Reasoning step | the model's own analysis grows, inside one tick | the analysis channel, sentence by sentence |

Two other orderings are not time. **Depth** (the layer, for the same token and input) is what the
app's trajectory plot and Sankeys already show. **Position** (the token within one forward pass)
matters only as the site a reading is taken at.

**The shape of an agent run.** Tick t's prompt holds the system prompt, every earlier
observation, every earlier action, and the new observation. The model writes its analysis, then
its action. The next tick's prompt keeps only the action as the assistant's turn
(`agent_loop.py:229`); the analysis is dropped. So the ticks form one growing line, and each
tick's reasoning is a branch off it that ends with the tick. A reading late in tick 2's reasoning
and the reading at tick 3's observation come from different contexts, so the difference between
them is not a change the model went through.

## 2. Rules

The paper wrote its measurement rules down after getting each one wrong first (its Box 1). They
aren't about context shift; they apply to any reading over time, so this software adopts them,
with two of its own:
1. **Same site, same carrier, always.** Readings across token positions collapse to a positional
   constant, and readings of one carrier through another carrier's axis are dominated by token
   identity.
2. **Validate held out by scene family.** The paper's axes separated classes at 0.905 and 0.910
   under leave-one-scene-pair-out validation, with 300 items per class.
3. **Compare every absolute reading with reference runs at the matched point.** At the paper's
   fiction/real site, drift reached half the distance between the class means by twenty
   sentences.
4. **Check that the axis still points the right way in the regime read.** As context
   accumulated, the paper's fiction/real axis kept only cos 0.57–0.63 of its single-sentence
   direction at layers 10–23, so its depth claims used axes refitted on accumulated reference
   states.
5. **Readings are positions along a designed contrast, never meanings.**
6. **Statistics at the scene-family level.**
7. **One fixed, saved lens reads every point.** Nothing is refitted per view, and nodes are never
   matched across separate clusterings.
8. **Dynamics are computed within one ordering** (§1).

**What broke these rules in the app.**
- **The old temporal panel mixes coordinate systems** (rules 1 and 7).
  - Its lag projection fits a new UMAP on the source session with fixed settings (`n_neighbors`
    15, all rows at the site).
  - It then measures each point against cluster centres stored from the clustering's own fit.
  - Unless that clustering was fitted with exactly those settings on exactly those rows, the two
    fits place points differently, and the distances between them aren't comparable.
- **The friend/foe figure reads different tokens at different ticks** (rule 1).
  - Its clusterings keep the last "person" in each tick's full sequence (prompt plus generation).
  - At tick 0 that is the " person" in the model's own final answer, "examine person", for 484 of
    499 captures.
  - At tick 1 it is a mix of the final action and mentions inside the reasoning.
  - "The last occurrence of the word" is not a site: it moves.
- **The old sequence capture reads a moving site** (rule 1).
  - It reads the target word inside each new sentence, and records nothing when the sentences
    don't contain it, as in the paper's tank contexts.
  - It can't re-append a carrier: its key/value-cache chain extends the context and never
    removes anything (`harmony_kv_chain.py`).
  - The paper didn't use it. Its captures went through the sentence-experiment route, with each
    step's cumulative text plus the carrier.

## 3. User stories

1. **An agent study.** Andrew runs people-assessment scenarios in which the person's intent is
   revealed at stage 3, beside the same scenarios with no reveal. The scripted runs give a study
   timeline aligned on the reveal:
   - the reading per tick, split by reveal direction, against the reference bands;
   - the model's would-be action at each tick.

   He might see, for example, the reading cross the bands two ticks after a friend-to-foe reveal
   but not after the reverse. Free play of the same scenarios then shows whether the agent's own
   choices change that, and which actions it took while the reading was still between the bands.
2. **One run.** He opens a free-play run that stayed undecided for several ticks. Its timeline
   shows:
   - each tick's observation, its reading and its action;
   - for each tick, the reasoning text beside the reading.

   The reading sits between the bands at the tick where the model wrote "they might be lying",
   and the action at that tick avoids committing: the agent keeps its distance.
3. **A sentence study.** A context-shift-style study (sentence sequences, a fixed carrier,
   reference sequences of one class) uses the same timeline. The view needs nothing
   paper-specific.
4. **The atlas.** An analyst agent receives, for each node of a validated lens, what a sequence
   study recorded:
   - how long runs stay in the node, and how many of those stays were censored;
   - what precedes and follows it;
   - the actions taken while in it.

   It writes the node's report, for example: "a passage: runs leave it within two steps in 90% of
   uncensored stays; entered from friend nodes after ambiguous cues".
5. **Watching live.** In the MUD a researcher types `watch agent` and follows the agent into each
   scenario (built in Phase 8a). The app's Runs mode shows the run timeline growing tick by tick.
6. **Later, steering.** Steered and unsteered runs are two conditions on one timeline: where they
   diverge, and how long the effect lasts.

## 4. The concepts, and what exists today

| Concept | Its job | Today |
|---|---|---|
| **Ordering** | where a reading sits: context step, tick, or reasoning step within a tick | steps and ticks recorded; reasoning steps not |
| **Site** | which token is read: a carrier's token, or a word in the model's own text | implicit ("last occurrence", "all occurrences") |
| **Lens** | turns a state at its site into a reading; fitted on calibration items, validated held out | lenses aren't saved; no site recorded |
| **Reading** | a node (UMAP) or an axis position (mass-mean) | computed ad hoc in scripts |
| **Condition** | what a set of runs varies; a study marks some runs as references for a comparison | in design draft E.5, not built |
| **Events** | stages and their labels, actions, would-be actions, outcomes | recorded by the runner (one-MUD plan, Phase 6.2) |

A timeline is the readings of one lens at one declared site, in one ordering, with the events
alongside and the references' bands behind. Nothing else.

## 5. Reading a run

### 5.1 Carriers, read by replay (the main method)

To read a recorded run at a point, take the run's exact context up to that point, append the
carrier, run one forward pass with no generation, and read the carrier's token. The agent never
sees the carrier, and the run is untouched.

A carrier is the lens's own template. A lens fitted on items that each end with "What is the
meaning of the word tank?" reads any run by appending that question, so building lenses
(slice 1) and reading over time use one site.

**Where an agent's carrier goes** is an experiment (§13). The two placements:
- **as a question:** a user turn after the observation, such as "What will you do about the
  person?", read at " person";
- **as a prefilled opening of the analysis channel:** the prompt ends at the assistant's header,
  so the replay appends `<|channel|>analysis<|message|>Assessment of the person:` and reads
  " person".

A token's state depends only on the tokens before it. So the replay reads the prefill's " person"
in one forward pass, without letting the model write anything after it, and the run's own
reasoning stays as it was. The prefill puts the reading in the analysis channel instead of
framing it as a question from the user. It is still a carrier, written by us, not the model's own
words (§5.2). Its calibration items carry the identical prefill.

**What a carrier measures.** A carrier reading shows what the model's state encodes about the
person when prompted at that point: what is readable, not what the model used. If carrier readings
flip at a reveal while the actions don't follow, the carrier may be drawing out an assessment the
agent never made, rather than showing behaviour lagging. Readings at the model's own words (§5.2)
are the other side of that comparison. Later, steering experiments test whether the model uses
what a reading shows.

### 5.2 The model's own words (the second method)

- **Natural mentions:** the target word wherever it occurs: in the observation, in the reasoning
  and in the action. The runner already captures every occurrence each tick.
- **Asked-for words** (design draft E.4): the agent's instructions ask it to name, in its
  reasoning, its assessment of the person in set words. This reads the representation inside the
  agent's own reasoning. The instruction is a condition that may change behaviour, so it runs
  beside an arm without it.

Both sit at moving positions and in varying context, so one axis can read them only if it is
fitted across that kind of site (design draft E.3's token-collection mode). Until such a lens
validates, these readings are for generating hypotheses, not claims.

### 5.3 Reasoning steps

Reading inside a tick's reasoning means placing a carrier mid-analysis. The natural construction
continues the agent's own monologue with the carrier's line ("…they might be lying. Assessment of
the person:"). Its references are runs with constant labels, read at matched amounts of
reasoning. This is the least certain part of the design, and it waits for its experiment (§13).
Until then, the run timeline shows each tick's reasoning text beside the tick's reading.

### 5.4 How a reading is computed

- **One full forward pass per point,** with no generation. This is the paper's method (each step's
  cumulative context plus the carrier), so calibration and reading share one path.
- **The key/value cache is never cropped.** Half of gpt-oss's 24 layers use sliding-window
  attention over 128 tokens, and transformers refuses to crop such a layer once it has seen 128
  tokens (`DynamicSlidingWindowLayer.crop`; the existing cache chain avoids cropping for this
  reason). A faster path, which copies the cache at each point and extends the copy, comes later,
  and only after a test shows it matches the full pass.
- **What a replay needs:**
  - for points at a tick's observation, the context can be re-rendered from the tick log through
    the function the runner uses (`harmony_token_ids`). Tick t's messages are the logged list
    without its last two entries (the action and the reply are appended before the log is
    written), plus the run's date;
  - that holds only for runs made by the current runner (since 2026-10-06), and only while the
    chat template and the runner's fixed model-identity line stay as they were; neither is
    recorded with the run;
  - checked on 2026-10-07: for all 10 ticks of the three runs made since then, the re-rendered
    prompt plus the re-encoded generation matched the recorded token count, and all 136 recorded
    target positions landed on " person";
  - earlier runs, including the v2 friend/foe session, were rendered differently and with the
    real date, so re-rendering them is approximate and has to be checked against their stored
    target positions;
  - for points inside the generated text (reasoning steps, the model's own words), a replay needs
    the exact generated token ids. The runner uses them in its capture pass but doesn't store
    them;
  - so each run should record its token ids, its date, its template hash and its model-identity
    line (decision 7).
- **What is stored:** the reading, a few numbers per point, layer and lens. States are stored
  only for calibration items.
- **Cost (measured 2026-10-07 on one agent run's first tick):**
  - generation took about 9 seconds;
  - the capture pass, including writing every row and the MUD round trip, took about 6.7 seconds;
  - a replay point is one forward pass without those writes, roughly 1–3 seconds (an estimate);
  - so a study of 200 runs × 7 ticks needs about 25–70 minutes of GPU for its readings, plus
    about 3.5 hours if every tick also generates a would-be action;
  - readings are therefore computed as a background job and stored; opening a view never starts
    a computation;
  - with a lens active, the runner can read each tick live, for one extra pass per tick.

## 6. Two kinds of agent study

**Scripted runs.**
- The runner's scripted-actions source plays a fixed path through the MUD, through the same loop
  as a model run, with no GPU. The staged engine has no randomness, so every run of a scenario has
  the same stages at the same ticks.
- With scenario texts matched in length (as the paper matched token budgets to ±2%), the ticks
  are matched points.
- Replay reads each tick. Optionally, at each tick the model also generates its would-be action,
  through a new action source that generates, then plays the script. This gives behaviour along
  the path without letting behaviour change the path.
- The references are the same scenarios with the reveal left out.
- The scripted actions appear as the assistant's turns in the context. That is part of the
  condition, and it is recorded.
- Only the loop's seam exists today. Nothing launches a scripted run that writes a session and a
  tick log: the API always plays the model, and `max_ticks` stays at its default of 5. Slice 5
  adds that entry point, with the number of ticks set per study.

**Free play.**
- The model plays; replay reads each tick.
- **The same tick is not a matched point here:**
  - stages advance only when the agent takes an action that leads to the next one
    (`transitions_to` in the scenario format), and a run ends with its decision;
  - so the no-reveal runs still going at tick 4 are the ones where the agent hesitated, a sample
    selected for ambiguity;
  - runs with a reveal carry extra text, so their contexts are longer at the same tick, and drift
    alone can then look like "unresolved";
  - a state a run ends in is censored.
- So readings are compared with the scripted references' bands at the same context length, not
  at the same tick. This is an assumption to check (§13). In the paper, length and step count rose
  together (one sentence per step, token budgets matched), so it doesn't show which one drives the
  drift. Agent contexts of equal length can also differ in their number of turns.
- The study timeline always shows how many runs reach each point.

Claims about dynamics (when a reading crosses the bands, how long it stays between them) rest on
scripted runs. Free play shows what the agent did with its states.

## 7. "Unresolved"

**The definition:**
- mass-mean lens: the reading lies between the classes' bands at the matched point;
- UMAP lens: membership in a node the lens learned for mixed states (and, later, a membership
  split between nodes, §8).

**Where the bands come from:**
- **the axis** is fitted on calibration items: single observations with the carrier, as the paper
  fitted its axes on single sentences. These are cheap (no generation), so 300 per class is
  feasible, and the axis is validated held out by scene family (rule 2);
- **the bands** come from reference runs at the matched point, read with that axis (rule 3);
- **the reference runs never include the data the axis was fitted on.** An axis places the states
  it was fitted on farther out than new states. Bands drawn from the fitting states would
  therefore sit too far apart, and new readings would fall between the bands too often;
- **the axis is checked in the regime read** (rule 4). If its direction rotates on accumulated
  reference states, it is refitted on the reference runs of some scene families, and the bands
  come from the others. A split that shares scenes would make the bands in-sample again.

If no references exist, the view shows readings against the calibration items' bands and says
that the levels may include drift. Reference runs are a general study feature: the same mechanism
compares steered with unsteered runs, scaffolded with plain, one model with another. The paper's
own analyses (integrator fits, the remnant gap, hysteresis loops) stay in the study; one is
promoted to a tool only when a second study needs it.

## 8. What goes on a timeline

| Lane | What it shows | In the first version |
|---|---|---|
| Events | stages and their labels; per tick the observation, reasoning and action (on hover); would-be actions in scripted runs | yes |
| The lens | position between the reference bands (mass-mean), with n per point in study timelines | yes |
| Node path | the node per point (UMAP) | next |
| Soft membership | a UMAP reading's share in each node | after its experiment |
| Typicality | distance from the lens's calibration states, as a percentile | after its experiment |
| Routing | routing entropy, or the top expert per layer | later |

**Defaults.** A timeline opens with the events and one lens. Five lanes of numbers at once would be
too much to read.

**Cautions recorded for the later lanes.**
- **Membership and typicality from one query.** The plan is a nearest-neighbour index over the
  lens's calibration states, in the space the lens was fitted in. For a new state, the share of
  its nearest calibration states in each node is its soft membership. Their distance, as a
  percentile of the calibration states' own distances, is its typicality. (For fewer than 4,096
  points umap-learn computes neighbours exactly and keeps no index; checked.)
- **A caution about typicality.** A state halfway between two classes is, in high dimensions, far
  from both. On synthetic data such points scored above the 99th percentile of the calibration
  states' own distances. A lens calibrated only on clean endpoints therefore calls every
  intermediate state atypical. Typicality means something only relative to a set that includes
  the regime's natural states (the references), and the view says what the set contains.
- **One lens's middle node is not yet a learned state.** A UMAP lens with too large a k can cut a
  continuum into nodes, and "dwells in the middle node" then reflects the cut. A learned
  intermediate state is claimed only when the instruments agree: a recurring middle node, a
  middle mode along the mass-mean axis, and normal typicality.

**Which instrument when.** Neither replaces the other. A UMAP lens shows combinations and
unexpected states, and lets an intermediate state appear as a node of its own. A mass-mean axis
gives a precise position on one contrast but is blind to anything at right angles to it. Which
reads a given contrast better is measured per lens (the fair comparison in slice 1).

## 9. Time feeds the atlas

The atlas is nodes, experts and routes, each with a report. Sequence data adds node dynamics:
- how long runs stay in the node, counting censored stays separately;
- what precedes and follows it;
- what the model does while in it.

These are the briefing's three possibilities as properties of nodes. A learned intermediate state
holds runs for a while, recurs and has its own behaviour. A passage is visited briefly between
other nodes. An off-manifold state is atypical for every node.

**Dwell needs long runs.** A run must continue well past the point of interest for a stay to be
measured; the paper had twenty steps after each shift. Dwell therefore comes from sentence
sequences and scripted runs designed that long. Free play, a few ticks ending in a decision,
contributes transitions and actions-in-node, not dwell. All of it is computed within one ordering.

## 10. The views

**Two modes in the app.**
- **Population** (today): which states exist and how populations flow through the layers. Its
  step filter selects a time slice at a declared site.
- **Runs** (new): how states change over time and connect to actions.

```
Runs mode, in the app page's four panes
┌ TIMELINES (top left) ──────────────────────────────────────────┐ ┌ RUNS AND CARD (top right) ──────────┐
│ lens: friend/foe · carrier "Assessment of the person:" · L14   │ │ v3/stranger_reveal_07  scripted 7 ✓ │
│ STUDY TIMELINE   aligned on: reveal   split by: direction      │ │ v3/stranger_reveal_07  free     3 ✗ │
│  ▓▓ friend band ▓▓▓▓▓╮                                         │ │ …                                   │
│      (between the bands) ╲                                     │ │ card: tick +1 · reading −0.2 ·      │
│  ▓▓ foe band ▓▓▓▓▓▓▓▓▓▓▓▓╰▓▓▓▓▓▓▓▓   ticks −2 … +4             │ │ between the bands · would-be: wait  │
│  n:  40  40  40  40  40  40  40                                │ └─────────────────────────────────────┘
│ RUN TIMELINE (one free-play run)                               │ ┌ MUD TERMINAL (bottom left) ─────────┐
│  events │ t0 arrives │ t1 reveal │ t2 …   ▲examine ▲keep distance│ │ a watched agent plays live          │
│  lens   │ ●friend    │ ●between  │ ●foe                        │ └─────────────────────────────────────┘
│         │  └ reasoning text        └ reasoning text            │ ┌ RUN TEXT (bottom right) ────────────┐
└────────────────────────────────────────────────────────────────┘ │ observation, reasoning, action;     │
                                                                   │ the selected point highlighted      │
                                                                   └─────────────────────────────────────┘
```

Legend: ▓ a class's band from the reference runs; n the number of runs reaching each tick;
● the reading at a tick; ▲ an action; "scripted 7 ✓" a scripted run of 7 ticks with the right
outcome, "free 3 ✗" a free-play run of 3 ticks with the wrong one. Each tick's reasoning hangs
below it and never joins the next tick (rule 8).

**Same page, same panes.** Runs mode reuses the app page's four panes, as drawn. The toolbar's
session and lens pickers stay; the clustering picker belongs to Population mode.

**Later views:**
- a depth × time heatmap (the reading per layer per point), once per-layer lenses exist;
- a temporal Sankey of node transitions, once a study has enough runs and few enough nodes.

**Checking the stories against this design.**
- **Story 1** needs scripted runs and their references, the study timeline and would-be actions:
  covered. Its free-play half needs bands at matched context lengths, whose experiment is in §13.
- **Story 2** needs the run timeline with reasoning text: covered. Readings inside the reasoning
  wait for their experiment.
- **Story 3** needs nothing paper-specific: covered.
- **Story 4** needs dwell from long sequences: covered, with censoring.
- **Story 5** needs `watch` (built) and live readings: one extra pass per tick.
- **Story 6** needs conditions: covered.

## 11. Analyses

**General, built as tools:**
- crossing time after an event;
- for free play, the number of runs reaching each point and the context lengths of the runs still
  going;
- dwell and return rate per node, with censored stays counted separately;
- the lag between a reading change and a behaviour change.

**Study-specific, kept in the study:** integrator and step model selection, the remnant gap,
hysteresis loops, the paper's band rules.

## 12. What to record, retire and build

- **Record now (before the next agent study):** each tick's prompt and generated token ids (a few
  kilobytes per tick), and the run's date, chat-template hash and model-identity line, so any
  past run replays exactly (decision 7).
- **Retire now** (deletions, each with its reason; decision 6):

  | What | Why | Its users |
  |---|---|---|
  | the app's temporal panel | mixes coordinate systems (§2) | the app |
  | the lag-data endpoint | the panel's computation | the panel |
  | the temporal-runs endpoint | lists the panel's runs | the panel, the `/temporal` skill |
  | the sequence-capture route, both modes, with its cache-chain helper | even its custom mode requires a UMAP clustering with two populated basins (`temporal.py:84-98`, checked before the custom branch at line 110); it reads a moving site and can't re-append a carrier (§2) | the `/temporal` skill |
  | the `/temporal` skill | drives the retired route, in the retired basin vocabulary | — |

  The paper's method stays: the sentence-experiment route with cumulative texts plus the carrier.
- **Retire when slice 1 lands:** the raw-axis endpoint.
  - It has no callers in the app, the skills or the studies.
  - It refits a difference-of-means axis on every call and reports in-sample spreads; slice 1's
    saved mass-mean lens replaces it.
- **Slice 1:** lenses saved with their site, their calibration items (with their scene families)
  and their validation.
- **Slice 5 (agent readings):**
  - the replay reading, which also captures the calibration items: these must be rendered in the
    agent's prompt format, and the sentence-experiment route renders a single user message;
  - an entry point for scripted runs that writes a session and a tick log, with the number of
    ticks set per study;
  - would-be actions in scripted runs (an action source that generates, then plays the script);
  - reference bands;
  - Runs mode with the run and study timelines;
  - live readings for the observatory.
- **Slice 6:** node dynamics into the atlas, the node path, the heatmap, the temporal Sankey, and
  the later lanes that passed their experiments.

**The first version** is the smallest thing that answers story 1:
- the replay reading at each tick's observation, by full forward passes;
- scripted runs with would-be actions, from the new entry point;
- one validated **mass-mean** lens;
- references from scripted runs of scene families the lens wasn't fitted on;
- a run timeline with the events, the lens and each tick's reasoning text;
- a study timeline aligned on an event, against the bands, with n per point.

Everything else is an increment on it.

**Why a mass-mean lens first.** "Between the bands" is a position along one contrast, which is
what a mass-mean axis measures by design. A UMAP lens reports membership instead. It can say
"unresolved" only through a node for mixed states, which a lens fitted on clean single
observations doesn't have, or through soft membership, which waits for its experiment (§8). A
UMAP lens's node path is the first increment after this version.

**Prerequisites that aren't software:**
- friend/foe v3 needs pairs of scenarios with and without a reveal, matched in length, and long
  enough after the reveal. Today's scenarios end at a single decision;
- one date for the whole study, recorded and shared by the calibration items, the references and
  the free-play runs. The date is part of the prompt, so its tokens must match.

## 13. Experiments that settle the open questions

| Question | Experiment |
|---|---|
| Carrier placement: a question in a user turn, or a prefilled opening of the analysis? | both on the same runs: held-out accuracy against `stage_entered` labels by scene family, and drift on the references |
| The model's own words against the carrier (the first experiment) | the same runs read three ways (the carrier; natural mentions; asked-for words, with and without the request), compared on how early and how accurately each tracks the labels, tick by tick |
| Does the agent axis rotate as ticks accumulate? | cosine between the single-observation axis and one refitted on accumulated reference states, per layer (rule 4) |
| Are free-play readings matched well enough by context length? | free-play runs with constant labels against the scripted references' bands at the same length |
| Reasoning steps: is a carrier continuing the monologue stable and accurate? | the construction on the same runs, against references read at matched amounts of reasoning |
| Can a UMAP lens fitted on pooled ticks separate class from accumulation? | the per-layer k profile, with and without the reference runs in the calibration items |
| Is typicality informative at all? | planted out-of-distribution states (synthetic check), then the references |

## 14. Decisions for Andrew

1. **Time as a dimension of readings at a declared site:**
   - a carrier appended at each point and read by replay as the main method;
   - the model's own words (natural, and asked-for, as in E.4) as the second;
   - comparing them is the first experiment.
2. **Two kinds of agent study:** scripted runs (would-be actions recorded) for claims about
   dynamics, and free play for behaviour, with n per point always shown.
3. **"Unresolved" from reference bands at matched points.** The references come from scene
   families the lens wasn't fitted on, and the axis direction is checked in the regime: the
   paper's rules 2–4, made general.
4. **Node dynamics in the atlas** from sequences long enough after the event, censoring counted,
   computed within one ordering. A learned state is claimed only when the instruments agree.
5. **Runs mode beside Population mode.** The first version is minimal: the events and one
   mass-mean lens (§12 says why); a UMAP lens's node path comes next, and the other lanes after
   their experiments.
6. **Retire now** (the table in §12):
   - the temporal panel and its two endpoints;
   - the sequence-capture route with its cache-chain helper;
   - the `/temporal` skill.

   Retire the raw-axis endpoint when slice 1 replaces it.
7. **Record more with each run now,** before friend/foe v3:
   - each tick's prompt and generated token ids;
   - the run's date, its chat-template hash and the runner's model-identity line.
