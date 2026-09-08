"""world.sim.operations.handlers.make_op — the `make` TEACHING verb (parser tolerance, 2026-09-07). Pure.

`make fire` / `build a shelter` / `start a fire with sticks` never succeeds by itself — the world has
no recipes (GDD §30: goals are conditions, not verb sequences). It answers with what the thing IS
MADE OF, physically (the hinting policy: name shapes and properties, never steps): "A fire wants
something fine and dry that catches, small dry wood to build it, bigger fuel to keep it — and a way
to light it." Named a tool (`make fire with sticks`), it asks the limited question: "How do you mean
to use the sticks?" Content lives in the scenario responses (`make.<thing>`, `make._`, `make.with`).
"""
from __future__ import annotations

import re

from world.sim import narrator
from world.sim.contracts import ActionResult, Resolution
from world.sim.parser.vocab import ARTICLES

VERBS = ("make", "build", "create", "craft", "construct", "assemble", "improvise", "fashion", "rig",
         "start", "begin", "erect", "prepare")


def _words(raw: str):
    toks = re.sub(r"[^\w\s]", " ", (raw or "").lower()).split()
    return [t for t in toks[1:] if t not in ARTICLES]


def resolve_make(attempt, world, materials):
    words = _words(attempt.raw)
    tool = None
    if "with" in words:
        i = words.index("with")
        tool = " ".join(words[i + 1:]) or None
        words = words[:i]
    if "using" in words:
        i = words.index("using")
        tool = tool or (" ".join(words[i + 1:]) or None)
        words = words[:i]
    thing = None
    for w in words:
        if narrator.get(f"make.{w}") is not None:
            thing = w
            break
    if thing is None:
        thing = words[-1] if words else "that"
    line = narrator.get(f"make.{thing}")
    if line is None:
        line = narrator.narrate("make._", {"thing": thing})
    if tool:
        line = f"{line} {narrator.narrate('make.with', {'named': tool, 'thing': thing})}"
    return ActionResult(Resolution.REDIRECT, tier=f"op:make:{thing if narrator.get(f'make.{thing}') else 'unknown'}",
                        narration=line)
