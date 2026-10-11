"""Read-only audit of the animal ontology set (data/sentence_sets/lexical/animals_ontology_v1.json), run
before its capture. It changes nothing: every problem is printed, fixes are made by hand in the set,
and the exit code is 1 while any check fails.

Beside the checks every single-word set gets (docs/studies/lexical_audit.py: shape, every value one
of its axis's values, duplicates, tokens, the capture's own reading, the prompt's own words), this
set's own:
  1. the earlier set is copied unchanged: the same names in the same order, and each item's group,
     target word, taxonomy and six earlier categories equal animals_kinship_v1's, with the eight
     new categories after them;
  2. counts per group for every axis, and how each axis crosses the others (Cramér's V for every
     pair, so the ways the design ties together, such as covering and descent, are on record);
  3. each taxonomy against its common names in the Catalogue of Life: the taxon is matched at its
     rank, its English vernacular names are fetched, and an animal whose names don't contain its
     word is listed for a look by hand (bee once matched a moth genus). COL has no English names
     for many higher taxa; those are counted, not flagged. This check prints a review list and
     never fails the audit: a name can be right and still differ ("cavy" against "guinea pig").

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/audit_set.py            # everything
  .venv/bin/python docs/studies/animal_ontology/analysis/audit_set.py --no-col   # without COL

Check 3 sends about 1,050 read-only requests to ChecklistBank's public service (a match and the
vernacular names per animal), one every 0.3 s: about ten minutes.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lexical_audit import (  # noqa: E402
    ROOT,
    check_capture,
    check_shape,
    entries,
    finish,
    report_counts,
)

SET = ROOT / "data/sentence_sets/lexical/animals_ontology_v1.json"
EARLIER = ROOT / "data/sentence_sets/lexical/animals_kinship_v1.json"
COL = "https://api.checklistbank.org/dataset/3LR"
EARLIER_FIELDS = ("order", "habitat", "movement", "diet", "wild_or_domestic", "tokens")
NEW_FIELDS = ("kind", "covering", "size", "legs", "where_met", "relation", "danger", "feeling")
CATEGORY_FIELDS = EARLIER_FIELDS + NEW_FIELDS
CROSSED = ("group",) + EARLIER_FIELDS[1:] + NEW_FIELDS  # every axis but the order (171 values)


def check_copy(data: Dict[str, Any], earlier: Dict[str, Any], problems: List[str]) -> None:
    """The earlier set's names, order, groups, taxonomies and categories, unchanged."""
    new_items = list(entries(data))
    old_items = list(entries(earlier))
    if len(new_items) != len(old_items):
        problems.append(f"copy: {len(new_items)} items, the earlier set has {len(old_items)}")
    if [g["label"] for g in data["groups"]] != [g["label"] for g in earlier["groups"]]:
        problems.append("copy: the groups differ from the earlier set's")
    for (label, e), (old_label, o) in zip(new_items, old_items):
        word = e["target_word"]
        for key in ("text", "group", "target_word", "taxonomy"):
            if e.get(key) != o.get(key):
                problems.append(f"copy: {word}'s {key} differs from the earlier set's ({o.get(key)!r})")
        if label != old_label:
            problems.append(f"copy: {word} is in group {label}, the earlier set has {old_label}")
        cats = e.get("categories") or {}
        if {k: cats.get(k) for k in EARLIER_FIELDS} != o.get("categories"):
            problems.append(f"copy: {word}'s earlier categories differ from the earlier set's")
        if list(cats) != list(CATEGORY_FIELDS):
            problems.append(f"copy: {word}'s categories are in the order {list(cats)}")


def cramers_v(a: List[str], b: List[str]) -> float:
    """How strongly two labellings go together: 0 independent, 1 one fixes the other."""
    rows, cols = sorted(set(a)), sorted(set(b))
    table = np.zeros((len(rows), len(cols)))
    for x, y in zip(a, b):
        table[rows.index(x), cols.index(y)] += 1
    n = table.sum()
    expected = table.sum(1, keepdims=True) @ table.sum(0, keepdims=True) / n
    chi2 = float(((table - expected) ** 2 / expected).sum())
    k = min(len(rows), len(cols)) - 1
    return float(np.sqrt(chi2 / (n * k))) if k > 0 else 0.0


