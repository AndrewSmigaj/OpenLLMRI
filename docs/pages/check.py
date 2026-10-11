"""Checks for the two documents and their requirements (DESIGN.md L26.2).

Usage (from the repo root):
  .venv/bin/python docs/pages/check.py                  every check
  .venv/bin/python docs/pages/check.py marks            one check by name
  .venv/bin/python docs/pages/check.py quotes --words F  with F a file of Andrew's stored words,
                                                         exported from the pages' stores and kept
                                                         outside the repo

The checks:
- requirements: the list's shape: every field present, statuses known, ids unique, every
  replaced_by naming a requirement that exists.
- marks: every line of DESIGN.md (at the list's snapshot commit) that carries a mark is cited by
  some requirement's `from`, and every cited line carries a mark, so nothing was lost in the move.
- citations: every requirement id the documents cite exists, and none is retired, except in the
  "Rejected and retired" and "Decision log" sections, which are history.
- coverage: once both documents exist, every requirement that isn't retired is cited by one.
- wording: no retired wording in the documents, outside those history sections and outside quotes.
- references: every link between the documents, and every requirement's `section`, names a
  section that exists.
- quotes: no repo file holds a run of eight or more of Andrew's own words.

Exit status 1 when a check fails.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / "docs/design/requirements.yaml"
DOCUMENTS = {"design.md": ROOT / "docs/design/design.md", "plan.md": ROOT / "docs/architecture/plan.md"}
FIELDS = {"id", "text", "status", "dates", "source", "from", "section"}
STATUSES = {"decided", "idea", "view", "proposed", "open", "built", "retired"}
MARK = re.compile(r"\[(?:Decided|Andrew's\s+idea|Andrew's\s+view|Built|Proposed|Open|approved)\b")
TABLE_MARK = re.compile(r"^\|.*\|\s*Decided\b")  # a status cell in a table, as in DESIGN.md E8
ID = r"[A-Z]+-\d+"
CITE_ITEM = rf"{ID}(?: to {ID})?"  # one id, or a range of one area's ids
CITATION = re.compile(rf"\[({CITE_ITEM}(?:,\s*{CITE_ITEM})*)\]")
LINK = re.compile(r"\]\((design\.md|plan\.md)#([a-z0-9-]+)\)")
RETIRED_SECTION = re.compile(r"^#+ .*(Rejected and retired|Decision log)", re.I)  # history
# Wording the design has retired, with what replaced it. Matched as whole words, any case.
RETIRED_WORDING: Dict[str, str] = {
    "basin": "node (a lens's cluster at one layer)",
    "kinship": "descent (the animal ontology's first way)",
    "NF4": "MXFP4 experts with fp16 elsewhere",
    "build-schema": "lens builds as background jobs",
    "Temporal Analysis": "Study's timelines and Watch",
}


def load_requirements() -> dict:
    return yaml.safe_load(REQUIREMENTS.read_text(encoding="utf-8"))


def check_requirements(data: dict) -> List[str]:
    problems = []
    seen: Set[str] = set()
    reqs = data["requirements"]
    for req in reqs:
        rid = req.get("id", "?")
        missing = FIELDS - set(req)
        if missing:
            problems.append(f"{rid}: missing {sorted(missing)}")
        if req.get("status") not in STATUSES:
            problems.append(f"{rid}: unknown status {req.get('status')!r}")
        if rid in seen:
            problems.append(f"{rid}: id used twice")
        seen.add(rid)
        if req.get("status") == "retired" and not req.get("replaced_by"):
            problems.append(f"{rid}: retired with no replaced_by")
    for req in reqs:
        for other in req.get("replaced_by") or []:
            if other not in seen:
                problems.append(f"{req['id']}: replaced_by names {other}, which doesn't exist")
    return problems


def marked_lines(snapshot: str) -> Dict[int, str]:
    """Every line of DESIGN.md at the snapshot that holds a mark, with its text."""
    text = subprocess.run(["git", "show", f"{snapshot}:docs/DESIGN.md"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout
    lines = text.split("\n")
    found = {}
    for match in MARK.finditer(text):  # over the whole text, since a mark can wrap onto a new line
        number = text.count("\n", 0, match.start()) + 1
        found[number] = lines[number - 1].strip()
    for number, line in enumerate(lines, start=1):
        if TABLE_MARK.search(line):
            found[number] = line.strip()
    return found


def check_marks(data: dict) -> List[str]:
    marks = marked_lines(str(data["snapshot"]))
    cited: Dict[int, List[str]] = {}
    for req in data["requirements"]:
        for line in req.get("from") or []:
            cited.setdefault(line, []).append(req["id"])
    problems = [f"DESIGN.md:{n} is cited by no requirement: {marks[n][:100]}"
                for n in sorted(set(marks) - set(cited))]
    problems += [f"DESIGN.md:{n} holds no mark, but {', '.join(cited[n])} cite it"
                 for n in sorted(set(cited) - set(marks))]
    if not problems:
        print(f"marks: all {len(marks)} marked lines of DESIGN.md at {data['snapshot']} are cited")
    return problems


def document_lines(name: str) -> List[Tuple[int, str, bool]]:
    """A document's lines as (number, text, inside a "Rejected and retired" section)."""
    path = DOCUMENTS[name]
    if not path.exists():
        return []
    out = []
    retired = False
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
        if line.startswith("#"):
            retired = bool(RETIRED_SECTION.match(line))
        out.append((number, line, retired))
    return out


