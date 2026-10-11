# How the model organizes animals: findings (2026-10-11)

Related: docs/research/animal_ontology.md (the proposal: the nine ways and the three measures),
docs/studies/animal_ontology/study.yaml (the study and its ledger),
data/sentence_sets/lexical/animals_ontology_v1.md (the set's rules and borderline calls),
docs/research/animals.md (the first animal study, whose findings stand),
docs/design/design.md (sentence sets: the animal ontology)

**Status:** exploratory, as the proposal set out: nothing was predicted as a gate. Every number
below is read from the result files in `docs/studies/animal_ontology/analysis/results/`, at the
layers it names; the scripts and figures sit beside them.

## What was run

- **The set** `animals_ontology_v1`: the first animal set's 524 one-word names, labelled by hand in
  eight new ways beside its six earlier ones (fourteen axes in nine ways). Its audit finds no
  problems; the earlier fields are copied unchanged, item by item. Of the taxonomy matches, 305
  have a Catalogue of Life common name holding the word; 22 have common names that don't, all
  checked by hand and right (irregular plurals such as dormice and geese, and synonyms such as
  stoat and ermine, cavy and guinea pig, langoustine and Norway lobster); 197 taxa have no English
  names in the Catalogue.
- **The capture** `session_5cd7091d` (524 names, none dropped), with the date pinned to 2026-09-16.
  Its states equal the first animal capture's (`session_6e485e10`) bit for bit at all 24 layers,
  routing included.
- **The lens** `onto-k8-n15`: 6-D UMAP, 15 neighbours, k 8 at every layer; validation and the
  axes analysis hold out whole taxonomic orders (12 folds, merged from the orders).
- **The measures,** at the name's last token, in raw space (the residual stream standardized and
  reduced to 50 principal components) and in the lens's own space:
  1. **neighbours:** how often an animal's 10 nearest neighbours share its value, as agreement
     beyond chance; chance from 1,000 shuffles within each token count;
  2. **held out:** κ on orders never seen, for a linear probe and for the lens's nodes, against
     each reader's decoy line;
  3. **own share:** a model of the distance between every pair of animals from whether they differ
     on each axis, the token count and the names' length; an axis's own share is what it explains
     with every other axis held fixed, tested with 1,000 permutations within each token count. A
     companion fits each axis **alone** beside the two controls. Both are given as a percentage of
     the distance variance the controls leave.
- **Examples:** the nearest neighbours of 26 animals where the ways disagree.

Figures: `neighbours.png`, `shares.png`, `held_out.png`, `leading.png` in
`docs/studies/animal_ontology/analysis/figures/`.

## In short

- **Descent leads, with the ways that go with it.** At every layer from L2, an animal's nearest
  neighbours share its group, its everyday kind, its legs and its body covering more than any
  other way, in raw space and in the lens; how it moves and where it lives come next. The ways
  that are about people (its relation to us, where we meet it, how we feel about it, its danger)
  are there beyond chance at nearly every layer, but at half the strength or less.
- **On orders the reader never saw, every way can be read.** A linear probe reads the group and the
  everyday kind best (κ 0.82 to 0.87 at L4 to L16) and danger least (0.22 to 0.33). The lens's eight
  nodes carry the descent-tied ways (0.32 to 0.58) and almost none of the people-centred ones.
- **What a way adds on its own is small.** The descent-tied ways explain the distances largely
  together: in raw space, covering and legs add nothing beyond descent and everyday kind at any
  layer. Size, the order, diet, feeling and the group add a little at most layers. Danger has the
  largest own share at its peak in raw space (L4) and holds at every layer from L4 to L16 in the
  lens; with size and danger graded it still holds, so it is not graded size (below).

## 1. Neighbours

Agreement beyond chance, averaged over L4 to L16 (figure `neighbours.png`):

| Axis | Raw space | Lens space |
|---|---|---|
| group (descent) | 0.58 | 0.59 |
| everyday kind | 0.58 | 0.59 |
| legs | 0.57 | 0.59 |
| body covering | 0.53 | 0.54 |
| movement | 0.50 | 0.48 |
| habitat | 0.41 | 0.39 |
| relation | 0.33 | 0.23 |
| size | 0.29 | 0.27 |
| wild or domestic | 0.28 | 0.12 |
| where met | 0.28 | 0.24 |
| feeling | 0.24 | 0.17 |
| diet | 0.22 | 0.16 |
| order (descent) | 0.19 | 0.16 |
| danger | 0.15 | 0.11 |

