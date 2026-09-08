"""world.sim.testing.pure_world — an in-memory WorldView with an in-memory apply() (DR-12, DR-18a). Pure.

`PureWorld` is the read boundary the pure core needs (`get` / `reachable` / `in_zone` /
`reachables`) over plain `EntityState`s, PLUS an `apply(effects)` that mirrors the shell's single
writer for every EffectKind — so a CHAIN of typed commands (break the bottle → cut with the shard →
burn the cover) can run entirely without Evennia: probes, fuzz, replay, render-scenes, the play
harness. It is NOT a second writer of Evennia state (DR-10 is untouched); it is the test double whose
semantics `tests/integration/test_apply_parity.py` pins to the real `apply()`.

Built from the same `OBJECT_TABLE` the Evennia loader walks (`from_table`), so the two worlds can't
drift. Containment is a parent map (the DR-24 reveal walk: contents of a container enter the world
only once it is open or searched; worn things show on their wearer). Zones come from the loaded zone
map; the actor stands in `actor_zone`. Pseudo-nouns (`zone:` / `form:`) resolve as in the shell.
"""
from __future__ import annotations

from dataclasses import replace

from world.sim.affordances import FORMS
from world.sim.conservation.ledger import EnvironmentSink, check
from world.sim.contracts import EffectKind, EntityState, Part, Reachable
from world.sim.space import perception
from world.sim.space import zones as zonemap


class LedgerError(Exception):
    """The ledger rejected an effect set (a bug in content/logic, never a player failure)."""


def _parts(rows) -> list:
    return [Part(id=p["id"], material=p.get("material", "unknown"), mass_g=int(p.get("mass_g", 0)),
                 attachment=p.get("attachment", "fixed"),
                 outputs_when_removed=tuple(p.get("outputs_when_removed", ())))
            for p in (rows or [])]