def anchors(name: str) -> Set[str]:
    """The section anchors a document defines: `{#anchor}` after a heading, or the heading's slug."""
    found = set()
    for _, line, _ in document_lines(name):
        if not line.startswith("#"):
            continue
        explicit = re.search(r"\{#([a-z0-9-]+)\}\s*$", line)
        if explicit:
            found.add(explicit.group(1))
        else:
            title = line.lstrip("#").strip().lower()
            found.add(re.sub(r"[^a-z0-9]+", "-", title).strip("-"))
    return found


def cited_ids(group: str, known: Dict[str, str]) -> List[str]:
    """The ids one citation names: "A-1, A-4 to A-6" gives A-1, A-4, A-5, A-6 (only ids that exist
    inside a range; the range's ends are always named, so a missing end is reported)."""
    out = []
    for item in re.split(r",\s*", group):
        if " to " not in item:
            out.append(item)
            continue
        first, last = item.split(" to ")
        area, a, b = first.rsplit("-", 1)[0], int(first.rsplit("-", 1)[1]), int(last.rsplit("-", 1)[1])
        out += [first, last] + [f"{area}-{n}" for n in range(a + 1, b) if f"{area}-{n}" in known]
    return out


SPLIT = re.compile(rf"\[{CITE_ITEM}(?:,\s*{CITE_ITEM})*(?:,|\s+to)?\s*$")  # a citation cut by a line break


def check_citations(data: dict) -> List[str]:
    status = {req["id"]: req["status"] for req in data["requirements"]}
    problems = []
    for name in DOCUMENTS:
        for number, line, retired_section in document_lines(name):
            if SPLIT.search(line):
                problems.append(f"{name}:{number} breaks a citation across lines; keep it on one line")
            for group in CITATION.findall(line):
                for rid in cited_ids(group, status):
                    if rid not in status:
                        problems.append(f"{name}:{number} cites {rid}, which doesn't exist")
                    elif status[rid] == "retired" and not retired_section:
                        problems.append(f"{name}:{number} cites {rid}, which is retired")
    return problems


def check_coverage(data: dict) -> List[str]:
    """Once both documents exist, every requirement that isn't retired is cited by one of them."""
    if not all(path.exists() for path in DOCUMENTS.values()):
        print("coverage: skipped until both documents exist")
        return []
    status = {req["id"]: req["status"] for req in data["requirements"]}
    cited: Set[str] = set()
    for name in DOCUMENTS:
        for _, line, _ in document_lines(name):
            for group in CITATION.findall(line):
                cited.update(cited_ids(group, status))
    return [f"{rid} ({status[rid]}) is cited by neither document" for rid in status
            if rid not in cited and status[rid] != "retired"]


def check_wording() -> List[str]:
    problems = []
    for name in DOCUMENTS:
        for number, line, retired_section in document_lines(name):
            if retired_section:
                continue
            unquoted = re.sub(r'"[^"]*"', "", line)  # a word in quotes is talked about, not used
            for word, instead in RETIRED_WORDING.items():
                if re.search(rf"\b{re.escape(word)}\b", unquoted, re.I):
                    problems.append(f"{name}:{number} uses retired wording {word!r}; say {instead}")
    return problems


def check_references(data: dict) -> List[str]:
    """Links between the documents, and every requirement's `section`, name sections that exist."""
    found = {name: anchors(name) for name in DOCUMENTS}
    problems = []
    for req in data["requirements"]:
        target, _, anchor = str(req.get("section", "")).partition("#")
        if target in found and found[target] and anchor not in found[target]:
            problems.append(f"{req['id']}: its section {target}#{anchor} doesn't exist")
    for name in DOCUMENTS:
        for number, line, _ in document_lines(name):
            for target, anchor in LINK.findall(line):
                if found[target] and anchor not in found[target]:
                    problems.append(f"{name}:{number} links to {target}#{anchor}, which doesn't exist")
    return problems


def check_quotes(words_file: str) -> List[str]:
    """No repo file holds a run of eight or more words from Andrew's stored notes."""
    if not words_file:
        print("quotes: skipped (no --words file)")
        return []
    def tokens(text: str) -> List[str]:
        return re.findall(r"[a-z0-9']+", text.lower())
    runs = set()
    for note in Path(words_file).read_text(encoding="utf-8").split("\n"):
        words = tokens(note)
        runs.update(" ".join(words[i:i + 8]) for i in range(len(words) - 7))
    tracked = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                             check=True, capture_output=True, text=True).stdout.split("\n")
    problems = []
    for rel in dict.fromkeys(tracked):
        path = ROOT / rel
        if not rel or path.suffix not in {".md", ".yaml", ".yml", ".py", ".html", ".txt", ".json"}:
            continue
        try:
            words = tokens(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        hits = [i for i in range(len(words) - 7) if " ".join(words[i:i + 8]) in runs]
        for i in [h for n, h in enumerate(hits) if n == 0 or h > hits[n - 1] + 1]:  # one line per run
            problems.append(f"{rel} holds eight of Andrew's own words in a row: {' '.join(words[i:i + 8])!r}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("checks", nargs="*",
                        default=["requirements", "marks", "citations", "coverage", "wording", "references",
                                 "quotes"])
    parser.add_argument("--words", default="", help="Andrew's stored words, one note per line")
    args = parser.parse_args()
    data = load_requirements()
    runs = {
        "requirements": lambda: check_requirements(data),
        "marks": lambda: check_marks(data),
        "citations": lambda: check_citations(data),
        "coverage": lambda: check_coverage(data),
        "wording": check_wording,
        "references": lambda: check_references(data),
        "quotes": lambda: check_quotes(args.words),
    }
    failed = False
    for name in args.checks:
        problems = runs[name]()
        for problem in problems:
            print(f"{name}: {problem}")
        failed = failed or bool(problems)
    print("FAILED" if failed else "ok")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
