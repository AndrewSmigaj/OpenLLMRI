# Objects: harmful, dual-purpose and benign (v1) — set guide

Related: data/sentence_sets/GUIDE.md (set format and doctrine), docs/DESIGN.md (C1 single-word
sets, C3 hold-out designs), docs/studies/objects_harm/study.yaml (the study that uses it),
docs/studies/objects_harm/analysis/audit_set.py (the audit)

## Purpose

A lens of objects by the harm they can do (lens slice 1c, 10d.6). Harmful objects are made to harm;
benign ones are made for another use and rarely harm; dual-purpose objects are made for another use
but can harm (a knife, rope, bleach, a car). The lens shows whether the model keeps the three apart,
layer by layer, in domains it was never fitted on. A harmful-against-benign axis then reads where
each dual-purpose object sits between the two.

## The words, and words that split

- Each item's text is the object's name with a space first (`" sword"`), given alone as the user's
  message in the chat template. Its target word is the name itself.
- A name that splits into several tokens (" halberd" is three) is read at its last token, and the
  capture records how many tokens it took. The set records it as `categories.tokens`.
- Weapons' names split more often than everyday words, so a set of common words would tie harm to
  token count. Benign names were chosen to match: 80% of harmful names split, 79% of benign ones,
  68% of dual-purpose ones. Mean name length is 7.4 to 7.5 letters in every class.

## Design

| Attribute | Values | How it varies |
|---|---|---|
| label (the class) | harmful, dual, benign | the designed contrast |
| domain | 19: kitchen, workshop, garden, medical, military, armoury, hunting, police and prison, household, office, outdoors, transport, sport, toys, construction, laboratory, bathroom, clothing, celebration | where the object is found or used; held out whole in validation (`metadata.holdout`: families field `domain`, whole names) |
| harm | cutting, piercing, blunt, fire, explosive, chemical, projectile, restraint, none | how the object harms; `none` exactly for benign objects |
| tokens | one, several | the name's token count with a space first |

**The classes:**
- **harmful:** made to harm people or animals: weapons and their ammunition (sword, rifle, bullet,
  crossbow), poisons (cyanide, rodenticide, pesticide), explosives and incendiaries made as weapons
  (grenade, landmine, napalm), and restraints and instruments of punishment (handcuffs, noose,
  guillotine). Hunting weapons are harmful: they are made to kill animals.
- **dual:** made for another use but able to harm: blades and tools (knife, axe, chainsaw, scalpel),
  chemicals and fuels (bleach, lye, gasoline), drugs that harm in overdose (morphine, fentanyl,
  insulin), motor vehicles (car, truck, bulldozer), explosives for blasting or display (dynamite,
  firework), sport implements descended from weapons (javelin, epee) and binding materials (rope,
  chain, wire).
- **benign:** made for another use and rarely able to harm: tableware, linen and furniture,
  stationery, toys, clothing, sports gear, instruments of care, and the protective gear of the
  military domains (helmet, chainmail, breastplate).

**How it harms** is the object's main way: a sword cuts, a dagger pierces, a cudgel is blunt, a
rifle and a crossbow harm by what they shoot (projectile), a grenade explodes, napalm and a
blowtorch burn (fire), poisons, acids and drugs are chemical, and handcuffs, a noose and rope
restrain. Motor vehicles harm by impact (blunt).

## Domains and classes

Whole domains are held out, so each test asks whether the lens tells harm apart in a domain it was
never fitted on. Domains cross the classes, but unevenly: weapons live in a few domains.

| Domain | Harmful | Dual | Benign |
|---|---|---|---|
| armoury | 38 | 0 | 4 |
| military | 27 | 1 | 6 |
| police and prison | 17 | 0 | 2 |
| hunting | 7 | 3 | 4 |
| laboratory | 5 | 8 | 5 |
| garden | 2 | 10 | 8 |
| household | 2 | 15 | 12 |
| medical | 0 | 14 | 10 |
| workshop | 0 | 14 | 7 |
| transport | 0 | 8 | 5 |
| kitchen | 0 | 6 | 10 |
| construction | 0 | 6 | 4 |
| sport | 0 | 4 | 7 |
| outdoors | 0 | 3 | 6 |
| celebration | 0 | 3 | 5 |
| bathroom | 0 | 1 | 8 |
| clothing | 0 | 0 | 7 |
| office | 0 | 0 | 9 |
| toys | 0 | 0 | 8 |

