# 12 — The pilot and bodies

> **Status: draft for review.** **Architecture counterpart:** none yet;
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) DR-06 lists the
> pilot among the puzzle-critical authored packets. Since he starts the run dead, what he needs is the
> general body of §4.3a.

## 2. Decisions

### Andrew's decisions
- **(2026-09-07)** Decisions across the moral spectrum — eating the pilot, stealing, hitting, killing.
  The body as a food path and a moral decision is Andrew's brief.
- **(2026-09-16, 2026-09-26)** No lethal-consent gate; violence resolves with real physics, and there
  is a combat system like a MUD's.
- **(2026-09-17)** **The pilot starts the run dead.** He is a body from the first look: no clock, no
  moaning, no lines. He carries no clues — the party does not need him to work out the rescue.
- **(2026-09-17)** Dead players are ghosts: they move freely and talk only in the out-of-character
  chat; ghosts hear ghosts, the living cannot.
- **(2026-09-17, 2026-09-27)** The endings are rescued or dead; the run ends when they die, of
  anything. There is no recap.
- **(2026-09-26)** A bear is in, and it acts; so do some bigger animals and a few birds. Body parts
  carry heat as part of their ontology; heat is a state system, and the plane is an entity with
  openings, open or closed, and an internal heat a fire raises. Food changes with heat — raw, cooked
  and spoiled differ.
- **(2026-09-26, 2026-09-27)** The season is the first week of October in interior Alaska (document 13
  §4.2).
- **(2026-09-27)** **His body is food, and eating it is taboo, not immoral.**
- **(2026-09-27)** Up to five play. A seat nobody plays is a dead character whose clothes and pockets
  can be searched.
- **(2026-09-27)** Nobody is told what can happen to a dead player's body — it is an open world. A
  series of tutorial rooms, each one simple situation, shows players what sort of things they can do
  (`PLAN.md` E19).
- **(2026-09-27)** Poison and bad meat make people very sick but never kill (document 11 §4.6).

### Proposals (Claude)
Everything else here is Claude's, for Andrew's check: the acts on the body (§4.3), the body in the
ontology — its parts, states, what it could become, butchering and what it yields, raw, frozen, cooked
and spoiled flesh, the body among the animals (§4.3a) — from real forensic, food-safety and wildlife
sources listed at the end of §4.3a.

## 3. In one paragraph

You come to in a wrecked Cessna in early October, and the man in the left seat is dead. Nothing about
him will speak or move again, and nobody in the game will ever say a word about him. He is a body in
the cockpit: a leather flight jacket that comes off easily now and will fight you in a few hours, a
lighter in a pocket, 78 kilos of a person, cooling. Over the days he goes stiff, then slack, and — once
the clear cold comes behind the storm — hard, from the fingers in. If someone lights a fire in the
fuselage he does not freeze, and what that means arrives slowly, through the nose. The ravens find him
if the cockpit is open; the bear may. And somewhere around the third hungry day, somebody does the
arithmetic.

## 4. The design

### 4.1 What is decided

| | |
|---|---|
| **He starts the run dead** (2026-09-17) | A body from the first look: no clock, no lines, no clues. The moral question starts on day one. |
| **Talking gets silence, never a list** | The never-a-menu rule (DR-08c): `talk to the pilot` answers with the physics of why ("nobody will"), not with topics or a prompt. |
| **His body is food; eating it is taboo, not immoral** (2026-09-27) | The world never comments on it (document 15). |
| **Nobody is told** (2026-09-27) | Nothing explains what can be done to a body, his or a dead player's; the tutorial rooms show what sort of things players can do. |

### 4.2 What the world never does here

No topic list, no "you could ask him about the radio", no prompt about what to do with him, no score
for covering him and no scolding for butchering him. Every consequence is physical (calories, illness,
warmth spent, a witness who saw it) or in the log. This is the never-a-menu rule (DR-08c) and the moral
layer's "possible, priced, witnessed, logged" (document 15).

### 4.3 The body — the acts

