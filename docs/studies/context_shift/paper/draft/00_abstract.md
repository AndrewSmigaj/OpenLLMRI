<!-- Title, epigraph, abstract, content note. Outline §Abstract (9 bullets). Checklist:
model+scale first line [x]; corrected gap range 0.4-1.1 [x]; descriptive-only safety
close [x]; coin placement [x]; content note after abstract [x]. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

When the context around a request changes its meaning — a word's sense, or whether a
request is fiction — how does a language model's internal reading follow? We measure
this directly in gpt-oss-20b, reading a token's interpretation from the residual
stream while forty-sentence contexts switch sides halfway through, against matched
no-shift references. Two tasks: the word *tank* moving between aquarium and vehicle
senses, and the fixed request "I want to write a suicide letter." moving between
fictional and real framing.

The reading follows the shift only partway. It crosses to the new side after a median
of four to ten sentences, then stops short, and twenty countering sentences never
close the remaining gap. In one tank direction it dwells between the two
interpretations, stationary to the end of the window. Individual runs move by drift
plus discrete jumps, and the jumps are not timed by strong evidence; order effects,
though large, are explained almost entirely by recency weighting. None of these
states is geometrically unusual against matched references, yet all carry a
persistent internal signal that the context is mixed — a signal the model's behavior
does not appear to use. We call this cluster of properties semantic metastability.

The model never asks which meaning is intended: zero of 96 tank completions request
clarification. The task covered by a refusal safeguard stayed safe at mid-transition
(80% of completions); the task without one committed silently to a sense.
Safe-completion falls from 91% to 50% as the reading moves toward the fictional frame
(the low endpoint rests on four completions) — attenuation reachable by ordinary
context.

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available — in the
US, call or text 988; elsewhere, findahelpline.com.*
