# The plane — a realistic interior inventory (content design)

> **Status: SCRATCHPAD — iterating with Andrew (2026-07-04).** The exhaustive what-COULD-be-there
> list for a realistic Alaska bush plane, section by section, before we choose what makes the
> scenario. Nothing here is content until curated into `build.py`/`zones.py` per the process.

## 1. What aircraft is this?

"Big enough for two rows of seats in the back, pilot only aboard" describes the classic Alaska
workhorses almost exactly:

- **Cessna 206/207 Stationair** — six seats (pilot + copilot up front, two rows of two behind),
  piston single, clamshell **cargo double-door** on the right rear, hat shelf + netted baggage
  bay behind the last row. The default choice.
- **de Havilland DHC-2 Beaver** — THE Alaska bush plane; radial engine, 6–7 seats, huge cargo
  doors, floats/skis/wheels.

Recommendation: model a **206-class piston single on wheel-skis**. One realism flag on our
current fiction: real bush planes have **no airline-style overhead bins** — they have a hat
shelf, floor tie-down tracks, and cargo netting. Options: (a) re-fiction our two "overhead bins"
into a **netted cargo bay + a hat shelf + a jammed cargo door**, or (b) keep the bins as fiction.
(a) is more Alaska and gives the same open/pry loops. **Andrew's call.**

## 2. Up front — the cockpit (pilot + right seat)

**The panel (fixtures; mostly salvage-by-parts):**
- The six-pack: airspeed indicator, attitude indicator, altimeter, turn coordinator, heading
  indicator, vertical-speed indicator — glass faces, cases, tiny screws.
- Engine gauges: tachometer, manifold pressure, oil temp/pressure, cylinder-head temp, fuel
  quantity L/R, ammeter, suction gauge.
- Magnetic **compass** on the glareshield (takeable! navigation!), outside-air-temp probe.
- **Radios**: VHF comm/nav stack, audio panel, transponder, maybe an old GPS unit — and the
  **ELT remote switch** with its ARM/ON/TEST placard (the breadcrumb pointing at the tail).
