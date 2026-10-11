# Animals: an ontology of animal words (v1) — set guide

Related: data/sentence_sets/lexical/animals_kinship_v1.md (the names, taxonomy and way of life,
unchanged here), docs/research/animal_ontology.md (the proposal: why these ways, and the three
measures), docs/studies/animal_ontology/study.yaml (the study that uses it),
data/sentence_sets/GUIDE.md (set format and doctrine), docs/design/design.md (sentence sets: the
animal ontology)

## Purpose

People organize animals in many ways at once: by descent, by what they look like, by where they
are met, by what they are to us. The first animal set framed one contest, descent against way of
life; this set gives every animal a value in nine ways instead, so the model's states can show
which ways it follows, at which layers, without a framing chosen in advance (the design's animal
ontology; Andrew's ruling L27 adopted the proposal as listed).

The study reads it three ways (neighbours beyond chance, held-out reading, each way's own share of
the distances), always within each token count. The proposal has the measures and the reasons for
each way; this guide has the rules each label follows and the borderline calls.

## What is new, and what is not

- **The same 524 names, in the same order,** as `animals_kinship_v1`: each item's text, group,
  target word, taxonomy and its six earlier categories (order, habitat, movement, diet,
  wild_or_domestic, tokens) are copied unchanged. The audit checks that item by item. The rules
  for those fields (which taxon a name gets, the Catalogue of Life source, habitat and movement)
  are in that set's guide.
- **Eight new categories** follow `tokens` in each item: `kind`, `covering`, `size`, `legs`,
  `where_met`, `relation`, `danger`, `feeling`. With the six earlier ones that makes fourteen axes,
  in nine ways (descent has two: the group and the order; danger and feeling are one way with two
  axes; way of life has four).
- **The read site and the hold-out design are unchanged:** each name is given alone as the user's
  message with a space first (`" lion"`), read at its last token; whole taxonomic orders are held
  out (`metadata.holdout`).
- **Who labelled it:** Claude Code, by hand, in one pass over all 524 names, one author for every
  group; no script and no subagent wrote a label.

## The nine ways

| Way | Axes and values |
|---|---|
| 1. descent | `label` (the group of eight) and `order`, from the earlier set |
| 2. everyday kind | `kind`: beast, bird, fish-like, snake-like, lizard-like, bug, shellfish, worm-like, sea creature |
| 3. body covering | `covering`: fur or hair, feathers, scales, bare skin, shell or hard case, soft body |
| 4. size | `size`: tiny, small, medium, large, huge |
| 5. legs | `legs`: none, two, four, six, eight, more than eight |
| 6. where people meet it | `where_met`: home, farm, town and gardens, countryside, sea or shore, far away |
| 7. relation to people | `relation`: companion, kept for work or food, dangerous, pest, wild |
| 8. danger and feeling | `danger`: harmless, can hurt, can kill; `feeling`: liked, neutral, feared or disliked |
| 9. way of life | `habitat`, `movement`, `diet`, `wild_or_domestic`, from the earlier set |

## The rules, and how they were applied

### Everyday kind

What an English speaker would call the animal at a glance, from its body form and where it lives,
whatever its descent (folk biology's life forms):
- **beast:** mammal-shaped animals with legs, furry or not: bats, seals, otters and walruses too;
- **bird:** every bird, flightless ones too;
- **fish-like:** swimmers with fins, flippers or flukes and no legs or fur: fish, sharks and rays,
  and the whales, dolphins, porpoises and sea cows (whale, humpback, dolphin, orca, porpoise,
  narwhal, beluga, manatee, dugong);
- **snake-like:** long, limbless bodies that move by bending: the snakes, the slowworm (a legless
  lizard), the caecilian and the amphiuma among amphibians, and the eel, lamprey and hagfish among
  fish;
- **lizard-like:** four legs, low to the ground, scaly or moist skin: lizards, crocodilians,
  turtles and tortoises, the tuatara, frogs, toads, salamanders and newts;
- **bug:** small animals with six or more jointed legs, larvae included: every insect and
  arachnid, and the woodlouse, pillbug, centipede, millipede and springtail;
- **shellfish:** water animals in a hard shell or case: the crabs, lobsters, shrimps, prawns,
  crayfish, krill and the small water crustaceans (copepod, daphnia), the barnacle, the bivalves,
  the sea snails and the chiton;
- **worm-like:** soft, small, limbless animals of land and mud: snails and slugs, earthworms and
  leeches, the lugworm and ragworm, the parasitic worms, the planarian, and the shipworm (a
  bivalve that looks like a worm);
- **sea creature:** soft or strange sea animals: octopus, squid, cuttlefish, nautilus, nudibranch,
  jellyfish, coral, starfish, brittlestar.

### Body covering

As seen on the adult: **fur or hair**; **feathers**; **scales** (visible at a glance: snakes,
lizards, crocodilians, most fish, the pangolin); **bare skin** (smooth or slimy); **shell or hard
case**; **soft body**.
- **Mammals that aren't furry:** walrus, pig, warthog, hippopotamus, rhinoceros, elephant,
  aardvark and the whales and sea cows have bare skin; the armadillo has a shell; the pangolin has
  scales.
- **Fish with bare skin:** the sharks and rays (shark, mako, hammerhead, dogfish, stingray, manta,
  sawfish), and the scaleless bony fish (catfish, eel, swordfish, paddlefish, lamprey, hagfish,
  pufferfish, stonefish, blenny, oarfish, anglerfish, turbot, monkfish). The seahorse's bony rings
  count as a hard case.
- **Amphibians** all have bare skin.
- **Shell or hard case:** adult insects and arachnids, the crustaceans, shelled molluscs, turtles
  and tortoises, starfish, the brittlestar and coral (its skeleton).
- **Soft body:** insect larvae and larva-like adults (silkworm, mealworm, the glowworm), the
  chigger (a larval mite), slugs, worms, leeches, the octopus, squid and cuttlefish, the
  nudibranch, the jellyfish and the shipworm.
- **The tarantula** is hairy enough to read as fur or hair.

### Size

By typical adult weight: **tiny** under 1 g; **small** 1 g to 1 kg; **medium** 1 to 30 kg;
**large** 30 to 1,000 kg; **huge** over 1,000 kg. A name that covers many animals takes the
member most people picture.
- **Generic names:** a snake is small (the snakes most people meet weigh under 1 kg); a shark is
  large (the large sharks people picture); a lizard, spider, beetle, butterfly and moth are tiny
  or small accordingly; a turtle is medium (a pond turtle or a snapping turtle).
- **Huge:** walrus, hippopotamus, giraffe, whale, humpback, orca, narwhal, beluga, rhinoceros,
  elephant, the manta.
- **Tiny, outside the insects:** guppy, zebrafish, most arachnids, the woodlouse, pillbug,
  centipede and millipede, the springtail, barnacle, copepod, daphnia, planarian, and the hookworm
  and pinworm.
- **Small, among the insects:** the scarab, silkworm (full grown), cicada, locust, katydid and
  mantis.
- **Coral** is sized as a single piece of coral people would see or hold (small), not a reef.

### Legs

Count the limbs the animal walks, hops or stands on. Wings, fins, arms and tentacles don't count;
flippers count only where the animal moves on land with them (seals, walruses, turtles).
- **Two:** every bird, and the bat, kangaroo, wallaby, quokka and jerboa among mammals.
- **None:** the whales and sea cows, snakes and the legless lizard and amphibians, every fish (the
  mudskipper's fins don't count), the molluscs, worms, jellyfish, coral, starfish and brittlestar
  (tube feet and arms don't count), the barnacle and daphnia.
- **Six:** every insect but the silkworm caterpillar, and the springtail; the chigger (a
  six-legged larval mite); the
  vinegaroon and solifuge, which walk on six and hold their front pair up as feelers.
- **Eight:** the other arachnids.
- **More than eight:** crabs, lobsters, shrimps, prawns, the langoustine and crayfish (ten), krill
  and copepods (their swimming legs), the woodlouse and pillbug (fourteen), the centipede and
  millipede, and the silkworm caterpillar (its six legs and its prolegs).

### Where people meet it

At home (pets and animals found indoors); on the farm; in town and gardens (streets, parks,
gardens); in the countryside (woods, fields, rivers, ponds); at sea or on the shore; or far away
(known mostly from zoos, aquariums, films and books).
- **Whose view:** someone in Britain or North America. An animal met in either place takes the
  setting where it is met there, and "far away" is kept for animals met in neither: a raccoon is a
  town-and-garden animal; the cougar, bear, alligator, rattlesnake, cottonmouth, copperhead,
  kingsnake, chuckwalla, hellbender, mudpuppy, amphiuma, spadefoot and bullfrog are countryside
  animals.
- **Several settings:** the one most people would name first. Pets kept indoors are home animals
  (including the gecko, tortoise, terrapin, axolotl and the aquarium fish: goldfish, guppy, betta,
  cichlid, zebrafish, loach, gourami, swordtail); so are animals found indoors: the household
  pests (weevil, housefly, bedbug, cockroach, termite, flea, louse, silverfish, firebrat, mealybug,
  mite), the moth, spider and centipede, and the pinworm and tapeworm.
- **Farm:** livestock (pig, cow, goat, sheep, horse, donkey, llama, alpaca, chicken, turkey), the
  farmed tilapia and silkworm, and the botfly (a livestock parasite).
- **Elk** is the North American wapiti (*Cervus canadensis*), as in the earlier set, and is labelled
  as met there (countryside); in British English "elk" names the moose.
- **Fish and other water animals:** sea fish met by anglers, fishermen and at the coast are "sea
  or shore"; river and pond fish (trout, carp, the coarse fish, the salmon on its river run, the
  shad) are countryside; tropical and deep-sea fish are far away. The slowworm and the anole are
  town-and-garden animals (garden compost heaps; yards in the American South).

### Relation to people

After the sociozoologic scale: **companion** (commonly kept as a pet); **kept for work or food**
(farmed, worked, or caught for food); **dangerous** (known to kill or badly hurt people); **pest**
(harms homes, crops, food, livestock or health); **wild** (none of these). Each animal takes the
role most people would name first; on a tie, the earlier in that list.
- **Caught for food counts as kept for food:** the food fish (salmon, trout, tuna, cod, haddock,
  herring, sardine, anchovy, mackerel, catfish, eel, swordfish, the flatfish, grouper, snapper,
  sturgeon, tilapia, whiting, hake, shad, capelin, monkfish, gurnard), the shellfish people eat
  (crab, lobster, shrimp, prawn, langoustine, crayfish, clam, oyster, mussel, scallop, cockle,
  whelk, winkle, abalone, geoduck) and the squid; game birds (quail, pheasant, grouse, partridge);
  the bee and honeybee, silkworm and mealworm.
- **Dangerous:** the big predators (lion, tiger, leopard, jaguar, cougar, wolf, hyena, bear), the
  hippopotamus, buffalo and cassowary, the venomous snakes and the anaconda, the crocodile and
  alligator, the shark, mako and stingray, the piranha and stonefish, the hornet and tsetse, the
  scorpion and the jellyfish. The adder, copperhead and piranha are dangerous in people's minds
  though rarely deadly (danger: can hurt).
- **Pests:** household, garden and crop pests, parasites and disease carriers (the mosquito is a
  pest first in Britain and North America; the tsetse, known only as a disease carrier, is
  dangerous). Spiders and centipedes are wild: they harm nothing on the list, however disliked.

### Danger and feeling

- **Danger** is given to every animal, whatever its main role: harmless, can hurt, can kill. "Can
  kill" is kept for animals known to kill people: the big predators and large herbivores
  (chimpanzee, moose, bison, rhinoceros, elephant beside the dangerous ones), venomous animals,
  disease carriers (mosquito, tsetse) and the pufferfish (if eaten). Stings, bites and pinches
  that hurt make "can hurt": bees and wasps, ants, crabs and lobsters, biting flies and parasites.
- **Feeling:** liked (commonly found cute, beautiful or admirable); feared or disliked (commonly
  feared or found disgusting); neutral. Most food fish and little-known animals are neutral.
  Feeling and danger come apart on purpose: the vulture, pigeon, skunk, toad, moth, slug and many
  insects are harmless and disliked; the hippopotamus and elephant can kill and are liked.

## Counts

| Axis | Values (count) |
|---|---|
| kind | beast 156, bird 122, fish-like 85, bug 68, lizard-like 30, shellfish 23, snake-like 20, worm-like 11, sea creature 9 |
| covering | fur or hair 148, feathers 122, shell or hard case 96, scales 88, bare skin 51, soft body 19 |
| size | small 229, medium 138, large 80, tiny 66, huge 11 |
| legs | four 181, none 140, two 127, six 56, more than eight 13, eight 7 |
| where_met | far away 197, countryside 123, sea or shore 82, town and gardens 65, home 44, farm 13 |
| relation | wild 357, kept for work or food 65, pest 42, dangerous 34, companion 26 |
| danger | harmless 412, can hurt 74, can kill 38 |
| feeling | neutral 270, liked 180, feared or disliked 74 |

Rare values (farm 13, eight legs 7, huge 11, sea creature 9) will be read with care: a measure
over few animals has wide uncertainty, and the study reports how many animals each value holds.

## Limits

- **One author's judgment.** Descent, legs, size and covering follow facts; everyday kind, where
  people meet the animal, relation, danger and feeling are judgments, made by one author with the
  rules above. The borderline calls are listed here so a reader can disagree with each.
- **One cultural view.** Where people meet an animal, its relation and how people feel about it
  are judged for Britain and North America; elsewhere many would differ.
- **Correlated ways.** Covering, legs and everyday kind follow descent closely, and relation,
  danger and feeling overlap. The study's own-share measure and the animals where the ways disagree
  are how it separates them.
- **The token count** splits these names at every layer (the first animal study), so every
  comparison is made within each token count.

## Audit and capture

- **The audit** (`docs/studies/animal_ontology/analysis/audit_set.py`) checks the file's shape and
  values, that every earlier field equals `animals_kinship_v1`'s item by item, the tokens and the
  prompt's own words, the counts and how each axis crosses the others, and each taxonomy match
  against the animal's common names in the Catalogue of Life.
- **The capture** uses the sentence route with `generate_output: false` and the date pinned to
  2026-09-16, the earlier animal capture's, so every state should equal that capture's for the
  same text.
