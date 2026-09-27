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
  party will spend real time finding that out. *(superseded 2026-09-26: on 2026-09-17 Andrew decided
  the pilot starts the run dead — document 12 §7 — so there is no first patient to tend; the party's
  first patients are each other.)*
- **No lethal-consent gate; violence resolves with real physics.** (2026-09-16.) Wounds are wounds
  whoever caused them; the engine does not soften a blow.

**Decisions made elsewhere that this document must now serve** *(gathered by Claude, 2026-09-26; Andrew's
words are in the documents named)*:

- **A combat system like a MUD's is in** (2026-09-26 — `README.md` writing rules; `PLAN.md` A10): stab
  with a spear, beat with a stick. Every blow lands on a body part as a wound.
- **A bear is in; the bear, some bigger animals and a few birds act** (2026-09-26 — document 23 §7).
- **Lethal places injure, never kill outright; fitness matters; a seeded dice roll, announced**
  (2026-09-17 — document 01 §7).
- **Extremities have their own cold, for frostbite** (2026-09-18 — document 08 §6 Q5), and **body parts
  carry heat as part of their ontology** (2026-09-26 — document 10 §7).
- **There is a `status` screen** that reports injuries in band words (2026-09-18 — document 08 §4.9).
- **The endings are rescued or dead, and the run ends when they die, of anything** (2026-09-17 —
  document 21; 2026-09-26 — document 10 §7). **Dead players are ghosts** (2026-09-17).
- **The season is October, at freeze-up** (2026-09-26 — `README.md`).

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
- **The 2026-09-26 re-review** (§4.6 and the answers in §6): the body as an entity, the real clocks of
  what kills, the sources of injury and the treatments, all from real medicine and wilderness first aid
  with the sources listed at the end of §4.6 — Claude's, for Andrew's check.

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
   *(Claude, 2026-09-26 — §6 Q1, Q4; for Andrew's check: a wound is a state on a body **part**, and the
   part is an entity with its own heat, wetness, pain and covering — §4.6. The shipped fields stay;
   `infected_at` becomes the state of the infection process (§6 Q4), and a wound gains
   `contamination` and `pain`.)*
2. **Bleeding is a process.** It costs hydration and warmth every tick until the wound is pressed or
   bound; a bound wound stops. *(Proposal.)* *(Claude, 2026-09-26 — §6 Q2, Q3; for Andrew's check:
   bleeding spends **blood volume**, in millilitres — about 70 mL per kilogram of body weight, some
   5 L in a 70 kg adult (the ATLS classes, §4.6) — and a body short of blood makes less heat, so it
   costs warmth too. Pressure slows it while it is held; a pressure dressing or packing holds it
   after; a tourniquet stops a limb's arterial bleed. A binding stops only a bleed it is equal to:
   arterial blood soaks straight through a strip.)*
3. **Infection is a clock, not a die roll.** A wound dressed with something dirty can infect after N
   hours — deterministic, with seeded jitter, so a run replays identically (DR-12). Then fever,
   which costs warmth and water; then, untended, worse (`events-and-escalation.md` §2).
   *(Claude, 2026-09-26 — §6 Q4: still deterministic and seeded, but a process driven by the
   wound's contamination, how it was cleaned and what covers it — not a fixed N. Real timings in
   §4.6.)*
4. **Medicine is systemic and improvised, never a recipe.** The seed's own examples are the
   specification (`design.md` §35): cloth becomes a bandage; seatbelt webbing becomes a tourniquet or
   a splint tie; branches, aluminium frames or poles become splints; alcohol disinfects; boiling water
   or a flame cleans some metal tools; snow reduces swelling and worsens cold exposure; painkillers
   improve function and mask danger; moving an injured person can save them from the cold and worsen
   the injury. Every one of those is a trade, and none of them is a crafting recipe.
   *(Claude, 2026-09-26 — §6 Q4, for Andrew's check: "alcohol disinfects" is true of a blade and of
   intact skin; poured into an open wound, alcohol kills tissue as well as germs, and the Wilderness
   Medical Society's guideline is to irrigate with plain drinkable water and add nothing. Whisky on
   the townie's arm is a real act with a real, worse result than clean water.)*
5. **Treatment is an act on a wound, with a tool.** `press`, `bind` / `wrap`, `splint`, `stitch`,
   `clean`. The wound is the target; what you use is whatever physically serves.
   *(Claude, 2026-09-26 — §6 Q3, Q4, Q5, Q7: the floor grows with the real acts, each its own
   operation because each does something different to the wound — `pack`, a tourniquet (`tie` a band
   above the wound, `twist` a rod through it), `rinse` / irrigate, pick out the grit, `elevate`,
   rewarm a frozen part, `carry` and `drag` a person.)*
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
| the salesman | concussion | tires fast; the first day is a fog (confusion messages) *(Claude, 2026-09-26 — §6 Q9: a real concussion is headache, nausea, dizziness, light sensitivity, fatigue and slowness, not a world that reads wrong)* |
| the kid | shock | physically fine; slower to act on day one *(Claude, 2026-09-26: this is an acute stress reaction — psychological. Circulatory shock is what blood loss does to a body (§4.6); both are real, and they are different states)* |

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
none of these are Andrew's and all are open for cutting: *(Claude, 2026-09-26: "open for cutting" is
withdrawn — nothing leaves the design for economy (`README.md` writing rules). §6 Q5 keeps all four,
from their real physics, and §4.6 adds what the list was missing.)*

