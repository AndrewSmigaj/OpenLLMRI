"""game.typeclasses.worldview — the read boundary: marshal Evennia objects → the pure core (DR-01).

Builds a per-action, read-only view of the room: `get(sim_id)` marshals an `EntityState` from an
object's Attributes; `reachables()` builds the parser's `Reachable` descriptors (name/aliases/ident +
part labels). The pure core never touches Evennia objects — only this view. READS only (no writes), so
it is NOT the single-writer (that's apply.py).

Object Attribute schema (set by content build.py): db.sim_id (str), db.materials (list[str]),
db.parts (list[dict{id,label,material,mass_g,attachment,outputs_when_removed}]), db.mass_g (int, body),
db.state (dict — incl. 'ident', 'zone' (DR-13a), tool capabilities like 'edge'/'leverage'),
db.provenance (list[str]), db.owner. The Evennia object's aliases feed noun-matching.

DR-13a: `reachables()` is the perception-VISIBLE set (+ zone pseudo-nouns, so destinations parse
and far things get honest 'too far' answers); `reachable()` is the manipulable same-zone set. An
unzoned room behaves byte-identically to pre-P3 (the one-zone compat rule).
"""
from __future__ import annotations

from world.sim.contracts import EntityState, Part, Reachable
from world.sim.space import perception, zones as zonemap


def zone_of(obj, room):
    """An object's effective zone: carried things are wherever their carrier is; otherwise
    state['zone']; otherwise the room's default zone; otherwise None (the one-zone world)."""
    loc = getattr(obj, "location", None)
    if loc is not None and loc is not room and hasattr(loc, "location"):   # carried
        return zone_of(loc, room)
    z = ((obj.db.state or {}) if hasattr(obj, "db") else {}).get("zone")
    return z or (room.db.default_zone if room is not None else None)


def _parts(obj):
    return [Part(id=p["id"], material=p.get("material", "unknown"), mass_g=int(p.get("mass_g", 0)),
                 attachment=p.get("attachment", "fixed"),
                 outputs_when_removed=tuple(p.get("outputs_when_removed", ())))
            for p in (obj.db.parts or [])]


def to_entity_state(obj) -> EntityState:
    return EntityState(
        id=obj.db.sim_id or obj.key, name=obj.key,
        materials=list(obj.db.materials or []), parts=_parts(obj),
        tags=[t for t in obj.tags.all() if t], mass_g=int(obj.db.mass_g or 0),
        state=dict(obj.db.state or {}), provenance=list(obj.db.provenance or []), owner=obj.db.owner)


def to_reachable(obj) -> Reachable:
    parts = tuple((p["id"], p.get("label", p["id"])) for p in (obj.db.parts or []))
    return Reachable(id=obj.db.sim_id or obj.key, name=obj.key,
                     aliases=tuple(obj.aliases.all()), ident=(obj.db.state or {}).get("ident", ""),
                     parts=parts)


class EvenniaWorldView:
    """Read-only per-action view over a room's objects (+ the actor). Satisfies the WorldView protocol."""

    def __init__(self, room, actor, seed=0):
        self.room = room
        self.actor = actor
        self.seed_state = int(seed or 0)
        self.actor_zone = zone_of(actor, room) if actor is not None else None
        self._zoned = bool(room is not None and room.db.default_zone and zonemap.loaded())
        self._by_sim = {}
        pool = list(room.contents) if room else []
        if actor is not None:
            pool += list(actor.contents)          # the actor's inventory is reachable too
        for obj in pool:
            self._by_sim[obj.db.sim_id or obj.key] = obj

    def _zone_of_sim(self, sim_id):
        obj = self._by_sim.get(sim_id)
        return zone_of(obj, self.room) if obj is not None else None

    def _carried(self, obj):
        return self.actor is not None and getattr(obj, "location", None) is self.actor

    def get(self, sim_id):
        if isinstance(sim_id, str) and sim_id.startswith("zone:"):
            z = zonemap.get(sim_id[5:])
            return EntityState(id=sim_id, name=z.name, materials=[], parts=[],
                               tags=["zone"], mass_g=0, state={"zone": z.id},
                               provenance=[], owner=None) if z else None
        obj = self._by_sim.get(sim_id)
        if obj is None:
            return None
        ent = to_entity_state(obj)
        z = zone_of(obj, self.room)
        if z:
            ent.state["zone"] = z    # the EFFECTIVE zone always wins: a carried thing is wherever
        return ent                   # its carrier stands, whatever its stale authored zone says

    def obj(self, sim_id):
        return self._by_sim.get(sim_id)

    def reachable(self, actor_id):
        """The MANIPULABLE set: same-zone + the actor's inventory (everything when unzoned)."""
        if not self._zoned:
            return list(self._by_sim)
        return [sid for sid, o in self._by_sim.items()
                if self._carried(o) or zone_of(o, self.room) == self.actor_zone]

    def in_zone(self, zone):
        if not self._zoned:
            return list(self._by_sim)
        return [sid for sid, o in self._by_sim.items() if zone_of(o, self.room) == zone]

    def reachables(self):
        """The parser's matching set: perception-VISIBLE entities + zone pseudo-nouns (DR-13a)."""
        if not self._zoned:
            return [to_reachable(o) for o in self._by_sim.values()]
        out = []
        for o in self._by_sim.values():
            if self._carried(o) or perception.perceive(
                    self.actor_zone, zone_of(o, self.room)).visible:
                out.append(to_reachable(o))
        for zid, z in sorted(zonemap.all_zones().items()):
            out.append(Reachable(id=f"zone:{zid}", name=z.name, aliases=z.aliases))
        return out
