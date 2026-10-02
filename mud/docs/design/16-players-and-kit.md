# 16 — Players and kit: the slots, draws, pockets, luggage, the 206 interior

> **Status: reviewed with Andrew 2026-09-28.** Architecture counterpart:
> [`../architecture/clothing-warmth.md`](../architecture/clothing-warmth.md) (DR-25; DR-25a's region,
> wind and wet model is live in code — `warmth.py` — but not yet written into that document; see §8).

---

## 2. Decisions

### Andrew's decisions

- **2026-09-07 — different draws, real luggage, the 206.** Each player starts with a different clothing
  and injury draw and different things in their pockets; luggage has things in it; the clothing system
  affects warmth loss and other things; the aircraft is a 206. Nothing about a player's starting kit is
  chosen; it is decided the moment the run begins.
- **2026-09-16 — the four-seat interior, and the kid.** The right seat, 1A, 1B, 2A and 2B, a hat shelf,
  a cargo net and a jammed cargo door (§4.6). The kid is in: the party is four adults and the kid.
- **2026-09-17 — the pilot starts the run dead.** **2026-09-27:** he carries no clues.
- **2026-09-18 — what you can carry.** Inventory is limited by weight and space; capacity lives on the
  things that carry (hands, pockets, bags, worn clothing, a dragged frame); bulk derives from density,
  and a gathered quantity is one aggregate; exceeding capacity is answered physically, never refused.
- **2026-09-26, 2026-09-27 — the season** is the first week of October in interior Alaska (document 13
  §4.2 has the weather and the daylight).
- **2026-09-27 — the party.** Up to five play. A seat nobody plays holds a dead character whose clothes
  and pockets can be searched; AI agents may play seats. No back stories: nobody needs a reason for
  flying. Characters differ in their clothes, their injuries and what they carry, and in how well and
  how fast they do things — a woodsman lights fires better; a technically proficient character sees a
  fault in a device.
- **2026-10-02 — a hidden skill sheet that grows with practice.** Every character has a hidden sheet
  of skills, one for each kind of act whose outcome involves chance; it starts from the seat and rises
  with practice (§4.1).
- **2026-09-29 — sex and name are the player's.** The seat is dealt at random; each player chooses
  their character's sex and name in the first tutorial room, and the body and pronouns follow (§4.1).
- **2026-09-28 — everyone boarded in a coat; some were lost in the crash.** It is cold out, so nobody
  flew without one; some came off in the warm cabin and the crash took them. The kid wears an ordinary
  jacket, not ski gear — full snow gear to sit in a plane makes no sense and would make the start too
  easy; his snow pants and mittens are packed in his duffel in the tail wreckage. *(Whose coats were
  lost and where they are, proposed by Claude for Andrew's check: the townie's winter parka went out
  through the breach onto the debris trail; the nurse's down jacket is stuffed down behind the rear
  seats, where the crash threw it.)*
- **2026-09-28 — the bags are not with their owners.** Some are in the back, some under their owner's
  seat or beside them; where each is, the crash decides (§4.3). The cooler holds only a few frozen
  salmon fillets — a meal or two. What is under the seats is §4.6's list.
- **2026-09-28 — pockets hold everyday things; anything useful is in a bag you have to find.** Nobody
  starts with a knife, medical supplies, a compass or fire in hand. Pockets hold a wallet, a phone,
  keys, gum, lip balm, a pen, reading glasses, a hip flask, a candy bar; the tools and supplies are in
  bags the crash left somewhere that takes work to reach (§4.1). The salesman's reading glasses are
  convex: in sun, they can light tinder. More things are under the seats (§4.6).
- **2026-09-28 — fire has to be found or earned.** Nobody starts with a lighter or matches in hand. A
  lighter is fine, but it has to be found — one is packed in a jacket in the luggage, and searching a
  bag turns up the clothes in it, each garment's pockets searched in turn; there can be more than one
  lighter, never everywhere. There can be more than one book of matches, and the easier one is to find,
  the fewer matches it holds; the dead pilot has a book with two left. No whole fire kit; a flint
  striker (a ferro rod) in a duffel is fine. Where each is (document 07 §4.6): the canvas jacket in the
  townie's suitcase; the nurse's damp book of about eight; the salesman's dry metal lighter in his
  laptop bag, which lights again on avgas; the ferro rod in the guide's duffel.
