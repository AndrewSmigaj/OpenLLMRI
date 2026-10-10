# Where a single word is read: its last token or the end marker after it (2026-10-09)

Related: docs/DESIGN.md (C1 single-word sets and split words; Part L, question 16),
docs/research/animals.md and docs/research/objects_harm.md (the two sets read at the last token),
docs/studies/read_site/study.yaml, docs/RECOMMENDATIONS.md

Lens slice 1c reads a single word at its last token. On both of its sets, one-token and split names
then sit apart at every layer. The proposal for a ruling (DESIGN.md, Part L, question 16) was to
read every word at the token after it instead: the message's end marker `<|end|>`. It is the same
token for every item, and it comes after all of the word's tokens. This note tests that proposal on
both sets. Every number here comes from the files listed at the end, and was re-read from them at
every layer it names.

## The captures

- **Both sets again, with a second site.** `animals_kinship_v1` (`session_5ce62b52`, 524 of 524
  items written) and `objects_harm_v1` (`session_079e85fb`, 321 of 321 items), with the chat
  template's date pinned to 2026-09-16 as before and nothing generated. Each capture also stored the
  end marker as a second site (position 2), beside the word's own site (position 1). No code
  changed: the capture already stores a second site, and a lens takes the position it reads.
- **The end marker comes right after the word** in every item: the message holds only the word.
- **The read site is the only difference.** At the word's own site, both new captures equal the
  earlier ones (`session_6e485e10`, `session_2be574c4`) bit for bit at all 24 layers.
- **The same lenses at both sites,** with the same settings, seed, items and folds:
  - animals: k 8, 15 neighbours, 6-D, held out on 12 folds of whole orders (`animals-k8-n15`,
    `animals-end-k8-n15`);
  - objects: k 3, held out on 5 grouped folds of whole domains (`objects-k3-n15`,
    `objects-end-k3-n15`);
  - the harm axis, benign at −1 and harmful at +1, on the same folds (`harm-axis`,
    `harm-axis-end`).

  Each was validated and given the axes analysis, and the studies' scripts ran on both sites.

## Whether the word split: still readable at the end marker

Every layer unless the cell names layers.

| Measure | last token | end marker |
|---|---|---|
| animals: share of a one-token name's 10 nearest neighbours that are one-token names, lens (chance 0.18) | 0.92 to 1.00 | 0.87 to 1.00 at L0–L12, 0.66 to 0.91 at L13–L23 |
| the same, raw space | 0.89 to 1.00 | 0.85 to 1.00 at L0–L12, 0.76 to 0.89 at L13–L23 |
| animals: a probe on one token against several, raw space (balanced accuracy) | 0.99 to 1.00 | 0.99 to 1.00 |
| animals: the lens's nodes on the token count, held out (κ) | 0.83 to 1.00 | 0.86 to 1.00 at L0–L12, 0.39 to 0.81 at L13–L23 |
| objects: the lens's nodes on the token count, held out (κ) | 0.79 to 1.00 at L0–L8, 0.00 to 0.71 at L9–L16, 0.95 to 0.98 at L17–L23 | 0.90 to 1.00 at L0–L5, 0.32 to 0.72 at L6–L19, 0.00 to 0.13 at L20–L23 |

- **One-token and split names remain distinguishable at the end marker.** A raw-space probe tells
  them apart at 0.99 or more at every layer, one-token animal names keep 0.66 or more one-token
  neighbours (chance 0.18), and through L12 the animal lens's nodes follow the token count as
  closely as at the last token. In the animal lens it weakens only from L13 on, in the object lens
  from L6.
- **What this design can't tell apart:** the end marker sits one position later for every extra
  token, so whether the word split and how far into the message the marker sits can't be told
  apart here.
- **The "-fish" names group by their last token much less.** At the last token, the 18 fish whose
  names end in "fish" have 0.76 to 0.90 of their raw-space neighbours ending in "fish" at L17 to
  L23; at the end marker, 0.14 to 0.23 (chance 0.04). In the early layers the share falls fast at
  the end marker (0.98 at L0, 0.43 at L3).

## The word's meaning: much weaker at the end marker

| Measure | last token | end marker |
|---|---|---|
| animals: neighbours sharing the group, lens, L4–L17 (chance 0.20) | 0.58 to 0.71 | 0.25 to 0.32 |
| the same, raw space, L4–L17 | 0.61 to 0.71 | 0.29 to 0.40 |
| animals: the group on held-out orders, the lens's nodes (AMI) | 0.07 to 0.40 (0.32 to 0.40 at L5–L13) | 0.00 to 0.10 |
| animals: the group, a logistic probe held out (the ceiling, AMI) | 0.45 to 0.82 (0.71 to 0.82 at L2–L19) | 0.07 to 0.57 (0.07 to 0.20 at L0–L3) |
| objects: the harm axis on held-out domains (accuracy, chance 0.50) | 0.62 to 0.85 at L0–L3, 0.90 to 0.93 at L4–L15, 0.74 to 0.90 at L16–L23 | 0.52 to 0.57 at L0–L3, 0.65 to 0.88 at L4–L10, 0.91 at L11, 0.57 to 0.87 at L12–L23 |
| objects: three classes on held-out domains, the lens's nodes (AMI) | −0.01 to 0.18 | −0.01 to 0.04 |

