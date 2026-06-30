#!/usr/bin/env python3
"""Gate: only the single enforced writer (apply()) mutates Evennia Attributes/Tags (DR-10).

AST-based scan of the Evennia shell (game/typeclasses, game/commands) for raw state writes:
  X.db.<a> = ... / X.ndb.<a> = ...        (assignment to a .db/.ndb attribute)
  X.attributes.add/remove(...)            X.tags.add/remove(...)
Examples in comments/docstrings are ignored (AST). The designated single-writer module(s) are
allowlisted in ALLOW (relative paths), added when apply() lands (roadmap P1). The shell is currently
stock/minimal, so this passes; the gate guards the apply() choke-point as the shell grows. Host-fast.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCAN = [ROOT / "game" / "typeclasses", ROOT / "game" / "commands"]
# Relative paths of the single-writer module(s); add the apply() host when it lands (roadmap P1).
ALLOW = set()  # e.g. {"game/typeclasses/objects.py"}


def is_db_attr_target(node: ast.AST) -> bool:
    # X.db.<name> = ...  or  X.ndb.<name> = ...
    return (isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Attribute)
            and node.value.attr in ("db", "ndb"))


def is_handler_write(node: ast.AST):
    # X.attributes.add/remove(...)  or  X.tags.add/remove(...)
    if (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in ("add", "remove")
            and isinstance(node.func.value, ast.Attribute)
            and node.func.value.attr in ("attributes", "tags")):
        return f".{node.func.value.attr}.{node.func.attr}()"
    return None


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
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AugAssign):
                    targets = [node.target]
                for t in targets:
                    if is_db_attr_target(t):
                        violations.append((path, node.lineno, "raw .db/.ndb attribute write"))
                hw = is_handler_write(node)
                if hw:
                    violations.append((path, node.lineno, f"{hw} write"))

    if violations:
        print("NO-RAW-WRITES GATE FAILED — state must change only via apply() (DR-10):")
        for path, lineno, what in violations:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {what}")
        print("  Route it through an Effect + apply(), or allowlist the single-writer module in ALLOW.")
        return 1

    print(f"no-raw-writes gate OK: {scanned} shell files, no raw Attribute/Tag writes outside apply().")
    return 0


if __name__ == "__main__":
    sys.exit(main())
