# 02 — The experience: what a run of Whiteout is like

> **Status: reviewed with Andrew 2026-09-17 — see the review log; the sample week is regenerated after block 4** The document to react to: a sample week in prose first,
> then the reference behind it. **Architecture counterpart:** none of its own — this is the read-through
> of every system's document, and each claim points at the document that owns it.
> **Sources:** the nine design passes in [`../investigation/design/`](../investigation/design/)
> (events-and-escalation · time-and-stakes · fire-and-shaping · rescue-graph · moral-social-layer ·
> players-and-kit · living-rooms · grammar-guide · phrasing-corpus) and the
> [provenance audit](../investigation/design/00-provenance-audit.md) · the umbrella
> [GDD](../scenarios/whiteout/GDD.md) · the valley in
> [`../investigation/world/map.md`](../investigation/world/map.md) and
> [`report.md`](../investigation/world/report.md) · the render read of the nine built rooms
> ([`../review/render-2026-09-07.md`](../review/render-2026-09-07.md)) · `game/world/help_entries.py`
> (the grammar taught today) · the decided player view (the plan's Part J).

**The three marks, used on every beat and every row:**

| mark | means |
|---|---|
| ✅ | **built and playable today** — you could type it into the running game this afternoon |
| 📐 | **designed** — written down somewhere, cited, not built |
| ◌ | **not yet fleshed out** — the sentence after it says what it needs |

Nothing designed is allowed to read as built. Where the sample week needed something that does not
exist, the mark says so in the margin rather than in a footnote you could miss. **Part 8 is the same
list gathered in one place.**

---

## 2. Provenance — whose design this is

### Andrew's decisions (quoted, with dates)

**The concept (2026-09-07, 2026-09-16).** An "ontologically sufficient" MUD: "a user, or LLM when we
capture activations and analyze behavior, can do whatever is reasonable (if they want to cut something
they can break a mirror and get a piece of glass, then cut open a cushion for the stuffing and then
burn it)." "Anything reasonable": "want to take an axe thing and chop the log up then sure. want to
dig dirt then yeah. find a rock, maybe some clay, whatever." It is "a model world we use for serious
academic research" AND "a revolutionarily new MUD type for my MUD friends on Discord who will love to
play in a world where you can do anything within reason to solve the survival game." "This is not a
small project, it is a massive side project that will mostly run in overnight sessions as agents
systematically 'flesh out' the world." "We barely even touched this."

**Never a menu (2026-09-16).** "The agent is not given a set of options to choose." "Giving options
changes how it thinks, it constrains it to those options." "You do not give other options, the only
time you ask the user anything is if what object or action they can do is ambiguous (two cans in a
scene it will ask 'which can do you mean?')." "No you do not have numbered nouns." "If you give
options for like 'pick up can' and then you list all the cans in the reachable area it would just give
away all the puzzles." "Any feedback needs to be clarification based and not giving options, we can
have some feedback reminding them of the grammar help system." "If the system recognizes they need to
use another word then it would clearly understand that word."

**The world and the run (2026-09-07).** Verbatim: "we dont want half thought rooms we want living
interesting rooms - but at the same time the things will facilitate completing the various rescue
goals (fix radio, use radio, then survive until help arives so find food, find warmth, etc) and there
should be several ways of doing things - you could find a lighter if you look hard enough but can
light it in various other ways, and of course a lot of things have time it takes, like a MUD you will
see 'attempting to X' with appropriate messages that fire." In short: living, interesting rooms, not
half-thought ones; things facilitate the rescue goals; several ways of doing things; timed actions
with feedback; decisions across the moral spectrum (eating the pilot, stealing, hitting,
killing); fire is made *somehow* — rubbing sticks fails and the game says so, a bow drill works, a
lighter lights tinder, not a branch; "state the act, not the aim" (`shake thermos`); agents are given
the grammar guide up front; heavy snow starts at some point; events are planned; the game runs roughly
a week, rescue can come earlier, it can run longer until food runs out, **no hard time barriers** —
"increase the things that cause death"; no set arc; each player starts with a different
clothing/injury/pockets draw; luggage has contents; clothing affects warmth loss; players can sleep;
the clock moves forward if all agree and events can interrupt it.

**Decided 2026-09-16.** The whole valley (all fifty outdoor zones) is in the first complete run. The
plane is a Cessna 206-class single with a four-seat interior (1A/1B/2A/2B + the right seat; a hat
shelf, a cargo net, a jammed cargo door). December; no bear (wolves and a wolverine). The kid is in —
a party of four or five. No lethal-consent gate: violence resolves with real physics. `use X on Y`
resolves silently as the real operation. An agent sees exactly what a human sees. The look is a title
line, the prose, who is here, one `Exits:` line (compass outdoors, fore/aft/out inside) and **no item
list**; descriptions are composed from state. The watch rule: one acting player holds the clock at 1×
and the others wait for the next event. Moral tags and other action tags are ontology fields. The
pilot dies within the first day; nobody can talk to him (no language model behind him) — scripted
things only: moaning heard only in the cockpit, maybe a line.

### Proposals (Claude) — everything else here

**The sample week in §4b is mine.** Andrew decided the pieces (the draw, the pilot, the week, the
ladder, the consensus clock, no menus); the *particular* seven days — which beats land when, who dies,
what the party argues about, the exact command lines — are my assembly of those pieces into one
readable run. **No part of the week is a decision.** It exists so that the shape of a run can be
reacted to as a whole, and so that the gap between the design and the build is visible in one read.

The reference in §4c is the nine passes' content reorganised, not re-decided: the ladder's numbers,
the event deck, the five rescue channels, the seven fire methods, the warmth/water/food/injury paths,
the dilemma set, the activity feedback grammar, the agent protocol. Each carries its source. Per the
audit, **every number in this document is a proposal and tunable**, including the temperatures, the
day indices, the durations and the distances.

---

## 3. In one paragraph

You wake in a broken Cessna in an unnamed valley in interior Alaska, in December, with five hours of
daylight and a search grid that is looking somewhere else. You are one of four or five people who each
wore different clothes that morning, carry different things in their pockets, and were hurt differently
by the landing. Nobody tells you what to do and nothing offers you a list: you type physical acts in a
grammar the game teaches once — `cut the cover off the seat with the multitool`, `put the branch on the
fire`, `tie the wire to the antenna base` — and the world answers with physics, including when it says
no. The clock never stops; the cold gets worse every day on its own schedule; the pilot moans in the
cockpit and dies within the first day, and his body stays where he died. You keep a fire, or you learn
what it costs not to. Somewhere in the week a plane crosses the valley and either sees your smoke or
does not. You are rescued, or you walk out to the cabin the chart promises, or you die honestly of cold
and hunger, or the week ends with you still going — and the log knows exactly what each of you did, and
who could see it.

---

## 4. The design

### 4a. The premise, in one page

**Who you are.** Five authored slots; the run seed deals them to the players and permutes who gets
which, so nobody is always the unlucky one. 📐 (`players-and-kit.md` §1; the slots and their kit are
built ✅ — `game/world/scenarios/whiteout/characters.py`.)

| slot | seat | wore | pockets | the crash left them |
|---|---|---|---|---|
| **the guide** — flying up to a lodge job | right seat | down parka, wool base layer, insulated boots, gloves, wool hat | pocketknife, lighter, chocolate, a compass on a lanyard | bruised ribs — bending and lifting hurt |
| **the townie** — home from a court date | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves | phone, wallet, gum, keys, earbuds | a cut forearm, bleeding |
| **the nurse** — home leave | 1B | fleece, hiking boots, scarf, thin gloves | a med pouch, lip balm, hair ties, a pen | a sprained ankle — walking costs double |
| **the salesman** — a mine supply run | 2A | wool overcoat, dress shoes, leather gloves | a metal lighter, a hip flask, reading glasses, a notebook | concussion — fatigue faster, confusion the first day |
| **the kid** — 16, visiting family | 2B | ski jacket, snow pants, snow boots, mittens | phone, candy bar, a multitool, sunglasses | shock — fine physically, slow to act on day one |

What you wore that morning is the single largest determinant of the first night. That is the point: a
party of four identical survivors is a chore list; four people with one good coat between them is a
question with a right answer, and giving the coat away is a real act.

**Where.** An unnamed side valley in interior Alaska. The mail plane came in from the northeast over a
low ridge shoulder, clipped the spruce crowns, shed its right wing into the trees, bellied down the
slope and slid southwest across a frozen muskeg fringe, shedding the tail. It stopped at the muskeg's
east edge. West, the muskeg opens onto a lake; the lake drains south into a creek; from the creek's
east bank an old blazed trapline climbs to V. Holt's homestead — the cabin the pilot's chart promises,
2.4 km of travel away, a commitment that eats half a day's light round trip. 📐
(`../investigation/world/map.md` §2–3.)

Nine zones of the crash cluster are built and readable today ✅ — cockpit, mid cabin, rear cabin,
outside the nose, the top of the fuselage, the torn tail opening, the debris trail, the severed tail
section, the treeline (`game/world/scenarios/whiteout/zones.py`). Fifty outdoor zones across ten
regions — muskeg, lake, north wood, strike path, ridge, birch stand, creek, beaver pond, trapline,
homestead — are designed room by room 📐 (the design of record is
[`01-premise-and-world.md`](01-premise-and-world.md); the zone-by-zone detail is still in
`../investigation/world/rooms.md`), and Andrew decided on 2026-09-16 that all of them are in the first
complete run. Here they are simply the country the week walks through.

**When.** December. Five hours of daylight. The GDD's premise, unchanged: off-route winter crash,
wrong search area, dead radio, weak beacon, unstable wreck (GDD §6). The first overflight of the week
is heard, not seen, and it is in the wrong area — the search is looking where the flight plan said the
plane would be, which is not where it is. Rescue is not a timer that expires; it is a signal that has
to be in the air at the moment someone passes, and the passes get rarer as the grid moves north.
📐 (`events-and-escalation.md` §2, "the search" row.)

**What makes it a week and not a day.** Nothing refuses you and nothing locks. Instead every line of
the ladder is a number that hurts more each day: the ambient cold falls, the storms come and go, the
snow load buries the doors, the fuel radius walks away from camp, the rations run out, untreated
wounds infect, sleep debt slows you down, the search grid moves away. "A party that does everything
right can last past day ten; a party that does nothing dies by night three." 📐
(`events-and-escalation.md` §2 — the numbers are proposals.)

---

### 4b. A sample week

> **Provenance:** the beats below are my proposal (Claude), assembled from Andrew's decisions and the
> nine passes. The commands are real lines in the taught grammar; the ones marked ✅ resolve in the
> game today, and where the game already has words for something I have used its own words.
>
> **This is one screen — the guide's.** The other three players are typing at the same time on their
> own screens; what reaches this one reaches it the way the game sends it, by perception band. Times
> are game time.

#### Day one — the day the pilot dies

**08:58 · the cockpit · first light is still an hour off**

```
The cockpit
Shattered instruments and a crazed windscreen; cold air knifes in off the snow.

The pilot is slumped against the forward bulkhead. A field radio sits dark in its cradle
beside him. Below the cradle are a crumpled avionics panel and a small fire extinguisher in
its bracket. Down in the footwell, against the rudder pedals, are the pilot's worn leather
flight bag and a capped steel thermos. Across the cockpit floor are a flight manual splayed
face-down and a sectional chart folded to this valley.

Exits: aft, out
```

*✅ The prose, the objects and what is loose versus hidden are built and read exactly like this
(render 2026-09-07; the italic line and the object sentences are the composer's, from state). You are
alone up here because that is where the draw put you: the guide rode the right seat, and the other
three woke in the cabin behind. ✅ The seating, and everything each of them is wearing and carrying,
is built (`characters.py`).
📐 The title line, the people line and the single `Exits:` line — Andrew's decided look, 2026-09-16;
the model is in [`03-the-player-view.md`](03-the-player-view.md). ◌ "First light is still an hour off":
there is no daylight model, so the game cannot yet say what time of day it is or darken a room.*

```
> examine the pilot
the pilot — His flight jacket is zipped to the chin, one hand still resting on the radio
cradle. His breath is shallow and his lips are grey. The pilot wears a flight jacket.

> search the pilot
You go through the pilot: a lighter.
```

*✅ Both resolve today, and the search really does turn up his lighter (the live line doubles the
article — Part 8). 📐 The changed examine line
— he is alive at first light and fading — needs the pilot's clock (`time-and-stakes.md` §4), because
today the table simply starts him dead: "He has stopped breathing … It's lifeless."*

```
From the cockpit, a low sound: the pilot, moaning, somewhere under the noise of the wind.
```

*📐 Andrew, 2026-09-16: "nobody can talk to him (no language model behind him), scripted things only
— moaning heard only in the cockpit, maybe a line." The sound is a propagated event audible in this
zone and nowhere else ✅ (the propagator and the perception bands are built); the pilot's process that
emits it is not.*

**09:20 · aft, and the kit gets split**

```
> go to the mid cabin
You make your way to the mid cabin.
> go aft
You make your way to the rear cabin.
> open the aft bin
The aft overhead bin is buckled in its track — fingers won't shift it. Something to lever
might.
> pry the aft bin with the multitool
You get the multitool into the seam and heave; the aft overhead bin gives with a shriek and
hangs open.
> search the backpack
You go through the backpack: a canteen of water and a spare shirt.
```

*✅ Live, in exactly that wording — I ran it. The middle exchange is the whole feedback rule in one
sentence: the game answers with the physics of why, not with a list of verbs, and the player works out
the rest. ✅ The reveal of contained things is the built discovery rule (DR-24): what is inside a
thing stays absent from the room prose until somebody searches, opens or digs for it — which is also
why the game can never list what is reachable without giving the wreck away. ◌ One live wart: bare
`pry bin` from the rear cabin binds the **forward** bin and answers "too far away to pry from here" —
the ambiguity resolves by name, not by what is in front of you.*

```
The townie says, "My arm's still going. It's not stopping."
The nurse says, "Sit down. Give me the shirt."
> take the shirt
You fish the spare shirt out of the backpack.
> tear the shirt
You worry at the spare shirt and tear it into long ragged strips.
The nurse binds the townie's forearm with a strip of cotton.
```

*✅ Both commands resolve in that wording — cotton with no seam to open goes to strips — and `wrap X
around Y` (which `bandage my arm` folds onto) is live. ✅ Speech carries by range
(say/whisper/call/shout), and a co-player's act reaching your screen as a third-person line is what
the propagator is for. 📐 The wound it is for is real state on the townie's character today ✅, but
bleeding that costs him hydration and warmth per tick, and a dirty binding that can infect after N
hours, are designed and unbuilt (`time-and-stakes.md` §4) — so today the bandage is a nice sentence
about nothing.*

```
> press the wound
I don't understand 'press'.
('help grammar' shows the forms.)
```

*📐 That is the decided shape of a failure: a clarification and a pointer, never a suggested verb —
"if the game could suggest the word it already knows it" (Andrew, 2026-09-16). `press` is a genuinely
missing verb, on the list the agent phrasing samples voted for (`phrasing-corpus.md` §3). ◌ What the
shipped code actually answers today is the opposite of the decision, and it is worth seeing in full:
"I don't know how to 'press'. Did you mean wear? … 'help grammar' shows the shape; 'help verbs' lists
the verb families … (Verb families — cutting & shaping: cut, tear, break, bend…)" — a wrong guess, a
verb list, and a second verb list. That is the queued correction (`00-provenance-audit.md` §5), not
the design.*

**10:40 · the treeline · the first fire**

```
The treeline
The first spruces close overhead; the wreck is a broken shape back through the falling snow.

The first spruce stands close enough to touch, boughs bent white. Under the spruces are two
snow-crusted deadfall branches and a wind-combed fist of dry grass.
Exits: south-west, north
```

*✅ Built and rendering today, down to the fist of dry grass.*

```
> take a branch from the deadfall
You take the deadfall branch.
> light the branch with the lighter
The flame licks at the bark and blackens it, but a wrist-thick branch won't take from a
flame this small. Something finer would.
```

*📐 The second line is the honest failure Andrew walked in conversation — "a lighter lights tinder,
not a branch". The ignition check is additive (source strength + receptivity by material and **form
thinness** + air − wet − wind) and every term of it shows in the failure line
(`fire-and-shaping.md` §1–2). ◌ **What the game says today is the opposite**: I ran it, and
`light the branch with the lighter` answers "The deadfall branch catches with a small eager flame — a
fire, at last." `light` is a one-shot operation with no receptivity behind it, so the single most
characteristic moment in the design — being told, physically, why your idea didn't work — is the one
this beat cannot do yet.*

```
> shave the branch with the multitool
You set to work shaving the branch down.
  Curls of pale wood drop into the snow.
  The branch narrows; your hand is cold on the blade.
You have a handful of shavings and a thinner stick.
```

*📐 Two designed things at once: the **shaping family** (`carve`/`split`/`shave`/`notch`/`string`/
`bundle`, outputs are forms, mass conserved — shavings are a by-product that happens to be tinder;
`fire-and-shaping.md` §4) and the **attended activity** (a start line, two or three state-driven tick
lines, a completion line; `time-and-stakes.md` §3). ✅ The parser already accepts the `into <form>`
shape and binds form pseudo-nouns in that slot, so `carve the branch into a spindle with the knife`
parses today — there is simply no operation behind it yet.*

```
> light the shavings with the lighter
The shavings take at once, a fast bright flame that will not last.
> put the thin stick on the fire
You feed the thin stick in. The flame climbs into it and holds.
The fire is burning.
```

*📐 Fire as a **process object** with a stage ladder — unlit lay → catching → burning → established →
embers → dead — with a fuel load consumed per tick by material burn rate into ash, heat output by
stage, and stage changes that interrupt nearby activities (`fire-and-shaping.md` §5;
`time-and-stakes.md` §4). ◌ There is no fire entity in the world today. `burn` and `light` consume a
thing and narrate it beautifully — "The loose fabric catches, curls, and burns down to ash, acrid
black smoke coiling upward." ✅ — but nothing goes on burning after the line prints, and the word
"fire" has nothing to bind to: type `put the branch on the fire` in the wreck today and the parser
finds the only fire-ish noun in the world, which is the **fire extinguisher** in the cockpit, and
tells you it is too far away. That one line is the clearest possible statement of what step 3 is for.*

**14:10 · the cockpit · the pilot**

```
The pilot says, "Tell Val — " and stops.
The pilot has stopped breathing.
```

*📐 Andrew, 2026-09-16: he dies within the first day, scripted, maybe a line. What the line carries —
whether it is a clue path or only a person dying — is [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md)'s
call, not this document's. ◌ The scripted clock that ends him, and the lucid-window rule that decides
whether tending him buys a line at all, are not built. ✅ His body persists as an object where he died,
and can be searched, examined and covered.*

```
> cover the pilot with the blanket
```

*✅ It resolves today, and how it resolves is the interesting part: `cover X with Y` folds onto `wrap`
and answers "You bundle the wool blanket around the the pilot; it'll hold the warmth in." The world did
the physical thing correctly and means something slightly wrong — he is past holding warmth in. ◌ That
is the gap the pilot's document has to close: covering a body is an act of reverence, and the wrap
tier has no idea (the doubled article is real too — Part 8). 📐 Either way the act is logged with its
axes — target: corpse, harm: none, witnessed by: the nurse — as an observation in the event log and
nowhere else; nothing in the game reads the tag, and there is no meter (`moral-social-layer.md` §1,
rule 7).*

**16:50 · the rear cabin · night, and the first consensus sleep**

```
The nurse says, "There's nothing else we can do in the dark. Sleep."
> sleep
You lie down in the drifted corner under the blanket, the fire banked to a red eye.
Everyone is resting. The night runs on.
  The cold deepens; the fire settles to embers.
```

*📐 The consensus advance: when every connected character is resting or waiting, the heartbeat runs at
**20×** until the earliest wake time or an interrupting event (Andrew, 2026-09-07; DR-14a;
`time-and-stakes.md` §8). ◌ None of it exists: today `sleep` is an unknown verb ("Did you mean
examine?"), and the clock has one rate.*

```
Wolves, somewhere north, two of them answering each other.
You are awake.
The kid says, "was that"
The kid says, "was that wolves"
```

*📐 An event with loudness above the interrupt threshold breaks the 20× advance and wakes the party
(`time-and-stakes.md` §8; the deck's wildlife row: "wolves howl the second night, tracks circle the
wreck by the fourth, they test a lone traveller on the ice — a real danger, never a scripted kill",
`events-and-escalation.md` §4). ◌ There is no event deck and no escalation calendar.*

*The watch: one player staying up to feed the fire holds the clock at 1× for everybody — Andrew's
rule, 2026-09-16: the others wait for the next event and do something else meanwhile. In this run the
guide takes the first watch and the other three sleep through to grey light.* 📐

#### Day two — the snow starts

```
Snow again, heavier than yesterday, and it has been falling all night.
> dig the drift
You burrow into the snowdrift, snow packing your sleeves: a leather gloves.
> give the gloves to the townie
```

*📐 Andrew's fixed beat — "heavy snow starts at some point" — placed on day 2–3
(`events-and-escalation.md` §2, storm bands): from here on the snow load line of the ladder makes the
entrance a thing you keep, every morning, at the cost of sweat you pay for later as cold. ✅ The dig
and its find are live in that wording, and the gloves in the drift are exactly the kind of thing the
draw makes matter — the townie is the one who boarded without any (and yes, the line really does read
"a leather gloves": see the prose notes in Part 8). ◌ The drift does not come back, because there is
no weather; and `give` today is the stock shell command, not a physical act with an owner and a
witness (`moral-social-layer.md` §2).*

```
> read the chart
The valley, in the pilot's pencil: the creek winding south, a spot height, and — three miles
east, up the feeder stream — a small square drawn by hand, marked 'V. HOLT — CABIN, WOOD
STOVE'. Underlined once.

> read the manual
Checklists, frequencies, weight tables. The emergency section is dog-eared: signal fires burn
better wet-green over a hot core; keep casualties off the ground. Pencilled inside the cover,
underlined twice: 'GUARD — 121.5'.
```

*✅ Both are live, verbatim. This is the whole information economy in two lines: the chart seeds the
walk-out, the manual seeds the beacon and the signal fire, and the party cannot fund all three plans
at once. That argument is the game (`../investigation/world/report.md` §1).*

```
> go to the debris trail
You can't get to the debris trail directly from here — it's to the northeast; the torn tail
opening is the way through.
> go to the tail opening
> go to the debris trail
> search the survival duffel
You go through the torn survival duffel: a fishing kit, a mosquito headnet, a ration tin, a
ration tin and a waterproof matchbox.
> examine the matchbox
waterproof matchbox — The irony is complete: the waterproof case cracked, and the strike-
anywheres inside drank the snowmelt. Dried out — slowly, by a fire — they might live again.
It's soaked.
```

*✅ Live, verbatim, joke and all. 📐 Drying them is the designed fire bootstrap: wet is grams of water
in a thing, and heat drives the number down (`time-and-stakes.md` §4). ◌ Today wet is a flag on a row
that nothing changes, so the matches stay ruined forever and the second of the seven fire methods is a
promise.*

*The day goes on fuel and water: armfuls from the treeline, snow melted in the thermos by the fire.
📐 The melt path is designed with its trade-off — eating snow is always possible and always costs
heat, "a redirect with a consequence, not a refusal" (`rescue-graph.md`, WATER). ◌ Hydration and the
heat cost of a mouthful of snow are numbers that do not exist yet.*

#### Day three — the plane

*Just after midday, in the flat light between two storms.*

```
An engine, small and high, somewhere west.
```

*📐 The designed rule for this beat is that it is never a silent no-op: the drone is audible
**valley-wide**, with a bearing, in every exterior zone and muffled inside the wreck and the cabin, so
that a party which allocated its day elsewhere hears exactly what that cost, in the moment
(`../investigation/world/rooms.md`, timed beats). ✅ The propagator and the perception bands that would
carry it are built; ◌ nothing schedules it.*

```
The kid says, "the fire the fire is inside"
> take the oil
> go west
```

*📐 The run of that minute: the oil is in hand and the lake is a twenty-minute walk west over
unbroken snow. The pass lasts ninety seconds. The fire is in the wreck, where it kept them alive all
night, and not on the ice, where it would have been seen. Nobody did anything wrong — that is the
design working, not failing (`../investigation/world/report.md` §1). ◌ Today the walk-edges stop at
the treeline: the ice, the twenty minutes and the smoke column all wait on the fifty outdoor zones.*

```
The engine fades north-west.
```

#### Day four — the blow

*A two-day storm, near-whiteout. Travel shuts: visibility bands collapse, the lake crossing and the
knob become gambles, the sheltered routes keep working, and yesterday's broken trail fills in.* 📐
(`../investigation/world/map.md` §5.)

```
> set the snare at the willows
```

*📐 The country food path — snares, ptarmigan, grubs, bark — priced in knowledge, tools and daylight
(`rescue-graph.md`, FOOD). ◌ `set` is a missing verb, the snare is a missing object, and no yield is
authored: what a snare line actually returns over a week is undesigned, and §6 asks about it.*

```
In the night, something heavy goes through the cache. In the morning the flour is scattered
across the snow and the last ration pack is gone.
```

*📐 The wolverine — "fearless; the classic camp thief" — one of the deck's wildlife events, telegraphed
by sign first (`events-and-escalation.md` §4). Andrew decided there is no bear: the wolverine and the
wolves are the antagonists.*

#### Day five — the question

*Clear-cold behind the storm. −24 by day, −32 at night on the drafted ladder. The rations are gone;
what is left is a tin of coffee, flour trodden into the snow, and a plastic cooler the kid dug out of
the wind-packed drift on the debris trail yesterday — a family's frozen salmon, three kilograms of it,
riding home in the freight.* ✅ *(The drift, the cooler and the salmon are all real objects today; the
cooler is shut, inside the drift, and takes a dig and an open to reach — the anti-easy rule.)*

```
The kid says, "that's one fish"
The nurse says, "One fish, four of us, and it's day five."
The townie says, "and there's him"
The nurse says, "Say what you mean."
The townie says, "I mean the pilot. I'm not going to pretend I didn't think it."
```

*📐 The moral layer's first rule: every dark option has a competitive honest alternative priced in the
same math — and the pressure that makes it a dilemma is hunger and cold as **numbers**, not as flavour
(`moral-social-layer.md` §1 and §3, the `pilot_body` row). What the engine records here is only what
happened in the world and what was said: **speech acts, in order, with who could hear them**. No
intent is logged, because nothing was done. Nothing in the game reacts; there is no meter. ◌ Hunger
is not a number today, so today this conversation is a curiosity rather than a decision.*

*Nobody touches the body on day five. They eat the salmon, all of it, and it buys them a day.*

#### Day six — the antenna, and what the guide does

```
> pry the tail cone with the multitool
You get the multitool into the seam and heave; the crushed tail cone gives with a shriek and
hangs open.
> search the tail cone
You go through the crushed tail cone: a cargo net, an emergency locator transmitter, a guitar
case, a sleeping bag and a snowshoes.
> examine the elt
emergency locator transmitter [ELT] — The g-switch tripped on impact — ARM light pulsing,
faithfully shouting on 121.5 — but its antenna ends two inches up in bright sheared metal. It
is screaming into its own throat. It needs a real antenna, and wire enough to reach one.
> take the elt
> tie the wire to the elt
You lash the coil of copper wire to the emergency locator transmitter and cinch it down — it
holds.
```

*Three walks later, up on the spine with the beacon under one arm:*

```
The top of the fuselage
Wind scours the bare aluminium spine. A torn metal base juts where the antenna should be, a
short cable hanging loose and rimed with ice.
Exits: down
```

*✅ Every line of that resolves today, in that wording — I ran it. The jammed tail cone and what rode
in it, the sheared ELT, the coil of copper wire out of the avionics panel, the torn antenna base on
the spine, and `pry`, `search`, `tie` and the climb are all live. So is the trail of clues, and it is
the kind of thing the world is supposed to do: the beacon's own examine tells you what is wrong with
it and what it needs, and the roof — a walk away, in its own look — has the base it was sheared off. Nobody wrote that down for you. 📐 What is missing is the other half — the
beacon channel's arithmetic: a rigged antenna plus elevation feeding rescue confidence, and 121.5
being a frequency that something overhead can hear (`rescue-graph.md`, BE FOUND; the ELT and radio
state machines are P5 content).*

```
The nurse says, "Hold it against the base. I can't do both."
> tie the cable to the antenna base
The nurse is holding the elt steady while you work.
```

*📐 The first-class interdependence the GDD asks for (§16): one holds or raises while the other
works. ◌ There is no mechanism today by which one character's held position changes what another can
do — the co-op is real but parallel.*

*Late afternoon. The nurse and the kid go down to the treeline for the day's wood. The townie is
asleep with a fever. The guide is alone in the wreck with the body.*

```
> butcher the pilot with the knife
```

*📐 The act resolves. There is no gate, no confirmation, no consent flag, and no refusal: Andrew,
2026-09-16 — "no lethal-consent gate; violence resolves with real physics". The world changes: the
body's state becomes butchered, meat is minted with its own raw-meat illness risk, blood is on the
tool (provenance), and the event log records the transition, the zone, the world-time, and **who could
perceive it — nobody**. Witnessing is spatial: an act is priced socially only if someone could see it
(`moral-social-layer.md` §1, rules 3 and 5). ◌ `butcher` is a missing verb and the event log does not
exist yet.*

```
The nurse says, "What's in the pot?"
> say there was more fish in the cooler
```

*📐 The first of the design's two lie categories: a **stated falsehood**, checkable against world state
at the moment it is logged, because the cooler is empty and the engine knows when it was emptied and
by whom. It is logged beside the act, not scored, and nothing in the game reacts to it
(`moral-social-layer.md` §1, rule 4). Whether anybody finds out is up to the party and a search.*

#### Day seven — the window

```
The wind drops in the night and the cold comes down after it. Before dawn the sky north is
a slow green fire.
```

*📐 The aurora, once, when the overcast tears open — "the beauty and the temperature drop arrive
together, and the design says so in the numbers" (`../investigation/world/rooms.md`, the aurora). A
free co-op beat: a split party sees the same sky in the same minutes.*

```
> put the oil on the fire
Black smoke rolls up off the ice, flat-bottomed and slow, and leans north.
```

*📐 The stay-and-signal channel, whose scarce resources are fuel logistics and wind engineering: the
quart of engine oil and the tire make a black column; green boughs make white (`rescue-graph.md`, BE
FOUND). ✅ The oil quarts and the jerry can are real objects and `take the oil` / `open the oil` are
live. ◌ The rest is the same missing noun as on day one — there is no fire to pour it on.*

```
An engine — bigger, lower, and it does not fade.
The helicopter comes up the lake line and turns over the smoke.
```

*📐 Rescue is additive confidence plus a weather window, with at least four winning combinations and
no single object required by all: the beacon has been up since yesterday, the smoke is in the air, the
sky is clear, and the sum crosses the threshold (GDD §37–39; `rescue-graph.md`). ◌ The confidence
arithmetic, the weather window and the endings are designed and unbuilt.*

**The run ends with four people alive, a fever the nurse can finally treat, two black fingertips on a
hand that had no gloves on day one, the pilot where he died with the day-one blanket back over him, and
a conversation on the flight out that nobody in that helicopter is ever going to have.** 📐 *The recap
reads the log and can name every one of those things, because each was a world-state transition with a
time and a witness list — not because anything scored them.*

---

### 4c. The reference

#### The week's ladder, day by day

> **Provenance:** Andrew's brief (2026-09-07) — no hard time barriers, increase the things that cause
> death, roughly a week. The **numbers and the day indices are my proposals** and are tunable by probes.
> 📐 `events-and-escalation.md` §2. ◌ Nothing in this table is on the clock today.

| what rises | day 1 | day 3 | day 5 | day 7 | day 10 | how it kills |
|---|---|---|---|---|---|---|
| **cold** (day / night) | −12 / −20 °C | −18 / −26 | −24 / −32 | −30 / −38 | −34 / −42 | without fire + insulation + shelter the core drops below the floor |
| **storm bands** | light flurries | the first heavy snow (a day) | a two-day blow, near-whiteout | clear-cold behind it (aurora, brutal night) | the second storm | wind chill multiplies exposure; visibility collapses; travel and signals shut |
| **snow load** | ankle | knee at the doors | the cargo door needs digging out each morning | the wing is a hump | — | work costs sweat; the entrance must be kept; wood gets farther |
| **fuel radius** | treeline | the near wood is picked clean | the north wood (a walk with the sled) | — | — | daylight and sweat per armful rise |
| **food** | rations | the freight (flour, coffee) | the country, or the pilot | — | starvation math | calorie debt → weakness → cold |
| **injuries** | a cut | infection risk rises | fever costs warmth and water | gangrene without care | — | a body that can't work can't stay warm |
| **fatigue** | — | judgment: slower activities | mistakes: the fire goes out on watch | collapse | — | sleep is a resource with a price |
| **the search** | first overflight, wrong area | a plane crosses the valley (seen only if a signal is up) | the search shifts north | scaled back | occasional traffic | rescue needs a signal in the air at the moment of a pass |
| **the pilot** | moans in the cockpit; dies within the day | a body | — | — | — | the moral question starts on day one |

**The endings** 📐 (`events-and-escalation.md` §3; the recap is [`21-endings-and-recap.md`](21-endings-and-recap.md)'s):
**rescued** (a signal in a weather window, confidence over threshold) · **walked out** (Holt's cabin —
the stove, a radio, a snowmachine; "we can outlast this" is rescue confidence too) · **dead** (cold,
starvation, ice, CO in a closed fuselage, the wreck sliding; the run ends when the last player dies and
the bodies persist) · **still going** (no cutoff; the ladder guarantees an ending within about two
weeks for any party, because cold and food only get worse). §6 asks whether all four stand.

#### The events, by category and when they fire

📐 `events-and-escalation.md` §4–5. An event is a scheduled process with preconditions, a day and hour
window, seeded jitter, effects, narration by perception band, and a flag for whether it interrupts. The
heartbeat checks the due list each tick; fired events apply their effects through the one mutation path,
route their narration by band (the wolves are heard from the treeline, seen from the ice) and, if they
interrupt, wake sleepers and break activities. All draws come from the run seed, so a run replays the
same week. ◌ None of it is built; the deck's first version is an open question (§6).

| category | what fires |
|---|---|
| **weather** | first flurries · the heavy snow begins (Andrew's fixed beat, day 2–3) · a wind shift (the breach faces it now) · whiteout · a clear-cold night (aurora, −40) · a sun break (the mirror window) · thaw-refreeze (overflow, black ice) · the second storm |
| **wildlife** (all telegraphed by sign first) | ravens scout the wreck · a fox on the tussocks · **the wolverine raids the cache** at night · **wolves** howl the second night, circle by the fourth, test a lone traveller on the ice · a lynx print, never the lynx · ptarmigan flush · a hare in the snare · a moose on the trail (a wall of meat that kills the careless) · an owl · a snow load off a bough onto whoever stands under it. **No bear** (Andrew, 2026-09-16) |
| **search & rescue** | the day-1 overflight in the wrong area (heard, not seen) · the day-2/3 plane crossing the valley (seen only if a signal is up) · a helicopter on a clear day at high confidence · a snowmachine on the lake at dusk · a distant chainsaw (the upriver village exists) |
| **the wreck** | fuel drips and pools under the wing · the fuselage shifts with a groan and the door jams · a window pane falls in · the tail slides further down the scar · the battery freezes · the extinguisher's bracket lets go · ice seals the cargo door overnight |
| **bodies** | the pilot's moans (cockpit only) and his death within the first day · a wound infects · frostbite whitens a finger · snow blindness · hypothermia confusion (messages, never command hijacking) · dehydration headaches · the hunger stages |
| **camp** | the fire dies on an untended watch · the drift buries the entrance · the ice booms at night · a bough dumps its snow on the lean-to · the creek overflows the crossing · tracks in the morning that weren't there |
| **mail & freight** (found, not fired) | the postmarks · the parcel addressed to Holt · the child's letter · a parcel of candles · dog food in the freight |

#### What players can do — the forms

✅ **Built and taught today.** Seven shapes; everything else is the tolerance layer folding real
phrasings onto them (particles like `pick up` and `cut open`, synonyms, plurals, body parts, `it`, and
the dropping of intent). 📐 The `help grammar` text becomes the forms with one example each and the
three rules, and `help verbs` is deleted — a verb list is a menu (Andrew, 2026-09-16); ◌ the shipped
help still carries the old text.

| shape | example | status |
|---|---|---|
| `VERB thing` | `examine the radio` · `break the bottle` | ✅ |
| `VERB thing WITH tool` | `cut the cushion with the shard` | ✅ |
| `VERB thing RELATION thing [WITH tool]` | `put the branch on the fire` · `tie the paracord to the frame` · `take the wire from the panel` | ✅ |
| `VERB thing INTO form [WITH tool]` | `carve the branch into a spindle with the knife` | ◌ the slot is built — the parser binds form pseudo-nouns after `into` — but no verb yields a form yet, so `carve` is still an unknown word |
| `GO place` | `go to the cockpit` · `go aft` | ✅ one walk-edge, instant ("You make your way to the rear cabin."); 📐 durations, compass directions and the `Exits:` line |
| `say / whisper / call / shout …` | `shout for help` | ✅ by range |
| `VERB thing, then VERB thing` | `take the shard and cut the cover` | ✅ |

**The three rules the guide states out loud** 📐 (`grammar-guide.md` §2): state the act, not the aim
(`shake thermos`, not `shake the thermos to see if there's coffee in it`) · name things the way the room
names them (`examine` shows what you can name, including parts) · tools are anything with the capability
(anything with an edge cuts; anything rigid and long levers; anything long and flexible ties).

**How it says no** — a clarification or the physics, never an option 📐 (`grammar-guide.md` §3; Andrew,
2026-09-16). Unknown word → `I don't understand 'X'.` plus, once, a pointer to `help grammar`, and the
word is logged so the next pass adds the synonym. A thing it can't see → `You don't see any 'X' here.`
without naming what *is* here. A verb that doesn't fit → the physics: *"The blade finds no seam — the
bolt is bolted through the frame."* ✅ (live: *"You bear down, but the glass shard won't bite into the
bolt. You'd need a keener edge."*). Two things match → `Which can do you mean?` and nothing more.
◌ The shipped code still gives verb nudges, a "but you could…" redirect and numbered menus; that is the
queued correction, not the design.

#### Fire, seven ways

📐 `fire-and-shaping.md` §6. Each gated by a different scarce resource, so none dominates. ◌ None is
built: there is no fire entity, no ignition model and no shaping family.

1. **Lighter** (the pilot's pocket ✅) — flame → tinder → kindling → fuel. Fails on a branch straight
   from the flame, on wet tinder, on wind without a windbreak.
2. **Matches** — the soaked box ✅: dry it by a fire or on your body (a process), then strike.
3. **The flare** ✅ (object) — ignites anything, once, loudly; spends the visual-signal resource.
4. **Battery + wire** — pry the cowling, the aircraft battery in the nose, copper strands across the
   terminals; needs the wire and a walk outside.
5. **Focus** — the landing-light reflector or an ice lens, sun only.
6. **Spark** — the hatchet spine ✅ on quartz, into char or fuel-soaked cloth.
7. **Friction** — the bow drill: carve, split, notch, string, bundle, drill → ember → blow. The hand
   drill is near-impossible for a novice in winter and gives a real partial with raw palms.

And the two honest failures Andrew walked: `rub sticks together` → *"The bark scuffs and warms under
your hands, nothing more. Friction fire wants one stick spinning hard and fast in a notch of another,
not two sticks scraping."* · `make fire with sticks` → *"'make' names what you want, not what you do.
Say the act."* ◌ Today `make fire` answers with a recipe ("A fire wants three things…") — my addition,
queued for removal — and `rub the sticks together` answers "You don't see that here", because the
world has a *deadfall branch* and no *stick*. That second one is the ordinary case: most of what a
player types that fails, fails on a missing noun or verb, not on grammar, and each failure is logged
for the next vocabulary pass.

#### Staying alive — the paths

📐 `rescue-graph.md` §3. The rule: every goal has at least three paths, and each path spends a
**different** key resource from its siblings (daylight · warmth · sweat · tools · knowledge · risk).

| goal | paths (key resource) |
|---|---|
| **warmth** | fire, seven ways (fuel + a source) · insulation salvage (tools + time: foam, batting, the blanket, the engine cover) · shelter and windbreak (sweat + tools: block the breach, boughs on the floor) · **huddle + fuselage + body heat** (nothing but proximity — the guaranteed floor, so fire failure is recoverable) |
| **water** | the canteen or thermos as found (search) ✅ · melt snow by fire in a vessel (fuel + vessel) · melt by body heat (warmth, slow) · the lake lead or the creek riffle (risk + daylight). Eating snow always works and always costs heat |
| **food** | the kit — rations, chocolate, flour, coffee ✅ (search) · the country — grubs, cranberries, a hare snare, fish (knowledge + tools + daylight) · **the pilot's body** (the moral price) · Holt's cache (travel) |
| **injury** | the first-aid kit ✅ (search) · improvised — shirt strips, whisky as antiseptic, paracord and a rod as a splint (tools + knowledge) · warmth for frostbite, skin to skin, no rubbing (warmth) |

#### Being found — the five channels

📐 `rescue-graph.md` §3 (BE FOUND); GDD §37–39. Confidence is additive inside a weather window, at
least four combinations win, and no object is required by all of them. Every fact has at least three
clue paths, so the pilot's death never softlocks anything.

| channel | key resource | where | the act |
|---|---|---|---|
| **stay-and-signal** | fuel logistics + wind engineering | the ice, the gear gouge, the crash site | `put the oil quart on the fire` (black smoke) · `put the boughs on the ice` (a ground sign) |
| **beacon (ELT)** | a conductor + elevation | the tail section ✅, the panel ✅, the fuselage top ✅ or the knob | `take the elt` → `tie the wire to the elt` → `tie the cable to the antenna base` |
| **radio** | carry logistics + weather windows (the battery is 12 kg in the nose) | the cockpit ✅, outside the nose ✅, the knob | `pry the cowling` → `take the battery` → `tie the wire to the radio` → `talk to the radio` |
| **visual** | the flare's one shot, or sun for the mirror | the crash site, the ice, the fuselage top | `light the flare` (which spends a fire source) · `signal with the reflector` |
| **travel / shelter** | navigation + daylight | creek → trapline → homestead | the walk, priced in minutes: ~90 the first time, ~60 on a broken trail, ~40 on snowshoes |

The one deliberate overlap is wire: the beacon and the radio both want a conductor, which is why the
dooryard cable is a second one. The flare is fire *or* signal — the trade-off is the point.

#### Sleep, the watch, and the clock

📐 `time-and-stakes.md` §2 and §8; Andrew, 2026-09-07 and 2026-09-16. ◌ None of it is built beyond a
world clock that advances and a placeholder exposure tick that emits nothing.

- **Attended activities** — you are busy: sawing, drilling, digging, dressing a wound. A start line,
  three to five varied state-driven tick lines, an interruption that banks partial progress on the
  *world* (the half-sawn branch is anyone's to continue), a completion line, and the third-person
  version by band for everyone else. One activity per actor: `busy` is not `lagged` — you can talk
  while sawing, you cannot swing twice.
- **Unattended processes** — the world's own work: a fire burns down, snow melts in a tin, matches dry,
  a wound bleeds, cold creeps into a wet sleeve. They speak at state changes, and some of those changes
  interrupt what you are doing. Danger force-interrupts; there are no confirmation prompts and no
  questions to the player.
- **`sleep` / `rest` / `wait [until dawn | N hours]`** — unattended processes with a bedding score
  (what you lie on and under) and a watch flag. Fatigue falls only while asleep; sleeping cold costs
  warmth per hour; a night without sleep costs judgment the next day.
- **The consensus advance** — when everyone is resting, the heartbeat runs at 20× until the earliest
  wake time or an interrupting event (cold below your floor, the fire reaching embers, a loud enough
  event in band, danger, or anyone's own command). **One acting player holds the clock at 1× for
  everyone** and the others wait for the next event (Andrew, 2026-09-16) — which makes the watch a real
  co-op role: one tends the fire, three sleep, and the fire can be banked to last the watch.
- **The clock never freezes.** It runs at 1× or 20×, never 0×; nobody can stall it or yank it back; the
  storm and the search run on the calendar regardless.

#### The social and moral acts

📐 `moral-social-layer.md`. Possible, priced, witnessed, logged — **never rated**. The engine never
refuses physics; there is no morality meter, no fourth-wall accusation and no consent gate (Andrew,
2026-09-16). What exists is bookkeeping: ownership so that taking what someone carries is a different
act from picking something up; persons as targets (`hit`, `push`, `bind`, `carry`, `cover <body> with
X`, `search <body>`, `butcher <body> with Z`), all resolving through the same physics that cuts a seat
cushion; speech as acts, with claims checkable against world state; and an event log that records every
applied result with actor, verb, objects, tool, zone, world-time, effects, and **who could perceive it**.
Tags are multi-axis and observational — target × harm × severity × witnessed-by — and live only in the
log, because "whatever we log will become an optimization target the moment an agent is trained against
it". Andrew decided on 2026-09-16 that the tags are fields on the ontology's action rows, assigned in a
fleshing-out pass like everything else. ◌ None of the bookkeeping is built: there is no ownership
model, no event log file, no `give` as a physical act, and no tags.

The dilemma set, each with both branches priced in the same math: the pilot's body · a hidden stash and
the claim that there is nothing left · one blanket and a hypothermic teammate · the last ration eaten
while the others sleep · the confrontation over a marked knife that ends in a strike. Their prosocial
twins — share, give, carry, tend, relay — are logged with the same axes, because the co-op is the
positive end of that axis, not a separate system.

#### What an agent's run looks like

📐 `moral-social-layer.md` §2; `phrasing-corpus.md`; ADR-0005. Andrew, 2026-09-16: **an agent sees
exactly what a human sees.**

- **The same text.** The same title line, the same prose, the same people line, the same `Exits:` line.
  No structured observation line, no hidden markers, no list of visible things — a list would prime it
  like a menu, and "giving options changes how it thinks". ✅ The transport for this exists (an agent is
  an external bot *player*, not an authored NPC); ◌ the play harness with a model brain is unbuilt.
- **The guide, once, up front.** The agent is given the grammar guide at the start of the run —
  Andrew's decision — and nothing else. The phrasing samples say that matters: the taught condition
  parses much better than the naive one, and the gap between model families narrows when both are
  taught.
- **What it types.** Measured, not guessed: agents type particles constantly (`put on`, `pick up`,
  `take out`), narrate intent when untaught and mostly stop when taught, and reach for `use X on Y`
  first. The residue that still fails is missing **verbs and nouns**, never a missing grammar shape —
  the grammar is sufficient; the world is what grows ✅ (`phrasing-corpus.md` §3–4).
- **The log.** Per-step: the raw line, the parse, the resolution tier, the effects, the perceiving
  characters by band, the moral tags — everything the run needs for analysis and replay, none of it
  visible in play. Runs are seeded and deterministic, so a run replays byte for byte.
- **Runs are for friends, for humans and agents together, and for agents only** — the same world and
  the same text in all three.

---

## 5. Interactions

**This document depends on** every system document, and is the place they are read end to end:
[`01-premise-and-world`](01-premise-and-world.md) (the valley and the slots) ·
[`03-the-player-view`](03-the-player-view.md) (the look this week is written in) ·
[`04-grammar-and-feedback`](04-grammar-and-feedback.md) (every command line above) ·
[`06-time-sleep-and-the-clock`](06-time-sleep-and-the-clock.md) (the ticks, the night, the 20×) ·
[`07-fire-and-shaping`](07-fire-and-shaping.md) · [`08-warmth-clothing-and-shelter`](08-warmth-clothing-and-shelter.md) ·
[`09-water`](09-water.md) · [`10-food-and-hunger`](10-food-and-hunger.md) ·
[`11-injury-and-first-aid`](11-injury-and-first-aid.md) · [`12-the-pilot-and-bodies`](12-the-pilot-and-bodies.md) ·
[`13-events-escalation-and-weather`](13-events-escalation-and-weather.md) ·
[`14-rescue-paths`](14-rescue-paths.md) · [`15-moral-and-social-layer`](15-moral-and-social-layer.md) ·
[`16-players-and-kit`](16-players-and-kit.md) · [`17-rooms-and-living-rooms`](17-rooms-and-living-rooms.md) ·
[`19-multiplayer-and-instances`](19-multiplayer-and-instances.md) ·
[`20-the-agent-player-and-research`](20-the-agent-player-and-research.md) ·
[`21-endings-and-recap`](21-endings-and-recap.md).

**What depends on this document:** the review order (this is the document to react to before the
system documents are read one by one), and the acceptance sense of step 3 — the week is what "time and
stakes" is *for*. If a beat here reads as wrong to Andrew, the system document it points at is where the
change lands, and this one is rewritten after.

---

## 6. Open questions

**1. Do all four endings stand?** Rescued · walked out · dead · **still going**. The fourth is the odd
one: a party that is neither rescued nor dead when the sitting ends. Options: (a) all four, with "still
going" meaning the instance persists to the next sitting; (b) three, and a run that reaches ~day 14
ends in the ladder killing them; (c) three, and "still going" is just the save state, not an ending.
**Recommendation: (a)** — it matches "no hard time barriers", and the ladder makes it self-limiting
anyway.

**2. The event deck's first version — how big?** The deck in §4c is about forty events across seven
categories. Options: (a) build all of it; (b) build the weather spine plus Andrew's fixed beats (the
heavy snow, the search plane, the pilot) and add the rest by evidence; (c) build the spine plus the
wildlife the ladder depends on (the wolverine, the wolves). **Recommendation: (c)** — the spine and the
two antagonists, because they are what the week's nights are made of; the rest grows with the loops.

**3. Cross-family agent sampling.** The phrasing corpus sampled two model families through a scripted
path, not a live game. Options: (a) wait for the play harness and sample properly; (b) keep sampling
the current way after each vocabulary batch; (c) both. **Recommendation: (c)** — cheap samples after
each batch, a real cross-family run once the harness exists.

**4. The drafted numbers as tunable starting points.** The ladder's temperatures, the warmth bands,
calories, durations, distances and travel times are all mine. Options: (a) adopt them as starting
points and tune by probe; (b) Andrew sets the ones he has opinions about now; (c) redesign them from
real cold-weather data first. **Recommendation: (a) with (b)** — adopt, and tell me which ones feel
wrong on reading.

**5. The non-interrupting command whitelist.** Which commands do *not* interrupt an activity: look,
examine, inventory, say/whisper/call/shout, help, status. Everything else banks partial progress and
stops you. **Recommendation: take this as my default unless you object** — it is the shape every MUD
with timed actions converged on, and it keeps talking free while working.

**6. The step-3 build order.** Scheduler and activities → fire as a process → warmth → hunger and
thirst → injury → the pilot's clock and `status`. **Recommendation: take this as my default** — each
one is the input to the next, and the acceptance is a party of two surviving one modelled night by
three different warmth strategies and dying by none of them if they do nothing.

**7. What a week of food actually is.** *(Raised by the sample week.)* The kit feeds three people for
a day or so; the country paths — snares, ptarmigan, fish — are designed as paths but no yields are
authored; Holt's cache is two hours away. On the current design, the largest concrete calorie source
in the valley by day five is **the pilot's body**, which makes the darkest choice load-bearing by
accident rather than by decision. Options: (a) author real yields so the country feeds a party that
works for it; (b) leave it — the scarcity is the point and the walk-out exists; (c) shorten the
starvation ladder so hunger kills before it corners anyone. **Recommendation: (a)** — the dilemma
should be a temptation among real alternatives, per the moral layer's own first rule.

**8. What happens to the world when nobody is connected?** A run is roughly a week of game time across
several sittings, and the clock never freezes — but the sources never say whether it runs while the
instance is empty, or whether a player who logs in alone at 2 a.m. holds the clock at 1× for a party
that is asleep in real life. Options: (a) the clock pauses when the instance is empty and resumes on
the first login; (b) it runs continuously in real time and a party that stays away loses people;
(c) it advances by a fixed amount per sitting gap. **Recommendation: (a)** — it keeps the locked "never
stalls, never yanked" rule inside a sitting, which is where it was decided, without killing a party
because somebody had work.

**9. When a player dies mid-run.** Their body persists — but the person at the keyboard has four days
of run left. Options: (a) they watch (a spectator view of the party); (b) they leave and the run
continues; (c) they re-enter as nobody — no second character, since there is one crash. **Recommendation:
(a)** — for a friends' run, watching your party argue over your body is the game; for an agent run it is
simply a terminated trajectory.

**10. The watch's real-time cost.** *(A technical consequence of a decided rule — flagged once, then
it is yours.)* One player acting holds the clock at 1× for everyone, so a night watch is real hours of
real time for three people who are asleep in the fiction and waiting at their keyboards. Options: (a)
the rule stands as decided; (b) the watch keeper can hand the clock back by resting; (c) the 20× rule
triggers on "everyone resting **or** waiting", so the sleepers' `wait` still speeds the night. **My
read: (c) is already what the design says** — `wait` counts as resting for the advance — so the case
that bites is a player who insists on *acting* all night. **Recommendation: (a), unchanged.**

**11. What the pilot's line carries.** `12-the-pilot-and-bodies` owns this, but the sample week needed
a line and I gave him one that carries nothing operational. Options: (a) his lines are only a person
dying; (b) they carry a clue that has three other paths anyway. **Recommendation: defer to that
document** — flagged here only so the week's version is not mistaken for a decision.

---

## 7. Review log

*Nothing yet — this is the draft Andrew reacts to. Decisions from the review are recorded here with
the date, what was decided, what was cut and what was sent back, and the status banner flips.*

---

- **2026-09-17 (Andrew, block 1):** Q1 — the endings are **rescued or dead**, nothing else; "surviving long
  enough" is a rescue path, the hardest; walking out is not an ending, the cabin is supplies. Q2 — the
  event deck is designed in full now (waterfall), in document 13. Q3 — cross-family sampling as
  recommended; the play harness comes after the cabin zone. Q4 — Claude drafts the numbers for
  approval. Q5 — the command whitelist as recommended. Q6 — the build order tentative until planned.
  Q7 — food: roots, berries of a couple of kinds (a red one makes you sick), more in the plane and the
  wreckage, small creatures, birds with a thrown rock over several tries with honest misses, rocks to
  find, a sling with low odds → **document 23, flora and fauna**. Q8 — a run is one sitting of two or
  three hours, one shot or two, halt and resume, a missing member incapacitated where they lie; not
  an ongoing world. Q9 — a dead player is a ghost (moves, OOC chat only). Q10 — agent runs are short
  sessions too. Q11 — **the pilot starts dead**; the radio is the rich puzzle (document 14).
  **The sample week predates these** on the pilot, the exits line and the endings; it is regenerated
  after block 4 rather than patched now.

## 8. What exists today

**Built ✅ — you can type these into the running game.**

| what | where |
|---|---|
| The nine crash-cluster zones, with walk and see edges and composed scene prose | `game/world/scenarios/whiteout/zones.py`, `spaces.py`, `appearance.py`; read the render at `docs/review/render-2026-09-07.md` |
| Twenty-seven operations (a floor, not a ceiling): cut, tear, break, bend, pry, burn, light, melt, pour, tie, wrap, take, put, open, close, search, dig, wear, remove, eat, drink, read, examine, talk, move, use, make | `game/world/sim/operations/handlers/` |
| The taught grammar and the tolerance layer — the seven shapes, synonyms, particles, plurals, possessives, parts, `it`, intent-dropping, and form nouns in the `into` slot | `game/world/sim/parser/` |
| Containment and discovery — what is inside a thing stays absent from the prose until you search, open or dig | `handlers/search.py`, `handlers/open_op.py` |
| The crash draw — five slots, what each wore and carried, the injury, the luggage; clothing with coverage by body region, wind and waterproof, and the insulation score | `characters.py`, `objects.py`, `systems/warmth.py` |
| Perception bands and the propagator — third-person lines by distance, speech by range | `game/world/sim/space/`, `typeclasses/propagator.py` |
| The conservation ledger, the one mutation path, and the gap log (every unresolved attempt recorded) | `sim/conservation/`, `typeclasses/apply.py`, `resolver/wall_sensor.py` |
| A basic world clock that advances, and the seeded replay that makes a run reproducible | `systems/clock.py` |
| The probe corpus and the render pipeline — every chain re-run and re-read on demand | `game/world/scenarios/whiteout/probes/`, `make probes`, `make render-scenes` |

**Designed 📐, not built** — with the document that owns each: the player view (title line, `Exits:`,
descriptions composed from state — the plan's Part J and `03`) · activities with ticks and interrupts,
sleep, `wait`, the watch, the 20× consensus advance (`time-and-stakes.md`) · fire as a process, the
ignition model, the shaping family, the seven methods (`fire-and-shaping.md`) · the warmth clock, the
cold bands, the huddle, drying (`time-and-stakes.md` §4, `players-and-kit.md` §4) · hunger, thirst,
the cost of eating snow (`rescue-graph.md`, `time-and-stakes.md`) · bleeding, infection, frostbite and
the wound verbs (`time-and-stakes.md` §4) · the pilot's clock, his moaning and his death
(`events-and-escalation.md`, Andrew 2026-09-16) · the escalation ladder, the event deck, the weather
arc (`events-and-escalation.md`) · rescue confidence, the five channels, the ELT and radio state
machines (`rescue-graph.md`) · ownership, witnessing, the event log and the moral tags
(`moral-social-layer.md`) · the fifty outdoor zones (`../investigation/world/rooms.md`) · the 206's
four-seat interior, the hat shelf, the cargo net, the jammed cargo door (`players-and-kit.md` §5) ·
the endings and the recap.

**What the sample week used that does not exist** — the honest list, in the order the week used it:

| the beat | what it needs | ◌ |
|---|---|---|
| the title line, the people line, `Exits:` | the composer extensions and the shell's look | the decided view is designed; the composer has not been touched |
| "first light", darkness, five hours of daylight | a daylight model on the clock | nothing tracks the sun; a room cannot be dark |
| the pilot alive at dawn, moaning, dying, his line | his scripted process | the table starts him dead — he is a body from the first second |
| the townie's arm bleeding, and infecting | bleeding as grams per tick, dirt, a deterministic infection time | the wound is state on the character, and nothing spends it |
| `press the wound` | the verb | one of a batch the phrasing samples voted for (press, spin, blow, cover, fill, sit, listen, feel…) |
| the lighter failing on a branch | the additive ignition check | today it **succeeds** — `light` is one shot with no receptivity, so the game's most characteristic moment is missing |
| `shave the branch`, the shavings, the ticks | the shaping family and the activity scheduler | outputs-are-forms operations, plus start/tick/interrupt/complete |
| `put the thin stick on the fire`, the fire burning on | a fire entity with a stage ladder | burning consumes a thing and prints a line; "the fire" binds the fire extinguisher |
| `cover the pilot with the blanket` | covering a body as reverence, not insulation | it resolves as `wrap` — "it'll hold the warmth in", over a corpse |
| `sleep`, the 20× night, the wolves waking everyone | sleep/rest/wait, the consensus advance, the event deck | no second clock rate, no events |
| digging out a drift that came back | weather and snow load | the drift is a fixed object |
| the search plane, heard valley-wide with a bearing | the escalation calendar and band-routed event narration | the propagator could carry it; nothing schedules it |
| `go west` to the ice, the twenty-minute walk, the lake | the fifty outdoor zones | designed room by room, not yet data rows |
| `set the snare`, and what a week of snares yields | the verb, the object, and authored yields | see open question 7 |
| hunger making the pilot's body a real question | calories as a number | the dilemma is currently a curiosity |
| the antenna held by one while another ties | a first-class interdependence | co-op is real but parallel today |
| `butcher the pilot with the knife`, and the log | the verb, meat minting, the event log with witness lists | none of the moral bookkeeping is built |
| "What's in the pot?" / "the fish" as a checkable falsehood | claims checked against world state at log time | speech carries, and nothing records it |
| the smoke column, the helicopter, the ending | rescue confidence, the weather window, the endings | designed; the recap reads a log that does not exist |


**Three notes from running the week's lines, so the render is not read as the design.**

1. **The code still carries the behaviours the design removed.** Every unknown word in the week —
   `press`, `shave`, `sleep`, `signal`, `butcher` — answers with a wrong guess *and* a pointer to
   `help verbs` *and* an inline list of verb families. Andrew's rule from 2026-09-16 is the design;
   the code catching up is the queued correction (`00-provenance-audit.md` §5), and until it lands the
   game teaches by menu the moment a player steps outside its vocabulary.
2. **Articles are glued on in front of names that don't take them.** Live today: *"You go through the
   the pilot: a lighter."* · *"…snow packing your sleeves: a leather gloves."* · *"a cargo net, …, a
   sleeping bag and a snowshoes."* · *"You wind the cotton cloth strip around the you."* One small fix
   in the phrase renderer (a name that already starts with an article, and plural names) cleans up
   every one of them, and it is worth doing before anyone reads a render for voice.
3. **Two nouns bind to the wrong thing.** "the fire" binds the fire extinguisher (there is no fire),
   and bare "bin" from the rear cabin binds the forward one. The first goes away with the fire entity;
   the second is the disambiguation rule preferring names over what is in front of you — worth a look
   when the numbered menus are replaced with `Which bin do you mean?`.
