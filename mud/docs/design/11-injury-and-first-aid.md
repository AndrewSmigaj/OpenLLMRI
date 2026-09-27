# 11 — Injury and first aid: wounds, bleeding, infection, frostbite, splints, the med pouch

> **Status: draft for review.** **Architecture counterpart:** none. This system had no design document
> of its own before this one.

## 2. Decisions

### Andrew's decisions
- **(2026-09-07)** Each player starts with a different injury draw, as with clothing and pockets. You do
  not choose what the crash did to you, and nobody in the party is whole.
- **(2026-09-07)** Decisions across the moral spectrum — the injured are one of the places that lands:
  who gets carried, who gets the bandage, who gets left by the fire.
- **(2026-09-16, 2026-09-26)** No lethal-consent gate; violence resolves with real physics, and there is a
  combat system like a MUD's — stab with a spear, beat with a stick. Wounds are wounds whoever caused
  them; the engine does not soften a blow.
- **(2026-09-17)** Dangerous places injure but never kill outright; fitness matters; a seeded dice roll,
  announced (document 01).
- **(2026-09-17)** The pilot starts the run dead, so the party's first patients are each other.
- **(2026-09-17, 2026-09-27)** The endings are rescued or dead; the run ends when they die. Dead players
  are ghosts.
- **(2026-09-18)** The extremities have their own cold, for frostbite (document 08). There is a `status`
  screen that reports injuries in band words (document 08 §4.9).
- **(2026-09-26)** Body parts carry heat as part of their ontology; heat is a state system. The bear,
  some bigger animals and a few birds act (document 23).
- **(2026-09-26, 2026-09-27)** The season is the first week of October in interior Alaska; the week's
  numbers are document 13 §4.2's.
- **(2026-09-27)** **What kills: blood loss, the bear, the cold and thirst.** Poison makes people very sick but
  never kills; other harms — infection, carbon monoxide and the rest — make them weak and sick.
- **(2026-09-27)** **Characters differ in how well and how fast they do things.** A character's success
  and the time an act takes depend on who they are — a woodsman lights fires better, and a nurse's
  hands are better at wound care. It shows only in the outcome, never as advice; the player still has
  to know what to do.

### Proposals (Claude)
Everything else here is Claude's, for Andrew's check: the wound model and the bleeding and infection
processes; which injury each slot draws; the body as an entity with parts and states (§4.6); the
treatments as operations (§4.7–§4.12); the injury list beyond the crash's; every number. The real-world
sources are listed at the end of §4.6.

## 3. In one paragraph

Everybody wakes up hurt, differently, and it shapes what each of you can do before anyone has said a
word about it. The cut forearm is bleeding into a sleeve and will keep bleeding until somebody
presses it and binds it; the sprained ankle makes every walk cost double until somebody thinks of a
stick and a strap; the bruised ribs make heavy work slow; the concussion makes the first day slow and
sick. None of it is a debuff you read off a sheet — it is your own description when you look at
yourself, and it is the reason the party has to decide who does what. The nurse has a pouch with gauze
and tape and sutures in it, and her hands are quicker and surer at wound care than anyone else's — but
the person playing her still has to know what to do, like everyone else. Later the wounds that were
dressed with a dirty shirt start to matter, and the fingers that spent an afternoon bare on cold metal
start to matter, and first aid stops being a one-off act and becomes a thing you keep doing.

## 4. The design

### 4.1 The rules

