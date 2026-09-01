<!-- Section 1: Introduction, Andrew's voice. Outline §1 (7 bullets). Checklist:
failure-stakes opening, no SCOUT [x]; humor lineage w/ epigraph referenced not retold
[x]; clinical incident paragraph [x]; post-hoc contrast marking [x]; three worlds +
one NEURO sentence [x]; collapse figure [x]; contributions [x]. -->

# 1. Introduction

Language models do not say they are uncertain. When the interpretation of what they
are reading is unresolved, they do not pause, ask, or flag it — they go with it. Much
of what we ask models to do quietly assumes the opposite: that by the time a model
acts, it has settled what the words in front of it mean. Safety behaviors in
particular often take the form *if the request is X, do Y* — a rule that inherits an
unexamined premise, namely that "the request is X" is a resolved fact rather than a
reading in transit. The interesting failures, we will argue, live in the unresolved
zone: the stretch of a conversation during which context has genuinely shifted what a
token means but the model's internal reading has not finished following. This paper
measures that zone directly.

The route to this study runs through an old question. Theories of humor have long
placed incongruity and its resolution at the center of the phenomenon: two mutually
exclusive understandings form while processing a text, and something must give.
Dynel's taxonomy separates the garden-path joke — one meaning established, a second
revealed, belief shifting from one to the other — from the pun, where the incongruity
is not resolved but held. The joke in our epigraph is the classic garden path built
on the word "tank." Years before large language models, one of us studied these
shifts by mining association spaces from the web and watching the word 'tank' move
between its meanings, by cosine distance, across the two halves of a garden-path
joke. What was then a visualization exercise is now a measurement problem with an
actual substrate: the in-between of a meaning shift is a trajectory in the residual
stream, and we can instrument it.

The second probe has a graver origin, and we state it plainly. In a widely reported
incident, a person who had been using a language model for fiction writing shifted,
over the course of a long interaction, to describing their real circumstances — and
the model assisted with a suicide letter. We do not analyze that case; we take from
it a precise scientific question. A model reading such a conversation maintains, in
some form, a reading of whether "I want to write a suicide letter." is a fictional or
a real request. How does that internal reading move as the surrounding context
shifts? As it happens — this was recognized after the fact, not designed — our two
probes bracket the safety question from both sides: the refusal safeguard behaves as
though it carries a default for unresolved cases, while the innocuous question "what
does *tank* mean?" carries none, so the pair lets us watch behavior both with and
without a net.

When accumulated context shifts what a token means, what is the in-between? Three
candidate worlds: a *learned state* — irresolution is itself something the model has
structure for; a *passage* — mere transit between the two resolved readings; or *off
the learned distribution entirely* — the token pushed into regions the model never
organized, where trained behavior has no writ. In the dynamics of biological neural
systems, transiently stable states that are not fixed-point attractors are the norm
rather than the anomaly, which should make us suspicious of forcing the first two
worlds apart prematurely. The title of this paper is a report on where the data
landed: *unresolved* describes the states we found, and, in part, the taxonomy.

Our design is deliberately simple. Two probe arms — the polysemous word, the framed
request — each pair a fixed carrier sentence with a designated measurement token.
Contexts grow one sentence at a time to forty, with the class of the evidence
flipping after twenty; the carrier is re-appended at every step, so the same token is
re-read under steadily shifting context; matched no-shift arms provide the ruler.
Figure fig_s9_collapse is the study in one image: from either direction, readings
cross into the in-between zone quickly — and neither ever reaches the opposite
reference.

We contribute: (1) an instrument doctrine for reading interpretations over
accumulating context without self-deception — including two artifacts, accumulation
drift and axis rotation, that we first mistook for findings (§2); (2) the shape of
reinterpretation: fast, partial, permanent-within-range (§3.2); (3) its mechanism:
drift plus discrete state-triggered jumps, with every smooth integrator rejected
head-to-head (§3.3); (4) the park — a stable intermediate whose behavioral output is
hedging, and the observation that in 96 of 96 completions the model answers rather
than asking (§3.4); (5) hysteresis fully explained by recency weighting — metastability
as a property of paths, not equilibria (§3.5); (6) a learned, persistent, behavior-
inert marker of mixed context — the model represents its own irresolution and does
not act on it (§3.6); and a corrections record of seventeen entries that we present
as method rather than confession (Appendix A). Every number in this paper regenerates
from committed code.
