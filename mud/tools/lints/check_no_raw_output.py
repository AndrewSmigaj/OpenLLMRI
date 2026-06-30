#!/usr/bin/env python3
"""Gate: game events reach players ONLY through the message propagator, never raw msg_contents (DR-13).

The architecture replaces plain `room.msg_contents(...)` with a per-observer message **propagator**
(Event -> rendered by perception band x loudness). That seam is what makes the overlapping perception
zones (DR-13) a clean drop-in later instead of a rewrite of every output site. This gate enforces it:
no `.msg_contents(...)` in the shell (game/typeclasses, game/commands) outside the allowlisted propagator
module(s). Direct 1:1 `caller.msg(...)` replies (parse errors, prompts) are fine and not flagged.

AST-based (comments/docstrings ignored). Host-fast. The shell is currently stock/minimal, so this passes;
it bites the first time a P1 output site tries to broadcast around the propagator. When the propagator
module lands (P1/P3), add it to ALLOW.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCAN = [ROOT / "game" / "typeclasses", ROOT / "game" / "commands"]
# The propagator module(s), e.g. "game/typeclasses/rooms.py" or "game/commands/propagator.py" (P1/P3).
ALLOW = set()


def main() -> int:
    violations = []
    scanned = 0
    for base in SCAN:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            if str(path.relative_to(ROOT)) in ALLOW:
                continue
            scanned += 1
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr == "msg_contents"):
                    violations.append((path, node.lineno))

    if violations:
        print("NO-RAW-OUTPUT GATE FAILED — game events must go through the message propagator (DR-13):")
        for path, ln in violations:
            print(f"  {path.relative_to(ROOT)}:{ln}: raw .msg_contents() — route the Event through the propagator")
        print("  This is the seam that keeps overlapping perception zones a clean drop-in. Allowlist the")
        print("  propagator module in ALLOW once it lands.")
        return 1

    print(f"no-raw-output gate OK: {scanned} shell files, no raw msg_contents outside the propagator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
