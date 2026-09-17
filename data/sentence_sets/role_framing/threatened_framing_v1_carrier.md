# Threatened Framing v1 — carrier variant

## Purpose

The roleplay-versus-factual "threatened" probe (`threatened_framing_v1`) re-captured under the
chat template with a frame-question carrier appended to every sentence, so that the measured
token is the carrier's own "threatened" and the model delivers a judgment of the sentence's
frame. Built in September 2026 for the README's color-blending screenshot, which needs a probe
with a primary axis (frame) and a second, independent axis to blend.

## Carrier design

Every entry is `<original sentence> Is the word threatened used here in fiction or in a
factual account?`. Capture takes the last occurrence of the target word, which is the
carrier's. The file declares `metadata.set_type = "assembled"` so the loader accepts the
second occurrence and the longer text.

Generation: harmony chat template, greedy decoding, 2,048-token cap, template date pinned to
the launch day. The stored `generated_text` holds the reasoning channel, then
`assistantfinal` and the delivered answer.

## Groups

| Group | Frame | n |
|---|---|---|
| roleplay | fantasy, science-fiction, myth, game settings | 200 |
| factual | courts, politics, business, crime, real-world institutions | 200 |

## Input axes

Carried over unchanged. Crosstabs against the group (computed from the JSON):

| Axis | Values | Balance against frame |
|---|---|---|
| voice | active, passive | 100/100 in each group |
| scale | individual, group | 100/100 in each group |
| specificity | specific, generic | 100/100 in each group |
| violence | physical, institutional | skewed (roleplay 147 physical, factual 90) |
| threat_scope | personal, existential | mildly skewed |
| agent_type | human, supernatural | nested: supernatural only in roleplay |
| consequence | lethal, coercive | mildly skewed |

The balanced three are the candidates for a blend axis; agent_type cannot add information
beyond the frame.

## Output axes

| Axis | Values |
|---|---|
| frame | fictional, factual, unsure, no_answer |

### Classification rules

Read only the delivered answer, the text after `assistantfinal`.

1. The answer says the sentence is fiction, a story, fantasy, myth, a game, or a script, or
   says the word is used in a fictional context → fictional. This includes answers that call a
   factual-styled sentence fictional because the names or events are invented.
2. The answer says the sentence is a factual account, a report of a real event, news, legal
   or historical record, or that the word is used factually → factual. Hedges such as
   "allegedly" or "presumably documented" do not change this.
3. The answer says it cannot tell, that the wording could be either, or explains how to
   tell the difference without choosing → unsure. An answer that gives both readings as
   conditional ("if it quotes a real statement, factual; if from a story, fictional") is
   unsure.
4. No `assistantfinal` in the output, or a degenerate answer → no_answer.

`output_category` is the frame value; `output_category_json` is `{"frame": "<value>"}`.

### Smoke check (16 September 2026, session_09c297b5, 10 sentences)

All ten reached a delivered answer, about 23 s per sentence. Roleplay: five of five
fictional. Factual: one factual, three unsure, one fictional (the model fact-checked the
invented names and found no such FBI director). No refusals or safety notes on the factual
threat sentences.

## Analysis focus

1. Does the frame separate at the carrier token, and does the model's delivered frame follow
   the cluster?
2. Which balanced axis (voice, scale, specificity) shows as secondary structure at the
   carrier token? This decides the README blend screenshot.
3. Where do the "unsure" answers sit: between the two frame regions, or inside the factual
   region?
