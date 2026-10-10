# Kinship or way of life (lens slice 1c's showcase)

One figure from lens slice 1c (`docs/DESIGN.md` K): `animals_showcase.png`, published with this note at
https://claude.ai/artifact/FfBovETJhN9NYJvxKzA9WS. It is made from the app's own
exports and the study's analysis figures. The figure's `recipe` chunk and `recipe.json` hold each
panel's recipe: for the app's panels, the view's link, the lens and its settings and the commits it
was served at; for the analysis panels, the script, its results file and the command that drew it.
The app's panels are in `panels/`; `compose.py` lays everything out, trims the 3-D views to their
drawing and crops the split-word figure to its first two rows:

    .venv/bin/python docs/studies/animals/showcase/compose.py

The runs behind the numbers are in `docs/research/animals.md` and `docs/research/objects_harm.md`;
the studies are `docs/studies/animals/study.yaml` and `docs/studies/objects_harm/study.yaml`. Every
number below was read from the lens files, the analyses' results or the API.

## What it shows

**A. The animal lens over all 24 layers** (`session_6e485e10`, `animals-k8-n15-tuned`).
- **The items:** 524 one-word animal names in 8 groups, each given alone with a space first
  (" lion"); 430 of them split into several tokens and are read at their last token.
- **The lens:** tuned on the group with whole taxonomic orders held out, k 6 to 10 per layer.
  Colour is the group. On 36 held-out orders its test AMI peaks at 0.36 (L6).
- **The dolphin's path is lit.** " dolphin" is one token, and its path rides the node of one-token
  names at every layer but L13: 55 to 127 animals, 70 to 100% of them one-token names and only 37 to
  60% mammals. At L13 it joins a node of 22 animals, 68% of them other invertebrates.

**B. Taxonomic neighbourhoods.** The share of each animal's 10 nearest neighbours sharing its group,
class, order, family and genus, against the taxonomy shuffled.
- At L6 to L13, 67 to 71% of neighbours share the group in the lens (chance 20%), 20 to 23% the
  order (chance 3%) and 6 to 7% the family (chance 1%).
- In raw space the group's share is already 0.64 at L2; in the lens it rises to 0.70 by L6. Both
  dip at L18 to L20.

**C. Kinship or way of life.** 33 animals whose way of life is another group's: swimming and
flying mammals, birds that don't fly, animals named "fish", legless animals, the mudskipper.
- **The index:** above zero when an animal's neighbours lean to its kin without its trait (for a
  dolphin, mammals that don't swim) rather than to look-alikes from other groups (non-mammals that
  swim). The grey band shuffles positions 1,000 times.
- **Every kind leans to kin,** and none to its look-alikes beyond chance at any layer. Swimming
  mammals lean to kin beyond chance at 18 lens layers and 20 raw; counted within each token count,
  at the same layers.
- **Animal by animal, the whales are the exception:** the humpback leans to fish at 12 lens layers,
  and the eel sits with the snakes in raw space at L10 to L18.

**D. One layer, previewed** in the build form (L6, k 8, held out on whole orders: the group's AMI
0.36, the token count's κ 0.96).
- **The same 3-D view twice:** coloured by group, then by whether the name split. The 94 one-token
  names form an island of their own.
- **Then the dolphin's path** in the lens's own space at L6 to L12: it runs along that island.

**E. Words that split,** in the lens's space and in raw space.
- **The last piece pulls, early and late:** the 23 names ending in "fish" have 99 to 100% of their
  neighbours ending in "fish" at L0 in the lens. In raw space that share falls lowest at L8 to L13
  and rises again at L20 to L23: a U across the layers.
- **The token count splits the space at every layer:** a probe tells one token from several at
  0.96 or more, and one-token names' neighbours are 86 to 100% one-token names (chance 18%).
- **Kinship holds within that split:** split names have 61 to 77% of their neighbours in their own
  group at L4 to L17.

**F. The harm axis on 321 objects** (`session_2be574c4`, `harm-axis`).
- **The axis:** benign at −1 and harmful at +1. Held out by whole domains, its accuracy is 0.90 or
  more at L4 to L15.
- **The dual-purpose objects,** never fitted, sit between the two ends at every layer (median −0.29
  to +0.17). At L5 the machete, javelin, fentanyl and oxycodone read near the harmful end; the
  airplane, tractor and rope near the benign one.

**G. Comparing lenses on the animals.** Held-out AMI on the group per layer for the untuned lens
(k 8) and the tuned one, with the tuned lens's score on the 119 test animals its search never saw
and its source lens's on the same animals. Tuning is better at 10 layers and worse at 14.

## What it means for the design

Reading a split name at its last token lets every animal and object in, but it doesn't make the read
site neutral. A word's last piece is a word-internal token, and a one-token word is a whole word
with its space; the two read differently at every layer, and every UMAP lens on these captures
spends nodes on that difference. Kinship and harm show within each kind of name, and on a single
axis harm carries over to domains the lens never saw. `docs/RECOMMENDATIONS.md` (2026-10-09)
proposes reading each word at the token after it, the same token for every item.
