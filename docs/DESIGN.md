# Open LLMRI — the design document

**Status:** approved by Andrew on 2026-10-08. It is the design's source of truth; changes go through him.

**Review progress:** every part reviewed with Andrew (2026-10-07), and Part M's recommendations
adopted into their parts (2026-10-08).

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
- M. Claude's final read: certainty and recommendations
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
- **What this document covers** [Decided, 2026-10-07]:
  - it says what the software is, who uses it and how it is used;
  - how things are built stays in technical companions: `docs/architecture/one-mud.md` (the MUD)
    and `mud/docs/architecture/implementation-architecture.md` (Winter Survival's engine);
  - Winter Survival's game design document stays separate under it (question L3);
  - where this document and another disagree, this one wins, and the other is corrected.
- **Once approved, it replaces** [Decided, 2026-10-07]:
  - the research-software draft in the one-MUD plan;
  - the time design and its review (`docs/scratchpad/time_in_the_mri*.md`);
  - the concepts in `docs/SOFTWARE_OVERVIEW.md`;
  - the user-facing parts of `one-mud.md`;
  - the scope in `LLMud/VISION.md`.

  Each of those keeps a pointer here, and CLAUDE.md's project summary is rewritten to match A1.

## Terms

| Term | Meaning |
|---|---|
| **gpt-oss-20b** | the model studied: a mixture-of-experts (MoE) model with 24 layers |
| **expert** | one of the 32 sub-networks in each layer; each token is sent to 4 of them |
| **expert route** | the experts a token is sent to, layer by layer: four in each layer, whose weights add up to 1. "Top-1" is the expert with the highest weight |
| **pipeline** | a sequence of experts that many tokens follow through consecutive layers |
| **hub** | an expert that many different routes pass through |
| **expert fingerprint** | a 24 × 32 grid of how much weight each expert gets at each layer, for one population of tokens |
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
| **condition** | whatever differs between runs of the same set: a scaffold, a steering vector, an ablation, an expert mask, another model or a decoding setting (I) |
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
| **atlas** | catalogues of nodes, experts, routes and analysed scaffolds, each entry with a written report |
| **paradigm** | the accepted findings, drawn as a map: facts about atlas entries, and links between them (H) |
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
  2026-10-04];
- **it starts with about twelve lenses across levels of language** [Decided, 2026-10-08]: grammar
  (tense, number agreement), meaning (the senses of "tank", animacy, an animal taxonomy),
  pragmatics (irony), feeling (positive or negative), social (friend or foe, intent), knowledge
  (fact or fiction), safety (harmful or harmless request) and reasoning (negation). Some have
  published results on other models, which benchmarks the instrument, and the breadth gives each
  team of AI scientists a start.

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

**C5. What comes with each node and lens.**
- **The neurons behind it,** found by correlation [Decided, 2026-10-04].
- **For each split between nodes** [Decided, 2026-10-06]:
  - how much of the split comes from attention, and how much from the experts;
  - the other token positions that carry the same signal;
  - what the node pushes toward, through the output vocabulary (the logit lens);
  - a check that surface features (length, first word) don't explain it.
- **Before a key finding is accepted** [Decided, 2026-10-06]: the population is steered into the
  other node, and what changes downstream is recorded.
- **Its expert fingerprint** [Decided, 2026-10-08]: how much weight each expert gets at each layer,
  for the node's population (E5).
- **How much of each lens the router sees** [Decided, 2026-10-08]: for each mass-mean lens and
  layer, the share of its axis that lies in what the next router reads. It says whether a concept
  steers expert choice or rides along as content. The split into what the router reads and what it
  ignores is Ye, Yuan and Sharkey's (M2).
- **The published features closest to it** [Decided, 2026-10-08]: from the public sparse
  autoencoders for gpt-oss-20b (Arditi's, on Neuronpedia). It is a comparison, not circuit
  discovery (B7), and lets others read the findings in their own vocabulary.

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
- **A caution** [Decided, 2026-10-07]: presence must be calibrated on states that include natural in-between
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
| **Atlas** | browse nodes, experts, routes and analysed scaffolds, with their reports, and the paradigm's map | later |
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
  approved in the time review]. Each export carries a recipe (the lens and its version, the
  captures, the settings, the commit), so the figure can be made again exactly [Decided,
  2026-10-08].

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
  - it opens the MUD terminal with the command ready: you play the scenario yourself (`simulate`)
    or start the agent on it (`agent run`), so runs still start in the MUD [Decided, 2026-10-07];
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
- it is the app's version of replaying a run in a scenario room (F1);
- **branch from any tick** [Decided, 2026-10-08]: replay up to a tick, change one thing (the
  observation, a scaffold or a steering vector) and let the model continue. The branch is a new
  run, so it starts through Claude Code or the MUD (F3); it is a condition (I) and opens side by
  side with the original.

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
- the first step toward monitoring agents (A1);
- **alerts are judged per run** [Decided, 2026-10-08]: by how many runs they catch at an acceptable
  rate of false alarms, not by AUROC alone. In a 2026 study, probes with AUROC above 0.93 still
  missed between a fifth and a third of cases at realistic false-alarm limits (M2).

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

