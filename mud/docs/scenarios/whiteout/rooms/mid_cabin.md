# Mid cabin — real-world ontology census & gap analysis

> Official room doc. Follows the exemplar `cockpit.md` (read its §2a/§2d for the **shared cabin
> baseline** — structure and the elusive entities, cold / air / light / darkness / sound / smell / time
> — which are the same interior and are not repeated here). This doc covers what is *distinctive* about
> the mid cabin: the crafting heart of the crash. Gaps are recommendations; no code is changed here.

---

## 1. The scene, if it were real

The middle of the cabin, seat rows buckled and shoved together, luggage burst down the aisle. One seat
(11B) is wrenched off true on its rails; an overhead bin hangs jammed above it; oxygen masks sway on
their tubes where the ceiling panel sprung. A duffel has split open on the floor. This is where a
survivor *harvests* — foam, fabric, webbing, tools — because the crash tore everything half-apart
already.

## 2. Entity census — what's distinctive here

### 2a. The seat (11B) — a parts machine (the crafting core)
| part | material | attachment → yields | real-world action |
|---|---|---|---|
| cover | synthetic_fabric | stitched → `loose_fabric` | cut/tear it free → strips, a wrap |
| cushion | foam | clipped → `loose_foam` | pry/cut it out → insulation, a sleeping pad, filthy fuel |
| seatbelt | nylon_webbing | bolted → `loose_webbing` | unbolt/cut → cordage that bears weight |
| bolt | steel | bolted | back it out with a screwdriver → hardware |
| the frame | steel | fixed | the anchor everything else hangs on |

The seat is the room's thesis: **objects are cheap, materials are the content** — one seat is four
materials and four operations.

### 2b. The overhead bin (fwd) — the tool cache (pry-gated)
`bin_fwd` (jammed, fixed) → **first-aid kit** (bandage, medical tape) + **tool roll** (duct tape,
safety wire = copper, **screwdriver** leverage 0.35). Pry the bin, open the kits, earn the tools.

### 2c. The burst duffel — the key tools (search-gated)
`duffel` (split) → **multitool** (edge 0.8, leverage 0.5 — the master tool), **paracord**, **wool
socks**. This is where the run's cutting/prying capability comes from.

### 2d. Oxygen masks — a fixed parts source
`masks` (fixed) → **cup** (plastic, clipped → `loose_cup`) + **tubing** (rubber, tied → `rubber_tubing`).
The rubber tubing is quietly important (a hose / a tie / antenna dressing).

### 2e. Shared cabin baseline → see `cockpit.md`
Structure (windows, aisle, ceiling, bulkheads), and the elusive set (cold, air, light, darkness, sound,
smell, time) are the same interior. **Delta:** the masks *sway* (a small motion/sound in the draft);
the aisle is the room's `default` space where spilled luggage lands.

## 3. Actions & relations → candidate MUD command
| entity | real-world action | candidate command | built? |
|---|---|---|---|
| seat cover | cut/tear it off | `cut cover off seat with multitool` | ✅ |
| seat cushion | pry/cut it out | `pry cushion from seat`, `cut cushion` | ✅ |
| seatbelt | cut / unbolt it | `cut belt from seat` | ✅ |
| seat bolt | back it out | `pry bolt`, (unscrew) `X bolt with screwdriver` | ~ pry ok; a true `unscrew` verb ❌ |
| seat (frame) | **sit / rest on it** | `sit on seat`, `rest` | ❌ (no rest/sit op) |
| bin_fwd | pry open | `pry bin`, `open bin` | ✅ |
| first-aid kit | open; bandage a wound | `open kit`; `bandage arm with bandage` | ~ open ✅; treat-wound op ❌ |
| tool roll | unroll / search | `open roll`, `search roll` | ✅ |
| screwdriver | pry / drive a screw | `pry X with screwdriver` | ~ pry ✅; drive ❌ |
| duffel | search it | `search duffel` → multitool | ✅ |
| multitool | cut / pry with it | `cut X with multitool` | ✅ |
| paracord | tie / lash | `tie X to Y with paracord` | ✅ |
| socks / cover / cushion | wear / wrap for warmth | `wear socks`, `wrap X in cover` | ✅ |
| oxygen masks | pull the tubing / cup free | `cut tubing from masks`, `pry cup` | ✅ (parts) |
| oxygen masks | breathe from them (empty) | `use masks` | ❌ (no O2; correctly inert) |
| side window | break for glass | `break window` → shard | ❌ (see cockpit gap #4) |

## 4. What's built today
The richest crafting room: 1 parts-machine seat (4 materials), 2 pry-gated container chains (bin →
kit/roll; the aft equivalents are next door), 1 search-gated duffel with the master multitool, 1 fixed
masks parts-source. All reachable through the taught grammar + the space model (mid_cabin: seat_rows /
overhead / aisle). The material×operation engine already delivers the harvest loop (cut, pry, tear,
tie, wrap, wear).

## 5. Gap analysis → recommendations (none applied; logged)

### Room-specific
1. **`sit` / `rest` / `sleep`** — the seat is a *place to rest* and there is no verb for it. Resting is
   a survival beat (recover, wait out weather, pass time on the clock). → new op; ties to the warmth +
   clock systems. **First appearance of a recurring need — expect it in every sheltered room.**
2. **`unscrew` / drive-a-screw** — the screwdriver's characteristic action; `pry` approximates it.
   Low priority (pry covers the gameplay).
3. **treat-a-wound** (`bandage X`, `splint X`) — the first-aid kit's contents have no use-verb yet.
   Ties to the injury system. Medium — log for when injuries are wired.

### Recurring votes (cross-room — see cockpit.md §5)
- **sense verbs `smell`/`listen`** — the swaying masks (sound), the cabin smell. (vote 2)
- **broken glass as a blade** — the side windows. (vote 2)
- **examinable scenery nouns** — windows, aisle, ceiling, seat rows. (vote 2)

---

*Companion: `rear_cabin.md` (the snowdrift / warmth-prize room).*
