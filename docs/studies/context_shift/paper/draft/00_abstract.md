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

A language model answers even while its interpretation of the conversation is
still in flux. What does its internal reading of a critical token do during that
flux, and what does the model do about it? In gpt-oss-20b, we study two tasks. In
the first, the word "tank" moves between its aquarium and vehicle senses. In the
second, the fixed request "I want to write a suicide letter." keeps its wording
while the surrounding frame moves between fiction writing and the speaker's real
circumstances. We track a difference-of-means reading in the residual stream, at
one token site per task, while forty-sentence contexts switch sides halfway
through. Each of the 72 shifted runs, spanning both tasks and both directions, is
compared with a matched context that never switches, which we call the no-shift
reference. At four points after the switch we generate completions, setting
behavior beside the reading.

The reading follows the shift only partway. It crosses to the new side after a
median of 4 to 10.5 sentences, by task and direction. On average it then stops
well short of the no-shift reference. Measured against the reference's own
distance from the midpoint between the two sides, the shortfall ranges from 40% to
109%, and the largest means the average reading ends at the midpoint. The twenty
sentences after the switch never close the remaining gap. In one tank direction
the reading stops at the midpoint and stays there, stationary to the end of the
window. Individual runs move by drift plus discrete jumps. Where the fits can
decide, drift plus jumps beats every smooth evidence-integration model we fit. The
jumps do not coincide with unusually strong evidence. Evidence order has a large
effect on the reading, explained almost entirely by recency weighting. None of the
intermediate states is geometrically unusual against the no-shift references. Yet
together they carry a persistent internal signal that the context is mixed, a
signal the model's behavior does not appear to use. We call this cluster of
properties semantic metastability.

What the model does while unresolved differs sharply between the tasks. Across the
312 completions we examine, none asks which reading is meant. The tank task has no
safeguard: the model lists both senses or commits silently to one. The
suicide-letter task has a refusal safeguard, and wherever the model answers, it
holds: 89% of the middle band's delivered answers and 95% of the real side's decline
the letter or redirect to support. What changes toward the fiction-writing frame is
whether an answer arrives at all. Under greedy decoding, 85 of the 204 completions
never leave the model's reasoning channel, and on the fiction side three of four do
not. A shorter generation budget had suggested the safeguard weakens toward the
fiction-writing frame; the regenerated completions show that was an artifact of
reading truncated reasoning.
