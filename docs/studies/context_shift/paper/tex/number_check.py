#!/usr/bin/env python3
"""Number checks for the paper draft.

Two checks, both over the numerals in a section's prose, tables, and the captions of
the figures it cites.

  trace         every numeral in the current draft appears in the findings record
                (findings/FINDINGS_FINAL.md, findings/FINDINGS_AND_ANALYSIS_v2.md) or in
                the allowlist (tex/number_allowlist.md, which records post-freeze and
                script-output values with their source).
  preservation  every numeral in the frozen pre-rewrite draft (paper/draft_v2/) still
                appears in the current draft. A numeral that moved to another section,
                a table, or a caption counts as preserved; the report says where it
                went. A numeral found nowhere is reported as LOST.

Usage:
    number_check.py trace [SECTION ...]          default: all sections + captions
    number_check.py preservation [SECTION ...]   default: all sections
    number_check.py all

SECTION is a basename such as 03_results_R1-R6.md.

What is a numeral: a token with digits, optionally signed, with commas or a decimal
point, not attached to letters (identifiers such as L4 or s13 are skipped), not a
section, figure, table, box, appendix, rule, or item number, and not a four-digit
year. Matching is by digit string: "+2.16" matches "2.16" and "2,880" matches "2880".
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
PAPER = HERE.parent
STUDY = PAPER.parent
DRAFT = PAPER / "draft"
FROZEN = PAPER / "draft_v2"
CAPTIONS = DRAFT / "captions.md"
ALLOWLIST = HERE / "number_allowlist.md"
RECORD = [STUDY / "findings" / "FINDINGS_FINAL.md",
          STUDY / "findings" / "FINDINGS_AND_ANALYSIS_v2.md"]

REF_WORDS = r"(?:§|Section|Sections|Figure|Figures|Fig\.|Figs\.|Table|Tables|Box|Appendix|Item|Items|Rule|rule|Step|step|Round|round|Correction|correction)\s*"
NUM = re.compile(r"(?<![\w.])[+−-]?(\d[\d,]*(?:\.\d+)?)(?![\w])")


def strip(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^#.*$", " ", text, flags=re.M)  # headings
    text = re.sub(r"\b\d{4}-\d\d-\d\d\b", " ", text)  # dates
    text = re.sub(REF_WORDS + r"[\dA-Z]+(?:\.\d+)?", " ", text)
    text = re.sub(r"\b(19|20)\d\d\b", " ", text)
    text = re.sub(r"\[CITE[^\]]*\]", " ", text)
    return text


def numerals(text):
    """Return list of (digit_string, context) in order of appearance."""
    out = []
    text = strip(text)
    for m in NUM.finditer(text):
        s = m.group(1).replace(",", "")
        ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
        out.append((s, ctx))
    return out


def digit_set(text):
    return {s for s, _ in numerals(text)}


def record_digits():
    text = "".join(p.read_text() for p in RECORD if p.exists())
    if ALLOWLIST.exists():
        text += ALLOWLIST.read_text()
    # record: match any digit string, attached or not
    return set(x.replace(",", "") for x in re.findall(r"\d[\d,]*(?:\.\d+)?", text))


def sections(names):
    if names:
        return [DRAFT / n for n in names]
    return sorted(DRAFT.glob("0*.md"))


def trace(names):
    rec = record_digits()
    files = sections(names)
    if not names or "captions.md" in names:
        files = [f for f in files if f.name != "captions.md"] + ([CAPTIONS] if CAPTIONS.exists() else [])
    bad = 0
    for f in files:
        misses = [(s, c) for s, c in numerals(f.read_text()) if s not in rec]
        print(f"\n[trace] {f.name}: {len(misses)} untraced")
        seen = set()
        for s, c in misses:
            if s in seen:
                continue
            seen.add(s)
            print(f"   {s:>10}   …{c.strip()}…")
        bad += len(seen)
    print(f"\n[trace] RESULT: {'PASS' if bad == 0 else f'FLAG — {bad} untraced numerals'}")
    return bad == 0


def preservation(names):
    if not FROZEN.exists():
        print("[preservation] no draft_v2/ — nothing to compare"); return True
    new_all = {}
    for f in list(DRAFT.glob("0*.md")) + ([CAPTIONS] if CAPTIONS.exists() else []):
        new_all[f.name] = digit_set(f.read_text())
    union = set().union(*new_all.values()) if new_all else set()
    lost = 0
    olds = sorted(FROZEN.glob("0*.md")) + [FROZEN / "captions.md"] if not names else [FROZEN / n for n in names]
    for old in olds:
        new = new_all.get(old.name, set())
        old_nums = numerals(old.read_text())
        seen = set()
        moved, gone = [], []
        for s, c in old_nums:
            if s in seen or s in new:
                continue
            seen.add(s)
            if s in union:
                where = [k for k, v in new_all.items() if s in v]
                moved.append((s, where))
            else:
                gone.append((s, c))
        print(f"\n[preservation] {old.name}: {len(moved)} moved, {len(gone)} LOST")
        for s, where in moved:
            print(f"   moved   {s:>10}   → {', '.join(where)}")
        for s, c in gone:
            print(f"   LOST    {s:>10}   …{c.strip()}…")
        lost += len(gone)
    print(f"\n[preservation] RESULT: {'PASS' if lost == 0 else f'FLAG — {lost} numerals lost'}")
    return lost == 0


def main(argv):
    if not argv:
        print(__doc__); return 2
    cmd, names = argv[0], argv[1:]
    ok = True
    if cmd in ("trace", "all"):
        ok &= trace(names)
    if cmd in ("preservation", "all"):
        ok &= preservation(names)
    if cmd not in ("trace", "preservation", "all"):
        print(__doc__); return 2
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
