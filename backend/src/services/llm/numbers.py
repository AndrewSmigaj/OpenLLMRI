"""The number checker (DESIGN.md E8), after the context-shift paper's `number_check.py`: every
numeral an analyst writes must trace to a fact in its evidence packet, cited right after it.

A citation is a bracketed group of fact ids after the numerals it supports, in the same sentence:
"89 items [F1]", "84% aquarium and 8% scuba [F5, F6]"; adjacent groups count as one ("[F5][F6]").
A numeral passes when it equals one of the group's facts at the precision written; a share (a
fraction) may be written as a percentage.
Skipped: numerals inside double quotes (quoted sentences) and identifiers (L12, L12C0, E5, P2, H1,
n2092, "layer 12", "rank 2", "rank-1", "top-1", "pipeline 3", "hub 2", "Card 2", the reconciler's
name for a draft). A sign is compared only when it is written.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Mapping, Optional

NUM = re.compile(r"(?<![\w.#])([+−-]?)(\d[\d,]*(?:\.\d+)?)(?![\w])")
CITE = re.compile(r"\[(F\d+(?:\s*,\s*F\d+)*)\]")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”")
REF = re.compile(r"\b(?:[Ll]ayers?|[Rr]anks?|[Ee]xperts?|[Cc]ards?|[Dd]rafts?|[Pp]ipelines?|[Hh]ubs?|[Tt]op)"
                 r"[\s-]+\d+(?:\s*(?:–|-|to|and)\s*\d+)?")
SENTENCE_END = re.compile(r"[.;!?](?=\s|$)|\n")


def _blank(text: str, pattern: re.Pattern[str]) -> str:
    """The text with the pattern's matches replaced by spaces, so positions stay put."""
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def _context(text: str, start: int, end: int) -> str:
    return " ".join(text[max(0, start - 40):end + 40].split())


def _matches(written: str, sign: str, percent: bool, value: float) -> bool:
    """Whether a written numeral equals the value at the precision written."""
    number = float(written.replace(",", ""))
    decimals = len(written.split(".")[1]) if "." in written else 0
    tolerance = 0.5 * 10 ** -decimals + 1e-9
    shown = -number if sign in ("-", "−") else number
    for candidate in ([value, 100 * value] if percent else [value]):
        target = candidate if sign else abs(candidate)
        if abs(shown - target) <= tolerance:
            return True
    return False


def cited_ids(text: str) -> List[str]:
    """The fact ids a text cites, in order, once each."""
    return list(dict.fromkeys(re.findall(r"F\d+", " ".join(c.group(1) for c in CITE.finditer(text)))))


def check_numbers(text: str, facts: Mapping[str, float]) -> Dict[str, Any]:
    """Every numeral in the text against the facts its citation names. Returns whether all
    passed, how many numerals were checked, and each failure with its context and reason."""
    plain = _blank(_blank(text, QUOTED), REF)
    ends = [m.start() for m in SENTENCE_END.finditer(plain)]
    cites = list(CITE.finditer(plain))
    failures: List[Dict[str, str]] = []
    for fid in cited_ids(plain):
        if fid not in facts:
            failures.append({"numeral": "", "context": "", "reason": f"cites {fid}, which isn't a fact"})
    count = 0
    for m in NUM.finditer(plain):
        count += 1
        sign, written = m.group(1), m.group(2)
        percent = plain[m.end():m.end() + 2].lstrip().startswith("%")
        shown = f"{sign}{written}{'%' if percent else ''}"
        context = _context(text, m.start(), m.end())
        end = next((e for e in ends if e >= m.end()), len(plain))
        cite: Optional[re.Match[str]] = next((c for c in cites if c.start() >= m.end()), None)
        if cite is None or cite.start() > end:
            failures.append({"numeral": shown, "context": context, "reason": "no citation in its sentence"})
            continue
        group = [cite]
        for after in cites[cites.index(cite) + 1:]:
            if plain[group[-1].end():after.start()].strip():
                break
            group.append(after)
        ids = [fid for c in group for fid in re.findall(r"F\d+", c.group(1)) if fid in facts]
        if not any(_matches(written, sign, percent, float(facts[fid])) for fid in ids):
            listed = ", ".join(f"{fid} = {facts[fid]}" for fid in ids) or "no known fact"
            failures.append({"numeral": shown, "context": context, "reason": f"doesn't match {listed}"})
    return {"passed": not failures, "numerals": count, "failures": failures}
