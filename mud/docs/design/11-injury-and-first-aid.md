# 11 — Injury and first aid: wounds, bleeding, infection, frostbite, splints, the med pouch

> **Status: reviewed with Andrew 2026-09-27 and 2026-09-28.** **Architecture counterpart:** none. This system had no design document
> of its own before this one.

## 2. Decisions

### Andrew's decisions
- **(2026-09-07, 2026-09-28)** Each player starts with a different injury draw, as with clothing and
  pockets, and you do not choose what the crash did to you — but the start is light: nobody is crippled
  or hindered for the sake of it. Most wake with minor bumps and bruises; one has a cut, which sends the
  party looking for bandage material, and one a concussion (§4.2).
- **(2026-09-07)** Decisions across the moral spectrum (Andrew's examples: eating the pilot, stealing,
  hitting, killing). *(Claude's, not yet decided: the injured are one of the places this lands — who gets
  carried, who gets the bandage, who gets left by the fire.)*
- **(2026-09-16, 2026-09-26)** No lethal-consent gate; violence resolves with real physics, and there is a
  combat system like a MUD's — stab with a spear, beat with a stick. Wounds are wounds whoever caused
  them; the engine does not soften a blow.
- **(2026-09-17, 2026-10-02)** Dangerous places injure — a fall may break a limb — but never kill
  outright; fitness matters; chance is never shown as dice — the player reads what happened, and the tutorials explain that success mixes chance with the character's stats (2026-10-02) (document 01).
- **(2026-09-17)** The pilot starts the run dead, so the party's first patients are each other.
- **(2026-09-17, 2026-09-27)** The endings are rescued or dead; the run ends when they die. Dead players
  are ghosts.
- **(2026-09-18)** The extremities have their own cold, for frostbite (document 08). There is a `status`
  screen that reports injuries in band words (document 08 §4.9).
- **(2026-09-26)** Body parts carry heat as part of their ontology; heat is a state system. The bear,
  some bigger animals and a few birds act (document 23).
- **(2026-09-26, 2026-09-27)** The season is the first week of October in interior Alaska; the week's
  numbers are document 13 §4.2's.
- **(2026-09-27)** **Nothing kills instantly.** Death is realistic and can come fairly fast, but always
  by the body running down — blood loss, the cold, thirst, a wound gone bad and the rest, each on its
  real clock — so a player always has time to respond. The bear and a knife kill through the bleeding
  they cause: a mauled person lies there bleeding, can play dead, and may or may not make it back. A
  body already near its end can go almost at once, never in one instant. Poison makes people very sick
  but never kills.
- **(2026-09-27)** **Characters differ in how well and how fast they do things.** A character's success
  and the time an act takes depend on who they are — a woodsman lights fires better, and a nurse's
  hands are better at wound care. It shows in the outcome and in subtle cues in what the character notices — never a "do this"
  hint (2026-10-02); the player still has to know what to do. It lives on a hidden skill sheet that starts from the seat and rises with practice
  (document 16 §4.1, 2026-10-02).
- **(2026-09-27)** **No hit points.** A wound is a named thing on a body part — a kind, a severity,
  bleeding or not, bound or not, and later infection — and each part has its own heat, wetness, pain
  and covering (§4.1, §4.6).
- **(2026-09-27)** **Players see meters** for what a person can sense about their own body: people are
  not cut off from their own senses. Seven bars with no numbers — hunger, thirst, warmth, rest, pain,
  stamina and blood (document 08 §4.9); a wound is never a meter.
- **(2026-09-27)** **A blow wounds only when it would really hurt.** Common sense and real physics
  decide: a feather does nothing; a spear thrust punctures.
- **(2026-09-27)** **Combat is roughly a MUD's, changed to suit this game.** Nothing in it is
  automatic: each attack is typed, like any other act. No attack hits automatically either: as in D&D,
  whether it lands depends on the fighters' stats and on chance, never shown as dice — the player
  reads what happened. The body at that moment decides the blow: skill; cold hands, pain, tiredness and
  stamina; the weapon; what the target wears. Every attack has a recovery, and the game says when it
  is over. The rest is `PLAN.md` §5 until the combat document is written.
- **(2026-09-27)** **Bleeding spends a real blood volume** — about 70 mL per kilogram, some 5 L in an
  adult — on the real clocks: a cut vein over hours, a cut artery in minutes, a broken thigh bone
  inside the leg. Losing it drains the blood meter, and the world says so too, in the real order —
  feeling faint, light-headed, confused; a body short of blood makes less heat. What stops a bleed has to match it (§4.1 rule 2, §4.6). The clocks stay
  real at the game's 15×: a cut artery leaves seconds of real time.
- **(2026-09-27)** **Whisky in a wound and over the needle are in** — the film scene — with their
  real result; boiled or iodine-treated water rinses a wound (§4.1 rule 4, §4.8).
- **(2026-09-27)** **No snow blindness**: the sky is always at least partly cloudy. **Carbon monoxide
  builds only where a space does not breathe enough for its fire** — by real physics: a small fire in
  a can with some ventilation is different from a big one in a sealed plane (§4.4).
