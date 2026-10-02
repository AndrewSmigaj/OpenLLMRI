# 09 — Water

> **Status: reviewed with Andrew 2026-09-18.**
> **Architecture counterpart:** none.

---

## 2. Decisions

### Andrew's decisions

- **(2026-09-07)** Water comes from melting ice in a container over the fire, from a stream, or from
  wherever else it can be had. Two things follow: water comes from more than one place, and the
  melting way runs through *a container* and *a fire* — it is a chain, not a verb.
- **(2026-09-07, 2026-09-27)** Every goal has several ways, water included, with no set number.
- **(2026-09-18)** Liquids are measured in millilitres: melting some snow is never a one-use thing.
- **(2026-09-27)** Thirst kills, on its real clock; nothing kills instantly.
- **(2026-09-18)** Thirst kills in a realistic time for thirst — though usually something else gets a
  person first — and a person needs to drink more than they eat.
- **(2026-09-27)** One of the packs holds a few iodine tablets, only a couple of days' worth
  (document 16).
- **(2026-09-18)** Eating snow is allowed and costs body heat.
- **(2026-09-18)** There is no boiling gate — just melting.
- **(2026-09-18, 2026-09-27)** Contamination is carried as provenance: fuel and oil, and germs
  depending on the source, realistically — not every water has them; melted clean snow is safe to
  drink, and lake water is likelier to carry them. The specifics are Claude's, left to Claude (§4.6).
- **(2026-09-18)** Steam is an entity. Players are not expected to build things to condense it, but if
  someone — a model included — thinks to, the steam is there.
- **(2026-09-18)** `fill` moves as much as fits. Much of the rest will be learned from how players and
  agents try to use the system.
- **(2026-09-27)** The season is the first week of October: the creek runs, the lake is open, and still
  water has skim ice; the ground is bare at the start, and snow comes on and off, building to a couple
  of inches by the end (document 13 §4.2).

### Proposals (Claude)

- The source, action and vessel lists and the vessel-safety idea, carried from the first AI-written
  seed through GDD §31–§36 — kept here as proposals.
- Hydration as an integer in millilitres spent per tick and per activity.
- The ways to water and their key resources (§4.3).
- The real figures: daily need, the heat cost of eating snow, the melt ratios (§4.6).
- What each source carries, and the numbers for it (§4.6) — Claude's call, as Andrew left it.
- Every number on this page.

---

## 3. In one paragraph

The water is there, and all of it costs something. The creek still runs and the lake is open, skinned
with ice at its edges — but both are a walk from the wreck, and a wet boot on the way is the cold's
opening. At first there is no snow at the wreck, only frost and frozen puddles, and the week never lays
more than a couple of inches. Snow is water you pay for twice — once in fuel to melt it and once in the
heat it steals if you cheat and eat it. That price is why the half-full canteen in the backpack matters
and why the open water at the riffle is worth the walk. Getting a drink is a small chain done right:
find something that holds liquid, fill it at the creek or pack it with ice from the puddles and the
pond edges, or with snow once it falls, get it near the fire you already have, wait, drink. Getting it
wrong is also modelled: a fuel-smelling can, snow scooped from under the wing where the fuel pooled, a
bottle you bled into. Thirst does not kill you as fast as the cold does, but it makes everything else
worse, and it is the quiet reason a party that never lights a fire loses even the days the cold was
going to give them.

---

## 4. The design

### 4.1 The rules

1. **Hydration is a number on the body**, in millilitres, spent per tick and per activity; drinking
   adds. Surfaced as words and on the meters (document 08 §4.9), never as a number. *(Proposal.)*
2. **What water carries, it carries from its source and its vessel** (Andrew, 2026-09-18:
   contamination is provenance). Melted snow is not safe just because snow is: a vessel that held fuel
   or oil, a bloody one, or one made of something toxic passes it on, and so does snow scooped where
   fuel pooled. This makes the *vessel* the interesting object (GDD §31–§36).
3. **Frozen water is not water.** `drink snow` does not slake; it redirects with the physics of why
   ("melt it to water first"). *(Shipped.)*
4. **Eating snow is always possible and always costs heat** (Andrew, 2026-09-18) — a redirect with a
   consequence, never a refusal. The world lets you do the stupid thing and charges you for it.
5. **Melting is a chain, not a verb** (Andrew, 2026-09-07): a vessel, a heat source, and time —
   melting ice in a container over the fire.
