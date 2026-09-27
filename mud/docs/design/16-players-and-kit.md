# 16 — Players and kit: the slots, draws, pockets, luggage, the 206 interior

> **Status: `draft for review` (2026-09-16).**
> **Architecture counterpart:** [`../architecture/clothing-warmth.md`](../architecture/clothing-warmth.md)
> (DR-25, the shipped v1; DR-25a's region/wind/wet model is live in code — `warmth.py` — but has not
> yet been written into that doc; see §8).
> **Sources:** `docs/investigation/design/players-and-kit.md` (primary — the draw, the pockets, the
> luggage, the clothing model, the honest interior) · `docs/investigation/plane-interior.md` (the
> 2026-07 investigation that chose the aircraft and proposed its curated v1 contents) ·
> `docs/architecture/implementation-architecture.md` (DR-25a; the DR-14a/DR-15a amendment,
> 2026-09-07 late and 2026-09-16, promoted on Andrew's review) ·
> `docs/investigation/design/00-provenance-audit.md` §1–§2 · code:
> `game/world/scenarios/whiteout/characters.py`, `objects.py`, `build.py`;
> `game/world/sim/systems/warmth.py`.

> **The season was settled on 2026-09-26: October, at freeze-up** (`README.md`; document 08's banner).
> This document was drafted for a December crash. Its kit is re-checked against mid-October, from real
> data, in §4.9 *(Claude, 2026-09-26 — for Andrew's check)*, and the December lines below are marked
> where they stand.

---

## 2. Provenance

### Andrew's decisions

- **Each player starts with a different clothing and injury draw and stuff in their pockets;
  luggage has stuff in it; the clothing system impacts warmth loss and other things; the plane is
  fine (the 206).** (2026-09-07, recorded in the DR-14a/DR-15a amendment and the provenance audit
  §1.) Nothing about a player's starting kit is chosen; it is decided the moment the run begins.
- **The four-seat interior (§4.6 below) is a go; the kid is in — a party of four or five; the crash
  is in December.** (2026-09-16, `players-and-kit.md`'s own banner and the same DR amendment.) The
  kid's inclusion sets the party at four adults plus the kid, or four without; exactly what a fifth
  player carries is still a proposal, not signed off item by item (open question 1). *(Superseded
  2026-09-26 for the month only: the crash is in October, at freeze-up — `README.md`, "The season".
  The four-seat interior and the kid stand.)*

### Proposals (Claude)

Everything else here is a proposal for review, per the provenance audit's own table
(`00-provenance-audit.md` §2: "players-and-kit — the five slots, luggage contents, clothing v2, the
206 interior"):

- The five specific slots — guide, townie, nurse, salesman, kid — and exactly what each wears,
  carries in their pockets, is injured by, and finds in their bag (§4.1–§4.3).
- The clothing model's mechanism — coverage by body region, the shell's wind/waterproof numbers,
  the wet fraction, sweat, dexterity, movement, signal, sharing (§4.4; designed in full in
  **08 — Warmth, clothing and shelter**).
- The honest interior's specific furniture — the seat labels 1A/1B/2A/2B and the right seat, the
  hat shelf, the baggage bay, the jammed cargo door, and the panel inventory (§4.5–§4.6): proposed
  2026-09-07 in `plane-interior.md` and `players-and-kit.md` §5, and approved as a four-seat interior
  on 2026-09-16 — but not a sign-off on every named object inside it.
- What this asks of the engine (§4.7) and the lens pass (§4.8).

---

## 3. In one paragraph

You come to belted into a seat you did not choose, wearing whatever you happened to have on when you
got on the plane, with a stranger's court date or ski trip or sales call in your pockets instead of
anything meant for this. The guide has a parka and a pocketknife and bruised ribs; the kid has a ski
jacket, mittens and a duffel full of hockey gear; the townie has a denim jacket, no gloves, and a
phone that is, for now, the party's only clock and light. What you are wearing when the plane stops
moving is the single biggest thing that decides whether you are cold tonight — and it is different
for everyone, which is what turns "who gets the good coat" into a question the party has to answer
together, in the first hour, long before anyone says the word "rescue."

---

## 4. The design

### 4.1 The draw (one slot per player, deterministic from the run seed)

> **Andrew, 2026-09-27:** *"we dont make up extensive back stories, no one should be forced to have
> reasons for flying just be given different clothes and stuff."* The slots are different clothes,
> injuries and things in pockets and bags; the reasons for flying in the table below are struck. Up to
> five play; an empty seat is empty, and an unplayed character is dead with its clothes there to search;
> AI agents may play seats. **No firearm.** The survival kit is gone — buried somewhere; the sleeping bag
> is buried with the tail wreckage; two blankets are hidden inside the plane — *"we dont want it too
> easy but not too hard."* The date is mid-October, either side of the 15th. The Alaska statute in §4.5
> and §4.9 is background, not a constraint.

A **slot** is a seat, plus what its occupant wore, carried, and suffered in the crash. Five slots are
authored; the run seed is meant to permute which player gets which — nothing is random at runtime
(§6, §8).

| slot | seat | wearing | pockets | injury | their bag |
|---|---|---|---|---|---|
| **the guide** (flying up to a lodge job) | right seat | parka (down, hood), wool base layer, insulated boots, gloves, wool hat | pocketknife, lighter, a chocolate bar, a compass on a lanyard | bruised ribs (slow, painful work; no bending) | his own duffel: a headlamp, a ferro rod, a steel cup *(Claude, 2026-09-26 — §6 Q4: the survival kit is the plane's by law, not his; the earlier "the survival duffel is HIS" is superseded)* |
| **the townie** (going home from a court date) | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves | phone (light, clock, a dead battery by day 2), wallet (cash, cards, ID — paper), gum, keys, earbuds (wire) | a cut forearm (bleeding; the census wound) | a soft suitcase: cotton clothes, a towel, toiletries (floss = cordage; razor = edge; sanitizer = fire starter; tampons = tinder + wound packing), a paperback |
| **the nurse** (home leave) | 1B | fleece jacket, hiking boots, a scarf, thin gloves | a small med pouch (gauze, tape, ibuprofen, a suture kit — she knows how; the player has to *(whether her trained hands make the same typed act go faster or better is document 11's Q6, left for Andrew — Claude, 2026-09-26)*), lip balm (wax), hair ties (cordage), a pen | a sprained ankle (walking costs double; splint it) | a backpack: canteen, spare shirt, a wool sweater, a headnet, a book of matches |
| **the salesman** (mine supply run) | 2A | wool overcoat, dress shoes, leather gloves, a good scarf | a metal lighter, a hip flask (whisky), reading glasses (a lens! sun only), a notebook (paper) | concussion (fatigue faster; confusion messages the first day) | a laptop bag: laptop (battery — sparks, heat, then dead), cables (wire), a metal water bottle, snacks, a wool blanket (bought for the trip) |
| **the kid** (16, visiting family) | 2B | ski jacket, snow pants, snow boots, mittens | a phone, a candy bar, a multitool (a gift), sunglasses (snow blindness) | shock: fine physically, slower to act day one | a duffel: hockey gear (a stick = a rod; tape = tape; pads = foam), a sleeping bag |

The **pilot** keeps his slot as designed (jacket, lighter, the radio, the manual, the chart) — he is
not a player slot; his own arc belongs to **12 — The pilot and bodies**. *(Claude, 2026-09-26: he
starts the run dead — Andrew, 2026-09-17 — so what he wore and carried is found on a body; its
materials are skin, fat, muscle, bone, blood and organs, document 12 §4.3a.)*

The draw makes the party heterogeneous, which is what makes sharing a real act — the blanket, the
gloves, the huddle — instead of five copies of the same survivor with no reason to talk to each
other.

### 4.2 Pockets

Pockets are a per-character container: stowed, and already revealed to their owner (`search me` /
`inventory` needs no `open` or `search` step first — the owner already knows what is in their own
pockets). Everything in §4.1's table is a real object with real materials: a phone is glass and
plastic with a `powered` state and a light; a wallet is leather with paper inside; lip balm is wax
(fuel); earbuds are copper wire in rubber; keys are steel (a poor scraper). None of it is decoration —
the townie's phone is the party's only clock and light until its battery goes, and that is meant to
matter.

### 4.3 Luggage (the baggage bay, and what the crash threw into the cabin and along the trail)

Every bag in §4.1, plus: the **mail sack** (letters, postmarks, a parcel of candles, a parcel
addressed to V. Holt), the **freight** (flour, the coffee tin, dog food, a box of shear pins, a
toolbox — screwdrivers, pliers, a hacksaw blade that is both an edge and a saw), a **cooler** (a
family's frozen fish — a vessel), and a **guitar case** (a story object: the strings are wire, the
case is a sled, the neck is wood).

The rule that decides where all of this actually sits (`plane-interior.md` §8b, "the crash is the
difficulty engine"): realism supplies the inventory; the crash supplies the difficulty. An intact
survival kit sitting in the open would solve the game in one `search`, so the law says the kit was
aboard and the crash decides where it is now and what shape it is in — the toolbox is in the crushed
tail cone (pry it open), the cooler is under a drift on the trail (dig for it), and the hacksaw blade
— the keenest edge in the valley — is a walk away. The **power ∝ cost** curve follows from the same
rule: the more a thing solves, the farther, deeper, or more broken the crash left it. A paperback is
at your feet; the hatchet is a hundred meters out under snow with a cracked haft.

### 4.4 The clothing system (DR-25 → v2)

Each wearable declares which body regions it covers, how much wind its outer shell stops, how
waterproof it is, and its mass; it inherits a wetness quantity and damage state from the world's
general object model. From that, the model derives warmth loss by region, a sweat/drying cycle, a
dexterity penalty for cold or mittened hands, a movement effect from footwear, a visual-signal value,
and the physics of sharing — the huddle bonus among them. This mechanism, its numbers, and what of it
is built versus still designed is **08 — Warmth, clothing and shelter** in full; this document keeps
only the draw that feeds it (§4.1).

### 4.5 The aircraft

The July investigation (`plane-interior.md` §1) weighed two classic Alaska bush planes against "big
enough for two rows of seats in the back, pilot only aboard": the **Cessna 206/207 Stationair** (six
seats, piston single, a clamshell cargo double-door on the right rear, a hat shelf and netted baggage
bay behind the last row) and the **de Havilland DHC-2 Beaver**. It recommended the 206-class piston
single on wheel-skis — the default choice *(Claude, 2026-09-26 — the season; for Andrew's check: at
October freeze-up, with an inch of snow and the lakes skimming over, a mail plane landing on village
gravel strips flies on wheels — big tundra tyres — and the skis go on when there is snow to land on.
The tyres and their tubes are rubber: black signal smoke, and a band that stretches for a sling)* — and flagged one realism problem with the game's earlier
fiction: real bush planes have no airline-style overhead bins, only a hat shelf, floor tie-down
tracks, and cargo netting. Andrew's decision (2026-09-07) settled the aircraft: "the plane is fine
(the 206)."

The aircraft's own legal cargo is the reason the survival economy exists at all: Alaska Statute
AS 02.35.110 requires a minimum emergency kit aboard any in-state flight — rations for each occupant
sufficient to sustain life for one week, one axe or hatchet, one first-aid kit, an assortment of
fishing tackle (hooks, flies, lines, sinkers), one knife, a fire starter, one mosquito headnet for
each occupant, and two small signalling devices in sealed metal containers; and, from October 15 to
April 1, also **one pair of snowshoes, one sleeping bag, and one wool blanket or equivalent for each
occupant over four**. *(Corrected, Claude, 2026-09-26, read at source — AS 02.35.110(a): the earlier
text said "a wool blanket per occupant" and left out the tackle, the knife, the fire starter and the
headnets. With the pilot and five passengers aboard — six occupants — the law asks for two blankets.
What the October date means for the winter items is in §4.9.)* The pilot was legal. The
kit is in the tail. This single fact justifies the survival economy without inventing anything
(`plane-interior.md` §7).

### 4.6 The honest interior (the 206; supersedes the airline fiction)

- **Seats**: pilot plus the right seat up front; **1A/1B** (row one), **2A/2B** (row two) — the
  labels the manifest in the pilot's kneeboard uses to name who sat where, itself a clue and a story.
  Each seat is the same parts-machine (cover, cushion, belt, bolts — the seat-row exemplar in
  **17 — Rooms and living rooms**) with a DIFFERENT damage and find: 1A intact; 1B wrenched (the
  salesman's laptop bag under it); 2A thrown loose (a movable frame — a windbreak, a sled base); 2B
  thrown against the hull (the life-vest pouch: vest, straps, a whistle).
- **The hat shelf** (behind row two): hats, a scarf, the kid's helmet — a shelf, not a bin.
- **The baggage bay** behind it: the cargo net over the bags (cut it or unhook it), the survival kit
  lashed to the floor rings, the freight and the mail against the bulkhead.
- **The double cargo door** on the right rear: jammed by the impact (pry it) — the second way out
  besides the breach; ice seals it overnight as an event.
- The old "overhead bins" become the hat shelf and the cargo net — the same open/pry/search loops,
  re-ficted to what a real bush plane actually carries.
- **Windows**: crazed plexiglass — sharp sheets when broken, and a possible cover for the breach.
- **Up front**: the six-pack instruments, the whiskey compass on the glareshield (takeable), the ELT
  remote placard (the breadcrumb pointing at the tail), headsets on the yokes, the halon
  extinguisher, the magneto key in the ignition, the kneeboard with the manifest and the sectional
  chart.

### 4.7 What this asks of the engine

Small — mostly content plus the warmth v2 model: `characters.py`'s slot table, plus a pure
`outfit(seed, slot) -> rows`; a loader step that dresses a character and fills their pockets at run
start (the instance-spawn work, and a `dress` helper smokes can call directly); `covers` / `wind` /
`waterproof` on wearable rows; `warmth.py` v2 (regional loss, wet fraction, wind multiplier,
dexterity, the huddle); a `give` verb; wetness as grams on things; a phone with a battery process.
Probes: each slot's first-night warmth band; "give gloves to the townie"; "wear the sweater under
the coat"; "huddle under the blanket with 2".

### 4.8 Lens pass

- **The Player** (GD — who are they, what do they bring?) — GREEN. Five people with different coats
  is a party; four identical survivors is a chore list.
- **Cooperation** (GD) — GREEN. Heterogeneous kit is the engine of sharing; the huddle and the glove
  hand-off are the first co-op acts, hours before the antenna.
- **Fairness** (GD) — YELLOW. The townie's draw is harsh; the party's job is to fix it. The seed is
  meant to permute slots so no one player is always the townie — not yet true at runtime (§8).

---

### What you can carry (Andrew, 2026-09-18)

Inventory is limited by **weight and space** — mass in grams, which the contract tracks, and bulk,
which derives from the material's density (document 18). Capacity is not a number on the character:
it lives on the things that carry.

| carrier | holds | notes |
|---|---|---|
| your hands | a couple of things, or one awkward one | a full armful means you cannot also pry a door |
| pockets | small, light things | the crash draw already fills them (§4.2) |
| a backpack, a duffel, a laptop bag, a guitar case | what its capacity says | each slot's bag becomes a real carrier, not a container of story items |
| worn clothing | its own pockets; a stuffed jacket | stuffing insulation is a use of space (document 08) |
| a dragged seat frame, the cargo net as a bundle | far more, and it costs you speed | the 2A seat is already designed as a movable frame; this is what it is for |

Exceeding capacity is never a refusal: you take what fits, the world names what you left behind, and
the load feeds the travel time (document 03 §4.1a). *Proposal: capacity is a `capacity_g` and a
`capacity_bulk` on any container row; the sum of what you hold, wear and haul is what you can carry.*

### 4.9 October — what these people would really wear, carry and fly with *(Claude, 2026-09-26 — the season; every line for Andrew's check)*

**The weather they dressed for.** Interior Alaska at freeze-up, from the National Weather Service's
Fairbanks daily normals (1981–2010): on 1 October a high of 7 °C and a low of −2 °C; on 15 October
1 °C and −8 °C; on 22 October −3 °C and −11 °C; on 31 October −7 °C and −16 °C; about 27 cm of snow
in an average October. Mid-month the day is about nine and three-quarter hours long, the sun up a
little before nine and down around half past six (Weather Spark). Clothes that are right on the 15th
are thin by the end of the run's week: **the week itself is the turn of the season**, which is the
ladder document 13 builds.

**What people in the Interior actually wear in October.** Locals dress for work and for the flight:
canvas work coats and bibs (Carhartt — cotton duck, often blanket-lined), fleece, a synthetic or down
puffy, a knit hat, work gloves, and rubber boots (XtraTufs, with wool socks) or leather work boots.
Bunny boots and heavy parkas are for −30 °C and colder, not October (Wikipedia, "Bunny boots" and
"Xtratuf"; Alaska Airlines News, "Look like a local"). Many rural women wear a kuspuk — a hooded
cotton over-shirt — over their layers. People who fly the bush are told to dress for the country they
fly over, not the town they land in (FAA, *General Aviation Survival*); travellers from Anchorage or
Outside dress for the town, which is exactly the salesman.

**Slot by slot.** Every slot passes October with at most a changed reason for flying; who the people
are is Andrew's (Q1).

| slot | against October | what would change |
|---|---|---|
| the guide | a down parka, wool base, insulated boots — more than mid-October needs, which is how a professional dresses for the bush | lodges close in September: "flying out to winterize a lodge" or "home after the hunting season" fits the date better than "flying up to a lodge job" |
| the townie | denim, a cotton hoodie, sneakers, no gloves — a real way to be dressed for a court date in town, and the harsh draw the fairness design wants | nothing; the Alaskan default would be a Carhartt and XtraTufs, which is why the townie is the lesson — cotton, soaked, in the first snow |
| the nurse | fleece, hiking boots, a scarf, thin gloves — right for the month | the headnet in her pack is left over from summer (the mosquitoes are gone after the first hard frosts); the law's kit carries one for each occupant as well |
| the salesman | wool overcoat, dress shoes, leather gloves — what an Outside business traveller wears | nothing |
| the kid | ski jacket, snow pants, snow boots, mittens — warmer than most October days, and true of a kid whose family dressed them for a bush flight | "visiting family" in the school term fits less well than a regional school trip, or a trip to town for the doctor or the dentist |

**The phones are a heat problem.** A phone's lithium battery gives up quickly below freezing and the
phone shuts itself off; Apple rates the iPhone for use between 0 °C and 35 °C (Apple Support). In a
jeans pocket at −8 °C the townie's phone dies the first night; kept in an inside pocket against the
body it keeps going. So the phone's battery process (§8) runs on the phone's own temperature — owned by
the heat-system design, to be written (`README.md`: heat is a state on every entity that really has
it). Pockets are warm places, and that matters elsewhere too: chocolate softens against the body
(cocoa butter melts at about 34 °C), and cold hand sanitizer will not light until it is warmed
(document 18 §4.8).

**What cannot be aboard, and what may be.** Strike-anywhere matches and aerosols do not fly as freight
into the Alaskan bush — they go by barge (Alaska Business, "Rural Retail Realities"). Bear spray is
larger than the one 118 ml self-defence spray allowed in checked baggage, so it is not allowed at all
(FAA PackSafe, "Sprays and repellents"): there is a bear, and nobody has spray. A firearm may fly
unloaded and cased in checked baggage, with small-arms ammunition up to 5 kg per person (FAA
PackSafe), and the statute no longer asks for a survival gun (Best Glide ASE, on AS 02.35.110).
Whether one is aboard is Andrew's (Q7).

**The survival kit, by the date.** The statute's winter additions start on **15 October**. A crash on
or after the 15th has snowshoes, a sleeping bag and two wool blankets in the kit by law; a crash before
it leaves them to the pilot's judgement. Which side of that line the crash falls on is Andrew's
(Q8); the recommendation is **on or just after 15 October** — it is freeze-up by the normals above,
and it keeps the winter kit legal and aboard. The date, once chosen, is recorded in documents 01 and
13. The rations — the real-life baseline, not a decision: the statute says "sufficient to sustain life
for one week" and names no number; commercial emergency ration packs are sold as 2,400–3,600 kcal for
three days (about 800–1,200 kcal a day), so a legal week for six occupants is on the order of
**35,000–50,000 kcal** — far more than the two ration tins in the shipped kit (document 10 §4.3). How
full the kit really is, and what the crash and the scavengers leave of it, is document 10's Q9,
Andrew's.

**What a 206 can lift at all.** A U206G's useful load is about 1,500 lb, roughly 680 kg (the type's
specification; the exact aircraft's weight-and-balance sheet on the kneeboard gives its own). The pilot
and five passengers weigh roughly 450–500 kg, and fuel for the leg plus a reserve at 13–16 US gallons an
hour is another 70–100 kg. That leaves on the order of **100–150 kg for the survival kit, five people's
bags, the mail and the freight**: a mail sack and a few boxes of bypass-mail groceries, which "must fit
around the mail and any passengers" (Alaska Business), not a truckload. The load is a real filter on
what is aboard, the way ecology is on the valley (`README.md`), and an empty seat carries freight in
its place (document 19 Q1).

**Carrying, in real figures.** For the carriers above, whose capacities live on the containers (Andrew,
2026-09-18): a fit adult carries about 22 kg as a working load and about 33 kg on a long march (U.S.
Army FM 21-18, *Foot Marches*: a 48 lb fighting load, a 72 lb approach-march load). A dragged frame or
sled moves far more — on packed snow over smooth ground. On an inch of snow over tussocks it snags on
every hummock; it runs once there is snow enough to fill the hollows and a trail packed by snowshoes.
So the storm that makes everything else harder is also what makes hauling possible.

*Sources for §4.9:* NWS Fairbanks, "October Normals, Fairbanks AK (1981–2010)"
(weather.gov/media/afg/climate/Fairbanks_Normals_October.pdf) · Weather Spark, "October weather in
Fairbanks" · AS 02.35.110 (law.onecle.com/alaska/title-02/02.35.110.html) · FAA PackSafe, "Sprays and
repellents" and the PackSafe chart (faa.gov/hazmat/packsafe) · Alaska Business, "Rural Retail
Realities" (akbizmag.com) · Best Glide ASE, "Survival equipment for Alaskan and Canadian air travel" ·
Cessna Flyer Association 206 specifications; planephd.com U206G specification · FAA, *General Aviation
Survival* · Wikipedia, "Bunny boots", "Xtratuf" · U.S. Army FM 21-18 · Apple Support (iPhone operating
temperature).

## 5. Interactions

**This depends on:**
- **08 — Warmth, clothing and shelter** — the draw's worn items are the input to the warmth score;
  the draw itself is only summarized here (§4.4).
- **Containment** (`../architecture/containment.md`, DR-24) — pockets, the survival duffel, the
  toolbox, and the cargo net are all found by the one reveal rule (`open` or `searched`); nothing on
  a player's body is a list, it is a container.
- **Presentation** (`../architecture/presentation.md`, DR-23) — the self-view (`examine me` / `look
  at me`) weaves the draw's worn items and wounds into one composed sentence.
- **Determinism/seeding** (DR-12) — the run's per-seed RNG substrate is what a seed-permuted slot
  assignment would use; it exists elsewhere in the architecture and is not yet wired to slot
  assignment (§8, open question 2).
- **15 — Moral and social layer** — the survival kit is legally the plane's, not anyone's; the pilot's
  wallet and jacket raise the dignity question of stripping a body. *(Claude, 2026-09-26 — §6 Q4:
  "the guide's duffel" read as the kit; corrected.)*
- **The heat system** (no design document yet — to be written; *Claude, 2026-09-26*) — every worn
  thing, every pocket and every body part carries a temperature; the phones' batteries, the chocolate
  and the sanitizer behave by theirs (§4.9).
- **01 — Premise and world / 13 — Events, escalation and weather** — the crash date inside October,
  which decides whether the law's winter kit is aboard (§4.9).

**These depend on it:**
- **17 — Rooms and living rooms** — the seats are the parts-machine that carries each slot's
  luggage; the seat labels proposed here (§4.6) are what that document's seat-row exemplar was
  recast to describe.
- **02 — The experience** — the first night's warmth band differs by slot, which is the sample
  week's opening beat.
- **20 — The agent player and research** — an agent draws a slot exactly as a human does.

---

## 6. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9) against block 1 and the October season.** Q2, Q4, Q5 and
Q6 are answered by the decided design or by reality, each marked for Andrew's check; Q1 and Q3 are his
and sharpened; Q7 and Q8 are new and his. The original wording of every question is kept as the record.

~~1. asked:~~ **Answered 2026-09-27 (Andrew):** *"we dont make up extensive back stories, no one should be forced to have reasons for flying just be given different clothes and stuff"* *The question as it was asked:* **Who are the five people, and does §4.9's October check of what they carry stand?** Andrew's
   2026-09-16 approval covers the four-seat interior and the kid, not the people. What he is deciding
   is taste: each person's reason to be on a mail plane into the Interior in mid-October, and the
   spread of what they wore. Every item already passes the October check in §4.9; the two reasons that
   fit the date less well are the guide's "lodge job" (lodges close in September) and the kid's
   "visiting family" (it is the school term). *Options:* (a) keep the five people, with §4.9's October
   notes; (b) revise individual people at the sitting as he reacts; (c) redraw the party from who really
   rides a mail run in October — village residents going home from town, a health aide, a teacher, a
   hunter going home, a mine worker on rotation. **Recommendation: (a), then (b) slot by slot** — the
   spread from the townie's cotton to the kid's snow pants is what makes sharing an act, and §4.9 keeps
   every item physically honest for the date.

   *(The original, kept as the record:)* **Are the five slots' specific contents final, or a placeholder for a fuller pass?** The
   provenance audit lists the whole table as Claude's proposal; Andrew's 2026-09-16 approval covers
   the four-seat interior and the kid's inclusion, not item-by-item sign-off on what each slot
   carries. *Options:* (a) approve the table as shipped — it is already built and probed (§8); (b)
   revise individual slots at the review sitting as Andrew reacts; (c) treat it as a placeholder and
   redo it from scratch. *Recommendation then: (b)* — the table is a working baseline with real physics
   behind every item; review it slot by slot rather than wholesale.

~~2. Does the seed actually permute who gets which slot?~~ **Claude's answer (2026-09-26), for
   Andrew's check:** yes — it is a draw, within each run. Andrew decided that nothing about a player's
   starting kit is chosen; it is decided the moment the run begins (§2, 2026-09-07), and document 02
   already says the seed deals the slots. So sign-up (b) contradicts his decision, and permuting only
   across runs (c) leaves one person the townie for a whole evening. The run seed deals the slots on the
   per-run seeded random-number stream (DR-12), and the deal is logged like every other seeded draw
   (document 20). It is built with the instance spawn, after the design is finalized (document 05 §2:
   nothing is built before then).

   *(The original, kept as the record:)* **Does the seed actually permute who gets which slot?** The design's fairness note depends on it
   ("the seed permutes slots so no player is always the townie"), but `build.py::dress()` currently
   takes an explicit `slot` argument with no seed-driven permutation — nothing assigns slots to
   players at all yet. *Options:* (a) build the permutation now, using the seeded RNG substrate
   DR-12 already provides; (b) leave slot assignment to whoever forms the party (sign-up, not a
   draw); (c) permute only across repeated runs, not within one. *Recommendation then: (a)* — the
   fairness claim is currently just a sentence in a document; it needs the mechanism it describes
   before more than one sitting relies on it.

~~3. asked:~~ **Answered 2026-09-27 (Andrew):** *"up to 5 people play, empty seats are empty - unused characters can be dead and clothes searched"*; and *"AI agents can play the game with players if they want. otherwise the char is dead if no one plays it"* *The question as it was asked:* **What is in a seat nobody plays?** *(Sharpened 2026-09-26: this is document 19's Q1 asked from the
   kit side, and it is decided once, there.)* Already settled: the plane carries five survivors — the
   right seat and 1A/1B/2A/2B — and the pilot, dead at the start; one survivor per player; an agent is
   a player like any other (2026-09-17). What Andrew is deciding is the social shape of a smaller run.
   The kit consequence of each answer: *(a)* nobody flew in it — the seat carries freight instead (real
   for a 206 on a bush run, and it fits the load in §4.9), that person's bag is not aboard, and the
   law's blanket count falls with the occupants; *(b)* that survivor died in the crash — a second body
   with clothes, pockets and a bag; *(c)* that survivor is aboard, alive and incapacitated; *(d)* an
   agent plays them. **Recommendation: as document 19 recommends** — (d) when the run includes agents,
   (a) otherwise; it keeps as much material in the plane as a full party has and adds no body nobody
   chose.

   *(The original, kept as the record:)* **How many players does a run support?** Five slots are authored (four adults plus the kid).
   *Options:* (a) exactly five, no more, no fewer; (b) a run seats any subset of the five, and an
   unfilled slot's occupant becomes an unplayed body or is simply absent; (c) more slots get authored
   later for a bigger party. *Recommendation then: (b)* — nothing requires every slot to be a human or
   an agent, and runs "for agents only" (per the framing every document keeps) may want fewer than
   five.

~~4. Is a slot's luggage welded to the slot, or a second draw?~~ **Claude's answer (2026-09-26), for
   Andrew's check:** welded — by reality, not for simplicity. A bag holds what its owner packed for
   their own trip, so the townie's toiletries and the salesman's laptop travel with whoever plays that
   person; a second, independent luggage draw (b) would put a stranger's life in your bag. What never
   moves with a slot is what is not anyone's: the survival kit (the plane's, by law), the mail and the
   freight. Where each bag ended up is the crash's, per §4.3. The table's old line that "the survival
   duffel is HIS" mixed the two and is corrected in §4.1.

   *(The original, kept as the record:)* **Are a slot's luggage contents welded to the slot, or do they permute independently of the
   clothing/injury draw?** *Options:* (a) luggage is furniture of the bag, keyed to the seat, and
   travels with whoever draws that slot; (b) luggage is a second, independent draw; (c) no
   permutation at all — luggage stays exactly where it is regardless of the draw.
   *Recommendation then: (a)* — simplest, and consistent with the guide's duffel being "legally the
   plane's," not his personally.

~~5. The guide's and the nurse's bags are missing their named extras.~~ **Claude's answer
   (2026-09-26), for Andrew's check:** not a design question — a gap between the design and the code,
   closed by the decided process. The extras are rows of the design: they go into the ontology store
   with their owners when the plane is censused (document 05 §4.5 — every item with its materials,
   mass, form, states and what it could become), and reach `objects.py` through the converter when the
   cabin zone is finalized. §4.9 changes one of them: the nurse's headnet is a summer leftover, and the
   law's kit carries one for each occupant besides.

   *(The original, kept as the record:)* **The guide's duffel and the nurse's backpack are missing their named extras.** §4.1's table lists
   the guide's duffel as adding a headlamp, a ferro rod and a steel cup, and the nurse's backpack as
   adding a wool sweater, a headnet and a book of matches; neither appears in `objects.py` — only the
   pre-existing duffel (multitool, paracord, socks) and backpack (canteen, spare shirt) are there.
   *Recommendation then: add the missing rows* — small, mechanical, and closes a real gap between this
   document and the shipped table.

~~6. The four-seat interior is approved but not built.~~ **Claude's answer (2026-09-26), for Andrew's
   check:** the same answer, and one thing more. The recast is content, written into the ontology store
   at the cabin zone's census and converted into rows when that zone is finalized (the program's "the
   cabin zone" step). The thing more is Andrew's 2026-09-26 decision that **the plane is an entity** —
   its seats, hat shelf, baggage bay, cargo door, windows and the breach are its parts, each opening
   open or closed, with an internal heat (document 17 §4.8). So the recast is not "just rows": the
   seats are parts of the plane entity, and the openings feed the heat-system design, to be written.

   *(The original, kept as the record:)* **The four-seat interior is approved but not built.** `characters.py`'s slot `seat` fields already
   say `1A` / `1B` / `2A` / `2B` / `right seat`, but the only seat objects in `objects.py` are the
   earlier six-seat draft's leftovers (`seat`, ident `11B`, in `mid_cabin`; `seat2`, ident `12C`, in
   `rear_cabin`) — there is no seat object for 1A, 2A, or the right seat, and no hat shelf or cargo
   door object anywhere. *Recommendation then: queue the recast as ordinary content work* behind the
   existing authoring seams (`objects.py` / `characters.py` rows only) — it needs no new mechanism,
   just the rows this document already specifies (§4.6).

~~7. asked:~~ **Answered 2026-09-27 (Andrew):** *"no"* *The question as it was asked:* **Is there a firearm aboard?** *(New, Claude, 2026-09-26.)* Reality allows it and often has it: a
   gun may fly unloaded and cased in checked baggage with up to 5 kg of ammunition (FAA PackSafe), guns
   are ordinary in the Alaskan bush, and the statute no longer requires a survival gun (§4.9). One gun
   changes the bear, the hunting (a shotgun makes a ptarmigan a near-certain meal), the combat system
   and the moral layer — which is why it is his. *Options:* (a) never aboard; (b) one in every run,
   where the crash puts it — a hunter's cased rifle in the baggage bay, or a survival shotgun lashed
   with the kit — with the ammunition a person really carries, a box or two; (c) a seeded run
   variable, like the hare cycle (document 23 §4.4): some runs have one, most do not. **Recommendation:
   (c)** — true to the place either way, a replay lever, and it keeps the thrown rock, the snare, the
   spear and the club the everyday ways to hunt and fight in most runs; when present, the crash decides
   its state and distance (power ∝ cost, §4.3).

~~8. asked:~~ **Answered 2026-09-27 (Andrew):** *"before or after is fine, the sleeping bag would be buried with the tail wreckage, two blankets can be inside the plane hidden somewhere, we dont want it too easy but not too hard"* Andrew, 2026-09-27: *"what do you mean by 'law'? it is a weird term to use."* — the Alaska statute was the reviewers' realism baseline; it is not a design constraint, and what is aboard is the design's call. *The question as it was asked:* **Which day in October does the plane go down — before or after the 15th?** *(New, Claude,
   2026-09-26.)* The month is settled (freeze-up); the day is not, and the law makes it matter: from 15
   October Alaska requires a pair of snowshoes, a sleeping bag and a wool blanket for each occupant over
   four in the kit (AS 02.35.110(a)); before it, those are the pilot's choice. The day also sets the
   weather (Fairbanks normals fall from about 7 °C / −2 °C on the 1st to 1 °C / −8 °C on the 15th and
   −7 °C / −16 °C on the 31st) and the daylight. *Options:* (a) on or just after 15 October — the
   winter kit is aboard by law; (b) early October, before the 15th — warmer, longer days, and a
   thinner kit unless the pilot carried the winter items anyway; (c) a seeded day within October, the
   kit following the law for that day. **Recommendation: (a)** — mid-October is freeze-up by the
   normals (an inch of snow, skim ice, berries still on the bush), and the winter kit is part of what
   the rescue graph was built on (§4.5). How full that kit is stays document 10's Q9.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18 (Andrew, block 1):** capacity lives on containers (hands, pockets, bags, worn clothing, a
  dragged frame); inventory is limited by weight and space; exceeding it is answered physically, never
  refused (document 04 §3.11, document 18 density).

- **2026-09-18 (Andrew):** bulk is derived from density and a gathered quantity is an aggregate; capacity on containers stands as written.

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-checked against block 1 and the October season.
  **Answered for Andrew's check:** Q2 (the seed deals the slots within each run — his "decided the
  moment the run begins"), Q4 (a bag travels with its owner; the kit, mail and freight are nobody's),
  Q5 and Q6 (gaps between design and code, closed through the ontology store and the converter; the
  seats are parts of the plane entity, document 17 §4.8). **Sharpened and left for Andrew:** Q1 (who
  the five people are, with §4.9's October notes), Q3 (the unplayed seat — decided once, in document
  19 Q1). **New for Andrew:** Q7 (a firearm aboard — recommended as a seeded run variable) and Q8 (the
  crash day relative to 15 October, which decides the law's winter kit — recommended on or just after
  it); how full the kit is points to document 10 Q9. **Design
  text:** the season banner; §4.5's statute read at source and corrected (one wool blanket for each
  occupant *over four*, plus the tackle, knife, fire starter and headnets) and wheels rather than skis
  at freeze-up; §4.9 added — October normals, what Interior Alaskans really wear, the phones as a heat
  problem, what cannot fly (bear spray, aerosols, strike-anywhere matches), the crash date on or after
  15 October recommended (Q8), the legal ration week (~35,000–50,000 kcal for six) as the real baseline, the 206's
  useful load (~100–150 kg left for kit, bags, mail and freight), real carrying loads. The nurse's
  suturing points at document 11 Q6; the pilot's body materials follow document 12 §4.3a.

- **2026-09-27 (Andrew):** Q1 no back stories; Q3 up to five play, empty seats are empty, an unplayed character is dead and searchable, agents may play; Q7 no firearm; Q8 either side of the 15th — the sleeping bag buried with the tail wreckage, two blankets hidden in the plane, *"not too easy but not too hard"*; the survival kit buried somewhere (document 10 Q9); the statute is not a constraint. Banner at §4.1.

## 8. What exists today

**Built**
- The crash draw for all five slots — worn items, pockets, injuries — exactly as §4.1's table:
  `game/world/scenarios/whiteout/characters.py` (`SLOTS`, `outfit()`, `character_state()`).
- The clothing v2 fields the draw needs (`covers`, `wind`, `waterproof`) and the model that reads
  them (regional loss, wind multiplier, wet fraction, the mitten fine-work gate, warmth bands):
  `game/world/sim/systems/warmth.py`.
- Dressing at spawn: `game/world/scenarios/whiteout/build.py::dress()` — called with an explicit
  slot argument (no seed permutation; open question 2).
- Most of §4.3's luggage: the townie's suitcase and toiletry bag (floss, razor, sanitizer, tampons)
  and paperback; the salesman's laptop bag (laptop, cables, water bottle, snacks); the kid's hockey
  duffel (stick, tape, pads); the mail sack (letters, twine) and the parcel addressed to V. Holt
  (beaver mitts inside); the freight crate and toolbox (pliers, hacksaw blade, shear pins) and the
  dog food; the cooler (frozen fish); the guitar case (a guitar whose strings are wire and neck is
  wood, as parts) — all in `game/world/scenarios/whiteout/objects.py` (its "the luggage, the mail
  and the freight" section).
- Tests and probes: `game/tests/sim/test_kit.py` (every slot's rows are sound; luggage is placed and
  reachable; a dressed actor sees its own pockets); `game/world/scenarios/whiteout/probes/kit.py` —
  fifteen probes across the five slots and the luggage, all `status: pass`.

**Designed, not built**
- The seed-permuted slot assignment (open question 2) — nothing wires DR-12's per-run seeded RNG to
  "which player gets which slot."
- The guide's duffel extras (headlamp, ferro rod, steel cup) and the nurse's backpack extras (wool
  sweater, headnet, book of matches) named in §4.1 — open question 5.
- The four-seat interior recast (§4.6) — open question 6: the seat labels are designed and
  referenced in `characters.py`, but no seat objects, hat shelf, or cargo door exist for it in
  `objects.py` / `zones.py` / `spaces.py`.
- `give X to Y`, the huddle (two bodies, one blanket, shared loss), the sweat/drying cycle, and
  dexterity decaying by the minute for bare hands (§4.4, §4.7) — `warmth.py` has only the binary
  mitten check (`fine_work_ok`); `huddle` exists only as a parser synonym mapped to `put`
  (`game/world/sim/parser/vocab.py`) and one `todo`-status phrasing probe.
- A phone battery process — the phones carry a `battery` number in state, but nothing ticks it down.

**Nothing**
- The satellite communicator / PLB question (`plane-interior.md` §9) — omitted per the 2026-07-04
  decision to backlog it.
