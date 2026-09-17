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

---

## 2. Provenance

### Andrew's decisions

- **Multiple ways of getting food.** (2026-09-07.)
- **The game runs until the food runs out.** (2026-09-07.) The run is roughly a week; rescue can come
  earlier and it can run longer — and what ends it, if nothing else does, is food. Hunger is the
  clock behind the clock.
- **"Will we eat the pilot" is one of the few moral decisions here.** (2026-09-07.) Recorded in the
  provenance audit among his moral-spectrum decisions ("eating the pilot, stealing, hitting,
  killing"). Food is the system that generates the game's headline moral question.
- **The pilot dies within the first day**, nobody can talk to him, and he becomes a body.
  (2026-09-16.) The moral question therefore starts on day one, not at the end of a long decline.
- **The crash is in December** and **the plane is a 206-class single** with freight and mail aboard.
  (2026-09-16.) There is no galley and there are no airline meals; what food exists is the survival
  kit, people's own snacks, the freight, and the country.

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
  question rather than a design.

---

## 3. In one paragraph

There is food, and there is not enough of it, and the distance between those two facts is the whole
week. The first day it is a question of finding it: two ration tins lashed under the floor rings, a
chocolate bar in a pocket, a thermos, somebody's trail mix, a sack of dog food in the freight and a
family's frozen salmon in a cooler under a drift on the trail. Around day three it stops being a
search and becomes work — snare wire and a hare run read right and then *left alone*, a fool hen in
a spruce that will stand there and let you try twice, a hole chopped through forty centimetres of
ice for fish that are actually down there. And the whole time there is the pilot, and then the
pilot's body, in the cockpit, getting colder, and nobody has to say anything about it because
everybody has already thought it.

---

## 4. The design

### 4.1 The rules

1. **Hunger is a number on the body** — calories, spent per tick and per activity, added by eating.
   Bands feed the status words and the pressure the moral layer needs: "hungry enough to look at the
   pilot" is a design goal, stated as such (`time-and-stakes.md` §4). *(Proposal.)*
2. **Food is the run's back-stop.** No hard time barrier ends a run; the escalation ladder does, and
   food is one of its rungs: rations on day 1, the freight by day 3, the country or the pilot by day
   5, starvation math after that — a calories-per-day debt that becomes weakness, and weakness is
   cold (`events-and-escalation.md` §2). *(Numbers are proposals.)*
3. **Several sources, spending different resources** — the at-least-three-paths rule (§4.2).
4. **Food is physical.** Frozen salmon is hard as a plank until it thaws; a bulged can is visibly
   bulged; dog food is food. Nothing is "a food item" by type — edibility is a material property,
   and the interesting cases are all things that are edible in a way you would rather not think
   about. *(Shipped: edibility is a material property.)*
5. **Cannibalism is mechanically possible but slow, grim and consequential.** It requires time,
   tools, preparation, cooking or freezing for safety, and it affects the ending (`design.md` §36,
   GDD §31–§36). The engine does not refuse it and does not editorialise; it is priced, witnessed
   and logged like any other act (see document 15).
6. **Never a menu.** Nothing tells the party to set a snare, names the forageable plants, or lists
   what is edible in the room. The grouse are described sitting in the branches "with the total
   unconcern of a bird that has never been wrong about anything", and the rest is the player's.

### 4.2 The four paths (the rescue graph's own check)

| path | key resource it spends | where | the chain |
|---|---|---|---|
| **the kit** (rations, chocolate, flour, the coffee tin) | search | the seat pocket, the survival duffel, the crate | `open tin` → `eat rations` |
| **the country** (snares, forage, birds, fish) | knowledge + tools + daylight | the tamarack, the tussocks, the willows, the lead | `set snare with paracord at willows` |
| **the pilot's body** | the moral price | the cockpit | `butcher pilot with knife` |
| **Holt's cache** | travel | the homestead | the walk-out route's reward |

### 4.3 What is aboard (the kit, the pockets, the freight)

*(Content; `players-and-kit.md` §1 and §3, and the shipped object table.)*

- **The survival kit** — two sealed ration tins (and the fishing kit) in the survival duffel. Dense,
  dull, life-sustaining. `players-and-kit.md` §5 proposes it lashed to the 206's floor rings in the
  baggage bay; the shipped slice has it as a torn duffel out on the debris trail.
- **Pockets** — the guide's chocolate bar; the kid's candy bar; the salesman's trail mix and hip
  flask; the townie's gum.
- **The freight** — flour, the coffee tin, a sack of dog food, a box of shear pins, a toolbox. The
  anti-easy rule holds: the toolbox is in the crushed tail cone and wants prying.
- **The cooler** — a family's fish, frozen, under the drift on the debris trail; it wants digging,
  and it is a vessel as well as a meal.
- **The mail sack** — letters, postmarks, a parcel of candles, a parcel for V. Holt. Not food, and
  the ravens will teach you that (§4.4).
- **The thermos of coffee** in the cockpit — the first warm thing anyone drinks.

### 4.4 The country (content — the valley's food, zone by zone)

*(From `rooms.md`. Every line is a floor, not a list of what is possible.)*

| zone | what it offers | what it costs |
|---|---|---|
| `tussock_flat` | lowbush cranberries, frozen hard at the tussock bases | knowledge + sweat; "a real but marginal calorie trickle — priced honestly low so it can't replace hunting" |
| `labrador_thicket` | labrador tea, leathery leaves that persist all winter | knowledge + a container + fire; warmth and morale, not calories |
| `tamarack_island` | the ravens' dig — a mail bundle, nothing to eat | knowledge (reading tracks); "a red herring with a heart" that teaches *tracks point at calories* |
| `lake_gate_willows` | the hare runs at the lake gate; a snare set on a run | wire or cordage + knowledge + the discipline to leave and come back |
| `grouse_thicket` | spruce grouse — real protein, comically tame | a thrown billet, a slow approach (rushing flushes the flock a zone away for hours), then plucking, cleaning and the whole fire chain |
| `hare_runs` | the snare line — "the valley's best protein-per-effort" | wire, reading which runs are fresh, setting loops right, and *leaving*; it pays on return visits, hours later |
| `aspen_fringe` | browse sign pointing back to the hare runs | the noticing; one snare |
| `chaga_tree` | chaga — tinder fungus, and the hot-drink loop | a climb, a throw, a pole or a chop |
| `game_trail_crossing` | a moose, kept permanently offstage | not food: "a wall of meat that kills the careless; not food unless the party can kill it, which they can't" |
| `gravel_bar_willows` | ptarmigan (white on white — visible only when they move or to a deliberate slow examine) and rose hips | patience in cold minutes; the rose hips are "vitamin/morale food, free but thorn-priced and never filling" |
| `confluence_pool` | the fishery — burbot and grayling, "the valley's only SCALING food source" | the longest tool-and-knowledge chain on the map: a chopped hole through 40 cm, a willow jig rod, the kit's line and hooks, bait, and patience |
| `food_cache_margin` | the beavers' larder: green pole stock and fresh aspen inner-bark | not human food — the bark is the snare line's upgrade bait ("bait a run, double the take") |
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
before you do; a wolverine raids the cache at night, fearless, the classic camp thief; ptarmigan
flush (food if you're quick); a hare in the snare; and "they'll appear again wherever food is
mishandled — the world's first scavenger pressure, played gently". Storing food badly is a mechanic,
not a flavour note.

### 4.5 The body as a food source

*(The moral layer and the pilot have their own documents; this is the food half.)* A body is a
physical object with identity, clothing, inventory, mass, temperature, wetness, injuries,
contamination, relationship significance, morale impact — and an edible-in-extreme-emergency flag
(`design.md` §36). What can be done with one: search, move, carry, drag, cover, bury, burn, leave,
protect from animals, take the clothing, recover the inventory, identify, mourn, hide, use as a grim
windbreak, use as emergency food. The engine's job is to make each of those a real operation with a
real cost, and to remember which one you chose.

### 4.6 Cooking (proposal — thin, and honestly so)

Nothing in the repo designs cooking. What the sources imply: the frozen salmon must thaw; the fish
and the birds need cleaning before they need heat; raw meat is edible and worse for you than cooked;
cooking wants the same vessel and fire as boiling water; and the cabin's stove has a cook top, which
is the only purpose-built cooking surface in the valley. Whether any of that is modelled beyond
"heat changes a state" is question 4 below.

---

## 5. Interactions

**This depends on:**
- **07 Fire and shaping** — cooking, thawing, and the chaga/labrador hot-drink loop.
- **09 Water** — the vessel and the fire are shared; dehydration and hunger compound.
- **06 Time, sleep and the clock** — hunger is spent on the heartbeat; snares pay on *return visits,
  hours later*, which is the clock doing design work.
- **13 Events, escalation and weather** — the food row of the ladder; ravens, the wolverine, the hare
  in the snare, daylight for foraging.
- **18 Materials and forms** — edibility is a material property; wire and cordage make snares.
- **01 Premise and world** / **17 Rooms** — the country's food lives in the fifty outdoor zones.

**These depend on it:**
- **08 Warmth** — a calorie deficit is a warmth input; a body that can't work can't stay warm.
- **11 Injury and first aid** — the bulged can; starvation weakness; cleaning game with a blade.
- **12 The pilot and bodies** — the body as a food source is this system pointing at that one.
- **15 Moral and social layer** — the last ration, the hidden chocolate bar, and the pilot.
- **21 Endings and recap** — "the game runs until the food runs out" is an ending condition, and
  what the party ate is part of the recap.

---

## 6. Open questions

1. **Do grubs and bark join the world, or leave the design?** *(a)* Add them to the tamarack and the
   aspen as real forage. *(b)* Drop them from the passes; the valley already has cranberries, rose
   hips, labrador tea, three kinds of protein and a fishery. **Recommendation: (b)** — the valley's
   food is better designed than the passes' shorthand, and inner bark as *bait* is a more
   interesting fact than inner bark as food.
2. **How hard does starvation bite in a week?** *(a)* A real calorie ledger where a party that finds
   nothing dies around day 8–10. *(b)* Hunger degrades (weakness, cold tolerance, slower work) and
   the cold does the killing. **Recommendation: (a) with (b)'s texture** — Andrew decided the run
   ends when the food runs out, so the number has to be real; the visible symptoms should be
   weakness and cold long before the death.
3. **Is cooking a system or a state change?** *(a)* A cooking system: raw / cooked / burnt, safety,
   yield. *(b)* Heat is heat — a thing near a fire gets hot, thaws, and eventually chars, and
   "cooked" is just a temperature state with a nutrition consequence. **Recommendation: (b)**, which
   is one rule instead of a subsystem and falls out of fire and materials the party already has.
4. **Raw versus boiled — does it matter mechanically?** **Recommendation: yes, modestly** — raw meat
   is edible and carries a small illness risk, cooked is safe and yields more; the manual's food page
   teaches it, so a party that reads gets it right without being told in the moment.
5. **Does hunting need new operations, or does it fall out?** The world design bills `throw`,
   `set/check snare` and `fish` as the three it assumes, each with a stated degradation.
   **Recommendation: `throw` and `set snare` as real operations** (they are general, and snares are
   the plan-ahead muscle the whole design wants), and fishing assembled from existing operations with
   only the catch as a seam.
6. **How is the pilot's body prepared, in grammar terms?** `butcher X with Y` is the rescue graph's
   chain. **Recommendation: no special verb for a person** — it is the same cut/prepare operation the
   hare and the grouse use, which is exactly why it lands the way it should.
7. **Does food spoil, and does cold preserve it?** **Recommendation: yes, trivially** — December does
   the preserving for free, and the interesting case is the opposite one: food kept warm, food the
   ravens find, and the wolverine at the cache. Storage is the mechanic, not decay.
8. **What does the party know about eating people, mechanically?** The seed requires "cooking or
   freezing for safety". **Recommendation: keep the requirement** — it makes the act take time and
   fuel, which is the difference between a decision and an impulse.
9. **Are the two ration tins the right amount?** The ladder says the kit's rations "for three" run
   out around day 3 with a party of four or five. **Recommendation: leave the number to the probes**
   — it should be enough that nobody starves in the first days and short enough that the country and
   the cockpit both become real options before the week is out.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

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
- The ravens / wolverine / cache-raid pressure (`events-and-escalation.md` §4).

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
