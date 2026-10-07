# Perception Model

> **Status: SPEC OF RECORD — v1 SHIPPED (P3, 2026-07-03; DR-13/DR-13a).** The `space/*` modules
> are implemented and the `PerceptionBand`/`PerceptionResult` contracts are in `contracts.py`
> (additive). This doc was reconciled against the shipped code; earlier drift (an unfrozen Event
> shape, the seed's four-verb look-tree, live weather math) is corrected below.

Design §10–15 (space, direction, perception, sound) realized on Evennia. The pure side lives in
[`game/world/sim/space/`](../../game/world/sim/space/); the shell side is the Room/Object
appearance overrides, the resolver's reach gate, and the message propagator.

> Core principle (§10): **do not collapse perception into "room."** Location, visibility,
> audibility, reachability, direction and detail are *separate* concerns.

## Scene-Room + zone attribute

Whiteout rooms are too chunky and pure coordinates too fiddly, so the model is *overlapping
perceptual spaces* ([ADR-0004](adr/0004-zone-as-attribute-perception.md)):

- A **Scene** (e.g. the crash site) is **one Evennia Room**.
- An entity's **zone** is `state["zone"]` (marshalled free through the existing Attribute schema;
  characters and objects alike). Carried objects track their carrier dynamically; a room's
  `default_zone` covers anything unassigned; minted objects inherit the acting player's zone.
- A [`Zone`](../../game/world/sim/space/zones.py) has a display name, planar coordinates
  (`x`, `y`), `elevation`, `terrain_tags`, `aliases`, authored survey prose, and **edges** to
  other zones with three flags: `walk` (movement), `see` (sightline — a fuselage wall is simply
  an ABSENT see-edge, which is the v1 occlusion model), `muffle` (sound passes, damped). The zone
  map is loaded-once scenario content (`zones.load_zones`), like the narration/appearance
  registries.

**The one-zone compatibility rule (load-bearing):** an observer or target with NO zone data is
`SAME_ZONE` — a zone-less world is a one-zone world. Unzoned rooms (all pure-test fixtures, the
smoketest scenario) behave byte-identically to the pre-P3 engine.

## Movement

A **zone move** sets the mover's zone via the `MOVE_ZONE` Effect through `apply()` (single-writer)
and recomputes perception; arriving prints the new zone survey. The taught grammar covers it: the
`move` operation (verbs go/move/walk/head/approach/climb/enter) takes a zone name (`go to the
cockpit`), or an entity (`approach the radio` — derives its zone). One walk-edge step per command,
**instant in v1** — durations and auto-pathing land with the P4 activity scheduler (the
`duration_minutes` seam is already plumbed). No walk-edge → an informative route redirect naming
the direction and first step. Scene transitions (a second Scene-Room, e.g. a future ravine) reuse
Evennia rooms/exits — none exist in the crash-site scenario yet.

## Perception bands

[`PerceptionBand`](../../game/world/sim/contracts.py) (design §14) grades *how clearly* one thing
is perceived from an observer's zone:

| Band | Detail |
|---|---|
| `SAME_ZONE` | detailed |
| `ADJACENT_ZONE` | clear |
| `NEAR_VISIBLE` | summarized |
| `DISTANT_VISIBLE` | vague |
| `BARELY_VISIBLE` | shape or motion |
| `AUDIBLE_ONLY` | sound only |
| `OUT_OF_SIGHT` | nothing (no message) |

**v1 band math** ([`perception.py`](../../game/world/sim/space/perception.py)): the visual band is
**see-edge hop count** through the zone graph (0 hops = `SAME_ZONE` … 4 = `BARELY_VISIBLE`; no
see-path = `OUT_OF_SIGHT`), shifted by the §15 weather band-steps. **Weather is a stub**: every
caller passes `"clear"` until the P7 weather arc threads real state (the seed's
`weather_visibility_m` meters model is part of that deferral, with planar-distance banding and
finer occlusion — recorded in DR-13a). Sight and hearing are computed separately; reachability is
separate again.

[`PerceptionResult`](../../game/world/sim/contracts.py) bundles the outcome: `band`, `visible`,
`audible`, `reachable`, `direction_phrase`, `distance_m`. Reachability is deliberately a distinct
boolean: you can *see* the case by the bulkhead yet not *manipulate* it (§17).

## Direction phrasing

[`direction.py`](../../game/world/sim/space/direction.py) turns `zones.bearing_deg` plus the
elevation delta into the 8 compass points with `upslope`/`downslope` — *"to the southeast and
upslope"*. Landmark-relative phrasing is scenario/shell layering, later.

**Rendering follows DR-23's look-tree**: bare `look` = the room survey ("You are in {zone}." +
zone prose + the scene composed per-band: same-zone full salience prose, then direction-framed
graded groups; `OUT_OF_SIGHT` absent); `look at X` ≡ `examine X` = the unified `describe()` when
in reach, the §17 "too far to {verb} from here" answer beyond it. The seed's `look <direction>` /
`scan` verbs are **deferred** (BACKLOG), not part of v1.

## Sound & speech propagation

[`sound.py`](../../game/world/sim/space/sound.py): voice modes map to reach — `whisper` → same
zone, `say` → adjacent, `call` → near, `shout` → distant (§15). Weather shifts reach in
band-steps (`steady_snow` −1 … `whiteout` −3; stubbed at `"clear"`), clamped so the same zone
always hears. A muffled edge costs 2 hops. Loudness governs non-speech events identically —
quiet work carries a zone; shattering glass carries three.

## The message propagator (replaces `msg_contents`)

For each observer the shell computes a `PerceptionResult` toward the event's source and renders
that band's text form (or nothing for `OUT_OF_SIGHT`): full third-person line → direction-framed
line → "…is working at something." → "A shape shifts {direction}." → sound-only → silence. The
**frozen** `Event(kind, source_id, loudness, data)` is the carrier: the shell derives the source
zone by looking `source_id` up in the room (with `data["zone"]` as an optional override) — the
seed's `Event(actor, zone, text_same_zone)` shape was never frozen and is retired. Voice lives in
the scenario responses (`perceive.*` templates) with in-code fallbacks.

## The reachability tax (known cost, paid)

Because a Scene is one Evennia Room, **containment no longer equals "reachable."** The tax is paid
in three places, not a mixin: (1) the **resolver's central reach gate** — any bound X/Y/tool
outside the actor's zone returns the §17 redirect ("You can see the {target} {direction}, but it
is too far away to {verb} from here.") before any tier runs, gating every taught verb including
`examine` and future authored rules; (2) the stock **`get` pre-flight** in the item commands;
(3) **`return_appearance`** for stock `look at`. The parser still *matches* visible-but-far nouns
(the worldview's `reachables()` is the perception-visible set; `reachable()` is the manipulable
same-zone set) — so distant things get honest "too far" answers, never "you don't see that here."

## Related

- [overview.md](overview.md) — where this sits in the whole.
- [presentation.md](presentation.md) — DR-23: the prose the bands feed.
- [tick-and-scheduler.md](tick-and-scheduler.md) — perception-routed *tick* messages (P4).
- Roadmap P3 (shipped) → the P4 scheduler picks up move durations; P7 the real weather.
