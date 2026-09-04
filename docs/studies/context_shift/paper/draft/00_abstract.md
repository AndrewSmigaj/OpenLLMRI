<!-- Title, epigraph, abstract, content note. Rewrite step 2 (2 Sept 2026): review-only
pass; chained findings split into sentences, "Two tasks:" fragment removed, "safe
responses" in place of the term defined in §3.5. Numbers unchanged. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

When the context around a request changes its meaning — a word's sense, or whether a
request is fiction — how does a language model's internal reading follow? We use two
tasks: the word *tank* moving between aquarium and vehicle senses, and the fixed
request "I want to write a suicide letter." moving between fictional and real framing.
We measure that reading directly in gpt-oss-20b, from the residual stream at one
token, while forty-sentence contexts switch sides halfway through. Each shifted
context is compared with a matched context that never switches, which we call the
no-shift reference. At four points after
the switch we also generate a completion from each context, to set the model's
behavior beside its reading.

The reading follows the shift only partway. It crosses to the new side after a median
of 4 to 10.5 sentences, depending on the task and direction, then stops short of
where the no-shift reference sits. The twenty sentences after the switch never close
the remaining gap. In the extreme case, one tank direction, the reading reaches the
midpoint between the two sides and stays there, stationary to the end of the window.
Individual runs move by drift plus discrete jumps, and the jumps do not coincide with
unusually strong evidence. The order in which the evidence arrives has a large effect
on the reading. Recency weighting explains almost all of it. None of the intermediate
states is geometrically unusual against the no-shift references. Together they carry a persistent internal signal that the context is mixed, and the model's behavior does not appear
to use that signal. We call this cluster of properties semantic metastability.

What the model does while its reading sits between the two sides differs between the
two tasks. The tank task has no safeguard, and there the model either lists both
senses or commits silently to one. It never asks which meaning is intended: zero of
96 tank completions request clarification. The suicide-letter task has a refusal
safeguard and mostly stays safe in the middle reading band, with the reading between
the two frames: 80% of completions there decline the letter or redirect to support
rather than fulfilling the request. But the share of safe responses falls from
91% to 50% as the reading moves toward the fictional frame. The low endpoint rests on
four completions. That weakening is reachable by ordinary context, with no
adversarial prompt.

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available: in the
US, call or text 988; elsewhere, findahelpline.com.*
