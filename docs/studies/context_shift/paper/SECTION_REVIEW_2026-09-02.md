# Section-by-section review of the paper draft (2 September 2026)

Read fresh, in order, from the current files. For each section: what it says, why it
is in the paper, and how well it is organized and worded. Nothing in the paper was
changed while writing this.

## Overall impression

The argument is sound and the numbers are unusually well checked. The problems are in
how the paper explains itself. The document does not build understanding in order:
terms appear before the reader has a picture of them, results paragraphs carry several
findings at once, the discussion presents three competing explanations in one block,
and the methods section, though now complete, reads like a specification rather than
an explanation. A reader who knows the mathematics can verify each sentence but cannot
easily hold the whole argument in their head. The fixes are mostly reordering and
splitting, not rewriting from scratch. Details follow.

## Title, epigraph, and abstract

**What it says.** The title names the phenomenon (semantic metastability), the
condition (context shift), and the verdict (unresolved). The epigraph is the tank joke.
The abstract opens with the question, gives the setup in two sentences (the model, two
tasks, forty-sentence contexts that switch sides halfway, matched references), then
tells the findings in order: the reading follows the shift only partway and leaves a
remnant; one direction dwells between interpretations; runs move by drift plus jumps;
order effects are explained by recency weighting; nothing is geometrically unusual, but
a signal of mixed context is present and unused by behavior. It names the cluster, then
closes with behavior and safety: the model never asks which meaning is meant, the
safeguarded task stays safe, the unsafeguarded one commits silently, and safe responses
fall from 91% to 50% as the reading moves toward the fictional frame.

**Why it matters.** Most readers read only this. It has to carry the question, the
result, and the stakes.

**Organization and wording.** This now reads well: three short paragraphs, one idea
per sentence. Two small things remain. "Safe-completion" is used as a noun before
anyone has defined it; "safe responses" would do the same work with no new term. And
the epigraph sits between the title and the abstract with no connection to either
until the second paragraph of the introduction; in print that is fine, on a web page
the joke can look like decoration. Consider a one-line footnote on the epigraph, or
leave it and trust the introduction.

## 1. Introduction

**What it says.** Paragraph one sets the stakes: models rarely say when the words in
front of them have not settled into one reading, safety rules assume a resolved fact,
and the paper measures the unresolved stretch directly. Paragraph two gives the origin
in humor theory: incongruity and resolution, garden path versus pun, the tank joke, and
the claim that this shift is now measurable inside a model. Paragraph three gives the
origin of the second task, the Raine case, with careful attribution, and turns it into
the scientific question. Paragraph four sets up the three candidate answers (a learned
state, a passage, or somewhere off the learned distribution) and hints that the first
two may not be distinct. Paragraph five describes the design in five sentences and
points to the central figure. The contributions follow as a numbered list.

**Why it matters.** It gives the reader the question, the stakes, and the three-way
frame that the results and discussion later resolve.

**Organization and wording.** The strongest section as prose. Three issues. First, the
order. A reader who came for the safety question meets Dynel and the joke before the
incident that motivates the study. Either move the humor paragraph after the incident
paragraph, or cut it to three sentences and let the epigraph carry the flavor. Second,
paragraph four ends by promising that "the three-worlds taxonomy itself" is unresolved.
That phrase means nothing until section 4. Say plainly what will be argued: the states
we found look like a learned state and like a passage at the same time, so those two
worlds are not separate. Third, contribution 5 ends with "the metastability lives in
the path, not the equilibrium." That is a conclusion from section 3.5 stated before the
reader knows what an equilibrium map is. Cut the clause and let 3.5 draw the moral.
Small: "a reading in transit" is a good phrase; the unresolved zone is defined where it
is first used, which is right.

## 2. Methods

