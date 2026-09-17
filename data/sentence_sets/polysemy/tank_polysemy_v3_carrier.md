# Tank Polysemy v3 — carrier variant

## Purpose

The five-sense tank probe (`tank_polysemy_v3`) re-captured under the chat template with the
context-shift paper's Q1 carrier appended to every sentence, so that the measured token is the
carrier's own "tank" (the paper's calibrated site) and the model delivers an answer that names
a sense. Built in September 2026 for the README's feature screenshots (stepped UMAP
trajectories, cluster route analysis) and to replace the March capture, whose raw-continuation
outputs were mostly degenerate repetition.

## Carrier design

Every entry is `<original sentence> What is the meaning of the word tank?`. Capture takes the
last occurrence of the target word, which is the carrier's. Unlike the paper's context
sentences, these sentences also contain "tank" once themselves; the file declares
`metadata.set_type = "assembled"` so the loader accepts the second occurrence and the longer
text.

Generation: harmony chat template, greedy decoding, 2,048-token cap, template date pinned to
the launch day (`pin_date`). The stored `generated_text` is the whole completion with special
tokens stripped: the reasoning channel first, then `assistantfinal` and the delivered answer.

## Groups

| Group | Sense | n |
|---|---|---|
| aquarium | glass tank holding fish, marine life, reef | 100 |
| vehicle | armored military vehicle | 100 |
| scuba | breathing-gas cylinder for diving | 100 |
| septic | sewage or waste-storage tank | 100 |
| clothing | sleeveless top | 100 |

## Input axes

Carried over unchanged from `tank_polysemy_v3`: `structure` (action / description) and
`register` (narrative / technical / casual).

## Output axes

| Axis | Values |
|---|---|
| sense | aquarium, vehicle, scuba, septic, clothing, container, multiple, no_answer |

### Classification rules

Read only the delivered answer, the text after `assistantfinal`. Rules apply in order, as in
the paper's behavior categorization (`docs/studies/context_shift/analysis/behavior_categorization_v2.md`):

1. The answer states which sense the sentence uses → that sense. Asides listing other senses
   ("it's not the military vehicle here") do not matter.
   - aquarium: fish tank, aquarium, container holding water for fish or marine life.
   - vehicle: armored fighting vehicle, military tank, tracked vehicle with a gun.
   - scuba: cylinder of breathing gas or compressed air for diving.
   - septic: septic tank, sewage or waste chamber, underground drainage vessel.
   - clothing: tank top, sleeveless shirt or garment.
2. The answer commits only to a generic storage vessel ("a large container for holding
   liquids or gases") without naming aquarium, scuba, or septic → container. Seen in the smoke
   check for a scuba sentence and a septic sentence; the model chose the generic sense.
3. The answer says the sentence could use two or more senses, or gives a dictionary entry
   spanning families without saying which the sentence uses → multiple.
4. No `assistantfinal` in the output (looped or stuck to the cap), or a degenerate answer →
   no_answer.

`output_category` is the sense value; `output_category_json` is `{"sense": "<value>"}`.

### Smoke check (16 September 2026, session_72eb5124, 10 sentences)

All ten reached a delivered answer, about 21 s per sentence. Eight named the design sense;
one scuba and one septic sentence were read as a generic container. No answer asked what the
user meant.

## Analysis focus

1. Do the five senses separate at the carrier token, and from which layer?
2. Which senses merge? Do aquarium, scuba, and septic share a "container" region?
3. Does the delivered sense follow the cluster? Where the model answers container, which
   cluster do those sentences sit in?
4. Are structure and register visible as secondary structure (blend axis) at the carrier token?