A domain holds several classes of objects, so the folds hold out whole domains grouped across the
classes (the validation says so). Clothing, office and toys hold benign objects only.

**Known covariates:**
- **Domain and class go together:** 82 of the 98 harmful objects are in the armoury, military and
  police-and-prison domains. A node that holds weapons also holds those domains; the held-out
  domains show what carries over.
- **Historic weapons:** 38 harmful objects are historic arms (swords, polearms, siege engines),
  rarer words than most dual-purpose and benign ones.
- **Harm type follows class:** benign objects are all `none`, and projectiles are almost all
  harmful (25 of 26).

## Choosing the words

- One-word English names, lower case, no hyphens. Two-word names (pepper spray, letter opener,
  baseball bat) are left out.
- **Left out for a strong second sense:** mace (the spice, the spray), club, bat, racket, foil,
  shell, cartridge, mortar, iron, torch, match and lighter, saw and jigsaw, bow, bolt, quiver,
  sling, snare, rack, stocks, flail, pike, stiletto (the heel), baton (the relay and the
  conductor's), blackjack, sap, gag, muzzle, whip, cane, drill, train, flare, pillory (the verb),
  spade (the card suit), hoe, grinder, tank (its own study's word).
- **Left out as weak or doubtful harm:** brick, rebar, thumbtack, shredder, puck, kettlebell,
  barbell, hairspray, skillet, peeler, fertilizer.
- **Left out as near duplicates:** pocketknife (penknife is in) and lorry (truck); van went too,
  to bring the dual-purpose names' share of split words nearer the others'.
- Benign words were cut from a longer list to balance the classes and their token counts; the cut
  kept words that split.
- No word from the prompt's own text (the template's system block, and "assistant").

## Audits (2026-10-09, before the capture)

`docs/studies/objects_harm/analysis/audit_set.py` checks every entry and changes nothing: the
shape and axis values; duplicates; harm `none` exactly for benign objects; `tokens` against the
tokenizer; each entry through the sentence route's prompt and the real capture step (a stand-in
model), read at the user's word with its token count and offset; no name in the prompt outside the
user's message; counts per class, domain and harm.

Result: 321 objects, 0 problems.

| Class | Objects | Split | Mean length | Domains |
|---|---|---|---|---|
| harmful | 98 | 78 (80%) | 7.4 | 7 |
| dual | 96 | 65 (68%) | 7.5 | 14 |
| benign | 127 | 100 (79%) | 7.4 | 19 |

| Class | Cutting | Piercing | Blunt | Fire | Explosive | Chemical | Projectile | Restraint |
|---|---|---|---|---|---|---|---|---|
| harmful | 18 | 14 | 10 | 3 | 7 | 12 | 25 | 9 |
| dual | 21 | 15 | 19 | 7 | 7 | 22 | 1 | 4 |

The loader's validator warns on every item: a single word isn't 10 to 30 words, and each item's
target word differs from the file's. Its checks are advisory (GUIDE.md) and don't apply to this
shape.

## Capture

```bash
curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "objects_harm_v1", "session_name": "objects_harm_v1",
       "generate_output": false, "pin_date": "2026-09-16"}'
```

The date is the one the other lexical captures pinned. The route counts only the items it wrote
and returns the words it dropped; the count is checked against the set (321), and each item's
recorded token count against its `tokens`.

## Lenses

- The capture keeps the set's hold-out design (families field `domain`, whole names), so every lens
  on it holds out whole domains unless a request names another field.
- The class is the lens's label; harm and tokens are its other axes.
- **The harm axis:** a mass-mean lens with benign at −1 and harmful at +1 (the build keeps only those
  two classes), held out by domain, then read on its own capture: each dual-purpose object gets a
  position on the axis at every layer.
- No output axes: nothing is generated.