class PureWorld:
    """Satisfies the WorldView protocol; adds `apply`, `reachables`, `give`, `snapshot`."""

    def __init__(self, entities, actor_id="me", actor_zone=None, seed=0, default_zone=None,
                 aliases=None, locations=None):
        self._e: dict = {}
        self._alias: dict = dict(aliases or {})
        self._loc: dict = dict(locations or {})     # id -> parent id (absent = loose in the room)
        for e in entities:
            self._e[e.id] = e
        self.actor_id = actor_id
        self.seed_state = int(seed or 0)
        self.default_zone = default_zone
        self.sink = EnvironmentSink()
        self.applied: list = []
        if actor_id not in self._e:
            self._e[actor_id] = EntityState(id=actor_id, name="you", materials=["flesh"],
                                            mass_g=70000, state={})
        if actor_zone:
            self._e[actor_id].state["zone"] = actor_zone

    # --- construction -------------------------------------------------------------------------
    @classmethod
    def from_table(cls, rows, actor_id="me", actor_zone=None, seed=0, default_zone="mid_cabin"):
        ents, aliases, loc = [], {}, {}
        for r in rows:
            st = dict(r.get("state") or {})
            if "zone" in r:
                st["zone"] = r["zone"]
            ents.append(EntityState(id=r["sim_id"], name=r["name"], materials=list(r.get("materials") or []),
                                    parts=_parts(r.get("parts")), tags=[], mass_g=int(r.get("mass_g", 0)),
                                    state=st, provenance=[], owner=None))
            aliases[r["sim_id"]] = tuple(r.get("aliases") or ())
            if "in" in r:
                loc[r["sim_id"]] = r["in"]
        return cls(ents, actor_id=actor_id, actor_zone=actor_zone, seed=seed, default_zone=default_zone,
                   aliases=aliases, locations=loc)

    # --- zones & containment ------------------------------------------------------------------
    @property
    def actor_zone(self):
        return self.effective_zone(self.actor_id)

    @property
    def zoned(self) -> bool:
        return bool(self.default_zone and zonemap.loaded())

    def parent(self, eid):
        return self._loc.get(eid)

    def contents(self, eid) -> list:
        return [k for k, v in self._loc.items() if v == eid and k in self._e]

    def effective_zone(self, eid):
        """A carried/stowed thing is wherever its top-level holder is (worldview.zone_of)."""
        seen = set()
        cur = eid
        while cur in self._loc and cur not in seen:
            seen.add(cur)
            cur = self._loc[cur]
        top = self._e.get(cur)
        z = (top.state or {}).get("zone") if top else None
        return z or self.default_zone

    def _revealed(self, eid) -> bool:
        st = (self._e[eid].state or {}) if eid in self._e else {}
        return bool(st.get("open") or st.get("searched"))

    def _visible_ids(self) -> list:
        """The DR-24 pool walk: loose things + the actor's things; descend only through revealed
        containers and the actor; worn layers show on their wearer."""
        pool = [k for k in self._e if k not in self._loc] + self.contents(self.actor_id)
        seen, out = set(), []
        while pool:
            eid = pool.pop(0)
            if eid in seen or eid not in self._e:
                continue
            seen.add(eid)
            out.append(eid)
            kids = self.contents(eid)
            if eid == self.actor_id or self._revealed(eid):
                pool.extend(kids)
            else:
                pool.extend(k for k in kids if (self._e[k].state or {}).get("worn_by"))
        return out

    # --- the WorldView protocol ---------------------------------------------------------------
    def get(self, sim_id):
        if isinstance(sim_id, str) and sim_id.startswith("zone:"):
            z = zonemap.get(sim_id[5:])
            return EntityState(id=sim_id, name=z.name, tags=["zone"], state={"zone": z.id}) if z else None
        if isinstance(sim_id, str) and sim_id.startswith("form:"):
            f = sim_id[5:]
            return EntityState(id=sim_id, name=f, tags=["form"], state={"form": f}) if f in FORMS else None
        ent = self._e.get(sim_id)
        if ent is None:
            return None
        st = dict(ent.state or {})
        par = self._loc.get(sim_id)
        if par is not None and par in self._e:
            st["in"] = par
        kids = self.contents(sim_id)
        if kids:
            st["contents"] = sorted(self._e[k].name for k in kids if not (self._e[k].state or {}).get("worn_by"))
            worn = sorted(self._e[k].name for k in kids if (self._e[k].state or {}).get("worn_by"))
            if worn:
                st["worn"] = worn
        z = self.effective_zone(sim_id)
        if z:
            st["zone"] = z
        return replace(ent, state=st, parts=list(ent.parts), materials=list(ent.materials),
                       tags=list(ent.tags), provenance=list(ent.provenance))

    def raw(self, sim_id):
        """The live stored EntityState (mutable) — tooling only; the core uses get()."""
        return self._e.get(sim_id)

    def reachable(self, actor_id):
        vis = self._visible_ids()
        if not self.zoned:
            return vis
        az = self.effective_zone(actor_id)
        return [i for i in vis if self._loc.get(i) == actor_id or self.effective_zone(i) == az]

    def in_zone(self, zone):
        vis = self._visible_ids()
        if not self.zoned:
            return vis
        return [i for i in vis if self.effective_zone(i) == zone]

    def reachables(self):
        """The parser's matching set: perception-VISIBLE entities + zone + form pseudo-nouns."""
        out = []
        az = self.actor_zone
        for i in self._visible_ids():
            e = self._e[i]
            if self.zoned and i != self.actor_id and self._loc.get(i) != self.actor_id:
                if not perception.perceive(az, self.effective_zone(i)).visible:
                    continue
            parts = tuple((p.id, p.id) for p in e.parts)
            aliases = self._alias.get(i, ())
            if i == self.actor_id:
                aliases = tuple(aliases) + ("me", "self", "myself")
            out.append(Reachable(id=i, name=e.name, aliases=tuple(aliases),
                                 ident=str((e.state or {}).get("ident", "") or ""), parts=parts,
                                 held=(self._loc.get(i) == self.actor_id)))
        if self.zoned:
            for zid, z in sorted(zonemap.all_zones().items()):
                out.append(Reachable(id=f"zone:{zid}", name=z.name, aliases=tuple(z.aliases)))
        for f in sorted(FORMS):
            out.append(Reachable(id=f"form:{f}", name=f))
        return out

    # --- tooling conveniences -----------------------------------------------------------------
    def give(self, sim_id):
        """Test setup: put a thing (wherever it is stowed) into the actor's hands."""
        if sim_id not in self._e:
            raise KeyError(sim_id)
        self._loc[sim_id] = self.actor_id
        self._e[sim_id].state.pop("zone", None)

    def snapshot(self) -> dict:
        """A comparable picture of the world (for the parity test): id → (name, materials, mass,
        parts, sorted state items, parent)."""
        out = {}
        for i, e in self._e.items():
            st = {k: v for k, v in (e.state or {}).items() if k not in ("zone",)}
            out[i] = (e.name, tuple(e.materials), int(e.mass_g),
                      tuple((p.id, p.material, p.mass_g, p.attachment) for p in e.parts),
                      tuple(sorted((k, repr(v)) for k, v in st.items())), self._loc.get(i))
        return out

    # --- the in-memory single writer (mirrors typeclasses/apply.py) ---------------------------
    def apply(self, effects):
        effects = list(effects)
        verdict = check(self, effects)
        if not verdict.ok:
            raise LedgerError(verdict.reason)
        for e in effects:
            self._apply_one(e)
        if verdict.sink_delta.get("mass_g"):
            self.sink.absorb(int(verdict.sink_delta["mass_g"]))
        self.applied.append(tuple(effects))
        return verdict

    def _apply_one(self, e):
        k = e.kind
        a = e.args
        if k == EffectKind.REMOVE_PART:
            ent = self._e[e.target_id]
            ent.parts = [p for p in ent.parts if p.id != a.get("part_id")]
        elif k == EffectKind.CREATE_OBJECT:
            state = dict(a.get("state") or {})
            if a.get("form"):
                state["form"] = a["form"]
            if self.actor_zone:
                state["zone"] = self.actor_zone
            self._e[e.target_id] = EntityState(
                id=e.target_id, name=str(a.get("template", e.target_id)).replace("_", " "),
                materials=[a["material"]] if a.get("material") else [], mass_g=int(a.get("mass_g", 0)),
                state=state, provenance=list(a.get("provenance", [])))
            self._alias[e.target_id] = ()
        elif k == EffectKind.CONSUME:
            ent = self._e.get(e.target_id)
            if ent is None:
                return
            m = a.get("mass_g")
            if m is not None and int(m) < ent.mass_g + sum(p.mass_g for p in ent.parts):
                ent.mass_g = max(0, ent.mass_g - int(m))
                return
            parent = self._loc.pop(e.target_id, None)
            for kid in self.contents(e.target_id):           # contents fall to the holder / room
                if parent is None:
                    self._loc.pop(kid, None)
                    self._e[kid].state["zone"] = self.effective_zone(e.target_id) or self.default_zone
                else:
                    self._loc[kid] = parent
            del self._e[e.target_id]
        elif k == EffectKind.SET_ATTR:
            self._e[e.target_id].state[a["key"]] = a["value"]
        elif k == EffectKind.ADJUST_ATTR:
            st = self._e[e.target_id].state
            st[a["key"]] = st.get(a["key"], 0) + a["delta"]
        elif k == EffectKind.SET_OWNER:
            self._e[e.target_id].owner = a.get("owner")
        elif k == EffectKind.TRANSFER:
            if e.target_id not in self._e or a.get("dest") not in self._e:
                raise LedgerError(f"transfer: unknown object ({e.target_id!r} -> {a.get('dest')!r})")
            self._loc[e.target_id] = a["dest"]
            self._e[e.target_id].state.pop("zone", None)
        elif k == EffectKind.MOVE_ZONE:
            self._loc.pop(e.target_id, None)
            self._e[e.target_id].state["zone"] = a.get("zone")