**What Watch needs from the rest of the software** [Decided, 2026-10-07]:
- the runner captures the kit's keywords in each action, and stores each tick's token ids;
- the scan runs over each tick's whole text, by replay or during the runner's own capture pass,
  whichever is cheaper, and stores only the readings: presence and position, per token, lens and
  layer;
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
- **Colour that reads true** [Decided, 2026-10-08]:
  - colours blend in a perceptual colour space (OKLab), so a half-and-half node looks halfway and
    mixes stay clean. Today's blend averages RGB values (`colorBlending.ts`), which turns mixes of
    opposing colours muddy and darker than either class;
  - an optional striped node shows the exact shares;
  - two designed axes can share one colour, hue for one and lightness for the other, with a square
    legend, so one Sankey shows a combination such as frame × voice. Today points can pair a second
    axis, but nodes can't.
- **Expert fingerprints** [Decided, 2026-10-08]: for any node, population or condition, a 24 × 32
  grid of how much weight each expert gets at each layer, and difference grids between two of
  them.
- **Expert Sankeys keep one layout** [Decided, 2026-10-08]: experts at each layer are ordered to
  minimize crossings, computed once from the pooled flows and kept fixed across conditions, so a
  difference between conditions is real rather than layout. Ye, Yuan and Sharkey lay out expert
  paths this way.
- **Where the instruments disagree is marked** [Decided, 2026-10-08]: items whose node differs
  between the UMAP lens and the best raw-space grouping (C4) are marked on the cluster Sankey, so
  the picture shows where it could mislead.
- **The 3-D trajectories show what the lens counts** [Decided, 2026-10-08]. Today's stepped 3-D
  view fits its own UMAP, separate from the clustering, and colours by label
  (`cluster_route_analysis.py`), so a point can sit in one bundle and be counted in another node.
  It colours by node, or draws from the lens's own fit.
- **Depth heatmaps** [Decided, 2026-10-08], per lens:
  - tokens × layers for one sentence or tick: where in the text, and at which depth, a concept
    forms (C5's question of which token made the decision). It opens from here for a sentence and
    from Watch for a tick;
  - layers × time for a run or a study: how a reading forms at each depth as evidence arrives
    (E6).
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
- **Depth over time** [Decided, 2026-10-08]: the layers × time heatmap for the study's lens (E5).
- **A temporal Sankey** [Decided, 2026-10-08]: node transitions across ticks or context steps, once
  a study has enough runs and few enough nodes.
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
- reports are marked as LLM-written. A finding still goes through the paradigm's review (Part H);
- **analysts are tested before they are trusted** [Decided, 2026-10-08], and again whenever prompts
  or models change:
  - decoys: cards and Sankeys built from shuffled labels or random groupings, where a sound analyst
    reports nothing;
  - planted findings, which a sound analyst finds;
  - predictive descriptions: given a node's description, another model must pick the node's members
    from held-out sentences, scored against a simple baseline, as RouterInterp scored its routing
    descriptions (M2);
- **reports have a budget** [Decided, 2026-10-08]. Every cluster, split point and route of one lens
  comes to hundreds of `claude -p` calls (24 layers × about 6 nodes is already 144 cluster cards).
  Reports are written first for validated lenses and selected items, the rest on demand, with a
  budget per job.

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
| Atlas | a report for each analysed scaffold, across its types of analysis (I) | Decided, 2026-10-07 |
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
- today the address comes from the root `.env` and is always localhost [Built];
- **hosting Scaffold Dynamics for others is planned before other researchers are invited**
  [Decided, 2026-10-08]: a server, accounts, abuse handling and cost. Until then the default
  address is localhost.

## Part G — Data and records

- **The data lake** [Decided, 2026-10-04: not copied wholesale; 2026-10-06: the six sessions kept]:
  - captures stay outside git;
  - the WSL lake holds the six kept sessions and every new capture;
  - the paper's lake stays on the C: drive.
- **The libraries:**
  - sentence sets and scenario sets, each set in its own folder for its study [Decided,
    2026-10-06];
  - scaffolds too, as versioned files (I) [Decided, 2026-10-07];
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

- **The atlas has four catalogues** [Decided, 2026-10-06; scaffolds added 2026-10-07], each entry
  with a report written by a Claude agent:
  - **nodes:** every node of every validated lens, layer by layer;
  - **experts:** all 24 × 32;
  - **routes:** pipelines and hubs, built from all four of each token's experts and weighted by the
    model's own weights [Decided, 2026-10-07]. Today's routes follow only the top-1 expert; the
    top-1 Sankey stays as one view of them;
  - **scaffolds:** every analysed scaffold, with its analyses (I).
- **Time adds node dynamics** [Decided, 2026-10-07]: how long runs stay in a node, what comes before
  and after it, and what the model does while in it. Runs that stay in a node for several steps show
  a state the model holds; runs that cross it in one step show a passage. This is how a question
  like the context-shift study's (D5) gets answered, node by node.
- **Bringing the lenses' findings together into one coherent model is the hard part** [Decided,
  2026-10-07].
