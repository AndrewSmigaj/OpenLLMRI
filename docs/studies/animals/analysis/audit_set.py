"""Read-only audit of the animal set (data/sentence_sets/lexical/animals_kinship_v1.json), run before
its capture. It changes nothing: every problem is printed, fixes are made by hand in the set, and
the exit code is 1 while any check fails.

Beside the checks every single-word set gets (docs/studies/lexical_audit.py: shape, duplicates,
tokens, the capture's own reading, the prompt's own words, counts), the animals' own:
  1. each taxonomy has every field;
  2. the group follows from the class (Mammalia, Aves, Reptilia, Amphibia, Insecta, Arachnida;
     fish for any other chordate, all of them vertebrates; other_invertebrate for everything else);
  3. the families field (`categories.order`) is the order, else the family when the Catalogue of
     Life places the family in no order, else the name itself (a name above order rank);
  4. the taxonomy against the Catalogue of Life: the name is accepted at its rank, and phylum,
     class, order, family and genus equal COL's classification (blank where COL has none);
  5. at least 3 held-out families per group.

Usage, from the repo root:
  .venv/bin/python docs/studies/animals/analysis/audit_set.py            # everything
  .venv/bin/python docs/studies/animals/analysis/audit_set.py --no-col   # without the COL requests

Check 4 sends about 520 read-only requests to ChecklistBank's public matching service, one every
0.3 s (several minutes).
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
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

SET = ROOT / "data/sentence_sets/lexical/animals_kinship_v1.json"
COL_MATCH = "https://api.checklistbank.org/dataset/3LR/match/nameusage"
RANKS = ("phylum", "class", "order", "family", "genus")
CATEGORY_FIELDS = ("order", "habitat", "movement", "diet", "wild_or_domestic", "tokens")
TAXONOMY_FIELDS = ("name", "rank") + RANKS
GROUP_OF_CLASS = {"Mammalia": "mammal", "Aves": "bird", "Reptilia": "reptile", "Amphibia": "amphibian",
                  "Insecta": "insect", "Arachnida": "arachnid"}


def expected_group(tax):
    if tax["class"] in GROUP_OF_CLASS:
        return GROUP_OF_CLASS[tax["class"]]
    return "fish" if tax["phylum"] == "Chordata" else "other_invertebrate"


def expected_family(tax):
    return tax["order"] or tax["family"] or tax["name"]


def check_taxonomy(data, problems):
    for label, e in entries(data):
        word, tax = e["target_word"], e.get("taxonomy") or {}
        if set(tax) != set(TAXONOMY_FIELDS):
            problems.append(f"taxonomy: {word}'s taxonomy is {sorted(tax)}")
            continue
        if expected_group(tax) != label:
            problems.append(f"group: {word} is {label}, but its class {tax['class']!r} makes it {expected_group(tax)}")
        if e["categories"].get("order") != expected_family(tax):
            problems.append(f"families field: {word} has {e['categories'].get('order')!r}, "
                            f"the rule gives {expected_family(tax)!r}")


def col_match(name, rank):
    query = urllib.parse.urlencode({"scientificName": name, "rank": rank, "code": "ZOOLOGICAL"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(f"{COL_MATCH}?{query}", timeout=30) as reply:
                return json.loads(reply.read())
        except Exception as error:  # a slow or busy service: try again
            last = error
            time.sleep(2 + 3 * attempt)
    return {"type": f"error: {last}"}


def check_col(data, problems):
    """Each taxonomy against COL, field by field; fish must be vertebrates."""
    for label, e in entries(data):
        tax = e["taxonomy"]
        found = col_match(tax["name"], tax["rank"])
        usage = found.get("usage") or {}
        if found.get("type") not in ("exact", "variant") or usage.get("status") != "accepted" \
                or usage.get("rank") != tax["rank"]:
            problems.append(f"COL: {e['target_word']}: {tax['name']} at {tax['rank']} matched "
                            f"{found.get('type')} {usage.get('status')} {usage.get('label')} ({usage.get('rank')})")
        else:
            path = {c.get("rank"): c.get("name") for c in usage.get("classification") or []}
            if tax["rank"] in RANKS:
                path[tax["rank"]] = usage.get("name")
            for rank in RANKS:
                if (path.get(rank) or "") != tax[rank]:
                    problems.append(f"COL: {e['target_word']}: {rank} is {tax[rank]!r}, COL has {path.get(rank)!r}")
            if label == "fish" and path.get("subphylum") != "Vertebrata":
                problems.append(f"group: {e['target_word']} is a fish outside the vertebrates ({path.get('subphylum')})")
        time.sleep(0.3)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--no-col", action="store_true", help="skip the Catalogue of Life requests")
    args = parser.parse_args()
    data = json.loads(SET.read_text(encoding="utf-8"))
    problems = []
    check_shape(data, CATEGORY_FIELDS, problems)
    check_taxonomy(data, problems)
    check_capture(data, problems)
    if not args.no_col:
        check_col(data, problems)
    report_counts(data, ("habitat", "movement", "diet", "wild_or_domestic"), "order", problems)
    finish(problems)


if __name__ == "__main__":
    main()
