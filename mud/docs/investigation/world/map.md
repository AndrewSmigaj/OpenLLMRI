# The Whiteout world map — the valley (macro design)

> **Status: SCRATCHPAD (investigation) — 2026-07-15 overnight design run.** The full outdoor
> scenario: every Scene and zone beyond the crash site, designed as if the room system were
> fully built (Scene-to-Scene travel, durations, weather bands). Companion docs:
> [`rooms.md`](rooms.md) (every zone in detail) · [`report.md`](report.md) (how the rooms are
> used in play + the quality assessment passes) · [`objects.md`](objects.md) (the per-room
> object inventory for the ontology build-out). Promotes into `docs/scenarios/whiteout/` and
> `zones.py` content when Andrew approves.

## 1. The design thesis

Three rules govern everything below.

**Each region anchors ONE rescue route.** GDD §37–39: rescue is additive confidence with ≥4
winning combinations, and the routes must draw on *distinct* scarce resources. The map IS that
design: the lake anchors the visual route (open sightlines), the ridge anchors radio/beacon
(elevation), the creek–trapline–cabin line anchors travel/shelter (distance and navigation),
and the crash site anchors stay-and-signal (the known point searchers will eventually grid).
The forest ring in between is the survival economy — fuel, food, insulation, water — that
every route spends from.

**The country is the difficulty engine.** Indoors, the crash supplied the difficulty
(plane-interior §8b). Outdoors, winter does: snow buries, ice gates, distance taxes, cold
punishes idleness, and the storm closes the world one band at a time. Nothing needed adding —
only honest pricing. Every resource out here costs at least two of the six currencies:

| Currency | What spends it |
|---|---|
| **Daylight** | travel and work both burn the ~5 h light budget (GDD §6); the storm shortens it further |
| **Warmth** | every zone has an exposure band; open ice and the ridge drain you while you work |
| **Sweat** | hard effort (digging, floundering, chopping) dampens clothing — a *deferred* cold debt |
| **Tools** | blade, chopper, saw, container, cordage — each unlocks a different shelf of the world |
| **Knowledge** | reading sign: tracks, ice color, blaze marks, squaw wood. `examine` is the tutor |
| **Risk** | thin ice, overflow, the cornice, the climb — always telegraphed, never random |

**The anti-easy rule.** Nothing usable lies loose on the surface anywhere in the valley except
what the crash itself scattered (that's canon, and it's already priced). Everything else is
under snow, inside ice, up a tree, behind a blaze you have to follow, or 2.4 km away. Fair,
not generous: every hazard telegraphs; every gate has ≥2 openings; `examine` always pays.

## 2. The valley (geography)

An unnamed side valley in interior Alaska, deep winter, ~−15 °C falling to −20 °C after dark.
The mail plane came in from the northeast over a low ridge shoulder, clipped the spruce crowns
(the strike path), shed its right wing into the trees, bellied down the slope, and slid
southwest across a frozen muskeg fringe — shedding the tail — to stop at the muskeg's east
edge. The pilot was stretching for the lake ice and almost made it. West, the muskeg opens
onto the lake; the lake drains from its south end into a creek that runs southeast through
spruce forest, past a beaver pond. From the creek's east bank an old blazed trapline climbs
to V. Holt's homestead on a bench — the cabin the chart promises.

```
                        THE RIDGE OVERLOOK  (knob · +120 m)
                              ▲  NE
                    lee cornice │ boulder field
                                │
                        THE STRIKE PATH
                    (wing in the trees · gear gouge)
                                │  sheared crowns
        THE NORTH WOOD          │
   (big spruce · deadfall ·     │            THE BIRCH STAND
    grouse · hare runs)         │         (bark · chaga · aspen)
              ╲                 │               ╱  E
               ╲     treeline ──┴── debris ── ╱
                ╲       │      trail · tail  ╱
    N ◄─────────────  THE CRASH SITE  ────────────► E
                        (the wreck)
                          │
         THE MUSKEG ──────┘ W
   (tussocks · tamarack · willows)
          │
      THE LAKE  ◄── far-shore burn (W, across the ice)
   (ice flat · pressure ridge ·
    inlet slush · outlet narrows)
          │ S (the outlet)
      THE CREEK
   (riffle · willow bar · overflow bend ·
    logjam · confluence pool)
          │ SE            ╲
    THE BEAVER POND        ╲ blazes climb E
   (dam · lodge · old set)  ╲
                       THE TRAPLINE
                    (spruce tunnel · marten set)
                              │ SE
                     HOLT'S HOMESTEAD
              (cabin · cache · woodshed · water hole)
```

Straight-line distances from the wreck: lake shore 500 m W · ridge knob 800 m NE (+120 m) ·
birch stand 350 m E · creek riffle 800 m SW · beaver pond 1.7 km SE · homestead 2.4 km
travel SE. The far-shore burn is 1.5 km W *across open lake ice*.

## 3. Travel is the price tag (design values for the P4 duration seam)

