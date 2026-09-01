<!-- Title, epigraph, abstract, content note. Outline §Abstract (9 bullets). Checklist:
model+scale first line [x]; corrected gap range 0.4-1.1 [x]; descriptive-only safety
close [x]; coin placement [x]; content note after abstract [x]. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

In gpt-oss-20b, a 20-billion-parameter mixture-of-experts language model, we track a
token's interpretation — read from the residual stream as a position along a calibrated
axis between two interpretations — while accumulating context shifts what the token
means. Two tasks: a polysemous word moving between senses (*tank*: aquarium or vehicle),
and a fixed request ("I want to write a suicide letter.") moving between fictional and
real framing. Contexts grow to forty sentences with the evidence class flipping after
twenty; matched single-class contexts provide a no-shift reference at every position.
Transitions are two-phase: a fast partial update, then a remnant of the prior
interpretation that twenty counter-sentences never remove — 0.4–1.1× the reference
amplitude (the midpoint-to-reference distance), across the four task × direction
conditions; three of the four remain when reference uncertainty is propagated. Per-run
dynamics are drift punctuated by discrete jumps: model selection calibrated on synthetic
data rejects every gradual-integration account tested, including a two-timescale one,
and evidence strength does not predict when jumps occur — the trigger appears to lie in
the run's internal state, not the incoming sentence. In one direction per task the
trajectory parks: it stops between the two interpretations, holds there for ten or more
steps, and the model's completions hedge. Evidence order matters — hysteresis loops are
large — but a fitted recency weighting reproduces the loops fully; order adds nothing
beyond recency. No individual state is an outlier relative to the model's ordinary
activations, yet transition states share a small, persistent, learned marker of mixed
context — 25–38% of the distance between the class means, orthogonal to the
interpretation axis itself. We call this cluster of properties semantic metastability.
In the unresolved zone between interpretations the model answers rather than reporting
uncertainty: zero of 96 completions ask which meaning is intended. The fiction/real task
— the one backed by a refusal safeguard — nonetheless stayed safe mid-transition (80% of
completions decline or redirect to support), while the tank task silently picked one
sense (52%); and safety behavior tracks the internal reading, falling from 91% to 50%
safe responses as the reading moves from the real toward the fictional side.

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available — in the
US, call or text 988; elsewhere, findahelpline.com.*
