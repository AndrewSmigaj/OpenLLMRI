# 09 — Water

> **Status: `draft for review` (2026-09-16). NEW — this system had no design document of its own.**
> **Architecture counterpart:** none. **Sources:** `docs/investigation/design/rescue-graph.md` §WATER
> (the four paths; eating snow costs heat) · `docs/investigation/design/time-and-stakes.md` §4
> (hydration as a number; drying and wetting) · GDD §31–§36 ("water — safety gated by container
> state") · the archived AI seed `design.md` §33 (sources, actions, containers, the safety rule),
> which GDD §31–§36 carries forward "unchanged" · `docs/architecture/containment.md` (final line:
> liquid containers are not modelled) · `BACKLOG.md` Later, "Containment/clothing v2" (liquid
> containers: drink-from / pour-into / fill) · `docs/investigation/world/rooms.md` (the valley's
> water zones and the manual's WATER page) · code: `game/world/sim/operations/handlers/melt.py`,
> `pour.py`, `drink.py`; `game/world/sim/systems/water.py`.

---

## 2. Provenance

### Andrew's decisions

- **Water sources: melting ice in a container over the fire, a stream, or whatever.** (2026-09-07.)
  Two things are decided by that sentence: water comes from more than one place, and the melting
  path runs through *a container* and *a fire* — it is a chain, not a verb.
- **Several ways of doing things** (2026-09-07, his general rule, recorded in the provenance audit)
  — water is one of the four "stay alive" goals and inherits the at-least-three-paths rule.

That is all that is decided. Everything else below is a proposal.

### Proposals (Claude)

- The seed's source, action and container lists and the container-safety rule (`design.md` §33) come
  from the **archived AI-written seed**, not from Andrew; GDD §31–§36 carries them "unchanged", which
  has given them an authority they were never granted. They are kept here as proposals.
- Hydration as an integer in millilitres spent per tick and per activity (`time-and-stakes.md` §4).
- The four water paths and their key resources (`rescue-graph.md` §WATER).
- Eating snow as always possible and always costing heat.
- Every number on this page.

---

## 3. In one paragraph

You are surrounded by water and none of it is water. Snow is water you have to pay for twice — once
in fuel to melt it and once in the heat it steals if you cheat and eat it — and the price is why the
half-full canteen in the backpack matters and why the black lead of open creek at the outlet riffle
is worth a walk. Getting a drink is a small chain done right: find something that holds liquid, put
snow or a slab of blue shore ice in it, get it near the fire you already have, wait, drink. Getting
it wrong is also modelled: a dirty vessel, a fuel-smelling can, a bottle you bled into. Thirst does
not kill you as fast as the cold does, but it makes everything else worse, and it is the quiet
reason a party that never lights a fire loses even the days the cold was going to give them.

---

## 4. The design

### 4.1 The rules

1. **Hydration is a number on the body**, in millilitres, spent per tick and per activity; drinking
   adds. Surfaced as words, never as a number. *(Proposal, `time-and-stakes.md` §4.)*
2. **Water safety is gated by container state**, not by a water-quality stat. Melted snow is not
   automatically safe if the container is dirty, fuel-contaminated, bloody, or made of something
   toxic (GDD §31–§36; `design.md` §33). This is the design's one real opinion about water and it is
   a good one: it makes the *vessel* the interesting object.
3. **Frozen water is not water.** `drink snow` does not slake; it redirects with the physics of why
   ("melt it to water first"). *(Shipped.)*
4. **Eating snow is always possible and always costs heat** — a redirect with a consequence, never a
   refusal. The world lets you do the stupid thing and charges you for it (`rescue-graph.md` §WATER).
5. **Melting is a chain, not a verb.** A vessel, a heat source, and time. Andrew's own phrasing —
   "melting ice in a container over the fire" — is the specification.
6. **At least three paths**, spending different key resources (§4.3).
7. **Never a menu.** The world does not tell you that you are thirsty in a way that names the cure,
   does not list vessels, and does not suggest melting. The thermos is described as a thermos.

### 4.2 The pieces (from the seed's lists — proposals, and each a floor)

| | the list (a floor, not a limit) |
|---|---|
| **sources** | snow · ice · creek water · stored drinks · liquid from canned food · condensation · unsafe aircraft fluids |
| **actions** | gather · melt · boil · filter · store · spill · freeze · contaminate · clean a container |
| **vessels** | a bottle · a canteen · a pot · a food can · a plastic bag · a glove · a helmet · a folded aircraft panel · an improvised bark or fabric carrier |

The vessel list is the interesting half: none of those are "water containers" by type, they are
things that happen to hold liquid. That is the ontology rule doing the work — a helmet holds water
because of what a helmet *is*, and the same must be true of anything else a player reasonably tries.

### 4.3 The four paths (the rescue graph's own check)

| path | key resource it spends | where | the chain |
|---|---|---|---|
| **the canteen / thermos as found** | knowledge (search) | cockpit, rear cabin | `search backpack` → `drink from canteen` |
| **melt snow or ice by fire in a vessel** | fuel + a vessel | anywhere with a fire | `put snow in thermos` → `put thermos by fire` → `drink` |
| **melt by body heat** | warmth (slow, and it costs you) | any | `put snow in canteen` → wear it under the jacket → time |
| **the lake lead / the seep** | risk + daylight | the inlet mouth, the shore, the creek | `fill canteen from lead` |

### 4.4 The valley's water (content — from the world design)

The fifty outdoor zones already price water honestly (`rooms.md`):

- **The outlet riffle** — free-running liquid water under a black open lead, "the melting-fuel
  bypass: a full container without spending a stick of firewood — the efficiency prize that funds
  every other fire". Priced in approach and wet risk: the ice shelves over it are "thin as biscuit"
  at their lips, and kneeling on one is a plunge to the knee and the wet-boot clock.
- **The inlet mouth shore lead** — the north's liquid water, so a day out on the lake signalling
  runs real logistics instead of a fuel-melting tax. The safe draw is the long way round on grounded
  gravel, prone, with a lashed dipper; the short way is forty feet of drum-note thin ice.
- **Blue ice** — the shore apron's blue ice chunks are "cleaner and denser than snow for melting",
  and the pressure ridge's clear blue slabs are "the cleanest melt-water stock on the map, already
  broken into liftable slabs (a container and a fire still gate the payoff)".
- **Holt's water hole** — a chopped basin in the creek ice under a weighted plank lid, a dipper can
  hanging on its wire above it. Break the thin skin and the homestead has bucket water with none of
  the riffle's risk: the walk-out route's reward, made concrete in chores.
- **The overflow bend** — the anti-water: water standing on top of good ice under fresh snow. It
  does not give you a drink, it soaks your boots a mile from a fire. Three telegraphs (the stain,
  the steam, the sag) and a definitive test (a pole comes up wet).
- **The manual's WATER page** is the in-world teacher for all of it: boil everything, blue-ice
  efficiency, melt ratios.

Inside the wreck: the thermos of coffee in the cockpit, the half-full canteen in the backpack behind
the jammed aft bin, the salesman's steel water bottle and hip flask, and the snowdrift that has
banked in through the hull breach — indoor weather that is also the room's water source.

### 4.5 Boiling, safety and contamination (proposal)

The seed's rule and the GDD's one-liner agree: safety is about the vessel, not the source. The
proposal for how that reads in play:

- A vessel carries what it has held (`provenance` is already conserved) and what is on it: fuel,
  blood, ash, dog food. Melting snow in the jerry can gives you avgas-smelling water and the
  narration says so before you drink it, not after.
- Boiling is a heat state of the water, not a separate purification stat: wild water wants boiling
  (the manual says so; the giardia line is authored), melted clean snow does not.
- Cleaning a container is an operation in the seed's action list and should stay one — it is the
  answer to a problem the player created, which is the shape everything in this game wants.

---

### The `make water` rows (Andrew, 2026-09-18)

The goal table's rows for this system; the form and the dispatch rule are document 04 §3.9. Vague, `make`
asks how; given the means it performs the act they imply and this system answers.

| field | water |
|---|---|
| `goal` | water · a drink · melt water |
| `vague` | "How are you going to get water?" |
| `roles` | **source**: snow, ice, a lead, a seep · **vessel**: a thing with `vessel` · **heat** (optional): a fire or a body |
| `realize` | with heat: `melt <source> in <vessel>` · without: `fill <vessel> from <source>`, or eating snow, which always works and always costs warmth |

*(Proposal: the row set is a floor — the loops add goals and means from what people and agents type.)*

## 5. Interactions

**This depends on:**
- **07 Fire and shaping** — the melting path's heat source; boiling.
- **08 Warmth, clothing and shelter** — eating snow costs heat; melting by body heat costs warmth;
  wet feet from drawing water at the riffle feed straight back into the cold clock.
- **17 Rooms and living rooms** / **18 Materials and forms** — `snow` and `ice` are materials with
  potability and the `frozen_water` tag; vessels are things whose form holds liquid.
- **06 Time, sleep and the clock** — melting is an unattended process; hydration is spent per tick.

**These depend on it:**
- **10 Food and hunger** — cooking and boiling share the vessel and the fire; dehydration makes
  hunger worse.
- **11 Injury and first aid** — bleeding costs hydration; a fever costs water; whisky and sanitizer
  are liquids that are not drinks.
- **13 Events, escalation and weather** — thaw-refreeze, overflow, a frozen canteen.
- **14 Rescue paths** — the walk-out and any day spent out on the ice are priced partly in water
  logistics.

---

## 6. Open questions

1. **Are liquid containers modelled at all in v1?** Today they are not: `containment.md` ends
   "liquid containers are NOT modeled (only the jerry can's `sealed` bit gates pouring)", and the
   canteen is an object *made of* water. *(a)* Model volume in millilitres with `fill` / `pour into`
   / `drink from`. *(b)* Keep liquids as whole objects that live inside vessels.
   **Recommendation: (b) first, (a) soon** — whole-object liquids already conserve mass correctly and
   ship today; volume is what `fill`, partial drinks and "the canteen is half-full" actually need,
   and it is already on the backlog.
2. **Does thirst kill, or only degrade?** *(a)* A real dehydration track that ends in death.
   *(b)* Dehydration degrades — headaches, slower work, worse cold tolerance — and the cold or
   hunger finishes it. **Recommendation: (b)**, because a week is short for thirst to be the
   headline killer and because the interesting failure is the compounding one.
3. **How expensive is eating snow, exactly?** It must be possible, must always cost heat, and must
   not be a trap that reads as a bug. **Recommendation: a real and visible warmth cost, with the
   narration owning it** — "it slakes something and takes something" — so the lesson is learnable in
   one go without a warning.
4. **Is boiling required for wild water, mechanically?** *(a)* Yes, with an illness consequence for
   skipping it. *(b)* Advisory only — the manual says boil, and nothing enforces it.
   **Recommendation: (a) but gentle** — a delayed, survivable, miserable consequence; a party that
   ignores a page of the manual should find out it was right, not die of it.
5. **What does "contaminated" do to a vessel, and can it be undone?** **Recommendation: a state on
   the vessel that the description carries and that fire or clean snow can clear** — it is a puzzle
   with an answer, not a ruined object.
6. **Does condensation survive as a source?** It is in the seed's list and it is real (a plastic bag
   on boughs, breath on metal). **Recommendation: keep it as an emergent possibility** rather than
   an authored path — if the ontology is right it should just work, and it is nobody's plan A.
7. **Where does `fill` live in the grammar?** `fill can from wing` (fuel), `fill canteen from lead`
   (water) and `fill pot with snow` are all the same operation over different materials.
   **Recommendation: one `fill` operation over any vessel and any source**, authored once — the
   censuses and the rescue graph both voted for it.

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-18:** the `make water` goal rows added (document 04 §3.9 owns the form and the dispatch rule).

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
- Hydration as a number spent on the clock (`time-and-stakes.md` §4).
- The safety model: container state gating potability; boiling; contamination; cleaning a vessel
  (`design.md` §33, GDD §31–§36).
- The melt-in-a-vessel chain as a timed process rather than an instant operation.
- The valley's water zones (`rooms.md`) — designed in full, not yet data.
- Liquid containers with volume, `fill` and `pour into` — on `BACKLOG.md` under
  "Containment/clothing v2".

**Nothing**
- `game/world/sim/systems/water.py` is a docstring and `from __future__ import annotations`.
- There is no `fill` operation, no `boil`, no `gather`, no `filter`, no container cleaning; the
  handler set today is `bend, break, burn, cut, drink, eat, examine, light, make, melt, open/close, pour,
  pry, move, read, search/dig, take/put, talk, tie, use, wear, wrap, tear`.
- Drinking has no hydration effect — it consumes the liquid and narrates; nothing on the character
  changes.
- `eat snow` currently succeeds as a meagre meal (snow carries a low edibility) and costs no heat.