- **Beyond chance almost everywhere:** in raw space every axis passes the shuffles' middle 95% at
  22 layers or more; in the lens every axis but diet (21) and wild or domestic (13) passes at 22 or
  more.
- **The leader alternates between the group, everyday kind and legs** (`leading.png`). The three
  agree for most animals (Cramér's V 0.78 to 0.84 between them in the design), so this measure
  can't tell them apart; the shares below are what separate them.
- **Peaks and dips:** the group peaks at 0.64 (raw L5; lens L10), legs at 0.64 (lens L8). Every
  axis dips at L18 to L20 (the group to 0.40 in raw space at L20, and to 0.32 in the lens), and
  most recover partly by L23 (the group to 0.49 raw and 0.40 lens), as the first study's
  taxonomic neighbourhoods dipped at L18 to L20.
- **The order** reads low on this scale (0.19 raw) because 99 of its 171 values hold a single
  name, which no neighbour can share; beyond chance it is at every layer.

## 2. Each axis alone, and with the others held fixed

Shares of the pairwise distances, as a percentage of the variance the controls (token count, name
length) leave (figure `shares.png`).

**Alone,** each axis beside the controls only:
- **raw space:** the group and everyday kind lead from L2 on, at most 5.6% (L17); covering 3.8%
  (L16), legs 3.9% (L17), movement 2.5% (L17), the order 2.0% (L10), habitat 1.8% (L23). Every
  people-centred way stays at or under 1.1% (relation, L22).
- **lens space:** the group 17.0% at L6, everyday kind 16.5%, legs 15.3%, covering 12.4%,
  movement 7.5%; habitat 3.2% (L10). The people-centred ways stay at or under 1.0%.

**With every other axis held fixed** (own share; significant layers at p < 0.05):

| Axis | Raw: layers, peak | Lens: layers, peak |
|---|---|---|
| group (descent) | 16; 0.23% (L16) | 18; 0.72% (L6) |
| order (descent) | 20; 0.41% (L10) | 15; 0.09% (L6) |
| everyday kind | 13; 0.23% (L7) | 3; 0.04% (L1) |
| body covering | 0 | 17; 0.30% (L12) |
| size | 21; 0.31% (L22) | 17; 0.39% (L4) |
| legs | 0 | 19; 1.86% (L9) |
| where met | 6 (L16 to L21); 0.12% (L17) | 15; 0.25% (L4) |
| relation | 4; 0.44% (L9) | 2; 0.24% (L23) |
| danger | 5 (L4, L5, L6, L13, L16); 0.76% (L4) | 13 (every layer L4 to L16); 0.86% (L11) |
| feeling | 14; 0.25% (L9) | 10; 0.05% (L22) |
| habitat | 3 (L17, L22, L23); 0.49% (L23) | 14; 0.92% (L0) |
| movement | 8; 0.23% (L0) | 10; 0.12% (L6) |
| diet | 17; 0.16% (L17) | 7; 0.03% (L10) |
| wild or domestic | 0 | 0 |

- **Most of what the descent-tied ways explain, they explain together:** alone, the group explains
  up to 5.6% (raw) and 17.0% (lens); held with the others, at most 0.23% and 0.72%.
- **Covering and legs add nothing in raw space** beyond descent and everyday kind (no layer below
  p = 0.05). In the lens, legs has the largest own share of any axis (1.86% at L9): the lens's
  space separates animals by legs more than raw space does, beyond the group and kind.
- **Small additions that hold across layers:** size (21 raw layers, 17 lens), the order (20 raw),
  diet (17 raw), feeling (14 raw). A difference in size, kept apart from descent, adds to how far
  apart two animals sit almost everywhere.
- **Danger:** its own share is the largest raw value at any layer (0.76% at L4) and in the lens it
  is significant at all 13 layers from L4 to L16. Each axis enters this model as "differ or not",
  so a pair of a huge and a tiny animal counts the same as a pair of a large and a huge one, and
  the animals that can kill are mostly large. With size and danger entered instead as how many
  steps apart two animals are (`graded.py`), danger's own share holds: in raw space at 10 layers
  (L4 to L6, L9, L11 to L16; 1.17% of what the controls leave at L4) and in the lens at every layer
  from L4 to L17 (1.01% at L6). Graded size keeps its own share too (19 raw layers, peak 0.98% at
  L5). Whether the danger signal is predators, venom, or size finer than five levels needs a set
  that varies danger within each kind.
- **Multiple tests:** 14 axes at 24 layers in each space; at p < 0.05, about one layer per axis
  would pass by chance. Runs of consecutive layers (danger at L4 to L16 in the lens, size at L3 to
  L23 in raw space) are unlikely to be chance; single layers (relation at L9) may be.
- **The token count in the lens:** at L1, L2, L18 and L19 the lens places one-token and split names
  in two far-apart clouds, and the controls alone explain 93 to 98% of the distances' variance
  (in raw space at most 32%, at L19). This is why the shares are given as a percentage of what the
  controls leave.

## 3. On orders never seen

κ on held-out orders, L4 to L16 (figure `held_out.png`):

| Axis | Linear probe | Lens nodes (k 8) |
|---|---|---|
| group (descent) | 0.82 to 0.87 | 0.39 to 0.53 |
| everyday kind | 0.83 to 0.87 | 0.40 to 0.54 |
| body covering | 0.78 to 0.84 | 0.32 to 0.48 |
| legs | 0.75 to 0.83 | 0.43 to 0.58 |
| habitat | 0.73 to 0.77 | 0.27 to 0.37 |
| movement | 0.68 to 0.74 | 0.34 to 0.48 |
| where met | 0.53 to 0.62 | 0.08 to 0.18 |
| feeling | 0.54 to 0.59 | −0.10 to 0.05 |
| relation | 0.49 to 0.55 | −0.02 to 0.10 |
| wild or domestic | 0.48 to 0.65 | 0.00 |
| size | 0.43 to 0.50 | 0.15 to 0.25 |
| diet | 0.43 to 0.55 | −0.06 to 0.12 |
| danger | 0.22 to 0.33 | 0.00 |

- **The probe** passes its decoy line at every layer for every axis but danger (22 layers). A linear
  readout of the residual stream carries all nine ways on orders it never saw, the people-centred
  ones included.
- **The lens's nodes,** cut at k 8 for the group, carry the descent-tied ways, movement and habitat
  at every layer, size at 23 and where met at 22; relation (13 layers), diet (11) and feeling (9)
  only weakly; danger at one layer and wild or domestic at none.
- **What "held out" rules out:** a reader that memorized an order's members. It doesn't rule out a
  shortcut through the class: pests are mostly insects, companions mostly mammals, birds and fish,
  so a people-centred axis read on unseen orders may still be read partly through descent.

## 4. Animals where the ways disagree

Nearest neighbours at L2, L6, L12, L18 and L23 (`results/disagreeing.json`):
- **The whales:** in raw space the whale's neighbours share its group at every one of those layers
  (0.7 to 0.9: dolphin, elephant, bear), with the shark among the five nearest from L6 on. In the
  lens at L6 and L12 they follow its kind and habitat instead (L6: trout, dolphin, salmon, shark,
  coral).
- **The penguin** sits with birds in the lens at L6 and L12 (group share 0.9 and 1.0: bustard,
  albatross, toucan; flamingo, ostrich, kakapo), and with seabirds and sea mammals in raw space
  (L6: puffin, panda, dolphin, pelican; L12: walrus, puffin).
- **The bat's** neighbours are other one-token names (cat, rat, ant, cod, carp), mammals and not,
  and almost never fliers (movement share 0.0 to 0.3 in raw space).
- **Names with a shared last piece** follow it, as the first animal study found: the slowworm's
  nearest neighbours are worms (ragworm, earthworm, glowworm, lugworm) at L6, L12 and L18 in raw
  space, and at L6 and L12 in the lens; the starfish and jellyfish sit with fish names and sea
  creatures (pufferfish, triggerfish, stonefish); the silverfish sits with household insects at L6
  and L12 (firebrat, cockroach, earwig) and with fish names at raw L18 (stonefish, lionfish,
  paddlefish, lungfish).
- **The eel** sits with the snake at raw L12 and L18 (snake and cobra among its five nearest at L12).

## Cautions

- **One author's judgment** made the people-centred labels and everyday kind; the guide lists
  every borderline call.
- **One cultural view:** where an animal is met, its relation to us and how we feel about it are
  judged for Britain and North America.
- **Correlated ways:** covering, legs and everyday kind follow descent (Cramér's V with the group
  0.79 to 0.84), and relation overlaps with danger (0.62) and feeling (0.55); the own shares are the
  only measure that separates them, and they are small.
- **Single words:** each name is read alone, at its last token. Which way leads may differ in
  sentences, where context picks the sense.
- **The token count** shapes both spaces; every null is drawn within it, and its effect on the
  examples is visible (the bat, the "-worm" and "-fish" names).

## Next

- What the danger signal holds: a set that varies danger within each kind (venomous and harmless
  snakes, dangerous and harmless large mammals).
- The lens's reports (its LLM-written cards, written on save) beside these numbers.
- Which way leads in sentences: a later study.