*(Proposed by Claude, for Andrew's check.)* The dead pilot is an ordinary physical thing made of a
person's body, and every act below is the general system applied to him, not pilot-specific code.

| the act | what it is | source |
|---|---|---|
| `search pilot` | the pocket contents — a lighter, one of the fire paths | census `pilot (body) — frisk` ✅; `objects.py` (`lighter` is `in: pilot`) |
| `remove jacket from pilot` | a leather flight jacket — insulation the material table calls middling; his boots, gloves and watch are still to be authored | [`rooms/cockpit.md`](../scenarios/whiteout/rooms/cockpit.md) §2b, §3 |
| `cover pilot with blanket` | a covered body — it keeps the birds off and hides him; no reward is invented for it, and a blanket on him is a blanket not on the living | [`rooms/cockpit.md`](../scenarios/whiteout/rooms/cockpit.md) §3; document 15 |
| `butcher pilot with knife` | the food path: an attended activity made of real cuts (§4.3a), witnessed by whoever is in perception band | document 15 |
| `examine pilot` | states plainly that he is dead | census ✅ (prose) |

**The pilot's body as a dilemma** (document 15): day 1 evening, no food found, cold rising; the
tempting act is butchering him for meat; the alternative is to cover or bury him, ration, and accept
the deficit. The world's answer is physical and recorded, never editorial: his body's states change
(§4.3a), the act is witnessed by whoever could perceive it, and other players' trust shifts only on
witness or disclosure. Eating him is taboo, not immoral (2026-09-27). The hunger bands are what make the
choice live — hungry enough to look at the pilot.

The engine work this needs is general: persons as targets for `cover`, `search`, `butcher` and
`carry`; blood on the tool as provenance; the witness check by perception band — and underneath them
the body as an entity with parts and states (document 11 §4.6), the heat system, the food-state and
spoilage system, and the animals' senses (§4.3a).

### 4.3a The body in the ontology

*(Proposed by Claude, for Andrew's check.)*

**What he is.** An `individual` of 78,000 g, the same kind of entity as a living player (document 11
§4.6): `materials` in order — skin, fat, muscle, bone, blood, organs; `parts` recursively, as a living
body's; a `container` (his pockets: the lighter); worn things with `worn_by: pilot` (the jacket today;
boots, gloves and a watch still to be authored); `located` in the left seat, `against` the forward
bulkhead. His states, each changed by a system:

| state | how it really behaves | changed by |
|---|---|---|
| `heat`, per part | a body cools about a degree an hour at first, faster in cold air and fastest in the thin parts. In a cockpit below freezing his fingers, face and feet freeze first, and the whole 78 kg takes days to freeze through, because the heat of some 45 kg of water has to leave it (a physics estimate, for the probes to tune) | the heat system: the cockpit's air, the plane's openings, a fire in the fuselage |
| `stiff` (rigor) | sets in 2–6 hours after death, peaks around 12, passes over the next day or two — more slowly in the cold. Stripping him is easy before it, a fight during it | time × heat |
| `frozen`, per part | frozen flesh is hard as wood: it will not bend, strip or cut with a knife — only a saw or an axe will go through, or thawing by a fire, which starts it spoiling | the heat system |
| `spoilage` | bacteria grow above about 4 °C (40 °F) and barely below it, and stop below freezing. The gut spoils first, from the inside — which is why a hunter guts a kill at once | time × heat; **the food-state and spoilage design, to be written** |
| `sensed.smell`, with a range | faint while cold and whole; strong once opened, warmed or spoiling. Smell is how the bear, the ravens and the gray jays find a carcass | his other states; read by the animals' behaviour rules (document 23) |
| `covered` · `buried` · `moved` · `stripped` · `searched` · `cut` (which parts) · `scavenged` | the record of what was done to him — each a physical fact the prose composes from, never a label | the acts below, and the animals |

**What he could become** (`could_become`, by capability; a verb never names a tool):

| act | needs | yields | how it really goes |
|---|---|---|---|
| strip — `remove jacket from pilot` (shipped) | hands | his clothes | easy in the first hours, a struggle through rigor, impossible frozen without cutting |
| search (shipped) | hands | his pockets — the lighter | — |
| move · drag · carry | his 78 kg against what the movers can haul (document 04 §3.11) | him, somewhere else | dragging over snow is the real way; two can carry him a short distance |
| cover | a sheet, a blanket, boughs, snow | a covered body | still there and still findable — a shape under a blanket. Covering keeps the birds off; snow keeps him frozen and hides him; a blanket on him is a blanket not on the living |
| bury | a `dig` capability and something to dig with; rocks | a grave or a cairn | the top of the ground freezes on the clear nights and the snow comes on day 3 (document 13 §4.2); a cairn of rocks, or a snow burial, is what a day's work can do |
| burn | fuel | ash and bone | an open-air pyre takes 400–600 kg of dry wood — days of the whole party's wood work |
| butcher | `edge` for skin, muscle and gut; `heft`, a saw or an axe for joints and bone | meat, fat, organs, marrow, skin, bone | below |

`cover` needs its own operation — today it parses to `wrap` — the same one that covers the hull's
openings (document 08).

**Covering and burying, and finding him again.** A covered body is a shape under a blanket; a snow
burial or a cairn is a mound; outside, the storm's snow buries him further by itself. Covering and
burying are real acts that can be undone by uncovering and digging, and the animals can undo them too
— the bear digs and caches, the ravens pick at what is exposed.

**Butchering, and what it yields.** `butcher` is the canonical word (its synonyms authored with it,
document 04 §3.7) for an **attended activity** (document 06) that works through the body part by part
and banks its progress on the body, so it can be left half-done and finished by anyone. Inside it,
the finer acts are their own operations, because each does something different: **`skin`**,
**`gut`** (open the belly and take out the organs — puncture the gut and the meat is contaminated),
**`cut <part> off`** at a joint, **`cut meat from <part>`**, **`crack`** a bone for its marrow
(`heft`). They are the same operations the hare, the grouse, the fish and the bear take (documents 10
and 23): to the engine a person is not special. A novice with a pocket knife is at it for hours on
the clock, with blood on the tool and the hands as provenance (document 15). There is no consent gate:
anyone can do any of it, alone (2026-09-16).

What it yields: an adult male body holds about 144,000 kcal, of which skeletal muscle about 32,000
and fat about 50,000, in a 66 kg man (Cole 2017, *Scientific Reports*); muscle runs about 1,300 kcal
per kilogram. For the 78 kg pilot that is roughly **38,000 kcal of muscle**, plus fat, organs and the
marrow. Against a party of five burning twelve to sixteen thousand a day (document 23 §4.4), the
muscle is two to three days of food — real, and not a rescue.

**Eating it — raw, frozen, cooked, spoiled.** Each is a state on the meat and a process in the eater's
gut (document 11 §4.6). Bad meat makes people very sick and never kills (2026-09-27).

- **Raw and fresh**, cleanly cut and kept cold: edible, and as safe as raw meat gets. The risk climbs
  with what touched it — a punctured gut, dirty hands, the knife that did everything. Food-poisoning
  bacteria show as vomiting and diarrhoea hours to a day or more later, spending the water document
  09 counts.
- **Frozen raw**: real northern food — frozen raw meat and fish are eaten shaved thin. Freezing stops
  bacteria growing but kills few of them. It costs body heat to eat: about 95 kcal per kilogram to
  thaw it and bring it to blood heat inside you (from the latent heat of its water — the same
  arithmetic as eating snow, document 09 §4.6), a small cost against the ~1,300 it gives.
- **Cooked**: heat right through to about 74 °C kills bacteria and parasites, and cooked meat gives
  more usable energy than raw (Carmody et al. 2011, *PNAS*). It needs the fire, a spit or a vessel,
  and fuel — time the party spends.
- **Spoiled** — warm too long, which is what happens if he lies in a heated fuselage: cooking does not
  make it safe, because some bacteria leave toxins heat will not destroy (staphylococcal toxin:
  vomiting within half an hour to eight hours — CDC). Spoiled is a state you can smell.
- **What a person's flesh carries that game does not**: prion disease (kuru) from the brain and
  nerves — no cooking destroys prions, and it takes years to decades to show — and whatever
  blood-borne infection he carried. Neither shows inside a week; both are true, and nothing fires for
  them during the run.

**The body among the animals** (the bear is in, 2026-09-26). A carcass is the strongest pull in the
country: bears find one by smell, feed, bury what they do not eat under debris, and **guard it**. A
bear's cache pile is called about the deadliest thing to walk into in the Alaska bush (*Anchorage
Daily News*, 2011), and the Alaska Department of Fish and Game's warning signs of one are gathering
ravens and jays, an out-of-place smell and a fresh mound of debris. Here the ravens and gray jays
come first, in daylight, and their gathering over the wreck is itself a sign the party can read. So
what the party does with him — leave him in a closed cockpit, drag him out onto the snow, butcher him
and hang the meat, cache it — is a real decision about the bear, read through his `smell` row and the
animals' behaviour rules (document 23; the animal-behaviour design, to be written). Nothing is
scripted.

