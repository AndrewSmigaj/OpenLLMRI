"""game.typeclasses.apply — the SINGLE enforced state writer (DR-10). Shell (touches Evennia + the DB).

`apply(effects, world, sink)` is the only thing that mutates world state: it runs the conservation
ledger BEFORE any write, wraps the writes in `transaction.atomic`, updates Attributes (+ Tag mirror
where relevant), and on a rolled-back transaction calls `reset_cache()` on the touched handlers (the
verified Evennia eager-cache footgun). A ledger rejection is a bug (LedgerError), not a player failure.

This module is ALLOWLISTED in tools/lints/check_no_raw_writes.py — it is the choke-point; nothing else
in the shell may write Attributes/Tags directly.
"""
from __future__ import annotations

import evennia
from django.db import transaction

from world.sim.conservation.ledger import EnvironmentSink, check
from world.sim.contracts import EffectKind

_DERIVED_TYPECLASS = "typeclasses.objects.Object"


class LedgerError(Exception):
    """The conservation ledger rejected an effect set (unphysical content/logic — a bug, not a failure)."""


def get_sink(room):
    """The room's per-run environment sink (a runtime accumulator on .ndb; DR-11)."""
    if room.ndb.sink is None:
        room.ndb.sink = EnvironmentSink()
    return room.ndb.sink


def apply(effects, world, sink=None):
    verdict = check(world, effects)
    if not verdict.ok:
        raise LedgerError(verdict.reason)

    touched = []
    try:
        with transaction.atomic():
            for e in effects:
                _apply_one(e, world, touched)
    except Exception:
        for obj in touched:
            try:
                obj.attributes.reset_cache()
                obj.tags.reset_cache()
            except Exception:
                pass
        raise

    if sink is not None and verdict.sink_delta.get("mass_g"):
        sink.absorb(int(verdict.sink_delta["mass_g"]))
    return verdict


def _apply_one(e, world, touched):
    k = e.kind
    if k == EffectKind.REMOVE_PART:
        obj = world.obj(e.target_id)
        obj.db.parts = [p for p in (obj.db.parts or []) if p.get("id") != e.args.get("part_id")]
        touched.append(obj)
    elif k == EffectKind.CREATE_OBJECT:
        key = str(e.args.get("template", e.target_id)).replace("_", " ")
        evennia.create_object(
            _DERIVED_TYPECLASS, key=key, location=world.room,
            attributes=[("sim_id", e.target_id),
                        ("materials", [e.args["material"]] if e.args.get("material") else []),
                        ("mass_g", int(e.args.get("mass_g", 0))),
                        ("state", {}),
                        ("provenance", list(e.args.get("provenance", [])))],
            tags=[("slice", "run_id")])
    elif k == EffectKind.CONSUME:
        obj = world.obj(e.target_id)
        if obj:
            obj.delete()
    elif k == EffectKind.SET_ATTR:
        obj = world.obj(e.target_id)
        st = dict(obj.db.state or {})
        st[e.args["key"]] = e.args["value"]
        obj.db.state = st
        touched.append(obj)
    elif k == EffectKind.ADJUST_ATTR:
        obj = world.obj(e.target_id)
        st = dict(obj.db.state or {})
        st[e.args["key"]] = st.get(e.args["key"], 0) + e.args["delta"]
        obj.db.state = st
        touched.append(obj)
    elif k == EffectKind.SET_OWNER:
        obj = world.obj(e.target_id)
        obj.db.owner = e.args.get("owner")
        touched.append(obj)
    # MOVE_ZONE lands with perception (P3).
