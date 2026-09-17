# 11 — Injury and first aid: wounds, bleeding, infection, frostbite, splints, the med pouch

> **Status: `draft for review` (2026-09-16). NEW — this system had no design document of its own.**
> **Architecture counterpart:** none. **Sources:**
> `docs/investigation/design/rescue-graph.md` §INJURY (the three paths) ·
> `docs/investigation/design/time-and-stakes.md` §4 (the wound model and the bleeding/infection
> clock) · `docs/investigation/design/players-and-kit.md` §1 (the five slots' injuries; the nurse's
> med pouch) · `docs/investigation/design/events-and-escalation.md` §2 (the injuries row) and §4
> (the Bodies deck) · GDD §31–§36 ("injury/medicine — systemic, improvised") · the archived AI seed
> `design.md` §35 (the injury list and the improvised-medicine list), carried forward "unchanged" by
> GDD §31–§36 · `docs/scenarios/whiteout/rooms/mid_cabin.md` §2b and §5 (the first-aid kit and the
> missing treat-a-wound verb) and `cockpit.md` §2c (the pilot's blood) · code:
> `game/world/sim/systems/injury.py`, `game/world/scenarios/whiteout/characters.py`.

---

## 2. Provenance

### Andrew's decisions

- **Each player starts with a different injury draw.** (2026-09-07, decided; recorded in the
  provenance audit alongside the clothing and pockets draws.) You do not choose what the crash did
  to you, and nobody in the party is whole.
- **Decisions across the moral spectrum** (2026-09-07) — the injured co-player is one of the places
  that lands: who gets carried, who gets the bandage, who gets left by the fire.
- **The pilot dies within the first day**, nobody can talk to him, and tending him is a physical act
  that resolves like any other. (2026-09-16.) First aid's first patient cannot be saved, and the
  party will spend real time finding that out.
- **No lethal-consent gate; violence resolves with real physics.** (2026-09-16.) Wounds are wounds
  whoever caused them; the engine does not soften a blow.

### Proposals (Claude)

- The wound model — named wounds with part, kind, severity, a bleeding rate and an infection time —
  and the bleeding/infection clock (`time-and-stakes.md` §4).
- The five slots' specific injuries and the nurse's med pouch (`players-and-kit.md` §1). The *draw*
  is Andrew's; *which* injuries are proposals.
- The three injury paths (`rescue-graph.md` §INJURY).
- The injuries row of the escalation ladder (`events-and-escalation.md` §2).
- The seed's injury list and improvised-medicine list (`design.md` §35) come from the **archived
  AI-written seed**, not from Andrew.
- **Frostbite, snow blindness and carbon monoxide are Claude's additions** from the 2026-09-07
  brainstorm (`events-and-escalation.md` §3–§4), not Andrew's — labelled as such throughout.
- Every number.

---

## 3. In one paragraph

Everybody wakes up hurt, differently, and it shapes what each of you can do before anyone has said a
word about it. The cut forearm is bleeding into a sleeve and will keep bleeding until somebody
presses it and binds it; the sprained ankle makes every walk cost double until somebody thinks of a
stick and a strap; the bruised ribs make heavy work slow; the concussion makes the first day a fog.
None of it is a debuff you read off a sheet — it is your own description when you look at yourself,
and it is the reason the party has to decide who does what. The nurse has a pouch with gauze and
tape and sutures in it and knows exactly what to do, which does the party no good at all, because
the person playing her has to work it out like everyone else. Later the wounds that were dressed
with a dirty shirt start to matter, and the fingers that spent an afternoon bare on cold metal start
to matter, and first aid stops being a one-off act and becomes a thing you keep doing.

---

## 4. The design

### 4.1 The rules

1. **Wounds are named things on a body, not a hit-point total.** The proposed shape
   (`time-and-stakes.md` §4, and the field names are shipped): `{part, kind, severity, bleeding
   (grams per minute, 0 = none), bound?, infected_at, note}`. A person has a list of them.
2. **Bleeding is a process.** It costs hydration and warmth every tick until the wound is pressed or
   bound; a bound wound stops. *(Proposal.)*
3. **Infection is a clock, not a die roll.** A wound dressed with something dirty can infect after N
   hours — deterministic, with seeded jitter, so a run replays identically (DR-12). Then fever,
   which costs warmth and water; then, untended, worse (`events-and-escalation.md` §2).
4. **Medicine is systemic and improvised, never a recipe.** The seed's own examples are the
   specification (`design.md` §35): cloth becomes a bandage; seatbelt webbing becomes a tourniquet or
   a splint tie; branches, aluminium frames or poles become splints; alcohol disinfects; boiling water
   or a flame cleans some metal tools; snow reduces swelling and worsens cold exposure; painkillers
   improve function and mask danger; moving an injured person can save them from the cold and worsen
   the injury. Every one of those is a trade, and none of them is a crafting recipe.
5. **Treatment is an act on a wound, with a tool.** `press`, `bind` / `wrap`, `splint`, `stitch`,
   `clean`. The wound is the target; what you use is whatever physically serves.
6. **The injury is in the description.** `examine me` reads your wounds back to you in plain words —
   this is shipped: *"Your forearm is cut and bleeding; your ankle is sprained."* No status screen,
   no numbers.
7. **Never a menu.** The game does not tell you to press the wound, does not list the med pouch's
   contents when you are bleeding, and does not name the tourniquet. It says the sleeve is soaking.

### 4.2 The starting draw (content — `players-and-kit.md` §1, shipped in `characters.py`)

| slot | injury | what it costs |
|---|---|---|
| the guide | bruised ribs | bending and lifting hurt; heavy work is slow |
| the townie | a cut forearm, bleeding | the census wound — bleeding through the sleeve; press it, bind it |
| the nurse | a sprained ankle | walking costs double; a splint and a stick would halve it |
| the salesman | concussion | tires fast; the first day is a fog (confusion messages) |
| the kid | shock | physically fine; slower to act on day one |

The point of the spread is that it is *heterogeneous*: the person who can walk is not the person who
can lift, and the person who knows medicine is the one who cannot get to you. The seed permutes which
player draws which slot, so no player is always the townie.

### 4.3 The three paths (the rescue graph's own check)

| path | key resource it spends | where | the chain |
|---|---|---|---|
| **the first-aid kit** (bandage, tape) | search | the forward bin in the mid cabin — pry-gated | `press wound` → `wrap arm with bandage` |
| **improvised** (shirt strips, whisky as antiseptic, paracord and a rod as a splint) | tools + knowledge | the rear cabin, the duffel | `tear shirt` → `pour whisky on wound` → `wrap arm with strip` |
| **warmth for frostbite** (skin to skin, no rubbing — the manual) | warmth | any | `wrap hands in socks` · sit by the fire |

**The med pouch** is the fourth thing in the room and belongs to a person, not the plane: gauze
pads, medical tape, ibuprofen, a suture kit — "she knows how; the player has to"
(`players-and-kit.md` §1, shipped in `characters.py`). The plane's kit is a bandage roll and medical
tape in the pried forward bin. Whisky and hand sanitizer are the alcohol, and both are also fuel.

### 4.4 The injury list (the coverage target)

From the seed (`design.md` §35), as the set the system should eventually honour — a floor, not a
list of what can happen: **bleeding · a broken limb · concussion · burns · frostbite · hypothermia ·
infection · shock · dehydration · smoke inhalation · exhaustion.** Three of those are the cold's
work and are really the warmth system's failures with a location (frostbite, hypothermia); two are
fire's (burns, smoke inhalation); two are the other survival clocks' (dehydration, exhaustion).

**Claude's additions from the 2026-09-07 brainstorm, labelled** (`events-and-escalation.md` §3–§4) —
none of these are Andrew's and all are open for cutting:

- **Frostbite** — it whitens a finger first; bare hands and feet drive it; the treatment is warmth,
  skin to skin, and specifically *not* rubbing, which the manual teaches.
- **Snow blindness** — a day on the open ice without the kid's sunglasses. It is the one injury the
  world gives you for doing the right thing in the wrong way.
- **Carbon monoxide** — a fire inside a closed fuselage. Listed among the endings ("dead — cold,
  starvation, a fall through ice, CO in a closed fuselage, the wreck sliding") and it is the reason
  blocking every gap is not a free move.
- **Hypothermia confusion** — messages, never command hijacking. The player is told the world is
  going strange; the engine never takes their hands off the controls.

### 4.5 The escalation (what untreated injury does over a week)

`events-and-escalation.md` §2, proposals: a cut on day 1 → infection risk rising on a dirty wound by
day 3 → fever costing warmth and water by day 5 → gangrene without care by day 7. The kill mechanism
is stated plainly and is the right one: *a body that can't work can't stay warm.* Injury rarely kills
directly in a week; it takes away the labour that keeps everyone else alive.

The Bodies deck adds the beats that make it visible: a wound infects; frostbite whitens a finger;
snow blindness on the ice; hypothermia confusion; dehydration headaches; the hunger stages — and, on
day one, the pilot's moans, heard only in the cockpit.

---

## 5. Interactions

**This depends on:**
- **08 Warmth, clothing and shelter** — frostbite and hypothermia *are* warmth failures; bleeding
  costs warmth; bare hands lose the dexterity that treatment needs.
- **09 Water** — bleeding and fever cost hydration; boiling cleans a tool.
- **07 Fire and shaping** — burns, smoke inhalation, sterilising a blade, and the warmth that treats
  frostbite.
- **06 Time, sleep and the clock** — bleeding and infection are processes on the heartbeat; dressing
  a wound is an attended activity with its own feedback; `SURVIVOR_WORSENS` force-interrupts.
- **18 Materials and forms** — cloth binds, webbing ties, a rod splints, alcohol disinfects; nothing
  is a "bandage" by type.
- **16 Players and kit** — the draw, the med pouch, the first-aid kit, the whisky.

**These depend on it:**
- **10 Food and hunger** — starvation weakness; the bulged can; cleaning game with a blade.
- **12 The pilot and bodies** — tending him is first aid that cannot work, and costs real time and
  warmth.
- **14 Rescue paths** — an injured party walks slower, climbs worse, and carries less; the walk-out
  is gated on who can move.
- **15 Moral and social layer** — the bandage, the painkillers, who gets carried, and whether the
  party leaves someone.
- **19 Multiplayer** — carrying a person is the co-op act with the highest price.

---

## 6. Open questions

1. **Does injury use hit points at all?** *(a)* Named wounds only, with severity. *(b)* A health
   total behind them. **Recommendation: (a)** — the shipped data is already wound-shaped, the
   descriptions are better, and "how hurt am I" is a question the game should answer in words about
   your forearm, not a number.
2. **What kills, and how fast?** **Recommendation: bleeding can kill in hours if nothing is done,
   infection kills in days, and everything else disables rather than kills** — which matches the
   ladder's own thesis that a body that can't work can't stay warm.
3. **Is `press` its own operation?** It is on the rescue graph's missing-verbs list and it is the
   only treatment that needs nothing but a hand. **Recommendation: yes** — it is the first-minute
   act for the townie's arm and it needs no object, which makes it the right teaching verb.
4. **Do wounds need a `clean` step, or does the tool's dirt just carry?** **Recommendation: the dirt
   carries** — a wound bound with a filthy shirt sets a later infection time, and cleaning is
   pouring alcohol or boiled water on it. One rule, no new subsystem.
5. **Do frostbite, snow blindness and carbon monoxide stay?** They are Claude's additions.
   **Recommendation: frostbite yes** (it is the cold's most legible consequence and the clothing
   model already computes bare regions); **carbon monoxide yes** (it is the price that makes sealing
   the fuselage a real trade); **snow blindness only if the ice days are long enough to earn it** —
   otherwise it is a gotcha attached to one pair of sunglasses.
6. **What does the nurse's knowledge actually do?** Andrew's rule is that knowledge lives in the
   world, not in a skill stat. **Recommendation: nothing mechanical** — she carries better *tools*
   and the manual carries the knowledge; the fiction that she knows how is in her description and in
   what the player does with it. Flagged because `players-and-kit.md` says "she knows how; the player
   has to", which is a design position worth confirming out loud.
7. **Can a player be carried?** `carry (a person)` is on the missing-verbs list and the pilot's litter
   is assumed by the world design ("a drag litter of paneling and cord: possible, priced in sweat and
   gentleness"). **Recommendation: yes, as a slow, two-hands, warmth-expensive activity** — it is the
   co-op act the whole injury system is pointing at.
8. **Does painkiller masking get modelled?** The seed says painkillers "improve function but can mask
   danger". **Recommendation: yes, and honestly** — ibuprofen removes the pain messages without
   removing the wound, so a player who takes it works normally and finds out later. It is one of the
   few places the game can lie to the player fairly.
9. **How does the concussion's confusion read without hijacking commands?** **Recommendation:
   unreliable *description*, never unreliable *input*** — the room reads wrong, the time of day is
   misjudged, names slip; the player's typed act always does what they typed. The same rule as
   hypothermia confusion.
10. **Does `examine <someone else>` show their wounds?** The self-view does. **Recommendation: yes,
    what is visible** — a soaked sleeve, a limp, a white finger — but not the internals. It makes
    checking on each other a real act.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

## 8. What exists today

**Built**
- `game/world/sim/systems/injury.py` — the wound *data* and the self-view line: `wounds(ent)` reads
  `state['wounds']`, and `wounds_summary(ent)` composes "Your forearm is cut and bleeding; your ankle
  is sprained." with per-kind wording for cut, sprain, concussion, bruised ribs, burn, frostbite and
  shock, plus the bleeding/bound suffixes.
- `game/world/scenarios/whiteout/characters.py` — the shipped starting draw: one injury per slot
  (bruised ribs / cut forearm with a bleeding rate / sprained ankle / concussion / shock), each with
  part, severity, bleeding and an authored note, written onto the character as `wounds`.
- The wound line is woven into the self-view: `warmth.py::self_view` appends `wounds_summary`, so
  `look at me` and `examine me` report injuries identically.
- `game/world/sim/operations/handlers/wrap.py` — `wrap` / `bandage` / `insulate` / `swaddle` over any
  flexible or fabric material; this is what `bandage arm with bandage` resolves as today.
- `game/world/sim/operations/handlers/tear.py` and `pour.py` — tearing a shirt into strips and
  pouring whisky or sanitizer are both real operations, so the improvised path's *materials* exist.
- Objects: the first-aid kit with a bandage roll and medical tape in the pry-gated forward bin; the
  nurse's med pouch with gauze, medical tape, ibuprofen and a suture kit; the whisky bottle; the hand
  sanitizer.
- Tests and probes: `game/tests/sim/test_kit.py::test_wounds_summary`;
  `probes/kit.nurse.med_pouch` (`open pouch` → `take gauze` → `wrap arm with gauze`) and
  `probes/census.py` `mid_cabin.open_kit` and `mid_cabin.bandage_arm_with_bandage` are measured
  passing.

**Designed, not built**
- The whole injury *clock*: bleeding per tick, binding stopping it, the infection timer, fever, the
  escalation to day 7 (`time-and-stakes.md` §4; `events-and-escalation.md` §2).
- Treatment as an act on a *wound*: `press`, `splint`, `stitch`, `clean` — `mid_cabin.md` §5 logs
  "treat-a-wound (`bandage X`, `splint X`) — the first-aid kit's contents have no use-verb yet. Ties
  to the injury system."
- The injuries the world can *inflict*: frostbite from bare regions, burns, hypothermia, smoke
  inhalation, exhaustion, snow blindness, carbon monoxide.
- Carrying an injured person; the pilot's litter.
- Wounds affecting what a character can do — the notes ("walking costs double", "heavy work is slow")
  are authored prose that nothing reads.

**Nothing**
- No operation targets a wound. `wrap arm with bandage` succeeds as a generic wrap: it sets
  `wrapped`/`insulated` on the target and changes nothing about the wound, which is not bound and
  does not stop bleeding — because nothing bleeds yet.
- No `press`, `splint`, `stitch`, `clean`, `carry` or `treat` in today's handler set (`bend, break, burn,
  cut, drink, eat, examine, light, make, melt, open/close, pour, pry, move, read, search/dig,
  take/put, talk, tie, use, wear, wrap, tear`).
- No frostbite, no hypothermia, no infection, no fever, no painkiller effect; ibuprofen is a bottle
  of plastic with a count on it.
- The pilot's blood in the cockpit is examine-prose only, and the pilot himself is already dead in
  the shipped slice — the "dies within the first day" decision (2026-09-16) is not implemented (see
  document 12).