**What it says.** 2.1: the model, its stock configuration, deterministic forward
passes, capture of the full residual stream at every layer; the definition of a site
and a reading; the two sites used. 2.2: the two tasks and their carriers; the eight
corpora with their counts; how sentences were written (language-model agents under a
blind protocol); a vocabulary paragraph defining run, cell, scene family, and
scene-held-out. 2.3: the axis (difference of class means), the projection formula, why
not a trained probe, the accuracy rule, the seven-rule protocol in Box 1, and a
glossary. 2.4: the four trajectory models and how they are chosen, the remnant gap,
the bootstrap, and behavior categorization. 2.5: reproducibility.

**Why it matters.** The reader has to be able to picture what a reading is and what
each later number measures. The section also carries the paper's methodological
contribution: the two instrument artifacts and the protocol that handles them.

**Organization and wording.** Complete, but in the wrong order for a reader. The eight
corpora arrive in 2.2, with counts, before the reader knows what a reading is (2.3) or
why any corpus exists. A better order: model and capture; the instrument (axis,
formula, accuracy rule); the tasks and corpora, each corpus introduced with the
question it answers; the protocol (Box 1); analysis methods; reproducibility.

Specific problems:

- 2.2 still contains "the transition corpus (D3)", "no-shift arms (D4)", and "the
  reference ruler". The codenames, the word arm, and the metaphor all survived the
  cleanup. These should be "the transition runs", "the no-shift control runs", and
  "the reference".
- The vocabulary paragraph is a definition list squeezed into prose. Make it a list.
- Box 1 is the heart of the method, but rules 1, 5, 6, and 7 state the rule without
  saying in plain words what goes wrong if you break it. Rules 3 and 4 do this well;
  match them.
- Rule 3's arithmetic ("half the class separation on an axis whose class means sit at
  ±1") is hard to follow. Say: an offset as large as half the distance between the two
  classes.
- The trajectory-models paragraph in 2.4 is one long chain of semicolons. One sentence
  per model.
- The glossary does not define "dwelling", which the paper uses everywhere. Add it.

## 3. Results

**Missing at the top.** There is no opening paragraph. Six subsections follow with no
statement of what they do or in what order. Add four or five sentences: first we check
the instrument (3.1); then we follow a reading through a shift, asking how far it moves
(3.2), what kind of process moves it (3.3), and what the model does while between
interpretations (3.4); then two boundary tests, whether order adds anything beyond
recency (3.5) and whether any of these states leaves the model's ordinary geometry
(3.6).

### 3.1 The instrument reads a real contrast

**What it says.** The axes separate the two classes (held-out accuracy 0.905 and
0.910 for single sentences; 0.93 to 1.00 on accumulated contexts at every layer).
Three lines of evidence show the axis reads sense or framing rather than topic: with
token identity held fixed, the signal concentrates at the sense-bearing token; minimal
pairs that differ only in framing cues move the reading by half the class separation;
and the effect does not grow with the number of cue words. The claim licensed is
modest: the reading tracks framing cues with content held fixed. The tank signal sits
at one token; the fiction/real signal is spread across the request.

**Why it matters.** Without it, every later number could be a topic artifact.

**Organization and wording.** Logically ordered and mostly readable. The minimal-pairs
sentence carries five statistics in one parenthesis; keep +0.99 and 95% in the prose
and move the test details to the figure caption. The symbol d′ appears with no gloss;
one clause ("a standard separation measure") is enough. The closing contrast between a
token-anchored and an utterance-wide signal is a good ending.

### 3.2 The shape of reinterpretation

**What it says.** Both directions in both tasks cross the midpoint after a median of
four to ten sentences and never reach the opposite reference. The fitted decay
parameters give evidence ages of about nine and fourteen sentences, and near-uniform
weighting in the dwelling direction. Across depth, the shallow fiction/real layers
cross fast and completely while tank is slower everywhere; where the layers end up,
fiction/real's middle layers settle partway and tank's middle and deep layers end at
the midpoint. No single recency-weighted average fits the transition; the late
shortfall is the remnant gap, positive in all four cases, with the tank-to-vehicle
plateau at the midpoint itself. One case demotes under a stricter bootstrap; the gap
is not explained by weaker material; permanent versus slow is undecidable here. The
asymmetry between directions replicates under a second carrier and has a candidate
cause in class breadth.

