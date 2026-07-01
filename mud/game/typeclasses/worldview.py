"""game.typeclasses.worldview — the read boundary: marshal Evennia objects → the pure core (DR-01).

Builds a per-action, read-only view of the room: `get(sim_id)` marshals an `EntityState` from an
object's Attributes; `reachables()` builds the parser's `Reachable` descriptors (name/aliases/ident +
part labels). The pure core never touches Evennia objects — only this view. READS only (no writes), so
it is NOT the single-writer (that's apply.py).

Object Attribute schema (set by content build.py): db.sim_id (str), db.materials (list[str]),
db.parts (list[dict{id,label,material,mass_g,attachment,outputs_when_removed}]), db.mass_g (int, body),
db.state (dict — incl. 'ident', tool capabilities like 'edge'/'leverage'), db.provenance (list[str]),
db.owner. The Evennia object's aliases feed noun-matching.
"""
from __future__ import annotations

from world.sim.contracts import EntityState, Part, Reachable


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
        self._by_sim = {}
        pool = list(room.contents) if room else []
        if actor is not None:
            pool += list(actor.contents)          # the actor's inventory is reachable too
        for obj in pool:
            self._by_sim[obj.db.sim_id or obj.key] = obj

    def get(self, sim_id):
        obj = self._by_sim.get(sim_id)
        return to_entity_state(obj) if obj else None

    def obj(self, sim_id):
        return self._by_sim.get(sim_id)

    def reachable(self, actor_id):
        return list(self._by_sim)

    def in_zone(self, zone):
        return list(self._by_sim)

    def reachables(self):
        return [to_reachable(o) for o in self._by_sim.values()]
