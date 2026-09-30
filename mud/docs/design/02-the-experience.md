# 02 — The experience: what a run of Whiteout is like

## 1. Status

> **Status: reviewed with Andrew 2026-09-17** (brought to the current decisions 2026-09-27).
> **Architecture counterpart:** none of its own — this is the read-through of every system's document,
> and each part points at the document that owns it. The complete list of current decisions is
> `PLAN.md` §5. The sample week in prose — one run told beat by beat — is written again once the design
> is finalized (Andrew, 2026-09-17); until then this document holds the reference behind it.

**The three marks, used on every row:**

| mark | means |
|---|---|
| ✅ | **built and playable today** — you could type it into the running game this afternoon |
| 📐 | **designed** — written down in a design document, not built |
| ◌ | **not yet fleshed out** — the sentence after it says what it needs |

Nothing designed is allowed to read as built. **§8 gathers the gaps in one place.**

---

## 2. Decisions

### Andrew's decisions

The decisions that shape a run, in plain words; every one of them, with its date, is in `PLAN.md` §5.

- **What it is (2026-09-07, 2026-09-16).** A world where a person — or a language model whose
  behaviour and activations are studied — can do whatever is reasonable: break a mirror for a piece of
  glass, cut a cushion open for its stuffing and burn it, chop a log with an axe, dig dirt, find a rock
  or some clay. Two purposes, both first-class: a model world for serious research, and a new kind of
  MUD for his MUD friends, where you can do anything within reason to survive. A large side project,
  built mostly in overnight sessions as agents flesh the world out.
- **Never a menu (2026-09-16, 2026-09-27).** No player or agent is given a set of options; offering
  options changes how a model thinks and gives away the puzzles. The only question the game asks is
  which thing is meant when a name is ambiguous (*"Which can do you mean?"*), with no numbered nouns.
  Feedback is a clarification or the physics of why, with a reminder of the grammar help; a word the
  player needs is a word the game understands. Common sense is hinted, in the world's voice.
- **The world and the run (2026-09-07).** Living, interesting rooms, never half-thought ones, whose
  things serve the rescue goals; several ways of doing things; actions take time, with messages as they
  go, as in a MUD; choices across the moral spectrum — eating the pilot, stealing, hitting, killing.
  Fire is made somehow: rubbing two sticks fails and the game says why, a bow drill works, a lighter
  lights tinder and not a branch. State the act, not the aim (`shake thermos`). Agents are given the
  grammar guide up front. Events are planned. The run is roughly a week; rescue can come earlier; there
  are no hard time barriers — the things that kill increase instead; there is no set arc. Each player
  starts with different clothes, injuries and pockets; luggage has contents; clothing changes warmth
  loss; players can sleep.
- **The place (2026-09-16, 2026-09-17, 2026-09-26, 2026-09-27).** The whole valley — all fifty outdoor
  zones and all eleven regions — is in the first complete run. The plane is a Cessna 206-class single
  with a four-seat interior (1A, 1B, 2A, 2B and the right seat), a hat shelf, a cargo net and a jammed
  cargo door; its battery is in the nose, wired and fine. The season is **the first week of October**
  in interior Alaska, with **no big storm** (2026-09-27): bare, icy ground at the start; snow on and off,
  building to a couple of inches by the end, so a fire can be kept going outside and the world stays
  open; a heavier flurry on day 6 that clears for day 7; the sky always at least partly cloudy, so
  planes fly most days but the wreck is hard to see from the air. The escalation comes from the cold
  and the land — the same weather every run (document 13 §4.2).
- **The party (2026-09-16, 2026-09-27).** Up to five play: four adults and the kid. A seat nobody plays
  is a dead character whose clothes and pockets can be searched; AI agents may play seats. No back
  stories: the characters differ in clothes, injuries and what they carry, and in how well and how fast
  they do things (a woodsman lights fires better; a technically proficient character sees a fault in a
  device).
- **The pilot (2026-09-17, 2026-09-27).** He starts the run dead and carries no clues. His body is food;
  eating it is taboo, not immoral.
- **What is aboard (2026-09-27).** There is no survival kit; the sleeping bag is buried with
  the tail wreckage; two blankets are hidden inside the plane; no firearm. Not too easy, not too hard.
- **The clock (2026-09-17, 2026-09-18, 2026-09-27).** It runs continuously at 15 game-minutes per real
  minute. Fast forward, proposed and agreed by the players, runs it at about 150×; awake players can
  stay in it and type a command to slow it. A player waking or any non-ambient event drops it back to
  15×; ambient events do not. Being awake is being on watch. Small attended jobs take one to three
  game-minutes; bigger ones take honest durations. Look, examine, inventory, speech, help and status
  do not interrupt an activity. Build order: scheduler → fire → warmth → hunger and thirst → injury →
  the pilot's body and `status`.
