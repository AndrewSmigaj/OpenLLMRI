#!/usr/bin/env python3
"""Gate: only the single enforced writer (apply()) mutates Evennia Attributes/Tags (DR-10).

AST-based scan of the Evennia shell (game/typeclasses, game/commands) for raw state writes:
  X.db.<a> = ... / X.ndb.<a> = ...        assignment to a .db/.ndb attribute
  X.db.<a>[k] = ... / X.ndb.<a>[k] = ...  subscript write into a .db/.ndb attribute
  X.db.<a>.append/extend/update/... (...) in-place mutation of a .db/.ndb SaverList/SaverDict
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
ALLOW = {"game/typeclasses/apply.py"}  # THE effects-centric single writer (DR-10)

# in-place mutators on a SaverList/SaverDict held in a .db/.ndb attribute
MUTATORS = {"append", "extend", "insert", "pop", "remove", "clear", "update",
            "setdefault", "sort", "reverse", "add", "discard", "popitem", "__setitem__"}


def chain_touches_db(node: ast.AST) -> bool:
    """True if the attribute/subscript chain rooted at `node` passes through a `.db`/`.ndb` access."""
    while isinstance(node, (ast.Attribute, ast.Subscript)):
        if isinstance(node, ast.Attribute) and node.attr in ("db", "ndb"):
            return True
        node = node.value
    return False


def violations_in(path: pathlib.Path):
    out = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        for t in targets:
            if (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Attribute)
                    and t.value.attr in ("db", "ndb")):
                out.append((node.lineno, "raw .db/.ndb attribute write"))
            elif isinstance(t, ast.Subscript) and chain_touches_db(t.value):
                out.append((node.lineno, "subscript write into a .db/.ndb attribute"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            f = node.func
            if (f.attr in ("add", "remove") and isinstance(f.value, ast.Attribute)
                    and f.value.attr in ("attributes", "tags")):
                out.append((node.lineno, f".{f.value.attr}.{f.attr}() write"))
            elif f.attr in MUTATORS and chain_touches_db(f.value):
                out.append((node.lineno, f"in-place .{f.attr}() mutation of a .db/.ndb value"))
    return out


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
            for lineno, what in violations_in(path):
                violations.append((path, lineno, what))

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
