# Open LLMRI — the design document

**Status:** a draft for Andrew's review (2026-10-07). Nothing new is built until he approves it.

**Review progress:** Parts A to G reviewed with Andrew (2026-10-07). Still open: L3, L9.

**Contents:**
- How this document works
- Terms
- A. What the software is for
- B. Principles
- C. Building lenses
- D. Reading over time
- E. The app
- F. The MUD
- G. Data and records
- H. The atlas and the paradigm
- I. Interventions and conditions
- J. User stories
- K. Order of work
- L. Questions for Andrew
- Appendix: decisions by date

## How this document works

**Marks.** Every passage carries one:
- **[Decided, date]**: Andrew decided it, in his own words, on that date;
- **[Andrew's idea, date]**: Andrew suggested it but didn't decide it. The design adopts it as a
  proposal until he confirms;
- **[Built]**: it exists in the software today;
- **[Proposed]**: Claude's, not yet decided. It needs Andrew's yes;
- **[Open]**: an experiment or a question settles it.

**Rules:**
- Andrew's decisions are paraphrased here, never quoted.
- Every question that needs his answer is collected in Part L.
- **What this document covers** [Proposed]:
  - it says what the software is, who uses it and how it is used;
  - how things are built stays in technical companions: `docs/architecture/one-mud.md` (the MUD)
    and `mud/docs/architecture/implementation-architecture.md` (Winter Survival's engine);
  - Winter Survival's game design document stays separate under it (question L3);
  - where this document and another disagree, this one wins, and the other is corrected.
- **Once approved, it replaces** [Proposed]:
  - the research-software draft in the one-MUD plan;
  - the time design and its review (`docs/scratchpad/time_in_the_mri*.md`);
  - the concepts in `docs/SOFTWARE_OVERVIEW.md`;
  - the user-facing parts of `one-mud.md`;
  - the scope in `LLMud/VISION.md`.

  Each of those keeps a pointer here.

## Terms

| Term | Meaning |
|---|---|
| **gpt-oss-20b** | the model studied: a mixture-of-experts (MoE) model with 24 layers |
| **expert** | one of the 32 sub-networks in each layer; each token is sent to 4 of them |
| **expert route** | the experts a token is sent to, layer by layer: four in each layer, whose weights add up to 1. "Top-1" is the expert with the highest weight |
| **pipeline** | a sequence of experts that many tokens follow through consecutive layers |
| **hub** | an expert that many different routes pass through |
| **residual stream** | a token's state at a layer: 2,880 numbers that each layer reads and adds to |
| **neuron** | one of those 2,880 numbers |
| **agent** | gpt-oss-20b playing scenarios in the MUD |
| **Claude agent** | an LLM run that writes or analyses: an analyst, an AI scientist, an author. By default Claude, run with `claude -p` (A3) |
| **sentence set** | sentences written to vary some properties on purpose and hold the rest fixed. Also called a probe set |
| **designed axis** | a property a sentence set or scenario set varies on purpose, such as the sense of "tank" |
| **target word** | the word a sentence set is captured at |
| **carrier** | a fixed sentence containing the target word, added after a context so the word is read the same way every time |
| **site** | the one token a reading is taken at |
| **scene family** | items that share one setting. Held-out tests leave whole families out |
| **capture** | the model's stored states for a sentence set or a run: residual stream, expert outputs and routing |
| **session** | one capture in the data lake |
| **schema** | today's saved clustering of a session, built layer by layer; lenses formalize it |
| **grouping** | a way to divide items into clusters, in UMAP space or in raw space |
| **lens** | a saved, validated way to read states at one site, of one of two kinds |
| **UMAP lens** | a lens that projects each layer's states with UMAP and clusters them |
| **node** | one cluster of a UMAP lens, at one layer |
| **mass-mean lens** | a lens that is one axis per layer, from one class's average state to the other's |
| **class** | one of the categories a lens separates. A mass-mean lens has two, one at each end of its axis |
| **reading** | what a lens gives for one state: a node, or a position on the axis (the class averages sit at −1 and +1) |
| **calibration items** | the labelled items a lens is fitted on |
| **lens kit** | the lenses chosen for a scenario set |
| **keyword** | a word from the scenario's MUD commands at which a kit lens is read in the agent's output |
| **scan** | reading every token of a text through a lens, each compared with how the same token reads in neutral text |
| **scenario** | a situation the agent plays in the MUD |
| **staged scenario** | a scenario of multiple-choice stages, with known labels at each stage |
| **world** | a free-form scenario with its own engine. Winter Survival is the first |
| **mini-world** | a starting situation played on a world's engine, with exit conditions (also called a microworld) |
| **scenario set** | scenarios designed together for a study, versioned, in the scenario library |
| **run** | one agent playing scenarios, or one sequence of sentences in a sentence study |
| **tick** | one agent turn: an observation, the model's reasoning, its action |
| **reasoning stream** | the model's own reasoning text in a tick (gpt-oss's analysis channel) |
| **ordering** | what a sequence of readings steps through: context steps, ticks, or reasoning steps inside one tick |
| **scaffold** | text that guides how the agent reasons, such as a system prompt, a persona or a planning prompt |
| **references** | runs whose label never changes, read with the same lens. They show where each class's readings sit at each point |
| **band** | the range holding most of one class's reference readings at one point |
| **between the bands** | a reading whose concept is present but sits between the classes at that point: the state is unresolved |
| **matched point** | a point in a run and a point in the references that are comparable |
| **scripted run** | an agent run whose actions follow a fixed script, so every run of a scenario has the same stages at the same ticks |
| **free play** | an agent run in which the model chooses its own actions |
| **would-be action** | in a scripted run, the action the model writes at a tick: recorded, not played |
| **censored** | a stay in a state cut off by the end of the run, so its true length is unknown |
| **presence** | whether a lens's concept is represented in a state at all |
| **position** | which class a reading leans to, and how far |
| **study** | a research question with its sets, runs, lenses, analyses and findings, kept as files in the repo |
| **atlas** | catalogues of nodes, experts and routes, each entry with a written report |
| **paradigm** | the accepted findings |
| **the paper** | Andrew's context-shift paper (`docs/studies/context_shift/`): how a reading changes when the context switches meaning |
| **lens catalogue** | the first research the software carries: building validated lenses for many candidate contrasts |
| **friend/foe v3** | the friend/foe scenarios redesigned as people assessment: multi-step, re-captured |
| **world-building pilot** | the planned trial of building Winter Survival's world with teams of Claude agents |
| **the institute** | Scaffold Dynamics: the MUD, with its hub, labs and simulator |

## Part A — What the software is for

**A1. The goal** [Decided, 2026-10-04, 2026-10-06 and 2026-10-07]:
- **Build an evidence-based paradigm of how gpt-oss-20b understands the world, and how it makes
  decisions from that understanding.** It covers:
  - which internal representations exist;
  - where they form: which layers, which tokens;
  - how each layer transforms them;
  - how tokens move through them, across layers and over time;
  - how experts route them, through pipelines and hubs;
  - how they lead to behaviour, including the points where reasoning fails. The context shift the
    paper studied is one of them.
- **The AI scientists work toward it with several tools:** lenses on sentence sets and scenarios,
  scaffolding experiments, steering from outside and inside the model, and ablation.
  - Scaffolding experiments show how a scaffold changes the way trajectories form, for example by
    suppressing a writing style. That is evidence about how the model works.
- **The paradigm makes it possible to monitor agents visually:** which understandings are active
  as they reason and act. This also helps in building effective scaffolds.
- **Visual knowledge discovery comes first:** cluster trajectory Sankeys, the words that travel
  through each node, colour blending, and more visual channels.
- **Another MoE model may be compared later** [Decided, 2026-10-06].

**A2. Who uses it** [Decided, 2026-10-04 and 2026-10-06]:
- **Andrew,** through the app, Claude Code and the MUD;
- **Claude agents** (`claude -p`), as analysts and AI scientists:
  - they use the same tools as Andrew, and their actions appear in the MUD as events;
  - they work in teams by topic: grammar, emotional salience, kinds of reasoning, safeguards and
    alignment;
  - they design sentence sets and scenarios from their own hypotheses and run studies on them;
- **researchers who install the software** [Decided, 2026-10-04 and 2026-10-07]:
  - they run their own app and backend;
  - they connect to Scaffold Dynamics by default, or to a MUD they run themselves, usually on
    localhost, by entering its address (F6);
- **visitors** to the MUD. A Mudlet package with simple views comes later.

**A3. Its pieces** [Decided, 2026-10-04 and 2026-10-06; Built]:
- **the app:** React, with a FastAPI backend that runs the model on the GPU;
  - the backend also runs Claude agents with `claude -p`, as often as it needs [Decided,
    2026-10-07];
  - an interface could let a user choose another LLM for those agents [Andrew's idea, 2026-10-07];
- **the MUD:** Scaffold Dynamics, the institute, running Evennia in Docker. Which server the app
  connects to is configurable (F6);
- **the data lake:** captures, kept outside git;
- **libraries and records, as files in one repo:** sentence sets, scenario sets, lab presets,
  studies, lenses, findings, the paradigm.

**A4. The first research it carries is the lens catalogue** [Decided, 2026-10-06]:
- building validated lenses for many candidate contrasts;
- finding internal representations is the aim of one kind of study, and many studies stay
  exploratory until every representation we can think of has been worked through [Decided,
  2026-10-04].

Part K gives the order of what follows.

## Part B — Principles

1. **Visual knowledge discovery first** [Decided, 2026-10-06]. Every analysis has a view.
2. **Two instruments, each measuring something different** [Decided, 2026-10-06]:
   - **UMAP lenses measure conceptual membership.**
     - They are fitted per layer, because the directions that separate concepts change from layer
       to layer.
     - What counts is which node a state falls in; the UMAP axes are never interpreted.
     - Two designed axes can give four nodes, which shows how the two are used together.
     - A trajectory is a path through each layer's nodes.
   - **Mass-mean lenses measure position on one designed contrast.** Distance along the axis is
     meaningful.
   - **Distances in full raw space are affected by noise.** The instruments read concept
     membership and contrast positions instead [Decided, 2026-10-07].
3. **Evidence over habit** [Decided, 2026-10-06]. The common habit is to move to raw space because
   UMAP distorts distances. Choices between the instruments are made by comparison instead.
4. **UMAP is preferred, once it holds up as a classifier against raw-space groupings** [Decided,
   2026-10-06].
5. **A lens is a model** [Decided, 2026-10-06]:
   - a UMAP configuration (its settings, its number of clusters) is tuned like any model, until it
     separates the classes and classifies held-out data well;
   - a lens is built from deliberately varied data, so any input that carries the concept lands in
     one of its nodes, or at its place on the axis;
   - new data is read by applying the lens;
   - nodes are never matched across separately fitted clusterings [Decided, 2026-10-07].
6. **Always MoE; experts over attention heads** [Decided, 2026-10-06].
7. **LLM agents analyse, rather than algorithms discovering circuits** [Decided, 2026-10-06; Claude
   as the default, 2026-10-07]:
   - where a decision is made is read from where a population of tokens splits between nodes, and
     from the expert routes;
   - activation patching and attribution graphs aren't planned. Circuits may come later.
8. **Claude-centred** [Decided, 2026-10-06]: Claude Code for Andrew's research, `claude -p` for
   Claude agents, the same tools for both.
9. **Screens show what matters** [Decided, 2026-10-07]: basic controls first and the rest behind
   an Advanced button; panels that size themselves to the window.
10. **The simplest design that meets every requirement** [Decided: Andrew's standing guidance,
    recorded in project memory].
11. **Design first, then build** [Decided, 2026-10-07]: this whole document is reviewed before
    anything new is built.
12. **Everything records how it was made:** model, format, decoding, seed, date, carrier, scaffold
    and intervention [Decided, 2026-10-07].

## Part C — Building lenses

Building lenses and using them to watch an agent are different activities [Decided, 2026-10-07].
This part covers building; Parts D and E cover using.

**C1. Sentence sets.**
- **What a sentence set is** [Built]: sentences that vary designed axes and hold the rest fixed,
  captured at a target word or a carrier.
- **A set can be as small as single words,** as a team studying grammar might use [Decided,
  2026-10-06].
- **Writing them:**
  - in the app, Claude agents generate sentence sets to instructions [Decided, 2026-10-04 and
    2026-10-07];
  - **one `claude -p` run writes each whole set,** all classes together, so author differences
    can't line up with the classes, and the audits check batches anyway [Decided, 2026-10-07]. This refines the
    2026-10-06 ruling that text joining a measured dataset is never written by subagents;
  - **the blind brief** [Built, as a study script]: authors see only the contrast and the
    diversity rules, as in the paper.
- **Audits** [Decided, 2026-10-07]: balance by class and scene family, length and register, a shuffle test,
  and scene diversity, promoted from the paper's scripts to tools.

**C2. Kinds of lens and grouping.**
- **UMAP lens:** usually 6 dimensions per layer, clustered, with k chosen per layer [Decided,
  2026-10-06; Built: today's schemas, with one k for every layer].
- **Mass-mean lens:** one axis per layer, validated on held-out data [Decided, 2026-10-06].
- **Raw-space groupings,** designed carefully and compared with UMAP [Decided, 2026-10-06]:
  - **standardized PCA:** centre, standardize each neuron, reduce to 50 dimensions, then
    cluster with Ward or spectral clustering [Decided, 2026-10-07: the best raw-space method in the
    2026-10-06 comparison of two sessions];
  - **relevant-neuron PCA** [Decided, 2026-10-07: Andrew's idea, with the details below]:
    - keep the neurons most associated with the sentence set's classes, then reduce them with PCA;
    - the axes are then weighted sums of named neurons, readable in raw-space terms;
    - a new token is read by a simple linear projection, which may suit watching agents;
    - **caution:** the classes choose the neurons, so separation is partly built in. The
      neurons are chosen inside each training fold, the result is judged only on held-out data,
      and it is compared with the supervised ceiling (C4), never with unsupervised groupings.

**C3. Choosing k per layer.**
- **Manual and automatic, both kept as tools** [Decided, 2026-10-07]:
  - you pick k for each layer by hand;
  - or the app suggests k for each layer and names its method.
- **Re-try the elbow method and the others on the tank polysemy sentence set,** where the number of
  senses is known [Decided, 2026-10-07].
  - In the 2026-10-06 comparison, silhouette mostly picked k = 2, which doesn't fit data that
    visibly clusters.
- **Better automatic methods** [Open]. One idea to test [Decided, 2026-10-07]: when clusters are nested,
  report every level where the structure is clear (for example 2 at the top and 5 below it),
  not one number.
- **A k profile per layer** [Decided, 2026-10-07]: for each layer and each k, the silhouette, the stability
  across seeds, and the agreement with each designed axis. The chosen k is saved with the lens.

**C4. Validating and comparing.**
- **A lens must classify held-out data well** [Decided, 2026-10-06]. The held-out data is whole
  scene families [Decided, 2026-10-07: the paper's method].
- **Sankeys from both instruments are compared** on class purity and separation, and the better
  is chosen [Decided, 2026-10-06].
- **A fair comparison** [Decided, 2026-10-07]:
  - the same k for all candidates;
  - unsupervised groupings compared only with each other;
  - groupings built from the labels shown as the **supervised ceiling**: how separable the classes
    are at all, never a competitor;
  - scores that are held out and corrected for chance.
- **A self-check** [Decided, 2026-10-07]: before lens search is trusted, it must find structure planted in
  synthetic data.

**C5. What comes with each node.**
- **The neurons behind it,** found by correlation [Decided, 2026-10-04].
- **For each split between nodes** [Decided, 2026-10-06]:
  - how much of the split comes from attention, and how much from the experts;
  - the other token positions that carry the same signal;
  - what the node pushes toward, through the output vocabulary (the logit lens);
  - a check that surface features (length, first word) don't explain it.
- **Before a key finding is accepted** [Decided, 2026-10-06]: the population is steered into the
  other node, and what changes downstream is recorded.

**C6. Lens kits.**
- **Each scenario set gets lenses designed for it, or reuses lenses already built** [Decided,
  2026-10-06; for scenario sets, 2026-10-07].
- **People assessment:** friend or foe, the type of foe [Decided, 2026-10-06], and others such as
  intent, threat, honesty and need [Decided, 2026-10-07].
- **Winter Survival:** what the agent is thinking about, such as hunger, food, fire, cold,
  injury, danger and trust in the others [Decided, 2026-10-07].
- **More lenses and situations to study will come** as the work goes on [Decided, 2026-10-07].
- **Each kit lens lists its keywords, drawn from the scenario's MUD commands** [Decided, 2026-10-07]:
  - for example the object in `greet stranger` for the friend/foe lens, or the words in `eat fish`
    and `light fire` for food and fire;
  - the lens is read at those keywords in the agent's output, where the decision is written (D3);
  - kit lenses are calibrated on text like the agent's own, since that is where they will be
    read.
- **How a lens reads a word is one of three modes** [Decided, 2026-10-06: an experiment chooses
  among them]:
  - **single token:** one word, calibrated on its own;
  - **token collection:** several words or positions calibrated together;
  - **scan:** a sweep through the sentence for any strong signal of the class.

**C7. Every lens gets a report, and lenses come in every size** [Decided, 2026-10-07]:
- LLM agents write each lens's report from its cluster and expert Sankeys, and agree on what it
  shows;
- lenses range from broad to specific. For example, a sentence set built on a taxonomy of animals
  shows where the model represents that taxonomy, and linguistic phenomena of every kind can be
  probed the same way;
- each such lens is a setting an AI scientist can learn from.

## Part D — Reading over time

**D1. Three orderings are time** [Decided, 2026-10-07]:
- context steps: a sentence sequence grows;
- ticks: the agent's turns;
- reasoning steps: the reasoning stream grows inside one tick.

The next tick's input excludes earlier reasoning streams: the runner hands back only the action as
the model's turn, which is also the convention of gpt-oss's chat format [Built]. So a reading at the
end of one tick's reasoning and one at the start of the next come from different inputs. Readings
are compared within one ordering, never across a tick. Depth (the layer) is not time.

**D2. Rules for reading over time** [Decided, 2026-10-07: the project's own rules, each kept because it earns its
place; most were learned in the paper]:
1. **The same kind of site, read the same way every time.** Otherwise a change over time is only a
   difference between sites.
2. **Validate on held-out scene families,** to know the lens learned the concept and not the
   settings.
3. **Check the lens in the context it reads.** A lens fitted on short sentences may not read the
   same way deep inside a long run.
4. **Statistics at the scene-family level.** Items from one scene aren't independent.
5. **One fixed, saved lens reads every point.** Separately fitted lenses can't be compared.
6. **Dynamics are computed within one ordering** (D1).

References are a tool for studies that compare levels over time (D5), not a rule for every
reading.

**D3. Where a run is read** [Decided, 2026-10-07]:
- **At the output: the main reading.**
  - Each lens is read at its keywords in the agent's action: the scenario's MUD commands, such as
    the object in `greet stranger`, or the words in `eat fish` and `light fire`.
  - That is the same kind of site at every tick, right where the decision is written.
- **Across the reasoning: a scan.**
  - Every token of the reasoning stream is read through each lens of the kit.
  - Each token is compared with how the same token reads in neutral text, because a raw reading at
    an arbitrary token mostly reflects what the token is.
  - The few tokens with a strong signal light up; most sentences have none.
- **Carriers, by replay: the controlled comparison.**
  - To read a recorded run at a point, take the run's exact context up to that point, add the
    lens's carrier, run one forward pass with no generation, and read the carrier's token. The run
    is untouched.
  - Carriers are the controlled comparison in agent studies, and the method for sentence studies.
- **Why the output leads for agents:**
  - carrier tokens help with demonstrations, but they don't show how the model would really act
    [Andrew's view, 2026-10-04];
  - the output is the best single place to capture understanding [Decided, 2026-10-07].
- **Two further ideas to test** [Andrew's ideas, 2026-10-06]:
  - asking the agent to use set words in its reasoning;
  - giving it words marked as for measurement only.

**D4. Two numbers in every reading** [Decided, 2026-10-07]:
- **Presence:** whether the lens's concept is represented here at all.
  - For a UMAP lens: how close the state is to the members of its nodes.
  - For a mass-mean lens: how strong the signal is, compared with the same token in neutral text.
- **Position:** which class the reading leans to, and how far.
- **Unresolved and absent are told apart:**
  - unresolved means present but between the classes;
  - absent means the concept isn't there.
  - One number on one axis can't tell these apart: its middle could mean either.
- **At the output, a reading should have resolved into its class,** unless there is a real
  incongruity. A reading that is present but still between the classes at the output is flagged,
  as something worth opening in Watch.
- **A caution** [Proposed]: presence must be calibrated on states that include natural in-between
  ones. On synthetic data, states halfway between two classes looked far from both classes'
  calibration states. Calibrated on clean classes only, a torn state would look absent.

**D5. "Between the bands" in studies** [Decided, 2026-10-07]:
- **In a study, "between the classes" is judged against bands,** the range of each class's readings
  at that point.
- **The bands come from references:** runs whose label never changes, from scene families the lens
  wasn't fitted on.
  - References are the general form of what the paper's no-shift runs did, which were specific to
    the paper: readings drift as context grows, whatever the class.
- **Agent studies come in two kinds:**
  - **scripted runs,** where every run has the same ticks, for claims about change over time;
  - **free play,** for behaviour, always showing how many runs reach each point.
- **The context-shift study's own question** [Decided, 2026-10-07: it belongs to that study, not to
  the software as a whole]: when an understanding shifts, what is the state in between?
  - a **learned state:** a stable intermediate representation the model has and uses;
  - a **passage:** a brief crossing from one state to another;
  - an **off-manifold state:** something outside the states the model normally takes.

  It is an example of a study that reads over time.

**D6. Questions experiments settle** [Open; Decided, 2026-10-07: the design stays flexible, and
more questions will come]:
- How early and how accurately do the output reading, the scan and the carriers track the
  scenario's labels, tick by tick? This is the first agent experiment.
- Which reading mode works at keywords: single token, token collection or scan?
- What neutral text should the scan compare against, and should it be per token or per kind of
  token?
- How is presence best measured, and does it separate absent from unresolved? Test it first on
  planted synthetic states, then on runs.
- Does a lens still read the same way as ticks accumulate (rule 3)?
- Can free-play runs be compared with references at equal context length?
- Does a carrier work better as a user's question, or as the opening of the model's reasoning?

**D7. The first version is tested on known answers** [Decided, 2026-10-07]:
- it must reproduce the paper's per-run tank results from the paper's tank runs, before it is used
  on agents. The results are the crossing point, the settled level and the dwell, in
  `tank_d3_metrics_L4.csv`;
- a subset of those sessions is copied from the C: drive for this.

## Part E — The app

**E1. Workspaces** [Decided, 2026-10-07]. The app is for analysing: runs that have happened, clusterings, and
the reports the LLMs write. It also holds the builders. It doesn't start runs; they start in the
MUD or through Claude Code (F3). It follows a run in progress one saved tick at a time (E4).

| Workspace | What you do there | Status |
|---|---|---|
| **Build** | write sentence sets and scenarios; build lenses and kits | new |
| **Layers** | see how a population flows through the layers: today's main view, improved | improved |
| **Watch** | follow one run, live or recorded | new |
| **Study** | compare many runs | new |
| **MUD** | maintain the MUD and design scenarios, with Claude agents' help | new |
| **Atlas** | browse nodes, experts and routes, with their reports | later |
| **Ideas** | track every research idea, generate new ones, follow the AI scientists. The idea evolver's engine moves into this repo | later [Decided, 2026-10-04] |

**E2. Rules for every screen:**
- **Basic controls first, the rest behind Advanced** [Decided, 2026-10-07]. For example,
  clustering's Advanced holds automatic k detection and the choice of method.
- **Panels size themselves to the window** [Decided, 2026-10-07]. Dividers can be dragged, and any panel can fill
  the screen and come back.
- **The MUD terminal folds away when it isn't needed** [Decided, 2026-10-07, approved in the time
  review].
- **The main pane shows one timeline at a time** [Decided, 2026-10-07, approved in the time
  review]. One chart per panel everywhere [Decided, 2026-10-07].
- **Each variable gets one visual channel,** such as colour, shape, pattern or line style, and the
  legend is always on [Decided, 2026-10-07, approved in the time review].
- **Missing pieces are named** [Decided, 2026-10-07, approved in the time review]:
  - with no validated lens for a site, the view says so and links to where lenses are built;
  - with too few runs at a point, that point is drawn faded.
- **No sideways scrolling of the page** [Decided, 2026-10-07]. Only charts meant to scroll do, such as the
  all-layer Sankeys.
- **An analysis panel beside each view** [Decided, 2026-10-07]: the LLM-written report on whatever is selected
  (E8).
- **Every chart exports its picture (SVG, PNG) and its data (CSV, JSON)** [Decided, 2026-10-07,
  approved in the time review].

**E3. Build.**
- **The sentence set builder** [Decided, 2026-10-07: it shows the instructions given to the authoring agents and
  the sets that come back; one `claude -p` run writes each whole set (C1)]:
  1. Describe the contrast: the target word, the classes, the carrier, the number of sentences per
     class, the scene families, the diversity rules.
  2. Read and edit the brief the authors will receive.
  3. Generate.
  4. Review the sentences in a table (text, class, scene family) beside the audits (C1). Edit or
     regenerate.
  5. Save the set with a version, then start its capture as a background job.
- **The scenario builder** [Decided, 2026-10-07]:
  - it lists scenario sets and their versions;
  - you edit a scenario's stages, actions and labels, and validate them;
  - you play it yourself in the simulator, or have the agent play it;
  - Claude agents can draft scenarios to instructions;
  - a mini-world builder comes later, with Claude agents and skills.
- **The lens builder** [Decided, 2026-10-07]:
  1. Pick a capture.
  2. **Basic:** UMAP n_neighbors and dimensions, k, a name, Build.
  3. **Advanced:**
     - k per layer, with the automatic suggestion and its method;
     - the reduction and grouping methods (C2);
     - filters.
  4. The build runs in the background, and the new lens opens when it is ready.
  5. Read the k profile and the held-out scores (C3, C4), then save the lens with its site and
     keywords.
- **The kit editor** [Decided, 2026-10-07]: for a scenario set, choose the lenses and their keywords.

**E4. Watch: which representations are active over time.**

Andrew's request [Decided, 2026-10-07]:
- for each scenario set, its own panel of lenses;
- a lens heatmap showing what is active in each sentence: every token is scanned through each lens,
  and most sentences show nothing;
- each lens read at the output too, at keywords from the scenario's MUD commands, since the output
  is the best place to capture understanding;
- for each lens, its own Sankeys: clusters, experts, latent space;
- lens panels, as many as you want, to see which light up;
- replay, explained readings, bookmarks, runs side by side and live alerts;
- good use of screen space.

**The layout** [Decided, 2026-10-07]: the lens heatmap on top, the lens panels below it, and a side drawer. Each
area can be resized and can fill the screen.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ run: v3/stranger_reveal_07 (live) · kit: people assessment · ◀ ▮▮ ▶ tick 1 of 3          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ LENS HEATMAP · brightness: presence · colour: which class                                │
│ events      │ t0 arrives      ▲   │ t1 reveal           ▲   │ t2 …                       │
│             │  O  R1 R2 R3   A    │  O  R1 R2 R3 R4   A    │                             │
│ friend↔foe  │  ·     █       █    │  ▒  ▒     ░  ▒    ░ !  │                             │
│ intent      │     ·  ▒            │     ▒  ▒          ▒    │                             │
│ threat      │                     │  ▒     ▒  ▒  ▒    ▒    │                             │
│ honesty     │        ░            │        ░  ▒            │                             │
│ █ ▒ strong, one class or the other · ░ present, between the classes · · faint            │
│ A the output reading, at the lens's keywords · ! still between at the output             │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ LENS PANELS · sorted by presence in tick 1 · pinned first · + add lens                   │
│ ▣ friend↔foe   clusters ⇄ experts   L0 ──────────────────────────────────────── L23 ▸    │
│     calibration flows faded; the output keyword's path in colour                         │
│ ▣ threat       clusters ⇄ experts   L0 ──────────────────────────────────────── L23 ▸    │
│     the strongest token's path (no threat keyword in this action)                        │
│ ▢ honesty      not present in tick 1: dimmed                                             │
└──────────────────────────────────────────────────────────────────────────────────────────┘
  side drawer: the run's text, tokens tinted by the selected lens · bookmarks · MUD
```

(The sketch shows ticks opened. By default each tick is one column; see below.)

**The lens heatmap:**
- **Rows:** the kit's lenses, grouped by theme, for example the person, the body, the world.
  - Each row's label names the lens's classes and its keywords.
  - A badge says whether the lens is validated where it is read, or exploratory there.
- **Columns:** time.
  - **By default each tick is one column,** holding the tick's output reading [Decided, 2026-10-07, approved in
    the time review]. During a live run the newest tick opens by itself.
  - **Opening a tick shows its parts:** the observation (O), the reasoning sentence by sentence
    (R1, R2, …), and the output (A).
- **Cells in the observation and the reasoning:** the scan's strongest token in that sentence, for
  that lens (D3).
  - Brightness is presence; colour is position, which class and how far (D4).
  - A UMAP lens colours by node.
  - Blank means nothing in that sentence carried the concept, which is the usual case.
- **The output cell (A):** the lens's reading at its keywords in the action. It is flagged (!) when
  the concept is present but still between the classes.
- **The events lane:** stage changes with their labels, and each action coloured by its type in the
  scenario file (friend or enemy in today's set).
- **The layer:** each lens is read at its best held-out layer by default [Decided, 2026-10-07, approved in the time
  review]. A selector changes it.

**The lens panels** [Decided, 2026-10-07]:
- **As many as you want, one lens per panel,** in a column that scrolls and sizes itself.
- **Each panel shows its lens's cluster Sankey,** with a toggle to its expert Sankey:
  - the cluster Sankey: the lens's calibration items flowing through its nodes, layer by layer;
  - the expert Sankey: their routes through the experts.
- **Panels sort by how strongly their lens is present in the selected tick.** Pinned panels stay at
  the top, and a panel whose lens isn't present dims, so the ones that light up stand out.
- **A mass-mean lens gets a Sankey too:** at each layer its readings fall into three bins: one
  class, between the classes, the other class.
- **All 24 layers in each panel,** scrolling sideways together, so a layer lines up across panels
  (E5).

**Which token each panel uses** [Decided, 2026-10-07, for now]:
- **To decide whether a lens lights up in a tick,** the panel takes the tick's strongest token. It
  compares that token with the strongest token in neutral text of the same length. The strongest of
  hundreds of tokens always looks fairly strong by chance, so a lens lights up only when it beats
  that level.
- **To draw the path, and compare ticks,** the panel takes the output keyword: the same kind of token
  every tick, at the decision. If the lens has no keyword in that tick's action, the panel falls
  back to the strongest token and says so.
- **Clicking any heatmap cell, or any token in the text,** switches the panels to that token. Each
  panel then draws its path over the faded calibration flows:
  - in the cluster Sankey, its node at each layer, found by applying the lens;
  - in the expert Sankey, the experts it actually used at each layer.

**Replay** [Decided, 2026-10-07]:
- play, pause and step through a recorded run tick by tick;
- the heatmap, the lens panels, the text and the MUD transcript all move together;
- it is the app's version of replaying a run in a scenario room (F1).

**A reading explains itself** [Decided, 2026-10-07]:
- hovering a lit cell shows the lens's own calibration sentences closest to that state;
- presence already finds those nearest states, so the examples cost nothing extra.

**Bookmarks** [Decided, 2026-10-07]:
- mark a moment with a note, for example that the agent misread the person here;
- the note is saved into the study's files, where analyst agents read it as evidence.

**Side by side** [Decided, 2026-10-07]:
- two runs with their ticks aligned;
- for example the same scenario with and without steering, ablation or a scaffold, or played by
  two different agents;
- Study compares averages; this compares cases.

**Live alerts** [Decided, 2026-10-07]:
- tell me when a chosen lens lights up, or when a reading is still between the classes at the
  output;
- the first step toward monitoring agents (A1).

**A run in progress** [Decided, 2026-10-07]:
- Watch opens it like a finished run. Each tick appears once it is saved, with its keyword
  readings.
- The scan never slows the agent. Its readings fill in as they are computed, at the latest when
  the run ends.
- Alerts fire as soon as the readings they watch exist.
- The agent's play is watched in the MUD (`watch agent`), in the drawer's terminal.

**The side drawer:**
- it holds the run's text (observation, reasoning, action), each token tinted by the selected
  lens's scan, so you can see which words lit up;
- it holds the bookmarks;
- during a live run it also holds the MUD terminal, where `watch agent` follows the agent;
- outside a live run, the terminal folds away.

**What Watch needs from the rest of the software** [Proposed]:
- the runner captures the kit's keywords in each action, and stores each tick's token ids;
- the scan runs by replay over each tick's whole text, and stores only the readings: presence and
  position, per token, lens and layer;
- each lens has:
  - a neutral baseline: how each token reads in neutral text;
  - the chance level for the strongest token in neutral text of each length;
  - a nearest-neighbour index over its calibration states, shared by presence and the explained
    readings;
- the paths for each tick's default tokens are worked out with the readings;
- readings are computed once, stored and shown. A live run adds one tick at a time.

**Risks, and what answers them:**
- **A raw reading at an arbitrary token mostly shows what the token is.** The scan compares each
  token with the same token in neutral text.
- **The strongest of many tokens looks strong by chance.** Lighting up is judged against the chance
  level.
- **The middle of an axis can mean torn or absent.** Presence tells them apart (D4), and presence is
  calibrated on states that include natural in-between ones.
- **Readings drift as a run grows.** By default the heatmap shows raw readings. With references,
  Advanced shows them against the bands.
- **A lens not yet validated where it is read** carries the exploratory badge.
- **Many lenses take space.** Heatmap rows group and fold, empty rows hide, and lens panels sort and
  dim.

**E5. Layers** (today's main view, improved) [Decided, 2026-10-07]:
- **All 24 layers in one view that scrolls sideways.** It replaces today's four fixed six-layer
  windows, whose edges cut flows [Built].
  - A zoom sets how many layers fit (6, 12 or 24).
  - An overview strip shows where you are.
- **The cluster Sankey and the expert Sankey are stacked and scroll together.**
- **Expert weights are the model's own** [Decided, 2026-10-07]:
  - wherever a weight is shown, it is the expert's weight among the token's four, not a figure
    computed over all 32 experts, as today's are;
  - all four ranks can be chosen; today only the first three can.
- **Clicking a node lists the runs that pass through it, and when** [approved in the time review].
- **Clustering can be run from this view, and from the polysemy lab's room in the MUD** [Decided,
  2026-10-04].
- **More visual channels than colour blending,** such as lines shaped by sine waves [Decided,
  2026-10-06], and patterned Sankey nodes.
- **Colour by any designed axis.** Today only the label can colour.
- **Cards with LLM-written reports** for clusters, experts, routes and expert routes (E8).

**E6. Study** [Decided, 2026-10-07: the parts below were approved in the time review]:
- **A study file sets up the view:** its runs, references, lens, layer, the event to align on, and
  how runs are grouped. You pick a study; Advanced overrides a setting for one look.
- **The study timeline:**
  - the readings over time, grouped by condition, against the bands;
  - a confidence interval from a bootstrap over scene families;
  - the number of runs at each point.
- **The run list:**
  - one list, whether a run was started in the MUD or through Claude Code, and marked with which;
  - each run's ticks between the bands, its crossing tick, its final class and its outcome, all
    sortable.
- **Opening a run** replaces the study timeline with that run's timeline, with a way back. A button
  also opens the run in Watch.
- **Behaviour:** each tick's action, or would-be action, against its reading.
- **Readings are background jobs,** computed once and stored. A study of 200 runs × 7 ticks takes
  about 25–70 minutes of GPU.

**E7. The app takes commands** [Decided, 2026-10-04: the app updates its views when told to,
through some syntax; one interface, 2026-10-07]:
- Claude Code, Claude agents and MUD commands use one small command interface to open a view, run a
  clustering or choose a lens.

**E8. LLM analysis** [Decided, 2026-10-07: an analysis panel wherever it helps, and cards with LLM-written reports
for clusters, experts, routes and expert routes].

LLMs are good at spotting patterns in this data, such as pipes, hubs and split points.

**The panel, the same everywhere** [Decided, 2026-10-07]:
- it sits beside a view and shows the report on whatever is selected;
- each report cites the numbers it used, and a checker re-computes them;
- reports are written in the background when their data is built, kept, and rewritten when the
  data changes;
- a question box asks a follow-up question about the current view;
- reports are marked as LLM-written. A finding still goes through the paradigm's review (Part H).

**Where analysis goes:**

| Where | What the LLM writes | Status |
|---|---|---|
| Layers | a card for each cluster, expert, route and expert route | Decided, 2026-10-07 |
| Layers | a card for each split point: what separates the two populations | Decided, 2026-10-07 |
| Layers | a report on the expert Sankey's pipes and hubs | Decided, 2026-10-07 |
| Layers | a short note on what each layer transition changes | Decided, 2026-10-07 |
| Build | a critic for each new sentence set, catching confounds the numeric audits can't, such as one class always written in the past tense | Decided, 2026-10-07 |
| Build | each lens's report (C7) | Decided, 2026-10-07 |
| Build | a k advisor that explains the k profile while you choose | Decided, 2026-10-07 |
| Watch | a run report: when the understanding formed, where it went wrong, why each flag fired | Decided, 2026-10-07 |
| Watch | a short note on a clicked moment | Decided, 2026-10-07 |
| Watch | a comparison report for runs side by side | Decided, 2026-10-07 |
| Study | a study report on crossings, and on the differences between conditions | Decided, 2026-10-07 |
| Atlas | reports connecting lenses, such as an expert or pipe that serves several of them: the start of the coherent model | Decided, 2026-10-07 |
| Ideas | what to probe next, from the gaps in the atlas | Decided, 2026-10-07 |
| MUD (later) | a guide in each lab who answers questions about the lab's view from the cards | Decided, 2026-10-07 |

## Part F — The MUD

**F1. What it is for** [Decided, 2026-10-04 and 2026-10-07]:
- experiencing, playing and watching: the institute, its labs, the simulator, and later the AI
  scientists' rooms and their events;
- entering a scenario room to replay a run and watch which internal representations light up
  [Decided, 2026-10-04];
- a user interface can live in the MUD [Andrew's idea, 2026-10-04];
- writing sentence sets and scenarios happens in the app's builders, not in the MUD [Decided,
  2026-10-07].

**F2. Rooms:**
- **the hub,** where everyone starts [Built];
- **the polysemy lab,** which opens its view on entry: `tank_polysemy_k6_n20` of session
  `1434a9be` [Built; the clustering decided 2026-10-06];
- **the simulator,** the scenario library's menu [Built];
- **the AI scientists' rooms** [Decided, 2026-10-04];
- **researchers' rooms** [Decided, 2026-10-07: planned].

**F3. Commands** [Built]. Andrew asked for every command to be documented [2026-10-07].

| Where | Command | What it does |
|---|---|---|
| anywhere | `look` | see the room |
| institute rooms | `watch <name>` | follow a character, such as `agent`, into each scenario it plays |
| institute rooms | `unwatch` | stop watching and go back |
| a watched scenario | `look`, `examine`, `actions` | a watcher reads the scenario and every line the player types |
| a watched scenario | — | a watcher can't act or speak there, since anything said would reach the agent's prompt |
| the simulator | `simulator` | list the scenario library's sets |
| the simulator | `simulator <set>` | list one set's scenarios |
| the simulator | `simulate <set> [<scenario>]` | play a scenario yourself. It opens with what the agent sees: the room, your inventory and the choices. Researchers only |
| the simulator | `agent run <set> [<scenario>]` | have the agent play scenarios while its activations are captured. Without a scenario it plays the whole set. Researchers only |
| the simulator | `agent stop` | stop the agent's run |
| a staged scenario | `look`, `examine <thing>`, `inventory` | read the situation |
| a staged scenario | `actions` | list the choices |
| a staged scenario | a choice's command | take that choice |
| a staged scenario | `leave` | go back to where you came from |
| Winter Survival | the world's grammar: `VERB thing [RELATION thing] [WITH tool]` | play the world |
| the login screen | `connect guest` | visit as a guest; guests can watch |

**Agent runs start in the MUD, with `agent run`, or through Claude Code** [Decided, 2026-10-07]. The app doesn't
start runs; it analyses them (E1). Today `agent` exists only in the simulator.

**F4. What the MUD plays** [Decided, 2026-10-04 and 2026-10-06]:
- sentence-set probes;
- staged scenarios: multiple choice, in stages, with known labels at each stage;
- worlds: Winter Survival is the first of many;
- mini-worlds: a starting situation on a world's engine, with exit conditions.

**F5. The agent in the MUD** [Built]: the runner plays through a control channel, and nothing a
watcher does reaches the agent.

**F6. Which MUD** [Decided, 2026-10-07]:
- by default the app and the backend connect to Scaffold Dynamics, the project's server;
- a user can run their own MUD instead, usually on localhost, and enter its address;
- today the address comes from the root `.env` and is always localhost [Built].

## Part G — Data and records

- **The data lake** [Decided, 2026-10-04: not copied wholesale; 2026-10-06: the six sessions kept]:
  - captures stay outside git;
  - the WSL lake holds the six kept sessions and every new capture;
  - the paper's lake stays on the C: drive.
- **The libraries:**
  - sentence sets and scenario sets, each set in its own folder for its study [Decided,
    2026-10-06];
  - scenario sets have versions, guides and provenance. Studies cite a set as `set@version`, and a
    set used by a finished study is never changed [Built].
- **Studies, lenses, findings and the paradigm are files in the repo** [Decided, 2026-10-06].
- **Captures include states after generation starts,** not only before it [Decided, 2026-10-06].
  Agent runs already capture every target word in the generated text [Built].
- **Each run records** [Decided, 2026-10-07: principle B12]:
  - its token ids for each tick, its date, its chat-template hash and its model-identity line, so it
    can be replayed exactly;
  - the capture recipe: model, format, decoding, seed, carrier, token sets, scaffold, intervention.
- **Routing is recorded in full** [Built]: every capture stores all 32 routing weights for each
  captured token at every layer. The model's own weights for its four experts are computed from
  them (the top four, scaled to add up to 1), so using all four ranks needs nothing new captured
  (E5, H).
- **Retirements** [Decided, 2026-10-07]:
  - **when building starts:**
    - the basin-era temporal panel and its two endpoints, replaced by the run and study timelines
      (E6) and Watch (E4);
    - the old sequence-capture route and its cache helper. The paper's method stays (cumulative
      texts with a carrier, through the sentence-experiment route), and agent runs use replay;
    - the `/temporal` skill, replaced by a skill for sentence runs over time;
  - **when saved mass-mean lenses replace it:** the raw-axis endpoint;
  - the suicide-letter study's capture scripts call the old sequence-capture route. They stay, as
    the record of how those captures were made.

## Part H — The atlas and the paradigm

- **The atlas has three catalogues** [Decided, 2026-10-06], each entry with a report written by a
  Claude agent:
  - **nodes:** every node of every validated lens, layer by layer;
  - **experts:** all 24 × 32;
  - **routes:** pipelines and hubs, built from all four of each token's experts and weighted by the
    model's own weights [Decided, 2026-10-07]. Today's routes follow only the top-1 expert; the
    top-1 Sankey stays as one view of them.
- **Time adds node dynamics** [Proposed]: how long runs stay in a node, what comes before and after
  it, and what the model does while in it. This is how a question like the context-shift study's
  (D5) gets answered, node by node.
- **Bringing the lenses' findings together into one coherent model is the hard part** [Decided,
  2026-10-07].
- **The paradigm is the accepted findings** [Decided, 2026-10-04 and 2026-10-06]:
  - the AI scientists propose findings, attack them and give evidence;
  - several models vote, and when most of them agree, the finding goes to Andrew for review;
  - knowledge consolidators extract the insights.

## Part I — Interventions and conditions

- **Steering and ablation, with behaviour studies** [Decided, 2026-10-06].
- **Steering a node and seeing what changes downstream** [Decided, 2026-10-06].
- **Scaffolds, and steering from outside and inside the model:** how each changes trajectories
  [Decided, 2026-10-06].
- **A scaffold comparison includes a neutral scaffold** of the same length and format [Proposed].
  Added text alone shifts readings, so this separates a scaffold's content from its presence.
- **How interventions are done** [Proposed]:
  - routing drift is always recorded;
  - an option to steer only in directions the router doesn't use;
  - expert masks through the router's bias.
- **Another MoE model** for comparison [Decided, 2026-10-06].

## Part J — User stories

Stories 1–6 come from the time design; 7–11 were added in its review, which Andrew asked to see
[2026-10-07]; 12–15 come from his 2026-10-07 requests. The steps in each are [Proposed].

1. **An agent study.** People-assessment scenarios with and without a reveal, as scripted runs.
   - Study shows the reading at each tick against the bands, and the would-be actions.
   - Free play then shows what the agent did with those states.
   - Needs friend/foe v3, the scripted entry point, lens kits, and Study.
2. **One run.** Sort Study's run list by ticks between the bands and open the top run. See where its
   reading sat between the bands, what the agent reasoned there, and what it did.
3. **A sentence study.** Sentence sequences with a fixed carrier, and references, in Study.
4. **The atlas.** A Claude analyst reads each node's dwell, neighbours and actions, and writes the
   node's report.
5. **Watching live.** `watch agent` in the MUD; in Watch, each tick appears once it is saved, and
   its scan fills in as it is computed. Needs lens kits.
6. **Steering.** Steered and unsteered runs as two conditions on one timeline.
7. **Check the instrument.** Reproduce the paper's per-run tank results in Study (D7). Every later
   story rests on this one.
8. **Compare the reading methods.** For the same runs, the carrier and the model's own words, as two
   rows.
9. **Follow the reasoning.** Open a tick in Watch's heatmap and see, sentence by sentence, where each
   lens's reading shifts.
10. **From a moment to the layers.** Click a cell in the heatmap; the four Sankey panels show that
    word's path through each lens's nodes and experts.
11. **Hand a study to an analyst.** Export a study's readings and events; a Claude analyst writes the
    report, and its numbers are re-checked.
12. **Create a new polysemy sentence set in the app.**
    - Build › sentence sets: describe the contrast, read the brief, generate, review with the audits,
      save, capture.
    - Build › lenses: cluster with the basic form, see the Sankeys across all layers, set k per layer
      under Advanced, validate, save the lens.
13. **Find the right k per layer.** Compare the automatic suggestion and its method with the k
    profile and your own choice, and save the k that classifies held-out data best.
14. **Build a kit for Winter Survival.** Choose its lenses and their keywords, and check each lens
    is validated where it will be read.
15. **Visit as a guest.** `connect guest`, then `watch agent`, and read the run as it plays.

## Part K — Order of work [Proposed, except where marked]

1. **Now:** Andrew's walk through the MUD, then the one-MUD branch merges into main. No new features.
2. **This document:** reviewed with Andrew section by section, then approved.
3. **Then the build, in slices:**
   1. **The lens core** [Decided, 2026-10-06: before the world-building pilot]:
      - validated, saved lenses;
      - k per layer, manual and automatic;
      - the comparison of UMAP with raw-space groupings;
      - atlas nodes, first version;
      - the clustering form, basic and Advanced [Decided, 2026-10-07; Andrew left its timing to
        Claude];
      - added by Claude [Proposed]: the all-layer Layers view, colour by any designed axis, study
        files, the analysis panel with its cards for clusters, experts, routes and expert
        routes, and the model's own expert weights with all four ranks.
   2. **The sentence set builder:** the lens catalogue starts with new sentence sets.
   3. **Time on sentence runs,** checked against the paper's tank results (D7), in Study.
   4. **Provenance and jobs:**
      - the capture recipe and per-run token ids;
      - the GPU job queue.
   5. **The world-building pilot** [Decided, 2026-10-06: after the lens core].
   6. **The scenario builder,** then friend/foe v3 [Decided, 2026-10-06: v3 after the lens core].
   7. **Agents:**
      - lens kits and keywords;
      - the scan, with each lens's neutral baseline;
      - replay;
      - scripted runs and would-be actions;
      - Watch, with its lens panels, replay, explained readings, bookmarks, runs side by side and
        live alerts;
      - the experiments of D6.
   8. **Conditions and interventions:** scaffold studies, steering, ablation.
   9. **Layer transitions and trajectory upgrades,** such as patterned nodes.
   10. **A second MoE model.**
   11. **The paradigm and the AI scientists:**
       - votes;
       - evidence packets with number checks;
       - the Ideas workspace;
       - the scientists' rooms;
       - monitoring.

## Part L — Questions for Andrew

- **L1. Who writes sentence sets in the builders?** Answered 2026-10-07: one `claude -p` run writes
  each whole set, all classes together, and the audits check batches (C1).
- **L2. Which reading leads for agents?** Answered 2026-10-07: the output reading at keywords
  leads, the scan shows the reasoning, and carriers are the controlled comparison (D3).
- **L3. Should Winter Survival's game design document fold into this one, or stay separate under
  it?** You asked for one design document; this draft keeps the world's own document separate.
- **L4. The time design.** Answered 2026-10-07: the orderings, the project's own rules, presence
  and position, and references for studies (D1–D5).
- **L5. The retirements in Part G.** Answered 2026-10-07: yes; three when building starts, the
  raw-axis endpoint when saved lenses replace it (G).
- **L6. Watch (E4).** Answered 2026-10-07: the layout as drafted, with lens panels as many as
  wanted, the token rule, replay, explained readings, bookmarks, side by side and live alerts.
- **L7. The workspaces (E1).** Answered 2026-10-07: as drafted.
- **L8. Relevant-neuron PCA (C2).** Answered 2026-10-07: yes, as a third kind of grouping, with the
  cautions given.
- **L9. The order of work (Part K):**
  - Is the sentence set builder second, and time on sentence runs third, right?
  - Should slices 2–4 come before the world-building pilot, as drawn, or after it?
- **L10. Where agent runs start.** Answered 2026-10-07: in the MUD or through Claude Code, never from
  the app (F3).
- **L11. One command interface (E7).** Answered 2026-10-07: yes.
- **L12. LLM analysis (E8).** Answered 2026-10-07: every place in the table.
- **L13. Live runs in the app?** Answered 2026-10-07: Watch follows a run in progress one saved tick
  at a time; the scan never slows the agent; the agent's play is watched in the MUD (E4).

## Appendix — Decisions by date

Paraphrased from Andrew's own words. His ideas not yet decided are listed separately.

- **2026-10-04 decisions:**
  - one repo and one MUD, hosting the institute, labs and scenarios;
  - the goal and its tools (A1);
  - the AI scientists design sentence sets and scenarios and run studies from their hypotheses;
  - teams of AI scientists, with a paradigm voted on;
  - running clustering from the polysemy lab;
  - an app that takes commands;
  - a conceptual exploration tab, and the idea evolver's engine moving in later;
  - replaying runs in a scenario room;
  - a Mudlet package later;
  - the data lake not copied wholesale;
  - the neurons behind clusters, by correlation.
- **2026-10-06 decisions:**
  - the research-software review and design before the pilot;
  - the lens catalogue first;
  - the research record as files in the repo;
  - the AI scientists use the tools directly, shown in the MUD;
  - the two instruments, and a lens treated as a model;
  - UMAP preferred once it holds up against raw space;
  - three reading modes, chosen by experiment;
  - Sankeys from both instruments, compared;
  - k per layer;
  - raw-space groupings designed carefully;
  - more visual channels;
  - always MoE, and Claude agents analysing;
  - the atlas and the paradigm;
  - lenses built from varied data, read by applying them;
  - lens kits per scenario;
  - people assessment, starting with the type of foe;
  - what comes with each node split;
  - no activation patching or attribution graphs for now;
  - friend/foe v3 after the lens core, and the lens core before the pilot;
  - the six kept sessions;
  - the polysemy lab's clustering;
  - the names Winter Survival and Scaffold Dynamics;
  - text joining a measured dataset written in the main conversation, never by subagents.
- **2026-10-07 decisions:**
  - the goal (A1): an evidence-based paradigm of how gpt-oss-20b understands the world and decides.
    Scaffolding experiments are one of the AI scientists' tools toward it, and monitoring agents
    is what the paradigm makes possible;
  - the in-between-state question belongs to the context-shift study, not to the software as a
    whole;
  - researchers who install the software connect to Scaffold Dynamics by default, or to their
    own MUD, whose address they enter;
  - the backend runs Claude agents with `claude -p` as often as it needs; no separate runner;
  - the principles of Part B, including LLM agents analysing with Claude as the default, and
    recording how everything was made;
  - every lens gets a report written and agreed by LLM agents; lenses range from broad (a
    taxonomy of animals) to specific, across all kinds of linguistic phenomena;
  - bringing the findings together into one coherent model is the hard part;
  - the old prototype retired once everything works in the MUD;
  - the clustering form, and manual and automatic k;
  - re-try the elbow method on the tank set;
  - a UX pass over the app and the MUD;
  - the sentence set builder and the scenario builder;
  - simulate shows what the agent sees;
  - one design document with a web view;
  - planned work kept in the plan;
  - the time review: test on the paper's tank runs first, and all its suggestions;
  - kits per scenario set;
  - building lenses separate from using them;
  - design approved before building;
  - researchers' rooms planned;
  - Claude agents generating sentence sets: one `claude -p` run writes each whole set, all classes
    together, and audits check batches;
  - Part C's details: the audits, the raw-space recipe, relevant-neuron PCA as a third grouping,
    the k profile and the hierarchy idea, scene-family hold-outs, the fair comparison, the
    self-check, keywords, and the kit examples (food, fire and more for Winter Survival);
  - every place for LLM analysis in E8, and the panel's design;
  - agent runs start in the MUD or through Claude Code; the app analyses runs, clusterings
    and reports, and holds the builders;
  - Part E: the workspaces, the screen rules, the builders' steps and the kit editor; Watch's
    layout, lens panels as many as wanted, which token each panel uses, replay, explained
    readings, bookmarks, runs side by side (conditions such as steering, ablation and
    scaffolds, or different agents) and live alerts; the Layers improvements; Study's button
    to Watch; one command interface; an analysis panel wherever it helps, with LLM cards for
    clusters, experts, routes and expert routes;
  - Part D: the orderings, with earlier reasoning excluded from later ticks; the project's own
    rules for reading over time; the output reading at keywords from the MUD commands as the
    main reading; the scan over the reasoning; carriers as the controlled comparison; presence
    and position in every reading, with unresolved told apart from absent; the flag for a
    reading still unresolved at the output; references for studies; the experiments left open;
  - Part G: expert weights read as the model's own, over each token's four experts, with all four
    ranks, and routes built from all four; the retirements of the basin-era temporal tools;
  - Watch follows a run in progress one saved tick at a time, and the scan never slows the agent.
- **Andrew's ideas, not yet decided:**
  - **2026-10-04:** a user interface in the MUD;
  - **2026-10-06:** asking the agent to use set words in its reasoning; giving it words marked as for
    measurement only;
  - **2026-10-07:**
    - an interface so users can choose the LLM for Claude agents' work.
