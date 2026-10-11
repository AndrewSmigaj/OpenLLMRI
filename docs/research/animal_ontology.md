# Ways of organizing animals: a proposed ontology (2026-10-11)

Related: docs/DESIGN.md (C1 the animal set, L27 this proposal), docs/research/animals.md (the
first animal study), docs/research/read_site.md (why a word stays read at its last token),
data/sentence_sets/lexical/animals_kinship_v1.md (the set's names, rules and audits),
docs/studies/animal_ontology/study.yaml

**Status:** Claude's proposal, adopted by Andrew on 2026-10-11 as listed (DESIGN.md C1, L27). The
work below is under way; its results will go in a findings note beside this one.

## Why

On 2026-10-11 Andrew changed the animal set's grouping and its framing (DESIGN.md C1, L16.1 and
L16.6). There are several ways of organizing animals, and in his view grouping animals is
pragmatic: an animal seen only for a moment has to be guessed from a few cues (a dog? a cat?). So
instead of one framing chosen in advance, each animal gets a label in every way of organizing, a
small ontology of the animal words, and the model's states show which ways it follows most. He
asked Claude to look into ways of organizing animals and propose some, and to justify the first
study's focus on kinship, including why the set went straight to kinship against way of life.

## Why the first study centred on kinship

- **Where it came from.** On 2026-10-09 Andrew asked for one lens over all the animals that records
  their genus, family and the rest of their taxonomy. Claude's recommended option added their way
  of life and the animals where the two disagree (whale, dolphin, bat, penguin, seal, ostrich),
  saying the lens would then show whether the model groups animals by kinship or by how they live,
  and Andrew picked it. The framing and the word were Claude's. "Kinship" meant relatedness by
  descent (a whale is a mammal), not kinship in the social sense. The word is dropped.
- **Why taxonomy still earns a place.** It is the one way of organizing animals that comes from
  science rather than from how animals look or how people live with them. Descent is stated in
  text (encyclopaedias, school biology) but can't be seen at a glance. How far the model follows
  it shows how much of its picture of animals is textbook knowledge and how much is everyday talk.
  Language models do carry such hierarchies: in Gemma and Llama 3, each level of WordNet's
  hierarchy (animal, then mammal, then dog) adds its own direction, at right angles to its parent's
  (Park et al., 2025).
- **What was wrong with the framing.** It made the question a contest between two framings chosen
  in advance, and its own results showed that was too narrow. The animals whose descent and way of
  life disagree mostly sat with their kin, the whales being the exception; but the strongest
  structure in the space was neither. It was how many tokens a name has
  (`docs/research/animals.md`). A way of organizing that nobody named in advance could be the one
  the model follows most, and a contest of two can't show it. A label in every way lets the data
  rank them, the pragmatic ones included.
- **In-group and out-group.** Among animals, the nearest thing is their relation to people (way 7
  below: companions on one side, pests and threats on the other). Among people, it is friend or
  foe, which the agent scenarios study (DESIGN.md C6).

## How people organize animals

- **Folk biology.** Folk classifications in many cultures share a few broad life forms (bird, fish,
  snake, small crawling "bugs", and four-legged mammals, often unnamed) and, below them, generic
  kinds such as robin or oak. The generic kinds match the scientific species or genus best; the
  life forms match science least, because they group animals by gross body form (Berlin, 1992;
  Atran, 1998). Folk systems often put whales and dolphins with the fish.
- **The basic level.** People name and recognize things fastest at one level of a hierarchy: dog,
  rather than animal or dalmatian. Members of a basic category share many attributes and a shape
  (Rosch et al., 1976). A glimpse is matched at this level, to a dog or a cat, from shape, size,
  covering and movement. Most names in the set are basic or generic kinds already, so the basic
  level isn't a way of organizing of its own; the ways based on looks, below, carry what a glimpse
  gives.
- **Features people list.** Asked to describe an animal, people list many features of how it
  looks: has fur, has four legs, is big (McRae et al., 2005, norms for 541 concepts).
- **Size and danger.** Word vectors hold graded knowledge about animals. Projected onto a line from
  "small" to "big", or from "safe" to "dangerous", they reproduce people's ratings of size and
  danger (Grand et al., 2022). The two can come apart: a dolphin and an alligator are about the
  same size, and differ greatly in danger.
- **Use.** Folk classifications have a large natural core and a periphery shaped by usefulness
  (Hunn, 1982).
- **Relation to people.** The sociozoologic scale ranks animals by their place in human life: pets
  and tools (working and food animals) as "good" animals, vermin and demons as "bad" ones (Arluke
  and Sanders, 1996). The same animal can move between places: a rabbit is a pet, a meal or a pest.
- **Feeling.** In Britain, fear of spiders, rats and snakes, animals that are harmless there, goes
  with disgust (Davey, 1994). How people feel about an animal is not the same as how dangerous it
  is.
- **What to expect of a language model.** Language models match people's broad category
  boundaries, but keep fewer of the finer distinctions within a category: they compress harder
  than people do (Shani et al., 2025).

## The proposed ontology

