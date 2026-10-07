"""world.sim.operations.handlers.open_op — open/close containers and caps (DR-24). Pure.

(`open_op` because `open` is a Python builtin; the verb is still "open".) `open X`: a jammed lid
wants leverage (pry it); a sealed cap unseals; a container opens. `close/shut X` mirrors. Opening
is what reveals contents to the world (the DR-24 reveal rule).
"""
from __future__ import annotations

from world.sim import effects, narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import resolve_ref

VERBS = ("open",)
CLOSE_VERBS = ("close", "shut")


def resolve_open(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    st = ent.state or {}
    if st.get("jammed"):
        return ActionResult(Resolution.REDIRECT, tier="op:open:jammed",
                            narration=narrator.narrate("open.jammed", {"target": ent.name}))
    if st.get("sealed"):
        return ActionResult(Resolution.SUCCESS, effects=(effects.set_attr(ent.id, "sealed", False),),
                            tier="op:open:unseal",
                            narration=narrator.narrate("open.unseal", {"target": ent.name}))
    if st.get("container"):
        if st.get("open"):
            return ActionResult(Resolution.REDIRECT, tier="op:open:already",
                                narration=narrator.narrate("open.already", {"target": ent.name}))
        return ActionResult(Resolution.SUCCESS, effects=(effects.set_attr(ent.id, "open", True),),
                            tier="op:open:open",
                            narration=narrator.narrate("open.open", {"target": ent.name}))
    return None                                     # nothing openable → the resolver redirects


def resolve_close(attempt, world, materials):
    ent, part = resolve_ref(attempt.X, world)
    if ent is None or part is not None:
        return None
    st = ent.state or {}
    if st.get("container") and st.get("open"):
        return ActionResult(Resolution.SUCCESS, effects=(effects.set_attr(ent.id, "open", False),),
                            tier="op:close:close",
                            narration=narrator.narrate("close.close", {"target": ent.name}))
    if st.get("container"):
        return ActionResult(Resolution.REDIRECT, tier="op:close:already",
                            narration=narrator.narrate("close.already", {"target": ent.name}))
    return None
