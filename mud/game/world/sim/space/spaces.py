"""world.sim.space.spaces — the authored SPACES within a zone (the scene-space model). Pure.

A zone's scene is a set of SPACES — physical areas (the floor, the footwell, overhead). Each space
owns a FRAME that describes POSITION, never history: "Across the cockpit floor {be} {items}." stays
true the instant a player drops a can opener onto it, where "spilled from the wreck" would become a
lie. A space also owns an `order` (where it falls in the survey), a `cap` (how many things it names
before absorbing the rest into an `overflow` phrase), and `aliases` (so `look at <space>` resolves).

An object's space is `state['space']` if a player placed it there, else the appearance entry's
authored `space` (its home), else the zone's `default` space. A space describes CHARACTER, not
inventory — discovery of what's inside things stays a `look at` / `search` / `open` (DR-24). Loaded
once as scenario CONTENT (`load_spaces`, mirroring the zones / appearance registries).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Space:
    id: str
    zone: str
    order: int = 50
    frame: str = ""                          # "Across the cockpit floor {be} {items}." ({be}=is/are)
    cap: int = 3                             # names at most `cap`, then absorbs into `overflow`
    overflow: str = ""                       # "a scatter of smaller debris" (look-at-able in Firing B)
    default: bool = False                    # where a player drop lands when no space is named
    aliases: tuple[str, ...] = ()


_SPACES: dict[tuple[str, str], Space] = {}   # (zone_id, space_id) -> Space
_BY_ZONE: dict[str, tuple[Space, ...]] = {}  # zone_id -> spaces, ordered


def load_spaces(space_table: dict) -> None:
    """Install a scenario's per-zone space table. At most one `default` per zone — a contradiction
    is a content error raised at load (the §44 spirit: fail at build, not at look)."""
    _SPACES.clear()
    _BY_ZONE.clear()
    for zid, spaces in (space_table or {}).items():
        ordered = []
        for sid, s in (spaces or {}).items():
            sp = Space(id=sid, zone=zid, order=int(s.get("order", 50)),
                       frame=s.get("frame", ""), cap=int(s.get("cap", 3)),
                       overflow=s.get("overflow", ""), default=bool(s.get("default")),
                       aliases=tuple(s.get("aliases", ())))
            _SPACES[(zid, sid)] = sp
            ordered.append(sp)
        ordered.sort(key=lambda sp: (sp.order, sp.id))
        _BY_ZONE[zid] = tuple(ordered)
        defaults = [sp.id for sp in ordered if sp.default]
        if len(defaults) > 1:
            raise ValueError(f"zone {zid!r} declares multiple default spaces: {defaults}")


def loaded() -> bool:
    return bool(_SPACES)


def get(zone, space_id) -> "Space | None":
    return _SPACES.get((zone, space_id)) if zone and space_id else None


def for_zone(zone) -> tuple[Space, ...]:
    """The zone's spaces, in survey order. () for an unzoned / un-authored zone (→ spaceless render)."""
    return _BY_ZONE.get(zone, ())


def default_space(zone) -> "Space | None":
    for sp in _BY_ZONE.get(zone, ()):
        if sp.default:
            return sp
    return None


def resolve_space(zone, phrase) -> "str | None":
    """The space in `zone` a player means by `phrase`: an id/alias match first, else a distinctive
    word (>=4 letters) from a space's overflow phrase — so `look at debris` finds the floor whose
    overflow is "a scatter of smaller debris". None if nothing matches (the caller falls back: a look
    to a normal examine, a drop to the default space)."""
    if not zone or not phrase:
        return None
    q = phrase.strip().lower()
    if not q:
        return None
    layout = _BY_ZONE.get(zone, ())
    for sp in layout:
        if q == sp.id.lower() or any(q == a.lower() for a in sp.aliases):
            return sp.id
    for sp in layout:
        if sp.overflow and q in (w for w in sp.overflow.lower().split() if len(w) >= 4):
            return sp.id
    return None
