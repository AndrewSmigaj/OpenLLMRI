"""world.sim.operations.handlers.talk — the soft social catch (no NPCs by design, §3.3). Pure.

`talk/ask/tell [to] X`: the pilot is scripted and dead, not an AI — the answer is honest silence.
Living characters are PLAYERS (talk to them with `say`). Objects have nothing to say. All
REDIRECTs, no effects; `say/whisper/call/shout` remain the real speech channel (§15).
"""
from __future__ import annotations

from world.sim import narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import resolve_ref

VERBS = ("talk", "ask", "tell")


def resolve_talk(attempt, world, materials):
    ref = attempt.X or (attempt.Y[0] if attempt.Y else None)
    ent, _part = resolve_ref(ref, world)
    if ent is None:
        return ActionResult(Resolution.REDIRECT, tier="op:talk:air",
                            narration=narrator.narrate("talk.air", {}))
    st = ent.state or {}
    if st.get("dead"):
        return ActionResult(Resolution.REDIRECT, tier="op:talk:dead",
                            narration=narrator.narrate("talk.dead", {"target": ent.name}))
    if "flesh" in (ent.materials or []):
        return ActionResult(Resolution.REDIRECT, tier="op:talk:no_answer",
                            narration=narrator.narrate("talk.no_answer", {"target": ent.name}))
    return ActionResult(Resolution.REDIRECT, tier="op:talk:inanimate",
                        narration=narrator.narrate("talk.inanimate", {"target": ent.name}))
