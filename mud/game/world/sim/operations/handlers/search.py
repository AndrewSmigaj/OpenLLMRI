"""world.sim.operations.handlers.search — earn the contents (DR-24). Pure, deterministic.

`search/rummage/frisk X` reveals what X physically holds — always exactly what's there (no RNG;
DR-12). Worn layers are excluded from finds (a frisk sees the jacket already). `dig/burrow X`
is search for snow. A second search finds nothing else; a shut rigid lid wants opening first.
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import resolve_ref

VERBS = ("search", "rummage", "frisk")
DIG_VERBS = ("dig", "burrow")


def _articled(name: str) -> str:
    if name.lower().startswith(("the ", "a ", "an ", "some ")):
        return name
    return ("an " if name[:1].lower() in "aeiou" else "a ") + name


def _and_list(names) -> str:
    items = [_articled(n) for n in names]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def _reveal(attempt, world, ent, found_id, nothing_id, again_id):
    st = ent.state or {}
    if st.get("jammed") or (st.get("container") and "open" in st and not st.get("open")):
        return ActionResult(Resolution.REDIRECT, tier="op:search:shut",
                            narration=narrator.narrate("search.shut", {"target": ent.name}))
    if st.get("searched"):
        return ActionResult(Resolution.REDIRECT, tier="op:search:again",
                            narration=narrator.narrate(again_id, {"target": ent.name}))
    finds = st.get("contents") or []
    eff = (effects.set_attr(ent.id, "searched", True),)
    ev = (Event(EventKind.IMPACT, ent.id, loudness=0.2, data={"verb": "search"}),)
    if finds:
        return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:search:found",
                            narration=narrator.narrate(found_id, {"target": ent.name,
                                                                  "finds": _and_list(finds)}))
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:search:nothing",
                        narration=narrator.narrate(nothing_id, {"target": ent.name}))


def resolve_search(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    return _reveal(attempt, world, ent, "search.found", "search.nothing", "search.again")


def resolve_dig(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    mats = set(ent.materials or [])
    if not ({"snow", "ice"} & mats):
        return ActionResult(Resolution.REDIRECT, tier="op:dig:nothing",
                            narration=narrator.narrate("dig.nothing", {"target": ent.name}))
    return _reveal(attempt, world, ent, "dig.found", "dig.nothing_there", "dig.again")
