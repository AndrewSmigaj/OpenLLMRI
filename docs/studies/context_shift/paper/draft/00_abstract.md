<!-- Title, epigraph, abstract, content note. Outline §Abstract (9 bullets). Checklist:
model+scale first line [x]; corrected gap range 0.4-1.1 [x]; descriptive-only safety
close [x]; coin placement [x]; content note after abstract [x]. -->

# Unresolved: Semantic Metastability in a Language Model Under Context Shift

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

## Abstract

In gpt-oss-20b, a 20-billion-parameter mixture-of-experts language model, we track a
token's reading — its residual-stream position along a calibrated axis between two
interpretations — while accumulating context shifts which interpretation the context
supports. Two tasks: a polysemous word moving between senses (*tank*: aquarium or
vehicle), and a fixed request ("I want to write a suicide letter.") moving between
fictional and real framing. Contexts grow to forty sentences with the evidence class
flipping after twenty; matched single-class contexts provide a no-shift reference at
every position. Transitions are two-phase: a fast partial update, then a remnant of the
prior interpretation that twenty counter-sentences never remove — 0.4–1.1× the reference
amplitude (the midpoint-to-reference distance), across the four task × direction
conditions; three of the four remain when reference uncertainty is propagated. Among
classifiable runs, per-run dynamics are dominated by drift punctuated by discrete jumps:
model selection calibrated on synthetic data rejects every gradual-integration account
tested, including a two-timescale one, and evidence strength — the one sentence property
tested — does not predict when jumps occur; state-dependence is our working
interpretation. In the tank task one direction dwells in the zone between
interpretations — stationary for ten or more steps, to the end of the measured window —
with 45% of mid-zone completions hedging between senses; an exploratory fiction/real
site (n = 4) shows the same signature. Evidence order matters — hysteresis loops are
large — but an exponentially recency-weighted average of the evidence, its one decay
parameter fitted to the data, reproduces the loops almost fully; only a mild
direction-dependent difference in that parameter remains. No individual state is an
outlier relative to matched no-shift states, yet transition states share a small,
persistent marker of mixed context — 25–38% of the distance between the class means,
orthogonal to the interpretation axis. We call this cluster of properties semantic
metastability. The model never asks which meaning is intended — zero of 96 tank
completions, across all reading bands — and in the unresolved zone it either surfaces
both senses (45%) or silently commits to one (52%). The fiction/real task, covered by a
refusal safeguard, safe-completed at mid-transition (80%); safe-completion co-varies
with the reading, falling from 91% to 50% across bands (the fiction-side endpoint at n =
4, the gradient partly scene-driven).

*Content note: this paper analyzes model behavior around suicide-related requests in a
research context. If you or someone you know is struggling, help is available — in the
US, call or text 988; elsewhere, findahelpline.com.*