- **2026-09-27 — what is aboard.** There is no survival kit. The sleeping
  bag is buried with the tail wreckage; two blankets are hidden inside the plane; there is no firearm.
  One of the packs holds a few very basic supplies — iodine tablets, only a couple of days' worth — for
  whoever takes the time to rummage through the plane and the wreckage; a sewing needle and thread are
  aboard; a tarp is aboard, to help seal the openings the crash tore in the plane — branches and
  anything else that covers serve too, and a lean-to is in. The tarp is also a ground signal: laid in
  the open it is something a search plane can see, so one tarp has two uses and the party chooses
  (document 14 §3.4). Not too easy, not too hard.
- **2026-09-27 — the battery and the radio.** The plane's battery is in the nose, wired and fine. The
  radio is a hand radio in the plane's cabin, and its batteries are buried in a bag in the tail section
  (document 14 §3.2).

### Proposals (Claude)

None left open: the slots, their clothes, pockets, injuries and bags, the luggage and where it lies,
the cabin and what is under the seats, carrying, and the early-October check were accepted at the
2026-09-28 sitting, with Andrew's changes. The clothing mechanism is document 08's.

---

## 3. In one paragraph

You come to belted into a seat you did not choose, wearing whatever you happened to have on when you
got on the plane, with whatever was in your pockets — almost none of it meant for this. One of you has
a parka, a pocketknife and a few bruises; one has a light jacket and a duffel full of hockey gear somewhere in the wreck;
one has a denim jacket, no gloves, and a phone that is, for now, the party's only clock and light. What
you are wearing when the plane stops moving is the single biggest thing that decides whether you are
cold tonight — and it is different for everyone, as is what each of you is good at, which turns "who
gets the good coat" into a question the party has to answer together, in the first hour, long before
anyone says the word "rescue." A seat nobody is playing holds someone the crash killed, still dressed.
There is no survival kit, and nobody has a gun.

---

## 4. The design

### 4.1 The draw (one slot per player, deterministic from the run seed)

A **slot** is a seat, plus what its occupant wore, carried, and suffered in the crash — no back story
(Andrew, 2026-09-27). Five slots are authored. Up to five play; a seat nobody plays holds a dead
character whose clothes, pockets and bag are there to search, and AI agents may play seats
(2026-09-27). The run seed deals the slots within each run (2026-09-28),
on the per-run seeded stream (DR-12), and the deal is logged like every other seeded draw (document
20) — nothing is random at runtime beyond the seed, and nobody is the townie every run.
**Each player chooses their character's sex and name** (Andrew, 2026-09-29), in the first tutorial room — *"Before you wake: are you a man or a woman? What's your name?"* The seat itself is still dealt at random, so what you wore and how you were hurt stay unchosen; the body and the pronouns follow the choice (the kid is a teenage boy or girl), and the seat's clothes are sized to fit. The pronouns in these documents are for reading only.

| slot | seat | wearing | pockets | injury | their bag |
|---|---|---|---|---|---|
| **the guide** | right seat | parka (down, hood), wool base layer, insulated boots, gloves, wool hat | a chocolate bar, a wallet | minor bumps and bruises (sore for a day or two) | his own duffel, in the baggage bay behind the jammed cargo door: his pocketknife (the one real knife aboard), a compass, a headlamp, a ferro rod, a steel cup |
| **the townie** | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves — the winter coat lost in the crash (below) | phone (light, clock, a dead battery by day 2), wallet (cash, cards, ID — paper), gum, keys, earbuds (wire) | a cut forearm (bleeding; the census wound) | a soft suitcase, in the baggage bay: cotton clothes, a canvas jacket with a lighter forgotten in its pocket, a towel, toiletries (floss = cordage; razor = edge; sanitizer = fire starter; tampons = tinder + wound packing; a travel sewing kit — a needle and a card of thread), a paperback |
| **the nurse** | 1B | fleece jacket, hiking boots, a scarf, thin gloves — the down jacket lost in the crash (below) | lip balm (wax), hair ties (cordage), a pen | minor bumps and bruises (sore for a day or two) | a backpack, behind the jammed aft bin: the med pouch (gauze, tape, ibuprofen, a suture kit — she knows how; the player still types each act), canteen, spare shirt, a wool sweater, a headnet, a book of matches (about eight, damp where the canteen leaked), a part-used bottle of iodine tablets |
| **the salesman** | 2A | wool overcoat, dress shoes, leather gloves, a good scarf | a hip flask (whisky), reading glasses (convex — in sun, a lens that can light tinder), a notebook (paper) | concussion (fatigue faster; confusion messages the first day) | a laptop bag, under his seat: laptop (battery — sparks, heat, then dead), cables (wire), a metal water bottle, snacks, a wool blanket, an old metal lighter in a side pocket, its wick dry |
| **the kid** (16) | 2B | a light insulated jacket, jeans, sneakers — no hat, no gloves | a phone, a candy bar, sunglasses | minor bumps and bruises (sore for a day or two) | a duffel, in the tail wreckage: hockey gear (a stick = a rod; tape = tape; pads = foam), a sleeping bag, snow pants and mittens packed for later in the season, a multitool (a gift — a knife blade among its tools) |

