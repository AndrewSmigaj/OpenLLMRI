# The severed tail — real-world ontology census

> Official room doc. The expedition cache: the tail tore off and rode out here, and whatever was
> stowed in the baggage bay rode with it — behind jammed metal that takes real force to open. This
> census maps what's here and the many things a person could do with it. Gaps flat, no ranking.

---

## 1. The scene, if it were real
The whole empennage lies canted deep in the snow at the end of the gouge, control cables trailing from
the stump like torn tendons. The baggage it carried is sealed inside a crushed tail cone and a nailed
freight crate — both buckled shut, both wanting a lever and real anger. This is the room you come *back*
to with a pry bar; it holds the rescue beacon, the mobility, and the warmth.

## 2. Entity census
### Built
| entity | material / state | some of what it affords (not exhaustive) |
|---|---|---|
| crushed tail cone | aluminum, jammed container (fixed) | pry it open → the expedition kit inside |
| — **ELT (locator beacon)** | plastic+copper_wire, armed, **antenna sheared** | the rescue headline — screaming on 121.5 but deaf; needs a real antenna + wire enough to reach one (the mount is up at fuselage_top) |
| — snowshoes | wood+nylon_webbing | wear them → the drifts stop being walls (the payoff is the movement system) |
| — **fuel-soaked sleeping bag** | wool, `fuel_soaked` | warm as a stove — and reeks of avgas: warmth vs. keep-it-away-from-fire, a real choice |
| — cargo net | nylon_webbing | cut free → metres of cordage |
| freight crate | wood, jammed container (fixed) | pry it open → the food |
| — coffee tin | steel, sealed | open → coffee (morale / a warm drink); the tin itself is a container |
| — flour sack | rations | open → flour (bannock over a fire, if a fire ever happens) |

### Scenery (unbuilt nouns)
the tail structure / empennage, the trailing control cables (sharp wire; cordage), the stump of torn
metal, the deep snow it's canted in, the tail's own gouge back toward the wreck.

### Elusive
cold, wind, worst-of-the-outdoors exposure; the ELT's slow red pulse and its shout on 121.5 (a *sound*/
signal you can't quite hear); the smell of avgas off the sleeping bag; sightlines back down the scar to
the debris trail and the wreck.

## 3. Things a person could do here → candidate command
| want to… | command | built? |
|---|---|---|
| pry the tail cone / crate open (jammed) | `pry cone`, `pry crate`, `open X` | ✅ (pry op) |
| take the ELT and rig it a real antenna | `take elt`, `tie wire to elt`, then mount up at fuselage_top | ~ (ELT + wire built; the antenna MOUNT is unbuilt — see `fuselage_top.md`) |
| wear the snowshoes to move in deep snow | `wear snowshoes` | ~ (wear ✅; the speed/effort payoff = the unbuilt movement system) |
| take the sleeping bag for warmth (fuel-soaked!) | `take bag`, `wrap self in bag` | ✅ (take/wrap; the `fuel_soaked` danger is the tension) |
| cut the cargo net into cordage | `cut net`, `cut cordage from net` | ✅ (cut) |
| open + brew coffee / bake bannock from flour | `open tin`, `brew coffee`, `bake flour` | ~ (open ✅; cooking/brewing ❌) |
| cut the trailing control cables for wire/cordage | `cut cable`, `take cable` | ❌ (scenery, not a noun) |
| head back down the scar to the wreck | `go to the debris trail` | ✅ (walk) |
| smell the avgas / listen for the beacon | `smell`, `listen` | ❌ (no sense verbs) |
| stash a load / drop the pry bar here | `drop X`, `put X in the snow` | ✅ (space model) |

## 4. What's built / what isn't
The expedition cache, and a genuine hook room: two pry-gated jammed containers holding the **rescue
beacon** (the ELT — a headline puzzle whose *other half*, the antenna mount, sits unbuilt at
fuselage_top), the **mobility** (snowshoes), the **warmth-with-a-catch** (the fuel-soaked bag), cordage
(cargo net), and food (coffee, flour). Not built, listed flat: the movement system that makes snowshoes
*mean* something, the antenna-rig completion up top, cooking (bannock / brew), the control cables as an
interactable, `smell`/`listen`, examinable scenery nouns. The ELT + antenna is the one real cross-room
dependency worth flagging (this room ↔ fuselage_top).

---
*Companion outer-cluster docs: `debris_trail.md`, `treeline.md`.*
