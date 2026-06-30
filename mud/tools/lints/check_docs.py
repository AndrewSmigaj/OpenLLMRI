#!/usr/bin/env python3
"""Gate: live docs don't regress to a decision we already locked (consistency / anti-drift).

The mechanical version of "did you check the docs?" — it forbids known STALE patterns from re-appearing
in the authoritative / always-loaded docs, so drift can't creep back silently.

Scans Markdown under the repo EXCEPT historical / being-revised files (see EXCLUDE). A forbidden pattern
on a line is a violation UNLESS the line also carries an ALLOW token (it's explicitly talking about the
rejected/old thing — e.g. "rejected", "retired", "archived", "superseded", "no longer").

Forbidden (each = a locked decision someone tried to undo):
  mass_kg            -> the contract field is mass_g (integer grams)            (DR-11)
  CMD_NOMATCH        -> runtime-LLM fallback; runtime is deterministic          (DR-02)
  event-driven       -> the clock is a continuously running real-time clock     (DR-14)
  "Pass <n>"         -> old roadmap numbering; phases are P0-P7
  a Markdown link to design.md presented as authoritative (it's the archived seed -> link GDD.md)

Host-fast, stdlib only. Run by `make lint` / `make verify` / the Stop hook / the pre-commit hook.
As each pre-v4 guide is rewritten (P1+), drop it from EXCLUDE_FILES so it's enforced too.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Historical record + the archived seed + the bannered pre-v4 guides are intentionally NOT enforced.
EXCLUDE_DIRS = ("docs/investigation/", "docs/architecture/review/", "docs/proposals/")
EXCLUDE_FILES = {
    "docs/scenarios/whiteout/design.md",
    "docs/scenarios/_TEMPLATE.md",
    "seed.md",
    "docs/guides/authoring-actions.md",
    "docs/guides/authoring-objects.md",
    "docs/guides/authoring-workflows.md",
    "docs/guides/validation-rules.md",
}

ALLOW = ("reject", "retire", "remov", "archiv", "supersed", "stale", "pre-v4", "deprecat",
         "legacy", "historical", "former", "replaced", "instead of", "rather than", "no longer",
         "not authoritative", "old ", "older", "previous", "we said no", "used to", "build-time",
         "build time", "forbid", "regress", "this gate", "doc-consistency")

PATTERNS = [
    (re.compile(r"\bmass_kg\b"), "stale field name — the contract is `mass_g` (integer grams), DR-11"),
    (re.compile(r"\bCMD_NOMATCH\b"), "runtime-LLM fallback — removed; runtime is deterministic (DR-02)"),
    (re.compile(r"intent[- ]fallback", re.I), "runtime-LLM intent-fallback — retired; runtime is deterministic (DR-02)"),
    (re.compile(r"event-driven", re.I), "the clock is a running real-time clock; event-driven was rejected (DR-14)"),
    (re.compile(r"\bPass\s+\d"), "old roadmap numbering — the phases are P0–P7 (slice-first roadmap)"),
    (re.compile(r"\]\([^)]*\bdesign\.md\b"), "links `design.md` as authoritative — it's the archived seed; link GDD.md"),
]


def is_excluded(rel: str) -> bool:
    return rel in EXCLUDE_FILES or any(rel.startswith(d) for d in EXCLUDE_DIRS)


def main() -> int:
    violations = []
    md_files = [p for p in ROOT.rglob("*.md") if not is_excluded(str(p.relative_to(ROOT)))]
    for path in sorted(md_files):
        rel = str(path.relative_to(ROOT))
        lines = path.read_text(encoding="utf-8").splitlines()
        low = [ln.lower() for ln in lines]
        for i, line in enumerate(lines):
            # The allow-token check spans this line +/- 1: Markdown wrapping can split a keyword from
            # its "rejected"/"retired"/"build-time" context onto an adjacent source line.
            ctx = " ".join(low[max(0, i - 1): i + 2])
            if any(tok in ctx for tok in ALLOW):
                continue
            for pat, msg in PATTERNS:
                if pat.search(line):
                    violations.append((rel, i + 1, msg, line.strip()))

    if violations:
        print("DOC-CONSISTENCY GATE FAILED — a live doc regressed to a locked decision:")
        for rel, i, msg, src in violations:
            print(f"  {rel}:{i}: {msg}")
            print(f"      > {src[:100]}")
        print("  Fix the doc, or — if it's intentionally describing the OLD thing — add a word like")
        print("  'rejected' / 'retired' / 'archived' so the gate knows it isn't a regression.")
        return 1

    print(f"doc-consistency gate OK: {len(md_files)} live docs, no regressions to locked decisions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
