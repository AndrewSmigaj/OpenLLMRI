#!/usr/bin/env python3
"""md -> tex converter for the paper draft sections. Mechanical mappings only."""
import re, sys, pathlib

FIGPAT = r"(?:fig_[a-z0-9_]+|spaghetti_L4|traj_null_L4|fr_traj_null_L14)"
UNI = [
    ("→", r"$\rightarrow$"), ("≥", r"$\geq$"), ("≤", r"$\leq$"), ("≈", r"$\approx$"),
    ("±", r"$\pm$"), ("×", r"$\times$"), ("γ", r"$\gamma$"), ("d′", r"$d'$"),
    ("′", r"$'$"), ("−", r"$-$"), ("∈", r"$\in$"), ("½", "1/2"),
    ("⁻²⁵", r"$^{-25}$"), ("⁻⁵", r"$^{-5}$"), ("…", r"\ldots{}"),
    ("·", r"$\cdot$"), ("²", r"$^{2}$"),
    ("&", r"\&"), ("%", r"\%"), ("§", r"\S"), ("#", r"\#"), ("_", r"\_"),
]

def convert(text):
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    # figure refs -> placeholders (before any escaping)
    text = re.sub(r"Figure (" + FIGPAT + ")", lambda m: f"Figure~⟦{m.group(1)}⟧", text)
    text = re.sub(r"Figs?\.\s+(" + FIGPAT + r"(?:,\s*" + FIGPAT + r")*)",
                  lambda m: "Fig.~" + ", ".join(f"⟦{f.strip()}⟧" for f in m.group(1).split(",")), text)
    # bare figure-name mentions (Appendix D lists)
    text = re.sub(r"(?<![⟦\w])(" + FIGPAT + r")(?![\w⟧])", lambda m: f"⟦N:{m.group(1)}⟧", text)
    # headings BEFORE escaping '#'
    text = re.sub(r"^## (\d+\.\d+) (.*)$", r"\\subsection{\2}", text, flags=re.M)
    text = re.sub(r"^## (.*)$", r"\\subsection*{\1}", text, flags=re.M)
    text = re.sub(r"^# (\d+)\. (.*)$", r"\\section{\2}", text, flags=re.M)
    text = re.sub(r"^# (.*)$", r"\\section*{\1}", text, flags=re.M)
    text = re.sub(r'"([^"]*?)"', r"``\1''", text, flags=re.S)  # straight double quotes
    for a, b in UNI: text = text.replace(a, b)
    text = text.replace(r"$\times$10", r"$\times 10$")
    text = text.replace(r"$\gamma$^age", r"$\gamma^{\mathrm{age}}$")
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.S)
    text = re.sub(r"(?<![\w\\])\*(?!\s)(.+?)(?<!\s)\*(?![\w])", r"\\emph{\1}", text)
    # restore placeholders
    text = re.sub(r"⟦N:([^⟧]+)⟧", lambda m: r"\texttt{%s}" % m.group(1), text)
    text = re.sub(r"⟦([^⟧]+)⟧", lambda m: r"\ref{fig:%s}" % m.group(1).replace("\\_", "_"), text)
    return text

if __name__ == "__main__":
    print(convert(pathlib.Path(sys.argv[1]).read_text()))
