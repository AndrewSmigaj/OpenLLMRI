# 10 — Food and hunger: the kit, the freight, the country, the body

> **Status: `draft for review` (2026-09-16). NEW — this system had no design document of its own.**
> **Architecture counterpart:** none. **Sources:** `docs/investigation/design/rescue-graph.md` §FOOD
> (the four paths) · `docs/investigation/design/events-and-escalation.md` §2 (the food row of the
> escalation ladder) and §4 (the wildlife and bodies decks) ·
> `docs/investigation/design/time-and-stakes.md` §4 (hunger as a number) ·
> `docs/investigation/design/players-and-kit.md` §3 (the freight and the luggage) ·
> `docs/investigation/world/rooms.md` (the country's food, zone by zone) · GDD §31–§36
> ("food/death/bodies, incl. consequential cannibalism") · the archived AI seed `design.md` §36
> (food categories, the body block, the body interactions, the cannibalism rule), carried forward
> "unchanged" by GDD §31–§36 · code: `game/world/sim/operations/handlers/eat.py`.
> **Note:** the pilot, bodies and the moral question have their own documents (12 and 15); this page
> covers food, and treats a body as one of its sources.

> **The season was settled on 2026-09-26: October, at freeze-up.** The run starts with about an inch
> of snow, bushes dusted but visible, skim ice on the water, roots and berries still findable;
> the storm starts light and gets heavier over the days, and the snow piles up the way a real storm of
> that kind piles it up — part of the escalation ladder. A bear is in. Andrew, 2026-09-26: *"It starts
> with just an inch, you can still get to berries and such, with the storm it accumulates however much
> snow storms that start from light then get heavier over the days (part of the increasing challenge
> mechanic)"*; *"we can have a bear, that would be neat"*. The month is Claude's pick, at Andrew's
> request (*"you pick the month"*): freeze-up is October in interior Alaska — the first lasting snow,
> skim ice on still water, berries still on the bush, bears feeding hard before they den.
> **The October revision was done 2026-09-26** (Claude, `PLAN.md` task A8), from the real
> interior-Alaska record in document 23 §4.0 — **for Andrew's check**: §3, §4.1, §4.3–§4.8 and §6 now
> read for mid-October freeze-up, and the December passages that remain are struck or marked
> superseded. `PLAN.md` §5 and task A8.

---

## 2. Provenance

### Andrew's decisions

- **Multiple ways of getting food.** (2026-09-07.)
- **The game runs until the food runs out.** (2026-09-07.) The run is roughly a week; rescue can come
  earlier and it can run longer — and what ends it, if nothing else does, is food. Hunger is the
  clock behind the clock. *(Andrew, 2026-09-26: "the run ends when they die so that is misleading
  could be of anything" — a run ends in rescue or death, and death can come from anything; hunger is
  one pressure among many, not the clock that ends the run.)*
- **"Will we eat the pilot" is one of the few moral decisions here.** (2026-09-07.) Recorded in the
  provenance audit among his moral-spectrum decisions ("eating the pilot, stealing, hitting,
  killing"). Food is the system that generates the game's headline moral question.
- **The pilot dies within the first day**, nobody can talk to him, and he becomes a body.
  (2026-09-16.) The moral question therefore starts on day one, not at the end of a long decline.
  *(Superseded 2026-09-26: the pilot starts the run dead — Andrew, 2026-09-17. The question is there
  from the first hour.)*
- **The crash is in December** and **the plane is a 206-class single** with freight and mail aboard.
  (2026-09-16.) There is no galley and there are no airline meals; what food exists is the survival
  kit, people's own snacks, the freight, and the country. *(Superseded 2026-09-26 for the month only:
  October, at freeze-up — settled 2026-09-26, see the banner. The 206 and what food exists stand.)*
- **Hunger is as it is in real life, and the run ends in rescue or death, of anything.** (2026-09-26.)
  *"however it is in real life, also the run ends when they die so that is misleading could be of
  anything."*
- **Cooking is a state system.** (2026-09-26.) *"yeah like a system, a state system, we dont want to be
  lazy here - snow should melt into water, food change based on heat, it is part of the implementation
  of that particular object, body parts have heat as part of their ontology […] fire would generate
  heat in that area and residual heat in other areas, we will have the plane as an entity itself with
  flags for open or closed and a fire source rule which uses it's heat amount to change it's internal
  heat calue, so this would all be part of planning the design and implementation of the fire and heat
  system"*
- **Raw, cooked and spoiled differ; there is spoiled food and there are poisonous mushrooms; there is a
  combat system like a MUD's.** (2026-09-26.) *"obviously in a survival situation especially raw meat
  will be different, especially spoiled (there should be perhaps at least one spoiled thing, poisonous
  mushrooms, etc. it would have a combat system like a MUD"*
- **Hunting, trapping, fishing and killing are real operations with their variants.** (2026-09-26.)
  *"building snares needs stuff, you can set the snae, you can throw rocks or whatever you can fish in
  different ways (cast line out/drop line in starts the fishing mechanic of course and their variants
  because this is ontologically significant as long as they follow our grammar rules, but you can also
  kill things in other ways, stab with a spear beat with a stick whatever"*
- **A bear is in** (2026-09-26), and **no wolverine** (2026-09-17).

### Proposals (Claude)

- Calories as an integer spent per tick and per activity, with bands (`time-and-stakes.md` §4).
- The four food paths and their key resources (`rescue-graph.md` §FOOD).
- The escalation ladder's food row and the starvation curve (`events-and-escalation.md` §2).
- The freight, the mail sack, the cooler and each slot's edible pocket contents
  (`players-and-kit.md` §1, §3).
- The country's food, zone by zone (`rooms.md`) — the fullest single body of food content in the
  repo, and none of it is Andrew's.
- The seed's food categories and body block (`design.md` §36) come from the **archived AI-written
  seed**, not from Andrew. Two of its food categories — "passenger snacks" and "airline meals" — are
  **superseded** by the 206 decision and are dropped here.
- Everything about cooking, calories, and raw versus boiled is a proposal, and most of it is an open
  question rather than a design. *(2026-09-26: Andrew answered the shape — a heat and state system in
  which raw, cooked, burnt and spoiled really differ; §4.6 now carries it. The numbers in it are
  Claude's, from real data, for his check.)*

---

## 3. In one paragraph

*(Rewritten for October — Claude, 2026-09-26, `PLAN.md` A8; the pilot starts the run dead,
2026-09-17. For Andrew's check.)*

There is food, and there is not enough of it, and the distance between those two facts is the whole
week. The first day it is a question of finding it: ration tins lashed under the floor rings, a
chocolate bar in a pocket, a thermos, somebody's trail mix, a sack of dog food in the freight and a
family's frozen salmon in a cooler thrown out onto the debris trail. The country is still open in
the first days — lowbush cranberries sweet from the frost under an inch of snow, rose hips on the
creek bar, a fool hen in a spruce that will stand there and let you try twice — and the storm closes
it a little more each day, burying the low berries first. Around day three it stops being a search
and becomes work — snare wire and a hare run read right in the new snow and then *left alone*, a line
cast into the last open water at the creek mouth, and later a hole chopped through lake ice that was
too thin to stand on when they arrived. Meat that is not eaten has to be kept somewhere cold enough
not to spoil and far enough from the ravens and the bear, which is still up, feeding hard before it
dens. And the whole time there is the pilot's body, in the cockpit, from the first hour, and nobody
has to say anything about it because everybody has already thought it.

*(The paragraph as drafted on 2026-09-16, kept as the record: the salmon was "under a drift on the
trail", the ice "forty centimetres", and the pilot died during the first day.)*

---

## 4. The design

### 4.1 The rules

1. ~~**Hunger is a number on the body** — calories, spent per tick and per activity, added by eating.~~
   **Hunger follows real physiology** *(Andrew, 2026-09-26: "however it is in real life"; written by
   Claude 2026-09-26 — §6 Q2; for Andrew's check)*. The body carries its energy as real stores, each a
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
   What the player feels comes in `status` band words (document 08 §4.9), in the real order: hungry →
   light-headed, slow and cold once the glycogen is gone → the pangs fading by the second or third day
   as ketosis takes over (the dangerous quiet) → weak, clumsy, irritable, cold-intolerant and poor at
   judgement (what the Minnesota Starvation Experiment recorded over months of semi-starvation, Keys et
   al. 1950, arriving here in its early form). "Hungry enough to look at the
   pilot" stays a design goal (`time-and-stakes.md` §4), and it arrives through the body, not a timer.
   **Starvation alone kills in weeks, not days** — people fasting with water have died after 46–73
   days (the 1981 hunger strike) — so inside a week-long run hunger kills the way it does in real cold:
   through the cold, through the fall a weak body takes on the ice, through the bad decision. The kid's
   smaller reserves run out first. *(The figures are real starting points; the probes tune them.)*
2. ~~**Food is the run's back-stop.** No hard time barrier ends a run; the escalation ladder does, and
   food is one of its rungs: rations on day 1, the freight by day 3, the country or the pilot by day
   5, starvation math after that — a calories-per-day debt that becomes weakness, and weakness is
   cold (`events-and-escalation.md` §2). *(Numbers are proposals.)*~~ *(Superseded 2026-09-26 — Andrew:
   "the run ends when they die so that is misleading could be of anything". A run ends in rescue or
   death, and death can come from anything; hunger is a pressure through the body (rule 1), never the
   clock that ends the run. The ladder's food row — rations on day 1, the freight by day 3, the country
   or the pilot by day 5 — survives only as the probes' check on when each path becomes worth taking,
   not as a schedule.)*
3. **Several sources, spending different resources** — the at-least-three-paths rule (§4.2).
4. **Food is physical.** Frozen salmon is hard as a plank until it thaws; a bulged can is visibly
   bulged; dog food is food. Nothing is "a food item" by type — edibility is a material property,
   and the interesting cases are all things that are edible in a way you would rather not think
   about. *(Shipped: edibility is a material property.)* **And food has states** — temperature,
   frozen, doneness, char, dryness, spoilage, contamination — that heat and time change, and that
   change what eating it does (§4.6). *(Claude, 2026-09-26 — §6 Q3/Q4; for Andrew's check.)*
5. **Cannibalism is mechanically possible but slow, grim and consequential.** It requires time,
   tools, preparation, ~~cooking or freezing for safety~~ and the same food states as any meat —
   raw carries the real risks, meat cooked to a real core temperature is safe from what cooking kills,
   and freezing only pauses bacteria *(Claude, 2026-09-26 — §6 Q8; for Andrew's check)* — and it
   affects the ending (`design.md` §36, GDD §31–§36). The engine does not refuse it and does not
   editorialise; it is priced, witnessed and logged like any other act (see document 15).
6. **Never a menu.** Nothing tells the party to set a snare, names the forageable plants, or lists
   what is edible in the room. The grouse are described sitting in the branches "with the total
   unconcern of a bird that has never been wrong about anything", and the rest is the player's.

### 4.2 The four paths (the rescue graph's own check)

| path | key resource it spends | where | the chain |
|---|---|---|---|
| **the kit** (rations, chocolate, flour, the coffee tin) | search | the seat pocket, the survival duffel, the crate | `open tin` → `eat rations` |
| **the country** (snares, forage, birds, fish) | knowledge + tools + daylight | the tamarack, the tussocks, the willows, the lead | ~~`set snare with paracord at willows`~~ `tie the wire into a noose` → `set the snare across the run` *(grammar forms of document 04 §3.1; Claude, 2026-09-26)* — the operations are §4.8 |
| **the pilot's body** | the moral price | the cockpit | `butcher pilot with knife` — the real acts are §6 Q6 |
| **Holt's cache** | travel | the homestead | the walk-out route's reward |

### 4.3 What is aboard (the kit, the pockets, the freight)

*(Content; `players-and-kit.md` §1 and §3, and the shipped object table.)*

- **The survival kit** — two sealed ration tins (and the fishing kit) in the survival duffel. Dense,
  dull, life-sustaining. `players-and-kit.md` §5 proposes it lashed to the 206's floor rings in the
  baggage bay; the shipped slice has it as a torn duffel out on the debris trail. *(Conflict flagged
  2026-09-26: Alaska Statute AS 02.35.110, which document 01 and `plane-interior.md` §7 use as the
  realism anchor, requires **a week of rations per occupant** — more than two tins "for three" — and
  from 15 October it adds snowshoes, a sleeping bag and a wool blanket per occupant. How much of that is
  aboard and what the crash leaves of it is §6 Q9, Andrew's.)*
- **Pockets** — the guide's chocolate bar; the kid's candy bar; the salesman's trail mix and hip
  flask; the townie's gum.
- **The freight** — flour, the coffee tin, a sack of dog food, a box of shear pins, a toolbox. The
  anti-easy rule holds: the toolbox is in the crushed tail cone and wants prying.
- **The cooler** — a family's fish, frozen, ~~under the drift on the debris trail; it wants digging~~
  thrown onto the debris trail and dusted with the first snow; the fish stays frozen only while it
  stays cold — carried into a wreck warmed by a fire it thaws, and over days it spoils (§4.6) — and by
  the storm's later days the cooler is under the drift and wants digging *(October — Claude,
  2026-09-26, A8)*; it is a vessel as well as a meal.
- **At least one spoiled thing, from the start** *(Andrew, 2026-09-26: "there should be perhaps at
  least one spoiled thing, poisonous mushrooms"; the instances are Claude's proposals, 2026-09-26)*:
  a paper sack wedged behind the pilot's seat — a lunch from some earlier day, the bread furred green
  and the meat in it slimed; it smells before it is opened, and `examine`, a sniff or a taste give it
  away (the signifier rule, document 03 §4.6). Holt's **bulged can** (§4.4) is the second. The country
  adds its own — mushrooms the frost killed, rotting where they stood (document 23 §4.2) — and the
  spoilage system (§4.6) makes more of whatever the party mishandles. The poisonous mushrooms are
  document 23's.
- **The mail sack** — letters, postmarks, a parcel of candles, a parcel for V. Holt. Not food, and
  the ravens will teach you that (§4.4).
- **The thermos of coffee** in the cockpit — the first warm thing anyone drinks.

### 4.4 The country (content — the valley's food, zone by zone)

*(From `rooms.md`. Every line is a floor, not a list of what is possible. `rooms.md` wrote these zones
for July and this page first read them for December; the October state of a row is marked where it
differs — Claude, 2026-09-26, A8. The October state of every living thing is document 23 §4.2–§4.3.)*

| zone | what it offers | what it costs |
|---|---|---|
| `tussock_flat` | lowbush cranberries, ~~frozen hard at the tussock bases~~ *(October:)* frost-sweetened on the mats under the first inch of snow, and bog cranberries in the wet hollows; the storm buries them day by day | knowledge + sweat; "a real but marginal calorie trickle — priced honestly low so it can't replace hunting" |
| `labrador_thicket` | labrador tea, leathery leaves that persist all winter | knowledge + a container + fire; warmth and morale, not calories |
| `tamarack_island` | the ravens' dig — a mail bundle, nothing to eat | knowledge (reading tracks); "a red herring with a heart" that teaches *tracks point at calories* |
| `lake_gate_willows` | the hare runs at the lake gate; a snare set on a run | wire or cordage + knowledge + the discipline to leave and come back |
| `grouse_thicket` | spruce grouse — real protein, comically tame | a thrown billet, a slow approach (rushing flushes ~~the flock~~ the birds a zone away for hours — a few birds, not a flock: Andrew, 2026-09-26), then plucking, cleaning and the whole fire chain |
| `hare_runs` | the snare line — "the valley's best protein-per-effort" | wire, reading which runs are fresh, setting loops right, and *leaving*; it pays on return visits, hours later |
| `aspen_fringe` | browse sign pointing back to the hare runs | the noticing; one snare |
| `chaga_tree` | chaga — tinder fungus, and the hot-drink loop | a climb, a throw, a pole or a chop |
| `game_trail_crossing` | a moose, ~~kept permanently offstage~~ *(superseded 2026-09-26: whether the moose is an actor is Andrew's — document 23 §6 Q7; in October the rut has just ended)* | ~~not food: "a wall of meat that kills the careless; not food unless the party can kill it, which they can't"~~ *(superseded 2026-09-26: nothing is scripted "can't". A moose is a wall of meat that kills the careless; killing one with improvised weapons is the combat system's physics — possible, rare, and deadly to try — and if it happens it feeds the party for the rest of the run)* |
| `gravel_bar_willows` | ptarmigan (~~white on white — visible only when they move or to a deliberate slow examine~~ *(October:)* a few birds, mostly white by mid-October — invisible on the new snow until they move, conspicuous against bare brush where the snow has not lain) and rose hips | patience in cold minutes; the rose hips are "vitamin/morale food, free but thorn-priced and never filling" *(October: frost-softened on the stem, and at about 160 kcal per 100 g of hip — USDA — richer than any berry; the seeds and their hairs must come out)* |
| `confluence_pool` | the fishery — burbot and grayling, "the valley's only SCALING food source" *(October: the grayling are leaving small streams for deep water before freeze-up; burbot feed from sunset to midnight; the pool is still open at the start)* | the longest tool-and-knowledge chain on the map: ~~a chopped hole through 40 cm~~ *(October:)* a line cast into open water at first, and a hole through the new ice once it holds a body (§4.8), a willow jig rod, the kit's line and hooks, bait, and patience |
| `food_cache_margin` | the beavers' larder: green pole stock and fresh aspen inner-bark *(October: being built now — the beavers cut and sink it before the ice locks the pond, working at dusk)* | not human food — the bark is the snare line's upgrade bait ("bait a run, double the take") |
| `the_lodge` | nothing, deliberately | hacking in is possible and is a bad trade: "the lodge stores food in the water, not the walls" — the map's one anti-loot lesson |
| `drowned_set` | yards of snare wire on a trapper's pole | cold fingers and patience; it opens the snare-line game fully |
| `marten_set_tree` | a marten frozen in the set — fur, not a meal | perception, prying the iced box, then skinning (blade + knowledge + stomach) |
| `cabin_interior` | Holt's shelf: flour, salt, lard, tea, a few tins — and **one bulged can** among the good ones | the walk; and the examine-gated poison lesson (the manual's food page names the bulge) |
| `cache` | the deep stores: beans, rice, a slab of dry fish | the whole journey, the climb, and carrying it all back down and home |

Two food sources named in the earlier design passes — **grubs** and **bark** as human food
(`rescue-graph.md` §FOOD, `events-and-escalation.md` §2) — **do not exist anywhere in the valley
design**, which gives the tamarack a mail bundle instead and treats inner bark as snare bait. Either
the world gains them or the passes drop them; flagged as an open question.

**Food events** (`events-and-escalation.md` §4): ravens scout the wreck and find the food cache
before you do; ~~a wolverine raids the cache at night, fearless, the classic camp thief~~ *(superseded:
no wolverine — Andrew, 2026-09-17)*; ptarmigan flush (food if you're quick); a hare in the snare; and
"they'll appear again wherever food is mishandled — the world's first scavenger pressure, played
gently". Storing food badly is a mechanic, not a flavour note.

*(October — Claude, 2026-09-26, A8; for Andrew's check.)* In October the scavengers are actors, not
events (document 23 §4.1): the **bear**, still up and feeding hard before it dens, follows its nose to
food from a long way off, and food kept at the wreck is what brings it there — the most dangerous
thing in the valley is drawn by the easiest mistake; the **raven** pair and the **Canada (gray) jays** find
a cache within the hour; the **fox** robs a snare line and eats what hangs in it. So where food is kept
is a real choice with real trade-offs — outside it stays cold and keeps, and anything can reach it;
inside the warmed wreck it is guarded and it spoils (§4.6); hung from a line between two trees, high
and well out from either trunk, it is out of the fox's reach and a grizzly's — a black bear climbs.

### 4.5 The body as a food source

*(The moral layer and the pilot have their own documents; this is the food half.)* A body is a
physical object with identity, clothing, inventory, mass, temperature, wetness, injuries,
contamination, relationship significance, morale impact — and an edible-in-extreme-emergency flag
(`design.md` §36). What can be done with one: search, move, carry, drag, cover, bury, burn, leave,
protect from animals, take the clothing, recover the inventory, identify, mourn, hide, use as a grim
windbreak, use as emergency food. The engine's job is to make each of those a real operation with a
real cost, and to remember which one you chose.

*(October — Claude, 2026-09-26, A8 and §6 Q7/Q8; for Andrew's check.)* A body is also meat with the
food states of §4.6, and its temperature is a state like any other thing's. In October the pilot's body
sits at the cockpit's temperature — near freezing by day, below it at night — and does not freeze
through for days; a fire kept in the plane warms the cabin and the body with it, and the spoilage
system runs on it exactly as it runs on a hare. Where the body is kept is therefore a real decision
twice over: the moral one (documents 12 and 15) and the physical one.

### 4.6 Food states, heat and spoilage (Claude, 2026-09-26 — §6 Q3, Q4, Q7; for Andrew's check)

~~**Cooking (proposal — thin, and honestly so).** Nothing in the repo designs cooking. What the sources
imply: the frozen salmon must thaw; the fish and the birds need cleaning before they need heat; raw meat
is edible and worse for you than cooked; cooking wants the same vessel and fire as boiling water; and
the cabin's stove has a cook top, which is the only purpose-built cooking surface in the valley. Whether
any of that is modelled beyond "heat changes a state" is question 4 below.~~ *(Superseded 2026-09-26 by
Andrew's answers to Q3 and Q4: cooking is part of a heat and state system, and raw, cooked, burnt and
spoiled really differ.)*

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
| **frozen** (the fraction of its water that is ice) | temperature over time; thawing costs latent heat | frozen meat cannot be cut or chewed like thawed meat; frozen food keeps | physics |
| **doneness** (the highest core temperature reached, and how long it was held) | heat into the core | kills what cooking kills at real core temperatures: 63 °C for whole cuts and fish, 71–74 °C for wild game — bear always cooked through, because *Trichinella* survives freezing (USDA 160 °F; ADF&G 165 °F) — and 74 °C for birds and hare (tularemia); cooked meat and cooked starch give the body more energy than raw | USDA FSIS safe minimum temperatures; CDC / ADF&G on *Trichinella nativa*; ADF&G tularemia guidance; Carmody et al., *PNAS* 2011; document 12 §4.3a |
| **char** (the burnt fraction of the surface) | surface held in flame or on coals too long | charred food is carbon — calories gone, bitter; a burnt thing's mass partly becomes ash (conserved, document 07) | physics |
| **dryness** (water fraction lost) | air, fire and smoke over hours and days | dried meat and fish keep and weigh less; smoke slows spoilage further | established practice |
| **spoilage** (microbial load) | time spent warm: bacteria grow fast between about 4 °C and 60 °C (doubling in as little as twenty minutes at the warm end), slowly near 0 °C, effectively not at all frozen | spoiled food smells, slimes and discolours (`sensed`), and eating it brings vomiting and diarrhoea within hours — water and the meal lost. **Cooking kills the bacteria but not every toxin**: staphylococcal toxin survives boiling, so cooking spoiled meat does not save it; botulinum toxin is destroyed by ten minutes' boiling, but the bulge is the warning | USDA "danger zone"; staphylococcal enterotoxin heat stability (e.g. *PLOS One* 2017); CDC on botulism |
| **contamination** (provenance, as in document 09) | gut contents from a careless cut, fuel, dirt, ash | tastes and smells of it; gut contents carry bacteria into the meat | document 09 §4.6 |
| **pathogen / parasite** (hidden, set by species and the seed) | nothing but heat to a real core temperature; **freezing does not kill *Trichinella nativa*** | undercooked bear: trichinellosis (stomach within days, muscles in weeks); undercooked hare, or gutting one bare-handed: tularemia, a fever in about 3–5 days — inside a run; raw freshwater fish: tapeworm, which outlasts the run and belongs to the recap | ADF&G (*Trichinella* in Alaska's bears; tularemia and snowshoe hares); CDC |

Plant foods have their own real cases: raw rowan berries carry parasorbic acid, which brings on vomiting
and cramps in quantity — frost starts converting it and cooking finishes the job; raw starch in a root
is barely digestible until it is cooked. What an illness then does to a body is document 11's.

**The cooking operations** — each its own operation, because each moves heat differently (Andrew,
2026-09-26: variants that are ontologically significant are operations within the grammar):
`hold the grouse over the fire` (radiant, attended — you turn it or it chars); `put the fish on the
coals` / `bury the fish in the embers` (contact, fast, easy to burn); `boil the hare in the pot`
(water at the boil, the gentlest and most even, and the fat stays in the broth); **stone-boiling** —
`put the hot stones in the bark bowl` — for a vessel that cannot go on a fire (a birch-bark basket, a
hide; a real northern method, and it uses the heated stones document 08 Q10 already put in); `fry the
meat on the lid` in fat; `smoke the fish over the fire` and `dry the strips by the fire` (hours to days,
unattended processes); `thaw the salmon`; `render the fat`; `crack the bone` for marrow. The grammar is
document 04 §3.1's (`VERB X RELATION Y [WITH Z]`); durations are honest (document 06): holding a spit
is attended work, a pot on the boil is a process that runs while you do something else. The cabin's
stove is still the only purpose-built cook top in the valley.

**Where food is kept sets its temperature, and who finds it.** In October the outdoors is a cold room,
not a freezer: at the start the afternoons reach about +1 °C and the nights −7 °C, a week later −2 and
−10 (document 23 §4.0). Meat kept outside in shade stays near or below freezing and keeps for the week;
a carcass left ungutted keeps its own heat inside for hours and sours from within; meat and fish kept
in the wreck once a fire has warmed it spoil in a day or two; guts and fish go first. And outside is
where the bear, the ravens, the jays and the fox are (§4.4). Storage is a real choice with a real
trade-off, not decay for its own sake.

*This section is owned in full by the **food state and spoilage** design document, to be written
(`PLAN.md` A10), with the heat system; illness by document 11.*

---

### 4.7 What else is missing (the question that replaced "what do we cut", 2026-09-18)

Everything the passes and the valley design named is in — the kit, the freight and the mail, the
cooler's frozen salmon, the pockets, cranberries, crowberries, highbush cranberries, rose hips,
spruce-needle tea, labrador tea, inner bark, chaga, the hare runs, ptarmigan and spruce grouse, the
red squirrel's midden, voles, **grubs under the bark**, the fishery under the ice, and the pilot's
body. Document 23 holds the living inventory.

And this is what a December forager in this country would also find, which the design did not yet
have. Every one of these is real here in winter, and each is a row for document 23 and the loops:
*(October, 2026-09-26: every row below is also real at freeze-up, most of them in better shape than in
December; their October state is in document 23 §4.2, where they are now rows.)*

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

**Audited against the place, 2026-09-18 (Andrew: "we have to think about what realistically is in an
area of that size … not just shove food sources in because they happen to be possible").** Existing in
Alaska is not the test; living in *this* habitat, in December *(October, since 2026-09-26)*, in numbers that matter, is. On that
test:

- **Solid** — bearberry (dry ridges, berries persist), birch polypore (common on birch), the squirrel's
  cached mushrooms, spruce pitch, rock tripe (the boulder field), wintergreen, juniper (dry slopes),
  and marrow, hide and blood, which are not species at all but parts of any kill.
- **Occasional, and the row says so** — mountain ash: present in the interior but never abundant, so a
  few trees in the birch stand, not a harvest.
- **Rare, and nearly gone by December** — blueberries dried on the bush: the birds and the bears have
  usually had them. It stays as a lucky find, not a food source. *(October: the same — by mid-October
  the birds and the bear have had most of them.)*

None of these replaces anything, and nothing is dropped for being surplus. The list is a floor — but a
floor of things that are genuinely *there*, in the numbers document 23 §4.4 gives them.

**What October adds** *(Claude, 2026-09-26 — A8 and Andrew's "at least one spoiled thing, poisonous
mushrooms"; each is a row in document 23 §4.2–§4.3 with its source and its density)*: **bog cranberry**
in the muskeg; the **velvet foot**, a mushroom that fruits in the cold on dead aspen and poplar, and
the **deadly galerina** on the rotting logs beside it — the one real lookalike that kills; the **fly
agaric**, the valley's commonest poisonous mushroom, and the squirrels' caches that hold it among the
good ones; **frost-killed mushrooms** rotting where they stood (spoiled food the country makes itself);
**wood frogs** frozen under the leaf litter by the ponds (a find of a few grams — the real animal in
the place of Andrew's lizards); **ruffed grouse** in the aspen; the **beavers** out at dusk building
their feed pile; the **bear** (food and danger at once — fat before denning, and *Trichinella* in the
meat); and, as candidates the loops check against this valley, **northern pike** in the lake, a
**whitefish** run in the creek, **muskrats** at the marsh, and the **root caches voles make in the sedge
meadows**, which people in western Alaska dig for.

### 4.8 Trapping, hunting, fishing and killing (Claude, 2026-09-26 — §6 Q5; for Andrew's check)

Andrew, 2026-09-26: *"building snares needs stuff, you can set the snae, you can throw rocks or
whatever you can fish in different ways (cast line out/drop line in starts the fishing mechanic of
course and their variants because this is ontologically significant as long as they follow our grammar
rules, but you can also kill things in other ways, stab with a spear beat with a stick whatever"*.

**The rule.** Every real technique is its own operation inside the grammar (document 04 §3.1), made
from entities whose capabilities derive from material × form × state (document 05 §4.2) — **a verb
never names a tool**. Anything fine and malleable enough can be a snare; anything long, rigid and
pointed can be a spear. The forms the canonical 26 (document 07) do not yet have — `noose`, `hook`,
`net`/`mesh` — are candidates for document 18; the goal-table rows (`make a snare`, `make a spear`,
`make a fishing line`) belong to the owning document. *The whole of this is owned by the **hunting,
trapping and fishing** design document and the **combat** design document, both to be written
(`PLAN.md` A10); this section fixes what each technique needs and how it is reached. Durations and
catch chances are the owning document's to value, from the real rates in document 23 §4.4.*

**Trapping** — the plan-ahead work: set, leave, come back.

| technique | the real thing | what it needs | the acts |
|---|---|---|---|
| **wire snare on a run** | a slip loop about 10 cm across, its bottom about four fingers above the snow, set in front of the tracks at a choke point and anchored to a tree, root or stake; trappers use fine malleable wire (22–24-gauge brass) | wire with `cordage` and the stiffness to hold a loop open: the tool roll's stainless safety wire, strands stripped from the wiring harness, the drowned set's snare wire; cord works worse (paracord's inner strands, fishing line, a bootlace sag or stretch) — the physics says how much | `tie the wire into a noose` · `set the snare across the run` · `tie the snare to the sapling` · `push sticks in beside the run` (the funnel) · going back to `examine the snare` |
| **spring pole** (twitch-up) | a bent sapling held by a notched trigger lifts the snared hare off the ground — out of the fox's reach, and a faster death | a live springy sapling (its `bent` state), two notched sticks (the shaping family, document 07) | `bend the sapling` · `notch the stick` · `hook the trigger under the peg` |
| **squirrel pole** | a pole leaned against a midden tree with small snares along it; the squirrels use it as a road | a pole, several small nooses | `lean the pole against the spruce` · `set the snares on the pole` |
| **deadfall** (figure-four, Paiute) | a heavy flat rock or log propped on a carved trigger, baited; for voles, squirrels, marten | a slab with `heft`, three carved and notched sticks, bait | `carve the stick into a trigger` · `prop the rock on the trigger` · `put the bait under the rock` |
| **grouse noose on a pole** | a spruce grouse sits still enough to have a noose slipped over its head from a pole — the tamest bird in the valley allows it | a long pole, a small noose | `tie the noose to the pole` · `slip the noose over the grouse's head` |
| **fish trap and weir** | willow stakes across a small creek funnelling fish into a basket or pen; a real northern way of taking fish on the move in fall | stakes, withies, a place where the creek narrows | `drive the stakes into the creek bed` · `weave the willow between the stakes` |

**Hunting and killing** — the combat system (Andrew, 2026-09-26: *"a combat system like a MUD"*), the
same acts on a grouse, a hare, the bear or a person; the physics of the weapon, the body and the
animal's own behaviour decides.

| technique | what it needs | the acts |
|---|---|---|
| **throw** | a projectile — a rock, a billet, a throwing stick, a spear — whose mass and form set how it flies and hits; the thrower's arm (fitness, cold hands — document 08); the range and the target's size and behaviour. Each throw is a seeded roll, announced; a miss lands somewhere, and the rock is in the snow now | `throw the rock at the grouse` |
| **sling** | a pouch and two cords (a cloth scrap, a strip of hide, cord); more range and power than a hand throw, harder to aim for a beginner — practice improves it | `throw the stone at the ptarmigan with the sling` (and its synonyms) |
| **stab / thrust** | a `point` on something long enough to reach: a carved and fire-hardened pole, a knife lashed to a pole | `stab the hare with the spear` · `spear the fish` |
| **club / strike** | `heft`: a stick, a billet, the hatchet's back | `hit the grouse with the stick` · `club the hare` |
| **by hand** | a snared hare or a winged bird is dispatched by hand, quickly | `wring the grouse's neck` · `break the hare's neck` |

The bigger animals are fought with the same acts. A moose, a wolf or the bear is a body with mass,
hide and its own behaviour (document 23 §4.1: the bear and some bigger animals are actors), and a party
with a spear and sticks against it is in real danger; nothing refuses the attempt, and a kill feeds the
party for the rest of the run.

**Fishing** — the ice decides which technique works, and the ice changes through the run (document 23
§4.0: open water and skim ice at the start, walkable new ice by the end of the first week at normal
temperatures).

| technique | the real thing | what it needs | the acts |
|---|---|---|---|
| **cast a line out** | a baited or lured hook thrown into open water — the creek mouth, the pool, the lake before it skins | line, hook, a weight, bait or a lure; a willow rod for reach; open water within a cast | `cast the line into the pool` |
| **drop a line through a hole** (jigging) | a line straight down through ice, worked up and down | a hole: `cut a hole in the ice with the hatchet` (a few minutes through new ice, far longer through thick; a rock breaks skim ice); the hole is an entity whose ice skins over again every cold night | `drop the line through the hole` · `jig the line` |
| **set line** | a baited hook left on the bottom overnight, tied off to a stick across the hole; the classic interior way to take burbot, which feed from sunset to midnight (ADF&G) | line, a big hook, bait, a sinker, a stick | `set the line through the hole` · `tie the line to the stick` — checked next day, frozen in |
| **spear fishing** | through a hole over clear new ice, the fish seen from above, sometimes drawn in by a decoy; interior Alaskans spear pike and whitefish this way (ADF&G) | a pronged or pointed spear; a hole; darkness over it helps the eye | `spear the pike` |
| **net** | a gill net under the ice between holes, or across the creek — the real subsistence method | mesh of the right size: the cargo net's mesh is far too coarse to hold a whitefish, and the physics says so; knotting a net from cord is real and days of work | `set the net under the ice` |
| **by hand** | a fish grabbed in a shallow riffle | wading ice-cold water, and paying for it in wet and warmth (document 08) | `grab the fish` |

**After the kill** — butchery is its own family of real acts on the body's parts, the same for any
body (§6 Q6): bleed, gut (opening the body cavity — and bare hands in a hare's insides are how
tularemia is caught, ADF&G), skin, pluck, scale, joint, bone, fillet, cut into strips for drying. Each
part is an entity with its materials and grams (conservation, document 05): meat, fat, liver and heart,
guts (bait), hide (food if boiled long enough, and a vessel, and clothing), bones and their marrow,
blood.

**This depends on:**
- **07 Fire and shaping** — cooking, thawing, and the chaga/labrador hot-drink loop.
- **09 Water** — the vessel and the fire are shared; dehydration and hunger compound.
- **06 Time, sleep and the clock** — hunger is spent on the heartbeat; snares pay on *return visits,
  hours later*, which is the clock doing design work.
- **13 Events, escalation and weather** — the food row of the ladder; ravens, ~~the wolverine~~ *(no
  wolverine, 2026-09-17)*, the hare in the snare, daylight for foraging; the storm that buries the low
  berries and insulates the new ice.
- **18 Materials and forms** — edibility is a material property; wire and cordage make snares; the
  forms `noose`, `hook` and `net`/`mesh` are candidates (§4.8).
- **01 Premise and world** / **17 Rooms** — the country's food lives in the fifty outdoor zones.
- **23 Flora and fauna** — what lives here in October, what each yields, and the animals that act.
- *(Added 2026-09-26.)* Systems with no design document yet (`PLAN.md` A10): **the heat system** (heat
  as a state on every entity and body part; fire heating its area with residual heat around it; the
  plane's openings and internal heat) — §4.6 reads it; **food state and spoilage** — §4.6 is its seed;
  **hunting, trapping and fishing** and **combat** — §4.8 is their seed; **animal behaviour** (the
  actors of document 23) — the scavengers of §4.4.
- **11 Injury and first aid** §4.6 — what a poison, bad meat or an illness does inside the body; **12
  The pilot and bodies** §4.3a — the body as an entity and its butchery.

**These depend on it:**
- **08 Warmth** — a calorie deficit is a warmth input; a body that can't work can't stay warm.
- **11 Injury and first aid** — the bulged can; starvation weakness; cleaning game with a blade.
- **12 The pilot and bodies** — the body as a food source is this system pointing at that one.
- **15 Moral and social layer** — the last ration, the hidden chocolate bar, and the pilot.
- **21 Endings and recap** — ~~"the game runs until the food runs out" is an ending condition~~
  *(superseded: the only endings are rescued or dead, and death can come from anything — Andrew,
  2026-09-17 and 2026-09-26)*, and what the party ate is part of the recap — including what does not
  show inside a week (a tapeworm from raw fish; document 12's prion and blood-borne risks).

---

## 6. Open questions

~~1. Do grubs and bark join the world, or leave the design?~~ **Answered 2026-09-18 (Andrew): they are
   in — and the question was wrong to ask.** The original recommendation was to drop them because
   the valley "already has" other food; that is scarcity reasoning, and this world has no ceiling.
   Grubs go under the bark of rotten spruce and birch; inner bark is food *and* snare bait, which is
   two facts rather than a choice between them. **The real question is what else is missing** — see
   §4.7 and document 23, which grew by a dozen rows in the same pass.
~~2. How hard does starvation bite in a week?~~ **Answered 2026-09-26 (Andrew):** however it is in
   real life — and the run ends when they die, of anything, so a question framed around the run ending
   when the food runs out was misleading. *(Written into §4.1 rules 1–2 by Claude, for his check: real
   energy stores and real symptoms; starvation alone takes weeks, so inside a run hunger kills through
   the cold, a weak body's fall and bad judgement.)* *(original)* *(a)* A real calorie ledger where a
   party that finds nothing dies around day 8–10. *(b)* Hunger degrades (weakness, cold tolerance,
   slower work) and the cold does the killing. Recommended then: (a) with (b)'s texture — Andrew
   decided the run ends when the food runs out, so the number has to be real; the visible symptoms
   should be weakness and cold long before the death.
~~3. Is cooking a system or a state change?~~ **Answered 2026-09-26 (Andrew):** a system — a state
   system, and not a lazy one. Snow melts into water; food changes with heat, as part of what each
   object is; body parts have heat in their ontology; a fire heats its area and leaves residual heat in
   the areas around it; the plane is an entity with openings flagged open or closed, and a fire-source
   rule uses the fire's heat to change the plane's internal heat — all of it part of designing and
   building the fire and heat system. *(Written into §4.6.)* *(original)* *(a)* A cooking system: raw /
   cooked / burnt, safety, yield. *(b)* Heat is heat — a thing near a fire gets hot, thaws, and
   eventually chars, and "cooked" is just a temperature state with a nutrition consequence.
   Recommended then: (b), "one rule instead of a subsystem".
~~4. Raw versus boiled — does it matter mechanically?~~ **Answered 2026-09-26 (Andrew):** obviously —
   in a survival situation raw meat is different, and spoiled meat especially; there should be at
   least one spoiled thing, and poisonous mushrooms; and there is a combat system like a MUD's. "Yes,
   modestly" made the world less interactive, not more. *(Written into §4.3, §4.6, §4.8 and document
   23.)* *(original)* Recommended then: yes, modestly — raw meat is edible and carries a small illness
   risk, cooked is safe and yields more; the manual's food page teaches it.
~~5. Does hunting need new operations, or does it fall out?~~ **Answered 2026-09-26 (Andrew):** it is
   ontology building. A snare needs stuff to build it, and you set it; you can throw rocks or whatever;
   you fish in different ways — casting a line out and dropping a line in each start the fishing
   mechanic, and so do their variants, because the difference is ontologically significant, as long
   as they follow the grammar rules; and you can kill things in other ways too — stab with a spear,
   beat with a stick, whatever. *(Written into §4.8.)* *(original)* The world design bills `throw`,
   `set/check snare` and `fish` as the three it assumes. Recommended then: `throw` and `set snare` as
   real operations, and fishing assembled from existing operations with only the catch as a seam.
~~6. How is the pilot's body prepared, in grammar terms?~~ **Claude's answer (2026-09-26), for Andrew's
   check — decided in document 12 §4.3a (its Q5), not re-decided here:** `butcher` is the canonical
   word for an **attended activity** (document 06) that works through a body part by part and banks
   its progress on the body; inside it the finer acts are their own operations because each does
   something different — `skin`, `gut` (puncture the gut and the meat is contaminated), `cut <part>
   off` at a joint, `cut meat from <part>`, `crack` a bone for its marrow — and they are the same
   operations the hare, the grouse, the fish and the bear take (§4.8). To the engine a person is not
   special; what differs is the entity (78 kg, clothed, its states) and who sees it (document 15). The
   old recommendation's "no special verb" was right that the verb does not know the target, and wrong
   in treating butchery as one cut. For the pilot, document 12 counts about 38,000 kcal of muscle.
~~7. Does food spoil, and does cold preserve it?~~ *(Wrong-headed: "yes, trivially — December does the
   preserving for free" collapsed a real process into a shortcut, and the month is now October.)*
   **Claude's answer (2026-09-26), for Andrew's check:** spoilage is a state on every food entity,
   driven by its temperature over time (§4.6): bacteria grow fast between about 4 °C and 60 °C, slowly
   near 0 °C and effectively not at all frozen (USDA). October is a cold room, not a freezer —
   afternoons about +1 °C at the start and −2 °C a week in, nights −7 to −10 °C (document 23 §4.0) — so
   meat kept outside in shade keeps for the week, meat kept in a wreck warmed by a fire spoils in a
   day or two, an ungutted carcass sours from the inside, and fish and guts go first. The other half
   of storage is the scavengers, who are actors now — the bear, the ravens, the jays, the fox; no
   wolverine (§4.4). Owned by the food state and spoilage design and the heat system, both to be
   written (`PLAN.md` A10).
~~8. What does the party know about eating people, mechanically?~~ **Claude's answer (2026-09-26), for
   Andrew's check — the facts are document 12 §4.3a's:** the seed's "cooking or freezing for safety" is
   half wrong, so it is replaced by the food states every meat has (§4.6, rule 5 of §4.1). Freezing
   stops bacteria growing but kills few of them; cooking through to about 74 °C kills bacteria and
   parasites but not heat-stable toxins, so spoiled meat stays dangerous cooked; freezing does not kill
   the Arctic *Trichinella* in bear meat (ADF&G). What a person's flesh carries that game does not —
   prion disease, blood-borne infection — shows in years, not inside a week, and belongs to what a
   player may know and to the recap (document 12). The act still takes time and fuel, because butchery
   is hours of attended work and cooking needs the fire: the difference between a decision and an
   impulse comes from the physics, not a special rule. *(original recommendation: keep the
   requirement.)*
9. **How much food does the survival kit really hold, and what does the crash leave of it?** Alaska
   Statute AS 02.35.110 — the realism anchor of document 01 and `plane-interior.md` §7 — requires **a
   week of rations per occupant**; the design has had two ration tins "for three" (`players-and-kit.md`),
   which is less than the law. Legal survival rations are "sufficient to sustain life" — dense bars and
   tins well under the 3,400–4,300 kcal a day the cold asks of a working adult (§4.1) — so even a full
   kit leaves everyone in deficit, and the pressure stays weakness and cold, not starvation. What is
   genuinely yours is how full the kit is and how the crash treats it. *(a)* The full legal week,
   intact and scattered by the crash — the party is hungry all week and never out of food; the country
   and the pilot are about strength and fat, not survival. *(b)* The full legal week, but the crash
   and the scavengers take a share — the tail is two hundred metres back up the scar, the duffel split,
   and the ravens, jays, fox and bear reach spilled tins and bars before a slow party does; what is
   left depends on how fast they get there. *(c)* A pilot who carried less than the law requires — two
   tins — and the week is short from the start. **Recommendation: (b)** — it keeps the statute true,
   makes the first hours' search and the race with the scavengers a real food act rather than a number,
   and lets the probes tune what the world takes by what the world does. *(original, 2026-09-16: are
   the two ration tins the right amount? — leave the number to the probes.)*

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18 (Andrew):** **Q1 answered, and the question retracted.** Grubs and bark are in; recommending
  a cut because the valley "already has" other food was scarcity reasoning in a world with no ceiling,
  and Andrew called it. §4.7 added: twelve more real December foods the design did not have (rowan,
  bearberry, dried blueberries, birch polypore, the squirrel's cached mushrooms, spruce pitch, rock
  tripe, wintergreen, juniper, marrow, hide, blood), each a row for document 23 and the loops. The
  writing rules in `docs/design/README.md` now forbid cut-for-economy questions outright.

- **2026-09-18 (Andrew):** the §4.7 additions audited against the place — habitat, month and density, not
  mere possibility. Most stand; mountain ash is marked occasional and dried blueberries a lucky find.
  The valley's real carrying capacity is now in document 23 §4.4 and it is the spine of the food
  clock: a good day of foraging by the whole party is one to two thousand calories against twelve to
  fifteen thousand burned.

- **2026-09-26 (Andrew): Q2–Q6, and why the rest of this document goes back to Claude.**
  - **Q2** — *"however it is in real life, also the run ends when they die so that is misleading could
    be of anything."*
  - **Q3** — *"yeah like a system, a state system, we dont want to be lazy here - snow should melt into
    water, food change based on heat, it is part of the implementation of that particular object, body
    parts have heat as part of their ontology (remember we are building a sufficient world with all the
    entities and relations needed and systems to change them, fire would generate heat in that area and
    residual heat in other areas, we will have the plane as an entity itself with flags for open or
    closed and a fire source rule which uses it's heat amount to change it's internal heat calue, so this
    would all be part of planning the design and implementation of the fire and heat system"*
  - **Q4** — *"raw vs boiled... so again you did the same thing in our GDD we had already discussed, you
    keep trying to make the world more interactive but less, obviously in a survival situation especially
    raw meat will be different, especially spoiled (there should be perhaps at least one spoiled thing,
    poisonous mushrooms, etc. it would have a combat system like a MUD but your vision is very tiny in
    the GDD."*
  - **Q5** — *"you just completely forgot about the ontology building, so building snares needs stuff, you
    can set the snae, you can throw rocks or whatever you can fish in different ways (cast line out/drop
    line in starts the fishing mechanic of course and their variants because this is ontologically
    significant as long as they follow our grammar rules, but you can also kill things in other ways,
    stab with a spear beat with a stick whatever"*
  - **Q6 and the rest** — *"it seems again you wrote this block wikthout really thinking about how the
    mechanics work, I just realized what the problem was, you wrote this before we iterated on the first
    section so you dont even know the mechanics probably, lets just stop here and have you review all
    thyese and see if you can't answer them themselves yourselves and then leave me the rest,
    implementation of the ontology is actually going to take time, there will be many systems."*

  Right on every count. This document, like 11–23, was drafted on 2026-09-16, before block 1 settled
  the ontology schema, states, forms and grammar (documents 03–05), and its recommendations shrank the
  world — "modestly", "one rule instead of a subsystem", "no special verb". The lessons are now writing
  rules in `README.md`. Claude re-reviews every remaining open question in 10–23 against block 1 and
  real life, answers what those answer (marked for Andrew's check), and leaves Andrew only what is his
  (`PLAN.md` task A9).

- **2026-09-26 (Claude, self-review — PLAN.md A9):** **Q2–Q5 marked answered in Andrew's terms** and
  the design text they affect rewritten: §4.1 rules 1–2 (hunger follows real physiology — glycogen,
  fat and protein stores, shivering on glycogen, starvation alone taking weeks, so hunger kills through
  the cold; the run ends in rescue or death, of anything), §4.6 (a heat and food-state system: frozen,
  doneness, char, dryness, spoilage, contamination, pathogens, with real temperatures and
  consequences, and the cooking operations each its own), §4.8 new (trapping, hunting, fishing and
  killing as real operations with what each needs and the grammar that reaches it), and the spoiled
  thing and poisonous mushrooms Andrew asked for (§4.3; document 23). **Answered for his check:** Q6
  (butchery — pointing to document 12 §4.3a, which decided it), Q8 (the seed's "cooking or freezing for
  safety" replaced by the real food states; document 12's facts). **Rewritten:** Q7 (spoilage "trivially,
  December preserves for free" was a shortcut and the wrong month). **Left for Andrew:** Q9, sharpened
  — how full the legally required kit is and what the crash leaves of it (a conflict with AS 02.35.110
  flagged in §4.3). **October revision (A8) done** across §3, §4.3–§4.7 and the banner; no wolverine,
  the pilot starts dead, the moose is no longer scripted "can't". Systems this needs that have no
  document: heat, food state and spoilage, hunting/trapping/fishing, combat, animal behaviour.

## 8. What exists today

**Built**
- `game/world/sim/operations/handlers/eat.py` — `eat` / `bite` / `chew` / `devour` over any material
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
- Calories on the clock, the bands, and the starvation curve (`time-and-stakes.md` §4;
  `events-and-escalation.md` §2).
- The country's food, zone by zone (`rooms.md`) — designed in detail for the whole valley, none of it
  in the object tables yet; the fifty outdoor zones are themselves still to be authored as data.
- Snares, throwing and fishing as operations (billed in `rooms.md`'s operations table with their
  degradations).
- The bodies model and the cannibalism chain (`design.md` §36; documents 12 and 15).
- The ravens / wolverine / cache-raid pressure (`events-and-escalation.md` §4). *(No wolverine,
  2026-09-17; the scavengers are the bear, ravens, jays and the fox, as actors — §4.4, document 23.)*
- The food states, the cooking operations and the trapping, hunting and fishing operations (§4.6,
  §4.8) — designed on this page, 2026-09-26; nothing of them is built.

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