**Why it matters.** This is the central finding: how far a reading follows a shift and
what remains.

**Organization and wording.** Still the hardest section to read, and the order is the
reason. It goes: figure, then the decay-parameter discussion, then depth crossing,
then depth endpoints, then the two-phase claim and the remnant gap, then the checks,
then the asymmetry. The reader meets the fitted-decay material and the entire depth
story before the section's main quantity, the remnant gap, is defined. Reorder: what
the figure shows; how far and how fast (crossing); the remnant gap and its four values;
the three checks; the comparison with evidence integration and the decay parameters;
depth; asymmetry. The two depth paragraphs carry about twenty numbers. Most belong in
the figure caption or a small table; the prose needs three: the shallow fiction/real
layers cross in three or four sentences and completely, tank's middle and deep layers
end at the midpoint, and the deepest layers hover in one direction of each task. The
heading is right.

### 3.3 The form of the dynamics

**What it says.** Four model forms are fit to each run; the selector was calibrated on
synthetic runs so it cannot produce a drift-plus-jump verdict from smooth truth. On
real runs, drift plus jump dominates among runs where selection is decisive; the
two-timescale model wins none. Jumps are not timed by evidence strength. Inside the
context, the post-shift sentences' own tokens read at about half their reference.

**Why it matters.** It rules out the default explanation, smooth integration of
evidence, and establishes discrete changes in the reading.

**Organization and wording.** Well argued, but the first paragraph gives the
calibration statistics before the reader knows why they would care. State the
conclusion first (no smooth model fits, and here is how we made sure the selector
cannot fake that), then the numbers. "Hybrid" is used as a label before it is
introduced as the name for drift plus step; say it once. The last paragraph, on
tokens inside the context, is a different topic from the rest of the section and
arrives without a sentence saying why it is here; give it a topic sentence or its own
short subsection.

### 3.4 Unresolved states and behavior

**What it says.** In one tank direction the reading becomes stationary between the
two interpretations for at least ten steps, as a single population; the same signature
appears at a second tank site and under the replicate carrier, and at one fiction/real
site with four runs per direction. Behavior tracks the reading: side readings answer
with that side's sense, middle readings answer with both senses about half the time.
Not one of 96 completions asks which sense is meant. At matched context composition
the reading carries some extra information mid-transition (graded suggestive). In the
fiction/real task, safe responses run 50%, 80%, 91% across the three bands. An
exploratory check finds no layer whose reading tracks behavior better than the
calibrated site's.

**Why it matters.** It connects internal readings to what the model actually does,
and carries the two facts the safety argument rests on: the model never asks, and the
safe-response rate follows the reading.

**Organization and wording.** Two subjects share one subsection: the dwell, and
behavior. Split them (3.4 the dwell, 3.5 behavior) and renumber. The dwell paragraph
is dense but correct; "the central tendency of the run distribution" should be "the
typical run". The behavior paragraphs are now in a sensible order. "Safe-completion"
is finally defined here, after the abstract and introduction have already used it.

### 3.5 Order and equilibrium

**What it says.** Static mixtures of the two classes, read in two orders, show large
hysteresis loops. A recency-weighted average fitted to the same data reproduces the
loops almost exactly, so there is no excess stickiness. The two orders prefer slightly
different decay parameters. This reconciles 3.3 and 3.5: the equilibrium map is
smooth, the path through a transition is not.

**Why it matters.** It removes the sticky-memory explanation and sharpens what
metastability means here: a property of paths, not of equilibria.

**Organization and wording.** The clearest results subsection: a question, a test, a
reserved question, an answer, and a reconciliation. Keep it as the model for the
others. One nit: "loop area" needs a clause of definition (the area between the two
branches).

### 3.6 The geometry of irresolution

