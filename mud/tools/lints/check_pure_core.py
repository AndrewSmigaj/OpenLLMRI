#!/usr/bin/env python3
"""Gate: the pure functional core (game/world/sim/**) stays pure & deterministic (ADR-0003, DR-12).

Fails (exit 1) if any module under game/world/sim:
  (a) imports a FORBIDDEN module: evennia / django (boundary) or
      random / time / datetime / uuid / secrets (nondeterminism sources, DR-12); or
  (b) declares a dataclass field whose name leaks identity/wall-clock — contains `dbid`/`uuid` or is
      a datetime/timestamp (DR-12 forbids these in EntityState snapshots).

AST-based, so docstrings/comments that merely MENTION these words don't trip it. Host-fast, no deps.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SIM = ROOT / "game" / "world" / "sim"
FORBIDDEN_IMPORTS = {"evennia", "django", "random", "time", "datetime", "uuid", "secrets"}
FORBIDDEN_FIELD_TOKENS = ("dbid", "uuid", "datetime", "timestamp")


def top(name: str) -> str:
    return (name or "").split(".")[0]


def class_field_names(classdef: ast.ClassDef):
    """Yield (field_name, lineno) for annotated dataclass fields in a class body."""
    for stmt in classdef.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            yield stmt.target.id, stmt.lineno


def main() -> int:
    violations = []
    files = sorted(SIM.rglob("*.py"))
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if top(alias.name) in FORBIDDEN_IMPORTS:
                        violations.append((path, node.lineno, f"forbidden import: {alias.name}"))
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and top(node.module or "") in FORBIDDEN_IMPORTS:
                    violations.append((path, node.lineno, f"forbidden import: from {node.module}"))
            elif isinstance(node, ast.ClassDef):
                for fname, lineno in class_field_names(node):
                    low = fname.lower()
                    if any(tok in low for tok in FORBIDDEN_FIELD_TOKENS):
                        violations.append((path, lineno, f"forbidden field name '{fname}' (determinism, DR-12)"))

    if violations:
        print("PURE-CORE GATE FAILED — boundary/determinism violations under game/world/sim:")
        for path, lineno, what in violations:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {what}")
        print("  world/sim/** is the functional core: stdlib only; no evennia/django; no")
        print("  random/time/datetime/uuid; and no dbid/uuid/datetime field names (DR-12).")
        return 1

    print(f"pure-core gate OK: {len(files)} files under game/world/sim — no forbidden imports or field names.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
