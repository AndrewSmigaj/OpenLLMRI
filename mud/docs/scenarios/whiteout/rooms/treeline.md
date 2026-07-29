# The treeline — real-world ontology census

> Official room doc. The edge of the forest, and the survival core's supply room: wood, tinder, and
> shelter material — plus the gateway to the wider woods (a Phase-1 zone). Per the traversal calibration
> (outdoor rooms are terrain, not puzzles), this one earns its keep as a *resource + gateway*, not a
> unique hook, and that's correct. Census maps the breadth; gaps flat, no ranking.

---

## 1. The scene, if it were real
The first spruces close overhead, boughs bent white with snow; the wreck is a broken shape back through
the falling snow. It's quieter here — the wind drops under the trees. Deadfall lies about under the
crust, dry grass clumps at the roots, and the forest keeps going, darker, north.

## 2. Entity census
### Built
| entity | material / state | some of what it affords (not exhaustive) |
|---|---|---|
| dry grass (tinder) | dry_grass | the ignition tinder — takes a spark like a held breath |
| spruce tree | wood, fixed; parts: **low branch** (reachable), **bough** (real cutting) | cut the low branch → firewood; cut a bough → shelter poles / bedding |
| deadfall branch ×2 | wood | dry firewood, gathered off the ground |

### Scenery (unbuilt nouns)
the wider treeline / forest continuing north (a *gateway* — the North Wood is a Phase-1 zone), the
snow-loaded boughs, tree-wells (the sheltered hollow under a big spruce — a real windbreak/shelter
spot), fallen needles + duff (fine tinder), bark.

### Elusive
cold — but *less wind* here (the trees break it; the first real relief from exposure); the falling snow;
the muffled forest quiet; the smell of spruce; sightlines back to the wreck (a broken shape through the
snow); the pull of the forest going on north.

## 3. Things a person could do here → candidate command
| want to… | command | built? |
|---|---|---|
| cut the low branch / a bough off the spruce | `cut low branch from spruce`, `cut bough` | ✅ (cut + parts → loose_branch / loose_bough) |
| gather the deadfall for dry firewood | `take deadfall`, `take branch` | ✅ (take; aggregate) |
| take the dry grass for tinder | `take grass`, `take tinder` | ✅ |
| light a fire (tinder + wood) — the survival core | `light tinder`, `burn wood` | ✅ (light / burn) |
| build a shelter / bed from the boughs | `build shelter from boughs`, `lay boughs` | ~ (boughs are a real output; a build-shelter op ❌) |
| shelter in a tree-well (natural windbreak) | `shelter under spruce`, `rest in tree well` | ❌ (tree-well not a noun; no shelter/rest op) |
| feel the wind drop under the trees | (warmth reading the `cover` terrain tag) | ~ (the zone is tagged `cover`; whether warmth reads it — verify) |
| go deeper into the woods | `go north`, `go to the forest edge` | ~ (edge only; the North Wood is Phase 1, unbuilt) |
| strip bark / rake needles for fine tinder | `strip bark`, `gather needles` | ❌ (scenery, not nouns) |
| smell the spruce / listen to the quiet | `smell`, `listen` | ❌ (no sense verbs) |
| stash firewood to haul back | `drop X`, `put X under the spruce` | ✅ (space model) |

## 4. What's built / what isn't
The supply room for the survival core: **firewood** (deadfall + the spruce's low branch and bough),
**tinder** (dry grass), and **shelter material** (boughs). It's also the first spot with *relief from
the wind* (under the trees) and the **gateway** to the wider forest. Built well for its job — the wood
and tinder that feed every fire come from here. Not built, listed flat: build-a-shelter / bough-bedding,
the tree-well as a shelter spot, whether warmth actually reads the `cover` terrain, deeper-forest
traversal (Phase 1's North Wood), `smell`/`listen`, scenery nouns (bark / needles / tree-wells), and the
movement effort/time of the outdoors. Fittingly for a traversal zone, most "gaps" here are *systems*
(shelter, movement, the wider forest), not missing objects — which is the right shape for it.

---
*Companion outer-cluster docs: `debris_trail.md`, `tail_section.md`. This completes the 9 crash-room censuses.*