*(The kid's sleeping bag and the salesman's blanket are the sleeping bag and one of the two blankets
Andrew placed on 2026-09-27 — see §4.3's note.)*

**What each is good at.** Characters differ in how well and how fast they do things (Andrew,
2026-09-27): a woodsman lights fires better; a technically proficient character sees a fault in a
device — the hand radio's loose wire — at once, where anyone else finds it more slowly, and the world
says so (document 14 §3.2). Which slot is good at what is content still to be written with the slots
(document 14 §3.8).

**The hidden skill sheet** (2026-10-02). Every character carries a sheet of skills the player never
sees, one for each kind of act whose outcome involves chance — throwing, aiming a sling, setting a
snare, fishing, friction fire, striking a spark, fighting, closing a wound, climbing, and any other the
acts come to need. It starts from the seat (the woodsman's fire and snares, the nurse's wound care) and
**rises with practice**: every attempt teaches a little, a miss as well as a hit, fastest at first and
slower later, as real learning goes. It shows only in outcomes — fewer misses, quicker, neater work —
never as a number or as advice, and it works the same for an agent as for a human. Cold hands, pain and
tiredness act on top of it (documents 08, 11). Getting better with time is also what keeps a party
that really tries from an endless run of bad luck (document 10 §4.8).

The **pilot** is not a player slot. He starts the run dead (Andrew, 2026-09-17) and carries no clues
(2026-09-27): what he wore and carried — a flight jacket, a lighter — is found on a body whose materials
are skin, fat, muscle, bone, blood and organs (document 12 §4.3a).

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
addressed to V. Holt), the **freight** (flour, the coffee tin, a small bag of dog food, a box of shear pins, a
toolbox — screwdrivers, pliers, a hacksaw blade that is both an edge and a saw), a **cooler** (a
few frozen salmon fillets — a meal or two, not a larder (2026-09-28); the cooler is a vessel), and a **guitar case** (a story object: the strings are wire, the
case is a sled, the neck is wood). A bag in the tail section holds the hand radio's batteries (document
14 §3.2).

**The crash is the difficulty engine.** Realism supplies the inventory; the crash supplies the
difficulty. A survival kit would make the game too easy, so there is none (Andrew, 2026-09-27). **The
sleeping bag is buried with the tail wreckage, and two blankets are hidden inside the plane**
(2026-09-27). The toolbox is in the crushed tail cone (pry it open), the cooler was thrown into the
brush along the trail (search for it — each flurry hides it a little more), and the hacksaw blade — the
keenest edge in the valley — is a walk away. A paperback is at your feet; the hatchet is a hundred
metres out in the brush with a cracked haft. Where each thing lies is decided case by case, by what makes the game better (2026-09-28): what would make the start too easy — the tools and supplies that solve the big problems — is not lying in plain sight in the first room, and no rule hides things away; everything else lies where it would really lie — a dead fish on the shore. Not too easy, not too hard.

**Where the bags are** (Andrew, 2026-09-28): not with their owners. Some are in the back — the baggage
bay, the aft bin, thrown into the tail — and some are under their owner's seat or beside them, as
carry-ons are; where each ended up is the crash's (§4.1's table, §4.6). What is in a bag is what its
owner packed for their own trip, so whoever plays the townie is the one whose suitcase holds the canvas
jacket; the mail and the freight are nobody's here.

