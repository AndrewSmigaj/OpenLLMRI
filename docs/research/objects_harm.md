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
  classes. Weapons live in a few domains (82 of the 98 harmful objects are in the armoury,
  military, and police and prison domains), so the domains are placed so that each class is about
  as common in every fold as overall (since 2026-10-16): in the worst held-out fold a class's share
  is 0.15 from its overall share, and in the worst training portion 0.04. Before, one fold held 55
  of the 98 harmful objects, and its training portion was only 18% harmful.

## Three classes in unseen domains: read linearly, hardly by the lens's nodes

Re-scored 2026-10-16, on folds that keep each class about as common in every fold as overall and
with the tuning tested on five test portions instead of one. The earlier numbers came from folds,
and a test portion, whose class mix differed from the rest's.

- **`objects-k3-n15`** (k 3, 15 neighbours, 6-D), held out on 5 grouped folds of whole domains:
  the class is read at AMI 0.01 to 0.16 (best at L11, κ 0.27), and κ is below zero at 7 of the 24
  layers (L0, L1, L3, L18, L19, L21 and L22, at most 0.04 below): there, the nodes' classes from
  the other domains predict no better than chance. With the earlier, unbalanced folds κ was below
  zero at 19 layers. The token count is read at AMI 0.55 to 0.85 at L0 to L8 and 0.62 to 0.80 at
  L17 to L23, and less in between (0.10 to 0.54 at L9 to L16).
- **`objects-k3-n15-tuned-v2`**, tuned again on the class. Its five test portions are the five
  balanced folds of whole domains in turn (33 to 96 objects each), and the lens itself comes from
  the first (45 objects). On the first portion its test AMI is at most 0.22 (L6, κ 0.31) and above
  0.15 at 14 layers; over the five portions its mean test AMI peaks at 0.20 (L7; 0.14 to 0.25
  across the portions). It beats the untuned settings at 15 layers on the first portion, and at 23
  of 24 on the mean over all five. The earlier `objects-k3-n15-tuned` was tested on one portion of
  79 objects with a skewed class mix (test AMI at most 0.27, at L11).
- **The ceiling,** a logistic probe on the raw states trained on the labels, reads the class on the
  held-out domains at a mean test AMI of 0.21 to 0.51 over the five portions (κ 0.44 to 0.70),
  best at L12 (0.40 to 0.66 across the portions). On the earlier, skewed test portion it read only
  0.16 to 0.35. So the three-way split does carry over to unseen domains linearly, moderately; it
  is the lens's nodes that hardly follow it.
- **The axes analysis** on `objects-k3-n15-tuned` (held out on its balanced folds, against decoys
  drawn within each class) agrees: a probe reads the class at κ 0.42 to 0.70 (best at L12) and how
  it harms at 0.31 to 0.65 (best at L4); the lens's nodes reach the class at −0.005 to 0.38; the
  token count is read at 1.00 by the probe at every layer and 0.49 to 1.00 by the nodes. The node
  details flag nodes by their token count at 21 of 24 layers.

## Two ends of an axis: clearly

A mass-mean lens, **`harm-axis`**, puts benign objects at −1 and harmful ones at +1 at every layer,
fitted on those two classes only. Validated on the balanced folds of whole domains as
`harm-axis-v2` (the same axis, bit for bit; 2026-10-16):

- held-out accuracy 0.90 or more at L4 to L14 and L16 (0.898 at L15), best at L7 (0.947, κ 0.88),
  against 0.66 at L0 and 0.78 to 0.79 at L19 and L20. Harmful and benign do separate in unseen
  domains along one direction;
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
- **Spread by kind, at L7** (where the axis separates its classes best held out; L5 before the
  balanced folds): the most harmful readings are fentanyl (+1.75), the javelin (+1.29), machete
  (+1.19), ketamine (+1.16), oxycodone (+1.15), dynamite (+1.10), epee (+1.06) and barbiturate
  (+1.04), at or beyond the harmful class's median (+1.01 at L7); the most benign are the
  lawnmower (−0.84), grater (−0.77), rope (−0.76), tractor (−0.75), syringe (−0.71), matchstick
  (−0.69), airplane (−0.62), screwdriver (−0.56) and bus (−0.56).
- **By how they harm, at L7:** projectile +0.43 (the slingshot alone), chemical +0.42, explosive
  +0.36, fire +0.19, cutting +0.18, piercing −0.02, blunt −0.26, restraint −0.35. By domain:
  medical +0.62, laboratory +0.56, construction +0.39, military and sport +0.36 at the harmful end;
  transport −0.41 and bathroom −0.53 at the benign end.

So the axis sorts the dual-purpose objects by how drug-like or weapon-like they are: opioids and
sedatives, weapons in shape or use (javelin, machete, epee) and blasting explosives read as
harmful; everyday tools, rope and vehicles read as benign, though ropes and vehicles harm in
practice.

## Words that split

As with the animals, the token count is one of the strongest things in every object lens (above),
and it is strongest early and late, weaker at L9 to L16. The harmful class splits as often as the
benign one (80% and 79%), so the class differences above aren't the token count's; but every
UMAP lens on this capture spends its early and late nodes on it. Reading each word at the token
after it doesn't help: tested on both sets in `docs/research/read_site.md`.

## Files

- The set: `data/sentence_sets/lexical/objects_harm_v1.json` and its guide; the audit
  `docs/studies/objects_harm/analysis/audit_set.py` (0 problems, 2026-10-09).
- The capture: `data/lake/session_2be574c4/` and `data/lake/_sessions/session_2be574c4.json`.
- The lenses: `data/lake/session_2be574c4/lenses/objects-k3-n15/` (`validation.json`),
  `objects-k3-n15-tuned/` (`search.json`, `validation.json`, `axes.json`, `details/`),
  `objects-k3-n15-tuned-v2/` (`search.json` with its five draws, `validation.json`), `harm-axis/`
  (`details/`) and `harm-axis-v2/` (`validation.json`, on the balanced folds); the saved version in
  `data/lenses/session_2be574c4/objects-k3-n15-tuned/`.
- The readings: `docs/studies/objects_harm/analysis/harm_axis.py`, `results/harm_axis_harm-axis-v2.json`
  and `figures/harm_axis_harm-axis-v2.png` (the earlier `harm_axis_harm-axis.*` ranked them at L5);
  in the app, Build › harm-axis-v2 › results › Readings.