- Circuit-breaker panel, master/avionics switches, magneto key (in the ignition — or the
  pilot's pocket?), cabin-heat and defrost knobs, fuel selector valve, trim wheel, flap lever,
  throttle/prop/mixture levers, parking brake.
- Two **yokes**, rudder pedals, **two headsets** (hung on the yokes; ear seals = insulation,
  cord = wire), push-to-talk switches.
- **Sun visors**, vent windows, windshield (crazed plexiglass — sharp sheets).
- A small **halon fire extinguisher** bracketed under the panel (common, near-universal).

**Door pockets & the pilot's kit:**
- **Sectional charts** (paper — tinder AND a map of where you are!), approach plates, a
  **kneeboard** with the flight plan and weight-and-balance sheet, grease pencil, pens.
- The **flight bag**: POH (our flight manual ✓), aircraft/engine logbooks, E6B flight computer
  (aluminum!), **fuel tester/sump cup**, **flashlight** + spare batteries, spare fuses,
  multitool ✓, work gloves, spare glasses.
- Personal effects: **thermos of coffee** (warm liquid!), sunglasses, lighter ✓ / matches,
  snacks, wallet, cigarettes, chapstick, and — very Alaska — a **satellite communicator
  (inReach/PLB)** or satphone. If we include one, it must be authored BROKEN or lost, or the
  game ends in five minutes. (Great cruel find: a PLB with a shattered antenna/dead battery —
  parts for the radio arc.)

**The pilot himself (existing ✓):** flight jacket ✓, lighter in pocket ✓; add: wallet, a keyring
(the magneto key?), a wristwatch, dog tags/ID — dignity-line territory, all optional.

## 3. The middle — two rows of passenger seats

- **Four seats** (two rows of two): cushions ✓, covers ✓, seatbelts ✓ (that's 4× webbing!),
  seat rails, adjustment levers, literature pockets on seatbacks ✓ (×4 — safety card, sick bag,
  someone's paperback, gum wrappers, a dead phone?).
- **Headsets** on hooks by each seat (more wire, more ear-seal foam).
- Air vents (wemacs), dome lights + lenses, window shades (rare in bush planes), armrests.
- **Windows**: big plexiglass panes — pryable sheets (windbreak! sled base! heliograph-ish?).
- **Floor**: carpet/rubber mats (insulation underfoot!), **cargo tie-down rings in floor
  tracks**, **tie-down straps/ropes** (cordage beyond the paracord), mud, gravel, a lost glove.
- Cabin **wall insulation batting** behind the headliner and side panels — the material table
  already anticipates `insulation_batting`; tearing panels open is a warmth jackpot.
- Possibly a second small fire extinguisher aft.

## 4. The back — baggage bay & tail cone

**The legally-required survival kit (THE find — see §7):** a duffel or ammo-can lashed in the
tail, containing per AS 02.35.110 (winter config, since it's Whiteout):
- **A week of rations per occupant** (dense stuff: pilot bread, pemmican-ish bars, tins),
- **an axe or hatchet** (the tool that changes the wood loop),
- **a first-aid kit** ✓ (ours can move here or stay a bin find),
- **two sealed signaling devices** (smoke bombs / railroad fusees / flare-pistol shells —
  fire-starting cheats AND rescue signals),
- the traditional list adds: an **assembled fishing kit** (hooks, line, sinkers), a **knife**,
  **two boxes of waterproof matches**, **mosquito headnets** (summer — netting = straining
  water, bandaging),
- winter (Oct 15–Apr 1): **snowshoes** (mobility over the drifts!), **a sleeping bag** (warmth
  mother-lode), **a wool blanket per occupant** (ours ✓ — now it has a reason to exist).

**Freight & luggage (a bush plane is a truck):**
- Passenger luggage: our duffel ✓ + a second bag or two; a cooler (empty? groceries?);
  **mail sacks** (paper! twine!); a **groceries box** for a village (canned goods, coffee,
  flour); a **machine-parts crate** (steel bits, bolts, grease).
- **Engine oil quarts** (2–6 always; oil burns dirty = signal smoke), an oil **funnel**, rags ✓.
- **The tool roll**: screwdrivers, pliers, safety wire (WIRE!), **duct tape** (always),
  hose clamps, bungee cords, spare spark plugs.
- **Engine & wing covers** — big insulated fabric blankets bush pilots use at every cold stop:
  enormous wearable/shelter fabric, totally period-correct.
- A **tarp**, tiedown ropes, wheel chocks, an ice scraper, maybe a **jerry can** ✓ of avgas or
  heating fuel, a spare tire tube (rubber!).
- **The ELT itself**: a bright orange box bracketed in the tail cone with its own **antenna**
  and battery — did the g-switch fire? Is it transmitting on **121.5** right now? This plus
  the manual clue plus the roof antenna is the whole rescue arc's furniture.

## 5. In the airframe (destructive salvage layer)

Wall/ceiling **insulation batting**, headliner fabric, wiring harnesses (copper ✓), control
cables (braided steel wire — strong cordage!), aluminum skin panels, stringers/ribs, plexiglass,
door seals (rubber), the doors themselves (windbreaks/sleds), seat rails, springs in cushions.

## 6. Engine bay & exterior (mostly existing zones)

**Battery** (12/24V — can it power the radio?! a spark source!), alternator, magnetos, engine
cowling sheets, exhaust stack (fire-hardened steel tube), the prop, **avgas in the wing tanks**
(fuel drains under the wings — a cup at a time, or siphon), pitot tube, static wicks, nav-light
lenses, tires + tubes (burning rubber = black signal smoke), skis/wheel-skis, the **comm antenna
base on the roof** ✓ (§38), tail surfaces, control-surface fabric (on a Beaver).

## 7. The Alaska survival-equipment law (the realism anchor)

Alaska Statute **AS 02.35.110 (Emergency Rations and Equipment)**: no flight in-state without
minimum emergency equipment — summer: a week's rations per occupant, an axe or hatchet, a first
aid kit, two small signaling devices in sealed containers (the traditional list also carries the
fishing kit, knife, matches, and mosquito headnets); **winter (Oct 15–Apr 1) adds snowshoes, a
sleeping bag, and a wool blanket per occupant**. Our pilot was legal. The kit is in the tail.
This single fact justifies the game's entire survival economy without inventing anything.

## 8. Mapping notes (game-side)

- **Containers**: survival duffel, mail sacks, groceries box, parts crate, cooler, tool roll,
  flight bag, door pockets, seatback pockets ✓(×4), glovebox-equivalent map pockets.
- **Wearables**: engine/wing covers (huge), sleeping bag (cloak-able?), headnets, more gloves.
- **New tools**: hatchet (wood loop!), knife, snowshoes (a movement modifier someday), duct
  tape, safety wire, flashlight.
- **Fire/signal**: matches, fusees/smoke bombs, avgas, oil, tires, flare shells.
- **Radio arc**: ELT (tail) + remote switch (panel) + 121.5 manual clue ✓ + roof antenna ✓ +
  battery + safety wire/control cable as antenna material.
- **Materials likely needed**: `insulation_batting` (anticipated in the table's comment),
  `canvas` (covers/tarp), maybe `down` (sleeping bag) — or map to wool/fabric.
- **Fiction decision needed**: overhead bins → netted cargo bay + hat shelf + jammed cargo door?

## 8b. Access design — the crash is the difficulty engine (Andrew's check, 2026-07-04)

An intact survival kit = the game solved in one `search`. The principle: **realism supplies the
inventory; the crash supplies the difficulty.** The law says the kit was ABOARD — the crash
decides where it is now and what shape it's in. Every gate is honest physics:

- **Distance**: the tail section (kit + ELT) tore off 200 m back up the crash path — an
  expedition through snow and (P5) a warmth budget; hauling it back costs trips and weight.
  Implies new zones: a debris trail + the separated tail section (cheap now — zone content).
- **Wreckage**: crushed tail cone; the bay pinned under shifted freight (unload first); the
  cargo net frozen into the frame; buckled aluminum wants two people and a lever.
- **Scatter**: the kit split on impact — contents strung along the debris field; the hatchet is
  in a drift somewhere off the trail; ration tins rolled; dig/search the crash path.
- **Damage → loops, not wins**: soaked matches (dry them by a fire you must start another way —
  a bootstrap puzzle); snapped axe haft (webbing + tape repair); the sleeping bag took avgas
  (warm, but flammable — choices); the ELT survived but its antenna sheared in the separation —
  transmitting into nothing; FIXING it is the rescue arc.
- **The power∝cost rule (authoring curve)**: the more game-solving an item, the farther /
  deeper / more broken the crash left it. A paperback is at your feet; the hatchet is a hundred
  meters out under snow with a cracked haft.

Pacing arc this produces: teasers at your feet → bins/bags for workers → expeditions for the
treasures → the radio/ELT arc as the long game.

## 8c. CURATED v1 — what shipped (2026-07-04; Andrew: "just go for it")

Two new zones: **the debris trail** (NE of the breach — gouged snow, shed metal) and **the severed
tail section** beyond it (a 4-hop expedition from the cabin). The kit scattered per §8b:
- *Debris trail*: the **torn survival duffel** (ration tins ×2, fishing kit, headnet, and the
  **soaked matchbox** — the drying bootstrap, narrated, mechanics later); a **wind-packed drift**
  hiding the **snapped hatchet** (edge 0.5 — usable choked-up, repairable later) and a flare
  shell; the **mail sack** (a child's letter you shouldn't read, postal twine); an aluminum sheet.
- *Tail section*: the **crushed tail cone** (pry) holding the **avgas-soaked sleeping bag**,
  **snowshoes**, the **cargo net**, and **the ELT** — g-switch fired, ARM lamp pulsing on 121.5,
  antenna sheared: "screaming into its own throat" (the rescue arc's second device, confirmed);
  the nailed **freight crate** (pry) with village groceries (coffee, flour).
- *Cabin/cockpit adds*: the pilot's **flight bag** (flashlight, fuel tester), the **sectional
  chart** (read: a hand-drawn square three miles east — "V. HOLT — CABIN, WOOD STOVE": the next
  scene's hook), the still-warm **thermos**, a fire extinguisher, the **tool roll** (duct tape,
  safety wire, screwdriver) in the fwd bin, the **quilted engine cover** (the warmth prize)
  behind the aft-bin pry, seat **12C** in the rear row, oil quarts outside.
- New materials: `rations`, `insulation_batting`. Decisions taken: bins KEPT as fiction (re-skin
  later if wanted); satcom OMITTED (backlogged); both seats fully parted; ELT = yes.

## 9. Open questions for Andrew

1. Bins vs. netted cargo bay (realism vs. keeping what's built)?
2. How much of §4 makes v1 — the survival kit alone is ~12 objects; the freight another ~10.
3. The satcom question: include a broken inReach/PLB (cruel + useful parts) or omit entirely?
4. Four seats: model all four with parts (lots of salvage) or two detailed + two background?
5. Does the ELT become the rescue arc's second device (tail) alongside the panel radio (§38)?

## Sources
- [AS 02.35.110 — Emergency Rations and Equipment (touchngo.com)](https://touchngo.com/lglcntr/akstats/Statutes/Title02/Chapter35/Section110.htm)
- [Alaska Statutes §02.35.110 (FindLaw)](https://codes.findlaw.com/ak/title-2-aeronautics/ak-st-sect-02-35-110/)
- [AOPA — Best Practices for Alaska Aviation Survival and Rescue Gear (PDF)](https://www.aopa.org/-/media/Files/AOPA/Home/Go-Flying/International-pdf-files/Best-Practices-for-Alaska-Aviation-Survival-and-Rescue-Gear.pdf)
- [Equipped To Survive — Alaskan & Canadian Survival Kit Regulations](http://www.equipped.org/ak_cnda.htm)