**One sleeping bag and two blankets in the whole plane** *(Claude's reading of Andrew's 2026-09-27 decision, for his
check)*: the sleeping bag in the kid's duffel is the one buried with the tail wreckage, and the salesman's wool
blanket is one of the two hidden inside the plane — the decision named one sleeping bag and two blankets, so the
slot table's are those, not more besides.

### 4.4 The clothing system (DR-25 → v2)

Each wearable declares which body regions it covers, how much wind its outer shell stops, how
waterproof it is, and its mass; it inherits a wetness quantity and damage state from the world's
general object model. From that, the model derives warmth loss by region, a sweat/drying cycle, a
dexterity penalty for cold or mittened hands, a movement effect from footwear, a visual-signal value,
and the physics of sharing — the huddle bonus among them. This mechanism, its numbers, and what of it
is built versus still designed is **08 — Warmth, clothing and shelter** in full; this document keeps
only the draw that feeds it (§4.1).

### 4.5 The aircraft

The aircraft is a **Cessna 206-class piston single** (Andrew, 2026-09-07) with the four-seat interior of
§4.6 (2026-09-16). The type has a clamshell cargo double door on the right rear, and a hat shelf and a
netted baggage bay behind the last row. A real bush plane has no airline-style overhead bins — only a
hat shelf, floor tie-down tracks and cargo netting — and neither has this one.

In early October (2026-09-28), with bare ground or a few centimetres of
snow and only skim ice on still water, a mail plane landing on village gravel strips flies on wheels —
big tundra tyres — and the skis go on when there is snow to land on. The tyres and their tubes are
rubber: black signal smoke, and a band that stretches for a sling.

The plane's **battery is in the nose, wired and fine** (Andrew, 2026-09-27); it does not power the hand
radio (document 14 §3.7). There is no survival kit (§4.3). Where the small supplies are (2026-09-28):
the iodine tablets are in the nurse's backpack — a part-used bottle of about twelve, two to a litre of
water, so about six litres: a couple of days for one person, less than a day for the party; the sewing
kit is in the townie's toiletry bag; the tarp — a folded blue plastic tarp, about 3 × 4 m — is in the
baggage bay under the cargo net, with the freight. It seals the crash's openings, and it is also a
ground signal: spread in the open, its blue shows against brown ground or new snow to a search plane
(document 14 §3.4). One tarp, two uses — sealing the plane or signalling — is a real choice
(2026-09-27).

### 4.6 The interior (the 206)

**Under the seats** (Andrew, 2026-09-28) — carry-ons and whatever the crash threw there, found by looking or searching
under each seat: under the pilot's seat his flight bag — a flashlight with weak batteries, a pair of
work gloves, a roll of duct tape, the plane's tie-down ropes; under 1A, a half-full water bottle that
rolled there; under 1B, a paper sack of the salesman's trail mix, burst; under 2A, the salesman's
laptop bag; under 2B, a phone charging cable and a crumpled chip bag.

- **Seats**: the pilot's seat and the right seat up front; **1A/1B** (row one), **2A/2B** (row two) —
  the labels the manifest on the kneeboard uses to name who sat where, itself a clue and a story. Each
  seat is the same parts-machine (cover, cushion, belt, bolts — the seat exemplar in
  **17 — Rooms and living rooms** §4.3) with a DIFFERENT damage and find: 1A intact; 1B wrenched on its
  bolts; 2A thrown loose (a movable frame — a windbreak, a sled base); 2B thrown against the hull. What
  is under each seat is the list above; there is no life vest (a land plane carries none).
- **The hat shelf** (behind row two): hats, a scarf, the kid's helmet — a shelf, not a bin.
- **The baggage bay** behind it: the cargo net over the bags (cut it or unhook it), the freight and the
  mail against the bulkhead.
- **The double cargo door** on the right rear: jammed by the impact (pry it) — the second way out
  besides the breach; ice seals it overnight as an event.
- The hat shelf and the cargo net are opened, pried and searched like any container.
- **Windows**: crazed plexiglass (acrylic — document 18 §4.8) — sharp sheets when broken, and a
  possible cover for the breach.
- **Up front**: the six-pack instruments, the whiskey compass on the glareshield (takeable), the ELT's
  remote switch and placard (the ELT itself is in the tail, and broken — document 14 §3), headsets on
  the yokes, the halon extinguisher, the magneto key in the ignition, the kneeboard with the manifest
  and the sectional chart.