6. **Several ways**, spending different key resources (§4.3).
7. **Never a menu.** The world does not tell you that you are thirsty in a way that names the cure,
   does not list vessels, and does not suggest melting. The thermos is described as a thermos.

### 4.2 The pieces (from the seed's lists — proposals, and each a floor)

| | the list (a floor, not a limit) |
|---|---|
| **sources** | snow · ice · creek water · lake water · stored drinks · liquid from canned food · condensation · unsafe aircraft fluids |
| **actions** | gather · melt · boil · filter · store · spill · freeze · contaminate · clean a container |
| **vessels** | a bottle · a canteen · a pot · a food can · a plastic bag · a glove · a helmet · a folded aircraft panel · an improvised bark or fabric carrier |

The vessel list is the interesting half: none of those are "water containers" by type, they are
things that happen to hold liquid. That is the ontology rule doing the work — a helmet holds water
because of what a helmet *is*, and the same must be true of anything else a player reasonably tries.

### 4.3 The ways to water

| way | key resource it spends | where | the chain |
|---|---|---|---|
| **the canteen / thermos as found** | knowledge (search) | cockpit, rear cabin | `search backpack` → `drink from canteen` |
| **melt snow or ice by fire in a vessel** | fuel + a vessel | anywhere with a fire | `put snow in thermos` → `put thermos by fire` → `drink` |
| **melt by body heat** | warmth (slow, and it costs you) | any | `put snow in canteen` → wear it under the jacket → time |
| **the creek, the lake, a seep** | a walk + daylight + the risk of wet feet | the outlet riffle, the fishing pool, the lake shore and the inlet mouth | `fill canteen from the creek` |

### 4.4 The valley's water (content — document 01's zones)

- **The outlet riffle** — free-running water: "a full container without spending a stick of firewood
  — the efficiency prize that funds every other fire". Priced in the walk and in wet risk: shelf ice
  rims the banks, thin at its lips, and kneeling on it is a plunge to the knee and the wet-boot clock.
- **The lake** — open at the start, with skim ice at its margins and on the ponds after a cold night;
  skim ice holds nothing. The inlet mouth is the north's liquid water, a walk west across the muskeg;
  at the shore a stick or a stone breaks the skim and a vessel dips, and a careless step soaks a boot.
- **Ice** — the frozen puddles round the wreck on the first mornings (carrying whatever the puddle
  held — fuel, under the wing), the skim ice from still water and the shelf ice on the creek. Ice is
  cleaner than the water it froze on, and gives far more water for its volume than snow does (§4.6).
- **Holt's water** — the homestead's own path down to the creek: bucket-water without the riffle's
  risks, the reward for the walk there.

Inside the wreck: the thermos of coffee in the cockpit, the half-full canteen in the backpack behind
the jammed aft bin, the salesman's steel water bottle and hip flask, and whatever the flurries blow in
through the hull breach — a skin of snow on the floor that is indoor weather and also the room's water
source, a little more after each flurry.

### 4.5 The `make water` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | water |
|---|---|
| `goal` | water · a drink · melt water |
| `vague` | "How are you going to get water?" |
| `roles` | **source**: snow, ice, the creek, the lake, a seep · **vessel**: a thing with `vessel` · **heat** (optional): a fire or a body |
| `realize` | with heat: `melt <source> in <vessel>` · without: `fill <vessel> from <source>`, or eating snow, which always works and always costs warmth |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

### 4.6 Liquids, thirst, snow and contamination (Andrew, 2026-09-18)

**Liquids have units.** Water is millilitres, not a token: a vessel has a capacity in ml, melting snow
yields ml in proportion to what you melted, a mouthful takes ml, and a half-full canteen is half full.
Melting some snow is never a one-use thing. Liquids are the same aggregate shape as a handful of stones
(document 04 §3.11): one entity, a quantity, split when spent.

**Thirst kills on a realistic clock, and you need more water than food** — though other things
usually get a person first.

| | proposal (real figures) |
|---|---|
| daily need, cold and working | ~3,000 ml |
| daily need, resting | ~2,000 ml |
| nothing at all | degrading within hours; dead in about three days, sooner if working |
| what usually happens first | the cold or an injury — thirst is the clock underneath, not the headline |

Cold is the trap: you do not feel thirsty, and you lose water breathing dry air all day. The symptoms
come before the danger — headache, dullness, poor decisions — and dehydration makes the cold worse,
so thirst kills mostly by making everything else harder. *(Numbers are proposals, tunable by probes.)*

