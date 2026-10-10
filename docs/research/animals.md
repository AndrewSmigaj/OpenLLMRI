# Animals: kinship, way of life and words that split (lens slice 1c, 10d.5, 2026-10-09)

Related: data/sentence_sets/lexical/animals_kinship_v1.md (the set, its rules and its audits),
docs/DESIGN.md (C1 single-word sets and split words, C3 hold-out designs, C4 tuning, C8 the axes
analysis), docs/research/single_words.md (the first single-word lens), docs/studies/animals/study.yaml

One lens for all the animals: does the model group animals by kinship (their taxonomy) or by how
they live, and what does reading a split name at its last token do? Every number here comes from
the files listed at the end, and was re-read from them at every layer it names.

## The capture

- **The set:** `animals_kinship_v1`, 524 one-word animal names in 8 groups (mammal 165, bird 122,
  reptile 32, amphibian 15, fish 79, insect 53, arachnid 10, other invertebrate 48), each with its
  taxonomy from the Catalogue of Life (COL26.9), checked field by field before the capture, and its
  way of life (habitat, movement, diet, wild or domestic).
- **The run:** `session_6e485e10`, the date pinned to 2026-09-16, nothing generated. 524 of 524
  written, none dropped. 94 names are one token; 430 split (303 into two tokens, 120 into three, 7
  into four), each read at its last token at character offset 1 of " name".
- **Held out by order:** the set declares its families (`metadata.holdout`: the order, whole
  names), the capture kept the declaration, and every lens took it without being told. Fold i holds
  out the i-th order of every group: 171 orders (or their stand-ins where COL gives none) make 41
  folds, merged round-robin into 12.

## The lenses

- **`animals-k8-n15`** (k 8 at every layer, 15 neighbours, 6-D), held out on 12 folds of whole
  orders: the group is read best at L6 to L12 (AMI 0.37 to 0.40, κ 0.45 to 0.53; peak AMI 0.40 at
  L10), weakly at L0 to L2 (0.07 to 0.10) and L18 to L22 (0.12 to 0.18). Whether the name split is
  read at AMI 0.28 to 0.36 at every layer.
- **`animals-k8-n15-tuned`**, tuned on the group. The test portion is 36 whole orders, 119 animals
  the selection never saw; the other orders made 5 selection folds. All 9 settings passed the
  self-check.

| Layer | settings (n, dims) | k | test AMI | test κ | untuned test AMI (k 8) | raw Ward test AMI | ceiling test AMI |
|---|---|---|---|---|---|---|---|
| L0 | 15, 3-D | 9 | 0.09 | 0.20 | 0.11 | 0.10 | 0.48 |
| L1 | 50, 3-D | 6 | 0.04 | 0.11 | 0.09 | 0.10 | 0.54 |
| L2 | 5, 3-D | 10 | 0.12 | 0.30 | 0.13 | 0.12 | 0.88 |
| L3 | 5, 12-D | 7 | 0.14 | 0.26 | 0.21 | 0.26 | 0.87 |
| L4 | 15, 6-D | 10 | 0.21 | 0.35 | 0.19 | 0.27 | 0.84 |
| L5 | 15, 12-D | 8 | 0.30 | 0.47 | 0.29 | 0.32 | 0.78 |
| L6 | 15, 6-D | 9 | 0.36 | 0.63 | 0.36 | 0.33 | 0.83 |
| L7 | 15, 12-D | 6 | 0.29 | 0.45 | 0.32 | 0.22 | 0.87 |
| L8 | 15, 6-D | 6 | 0.33 | 0.48 | 0.32 | 0.18 | 0.72 |
| L9 | 15, 3-D | 8 | 0.32 | 0.42 | 0.31 | 0.28 | 0.77 |
| L10 | 15, 12-D | 8 | 0.34 | 0.40 | 0.35 | 0.26 | 0.78 |
| L11 | 5, 6-D | 7 | 0.29 | 0.31 | 0.35 | 0.32 | 0.70 |
| L12 | 5, 6-D | 8 | 0.32 | 0.35 | 0.32 | 0.29 | 0.74 |
| L13 | 5, 12-D | 10 | 0.30 | 0.42 | 0.29 | 0.29 | 0.75 |
| L14 | 5, 6-D | 10 | 0.22 | 0.38 | 0.28 | 0.27 | 0.72 |
| L15 | 5, 6-D | 8 | 0.26 | 0.37 | 0.29 | 0.23 | 0.74 |
| L16 | 15, 12-D | 9 | 0.30 | 0.44 | 0.29 | 0.28 | 0.74 |
| L17 | 5, 12-D | 8 | 0.22 | 0.43 | 0.24 | 0.26 | 0.72 |
| L18 | 5, 3-D | 10 | 0.10 | 0.07 | 0.07 | 0.18 | 0.74 |
| L19 | 5, 3-D | 10 | 0.10 | 0.15 | 0.07 | 0.17 | 0.67 |
| L20 | 15, 6-D | 9 | 0.12 | 0.18 | 0.11 | 0.13 | 0.64 |
| L21 | 5, 12-D | 10 | 0.15 | 0.24 | 0.15 | 0.19 | 0.73 |
| L22 | 5, 12-D | 10 | 0.18 | 0.23 | 0.18 | 0.24 | 0.72 |
| L23 | 5, 12-D | 8 | 0.12 | 0.32 | 0.21 | 0.22 | 0.71 |

