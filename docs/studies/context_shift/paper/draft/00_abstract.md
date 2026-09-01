<!-- Title, epigraph, abstract, content note. Outline §Abstract (9 bullets). Checklist:
model+scale first line [x]; corrected gap range 0.4-1.1 [x]; descriptive-only safety
close [x]; coin placement [x]; content note after abstract [x]. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

In gpt-oss-20b, a 20-billion-parameter mixture-of-experts language model, we track a
token's interpretation — read from the residual stream along calibrated contrast axes —
while accumulating context shifts what that token means: a polysemous word moving
between senses, and a fixed request ("I want to write a suicide letter.") moving
between fictional and real framing. Transitions are two-phase: a fast partial update
followed by a residual of the prior interpretation that twenty counter-sentences never
remove — 0.4–1.1× the class separation, three of four conditions robust to reference
uncertainty. Per-run dynamics are drift punctuated by discrete jumps; simulation-
calibrated model selection rejects every smooth integrator tested, including a
two-timescale one, and evidence strength does not predict when jumps occur — the
trigger appears to lie in the state of the run.
In one direction per probe the trajectory parks: a stationary intermediate
configuration, held for ten or more steps, whose behavioral output is hedging. Order of
evidence matters — hysteresis loops are large — but is fully explained by fitted
recency weighting: no measurable stickiness. Everything runs on learned structure: no
individual state leaves the model's activation distribution, but transition states carry a small,
persistent, learned marker of mixed context (25–38% of class separation), orthogonal
to the content contrast. We call this cluster of properties semantic metastability. In
the unresolved zone the model answers rather than reporting uncertainty — zero of 96
completions request disambiguation; the refusal task nonetheless held (80%
safe-completion at mid-transition) while the sense task committed silently (52% of
mid-band completions), and
safeguard behavior attenuates along the learned frame axis (91%→50%).

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available — in the
US, call or text 988; elsewhere, findahelpline.com.*
