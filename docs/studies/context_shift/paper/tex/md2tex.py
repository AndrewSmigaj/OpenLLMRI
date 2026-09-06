#!/usr/bin/env python3
"""md -> tex converter for the paper draft sections. Mechanical mappings only."""
import re, sys, pathlib, json

FIGPAT = r"(?:fig_[a-z0-9_]+|spaghetti_L4|traj_null_L4|fr_traj_null_L14)"
_CMAP = pathlib.Path(__file__).with_name("cite_map.json")
CITES = json.loads(_CMAP.read_text()) if _CMAP.exists() else {}
UNMAPPED = []  # placeholder texts with no entry in cite_map.json (left visible)
UNI = [
    ("→", r"$\rightarrow$"), ("≥", r"$\geq$"), ("≤", r"$\leq$"), ("≈", r"$\approx$"),
    ("±", r"$\pm$"), ("×", r"$\times$"), ("γ", r"$\gamma$"), ("d′", r"$d'$"),
    ("′", r"$'$"), ("−", r"$-$"), ("∈", r"$\in$"), ("½", "1/2"),
    ("⁻²⁵", r"$^{-25}$"), ("⁻⁵", r"$^{-5}$"), ("…", r"\ldots{}"),
    ("·", r"$\cdot$"), ("²", r"$^{2}$"),
    ("&", r"\&"), ("%", r"\%"), ("§", r"\S"), ("#", r"\#"), ("_", r"\_"),
]

def _lists(text):
    """Markdown lists -> enumerate/itemize. A marker line starts a list only at the
    beginning of a block (after a blank line or heading) or inside a list; indented
    lines continue the current item; a blank line ends the list unless the next
    non-blank line is another marker of the same kind."""
    lines = text.split("\n"); out = []; kind = None; prev_blank = True
    def close():
        nonlocal kind
        if kind: out.append("\\end{%s}" % kind); kind = None
    for i, ln in enumerate(lines):
        m_num = re.match(r"^\d+\.\s+(.*)$", ln); m_bul = re.match(r"^[-*]\s+(.*)$", ln)
        this = "enumerate" if m_num else ("itemize" if m_bul else None)
        if this and (prev_blank or kind):
            if kind and kind != this: close()
            if not kind: out.append("\\begin{%s}" % this); kind = this
            out.append("\\item " + (m_num or m_bul).group(1)); prev_blank = False; continue
        if kind:
            if ln.strip() == "":
                nxt = next((l for l in lines[i+1:] if l.strip()), "")
                if re.match(r"^\d+\.\s+", nxt) and kind == "enumerate" or re.match(r"^[-*]\s+", nxt) and kind == "itemize":
                    prev_blank = True; continue
                close(); out.append(ln); prev_blank = True; continue
            if ln.startswith(" "):
                out.append(ln.strip()); continue
            close()
        out.append(ln); prev_blank = (ln.strip() == "" or ln.startswith("#"))
    close()
    return "\n".join(out)

def _tables(text):
    """Pipe tables -> table floats. A paragraph '**Table N.** caption' directly before
    the table becomes its caption. Structural & and \\ are emitted as placeholders and
    restored after escaping."""
    blocks = re.split(r"(\n\s*\n)", text); out = []; i = 0
    while i < len(blocks):
        b = blocks[i]
        rows = [l.strip() for l in b.strip().split("\n")]
        if rows and all(r.startswith("|") for r in rows) and len(rows) >= 2:
            cap = ""
            if len(out) >= 2 and re.match(r"^\*\*Table \d+\.\*\*", out[-2].strip()):
                cap = re.sub(r"^\*\*Table \d+\.\*\*\s*", "", out[-2].strip()); out[-2] = ""
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", c or "-") for c in r)]
            ncol = max(len(r) for r in cells)
            widths = [max(len(r[j]) if j < len(r) else 0 for r in cells) for j in range(ncol)]
            body = ["⟦AMP⟧".join(r + [""] * (ncol - len(r))) + "⟦NL⟧" for r in cells]
            size = "\\small"
            if ncol >= 6 or sum(widths) > 90:
                # wide table (many columns, or long headers such as the direction
                # labels): full-width wrapping columns so nothing runs past the
                # margin; the first column gets 1.4 shares, numeric columns are
                # right-aligned, headers wrap.
                NUM = re.compile(r"^[\s\d.,+\-\u2212\u00b1%\[\]/\u2248()\u2014]*$")
                rest = (ncol - 1.4) / (ncol - 1)
                cols = ["\\hsize=1.4\\hsize\\raggedright\\arraybackslash"]
                for j in range(1, ncol):
                    numeric = all(NUM.match(r[j] if j < len(r) else "") for r in cells[1:])
                    cols.append(f"\\hsize={rest:.4f}\\hsize" + ("\\raggedleft" if numeric else "\\raggedright") + "\\arraybackslash")
                spec = "".join(">{" + c + "}X" for c in cols)
                env = ("\\begin{tabularx}{\\linewidth}{" + spec + "}", "\\end{tabularx}")
                size = "\\footnotesize"
            elif max(widths) > 28:  # text-heavy table: wrapping columns, left-aligned
                spec = "l" + "".join("X" if w > 28 else "l" for w in widths[1:])
                env = ("\\begin{tabularx}{\\linewidth}{" + spec + "}", "\\end{tabularx}")
            else:
                spec = "l" + "r" * (ncol - 1)
                env = ("\\begin{tabular}{" + spec + "}", "\\end{tabular}")
            tex = ("\\begin{table}[htbp]\\centering" + size + "\n"
                   + (f"\\caption{{{cap}}}\n" if cap else "")
                   + env[0] + "\n\\toprule\n" + body[0]
                   + "\n\\midrule\n" + "\n".join(body[1:]) + "\n\\bottomrule\n" + env[1] + "\n\\end{table}")
            out.append(tex)
        else:
            out.append(b)
        i += 1
    return "".join(out)