The same 524 names as `animals_kinship_v1`. Each way of organizing below is one or more designed
axes, and every animal gets a value on each: fourteen labels in nine ways, eight of them new
(ways 2 to 8) beside the six the set already has (ways 1 and 9). The proposal Andrew approved
counted ten; the list was the same. Because every axis is in the capture, the app colours by any of them and
the axes analysis reads each one. One author (Claude) labels every animal, in one pass, by hand.
The set's guide records each rule and lists the borderline cases.

1. **Descent** (in the set): the familiar group of eight, which follows from the class (mammal,
   bird, reptile, amphibian, fish, insect, arachnid, other invertebrate), and the taxonomic order,
   which stays the family held out in validation. The full taxonomy (phylum to genus) stays beside
   the designed axes.
2. **Everyday kind** (`kind`), modelled on folk biology's life forms: what an English speaker would
   call the animal at a glance, from its body form and where it lives, whatever its descent.
   - **beast:** mammal-shaped animals with legs, furry or not, including bats, seals and otters;
   - **bird:** every bird, flightless ones too;
   - **fish-like:** swimmers with fins, flippers or flukes and no legs or fur: fish, sharks, rays,
     whales, dolphins, manatees;
   - **snake-like:** long, limbless bodies that move by bending: snakes, legless lizards,
     caecilians, eels, lampreys;
   - **lizard-like:** four legs, scaly or moist skin, low to the ground: lizards, crocodiles,
     turtles, salamanders, newts, frogs and toads;
   - **bug:** small animals with six or more jointed legs: insects and their larvae, spiders,
     scorpions, mites, ticks, centipedes, millipedes, woodlice;
   - **shellfish:** water animals in a hard shell or case: crabs, lobsters, shrimps, barnacles,
     clams, mussels, oysters, sea snails;
   - **worm-like:** soft, small, limbless animals of land and mud: earthworms, leeches, lugworms,
     slugs and land snails;
   - **sea creature:** soft or strange sea animals: jellyfish, octopuses, squids, starfish, sea
     urchins, anemones, corals, sponges.
3. **Body covering** (`covering`), as seen on the adult: fur or hair; feathers; scales (visible at
   a glance: snakes, lizards, most fish, pangolins); bare skin (smooth or slimy: amphibians,
   whales, elephants, hippos, eels, sharks); shell or hard case (insects, spiders, crabs, shelled
   molluscs, turtles, armadillos, starfish and urchins); soft body (worms, slugs, jellyfish,
   octopuses, insect larvae).
4. **Size** (`size`), by typical adult weight: tiny (under 1 g), small (1 g to 1 kg), medium (1 to
   30 kg), large (30 to 1,000 kg), huge (over 1,000 kg). A name that covers many animals (bat,
   whale, shark) takes the member most people picture.
5. **Legs** (`legs`): none, two, four, six, eight, or more than eight. Count the limbs it walks,
   hops or stands on. Wings, fins, arms and tentacles don't count; flippers count only where the
   animal moves on land with them (seals, turtles). Crabs and lobsters have ten.
6. **Where people meet it** (`where_met`): at home (pets and animals found indoors); on the farm;
   in town and gardens (streets, parks, gardens); in the countryside (woods, fields, rivers,
   ponds); at sea or on the shore; or far away (known mostly from zoos, films and books). Judged
   for someone in Britain or North America: an animal met in either place takes the setting where
   it is met there (a raccoon is a town-and-garden animal), and "far away" is kept for animals met
   in neither. When it is met in several settings, it takes the one most people would name first.
   Where you are is one more cue for guessing what a glimpsed animal is (Claude's addition to
   Andrew's example).
7. **Relation to people** (`relation`), after the sociozoologic scale: companion (commonly kept as
   a pet); kept for work or food (farmed, worked, or caught for food); dangerous (known to kill or
   badly hurt people); pest (harms homes, crops, food, livestock or health); wild (none of these).
   Each animal takes the role most people would name first; on a tie, the earlier in that list.
8. **Danger and feeling:**
   - **danger to people** (`danger`): harmless, can hurt, can kill. Unlike the relation, every
     animal gets one, whatever its main role: a bull is kept for work or food, and can kill;
   - **how people feel** (`feeling`): liked (commonly found cute, beautiful or admirable); feared or
     disliked (commonly feared or found disgusting); neutral.
9. **Way of life** (in the set): habitat, movement, diet, wild or domestic.

**Controls:** the name's token count (in the set) and its length in characters. Every comparison
below is made within each token count.

## Which way of organizing leads

A way of organizing **leads** at a layer when it explains most about which animals sit near each
other there, with the other ways and the token count held fixed. At every layer, at the name's last
token, three measures are taken, in raw space (the residual stream, centred, standardized and
reduced to 50 dimensions, as validation does) and in the lens's own space:

1. **Neighbours:** how often an animal's 10 nearest neighbours share its value, as agreement beyond
   chance: (observed − expected) / (1 − expected). The expected share comes from 1,000 shuffles of
   the values within each token count. This puts axes with different numbers of values on one
   scale.
2. **Held out:** the axes analysis on a lens of the new capture, with whole taxonomic orders (such
   as Carnivora) held out: how well a linear probe (a simple classifier) and the lens's nodes read
   each axis on orders they never saw, as κ, agreement beyond chance. An axis that follows descent
   closely, such as covering or everyday kind, is tested here on unseen branches of the tree.
3. **Each way's own share:** a model of the distance between every pair of animals, given whether
   they differ on each axis (all at once, with the token count and name length). Each axis's
   share is what it explains with the others held fixed. Its p-value comes from 1,000 permutations
   of the animals within each token count.

The result is a heatmap of axes by layer for each measure, and the leading way at each layer. The
animals where the ways disagree are shown as examples, with their nearest neighbours: the whales
(descent says mammal, everyday kind says fish-like), the bats (descent and everyday kind say beast,
movement says flier), the flightless birds, the names ending in "fish" that aren't fish, the eel
and the legless lizards. A way that leads at a layer and also holds on held-out orders is the
strongest evidence that the model organizes animals that way there. The study is exploratory:
nothing is predicted as a gate.

## Cautions

- **One author's judgment.** Descent, legs, size and covering follow facts; everyday kind, where
  people meet the animal, relation, danger and feeling are judgments, made by one author with
  written rules. The guide lists every borderline case, and the audit shows how each axis crosses
  the others.
- **Correlated ways.** Covering, legs and everyday kind follow descent closely, and relation,
  danger and feeling overlap. The own-share measure and the animals where the ways disagree are
  what separate them.
- **The token count.** It splits the space at every layer (`docs/research/animals.md`), so every
  comparison is made within it.
- **Single words.** Each animal is read as a word alone. Which way leads may differ in sentences,
  where context picks the sense; that is a later study.

## The work

1. The set `animals_ontology_v1`: the same 524 names, with the new axes, its guide and its audit,
   including a check of each taxonomy match against the animal's common names (DESIGN.md C4,
   L18.5), as a study script for now.