- **The paradigm is the accepted findings** [Decided, 2026-10-04 and 2026-10-06]:
  - the AI scientists propose findings, attack them and give evidence;
  - several models vote, and when most of them agree, the finding goes to Andrew for review;
  - knowledge consolidators extract the insights.
- **The accepted findings form a map, the shape of the coherent model** [Decided, 2026-10-07]:
  - the atlas gives the entries. A finding is either a fact about one entry, written into its
    report, or a link between entries, of one of the kinds below;
  - the map lays the accepted links over the atlas by the layer where each concept forms. It is
    drawn in the Atlas workspace, and the consolidators write the story over it;
  - findings connect because each names the entries it links. Contradictions show up as clashing
    links, and each is a study waiting to happen;
  - later, the map is scored on how well it predicts what a new lens will show: a score for the
    paradigm, never a gate on analysis;
  - every fact and link carries its strength [Decided, 2026-10-08]: supported, tested and absent,
    or untestable here, so the map shows what was checked and found missing, not only what holds.
- **The atlas is published** [Decided, 2026-10-08]: exported as a static website (entries,
  reports, figures and the map), with the sentence sets, lens directions and summary readings on
  Hugging Face in formats others can load. It is the project's public face, linkable from posts
  and papers.

**The kinds of link** [Decided, 2026-10-07], each measured by its own tool. The examples are
questions, not findings.

| Link | Example | Measured by |
|---|---|---|
| overlap | Does the danger lens, read on the animal-taxonomy sentences, put predators in "dangerous"? | one saved lens reading another lens's data (C), with presence (D4) saying whether its concept is there at all |
| nesting | Does "dog" sit inside "mammal" inside "animal"? | the levels of the k profile's hierarchy (C) |
| order in depth | Does word sense settle before the scene's threat level? | per-layer held-out scores (C) |
| shared direction | Do one set's threat axis and another's danger axis point the same way? | the angle between two mass-mean axes |
| shared machinery | Do two concepts' tokens take the same pipes and hubs? | the expert and route catalogues, and expert fingerprints (E5) |
| use in decisions | Does the reading predict the action, and does steering it change the action? | behaviour by reading (E6) and steering a node (I) |
| changes | Does a scaffold make a concept form earlier in a run, or suppress a writing style? | the condition comparison, against the scaffold's neutral texts (I) |
| steers routing | Does the threat axis lie in what the router reads, so that threat changes which experts a token goes to? | the share of the lens's axis in what the next router reads (C5) [Decided, 2026-10-08] |

## Part I — Interventions and conditions

- **Steering and ablation, with behaviour studies** [Decided, 2026-10-06].
- **Steering a node and seeing what changes downstream** [Decided, 2026-10-06].
  - **The push is told apart from its effects** [Decided, 2026-10-07]. At the steered layer the
    population lands in the other node by construction. So the view shows whether it stays there
    at later layers or drifts back (later layers can undo a push, known as self-repair), and what
    else changes: other lenses, routes and behaviour.
- **Scaffolds, and steering from outside and inside the model:** how each changes trajectories
  [Decided, 2026-10-06].