**Witnessed, logged, never commented on** (document 15). Each act is ground truth in the log; the
others learn of it by seeing it (perception bands), by the evidence it leaves — a covered shape
smaller than it was, blood on a knife, meat by the fire — or by being told.

**Real-world sources for this section:**
- Cole, *Assessing the calorific significance of episodes of human cannibalism in the Palaeolithic*
  (*Scientific Reports* 7, 44707, 2017) — a 66 kg adult male template: ~143,800 kcal in all, skeletal
  muscle ~32,400, adipose ~49,900, skeleton ~25,300, skin ~10,300; muscle ~1,300 kcal/kg.
- Forensic references on the post-mortem interval (algor and rigor mortis; the Henssge nomogram) — a
  body cools roughly 1 °C an hour at first; rigor from 2–6 hours, peaking near 12, passing over one to
  two days; cold slows every stage.
- USDA / state extension food-safety guidance for wild game (e.g. Clemson HGIC; Penn State Extension)
  — gut at once, never puncture the gut, cool below 4 °C (40 °F); bacteria grow between 4 and 60 °C.
- CDC — staphylococcal food poisoning (30 minutes to 8 hours; heat-stable toxin); *C. perfringens*
  (6–24 hours). Alaska Department of Fish and Game — Arctic *Trichinella* survives freezing, so bear
  meat must always be cooked (to about 74 °C / 165 °F) — for the bear, not for the pilot.