- **(2026-09-28)** **The body as an entity with parts and states** (§4.6) — the same for the living,
  the pilot and a dead player; every source of injury on its real clock. **The cold hurts above all
  through getting wet — the whole body**: breaking through the ice, the flurries, the creek, and sweat,
  which keeps you warm while you work and chills you once you stop.
- **(2026-09-28)** **A person can be carried in every real way** — on the back, by two, dragged, on a
  litter or sled — at a real cost to both (§4.9). The mechanics of one player helping another drag or
  carry are still to be worked out (documents 04 and 19).
- **(2026-09-28)** **Painkillers mask pain honestly** — the pain meter falls while the wound is
  unchanged — and a side effect too small to matter in a week is not modelled: ibuprofen's cost is the
  tablets and who gets them (§4.10).
- **(2026-09-28)** **The body can fail at an act, but the engine never performs an act the player did
  not type** — a concussion or hypothermia reads as what the body really does (§4.11).
- **(2026-09-28)** **Another person's wounds are known by the senses** — touch, smell and sight. A
  serious condition shows in the person's line in the room; the body's signs (a cough, a wince,
  shivering) arrive as emotes; examining or looking at the person reveals the smaller things you would
  not see from across the room (§4.12).
- **(2026-09-27)** **Each real first-aid act is its own act** — press (held, an activity that ties up
  the hands), pack, a tight bandage, a tourniquet, raising the limb, rinsing, picking out grit,
  rewarming, splinting, stitching, carrying and dragging — each with its everyday names (§4.1 rule 5,
  §4.7).

### Proposals (Claude)
Every number here is a real starting point, from the sources at the end of §4.6, and playtesting tunes
it.

## 3. In one paragraph

Everybody wakes up sore — bumps and bruises — and two of you are really hurt. The cut forearm is
bleeding into a sleeve and will keep bleeding until somebody presses it and binds it, which sends the
party looking for anything that will do as a bandage; the concussion makes one person's first day slow
and sick. Nobody is crippled: the crash gives the party its first job, not a handicap. None of it is a
debuff you read off a sheet — it is your own description when you look at
yourself, and it is the reason the party has to decide who does what. The nurse has a pouch with gauze
and tape and sutures in it, and her hands are quicker and surer at wound care than anyone else's — but
the person playing her still has to know what to do, like everyone else. Later the wounds that were
dressed with a dirty shirt start to matter, and the fingers that spent an afternoon bare on cold metal
start to matter, and first aid stops being a one-off act and becomes a thing you keep doing.

## 4. The design

### 4.1 The rules

1. **Wounds are named things on a body part; there are no hit points** (2026-09-27). A body has none,
   so the game has none. The shipped shape is `{part, kind, severity, bleeding (grams per minute, 0 =
   none), bound?, infected_at, note}`, and a person has a list of them. A wound is a state on a body
   **part**, and the part is an entity with its own heat, wetness, pain and covering (§4.6); a wound
   gains `contamination` and `pain`, and `infected_at` becomes the state of the infection process
   (§4.8). **A blow wounds only when it would really hurt** (2026-09-27): what struck, how hard, where
   it landed and what that part wears decide it, by common sense and real physics — a feather does
   nothing, a shove may only knock someone off their feet, a punch through a parka may not even bruise,
   a spear thrust punctures what it reaches, the bear's claws cut and tear. How a fight plays is the
   combat design's (§5); what a blow that lands does to a body is this document's.
2. **Bleeding is a process, and blood loss kills** (2026-09-27). Bleeding spends **blood volume**, in
   millilitres — about 70 mL per kilogram of body weight,
   some 5 L in a 70 kg adult — and a body short of blood makes less heat, so it costs warmth too.
   Pressure slows it while it is held; a pressure dressing or packing holds it after; a tourniquet stops
   a limb's arterial bleed (§4.7). A binding stops only a bleed it is equal to: arterial blood soaks
   straight through a strip.
3. **Infection is a process on the wound** (2026-09-27), seeded (DR-12) so a run replays identically,
   and driven by the wound's contamination, how it was cleaned and what covers it (§4.8). Then fever,
   which costs warmth and water, and, untended, a spread into the blood that kills on its real clock of
   days — never at once, like everything that kills.
4. **Medicine is systemic and improvised, never a recipe.** Cloth becomes a bandage; seatbelt webbing
   becomes a tourniquet or a splint tie; branches, aluminium frames or poles become splints; alcohol
   cleans a blade and intact skin; boiling water or a flame cleans some metal tools; snow reduces
   swelling and worsens cold exposure; painkillers improve function and mask danger; moving an injured
   person can save them from the cold and worsen the injury. Every one of those is a trade, and none of
   them is a crafting recipe. **Whisky poured into a wound, and over the needle before stitching, are
   in** (2026-09-27) — the scene everyone knows from the films — with their real result: poured into
   an open wound, alcohol kills tissue as well as germs and burns badly, and the Wilderness Medical
   Society's guideline is to irrigate with plain drinkable water and add nothing, so a rinse cleans the
   wound a little better. The world tells it by what happens, never by a warning.
5. **Treatment is an act on a wound, with a tool.** `press`, `bind` / `wrap`, `splint`, `stitch`,
   `clean`. The wound is the target; what you use is whatever physically serves. The floor grows with
   the real acts, each its own operation because each does something different to the wound
   (2026-09-27) — `pack`, a tourniquet (`tie` a band above the wound, `twist` a rod
   through it), `rinse` / irrigate, pick out the grit, `elevate`, rewarm a frozen part, `carry` and
   `drag` a person (§4.7–§4.9).