- **A condition is whatever differs between runs of the same set** [Decided, 2026-10-07]: a
  scaffold, a steering vector, an ablation, an expert mask, another model or a decoding setting.
  A change made at one tick of a branched run is a condition too (E4) [Decided, 2026-10-08].
  - All are compared the same way, under one fixed lens: side by side in Watch, and as averages
    in Study.
  - Each run records its condition (G).
- **Comparisons are fair** [Decided, 2026-10-07]:
  - **paired:** a condition and its baseline share everything else (scenario, decoding, seed,
    date), so a difference comes from the condition. Where the two runs part ways is itself a
    result;
  - **a same-size control without the content:** random directions for steering and ablation,
    random experts for expert masks, and two or three neutral texts of the same length and format
    for scaffolds. Added text alone shifts readings, so the neutral texts separate a scaffold's
    content from its presence;
  - **dose:** strength and layer are swept, so a result shows how the effect grows.
- **How interventions are done** [Decided, 2026-10-07]:
  - routing drift is always recorded: a push can switch experts at later layers, because the
    routers read the residual stream;
  - an option to steer only in directions the routers don't use;
  - expert masks through the router's bias. On the 4-bit loading path the router's own code never
    runs, so it can't be hooked, but that path reads the bias on every call.
- **Replications are named as such** [Decided, 2026-10-08]. Steering where the routers can't see is
  RARE's method, built on Ye, Yuan and Sharkey's split, and switching experts is SteerMoE's (M2).
  Both are cited, and each is first reproduced on a published result. For agents, one published
  gpt-oss result is replicated as a MUD scenario: game probes that stay accurate when the agents
  know they are watched.
- **A catalogue of analysed scaffolds** [Decided, 2026-10-07]: each scaffold with its reports and
  different types of analysis.
  - **Its shape** [Decided, 2026-10-07]:
    - the analyses: what the scaffold changes in each lens's readings, and when in a run; in
      routes; and in behaviour, including the style of what the agent writes. Each is measured
      against the scaffold's neutral controls;
    - it is the atlas's fourth catalogue, so the map (H) can link a scaffold to what it changes,
      with a seventh kind of link, "changes", measured by the condition comparison;
    - scaffolds are kept as versioned files in the repo, like the sentence and scenario sets.
- **Another MoE model** for comparison [Decided, 2026-10-06].

## Part J — User stories

Stories 1–6 come from the time design; 7–11 were added in its review, which Andrew asked to see
[2026-10-07]; 12–15 come from his 2026-10-07 requests; 16–19 cover decisions in Parts C, E, H and
I. The steps in each are [Decided, 2026-10-07].

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
10. **From a moment to the layers.** Click a cell in the heatmap; the lens panels show that word's
    path through each lens's nodes and experts.
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
16. **Join two lenses.** Read the danger lens on the animal-taxonomy set and see which animals land
    where. An AI scientist proposes an overlap link, others attack it and vote, and once you
    accept it, it appears on the map.
17. **Analyse a scaffold.** From Claude Code, run one scenario set four ways, paired: no scaffold,
    the scaffold, and two neutral texts of the same length. Study shows what the scaffold changed
    beyond the neutral texts. A Claude agent writes its report, and the scaffold joins the atlas.
18. **Check a finding by steering.** Before a key finding is accepted, steer its population into
    the other node, with random directions as controls and a sweep of strengths. The downstream
    view shows whether the population stays there, what else changes, and which experts switched.
19. **Build and test a scenario.** In Build › scenarios, a Claude agent drafts scenarios to your
    instructions. Edit the stages, actions and labels, validate them, play the scenario in the
    simulator, have the agent play it there, and save the set with a version.

## Part K — Order of work [Decided, 2026-10-07]

1. **Done:** Andrew's walk through the MUD, and the one-MUD branch merged into main (2026-10-07).
2. **This document:** reviewed with Andrew section by section, then approved. Nothing new is built
   until then.
