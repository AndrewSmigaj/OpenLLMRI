<!-- Section 1: Introduction, scientific register. Outline §1 (7 bullets). Checklist:
failure-stakes opening, no SCOUT [x]; humor lineage w/ epigraph referenced not retold
[x]; clinical incident paragraph [x]; post-hoc contrast marking [x]; three worlds +
one NEURO sentence [x]; collapse figure [x]; contributions [x]. -->

# 1. Introduction

Language models can be made to express uncertainty, and sometimes do. What they do far
less reliably — and in the 96 completions we examine here, never — is volunteer that the
words in front of them have not settled into one reading. Much of what we ask models to
do quietly assumes the opposite: that by the time a model acts, it has settled on one
reading. Safety behaviors in particular often take the form *if the request is X, do Y*
— a rule that inherits an unexamined premise: that "the request is X" is a resolved fact
rather than a reading in transit. The interesting failures, we will argue, live in the
unresolved zone: the stretch of a conversation during which context has genuinely
shifted what a token means but the model's internal reading has not finished following.
This paper measures that zone directly.

The route to this study runs through an old question. Theories of humor have long placed
incongruity and its resolution at the center of the phenomenon: two mutually exclusive
understandings of a text form, and something must give. Dynel's taxonomy of
conversational humor separates the garden-path joke — one meaning established, a second
revealed, belief shifting from one to the other — from the pun, where the incongruity is
not resolved but held. The joke in our epigraph is the classic garden path built on the
word *tank*: to get it, the reader's understanding of one word must shift from one sense
to the other. That shift was long observable only through behavior. In a language model
it is a measurement problem with an actual substrate: the in-between of a meaning shift
is a trajectory in the residual stream, and we can instrument it.

The second task has a graver origin, and we state it plainly. In a widely reported
incident, a person who had been using a language model for fiction writing shifted, over
the course of a long interaction, to describing their real circumstances — and the model
assisted with a suicide letter. We do not analyze that case; we take from it a precise
scientific question. A model processing such a conversation maintains, in some form, a
reading of whether "I want to write a suicide letter." is a fictional or a real request.
How does that internal reading move as the surrounding context shifts? As it happens —
this was recognized after the fact, not designed — our two tasks bracket the safety
question from both sides. The request that triggers a refusal safeguard turns out to
behave as though the safeguard has a default answer for unresolved cases; the innocuous
question "what does *tank* mean?" has no safeguard and no default. The pair lets us
watch behavior with and without a trained fallback.

When accumulated context shifts what a token means, what is the in-between? Three
candidate worlds: a *learned state* — irresolution is itself something the model has
structure for; a *passage* — mere transit between the two resolved readings; or *off the
learned distribution entirely* — the token pushed into regions the model never
organized, where no trained behavior applies. In the dynamics of biological neural
systems, transiently stable states that are not fixed-point attractors are the norm
rather than the anomaly. That norm warns against assuming the first two worlds — learned
state and passage — must be distinct. The title of this paper is a report on where the
data landed:
*unresolved* describes the states we found — and, we will argue, the three-worlds
taxonomy itself.

The design is simple: two tasks — the polysemous word, the framed request — each with a
fixed *carrier* sentence containing the measurement token. Contexts grow one sentence at
a time to forty, with the class of the evidence — which sense, or which framing, the
sentences support — flipping after twenty; the carrier is re-appended at every step, so
the same token is re-read under steadily shifting context; matched single-class contexts
provide the reference scale. Figure fig_s9_collapse shows the central result: from
either direction, readings cross into the in-between zone quickly, and neither ever
reaches the opposite reference.

We contribute: (1) a measurement protocol for reading interpretations over accumulating
context without self-deception — including two instrument artifacts, accumulation offset
and axis rotation, that we first mistook for findings (§2); (2) the shape of
reinterpretation — fast and partial, with a remnant of the old interpretation persisting
to the end of the tested horizon (§3.2); (3) its mechanism: drift plus discrete
state-triggered jumps, with every smooth integrator rejected head-to-head (§3.3); (4)
the dwelling within the unresolved zone — a stationary intermediate whose behavioral
output is hedging — and the observation that in 96 of 96 completions the model answers
rather than asking (§3.4); (5) hysteresis fully explained by recency weighting — order
effects are real but add nothing beyond recency, so the metastability lives in the path,
not the equilibrium (§3.5); (6) a learned, persistent marker of mixed context that does
not influence behavior — the model represents that its context is mixed and does not act
on it (§3.6); and a corrections record of eighteen entries that we present as method
rather than confession (Appendix A). All numbers regenerate from the committed
repository.
