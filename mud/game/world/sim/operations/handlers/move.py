"""world.sim.operations.handlers.move — zone movement inside the Scene (DR-13a, §18). Pure.

`go/move/walk/head/approach/climb/enter <zone or thing>` steps ONE walk-edge, instantly (v1 —
durations/auto-pathing land with the P4 scheduler; `duration_minutes` is already plumbed).
Destination: a zone noun ("go to the cockpit"), or a thing's zone ("approach the radio"). Bare
`go` orients (lists where you can walk); an unwalkable destination gets a route redirect naming
the direction and first step. In an unzoned world the handler returns None → the generic redirect
(the one-zone compat rule).
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Event, EventKind, Resolution
from world.sim.operations._helpers import resolve_ref
from world.sim.space import direction, zones

VERBS = ("go", "move", "walk", "head", "approach", "climb", "enter")


def resolve_move(attempt, world, materials):
    actor_ent = world.get(attempt.actor)
    cur = (actor_ent.state or {}).get("zone") if actor_ent else None
    if cur is None or not zones.loaded():
        return None                                   # unzoned world → resolver redirects

    dest = _destination(attempt, world)
    if dest is None:
        neighbors = zones.walk_neighbors(cur)
        options = ", ".join(zones.get(z).name for z in neighbors if zones.get(z))
        return ActionResult(Resolution.REDIRECT, tier="op:move:orient",
                            narration=narrator.narrate("move.orient",
                                                       {"here": zones.get(cur).name,
                                                        "options": options or "nowhere"}))
    if dest == cur:
        return ActionResult(Resolution.REDIRECT, tier="op:move:already",
                            narration=narrator.narrate("move.already",
                                                       {"zone": zones.get(cur).name}))
    if dest not in zones.walk_neighbors(cur):
        step = _first_step(cur, dest)
        return ActionResult(Resolution.REDIRECT, tier="op:move:no_route",
                            narration=narrator.narrate("move.no_route",
                                                       {"zone": zones.get(dest).name,
                                                        "direction": direction.phrase(cur, dest) or "away",
                                                        "step": step}))
    eff = (effects.move_zone(attempt.actor, dest),)
    ev = (Event(EventKind.ACTIVITY_TICK, attempt.actor, loudness=0.25,
                data={"verb": "move", "from": cur, "to": dest}),)
    return ActionResult(Resolution.SUCCESS, effects=eff, events=ev, tier="op:move:step",
                        narration=narrator.narrate("move.arrive",
                                                   {"zone": zones.get(dest).name}))


def _destination(attempt, world):
    """The destination zone id: a zone noun in X or (relation) Y, or a thing's zone."""
    for ref in (attempt.X,) + tuple(attempt.Y or ()):
        if ref is None:
            continue
        if ref.entity_id.startswith("zone:"):
            return ref.entity_id[5:]
        ent, _part = resolve_ref(ref, world)
        z = (ent.state or {}).get("zone") if ent else None
        if z:
            return z
    return None


def _first_step(cur, dest):
    """The first walk-edge step of the shortest walk route cur→dest ('' if unroutable)."""
    seen, frontier = {cur}, [(cur, None)]
    while frontier:
        nxt = []
        for node, first in frontier:
            for n in zones.walk_neighbors(node):
                if n in seen:
                    continue
                f = first or n
                if n == dest:
                    z = zones.get(f)
                    return z.name if z else ""
                seen.add(n)
                nxt.append((n, f))
        frontier = nxt
    return ""