def convert(text):
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    # citations: [CITE: text] -> \citep{keys} via cite_map.json (placeholder survives escaping)
    cites = []
    def _cite(m):
        key = " ".join(m.group(1).split()); ent = CITES.get(key)
        if ent is None:
            UNMAPPED.append(key); return m.group(0)
        keys, pre = (ent, "") if isinstance(ent, list) else (ent["keys"], ent.get("pre", ""))
        cmd = ("\\citep[%s][]{%s}" % (pre, ",".join(keys))) if pre else "\\citep{%s}" % ",".join(keys)
        cites.append(cmd); return "⟦CITE%d⟧" % (len(cites) - 1)
    text = re.sub(r"\[CITE:\s*(.*?)\]", _cite, text, flags=re.S)
    # figure refs -> placeholders (before any escaping)
    text = re.sub(r"Figure\s+(" + FIGPAT + ")", lambda m: f"Figure~⟦{m.group(1)}⟧", text)
    text = re.sub(r"Figs?\.\s+(" + FIGPAT + r"(?:,\s*" + FIGPAT + r")*)",
                  lambda m: "Fig.~" + ", ".join(f"⟦{f.strip()}⟧" for f in m.group(1).split(",")), text)
    # bare figure-name mentions (Appendix D lists)
    text = re.sub(r"(?<![⟦\w])(" + FIGPAT + r")(?![\w⟧])", lambda m: f"⟦N:{m.group(1)}⟧", text)
    # headings BEFORE escaping '#'
    text = re.sub(r"^## (\d+\.\d+) (.*)$", r"\\subsection{\2}", text, flags=re.M)
    text = re.sub(r"^## (.*)$", r"\\subsection*{\1}", text, flags=re.M)
    text = re.sub(r"^# (\d+)\. (.*)$", r"\\section{\2}", text, flags=re.M)
    text = re.sub(r"^# (.*)$", r"\\section*{\1}", text, flags=re.M)
    text = _tables(_lists(text))
    text = re.sub(r'"([^"]*?)"', r"``\1''", text, flags=re.S)  # straight double quotes
    for a, b in UNI: text = text.replace(a, b)
    text = text.replace(r"$\times$10", r"$\times 10$")
    text = text.replace(r"$\gamma$^age", r"$\gamma^{\mathrm{age}}$")
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.S)
    text = re.sub(r"(?<![\w\\])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w])", r"\\emph{\1}", text)  # italics may wrap lines
    # restore placeholders
    text = text.replace("⟦AMP⟧", " & ").replace("⟦NL⟧", " \\\\")
    text = re.sub(r"⟦CITE(\d+)⟧", lambda m: cites[int(m.group(1))], text)
    text = re.sub(r"⟦N:([^⟧]+)⟧", lambda m: r"\texttt{%s}" % m.group(1), text)
    text = re.sub(r"⟦([^⟧]+)⟧", lambda m: r"\ref{fig:%s}" % m.group(1).replace("\\_", "_"), text)
    return text

if __name__ == "__main__":
    print(convert(pathlib.Path(sys.argv[1]).read_text()))