3. **Before the first slice:** the basin-era temporal tools retire (G).
4. **Then the build, in slices.** Each ends with a showcase: one striking figure and a short
   findings note [Decided, 2026-10-08].
   1. **The lens core** [Decided, 2026-10-06: before the world-building pilot]:
      - validated, saved lenses, with the self-check on planted structure (C4);
      - k per layer, manual and automatic, with the k profile and the k advisor (C3, E8);
      - the comparison of UMAP with raw-space groupings (C2, C4);
      - the clustering form, basic and Advanced (E3) [Decided, 2026-10-07], and clustering from
        the polysemy lab in the MUD, through the one command interface (E5, E7);
      - each lens's report, the analysis panel with its cards for clusters, experts, routes and
        expert routes, and the number checker behind every report (C7, E8);
      - the neurons behind each node, the logit lens and the surface check (C5);
      - atlas nodes, first version;
      - the all-layer Layers view, colour by any designed axis, study files, and the model's own
        expert weights with all four ranks (E5);
      - the raw-axis endpoint retires once saved mass-mean lenses replace it (G);
      - the additions of 2026-10-08: colour that reads true, expert fingerprints, one layout for
        expert Sankeys, marked disagreements, the 3-D fix, figure recipes, the analyst tests, a
        budget for reports, and how much of each lens the router sees (C5, E2, E5, E8).
   2. **Capture and jobs:**
      - the capture recipe and per-run token ids (G);
      - the GPU job queue;
      - more token positions, and states after generation starts for sentence sets too (C5, G);
      - entering your own MUD's address (F6).

      It comes before the builder because the builder captures each new set as a background job,
      and every capture records how it was made (B12).
   3. **The sentence set builder,** with its audits and critic (C1, E3), then the starter lens
      catalogue (A4).
   4. **Time on sentence runs,** checked against the paper's tank results (D7), in Study: readings
      with presence and position, references and bands (D4, D5). Depth heatmaps and the temporal
      Sankey come with it (E5, E6).
   5. **The atlas, second version:** the expert and route catalogues across every capture, node
      dynamics from sentence runs, cross-lens reports, and overlaps by cross-reading (H, E8). By
      then the builder has produced several lenses to connect. The atlas is published, with its
      data, and each node lists its nearest published features (C5, H).
   6. **The world-building pilot** [Decided, 2026-10-06: after the lens core; 2026-10-07: after
      slice 5].
   7. **The scenario builder and the MUD workspace,** then friend/foe v3 [Decided, 2026-10-06: v3
      after the lens core].
   8. **Agents:**
      - lens kits and keywords;
      - the scan, with each lens's neutral baseline;
      - replay, in the app and in a scenario room in the MUD (F1);
      - scripted runs and would-be actions;
      - Watch, with its lens panels, explained readings, bookmarks, runs side by side and live
        alerts;
      - node dynamics from agent runs;
      - tokens × layers heatmaps for ticks, and alerts judged per run (E4, E5);
      - one published game-probe result replicated as a MUD scenario (I);
      - the experiments of D6.
   9. **Conditions and interventions:** scaffold studies and the scaffold catalogue; steering,
      ablation and expert masks; the steering check before a key finding is accepted;
      branching a run from any tick; RARE's and SteerMoE's methods reproduced and cited (C5, E4,
      I).
   10. **Layer transitions and trajectory upgrades:** how much of each split comes from attention
       and how much from the experts (C5); wave lines and patterned nodes (E5).
   11. **A second MoE model.**
   12. **The paradigm and the AI scientists:**
       - the map: links, votes and the consolidators, with a strength on every finding and the
         eighth kind of link (H);
       - evidence packets for the AI scientists;
       - the Ideas workspace;
       - the scientists' and researchers' rooms (F2);
       - monitoring.
5. **Later:** the Mudlet package (A2), the lab guide in the MUD (E8), a mini-world builder (E3), and
   hosting Scaffold Dynamics before other researchers are invited (F6).

## Part L — Questions for Andrew

- **L1. Who writes sentence sets in the builders?** Answered 2026-10-07: one `claude -p` run writes
  each whole set, all classes together, and the audits check batches (C1).
- **L2. Which reading leads for agents?** Answered 2026-10-07: the output reading at keywords
  leads, the scan shows the reasoning, and carriers are the controlled comparison (D3).
- **L3. Winter Survival's game design document.** Answered 2026-10-07: it stays separate, under
  this one. This document links to it and wins where the two disagree.
- **L4. The time design.** Answered 2026-10-07: the orderings, the project's own rules, presence
  and position, and references for studies (D1–D5).
- **L5. The retirements in Part G.** Answered 2026-10-07: yes; three when building starts, the
  raw-axis endpoint when saved lenses replace it (G).
- **L6. Watch (E4).** Answered 2026-10-07: the layout as drafted, with lens panels as many as
  wanted, the token rule, replay, explained readings, bookmarks, side by side and live alerts.
- **L7. The workspaces (E1).** Answered 2026-10-07: as drafted.
- **L8. Relevant-neuron PCA (C2).** Answered 2026-10-07: yes, as a third kind of grouping, with the
  cautions given.
