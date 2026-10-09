# Single words: what a word alone carries (lens slice 1b, 10c.6, 2026-10-09)

Related: data/sentence_sets/lexical/nouns_meaning_feeling_v1.md (the set and its audits),
docs/DESIGN.md (C1 single-word sets, C4 tuning, C8 the axes analysis),
docs/research/lens_core_validation.md (the methods, and the threatened set's axes),
docs/studies/single_words/study.yaml

What a lens fitted on single words finds: the category, the levels above it, feeling, and how
words route. It also asks whether the lens can read a word inside sentences. Every number here
comes from the files listed at the end.

## The capture

- **The set:** `nouns_meaning_feeling_v1`, 861 nouns in 8 categories of 5 families each. Each
  noun is given alone as the user's message with a space first (" eagle"), so it is one token.
- **The run:** `session_8f536bea`, with the date pinned to 2026-09-16 and nothing generated. It
  took 3.5 minutes.
- **The check:** every word is stored at the user's token on all 24 layers, 861 of 861.

## The tuned lens (`words-k8-n15-tuned`)

- **The base:** `words-k8-n15` (k 8 at every layer, 15 neighbours, 6-D), built in 45 s; its
  self-check passed.
- **The tuning:** on the category, with whole families as the units held out.
  - The test portion is one family per category, 171 words: wild animals, ages, fruit, devices,
    rail vehicles, rooms, outlook emotions and science ideas.
  - The other four families per category made four selection folds.
  - All 9 settings passed the self-check, and the job took 10.6 minutes.

| Layer | settings (n, dims) | k | test AMI | test κ | untuned test AMI (k 8) | raw Ward test AMI | ceiling test AMI |
|---|---|---|---|---|---|---|---|
| L0 | 15, 6-D | 4 | 0.40 | 0.30 | 0.35 | 0.45 | 0.85 |
| L1 | 15, 3-D | 6 | 0.44 | 0.34 | 0.42 | 0.46 | 0.86 |
| L2 | 15, 12-D | 7 | 0.46 | 0.41 | 0.50 | 0.39 | 0.87 |
| L3 | 15, 6-D | 5 | 0.53 | 0.43 | 0.55 | 0.44 | 0.90 |
| L4 | 15, 12-D | 9 | 0.55 | 0.57 | 0.54 | 0.55 | 0.87 |
| L5 | 50, 12-D | 9 | 0.57 | 0.61 | 0.60 | 0.56 | 0.84 |
| L6 | 15, 12-D | 9 | 0.59 | 0.67 | 0.55 | 0.63 | 0.81 |
| L7 | 15, 3-D | 6 | 0.63 | 0.62 | 0.60 | 0.48 | 0.83 |
| L8 | 15, 3-D | 8 | 0.62 | 0.67 | 0.70 | 0.48 | 0.84 |
| L9 | 15, 6-D | 10 | 0.52 | 0.60 | 0.54 | 0.50 | 0.82 |
| L10 | 5, 3-D | 7 | 0.50 | 0.55 | 0.57 | 0.45 | 0.80 |
| L11 | 15, 6-D | 9 | 0.57 | 0.58 | 0.58 | 0.44 | 0.80 |
| L12 | 15, 3-D | 10 | 0.51 | 0.52 | 0.53 | 0.43 | 0.76 |
| L13 | 5, 6-D | 7 | 0.54 | 0.45 | 0.53 | 0.35 | 0.78 |
| L14 | 15, 6-D | 7 | 0.42 | 0.40 | 0.47 | 0.28 | 0.79 |
| L15 | 15, 12-D | 9 | 0.49 | 0.52 | 0.47 | 0.31 | 0.78 |
| L16 | 15, 12-D | 9 | 0.50 | 0.52 | 0.53 | 0.43 | 0.79 |
| L17 | 5, 6-D | 7 | 0.57 | 0.60 | 0.52 | 0.48 | 0.81 |
| L18 | 15, 6-D | 9 | 0.57 | 0.58 | 0.56 | 0.58 | 0.80 |
| L19 | 15, 12-D | 7 | 0.56 | 0.50 | 0.58 | 0.59 | 0.81 |
| L20 | 15, 6-D | 6 | 0.55 | 0.36 | 0.54 | 0.53 | 0.81 |
| L21 | 15, 12-D | 6 | 0.56 | 0.52 | 0.58 | 0.62 | 0.81 |
| L22 | 15, 12-D | 10 | 0.55 | 0.65 | 0.55 | 0.63 | 0.81 |
| L23 | 15, 12-D | 7 | 0.52 | 0.55 | 0.51 | 0.66 | 0.79 |

- **Tuned against untuned:** on the test portion the tuned lens is better at 10 layers, worse at
  12 and level at 2; the median difference is −0.004. The tuned lens peaks at 0.63 (L7), the
  untuned one at 0.70 (L8). The winner led its best runner-up by less than 0.02 AMI at 22 of 24
  layers. So settings matter as little here as on the tank and calibration sets.
- **The ceiling:** a logistic probe reaches 0.76 to 0.90 AMI on the same test families. The
  category is linearly there at every layer, well beyond what any grouping recovers.

## The levels above the category

The design nests animacy and concreteness above the category. Cutting the tuned lens's own
embedding into two shows which level the first split follows. The table gives each category's
share on the side that holds the ideas:

| Layer | animal | person | food | tool | vehicle | place | emotion | idea |
|---|---|---|---|---|---|---|---|---|
| L0 | 2% | 4% | 1% | 1% | 0% | 10% | 97% | 94% |
| L1 | 0% | 3% | 0% | 2% | 0% | 2% | 97% | 92% |
| L2 | 0% | 7% | 0% | 2% | 2% | 4% | 100% | 90% |
| L3 | 0% | 8% | 0% | 1% | 2% | 0% | 100% | 86% |
| L4 | 0% | 89% | 0% | 3% | 2% | 7% | 100% | 98% |
| L5 | 0% | 9% | 0% | 1% | 2% | 0% | 100% | 58% |
| L6 | 0% | 9% | 0% | 2% | 2% | 2% | 100% | 90% |
| L7 | 2% | 12% | 1% | 3% | 5% | 2% | 99% | 94% |
| L8 | 12% | 100% | 6% | 97% | 100% | 100% | 100% | 100% |
| L9 | 14% | 100% | 5% | 97% | 98% | 100% | 100% | 100% |
| L10 | 21% | 99% | 5% | 93% | 98% | 99% | 100% | 100% |
| L11 | 30% | 100% | 10% | 100% | 100% | 100% | 100% | 100% |
| L12 | 32% | 100% | 7% | 100% | 100% | 100% | 100% | 100% |
| L13 | 17% | 99% | 6% | 94% | 98% | 99% | 100% | 98% |
| L14 | 28% | 100% | 10% | 100% | 100% | 100% | 100% | 100% |
| L15 | 27% | 100% | 13% | 100% | 100% | 100% | 100% | 100% |
| L16 | 25% | 99% | 10% | 100% | 100% | 100% | 100% | 100% |
| L17 | 24% | 100% | 7% | 100% | 100% | 100% | 100% | 100% |
| L18 | 5% | 96% | 2% | 84% | 81% | 96% | 100% | 98% |
| L19 | 10% | 93% | 2% | 79% | 83% | 94% | 100% | 99% |
| L20 | 10% | 90% | 1% | 57% | 75% | 86% | 100% | 100% |
| L21 | 2% | 89% | 1% | 26% | 10% | 57% | 99% | 98% |
| L22 | 9% | 93% | 2% | 39% | 20% | 66% | 100% | 99% |
| L23 | 3% | 93% | 2% | 28% | 14% | 55% | 100% | 97% |

- **L0 to L7:** the first split is concrete against abstract. Emotions (97 to 100%) and most ideas
  sit on one side. The exceptions are L4, where people join them (89%), and L5, where only 58% of
  the ideas do. In the k profile the two-node cut agrees with concreteness at in-sample AMI 0.72
  to 0.80 at L0 to L3, L6 and L7.
- **L8 to L17:** the first split sets food and animals (5 to 13% and 12 to 32% on the other side)
  apart from everything else. People, tools, vehicles and places go with the emotions and ideas.
- **L18 to L23:** tools and vehicles move over to the food and animals (tools 84% down to 26%,
  vehicles 81% down to 10% on the ideas' side), and places divide (55 to 96%). People stay with
  emotions and ideas (89 to 96%).
- **Animacy never makes the first split.** Its in-sample AMI with the two-node cut is at most
  0.12, at every layer. Animals and people sit on opposite sides from L8 on.

## The axes (DESIGN.md C8)

The four attributes are the category, animacy, concreteness and valence. The family field groups
items, so it is not scored as an attribute. Decoys are random per family, five per attribute.

**Recovered:** every technique passes the decoy line for all four attributes at nearly every
layer. Raw Ward misses one at L0 and L10, and raw spectral one at L13. The strengths tell the
techniques apart:

| Layer | k | UMAP lens: category / animacy / concreteness / valence | probe: category / animacy / concreteness / valence | independent directions (95th permuted) | effective dimensionality |
|---|---|---|---|---|---|
| L0 | 4 | 0.31 / 0.34 / 0.89 / 0.24 | 0.89 / 0.86 / 0.94 / 0.56 | 5.44 (7.48) | 298 |
| L1 | 6 | 0.36 / 0.36 / 0.88 / 0.27 | 0.90 / 0.89 / 0.94 / 0.59 | 5.32 (7.39) | 220 |
| L2 | 7 | 0.45 / 0.43 / 0.88 / 0.32 | 0.90 / 0.90 / 0.94 / 0.62 | 5.55 (7.36) | 200 |
| L3 | 5 | 0.48 / 0.50 / 0.90 / 0.29 | 0.91 / 0.89 / 0.93 / 0.63 | 5.68 (7.39) | 207 |
| L4 | 9 | 0.60 / 0.67 / 0.84 / 0.32 | 0.91 / 0.91 / 0.93 / 0.64 | 5.59 (7.34) | 192 |
| L5 | 9 | 0.69 / 0.79 / 0.86 / 0.29 | 0.89 / 0.91 / 0.94 / 0.67 | 5.72 (7.48) | 173 |
| L6 | 9 | 0.65 / 0.78 / 0.86 / 0.33 | 0.88 / 0.90 / 0.94 / 0.69 | 5.59 (7.38) | 155 |
| L7 | 6 | 0.54 / 0.71 / 0.78 / 0.32 | 0.89 / 0.91 / 0.91 / 0.68 | 5.65 (7.40) | 146 |
| L8 | 8 | 0.65 / 0.77 / 0.81 / 0.25 | 0.88 / 0.92 / 0.93 / 0.68 | 5.58 (7.28) | 128 |
| L9 | 10 | 0.67 / 0.69 / 0.77 / 0.33 | 0.88 / 0.92 / 0.93 / 0.67 | 5.60 (7.43) | 116 |
| L10 | 7 | 0.52 / 0.66 / 0.78 / 0.27 | 0.87 / 0.91 / 0.92 / 0.64 | 5.67 (7.24) | 92 |
| L11 | 9 | 0.59 / 0.65 / 0.71 / 0.35 | 0.86 / 0.91 / 0.90 / 0.65 | 5.71 (7.31) | 82 |
| L12 | 10 | 0.56 / 0.62 / 0.71 / 0.31 | 0.85 / 0.91 / 0.91 / 0.64 | 5.67 (7.23) | 64 |
| L13 | 7 | 0.48 / 0.57 / 0.76 / 0.32 | 0.84 / 0.89 / 0.91 / 0.62 | 5.74 (7.26) | 58 |
| L14 | 7 | 0.44 / 0.50 / 0.71 / 0.27 | 0.85 / 0.90 / 0.92 / 0.62 | 5.75 (7.34) | 54 |
| L15 | 9 | 0.52 / 0.55 / 0.77 / 0.30 | 0.85 / 0.91 / 0.92 / 0.64 | 5.80 (7.36) | 51 |
| L16 | 9 | 0.55 / 0.66 / 0.75 / 0.32 | 0.87 / 0.91 / 0.93 / 0.64 | 5.82 (7.18) | 58 |
| L17 | 7 | 0.50 / 0.55 / 0.77 / 0.26 | 0.87 / 0.91 / 0.93 / 0.61 | 5.88 (7.34) | 75 |
| L18 | 9 | 0.58 / 0.60 / 0.82 / 0.23 | 0.86 / 0.92 / 0.93 / 0.60 | 5.76 (7.33) | 78 |
| L19 | 7 | 0.58 / 0.65 / 0.89 / 0.26 | 0.86 / 0.92 / 0.95 / 0.59 | 5.97 (7.46) | 102 |
| L20 | 6 | 0.51 / 0.62 / 0.78 / 0.27 | 0.86 / 0.92 / 0.95 / 0.57 | 5.98 (7.41) | 127 |
| L21 | 6 | 0.57 / 0.72 / 0.73 / 0.22 | 0.85 / 0.90 / 0.94 / 0.55 | 6.00 (7.49) | 136 |
| L22 | 10 | 0.54 / 0.66 / 0.76 / 0.27 | 0.85 / 0.89 / 0.93 / 0.56 | 6.06 (7.36) | 138 |
| L23 | 7 | 0.52 / 0.67 / 0.67 / 0.26 | 0.84 / 0.90 / 0.93 / 0.55 | 5.71 (7.53) | 163 |

- **The probe** reads the category at κ 0.84 to 0.91, animacy at 0.86 to 0.92 and concreteness
  at 0.90 to 0.95 at every layer, but valence only at 0.55 to 0.69.
- **The lens's nodes** carry concreteness best (0.67 to 0.90), then animacy (0.34 to 0.79, peak
  L5) and the category (0.31 to 0.69, peak L5). Valence is lowest, at 0.22 to 0.35.
- **Valence follows the category by design** (tools and vehicles are almost all neutral, emotions
  rarely). The category alone predicts valence at κ 0.187: each held-out word takes its
  category's most common valence in training. So the nodes' valence (0.22 to 0.35) is little more
  than the category's. The model carries valence beyond the category all the same: with each
  category's training mean taken out of its words, a probe still reads valence at κ 0.489 (L0),
  0.598 (L4), 0.595 (L8), 0.575 (L12), 0.571 (L16), 0.557 (L20) and 0.524 (L23).
- **Fewer independent directions than random contrasts.** The partial axes span 5.32 to 6.06
  independent directions, below what permuted design rows give (95th percentile 7.18 to 7.53).
  This set's thirteen rows (eight category values, animacy, concreteness and three valence values)
  share structure: animacy and concreteness are themselves contrasts of categories, and the
  categories group by the levels above them. In the threatened set, whose eight attributes cross,
  the real axes span more directions than the null from L5 on.
- **Angles at L5** (each pair against its own band from permuted design rows): animacy lines up
  with the people direction at 0.83, above the band (0.42 to 0.72), and with the animals' only at
  0.36, below theirs (0.41 to 0.66). What the model separates as animate is mostly people. Emotions
  and ideas share a direction (0.57, against a band of −0.22 to 0.09), and the abstract-against-
  concrete axis follows them (0.84 and 0.88, above bands of 0.44 to 0.65 and 0.63 to 0.79).
- **Effective dimensionality** (the participation ratio of the standardized spectrum) is far higher
  than for sentences, and U-shaped: 298 at L0, 51 at its lowest (L15), 163 at L23. Half the
  variance lies in 145 components at L0 and in 32 at L16. The threatened sentences sit at 12.5 to
  25.2.

## Suffixes

Among the 218 emotions and ideas, 52 carry a derivational suffix. Does the lens's grouping
follow the suffix more than chance? The test is AMI between suffix and node, against shuffling
the suffix within each category (500 shuffles). It passes the shuffles' 95th percentile at 13 of
24 layers, but stays small: at most 0.066 (L14). The category's own agreement with the nodes is
far larger. The suffix leaves a trace in the abstract nodes, not their shape.

## Experts, pipelines and hubs

Single words route apart, as the plan expected; sentences built on one target word routed as one
trunk. The routes are worked out with families as the permutation's groups.
- **Pipelines:** three. P1 runs from L7 to L23 and holds 595 of 861 words across every category,
  a trunk. P2 runs from L11 to L22 with 50 words, 28 of them tools, and isn't found again in both
  halves of the folds. P3 runs from L0 to L5 with 68 words of mixed categories.
- **Hubs:** 15, at L4 to L7: experts whose words arrive from several experts, up to 3.29
  effective sources (L7E5, from L6E30, L6E28 and L6E2).
- **Experts involved:** for example, L6E24 weighs people more (difference 0.362, AUC 0.974), L17E16
  food (0.229, AUC 0.974) and L4E18 emotions (0.218, AUC 0.943). Valence has experts too (10 per
  value), but valence follows the category, so these may be the categories' experts.

## Reading the tank capture through the word lens

The lens read the tank set (`session_1434a9be`, 499 sentences, "tank" in five senses) at the
same site, position 1, the target token. This is exploratory: a lens fitted on words alone, read
inside sentences (DESIGN.md D2, rule 3).
- **How far out:** the sentences' "tank" tokens are far from every word: their median distance
  percentile, measured in raw residual space against the lens's own nearest-neighbour distances,
  is 55.2 at L0, 98.7 at L1 and 99.9 to 100 from L2 on. Every layer from L1 is flagged far out.
- **What that means:** a word inside a sentence isn't where the same word sits alone. From the
  first layer on, the context moves its token outside the region single words occupy, so the
  nodes a reading lands in only say which words are least far. This is the finding the plan
  allowed for.
- **The nodes, read with that caveat,** still differ by sense:
  - at L4, 86% of the vehicle sentences vote into a node whose words are mostly vehicles (under
    half), against 25% of the aquarium ones;
  - at L8, the vehicle (95%), clothing (96%) and scuba (80%) sentences fall in tool nodes, while
    66% of the aquarium sentences fall in a place node.

## The report

The tested analysts (prompts `6adec8f4b5b7`) wrote two cards in 4 calls:
- **The lens report:** two drafts reconciled; all 103 numerals checked.
- **The routes card:** all 41 numerals checked.

Their reading agrees with this note's:
- **Nodes:** people get their own node at L0 (L0C2, 97% person). Agreement with the category
  peaks at in-sample AMI 0.723 at L6. Ideas and emotions share a node at L7 and part at L8, and
  tools and vehicles share one at L7 and part at L9.
- **Experts:** the rank-1 expert follows the category only weakly (agreement at most 0.341). No
  expert's weight separates tools or vehicles beyond chance.
- **Pipelines:** P1 is a trunk. P2's lean to tools (56% against 13% of all words) comes from a
  pipeline not found again in both halves of the folds. P3 leans to emotion, abstract and
  negative words.

## Caveats

- Valence is one author's judgment, made in one pass. It follows the category by design.
- The one-token rule thinned some families: vehicles have 59 words and animals 96, against 115 to
  125 for the other categories.
- Abstract nouns carry derivational suffixes (27% of emotions, 22% of ideas); their trace in the
  nodes is measured above.
- The test portion is one family per category; its scores are unbiased but rest on one draw.

## Files

- `data/lake/session_8f536bea/` (the capture) and its lenses:
  - `lenses/words-k8-n15/` (the base);
  - `lenses/words-k8-n15-tuned/`: `search.json` (the tuning), `validation.json` (families as
    folds, with decoys), `axes.json` (89 s), `routes.json`, `details/v1.json`, and
    `readings/1434a9be/` (the tank capture read through it, 54 s).
- `data/sentence_sets/lexical/nouns_meaning_feeling_v1.json` and its guide (the audits).
