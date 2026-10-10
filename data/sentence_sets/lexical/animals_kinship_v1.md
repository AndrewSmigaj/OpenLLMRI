# Animals: kinship and way of life (v1) — set guide

Related: data/sentence_sets/GUIDE.md (set format and doctrine), docs/DESIGN.md (C1 single-word
sets, C3 hold-out designs), docs/studies/animals/study.yaml (the study that uses it),
docs/studies/animals/analysis/audit_set.py (the audit)

## Purpose

One lens for all the animals (lens slice 1c, 10d.5). Each animal carries two kinds of knowledge:
its kinship (its group, and its taxonomy down to the genus) and its way of life (where it lives,
how it moves, what it eats, whether people keep it). Some animals' kinship and way of life
disagree: a dolphin is a mammal that lives like a fish, a bat a mammal that flies. Read layer by
layer, the lens shows which of the two the model groups animals by, and where that changes.

## The words, and words that split

- Each item's text is the animal's name with a space first (`" lion"`), given alone as the user's
  message in the chat template. Its target word is the name itself.
- Most animal names split into several tokens (" jaguar" is " jag" + "uar"). The capture reads a
  name that splits at its last token, which has taken in the whole word, and records how many
  tokens it took (`target_token_count`). The set records the same as `categories.tokens` (one or
  several), so every lens can be checked for grouping by token count.
- Split names are balanced across the groups as far as the names allow: 75% of mammals split, and
  80 to 87% of every other group.
- Names that end in the same piece ("goldfish", "catfish", "starfish", "jellyfish") may group by
  that piece in early layers. The study measures it.

## Design

| Attribute | Values | How it varies |
|---|---|---|
| label (the group) | mammal, bird, reptile, amphibian, fish, insect, arachnid, other_invertebrate | follows from the class in the Catalogue of Life (below); eight, so no two groups share a colour in the app's palette |
| order | 171 names (Carnivora, Passeriformes, Squamata …) | the families held out whole in validation (`metadata.holdout`: families field `order`, whole names) |
| habitat | land, fresh water, sea, land and water | crosses the groups where animals allow (below) |
| movement | walks, flies, swims, crawls, stays put | as above |
| diet | carnivore, herbivore, omnivore | as above |
| wild_or_domestic | wild, domestic | domestic animals are mammals, birds, fish and two insects |
| tokens | one, several | the name's token count with a space first |

**Taxonomy**, in each entry's `taxonomy` object beside its categories: the accepted scientific
name and its rank, then phylum, class, order, family and genus.
- It stays out of the categories on purpose. Every category is a designed axis in the app's
  charts, reports and tests, and genus alone has hundreds of values.
- The capture records only the categories, so analyses read the taxonomy from this file by the
  item's text (each text is unique).

### The taxonomy's source and rules

- **Source:** the Catalogue of Life, release COL26.9 (ChecklistBank dataset 316321, issued
  2026-09-11), through ChecklistBank's matching service, with the zoological code and the taxon's
  rank. Matching at a rank separates homonyms: *Morus* is both the gannets and the mulberries,
  *Plecoptera* both the stoneflies' order and a moth genus.
- **Which taxon a name gets:** the narrowest taxon that holds what the name commonly refers to,
  at any rank from species up to class: bat, the order Chiroptera; whale, the order Cetacea, which
  also holds the dolphins; snail, the class Gastropoda. When a name has one species it most
  commonly means, it gets that species: salmon, the Atlantic salmon *Salmo salar*; trout, the brown
  trout *Salmo trutta*; cod, *Gadus morhua*.
- **Accepted names:** a synonym is entered under the Catalogue's accepted name (mink, *Neogale
  vison*; bison, *Bos bison*; bullfrog, *Aquarana catesbeiana*).
- **Ranks:** phylum, class, order, family and genus are COL's classification of the taxon, and the
  taxon itself at its own rank. A field is blank below the taxon's rank (a bat has no family or
  genus) and wherever COL's classification has no taxon at that rank:
  - COL gives some families no order: the barracudas', clownfishes', snappers', wrasses' (with
    the parrotfishes) and archerfishes' families sit straight under their class, and the
    tuatara's, the octopuses', the lugworm's and the shipworm's families under ranks between
    order and class;
  - lungfishes and the coelacanth have no class in COL: they sit in superclasses (Dipnoi,
    Actinistia);
  - a few species' classifications skip their family or genus (the firebrat's genus; the pillbug's
    family and genus; the hookworm's and daphnia's family).
- **The group follows from the class:** Mammalia, Aves, Reptilia, Amphibia, Insecta and Arachnida
  by name; fish for every other chordate (all of them vertebrates: sharks and rays, ray-finned
  fishes, sturgeons, gars, lampreys, hagfishes, lungfishes, the coelacanth); other_invertebrate for
  every other animal. COL keeps the springtails (Collembola) out of the insects, so they are other
  invertebrates.