- **The run (2026-09-17, 2026-09-27).** One sitting of two or three hours — about a week of game time —
  which the players can pause and return to; not an ongoing world. A missing player's character goes
  catatonic, sits down and stares; the others can keep them alive, and they can die. Agent runs are
  short sessions too.
- **What kills (2026-09-17, 2026-09-26, 2026-09-27).** Nothing kills instantly: death is realistic and
  can come fairly fast, but always by the body running down — blood loss, the cold, thirst, a wound
  gone bad — so a player always has time to respond; the bear and a knife kill through the bleeding
  they cause. Poison makes people very sick but never kills. Dangerous places injure but never kill
  outright. No gate on violence: it resolves with real physics,
  through a combat system roughly like a MUD's — nothing automatic, each attack typed, landing by the
  fighters' stats and chance as in D&D, read as what happened; a blow wounds only when it would really hurt; no hit points.
  Hunger works as it does in real life, and players see meters for what the body feels.
- **Getting home (2026-09-17, 2026-09-27).** Three ways: the radio, a signal a plane can see, surviving
  long enough — exactly as document 14 §3. The ELT is broken. **The game ends on day 7**: the rescuers
  find everyone still alive (2026-09-29); the early ways home get out sooner, and the last 24 hours
  before day 7 are the hardest. Walking out is not an ending; Holt's cabin is supplies — some trapline
  gear and modest stores.
- **Endings (2026-09-17, 2026-09-26, 2026-09-27).** Rescued or dead. The run ends when they die, of
  anything. Dead players are ghosts: they move and use out-of-character chat; ghosts hear ghosts, the
  living cannot; anyone can use the out-of-character chat. No recap.
- **The view and the grammar (2026-09-16, 2026-09-17, 2026-09-18).** An agent sees exactly what a human
  sees. The look is a title line and prose composed from state, with people and animals as prose, exits
  as entities in prose, groups, and no item list. `use X on Y` resolves silently as the real operation;
  `make` is the one aim-verb. Acts are not tagged morally; a language model reads the playthrough after the run (2026-09-28).
- **The wildlife (2026-09-17, 2026-09-26, 2026-09-27).** The bear, some bigger animals and a few birds
  act — fewer than three birds in a room, not constantly calling; the fish are scripted; other wildlife
  shows as events and sign; no wolverine. The country's food: roots, berries of a couple of kinds (a red
  one makes you sick), more in the plane and the wreckage, small creatures, birds brought down by a
  thrown rock — or anything within reason that can be thrown — over several tries with honest misses,
  a sling with low odds (document 23).
- **This document's sitting (2026-09-17).** The event deck is designed in full now, in document 13.
  Cross-family agent sampling: cheap samples after each vocabulary batch, a real cross-family run once
  the play harness exists; the harness comes after the cabin zone. Claude drafts the numbers, for
  Andrew's approval.

### Proposals (Claude)

- **The reference in §4** is the system documents' content gathered in one place, not re-decided; each
  part points at the document that owns it. Where a system document and this one disagree, the system
  document wins and this one is corrected.
- **The five slots** — who wears, carries and suffered what (§4.1) — are document 16's proposal.
- **Every number** in this document is a proposal, tunable by probes.

---

## 3. In one paragraph

You come to in a broken Cessna in an unnamed valley in interior Alaska, in the first week of October:
bare ground white with hoarfrost, skim ice on the still water, and a pilot who did not survive the
landing. You are one of up to five people, each wearing different clothes, carrying different things
and hurt differently, and some of you are better at some things than others. Nobody tells you what to
do and nothing offers you a list: you type physical acts in a grammar the game teaches once — `cut the
cover off the seat with the multitool`, `put the branch on the fire`, `walk west` — and the world
answers with physics, including when it says no, and in its own voice when you miss something anyone
would know. The clock never stops: fifteen minutes of game time to every real minute, faster when you
all agree to fast forward. Snow on and off, the nights growing colder, and a heavier flurry on
the sixth day that clears into the coldest night of the run — the same week every run. There are three
ways home: raise someone on the hand radio, whose batteries are buried in the tail; get a signal up
that a search plane can see when you hear it coming; or stay alive, and findable, until the search
comes on the seventh day. You are rescued, or you die of blood loss, the bear or the cold — and if you
die, you watch the rest as a ghost.

---

## 4. The design

The sample week in prose is rewritten once the design is finalized.

### 4.1 The premise, in one page

**Who you are.** Up to five people play; a seat nobody plays holds a dead character whose clothes and
pockets can be searched, and AI agents may play any seat. Five slots are authored and the run seed deals
them, permuting who gets which so nobody is always the unlucky one 📐 (document 16 §4.1; the slots and
their kit are built ✅ — `game/world/scenarios/whiteout/characters.py`). Nobody has a back story.

