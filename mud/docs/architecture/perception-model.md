# Perception Model

Design §10–15 (space, direction, perception, sound) realized on Evennia. The
pure side lives in [`game/world/sim/space/`](../../game/world/sim/space/); the
shell side is the Room/Character `return_appearance` and a message propagator.

> Core principle (§10): **do not collapse perception into "room."** Location,
> visibility, audibility, reachability, direction and detail are *separate*
> concerns, each distance/weather/occlusion-aware.

## Scene-Room + zone attribute

Whiteout rooms are too chunky and pure coordinates too fiddly, so the model is
*overlapping perceptual spaces* ([ADR-0004](adr/0004-zone-as-attribute-perception.md)):

- A **Scene** (e.g. `wreck_cabin`, `crash_basin`) is **one Evennia Room**.
- A character's **zone** (e.g. `camp_edge`, `rear_seat_row`) is a **position
  Attribute on the Character**, *not* a separate room.
- A [`Zone`](../../game/world/sim/space/zones.py) has planar coordinates
  (`x`, `y`), `elevation` and `terrain_tags`, so the engine can compute distance
  bands and relative-direction phrases (§12).

Everyone in a Scene therefore shares a single Evennia Room. That is what makes
intra-scene movement and perception custom rather than free from Evennia's room
graph — and it creates the reachability tax (below).

## Two kinds of movement

| Movement | Mechanism | Owner |
|---|---|---|
| **Scene transition** (cabin → exterior → forest) | Evennia rooms, exits, `move_to` | Evennia (shell) |
| **Zone move** (within a Scene) | set the zone Attribute; recompute perception | custom (`space/*`) |

Scene transitions reuse Evennia's battle-tested machinery; intra-scene moves and
all perception are custom because they no longer correspond to room containment.

## Perception bands

[`PerceptionBand`](../../game/world/sim/contracts.py) (design §14) grades *how
clearly* one thing is perceived from an observer's zone:

| Band | Detail |
|---|---|
| `SAME_ZONE` | detailed |
| `ADJACENT_ZONE` | clear |
| `NEAR_VISIBLE` | summarized |
| `DISTANT_VISIBLE` | vague |
| `BARELY_VISIBLE` | shape or motion |
| `AUDIBLE_ONLY` | sound only |
| `OUT_OF_SIGHT` | nothing (no message) |

[`perception.py`](../../game/world/sim/space/perception.py) computes the band
from same/adjacent-zone graph relation, planar distance and **weather
visibility** (§8): nothing past `weather_visibility_m` is visible at all, so a
whiteout collapses bands toward `OUT_OF_SIGHT`. Sight and hearing are computed
separately; reachability is separate again.

[`PerceptionResult`](../../game/world/sim/contracts.py) bundles the outcome:
`band`, `visible`, `audible`, `reachable`, `direction_phrase`, `distance_m`.
Reachability is deliberately a distinct boolean: you can *see* the orange case by
the bulkhead yet not be able to *manipulate* it (§17).

## Direction phrasing

[`direction.py`](../../game/world/sim/space/direction.py) turns a bearing
(`zones.bearing_deg`) plus elevation delta into natural language (§11–12): the
8 compass points, plus `upslope`/`downslope`, yielding phrases like *"to the
southeast and upslope"*. Compass language is used for clarity; landmark-relative
phrasing (*"back toward camp"*) is layered on by the scenario/shell when the
character is disoriented or in whiteout — the core only produces the compass
form.

`look`, `look south`, `scan cabin`, `examine` (§17) all render from the *actual*
computed perception: if camp falls out of sight it no longer appears in the main
description (§13).

## Sound & speech propagation

[`sound.py`](../../game/world/sim/space/sound.py) holds the baseline voice-range
tables and modifier arithmetic (§15):

- Voice modes reach different bands in clear conditions —
  `whisper` → same zone, `say` → adjacent, `call` → near-visible,
  `shout` → distant-visible.
- Weather shifts reach in band-steps: `steady_snow` −1, `heavy_snow` −2,
  `whiteout` −3. Terrain (fuselage, forest, ravine) and wind modify further.
- Loudness governs non-speech events too: quiet pocketing of food routes only to
  someone nearby; a metallic bang, fire flare-up or fuselage shift routes far.

A degraded message is produced per band — *"To the south, Andrew says, …"* one
zone away; *"A shout comes from somewhere south of you. You cannot make out the
words."* in whiteout.

## The message propagator (replaces `msg_contents`)

A plain Evennia `room.msg_contents("Mara saws at the seatbelt")` would tell
*everyone in the room* the same thing — wrong here, because the room is a whole
Scene. Instead the shell runs a **message propagator**: for each observer it
computes their `PerceptionResult` toward the source and renders the band's text
form (or nothing for `OUT_OF_SIGHT`). The pure side supplies the inputs —
`Event` (`actor`, `zone`, `loudness`, `text_same_zone`) plus the per-observer
band — and the shell sends the per-observer string. See
[`events.py`](../../game/world/sim/events.py) and
[`narrator.py`](../../game/world/sim/narrator.py).

## The reachability tax (known cost)

Because a Scene is one Evennia Room, **Evennia's room containment no longer
equals "reachable."** Default commands (`get`/`drop`/`look`/`give`, and every
manipulation verb) must therefore be gated by a reachability check on *every*
interaction: a **`ReachabilityMixin`** consults the perception layer before the
verb runs. This is the deliberate tax accepted in
[ADR-0004](adr/0004-zone-as-attribute-perception.md) — the price of zone-as-
attribute over one-room-per-zone, which would have multiplied the room count and
broken single-scene perception.

## Related

- [overview.md](overview.md) — where this sits in the whole.
- [tick-and-scheduler.md](tick-and-scheduler.md) — perception-routed *tick*
  messages while work progresses.
- Roadmap P3 implements perception/zones — the full band-shifting and propagator
  ([roadmap](../scenarios/whiteout/roadmap.md)).