- **The held-out families (`categories.order`):** the order. When COL places the family in no
  order, the family; for a name above order rank, the name itself (snail and slug, Gastropoda;
  shark, Selachii; mite, Acariformes; hagfish, Myxini). Each is held out whole, so a held-out name
  has no kin of its order in training. A name above order rank can still have kin in other
  families: the shark's (Selachii) are the mako's, the hammerhead's and the dogfish's orders.

## Choosing the names

- One-word English names, lower case, no hyphens. Two-word names (sea lion, polar bear, guinea
  pig, stick insect) are left out, and so are the names of the groups themselves (mammal, bird,
  fish, insect …).
- A name whose kinds span several classes or phyla is left out, and its kinds come in by name:
  worm (earthworm, leech, lugworm, hookworm …), bug.
- **Left out for a strong second sense:**

| Name | Its other sense |
|---|---|
| python | the programming language |
| kite | the toy |
| swift | the adjective |
| ray | a beam |
| skate | the sport and the boot |
| tick | the mark |
| mole | the spy, the skin mark and the unit |
| cardinal | the churchman and the number |
| rook | the chess piece |
| lark | a bit of fun |
| swallow | the verb |
| perch | the verb and the seat |
| fly | the verb |
| weaver | the craftsperson |
| harrier | the runner, the hound and the aircraft |
| crane | the machine |
| kiwi | the fruit and the New Zealander |
| booby, tit | slang |
| pike | the weapon |
| mullet | the haircut |
| basilisk | the legendary serpent |
| barbel | the whisker-like organ of fishes |
| walkingstick | the cane |

- **Left out for another reason:**
  - bluebottle names both a blowfly and the Portuguese man o' war, two classes apart;
  - angelfish names two families in different orders (the marine angelfishes and the freshwater
    *Pterophyllum*), neither the obvious one;
  - antlion names the larva, a pit-trapping predator that hardly moves, as often as the flying
    adult, so its way of life has no one answer;
  - dingo is a form of the dog in the Catalogue (*Canis familiaris*), so it would repeat dog.
- **Kept despite a second sense:** bat and seal, a flying mammal and a sea mammal, central to the
  question of kinship or way of life. Their neighbours in each layer show whether the model reads
  them as animals.