6. **The injury is in the description.** `examine me` reads your wounds back to you in plain words —
   this is shipped: *"Your forearm is cut and bleeding."* The `status` screen
   reports them too, in band words, never numbers, and the meters show what the body feels at a glance
   (2026-09-27; document 08 §4.9). A wound is never a meter: it is named.
7. **Never a menu, and common sense is hinted.** The game does not tell you to press the wound, does
   not list the med pouch's contents when you are bleeding, and does not name the tourniquet. It says
   the sleeve is soaking.
8. **Trained hands** (2026-09-27). A character's trade changes how well and how fast they do the acts
   of that trade: the nurse's stitches close neater and cleaner and take less time, and her splint
   holds. It shows in the outcome (*"the edges meet neatly"*) and in subtle cues in what the character
   notices, never as a "do this" hint (2026-10-02), and it applies to an agent exactly as to a human.

### 4.2 The starting draw (content — shipped in `characters.py`)

| slot | injury | what it costs |
|---|---|---|
| the guide | minor bumps and bruises | sore for a day or two; nothing it stops |
| the townie | a cut forearm, bleeding | bleeding through the sleeve; press it, bind it — the party's first search is for something to bind it with |
| the nurse | minor bumps and bruises | sore for a day or two; nothing it stops |
| the salesman | concussion | tires fast; the first day is slow — headache, nausea, dizziness, light hurts, slower acts (§4.11) |
| the kid | minor bumps and bruises | sore for a day or two; nothing it stops |

The start is light on purpose (2026-09-28): nobody is crippled or hindered for the sake of it. The cut
gives the party its first job — find something to bind it with — and the concussion slows one person's
first day; everyone else is only sore. The seed permutes which player draws which slot, so no player is
always the townie. A seat nobody plays is a dead character
(document 12 §4.4), so its injury never runs.

### 4.3 Ways to treat a wound (a floor — the loops add more)

| way | what it spends | where | the chain |
|---|---|---|---|
| **the first-aid kit** (bandage, tape) | search | the forward bin in the mid cabin — pry-gated | `press wound` → `wrap arm with bandage` |
| **improvised** (a torn-up shirt or any cloth, clean water to rinse, paracord and a rod as a splint, a sewing needle and thread to stitch — boiled first) | tools + knowledge | the rear cabin, the duffel; the sewing kit in the townie's toiletry bag (document 16) | `tear shirt` → `pour water on the cut` → `wrap arm with strip` |
| **warmth for frostbite** (skin to skin, no rubbing) | warmth | any | `wrap hands in socks` · sit by the fire |

**The med pouch** belongs to a person, not the plane, and it is in the nurse's backpack behind the
jammed aft bin, not her pocket (2026-09-28): gauze pads, medical tape, ibuprofen, a suture kit
(shipped in `characters.py`). Her hands are trained; the player still has to know what to do. The
plane's first-aid kit is a bandage roll and medical tape in the pried forward bin. Whisky and hand
sanitizer are the alcohol, and both are also fuel.

### 4.4 The injury list (a floor)

The set the system honours — a floor, not a list of what can happen: **bleeding · a broken limb ·
concussion · burns · frostbite · hypothermia · infection · shock · dehydration · smoke inhalation ·
exhaustion** — and, because they are real here, **non-freezing cold injury, contact frostbite,
cold-water immersion, carbon monoxide, bites and maulings, blows and stab wounds,
poisoning, and the blisters, splinters and cuts of work in a wreck** (§4.6). Frostbite and hypothermia
are the warmth system's failures with a location; burns and smoke inhalation are fire's; dehydration
and exhaustion are the other survival clocks'.

- **Frostbite** is a part's `heat` below about −0.5 °C (document 08's extremities; the heat design). It
  whitens a finger first; bare hands and feet drive it. The care is the survivor's act, and real:
  rewarm against warm skin (an armpit, a belly) or in water at 37–39 °C; never rub; and **never thaw a
  part that may freeze again** — refreezing is worse than staying frozen, so a party that must walk on
  frozen feet may be right to walk first (WMS frostbite guidelines, 2024). The nurse's ibuprofen is real
  field treatment for frostbite. Blisters come in the hours after rewarming; dead tissue takes weeks to
  show, longer than the run.
