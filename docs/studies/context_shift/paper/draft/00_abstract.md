<!-- Title, epigraph, abstract, content note. Rewrite step 2 (2 Sept 2026): review-only
pass; chained findings split into sentences, "Two tasks:" fragment removed, "safe
responses" in place of the term defined in §3.5. Numbers unchanged. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available: in the
US, call or text 988; elsewhere, findahelpline.com.*

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

A language model answers even while the meaning of the conversation is still in
flux. We measure what its internal reading of a critical token does during that
flux, and what the model does about it. In gpt-oss-20b, we track a
difference-of-means reading in the residual stream at a single token site while
forty-sentence contexts switch sides halfway through: the word "tank" moving between
aquarium and vehicle senses, and the fixed request "I want to write a suicide
letter." moving between fictional and real framing. Every shifted context, 72 runs
across tasks and directions, is compared with a matched context that never switches,
and at four points after the switch we generate completions, setting behavior beside
the reading.

The reading follows the shift only partway. It crosses to the new side after a
median of 4 to 10.5 sentences, by task and direction, then stops short of the
matched reference by 40% to 109% of the reference level, and the twenty sentences
after the switch never close the remaining gap. In one tank direction it stops at
the midpoint between the senses and stays there, stationary to the end of the
window. Individual runs move by drift plus discrete jumps, and where the fits can
decide, drift plus jumps beats every smooth evidence-integration model we fit. The
jumps do not coincide with unusually strong evidence, and the large effect of
evidence order is explained almost entirely by recency weighting. None of the
intermediate states is geometrically unusual against the no-shift references, yet
together they carry a persistent internal signal that the context is mixed, a signal
the model's behavior does not appear to use. We call this cluster of properties
semantic metastability.

What the model does while unresolved differs sharply between the tasks, and across
the 300 completions we examine, none asks which reading is meant. The tank task has
no safeguard: the model lists both senses or commits silently to one. The
suicide-letter task has a refusal safeguard, and it mostly holds while the reading
sits between frames: 80% of completions there decline the letter or redirect to
support. But safe responses fall from 91% to 50% as the reading moves toward the
fictional frame (the 50% rests on four completions). That weakening is reachable by
ordinary, coherent context, with no adversarial prompt.
