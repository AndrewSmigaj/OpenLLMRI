# Who writes each split, attention or the experts: findings (2026-10-16)

Related: docs/studies/attention_experts/study.yaml (the study and its ledger),
docs/design/design.md (lenses: what comes with each split; the decision card L33),
docs/architecture/plan.md (phase 10g, step 6),
backend/src/services/lenses/writers.py (the same account for the node card, held for L33)

**Status:** exploratory: no prediction gates any analysis. Every number below is read from the
result files in `docs/studies/attention_experts/analysis/results/`, at the layers it names; the
scripts and figures sit beside them.

## The question

When a lens's classes or nodes part, which part of the model writes the difference into the read
token's state: attention, which moves information between positions (the token's own included), or
the experts, which transform the token's state where it is? And at which layers? This is the first part of LENS-30; its second part, the other
token positions that carry the same signal, waits for the extra positions slice 2 records.

## What was run

- **The account.** Each decoder layer of gpt-oss-20b adds two things to a token's state:
  attention's output and the experts' output (the gate-weighted sum of its four experts), nothing
  scaled. Every capture stores each layer's output and the experts' output at the read token, so
  attention's part at layer l is the layer's output minus the one before minus the experts' output;
  before layer 0 the state is the read token's row of the embedding table.
  - For two groups of items, the difference between their mean states at a target layer is exactly
    the embedding's part plus every layer's attention and experts parts up to it.
  - Projected on its own direction, the separation (the length of that difference) divides into
    shares that add up to one: the embedding's, and attention's and the experts' at each layer up
    to the target. A share can be negative: a part that narrows the split.
  - A share says who wrote the split into the state directly. The experts read the state after
    attention has added to it, so a split the experts write can still depend on what attention
    brought in.
- **Read against random splits.** In six of the seven captures the experts' part varies more from
  one item to the next than attention's, at every layer (1.08 to 15.4 times the variance), so the
  experts take most of any difference between groups, random ones included; in friend/foe the two
  vary about equally through L16 (0.87 to 1.60 times). Every share therefore stands beside the same
  share for 200 random splits of the same items (the same items shuffled into groups of the same
  sizes), as a band: the random splits' 5th, 50th and 95th percentiles. Random splits are drawn at the split's own grain: whole units (the Units
  column below) when no unit holds items of both groups, items otherwise. A share inside its band
  says nothing about who made the split. Each band leaves 5% of random splits on each side, so about
  one target in ten falls outside its band by chance, and neighbouring layers are not independent.
- **Seven captures,** each read through one lens's items and nodes:

  | Capture | Session | Lens | Items | Units | Read token |
  |---|---|---|---|---|---|
  | tank senses (sentences) | `session_1434a9be` | `tank-k5-n15` | 499 | texts | "tank", the same for all |
  | tank: aquarium or vehicle (sentences) | `session_29a80932` | `calibration-q1-k2-n15` | 600 | scenes (24) | "tank", the same for all |
  | roleplay or factual framing (sentences) | `session_673360a5` | `framing-k4-auto-levels` | 400 | texts | "threatened", the same for all |
  | friend or foe (agent runs, tick 1) | `session_b629b6c5` | `friend-foe-t1` | 479 | scenarios (248) | "person", 2 token forms |
  | single nouns | `session_8f536bea` | `words-k8-n15-tuned` | 861 | families (40) | 861 different |
  | single animal names | `session_5cd7091d` | `onto-k8-n15` | 524 | orders (171) | 381 different |
  | single object names | `session_2be574c4` | `objects-k3-n15-tuned` | 321 | domains (19) | 284 different |

- **Designed splits,** at every layer as the target: each label value against the rest (when a set
  has more than two), and the pairs the studies use: vehicle against aquarium, septic against
  aquarium, factual against roleplay, foe against friend, harmful against benign, and the animals
  that can kill against the harmless ones.
- **Node splits:** every branch of every split point of each lens's current version (the report
  cards' rule: branches holding at least max(5, 15%) of a node's items), against the node's other
  items, at the layer where they part. Random splits for node splits are drawn by item.
- **Checks:** each read token decodes to the end of its word; the most fp16 rounding could move the
  separation; a null for the separation from 1,000 random splits (only splits beyond its 95th
  percentile are summarized); intervals for the designed splits (the 5th to 95th percentiles of 500
  resamples of whole units); and a second direction (section 6).

