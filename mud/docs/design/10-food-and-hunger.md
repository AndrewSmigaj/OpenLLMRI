# 10 — Food and hunger: what is aboard, the country, the body

> **Status: reviewed with Andrew 2026-09-27.**
> **Architecture counterpart:** none.
> The pilot, bodies and the moral question have their own documents (12 and 15); this page covers
> food, and treats a body as one of its sources.

---

## 2. Decisions

### Andrew's decisions

- **(2026-09-07)** Several ways of getting food.
- **(2026-09-07, 2026-09-17, 2026-09-27)** Whether to eat the pilot is one of the few big decisions
  here. The pilot starts the run dead and carries no clues; his body is food, and eating it is taboo,
  not immoral.
- **(2026-09-16)** The plane is a 206-class single with freight and mail aboard. There is no galley
  and there are no airline meals; what food exists is people's own snacks and bags, the freight, and
  the country.
- **(2026-09-17, 2026-09-26)** A run ends in rescue or death — it ends when they die, of anything.
  Hunger is one pressure among many, not the clock that ends the run.
- **(2026-09-18)** Grubs and inner bark are in. The foods are audited against the place — what
  realistically lives in an area of this size, not food sources added because they happen to be
  possible.
- **(2026-09-26)** Hunger works as it does in real life.
- **(2026-09-26)** Cooking is part of a heat and state system, done properly: snow melts into water;
  food changes with heat, as part of what each object is; body parts have heat in their ontology; a
  fire heats its area and leaves residual heat in other areas; the plane's cabin is rooms with openings
  flagged open or closed, and a fire inside raises their shared internal heat. All of it belongs to designing
  the fire and heat system.
- **(2026-09-26, 2026-09-27)** Raw, cooked and spoiled food differ. Most fresh raw meat does not make
  anyone sick; rotten meat does — a fish left too long, an animal found long dead. There should be at
  least one spoiled thing, and there are poisonous mushrooms.
- **(2026-09-26)** There is a combat system like a MUD's.
- **(2026-09-26)** Hunting, trapping, fishing and killing are real operations, each variant its own:
  a snare takes materials to build, and you set it; you can throw rocks or anything else; you fish in
  different ways — casting a line out and dropping a line in each start fishing, and so do their
  variants, because the difference is ontologically significant, within the grammar rules; and you can
  kill things in other ways — stab with a spear, beat with a stick.
- **(2026-09-17, 2026-09-26, 2026-09-27)** A bear is in; there is no wolverine. The bear, some bigger
  animals and a few birds act (which is document 23 §4.1a, decided 2026-10-01); the fish are scripted;
  no wolves (2026-10-01).
- **(2026-09-27)** There is no survival kit — it would make the game too easy.
- **(2026-09-27, 2026-09-28)** Holt's cabin is supplies: some trapline gear, an axe, and modest stores,
  not piles of food.
- **(2026-09-27)** The season is the first week of October in interior Alaska, with no big storm: the
  snow builds to a couple of inches through the week and covers the low forage a little at a time
  (document 13 §4.2).
- **(2026-09-27)** Nothing kills instantly: death comes by the body running down, on real clocks, with
  time to respond. Poison makes people very sick but never kills.

### Proposals (Claude)

- The seed's food categories and body block, carried through GDD §31–§36; its "passenger snacks" and
  "airline meals" do not fit a 206 and are not used.

---

## 3. In one paragraph

There is food, and there is not enough of it, and the distance between those two facts is the whole
week. The first day it is a question of finding it: a chocolate bar in a pocket, a thermos, somebody's
trail mix, a small bag of dog food in the freight, a few frozen salmon fillets (a meal or two, not a larder — 2026-09-28) in a family's cooler thrown out onto
the debris trail. The country is still open in the first days — lowbush cranberries sweet from the
frost on bare ground, rose hips on the creek bar, a fool hen in a spruce that will stand there and let
you try twice — and each flurry closes it a little more, the lowest berry mats going under first.
Around day three it stops being a search and becomes work — snare wire and a hare run read right in the
new snow and then *left alone*, a line cast into the open water at the creek mouth. Meat that is not
eaten has to be kept somewhere cold enough not to spoil and far enough from the ravens and the bear,
a male grizzly still up all week, feeding hard before he dens. And the whole time there is the pilot's body, in the
cockpit, from the first hour, and nobody has to say anything about it because everybody has already
thought it.

---

## 4. The design

### 4.1 The rules

