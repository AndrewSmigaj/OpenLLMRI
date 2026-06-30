#!/usr/bin/env python3
"""Gate: the pure functional core (game/world/sim/**) stays pure & deterministic (ADR-0003, DR-12).

Fails (exit 1) if any module under game/world/sim imports a FORBIDDEN module:
  - evennia / django                              (the functional-core boundary, ADR-0003)
  - random / time / datetime / uuid / secrets     (nondeterminism sources, DR-12)

AST-based, so docstrings/comments that merely MENTION these words don't trip it. Host-fast, no deps.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]          # tools/lints/ -> repo root
SIM = ROOT / "game" / "world" / "sim"
FORBIDDEN = {"evennia", "django", "random", "time", "datetime", "uuid", "secrets"}


def top(name: str) -> str:
    return (name or "").split(".")[0]


def main() -> int:
    violations = []
    files = sorted(SIM.rglob("*.py"))
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if top(alias.name) in FORBIDDEN:
                        violations.append((path, node.lineno, f"import {alias.name}"))
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and top(node.module or "") in FORBIDDEN:
                    violations.append((path, node.lineno, f"from {node.module} import ..."))

    if violations:
        print("PURE-CORE GATE FAILED — forbidden imports under game/world/sim (boundary/determinism):")
        for path, lineno, what in violations:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {what}")
        print("  world/sim/** is the functional core: stdlib only; no evennia/django; no "
              "random/time/datetime/uuid (determinism, DR-12).")
        return 1

    print(f"pure-core gate OK: {len(files)} files under game/world/sim, no forbidden imports.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