- **Carbon monoxide** is a gas in a zone's air, and it builds only where the space does not breathe
  enough for the fire in it (2026-09-27) — real physics: the level is what the fire puts out against
  what the openings let out (the cabin's rooms have openings, open or closed, 2026-09-26). What
  the fire puts out depends on its size and how well it burns — a smouldering, banked or starved fire
  makes far more than a small bright one. A small fire in a can with a gap left open near it is how
  people really heat a shelter; a big fire in a plane sealed tight is how they poison themselves. A
  body takes it up and gives it back only slowly, over hours of fresh air: headache and nausea first,
  then confusion, then collapse, and, left to build, death — by the level rising in the blood over
  hours, never at once (2026-09-27). A body getting worse wakes a sleeper, as the cold does (document
  06), so there is time to respond. It is why sealing every gap is not free. Owned by the heat design
  (the air in enclosed zones).
- **Hypothermia's confusion** is clumsiness, slowness and poor judgment — the body can fail at an act,
  and the engine never performs one the player did not type (§4.11).

### 4.5 The escalation (what untreated injury does over a week)

A cut on day 1; a dirty wound shows infection in 24–72 hours (an animal bite in 12–24); fever and
spreading redness over the next days, costing warmth and water; untended, the spread into the blood
kills over days (2026-09-27). A deep, dirty wound can turn to gas gangrene within hours to three days;
the black of dead frostbitten tissue takes weeks to declare itself, longer than the run. Long before
any of it kills, it takes the labour that keeps everyone else alive. Nothing kills instantly (§4.6).

The Bodies cards of the event deck (document 13 §4.3) make it visible: a wound infects; frostbite
whitens a finger; hypothermia's clumsiness; dehydration headaches; the hunger stages.

### 4.6 The body, and everything that can hurt it

Injury has many sources — a combat system like a MUD's, a bear and other animals that
act, dangerous places, the ice, the cold in the extremities — and all of them act on the same thing:
**the body, as an entity in the ontology** (document 05 §4.5), whose parts carry states that systems
change. A living player, the dead pilot and a dead player are the same kind of entity (document 12
§4.3a).

**The body.** An `individual` with `materials` (skin, fat, muscle, bone, blood) and `parts`,
recursively: head (face, eyes, ears, nose), neck, torso (chest, belly, back), arms, hands and
fingers, legs, feet and toes. Every part carries its own states:

| state, per part | what it is | what changes it |
|---|---|---|
| `heat` | tissue temperature — body parts carry heat as part of their ontology (2026-09-26) | the core, what covers the part, wind, wet, contact (metal, snow, fuel, a hot stone), blood flow — the heat design, to be written; document 08 for the extremities |
| `wet` | grams of water on and in what covers it | document 08 §4.5 |
| `frozen` | ice in the tissue — frostbite | `heat` below about −0.5 °C |
| `wounds` | the named wounds on it, in the shipped shape (§4.1), plus `contamination` and the infection's state (§4.8) | every source below; every treatment |
| `pain`, `swelling` | what the person feels, and what limits the part | the wound, movement, cold, drugs (§4.10) |
| `covered_by` | the worn layers over it | clothing (document 08 §4.2); it is also what an onlooker can see (§4.12) |

And the whole body carries the quantities that decide whether it lives: **blood volume** (mL),
**core temperature** (document 08), **hydration** (mL, document 09), **energy** (document 10's stores —
glycogen, fat, protein — not one kcal number), **carbon-monoxide saturation**, **what is in the gut**
(poison, bad meat), **infection and fever**, **fatigue**, **stamina** (breath — spent by running,
fighting and hauling, back with a rest), **consciousness**. None of them is a
hit-point total; each is a real quantity.

**How death comes** (Andrew, 2026-09-27): **nothing kills instantly.** Death is realistic and can come
fairly fast, but always by the body running down on a real clock, so a player always has time to
respond — to press the wound, get to the fire, drink, play dead. A body already near its end can go
almost at once, never in one instant. The bear and a knife kill through the bleeding they cause: a
mauled or stabbed person lies there bleeding, and whether they make it back is the clock against what
the party does. A fall in a dangerous place injures — a broken limb — and never kills outright.

| what runs down | what the body does on the way | how fast |
|---|---|---|
| **blood loss** — blood volume, about 70 mL/kg, ~5 L in a 70 kg adult | up to 15% lost: nothing shows · 15–30%: fast pulse, anxiety · 30–40%: falling blood pressure, confusion · over 40%: unconsciousness, then death (the ATLS classes). A mauling or a stab wound kills this way | minutes from an artery; hours from a venous cut left alone; a broken thigh bone bleeds 1–1.5 L inside the leg with no wound to press |
| **the cold** — core temperature | shivering; then clumsiness and confusion; shivering stops; unconsciousness; the heart stops (the WMS staging behind document 08's bands) | a night, badly dressed and unsheltered — never night one, which costs warmth and rest but does not kill (2026-09-28); about an hour in ice water |
| **hydration** | document 09 §4.6: thirst, headache, weakness, then death | about three days |
| **a wound's infection** | red, hot and swollen, then pus and a smell, then fever, then spreading into the blood — 24–72 hours to show on a dirty wound, 12–24 on an animal bite; tetanus 3–21 days (about 8 on average) | days |
| **inside the skull** | a head strike, a lucid spell, then a fast decline into unconsciousness and death (an epidural bleed; 20–50% of them have the lucid interval) | hours |
| **the chest** | broken ribs make every breath hurt, so breathing goes shallow, and pneumonia follows within the week | days |
| **carbon monoxide** | headache and nausea; dizziness and confusion; collapse; death | 200 ppm: a headache in 2–3 hours · 800 ppm: dizziness and nausea within 45 minutes · 1,600 ppm: collapse within the hour |
| **energy** | document 10: weakness, then cold | weeks — hunger alone does not kill inside the run |

**What never kills** (Andrew, 2026-09-27): **poison** — so nobody is killed off for eating a mushroom.
Water hemlock: seizures within the first hour; botulism from the bulged can: weakness and paralysis
from about a day on; spoiled meat (a fish left too long, an animal long dead): vomiting and diarrhoea
from half an hour to days later, spending water. Very sick, never dead — hours to days.

**Where injuries come from** (a floor; each source's system owns how it delivers the wound):

| source | what it does to a part | owned by |
|---|---|---|
| the crash | the starting draw (§4.2) | document 16 |
| a person with a stick, a spear, a knife, a rock | when the blow is hard enough to hurt: `heft` bruises, breaks bone, concusses; `edge` cuts; `point` punctures — small, deep and dirtier than it looks; what covers the part changes what gets through. Whether an attack lands at all is the fighters' stats and chance (2026-09-27) | **the combat design, to be written** |
| the bear and the other animals that act | claws cut and tear; a bite punctures and crushes. Every animal wound is heavily contaminated. A defensive attack usually ends when the person stops being a threat — playing dead — and a predatory one does not | document 23 and **the animal-behaviour design, to be written** |
| a fall — the steep lee slope, the climb, a slip on the ice or on frosty rock | a sprain, a broken limb, a head strike. **Dangerous places injure, never kill outright; fitness matters; the chance is never shown as dice — told as what happened** (2026-09-17, 2026-10-02) — the wound then runs its own real clock, which the party can answer | documents 01 and 13 |
| cold air on a part | the part's `heat` falls: fine work goes when finger skin is below about 15 °C, the part is numb below about 7 °C, and it freezes below about −0.5 °C | document 08 (extremities); **the heat design** |
| cold metal and cold fuel | contact frostbite: bare skin on cold metal loses heat fast; avgas or oil below freezing is still liquid and freezes skin almost at once as it evaporates | **the heat design** |
| wet, cold feet above freezing | **non-freezing cold injury** (trench foot): numb, swollen, then painful — usually after two or three days wet and cold at 0–15 °C, in as little as 10–14 hours. This week's own cold injury, before it is cold enough for frostbite from the air: the townie's sneakers | **the heat design**; document 08 (wet) |
| cold water — through the ice | cold shock and gasping in the first minute; about ten minutes of useful movement; about an hour before hypothermia takes consciousness (Giesbrecht's 1-10-1). Out of the water, wet clothes in the wind keep spending heat. It is the cold that kills | document 13 (the ice); **the heat design** |
| heat | burns: skin is damaged above about 44 °C, slowly at first and almost at once as the temperature climbs — a hot stone held too long, the boiling pot, the fire | document 07; **the heat design** |
| the air in a closed space | carbon monoxide from a fire in the fuselage; smoke; toxic smoke from burning foam (document 07's foam warning) | **the heat design** (the plane's openings and internal air) |
| the gut | the hemlock root and the baneberry (document 23), the bulged can, rotten meat, fuel-tainted water (document 09) | documents 10, 23, 09; **the food-state and spoilage design, to be written** |
| the eyes | smoke, sparks from the ferro rod or the hatchet on quartz | this document |
| work | blisters from the bow drill, splinters, cuts from torn aluminium — rummaging through the wreckage can cut you on something sharp (2026-09-28) — a strained back | the activity that caused it (document 06) |

**The animals are real animals.** Alaska's record for brown bears (1986–1996) is about 2.75 people
injured and 0.42 killed a year: a bear injures far more often than it kills, and a defensive attack
usually ends when the person stops being a threat. Most fatal black-bear attacks were predatory
(Herrero et al. 2011), and those do not stop. In early October the bears are feeding hard before they
den. How each animal decides is the animal-behaviour design's; what its claws and teeth do to a body is
this table's.

**The week decides which cold injuries come first.** In the first week of October the days are a few
degrees above freezing, falling below it by the end, and every night is below it, colder as the week
goes, down to the clear night after the day-6 flurry, the coldest of the run (document 13 §4.2), but
frostbite from the air alone needs a wind chill near −28 °C to strike in half an hour (the National
Weather Service chart). So this week the cold injures above all through **wet** — the whole body, not only hands and feet
(2026-09-28): clothes soaked through by breaking through the ice, by the wet flurries and the creek,
and by sweat, which keeps a body warm while it works and chills it once the work stops (document 08) —
**contact** (metal, fuel), **immobility** (the injured and the sleeping)
and **tight boots** — and non-freezing cold injury in feet that stay wet for days is the week's own.
That is the real order, and the world teaches it by happening in it.

**Real-world sources for this section and §4.7–§4.12:**
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
- CDC — tetanus incubation 3–21 days (Pink Book ch. 21); staph food poisoning 30 minutes to
  8 hours, heat-stable toxin; *C. perfringens* 6–24 hours. StatPearls — *Pasteurella* infection within
  24 hours of a bite.
- OSHA confined-space handout, *Effects of Carbon Monoxide at Different Concentrations*.
- Giesbrecht's 1-10-1 principle of cold-water immersion.
- Moritz & Henriques, *Studies of Thermal Injury II* (Am. J. Pathology, 1947) — burn threshold ~44 °C.
- UpToDate / *Nonfreezing Cold Injury (Trench Foot)* — 0–15 °C, days (as little as 10–14 hours).
- Occupational studies of hand cooling — marked loss of dexterity below ~15 °C finger skin; numb
  below ~7 °C; tissue freezes at about −0.55 °C; supercooled fuel causes instant frostbite.
- National Weather Service wind chill and frostbite chart.
- Smith & Herrero, *Human–bear conflict in Alaska: 1880–2015* (Wildlife Society Bulletin, 2018); the
  1986–1996 Alaska brown-bear rate of about 2.75 injuries and 0.42 deaths a year as cited in the Alaska
  bear-deterrent studies (Smith et al.); Herrero et al., *Fatal attacks by American black bear on
  people: 1900–2009* (J. Wildlife Management, 2011).
- Epidural haematoma and the lucid interval (AMBOSS; StatPearls); pneumonia after rib fractures
  (*Am. J. Emergency Medicine*, 2019).
- Alcohol, skin vasodilation and blunted shivering.

### 4.7 Stopping the bleeding

Direct pressure is the first thing every bleeding-control
course teaches (Stop the Bleed, the Red Cross), and it needs nothing but a hand. **`press`** is an
**attended activity** (document 06): while it is held the wound's bleeding rate falls; lifting early
lets the bleed restart; held long enough — minutes, ten or more for a heavy bleed — a clot holds and the
hand can come away. The acts around it are each their own operation, because each does something
different to the wound: **`press`** (a hand or a pad on it — `press the cut`, `press the gauze on Mara's
arm`); **`pack`** (stuff gauze or cloth — the tampons in the townie's bag — into a deep wound that
pressure on the surface cannot reach, then press); a **pressure dressing** (`bind` or `wrap` tight over
a pad, which frees the hands); a **tourniquet** (`tie` a wide band above a limb wound and `twist` a rod
through it to tighten — seatbelt webbing is the right width; string or wire cuts in and fails; and past
about two hours a tourniquet starts killing the limb it saves); and **`elevate`**. Canonical words and
their synonyms are authored together (document 04 §3.7): press · apply pressure · hold · push on.

### 4.8 Cleaning, and infection

A wound carries **`contamination`** as a state — how much and
of what: crash grit, cloth fibres, soil, avgas, an animal's mouth — set by what made it (a bite or a
claw is always dirty; a clean slice from the razor barely is). **Infection is a process on the wound**
that grows from that contamination over real hours, deterministic and seeded (DR-12): a dirty wound
shows redness, heat and swelling in 24–72 hours (an animal bite in 12–24), then pus and a smell, then
fever — which spends water and warmth — and, untreated, spreads into the blood, which kills over days.
Cleaning is its own set of real operations: **irrigate** — pour or squirt drinkable water into it, in
millilitres (document 09), harder if you pierce a bag or a bottle cap — boiled water, or water treated
with the iodine tablets, is drinkable and so is right for it; the Wilderness Medical Society's
guideline is that drinkable water is enough and nothing should be added; **pick out** grit and
splinters with a point (the multitool, a clean knife tip); and scrub the skin around it. Whisky and
sanitizer are alcohol: they clean a blade and intact skin, but in the wound they kill tissue as well as
germs and hurt badly — a real act, worse than clean water. Whatever covers the wound carries its own
contamination as provenance, the way a vessel does (document 09 §4.6): a torn-up shirt makes a
dressing, as any cloth does, and brings whatever it carries — a boiled strip cleanest, a shirt worn for
days less clean. Sphagnum moss from the muskeg makes an absorbent pad, held on with a strip of cloth
(document 23 §4.2). A sewing needle and thread (document 16) close a wound, though worse than the suture kit — sewing
thread is braided and wicks germs in, and a straight needle tears more — once the needle is boiled,
held in a flame or soaked in whisky. And **closing** a dirty wound traps it — the guideline leaves a grossly
contaminated wound open and packed — so the nurse's suture kit is a real choice with a real downside,
not a finish line. Boiling a strip or a blade is the heat design's (to be written).

### 4.9 Carrying a person

A person can be carried in every real way (2026-09-28), because a person
is an entity with a mass and the carrying rules already exist (document 04 §3.11: capacity is what you
hold, wear and haul; the load feeds travel time). **`carry`** on the back or over the shoulders is one
strong person, a short way; **two people** can carry one between them; **`drag`** by the shoulders or
the jacket works on frosty moss or snow; and a **litter or sled** — a seat frame, the panelling, a tarp
or a blanket between two poles — dragged over the ground hauls a person much farther for the same
effort, sliding best where snow lies on smooth ground, which is why it is the real answer (the world
design already has a drag litter of panelling and cord). Carrying makes the **carrier** hot and
sweating — the deferred cold debt (document 08 §4.2) — while the **carried** person, not moving and
often lying on frozen ground or snow, cools fast and needs insulation under and around them. Moving an
unsplinted break grinds the bone ends: pain, more bleeding, damaged nerves. Two people carrying one
needs a co-operative form in the grammar — two actors on one entity, such as one player helping
another drag something — whose mechanics are still to be worked out, in documents 04 and 19
(2026-09-28).

### 4.10 Painkillers

Pain is a state on the part (§4.6) and part of what limits the part, so masking it is modelled,
honestly (2026-09-28). Ibuprofen — the nurse's pouch holds a count of tablets —
works in 30–60 minutes and lasts four to six hours; it lowers pain and swelling, and `status`
truthfully reports less pain while the wound is unchanged: that is the fair lie. How much the part
gives back depends on the wound — a sprain's limit is mostly pain, so a sprained ankle walks better; a broken
bone's limit is mechanical, so no pill makes it bear weight. Over a week its side effects are too small
to matter (2026-09-28): what it costs is the tablets, and who gets them. It is also the field treatment
for frostbite. Whisky dulls pain and judgment, and it opens
the skin's blood vessels and blunts shivering, so it costs heat — the brandy-in-the-snow cure is a myth.
Willow grows in the valley, so willow-bark tea (document 23) is a weak real painkiller.

### 4.11 How impairment reads

By what the body really does, and never by doing something the player did not type (2026-09-28). A concussion is headache, nausea, dizziness, light sensitivity, fatigue and
slowness — not a world that looks wrong — so the salesman's first day is slower acts (activities take
longer, document 06), more fine-work failures, lines of headache and nausea, and a pull toward sleep;
the room reads true. Hypothermia's confusion (document 08's `impaired` band) is clumsiness and poor
judgment: the fumbled match, the knot that will not hold, the slurred word. So the rule: **the body can
fail at an act** — fumble it, slow it, collapse, lose consciousness (a missing member is already
incapacitated where they lie) — **but the engine never performs an act the player did not type.**
Severe hypothermia's paradoxical undressing is real — the dying feel hot and strip — and it arrives as a
felt urge in the prose ("the parka is unbearable"); taking it off is the player's choice.

### 4.12 Seeing another person's wounds

By the senses (2026-09-28), the way the tell-and-hide rule works for everything else (document 03
§4.3: the worn layer is what shows); a player's meters show only their own body. **A serious condition
shows in the person's line in the room** — what anyone would see from across it: a sleeve soaked dark
with blood, a leg at the wrong angle, someone pale and shaking, hopping on one foot (document 03 §4.1).
**The body's own signs arrive as emotes** — a cough, a wince, teeth chattering, a limp as someone
moves — single lines now and then, routed by distance like any event (document 03 §4.7). **Examining
or looking at the person** reveals the smaller things you would not see from across the room — a white
patch on a bare cheek, a bandage's edge, a swollen wrist; what is under a glove or a boot stays hidden
until someone takes it off, which costs that part its heat. **Touch** gives heat — a hot forehead is a fever, a cold hand is cold — swelling and
a pulse; **smell** gives an infected wound away. Wounds and parts carry this in their `sensed` rows
(document 05 §4.5). Asking is speech, and the person can answer truly or not. Each is its own act:
`examine Mara`, `examine Mara's hand`, `feel Mara's forehead`, `take the glove off Mara's hand`.

### 4.13 The `make a splint` rows (the goal chosen 2026-09-18; its rows kept 2026-09-28)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | a splint |
|---|---|
| `goal` | a splint · a bandage · to stop the bleeding |
| `vague` | "How are you going to splint it?" / "…stop the bleeding?" |
| `roles` | **rigid**: a rod, a board, a stick · **binding**: cordage, a strip, tape · **wound**: the named wound |
| `realize` | `bind <wound> with <rigid> and <binding>` — the ordinary wound operations; a wrong pairing gets the physics (a strip alone will not hold a bone) |

The row set is a floor — the loops add goals and means from what people and agents type (2026-09-28).

## 5. Interactions

**This depends on:**
- **08 Warmth, clothing and shelter** — frostbite and hypothermia *are* warmth failures; bleeding costs
  warmth; bare hands lose the dexterity that treatment needs; `status`.
- **09 Water** — bleeding and fever cost hydration; irrigating a wound spends drinkable water; boiling
  cleans a tool.
- **07 Fire and shaping** — burns, smoke inhalation, sterilising a blade, and the warmth that treats
  frostbite.
- **06 Time, sleep and the clock** — bleeding and infection are processes on the heartbeat; pressing and
  dressing a wound are attended activities with their own feedback; `SURVIVOR_WORSENS` force-interrupts.
- **18 Materials and forms** — cloth binds, webbing ties, a rod splints, alcohol cleans a blade; nothing
  is a "bandage" by type.
- **16 Players and kit** — the draw, the med pouch, the first-aid kit, the whisky; how well and how fast
  each character does things.
- **13 Events, escalation and weather** — the week's cold, wet and light (13 §4.2); the Bodies cards.
- **01 Premise and world** and **13** — the dangerous places and the ice, which deliver wounds and never
  kill outright.
- **The combat design** *(to be written)* — each attack typed, landing by the fighters' stats and
  chance; the blows that really hurt arrive here as wounds on parts.
- **The heat design** *(to be written)* — `heat` on every body part, contact heat and cold, burns, the
  plane's openings and internal air (carbon monoxide, smoke).
- **23 Flora and fauna** and **the animal-behaviour design** *(to be written)* — the bear's and the other
  animals' attacks; the poisons.
- **The food-state and spoilage design** *(to be written)* — what raw, frozen, cooked and spoiled food
  does in the gut.

**These depend on it:**
- **10 Food and hunger** — starvation weakness; the bulged can; cleaning game with a blade.
- **12 The pilot and bodies** — the body as an entity with parts and states (§4.6), the same for the
  living and the dead.
- **14 Rescue** — an injured party walks slower, climbs worse and carries less, so every way home costs
  it more.
- **15 Moral and social layer** — the bandage, the painkillers, who gets carried, and whether the party
  leaves someone.
- **19 Multiplayer** — carrying a person is the co-op act with the highest price.

## 6. Open questions

None open.

## 7. Review log

- **2026-09-18 (Andrew):** the `make a splint` goal rows (document 04 §3.9 owns the form and the dispatch
  rule).
- **2026-09-26 (Claude's self-review, for Andrew's check):** the body as an entity with parts and
  states; the real clocks; every source of injury; the treatments and the other design answers from
  real medicine and wilderness first aid (§4).
- **2026-09-27 (Andrew):** characters differ in how well and how fast they do things; what kills is
  blood loss, the cold and thirst — poison sickens but never kills.
- **2026-09-27 (Andrew, the document's sitting):** item 1 — no hit points: named wounds on body parts,
  each part with its own states; meters for what the body feels (document 08 §4.9); a blow wounds only
  when it would really hurt; combat is roughly a MUD's, with every attack typed and landing by stats
  and chance, as in D&D, read as what happened; a recovery after each attack; stepping in for a
  friend; the bear's warnings, and running as the wrong answer to a bear. The meters. Item 2 —
  bleeding as a real blood volume on the real clocks, kept real at 15×, with a blood meter and the
  world's own messages, such as feeling faint. Item 3 — infection and
  cleaning; nothing kills instantly, and death is realistic, by the body running down with time to
  respond — wounds and infection can kill, poison never does, a fall never kills outright; a torn-up
  shirt makes a dressing; a few iodine tablets in one of the packs and a sewing needle and thread
  aboard. Item 4 — whisky in a wound and over the needle are in, the film scene, with their real
  result; boiled or iodine-treated water rinses a wound. Item 5 — each real first-aid act its own act,
  pressing held. Item 6 — frostbite and hypothermia as proposed; no snow blindness, since the sky is
  always at least partly cloudy; carbon monoxide only where the space does not breathe enough for the
  fire, by real physics; a tarp aboard for sealing the crash's openings.
- **2026-09-28 (Andrew, the document's sitting, continued):** item 7 — the body as proposed; the cold
  hurts above all through getting wet, the whole body — the ice, the flurries, sweat once the work
  stops. Item 8 — carrying a person in every real way; the mechanics of helping someone drag or carry
  are still to be worked out. Item 9 — painkillers as proposed, without side effects too small to
  matter in a week; willow-bark tea, since willow grows here. Item 10 — how impairment reads: the body
  can fail at an act, and the engine never performs one the player did not type. Item 11 — seeing
  another's wounds by the senses: a serious condition in the person's line in the room, the body's
  signs as emotes, the smaller things on a closer look. Item 12 — the start is light: bumps and
  bruises for most, a cut and a concussion, no sprained ankle; the treatments, the injury list and the
  goal rows are floors; the numbers are real starting points. **Reviewed in full.**
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

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
  pouring water, whisky or sanitizer are real operations, so the improvised way's *materials* exist.
- Objects: the first-aid kit with a bandage roll and medical tape in the pry-gated forward bin; the
  nurse's med pouch with gauze, medical tape, ibuprofen and a suture kit; the whisky bottle; the hand
  sanitizer.
- Tests and probes: `game/tests/sim/test_kit.py::test_wounds_summary`;
  `probes/kit.nurse.med_pouch` (`open pouch` → `take gauze` → `wrap arm with gauze`) and
  `probes/census.py` `mid_cabin.open_kit` and `mid_cabin.bandage_arm_with_bandage` are measured
  passing.

**Designed, not built**
- The light start (§4.2): `characters.py` still ships bruised ribs, a sprained ankle and shock for the
  guide, the nurse and the kid, where the design now has minor bumps and bruises.
- The injury processes: bleeding per tick, binding stopping it, infection, fever.
- Treatment as an act on a *wound*: `press`, `pack`, `splint`, `stitch`, `clean` —
  the first-aid kit's contents have no use-verb yet.
- The injuries the world can *inflict*: frostbite from bare regions, burns, hypothermia, smoke
  inhalation, exhaustion, carbon monoxide.
- Carrying an injured person.
- Wounds affecting what a character can do — the notes ("walking costs double", "heavy work is slow")
  are authored prose that nothing reads.
- How well and how fast each character does things.

**Nothing**
- No operation targets a wound. `wrap arm with bandage` succeeds as a generic wrap: it sets
  `wrapped`/`insulated` on the target and changes nothing about the wound, which is not bound and
  does not stop bleeding — because nothing bleeds yet.
- No `press`, `splint`, `stitch`, `clean`, `carry` or `treat` in today's handler set (`bend, break, burn,
  cut, drink, eat, examine, light, make, melt, open/close, pour, pry, move, read, search/dig,
  take/put, talk, tie, use, wear, wrap, tear`).
- No frostbite, no hypothermia, no infection, no fever, no painkiller effect; ibuprofen is a bottle
  of plastic with a count on it.
- The pilot's blood in the cockpit is examine-prose only; the pilot is dead in the shipped slice, as
  designed (document 12).
- No body parts as entities, no per-part `heat`, no blood volume, no contamination or infection
  process, no combat, no animal attacks, no carbon monoxide.