2. A new capture: the analysis tools read only the axes a capture recorded, so the names are
   captured again, with the date pinned to 2026-09-16 as before. Every state then equals the first
   capture's.
3. A lens like `animals-k8-n15`, with whole orders held out; validation, the axes analysis, routes
   and node details.
4. The comparison scripts, in `docs/studies/animal_ontology/analysis/`, with their figures.
5. A findings note, the study's ledger, and a figure.

The labels take the longest; the capture takes minutes, the lens jobs and analyses about an hour.

## Sources

- Arluke, A. and Sanders, C. R. (1996). *Regarding Animals*. Temple University Press.
  [publisher](https://alt.library.temple.edu/tupress/titles/1151_reg.html)
- Atran, S. (1998). Folk biology and the anthropology of science: cognitive universals and
  cultural particulars. *Behavioral and Brain Sciences*, 21(4), 547–569.
  [pdf](https://qualquant.org/wp-content/uploads/cda/*atran%201998%20folk%20biology%20and%20the%20anthro%20of%20science.pdf)
- Berlin, B. (1992). *Ethnobiological Classification*. Princeton University Press.
  [review](https://ethnobiology.org/sites/default/files/pdfs/JoE/13-1/BREthnobiologicalClassification.pdf)
- Davey, G. C. L. (1994). Self-reported fears to common indigenous animals in an adult UK
  population: the role of disgust sensitivity. *British Journal of Psychology*, 85, 541–554.
  [record](https://sro.sussex.ac.uk/id/eprint/14745/)
- Grand, G., Blank, I. A., Pereira, F. and Fedorenko, E. (2022). Semantic projection recovers rich
  human knowledge of multiple object features from word embeddings. *Nature Human Behaviour*, 6(7),
  975–987. [article](https://pmc.ncbi.nlm.nih.gov/articles/PMC10349641/)
- Hunn, E. (1982). The utilitarian factor in folk biological classification. *American
  Anthropologist*, 84, 830–847. [record](https://tlopo.clld.org/sources/Hunn1982)
- McRae, K., Cree, G. S., Seidenberg, M. S. and McNorgan, C. (2005). Semantic feature production
  norms for a large set of living and nonliving things. *Behavior Research Methods*, 37, 547–559.
  [doi](https://www.doi.org/10.3758/BF03192726)
- Park, K., Choe, Y. J., Jiang, Y. and Veitch, V. (2025). The geometry of categorical and
  hierarchical concepts in large language models. ICLR 2025.
  [arXiv](https://arxiv.org/abs/2406.01506)
- Rosch, E., Mervis, C. B., Gray, W. D., Johnson, D. M. and Boyes-Braem, P. (1976). Basic objects
  in natural categories. *Cognitive Psychology*, 8, 382–439.
  [pdf](https://www.cns.nyu.edu/~msl/courses/2223/Readings/Rosch-CogPsych1976.pdf)
- Shani, C., Soffer, L., Jurafsky, D., LeCun, Y. and Shwartz-Ziv, R. (2025). From tokens to
  thoughts: how LLMs and humans trade compression for meaning.
  [arXiv](https://arxiv.org/abs/2505.17117)