- Carmody, Weintraub & Wrangham, *Energetic consequences of thermal and nonthermal food processing*
  (*PNAS* 108, 2011) — cooking increases the energy gained from meat.
- Kuru and the prion diseases (NINDS; the Fore studies) — transmitted by eating nervous tissue,
  incubation years to decades, not destroyed by cooking.
- Alaska Department of Fish and Game, bear-safety guidance and carcass warnings — bears bury and
  defend carcasses; scavenging birds, an unusual smell and a fresh debris pile mark one; *Anchorage
  Daily News* (2011) on grizzly cache piles.
- Studies of open-air pyre cremation in South Asia (Chakrabarty et al. 2013; UN survey figures) —
  roughly 400–600 kg of dry wood per body.
- The heat to eat frozen meat is arithmetic from meat's ~70–75% water: warming it from −10 °C, the
  latent heat of fusion (334 kJ/kg), and warming to 37 °C — about 400 kJ, ~95 kcal, per kilogram.

### 4.4 Bodies in general

- **A seat nobody plays is a dead character from the start** (2026-09-27): a body in the plane with
  their clothes on it and their pockets full, the same entity as the pilot's (§4.3a), which can be
  searched and everything else the pilot's body can.
- **A dead player's body stays where they died** — an entity exactly like the pilot's: their clothes on
  it, their pockets full, cooling, stiffening, freezing, smelling to the bear — and every act on the
  pilot works on it. The player is a ghost who moves freely and talks only out of character, and can
  walk in and watch. Nobody is told in advance (2026-09-27).
- **The run ends when the last player dies.** The endings are rescued or dead (document 21).
- **The bodies' event cards** (document 13 §4.3) are their own state changes — stiffening, freezing, the
  first raven — each a line that belongs to the body's `sensed` rows.

## 5. Interactions