1. **Hunger follows real physiology** (Andrew, 2026-09-26; the physiology below accepted 2026-09-27). The body carries its energy as real stores, each a
   quantity on the body and set per character with the draw (document 16): **glycogen** in liver and
   muscle (roughly 400–500 g, about 1,600–2,000 kcal — gone in about a day of hard work in the cold),
   **fat** (a few kilograms on the kid, tens on a heavy adult; about 9 kcal a gram) and **muscle
   protein**, which the body burns as well. Spending runs on the heartbeat (document 06): a basal rate,
   each activity's cost, and the cold's cost — and **shivering runs mostly on muscle glycogen** (Haman
   et al., *J Physiol* 2005, "muscle glycogen becomes dominant as shivering intensifies"), so an empty
   body shivers less and cools faster; hunger reaches the warmth system (document 08) through that
   real channel. A working adult in the cold needs about **3,400–4,300 kcal a day** (Institute of
   Medicine, *Nutritional Needs in Cold and in High-Altitude Environments*, 1996: 45–57 kcal/kg/day);
   resting in shelter, less. Eating fills the gut; digestion takes hours; what a food yields depends on
   its **state** (§4.6) — cooked meat and cooked starch give the body more than raw (Carmody et al.,
   *PNAS* 2011) — and lean meat alone cannot be lived on (**rabbit starvation**: protein above about
   35–45 % of energy brings nausea and diarrhoea within about a week; document 23 §4.4).
   What the player feels shows on the hunger meter and in `status` band words (document 08 §4.9), in
   the real order: hungry →
   light-headed, slow and cold once the glycogen is gone → the pangs fading by the second or third day
   as ketosis takes over (the dangerous quiet) → weak, clumsy, irritable, cold-intolerant and poor at
   judgement (what the Minnesota Starvation Experiment recorded over months of semi-starvation, Keys et
   al. 1950, arriving here in its early form). Hungry enough to look at the pilot stays a design goal,
   and it arrives through the body, not a timer. **Starvation alone kills in weeks, not days** —
   people fasting with water have died after 46–73 days (the 1981 hunger strike) — so inside a
   week-long run hunger does not kill by itself: it weakens, and the cold does the killing
   (2026-09-27) — a hungry body shivers less, cools faster, falls more and decides worse. The kid's
   smaller reserves run out first. *(The figures are real starting points; the probes tune them.)*
2. **Hunger is a pressure, not the clock that ends the run.** A run ends in rescue or death, of
   anything (Andrew, 2026-09-17, 2026-09-26). The probes check when each way to eat becomes worth
   taking — roughly, what is aboard on day 1, the freight by day 3, the country or the pilot by day 5
   — as a check, not a schedule.