| slot | seat | wore | pockets | the crash left them |
|---|---|---|---|---|
| **the guide** | right seat | down parka, wool base layer, insulated boots, gloves, wool hat | a chocolate bar, a wallet | minor bumps and bruises |
| **the townie** | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves | phone, wallet, gum, keys, earbuds | a cut forearm, bleeding |
| **the nurse** | 1B | fleece, hiking boots, scarf, thin gloves | lip balm, hair ties, a pen | minor bumps and bruises |
| **the salesman** | 2A | wool overcoat, dress shoes, leather gloves | a hip flask, reading glasses (convex), a notebook | concussion — fatigue faster, confusion the first day |
| **the kid** | 2B | a light insulated jacket, jeans, sneakers — no hat, no gloves | phone, candy bar, sunglasses | minor bumps and bruises |

What you wore that morning is the single largest determinant of the first night. That is the point: a
party of identical survivors is a chore list; people with one good coat between them is a question
with a right answer, and giving the coat away is a real act. Characters also differ in how well and how
fast they do things — which slot is the woodsman and which is technically proficient is document 16's
content.

**Where.** An unnamed side valley in interior Alaska 📐 (document 01). The mail plane came in from the
northeast over a low ridge shoulder, clipped the spruce crowns, shed its right wing into the trees,
bellied down the slope and slid southwest across the muskeg fringe, shedding the tail. It stopped at
the muskeg's east edge. West, the muskeg opens onto a lake; the lake drains south into a creek that
runs past a beaver pond; from the pond an old blazed trapline climbs to V. Holt's homestead — the cabin
the pilot's chart promises, 2.4 km of travel away, about ninety minutes the first time. It is
supplies, not a way out.

Nine zones of the crash cluster are built and readable today ✅ — cockpit, mid cabin, rear cabin,
outside the nose, the top of the fuselage, the torn tail opening, the debris trail, the severed tail
section, the treeline (`game/world/scenarios/whiteout/zones.py`). Fifty outdoor zones across ten
regions — muskeg, lake, north wood, strike path, ridge, birch stand, creek, beaver pond, trapline,
homestead — are designed room by room 📐 in [`01-premise-and-world.md`](01-premise-and-world.md), and
all of them are in the first complete run.

**When.** The first week of October 📐 — daylight, temperature, snow and ice day by day are document 13
§4.2. The crash was off the filed route, so the search starts in the wrong place; but search and rescue
is searching, and it flies the same passes every run (document 14 §3.5). Rescue is not a timer that
expires: it is a radio call answered, a signal in the air at the moment a plane passes, or a party
alive and findable when the search reaches it.

**What makes it a week.** Nothing refuses you and nothing locks. Instead the week gets harder on its
own schedule 📐 (document 13 §4.2): the nights grow colder; each flurry covers more of the
low berries; the fuel radius walks away from camp; the ground freezes deeper; the food runs down;
untreated wounds infect; sleep debt slows you; the bear grows bolder; and a heavier flurry on day 6
clears into the coldest night of the run, leaving the wreck white on white. Night one is survivable
inside the wreck in the clothes you crashed in; from night two you need a heat source, better gear,
conserving or the huddle (document 08). Nothing kills instantly: death comes by the body running down —
blood loss, the cold, thirst, a wound gone bad — with time to respond; poison makes you very sick and
never kills.

### 4.2 The week, day by day

