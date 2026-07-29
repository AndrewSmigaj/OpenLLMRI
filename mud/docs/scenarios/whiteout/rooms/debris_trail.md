# The debris trail — real-world ontology census

> Official room doc. The scatter: the long gouge the plane tore on its way in, shedding things that
> the snow has been half-burying since. This census maps what's here and the many things a person could
> do with it — a wide possibility space. Gaps are listed flat, no priority implied.

---

## 1. The scene, if it were real
A ragged furrow of gouged snow and shed metal running back the way the plane came. A survival duffel
has burst along its seam and spilled its kit; a wind-packed drift has swallowed a hatchet and a flare;
a mail sack lies spilled and freezing. A twisted sheet of fuselage skin juts up out of the crust.
Things fell here at speed and scattered — you find them by *looking through* the mess, not at a glance.

## 2. Entity census
### Built
| entity | material / state | some of what it affords (not exhaustive) |
|---|---|---|
| torn survival duffel | synthetic_fabric, container (split) | search → the kit; fabric to cut into strips / a wrap |
| — ration tins ×2 | rations, sealed | open → food; sealed tin = a small container / striker |
| — fishing kit | plastic | hooks + line + weights → fishing, snares, fine cordage |
| — mosquito headnet | cotton_cloth | strain meltwater, a bag, gauze |
| — **waterproof matchbox** | plastic, **wet** | the fire bootstrap — dry the strike-anywheres out by a fire → ignition |
| wind-packed drift | snow, fixed (searchable) | dig it → what punched in; melt → water; a windbreak bank |
| — **snapped hatchet** | steel+wood, **broken** (edge 0.5, leverage 0.3) | choked-up it still bites; lash+tape the cracked haft → a whole axe |
| — flare shell | cardboard, sealed | a signal (fire it), a fire-starter, dry powder |
| mail sack | cotton_cloth, container | search → letters + twine; heavy cloth |
| — bundle of letters | paper | read (the human gut-punch, §38); burns like any paper |
| — ball of twine | nylon_webbing | knots, snares, lashings (incl. the hatchet repair) |
| twisted aluminum sheet | aluminum | a windbreak, a fire-back, a sled for a heavy load |

### Scenery (unbuilt nouns)
the gouged scar itself (a *direction* — it runs back toward where the plane came and on to the tail),
shed metal fragments too small to name, the snow crust, blown-in powder healing the holes.

### Elusive
cold, wind, the scar-as-a-trail (traversal — it goes somewhere), sightlines back to the wreck and out
to the severed tail, the buried-ness of things (you *search* to find them), the smell of cold mail and
paper, the quiet of open snow.

## 3. Things a person could do here → candidate command
| want to… | command | built? |
|---|---|---|
| search the duffel / drift / sack | `search duffel`, `dig drift`, `search sack` | ✅ (search/dig + DR-24 containment) |
| **dry the wet matches** by a fire → working matches | `dry matchbox`, `warm matches by fire` | ❌ (no dry-by-heat op — a real gap; it's the authored bootstrap) |
| **repair the snapped hatchet** (lash the cracked haft) | `tie twine around hatchet`, `tape haft` | ~ (tie/wrap exist; whether "repair" resolves needs a look) |
| chop with the hatchet as-is (choked up) | `cut X with hatchet` | ~ (broken/edge state; verify it still cuts) |
| fire the flare to signal | `light flare`, `fire flare` | ~ (light exists; a *signal* effect ❌) |
| read the letters (the emotional beat) | `read letters` | ✅ (§38 read text) |
| burn letters / paper for tinder | `burn letters`, `light letters` | ✅ (paper flammable) |
| open + eat the rations | `open tin`, `eat rations` | ✅ (open + eat) |
| fish with the kit (at the creek, elsewhere) | `fish`, `cast line` | ❌ (no fishing op; the creek is a Phase-1 zone) |
| use the aluminum sheet — windbreak / sled / fire-back | `drag sheet`, `build windbreak from sheet` | ~ (object exists; drag/build ❌) |
| take twine / fabric for cordage & wraps | `take twine`, `cut fabric from duffel` | ✅ |
| follow the scar onward / back | `go to the severed tail`, `go to the breach` | ✅ (walk) |
| smell the cold mail / listen | `smell`, `listen` | ❌ (no sense verbs) |
| stash a haul here to come back for | `drop X`, `put X on the scar` | ✅ (space model) |

## 4. What's built / what isn't
This is a content-rich scatter, not just terrain: three search-gated container chains (duffel / drift /
sack) carrying the survival kit, the **fire bootstrap** (the deliberately-wet matchbox), the **hatchet
repair** (a broken tool made whole by lashing), and the **letters** (the §38 emotional gut-punch). Not
built, listed flat (no ranking): the dry-the-matches mechanic (load-bearing for the bootstrap — worth a
look at whether *any* path dries them), the hatchet-repair resolving cleanly, flare-as-signal, a fishing
op, drag/build for the aluminum sheet, `smell`/`listen`, examinable scenery nouns, and the movement
effort/time this trail implies. Several recur across rooms — data for later, not a verdict on the game.

---
*Companion outer-cluster docs: `tail_section.md`, `treeline.md`.*
