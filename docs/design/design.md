# OpenLLMRI: design and requirements

Related: docs/design/requirements.yaml (the numbered requirements), docs/architecture/plan.md (the
plan and architecture), docs/pages/build.py (the pages), docs/pages/check.py (the page checks)

**Status:** drafted on 2026-10-11 from the requirements list, for Andrew's review section by
section. Once he has reviewed it, it replaces `docs/DESIGN.md` as the design's source of truth;
until then DESIGN.md remains the source of truth for the decisions made up to 2026-10-11
[DOC-3, DOC-11]. Decisions made since are recorded here and in the plan-and-architecture document,
and DESIGN.md's header names the placements of its own that they replace (Claude's arrangement
while the review waits) [ORDER-20].

## How to use this page {#how-to-use}

This document says what OpenLLMRI is for, who uses it and how. How it is built, the order of work
and each phase's plan are in the other of the two documents, [the plan-and-architecture
document](plan.md#where-we-are) [DOC-2, DOC-4, DOC-13].

- **Words.** Technical and project words are explained under [Terms](design.md#terms), near the
  end.

- **Requirements first.** Every decision is a numbered requirement in
  `docs/design/requirements.yaml`, with its date, what settled it and its status. The sections
  below cite requirements by id, in brackets: on the page each id is a chip coloured by its status,
  and pointing at it shows the requirement in full [DOC-6].
- **Statuses** [DOC-1]: **decided** by Andrew (with the date); Andrew's **idea**, not yet decided;
  Andrew's **view**, kept as context; **proposed** by Claude, waiting for his yes; **open**, for an
  experiment or a question to settle; **built**, existing with no separate decision; **retired**,
  replaced by another requirement. Beside each requirement the page also shows whether it exists
  in the software yet: yes, partly or no.
- **Writing on the page.** Under every section is a box to write in. Text saves as it is typed,
  and every box is collected in the last section, "Everything you've written", with a button that
  copies it all. Claude reads the boxes before each change [DOC-4].
- **Questions are cards,** numbered in the order they were asked (L1, L2 and so on; in charts, L0
  to L23 are layers instead). Each open question has its choices, the one Claude recommends, an
  "Other" and a note. Answers save as they are chosen [DOC-12].
- **Andrew's words stay private.** The repo is public, so this document paraphrases every decision;
  Andrew's own words appear only on the published page, read from its private store [DOC-8].
- **Which document wins.** Where this document and another disagree, this one wins and the other is
  corrected [DOC-15]. Winter Survival's game design document stays separate, under this one
  [DOC-14].
- **Checks.** Before each version reaches Andrew, it gets an independent audit of every mark
  against his own words, a readability review, and the page checks (every cited id exists and is
  current, no retired wording, links resolve) [DOC-7, DOC-10].

## What OpenLLMRI is for {#purpose}

**The goal** is an evidence-based paradigm of how gpt-oss-20b understands the world and makes
decisions from that understanding [GOAL-1]. It covers:
- which internal representations exist;
- where they form: which layers, which tokens;
- how each layer transforms the representations;
- how tokens move through the representations, across layers and over time;
- how experts route the representations, through pipelines and hubs;
- how the representations lead to behaviour, including the points where reasoning fails, such as
  the context shift the paper studied.

**How it gets there.** The AI scientists work toward the paradigm with lenses on sentence sets and
scenarios, scaffolding experiments, steering from outside and inside the model, and ablation. How
a scaffold changes the way trajectories form (for example, suppressing a writing style) is
evidence about how the model works [GOAL-2]. The paradigm makes it possible to monitor agents
visually, seeing which understandings are active as they reason and act. That monitoring also
helps in building scaffolds that work [GOAL-3].

**Visual knowledge discovery comes first:** cluster trajectory Sankeys, the words that travel
through each node, colour blending, and more visual channels [GOAL-4]. Another mixture-of-experts
model may be compared later [GOAL-5].

**Who uses it:**
- **Andrew,** through the app, Claude Code and the MUD [GOAL-6];
- **Claude agents** (`claude -p`), as analysts and AI scientists [GOAL-7]:
  - they use the same tools as Andrew, and their actions appear in the MUD as events;
  - they work in teams by topic: grammar, emotional salience, kinds of reasoning, safeguards and
    alignment;
  - they design sentence sets and scenarios from their own hypotheses, and run studies on them;
- **researchers who install the software:** they run their own app and backend and connect to
  Scaffold Dynamics by default, or to their own MUD by entering its address [GOAL-8];
- **visitors** to the MUD. A Mudlet package with simple views comes later [GOAL-9].

**Its pieces** [GOAL-10]:
- **the app:** React, with a FastAPI backend that runs the model on the GPU. The backend also runs
  Claude agents with `claude -p`, as often as it needs [GOAL-11]. An interface could let a user
  choose another LLM for that work [GOAL-12];
- **the MUD,** named Scaffold Dynamics, running Evennia in Docker; it hosts the institute (its hub,
  labs and simulator) and the scenarios;
- **the data lake:** captures, kept outside git;
- **libraries and records,** as files in one repo: sentence sets, scenario sets, lab presets,
  studies, lenses, findings, the paradigm.

**The first research it carries is the lens catalogue:** validated lenses for many candidate
contrasts [GOAL-13]. Finding internal representations is the aim of one kind of study, and many
studies stay exploratory until every representation we can think of has been worked through
[GOAL-14]. The catalogue starts with about twelve lenses across levels of language: grammar
(tense, number agreement), meaning (the senses of "tank", animacy, an animal taxonomy), pragmatics
(irony), feeling (positive or negative), social (friend or foe, intent), knowledge (fact or
fiction), safety (harmful or harmless request) and reasoning (negation). Some have published
results on other models, and those results benchmark the instrument; the breadth gives each team
of AI scientists a start [GOAL-15].

## Decisions needed {#decisions-needed}

The open questions, as cards. The answered ones are in the decision log at the end.

### L35. Attention in the analysis, reworked [Open]

*Rewritten on 2026-10-20, after Andrew's notes on the first version.* He doubted the first proposal
was useful and asked whether it was a reflex. He asked what attention would add to modelling how
the model thinks, and whether its share of a split is worth knowing; how it serves the lenses, the
internal representations they find and the expert routes; and how it helps the two aims,
understanding the model and scaffolding AI systems. He noted ablation and similar interventions
as known uses of attention. If attention adds little, he asked Claude to say so rather
than invent uses. He thought an attention Sankey over the population might be best.
Claude's answer is the section [Attention in the analysis](design.md#attention), after a second
round of tests. In short:
- **attention can add one thing:** what a token takes from the rest of its input, and at which
  layers. The lenses and the expert routes both read the token itself. A scaffold (a system
  prompt, an instruction, earlier turns) reaches the model only through attention, so for
  scaffolding this is the central question. In sets like the tank sentences, where the meaning sits
  in a clue word next to the read word, it adds little;
- **its share of a split,** on its own, says which step wrote a difference, not what caused it, and
  it changes with the direction it is measured along. It stays off the node card for now (L33);
- **the population Sankey, tested two ways.** Grouping items by where attention reads from follows
  the read word's place in its sentence, not its meaning. A lens on what attention writes worked in
  one capture of four. In the framing set, whose read word sits in a question after the sentence,
  it beats the state lens clearly at layers 6, 14, 16, 18 and 19: by 0.08 to 0.55 with two nodes
  (at layer 18, 0.87 against 0.32), and by 0.09 to 0.35 when each lens has its best number of
  nodes. It also carries the sentence's scale and threat scope at layer 3, where the state lens
  shows them only weakly (0.20 and 0.24 with two nodes). In the calibration scenes, also read from
  a question after the text, it is ahead by more than 0.01 at one layer only (layer 19, 0.44
  against 0.39, with each lens's best number of nodes). In friend/foe and tank it shows less than
  the state lens;
- **so the gain is modest and specific:** mainly for scaffold studies, and for reading expert nodes
  that their context fills. It is not a new view of everything.

Four parts, each on its own card.

#### L35.1. A lens on what attention writes, as the attention row [Open]

Claude's form of the third population view Andrew asked for, beside the latent-node Sankey and the
expert-route Sankey: a lens built on attention's write at the read token (what attention adds to
the token at each layer) instead of on the token's state. Its Sankey becomes the attention row
under the other two, lined up with them and lit by the same selection
[LENS-57, LENS-55, APP-37, APP-35]. It needs no new captures, and every lens tool works on it
unchanged: tuning, validation, lit paths, node details and reports. It can pay where a token
reads its context, such as a question after a text or a decision under a scaffold. In the tests
it paid in one of the two captures of that kind, and in neither of the other two.

When: with the observatory, the new app's room for reading a lens across its layers (today's Layers
screen; step 6 of the new app's plan). Or later, with the scaffold studies, which are part of slice
8 (conditions and interventions), after the Winter Survival pilot, near the end of the roadmap.

- ( ) Build it with the observatory (recommended)
- ( ) Build it later, with the scaffold studies (slice 8)
- ( ) Don't build it
- ( ) Other

#### L35.2. Brought by attention, on the expert node cards [Open]

For each expert node: the share of its tokens whose expert would change if that layer's attention
to their own context were taken away, beside the share for the whole layer [LENS-56]. What it is
for (Andrew asked the same question of this part):
- **reading an expert node:** it tells whether the node is about the word or about its
  surroundings. Routing is mostly decided by the token itself: its own attention changes the first
  expert for a median of 2% to 10% of items, by capture (at most 43%, at one layer). But some
  nodes are filled by context. In the tank sentences, 48
  of the 54 tokens in expert 5 at layer 2 got there through their own context, 33 of them from
  vehicle sentences; without the share, that node's card would read as being about " tank";
- **scaffold studies:** a scaffold can change which experts a deciding token uses only through such
  nodes, so the share shows a study where to look;
- **how it differs from the split shares kept off the node card (L33):** it counts tokens whose
  expert actually changes, so there is no direction to choose and no random splits to compare
  with. The recomputed routing matches the capture for at least 98.8% of items.

It covers expert nodes, not the edges between them; the same count could be given for an edge's
tokens if the nodes prove useful. It needs no new data.

- ( ) Yes, with the observatory (recommended)
- ( ) Later, with the scaffold studies (slice 8)
- ( ) No
- ( ) Other

#### L35.3. Blocking attention, with the interventions [Open]

Stopping a token from reading a chosen part of its input (a scaffold, a sentence) at chosen layers,
then reading the lenses again: Claude's form of the ablation Andrew named as a known use. The lens
and the share above only show what attention brought in; blocking it tests whether that changes
what the model does, and at which layers [INT-10]. It
belongs with slice 8, conditions and interventions, which brings the ways of changing the model's
activity during a run.

- ( ) Yes, in slice 8 (recommended)
- ( ) No
- ( ) Other

#### L35.4. What goes [Open]

Claude withdrew the first proposal's parts on 2026-10-20 (listed under
[Rejected and retired](design.md#retired)). It proposes not building them, nor the uses that
proposal already advised against; the reasons are under
[Where not to go](design.md#attention-not). This card asks whether any should come back:
- the row of words (how much the token drew on each earlier word), and the heads' weights as a
  view;
- the words for the split card's analyst, the words that recur, and the words that pushed a token
  toward an expert;
- recording those word-by-word parts during capture, and running the word-by-word pass on the CPU
  over more sentence sets;
- single heads; attention traced back across layers; claims about causes read from any of these
  views.

Attention's share of a split is not on this list: it stays off the node card for now, as decided
(L33).

- ( ) Drop them all (recommended)
- ( ) Keep some (say which in the note)
- ( ) Other

### L25. Anything else [Open]

Always the last question: anything you want Claude to know, change or look at [DOC-18].

## What's built today {#built}

A short tour of what exists on 2026-10-20. Each part's section says what of it is built.
- **The MUD:** Scaffold Dynamics, running Evennia 6 in Docker, with the hub, the polysemy lab and
  the simulator. The simulator loads staged scenario sets (friend/foe v2, 250 scenarios) and
  Winter Survival; the agent plays through a control channel; visitors log in as guests and watch
  the agent play [MUD-11, MUD-14, MUD-17].
- **Captures:** sentence sets and agent runs, captured into the lake with the residual stream and
  all 32 routing weights at every layer [DATA-11].
- **Lenses:** UMAP lenses with k per layer, built and validated in the background; tuned lenses;
  lenses read on other captures; mass-mean lenses; node details, routes, the axes analysis; and an
  LLM-written report for each, every number checked [LENS-2, LENS-3, LENS-17, LENS-43]. Since
  2026-10-16 they are scored with the four method changes: folds that keep each class's share,
  decoys within each label value, a stricter line, and the tuning tested on several draws
  [LENS-21, LENS-22, LENS-24; LENS-23 in part].
- **The app:** two views, Layers (a lens across all 24 layers, with the cluster and expert Sankeys,
  3-D, lit paths, fingerprints, pipes and hubs, and the analysis panel) and Build (the lens form,
  preview, compare, validation, tuning, the axes analysis, mass-mean lenses), with the MUD terminal
  folding along the bottom [APP-18, BUILD-8].
- **Studies,** as files in the repo (`docs/studies/`), each with a showcase where its slice ended
  in one: the lens core, single words, and animals with the harm axis [DATA-5, ORDER-2]; and the
  animal ontology, run beside the two documents, with its findings note [SET-17].

## Principles {#principles}

1. **Visual knowledge discovery first:** every analysis has a view [PRIN-1].
2. **Two instruments, each measuring something different** [PRIN-2]:
   - **UMAP lenses measure conceptual membership.** They are fitted per layer, because the
     directions that separate concepts change with depth. What counts is which node a state falls
     in; the UMAP axes are never interpreted. Two designed axes can give four nodes, which shows
     how the model combines the two axes, and a trajectory is a path through each layer's nodes.
   - **Mass-mean lenses measure position on one designed contrast,** where distance along the axis
     means something.
   - Distances in full raw space are affected by noise, so the instruments read membership and
     contrast positions instead [PRIN-3].
3. **Evidence over habit:** choices between the instruments are made by comparison, not by the
   common habit of moving to raw space because UMAP distorts distances [PRIN-4]. UMAP is preferred
   once it holds up as a classifier against raw-space groupings [PRIN-5].
4. **A lens is a model,** tuned like any model until it separates the classes and classifies
   held-out data well [PRIN-6]. It is built from deliberately varied data, so any input carrying
   the concept lands in one of its nodes or at its place on the axis [PRIN-7]. New data is read by
   applying the lens [PRIN-8], and nodes are never matched across separately fitted clusterings
   [PRIN-9].
5. **Always mixture-of-experts models,** with experts over attention heads [PRIN-10].
6. **LLM agents analyse, rather than algorithms discovering circuits.** Where a decision is made is
   read from where a population of tokens splits between nodes, and from the expert routes.
   Activation patching and attribution graphs aren't planned; circuits may come later. Claude is
   the default analyst [PRIN-11].
7. **Claude-centred:** Claude Code for Andrew's research and `claude -p` for Claude agents, with
   the same tools for both [PRIN-12].
8. **Screens show what matters** (see [Rules for every screen](design.md#screens)) [PRIN-13].
9. **The simplest design that meets every requirement,** with as few moving parts as possible
   [PRIN-14].
10. **Design first, then build:** the design is reviewed before anything new is built [PRIN-15].
11. **Everything records how it was made:** model, format, decoding, seed, date, carrier, scaffold
    and intervention [PRIN-16].

## Sentence sets {#sets}

**What a set is.** Sentences that vary designed axes and hold the rest fixed, captured at a target
word or a carrier [SET-1]. Text that joins a measured dataset is never written by subagents
(helper agents Claude Code starts on its own): Claude writes it in the main conversation [SET-28].
In the app's builder, a whole set is written by one `claude -p` run or by a team of Claude agents
each working across all the classes (see [the builder](design.md#builder)). Every set gets audits:
balance by class and scene family,
length and register, a shuffle test and scene diversity, promoted from the paper's scripts to
tools [SET-30].

**Single words.** A set can hold single words rather than sentences; a team studying grammar might
use one [SET-2].
- **The word is the user's message, with a space before it,** so it is one token for nearly every
  common word: the same token the word has inside a sentence [SET-3].
- **A word that splits into several tokens is read at its last token,** which has taken in the
  whole word. Whether it split is recorded and balanced across classes, and the analysis checks
  whether early layers group split words by their last piece (goldfish, catfish and starfish all
  end in "fish") [SET-4]. The capture tries a word's one-token forms first, so a word that doesn't
  split is captured exactly as before [SET-5].
- **The read site stays the last token.** Read there, one-token and split names sit apart at every
  layer; the token after the word was tested and carries the meaning much more weakly
  (`docs/research/read_site.md`). So the gap is handled in the sets and the analyses [SET-6]: split
  names are balanced across classes in each set [SET-4], and Claude proposes that analyses compare
  within each token count [SET-7].

**The single-word sets so far:**
- **Meaning and feeling** (`nouns_meaning_feeling_v1`, 861 nouns): a semantic category with
  subcategories, animacy and concreteness, and valence. Grammar and surface form aren't varied, so
  it holds singular nouns; its subcategories are its held-out families [SET-8].
- **Animals and objects** [SET-9]:
  - **animals** (`animals_kinship_v1`, 524 names), each with its taxonomy and its way of life
    (habitat, movement, diet, wild or domestic) [SET-10]. Each name is entered with the narrowest
    taxon that holds what it commonly names, or the one species it most commonly means (salmon,
    *Salmo salar*) [SET-18]. The taxa are the Catalogue of Life's (a bat is the order Chiroptera,
    so it has no family or genus), and a name whose kinds span several classes is left out
    [SET-19]. Its main axis (the set's `label` field) is the familiar group of eight (mammal,
    bird, reptile, amphibian, fish, insect, arachnid, other invertebrate), with whole taxonomic
    orders as the held-out families [SET-20]. The taxonomy is kept beside the designed axes, not among them, since genus alone has
    hundreds of values [SET-21]. Habitat is land, fresh water, sea, or land and water; flying is
    left to how an animal moves [SET-22];
  - **objects** (`objects_harm_v1`, 321 objects): harmful, dual-purpose or benign, each with how it
    harms and its domain. Whole domains are held out, and a harmful-against-benign axis shows where
    the dual-purpose objects sit between the two [SET-23]. How an object harms: cutting, piercing,
    blunt, fire, explosive, chemical, projectile, restraint or none [SET-24]. The set holds 321
    objects rather than about 400, because single-word names of harmful things ran out [SET-25].

**The animal ontology.** Animals can be organized in many ways, so each animal gets a value in
many of them, a small ontology of the animal words: the space is explored rather than fitted to one
framing chosen in advance, and the model's states show which ways it follows most [SET-12]. In
Andrew's view, people group animals for practical reasons: an animal seen for a moment is
identified from a few cues [SET-14]. Why the first animal study compared descent with way of life,
and why that was too narrow, is answered in `docs/research/animal_ontology.md` [SET-13]. All 524
names are labelled in nine ways, with fourteen axes in all, since some ways have two [SET-15]:

| Way | Axes and their values |
|---|---|
| 1. descent | the group of eight; the taxonomic order |
| 2. everyday kind | beast, bird, fish-like, snake-like, lizard-like, bug, shellfish, worm-like, sea creature |
| 3. body covering | fur or hair, feathers, scales, bare skin, shell or hard case, soft body |
| 4. size | tiny, small, medium, large, huge, by typical adult weight |
| 5. legs | none, two, four, six, eight, more than eight |
| 6. where people meet it | at home, on the farm, in town and gardens, in the countryside, at sea or on the shore, far away |
| 7. relation to people | companion, kept for work or food, dangerous, pest, wild |
| 8. danger and feeling | danger to people: harmless, can hurt, can kill; how people feel: liked, neutral, feared or disliked |
| 9. way of life | habitat, movement, diet, wild or domestic |

A way **leads** at a layer when it explains more than any other way does about which animals sit
near each other there, with the other ways and the token count held fixed. Three measures judge it:
neighbours beyond chance, held-out reading with whole orders left out, and each way's own share of
the distances. Every axis can colour the app's charts, and the animals where the ways disagree
(whales, bats, flightless birds) are examples, not the frame [SET-16]. The study ran beside the
two documents; its findings are in `docs/research/animal_ontology_findings.md` [SET-17]. The first set's single framing is retired (see
[Rejected and retired](design.md#retired)).

## Lenses {#lenses}

Building lenses and using them to watch an agent are different activities; this section covers
building [LENS-1].

**Kinds of lens and grouping:**
- **a UMAP lens:** usually 6 dimensions per layer, clustered, with k chosen per layer [LENS-2];
- **a mass-mean lens:** one axis per layer, validated on held-out data [LENS-3];
- **raw-space groupings,** designed carefully and compared with UMAP [LENS-4]:
  - **standardized PCA:** centre, standardize each neuron, reduce to 50 dimensions, then cluster
    with Ward or spectral clustering [LENS-5];
  - **relevant-neuron PCA:** keep the neurons most associated with the classes, then reduce them
    with PCA, so the axes are weighted sums of named neurons and a new token is read by a linear
    projection. The classes choose the neurons, so they are chosen inside each training fold,
    judged only held out, and compared with the supervised ceiling, never with unsupervised
    groupings [LENS-6].

**Choosing k per layer:**
- **By hand or automatically:** k is set by hand, or suggested with its method named; both stay as
  tools [LENS-7].
- **The methods were re-tried** on the tank polysemy set, where the number of senses is known
  (`docs/research/lens_core_validation.md`) [LENS-8].
- **Nested clusters:** the levels method reports every level where the structure is clear (2 at
  the top and 5 below it, say), not one number [LENS-10]. Better automatic methods stay open
  [LENS-9].
- **A k profile per layer:** for each layer and k, the silhouette, the stability across seeds and
  the agreement with each designed axis; the chosen k is saved with the lens [LENS-11].
- **Tuning** chooses k and the settings by held-out AMI with the designed classes, because held-out
  accuracy keeps rising with k; accuracy and κ are shown beside it [LENS-12].

**Validating and comparing:**
- a lens must classify held-out data well, and the held-out data is whole scene families
  [LENS-13];
- Sankeys from both instruments are compared on class purity and separation, and the better is
  chosen [LENS-14]. The comparison is fair: the same k for all; unsupervised groupings compared
  only with each other; groupings built from the labels shown as the supervised ceiling, never a
  competitor; scores held out and corrected for chance [LENS-15];
- a self-check: tuning's search must find structure planted in synthetic data before it is
  trusted [LENS-16];
- **tuning:** a search over UMAP's settings and k, layer by layer; settings that fail the
  self-check drop out; winners are chosen on selection folds and scored on a test portion of whole
  families the search never saw, beside the lens it started from, the raw groupings and the
  ceiling. The tuned lens says its own validation is partly selection-biased; the test score is
  the unbiased one [LENS-17];
- **tuning by hand,** for better clusters: more settings in the form, a one-layer preview and a
  chart comparing lenses [LENS-18]. Hand-picked settings are recorded as such, and a lens whose
  settings were picked on held-out scores says it is selection-biased [LENS-19];
- **a lens remembers how it is held out:** the set declares its families, the capture keeps the
  declaration, and each lens records its families field, whole names, fold cap and test split for
  later jobs [LENS-20];
- **new data is judged on held-out sentences;** in Andrew's experience, lenses built from large,
  varied probes place held-out sentences in the right clusters strongly [LENS-46].

**Five method changes,** decided [LENS-21 to LENS-25]. The first four come first, ahead of the new
app: they need no model, and Andrew is using the machine for other work [ORDER-20]:
- the tuning's test split repeated over several draws [LENS-21];
- a stricter line beside "beyond the decoys", such as half the κ a linear probe reaches [LENS-22];
- decoys that keep the design's correlations [LENS-23];
- folds that hold out whole domains with each class's share about equal [LENS-24];
- each taxonomy match checked against the animal's common names [LENS-25]. Claude proposes running
  it first as a study script in the animal ontology's audit [LENS-27], then with the set audits in
  the builder [LENS-28].

The first four were built on 2026-10-16, and every lens they affect was scored again by
2026-10-20. Tested on five draws, tuning settings and k per layer gains little over the untuned
lens: a median over the layers of 0.02 and 0.05 AMI on the tank and calibration sets, and nothing
on the single words and the animals. The tuned lens is ahead on every draw at only 7 of 24 layers
on the tank set and 3 on calibration (`docs/research/lens_core_validation.md`). The decoys keep
the design's correlations that run through the label; keeping the others too waits (Claude's
suggestion in `docs/RECOMMENDATIONS.md`).

**What comes with each node and lens:**
- the neurons behind each node, found by correlation [LENS-29];
- what each node pushes toward through the output vocabulary (the logit lens) [LENS-31];
- a check that surface features (length, first word) don't explain the node [LENS-32];
- for each split between nodes, the share that comes from attention and the share from the
  experts, and the other token positions that carry the same signal [LENS-30]. Andrew moved the
  shares ahead [ORDER-20]. Claude's study on the stored captures
  (`docs/research/attention_and_experts.md`) found that they depend on the direction a split is
  measured along, so they stay off the node card for now, as Andrew decided (L33); the code built
  for the card is kept on a git branch [LENS-48].
  The other positions wait for the extra token positions that slice 2 records (Claude's placement)
  [DATA-7];
- the lens's expert fingerprints [LENS-34];
- how the lens bears on routing: the routing effect, and for mass-mean lenses the router alignment
  against random directions [LENS-35];
- the published features closest to each node, from the public sparse autoencoders for
  gpt-oss-20b: a comparison, not circuit discovery [LENS-36].

Before a key finding is accepted, its population is steered into the other node and what changes
downstream is recorded (see [interventions](design.md#interventions)) [LENS-33].

**How a lens reads a word** is one of three modes, chosen by experiment: a single token, a token
collection calibrated together, or a scan for any strong signal [LENS-42].

**How many axes** [LENS-45]. For a set with several designed axes, an analysis counts how many
each technique recovers on held-out data, layer by layer:
- the techniques: the UMAP lens's nodes, raw-space groupings, a linear probe (the ceiling) and
  PCA, with PCA's effective dimensionality beside the count;
- chance comes from decoy axes;
- angles between axes use partial axes, shown beside the design's own correlations, so axes
  correlated by design don't read as shared representation.

**Reports.** Every lens gets a report, agreed by LLM agents, covering its nodes, the experts
involved, and its pipelines and hubs, with every number checked (see
[LLM analysis](design.md#analysis)) [LENS-43, LENS-44].

## Attention in the analysis {#attention}

*Reworked on 2026-10-20 after Andrew's notes, and tested again. It replaces Claude's proposal of
2026-10-19, which Claude withdrew; its parts are listed under
[Rejected and retired](design.md#retired). The four parts have cards in L35.*

**What Andrew set and asked:**
- on 2026-10-19: attention joins the analysis as more information [LENS-49]; a row for its
  visualization goes below the Sankeys and the 3-D view [APP-35]; and can attention be analysed for
  each expert node and latent node, following the tokens along the nodes and edges they take
  [LENS-50];
- on 2026-10-20 he doubted the first proposal was useful and asked whether it was a reflex. He
  asked what attention adds to modelling how the model thinks, and whether its share of a split is
  worth knowing; how it serves the project's kinds of interpretability (the lenses, the internal
  representations they find and the expert routes); and how it helps the two aims, understanding
  the model and scaffolding AI systems. He noted ablation and similar interventions as known uses
  of attention. He asked for the case to be argued, and for Claude to say plainly if attention
  adds little rather than invent uses. He also asked for an attention Sankey
  over the population, which he thought might be best, so that the population can be analysed
  from three views: the latent nodes, the expert routes and attention [LENS-57].

### What attention can add {#attention-measure}

Claude's answer, from the tests under the next two headings. Attention adds less than the first
proposal suggested, and one thing it adds matters:
- **one kind of knowledge.** The lenses read what a token's state holds at each layer, and the
  expert routes say which experts work on it; both look at the token itself. Attention is the only
  step that brings anything from the rest of the input into the token. So it can add what a token
  takes from its context, and at which layers. Where the token's own state already shows the
  answer, it adds little;
- **scaffolding is about context.** A scaffold (a system prompt, a persona, an instruction, a
  description of the situation, earlier turns) changes what the model does only through what tokens
  take from it, so only through attention. Whether a deciding token takes the scaffold in, at which
  layers, and what it brings in, are attention's questions. Whether that changes the decision needs
  an intervention: blocking the token from reading the scaffold and reading the lenses again
  (L35.3), Claude's form of the ablation Andrew named;
- **its share of a split, on its own, is of little use.** It says which step wrote a difference
  into the state, not what caused it, and it changes with the direction it is measured along
  (`docs/research/attention_and_experts.md`, section 6). It stays off the node card for now
  (decided, L33) [LENS-48]; these reasons are Claude's;
- **in sets like the tank sentences it adds little.** There the meaning sits in a clue word the set
  put near the read word on purpose, so finding that the token reads the clue tells nothing new.
  Sets whose read word comes after the text, such as the framing set, are where it can add more.

### Latent nodes: a lens on what attention writes {#attention-nodes}

Claude tested Andrew's attention Sankey in two forms (`docs/research/attention_and_experts.md`,
section 11).

**First form: grouped by where attention reads from.** In the tank sentences, each item's share of
attention taken from the word itself, the token before it, the first token and the other words (or
from each distance back) was grouped into five groups, layer by layer. The groups follow where
" tank" sits in its sentence, not its sense. At every layer they agree with the sense at 0.01 to
0.08, and with the word's place in the sentence at 0.23 to 0.58 (AMI, adjusted mutual information:
0 is chance, 1 a perfect match). The state lens's nodes agree with the sense at 0.35 to 0.50 from
layer 4 on. A classifier trained to tell the senses apart from these shares (a probe) gets 0.23 to
0.34 balanced accuracy (the average of its hit rates per sense); from the word's place alone it
gets 0.24, and chance is 0.20. So where attention reads from is mostly a matter of the word's place
in its sentence.

**Second form: grouped by what attention writes.** A lens is built at each layer on attention's
write at the read token (the layer's output, minus its input, minus the experts' write) instead of
on the token's state. It was scored on held-out items in the same way as a lens's own validation,
in four captures. The numbers are agreement with the class on items the lens was not fitted on
(AMI), at as many nodes as classes; where the comparison changes when each lens gets its best
number of nodes (2 to 10 at each layer), the table says so:

| Capture | Where the class is | State lens | Lens on attention's write |
|---|---|---|---|
| framing (400 sentences, fiction or fact) | in the sentence before the read word, which is in a question after it | 0.28 to 0.87 from layer 3 on | higher than the state lens at layers 0, 2, 6, 14, 16, 18, 19, 20 and 21: by 0.08 to 0.55 at 6, 14, 16, 18 and 19 (at 18, 0.87 against 0.32), by 0.04 at 21 and 0.01 at 20. At 0 and 2 it is ahead only because the state lens finds almost nothing there (0.11 and 0.04, against 0.01 and 0.00). Under 0.06 at layers 1 to 3, 5 and 7 to 9. With each lens's best number of nodes it is ahead at the same five layers, by 0.09 to 0.35 (at 18, 0.87 against 0.52), and at layer 0 (0.15 against 0.06) |
| calibration scenes (600, aquarium or vehicle) | in the scene before the read word, which is in a question after it | 0.34 to 0.51 at layers 3 to 20 | above the chance line at 11 layers, up to 0.39; higher than the state lens only at layer 21 (0.28 against 0.09), where the state lens's two nodes collapse. With each lens's best number of nodes, it is ahead by more than 0.01 only at layer 19 (0.44 against 0.39) |
| friend/foe, tick 1 (479 ticks) | in the scene, read at "person" | at most 0.03 | at most 0.01. With two nodes no source groups by friend or foe; with more, all three do weakly (at best 0.27 for the state, 0.21 for attention's write, 0.26 for the experts' write) |
| tank (499 sentences, five senses) | in the sentence, around the read word | 0.26 to 0.48 from layer 3 on | 0.02 to 0.28, lower than the state lens at every layer |

In the framing set the read word is in a question after the sentence, so the sentence's own
attributes can reach it only through attention. Each of the event's scale and the threat's scope
has two values. With two nodes, the attention lens matches them at 0.73 and 0.70 at layer 3, where
the state lens's two nodes reach at most 0.20 and 0.24 at any layer. The state lens shows them only
with more nodes and later: at best 0.58 and 0.53, at layer 5, with four nodes. So in this capture
a lens on attention's write shows when the context comes in, and at which layers, which the state
lens can't. In the calibration scenes, whose read word is also in a question after the text, it
does not, apart from one layer. Where the meaning is in the token's own sentence (tank), it shows
less than the state lens does.

**Claude's proposal** [LENS-55]: attention's write as another input a lens can be built on (today a
lens is built on the token's state or on the experts' write), with its Sankey as the third
population view Andrew asked for. It is worked out from what every capture stores, so nothing new
is captured, and every lens tool works on it as it is: tuning, validation, the Sankey, lit paths,
node details and reports. Read beside the state lens's nodes and the expert routes, through lit
paths and cross-tables of nodes (how many tokens fall in each pair of nodes), it answers LENS-50
for latent nodes: the tokens of a node or a branch, followed through the attention lens's nodes,
show at which layers they took in different things. Its first use is a token reading its context:
a question after a text, and a decision under a scaffold.

### Expert nodes: brought by attention {#attention-experts}

Kept from the first proposal [LENS-56]. Andrew asked the same question of this part, so its use is
argued below and on its card (L35.2). At each layer the router reads the token after that layer's
attention has added to it. The router is worked out again with that layer's attention output
replaced by its mean over the lens's items: what attention adds to every item alike stays, and what
it adds to this item goes. An expert node's tokens whose expert would then be another are the ones
their own context sent there; the node card shows their share beside the layer's. It needs nothing
new: the states every capture stores, and the router's weights read from the model's files.

What the routing study found (`docs/research/attention_and_experts.md`, section 9):
- the item's own attention changes the first expert for 0% to 28% of items, by capture and layer,
  in the three sentence sets: routing is mostly decided by the token itself;
- some expert nodes are filled by context: small side branches of the expert Sankey (a median of
  28 to 69 tokens). In the tank sentences, 48 of the 54 tokens in expert 5 at layer 2 got there
  through their own context, 33 of them in vehicle sentences.

What it is for:
- **reading an expert node:** whether the node is about the word or about its surroundings. Without
  the share, expert 5 at layer 2 in the tank sentences would read as being about " tank", when
  most of its tokens were sent there by their context, mostly vehicle sentences;
- **scaffold studies:** a context can redirect the routing at a deciding token only through such
  nodes, so they show a study where a scaffold can move the routing;
- **unlike the split shares kept off the node card (L33):** it counts tokens whose expert actually
  changes, so there is no direction to choose and no random splits to compare with. The recomputed
  routing matches the capture for at least 98.8% of items.

It covers expert nodes, not the edges between them (LENS-50 asked about edges too). The same count
could be given for an edge's tokens, which Claude would propose only once the nodes prove useful.
The words that pushed toward an expert (each word's part of its router score) are dropped: they
need the word-by-word parts, and they mostly echoed the sets' planted clue words.

### The row {#attention-row}

Claude's proposal [APP-37]. When a capture has a lens on attention's write, the row under the
cluster Sankey and the expert Sankey is that lens's Sankey, its columns lined up with theirs; it
shares their selection, so an item, a node or a branch lights its path through all three. Brought
by attention shows on the expert node cards. Every chart exports with its recipe [APP-17]. With no
such lens, the row offers to build one.

### Where the numbers come from {#attention-data}

Nothing new to capture. Every capture stores the token's state after each layer and the experts'
write; attention's write is the state minus the state before the layer minus the experts' write (at
layer 0, minus the word's own starting vector). The word-by-word parts the first proposal needed
are dropped with it: they came from running the model on the CPU one layer at a time, or would
have been recorded during capture.

### Where not to go {#attention-not}

Claude's proposal [LENS-54], from the tests:
- **rows of words:** where attention reads from, word by word, mostly finds "the", follows the read
  word's place in its sentence, or finds the clue words the set planted;
- **the heads' weights as a view, and single heads:** a weight is where a head looks, not what it
  brings back; there are 1,536 heads, and the design puts experts before heads [PRIN-10, PRIN-11];
- **attention rolled out or traced back across layers:** tested, it piles onto the first token;
- **recording word-by-word parts during capture, and the word-by-word run on the CPU over more
  sets:** nothing kept needs them;
- **causes from any of these readings:** blocking attention is the test of a cause (L35.3).

Attention's share of a split is not on this list: it stays off the node card for now, and the
question returns with slices 2 and 8 (L33) [LENS-48].

### When {#attention-order}

Claude's proposal [ORDER-21]:
1. **done now, without the model:** the tests, and the findings in the study's note;
2. **with the observatory,** the new app's room for reading a lens across its layers (step 6 of the
   new app's plan): attention's write as a lens input, its Sankey as the row, and brought by
   attention on the expert node cards;
3. **slice 8, conditions and interventions** (after the Winter Survival pilot): blocking attention
   [INT-10], and the scaffold studies that use the attention lens first.

### How sure {#attention-sure}

"Right to build" is how sure Claude is that the part is worth building; "works as described", that
it will work as written.

| Part | Right to build | Works as described | What it rests on | What would raise it |
|---|---|---|---|---|
| a lens on attention's write (L35.1) | 70% | 95% | held out on four captures: useful in one (framing); in the calibration scenes, also read from a question, ahead of the state lens at one layer only; lower in friend/foe and tank. Built from stored data with the existing lens tools | a set made for it (questions about texts, scaffolds), tuning, a second random seed: the framing results swing from layer to layer (0.15 at layer 17, 0.87 at 18) |
| brought by attention (L35.2) | 80% | 95% | the recomputed routing matches the capture for at least 98.8% of items; context-filled nodes in all seven captures; its use is in reading those nodes and in scaffold studies | more lenses, and a scaffold study |
| blocking attention (L35.3) | 85% | 80% | a standard intervention; needs slice 8's ways of changing the model's activity | building it with slice 8 |
| what goes (L35.4) | 90% | not applicable | the tests above | none needed |

The weakest part is the attention lens's reach: one capture of four shows what it is for, and the
other capture of the same shape (the calibration scenes) does not. A set built for it in the
builder (slice 3), with questions about texts and scaffolds, would show how often it pays.

## Reading over time {#time}

**Three orderings are time:** context steps (a sentence sequence grows), ticks (the agent's turns)
and reasoning steps (the reasoning stream grows inside one tick) [TIME-1]. The next tick's input
leaves out earlier reasoning streams: the runner hands back only the action, as gpt-oss's chat
format does [TIME-2]. So readings are compared within one ordering, and never from one tick's
reasoning to the next tick's; depth (the layer) is not time [TIME-1].

**Rules for reading over time,** each kept for a reason [TIME-3]:
1. the same kind of site, read the same way every time;
2. validation on held-out scene families;
3. the lens checked in the context it reads;
4. statistics at the scene-family level;
5. one fixed, saved lens reads every point;
6. dynamics computed within one ordering.

References are a tool for studies, not a rule for every reading.

**Where an agent's run is read:**
- **at the output, the main reading:** each lens is read at its keywords in the agent's output
  (the action it sends to the MUD), the same kind of site every tick, where the decision is written
  [TIME-4]. The output is the best single place to capture understanding [TIME-8];
- **across the reasoning, a scan:** every token is read through each lens of the kit and compared
  with how the same token reads in neutral text; the few tokens with a strong signal light up
  [TIME-5];
- **carriers, by replay, the controlled comparison:** take the run's exact context up to a point,
  add the lens's carrier, run one forward pass with no generation, and read the carrier's token.
  Carriers are also the method for sentence studies [TIME-6]. They help with demonstrations but
  don't show how the model would really act [TIME-7].

**The reasoning streams are analysed first,** mostly for frequent words, before the agent is asked
to use any word [TIME-9]. Claude proposes that words it uses often become candidate read sites
[TIME-10]. Asking it to use words chosen for it is a last resort [TIME-11]; giving it words marked as for
measurement only stays an idea to test [TIME-12].

**Two numbers in every reading:** presence (whether the concept is there at all) and position
(which class it leans to, and how far). Unresolved, present but between the classes, is told apart
from absent; a reading still between the classes at the output is flagged as worth opening in
Watch [TIME-13]. Presence is calibrated on states that include natural in-between ones [TIME-14].

**"Between the bands" in studies.** A study judges "between the classes" against bands, the range
of each class's readings at that point, taken from references: runs whose label never changes,
from scene families the lens wasn't fitted on. Agent studies come as scripted runs, for claims
about change over time, and free play, for behaviour [TIME-15]. The context-shift study's own
question, whether the in-between state is learned, a passage or off the model's usual states,
belongs to that study [TIME-16].

**The first version is tested on known answers:** it must reproduce the paper's per-run tank
results (the crossing point, the settled level and the dwell) before it is used on agents [TIME-18].
The questions experiments settle are under [Open questions](design.md#open-questions) [TIME-17].

## The app and its rooms {#app}

**The app is rebuilt** from the ground up rather than changed, as long as everything it does today
comes back; tools and approaches may change, and the approach is Claude's to choose [APP-1]. More
of it is visual: values are set with visual controls rather than typed, as the clustering controls
now are [APP-2]. Andrew also suggested controls that fold, and doing some of the work from the MUD
[APP-3]. Straight after the two documents, the app is built room by room until it does everything
today's app does [APP-5].

Claude's approach [APP-6]: the new app is built beside the current one, with the charts' code
carried over with its tests and the same tools (React, TypeScript, Vite, ECharts); every room is
walked against a checklist of every current feature before it is called done. The checklist and
the build are in the [plan-and-architecture document](plan.md#the-new-app).

**What the app is for.** Analysing runs that have happened, clusterings and the reports the LLMs
write, and holding the builders. It doesn't start runs: they start in the MUD or through Claude
Code [APP-7, MUD-15]. Its workspaces, as decided before the rooms, are Build, Layers, Watch, Study,
MUD (keeping the MUD running, and designing scenarios with Claude agents) and Atlas [APP-7], and
later Ideas [APP-8]. The rooms below take them over; the table says which room holds which. A pass
over what is done where, so common tasks are easy and screens aren't crowded with parameters,
shapes the rooms [ORDER-18].

### The rooms {#rooms}

**Rooms are the app's places** [APP-4, MUD-4]: each room has its own colours and tools; a map and a
quick-jump box reach any room at once; with the MUD open, moving in either one moves the other;
and the app works with the MUD closed. Andrew likes moving between rooms as a way to get around
the app [MUD-5].

**The institute's layout** (Andrew, in his answer to L30 on 2026-10-18 and his notes on L31 and L34
on 2026-10-20):
- **an AI greets** users and guests when they arrive [MUD-23];
- **public simulation rooms:** most visitors come to play Winter Survival, so the institute has
  public simulation rooms (Andrew suggested three), and every lab has its own [MUD-24];
- **four departments,** which he also calls labs: linguistics, general mechanistic
  interpretability, alignment, and discordant studies; each has its AI scientists, a description
  of the place, its simulation room, its boards and whatever else suits it [MUD-25];
- **a lounge** to spend time in [MUD-26];
- **a meeting room** for discussions among the AIs: mainly adding to the paradigm; also changes to
  gpt-oss-20b itself, such as a steering vector or a scaffold; and, as a nice-to-have, work that
  crosses departments and may call for specialists, such as planning scaffolds with people or
  without them [MUD-27];
- **the greeter is an AI with a form,** not called a robot (L38.3, 2026-10-22) [MUD-29];
- **out-of-service stairs** lead to a closed floor, kept for what the AI scientists open when they
  redesign the institute (L38.4, 2026-10-22) [MUD-30];
- **characters for the non-player characters,** built in the MUD (Andrew's suggestion) [MUD-31];
- **polishing passes:** a couple of passes over the layout before building begins, with a map of
  the institute in the app; then iterations to improve the room descriptions [ROOM-19];
- **in the long run,** the AI scientists design the institute themselves, around what the research
  finds the study of gpt-oss-20b needs [MUD-28].

**The rooms** (Claude's proposal, approved by Andrew on 2026-10-20, L34) [ROOM-1]:

| Room | What you do there | What it replaces today |
|---|---|---|
| **the entrance hall** | where everyone arrives: the greeter (built with the AI scientists, slice 11), the map of the institute with what is new in each room, the quick-jump box [ROOM-2, MUD-23] | the MUD's hub room |
| **the public simulation rooms** | visitors play Winter Survival; researchers watch, or start agent runs; Watch (following an agent's run as it plays) from slice 4 [ROOM-7, MUD-24] | the MUD's simulator room, whose jobs go to these rooms and the departments' own [ROOM-21] |
| **a department** (four; each is also a lab) | opens the shared rooms with its own studies loaded; its own simulation room; its boards (its studies, open questions, findings proposed, recent results); its AI scientists from slice 11 [ROOM-15, MUD-25] | the polysemy lab stays its own room, in linguistics [ROOM-21] |
| **the observatory** | read a lens across its layers: the Sankeys, 3-D, members, the output table, pipelines and hubs, fingerprints, node details, the analysis panel [ROOM-3] | the Layers screen |
| **the lens workshop** | make and judge lenses: the form, preview, compare, validation, tuning, axes, mass-mean lenses; start node details [ROOM-4] | the Build screen |
| **the library** | the papers and articles we write, at the front where visitors can go [ROOM-5] | nothing (new) |
| **the studies room** | every study: question, sets, captures, lenses, findings, ledger, status, showcase, and the department that holds it [ROOM-8, STUDY-2] | nothing (new) |
| **the lounge** | spend time and talk, with people and with the AIs; it has no tools, so the app stays where it is [MUD-26] | nothing (new) |
| **the meeting room** | the AIs' discussions, findings proposed to the paradigm among them; their agenda and record shown in the app from slice 11 (the AI scientists) [MUD-27] | nothing (new) |
| **the scaffold studio** | scaffold studies; its tools come with slice 8 [ROOM-26] | nothing (new) |

**Shared tools:** the observatory, the lens workshop and the studies room serve every department,
and a department opens them with its own studies already loaded, as the polysemy lab does now
[ROOM-15]. Capturing, steering and similar tools are not rooms (there is no capture room or
steering room): they are used inside whichever room needs them [ROOM-26]. The MUD workspace of the
earlier design did two jobs, now split: designing scenarios moves to the builder, whose room is
waiting for a decision when slice 3 is planned, and keeping the MUD running to the simulation rooms
[ROOM-1]. Later rooms: the atlas, ideas (in the department of discordant studies), and researchers'
rooms [ROOM-1, MUD-13].

**Which department holds each study** (a study can move later) [ROOM-17]:

| Department | Studies |
|---|---|
| linguistics | single words; animals; the animal ontology; the read site (which token of a single word to read); and the polysemy lab, with the tank lens (the five senses of "tank") |
| general mechanistic interpretability | the lens core (the instrument and its checks); the attention-and-experts study; the context-shift paper |
| alignment | objects and the harm axis; the suicide letter; friend/foe, with the people-assessment set (friend/foe broadened to more ways of judging people) planned after it |
| discordant studies | the Ideas workspace and its idea-tracking engine [APP-8]. Claude assumes the department takes the role a department of discordant research had in the institute's first vision (now archived): bringing discord into the research on purpose, by inverting assumptions and setting frames against each other |

**Built in stages** [ROOM-18]:
1. with the new app's rooms: the layout file, the map, and every room in the MUD with its
   description, exits and boards;
2. with slice 11 (the paradigm and the AI scientists): the greeter, the AI scientists and the
   meetings;
3. with hosting [MUD-20] and the Winter Survival pilot: public play, one Winter Survival world per
   public simulation room.

With the new app's plan (Claude's timing, approved by Andrew on 2026-10-22, L38), the non-player
characters are written and placed in their rooms in the first stage, so visitors can look at them
and read about them; their minds come in the second [MUD-31].

**The floor plan** (approved by Andrew on 2026-10-27, after two rounds of drafts and his
corrections) [ROOM-25]. A gap in a wall is a door; the dotted strips are corridors:

```
┌────────────┬────────────┬───────────────────────────────┬─────────────────────────┬─────────────────────────┐
│  Polysemy  │            │                               │                         │                         │
│    lab     │ Ling. sim  │           Mech. sim           │       Align. sim        │      Discord. sim       │
│            │            │                               │                         │                         │
├────     ───┴────     ───┼────     ──────────────────────┼────     ────────────────┼────     ────────────────┤
│                         │                               │                         │       DISCORDANT        │
│       LINGUISTICS       │         MECH. INTERP          │        ALIGNMENT        │         STUDIES         │
│                         │                               │                         │                         │
├────     ────────────────┴────     ──────────────────────┴────     ────────────────┴────     ────────────────┤
│· · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·│
├────     ────────────────┬─────────────────────────┐ · · ┌─────────────────────────┬────     ────────────────┤
│                         │                         │· · ·│                         │        Scaffold         │
│      Meeting room       │       Observatory         · ·        Lens workshop      │         studio          │
│                         │                         │· · ·│                         │                         │
│                         ├─────────────────────────┤ · · ├─────────────────────────┤                         │
│                         │                         │· · ·│                         │                         │
│                         │         Lounge          │ · ·        Studies room       │                         │
│                         │                         │· · ·│                         │                         │
├─────────────────────────┴────────────┬────     ───┴─   ─┴────────────┬────────────┴─────────────────────────┤
│                                      │                               │                                      │
│             Public sim 1                                                                                    │
│                                      │                               │                                      │
├──────────────────────────────────────┤                               │                                      │
│                                      │         ENTRANCE HALL         │                                      │
│             Public sim 2                     greeter · stairs        │               Library                │
│                                      │                               │                                      │
├──────────────────────────────────────┤                               │                                      │
│                                      │                               │                                      │
│             Public sim 3                                             │                                      │
│                                      │                               │                                      │
└──────────────────────────────────────┴──────────────   ──────────────┴──────────────────────────────────────┘
```

- **one floor,** with the out-of-service stairs rising from the entrance hall to a closed floor that
  isn't drawn [ROOM-20, MUD-30];
- **the visitors' rooms at the front:** the three public simulation rooms together and the same
  size, the library with our papers, and the lounge, all opening onto the entrance hall
  [ROOM-22, ROOM-5];
- **the shared research rooms in the middle,** around a short central corridor; no shared room is
  reached through another;
- **the four departments together along the back,** on their own corridor, each with its private
  rooms opening only from inside it; the polysemy lab stays its own room, in linguistics [ROOM-21];
- **rooms, not tools, and no hallways turned into rooms** [ROOM-26].

The earlier passes are kept in the decision log: Claude's first map on three floors (2026-10-20),
and four drafts with suggested rooms (2026-10-24), which Andrew turned down as convoluted.

**The layout is data** (Claude's proposal, approved with the new app's plan, L38): the institute is
built from one file holding its floor plan, `data/institute/layout.yaml` (a grid, each room a
rectangle on it, and the doors between rooms), as the lab presets are today (`data/labs/`). A department or a room can then be added, renamed or moved without changing code;
the AI scientists will need this to redesign the institute [ROOM-16, MUD-28]. Each study names its
department in its `study.yaml`.

**How rooms work** (Claude's proposal):
- **one room in the MUD for each:** walking there in the MUD opens it in the app, and choosing it
  in the app moves your character; with the MUD closed, the map and the quick-jump box move you;
  the lounge is in the MUD alone [ROOM-9];
- **the quick-jump box** takes a room's name or a MUD-style command: `go workshop`,
  `lens show tank-k5-n15`, `study animals` [ROOM-10];
- **each room's look:** its own accent colour and header from one set of design tokens; the colours
  that carry data (classes, nodes, experts) never change between rooms, so a chart reads the same
  everywhere [ROOM-11];
- **inside a room:** controls in panels that fold, the basic ones open; sliders and toggles for
  numbers; whatever is selected opens in a details panel beside its chart [ROOM-12];
- **what every room shares:** the top bar (the room, the capture and lens where they apply,
  background jobs, the MUD's connection and your role), the folding MUD terminal, deep links (the
  view's state in the address), and commands from Claude Code and the MUD [ROOM-13];
- **roles:** visitors read and researchers act; a lab room locks its capture [ROOM-14].

### Rules for every screen {#screens}

- Basic controls first, the rest behind Advanced: clustering's Advanced holds automatic k and the
  choice of method [APP-9].
- Panels size themselves to the window; dividers drag; any panel can fill the screen and come back
  (built in Layers) [APP-10].
- The MUD terminal folds away when it isn't needed [APP-11].
- The main pane shows one timeline at a time, and every panel holds one chart [APP-12].
- Each variable gets one visual channel (colour, shape, pattern or line style), and the legend is
  always on [APP-13].
- Missing pieces are named: with no validated lens for a site, the view says so and links to where
  lenses are built; with too few runs at a point, that point is drawn faded [APP-14].
- The page never scrolls sideways; only charts meant to scroll do [APP-15].
- An analysis panel sits beside each view [APP-16].
- Every chart exports its picture (SVG, PNG) and its data (CSV, JSON), with a recipe (the lens and
  version, the captures, the settings, the commit) so the figure can be made again [APP-17].
- The app takes commands: Claude Code, Claude agents and the MUD use one small command interface to
  open a view, run a clustering or choose a lens [APP-34].

### Reading a lens across its layers {#layers}

Today's Layers view [APP-18], which Claude proposes becomes the observatory [ROOM-3]:
- **all 24 layers in one view that scrolls sideways,** with a zoom (6, 12 or 24 layers) and an
  overview strip; the cluster Sankey and the expert Sankey stacked and scrolling together;
- **expert weights are the model's own:** the expert's weight among the token's four, with all four
  ranks [APP-19], and a weighted view of all four ranks where a pipeline's every step can be drawn
  [APP-31];
- **clustering** from this view and from the polysemy lab's room in the MUD; today it runs from
  Build and from the lab [APP-21];
- **colour by any designed axis** [APP-23], with mixtures shown faithfully: blended in a
  perceptual colour space (OKLab), with optional striped nodes for exact shares, and two axes in
  one colour (hue and lightness) with a square legend [APP-24];
- **expert fingerprints:** for any node, population or condition, a 24 × 32 grid of each expert's
  weight at each layer, and difference grids [APP-25];
- **one layout for expert Sankeys,** fixed across conditions, so a difference is real rather than
  layout [APP-26];
- **where the instruments disagree is marked** on the cluster Sankey [APP-27];
- **the 3-D view** shows what the lens counts, coloured by node [APP-28], drawn in the lens's own
  space: its three main directions, each layer turned to line up with the one before, one scale on
  all axes, read items in the same frame, in its own panel [APP-29];
- **a selection lights its path:** an item, a node's members, a pipeline or one step of a run, in
  both Sankeys and in 3-D; Watch will draw a tick's path the same way [APP-30];
- **cards with LLM-written reports** for clusters, experts, routes and expert routes [LLM-5].

Still to come here:
- clicking a node lists the runs that pass through it, and when [APP-20];
- more visual channels: lines shaped by sine waves, patterned Sankey nodes [APP-22];
- depth heatmaps: tokens × layers for one sentence or tick, and layers × time for a run or a study
  [APP-32].

## The builder {#builder}

**One builder for sentence sets and scenarios** [BUILD-1]: `claude -p` drafts a labelled sentence
set or a scenario; you review it in a table beside its audits, edit or redraft it, and save it as a
version. A friend/foe scenario gives the model the scene and the list of commands at each tick, so
the builder can draft one. In the app, Claude agents generate sentence sets to instructions
[SET-26].
- **It stays open to experiment for scenarios:** several authoring setups and teams of Claude
  agents can be tried until the scenarios meet their criteria, instead of a single bare request
  [BUILD-2].
- **Who writes a set:** one `claude -p` run writes each whole set, all classes together, or a team
  whose every agent works across all the classes, so author differences can't line up with the
  classes; the audits check batches anyway [SET-27, BUILD-3]. Authors get a blind brief: only the
  contrast and the diversity rules, as in the paper [SET-29].
- **Later** it also edits a study's design [BUILD-4].
- Claude proposes treating the sentence set builder and the scenario builder below as its two
  halves [BUILD-5].

**The sentence set builder** shows the instructions given to the authoring agents and the sets that
come back [BUILD-6]:
1. describe the contrast: the target word, the classes, the carrier, the number of sentences per
   class, the scene families, the diversity rules;
2. read and edit the brief the authors will receive;
3. generate;
4. review the sentences in a table (text, class, scene family) beside the audits, and a critic that
   catches confounds the numeric audits can't, such as one class always written in the past tense
   [LLM-9]; edit or regenerate;
5. save the set with a version, then start its capture as a background job.

**The scenario builder** [BUILD-7]:
- it lists scenario sets and their versions;
- you edit a scenario's stages, actions and labels, and validate them;
- the builder opens the MUD terminal with the command ready, so you play the scenario yourself
  (`simulate`) or start the agent on it (`agent run`); runs still start in the MUD;
- Claude agents can draft scenarios to instructions; a mini-world builder comes later.

**The lens builder** [BUILD-8], built today with UMAP and Ward as its one reduction and grouping:
1. pick a capture;
2. set the Basic settings: UMAP's neighbours and dimensions, minimum distance and distance metric,
   k, a name;
3. under Advanced, set the settings per layer, k per layer (with the automatic suggestion and its
   method), the reduction and grouping methods, the hold-out design and the filters;
4. build: the build runs in the background, and the new lens opens when it is ready;
5. read the k profile and the held-out scores, then save the lens with its site and keywords.

Around it: "Rebuild with…" on each lens card [BUILD-9]; a one-layer preview in seconds, held out
on request, run as a background job so it matches a build exactly [BUILD-10]; a chart comparing
lenses, with a tuned lens's test score [BUILD-11]; and a mass-mean lens's readings by class, so the
dual-purpose objects' place on the harm axis shows [BUILD-12].

**The kit editor:** for a scenario set, choose its lenses and their keywords [BUILD-13].

## Watch {#watch}

**Watch,** the app's view of an agent's run (not the MUD's `watch` command, which follows a
character), shows which representations are active over time [WATCH-1]:
- for each scenario set, its own panel of lenses;
- a lens heatmap in which every token is scanned through each lens (most sentences show nothing);
- each lens also read at the output, at keywords from the scenario's MUD commands;
- for each lens, its own Sankeys; lens panels, as many as wanted;
- replay, explained readings, bookmarks, runs side by side and live alerts;
- the screen's space used well.

**The layout:** the lens heatmap on top, the lens panels below it, and a side drawer holding the
run's text (tinted by the selected lens), the bookmarks and, during a live run, the MUD terminal.
Each area resizes and can fill the screen [WATCH-2].

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

**The lens heatmap** [WATCH-3]: rows are the kit's lenses grouped by theme, each naming its classes
and keywords, with a badge saying whether the lens is validated where it is read. By default each
tick is one column holding its output reading; opening a tick shows the observation (O), the
reasoning sentence by sentence (R1, R2…) and the output (A). Brightness is presence and colour is
position; a UMAP lens colours by node. The output cell is flagged (!) when the concept is present
but still between the classes, and an events lane shows stage changes and each action by type.
Each lens is read at its best held-out layer by default, with a selector to change it [WATCH-4].

**The lens panels** [WATCH-5]: as many as wanted, one lens per panel, each showing its cluster
Sankey with a toggle to its expert Sankey. Panels sort by how strongly their lens is present in the
selected tick; pinned panels stay on top and absent ones dim. A mass-mean lens gets a three-bin
Sankey (one class, between, the other class). All 24 layers scroll sideways together.

**Which token each panel uses, for now** [WATCH-6]: a lens lights up in a tick only when its
strongest token beats the strongest token in neutral text of the same length (the strongest of
hundreds always looks strong by chance). Its path is drawn from the output keyword, the same kind
of token every tick, or from the strongest token, said so, when there is no keyword. Clicking any
heatmap cell or token switches the panels to that token, drawn over the faded calibration flows.

**Around it:**
- **replay:** step through a recorded run tick by tick, with the heatmap, panels, text and MUD
  transcript moving together [WATCH-7];
- **branch from any tick:** change one thing (the observation, a scaffold or a steering vector) and
  let the model continue; the branch is a new run and a condition, opened side by side with the
  original [WATCH-8];
- **a reading explains itself:** hovering a lit cell shows the lens's calibration sentences closest
  to that state [WATCH-9];
- **bookmarks:** a note on a moment, saved into the study's files for analyst agents [WATCH-10];
- **side by side:** two runs with their ticks aligned [WATCH-11];
- **live alerts:** when a chosen lens lights up, or a reading is still between the classes at the
  output; judged per run, by how many runs they catch at an acceptable false-alarm rate [WATCH-12];
- **a run in progress** opens like a finished run, each tick appearing once saved; the scan never
  slows the agent, and the agent's play is watched in the MUD [WATCH-13];
- **LLM notes:** a run report, a note on a clicked moment, and a comparison of runs side by side
  [LLM-12].

**What Watch needs from the rest of the software** [WATCH-14]: the runner captures the kit's
keywords in each action and stores each tick's token ids; the scan runs by replay or during the
runner's capture pass and stores only the readings; each lens has a neutral baseline, a chance
level for the strongest token and a nearest-neighbour index over its calibration states; readings
are computed once and stored.

**Risks, and what answers them** [WATCH-15]:
- a raw reading at an arbitrary token mostly shows what the token is: the scan compares each token
  with the same token in neutral text;
- the strongest of many tokens looks strong by chance: lighting up is judged against the chance
  level;
- the middle of an axis can mean torn or absent: presence tells them apart;
- readings drift as a run grows: the heatmap shows raw readings by default, and with references
  Advanced shows them against the bands;
- a lens not validated where it is read carries the exploratory badge;
- many lenses take space: heatmap rows group and fold, empty rows hide, and lens panels sort and
  dim.

## Studies {#studies}

**The studies room** is one of the new app's first rooms: a clear place showing which studies there
are, where their designs are iterated on [STUDY-2]. Its first version shows each study with its
question, sets, captures, lenses, findings and ledger; designs are edited with the builder later
[STUDY-3]. Claude proposes showing each study's status and showcase too, its design when opened,
and its runs' timelines once it has runs; until the builder edits designs, a study file changes
through Claude Code or by hand, and git keeps each earlier design [STUDY-4].

**Study, the view that compares many runs of a study** [STUDY-1] (it opens from the studies room
once a study has runs):
- a study file sets up the view: its runs, references, lens, layer, the event to align on and how
  runs are grouped;
- the study timeline: readings over time by condition, against the bands, with a confidence
  interval from a bootstrap over scene families and the number of runs at each point;
- one run list, marked by where each run was started, sortable by its ticks between the bands, its
  crossing tick, its final class and its outcome; opening a run shows its timeline, with a button to
  Watch;
- behaviour: each tick's action, or would-be action, against its reading;
- depth over time, the layers × time heatmap for the study's lens [STUDY-5], and a temporal Sankey
  of node transitions once there are enough runs [STUDY-6];
- a study report on crossings and the differences between conditions [LLM-13];
- readings are background jobs, computed once and stored (200 runs × 7 ticks take about 25 to 70
  minutes of GPU).

## LLM analysis {#analysis}

LLMs are good at spotting patterns in this data, such as pipelines, hubs and split points, so
there is an analysis panel wherever it helps, and cards with LLM-written reports
[LLM-1, APP-16].

**The panel, the same everywhere** [LLM-2]: beside a view, showing the report on whatever is
selected; each report cites its numbers, and a checker re-computes them; reports are written in the
background when their data is built, kept, and rewritten when the data changes; a question box asks
follow-ups; reports are marked as LLM-written, and a finding still goes through the paradigm's
review. Analysts are tested before they are trusted, and again when prompts or models change:
decoys (a sound analyst reports nothing), planted findings (it finds them) and predictive
descriptions (another model picks a node's members from its description) [LLM-3]. Reports have a
budget: validated lenses and selected items first, the rest on demand [LLM-4].

**Where analysis goes** (by today's view names; the rooms take them over):

| Where | What the LLM writes | Requirement |
|---|---|---|
| Layers | a card for each cluster, expert, route and expert route | [LLM-5] |
| Layers | a card for each split point: what separates the two populations | [LLM-6] |
| Layers | a report on the pipelines and hubs (the routes card) | [LLM-7] |
| Layers | a short note on what each layer transition changes | [LLM-8] |
| Build | a critic for each new sentence set | [LLM-9] |
| Build | each lens's report: its nodes, experts, pipelines and hubs, agreed by two drafts | [LLM-10, LENS-43, LENS-44] |
| Build | a k advisor that explains the k profile while you choose | [LLM-11] |
| Watch | a run report, a note on a clicked moment, a comparison of runs side by side | [LLM-12] |
| Study | a report on crossings and on differences between conditions | [LLM-13] |
| Atlas | reports connecting lenses, and a report for each analysed scaffold | [LLM-14] |
| Ideas | what to probe next, from the gaps in the atlas | [LLM-15] |
| the MUD, later | a guide in each lab who answers questions from the cards | [LLM-16] |

## The MUD and agents in scenarios {#mud}

**What the MUD is for:**
- **first,** Andrew's idea: running agents in scenarios, alone or with people taking part [MUD-2].
  How people take part is chosen per scenario: they only watch, or play a character the agent
  meets, with their lines recorded as part of the run's conditions [MUD-3];
- **second,** a way to move around the app, now its rooms [MUD-4];
- **experiencing, playing and watching:** the institute, its labs, the simulator, and later the AI
  scientists' rooms and their events [MUD-7]; entering a scenario room to replay a run and watch
  which representations light up [MUD-8]; a user interface could live in the MUD [MUD-9];
- **not for writing:** sentence sets and scenarios are written in the app's builders [MUD-10].

Winter Survival, the free-form world, is a different undertaking, with its own game design document
[MUD-6, DOC-14].

**One repo and one MUD** [MUD-1]. The MUD, named Scaffold Dynamics, hosts the institute and the
scenarios; its first free-form world is Winter Survival [MUD-21]. The old prototype MUD was retired
once everything worked in the new one [MUD-22], and `simulate` shows what the agent sees when a
scenario loads [MUD-22].

**The institute's rooms,** built today: the hub, where everyone starts; the polysemy lab, which
opens its view on entry; the simulator, the scenario library's menu [MUD-11]. Andrew's layout of
2026-10-18 adds a greeter, public simulation rooms, four departments with their AI scientists, a
lounge and a meeting room [MUD-23 to MUD-28]; Claude reads the departments as the AI scientists'
rooms decided earlier [MUD-12]. Researchers' rooms come later
[MUD-13]. Each is described under [The rooms](design.md#rooms), and Claude proposes a room in the
MUD for each of the app's rooms [ROOM-9].

**What the MUD plays:** sentence sets; staged scenarios, multiple choice in stages with known
labels at each stage; worlds, Winter Survival the first of many; mini-worlds, a starting situation
on a world's engine with exit conditions [MUD-16].

**Agent runs start in the MUD,** with `agent run`, or through Claude Code; the app analyses them
[MUD-15]. The runner plays through a control channel, and nothing a watcher does reaches the agent
[MUD-17].

**Commands.** Every command is documented [MUD-14]:

| Where | Command | What it does |
|---|---|---|
| anywhere | `look` | see the room |
| institute rooms | `watch <name>` | follow a character, such as `agent`, into each scenario it plays |
| institute rooms | `unwatch` | stop watching and go back |
| a watched scenario | `look`, `examine`, `actions` | a watcher reads the scenario and every line the player types, and can't act or speak there, since anything said would reach the agent's prompt |
| the simulator | `simulator` | list the scenario library's sets |
| the simulator | `simulator <set>[/<subset>]` | list one set's scenarios, or one subset's |
| the simulator | `simulate <set>[/<subset>]` or `simulate <set> <scenario>` | play a scenario yourself, opening with what the agent sees. Researchers only |
| the simulator | `agent run <set>[/<subset>] [<scenario>]` | have the agent play, with its activations captured; without a scenario it plays the whole set or subset. Researchers only |
| the simulator | `agent stop` | stop the agent's run |
| the polysemy lab | `lens` | say what the lab shows |
| the polysemy lab | `lens list` | list the lab capture's lenses |
| the polysemy lab | `lens show <name>` | open a lens in your app |
| the polysemy lab | `lens build [k=] [n=] [dims=] [as <name>]` | build a lens in the background; your app opens it when it's built. Researchers only |
| a staged scenario | `look`, `examine <thing>`, `inventory` | read the situation |
| a staged scenario | `actions` | list the choices |
| a staged scenario | a choice's command | take that choice |
| a staged scenario | `leave` | go back to where you came from |
| Winter Survival | `VERB thing [RELATION thing] [WITH tool]` | play the world |
| the login screen | `connect guest` | visit as a guest; guests can watch |

**Which MUD:** once Scaffold Dynamics is hosted for others, the app and the backend connect to it by
default; a user can run their own MUD instead, usually on localhost [MUD-18]. Hosting it (a server,
accounts, abuse handling and cost) comes before other researchers are invited; until then the
default address is localhost [MUD-20]. The address is entered in the app and checked with the MUD
before it is saved [MUD-19].

### Lens kits for scenarios {#agents}

- Each scenario set gets lenses designed for it, or reuses lenses already built [LENS-37].
- **People assessment:** friend or foe and the type of foe, and others such as intent, threat,
  honesty and need [LENS-38].
- **Winter Survival:** what the agent is thinking about, such as hunger, food, fire, cold, injury,
  danger and trust in the others [LENS-39].
- More lenses and situations will come as the work goes on [LENS-40].
- **Each kit lens lists its keywords,** drawn from the scenario's MUD commands (the object in
  `greet stranger`, the words in `eat fish` and `light fire`). The lens is read at those keywords
  in the agent's output, and kit lenses are calibrated on text like the agent's own [LENS-41].

## Data and records {#data}

- **The data lake:** captures stay outside git. The lake on WSL's disk holds the six kept sessions
  and every new capture, and was not copied wholesale; the paper's lake stays on the C: drive
  [DATA-1].
- **Libraries:** sentence sets and scenario sets, each set in its own folder for its study [DATA-2];
  scaffolds too, as versioned files [DATA-3]. Scenario sets have versions, guides and provenance;
  studies cite a set as `set@version`, and a set used by a finished study is never changed [DATA-4].
- **Studies, lenses, findings and the paradigm are files in the repo** [DATA-5]: lenses in
  `data/lenses/`, studies in `docs/studies/<id>/study.yaml` so far.
- **Which states are captured:** states after generation starts, not only before it; agent runs
  already capture every target word in the generated text [DATA-6]. Sentence sets will also capture
  named sites in the message (a carrier's words, the end marker), every position of the message
  (opt-in, with the size shown before it starts), and states after generation starts (words in the
  generated text, the answer's first token) [DATA-7].
- **GPU jobs:** captures, agent runs and generation become background jobs, run one at a time
  inside the backend, where the model is already loaded [DATA-8].
- **An agent run's items** each keep the tick's observation as their text; the whole conversation
  is stored once per tick, as the run's token ids, and the system prompt once per run [DATA-9].
- **Each run records** its token ids for each tick, its date, its chat-template hash and its
  model-identity line, so it can be replayed exactly, and its capture recipe: model, format,
  decoding, seed, carrier, token sets, scaffold, intervention [DATA-10].
- **Routing is recorded in full:** all 32 routing weights for each captured token at every layer,
  from which the model's own top-four weights are computed [DATA-11].
- **Leftovers to remove,** with slice 2: a health check reporting on a retired service; seven app
  functions nothing calls and an unused response type; the session-start reminder about temporal
  captures;
  the test lens `lab-k4-n15`; the README's "basin" wording; 13 unused images in `docs/images/`
  [DATA-13].

## The atlas and the paradigm {#atlas}

**The atlas has four catalogues,** each entry with a report written by a Claude agent [ATLAS-1]:
- **nodes:** every node of every validated lens, layer by layer (the first version is built: every
  saved lens version's nodes, with their reports);
- **experts:** all 24 × 32;
- **routes:** pipelines and hubs, built from all four of each token's experts and weighted by the
  model's own weights; the top-1 Sankey stays as one view of them [ATLAS-2];
- **scaffolds:** every analysed scaffold, with its analyses (see
  [interventions](design.md#interventions)) [INT-8].

**Time adds node dynamics:** how long runs stay in a node, what comes before and after it, and what
the model does while in it. Runs that stay several steps show a state the model holds; runs that
cross in one step show a passage [ATLAS-3].

**The paradigm.** Bringing the lenses' findings together into one coherent model is the most
difficult step [ATLAS-4]. The paradigm is the accepted findings: the AI scientists propose findings, attack them
and give evidence; several models vote, and when most agree the finding goes to Andrew for review;
knowledge consolidators extract the insights [ATLAS-5].
- **The findings form a map,** the shape of the coherent model. A finding is a fact about one atlas
  entry, written into its report, or a link between entries. The map lays the accepted links over
  the atlas by the layer where each concept forms, drawn in the Atlas workspace, with the
  consolidators' story over it; contradictions show as clashing links, each one a question for a
  study. Later the map is scored on how well it predicts what a new lens shows, never as a gate
  [ATLAS-6].
- **Every fact and link carries its strength,** one of three: supported; tested and found absent;
  or untestable here [ATLAS-7].
- **The atlas is published** as a static website (entries, reports, figures, the map), with the
  sentence sets, lens directions and summary readings on Hugging Face in formats others can load:
  the project's public record [ATLAS-8].

**The kinds of link** [ATLAS-9], each measured by its own tool (the examples are questions, not
findings):

| Link | Example | Measured by |
|---|---|---|
| overlap | Does the danger lens, read on the animal set, put predators in "dangerous"? | one saved lens reading another lens's data, with presence |
| nesting | Does "dog" sit inside "mammal" inside "animal"? | the levels of the k profile |
| order in depth | Does word sense settle before the scene's threat level? | per-layer held-out scores |
| shared direction | Do one set's threat axis and another's danger axis point the same way? | the angle between two mass-mean axes |
| shared machinery | Do two concepts' tokens take the same pipelines and hubs? | the expert and route catalogues, and fingerprints |
| use in decisions | Does the reading predict the action, and does steering it change the action? | behaviour by reading, and steering a node |
| changes | Does a scaffold make a concept form earlier, or suppress a writing style? | the condition comparison, against neutral texts |
| steers routing | Does the threat axis lie in what the router reads? | the routing effect and router alignment [LENS-35] |

## Interventions and conditions {#interventions}

- **Steering and ablation, with behaviour studies** [INT-1].
- **Steering a node and seeing what changes downstream.** At the steered layer the population lands
  in the other node by construction, so the view shows whether it stays there at later layers or
  drifts back (later layers can undo a push), and what else changes: other lenses, routes and
  behaviour [INT-2]. Before a key finding is accepted, its population is steered this way
  [LENS-33].
- **Scaffolds, and steering from outside and inside the model:** how each changes trajectories
  [INT-3].
- **A condition is whatever differs between runs of the same set:** a scaffold, a steering vector,
  an ablation, an expert mask, another model, a decoding setting, or a change at one tick of a
  branched run. All are compared the same way under one fixed lens (side by side in Watch, as
  averages in Study), and each run records its condition [INT-4].
- **Comparisons are fair** [INT-5]: paired runs that share everything else, so where they part ways
  is itself a result; a same-size control without the content (random directions for steering and
  ablation, random experts for masks, two or three neutral texts of the same length and format for
  scaffolds); and dose, sweeping strength and layer.
- **How interventions are done** [INT-6]: routing drift is always recorded; an option steers only in
  directions the routers don't use; expert masks go through the router's bias, which the 4-bit
  loading path reads on every call.
- **Replications are named as such:** steering where the routers can't see is RARE's method, built
  on Ye, Yuan and Sharkey's split, and switching experts is SteerMoE's; both are cited and first
  reproduced on a published result. For agents, one published gpt-oss result (game probes that stay
  accurate when the agents know they are watched) is replicated as a MUD scenario [INT-7].
- **A catalogue of analysed scaffolds:** what each scaffold changes in each lens's readings and when
  in a run, in routes, and in behaviour (including the style of what the agent writes), each
  measured against its neutral controls; it is the atlas's fourth catalogue, linked by "changes",
  with scaffolds kept as versioned files [INT-8].
- **Another mixture-of-experts model,** for comparison [INT-9].

## User stories {#stories}

How the software is used, one story at a time.

1. **An agent study:** people-assessment scenarios with and without a reveal, as scripted runs;
   Study shows each tick's reading against the bands and the would-be actions; free play shows what
   the agent did with those states [STORY-1].
2. **One run:** sort Study's run list by ticks between the bands and open the top run [STORY-2].
3. **A sentence study:** sentence sequences with a fixed carrier, and references, in Study [STORY-3].
4. **The atlas:** a Claude analyst reads each node's dwell, neighbours and actions, and writes the
   node's report [STORY-4].
5. **Watching live:** `watch agent` in the MUD; in Watch each tick appears once saved [STORY-5].
6. **Steering:** steered and unsteered runs as two conditions on one timeline [STORY-6].
7. **Check the instrument:** reproduce the paper's per-run tank results in Study; every later story
   rests on this one [STORY-7].
8. **Compare the reading methods:** the carrier and the model's own words as two rows [STORY-8].
9. **Follow the reasoning:** open a tick in Watch and see where each lens's reading shifts, sentence
   by sentence [STORY-9].
10. **From a moment to the layers:** click a heatmap cell; the lens panels show that word's path
    [STORY-10].
11. **Hand a study to an analyst:** export its readings and events; a Claude analyst writes the
    report, its numbers re-checked [STORY-11].
12. **Create a new polysemy sentence set in the app,** from the contrast to a saved, validated lens
    [STORY-12].
13. **Find the right k per layer** with the suggestion, the k profile and your own choice
    [STORY-13].
14. **Build a kit for Winter Survival,** checking each lens is validated where it will be read
    [STORY-14].
15. **Visit as a guest:** `connect guest`, then `watch agent` [STORY-15].
16. **Join two lenses:** an overlap link proposed, attacked, voted on and accepted onto the map
    [STORY-16].
17. **Analyse a scaffold:** one scenario set run four ways, paired, from Claude Code [STORY-17].
18. **Check a finding by steering,** with random controls and a sweep of strengths [STORY-18].
19. **Build and test a scenario** in the builder and the simulator [STORY-19].

## Among other work {#related}

Claude surveyed 2025–2026 work and re-read it at the sources; Andrew accepted the survey with
Claude's final read of the design [DOC-17]. What it found:
- **What others have for gpt-oss-20b:** sparse autoencoders for the residual stream at every layer
  (Arditi), browsable on Neuronpedia; routing predicted from those features (RouterInterp); the
  residual stream split into a part the router reads and a part it ignores, with expert routes
  grouping tokens by function (Ye, Yuan and Sharkey); steering by switching experts (SteerMoE) and
  in directions the router can't see (RARE); probes on gpt-oss agents in games, and probe scores
  taken as the maximum over a reasoning trace.
- **Earlier work on the same pictures:** cluster flows across layers drawn as Sankeys (LayerFlow;
  Andrew's own Concept Trajectory Analysis, on GPT-2); per-token probe colouring of transcripts
  (Apollo); agents' beliefs tracked turn by turn against a game's ground truth by asking them
  (MafiaScope).
- **What the survey found nowhere else:** cluster flows and expert routes for the same tokens across
  every layer of a mixture-of-experts model; UMAP lenses validated on held-out scene families and
  compared fairly with raw space; many lenses read at once over every token of an agent's
  reasoning; an agent read tick by tick against staged ground truth, with its routing, in a text
  world; colour blending of label mixtures; a typed map of concept links built by agents who attack
  and vote, with every cited number re-computed.
- **So:** distinctive as a combination. The field moves fast, so getting results out early matters
  as much as the design.

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
[MafiaScope](https://arxiv.org/abs/2607.10645)

## Open questions {#open-questions}

**Settled by experiment** [TIME-17, LENS-9]:
- How early and how accurately do the output reading, the scan and the carriers track a
  scenario's labels, tick by tick? This is the first agent experiment.
- Which reading mode works at keywords: a single token, a token collection or a scan?
- What neutral text should the scan compare against, and should it be per token or per kind of
  token?
- How is presence best measured, and does it separate absent from unresolved? First on planted
  synthetic states, then on runs.
- Does a lens still read the same way as ticks accumulate?
- Can free-play runs be compared with references at equal context length?
- Does a carrier work better as a user's question, or as the opening of the model's reasoning?
- Are there better automatic methods for choosing k?

More questions will come; the design stays flexible [TIME-17].

**Andrew's ideas, not yet decided:**
- a user interface in the MUD [MUD-9];
- giving the agent words marked as for measurement only [TIME-12];
- running agents in scenarios, alone or with people taking part, as the MUD's first job [MUD-2];
- controls that fold, and doing some of the work from the MUD [APP-3];
- letting users choose the LLM for Claude agents' work [GOAL-12].

## Requirements {#requirements}

Every requirement, by area, from `docs/design/requirements.yaml`. On the page the list is drawn
here, with each requirement's status and whether it is built.

<!-- requirements -->

## Rejected and retired {#retired}

What the design replaced, and with what:
- **The animal set's framing** as a contest between kinship and way of life, replaced by many ways
  of organizing animals and the ontology [SET-11].
- **One design document, with planned work in Claude Code's plan file,** replaced by the two
  documents and the plan in the plan-and-architecture document [ORDER-17].
- **The basin-era tools:** the temporal panel and its endpoints, the old sequence-capture route,
  the `/temporal` skill and the raw-axis endpoint, replaced by Study's timelines, Watch and saved
  mass-mean lenses [DATA-12]. The word "basin" for a lens's cluster gave way to "node".
- **The old view's four fixed six-layer windows,** whose edges cut flows, replaced by the all-layer
  view [APP-18].
- **A plain share of an axis in what the router reads,** which a random direction matches, replaced
  by the routing effect and router alignment [LENS-35].
- **Reading single words at the token after them** (proposed 2026-10-09 to remove the gap between
  one-token and split names): tested the same day and withdrawn, since it kept the gap and carried
  much less of the word [SET-6].
- **The old prototype MUD,** retired once everything worked in the new one [MUD-22].
- **Layers' report cards as a requirement of their own:** the same cards are LLM analysis's
  requirement for Layers, so the duplicate was retired [APP-33].
- **Building the first four method changes with slice 2** (Claude's timing, 2026-10-11): replaced
  when Andrew moved them ahead, to be built while the machine is shared with other work
  [LENS-26, ORDER-20].
- **Attention's first proposal** (Claude's, 2026-10-19): a row of the words each item drew on,
  the words for the split card's analyst, recurring words, the words that pushed toward an
  expert, and the word-by-word parts recorded during capture. Withdrawn by Claude on 2026-10-20,
  after Andrew's questions and the tests, in favour of a lens on what attention writes and brought
  by attention; L35.4 asks Andrew whether any part should come back
  [LENS-51 to LENS-53, APP-36, DATA-14].
- **Marking who wrote a split where both directions agree** (Claude's proposal, 2026-10-16):
  replaced by keeping the shares off the node card for now, as Andrew decided (L33)
  [LENS-47, LENS-48].

## Terms {#terms}

| Term | Meaning |
|---|---|
| **gpt-oss-20b** | the model studied: a mixture-of-experts (MoE) model with 24 layers |
| **token** | a piece of text the model reads as one unit: a word, part of a word or a mark |
| **layer** | one of the model's 24 processing steps; each reads every token's state and changes it. Charts write layers as L0 to L23 |
| **depth** | position among the layers, from L0 to L23; not time |
| **expert** | one of the 32 sub-networks in each layer; each token is sent to 4 of them |
| **attention** | the other step in each layer: it brings information from earlier tokens (and the token itself) into a token's state |
| **attention's write** | what attention adds to a token's state at one layer: the layer's output minus its input minus the experts' write. The experts' write is what the four experts add |
| **head** | one of attention's 64 parallel readers in each layer, each with its own weights over the earlier tokens |
| **sink** | a head's place to put weight on no token at all; gpt-oss learns one for each head |
| **expert route** | the experts a token is sent to, layer by layer: four in each layer, whose weights add up to 1. "Top-1" is the expert with the highest weight |
| **route** | a token's path through a lens's nodes, layer by layer |
| **pipeline** | a sequence of experts that many tokens follow through consecutive layers (the app's tab says "pipes") |
| **hub** | an expert that many different routes pass through |
| **expert fingerprint** | a 24 × 32 grid of how much weight each expert gets at each layer, for one population of tokens |
| **residual stream** | a token's state at a layer: 2,880 numbers that each layer reads and adds to |
| **neuron** | one of those 2,880 numbers |
| **agent** | gpt-oss-20b playing scenarios in the MUD |
| **Claude agent** | an LLM run that writes or analyses: an analyst, an AI scientist, an author; by default Claude, run with `claude -p` |
| **sentence set** | sentences written to vary some properties on purpose and hold the rest fixed. Older documents call it a probe set |
| **linear probe** | a simple classifier trained on the states to read a property; the ceiling the lenses are compared with |
| **designed axis** | a property a sentence set or scenario set varies on purpose, such as the sense of "tank" |
| **target word** | the word a sentence set is captured at |
| **carrier** | a fixed sentence containing the target word, added after a context so the word is read the same way every time |
| **site** | the one token a reading is taken at |
| **token count** | how many tokens a word splits into; a word that splits is read at its last token |
| **scene family** | items that share one setting; held-out tests leave whole families out |
| **held out** | kept out of a lens's fitting and used only to test it |
| **population** | a group of tokens or items read together, such as a node's members |
| **capture** | the model's stored states for a sentence set or a run: residual stream, expert outputs and routing |
| **session** | one capture in the data lake |
| **schema** | a saved clustering made before lenses existed; still readable |
| **grouping** | a way to divide items into clusters, in UMAP space or in raw space |
| **lens** | a saved, validated way to read states at one site, of one of two kinds |
| **UMAP** | a method that maps high-dimensional states to a few dimensions while keeping near neighbours near |
| **UMAP lens** | a lens that projects each layer's states with UMAP and clusters them |
| **Ward** | the clustering method the lenses use: it merges the closest groups step by step, so any number of clusters is a cut |
| **k** | the number of clusters at a layer |
| **PCA** | principal component analysis: the directions along which the states vary most |
| **AMI** | adjusted mutual information: how well the clusters match the designed classes, beyond chance (0 is chance, 1 is a perfect match) |
| **κ (kappa)** | agreement between predicted and true classes, beyond chance |
| **decoy** | a made-up axis with random values, used to set the level a score must beat |
| **Sankey** | a flow chart: at each layer a column of nodes, and bands showing how many items move between nodes |
| **node** | one cluster of a UMAP lens, at one layer |
| **split point, branch, edge** | an edge is one band of a Sankey, between a node and a node of the next layer; a split point is a node whose items go on to two nodes or more at the next layer, and each edge leaving it is a branch |
| **expert node** | the tokens sent to one expert at one layer and rank: a node of the expert Sankey |
| **brought by attention** | an item whose expert at a layer would be another without what attention added to that item in particular at that layer |
| **mass-mean lens** | a lens that is one axis per layer, from one class's average state to the other's |
| **class** | one of the categories a lens separates |
| **reading** | what a lens gives for one state: a node, or a position on the axis (the class averages sit at −1 and +1) |
| **lens kit** | the lenses chosen for a scenario set |
| **keyword** | a word from the scenario's MUD commands at which a kit lens is read in the agent's output |
| **scan** | reading every token of a text through a lens, each compared with how the same token reads in neutral text |
| **lens catalogue** | the validated lenses built so far, starting with about twelve |
| **scenario** | a situation the agent plays in the MUD |
| **staged scenario** | a scenario of multiple-choice stages, with known labels at each stage |
| **world** | a free-form scenario with its own engine; Winter Survival is the first |
| **mini-world** | a starting situation played on a world's engine, with exit conditions |
| **scenario set** | scenarios designed together for a study, versioned, in the scenario library |
| **run** | one agent playing scenarios, or one sequence of sentences in a sentence study |
| **tick** | one agent turn: an observation, the model's reasoning, its action |
| **output, action** | the final text the model writes in a tick, which the runner sends to the MUD as its command |
| **reasoning stream** | the model's own reasoning text in a tick (gpt-oss's analysis channel) |
| **runner** | the backend's agent loop: it plays the model through scenarios in the MUD and captures its states |
| **ordering** | what a sequence of readings steps through: context steps, ticks, or reasoning steps inside one tick |
| **scaffold** | text that guides how the agent reasons, such as a system prompt, a persona or a planning prompt |
| **steering** | adding a direction to the model's states during a run, to push them toward a class |
| **ablation** | removing a direction from the model's states, to see what depends on it |
| **condition** | whatever differs between runs of the same set |
| **references** | runs whose label never changes, read with the same lens, showing where each class's readings sit at each point |
| **band** | the range holding most of one class's reference readings at one point |
| **presence** | whether a lens's concept is represented in a state at all |
| **position** | which class a reading leans to, and how far |
| **scripted run** | an agent run whose actions follow a fixed script |
| **free play** | an agent run in which the model chooses its own actions |
| **would-be action** | in a scripted run, the action the model writes at a tick: recorded, not played |
| **study** | a research question with its sets, runs, lenses, analyses and findings, kept as files in the repo |
| **ledger** | a study's list of ideas, each with its experiment and finding |
| **showcase** | a short published page and figure showing what a slice made possible |
| **phase, slice** | a phase is one unit of planned work in the plan-and-architecture document; a slice is a phase that adds a usable piece of the software and ends with a showcase |
| **atlas** | catalogues of nodes, experts, routes and analysed scaffolds, each entry with a written report |
| **paradigm** | the accepted findings, drawn as a map |
| **room** | one of the app's places, each with its own colours and tools; Claude proposes a room of the same name in the MUD for each |
| **requirement** | one numbered decision, idea, view, proposal or open question in `docs/design/requirements.yaml` |
| **the two documents** | this design-and-requirements document and the plan-and-architecture document |
| **the paper** | Andrew's context-shift paper (`docs/studies/context_shift/`) |
| **Scaffold Dynamics** | the MUD's name |
| **the institute** | the MUD's own rooms (the hub, the labs and the simulator), as distinct from its scenarios |
| **MUD** | a text world played by typing commands; here it runs on Evennia, a Python framework for such worlds |
| **subagent** | a helper agent that Claude Code starts on its own during a conversation |
| **`claude -p`** | Claude Code run from a script, without a conversation: how Claude agents run |
| **Docker** | a tool that runs a program in its own container, with everything it needs |
| **FastAPI, React** | the backend's web framework (Python) and the app's interface library (TypeScript) |
| **GPU** | the graphics card the model runs on |
| **repo, git** | the project's files under version control (git), published on GitHub |
| **localhost** | the user's own computer, as a network address |
| **WSL** | Windows Subsystem for Linux, where the project runs on Andrew's Windows machine |
| **hash** | a short fingerprint of a file's contents, which changes if the file changes |

## Changelog {#changelog}

- **2026-10-07:** the design drafted from Andrew's own words as `docs/DESIGN.md`, reviewed with him
  part by part.
- **2026-10-08:** approved, with Claude's final read accepted and its recommendations written in.
- **2026-10-08 to 2026-10-11:** slices 1b and 1c added, and Andrew's form answers (L16 to L29)
  written in.
- **2026-10-11:** this document drafted from the requirements list, with the rooms proposed (L30);
  checked by three independent audits and two readability reviews before Andrew's first read, and
  their fixes applied.
- **2026-10-16:** the four method changes and the attention-and-experts shares moved ahead in the
  order of work; the attention-and-experts study done, and how the node card reads its shares put
  to Andrew (L33).
- **2026-10-18:** Andrew's layout for the institute (L30) written in, with Claude's rooms revised
  around it and four follow-up questions (L34); L33 rewritten after his questions about attention,
  with Claude's recommendation changed.
- **2026-10-19:** Andrew's decisions and question on attention written in, with Claude's proposal
  for it in seven parts (L35), tested first without the model.
- **2026-10-20:** Andrew's answers written in: who writes each split stays off the node card (L33);
  the rooms approved, with the departments' studies, the meeting room's purposes and the stages
  (L34); a robot, polishing passes with a map, and as ideas out-of-service stairs and characters for
  the non-player characters (his note on L31), with Claude's first map of the institute; Winter
  Survival after OpenLLMRI's roadmap (L36); the superseded documents archived (L32). Attention in
  the analysis reworked after his notes and a held-out test of a lens on attention's write, with
  four new cards (L35.1 to L35.4); his attention Sankey over the population recorded as an idea
  [LENS-57]; Claude's first attention proposal withdrawn. The four tuned lenses scored again on
  five test draws, the last of the re-scoring after the method changes [LENS-21].
- **2026-10-22:** Andrew's answers to L38 and L37 written in: the new app's plan approved and
  started; the greeter an AI with a form; the stairs to a closed floor; the polishing passes from
  Claude's first map, whose layout file and map are built; Winter Survival after slice 6. The study
  of whether the UMAP lens beats raw space set aside [ORDER-23].
- **2026-10-24:** the second polishing pass: Andrew's rules for the layout written in (one floor
  preferred, two at most; today's rooms kept; the public rooms by the entrance), with Claude's four
  drafts and suggested rooms.
- **2026-10-27:** the floor plan approved after Andrew's corrections: the scaffold studio kept and
  the other suggested rooms dropped (the calibration lab folded into the lens workshop by Claude),
  the simulator folded into the simulation rooms, the library for our papers at the front, the
  departments together along the back.

## Decision log {#decision-log}

Every decision, by date, paraphrased. Each requirement holds its own date and source.
- **2026-10-04:**
  - one repo and one MUD [MUD-1], with the institute's rooms [MUD-11];
  - the goal and its tools [GOAL-1, GOAL-2];
  - the AI scientists designing sets and scenarios, in teams, with a voted paradigm
    [GOAL-7, ATLAS-5];
  - clustering from the polysemy lab [APP-21]; an app that takes commands [APP-34];
  - later, an Ideas workspace, with an existing idea-tracking engine moving in [APP-8];
  - replaying runs in a scenario room [MUD-8]; a Mudlet package later [GOAL-9];
  - the lake not copied wholesale [DATA-1]; the neurons behind clusters [LENS-29].
- **2026-10-06:**
  - the research-software review before the pilot, and the lens catalogue first
    [ORDER-16, GOAL-13];
  - records as files in the repo [DATA-5];
  - the two instruments, a lens as a model, UMAP preferred once it holds up
    [PRIN-2, PRIN-6, PRIN-5];
  - three reading modes [LENS-42]; Sankeys from both instruments compared [LENS-14];
  - k per layer [LENS-2]; raw-space groupings [LENS-4]; more visual channels [APP-22];
  - always MoE, and LLM analysts [PRIN-10, PRIN-11];
  - the atlas and the paradigm [ATLAS-1]; lens kits and people assessment [LENS-37, LENS-38];
  - what comes with each split [LENS-30, LENS-31, LENS-32, LENS-33];
  - friend/foe v3 after the lens core, and the lens core before the pilot [ORDER-3, ORDER-9];
  - the six kept sessions [DATA-1]; the polysemy lab's clustering [MUD-11];
  - the names Winter Survival and Scaffold Dynamics [MUD-21];
  - datasets never written by subagents [SET-28].
- **2026-10-07:**
  - the goal restated, with monitoring agents as what the paradigm makes possible [GOAL-1, GOAL-3];
  - the in-between-state question belonging to the context-shift study [TIME-16];
  - researchers connecting by default to Scaffold Dynamics [GOAL-8];
  - Claude agents run by the backend [GOAL-11];
  - the principles [PRIN-1 to PRIN-16];
  - every lens with an agreed report [LENS-43]; the coherent model as the hard part [ATLAS-4];
  - the old prototype retired [MUD-22];
  - the clustering form, and k by hand or automatically [ORDER-4, LENS-7];
  - a UX pass [ORDER-18]; the builders [BUILD-6, BUILD-7];
  - one design document with a web view [ORDER-17];
  - the time design: the orderings, the rules, the output reading, the scan, carriers, presence
    and position, references [TIME-1, TIME-3 to TIME-6, TIME-8, TIME-13 to TIME-15];
  - kits per scenario set [LENS-37]; building lenses separate from using them [LENS-1];
  - design approved before building [PRIN-15]; researchers' rooms [MUD-13];
  - one run per set [SET-27];
  - the details of lenses, validation and comparison
    [LENS-5 to LENS-8, LENS-10, LENS-11, LENS-15, LENS-16];
  - LLM analysis wherever it helps [LLM-1, LLM-2, LLM-5 to LLM-16];
  - runs started in the MUD or through Claude Code [MUD-15];
  - the workspaces and screen rules [APP-7, APP-9 to APP-17], Watch
    [WATCH-1 to WATCH-7, WATCH-9 to WATCH-15] and Layers [APP-18, APP-23];
  - expert weights as the model's own [APP-19]; the retirements [DATA-12];
  - the atlas's node dynamics and map [ATLAS-3, ATLAS-6, ATLAS-9];
  - conditions, fair comparisons and interventions [INT-2, INT-4 to INT-6, INT-8];
  - the stories [STORY-1 to STORY-19]; the order of work [ORDER-1], with slice 4's contents
    [ORDER-10].
- **2026-10-08:**
  - Claude's final read accepted, its recommendations adopted, the name kept [DOC-17];
  - colour that reads true, fingerprints, one expert layout, marked disagreements, the 3-D fix
    [APP-24 to APP-28]; depth heatmaps and a temporal Sankey [APP-32, STUDY-6]; figure recipes
    [APP-17];
  - a published atlas, with a strength on every finding [ATLAS-8, ATLAS-7];
  - a showcase per slice [ORDER-2]; the starter lens catalogue [GOAL-15];
  - the analyst tests and a budget for reports [LLM-3, LLM-4];
  - how each lens bears on routing [LENS-35]; the nearest published features [LENS-36];
  - held-out sentences as the judge of a lens's reading of new data [LENS-46];
  - replications named [INT-7]; alerts judged per run [WATCH-12]; branching a run [WATCH-8];
  - hosting before others are invited [MUD-20];
  - slice 1b: tuned lenses, reports on experts, pipelines and hubs, single words, the axes
    analysis, the 3-D view in the lens's own space, lit paths
    [ORDER-3, LENS-12, LENS-17, LENS-44, SET-8, LENS-45, APP-29, APP-30].
- **2026-10-09:** slice 1c: the animal and object sets [SET-9, SET-10, SET-23]; words that split,
  read at their last token [SET-4]; tuning by hand [LENS-18]; a studies area [STUDY-2].
- **2026-10-10:**
  - the app rebuilt, more of it visual [APP-1, APP-2];
  - reasoning streams analysed before any chosen words [TIME-9, TIME-11];
  - two documents, each consistent throughout [DOC-2]; questions as forms [DOC-12].
- **2026-10-11:**
  - the two documents in the repo: their shape, requirements first, the plan in the
    plan-and-architecture document, and the checks before Andrew reads [DOC-2, DOC-4 to DOC-10];
  - the order of work [ORDER-5, APP-5]; rooms [APP-4]; the studies room first [STUDY-2, STUDY-3];
  - one builder, open to experiment for scenarios, with teams for sets [BUILD-1 to BUILD-4];
  - people with agents chosen per scenario [MUD-3];
  - the animal ontology [SET-12 to SET-17];
  - slice 1c's details kept:
    - the sets [SET-5, SET-6, SET-18, SET-20 to SET-22, SET-24, SET-25];
    - honest hand tuning and the hold-out record [LENS-19, LENS-20];
    - the builder's extras [BUILD-8 to BUILD-12];
  - five method changes [LENS-21 to LENS-25];
  - the decisions for capture and jobs [DATA-7 to DATA-9, DATA-13, MUD-19].
- **2026-10-16:**
  - while Andrew uses the machine for other work, the four method changes and the
    attention-and-experts shares move ahead in the order, since neither needs the model [ORDER-20].
- **2026-10-18:** the institute's layout (L30): an AI greeting users and guests, public simulation
  rooms and one in every lab, four departments (also called labs) with their AI scientists, a
  lounge, a meeting room for different AIs, and in the long run an institute the AI scientists
  design themselves [MUD-23 to MUD-28].
- **2026-10-19:** attention joins the analysis as more information, with a row for its
  visualization below the Sankeys and the 3-D view [LENS-49, APP-35].
- **2026-10-20:**
  - who writes each split stays off the node card, its code kept on a git branch [LENS-48];
  - the rooms as Claude proposed them, the tools shared by every department, which department
    holds each study, and the stages they are built in [ROOM-1, ROOM-15, ROOM-17, ROOM-18]; what
    the meeting room is for [MUD-27];
  - a robot, and a couple of polishing passes with a map before building begins, then iterations
    on the room descriptions [MUD-29, ROOM-19]; as ideas, perhaps out-of-service stairs, and
    characters for the non-player characters [MUD-30, MUD-31];
  - Winter Survival waits for OpenLLMRI's roadmap [ORDER-22]; the superseded documents are archived
    [DOC-19].
- **2026-10-22:**
  - the new app's plan approved and started at once, the documents' review going on alongside
    [ORDER-24]; the layout as data, and characters for the non-player characters with the new app
    [ROOM-16, MUD-31];
  - the greeter is an AI with a form, not called a robot; the out-of-service stairs lead to a closed
    floor; the polishing passes start from Claude's first map [MUD-29, MUD-30, ROOM-19];
  - Winter Survival after slice 6, which Andrew left to Claude [ORDER-22]; the study of whether the
    UMAP lens beats raw space set aside until later in the order of work [ORDER-23].
- **2026-10-24:**
  - the institute on a single floor for the time being, two at most [ROOM-20];
  - today's rooms kept, the polysemy lab its own room [ROOM-21];
  - the simulation rooms and the public rooms near the entrance, the rest as Claude thinks best
    [ROOM-22];
  - four drafts for the second pass, with Claude's suggested rooms for Andrew to veto [ROOM-23].
- **2026-10-27:**
  - the floor plan, on one floor, with the stairs kept [ROOM-25, ROOM-20];
  - capturing and steering are tools used in the rooms, not rooms of their own; no hallways
    turned into rooms; the scaffold studio kept [ROOM-26];
  - the library holds the papers and articles we write [ROOM-5];
  - the public simulation rooms together and the same size; the simulator's jobs go to the
    simulation rooms [ROOM-22, ROOM-21].