1. **Wounds are named things on a body part, not a hit-point total.** The shipped shape is `{part, kind,
   severity, bleeding (grams per minute, 0 = none), bound?, infected_at, note}`, and a person has a
   list of them. *(Proposed by Claude, for Andrew's check:)* a wound is a state on a body **part**, and
   the part is an entity with its own heat, wetness, pain and covering (§4.6); a wound gains
   `contamination` and `pain`, and `infected_at` becomes the state of the infection process (§4.8).
   There are no hit points anywhere: a body has none, so the game has none. The combat system is built
   on this, not beside it — a spear thrust is a `point` wound to the part it reaches, through what that
   part wears; a stick is `heft` — a bruise, a break, a concussion; the bear's claws are `edge`, its bite
   a puncture and a crush. What combat *feels* like — the exchange of blows, its pace, breaking off and
   running — is the combat design's to write; that every blow resolves into a named wound on a body
   part is this document's rule.
2. **Bleeding is a process, and blood loss kills** (2026-09-27). *(Proposed by Claude, for Andrew's
   check:)* bleeding spends **blood volume**, in millilitres — about 70 mL per kilogram of body weight,
   some 5 L in a 70 kg adult — and a body short of blood makes less heat, so it costs warmth too.
   Pressure slows it while it is held; a pressure dressing or packing holds it after; a tourniquet stops
   a limb's arterial bleed (§4.7). A binding stops only a bleed it is equal to: arterial blood soaks
   straight through a strip.
3. **Infection is a process on the wound, and it weakens rather than kills** (2026-09-27). *(Proposed by
   Claude, for Andrew's check:)* deterministic and seeded (DR-12), so a run replays identically, and
   driven by the wound's contamination, how it was cleaned and what covers it (§4.8). Then fever, which
   costs warmth and water, and, untended, worse — but never death on its own.
4. **Medicine is systemic and improvised, never a recipe.** Cloth becomes a bandage; seatbelt webbing
   becomes a tourniquet or a splint tie; branches, aluminium frames or poles become splints; alcohol
   cleans a blade and intact skin; boiling water or a flame cleans some metal tools; snow reduces
   swelling and worsens cold exposure; painkillers improve function and mask danger; moving an injured
   person can save them from the cold and worsen the injury. Every one of those is a trade, and none of
   them is a crafting recipe. *(Proposed by Claude, for Andrew's check:)* poured into an open wound,
   alcohol kills tissue as well as germs, and the Wilderness Medical Society's guideline is to irrigate
   with plain drinkable water and add nothing — whisky on a cut arm is a real act with a real, worse
   result than clean water.
5. **Treatment is an act on a wound, with a tool.** `press`, `bind` / `wrap`, `splint`, `stitch`,
   `clean`. The wound is the target; what you use is whatever physically serves. *(Proposed by Claude,
   for Andrew's check:)* the floor grows with the real acts, each its own operation because each does
   something different to the wound — `pack`, a tourniquet (`tie` a band above the wound, `twist` a rod
   through it), `rinse` / irrigate, pick out the grit, `elevate`, rewarm a frozen part, `carry` and
   `drag` a person (§4.7–§4.9).
6. **The injury is in the description.** `examine me` reads your wounds back to you in plain words —
   this is shipped: *"Your forearm is cut and bleeding; your ankle is sprained."* The `status` screen
   reports them too, in band words, never numbers (document 08 §4.9).
7. **Never a menu, and common sense is hinted.** The game does not tell you to press the wound, does
   not list the med pouch's contents when you are bleeding, and does not name the tourniquet. It says
   the sleeve is soaking.
8. **Trained hands** (2026-09-27). A character's trade changes how well and how fast they do the acts
   of that trade: the nurse's stitches close neater and cleaner and take less time, and her splint
   holds. It shows only in the outcome (*"the edges meet neatly"*), never as advice, and it applies to
   an agent exactly as to a human.

### 4.2 The starting draw (content — shipped in `characters.py`)

| slot | injury | what it costs |
|---|---|---|
| the guide | bruised ribs | bending and lifting hurt; heavy work is slow |
| the townie | a cut forearm, bleeding | the census wound — bleeding through the sleeve; press it, bind it |
| the nurse | a sprained ankle | walking costs double; a splint and a stick would halve it |
| the salesman | concussion | tires fast; the first day is slow — headache, nausea, dizziness, light hurts, slower acts (§4.11) |
| the kid | shock | physically fine; slower to act on day one. This is an acute stress reaction — psychological. Circulatory shock is what blood loss does to a body (§4.6); both are real, and they are different states |

The point of the spread is that it is *heterogeneous*: the person who can walk is not the person who
can lift, and the person who knows medicine is the one who cannot get to you. The seed permutes which
player draws which slot, so no player is always the townie. A seat nobody plays is a dead character
(document 12 §4.4), so its injury never runs.

### 4.3 Ways to treat a wound (a floor — the loops add more)

| way | what it spends | where | the chain |
|---|---|---|---|
| **the first-aid kit** (bandage, tape) | search | the forward bin in the mid cabin — pry-gated | `press wound` → `wrap arm with bandage` |
| **improvised** (shirt strips, clean water to rinse, paracord and a rod as a splint) | tools + knowledge | the rear cabin, the duffel | `tear shirt` → `pour water on the cut` → `wrap arm with strip` |
| **warmth for frostbite** (skin to skin, no rubbing) | warmth | any | `wrap hands in socks` · sit by the fire |

**The med pouch** belongs to a person, not the plane: gauze pads, medical tape, ibuprofen, a suture kit
(shipped in `characters.py`). Her hands are trained; the player still has to know what to do. The
plane's first-aid kit is a bandage roll and medical tape in the pried forward bin. Whisky and hand
sanitizer are the alcohol, and both are also fuel.

### 4.4 The injury list (a floor)

The set the system honours — a floor, not a list of what can happen: **bleeding · a broken limb ·
concussion · burns · frostbite · hypothermia · infection · shock · dehydration · smoke inhalation ·
exhaustion** — and, because they are real here, **non-freezing cold injury, contact frostbite,
cold-water immersion, snow blindness, carbon monoxide, bites and maulings, blows and stab wounds,
poisoning, and the blisters, splinters and cuts of work in a wreck** (§4.6). Frostbite and hypothermia
are the warmth system's failures with a location; burns and smoke inhalation are fire's; dehydration
and exhaustion are the other survival clocks'.

*(Proposed by Claude, for Andrew's check.)*
- **Frostbite** is a part's `heat` below about −0.5 °C (document 08's extremities; the heat design). It
  whitens a finger first; bare hands and feet drive it. The care is the survivor's act, and real:
  rewarm against warm skin (an armpit, a belly) or in water at 37–39 °C; never rub; and **never thaw a
  part that may freeze again** — refreezing is worse than staying frozen, so a party that must walk on
  frozen feet may be right to walk first (WMS frostbite guidelines, 2024). The nurse's ibuprofen is real
  field treatment for frostbite. Blisters come in the hours after rewarming; dead tissue takes weeks to
  show, longer than the run.
- **Snow blindness** is a dose of UV on the eyes: the sun (by date, hour and cloud) × the snow's
  reflection (fresh snow reflects up to 80–90%) × the hours unprotected. It shows **6–12 hours later** —
  typically waking in the night with burning, gritty eyes — and heals in a day or two in the dark. This
  week the sun is low, so it is uncommon, and likeliest on the clear days after the storm, on fresh
  snow in the open (document 13 §4.2). The kid's sunglasses are one answer among real ones: slit
  goggles cut from bark, cardboard, leather or cloth, and soot under the eyes. Physics with improvisable
  answers, not a gotcha.
- **Carbon monoxide** is a gas in a zone's air. A fire in a closed space makes it — a smouldering or
  banked fire more than a bright one — and the plane's openings let it out (the plane is an entity with
  openings, open or closed, 2026-09-26). A body takes it up and gives it back only slowly, over hours of
  fresh air: headache and nausea first, then confusion, then collapse. It makes a body very sick and
  never kills on its own (2026-09-27); it is why blocking every gap is not free. Owned by the heat
  design (the air in enclosed zones).
- **Hypothermia's confusion** is clumsiness, slowness and poor judgment — the body can fail at an act,
  and the engine never performs one the player did not type (§4.11).

### 4.5 The escalation (what untreated injury does over a week)

*(Proposed by Claude, for Andrew's check.)* A cut on day 1; a dirty wound shows infection in 24–72
hours (an animal bite in 12–24); fever and spreading redness over the next days, costing warmth and
water. A deep, dirty wound can turn to gas gangrene within hours to three days; the black of dead
frostbitten tissue takes weeks to declare itself, longer than the run. None of that kills on its own
(2026-09-27): what it takes is the labour that keeps everyone else alive — *a body that can't work
can't stay warm.* What kills is blood loss, the bear, the cold and thirst (§4.6).

The Bodies cards of the event deck (document 13 §4.3) make it visible: a wound infects; frostbite
whitens a finger; snow blindness; hypothermia's clumsiness; dehydration headaches; the hunger stages.

### 4.6 The body, and everything that can hurt it

*(Proposed by Claude, for Andrew's check — except the rule of what kills, which is Andrew's,
2026-09-27.)* Injury has many sources — a combat system like a MUD's, a bear and other animals that
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
(poison, bad meat), **infection and fever**, **fatigue**, **consciousness**. None of them is a
hit-point total; each is a real quantity.

**What kills** (Andrew, 2026-09-27) — three things, on their real clocks:

| what kills | what the body does on the way | how fast |
|---|---|---|
| **blood loss** — blood volume, about 70 mL/kg, ~5 L in a 70 kg adult | up to 15% lost: nothing shows · 15–30%: fast pulse, anxiety · 30–40%: falling blood pressure, confusion · over 40%: unconsciousness, then death (the ATLS classes) | minutes from an artery; hours from a venous cut left alone; a broken thigh bone bleeds 1–1.5 L inside the leg with no wound to press |
| **the bear** — through its claws and teeth, and the bleeding they cause | claws cut and tear; a bite punctures and crushes; a defensive attack usually ends when the person stops being a threat, a predatory one does not | one encounter |
| **the cold** — core temperature | shivering; then clumsiness and confusion; shivering stops; unconsciousness; the heart stops (the WMS staging behind document 08's bands) | a night, badly dressed and unsheltered; about an hour in ice water |

**What weakens and sickens, and never kills on its own** (2026-09-27) — a body brought low by these is
what the cold and blood loss find:

| what fails | what the body does | how fast |
|---|---|---|
| **carbon monoxide** | headache and nausea; dizziness and confusion; collapse | 200 ppm: a headache in 2–3 hours · 800 ppm: dizziness and nausea within 45 minutes · 1,600 ppm: collapse within the hour |
| **a wound's infection** | red, hot and swollen, then pus and a smell, then fever, then spreading — 24–72 hours to show on a dirty wound, 12–24 on an animal bite; tetanus 3–21 days (about 8 on average) | days |
| **inside the skull** | a head strike, a lucid spell, then a fast decline into unconsciousness (an epidural bleed; 20–50% of them have the lucid interval) | hours |
| **the chest** | broken ribs make every breath hurt, so breathing goes shallow, and pneumonia follows within the week | days |
| **the gut — poison** | water hemlock: seizures within the first hour; botulism from the bulged can: weakness and paralysis from about a day on; spoiled meat (a fish left too long, an animal long dead): vomiting and diarrhoea from half an hour to days later, spending water. Very sick, never dead (2026-09-27) | hours to days |
| **energy** | document 10: weakness, then cold | weeks |
| **hydration** | document 09 §4.6: thirst, headache, weakness — on a real clock of about three days. Thirst kills on its real clock (2026-09-27) | days |

**Where injuries come from** (a floor; each source's system owns how it delivers the wound):

| source | what it does to a part | owned by |
|---|---|---|
| the crash | the starting draw (§4.2) | document 16 |
| a person with a stick, a spear, a knife, a rock | `heft` bruises, breaks bone, concusses; `edge` cuts; `point` punctures — small, deep and dirtier than it looks; what covers the part changes what gets through | **the combat design, to be written** |
| the bear and the other animals that act | claws cut and tear; a bite punctures and crushes. Every animal wound is heavily contaminated | document 23 and **the animal-behaviour design, to be written** |
| a fall — the cornice, the climb, a slip on the ice | a sprain, a break, a head strike. **Dangerous places injure, never kill outright; fitness matters; the dice roll is announced** (2026-09-17) — the wound then runs its own real clock, which the party can answer | documents 01 and 13 |
| cold air on a part | the part's `heat` falls: fine work goes when finger skin is below about 15 °C, the part is numb below about 7 °C, and it freezes below about −0.5 °C | document 08 (extremities); **the heat design** |
| cold metal and cold fuel | contact frostbite: bare skin on cold metal loses heat fast; avgas or oil below freezing is still liquid and freezes skin almost at once as it evaporates | **the heat design** |
| wet, cold feet above freezing | **non-freezing cold injury** (trench foot): numb, swollen, then painful — usually after two or three days wet and cold at 0–15 °C, in as little as 10–14 hours. This week's own cold injury, before it is cold enough for frostbite from the air: the townie's sneakers | **the heat design**; document 08 (wet) |
| cold water — through the ice | cold shock and gasping in the first minute; about ten minutes of useful movement; about an hour before hypothermia takes consciousness (Giesbrecht's 1-10-1). Out of the water, wet clothes in the wind keep spending heat. It is the cold that kills | document 13 (the ice); **the heat design** |
| heat | burns: skin is damaged above about 44 °C, slowly at first and almost at once as the temperature climbs — a hot stone held too long, the boiling pot, the fire | document 07; **the heat design** |
| the air in a closed space | carbon monoxide from a fire in the fuselage; smoke; toxic smoke from burning foam (document 07's foam warning) | **the heat design** (the plane's openings and internal air) |
| the gut | the hemlock root and the baneberry (document 23), the bulged can, rotten meat, fuel-tainted water (document 09) | documents 10, 23, 09; **the food-state and spoilage design, to be written** |
| the eyes | snow blindness (§4.4), smoke, sparks from the ferro rod or the hatchet on quartz | this document |
| work | blisters from the bow drill, splinters, cuts from torn aluminium, a strained back | the activity that caused it (document 06) |

**The animals are real animals.** Alaska's record for brown bears (1986–1996) is about 2.75 people
injured and 0.42 killed a year: a bear injures far more often than it kills, and a defensive attack
usually ends when the person stops being a threat. Most fatal black-bear attacks were predatory
(Herrero et al. 2011), and those do not stop. In early October the bears are feeding hard before they
den. How each animal decides is the animal-behaviour design's; what its claws and teeth do to a body is
this table's.

**The week decides which cold injuries come first.** In the first week of October the days are near
freezing and the clear nights after the storm are well below it (document 13 §4.2), but frostbite from
the air alone needs a wind chill near −28 °C to strike in half an hour (the National Weather Service
chart). So this week the cold injures through **wet** (hands and feet soaked in wet snow, the creek,
the ice), **contact** (metal, fuel), **immobility** (the injured and the sleeping) and **tight boots** —
and non-freezing cold injury in feet that stay wet for days is the week's own. That is the real order,
and the world teaches it by happening in it.

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
- The College of Optometrists and the American Academy of Ophthalmology — photokeratitis shows 6–12
  hours after exposure and heals in 24–48; fresh snow reflects up to 80–90% of UV.
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
- NSAIDs and platelets (Schafer, J. Clin. Pharmacology, 1995); NSAIDs and acute kidney injury when
  dehydrated (National Kidney Foundation); alcohol, skin vasodilation and blunted shivering.

### 4.7 Stopping the bleeding

*(Proposed by Claude, for Andrew's check.)* Direct pressure is the first thing every bleeding-control
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

*(Proposed by Claude, for Andrew's check.)* A wound carries **`contamination`** as a state — how much and
of what: crash grit, cloth fibres, soil, avgas, an animal's mouth — set by what made it (a bite or a
claw is always dirty; a clean slice from the razor barely is). **Infection is a process on the wound**
that grows from that contamination over real hours, deterministic and seeded (DR-12): a dirty wound
shows redness, heat and swelling in 24–72 hours (an animal bite in 12–24), then pus and a smell, then
fever — which spends water and warmth — and, untreated, spreads, weakening the body without killing it.
Cleaning is its own set of real operations: **irrigate** — pour or squirt drinkable water into it, in
millilitres (document 09), harder if you pierce a bag or a bottle cap; the Wilderness Medical Society's
guideline is that drinkable water is enough and nothing should be added; **pick out** grit and
splinters with a point (the multitool, a clean knife tip); and scrub the skin around it. Whisky and
sanitizer are alcohol: they clean a blade and intact skin, but in the wound they kill tissue as well as
germs and hurt badly — a real act, worse than clean water. Whatever covers the wound carries its own
contamination as provenance, the way a vessel does (document 09 §4.6): a boiled strip is clean; the
shirt you slept in is not. And **closing** a dirty wound traps it — the guideline leaves a grossly
contaminated wound open and packed — so the nurse's suture kit is a real choice with a real downside,
not a finish line. Boiling a strip or a blade is the heat design's (to be written).

### 4.9 Carrying a person

*(Proposed by Claude, for Andrew's check.)* A person can be carried in every real way, because a person
is an entity with a mass and the carrying rules already exist (document 04 §3.11: capacity is what you
hold, wear and haul; the load feeds travel time). **`carry`** on the back or over the shoulders is one
strong person, a short way; **two people** can carry one between them; **`drag`** by the shoulders or
the jacket works on snow; and a **litter or sled** — a seat frame, the panelling, a tarp or a blanket
between two poles — dragged over snow hauls a person much farther for the same effort, which is why it
is the real answer (the world design already has a drag litter of panelling and cord). Carrying makes
the **carrier** hot and sweating — the deferred cold debt (document 08 §4.2) — while the **carried**
person, not moving and often lying on snow, cools fast and needs insulation under and around them.
Moving an unsplinted break grinds the bone ends: pain, more bleeding, damaged nerves. Two people
carrying one needs a co-operative form in the grammar (two actors on one entity), which is documents 04
and 19 to write.

### 4.10 Painkillers

*(Proposed by Claude, for Andrew's check.)* Pain is a state on the part (§4.6) and part of what limits
the part, so masking it is modelled, honestly. Ibuprofen — the nurse's pouch holds a count of tablets —
works in 30–60 minutes and lasts four to six hours; it lowers pain and swelling, and `status`
truthfully reports less pain while the wound is unchanged: that is the fair lie. How much the part
gives back depends on the wound — a sprain's limit is mostly pain, so the nurse walks better; a broken
bone's limit is mechanical, so no pill makes it bear weight. Its real prices: it slows clotting (the
bleeding townie should not take it), and taken while dehydrated it can injure the kidneys (document
09's clock). It is also the field treatment for frostbite. Whisky dulls pain and judgment, and it opens
the skin's blood vessels and blunts shivering, so it costs heat — the brandy-in-the-snow cure is a myth.
Willow-bark tea (document 23) is a weak real painkiller.

### 4.11 How impairment reads

*(Proposed by Claude, for Andrew's check.)* By what the body really does, and never by doing something
the player did not type. A concussion is headache, nausea, dizziness, light sensitivity, fatigue and
slowness — not a world that looks wrong — so the salesman's first day is slower acts (activities take
longer, document 06), more fine-work failures, lines of headache and nausea, and a pull toward sleep;
the room reads true. Hypothermia's confusion (document 08's `impaired` band) is clumsiness and poor
judgment: the fumbled match, the knot that will not hold, the slurred word. So the rule: **the body can
fail at an act** — fumble it, slow it, collapse, lose consciousness (a missing member is already
incapacitated where they lie) — **but the engine never performs an act the player did not type.**
Severe hypothermia's paradoxical undressing is real — the dying feel hot and strip — and it arrives as a
felt urge in the prose ("the parka is unbearable"); taking it off is the player's choice.

### 4.12 Seeing another person's wounds

*(Proposed by Claude, for Andrew's check.)* By the senses, the way the tell-and-hide rule works for
everything else (document 03 §4.3: the worn layer is what shows). **Looking** shows what the covering
allows — blood through a sleeve, a limp, a white patch on a bare cheek, a leg at the wrong angle,
pallor, shivering; what is under a glove or a boot stays hidden until someone takes it off, which costs
that part its heat. **Touch** gives heat — a hot forehead is a fever, a cold hand is cold — swelling and
a pulse; **smell** gives an infected wound away. Wounds and parts carry this in their `sensed` rows
(document 05 §4.5). Asking is speech, and the person can answer truly or not. Each is its own act:
`examine Mara`, `examine Mara's hand`, `feel Mara's forehead`, `take the glove off Mara's hand`.

### 4.13 The `make a splint` rows (Andrew, 2026-09-18)

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
- **The combat design** *(to be written)* — blows, cuts and stabs, delivered as wounds on parts.
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
  blood loss, the bear, the cold and thirst — poison sickens but never kills, and other harms weaken.

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
- The injury processes: bleeding per tick, binding stopping it, infection, fever.
- Treatment as an act on a *wound*: `press`, `pack`, `splint`, `stitch`, `clean` —
  the first-aid kit's contents have no use-verb yet.
- The injuries the world can *inflict*: frostbite from bare regions, burns, hypothermia, smoke
  inhalation, exhaustion, snow blindness, carbon monoxide.
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