- **Frostbite** — it whitens a finger first; bare hands and feet drive it; the treatment is warmth,
  skin to skin, and specifically *not* rubbing, which the manual teaches.
- **Snow blindness** — a day on the open ice without the kid's sunglasses. It is the one injury the
  world gives you for doing the right thing in the wrong way.
- **Carbon monoxide** — a fire inside a closed fuselage. Listed among the endings ("dead — cold,
  starvation, a fall through ice, CO in a closed fuselage, the wreck sliding") and it is the reason
  blocking every gap is not a free move.
- **Hypothermia confusion** — messages, never command hijacking. The player is told the world is
  going strange; the engine never takes their hands off the controls. *(Claude, 2026-09-26 — §6 Q9:
  real hypothermic confusion is clumsiness, slowness and poor judgment, not a world that looks
  strange; the body can fail at an act, and the engine never performs one the player did not type.)*

### 4.5 The escalation (what untreated injury does over a week)

`events-and-escalation.md` §2, proposals: a cut on day 1 → infection risk rising on a dirty wound by
day 3 → fever costing warmth and water by day 5 → gangrene without care by day 7. The kill mechanism
is stated plainly and is the right one: *a body that can't work can't stay warm.* Injury rarely kills
directly in a week; it takes away the labour that keeps everyone else alive.

*(Claude, 2026-09-26 — §6 Q2; for Andrew's check: the real timings are faster, and "rarely kills
directly in a week" is wrong. A dirty wound shows infection in 24–72 hours and an animal bite in
12–24; fever and spreading redness follow over the next days. "Gangrene by day 7" is two different
real things: gas gangrene, which can appear within hours to three days of a deep dirty wound, and
the black of dead frostbitten tissue, which takes weeks to declare itself — longer than the run.
And injury does kill inside a week: bleeding in minutes to hours, a fall through the ice in about an
hour, carbon monoxide in hours, a bear in one encounter — §4.6. The thesis still holds as one way of
dying among many.)*

The Bodies deck adds the beats that make it visible: a wound infects; frostbite whitens a finger;
snow blindness on the ice; hypothermia confusion; dehydration headaches; the hunger stages — and, on
day one, the pilot's moans, heard only in the cockpit. *(superseded 2026-09-26: the pilot starts the
run dead — Andrew, 2026-09-17, document 12 — so there are no moans; his body's own states are its
beats there.)*

### 4.6 The body, and everything that can hurt it (Claude, 2026-09-26 — §6 Q1, Q2, Q5; for Andrew's check)

This document was drafted around the crash's five wounds. Injury now has many more sources — a combat
system like a MUD's, a bear and other animals that act, places that injure, the ice, the cold in the
extremities — and all of them act on the same thing: **the body, as an entity in the ontology**
(document 05 §4.5), whose parts carry states that systems change. A living player, the dead pilot and
a dead player are the same kind of entity (document 12 §4.3a).

**The body.** An `individual` with `materials` (skin, fat, muscle, bone, blood) and `parts`,
recursively: head (face, eyes, ears, nose), neck, torso (chest, belly, back), arms, hands and
fingers, legs, feet and toes. Every part carries its own states:

| state, per part | what it is | what changes it |
|---|---|---|
| `heat` | tissue temperature — Andrew, 2026-09-26: *"body parts have heat as part of their ontology"* | the core, what covers the part, wind, wet, contact (metal, snow, fuel, a hot stone), blood flow — the heat-system design, to be written; document 08 for the extremities |
| `wet` | grams of water on and in what covers it | document 08 §4.5 |
| `frozen` | ice in the tissue — frostbite | `heat` below about −0.5 °C |
| `wounds` | the named wounds on it, in the shipped shape (§4.1), plus `contamination` and the infection's state (§6 Q4) | every source below; every treatment |
| `pain`, `swelling` | what the person feels, and what limits the part | the wound, movement, cold, drugs (§6 Q8) |
| `covered_by` | the worn layers over it | clothing (document 08 §4.2); it is also what an onlooker can see (§6 Q10) |