Unbroken snow is the tyrant: knee-deep trail-breaking moves at ~1.5 km/h and costs sweat.
Your own broken trail is twice as fast — until the storm refills it (GDD §8 degrades tracks).
The creek ice is a highway with a toll (overflow). Snowshoes (in Holt's cache) roughly double
open-country speed — the mobility upgrade is treasure precisely because the map is big.

| Leg (one way) | First time | Broken trail | On snowshoes |
|---|---|---|---|
| wreck → lake shore | 20 min | 12 min | 8 min |
| wreck → big spruce hollow | 15 min | 8 min | 6 min |
| wreck → birch stand | 25 min | 15 min | 10 min |
| wreck → ridge knob | 55 min | 40 min | 35 min (wind, not depth) |
| wreck → creek riffle | 30 min | 18 min | 12 min |
| wreck → beaver pond | 55 min | 35 min | 25 min |
| wreck → homestead | ~90 min | ~60 min | ~40 min |
| lake crossing to the burn | 25 min | — (wind erases) | 15 min |

Against a ~5 h light budget, the homestead is a **commitment**: first trip eats half the
usable day round-trip. That is the stay-or-go tension, made of minutes instead of dialogue.

## 4. How players learn the world exists (discovery chains)

No region is announced. Each is discovered by at least two independent chains, so parties
that miss one clue aren't locked out (GDD: no single required path):

- **The cabin**: the sectional chart ("V. HOLT — CABIN, WOOD STOVE") → a bearing; the ridge
  knob → the actual roof-shape seen SE; the drowned-set blaze at the beaver dam → the trail
  itself; the pilot's last lucid line (if they stabilized him early) → "follow the creek."
- **The trapline**: the blaze on the shore tree by the old drowned set; or walked into from
  the homestead end; or the marten-set wire glinting, noticed from the creek.
- **The ridge**: the inbound gouge + sheared crowns literally point back up at the notch —
  aligning the wreck's own scar is the orientation puzzle; the manual's ELT/121.5 pages plus
  "line of sight" reasoning invite elevation.
- **The lake**: visible as sky-glare W from the fuselage top; the muskeg simply opens onto it.
- **Open water**: the outlet riffle is *audible* before visible — running water in a frozen
  world is a sound event (the §15 machinery pays off outdoors).
- **The burn**: a smudge of standing black sticks across the ice, visible from the shore
  apron on a clear band; invisible once the storm thickens — an early-scout reward.

## 5. The storm re-prices the map (P7 design intent)

GDD §8's arc, applied spatially. Each phase doesn't just dim the world — it *re-prices* it:

1. **Light snow (morning)** — the whole map is open. Scouting is cheap; the far burn and the
   ridge are affordable. Everything you learn now (broken trails, blaze positions, where the
   riffle sounds from) is capital for later.
2. **Steady (midday)** — see-bands tighten one step; the search plane's pass happens in here
   somewhere (§8 timed beat — over the lake line, following the drainage, as real pilots do).
   You are either ready on the ice with smoke, or you eat the near-miss.
3. **Heavy (afternoon)** — open country turns hostile: the lake crossing and the knob become
   gambles; your morning trail is filling in. The sheltered routes (spruce tunnel, creek
   under the banks) keep working. Committing to the cabin is still possible — barely.
4. **Near-whiteout (dusk)** — navigation collapses to handrails: the creek, the blazes, a
   rope line you rigged, the wind's one constant direction. Zones effectively shrink to
   arm's length. Anyone caught in the open is spending warmth they don't have.
5. **Night (−20 °C)** — the world is three lit rooms: a fire you built, the fuselage huddle
   (the §-warmth floor), or Holt's stove. Everything else is a mistake.

## 6. Density gradient (GDD §6 honored)

The GDD gives the dense scene (cabin + camp + near-forest) the whole data budget. The map
keeps that: **Ring 0** (crash site + big-spruce forward camp) stays modeled to the hilt;
**Ring 1** (muskeg, strike path, birch stand, near creek) carries full interaction but leaner
object counts; **Ring 2** (lake, ridge, pond, trapline) is purposeful terrain — each zone
exists for one decision, one resource, one hazard, one story beat; **the homestead** is the
second dense node (it's the "cabin + camp" of the endgame). Nothing is filler; a zone that
serves no route, economy, hazard, or beat got cut in the polish passes (see report.md).

## 7. Implementation seams (what "as if it works" assumes)

All designed-to, none built tonight — each already has a seam named in the architecture:
Scene-to-Scene transitions (DR-13a treats the world as one zone graph partitioned into
Scenes; cross-Scene edges are ordinary walk/see edges with a Scene hop); travel durations
(the P4 `duration_minutes` seam); exposure/warmth drain per zone (P5 consumes the per-zone
exposure band authored in rooms.md); weather bands (the P7 `weather=` parameter steps the
§14 ladder); hazard triggers, forage/snare/fish operations (the tier-1 authored-rule seam,
already backlogged); own-track persistence and decay (GDD §8 requires track degradation
anyway). The rooms are written so that *none of them need redesign* when those seams light up
— zones degrade gracefully to "terrain + description + contents" until then.