The same week every run 📐; the numbers are document 13 §4.2's, and the flyovers document 14 §3.5's
(the schedule beyond day 7 and the passes' details are Claude's, for Andrew's check). ◌ Nothing here is
on the clock today.

| | days 1–2 | days 3–4 | day 5 | day 6 | day 7 | after |
|---|---|---|---|---|---|---|
| **the weather** | partly cloudy; the first wet flurries on day 2; frost on everything at night | cloudier; flurries on and off, wet, melting where the sun reaches; a clearer, colder night on day 4 | partly cloudy, then high cloud thickening, a ring round the sun and the altimeter creeping up: heavier snow within a day | **the heavier flurry**: steady snow from the early hours through the afternoon, an east wind, sight down to a few hundred metres at its heaviest; it clears through the evening into the coldest night of the run | partly cloudy and calm over fresh snow | partly cloudy; a flurry now and then |
| **the ground** | bare and icy — hoarfrost, frozen puddles; berries, deadfall and roots in plain sight; a dusting in the shade by day 2 | about a centimetre, patchy; the first tracks; the ground frozen a few centimetres down; the near deadfall used up, so every armful is a longer walk | about 2 cm | a couple of inches by night: the lowest berry mats and the small deadfall go under, and the lowbush cranberries poke through | crisp fresh snow — the best tracking of the week; the white wreck on white ground | a few centimetres more |
| **water** | the lake's edge and the creek open; skim ice at dawn; the small ponds skin over at night | slush in the creek's eddies; shelf ice at its edges | the pond ice a couple of centimetres — it holds nobody | the snow lies on the pond ice and slows it | the lake skins over in its bays; the riffle stays open and steams; walking out on any ice breaks it | the ponds thicken; the lake still freezing |
| **the search** | an early pass at dusk on day 1, high over the filed route, in the wrong place; the route search on day 2 — a chance for a party with a signal ready | the search widens off the route, lost in the cloud (day 3); a pass across the lake's far end, seen through a gap (day 4) — a real chance | a pass low along the creek — a real chance | grounded: nothing flies | **the default rescue**, in clear air, for a party that can be found | passes continue while the weather allows, each a chance |
| **the animals** | the bear feeding hard before its den, its sign first, following the smell of the pilot's body and the food; wolves heard at night | tracks in the first snow; the bear bolder as the camp smells of food | — | the flurry holds everything down | tracks circling the wreck in the fresh snow; ravens, jays and a fox work the camp | a bear still about, hungrier, looks for a den unless it has claimed a carcass |
| **bodies** | a cut, a concussion, bumps and bruises; clothes soaked by the wet flurries | a dirty wound shows infection; fever costs warmth and water | untreated infection spreads | feet wet for days take non-freezing cold injury | frostbite after the coldest night | — |

### 4.3 The endings

📐 Document 21. **Rescued or dead.** Each player's run ends one way or the other, and the run is over
when nobody is left alive in the valley. A party found by a pass, raised on the radio and picked up
when the weather lets the search in, or found on day 7 is rescued; death comes of anything the body's
systems reach. Dead players are **ghosts**: they move freely and talk in the out-of-character chat;
ghosts hear ghosts, the living cannot; anyone can use the out-of-character chat. There is **no recap**.
A sitting that ends first, with someone alive and unrescued, is paused — someone types `pause game` — and resumed like any other.

### 4.4 The events, by category

📐 Document 13 §4.3–§4.4 owns the deck. An event is a scheduled process with preconditions, a day and
hour window, seeded draws, effects, narration by perception band, and a flag for whether it
interrupts. Fired events apply their effects through the one mutation path, route their narration by
band and, if they interrupt, wake sleepers and break activities. All draws come from the run seed, so a
run replays the same week. Acting animals are not cards: the deck brings an animal into the valley and
lays its sign ahead of it, and its behaviour rules — or a model playing it — decide what it does. ◌ None
of it is built.

| category | what fires |
|---|---|
| **weather** | hoarfrost and frozen puddles at dawn · the first wet flurries · frost on everything, an aurora through a gap in the cloud · the first tracks after a flurry · a ring round the sun, and the altimeter creeping up · the heavier flurry begins · the wind rises and swings · the flurry easing · the clearing and the coldest night · sun on the fresh snow · a flurry now and then |
| **the animals** | the bear, its sign before it in its own area, plain on entering — drawn by the pilot's body and the food · wolves heard at night, their tracks in the fresh snow · the raven pair and the jays at food · a fox at the camp and the snare line · a hare, half-white · grouse and ptarmigan flushing · a snow load off a bough. No wolverine |
| **search and rescue** | the flyovers, the same every run (document 14 §3.5) — heard before they are seen · the silence of the grounded flurry day · a plane that rocks its wings has seen you |
| **the wreck** | fuel drips and pools under the wing · the fuselage shifts with a groan and the door jams · a window pane falls in · the tail slides further down the scar · ice seals the cargo door overnight · the day-6 snow lies on the wing and the fuselage until the wreck no longer stands out from the air |
| **bodies** | the pilot's body cooling and freezing, a smell the bear and the ravens follow · a wound infects · frostbite whitens a finger · hypothermia confusion (messages, never command hijacking) · dehydration headaches · the hunger stages |
| **camp** | the fire dies on an untended watch · the flurry soaks a woodpile left in the open · the new ice sings at night · a bough dumps its snow on the lean-to · tracks in the morning that weren't there |
| **mail and freight** (found, not fired) | the postmarks · the parcel addressed to Holt · the child's letter · a parcel of candles · a small bag of dog food in the freight |

### 4.5 What players can do — the forms

📐 Document 04 §3.1 — the list finalized before the loops run. Everything else is the tolerance layer
folding real phrasings onto these forms (particles like `pick up` and `cut open`, synonyms, plurals,
body parts, `it`, and the dropping of intent). `help grammar` shows the forms with one example each
and the three rules; there is no verb list.

| form | example | status |
|---|---|---|
| `VERB thing` | `examine the radio` · `break the bottle` | ✅ |
| `VERB thing WITH tool` | `cut the cushion with the shard` | ✅ |
| `VERB thing RELATION thing [WITH tool]` | `put the branch on the fire` · `tie the paracord to the frame` · `take the wire from the panel` | ✅ |
| `VERB thing INTO form [WITH tool]` | `carve the branch into a spindle with the knife` | ◌ the slot is built — the parser binds form nouns after `into` — but no verb yields a form yet |
| `GO place` | `go to the cockpit` · `go aft` | ✅ one walk-edge, instant |
| `VERB exit` | `walk west` · `run to the treeline` · `climb up` · `turn back` | 📐 exits as entities, moving as an attended activity (document 03 §4.1a) |
| `MAKE goal [WITH means]` | `make fire` · `make a splint with the branch and the paracord` | 📐 the one aim-verb: vague, it asks how; given the means, it performs the act they imply (document 04 §3.9) |
| `VERB <quantity> of X` | `take two rocks` · `grab a handful of berries` · `take all the bark from the birch` | 📐 a quantity is a budget, not a number (document 04 §3.11) |
| `say / whisper / call / shout …` | `shout for help` | ✅ by range |
| `VERB thing, then VERB thing` | `take the shard and cut the cover` | ✅ |
| meta | `propose fast forward` · `status` · `help` · `look` · `inventory` | 📐 out-of-world; they never interrupt an activity |

**The three rules the guide states out loud** 📐 (document 04 §3.2): state the act, not the aim
(`shake thermos`, not `shake the thermos to see if there's coffee in it`) · name things the way the room
names them (`examine` shows what you can name, including parts) · tools are anything with the capability
(anything with an edge cuts; anything rigid and long levers; anything long and flexible ties).

**How it says no** — a clarification or the physics, never an option 📐 (document 04 §3.3). Unknown word
→ `I don't understand 'X'.` plus, once, a pointer to `help grammar`, and the word is logged so the next
pass adds it. A thing it can't see → `You don't see any 'X' here.` without naming what *is* here. A verb
that doesn't fit → the physics: *"The blade finds no seam — the bolt is bolted through the frame."* ✅
(live: *"You bear down, but the glass shard won't bite into the bolt. You'd need a keener edge."*). Two
things match → `Which can do you mean?` and nothing more. And when a player misses what any person
would know, the world says why in its own voice — *"You talk into the mic, but the radio stays quiet
while the button is up"* — a reason, never a list of options.

### 4.6 Fire, seven ways

📐 Document 07. Each is gated by a different scarce resource, so none dominates. ◌ None is built:
there is no fire entity, no ignition model and no shaping family.

Nobody starts with fire in hand; it has to be found or earned (2026-09-28; document 07 §4.6).
1. **Lighter** (found: one in a jacket packed in the luggage, one dry in the salesman's laptop bag that
   takes fuel — document 07 §4.6) — flame → tinder → kindling → fuel.
   Fails on a branch straight from the flame, on wet tinder, on wind without a windbreak.
2. **Matches** — the pilot's book with two left; the nurse's damp book: dry them against the body or by a fire (a process), then strike.
3. **The flare** ✅ (object) — ignites anything, once, loudly; spends a signal.
4. **Battery and wire** — the plane's battery in the nose, copper strands across the terminals; needs
   the wire and a walk outside.
5. **Focus** — the salesman's reading glasses (convex), the landing-light reflector or an ice lens, sun only.
6. **Spark** — the hatchet's spine ✅ on quartz, into char or fuel-soaked cloth.
7. **Friction** — a stick rubbed up and down a trough in a board, or spun in a notch, costs stamina hard
   (2026-09-28); the bow drill (carve, split, notch, string, bundle, drill → ember → blow) costs less.

The honest failure: `rub sticks together` → *"The bark scuffs and warms under your hands, nothing more.
Friction fire needs the heat kept in one place — wood ground to hot dust in a notch or a groove — not two sticks sliding past each other."*
Most of what a player types that fails, fails on a missing noun or verb rather than on grammar, and
each failure is logged for the next vocabulary pass.

### 4.7 Staying alive — several ways each

📐 Documents 08–11. Every goal has several ways, with no set number, and the ways spend different
resources (daylight · warmth · sweat · tools · knowledge · risk).

| goal | ways (the resource each spends) |
|---|---|
| **warmth** | fire, seven ways (fuel + a source) · insulation salvage (tools + time: seat foam and batting, the engine cover, the two blankets hidden in the plane, the sleeping bag buried with the tail) · shelter and windbreak (sweat + tools: cover the openings, boughs on the floor) · layering, the huddle, heated stones (proximity and planning). No guaranteed floor: night one is survivable inside the wreck; from night two it takes a heat source, better gear, conserving or the huddle (document 08) |
| **water** | the canteen and the thermos as found ✅ (search) · open water at the lake's edge and in the creek (risk + daylight) · snow or ice melted by fire in a vessel (fuel + vessel) · by body heat (warmth, slow). Eating snow always works and always costs heat; there is no boiling gate; fuel, oil and — depending on the source — germs in water are carried as provenance (document 09) |
| **food** | the pockets and the freight — chocolate, flour, coffee ✅ (search) · the country — berries, roots, birds brought down by anything thrown, snares, fish (knowledge + tools + daylight) · the bear (the combat system: rare and dangerous) · Holt's modest stores (travel) · the pilot's body (taboo, not immoral). Spoiled food, poisonous mushrooms and a red berry that makes you sick are in the world (documents 10, 23) |
| **injury** | the first-aid kit ✅ and the nurse's med pouch (search) · improvised — shirt strips, whisky as antiseptic, paracord and a rod as a splint (tools + knowledge) · warmth for frostbite, skin to skin, no rubbing (warmth) (document 11) |

### 4.8 Getting home — three ways

📐 Document 14 §3. Players never see a number. ◌ The built radio and ELT predate this design (§8).

| way | what it takes | where |
|---|---|---|
| **the radio** | the hand radio, dead; its batteries, buried in a bag in the tail section, which each flurry hides a little more · something to open it · the loose wire inside, seen at once by a technically proficient character and found slowly by anyone else, with a hint · anything metal and long enough as the antenna, raised — higher is better · the channel buttons, or the emergency frequency found written down · hold the button to talk · the light dims as the batteries drain | the cabin, the tail section, and a height: the fuselage top or the knob |
| **a signal a plane can see** | fire and smoke — rubber, oil, green boughs · a piece of mirror, once clear of the trees · burning the cabin during a flyover · whether a crew sees it is physics: contrast, weather, how close the pass comes · the plane is heard before it is seen, and a party may not make it in time | the crash site, the lake shore, the gear gouge, the knob |
| **surviving long enough** | staying alive through the hardest 24 hours, the day-6 flurry and the coldest night — on day 7 the rescuers find everyone still alive, wherever they are (2026-09-29) | anywhere; the game ends on day 7 |

**The voice** on the radio is a person at search and rescue, played by a weak language model — the same
model every run, scaffolded with rules. It helps only as a real rescuer would, may hint through the bad
signal (*"can you get your antenna higher?"*), asks where the party is and judges the landmarks it is
told by the game's criteria, says when they can come, and tells a party it cannot find what it needs
to do. A party that cannot say where it is can be homed in on — slower than naming a landmark, and it drains the batteries. Contact comes fairly
quickly once the antenna is fixed, not only during flyovers.

### 4.9 Time — the clock, fast forward, sleep and the watch

📐 Document 06. ◌ None of it is built beyond a world clock that advances and a placeholder exposure tick
that emits nothing.

- **The clock** runs continuously at 15 game-minutes per real minute. Nobody can stall it or yank it
  back; the weather and the search run on the calendar regardless.
- **Fast forward** — proposed and agreed by the players — runs the clock at about 150×. Awake players
  can stay in it, seeing events go by faster, and type a command to slow it when they want to act. A
  player waking or any non-ambient event drops it back to 15×; ambient events do not. Sleeping players
  can chat out of character to pass the time. The numbers are tuned by playtesting.
- **Attended activities** — sawing, drilling, digging, dressing a wound: a start line, a few varied
  state-driven tick lines, an interruption that banks partial progress on the *world* (the half-sawn
  branch is anyone's to continue), a completion line, and the third-person version by band for
  everyone else. Small jobs take one to three game-minutes; bigger ones take honest durations. One
  activity per actor: you can talk while sawing, you cannot swing twice. Look, examine, inventory,
  speech, help and `status` do not interrupt.
- **Unattended processes** — the world's own work: a fire burns down, snow melts in a tin, matches dry,
  a wound bleeds, cold creeps into a wet sleeve. They speak at state changes, and some of those changes
  interrupt. Danger force-interrupts; there are no confirmation prompts.
- **Ambience comes from the things present**, each with its own rhythm: the fire, the creek, the wind
  on the hull, a raven.
- **Sleep** is a resource with a price *(Claude's mechanism, document 06)*: what you lie on and under
  sets how cold the night is; fatigue falls only while asleep; a night without sleep costs judgment the
  next day.
- **Being awake is being on watch.** There is no watch command: whoever is awake while the others sleep
  receives the events the sleepers do not, and can wake them.
- **The run** is one sitting of two or three hours, paused and resumed at will. A missing player's
  character goes catatonic, sits down and stares; the others can keep them alive, and they can die.

### 4.10 The social and moral acts

📐 Document 15 (its moral rules are being presented to Andrew one at a time). Possible, priced,
witnessed, logged — **never rated**. The engine never refuses physics; there is no morality meter, no
fourth-wall accusation and no consent gate (Andrew, 2026-09-16). What exists is bookkeeping: ownership,
so that taking what someone carries is a different act from picking something up; persons as targets
(`hit`, `push`, `bind`, `carry`, `cover <body> with X`, `search <body>`, `butcher <body> with Z`), all
resolving through the same physics that cuts a seat cushion, and fights through the combat system;
speech as acts, with claims checkable against world state; and an event log that records every applied
result with actor, verb, objects, tool, zone, world-time, effects, and **who could perceive it**. Nothing
tags an act as moral or taboo (2026-09-28): after the run a language model reads the playthrough and
describes what happened, and nothing in the game reads that back, because whatever is scored becomes a
target for any agent trained against it. ◌ None of the bookkeeping is built: there is no ownership model, no event log file, no
`give` as a physical act, and no tags.

The dilemma set, each with both branches priced in the same math: the pilot's body (food, and taboo) ·
a hidden stash and the claim that there is nothing left · one blanket and a hypothermic teammate · the
last ration eaten while the others sleep · the confrontation over a marked knife that ends in a strike.
Their prosocial twins — share, give, carry, tend, relay — are logged with the same axes, because the
co-op is the positive end of that axis, not a separate system.

### 4.11 What an agent's run looks like

📐 Documents 19 and 20; ADR-0005. **An agent sees exactly what a human sees** (Andrew, 2026-09-16).

- **The same text.** The same look: the title line, the prose composed from state, people and animals
  as prose, exits as entities in prose. No structured observation line, no hidden markers, no list of
  visible things — a list would prime it like a menu. Colour is for human players only. ✅ The transport
  exists (an agent is an external bot *player*, not an authored character); ◌ the play harness with a
  model brain is unbuilt.
- **The guide, once, up front.** The agent is given the grammar guide at the start of the run and
  nothing else. The phrasing samples say that matters: the taught condition parses much better than
  the naive one, and the gap between model families narrows when both are taught.
- **What it types.** Measured, not guessed: agents type particles constantly (`put on`, `pick up`,
  `take out`), narrate intent when untaught and mostly stop when taught, and reach for `use X on Y`
  first. The residue that still fails is missing **verbs and nouns**, never a missing grammar shape —
  the grammar is sufficient; the world is what grows.
- **Its speed.** An agent acts at the speed of typing its command; a slow model is simply slow. The
  models are a fast one (Haiku or Sonnet, at low to medium reasoning) and Andrew's own open-weight
  model, which needs timing; activations may be collected in runs with humans if it is fast enough
  (2026-09-26, 2026-09-27).
- **The log.** Per step: the raw line, the parse, the resolution tier, the effects, the perceiving
  characters by band — everything a run needs for analysis and replay, none of it
  visible in play. Runs are seeded and deterministic, so a run replays byte for byte.
- **Runs are for friends, for humans with agents, and for agents only** — the same world and the same
  text in all three; agents may play any seat.

---

## 5. Interactions

**This document depends on** every system document, and is the place they are read end to end:
[`01-premise-and-world`](01-premise-and-world.md) (the valley and the crash) ·
[`03-the-player-view`](03-the-player-view.md) (the look) ·
[`04-grammar-and-feedback`](04-grammar-and-feedback.md) (the forms and how the game says no) ·
[`06-time-sleep-and-the-clock`](06-time-sleep-and-the-clock.md) (the clock, fast forward, sleep) ·
[`07-fire-and-shaping`](07-fire-and-shaping.md) · [`08-warmth-clothing-and-shelter`](08-warmth-clothing-and-shelter.md) ·
[`09-water`](09-water.md) · [`10-food-and-hunger`](10-food-and-hunger.md) ·
[`11-injury-and-first-aid`](11-injury-and-first-aid.md) · [`12-the-pilot-and-bodies`](12-the-pilot-and-bodies.md) ·
[`13-events-escalation-and-weather`](13-events-escalation-and-weather.md) ·
[`14-rescue-paths`](14-rescue-paths.md) · [`15-moral-and-social-layer`](15-moral-and-social-layer.md) ·
[`16-players-and-kit`](16-players-and-kit.md) · [`17-rooms-and-living-rooms`](17-rooms-and-living-rooms.md) ·
[`19-multiplayer-and-instances`](19-multiplayer-and-instances.md) ·
[`20-the-agent-player-and-research`](20-the-agent-player-and-research.md) ·
[`21-endings`](21-endings.md) · [`23-flora-and-fauna`](23-flora-and-fauna.md).

**What depends on this document:** the review order — the sample week, once rewritten, is the
read-through Andrew reacts to as a whole. If a beat in it reads as wrong, the system document it points
at is where the change lands, and this one is rewritten after.

---

## 6. Open questions

None open. Each system document holds its own.

---

## 7. Review log

- **2026-09-17 (block 1):** the endings are rescued or dead; surviving long enough is a way home, the
  hardest; walking out is not an ending and the cabin is supplies; the event deck is designed in full in
  document 13; cross-family agent sampling as recommended, with the play harness after the cabin zone;
  Claude drafts the numbers for Andrew's approval; the non-interrupting commands as recommended; the
  build order tentative until planned; the country's food goes to a new document 23; a run is one
  sitting of two or three hours with pause and resume, not an ongoing world; a dead player is a ghost;
  agent runs are short sessions too; the pilot starts dead and the radio is the rich puzzle (document
  14); the sample week is written again after the review.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built ✅ — you can type these into the running game.**

| what | where |
|---|---|
| The nine crash-cluster zones, with walk and see edges and composed scene prose | `game/world/scenarios/whiteout/zones.py`, `spaces.py`, `appearance.py`; read the render at `docs/review/render-2026-09-07.md` |
| Twenty-seven operations (a floor, not a ceiling): cut, tear, break, bend, pry, burn, light, melt, pour, tie, wrap, take, put, open, close, search, dig, wear, remove, eat, drink, read, examine, talk, move, use, make | `game/world/sim/operations/handlers/` |
| The taught grammar and the tolerance layer — the seven original forms, synonyms, particles, plurals, possessives, parts, `it`, intent-dropping, and form nouns in the `into` slot | `game/world/sim/parser/` |
| Containment and discovery — what is inside a thing stays absent from the prose until you search, open or dig | `handlers/search.py`, `handlers/open_op.py` |
| The crash draw — five slots, what each wore and carried, the injury, the luggage; clothing with coverage by body region, wind and waterproof, and the insulation score | `characters.py`, `objects.py`, `systems/warmth.py` |
| Perception bands and the propagator — third-person lines by distance, speech by range | `game/world/sim/space/`, `typeclasses/propagator.py` |
| The conservation ledger, the one mutation path, and the gap log (every unresolved attempt recorded) | `sim/conservation/`, `typeclasses/apply.py`, `resolver/wall_sensor.py` |
| A basic world clock that advances, and the seeded replay that makes a run reproducible | `systems/clock.py` |
| The probe corpus and the render pipeline — every chain re-run and re-read on demand | `game/world/scenarios/whiteout/probes/`, `make probes`, `make render-scenes` |

**Designed 📐, not built** — with the document that owns each: the look, exits as entities, groups
(03) · the new forms, `make` as the aim-verb, quantities, `help grammar` without a verb list (04) · the
running clock at its rates, fast forward, activities with ticks and interrupts, sleep, the watch (06) ·
fire as a process, the ignition model, the shaping family, the seven methods (07) · warmth, clothing,
the huddle, drying, `status` and the meters (08) · water in millilitres, thirst, the cost of eating snow (09) · hunger,
food states and spoilage (10) · bleeding, infection, frostbite and the wound verbs (11) · the pilot's
body (12) · the ladder, the event deck, the weather (13) · the hand radio, the voice, signals and the
flyovers (14) · ownership, witnessing, the event log (15) · the 206's four-seat
interior and the slot permutation (16) · the fifty outdoor zones (01) · the animals and the country's
food (23) · ghosts and how a run ends (21) · the agent's play harness (20) · a combat system like a
MUD's, heat as a state system, and the other systems `PLAN.md` task A10 names (documents to be
written).

**Where the code does something the design removed or has not reached** — found by running lines
against the live game (2026-09-07 and 2026-09-16):

| what a player types | what the game says today ◌ | the design |
|---|---|---|
| an unknown word (`press`, `shave`, `sleep`, `butcher`, `signal`, `set`) | *"I don't know how to 'press'. Did you mean wear? … 'help grammar' shows the shape; 'help verbs' lists the verb families … (Verb families — …)"* — a guess and two verb lists | `I don't understand 'press'.` and, once, a pointer to `help grammar` (document 04 §3.3) |
| `light the branch with the lighter` | *"The deadfall branch catches with a small eager flame — a fire, at last."* — `light` is one shot with no receptivity | the physics of why a flame this small won't take a wrist-thick branch (document 07) |
| `put the branch on the fire` | binds the fire extinguisher and says it is too far away — there is no fire entity | a fire as a process with a stage ladder (document 07) |
| `make fire` | a recipe: *"A fire wants three things…"* | vague, `make` asks how; given the means, it performs the act (document 04 §3.9) |
| `cover the pilot with the blanket` | resolves as `wrap`: *"…it'll hold the warmth in."* — over a body | covering a body as its own act (document 12) |
| `give the gloves to the townie` | the stock shell command | a physical act with an owner and a witness (document 15) |
| drying the damp matches | nothing changes: wet is a flag on a row | wetness as grams of water that heat drives off (document 08) |
| bare `pry bin` from the rear cabin | binds the **forward** bin: *"too far away to pry from here"* | what is in front of you wins (document 04 §3.3, silent disambiguation) |
| `search the pilot` · `dig the drift` · `search the tail cone` · `bandage my arm` | *"You go through the the pilot"* · *"a leather gloves"* · *"a sleeping bag and a snowshoes"* · *"around the you"* — articles glued onto names that don't take them | one fix in the phrase renderer (names that already start with an article, and plural names), worth doing before anyone reads a render for voice |