- **Corrected at the source:** the matching service matched "Anthophila" (the bees' clade) to a
  moth genus of the same name. The bees' clade has no rank in COL, so bee is entered as Apoidea,
  the superfamily that holds every bee (and the apoid wasps).

## Way of life

One author's judgment for every animal, made in one pass and recorded with its rules:

- **habitat** is where the adult lives and feeds:
  - *land*, *fresh water* or *sea*;
  - *land and water* for animals of the water's edge that feed or breed in the water: otters,
    beavers, frogs, crocodilians, ducks, herons, dragonflies, mayflies;
  - sea animals that breed or rest on land are *sea* (seals, penguins, albatrosses);
  - fish that move between rivers and the sea take the water they grow in: salmon and shad the
    sea, sturgeons and lampreys fresh water, eels (an order of mostly sea fishes) the sea;
  - parasites take their hosts' habitat: hookworms, tapeworms, fleas and lice live on land.
- **movement** is how it mainly moves:
  - *walks*: on legs, including running, hopping and climbing (frogs hop, crabs walk);
  - *flies*, including gliding (the colugo);
  - *swims*;
  - *crawls*: on its belly or a muscular foot, or as a legless larva (snakes, snails, earthworms,
    the silkworm, the mealworm, the glowworm's larva-like female);
  - *stays put*: fixed, or nearly so (corals, barnacles, mussels, oysters, tapeworms).
  - Game birds, the roadrunner, the secretarybird and the bustard mostly walk; the mudskipper, a
    fish, walks on its fins over mudflats.
- **diet:**
  - *carnivore* eats animals, including insects, plankton animals and blood;
  - *herbivore* eats plants, algae, nectar, seeds, wood or decaying plant matter;
  - *omnivore* eats both;
  - filter feeders go by what they filter: baleen whales and anchovies are carnivores, mussels and
    clams (plant plankton) herbivores, barnacles and copepods omnivores;
  - an insect whose larva is the feeding stage goes by what it is known for eating: lacewings
    (their larvae eat aphids) are carnivores, hoverflies (flower visitors) herbivores.
- **wild or domestic:** domestic for animals people keep and breed in domesticated forms: pets
  (cat, dog, hamster, budgerigar, goldfish, betta, guppy, swordtail), livestock (cow, sheep, pig,
  llama, chicken, turkey), the silkworm and the honeybee. Wild species that are farmed or kept
  (salmon, tilapia, oysters, iguanas) are wild.

## Where kinship and way of life disagree

The kinship-or-way-of-life analysis follows these 33 animals. DESIGN.md C1 names whales, bats and
penguins as examples; the rest follow by the same rule: an animal that lives the way another
group typically does.

| Kind | Animals |
|---|---|
| mammals that swim | whale, humpback, dolphin, orca, porpoise, narwhal, beluga, manatee, dugong, seal, walrus, otter, beaver, muskrat, nutria, platypus |
| mammals that fly | bat, colugo |
| birds that don't fly | penguin, ostrich, emu, cassowary, rhea, kakapo |
| animals named "fish" that aren't fish | starfish, jellyfish, cuttlefish, crayfish, silverfish |
| legless animals outside the snakes | eel, caecilian, slowworm |
| a fish that walks | mudskipper |

Kiwi, a bird that doesn't fly, is left out for its second senses (above).

## Audits (2026-10-09, before the capture)

`docs/studies/animals/analysis/audit_set.py` checks every entry and changes nothing; fixes are
made by hand in the set. Its checks: the entry's shape and axis values; duplicates; the group
from the class; the held-out family from the rule above; the taxonomy against the Catalogue of
Life, field by field; `tokens` against the tokenizer; each entry through the sentence route's
prompt and the real capture step (a stand-in model), read at the user's word with its token count
and offset; no name in the prompt outside the user's message; at least 3 held-out families per
group.

Result: 524 animals, 0 problems.

| Group | Animals | Held-out families | Split | Land | Fresh water | Sea | Land and water | Domestic |
|---|---|---|---|---|---|---|---|---|
| mammal | 165 | 24 | 123 (75%) | 146 | 0 | 11 | 8 | 19 |
| bird | 122 | 33 | 106 (87%) | 87 | 0 | 11 | 24 | 6 |
| reptile | 32 | 4 | 27 (84%) | 24 | 0 | 0 | 8 | 0 |
| amphibian | 15 | 3 | 13 (87%) | 6 | 5 | 0 | 4 | 0 |
| fish | 79 | 41 | 68 (86%) | 0 | 29 | 49 | 1 | 4 |
| insect | 53 | 20 | 46 (87%) | 47 | 0 | 0 | 6 | 2 |
| arachnid | 10 | 8 | 8 (80%) | 10 | 0 | 0 | 0 | 0 |
| other_invertebrate | 48 | 38 | 39 (81%) | 11 | 4 | 33 | 0 | 0 |

| Group | Walks | Flies | Swims | Crawls | Stays put | Carnivore | Herbivore | Omnivore |
|---|---|---|---|---|---|---|---|---|
| mammal | 147 | 2 | 16 | 0 | 0 | 53 | 79 | 33 |
| bird | 15 | 106 | 1 | 0 | 0 | 57 | 32 | 33 |
| reptile | 11 | 0 | 8 | 13 | 0 | 28 | 3 | 1 |
| amphibian | 9 | 0 | 5 | 1 | 0 | 15 | 0 | 0 |
| fish | 1 | 0 | 78 | 0 | 0 | 59 | 1 | 19 |
| insect | 19 | 31 | 0 | 3 | 0 | 17 | 27 | 9 |
| arachnid | 10 | 0 | 0 | 0 | 0 | 8 | 0 | 2 |
| other_invertebrate | 9 | 0 | 12 | 18 | 9 | 15 | 21 | 12 |

**Known covariates:**
- **Way of life follows the group,** as it does in nature: fish swim, birds fly, amphibians and
  reptiles are carnivores. So a node that holds one group also holds its way of life; only the
  animals whose kinship and way of life disagree (above) can tell the two apart.
- **The groups differ in size** (10 arachnids, 165 mammals), as the one-word rule and common
  English allow. Held-out scores are chance-corrected, and the analyses report each group.
- **Split names** run from 75% of mammals to 87% of birds, insects and amphibians; the surface
  check and the `tokens` axis read what's left.

The loader's validator warns on every item: a single word isn't 10 to 30 words, and each item's
target word differs from the file's. Its checks are advisory (GUIDE.md) and don't apply to this
shape.

## Capture

```bash
curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "animals_kinship_v1", "session_name": "animals_kinship_v1",
       "generate_output": false, "pin_date": "2026-09-16"}'
```

The date is the one the nouns capture pinned, so the two captures' prompts differ only in the
word. The route counts only the items it wrote and returns the words it dropped; the count is
checked against the set (524), and each item's recorded token count against its `tokens`.

## Lenses

- The capture keeps the set's hold-out design (families field `order`, whole names), so every
  lens on it holds out whole orders unless a request names another field. Folds beyond 12 merge
  round-robin.
- The group is the lens's label; habitat, movement, diet, wild or domestic, and tokens are its
  other axes. The taxonomy is read from this file by the analyses in `docs/studies/animals/`.
- No output axes: nothing is generated.