- **Little of the word is read at the end marker in the early layers.** At L0 to L3 the logistic
  ceiling reads the animal's group at AMI 0.07 to 0.20, and the harm axis is at 0.52 to 0.57
  accuracy (chance 0.50). Harm is read well there only at L10 to L12 (0.87 to 0.91), where the last
  token reads it at 0.90 or more from L4 to L15. The group's ceiling peaks at 0.57 at the end marker,
  against 0.82 at the last token.
- **The lens's nodes follow the group much less** (AMI at most 0.10, against up to 0.40); through
  L12 they follow the token count as closely as at the last token (κ 0.86 to 1.00).
- **Kinship or way of life:** the layers, of 24, where a kind's nearest neighbours are its kin more
  often than chance (the lens, all names):

  | Kind | last token | end marker |
  |---|---|---|
  | mammals that swim (16) | 21 | 7 |
  | mammals that fly (2) | 18 | 5 |
  | birds that don't fly (6) | 10 | 1 |
  | named "fish", not fish (5) | 14 | 18 |
  | legless, not snakes (3) | 6 | 1 |
  | a fish that walks (1) | 22 | 8 |

  At the end marker the legless animals (eel, caecilian, slowworm) lean to their look-alikes, the
  snakes, at L17 to L20 in the lens and at L14 and L16 to L21 in raw space; at the last token only at
  L3 and L17 in the lens. Only the animals named "fish" lean to kin at more layers at the end
  marker (18 against 14).
- **The dual-purpose objects:**
  - their median sits between the harmful and benign medians at every layer at the end marker
    (−0.85 at L23 to +0.56 at L6), but the objects are ordered differently;
  - at the end marker's best layer (L11) the most harmful readings are drugs and chemicals:
    fentanyl +2.10, ketamine +2.08, thermite +2.01, oxycodone +2.00, warfarin +1.89 and chloroform
    +1.87, beyond the harmful median (+0.94). The most benign are vehicles, wire and chain: the car
    −1.91, airplane −1.16, bus −1.05, wire −1.05, motorcycle −0.99 and chain −0.86;
  - at the last token's best layer (L5) the most harmful readings were weapon-shaped objects and
    opioids: the machete +1.40, javelin +1.39, fentanyl +1.26, oxycodone +1.18 and epee +1.14.

## What a linear probe reads at each site

Held out on the same folds (the axes analysis), a linear probe reads every attribute of meaning
less at the end marker, at each of the 20 layers from L4 to L23 (compared layer by layer), while
whether the name split is read at 0.98 to 1.00 at both sites. Mean κ over L4–L23, with its range:

| Attribute | last token | end marker |
|---|---|---|
| animals: group | 0.83 (0.79 to 0.87) | 0.59 (0.43 to 0.70) |
| animals: habitat | 0.74 (0.67 to 0.77) | 0.45 (0.35 to 0.58) |
| animals: movement | 0.71 (0.67 to 0.74) | 0.50 (0.39 to 0.63) |
| animals: wild or domestic | 0.54 (0.29 to 0.65) | 0.33 (0.19 to 0.52) |
| animals: diet | 0.43 (0.30 to 0.55) | 0.24 (0.12 to 0.36) |
| animals: whether the name split | 1.00 (0.99 to 1.00) | 1.00 (0.99 to 1.00) |
| objects: class (harmful, dual-purpose, benign) | 0.55 (0.47 to 0.60) | 0.48 (0.36 to 0.54) |
| objects: how it harms (9 kinds) | 0.57 (0.54 to 0.61) | 0.43 (0.32 to 0.52) |
| objects: whether the name split | 0.99 (0.98 to 1.00) | 1.00 (0.99 to 1.00) |

## What it means

- **The proposal is withdrawn.** At the end marker, one-token and split names remain
  distinguishable at every layer (by a raw-space probe at 0.99 or more), and the end marker's state
  carries less of the word: animals' neighbours share their group 25 to 40% of the time at L4–L17
  (chance 20%), the lens's nodes barely follow the group, a linear probe reads every attribute of
  meaning less at every layer from L4, and harm is read well only at L10 to L12.
- **The last token stays the read site** (DESIGN.md C1 as built). A linear probe reads every
  attribute of meaning better there at every layer from L4, and the divide is handled by the design
  of the set and of the analyses:
  - split names balanced across the classes, as both sets already are;
  - the token count recorded with every item (`target_token_count`), read by every lens's surface
    check, and declared as a category in both sets, so every validation scores it;
  - every claim that compares groups re-counted within each token count, as the kinship analysis
    already does;
  - a set of one-token words where a question needs neighbourhoods free of the divide.
- **Not tested here:** a plain token after the word (a full stop) instead of the special end
  marker, and whether the divide at the end marker comes from the word's tokens or from the
  marker's position.

## Files

- The captures: `data/lake/session_5ce62b52/` and `data/lake/session_079e85fb/`, with their
  `_sessions` files; the earlier ones, `session_6e485e10` and `session_2be574c4`.
- The lenses: `animals-end-k8-n15` (`validation.json`, `axes.json`), `objects-end-k3-n15`
  (`validation.json`, `axes.json`) and `harm-axis-end` (`validation.json`) beside their last-token
  counterparts `animals-k8-n15`, `objects-k3-n15` and `harm-axis` (each `axes.json` made on
  2026-10-09 for this comparison).
- The studies' scripts on the end-marker lenses: `docs/studies/animals/analysis/results/*_animals-end-k8-n15.json`
  and `docs/studies/objects_harm/analysis/results/harm_axis_harm-axis-end.json`, with their figures.
- The comparison: `docs/studies/read_site/analysis/compare_sites.py`, its
  `results/compare_sites.json` and `figures/compare_sites.png`.
