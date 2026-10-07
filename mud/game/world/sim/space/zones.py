"""world.sim.space.zones — a character's zone within the one Scene (DR-13/DR-13a, §10). Pure.

A Scene is ONE Evennia Room; a zone is a position within it: coords + terrain tags + authored
edges. The zone map is loaded-once scenario CONTENT (`load_zones`, mirroring the narrator /
appearance registries). Edges are undirected with three flags: `walk` (movement), `see`
(sightline — a fuselage wall is simply an ABSENT see-edge), `muffle` (sound passes but damped;
costs 2 hops). Band math v1 uses see-edge HOPS; coords feed direction/distance phrases only
(planar-distance band refinement is a recorded deferral, DR-13a).
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    id: str
    name: str                                # display: "the mid cabin"
    x: float
    y: float
    elevation: float = 0.0
    terrain_tags: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    look: str = ""                           # authored zone-survey prose (content)


_ZONES: dict[str, Zone] = {}
_EDGES: dict[frozenset, dict] = {}


def load_zones(zone_table: dict) -> None:
    """Install a scenario's zone map. Edges may be declared on either side; a contradictory
    double declaration is a content error (raised at load — the §44 spirit: fail at build)."""
    _ZONES.clear()
    _EDGES.clear()
    for zid, z in (zone_table or {}).items():
        _ZONES[zid] = Zone(id=zid, name=z["name"], x=float(z["x"]), y=float(z["y"]),
                           elevation=float(z.get("elevation", 0.0)),
                           terrain_tags=tuple(z.get("terrain_tags", ())),
                           aliases=tuple(z.get("aliases", ())),
                           look=z.get("look", ""))
    for zid, z in (zone_table or {}).items():
        for other, props in (z.get("adjacent") or {}).items():
            if other not in _ZONES:
                raise ValueError(f"zone {zid!r} adjacent to unknown zone {other!r}")
            if other == zid:
                raise ValueError(f"zone {zid!r} declared adjacent to itself")
            key = frozenset((zid, other))
            norm = {"walk": bool(props.get("walk")), "see": bool(props.get("see")),
                    "muffle": bool(props.get("muffle"))}
            if key in _EDGES and _EDGES[key] != norm:
                raise ValueError(f"contradictory edge declarations for {sorted(key)}")
            _EDGES[key] = norm


def loaded() -> bool:
    return bool(_ZONES)


def get(zone_id) -> "Zone | None":
    """None for unknown/None ids — a stale zone id degrades to 'unzoned', never a crash."""
    return _ZONES.get(zone_id) if zone_id else None


def all_zones() -> dict[str, Zone]:
    return dict(_ZONES)


def _neighbors(zone_id):
    for key, props in _EDGES.items():
        if zone_id in key:
            (other,) = key - {zone_id}
            yield other, props


def walk_neighbors(zone_id: str) -> tuple[str, ...]:
    return tuple(sorted(other for other, props in _neighbors(zone_id) if props["walk"]))


def see_hops(a, b) -> "int | None":
    """Hop count over see-edges; None = no sightline. Deterministic (sorted expansion)."""
    return _hops(a, b, cost=lambda props: 1 if props["see"] else None)


def sound_hops(a, b) -> "int | None":
    """Weighted hops over ALL edges for sound; a muffled edge costs 2 (−1 band, §15)."""
    return _hops(a, b, cost=lambda props: 2 if props["muffle"] else 1)


def _hops(a, b, cost):
    if a is None or b is None or a not in _ZONES or b not in _ZONES:
        return None
    if a == b:
        return 0
    dist = {a: 0}
    frontier = [(0, a)]
    while frontier:
        d, cur = heapq.heappop(frontier)
        if d > dist.get(cur, d):
            continue
        for other, props in sorted(_neighbors(cur)):
            c = cost(props)
            if c is None:
                continue
            nd = d + c
            if nd < dist.get(other, nd + 1000000):
                dist[other] = nd
                heapq.heappush(frontier, (nd, other))
    return dist.get(b)


def bearing_deg(a: str, b: str) -> float:
    """Compass bearing a→b in degrees, 0 = north (y+), clockwise. Deterministic."""
    za, zb = _ZONES[a], _ZONES[b]
    return math.degrees(math.atan2(zb.x - za.x, zb.y - za.y)) % 360.0


def distance_m(a: str, b: str) -> float:
    za, zb = _ZONES[a], _ZONES[b]
    return math.hypot(zb.x - za.x, zb.y - za.y)