- **Tuned against untuned:** on the test portion the tuned lens is better at 10 layers and worse at
  14; the median difference is −0.003. Both peak at L6 (0.36). The winner led its runner-up by less
  than 0.02 AMI at 22 of 24 layers, so, as on the nouns, the settings matter little and k most.
- **The ceiling** (a logistic probe on the raw states, trained on the labels) reaches 0.48 to 0.88
  test AMI: the groups are far more separable than any unsupervised grouping finds them.

## Taxonomic neighbourhoods

For every animal, the share of its 10 nearest neighbours that share its group and each rank of its
taxonomy (a rank counted only where both animals have it), against the same share with the
taxonomy shuffled 200 times (`analysis/taxonomic_neighbourhoods.py`).

| Shared | lens L6–L13 | raw L6–L13 | chance |
|---|---|---|---|
| group | 0.67 to 0.71 | 0.64 to 0.70 | 0.20 |
| class | 0.61 to 0.65 | 0.59 to 0.64 | 0.18 to 0.19 |
| order | 0.20 to 0.23 | 0.21 to 0.26 | 0.03 |
| family | 0.06 to 0.07 | 0.06 to 0.09 | 0.01 |
| genus | 0.01 to 0.02 | 0.02 | 0.001 |

- The group's share rises from 0.33 at L0 to 0.70 at L6 in the lens; in raw space it is already
  0.64 at L2. It falls at L18 to L20 (0.46 to 0.49 in the lens, 0.52 to 0.57 raw) and recovers a
  little by L23.
- Every rank is far above chance: in the lens, neighbours share an order 7 to 8.5 times as often
  as chance, and a family about 10 times. The finer the rank, the smaller the share, as nested
  kinship would give.

## Kinship or way of life

The guide lists 33 animals whose kinship and way of life disagree. For each, at every layer: its
neighbours among its kin without the trait that sets it apart (for a dolphin, mammals that don't
swim), against its look-alikes from other groups (non-mammals that swim), each against chance
(`analysis/kinship_or_way_of_life.py`). The index is above 0 when the neighbours lean to kin.
"Beyond chance" means outside the middle 95% of the same index with the items' positions shuffled
1,000 times. Because whether a name split divides the space (below), the index is also counted
within the animal's own token count: only neighbours with its token count, against chance in that
pool, with positions shuffled within each token count. Five of the 33 are one-token names (whale,
dolphin, seal, bat, eel).

| Kind | lens: kin beyond chance | raw: kin beyond chance | within token count (lens, raw) |
|---|---|---|---|
| mammals that swim (16) | 18 layers (L0, L1, L4–L7, L9–L20) | 20 layers (L2–L18, L21–L23) | the same 18 and 20 |
| mammals that fly (2) | 12 layers | 12 layers | 5 and 10 |
| birds that don't fly (6) | 7 layers (L7–L13) | 5 layers | 8 (L7–L13, L21) and 6 |
| named "fish", not fish (5) | 16 layers (L4, L6–L20) | 17 layers (L2–L18) | 14 (L6–L19) and 15 |
| legless, not snakes (3) | L7, L8, L10 | none | L7, L8, L10 and L5, L8 |
| a fish that walks (1) | 20 layers | 22 layers (L2–L23) | 19 and 21 |

- **The kinds lean to kin.** No kind leans to its look-alikes beyond chance at any layer, in either
  space or either count. Swimming mammals sit among land mammals rather than among fish, and the
  named "fish" (starfish, jellyfish, cuttlefish, crayfish, silverfish) sit with their own groups
  rather than with fish whose names don't end in "fish".
- **Not the token count's doing:** counted within each token count, the swimming mammals lean to
  kin at the very same layers. Only the flying mammals lose much (5 lens layers instead of 12): the
  bat is a one-token name, and the one-token names are mostly mammals.
- **Animal by animal, the whales are the exception.** The humpback leans to its look-alikes (index
  −2 or below) at 12 layers in the lens and at 8 in raw space (L1, L8, L15, L19–L23); the porpoise
  at L14, L16 and L21–L23 in the lens and L9 and L21–L23 raw; the whale at L6, L9, L11 and L14 in
  the lens. The otter's index never falls below −0.43, and the beaver, muskrat and nutria lean to
  kin at 19 to 24 of the 24 layers in either space.