- **L9. The order of work (Part K).** Answered 2026-10-07: capture and jobs comes before the
  sentence set builder, a second version of the atlas follows time on sentence runs, and slices
  1–5 come before the world-building pilot.
- **L10. Where agent runs start.** Answered 2026-10-07: in the MUD or through Claude Code, never from
  the app (F3).
- **L11. One command interface (E7).** Answered 2026-10-07: yes.
- **L12. LLM analysis (E8).** Answered 2026-10-07: every place in the table.
- **L13. Live runs in the app?** Answered 2026-10-07: Watch follows a run in progress one saved tick
  at a time; the scan never slows the agent; the agent's play is watched in the MUD (E4).
- **L14. The scaffold catalogue's shape (I).** Answered 2026-10-07: yes; analyses against the
  neutral texts, the atlas's fourth catalogue with a seventh kind of link ("changes"), and
  scaffolds as versioned files.
- **L15. Part M's recommendations.** Answered 2026-10-08: all adopted and written into their parts;
  the project keeps the name OpenLLMRI.

## Part M — Claude's final read: certainty and recommendations [Decided, 2026-10-08: Andrew accepted it]

Written for Andrew's final read (2026-10-07). M1 grades how sure Claude is that the design does what
it is for. M2 places it among other work on gpt-oss and MoE models, from a survey of 2025–2026 work
whose main claims were re-read at their sources. M3 lists the recommendations: Andrew adopted them
(2026-10-08), and each is now written into its part.

**M1. How sure the design is.** Certainty follows how a claim was checked: read at the source or
run, reasoned from checked facts, or taken from the survey.

| Question | Evidence | Certainty | What would raise it |
|---|---|---|---|
| Does it serve the goal (A1)? | Every part of A1 has a home: which representations exist (C, H); where they form (per-layer held-out scores, C4; other token positions, C5); how each layer transforms them (slice 10); how tokens move through them (B2, D, E5, E6); how experts route them (E5, H); behaviour and failure points (D3–D5, E6, I); monitoring (E4, slice 12) | 90% | How each layer transforms them is the thinnest part, and it comes late (slice 10) |
| Can its readings be trusted? | Held-out scene families, chance-corrected scores, the fair comparison against a supervised ceiling, the self-check on planted structure, the surface check, the steering check, statistics per scene family. In practice, lenses built from large probes have assigned held-out sentences to the right clusters strongly (Andrew, 2026-10-08) | 90% | Held-out families show that a lens generalizes across the kinds of text it was built from. Two things cover the rest: lenses are built from text like the text they will read, with families of it held out (C6, D2 rule 3); and presence flags a state unlike any the lens was built from, which UMAP's transform would still place in some node (D4) |
| Does reading agents work? | The output reading at keywords is a fixed site at the decision. The scan's neutral baseline, the presence measure and the chance level are open experiments (D6); carriers by replay are the controlled fallback. The rule that a lens lights up on its strongest token matches the max-over-tokens scoring that worked best in a 2026 study of reasoning traces (M2) | 70% | The least certain part, and an experiment by design. D6's first experiment, on scripted runs with known labels, settles it; slice 8 runs it first |
| Does it run on one 16 GB GPU? | The model uses 14.3 GB; a capture step takes about 6.7 s per tick; a study of 200 runs × 7 ticks takes 25–70 minutes; storing every position (about 280 KB per token) is opt-in; lens fits run on the CPU | 85% | About 1.7 GB of GPU memory is left, which limits how many lenses a scan can hold on the GPU at once. Measured when the scan is built |
| Are the LLM analysts reliable enough? | Cited numbers are re-computed, several models vote, the surface and steering checks apply, Andrew reviews | 75% | No false-discovery rate has been measured yet; the analyst tests measure it (E8) |
| Does the order give value early? | Slice 1 alone gives validated lenses, the all-layer Layers view, cards with reports and atlas v1; each slice is usable on its own | 85% | Slices are large, so each ends with a showcase (K) |
| Are its visualizations distinctive? | Cluster Sankeys across all 24 layers beside expert Sankeys, colour blending of label mixtures, the lens heatmap over the reasoning, lens panels, the paradigm's map, and the additions of 2026-10-08: expert fingerprints, depth heatmaps, a temporal Sankey, two-axis colour. The survey found no match for blended label colours or for many lenses at once over every token | 85% | Built and seen on real data |
| Is it competitive? | M2 | 75% | Results out early, in forms others can use: a showcase per slice (K), the published atlas and data (H), the nearest published features for each node (C5) |
| Does the record stay honest? | Marks traced to Andrew's words, how everything was made (B12), study files in git, number checks | 90% | — |