**The cabin is rooms like any others** (Andrew, 2026-09-26, 2026-09-28): the cockpit, the mid cabin
and the rear cabin, with the seats, the hat shelf, the baggage bay, the cargo door, the windows and the
breach in them, each opening open or closed, and one shared internal heat (document 17 §4.8). There is
no plane object — nobody can move it; the wing, the engine and the tail section torn off up the scar
are fixed wreckage in their places, and the pieces along the debris trail are things like any other. The interior is
content — written into the ontology store at the cabin zone's census and converted into rows when that
zone is finalized; the openings feed the heat-system design, to be written (2026-09-28).

### 4.7 What this asks of the engine

Small — mostly content plus the warmth v2 model: `characters.py`'s slot table, plus a pure
`outfit(seed, slot) -> rows`; a loader step that dresses a character and fills their pockets at run
start (the instance-spawn work, and a `dress` helper smokes can call directly), and that leaves the
dead occupant of a seat nobody plays dressed and searchable; `covers` / `wind` / `waterproof` on
wearable rows; `warmth.py` v2 (regional loss, wet fraction, wind multiplier, dexterity, the huddle); a
`give` verb; wetness as grams on things; a phone with a battery process. Probes: each slot's
first-night warmth band; "give gloves to the townie"; "wear the sweater under the coat"; "huddle under
the blanket with 2".

### 4.8 Lens pass

- **The Player** (GD — who are they, what do they bring?) — GREEN. Five people with different coats
  is a party; four identical survivors is a chore list.
- **Cooperation** (GD) — GREEN. Heterogeneous kit is the engine of sharing; the huddle and the glove
  hand-off are the first co-op acts, hours before the antenna.
- **Fairness** (GD) — YELLOW. The townie's draw is harsh; the party's job is to fix it. The seed deals
  the slots so no one player is always the townie — not yet true at runtime (§8).

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
the load feeds the travel time (document 03 §4.1a). Capacity is a `capacity_g` and a `capacity_bulk`
on any container row; the sum of what you hold, wear and haul is what you can carry (2026-09-28).

### 4.9 Early October — what these people would really wear, carry and fly with (2026-09-28)

**The weather they dressed for.** The run is the first week of October in interior Alaska; its
temperatures, snow and daylight are document 13 §4.2's. Clothes that are right on the day they flew are
thin by the end of the run's week: the week is the turn of the season, which is the ladder document 13
builds.

**What people in the Interior actually wear in October.** Locals dress for work and for the flight:
canvas work coats and bibs (Carhartt — cotton duck, often blanket-lined), fleece, a synthetic or down
puffy, a knit hat, work gloves, and rubber boots (XtraTufs, with wool socks) or leather work boots.
Bunny boots and heavy parkas are for −30 °C and colder, not October (Wikipedia, "Bunny boots" and
"Xtratuf"; Alaska Airlines News, "Look like a local"). Many rural women wear a kuspuk — a hooded
cotton over-shirt — over their layers. People who fly the bush are told to dress for the country they
fly over, not the town they land in (FAA, *General Aviation Survival*); travellers from Anchorage or
Outside dress for the town, which is exactly the salesman.

**Slot by slot**, against early October:

| slot | what they wear, against the season |
|---|---|
| the guide | a down parka, wool base, insulated boots — more than early October needs, which is how a professional dresses for the bush |
| the townie | denim, a cotton hoodie, sneakers, no gloves — the winter parka out on the debris trail where the crash threw it; a real way to be dressed for a day in town, and the harsh draw the fairness design wants. The Alaskan default would be a Carhartt and XtraTufs, which is why the townie is the lesson — cotton, soaked, in the first snow |
| the nurse | fleece, hiking boots, a scarf, thin gloves — her down jacket stuffed behind the rear seats by the crash; right for the month. The headnet in her pack is left over from summer; the mosquitoes are gone after the first hard frosts |
| the salesman | wool overcoat, dress shoes, leather gloves — what an Outside business traveller wears |
| the kid | a light insulated jacket, jeans, sneakers — no hat, no gloves — what a sixteen-year-old wears to sit on a plane; his snow pants and mittens are packed in his duffel, out in the tail wreckage (2026-09-28). Only the guide is dressed warm, so warm gear is found, not worn |

