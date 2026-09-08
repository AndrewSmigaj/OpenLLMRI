"""world.sim.operations.handlers.use — the `use` TEACHING verb (parser tolerance, 2026-09-07). Pure.

`use X on Y` is what newcomers and agents type first. It is never free success: it dispatches through
X's CAPABILITIES (authored or derived, DR-26) to the real verb — an edge cuts, a flame lights, leverage
pries, cordage ties, a sheet wraps, heft breaks — runs that handler on the identical pipeline, and
ECHOES the verb it chose ("(That's 'cut cover with shard'.)") so the guess becomes a lesson (Aaron
Reed's Small Kindnesses `USE`). `use X` alone says what X affords (≤2 verbs). `use X to VERB Y` never
reaches here: the parser rewrites it to `VERB Y with X`. Returns None if X isn't a thing.
"""
from __future__ import annotations

from dataclasses import replace

from world.sim import narrator
from world.sim.contracts import ActionAttempt, ActionResult, Resolution
from world.sim.operations._helpers import capability, name_of, resolve_ref

VERBS = ("use", "utilize", "employ", "operate", "wield")
# capability → the verb it affords, in the order a survivor would reach for them
_AFFORDS = (("edge", "cut"), ("flame", "burn"), ("ignition", "light"), ("leverage", "pry"),
            ("cordage", "tie"), ("sheet", "wrap"), ("heft", "break"), ("point", "cut"))
_MIN = 0.2


def _affordances(ref, world, materials):
    out = []
    for axis, verb in _AFFORDS:
        if capability(ref, world, axis, materials) >= _MIN and verb not in [v for _, v in out]:
            out.append((axis, verb))
    return out


def resolve_use(attempt, world, materials):
    from world.sim.operations.registry import handler_for      # local: the registry imports this module
    x_ent, _ = resolve_ref(attempt.X, world)
    if x_ent is None:
        return None
    affords = _affordances(attempt.X, world, materials)
    y_ref = attempt.Y[0] if attempt.Y else None
    y_name = name_of(y_ref, world) if y_ref is not None else None

    if y_ref is None or y_name is None:
        if not affords:
            return ActionResult(Resolution.REDIRECT, tier="op:use:nothing",
                                narration=narrator.narrate("use.nothing", {"tool": x_ent.name}))
        verbs = " or ".join(v for _, v in affords[:2])
        return ActionResult(Resolution.REDIRECT, tier="op:use:what",
                            narration=narrator.narrate("use.what", {"tool": x_ent.name, "verbs": verbs,
                                                                    "axis": affords[0][0]}))
    if not affords:
        return ActionResult(Resolution.REDIRECT, tier="op:use:nothing",
                            narration=narrator.narrate("use.nothing", {"tool": x_ent.name}))
    # the flame verb depends on the target: light kindling/tinder, burn a thing outright
    for axis, verb in affords:
        real = ActionAttempt(actor=attempt.actor, verb=verb, X=y_ref, relation=None, Y=None,
                             tool=attempt.X, raw=attempt.raw)
        handler = handler_for(verb)
        r = handler(real, world, materials) if handler else None
        if r is None and verb == "burn":
            r = handler_for("light")(real, world, materials)
            verb = "light"
        if r is None:
            continue
        echo = narrator.narrate("use.echo", {"verb": verb, "target": y_name, "tool": x_ent.name})
        return replace(r, narration=f"{echo} {r.narration}".strip(), tier=f"use>{r.tier}")
    return ActionResult(Resolution.REDIRECT, tier="op:use:no_fit",
                        narration=narrator.narrate("use.no_fit", {"tool": x_ent.name, "target": y_name,
                                                                  "verb": affords[0][1]}))
