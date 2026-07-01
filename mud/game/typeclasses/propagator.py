"""game.typeclasses.propagator — the message propagator seam (DR-8/DR-13). Shell.

Routes each pure `Event` to the OTHER characters in the room, rendered per observer (P1 = the same
third-person line to everyone; DR-13 later renders by perception band). Uses per-observer `obj.msg(...)`
— **never `msg_contents`** (the check_no_raw_output gate). The actor is excluded (they already got the
first-person `ActionResult.narration`).
"""
from __future__ import annotations

from world.sim.contracts import EventKind

_VERB_PAST = {"cut": "saws at", "burn": "sets fire to", "pry": "levers at"}


def propagate(room, events, actor):
    if not room or not events:
        return
    observers = [o for o in room.contents if o is not actor and getattr(o, "account", None) is not None]
    if not observers:
        return
    line = "\n".join(_render(ev, actor) for ev in events if _render(ev, actor))
    if not line:
        return
    for obs in observers:
        obs.msg(line)


def _render(ev, actor) -> str:
    who = getattr(actor, "key", "someone")
    verb = ev.data.get("verb") if ev.data else None
    part = ev.data.get("part") if ev.data else None
    if ev.kind == EventKind.FIRE_STATE_CHANGE:
        return f"{who} sets something alight; smoke rises."
    if verb in _VERB_PAST:
        tail = f" the {part}" if part else " something"
        return f"{who} {_VERB_PAST[verb]}{tail}."
    return f"{who} does something."