**Verdict:** proceed. The readings, the core of the goal, stand at 90%: held-out validation does the
work, as long as lenses are built from the kinds of text they will read, and presence flags states
unlike any a lens was built from. The least certain parts are agent reading (70%, an experiment by
design) and the LLM analysts (75%, until the tests in E8 have run).

**M2. Among other work on gpt-oss and MoE models.**
- **What others have for gpt-oss-20b:**
  - feature dictionaries: sparse autoencoders for the residual stream at every layer (Arditi,
    September 2025), browsable on Neuronpedia with search and steering;
  - routing: features from those dictionaries predict which experts a token goes to with 81% recall,
    against 55% for a baseline that uses only the token and the one before it (RouterInterp, January
    2026);
  - routing as control: the residual stream splits into a part the router reads and a part it
    ignores. Expert paths group tokens by their function, while language, token identity and
    position travel in the part the router ignores (Ye, Yuan and Sharkey, April 2026, six MoE models
    including gpt-oss-20b);
  - steering in MoE models: switching experts on and off (SteerMoE, both gpt-oss sizes), and
    steering in directions the router can't see (RARE, 2026);
  - agents: probes on gpt-oss-20b in blackjack and prisoner's-dilemma games stay accurate even when
    the agents know they are watched (September 2026). Over a reasoning trace, taking each probe's
    maximum over tokens reaches up to 95% AUROC, while the average or the last token falls to near
    chance (May 2026).
- **Earlier work on the same pictures:** cluster flows across layers drawn as Sankeys exist in
  LayerFlow (2025, on BERT) and in Andrew's own Concept Trajectory Analysis (2025, on GPT-2, with
  LLM-written cluster descriptions). Apollo's deception probes colour each token of a transcript by
  its probe score. MafiaScope (2026) tracks agents' beliefs turn by turn against a game's ground
  truth, but by asking them questions, not by reading activations.
- **What the survey found nowhere else:**
  - cluster flows and expert routes for the same tokens, across all the layers of an MoE model; no
    cluster-flow Sankey of gpt-oss at all;
  - UMAP lenses validated on held-out scene families and compared fairly with raw space;
  - many lenses read at once over every token of an agent's reasoning;
  - an agent read tick by tick against staged ground truth, with its routing, in a text world;
  - colour blending of label mixtures;
  - a typed map of concept links built by agents who attack and vote, with every cited number
    re-computed.
- **Where the design overlapped or was behind,** each now answered:
  - steering in directions the router can't see is RARE's method, and the split it relies on is Ye
    et al.'s: named as replications and cited (I);
  - steering by switching experts is SteerMoE's: the same (I);
  - the public gpt-oss sparse autoencoders weren't used: each node now lists its nearest published
    features (C5);
  - LLM-written descriptions of routing have a published bar on gpt-oss-20b, the 81% recall above:
    the analysts' descriptions are tested the same way (E8);
  - the name: a 2024 Python module is called LLM-MRI. This project is OpenLLMRI, a different name,
    and keeps it (Andrew, 2026-10-08).
- **Verdict:** distinctive as a combination. Each piece has neighbours, but nothing found combines
  concept flows beside routing on an MoE model, validated lenses, agents read against ground truth
  and an agent-built map. The field moves fast (many 2026 papers on gpt-oss), so getting results
  out early matters as much as the design.