And the whole body carries the quantities that decide whether it lives: **blood volume** (mL),
**core temperature** (document 08), **hydration** (mL, document 09), **energy** (document 10's stores — glycogen, fat, protein — not one kcal number),
**carbon-monoxide saturation**, **what is in the gut** (poison, bad meat), **infection and fever**,
**fatigue**, **consciousness**. None of them is a hit-point total. Each is a real quantity, and a
person dies when one crosses its real threshold.

**What kills, and how fast** (real clocks; the numbers are data first, tuned by probes after):

| what fails | what the body does on the way | how fast it can kill |
|---|---|---|
| **blood volume** — about 70 mL/kg, ~5 L in a 70 kg adult | up to 15% lost: nothing shows · 15–30%: fast pulse, anxiety · 30–40%: falling blood pressure, confusion · over 40%: unconsciousness (the ATLS classes) | minutes from an artery; hours from a venous cut left alone; a broken thigh bone bleeds 1–1.5 L inside the leg with no wound to press |
| **core temperature** | shivering; then clumsiness and confusion; shivering stops; unconsciousness; the heart stops (the WMS staging behind document 08's bands) | a night, badly dressed and unsheltered; about an hour in ice water |
| **carbon monoxide** | headache and nausea; dizziness and confusion; collapse | 200 ppm: a headache in 2–3 hours · 800 ppm: dizziness and nausea within 45 minutes, death in 2–3 hours · 1,600 ppm: death within an hour |
| **a wound's infection** | red, hot and swollen, then pus and a smell, then fever, then spreading — 24–72 hours to show on a dirty wound, 12–24 on an animal bite; tetanus 3–21 days (about 8 on average) | days |
| **inside the skull** | a head strike, a lucid spell, then a fast decline (an epidural bleed; 20–50% of them have the lucid interval) | hours |
| **the chest** | broken ribs make every breath hurt, so breathing goes shallow, and pneumonia follows within the week | days |
| **the gut** | water hemlock: seizures within the first hour; botulism from the bulged can: weakness and paralysis from about a day on; spoiled or raw meat: vomiting and diarrhoea from half an hour to days later, spending water | hours (hemlock) to days |
| **hydration** | document 09 §4.6 | about three days |
| **energy** | document 10: weakness, then cold | weeks — the cold takes a starving body first |

**Where injuries come from** (a floor; each source's system owns how it delivers the wound):

| source | what it does to a part | owned by |
|---|---|---|
| the crash | the starting draw (§4.2) | document 16 |
| a person with a stick, a spear, a knife, a rock | `heft` bruises, breaks bone, concusses; `edge` cuts; `point` punctures — small, deep and dirtier than it looks; what covers the part changes what gets through | **the combat design, to be written** |
| the bear and the other animals that act | claws cut and tear; a bite punctures and crushes; a moose's kick or trample breaks bone. Every animal wound is heavily contaminated | document 23 and **the animal-behaviour design, to be written** |
| a fall — the cornice, the climb, a slip on the ice | a sprain, a break, a head strike. **Lethal places injure, never kill outright; fitness matters; the dice roll is announced** (Andrew, 2026-09-17) — the wound then runs its own real clock, which the party can answer | documents 01 §7 and 13 |
| cold air on a part | the part's `heat` falls: fine work goes when finger skin is below about 15 °C, the part is numb below about 7 °C, and it freezes below about −0.5 °C | document 08 (extremities); **the heat design** |
| cold metal and cold fuel | contact frostbite: bare skin on cold metal loses heat fast; avgas or oil below freezing is still liquid and freezes skin almost at once as it evaporates | **the heat design** |
| wet, cold feet above freezing | **non-freezing cold injury** (trench foot): numb, swollen, then painful — usually after two or three days wet and cold at 0–15 °C, in as little as 10–14 hours. October's own cold injury, before it is ever cold enough for frostbite: the townie's sneakers | **the heat design**; document 08 (wet) |
| cold water — through the ice | cold shock and gasping in the first minute; about ten minutes of useful movement; about an hour before hypothermia takes consciousness (Giesbrecht's 1-10-1). Out of the water, wet clothes in the wind keep spending heat | document 13 (the ice); **the heat design** |
| heat | burns: skin is damaged above about 44 °C, slowly at first and almost at once as the temperature climbs — a hot stone held too long, the boiling pot, the fire | document 07; **the heat design** |
| the air in a closed space | carbon monoxide from a fire in the fuselage; smoke; toxic smoke from burning foam (document 07's foam warning) | **the heat design** (the plane's openings and internal air) |
| the gut | the hemlock root and the baneberry (document 23), the bulged can, spoiled or raw meat, fuel-tainted water (document 09) | documents 10, 23, 09; **the food-state and spoilage design, to be written** |
| the eyes | snow blindness (§6 Q5), smoke, sparks from the ferro rod or the hatchet on quartz | this document |
| work | blisters from the bow drill, splinters, cuts from torn aluminium, a strained back | the activity that caused it (document 06) |

**The animals are real animals.** Alaska's record for brown bears (1986–1996) is about 2.75 people
injured and 0.42 killed a year: a bear injures far more often than it kills, and a defensive attack
usually ends when the person stops being a threat. Most fatal black-bear attacks were predatory
(Herrero et al. 2011), and those do not stop. In October the bears are feeding hard before they den.
How each animal decides is the animal-behaviour design's; what its claws and teeth do to a body is
this table's.

**October decides which cold injuries come first.** Fairbanks in October averages about 0 °C by day
and −9 °C by night (NOAA normals), and the storm deepens it day by day. Frostbite from air alone
needs a wind chill near −28 °C to strike in half an hour (the National Weather Service chart), so early
in the run the cold injures through **wet** (hands and feet soaked in wet snow, overflow, the ice),
**contact** (metal, fuel), **immobility** (the injured and the sleeping) and **tight boots** — and the
air takes over as the ladder climbs. That is the real order, and the world teaches it by happening
in it.

**Real-world sources for this section and §6:**
- Wilderness Medical Society, *Clinical Practice Guidelines for the Prevention and Treatment of
  Frostbite: 2024 Update* (McIntosh et al., Wilderness & Environmental Medicine, 2024) — rewarming at
  37–39 °C, no rubbing, never thaw what may refreeze, ibuprofen in the field.
- Wilderness Medical Society, *Practice Guidelines for Basic Wound Management in the Austere
  Environment* (Quinn et al., 2014) — irrigate early with drinkable water, add nothing; leave grossly
  contaminated wounds open and packed.
- Wilderness Medical Society, *Out-of-Hospital Evaluation and Treatment of Accidental Hypothermia:
  2019 Update* (Dow et al.).
- American College of Surgeons, ATLS classes of haemorrhage (blood volume ~70 mL/kg); femur fracture
  blood loss of 1,000–1,500 mL (trauma literature, e.g. *Injury*, 2022).
- Stop the Bleed / American Red Cross — direct pressure, packing, hold pressure (minutes; 10 or more
  for a heavy bleed); tourniquets considered safe to about two hours, worse outcomes past four
  (scoping review, *Injury*, 2023); improvised tourniquets often fail when too narrow.
- CDC — tetanus incubation 3–21 days (Pink Book ch. 21); staphylococcal food poisoning 30 minutes to
  8 hours, heat-stable toxin; *C. perfringens* 6–24 hours. StatPearls — *Pasteurella* infection within
  24 hours of a bite.
- OSHA confined-space handout, *Effects of Carbon Monoxide at Different Concentrations*.
- Giesbrecht's 1-10-1 principle of cold-water immersion.
- Moritz & Henriques, *Studies of Thermal Injury II* (Am. J. Pathology, 1947) — burn threshold ~44 °C.
- The College of Optometrists and the American Academy of Ophthalmology — photokeratitis shows 6–12
  hours after exposure and heals in 24–48; fresh snow reflects up to 80–90% of UV.
- UpToDate / *Nonfreezing Cold Injury (Trench Foot)* — 0–15 °C, days (as little as 10–14 hours).
- Occupational studies of hand cooling — marked loss of dexterity below ~15 °C finger skin; numb
  below ~7 °C; tissue freezes at about −0.55 °C; supercooled fuel causes instant frostbite.
- National Weather Service wind chill and frostbite chart; NOAA climate normals for Fairbanks
  (October: 31.9 °F high, 16.5 °F low).
- Smith & Herrero, *Human–bear conflict in Alaska: 1880–2015* (Wildlife Society Bulletin, 2018); the
  1986–1996 Alaska brown-bear rate of about 2.75 injuries and 0.42 deaths a year as cited in the Alaska
  bear-deterrent studies (Smith et al.); Herrero et al., *Fatal attacks by American black bear on
  people: 1900–2009* (J. Wildlife Management, 2011).
- Epidural haematoma and the lucid interval (AMBOSS; StatPearls); pneumonia after rib fractures
  (*Am. J. Emergency Medicine*, 2019).
- NSAIDs and platelets (Schafer, J. Clin. Pharmacology, 1995); NSAIDs and acute kidney injury when
  dehydrated (National Kidney Foundation); alcohol, skin vasodilation and blunted shivering.

---

### The `make a splint` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | a splint |
|---|---|
| `goal` | a splint · a bandage · to stop the bleeding |
| `vague` | "How are you going to splint it?" / "…stop the bleeding?" |
| `roles` | **rigid**: a rod, a board, a stick · **binding**: cordage, a strip, tape · **wound**: the named wound |
| `realize` | `bind <wound> with <rigid> and <binding>` — the ordinary wound operations; a wrong pairing gets the physics (a strip alone will not hold a bone) |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

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
- *(Claude, 2026-09-26, for Andrew's check — the systems injury now also depends on:)*
  - **the combat design** *(to be written)* — blows, cuts and stabs, delivered as wounds on parts;
  - **the heat design** *(to be written)* — `heat` on every body part, contact heat and cold, burns,
    the plane's openings and internal air (carbon monoxide, smoke);
  - **23 Flora and fauna** and **the animal-behaviour design** *(to be written)* — the bear's and the
    other animals' attacks; the poisons;
  - **the food-state and spoilage design** *(to be written)* — what raw, frozen, cooked and spoiled
    food does in the gut;
  - **01 / 13** — the lethal places and the ice, which deliver wounds and never kill outright.

**These depend on it:**
- **10 Food and hunger** — starvation weakness; the bulged can; cleaning game with a blade.
- **12 The pilot and bodies** — tending him is first aid that cannot work, and costs real time and
  warmth. *(superseded 2026-09-26: he starts the run dead (2026-09-17). What document 12 takes from
  this one now is the body as an entity with parts and states (§4.6) — the same for the living and
  the dead.)*
- **14 Rescue paths** — an injured party walks slower, climbs worse, and carries less; the walk-out
  is gated on who can move.
- **15 Moral and social layer** — the bandage, the painkillers, who gets carried, and whether the
  party leaves someone.
- **19 Multiplayer** — carrying a person is the co-op act with the highest price.

---

## 6. Open questions

**Re-reviewed 2026-09-26 (Claude, `PLAN.md` A9), for Andrew's check:** Q1, Q3, Q7, Q8, Q9 and Q10 are
answered from real medicine and the decided design; Q2, Q4 and Q5 were wrong-headed (a shrunken kill
list, a shortcut, a cut question) and are rewritten and answered; **Q6 is Andrew's** — whether a
character's trade changes what their hands do. The originals are kept, struck, as the record.

~~1. Does injury use hit points at all? *(a)* Named wounds only, with severity. *(b)* A health total
   behind them. Recommendation: (a).~~ **Claude's answer (2026-09-26), for Andrew's check:** no — a
   body has no hit points, so the game has none. A person is an entity with parts, each part with its
   own states (`heat`, `wet`, `frozen`, `wounds`, `pain`, `swelling`, `covered_by`), and the whole body
   carries the real quantities that decide life: blood volume in millilitres, core temperature,
   hydration, energy, carbon-monoxide saturation, what is in the gut, infection and fever, fatigue,
   consciousness (§4.6). A person dies when one of those crosses its real threshold, of whatever
   caused it — the run ends in death "of anything" (Andrew, 2026-09-26). The combat system is built
   on this, not beside it: a spear thrust is a `point` wound to the part it reaches, through what that
   part wears; a stick is `heft` — a bruise, a break, a concussion; the bear's claws are `edge`, its
   bite a puncture and a crush. What MUD-like combat *feels* like — the exchange of blows in lines,
   its pace, breaking off and running — is the combat design's to write; that every blow resolves
   into a named wound on a body part is this document's rule. `status` and `examine` read it all back
   in band words, never numbers (document 08 §4.9).
~~2. What kills, and how fast? Recommendation: bleeding can kill in hours if nothing is done,
   infection kills in days, and everything else disables rather than kills.~~ *(Rewritten
   2026-09-26: "everything else disables rather than kills" shrank the world — the run ends when they
   die, of anything, and in real life a great deal kills inside a week.)* **Claude's answer
   (2026-09-26), for Andrew's check:** whatever really kills, on its real clock — §4.6 has the table
   and the sources. Arterial bleeding in minutes; a venous cut in hours if nothing is done; a broken
   thigh bone by bleeding inside the leg; infection in days; a fall through the ice in about an hour
   (cold shock, then ten minutes of useful movement, then hypothermia — the 1-10-1 principle); carbon
   monoxide in hours, or in minutes when it is dense; the cold in a night; a bleed inside the skull
   in hours after a lucid spell; the hemlock root in hours; thirst in about three days (document 09).
   The bear and a person with a spear can kill, because violence resolves with real physics
   (2026-09-16) — though a bear, in Alaska's own record, injures far more often than it kills. **Places
   are the exception Andrew set: lethal places injure, never kill outright** (2026-09-17). The cornice,
   the climb and the thin ice deliver a wound — a break, a head strike, an immersion — and that wound
   then runs its own real clock, which the party can answer. The ladder's thesis, that a body that
   can't work can't stay warm, stays true as one way of dying among many.
~~3. Is `press` its own operation? Recommendation: yes — the first-minute act for the townie's arm.~~
   **Claude's answer (2026-09-26), for Andrew's check:** yes. Direct pressure is the first thing every
   bleeding-control course teaches (Stop the Bleed, the Red Cross), and it needs nothing but a hand.
   It is an **attended activity** (document 06): while it is held the wound's bleeding rate falls;
   lifting early lets the bleed restart; held long enough — minutes, ten or more for a heavy bleed — a
   clot holds and the hand can come away. The acts around it are each their own operation, because
   each does something different to the wound: **`press`** (a hand or a pad on it — `press the cut`,
   `press the gauze on Mara's arm`); **`pack`** (stuff gauze or cloth — the tampons in the townie's bag
   — into a deep wound that pressure on the surface cannot reach, then press); a **pressure dressing**
   (`bind` or `wrap` tight over a pad, which frees the hands); a **tourniquet** (`tie` a wide band above
   a limb wound and `twist` a rod through it to tighten — seatbelt webbing is the right width; string
   or wire cuts in and fails; and past about two hours a tourniquet starts killing the limb it saves);
   and **`elevate`**. Canonical words and their synonyms are authored together (document 04 §3.7):
   press · apply pressure · hold · push on.
~~4. Do wounds need a `clean` step, or does the tool's dirt just carry? Recommendation: the dirt
   carries … one rule, no new subsystem.~~ *(Rewritten 2026-09-26: "one rule, no new subsystem"
   collapsed a real process into a shortcut, and cleaning is the act that most changes a wound's
   outcome.)* **Claude's answer (2026-09-26), for Andrew's check:** a wound carries
   **`contamination`** as a state — how much and of what: crash grit, cloth fibres, soil, avgas, an
   animal's mouth — set by what made it (a bite or a claw is always dirty; a clean slice from the
   razor barely is). **Infection is a process on the wound** that grows from that contamination over
   real hours, deterministic and seeded (DR-12): a dirty wound shows redness, heat and swelling in
   24–72 hours (an animal bite in 12–24), then pus and a smell, then fever — which spends water and
   warmth — and, untreated, spreads. Cleaning is its own set of real operations: **irrigate** — pour or
   squirt drinkable water into it, in millilitres (document 09), harder if you pierce a bag or a
   bottle cap; the Wilderness Medical Society's guideline is that drinkable water is enough and nothing
   should be added; **pick out** grit and splinters with a point (the multitool, a clean knife tip);
   and scrub the skin around it. Whisky and sanitizer are alcohol: they clean a blade and intact skin,
   but in the wound they kill tissue as well as germs and hurt badly — a real act, worse than clean
   water. Whatever covers the wound carries its own contamination as provenance, the way a vessel does
   (document 09 §4.6): a boiled strip is clean; the shirt you slept in is not. And **closing** a dirty
   wound traps it — the guideline leaves a grossly contaminated wound open and packed — so the nurse's
   suture kit is a real choice with a real downside, not a finish line. Boiling a strip or a blade is
   the heat design's (to be written).
~~5. Do frostbite, snow blindness and carbon monoxide stay? Recommendation: frostbite yes; carbon
   monoxide yes; snow blindness only if the ice days are long enough to earn it.~~ *(Rewritten
   2026-09-26: "stay or go" was a cut question; all three are real here, so they are in — and the
   list was short.)* **Claude's answer (2026-09-26), for Andrew's check:** all three are in, each by
   its physics, and more besides.
   - **Frostbite** is a part's `heat` below about −0.5 °C (document 08's extremities; the heat
     design). The care is the survivor's act, and real: rewarm against warm skin (an armpit, a belly)
     or in water at 37–39 °C; never rub; and **never thaw a part that may freeze again** — refreezing
     is worse than staying frozen, so a party that must walk on frozen feet may be right to walk first
     (WMS frostbite guidelines, 2024). The nurse's ibuprofen is real field treatment for frostbite.
     Blisters come in the hours after rewarming; dead tissue takes weeks to show, longer than the run.
   - **Snow blindness** is a dose of UV on the eyes: the sun (by date, hour and cloud) × the snow's
     reflection (fresh snow reflects up to 80–90%) × the hours unprotected. It shows **6–12 hours
     later** — typically waking in the night with burning, gritty eyes — and heals in a day or two in
     the dark. In October at this latitude the sun is low and weak, so it is rare, and likeliest on a
     clear day on fresh snow out on the open ice. The kid's sunglasses are one answer among real
     ones: slit goggles cut from bark, cardboard, leather or cloth, and soot under the eyes. Not a
     gotcha — physics with improvisable answers.
   - **Carbon monoxide** is a gas in a zone's air. A fire in a closed space makes it — a smouldering
     or banked fire more than a bright one — the plane's openings let it out (the plane as an entity
     with openings open or closed, Andrew, 2026-09-26), and a body takes it up and gives it back only
     slowly, over hours of fresh air. Headache and nausea first, then confusion, then collapse (§4.6's
     table). It is why blocking every gap is not free, and why a banked fire overnight in a sealed
     fuselage is the killer it really is. Owned by the heat design (the air in enclosed zones).
   - **Added, because they are real here** (§4.6): non-freezing cold injury — October's own; contact
     frostbite from metal and fuel; cold-water immersion; burns and scalds; smoke; bites and
     maulings; blows and stab wounds; poisoning; blisters, splinters and cuts from the wreck.
6. **Does a character's trade change what their hands can do?** *(Sharpened 2026-09-26 — the old
   question was "what does the nurse's knowledge actually do?", recommending nothing mechanical.)*
   What you are deciding: whether **who the character is** changes the outcome of a typed act,
   separately from what the **player** knows. The player's knowledge is the player's either way —
   nothing ever tells anyone what to do (never a menu), and `players-and-kit.md`'s "she knows how; the
   player has to" stands. *(a)* Nothing mechanical: the nurse is a nurse only in her description, and
   her stitch is exactly the salesman's. *(b)* **Trained hands**: a character's trade makes the acts of
   that trade faster and better — the nurse's stitches close neater and cleaner and take less time, her
   splint holds; the guide's snare sits right and the guide's fire catches sooner — shown only in the outcome
   ("the edges meet neatly"), never as advice. *(c)* Trained hands and a trained eye: her `examine` of a
   wound also reads more (how deep, how dirty). **Recommendation: (b).** It is how it really is — a
   nurse's hands are better at wound care than a salesman's — it is the same kind of thing as the
   fitness you already put in (2026-09-17), it applies to an agent exactly as to a human, and it never
   hands anyone a solution. (c) edges toward telling the player what a wound needs, which is what a
   hint must never do.
~~7. Can a player be carried? Recommendation: yes, as a slow, two-hands, warmth-expensive
   activity.~~ **Claude's answer (2026-09-26), for Andrew's check:** yes, in every real way, because a
   person is an entity with a mass and the carrying rules already exist (document 04 §3.11: capacity
   is what you hold, wear and haul; the load feeds travel time). **`carry`** on the back or over the
   shoulders is one strong person, a short way; **two people** can carry one between them; **`drag`**
   by the shoulders or the jacket works on snow; and a **litter or sled** — a seat frame, the
   panelling, a tarp or a blanket between two poles — dragged over snow hauls a person much farther for
   the same effort, which is why it is the real answer (the world design already has "a drag litter of
   paneling and cord"). The price is not what the old recommendation said: carrying makes the
   **carrier** hot and sweating — the deferred cold debt (document 08 §4.2) — while the **carried**
   person, not moving and often lying on snow, cools fast and needs insulation under and around them.
   Moving an unsplinted break grinds the bone ends: pain, more bleeding, damaged nerves. Two people
   carrying one needs a co-operative form in the grammar (two actors on one entity), which is
   documents 04 and 19 to write.
~~8. Does painkiller masking get modelled? Recommendation: yes, and honestly.~~ **Claude's answer
   (2026-09-26), for Andrew's check:** yes, and honestly, because pain is a state on the part (§4.6)
   and it is part of what limits the part. Ibuprofen — the nurse's pouch holds a count of tablets —
   works in 30–60 minutes and lasts four to six hours; it lowers pain and swelling, and `status`
   truthfully reports less pain while the wound is unchanged: that is the fair lie. How much the part
   gives back depends on the wound — a sprain's limit is mostly pain, so the nurse walks better; a
   broken bone's limit is mechanical, so no pill makes it bear weight. Its real prices: it slows
   clotting (the bleeding townie should not take it), and taken while dehydrated it can injure the
   kidneys (document 09's clock). It is also the field treatment for frostbite. Whisky dulls pain
   and judgment, and it opens the skin's blood vessels and blunts shivering, so it costs heat — the
   brandy-in-the-snow cure is a myth. Willow-bark tea (document 23) is a weak real painkiller.
~~9. How does the concussion's confusion read without hijacking commands? Recommendation: unreliable
   description, never unreliable input.~~ **Claude's answer (2026-09-26), for Andrew's check:** by what
   the body really does, and never by doing something the player did not type. A concussion is
   headache, nausea, dizziness, light sensitivity, fatigue and slowness — not a world that looks wrong
   — so the salesman's first day is slower acts (activities take longer, document 06), more fine-work
   failures, lines of headache and nausea, and a pull toward sleep; the room reads true. Hypothermia's
   confusion (document 08's `impaired` band) is clumsiness and poor judgment: the fumbled match, the
   knot that will not hold, the slurred word. So the rule: **the body can fail at an act** — fumble it,
   slow it, collapse, lose consciousness (a missing member is already incapacitated where they lie) —
   **but the engine never performs an act the player did not type.** Severe hypothermia's paradoxical
   undressing is real — the dying feel hot and strip — and it arrives as a felt urge in the prose
   ("the parka is unbearable"); taking it off is the player's choice. *(Andrew's to overrule if he
   ever wants the engine to act for a character.)*
~~10. Does `examine <someone else>` show their wounds? Recommendation: yes, what is visible.~~
   **Claude's answer (2026-09-26), for Andrew's check:** yes, by the senses, the way the tell/hide rule
   works for everything else (document 03 §4.3: the worn layer is what shows). **Looking** shows what
   the covering allows — blood through a sleeve, a limp, a white patch on a bare cheek, a leg at the
   wrong angle, pallor, shivering; what is under a glove or a boot stays hidden until someone takes it
   off, which costs that part its heat. **Touch** gives heat — a hot forehead is a fever, a cold hand is
   cold — swelling and a pulse; **smell** gives an infected wound away. Wounds and parts carry this in
   their `sensed` rows (document 05 §4.5). Asking is speech, and the person can answer truly or not.
   Each is its own act: `examine Mara`, `examine Mara's hand`, `feel Mara's forehead`, `take the glove
   off Mara's hand`.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18:** the `make a splint` goal rows added (document 04 §3.9 owns the form and the dispatch rule).

- **2026-09-26 (Claude, self-review — PLAN.md A9):** re-reviewed against block 1 (03–09), the decisions
  since (combat, the bear, October, lethal places injure, extremities' own cold, body parts carry heat,
  the pilot dead at the start) and real medicine and wilderness first aid, with sources (§4.6). **Added
  §4.6** — the body as an entity with parts and per-part states, the real clocks of what kills, and
  every source of injury with the system that owns it. **Answered, for Andrew's check:** Q1 (no hit
  points — parts, states and real body quantities; combat resolves into wounds on parts), Q3 (`press`
  is an attended operation, with `pack`, the pressure dressing, the tourniquet and `elevate` as their
  own), Q7 (carry, drag, two-person carry, the litter; the carrier sweats and the carried cools), Q8
  (ibuprofen honestly, with its real prices; whisky costs heat), Q9 (the body fails at acts, the engine
  never performs one), Q10 (by the senses, through what is worn). **Rewritten and answered:** Q2 (the
  "everything else disables" kill list shrank the world), Q4 (the "one rule" shortcut — contamination
  and infection are states and processes, cleaning is its own operations), Q5 (a cut question — all
  three stay, plus non-freezing cold injury, contact frostbite, immersion, burns, smoke, maulings).
  **Left for Andrew:** Q6, sharpened — whether a character's trade changes what their hands can do.
  Rules 1–5, the draw's concussion and shock rows, §4.4, §4.5 and §5 annotated; the pilot-alive lines
  marked superseded. Needs design documents: combat, heat (including the air in closed zones), animal
  behaviour, food state and spoilage.

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
  document 12). *(superseded 2026-09-26: since 2026-09-17 he starts the run dead, so the shipped
  `dead: True` start is correct.)*
- *(Claude, 2026-09-26:)* No body parts as entities, no per-part `heat`, no blood volume, no
  contamination or infection process, no combat, no animal attacks, no carbon monoxide.