- **The eel sits with the snakes** in raw space at L10 to L18 (and at L3 and L21; index down to
  −3.70), and less in the lens (L12).

## Words that split

`analysis/split_words.py` asks three things, in the lens's space, in raw space, and in raw space
with each token count's mean taken out.

- **The last piece pulls, early and late.**
  - Split names that share their last piece with another split name have 34% of their neighbours
    ending in the same piece at L0 in the lens (33% raw); chance is 1%. By L8 to L16 it is 15 to
    17% (12 to 15% raw).
  - The 23 names ending in "fish" cluster almost entirely by that piece at first: in the lens at
    L0, 99% of the fish's neighbours and 100% of the non-fish's end in "fish" (chance 4%). In raw space the
    share falls to its lowest at L8 to L13 (fish 0.44, the non-fish 0.30 to 0.40) and comes back at
    L20 to L23 (0.74 to 0.94). The pull of the piece is a U across the layers: meaning wins in the
    middle, and the token's own identity again at the end.
- **The token count splits the space at every layer.**
  - A probe tells one token from several at a balanced accuracy of 0.96 or more at every layer in
    the lens, and 0.99 or more in raw space.
  - The 94 one-token names' 10 nearest neighbours are 86 to 100% other one-token names in the lens
    and 89 to 100% in raw space, at every layer; chance is 18%.
  - Taking out each token count's mean leaves 77 to 99% through L18; only from L19 does it fall
    (43 to 58% at L19 to L23). So the difference between the two kinds of name is more than an
    offset.
  - In the axes analysis the lens's nodes read the token count at κ 0.81 to 1.00 at every layer,
    and raw Ward groupings at 0.85 to 1.00. The node details flag a node by its token count at all
    24 layers.
- **Within that split, kinship holds.** In the lens, from L4 to L17, split names have 61 to 77%
  of their neighbours in their own group (chance 19%); one-token names 35 to 44% (chance 22%),
  most of their neighbours being other one-token names of any group.

**Why it matters:** the lens's main division at every layer is whether a name split, not what
the animal is. A one-token name is a whole word that starts with a space; a split name is read at a
word-internal piece. The kinship results stand within each kind of name, but every lens on this
capture mixes the two. A proposal for Andrew is in RECOMMENDATIONS.md: read each word at the token
after it (the end of the message), which is the same token for every item and has taken in the
whole word.

## The axes analysis (`animals-k8-n15-tuned`)

Held out on the lens's 12 folds of whole orders, against five decoys per attribute:

| Attribute | probe κ (L0) | probe κ (L4–L23) | the lens's nodes κ (L4–L16) |
|---|---|---|---|
| group | 0.60 | 0.79 to 0.87 | 0.40 to 0.52 (peak L6) |
| habitat | 0.44 | 0.67 to 0.77 | 0.27 to 0.37 |
| movement | 0.56 | 0.67 to 0.74 | 0.35 to 0.47 |
| diet | 0.20 | 0.30 to 0.55 (peak L7) | about 0 (−0.06 to 0.12) |
| wild or domestic | 0.17 | 0.29 to 0.65 (peak L11) | 0 |
| tokens | 1.00 | 0.99 to 1.00 | 0.81 to 0.99 |

A linear probe reads every attribute above its decoys from L0. Habitat and movement are read
nearly as well as the group, though they follow the group in most animals (fish swim, birds fly):
only the 33 disagreeing animals tell them apart, and those lean to kin.

## Node details and routing

- The surface check predicts the lens's nodes from surface features alone at held-out κ 0.16 to
  0.39; at every layer at least one node is flagged by the target's token count.
- The nodes explain 0.07 to 0.46 of the next layer's routing variance (the routing effect).

## Files

- The set: `data/sentence_sets/lexical/animals_kinship_v1.json` and its guide; the audit
  `docs/studies/animals/analysis/audit_set.py` (0 problems, 2026-10-09).
- The capture: `data/lake/session_6e485e10/` and `data/lake/_sessions/session_6e485e10.json`.
- The lenses: `data/lake/session_6e485e10/lenses/animals-k8-n15/` (`validation.json`) and
  `animals-k8-n15-tuned/` (`search.json`, `validation.json`, `axes.json`, `details/`); the saved
  version in `data/lenses/session_6e485e10/animals-k8-n15-tuned/`.
- The analyses: `docs/studies/animals/analysis/` (scripts, `results/*.json`, `figures/*.png`), run
  on both lenses; the tuned lens's numbers are quoted here, and the untuned lens's agree (the
  group's share peaks at 0.71 at L10 in both).
