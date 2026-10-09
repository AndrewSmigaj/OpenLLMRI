# The lens core's showcase (lens slice 1)

One figure from lens slice 1 (`docs/DESIGN.md` K), made from the app's own exports:
`lens_core_showcase.png`. The figure's `recipe` chunk and `recipe.json` hold each panel's recipe:
the view's link, the lens and its settings, and the commits it was built and served at. The panels
are in `panels/`, and `compose.py` lays them out:

    .venv/bin/python docs/studies/lens_core/showcase/compose.py

The runs behind the numbers are in `docs/research/lens_core_validation.md`, and the study is
`docs/studies/lens_core/study.yaml`. Every number below was read from the lens files or the API.

## What it shows

**A. The tank lens over all 24 layers** (`session_1434a9be`, `tank-k5-n15`, k 5 at every layer;
499 sentences, 100 per sense, 99 for scuba). From L9 to L16, vehicle, clothing and aquarium each
hold a nearly pure node (79% to 100% one sense). Septic and scuba share a node from L8 to L13
(at L13, 91 septic and 71 scuba sentences in a node of 191). From L17 on, aquarium shares its
node with septic and scuba (at L23, 63 aquarium, 50 septic and 46 scuba in a node of 161): the
three senses in which a tank holds something. Vehicle and clothing keep nodes of their own to the
last layer (vehicle's takes in 23 scuba sentences at L22). Held out, the senses separate most at
L11 to L13 (κ 0.60, 0.57 and 0.62). The outlined nodes hold items that the better raw-space
grouping puts with different neighbours: about half the items at a typical layer, from 14% at L4
to 91% at L2. The two instruments score alike against the senses (within about 0.1 κ) but group
the items differently.

**B. Where the senses separate, and what the methods suggest.** The k profile scores every k
from 2 to 10 on held-out items at every layer. The in-sample methods, which don't see the labels,
never settle on five: the elbow picks 2 at 20 of 24 layers, silhouette ranges from 2 to 8, and
the hierarchy levels include 5 only at L18 and L19. The held-out best k is 7 to 10 at every
layer, and is selection-biased (the best of nine scores on the same folds). So k is chosen from
the profile; better automatic methods stay open (DESIGN.md C3).

**C. The calibration axis matches the paper.** The aquarium-against-vehicle mass-mean axis on
`session_29a80932`, held out by scene family in 12 folds, scores accuracy 0.905 at L4: the
paper's figure, exactly. The two-cluster UMAP lens on the same capture peaks at 0.86 (L5).

**D. Two axes in one colour.** On the threatened set (`session_673360a5`,
`framing-k4-auto-levels`, k 2 to 8 per layer from the hierarchy levels), hue shows the frame
(roleplay or factual) and lightness shows the voice (active or passive). Voice organizes the nodes
first (AMI 0.98 at L1). From L4 to L7 the frame alone does (0.53 to 0.57, voice 0). From L9 to
L21 both do (frame 0.42 to 0.60, voice mostly 0.36 to 0.44). At L22 and L23 the frame alone
remains (0.86 and 0.87, with two nodes each).

**E. Expert fingerprints by sense.** On the tank set, the mean gate weight on each expert at each
layer (the model's own top four), aquarium sentences minus vehicle sentences. The two senses' routing
differs most at L4 to L5 and L10 to L12, where 0.26 to 0.31 of the gate weight goes to different
experts (total variation). It differs least at L13 and L23 (0.07 and 0.06). The largest single
difference is expert 15 at L10: 0.34 of the aquarium sentences' gate weight, 0.10 of the vehicle
sentences'.

**F. The routers aren't tuned to this contrast.** C's axis, pushed through each next layer's
router, moves routing less than the median random direction of the same length at 19 of 23
layers. It never goes beyond the random 95th percentile: its peak, 1.26 times the median at L10
and L11, is the 94th. From L13 to L20 it sits at 0.19 to 0.59 times the median. The senses still
route differently (E); what F adds is that the routers respond to this direction no more than to
a random one. On the tank lens, the nodes explain 0.11 (L1) to 0.49 (L11) of the next layer's
routing variance.

## Caveats

- The tank set has no scene families, so its held-out scores come from weaker folds.
- One model and three captures; these are first readings of the instrument.
- The frame × voice lens is an unsaved draft whose k came from one automatic method.
