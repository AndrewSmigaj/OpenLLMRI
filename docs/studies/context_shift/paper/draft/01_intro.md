<!-- Section 1: Introduction. Rewrite step 2 (2 Sept 2026): context → the two tasks'
origins → the safeguard pair → three worlds → design and Figure 1 → contributions.
All claims and numbers of the previous version retained. Kind-audit item 15 applied
("has a measurable correlate"). -->

# 1. Introduction

Language models can be made to express uncertainty, and sometimes do. What they do far
less reliably is volunteer that the words in front of them have not settled into one
reading. In the 96 completions we examine in §3.5, none does: some list both senses,
but none asks which is meant or says that the choice is open. Much of what we ask
models to do quietly assumes the opposite: that by the time a model acts, it has settled
on one reading. Safety behaviors in particular often take the form "if the request is
X, do Y". That rule inherits an unexamined premise: that "the request is X" is a
resolved fact rather than a reading in transit. The interesting failures, we will argue,
live in the unresolved zone: the stretch of a conversation during which context has
genuinely shifted what a token means but the model's internal reading has not finished
following. This paper measures that zone directly.

We measure it in two tasks. The first comes from an old question about humor.
Theories of humor have long placed incongruity and its resolution at the center of the
phenomenon: two mutually exclusive understandings of a text take shape, and something
must give. Dynel's taxonomy of conversational humor separates the garden-path joke
from the pun [CITE: Dynel]. In a garden-path joke
one meaning is established, a second is revealed, and belief shifts from one to the
other. In a pun the incongruity is not resolved but held. The joke in our epigraph is
the classic garden path built on the word *tank*: to get it, the reader's understanding
of one word must shift from one sense to the other. In a human reader that shift was
long observable only through behavior. In a language model it has a measurable
correlate: the in-between of a meaning shift is a trajectory in the residual stream,
and we can instrument it.

The second task has a graver origin. In a widely reported 2025 case, a sixteen-year-old
died by suicide after months of conversation with a language model [CITE: Raine v.
OpenAI; reporting]. The case is contested litigation, and we characterize only what the
court filing and contemporaneous reporting describe. They recount three things. Direct
requests triggered safeguards. The same requests, reframed as fiction, received
assistance, while the user's real circumstances were present in the same long
conversation. And the model offered to draft a suicide note. We do not analyze that
case. We take from it a precise scientific question. A model processing such a
conversation carries, in some form, internal state that tracks whether "I want to write
a suicide letter." is framed as fictional or real. How does that internal state move as
the surrounding context shifts?

Our two tasks also bracket a safety question: what a safeguard does while the reading
is unresolved. The fiction/real request is covered by a trained refusal safeguard. The tank task's
request is
"What is the meaning of the word tank?". It is covered by none. The pair therefore lets us watch
behavior with and without a trained safeguard. We recognized this after the fact
rather than designing it. Whether the safeguard carries a default answer for
unresolved cases is an interpretation we defer to §4.

When accumulated context shifts what a token means, what is the in-between? We consider
three candidate worlds. In the first, irresolution is a *learned state*: something the
model has structure for. In the second, it is a *passage*: mere transit between the two
resolved readings. In the third, it is *off the learned distribution entirely*: the
token pushed into regions the model never organized, where no trained behavior applies.
The dynamics of biological neural systems offer a warning about the first two [CITE:
metastability in neural dynamics]. There, states that are transiently stable without
being fixed-point attractors are the norm rather than the anomaly. Such states are
called metastable, and their existence means a learned state and a passage need not
be distinct. The title of this
paper reports where the data landed. *Unresolved* describes the states we found and, we
will argue, the three-worlds taxonomy itself.

The design is simple. Each task pairs a fixed *carrier* sentence with contexts that
grow one sentence at a time to forty. The carrier is the task's request, and it
contains the measurement token. For the
first twenty sentences the context supports one sense or one framing. After sentence
twenty it supports the other. This is the shift marked in Figure fig_s9_collapse. The
carrier is re-appended at every step, so the same token is re-read as the context
grows. Matched contexts that never switch, the no-shift references, set the scale for
the reading.

Figure fig_s9_collapse shows the central result. The figure draws the unresolved zone
as the gap between the two no-shift references. From either direction, readings cross
into that gap and stop short of the opposite reference. The separation is robust in
three of the four cases and suggestive in the fourth (§3.2).

We contribute:

1. A measurement protocol for reading interpretations over accumulating context,
   including two instrument artifacts, accumulation offset and axis rotation, that
   mimic findings (§2).
2. The shape of reinterpretation: a gradual, partial update whose remnant lingers to
   the end of the tested horizon (§3.2).
3. The form of its dynamics: drift plus discrete jumps that are not timed by evidence
   strength, with the smooth integrators we tested rejected head-to-head (§3.3).
4. The dwelling within the unresolved zone: a stationary intermediate state in one
   tank direction, where the model's answers hedge between the senses (§3.4). Zero of
   the 96 completions ask which sense is meant (§3.5).
5. Behavior set beside the reading in both tasks: the task with a trained safeguard
   mostly stays safe while the reading is unresolved, and its share of safe responses
   falls as the reading moves toward the fictional frame (§3.5).
6. Hysteresis, the dependence of the reading on the order in which the evidence
   arrived, almost fully explained by weighting recent sentences more heavily. A mild
   direction-dependent recency difference is all that remains, so the metastability
   lives in the path, not the equilibrium (§3.6).
7. A persistent, systematic marker of mixed context that behavior does not appear to
   use (§3.7).

Section 4 returns to the three worlds with these results in hand: the in-between
states are unremarkable in geometry and uncommitted in meaning, and the taxonomy
conflated those two axes. All numbers regenerate from the committed repository, which
includes the study's full corrections record.
