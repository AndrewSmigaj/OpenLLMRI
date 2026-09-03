#!/usr/bin/env python3
"""Prose metrics for the paper draft, checked against WRITING_STANDARD.md.

Usage:
    prose_metrics.py SECTION.md [SECTION.md ...]   report per file, PASS/FLAG per target
    prose_metrics.py --long SECTION.md              also list sentences over 35 words
    prose_metrics.py --dense SECTION.md             also list paragraphs with >2 numbers
    prose_metrics.py --all                          every draft section
    prose_metrics.py --section "## 3.2" FILE        one subsection only

What counts:
    * Paragraphs are blank-line-separated blocks. Lines inside a block are joined.
    * Headings (#), tables (|), HTML comments, and the captions file are excluded
      from the counts. List items count as paragraphs.
    * A number is a numeral token in prose. Numbers that name a section, figure,
      table, box, appendix, or item are not counted, nor are numbers attached to
      letters (identifiers such as L4 or s13) or four-digit years.
    * Em-dashes are the character "—" or the sequence " -- ".

Targets (WRITING_STANDARD.md): mean words/sentence <= 27; sentences over 35 words
<= 15%; em-dashes <= 6 per 1,000 words; semicolons <= 5 per 1,000 words; numbers per
prose paragraph <= 2.5 mean. Parentheses, paragraph length, and the maximum numbers
in one paragraph are reported but not gated.
"""
import re, sys, pathlib, statistics

TARGETS = {
    "words_per_sentence": 27.0,
    "pct_over_35": 15.0,
    "dashes_per_1000": 6.0,
    "semicolons_per_1000": 5.0,
    "numbers_per_paragraph": 2.5,
}

REF_WORDS = r"(?:§|Section|Sections|Figure|Figures|Fig\.|Figs\.|Table|Tables|Box|Appendix|Item|Items|Rule|rule|Step|step|Chapter)\s*"
NUM = re.compile(r"(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?(?![\w])")
ABBREV = ("e.g.", "i.e.", "vs.", "cf.", "et al.", "Fig.", "Figs.", "approx.", "no.", "No.")


