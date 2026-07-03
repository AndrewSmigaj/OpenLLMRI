# ADR-0004: Zone as a position attribute, not a room

- **Status:** Accepted
- **Date:** 2026-06

## Context

Design §10–15 calls for **overlapping perceptual spaces**: within a broad
dramatic *Scene*, a character occupies a *zone* (a position), and what they
perceive — visibility, audibility, reachability, relative direction, detail — is
computed from that position and is distance/weather/occlusion-aware. Crucially
(§10): *"do not collapse these into room."*

Two ways to map this onto Evennia's room graph:

1. **Zone-as-room.** Make every zone its own Evennia Room and wire exits between
   them. Reuses room containment and `move_to`, but a single crash basin becomes
   a dozen-plus rooms; perception *within* a scene (the whole point of §10–15)
   would have to be reconstructed *across* rooms anyway, and "everyone in the same
   dramatic space" is lost. Room count explodes per scenario.
2. **Zone-as-attribute (chosen).** One Evennia Room per **Scene**; the character's
   **zone** is a position **Attribute**. Perception is computed by the pure
   [`world/sim/space/*`](../../../game/world/sim/space/) layer from zone
   coordinates.

## Decision

A **Scene = one Evennia Room.** A character's **zone = a position Attribute**
(a coordinate/graph node with `x`, `y`, `elevation`, `terrain_tags`).

- **Scene transitions** (cabin → exterior → forest) use Evennia rooms, exits and
  `move_to` — normal Evennia machinery.
- **Intra-scene zone moves and all perception** are custom, driven by
  `world/sim/space/{zones,perception,direction,sound}`.

## Consequences

- **Single dramatic space preserved.** Everyone in a Scene shares one Room, so
  §10–15's overlapping-zone perception is natural and the world isn't shredded
  into micro-rooms.
- **The reachability tax (accepted cost).** Because everyone in a Scene shares one
  Evennia Room, **Evennia's room containment no longer equals "reachable."**
  Default `get`/`drop`/`look`/`give` and every manipulation verb must be **gated
  by a reachability check on each interaction** — a **`ReachabilityMixin`**
  consulting the perception layer before the verb runs. You can *see* the orange
  case by the bulkhead yet be unable to *manipulate* it (§17). This per-command
  gating is the deliberate price of zone-as-attribute.
- A plain `msg_contents` is wrong (it would tell the whole Scene one thing); the
  shell uses a **message propagator** that renders per observer by perception
  band. See [../perception-model.md](../perception-model.md).

## Implementation note (appended 2026-07 — P3 shipped)

Shipped as specified, with one refinement: the reachability tax is paid by a **central resolver
reach gate** (plus the stock-get pre-flight and `return_appearance`) rather than a per-command
`ReachabilityMixin` — one choke-point gates every taught verb, including future authored rules.
Zone storage landed as `state["zone"]` (not a dedicated Attribute); v1 bands are see-edge hops;
weather is a stubbed parameter until P7. Details: `implementation-architecture.md` DR-13a and
`perception-model.md` (spec of record).