**Eating snow works, and here is what it costs.** Melting a litre of snow inside you takes the latent
heat of fusion plus warming it from freezing to blood temperature: about **490 kJ, roughly 120 kcal,
taken straight out of your core**. And snow is mostly air:

| source | volume needed for 1 L of water |
|---|---|
| fresh loose snow | ~10 L |
| wind-packed snow or old settled snow | ~3 L |
| ice | ~1.1 L |

So eating snow is always allowed, always costs warmth you can feel, and ice — the frozen puddles, the
pond skins, the creek's shelf ice — gives nearly ten times the water of fresh snow for its volume, a
real thing to learn. Melting it over a
fire costs fuel instead of body heat, which is the whole point of having one.

**No boiling gate.** Most of the valley's water is safe enough to drink, so boiling is never a wall
between the party and a drink. It is still worth doing — it is warm, it makes tea, it thaws — and a
rolling boil for about a minute kills every germ the water carries (CDC).

**What the water carries depends on where it came from** (2026-09-27; the specifics are Claude's, as
Andrew left them). Not every water has germs:

| source | what it can carry |
|---|---|
| fresh snow, away from the camp and from animals | nothing worth fearing — people melt it and eat it safely |
| trampled or yellow snow; snow by the camp, the latrine, a carcass or animal sign | germs from people and animals — the camp makes its own dirty snow |
| snow under the wing where fuel pooled; anything melted in the jerry can | fuel |
| skim ice and the creek's shelf ice | less than the water it froze on — freezing kills some germs, not all |
| the creek, running | some risk: beaver fever from beavers upstream — higher below the lodge, lower in fast water |
| the lake, still | the likeliest: beaver fever, and bacteria from birds and animals — worst near the beaver lodge and the marsh edge |
| the canteen, the thermos, bottled drinks | whatever they were filled with |

The germs are real and so is their timing. Bacteria such as *Campylobacter* show in two to five days —
inside the run — as cramps, diarrhoea and fever, which spend water on thirst's clock; beaver fever
(*Giardia*) takes one to three weeks, so a party drinking lake water on day one may feel it at the very
end or not within the run (CDC). Whether a given drink sickens is seeded chance by its dose (DR-12).
What kills them: boiling, always; **iodine tablets**, given time — about half an hour, longer in water
near freezing — for most of them; a cloth filter takes out silt, not germs. The one pack's few tablets
(document 16) make a couple of days of safe water, which is why the lake is worth boiling for.

**Fuel and oil** are the aircraft's own hazard. Snow scooped from under the wing where fuel pooled, water melted in the jerry can, a vessel that
held oil — the water carries it, it smells and tastes of it, and drinking it makes you sick (sick, not
dead: poison never kills, 2026-09-27). Contamination is **provenance**, carried from the source or the
vessel exactly as the conservation rules already carry it: a vessel carries what it has held and what
is on it — fuel, oil, blood, ash, dog food — and melting snow in the jerry can gives you avgas-smelling
water that the narration names before you drink it, not after. `examine` or a sniff gives it away.
Cleaning a vessel is an ordinary act — scour it with snow, burn it out — the answer to a problem the
player created, not a special mechanic.

**Steam is a thing, if someone thinks to make it.** Boiling water produces steam as a real entity;
where it meets something cold it condenses. Nothing authors a still, and nothing needs to: the pieces
are there for anyone who reasons their way to it, which is the whole point of the world.