**The phones are a heat problem.** A phone's lithium battery gives up quickly below freezing and the
phone shuts itself off; Apple rates the iPhone for use between 0 °C and 35 °C (Apple Support). On a
night below freezing (document 13 §4.2) the townie's phone in a jeans pocket dies the first night; kept
in an inside pocket against the body it keeps going. So the phone's battery process (§8) runs on the
phone's own temperature — owned by the heat-system design, to be written (heat is a state on every
entity that really has it, Andrew, 2026-09-26). Pockets are warm places, and that matters elsewhere too:
chocolate softens against the body (cocoa butter melts at about 34 °C), and cold hand sanitizer will not
light until it is warmed (document 18 §4.8).

**What cannot be aboard.** Strike-anywhere matches and aerosols do not fly as freight into the Alaskan
bush — they go by barge (Alaska Business, "Rural Retail Realities"). Bear spray is larger than the one
118 ml self-defence spray allowed in checked baggage, so it is not allowed at all (FAA PackSafe, "Sprays
and repellents"): there is a bear, and nobody has spray. And there is **no firearm** aboard (Andrew,
2026-09-27).

**What a 206 can lift at all.** A U206G's useful load is about 1,500 lb, roughly 680 kg (the type's
specification; the exact aircraft's weight-and-balance sheet on the kneeboard gives its own). The pilot
and five passengers weigh roughly 450–500 kg, and fuel for the leg plus a reserve at 13–16 US gallons an
hour is another 70–100 kg. That leaves on the order of **100–150 kg for five people's bags, the mail
and the freight**: a mail sack and a few boxes of bypass-mail groceries, which "must fit
around the mail and any passengers" (Alaska Business), not a truckload. The load is a real filter on
what is aboard, the way ecology is on the valley (`README.md`).

**Carrying, in real figures.** For the carriers above, whose capacities live on the containers (Andrew,
2026-09-18): a fit adult carries about 22 kg as a working load and about 33 kg on a long march (U.S.
Army FM 21-18, *Foot Marches*: a 48 lb fighting load, a 72 lb approach-march load). A dragged frame or
sled moves far more — on snow over smooth ground. Over bare tussocks, or the thin snow this week lays
on them, it snags on every hummock: the week never brings snow enough to fill the hollows. It runs best
on the smooth, frozen ground — the gravel bar, the shore, a trail beaten down between camp and the wood
— once the flurries have laid a skin of snow on it.

*Sources for §4.9:* FAA PackSafe, "Sprays and repellents" (faa.gov/hazmat/packsafe) · Alaska Business,
"Rural Retail Realities" (akbizmag.com) · Cessna Flyer Association 206 specifications; planephd.com
U206G specification · FAA, *General Aviation Survival* · Wikipedia, "Bunny boots", "Xtratuf" · Alaska
Airlines News, "Look like a local" · U.S. Army FM 21-18 · Apple Support (iPhone operating temperature).

## 5. Interactions

**This depends on:**
- **08 — Warmth, clothing and shelter** — the draw's worn items are the input to the warmth score;
  the draw itself is only summarized here (§4.4).
- **Containment** (`../architecture/containment.md`, DR-24) — pockets, bags, the toolbox, and the cargo
  net are all found by the one reveal rule (`open` or `searched`); nothing on a player's body is a list,
  it is a container.
- **Presentation** (`../architecture/presentation.md`, DR-23) — the self-view (`examine me` / `look
  at me`) weaves the draw's worn items and wounds into one composed sentence.
- **Determinism and seeding** (DR-12) — the run's per-seed random-number stream is what deals the
  slots; it exists elsewhere in the architecture and is not yet wired to slot assignment (§8).
- **14 — Rescue** — the hand radio's batteries in a bag in the tail; which character is technically
  proficient (§4.1).
- **15 — Moral and social layer** — the mail and the freight are nobody's here, and
  what a survivor wore, carried or packed is theirs (document 15 §4.6); stripping a body — the pilot's,
  or the dead occupant of a seat nobody plays — is an act that layer logs.
- **The heat system** (no design document yet — to be written) — every worn thing, every pocket and
  every body part carries a temperature; the phones' batteries, the chocolate and the sanitizer behave
  by theirs (§4.9).
- **13 — Events, escalation and weather** — the week's weather (§4.2 there) is what the clothes are
  measured against (§4.9).

**These depend on it:**
- **17 — Rooms and living rooms** — the seats are the parts-machine that carries each slot's
  luggage; the seat labels here (§4.6) are what that document's seat exemplar describes.