def report_crossings(data: Dict[str, Any]) -> None:
    values = {axis: [] for axis in CROSSED}
    for label, e in entries(data):
        for axis in CROSSED:
            values[axis].append(label if axis == "group" else e["categories"][axis])
    print("\nHow each axis crosses the others (Cramér's V; 0 independent, 1 one fixes the other):")
    short = [a[:8] for a in CROSSED]
    print(f"  {'':17s}" + "".join(f"{s:>9s}" for s in short))
    for a in CROSSED:
        row = []
        for b in CROSSED:
            row.append("        ." if a == b else f"{cramers_v(values[a], values[b]):9.2f}")
        print(f"  {a:17s}" + "".join(row))
    strongest = sorted(((cramers_v(values[a], values[b]), a, b) for a, b in combinations(CROSSED, 2)),
                       reverse=True)[:8]
    print("  strongest pairs: " + "; ".join(f"{a} and {b} {v:.2f}" for v, a, b in strongest))


def col_get(path: str, params: Optional[Dict[str, str]] = None) -> Any:
    url = f"{COL}/{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    last: Exception = RuntimeError("no attempt")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as reply:
                return json.loads(reply.read())
        except Exception as error:  # a slow or busy service: try again
            last = error
            time.sleep(2 + 3 * attempt)
    return {"error": str(last)}


def name_holds(word: str, names: List[str]) -> bool:
    """Whether a common name holds the word: as a word, a plural, or inside the name written
    without spaces or hyphens ("honeybee" in "western honey bee")."""
    for name in names:
        low = name.lower()
        words = re.findall(r"[a-z]+", low)
        compact = re.sub(r"[^a-z]", "", low)
        if word in words or word + "s" in words or word + "es" in words or word in compact:
            return True
    return False


def check_common_names(data: Dict[str, Any]) -> Tuple[List[str], List[str], int]:
    """Each taxon's English vernacular names against the animal's word. Returns the names that
    differ (for a look by hand), the taxa COL couldn't match, and how many matched."""
    differ, unmatched, held, no_names = [], [], 0, 0
    for label, e in entries(data):
        word, tax = e["target_word"], e["taxonomy"]
        found = col_get("match/nameusage", {"scientificName": tax["name"], "rank": tax["rank"],
                                            "code": "ZOOLOGICAL"})
        usage = found.get("usage") or {}
        time.sleep(0.3)
        if not usage.get("id") or usage.get("rank") != tax["rank"]:
            unmatched.append(f"{word}: {tax['name']} ({tax['rank']}) matched {found.get('type')} "
                             f"{usage.get('label')} ({usage.get('rank')})")
            continue
        names = col_get(f"taxon/{usage['id']}/vernacular")
        time.sleep(0.3)
        english = sorted({v["name"] for v in names if isinstance(v, dict)
                          and (v.get("language") or "").lower() in ("eng", "en")}) \
            if isinstance(names, list) else []
        if not english:
            no_names += 1
        elif name_holds(word, english):
            held += 1
        else:
            differ.append(f"{word} ({label}): {tax['name']} ({tax['rank']}) is called "
                          + "; ".join(english[:6]) + ("…" if len(english) > 6 else ""))
    print(f"\nCommon names: {held} hold the word, {len(differ)} differ, {no_names} have no English "
          f"names in COL, {len(unmatched)} unmatched")
    return differ, unmatched, no_names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--no-col", action="store_true", help="skip the Catalogue of Life requests")
    args = parser.parse_args()
    data = json.loads(SET.read_text(encoding="utf-8"))
    earlier = json.loads(EARLIER.read_text(encoding="utf-8"))
    problems: List[str] = []
    check_shape(data, CATEGORY_FIELDS, problems)
    check_copy(data, earlier, problems)
    check_capture(data, problems)
    report_counts(data, NEW_FIELDS + EARLIER_FIELDS[1:5], "order", problems)
    report_crossings(data)
    totals = {axis: Counter(e["categories"][axis] for _, e in entries(data)) for axis in NEW_FIELDS}
    print("\nValues overall: " + "; ".join(f"{axis}: " + ", ".join(f"{v} {n}" for v, n in c.most_common())
                                           for axis, c in totals.items()))
    if not args.no_col:
        differ, unmatched, _ = check_common_names(data)
        print("\nFor a look by hand (the common names don't contain the word):")
        for line in differ:
            print("  " + line)
        for line in unmatched:
            print("  unmatched: " + line)
    finish(problems)


if __name__ == "__main__":
    main()