**`fill` is a transfer of as much as fits.** `fill the canteen from the creek`, `fill the thermos with
snow`, `fill the tin from the lake` — it moves as much as the target can take from the source, and
the world says what you got ("the canteen is full"; "there is enough to cover the bottom of the
tin"). The same budget rule as every other quantity (document 04 §3.11), and the same one operation
over any vessel and any source — water, fuel or snow.

## 5. Interactions

**This depends on:**
- **07 Fire and shaping** — the melting way's heat source; boiling.
- **08 Warmth, clothing and shelter** — eating snow costs heat; melting by body heat costs warmth;
  wet feet from drawing water at the riffle feed straight back into the cold clock.
- **17 Rooms and living rooms** / **18 Materials and forms** — `snow` and `ice` are materials with
  potability and the `frozen_water` tag; vessels are things whose form holds liquid.
- **06 Time, sleep and the clock** — melting is an unattended process; hydration is spent per tick.
- **13 Events, escalation and weather** — the creek and the lake through the week, the snow the week
  lays (§4.2).

**These depend on it:**
- **10 Food and hunger** — cooking and boiling share the vessel and the fire; dehydration makes
  hunger worse.
- **11 Injury and first aid** — bleeding costs hydration; a fever costs water; whisky and sanitizer
  are liquids that are not drinks.
- **13 Events, escalation and weather** — thaw and refreeze, a frozen canteen, skim ice thickening.
- **14 Rescue paths** — a day spent away from water, signalling from the ridge or walking to the
  cabin, is priced partly in water logistics.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-16** — first draft, gathering the water material from the earlier passes and the seed.
- **2026-09-18 (Andrew)** — the `make water` goal rows; liquids in millilitres; thirst kills on a
  realistic clock, and the daily need is larger than the food need; the real cost of eating snow; no
  boiling gate; contamination as fuel and oil, carried as provenance; steam as an entity; `fill` moves
  as much as fits. Reviewed in full.
- **2026-09-27** — the first week of October carried in: the creek runs, the lake is open and still
  water has skim ice, so the midwinter features (a chopped water hole, overflow, the lake's blue ice)
  are gone; thirst's clock set beside the rule on what kills (§6).
- **2026-09-27 (Andrew)** — thirst kills, on its real clock; a few iodine tablets in one of the packs;
  whether water carries germs depends on its source, realistically, with the specifics left to Claude
  (§4.6).
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).

## 8. What exists today

**Built**
- `game/world/sim/operations/handlers/melt.py` — `melt` / `thaw` over anything tagged `frozen_water`,
  given a heat source (the tool's flame or any lit thing reachable); the ice is consumed and an equal
  mass of water is minted, ledger-balanced; informative redirects for a composite target and for no
  heat.
- `game/world/sim/operations/handlers/drink.py` — `drink` / `sip` / `gulp` / `swig` over any material
  with potability; frozen water redirects to "melt it first"; low-potability liquids get the
  risky-drink narration. Drinking consumes the liquid.
- `game/world/sim/operations/handlers/pour.py` — `pour` / `tip` / `douse` / `splash` X on/into Y;
  water on a lit thing douses it, otherwise it wets the target; a sealed vessel pours nothing.
- Materials: `snow` (potability, edibility, `frozen_water`), `ice` (potability, `frozen_water`,
  brittle), `water` (high potability, `liquid`, `extinguisher`), `alcohol` (low potability, liquid,
  flammable).
- Objects: the thermos of coffee, the half-full canteen, the steel water bottle and its water, the
  hip flask, the snowdrift in the rear cabin, the jerry can with its `sealed` bit.
- Tests: `game/tests/sim/test_operations_survival.py` covers drinking water, the frozen redirect, the
  non-potable non-match, and mass conservation. Probes in `probes/census.py`:
  `cockpit.drink_coffee`, `cockpit.drink_from_thermos`, `rear_cabin.drink_from_canteen`,
  `rear_cabin.dig_snowdrift` measured passing; `rear_cabin.melt_snow`, `rear_cabin.melt_drift`,
  `outside_nose.melt_snow`, `fuselage_top.melt_ice_on_cable`, `cockpit.scrape_frost` still `todo`.

**Designed, not built**
- Hydration as a number spent on the clock.
- Contamination as provenance on water and vessels; boiling as a heat state; cleaning a vessel.
- The melt-in-a-vessel chain as a timed process rather than an instant operation.
- The valley's water (document 01's zones) — designed, not yet data.
- Liquid containers with volume, `fill` and `pour into` — on `BACKLOG.md` under
  "Containment/clothing v2".

**Nothing**
- `game/world/sim/systems/water.py` is a docstring and `from __future__ import annotations`.
- Liquid volume: the canteen is an object *made of* water, and
  [`containment.md`](../architecture/containment.md) records that liquid containers are not modelled
  (only the jerry can's `sealed` bit gates pouring).
- There is no `fill` operation, no `boil`, no `gather`, no `filter`, no container cleaning; the
  handler set today is `bend, break, burn, cut, drink, eat, examine, light, make, melt, open/close, pour,
  pry, move, read, search/dig, take/put, talk, tie, use, wear, wrap, tear`.
- Drinking has no hydration effect — it consumes the liquid and narrates; nothing on the character
  changes.
- `eat snow` currently succeeds as a meagre meal (snow carries a low edibility) and costs no heat.