- **02 — The experience** — the first night's warmth band differs by slot, which is the sample
  week's opening beat.
- **19 — Multiplayer and instances; 20 — The agent player and research** — up to five play; an agent
  plays a seat and draws a slot exactly as a human does.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-07 (Andrew):** different draws per player, real luggage, the clothing system; the aircraft
  is a 206.
- **2026-09-16 (Andrew):** the four-seat interior; the kid is in.
- **2026-09-18 (Andrew):** capacity lives on containers; inventory is limited by weight and space; bulk
  derives from density and a gathered quantity is an aggregate; exceeding capacity is answered
  physically, never refused.
- **2026-09-26 (Claude, self-review):** the seed deals the slots within each run; a bag travels with
  its owner; the bags' extras and the four-seat interior go through the ontology store; the
  early-October check of what these people wear and carry (§4.9) — all for Andrew's check.
- **2026-09-27 (Andrew):** no back stories; characters differ in skill; up to five play, an unplayed
  seat is a dead character whose clothes can be searched, and agents may play seats; no firearm; the
  no survival kit, the sleeping bag with the tail wreckage, two blankets hidden in the
  plane; the plane's battery in the nose and fine.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2); the tarp is also a ground signal.
- **2026-09-28 (Andrew, the document's sitting):** pockets hold everyday things and anything useful is in
  a bag to find — the one real knife behind the jammed cargo door, the med pouch behind the jammed aft
  bin, the multitool in the tail; the salesman's reading glasses are convex; more things under the
  seats; the bags lie where the crash left them, not with their owners; a few frozen salmon fillets; the
  cabin is rooms like any others that hold heat; the kid wears ordinary clothes, his snow gear packed;
  pockets are warm places. **Reviewed in full.**

## 8. What exists today

**Built**
- The crash draw for all five slots — worn items, pockets, injuries — exactly as §4.1's table:
  `game/world/scenarios/whiteout/characters.py` (`SLOTS`, `outfit()`, `character_state()`).
- The clothing v2 fields the draw needs (`covers`, `wind`, `waterproof`) and the model that reads
  them (regional loss, wind multiplier, wet fraction, the mitten fine-work gate, warmth bands):
  `game/world/sim/systems/warmth.py`.
- Dressing at spawn: `game/world/scenarios/whiteout/build.py::dress()` — called with an explicit
  slot argument (no seed dealing; §4.1).
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
- The seed-dealt slot assignment (§4.1) — nothing wires DR-12's per-run seeded stream to "which player
  gets which slot"; nothing spawns the dead occupant of a seat nobody plays; no skill differences
  between characters, and no skill sheet.
- What is aboard as decided on 2026-09-27: `objects.py` still has a survival duffel on the debris
  trail, a sleeping bag in the tail cone, a wool blanket in the rear cabin, a field radio in the
  cockpit and an armed ELT in the tail cone (`PLAN.md` A12).
- The guide's duffel extras (headlamp, ferro rod, steel cup) and the nurse's backpack extras (wool
  sweater, headnet, book of matches) named in §4.1 — not in `objects.py`, which has only the earlier
  duffel (multitool, paracord, socks) and backpack (canteen, spare shirt). They go into the ontology store with their owners when the plane is censused
  (document 05 §4.5), and reach `objects.py` through the converter when the cabin zone is finalized.
- The four-seat interior (§4.6): the seat labels are designed and referenced in `characters.py`, but
  the only seat objects in `objects.py` are `seat` (ident `11B`, in `mid_cabin`) and `seat2` (ident
  `12C`, in `rear_cabin`) — no seat object for 1A, 2A or the right seat, and no hat shelf or cargo door
  object anywhere; the plane is not an entity.
- `give X to Y`, the huddle (two bodies, one blanket, shared loss), the sweat/drying cycle, and
  dexterity decaying by the minute for bare hands (§4.4, §4.7) — `warmth.py` has only the binary
  mitten check (`fine_work_ok`); `huddle` exists only as a parser synonym mapped to `put`
  (`game/world/sim/parser/vocab.py`) and one `todo`-status phrasing probe.
- A phone battery process — the phones carry a `battery` number in state, but nothing ticks it down.

**Nothing**
- A satellite communicator or personal locator beacon aboard — backlogged on 2026-07-04; not in the
  design.
