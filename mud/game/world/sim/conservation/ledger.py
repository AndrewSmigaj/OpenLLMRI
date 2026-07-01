"""world.sim.conservation.ledger — the pre-commit conservation ledger (DR-11, §24). Pure.

Runs inside the shell's `apply()` BEFORE commit. Invariant: **mass is never CREATED** (added ≤ removed);
any legitimate loss (removed − added — e.g. smoke/heat when burning) goes to the **accountable
environment sink** (monotonic). Created objects must carry provenance. An `ok=False` verdict is a BUG
(unphysical authored content / handler logic), not a player failure — it's logged and fails the build.

Mass model: an object's `mass_g` is its BODY mass (EXCLUDING its parts); each `Part` carries its own
mass; total = `mass_g` + Σ parts. `REMOVE_PART` removes the part's mass; `CONSUME` removes the whole
object (or a given mass); `CREATE_OBJECT` adds a mass. `SET_ATTR`/`ADJUST_ATTR` only move mass if they
touch `mass_g` (defensive — the P1 operations never do).
"""
from __future__ import annotations

from world.sim.contracts import EffectKind, LedgerVerdict


def _total_mass(ent) -> int:
    return int(ent.mass_g) + sum(int(p.mass_g) for p in ent.parts)


def _find_part(ent, part_id):
    for p in ent.parts:
        if p.id == part_id:
            return p
    return None


def check(pre, effects) -> LedgerVerdict:
    """Verify a set of Effects conserves mass before commit. Returns a LedgerVerdict."""
    added = 0
    removed = 0
    no_provenance = []
    for e in effects:
        k = e.kind
        if k == EffectKind.CREATE_OBJECT:
            added += int(e.args.get("mass_g", 0) or 0)
            if not e.args.get("provenance"):
                no_provenance.append(e.target_id)
        elif k == EffectKind.REMOVE_PART:
            ent = pre.get(e.target_id)
            part = _find_part(ent, e.args.get("part_id")) if ent else None
            if part is None:
                return LedgerVerdict(False, f"remove_part: no part {e.args.get('part_id')!r} on {e.target_id!r}")
            removed += int(part.mass_g)
        elif k == EffectKind.CONSUME:
            ent = pre.get(e.target_id)
            if ent is None:
                return LedgerVerdict(False, f"consume: unknown target {e.target_id!r}")
            m = e.args.get("mass_g")
            removed += int(m) if m is not None else _total_mass(ent)
        elif k in (EffectKind.SET_ATTR, EffectKind.ADJUST_ATTR) and e.args.get("key") == "mass_g":
            ent = pre.get(e.target_id)
            old = int(ent.mass_g) if ent else 0
            delta = (int(e.args.get("value", old)) - old) if k == EffectKind.SET_ATTR else int(e.args.get("delta", 0))
            if delta >= 0:
                added += delta
            else:
                removed += -delta
        # MOVE_ZONE, SET_OWNER, and non-mass SET/ADJUST: no mass change.

    if added > removed:
        return LedgerVerdict(False, f"mass created from nothing: +{added}g added vs {removed}g removed")
    if no_provenance:
        return LedgerVerdict(False, f"created object(s) without provenance: {no_provenance}")
    return LedgerVerdict(True, sink_delta={"mass_g": removed - added})


class EnvironmentSink:
    """The accountable pseudo-entity that absorbs mass legitimately leaving the modeled world (smoke,
    heat). Tracks its running total and may only GROW (DR-11) — anomalous growth is reviewable and a bug
    signal. Used by the shell's `apply()` AFTER commit; `check()` above stays pure."""

    def __init__(self):
        self._mass_g = 0

    @property
    def mass_g(self) -> int:
        return self._mass_g

    def absorb(self, mass_g: int) -> None:
        if mass_g < 0:
            raise ValueError("environment sink is monotonic — it cannot release mass")
        self._mass_g += int(mass_g)