Figures in `docs/studies/attention_experts/analysis/figures/`: `shares_by_layer.png`,
`two_directions.png`, `outside_bands.png`, `writing_layers.png`, `node_splits.png`; the numbers
quoted here are gathered in `results/summary.json` (`summary.py`) and `results/variance.json`
(`variance.py`).

## In short

- **The experts write most of every split, and a similar share of random splits of the same
  items.** From L4 to L20, the experts write 0.56 to 1.10 of the designed splits' separations, and
  random splits give them a median of 0.45 to 0.96, depending on the capture. Their share alone
  says little.
- **In the tank sentences, attention writes less of the senses' splits than of random splits of the
  same sentences, so the experts write more.** Along the mean difference, attention's share sits
  below its random band at 104 of the 119 split-and-layer targets from L4 to L20, and above it at
  none; along a second direction (the discriminant, section 6), below at 74; in both, at 67.
- **The other sets with context show no difference from random splits that holds in both
  directions.** Along the mean difference, attention's share sits below its band at 9, 5 and 4 of
  the 17 layers in the calibration scenes, the framing set and friend/foe; along the discriminant,
  at none.
- **In single words, the word's own embedding row writes most of the early split, then the
  experts; attention writes about what it writes for random splits.** Along the mean difference
  its share falls outside its band at about the rate chance gives, apart from a few splits; along
  the discriminant, at 6 of 323 targets.
- **The absolute shares depend on the direction they are measured along, and so do most marks.**
  Along the discriminant, attention's share in the sets with context is larger by a median of 0.13
  (up to 0.55). Of the 156 targets where the mean difference puts attention's share up to the
  target outside its band, 71 are outside along the discriminant too, 67 of them in the tank
  sentences, and none on the other side.
- **For node splits, few marks hold in both directions.** Along the mean difference, attention's
  share at the layer where a branch parts is outside its band at 197 of 662 branches; 26 of them
  are outside along the discriminant too, on the same side.

## 1. The checks

- **Read tokens:** every read token decodes to the end of its item's word, in all seven captures
  (0 mismatches).
- **The parts add up:** the embedding's, attention's and the experts' shares sum to one within
  0.0001 at every target.
- **Rounding:** the most fp16 rounding could move a designed split's separation is 5.4% of it
  (calibration's vehicle-against-aquarium split at L23). 4 of the 744 designed-split targets are
  above 5%: that one, and framing's factual-against-roleplay split at L0, L22 and L23 (5.1% to
  5.3%). The tank's largest is 2.25% (scuba against the rest, L20).
- **The separation's null:** every designed split is beyond its null at all 17 layers from L4 to
  L20, except two of the animal groups against the rest (amphibians and reptiles), which are beyond
  it at none and are left out below.

## 2. The experts write most of everything

Because the experts' part varies more from item to item (in friend/foe, about as much as
attention's), the experts take most of the separation of any two groups, random ones included, and
about half of it in friend/foe. From L4 to L20, over every designed split beyond its null:

| Capture | Designed splits: the experts' share | Random splits: the experts' median share |
|---|---|---|
| tank senses | 0.71 to 0.90 | 0.64 to 0.78 |
| tank: aquarium or vehicle | 0.83 to 0.96 | 0.76 to 0.87 |
| framing | 0.60 to 0.89 | 0.52 to 0.76 |
| friend or foe | 0.56 to 0.71 | 0.45 to 0.63 |
| single nouns | 0.57 to 0.98 | 0.61 to 0.95 |
| animal names | 0.74 to 1.10 | 0.69 to 0.96 |
| object names | 0.71 to 0.97 | 0.69 to 0.94 |

A share above one goes with a negative share elsewhere: the danger split's attention share at L20
is −0.095 (section 5). Because random splits give the experts a large share too, the sections below
read each split's attention share against its own band.

## 3. The tank sentences: attention writes less of the senses than of random splits

In the tank sentences every item is read at "tank", so the read token's embedding is the same for
all and adds nothing (its share is 0). Along the mean difference, attention's share sits below its
random band at 104 of the 119 targets from L4 to L20 (7 splits by 17 layers), and above it at
none; along the discriminant (section 6), below at 74 and above at none; below in both at 67:

| Split | Layers of L4 to L20 below the band: mean difference | discriminant |
|---|---|---|
| aquarium against the rest | 15 | 16 |
| clothing against the rest | 15 | 9 |
| scuba against the rest | 15 | 11 |
| septic against the rest | 9 | 8 |
| vehicle against the rest | 17 | 15 |
| vehicle against aquarium | 17 | 8 |
| septic against aquarium | 16 | 7 |

For vehicle against aquarium (100 sentences each):

| Layer | Separation (null's 95th percentile) | Attention's share (interval) | Random splits: 5th, median, 95th | The experts' share (random median) | Along the discriminant: attention's share (random 5th, median, 95th) |
|---|---|---|---|---|---|
| L4 | 137.2 (31.2) | 0.131 (0.117 to 0.156) | 0.149, 0.297, 0.445 | 0.869 (0.703) | 0.230 (0.247, 0.377, 0.467) |
| L8 | 387.6 (83.7) | 0.109 (0.100 to 0.124) | 0.139, 0.256, 0.363 | 0.891 (0.744) | 0.239 (0.224, 0.327, 0.387) |
| L12 | 737.9 (157.8) | 0.110 (0.104 to 0.122) | 0.145, 0.238, 0.328 | 0.890 (0.762) | 0.259 (0.182, 0.329, 0.443) |
| L16 | 1329.3 (333.7) | 0.116 (0.112 to 0.133) | 0.188, 0.277, 0.343 | 0.884 (0.723) | 0.208 (0.221, 0.338, 0.404) |
| L20 | 3114.7 (857.6) | 0.127 (0.112 to 0.154) | 0.224, 0.304, 0.357 | 0.874 (0.696) | 0.192 (0.247, 0.340, 0.401) |
| L23 | 6044.1 (1597.3) | 0.355 (0.299 to 0.405) | 0.208, 0.281, 0.432 | 0.645 (0.720) | 0.340 (0.229, 0.291, 0.364) |

At the last layer the pattern ends: attention's share (0.355) is inside its band, and the last
layer's own attention writes 0.167 of the separation there.

## 4. The other sets with context

In the calibration scenes (aquarium against vehicle, random splits drawn by whole scene), the
framing set and friend/foe, attention's share sits below its band at some layers along the mean
difference, and inside it at every layer along the discriminant. How far below is given as a share
of the band's width (its 95th percentile minus its 5th):

| Capture and split | Layers of L4 to L20 below the band (how far, in band widths) | Examples (attention's share; band) | Along the discriminant |
|---|---|---|---|
| calibration: vehicle against aquarium | 9 (0.01 to 0.11) | L12 0.135 (0.150 to 0.302); L16 0.087 (0.104 to 0.296) | inside at all 17 |
| framing: factual against roleplay | 5 (0.01 to 0.21) | L12 0.302 (0.315 to 0.459); L16 0.246 (0.264 to 0.410) | inside at all 17 |
| friend/foe: foe against friend | 4 (0.10 to 0.63) | L5 0.347 (0.460 to 0.640); L8 0.422 (0.441 to 0.626) | inside at all 17 |

None is above its band at any layer, along either direction. So in these sets no layer shows the
experts writing more of the split than of random differences along both directions. In friend/foe,
attention writes 0.29 to 0.44 of the split from L4 to L20, the largest share of the seven captures'
main splits at 11 of those 17 layers.

## 5. Single words: the embedding first, then the experts

A single word's own embedding row carries the early split, and its share falls fast:

| Split | L0 | L4 | L8 | L12 |
|---|---|---|---|---|
| single nouns: animal against the rest | 0.870 | 0.279 | 0.077 | 0.034 |
| object names: harmful against benign | 0.653 | 0.111 | 0.030 | 0.011 |
| animal names: can kill against harmless | 0.627 | 0.180 | 0.048 | 0.015 |

From L8 the experts write most of it (0.87 to 0.92 at L12 for these three). Attention's share
falls outside its band at about the rate chance gives (one target in ten), apart from a few splits:

- **single nouns:** above its band at 15 of 136 targets (place 6, emotion 5, tool 3, idea 1),
  below at 2 (animal);
- **animal names:** below at 17 of 119 (other invertebrates 11, can kill 3, birds 2, fish 1),
  above at none;
- **object names:** inside at all 68.

The danger split's attention share at L20 is −0.095, below its band (0.002 to 0.149): there,
attention narrows the split and the experts write more than all of it (1.095).

Along the discriminant, attention's share is outside its band at 6 of the 323 single-word targets,
all in the animal names (can kill 5, other invertebrates 1), and below it at each.

## 6. Two directions

The account measures each split along its own mean difference: the direction from one group's
mean state to the other's, the same direction a mass-mean lens uses. A second direction checks
whether the shares hinge on that choice: the split's shrinkage discriminant (the mean difference
weighed by the inverse of the groups' Ledoit-Wolf covariance, so that directions in which the items
within each group vary little count more), at every layer. Random splits are measured the same
way, each along its own discriminant in the same metric, so their bands compare.

- **In single words the two agree:** attention's share differs by a median of −0.004 between them,
  and by at most 0.049 at 90% of the 323 targets from L4 to L20 (at most 0.160).
- **In the sets with context they don't:** attention's share is larger along the discriminant by a
  median of 0.128 (−0.007 to 0.554 over 170 targets). For example, calibration at L20: 0.040 along
  the mean difference, 0.595 along the discriminant; friend/foe at L12: 0.398 and 0.683; framing
  at L16: 0.246 and 0.465; the tank's vehicle against aquarium at L12: 0.110 and 0.259. So
  attention's part lies more along directions in which the items within each group vary little,
  which the discriminant weighs up, and the experts' part more along directions in which they vary
  a lot.
- **Random splits move the same way, but not always as far:** in the sets with context their median
  attention share is larger along the discriminant by a median of 0.082 (up to 0.341), in single
  words by 0.001. Counting attention's share up to each target:
  - of the 493 targets, the two directions put the share in the same place at 399: inside its band
    at 328, below it at 71; at the other 94, one puts it outside and the other inside; at none is
    it above its band along one direction and below it along the other;
  - of the 156 targets the mean difference marks (outside its band), the discriminant marks 71 too:
    67 of 122 in the sets with context, all of them in the tank sentences, and 4 of 34 in single
    words.

So the absolute shares are a property of the direction chosen. Only the comparison with random
splits in the same direction should be read, and only a mark that holds in both directions says
something about the model rather than about the direction.

## 7. Where each split is written

At any target, most of a split was written by the layers shortly before it. The separations grow
with depth (the tank's vehicle against aquarium from 137 at L4 to 738 at L12 and 6,044 at L23), so
the later layers' parts are larger. At L12, the six layers L7 to L12 wrote 0.68 to 0.87 of the
seven main splits (attention and experts together), and the four layers L9 to L12 wrote 0.44 to
0.76; at L20, the four layers L17 to L20 wrote 0.60 to 0.84 (`writing_layers.png`).

## 8. Node splits

This section reads the 307 split points (of the 310 in the seven lens versions) that have a branch
beyond its separation null, at the layer where the branches part, along both directions. A node that splits
cleanly in two gives two branches that are mirror images of one split (55 of the 307 split points),
so split points are counted as well as branches. Every branch is beyond its separation null except
6 of the animal names' 169 and 11 of the object names' 173.

**What the parting layer writes.** The layer where the branches part writes a median of 0.20 to
0.47 of their separation there (attention and experts at that layer), most of it by the experts;
the rest was written before:

| Capture | Branches | The parting layer writes (median) | Its attention | Random splits' attention (median) | Its experts |
|---|---|---|---|---|---|
| tank senses | 70 | 0.333 | 0.046 | 0.085 | 0.286 |
| tank: aquarium or vehicle | 28 | 0.351 | 0.032 | 0.109 | 0.306 |
| framing | 52 | 0.475 | 0.163 | 0.202 | 0.281 |
| friend or foe | 42 | 0.363 | 0.151 | 0.176 | 0.208 |
| single nouns | 145 | 0.204 | 0.023 | 0.012 | 0.178 |
| animal names | 163 | 0.278 | 0.028 | 0.026 | 0.231 |
| object names | 162 | 0.230 | 0.016 | 0.014 | 0.209 |

**Against random splits, along each direction** (attention's share at the parting layer; branches
above, inside and below its band):

| Capture | Mean difference | Discriminant | Outside in both, same side | Split points outside along the mean difference, the discriminant, both |
|---|---|---|---|---|
| tank senses | 2, 39, 29 | 0, 70, 0 | 0 | 18, 0, 0 of 34 |
| tank: aquarium or vehicle | 0, 13, 15 | 0, 10, 18 | 9 | 8, 10, 5 of 14 |
| framing | 7, 40, 5 | 0, 52, 0 | 0 | 7, 0, 0 of 24 |
| friend or foe | 4, 33, 5 | 0, 42, 0 | 0 | 5, 0, 0 of 20 |
| single nouns | 41, 94, 10 | 19, 125, 1 | 14 | 32, 15, 10 of 70 |
| animal names | 26, 122, 15 | 0, 162, 1 | 1 | 29, 1, 1 of 73 |
| object names | 25, 124, 13 | 0, 159, 3 | 2 | 28, 2, 1 of 72 |

- **Along the mean difference** attention's share is outside its band at 197 of the 662 branches
  (127 of the 307 split points), three times the rate chance gives.
- **Along the discriminant** it is outside at 42 branches (6%, where chance gives 10%; 28 split
  points). Its random bands are also wider there: a median 1.05 to 1.96 times as wide as the mean
  difference's, depending on the capture.
- **In both:** 26 branches at 17 split points; no branch is above its band along one direction and
  below it along the other. In the calibration scenes, 5 of the 14 split points have attention
  writing less than random splits in both, all parting at L3 to L7. In the single nouns, 10 of the
  70 hold in both: at 9 attention writes more than random splits, and 7 of the 10 part at L18 to
  L23.
- **The tank's sense splits and its node splits differ:** along both directions attention writes
  less of the designed sense splits than of random splits at 67 targets (section 3), but none of
  the tank's node splits is outside its band along the discriminant.

So, counting attention's share at the parting layer, 26 of the 197 branches the mean difference
marks hold along the discriminant (13%, at 17 of the 127 marked split points); counting its share
up to the parting layer, 27 of 199 (14%). For the designed splits the marks hold more often: 71 of
156 for the share up to each target (46%), 54 of 138 for the share at the target layer itself
(39%).

The node card shows five shares (the embedding's, and attention's and the experts' at the parting
layer and up to it). Counting all five, at least one is outside its band at 487 of the 662 branches
along the mean difference, and at 74 along both directions on the same side. The shares counted
above (attention's up to each target for the designed splits, at the parting layer for the node
splits) never lie on opposite sides of their bands in the two directions. Among all the shares of
all the splits, 4 do: attention's and the experts' shares up to the parting layer at two node splits
in the single nouns (L7C1 and L7C2 into L8C1), the experts' share at L6 itself in the tank's
clothing split, and attention's share at L9 itself in the animals' danger split.

## Limits

- **Direct writers only.** The experts read the state after attention has added to it, so a split
  the experts write can still depend on what attention brought in. The account can't say what
  caused a split; steering or ablation would.
- **One read token.** Attention's part is what it moved into that token's state from every position
  it reads, the token itself included. In a one-word prompt the items differ only in the word, so
  there attention's part comes from the word's own token, or from its earlier pieces when it
  splits, not from context. Which other tokens carry a split first is LENS-30's second part.
- **The direction.** The absolute shares depend on the direction measured along (section 6).
- **Many comparisons.** About one target in ten falls outside its band by chance, and neighbouring
  layers are not independent, so a few outside-band layers in a split mean little.
- **Node splits are chosen by the data.** A lens finds its nodes from the states at the layer where
  they part, so a node split's direction is one the data picked; random splits of the same items
  aren't picked.
- **Rounding.** Up to 5.4% of a separation (section 1).

## For the node card

The node card (built and held, `backend/src/services/lenses/writers.py`) measures each split along
its mean difference in the residual stream at the lens's read site (the states the lens is fitted
on, and the axis a mass-mean lens uses), and marks every share outside its random band. In the
study, at least one of a branch's five shares would be marked at 487 of the 662 branches, and a
mark holds along the discriminant at 74 of them; for attention's share at the parting layer, 197
and 26. The card draws 100 random splits where the study drew 200, so its counts would differ a
little. How the node card should read them is
Andrew's call: card L33 on the design page.