**What it says.** With reference, measure, and noise level fixed, no individual state
leaves the reference distribution; the pre-registered prediction that jump steps would
failed. The mean displacement of transition states, however, is far outside the null:
a shared component of 25% and 38% of the class separation, orthogonal to the class
axis, surviving held-out estimation, and not explained by unfamiliar families. It
marks mixed context, partly the blocked structure of the shift in fiction/real, and
does not predict behavior at the site tested. Whether it is a learned representation
is left open. Three senses of off-distribution are distinguished; these shifts are the
tamest case.

**Why it matters.** It settles the third candidate world and produces the marker.

**Organization and wording.** Good order: setup, per-state null, the mean signal,
what it is, scope. The sentence stating that paired values are tank first then
fiction/real is exactly the kind of help the other sections lack. The orthogonality and
novelty sentences are dense with cosines and percentages that could move to the
caption.

## 4. Discussion

**What it says.** Ten bold-headed paragraphs: what "metastable" means here (anchored
in neuroscience, a property of paths, not bistability); the human parallel
(good-enough sentence processing); safety stated descriptively; the interpretation
that the two tasks differ in whether they carry a trained default; two further
candidate explanations for why the safeguard held (deeper layers settle; a safeguard
that reads shallow layers), with none of the three causally established; a monitor
calibration (AUC 0.61); garden path versus pun; typicality versus commitment; the
signal behavior does not use, with the parallel to the hallucination literature and to
the motivating case; and a closing.

**Why it matters.** It says what the findings mean, what they do not mean, and what
they suggest for alignment work.

**Organization and wording.** Each paragraph is now fine on its own. The section as a
whole has no spine: term, human parallel, safety, interpretation, jokes, typicality,
signal, close, in an order the reader cannot predict. Group it. First, what we found:
the definition of metastability and the typicality-versus-commitment point belong
together. Second, what it means for safety: the descriptive paragraph, the trained
default, the three candidate accounts, the monitor calibration, and the unused signal,
in that order. Third, connections: the human parallel and garden path versus pun.
Then the closing. The three-candidate paragraph is still the longest in the paper; it
needs a first sentence that says "three accounts could explain why the safeguard held,
and we cannot yet separate them", then one short paragraph per account. The heading
"Then the interpretation, with its caveat stated first" describes the paragraph's
rhetoric, not its content; name what it says, for example "A trained default for
unresolved cases?".

## 5. Limitations and future work

**What it says.** One model, one site and layer per task, internal replication only;
what did not replicate cleanly; the named open question (permanent versus slow) and
the two experiments that would settle it; a list of deferred work; the note that
analyses were frozen before drafting.

**Why it matters.** It states the scope honestly and tells the next person what to
run.

**Organization and wording.** Clear and in the right order. The first sentence stacks
the single-layer limitation onto the one-model limitation with a dash; split it. The
deferred-work paragraph is a seven-item semicolon sentence; make it a list.

## Back matter

The related-work section is still a list of anchors and must be drafted into prose
before submission. Appendix A is now short and factual. The terminology map for
repository readers is useful. The acknowledgments line is still a placeholder.

## Across the document

The five changes that would do the most for a reader, in order:

1. Add a roadmap paragraph at the start of Results, and open each results subsection
   with one sentence that connects it to the previous one (3.5 already does this).
2. Reorder 3.2 so the remnant gap comes before the decay parameters and the depth
   material.
3. Reorder Methods so the instrument comes before the corpora, and introduce each
   corpus with the question it answers.
4. Group the Discussion into what we found, what it means for safety, connections,
   and closing; split the three-candidate paragraph.
5. Move most of the numbers in 3.2 and 3.6 into captions or two small tables (the
   four remnant gaps with their intervals; the depth bands), leaving in prose only the
   values the argument turns on.

Smaller items: define "dwelling" in the glossary; say "safe responses" in the abstract;
introduce "hybrid" once; split 3.4 into dwell and behavior; remove the leftover D3, D4,
arms, and ruler from 2.2; convert the vocabulary paragraph and the deferred-work
paragraph into lists.
