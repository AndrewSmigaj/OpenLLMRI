# Objects: harmful, dual-purpose and benign (lens slice 1c, 10d.6, 2026-10-09)

Related: data/sentence_sets/lexical/objects_harm_v1.md (the set, its classes and its audits),
docs/DESIGN.md (C1 single-word sets, C3 hold-out designs, C4 tuning, C8 the axes analysis),
docs/research/animals.md (the animal lens, and words that split), docs/studies/objects_harm/study.yaml

Does the model keep harmful, dual-purpose and benign objects apart in domains it was never fitted
on, and where do the dual-purpose objects sit between harmful and benign? Every number here comes
from the files listed at the end, and was re-read from them at every layer it names.

## The capture

- **The set:** `objects_harm_v1`, 321 one-word object names: 98 harmful, 96 dual-purpose, 127
  benign, in 19 domains, each with how it harms. 80% of harmful names split into several tokens,
  68% of dual-purpose ones and 79% of benign ones; mean length is 7.4 to 7.5 letters in each class.
- **The run:** `session_2be574c4`, the date pinned to 2026-09-16, nothing generated. 321 of 321
  written, none dropped, each read at the user's word (split names at their last token).
- **Held out by domain:** the set declares its families (`metadata.holdout`: the domain, whole
  names). A domain holds several classes, so the folds hold out whole domains grouped across the
  classes; weapons live in a few domains (82 of the 98 harmful objects are in the armoury,
  military, and police and prison domains), so each fold's class mix differs from the rest's.

## Three classes in unseen domains: hardly at all

- **`objects-k3-n15`** (k 3, 15 neighbours, 6-D), held out on 5 grouped folds of whole domains:
  the class is read at AMI −0.01 to 0.18 (best at L11, κ 0.21), and κ is below zero at 19 of the
  24 layers: in a held-out domain, the nodes' classes from the other domains predict worse than
  chance. The token count is read at AMI 0.58 to 0.84 at L0 to L8 and 0.61 to 0.80 at L17 to L23,
  and less in between (0.09 to 0.54 at L9 to L16).
- **`objects-k3-n15-tuned`**, tuned on the class with 79 objects of whole domains as the test
  portion: test AMI at most 0.27 (L11), above 0.15 only at L5, L8 and L10 to L12. Tuning beat the
  untuned lens at 15 layers and lost at 8.
- **The ceiling,** a logistic probe on the raw states trained on the labels, reaches only 0.16 to
  0.35 test AMI (κ 0.18 to 0.43) on the same held-out domains. So the three-way split hardly
  carries over to a new domain even linearly: what the model holds for "harmful", "dual-purpose"
  and "benign" leans on the domains it was learned in.
- **The axes analysis** (held out on the lens's folds, against decoys) agrees: a probe reads the
  class at κ 0.30 to 0.60 (best at L17) and how it harms at 0.28 to 0.61 (best at L4); the lens's
  nodes reach the class at −0.10 to 0.28; the token count is read at 0.98 to 1.00 by the probe and
  0.43 to 1.00 by the nodes. The node details flag nodes by their token count at 21 of 24 layers.

## Two ends of an axis: clearly

A mass-mean lens, **`harm-axis`**, puts benign objects at −1 and harmful ones at +1 at every layer,
fitted on those two classes only and validated on the same grouped folds of whole domains:

- held-out accuracy 0.90 or more from L4 to L15 (0.93 at L5 and L11, κ 0.78), against 0.62 at L0
  and 0.74 to 0.76 at L19 and L20. Harmful and benign do separate in unseen domains along one
  direction;
- at L9 to L12 the axis, pushed through the next layer's router, moves the routing more than 97 to
  100% of 1,000 random directions of the same length (2.06 times their median at L11): the
  routers single harm out there, and only there;
- through the logit lens, the harmful side favours " Weapons", " devastating", " retaliation", "
  violence", " weapon" and the Chinese for weapon and attack at L11, and nothing but forms of
  "weapon" at L23; the benign side favours " topper", " stitching", " dressing", " cozy", "
  comforting", " upholstery" at L23.

## Where the dual-purpose objects sit

The dual-purpose objects were never fitted, so their readings are the measurement
(`analysis/harm_axis.py`):

- **In between, at every layer:** their median runs from −0.29 (L23) to +0.17 (L2), against
  harmful medians of 0.91 to 1.19 and benign medians of −1.05 to −0.93 (those two are fitted, so
  near ±1 by construction). Between 39 and 56 of the 96 sit on the harmful side of zero.
- **Spread by kind, at L5** (where the axis separates its classes best held out): the most harmful
  readings are the machete (+1.40), javelin (+1.39), fentanyl (+1.26), oxycodone (+1.18), epee
  (+1.14), nail gun (+1.10), dynamite (+1.03) and tranquilizer (+0.99), at or beyond the harmful
  class's median (+1.03 at L5);
  the most benign are the airplane (−0.87), tractor (−0.86), rope (−0.83), matchstick (−0.76),
  lawnmower (−0.75), car (−0.68), mothballs (−0.62) and cord (−0.60).
- **By how they harm, at L5:** projectile +0.58 (the slingshot alone), explosive +0.43, chemical
  +0.22, fire +0.11, piercing −0.03, cutting −0.07, blunt −0.27, restraint −0.46. By domain: medical
  +0.52 (drugs, and the scalpel, syringe, needle and lancet), sport +0.43 (javelin, epee, dart,
  discus), laboratory +0.22 at the harmful end; transport −0.40 and household −0.19 at the benign
  end.

So the axis sorts the dual-purpose objects by how weapon-like or drug-like they are: weapons in
shape or use (machete, javelin, epee), opioids and sedatives, and blasting explosives read as
harmful; vehicles, binding materials and everyday tools read as benign, though cars and ropes harm
in practice.

## Words that split

As with the animals, the token count is one of the strongest things in every object lens (above),
and it is strongest early and late, weaker at L9 to L16. The harmful class splits as often as the
benign one (80% and 79%), so the class differences above aren't the token count's; but every
UMAP lens on this capture spends its early and late nodes on it. The proposal in
RECOMMENDATIONS.md (read each word at the token after it) applies here too.

## Files

- The set: `data/sentence_sets/lexical/objects_harm_v1.json` and its guide; the audit
  `docs/studies/objects_harm/analysis/audit_set.py` (0 problems, 2026-10-09).
- The capture: `data/lake/session_2be574c4/` and `data/lake/_sessions/session_2be574c4.json`.
- The lenses: `data/lake/session_2be574c4/lenses/objects-k3-n15/` (`validation.json`),
  `objects-k3-n15-tuned/` (`search.json`, `validation.json`, `axes.json`, `details/`) and
  `harm-axis/` (`validation.json`, `details/`); the saved version in
  `data/lenses/session_2be574c4/objects-k3-n15-tuned/`.
- The readings: `docs/studies/objects_harm/analysis/harm_axis.py`, `results/harm_axis_harm-axis.json`
  and `figures/harm_axis_harm-axis.png`; in the app, Build › harm-axis › results › Readings.