def paragraphs(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if all(l.startswith("|") for l in lines):
            continue  # table
        if lines[0].startswith("**Table "):
            continue  # table caption: reviewed with the table, not gated as prose
        lines = [l for l in lines if not l.startswith("#")]
        if not lines:
            continue
        # split list items into their own paragraphs
        items, cur = [], []
        for l in lines:
            if re.match(r"^(?:\d+\.|[-*])\s+", l) and cur:
                items.append(cur); cur = []
            cur.append(l)
        items.append(cur)
        for it in items:
            para = " ".join(it)
            para = re.sub(r"^\s*(?:\d+\.|[-*])\s+", "", para)  # list marker
            para = re.sub(r"\*\*|(?<!\w)\*|\*(?!\w)", "", para)  # bold/italic markers
            out.append(para)
    return out


def sentences(para):
    p = para
    for a in ABBREV:
        p = p.replace(a, a.replace(".", "<DOT>"))
    # split after . ! ? followed by space and an opener (capital, quote, paren, digit)
    parts = re.split(r"(?<=[.!?])[\"”’)]?\s+(?=[\"“‘(A-Z0-9§])", p)
    parts = [s.replace("<DOT>", ".").strip() for s in parts if s.strip()]
    return parts


def words(s):
    return [w for w in re.findall(r"[^\s]+", s) if re.search(r"[\w]", w)]


def count_numbers(para):
    p = re.sub(REF_WORDS + r"[\dA-Z]+(?:\.\d+)?", " ", para)  # section/figure refs
    p = re.sub(r"\b(19|20)\d\d\b", " ", p)  # years
    return len(NUM.findall(p))


def measure(text):
    paras = paragraphs(text)
    sents = [s for p in paras for s in sentences(p)]
    wc = [len(words(s)) for s in sents]
    total_words = sum(wc) or 1
    nums = [count_numbers(p) for p in paras]
    body = "\n".join(paras)  # comments, headings, tables excluded
    dashes = body.count("—") + len(re.findall(r"\s--\s", body))
    return {
        "paragraphs": len(paras),
        "sentences": len(sents),
        "words": total_words,
        "words_per_sentence": sum(wc) / max(len(wc), 1),
        "median_wps": statistics.median(wc) if wc else 0,
        "pct_over_35": 100 * sum(1 for w in wc if w > 35) / max(len(wc), 1),
        "numbers_per_paragraph": sum(nums) / max(len(nums), 1),
        "max_numbers": max(nums) if nums else 0,
        "pct_paras_le2": 100 * sum(1 for n in nums if n <= 2) / max(len(nums), 1),
        "dashes_per_1000": 1000 * dashes / total_words,
        "semicolons_per_1000": 1000 * body.count(";") / total_words,
        "parens_per_1000": 1000 * body.count("(") / total_words,
        "words_per_paragraph": total_words / max(len(paras), 1),
        "_paras": paras, "_sents": sents, "_wc": wc, "_nums": nums,
    }


def report(path, m, show_long=False, show_dense=False):
    flags = []
    def line(label, key, fmt, gate=True):
        v = m[key]
        status = ""
        if gate and key in TARGETS:
            ok = v <= TARGETS[key]
            status = "  PASS" if ok else f"  FLAG (target {TARGETS[key]:g})"
            if not ok:
                flags.append(label)
        print(f"  {label:<34}{fmt.format(v)}{status}")
    print(f"\n{path}  ({m['paragraphs']} paragraphs, {m['sentences']} sentences, {m['words']} words)")
    line("words per sentence (mean)", "words_per_sentence", "{:.1f}")
    line("words per sentence (median)", "median_wps", "{:.0f}", gate=False)
    line("sentences over 35 words", "pct_over_35", "{:.0f}%")
    line("numbers per paragraph (mean)", "numbers_per_paragraph", "{:.1f}")
    line("most numbers in one paragraph", "max_numbers", "{:d}", gate=False)
    line("paragraphs with <=2 numbers", "pct_paras_le2", "{:.0f}%", gate=False)
    line("em-dashes per 1,000 words", "dashes_per_1000", "{:.1f}")
    line("semicolons per 1,000 words", "semicolons_per_1000", "{:.1f}")
    line("parentheses per 1,000 words", "parens_per_1000", "{:.1f}", gate=False)
    line("words per paragraph (mean)", "words_per_paragraph", "{:.0f}", gate=False)
    print("  RESULT: " + ("PASS" if not flags else "FLAG: " + ", ".join(flags)))
    if show_long:
        print("  --- sentences over 35 words ---")
        for s, w in zip(m["_sents"], m["_wc"]):
            if w > 35:
                print(f"  [{w}] {s}")
    if show_dense:
        print("  --- paragraphs with more than 2 numbers ---")
        for p, n in zip(m["_paras"], m["_nums"]):
            if n > 2:
                print(f"  [{n}] {p[:160]}{'…' if len(p) > 160 else ''}")
    return not flags


def subsection(text, heading):
    """Return the text from the line starting with `heading` (e.g. "## 3.2") up to the
    next heading of the same or higher level."""
    lines = text.split("\n"); level = heading.split(" ")[0]
    start = next(i for i, l in enumerate(lines) if l.startswith(heading))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^#{1,%d} " % len(level), lines[i]):
            end = i; break
    return "\n".join(lines[start:end])


def main(argv):
    show_long = "--long" in argv
    show_dense = "--dense" in argv
    sec = None
    if "--section" in argv:
        k = argv.index("--section"); sec = argv[k + 1]; argv = argv[:k] + argv[k + 2:]
    files = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        here = pathlib.Path(__file__).resolve().parent
        files = sorted(str(p) for p in (here.parent / "draft").glob("0*.md"))
    if not files:
        print(__doc__); return 2
    ok = True
    for f in files:
        text = pathlib.Path(f).read_text()
        if sec:
            text = subsection(text, sec)
        ok &= report(f + (f"  [{sec}]" if sec else ""), measure(text), show_long, show_dense)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