**Depends on:**
- **11 Injury and first aid** — the body as an entity with parts and states (11 §4.6), the same for the
  living and the dead; what bad meat does in the gut.
- **The heat design** *(to be written)* — his cooling and freezing, and the fuselage's internal heat
  when a fire burns in it; **13** — the week's air that cools and freezes him (13 §4.2).
- **The food-state and spoilage design** *(to be written)* — raw, frozen, cooked, spoiled.
- **23 Flora and fauna** and **the animal-behaviour design** *(to be written)* — the bear, the ravens and
  the jays finding him by smell.
- **10 Food and hunger** — what the meat is worth, and the hunger that makes the choice live.
- **15 The moral and social layer** — witness, evidence, the log, and the taboo.
- **03 The player view** and **04 Grammar and feedback** — how his body's states compose into the
  cockpit's prose; `talk to the pilot` answering with silence, not options.
- **06 Time, sleep and the clock** — butchering and burying as attended activities.
- **16 Players and kit** — what an unplayed seat's body wears and carries.
- **19 Multiplayer** and **21 Endings** — ghosts.

**Depended on by:**
- **13 Events, escalation and weather** — the ladder's pilot's-body row and the bodies' event cards.
- **17 Rooms and living rooms** — the cockpit's prose switches on his body's states (stiff, frozen,
  covered, stripped, cut, scavenged).
- **10 Food and hunger** — his body as one of the food sources.
- **21 Endings** — the body, and what was done to it, is in the log.

## 6. Open questions

None open. The proposals in §4.3 and §4.3a wait for Andrew's check at this document's sitting.

## 7. Review log

- **2026-09-17 (Andrew):** the pilot starts the run dead — no clock, no lines, no clues; dead players
  are ghosts.
- **2026-09-26 (Claude's self-review, for Andrew's check):** the body as an entity with parts and
  states; what butchering yields; raw, frozen, cooked and spoiled flesh; the body among the animals.
- **2026-09-27 (Andrew):** nobody is told what can happen to a dead player's body — an open world, with
  tutorial rooms; eating the pilot is taboo, not immoral; a seat nobody plays is a dead character.

## 8. What exists today

**Built** — the pilot as an object, and the acts the existing general systems already give him:
- `game/world/scenarios/whiteout/objects.py` — the `pilot` row: materials `['flesh']`, `mass_g`
  78000, `zone: 'cockpit'`, `state: {'dead': True}`; `lighter` is `in: 'pilot'`; `jacket` is
  `in: 'pilot'` with `state: {'worn_by': 'pilot'}`. The dead start is as designed.
- `game/world/scenarios/whiteout/appearance.py` — a `pilot` entry anchoring the `left_seat` space, with
  a dead variant and an alive one that the dead start leaves unused.
- `game/world/sim/presentation.py` switches his scene phrase on `dead` (held by
  `game/tests/sim/test_presentation.py::test_scene_phrase_switches_on_state`).
- `game/world/scenarios/whiteout/responses/slice.py` — `talk.dead` ("You say it aloud. The {target}
  doesn't answer; nobody will.") and `take.strip_dead`; the honest-silence behaviour is held by
  `game/tests/integration/test_discovery_int.py::test_talking_gets_honest_silence`.
- Probes in `game/world/scenarios/whiteout/probes/census.py`: `census.cockpit.search_pilot` **pass**,
  `census.cockpit.examine_pilot` **pass**; `remove_jacket_from_pilot`, `take_boots`,
  `cover_pilot_with_blanket` are **todo**.

**Designed, not built** — §4.3a: the body's parts and states, its could-become rows, butchering, the
food states, the animals' smell; unplayed seats as bodies; and a content fix — `objects.py` authors him
as `materials: ['flesh']`, where §4.3a's materials are skin, fat, muscle, bone, blood and organs
(`PLAN.md` A12). `game/world/scenarios/whiteout/authored.py` is empty. `butcher` has no handler, and
`cover` resolves to `wrap` in `game/world/sim/parser/vocab.py`.

**Nothing** — no body parts as entities, no per-part heat, no rigor, freezing or spoilage, no smell
with a range, no `butcher`, `skin`, `gut` or `bury` operation.
