# Rear cabin — real-world ontology census & gap analysis

> Official room doc. Follows `cockpit.md` (the **shared cabin baseline**, §2a/§2d) and `mid_cabin.md`
> (the seat parts-machine — 12C here is identical to 11B). This doc covers what is distinctive: the
> hull is *open* here, so the outside comes in — snow, wind, cold — and the room's rewards are warmth.
> Gaps are recommendations; no code is changed here.

---

## 1. The scene, if it were real

The back of the cabin, where the hull has split open to the sky. Snow has drifted in and banked white
against the rear rows; it sifts down with every gust. A second seat (12C) lies thrown against the hull.
An aft overhead bin is buckled shut. A whisky bottle has come through unbroken; a wool blanket half
spills from a bin. This is the cold room — and, behind the jammed bin, the warm one.

## 2. Entity census — what's distinctive here

### 2a. The snowdrift (indoor weather — the standout entity)
`snowdrift` (fixed, material `snow`) → **dig** it for the buried **leather gloves**. It is also the
room's **water source** (melt → water) and a cold sink. Snow *indoors* is the whole point of the split
hull: the outside has entered the shelter.

### 2b. The aft bin — the warmth prize (pry-gated, the reward loop)
`bin_aft` (jammed, fixed) → **backpack** (canteen of water — half-full; spare shirt) + **engine cover**
(cotton + `insulation_batting` — the best insulation in the crash, "holds heat against metal all
night"). The pry-loop's payoff.

### 2c. The whisky bottle — the game's modelled glass blade
`bottle` (glass) → **break** → sharp `glass shard`s. This is the ONE place broken glass yields a blade
today (the cockpit windscreen and cabin windows do not — see the recurring gap). Worth noting the
bottle *carries* that whole affordance for the early game.

### 2d. Seat 12C + the blanket
Seat 12C = the 11B parts-machine (cover/cushion/belt/bolt → fabric/foam/webbing/steel; see
`mid_cabin.md §2a`). `blanket` (wool) — a warmth/wrap/bandage staple.

### 2e. The hull breach itself (the elusive standout)
The tear is an *entity in effect*: it is the way outside (a walk-edge to `outside_tail`), the wind's
door, and the reason this room is colder than the others. A real survivor's first instinct is to
**block it**.

## 3. Actions & relations → candidate MUD command
| entity | real-world action | candidate command | built? |
|---|---|---|---|
| snowdrift | dig for buried things | `dig snowdrift`, `search drift` | ✅ |
| snowdrift | melt snow → water | `melt snow`, `melt drift` | ✅ (melt op) |
| snow | pack it / build with it (wall, block) | `pack snow`, `build wall from snow` | ❌ |
| snow | eat it (risky hydration) | `eat snow` | ~ eat op exists; snow-as-food ❌ |
| bin_aft | pry it open | `pry bin`, `open aft bin` | ✅ |
| backpack | search / open | `search backpack` | ✅ |
| canteen | drink (half-full) | `drink from canteen` | ✅ |
| engine cover | wrap up in it for warmth | `wrap self in cover`, `wear cover` | ✅ (insulation) |
| whisky bottle | break for a blade | `break bottle` → shard | ✅ |
| glass shard | cut with it | `cut X with shard` | ✅ |
| blanket | wear / wrap / bandage | `wrap X in blanket`, `wear blanket` | ✅ |
| seat 12C | strip for materials | see `mid_cabin.md §3` | ✅ |
| seat 12C | sit / rest | `sit on seat`, `rest` | ❌ (recurring) |
| hull breach | go outside through it | `go to the breach` / `go outside` | ✅ (walk-edge) |
| hull breach | **block / cover the tear** | `cover breach with cover`, `block hull` | ❌ (the block-the-draft gap) |
| falling snow / gust | shelter from it | (see block gap) | ❌ |

## 4. What's built today
The cold-and-warmth room: an indoor **snow** source (dig + melt), the pry-gated **warmth prize** (engine
cover) mirroring mid_cabin's tool prize, a second parts-seat, and the early game's **glass blade**
(bottle). Systemically it leans hardest on **warmth/cold** (it is authored to be the coldest interior)
and on **melt** (its water). Space model: rear_rows / overhead / floor, with the snowdrift + seat 12C as
the anchors.

## 5. Gap analysis → recommendations (none applied; logged)

### Room-specific
1. **Block / cover the hull breach** — the single most natural survival act here (cut the wind, warm
   the room) has no affordance. This is the concrete, high-value form of the cross-cutting
   *block-the-draft* gap: a `cover <opening> with <material>` operation + a per-zone `draft`/exposure
   the cover reduces, feeding the warmth system. **Recommend a design spike** — it would light up the
   whole warmth loop and recurs at every exterior opening.
2. **Snow as a buildable / edible material** — `pack snow` (a wall, a block, cover) and `eat snow`
   (risky hydration vs. core-cooling). Extends the `snow` material + a build op. Medium.

### Recurring votes (cross-room)
- **`sit`/`rest`/`sleep`** — seat 12C. (vote 2, with mid_cabin)
- **broken glass as a blade** — here it IS built (bottle); note the *contrast* with the cockpit
  windscreen / cabin windows, which should match. (glass-blade gap vote stands at 2 for the unglazed
  openings)
- **sense verbs `smell`/`listen`** — the gust, the wind through the tear (sound + direction). (vote 3)
- **examinable scenery nouns** — the breach, the rear rows, the drift's bank. (vote 3)

---

*Next pair: `outside_nose.md` + `fuselage_top.md` (the sparse exterior approach zones).*