3. **Several ways, spending different resources** (§4.2).
4. **Food is physical.** Frozen salmon is hard as a plank until it thaws, though a knife still shaves it; a bulged can is visibly
   bulged; dog food is food. Nothing is "a food item" by type — edibility is a material property,
   and the interesting cases are all things that are edible in a way you would rather not think
   about. *(Shipped: edibility is a material property.)* **And food has states** — temperature,
   frozen, doneness, char, dryness, spoilage, contamination — that heat and time change, and that
   change what eating it does (§4.6). *(Andrew decided on 2026-09-26 that raw, cooked and spoiled
   differ; the axes are Claude's, for his check.)*
5. **The pilot's body is food, and eating it is taboo, not immoral** (Andrew, 2026-09-27). It is
   mechanically possible, slow and grim. It takes time, tools, preparation and the same food states as
   any meat: fresh raw meat is mostly safe and rotten meat is what makes people sick; meat cooked to a
   real core temperature is safe from what cooking kills, and freezing only pauses bacteria (document
   12 §4.3a).
   Butchery is hours of attended work and cooking needs the fire, so the difference between a decision
   and an impulse comes from the physics, not a special rule. The engine does not refuse it and does
   not editorialise; it is priced, witnessed and logged like any other act (document 15). *(The food
   facts are Claude's, from document 12, for Andrew's check.)*
6. **Never a menu.** Nothing tells the party to set a snare, names the forageable plants, or lists
   what is edible in the room. The grouse are described sitting in the branches "with the total
   unconcern of a bird that has never been wrong about anything", and the rest is the player's.

### 4.2 The ways to eat

| way | key resource it spends | where | the chain |
|---|---|---|---|
| **what is aboard** (the pockets, the luggage, the freight: flour, the coffee tin, a small bag of dog food) | search | the pockets, the luggage, the freight | `search <bag>` → `eat <what you find>` |
| **the country** (snares, forage, birds, fish) | knowledge + tools + daylight | the tamarack, the tussocks, the willows, the creek | `tie the wire into a noose` → `set the snare across the run` (the grammar forms of document 04 §3.1) — the operations are §4.8 |
| **the pilot's body** | the taboo | the cockpit | `butcher pilot with knife` — the acts are §4.8 |
| **Holt's stores** | travel | the homestead | modest stores, the reward for the walk there |

### 4.3 What is aboard (the pockets, the luggage, the freight)

Every food in the design, in one place and growing as the world is fleshed out, is the
[food list](food-list.md).

*(Content, with document 16 and the shipped object table.)*

- **There is no survival kit** (Andrew, 2026-09-27).
- **Pockets** — the guide's chocolate bar; the kid's candy bar; the salesman's trail mix and hip
  flask; the townie's gum. A seat nobody plays is a dead character whose pockets can be searched
  (2026-09-27).
- **The freight** — a 10 lb (4.5 kg) bag of flour, about 16,000 kcal, roughly a day of the party's food and
  worth much only with water and a fire (2026-10-02); the coffee tin; a small bag of dog food (never enough
  to live on — Andrew, 2026-09-27); a box of shear pins, a toolbox. The
  anti-easy rule holds: the toolbox is in the crushed tail cone and wants prying.
- **The cooler** — a few fillets of a family's fish, a meal or two (2026-09-28), frozen, thrown onto the debris trail and rimed with frost. The
  fish stays frozen only while it stays cold — carried into a wreck warmed by a fire it thaws, and over
  days it spoils (§4.6) — and after the day-6 flurry the cooler is one more white shape on the white
  debris trail. It is a vessel as well as a meal.
- **At least one spoiled thing** (Andrew, 2026-09-26): **a half-rotten fish** (Andrew, 2026-09-27; where
  it lies is placed with the zones); and, Claude's proposals, a paper
  sack wedged behind the pilot's seat — a lunch from some earlier day, the bread furred green and the
  meat in it slimed; it smells before it is opened, and `examine`, a sniff or a taste give it away (the
  signifier rule, document 03 §4.6). Holt's **bulged can** (§4.4) is the second. The country adds its
  own — mushrooms the frost killed, rotting where they stood (document 23 §4.2) — and the spoilage
  system (§4.6) makes more of whatever the party mishandles. The poisonous mushrooms are document 23's.
- **The mail sack** — letters, postmarks, a parcel of candles, a parcel for V. Holt. Not food.
- **The thermos of coffee** in the cockpit — the first warm thing anyone drinks.

### 4.4 The country (content — the valley's food, zone by zone)

*(The zones are document 01's. Every line is a floor, not a list of what is possible. The October
state of every living thing is document 23 §4.2–§4.3.)*

| zone | what it offers | what it costs |
|---|---|---|
| `tussock_flat` | lowbush cranberries, frost-sweetened on the bare mats, and bog cranberries in the wet hollows; each flurry covers more, and the day-6 snow buries the bog cranberries while the lowbush cranberries poke through | knowledge + sweat; a real but marginal calorie trickle, priced honestly low so it cannot replace hunting |
| `labrador_thicket` | Labrador tea, leathery leaves that persist all winter | knowledge + a container + fire; warmth and morale, not calories |
| `lake_gate_willows` | the hare runs at the lake gate; a snare set on a run | wire or cordage + knowledge + the discipline to leave and come back |
| `grouse_thicket` | spruce grouse — real protein, comically tame | anything within reason thrown, a slow approach (rushing flushes the birds a zone away for hours — a few birds, not a flock: Andrew, 2026-09-26), then plucking, cleaning and the whole fire chain |
| `hare_runs` | the snare line — the valley's best protein-per-effort | wire, reading which runs are fresh — easiest the morning after a flurry, when every track is new — setting loops right, and *leaving*; it pays on return visits, hours later |
| `aspen_fringe` | browse sign pointing back to the hare runs | the noticing; one snare |
| `chaga_tree` | chaga — tinder fungus, and the hot-drink loop | a climb, a throw, a pole or a chop |
| `gravel_bar_willows` | ptarmigan — a few birds, turning white (document 23 §4.3), invisible on the new snow until they move, conspicuous against bare brush where the snow has not lain — and rose hips, frost-softened on the stem, at about 160 kcal per 100 g of hip (USDA) richer than any berry; the seeds and their hairs must come out | patience in cold minutes; the rose hips are vitamin and morale food, free but thorn-priced and never filling |
| `confluence_pool` | the fishery — burbot and grayling, the valley's only food source that scales; the grayling are leaving small streams for deep water before freeze-up, burbot feed from sunset to midnight, and the pool is open | the longest tool-and-knowledge chain on the map: a line cast into open water, a willow jig rod, line and hooks, bait, and patience; a hole through the ice only if ice comes that holds a body (§4.8) |
| `food_cache_margin` | the beavers' larder: green pole stock and fresh aspen inner bark, being built now — the beavers cut and sink it before the ice locks the pond, working at dusk | inner bark is food, and the snare line's upgrade bait (bait a run, double the take) |
| `the_lodge` | nothing, deliberately | hacking in is possible and is a bad trade: the lodge stores food in the water, not the walls — the map's one anti-loot lesson |
| `drowned_set` | yards of snare wire on a trapper's pole | cold fingers and patience; it opens the snare-line game fully |
| `marten_set_tree` | Holt's old marten set — the box and its snare wire, empty: the trapping season has not opened | perception, and prying the box open |
| `cabin_interior` | Holt's shelf: flour, salt, lard, tea, a few tins — and **one bulged can** among the good ones | the walk; and the examine-gated poison lesson (a careful look shows the bulge) |
| `cache` | the rest of Holt's modest stores: some beans and rice, a slab of dry fish | the whole journey, the climb, and carrying it back down and home |

**Grubs and inner bark are food** (Andrew, 2026-09-18). Grubs live under the bark of dead and rotting spruce
and birch, carpenter ants winter in rotting logs, and stonefly and caddis larvae live under the creek's
stones all winter — a handful of food, and bait (document 23 §4.3); inner bark is food *and* snare bait, which is two facts rather than a choice between them.

**Food events** (document 13's event deck): ravens scout the wreck and find the food cache before you
do; ptarmigan flush (food if you're quick); and the scavengers come again wherever
food is mishandled — the world's first scavenger pressure. Storing food badly is a mechanic, not a
flavour note.

**The scavengers act** (document 23 §4.1a, 2026-10-01). The **bear**,
a male grizzly up all week and feeding hard before he dens, follows its nose to food from a long way off, and food kept
at the wreck is what brings it there — the most dangerous thing in the valley is drawn by the easiest
mistake; the **raven** pair and a **gray jay** or two find a cache within the hour; the **fox** robs a
snare line and eats what hangs in it. So where food is kept is a real choice with real trade-offs —
outside it stays cold and keeps, and anything can reach it; inside the warmed wreck it is guarded and
it spoils (§4.6); hung from a line between two trees, high and well out from either trunk, it is out of
the fox's reach and a grizzly's — a black bear climbs.

### 4.5 The body as a food source

*(The taboo and the pilot have their own documents; this is the food half.)* A body is a physical
object with identity, clothing, inventory, mass, temperature, wetness, injuries and contamination —
the same entity as a living body (document 12 §4.3a). What can be done with one: search, move, carry, drag, cover, bury, burn, leave, protect from
animals, take the clothing, recover the inventory, identify, mourn, hide, use as a grim windbreak, use
as emergency food. The engine's job is to make each of those a real operation with a real cost, and to
remember which one you chose.

A body is also meat with the food states of §4.6, and its temperature is a state like any other
thing's *(proposed by Claude, for Andrew's check)*. The pilot's body sits at the cockpit's temperature
(document 13 §4.2) and does not freeze through for days; a fire kept in the plane warms the cabin and
the body with it, and the spoilage system runs on it exactly as it runs on a hare. Where the body is
kept is therefore a real decision twice over: the taboo (documents 12 and 15) and the physical one.

### 4.6 Food states, heat and spoilage (Andrew, 2026-09-26; the working-out accepted 2026-09-27)

**Heat is a state on everything that has it** (Andrew, 2026-09-26). Every food entity carries a
`temperature` (integer tenths of a degree, the same unit as the body's core, document 08 §4.1), and the
**heat system** changes it: a fire heats its area and leaves residual heat in the areas around it; the
plane is an entity whose openings are open or closed and whose internal heat a fire inside raises;
things take heat by radiation (held over flame), by contact (on the coals, on a hot lid), by
conduction through a vessel and the water in it, and lose it to cold air, snow and wind — thin things
fast, thick things slowly (heating time grows with the square of the thickness, which is why a
quartered hare cooks and a whole frozen salmon takes an afternoon to thaw). *The heat system is owned by
its own design document, to be written (`PLAN.md` A10); this section says what food does with heat.*

**The food states** — each a real axis in the entity's `states` (document 05 §4.5), each changed by a
system, each with a real consequence:

| state | what changes it | what it does | source |
|---|---|---|---|
| **frozen** (the fraction of its water that is ice) | temperature over time; thawing costs latent heat | frozen fish and meat still cut with a knife — shaved thin, as northern people eat them (Andrew, 2026-09-27) — though they bend and chew like wood, not flesh; eating them frozen costs body heat (document 12 §4.3a); frozen food keeps | physics |
| **doneness** (the highest core temperature reached, and how long it was held) | heat into the core | kills what cooking kills at real core temperatures: 63 °C for whole cuts and fish, 71–74 °C for wild game — bear always cooked through, because the trichinosis worm survives freezing (USDA 160 °F; ADF&G 165 °F) — and 74 °C for birds and hare (against rabbit fever); cooked meat and cooked starch give the body more energy than raw | USDA FSIS safe minimum temperatures; CDC / ADF&G on the trichinosis worm; ADF&G rabbit fever (tularemia) guidance; Carmody et al., *PNAS* 2011; document 12 §4.3a |
| **char** (the burnt fraction of the surface) | surface held in flame or on coals too long | charred food is carbon — calories gone, bitter; a burnt thing's mass partly becomes ash (conserved, document 07) | physics |
| **dryness** (water fraction lost) | air, fire and smoke over hours and days | dried meat and fish keep and weigh less; smoke slows spoilage further | established practice |
| **spoilage** (microbial load) | time spent warm: bacteria grow fast between about 4 °C and 60 °C (doubling in as little as twenty minutes at the warm end), slowly near 0 °C, effectively not at all frozen | spoiled food smells, slimes and discolours (`sensed`), and eating it brings vomiting and diarrhoea within hours — water and the meal lost. **Cooking kills the bacteria but not every toxin**: staph toxin survives boiling, so cooking spoiled meat does not save it; botulinum toxin is destroyed by ten minutes' boiling, but the bulge is the warning | USDA "danger zone"; staph enterotoxin heat stability (e.g. *PLOS One* 2017); CDC on botulism |
| **contamination** (provenance, as in document 09) | gut contents from a careless cut, fuel, dirt, ash | tastes and smells of it; gut contents carry bacteria into the meat | document 09 §4.6 |
| **pathogen / parasite** (hidden, set by species and the seed) | nothing but heat to a real core temperature; **freezing does not kill the trichinosis worm** | undercooked bear: trichinellosis (stomach within days, muscles in weeks); undercooked hare, or gutting one bare-handed: rabbit fever (tularemia), a fever in about 3–5 days — inside a run; raw freshwater fish: tapeworm, which outlasts the run | ADF&G (the trichinosis worm in Alaska's bears; rabbit fever (tularemia) and snowshoe hares); CDC |

Whatever it is, food that sickens never kills: poison makes people very sick and never kills
(2026-09-27). Plant foods have their own real cases: raw mountain ash berries carry
an acid that brings on vomiting and cramps in quantity — frost starts converting it and
cooking finishes the job; raw starch in a root is barely digestible until it is cooked. What an
illness then does to a body is document 11's.

**The cooking operations** — each its own operation, because each moves heat differently (Andrew,
2026-09-26: variants that are ontologically significant are operations within the grammar):
`hold the grouse over the fire` (radiant, attended — you turn it or it chars); `put the fish on the
coals` / `bury the fish in the embers` (contact, fast, easy to burn); `boil the hare in the pot`
(water at the boil, the gentlest and most even, and the fat stays in the broth); **stone-boiling** —
`put the hot stones in the bark bowl` — for a vessel that cannot go on a fire (a birch-bark basket, a
hide; a real northern method, and it uses the heated stones document 08 §4.1 puts in); `fry the
meat on the lid` in fat; `smoke the fish over the fire` and `dry the strips by the fire` (hours to days,
unattended processes); `thaw the salmon`; `render the fat`; `crack the bone` for marrow. The grammar is
document 04 §3.1's (`VERB X RELATION Y [WITH Z]`); durations are honest (document 06): holding a spit
is attended work, a pot on the boil is a process that runs while you do something else. The cabin's
stove is the only purpose-built cook top in the valley.

**Where food is kept sets its temperature, and who finds it.** In October the outdoors is a cold room,
not a freezer (the temperatures by day are document 13 §4.2). Meat kept outside in shade stays cold and
keeps for the week; a carcass left ungutted keeps its own heat inside for hours and sours from within;
meat and fish kept in the wreck once a fire has warmed it spoil in a day or two; guts and fish go
first. And outside is where the bear, the ravens, the jays and the fox are (§4.4). Storage is a real
choice with a real trade-off, not decay for its own sake.

*This section is owned in full by the **food state and spoilage** design document, to be written
(`PLAN.md` A10), with the heat system; illness by document 11.*

---

### 4.7 What else the country holds (2026-09-18)

Everything the earlier passes and the valley design named is in — the freight and the mail,
the cooler's frozen salmon, the pockets, cranberries, crowberries, highbush cranberries, rose hips,
spruce-needle tea, Labrador tea, inner bark, chaga, the hare runs, ptarmigan and spruce grouse, the
red squirrel's midden, voles, **grubs under the bark**, the fishery, and the pilot's body. Document 23
holds the living inventory.

And these are what a forager in this country would also find, which the design first lacked. Each is
real here in October, and each is a row in document 23 §4.2–§4.3 and for the loops:

| addition | where | what it gives |
|---|---|---|
| **mountain ash (rowan) berries** | the birch stand, forest edges | bitter clusters that hang all winter and sweeten after frost — one of the few berries still *on* the tree at eye height |
| **bearberry (kinnikinnick)** | the ridge, dry open ground | mealy red berries that persist under snow; the leaves make a tea |
| **blueberries dried on the bush** | muskeg, open spruce | shrivelled and sweet where the birds missed them |
| **birch polypore and tinder conk** | dead and dying birch | one is a poor tea and a real medicine; both are tinder |
| **the squirrel's cached mushrooms** | wedged in spruce forks above the midden | dried by the squirrel in autumn; raiding a midden gets seeds *and* mushrooms |
| **spruce pitch** | any wounded trunk | chewable, antiseptic on a wound, and it burns |
| **rock tripe** | the boulder field, the erratic | famine lichen — edible after long boiling, sour and poor |
| **wintergreen / pyrola leaves** | under snow in the spruce | an evergreen leaf tea |
| **juniper berries** | the ridge, dry slopes | flavouring, and a hot drink |
| **marrow** | any bone from any kill | the calories the rest of the animal does not have |
| **hide** | any kill | boiled long enough it is food; the real last resort before the body |
| **blood** | any kill, if caught | dense calories, and it freezes |

**Audited against the place** (Andrew, 2026-09-18): what realistically lives in an area of this size,
not food sources added because they happen to be possible. Existing in Alaska is not the test; living
in *this* habitat, in this month, in numbers that matter, is. On that test:

- **Solid** — bearberry (dry ridges, berries persist), birch polypore (common on birch), the squirrel's
  cached mushrooms, spruce pitch, rock tripe (the boulder field), wintergreen, juniper (dry slopes),
  and marrow, hide and blood, which are not species at all but parts of any kill.
- **Occasional, and the row says so** — mountain ash: present in the interior but never abundant, so a
  few trees in the birch stand, not a harvest.
- **Rare** — blueberries dried on the bush: by October the birds and the bear have usually had them.
  They stay as a lucky find, not a food source.

None of these replaces anything, and nothing is dropped for being surplus. The list is a floor — but a
floor of things that are genuinely *there*, in the numbers document 23 §4.4 gives them.

**What October adds** (each a row in document 23 §4.2–§4.3 with its source and its density, reviewed
2026-10-02): **bog cranberry** in the muskeg; the **velvet foot**, a mushroom
that fruits in the cold on dead aspen and poplar, and the **deadly galerina** on the rotting logs
beside it — the one real lookalike that kills in life, and in the game makes a person very sick, since
poison never kills (2026-09-27); the **fly agaric**, the valley's commonest poisonous mushroom, and the
squirrels' caches that hold it among the good ones; **frost-killed mushrooms** rotting where they stood
(spoiled food the country makes itself); **wood frogs** frozen under the leaf litter by the ponds (a
find of a few grams); **ruffed grouse** in the aspen; the **beavers** out at dusk building their feed
pile; the **bear** (food and danger at once — fat before denning, and the trichinosis worm in the meat); and,
as candidates the loops check against this valley, **northern pike** in the lake, a **whitefish** run
in the creek, **muskrats** at the marsh, and the **root caches voles make in the sedge meadows**, which
people in western Alaska dig for.

### 4.8 Trapping, hunting, fishing and killing (Andrew, 2026-09-26; the techniques accepted 2026-09-27)

**The rule.** Anything a survival manual teaches can be done in the game (Andrew, 2026-09-27). Every
real technique is its own operation inside the grammar (document 04 §3.1), made
from entities whose capabilities derive from material × form × state (document 05 §4.2) — **a verb
never names a tool**. Anything fine and malleable enough can be a snare; anything long, rigid and
pointed can be a spear. The forms the canonical 26 (document 07) do not yet have — `noose`, `hook`,
`net`/`mesh` — are candidates for document 18; the goal-table rows (`make a snare`, `make a spear`,
`make a fishing line`) belong to the owning document. *The whole of this is owned by the **hunting,
trapping and fishing** design document and the **combat** design document, both to be written
(`PLAN.md` A10); this section fixes what each technique needs and how it is reached. Durations are
the owning document's to value; the starting chances are below, from the real rates in document 23 §4.4.*

**Trapping** — the plan-ahead work: set, leave, come back.

| technique | the real thing | what it needs | the acts |
|---|---|---|---|
| **wire snare on a run** | a slip loop about 10 cm across, its bottom about four fingers above the snow, set in front of the tracks at a choke point and anchored to a tree, root or stake; trappers use fine malleable wire (22–24-gauge brass) | wire with `cordage` and the stiffness to hold a loop open: the tool roll's stainless safety wire, strands stripped from the wiring harness, the drowned set's snare wire; cord works worse (paracord's inner strands, fishing line, a bootlace sag or stretch) — the physics says how much | `tie the wire into a noose` · `set the snare across the run` · `tie the snare to the sapling` · `push sticks in beside the run` (the funnel) · going back to `examine the snare` |
| **spring snare** (spring pole) | a bent sapling held by a notched trigger lifts the snared hare off the ground — out of the fox's reach, and a faster death | a live springy sapling (its `bent` state), two notched sticks (the shaping family, document 07) | `bend the sapling` · `notch the stick` · `hook the trigger under the peg` |
| **squirrel pole** | a pole leaned against a tree where squirrels live, with small wire snares along it; the squirrels run up it as a shortcut and into the loops | a pole, several small nooses | `lean the pole against the spruce` · `set the snares on the pole` |
| **deadfall trap** (figure-four) | a heavy flat rock or log propped on a carved trigger, baited; for voles, squirrels, marten | a slab with `heft`, three carved and notched sticks, bait | `carve the stick into a trigger` · `prop the rock on the trigger` · `put the bait under the rock` |
| **grouse noose on a pole** | a spruce grouse sits still enough to have a noose slipped over its head from a pole — the tamest bird in the valley allows it | a long pole, a small noose | `tie the noose to the pole` · `slip the noose over the grouse's head` |
| **fish trap** | willow stakes across a small creek funnelling fish into a basket or pen; a real northern way of taking fish on the move in fall | stakes, withies, a place where the creek narrows | `drive the stakes into the creek bed` · `weave the willow between the stakes` |

**Hunting and killing** — the combat system (Andrew, 2026-09-26: a combat system like a MUD's), the
same acts on a grouse, a hare, the bear or a person; the physics of the weapon, the body and the
animal's own behaviour decides.

| technique | what it needs | the acts |
|---|---|---|
| **throw** | a projectile — a rock, a billet, a throwing stick, a spear — whose mass and form set how it flies and hits; the thrower's arm (fitness, cold hands — document 08); the range and the target's size and behaviour. Anything within reason can be thrown. What happens is told as feedback, never a dice roll (Andrew, 2026-09-27) — a miss lands somewhere, and the rock is in the snow now | `throw the rock at the grouse` |
| **sling** | a pouch and two cords (a cloth scrap, a strip of hide, cord); more range and power than a hand throw, harder to aim for a beginner — practice improves it | `throw the stone at the ptarmigan with the sling` (and its synonyms) |
| **stab / thrust** | a `point` on something long enough to reach: a carved and fire-hardened pole, a knife lashed to a pole | `stab the hare with the spear` · `spear the fish` |
| **club / strike** | `heft`: a stick, a billet, the hatchet's back | `hit the grouse with the stick` · `club the hare` |
| **by hand** | a snared hare or a winged bird is dispatched by hand, quickly | `wring the grouse's neck` · `break the hare's neck` |

The bigger animals are fought with the same acts. The bear is a body with mass,
hide and its own behaviour (document 23 §4.1: the bear and some bigger animals are actors), and a party
with a spear and sticks against it is in real danger; nothing refuses the attempt, and a kill feeds the
party for the rest of the run.

**Fishing** — the water decides which technique works. At the start the creek and the lake are open,
with skim ice on still water; how far the ice grows through the week is document 13 §4.2's. The
through-the-ice techniques are real operations, but this week walking out on the ice breaks it
(Andrew, 2026-09-27).

| technique | the real thing | what it needs | the acts |
|---|---|---|---|
| **cast a line out** | a baited or lured hook thrown into open water — the creek mouth, the pool, the lake before it skins | line, hook, a weight, bait or a lure; a willow rod for reach; open water within a cast | `cast the line into the pool` |
| **drop a line through a hole** (jigging) | a line straight down through ice, worked up and down | a hole: `cut a hole in the ice with the hatchet` (a few minutes through new ice, far longer through thick; a rock breaks skim ice); the hole is an entity whose ice skins over again every cold night | `drop the line through the hole` · `jig the line` |
| **set line** | a baited hook left on the bottom overnight, tied off to a stick across the hole; the classic interior way to take burbot, which feed from sunset to midnight (ADF&G) | line, a big hook, bait, a sinker, a stick | `set the line through the hole` · `tie the line to the stick` — checked next day, frozen in |
| **spear fishing** | through a hole over clear new ice, the fish seen from above, sometimes drawn in by a decoy; interior Alaskans spear pike and whitefish this way (ADF&G) | a pronged or pointed spear; a hole; darkness over it helps the eye | `spear the pike` |
| **net** | a gill net under the ice between holes, or across the creek — the real subsistence method | mesh of the right size: the cargo net's mesh is far too coarse to hold a whitefish, and the physics says so; knotting a net from cord is real and days of work | `set the net under the ice` |
| **by hand** | a fish grabbed in a shallow riffle — it almost never works, but it can be tried (Andrew, 2026-09-27) | wading ice-cold water, and paying for it in wet and warmth (document 08) | `grab the fish` |

**Chances — starting points (2026-10-02).** Getting food from the country takes a few attempts and some
waiting, and a party that finds something to catch and really tries gets something eventually — never a
game where nothing works (Andrew, 2026-10-02). The chances below are per try, never shown, and read as
what happened, as in combat (document 11); play tunes them. What moves each is real: where it is set,
skill and practice, cold hands (document 08), distance, the animal's behaviour. The hare year is a middle year, the same every run (document 23 §4.4).

| way | target | chance per try (starting point) | what moves it |
|---|---|---|---|
| thrown rock | a spruce grouse sitting 5–10 m off | ~10 % | distance, cold hands, the arm; a spruce grouse usually stays put after a miss |
| thrown rock | a ptarmigan or a ruffed grouse | ~5 %, and a near miss flushes it | the same |
| thrown stick, spun end over end | a sitting grouse or hare | ~15 % — a bigger thing to hit with | the same |
| sling | a grouse at 10–20 m | ~5 % at first, rising to ~15 % with practice over the days | practice is the sling's real cost; it reaches further and hits harder |
| noose on a pole | a spruce grouse | ~40 % a try, if the bird stays | a slow approach |
| snare | a hare, per snare per night | **~20 %** set at a narrow spot (between trees, under a log, or brush funnelling the run) on a run with fresh tracks; ~10 % on a run without one; ~1 % off the runs; these are the valley's middle hare year (document 23 §4.4) | skill (a woodsman sets better), wire over cord (a hare chews cord), the loop's size and height, fresh human scent; a fox takes about one catch in five |
| baited deadfall | a vole or squirrel, per night | ~15 % | set on a runway |
| line from the shore | grayling, per hour in the right place | ~20–30 % a fish | dusk, the pool, grubs for bait |
| set line, overnight | burbot, per hook | ~25 % | they feed from sunset to midnight |
| spear | a fish in the shallows | ~5 % a thrust | clear, still water |

So ten snares on good runs catch about two hares a night, and about nine parties in ten find at least
one the first morning; a few minutes of throwing brings down a grouse. **An empty snare is never a
blank** — tracks going around it (the wrong spot), the loop sprung and empty (too big: the hare pulled
free), the snare knocked flat, fur and blood and fox tracks (robbed): each tells the trapper something
real. The sources for the snare rate are document 23 §4.4.

**Luck and practice** (2026-10-02). Each try is a plain roll of the dice, as real luck is. What keeps a
party that really tries from an endless losing streak is that every character gets better with
practice — the hidden skill sheet (document 16 §4.1): the thrower learns the range, the trapper learns
where a snare catches. A thrower who starts at one in ten and improves a little with each throw almost
never misses thirty in a row. If play shows that streaks still hurt, luck drawn like a shuffled deck —
a losing run cannot last long — is the fallback.

**After the kill** — butchery is its own family of real acts on the body's parts, the same for any
body *(proposed by Claude, for Andrew's check — decided in document 12 §4.3a)*. `butcher` is the
canonical word for an **attended activity** (document 06) that works through a body part by part and
banks its progress on the body; inside it the finer acts are their own operations because each does
something different: bleed; `skin`; `pluck`; `scale`; `gut`, opening the body cavity (puncture the gut
and the meat is contaminated; bare hands in a hare's insides are how rabbit fever (tularemia) is caught, ADF&G);
`cut <part> off` at a joint; `cut meat from <part>`; bone; fillet; cut into strips for drying; `crack`
a bone for its marrow. They are the same operations the hare, the grouse, the fish, the bear and the
pilot take. To the engine a person is not special; what differs is the entity (78 kg, clothed, its
states) and who sees it (document 15) — and for the pilot, document 12 counts about 38,000 kcal of
muscle. Each part is an entity with its materials and grams (conservation, document 05): meat, fat,
liver and heart, guts (bait), hide (food if boiled long enough, and a vessel, and clothing), bones and
their marrow, blood.

## 5. Interactions

**This depends on:**
- **07 Fire and shaping** — cooking, thawing, and the chaga/labrador hot-drink loop.
- **09 Water** — the vessel and the fire are shared; dehydration and hunger compound.
- **06 Time, sleep and the clock** — hunger is spent on the heartbeat; snares pay on *return visits,
  hours later*, which is the clock doing design work.
- **13 Events, escalation and weather** — the food row of the ladder; ravens,
  daylight for foraging; the flurries that cover the low berries a little at a time.
- **18 Materials and forms** — edibility is a material property; wire and cordage make snares; the
  forms `noose`, `hook` and `net`/`mesh` are candidates (§4.8).
- **01 Premise and world** / **17 Rooms** — the country's food lives in the outdoor zones.
- **23 Flora and fauna** — what lives here in October, what each yields, and the animals that act.
- Systems with no design document yet (`PLAN.md` A10): **the heat system** (heat as a state on every
  entity and body part; fire heating its area with residual heat around it; the plane's openings and
  internal heat) — §4.6 reads it; **food state and spoilage** — §4.6 is its seed; **hunting, trapping
  and fishing** and **combat** — §4.8 is their seed; **animal behaviour** (the actors of document 23) —
  the scavengers of §4.4.
- **11 Injury and first aid** §4.6 — what a poison, bad meat or an illness does inside the body; **12
  The pilot and bodies** §4.3a — the body as an entity and its butchery.

**These depend on it:**
- **08 Warmth** — a calorie deficit is a warmth input; a body that can't work can't stay warm, and an
  empty body shivers less.
- **11 Injury and first aid** — the bulged can; starvation weakness; cleaning game with a blade.
- **12 The pilot and bodies** — the body as a food source is this system pointing at that one.
- **15 Moral and social layer** — the last ration, the hidden chocolate bar, and the pilot.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-16** — first draft; this system had no design document of its own.
- **2026-09-18 (Andrew)** — grubs and inner bark are in, and asking what else is missing replaced any
  question of cutting: twelve more real foods added (§4.7).
- **2026-09-18 (Andrew)** — the additions audited against the place: habitat, month and density, not
  mere possibility. Most stand; mountain ash is occasional and dried blueberries a lucky find. The
  valley's real carrying capacity is document 23 §4.4, the spine of the food clock: a good day of
  foraging by the whole party is one to two thousand calories against twelve to fifteen thousand
  burned.
- **2026-09-26 (Andrew)** — hunger as in real life; a run ends in rescue or death, of anything; cooking
  as part of a heat and state system; raw, cooked and spoiled differ, with spoiled food and poisonous
  mushrooms; a combat system like a MUD's; hunting, trapping, fishing and killing as real operations
  with their variants; a bear, and no wolverine. Claude to answer the rest from the decided design and
  real life, for his check.
- **2026-09-26 (Claude)** — §4.1, §4.6 and §4.8 written from those decisions; butchery, spoilage and
  the safety of human meat answered from document 12 and real data, for Andrew's check; the season
  revised to October.
- **2026-09-27 (Andrew)** — there is no survival kit. Carried in with it: the first week of October, the pilot's body as taboo and
  not immoral, poison that never kills, Holt's modest stores, and the pockets of a seat nobody plays.
- **2026-09-27 (Andrew):** hunger's physiology accepted — real energy stores, symptoms in the real order,
  starvation weakening within the week rather than killing (§4.1).
- **2026-09-27 (Andrew):** there is no survival kit; the ways to eat accepted (§4.2); a half-rotten fish
  is among the spoiled things (§4.3).
- **2026-09-27 (Andrew):** the country's food accepted (§4.4, §4.7) — no ravens digging at the mail;
  Holt's marten set kept, empty; anything within reason can be thrown.
- **2026-09-27 (Andrew):** food states, cooking and storage accepted (§4.6); frozen fish and meat still cut
  with a knife.
- **2026-09-27 (Andrew):** trapping, hunting, fishing and killing accepted (§4.8) — anything a survival
  manual teaches can be done; no moose; feedback, not dice, for throws; a fish grabbed by hand almost
  never works; walking out on the ice breaks it; common names first. Document 10 reviewed in full.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built**
- `game/world/sim/operations/handlers/eat.py` — `eat` / `bite` / `chew` / `devour` ov
- **2026-09-27 (Andrew):** what is aboard accepted (§4.3), with the dog food a small bag — never enough
  to live on.
er any material
  with an edibility property; a low-edibility material gets the meagre-meal narration. Eating
  consumes the thing, ledger-balanced.
- Edible materials in `materials/table.py`: `rations`, `chocolate`, `fish`, and `snow` (low
  edibility — which is why `eat snow` currently succeeds).
- Food objects in `objects.py`: two ration tins, the chocolate bar, the coffee tin, the thermos of
  coffee, the bag of trail mix, the sack of dog food, the frozen salmon in the cooler (carrying a
  temperature state), plus the guide's and kid's pocket bars in `characters.py`.
- Tests: `game/tests/sim/test_operations_survival.py` covers eating a ration with conservation and
  the inedible non-match. Probe `kit.luggage.eat_kibble` exercises the dog food.

**Designed, not built**
- The body's energy stores on the clock, and hunger's bands (§4.1).
- No survival kit (§4.3) — the shipped slice still has one, as a torn duffel out on the debris trail.
- The country's food, zone by zone (§4.4) — designed for the whole valley, none of it in the object
  tables yet; the outdoor zones are themselves still to be authored as data.
- Snares, throwing and fishing as operations (§4.8).
- The bodies model and the butchery chain (documents 12 and 15).
- The scavengers — the bear, the ravens, the jays and the fox — as actors, and the cache-raid pressure
  (§4.4, document 23).
- The food states, the cooking operations and the trapping, hunting and fishing operations (§4.6,
  §4.8) — nothing of them is built.

**Nothing**
- Eating has no nutritional effect: `eat` consumes the object and narrates; no number on the
  character changes, because there is no hunger number.
- No cooking, thawing-as-food, spoiling, storage or scavenger pressure; the frozen salmon's
  temperature state is carried and read by nothing.
- No `set snare`, no `throw`, no `fish`, no `butcher`, no `clean`/`prepare` — the handler set today is
  `bend, break, burn, cut, drink, eat, examine, light, make, melt, open/close, pour, pry, move,
  read, search/dig, take/put, talk, tie, use, wear, wrap, tear`.
- No bodies: the pilot is an entity, but there is no body model, no edible-in-emergency state, and
  no butchering chain.