Sources:
[Arditi's SAEs](https://huggingface.co/andyrdt/saes-gpt-oss-20b) ·
[Neuronpedia](https://www.neuronpedia.org/gpt-oss-20b) ·
[RouterInterp](https://library.sparai.org/reports/interpreting-mixture-of-experts-routing-through-sparse-autoencoders-z8khhk/) ·
[Ye, Yuan and Sharkey](https://arxiv.org/abs/2604.17837) ·
[SteerMoE](https://arxiv.org/abs/2509.09660) ·
[RARE](https://arxiv.org/abs/2608.21236) ·
[probes in multi-agent games](https://arxiv.org/abs/2609.03035) ·
[probe trajectories](https://arxiv.org/abs/2605.18549) ·
[alarm policies](https://arxiv.org/abs/2610.04575) ·
[LayerFlow](https://arxiv.org/abs/2504.10504) ·
[Concept Trajectory Analysis](https://sotaverified.org/papers/how-neural-networks-organize-concepts) ·
[Apollo's deception probes](https://www.apolloresearch.ai/research/deception-probes) ·
[MafiaScope](https://arxiv.org/abs/2607.10645) ·
[LLM-MRI](https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/30782)

**M3. Recommendations** [Decided, 2026-10-08: all adopted; the name stays]. ★ marks Claude's top
five. Each is written into the part named.

| # | Recommendation | Now in | Slice |
|---|---|---|---|
| 1 | Colours blended in a perceptual colour space, with optional striped nodes | E5 | 1 |
| 2 | Two designed axes in one colour | E5 | 1 |
| 3 | The 3-D trajectories show what the lens counts | E5 | 1 |
| 4 ★ | Expert fingerprints | C5, E5, H | 1, 5 |
| 5 ★ | Depth heatmaps: tokens × layers, and layers × time | E5, E6 | 4, 8 |
| 6 | A temporal Sankey | E6 | 4, 8 |
| 7 | Where the instruments disagree, marked on the Sankey | E5 | 1 |
| 8 | One fixed layout for expert Sankeys | E5 | 1 |
| 9 | Figure recipes | E2 | 1 |
| 10 ★ | A published atlas, with its data | H | 5 |
| 11 | A showcase per slice | K | every slice |
| 12 | A starter lens catalogue across levels of language | A4 | 3 |
| 13 ★ | Analysts tested before they are trusted | E8 | 1 |
| 14 ★ | How much of each lens the router sees, and an eighth kind of link | C5, H | 1, 12 |
| 15 | The published features closest to each node | C5 | 5 |
| 16 | Published results replicated inside the platform | I | 8, 9 |
| 17 | Live alerts judged per run | E4 | 8 |
| 18 | Branching a run from any tick | E4, I | 9 |
| 19 | A strength on every finding, absences included | H | 12 |
| 20 | A budget for LLM reports | E8 | 1 |
| 21 | Hosting Scaffold Dynamics before other researchers are invited | F6 | later |
| 22 | The name | — | not adopted: the project stays OpenLLMRI |

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
  - Watch follows a run in progress one saved tick at a time, and the scan never slows the agent;
  - Part H: node dynamics in the atlas; the accepted findings form a map, with facts about single
    entries and links of six kinds between them, scored later on how well it predicts new lenses;
  - Part I: one idea of a condition; fair comparisons (paired runs, a same-size control without
    the content, with two or three neutral texts for scaffolds, and dose); steering a node tells
    the push from its effects; routing drift, steering the routers ignore, and bias masks; a
    catalogue of analysed scaffolds, with reports and different types of analysis: the atlas's
    fourth catalogue, with a seventh kind of link, "changes", and scaffolds as versioned files;
  - Part J: the stories' steps, and four new stories (joining two lenses, analysing a scaffold,
    checking a finding by steering, building and testing a scenario); the scenario builder opens
    the MUD terminal with the command ready, so runs still start in the MUD;
  - Part K: every decided feature placed in a slice; capture and jobs before the sentence set
    builder; a second version of the atlas; slices 1–5 before the world-building pilot; the
    one-MUD branch merged into main;
  - Part L and the last proposals: Winter Survival's game design document stays separate, under
    this one; what this document covers and what it replaces, with CLAUDE.md's project summary
    rewritten to match A1; presence calibrated on states that include natural in-between ones;
    what Watch needs, with the scan run by replay or during the runner's capture pass.
- **2026-10-08 decisions:**
  - every recommendation in Part M adopted and written into its part: colour that reads true,
    expert fingerprints, depth heatmaps, a temporal Sankey, marked disagreements, one layout for
    expert Sankeys, the 3-D fix, figure recipes, a published atlas and data, a showcase per slice,
    the starter lens catalogue, the analyst tests, how much of each lens the router sees (an eighth
    kind of link), the nearest published features, replications named and reproduced, alerts
    judged per run, branching a run from any tick, a strength on every finding, a budget for
    reports, and hosting before other researchers are invited;
  - the project keeps the name OpenLLMRI;
  - held-out sentences are how a lens's reading of new data is judged, and lenses built from large,
    varied probes have assigned held-out sentences strongly (M1).
- **Andrew's ideas, not yet decided:**
  - **2026-10-04:** a user interface in the MUD;
  - **2026-10-06:** asking the agent to use set words in its reasoning; giving it words marked as for
    measurement only;
  - **2026-10-07:**
    - an interface so users can choose the LLM for Claude agents' work.
