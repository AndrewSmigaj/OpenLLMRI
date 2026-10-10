"""Read-only audit of the object set (data/sentence_sets/lexical/objects_harm_v1.json), run before its
capture. It changes nothing: every problem is printed, fixes are made by hand in the set, and the
exit code is 1 while any check fails.

Beside the checks every single-word set gets (docs/studies/lexical_audit.py: shape, duplicates,
tokens, the capture's own reading, the prompt's own words, counts), the objects' own:
  1. how it harms is "none" exactly for the benign objects;
  2. every domain holds at least 2 objects, and the counts per domain and class are printed (whole
     domains are held out, so a domain that holds one class only is named).

Usage, from the repo root:
  .venv/bin/python docs/studies/objects_harm/analysis/audit_set.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lexical_audit import (  # noqa: E402
    ROOT,
    check_capture,
    check_shape,
    entries,
    finish,
    report_counts,
)

SET = ROOT / "data/sentence_sets/lexical/objects_harm_v1.json"
CATEGORY_FIELDS = ("domain", "harm", "tokens")


def check_objects(data, problems):
    domains = defaultdict(Counter)
    for label, e in entries(data):
        cats = e["categories"]
        if (cats["harm"] == "none") != (label == "benign"):
            problems.append(f"harm: {e['target_word']} is {label} with harm {cats['harm']!r}")
        domains[cats["domain"]][label] += 1
    labels = [g["label"] for g in data["groups"]]
    print(f"\n{'domain':20s}" + "".join(f"{lab:>10s}" for lab in labels))
    for domain, c in sorted(domains.items()):
        note = "  (one class only)" if len(c) == 1 else ""
        print(f"{domain:20s}" + "".join(f"{c[lab]:10d}" for lab in labels) + note)
        if sum(c.values()) < 2:
            problems.append(f"domain: {domain} holds {sum(c.values())} object")


def main():
    data = json.loads(SET.read_text(encoding="utf-8"))
    problems = []
    check_shape(data, CATEGORY_FIELDS, problems)
    check_objects(data, problems)
    check_capture(data, problems)
    report_counts(data, ("harm",), "domain", problems, min_families=1)
    finish(problems)


if __name__ == "__main__":
    main()
