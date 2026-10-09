# How many axes in a word (lens slice 1b's showcase)

One figure from lens slice 1b (`docs/DESIGN.md` K), made from the app's own exports:
`single_words_showcase.png`, published with this note at
https://claude.ai/artifact/332M3bVPuYRFbwdHALUfam. The figure's `recipe` chunk and `recipe.json` hold each panel's
recipe: the view's link, the lens and its settings, and the commits it was built and served at.
The panels are in `panels/`; `compose.py` lays them out and crops panel F to its layers:

    .venv/bin/python docs/studies/single_words/showcase/compose.py

The runs behind the numbers are in `docs/research/single_words.md` (the single words) and
`docs/research/lens_core_validation.md` (the tank tuning). The study is
`docs/studies/single_words/study.yaml`. Every number below was read from the lens files or the API.

## What it shows

**A. The single-word lens over all 24 layers** (`session_8f536bea`, `words-k8-n15-tuned`).
- **The items:** 861 nouns, each given alone with a space first (" eagle"), in 8 categories of 5
  families.
- **The lens:** tuned on the category with whole families held out, k 4 to 10 per layer. Hue is
  the category and lightness the valence.
- **Its score:** on one held-out family per category, its test AMI runs from 0.40 to 0.63
  (peak L7). A logistic probe reaches 0.76 to 0.90 on the same families.
- **Where it splits first** (cutting each layer's embedding into two):
  - concrete against abstract at L0 to L7;
  - food and animals against the rest at L8 to L17;
  - physical things against people and abstractions at L18 to L23.

  Animacy never makes that first split.

**B. What each technique reads.** Held-out κ per attribute and layer, with decoys given per
family:
- **The probe** reads the category at 0.84 to 0.91, animacy at 0.86 to 0.92 and concreteness at
  0.90 to 0.95 at every layer, and valence at 0.55 to 0.69.
- **The lens's nodes** carry concreteness best (0.67 to 0.90) and valence least (0.22 to 0.35).
  The category alone gives valence 0.19.
- **The model still carries valence beyond the category:** with each category's mean taken out
  of its words, a probe reads it at 0.49 to 0.60.
- **The count saturates.** Every technique passes its decoys for all four attributes at nearly
  every layer, so the strengths, not the count, tell the techniques apart.

**C. Directions and dimensionality.**
- **Fewer independent directions than random:** the attributes' partial axes span 5.3 to 6.1
  independent directions, fewer than permuted design rows give (95th percentile 7.2 to 7.5).
  Animacy and concreteness are contrasts of categories, and the categories group by the levels
  above them.
- **A U-shaped spectrum:** effective dimensionality is 298 at L0, 51 at L15 and 163 at L23. The
  threatened sentences, for comparison, sit at 12.5 to 25.2.

**D. The lens's own space in 3-D,** at L4 to L10, where the three main directions hold 89 to
100% of each layer's variance. " eagle" stays in the animal node at every one of these layers,
with food below and emotions and ideas above.

**E. Angles at L5.** The cosines between the partial axes are faded inside the band permuted
design rows give, and shown beside the design's own correlations.
- **Animacy leans to people:** it lines up with the people direction at 0.83, above the
  permuted rows' 0.42 to 0.72, and with the animals' only at 0.36, below their 0.41 to 0.66.
- **Emotions and ideas share a direction** (0.57), and abstract-against-concrete follows them
  (0.84 and 0.88).

**F. A pipeline lit on the expert chart** (rank 1, cropped to L0 to L6). P3 is an early route of
68 words, found again in both halves of the folds.
- **Its route:** L0E2 to L5E24 among each word's four experts. At rank 1 its members run L1E28,
  L2E31, L3E31, L4E14 and L5E24.
- **Its lean:** to emotions (22% against 11% of all words), abstract words (37% against 25%) and
  negative ones (29% against 17%).

Single words route apart: the lens has 3 pipelines and 15 hubs (at L4 to L7). The tank sentences
routed as one trunk.

**G. Tuning on the tank set** (`tank-k5-n15-tuned`). Settings and k were searched per layer by
held-out AMI, then scored on a test portion the search never saw.
- **Against the untuned lens:** the tuned one is better at 15 layers and worse at 6 (median
  +0.02), and both peak at 0.57 (L11).
- **On the words:** tuning gains as little (better at 10 layers, worse at 12, median −0.004).

## And the word inside a sentence

Read through this lens, the tank set's "tank" tokens lie beyond the words' own neighbourhoods
from L1 on. Their median distance percentile in raw residual space is 98.7 at L1 and 99.9 to 100
from L2. A word inside a sentence is not where the same word sits alone.
