#!/usr/bin/env python3
"""Build main.tex from the draft md sections + figure captions, then run tectonic."""
import re, pathlib, subprocess, sys
sys.path.insert(0, ".")
from md2tex import convert

D = pathlib.Path("../draft")
def load_captions(path=D/"captions.md"):
    """captions.md: '## <figure id>' headings, each followed by its caption text."""
    text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    caps = {}
    for m in re.finditer(r"^## (\S+)\s*\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S):
        caps[m.group(1)] = convert(" ".join(m.group(2).split()))
    return caps
CAP = load_captions()
SEC_FIGS = {
 "intro": ["fig_s9_collapse"],
 "3.1": ["fig_r3_heatmap_secondary_fr","fig_r3_axis_rotation","fig_r2_carrier_dprime","fig_s9_d5_pairs","fig_r6_carrier_dprime_fr"],
 "3.2": ["fig_r1_residual_gap","fig_s13_collapse_layers","fig_s9_asymmetry"],
 "3.3": ["fig_s9_model_classes","fig_r1_fit_gallery_tank","spaghetti_L4","fig_r2_within_stream","fig_s9_within_stream_fr"],
 "3.4": ["fig_r2_mode_track","fig_r6_behavior_bands","fig_s9_behavior_matchedk","fig_s14_behavior_by_layer"],
 "3.5": ["fig_r6_d6_loop_tank"],
 "3.6": ["fig_r5_geometry","fig_s9_shift_marker"],
}
def figenv(name):
    return ("\\begin{figure}[tbp]\\centering\n"
            f"\\includegraphics[width=\\linewidth]{{{name}.png}}\n"
            f"\\caption{{{CAP[name]}}}\\label{{fig:{name}}}\n\\end{{figure}}\n")

def box_enumerate(t):
    m1 = t.find("\\textbf{Box 1"); m2 = t.find("\\textbf{Glossary")
    assert m1 > 0 and m2 > m1
    region = t[m1:m2]
    region = re.sub(r"^(\d+)\.\s", r"\\item ", region, flags=re.M)
    first = region.find("\\item")
    region = region[:first] + "\\begin{enumerate}\n" + region[first:] + "\\end{enumerate}\n\n"
    return t[:m1] + region + t[m2:]

# abstract pieces
abs_md = (D/"00_abstract.md").read_text()
abs_body = abs_md.split("## Abstract")[1].split("*Content note:")[0].strip()
note = "Content note:" + abs_md.split("*Content note:")[1].strip().rstrip("*")
abs_tex = convert(abs_body); note_tex = convert(note)

def list_enumerate(tex, start, stop):
    i = tex.find(start); j = tex.find(stop)
    assert 0 < i < j
    region = re.sub(r"^\d+\.\s", r"\\item ", tex[i:j], flags=re.M)
    first = region.find("\\item")
    region = region[:first] + "\\begin{enumerate}\n" + region[first:] + "\\end{enumerate}\n\n"
    return tex[:i] + region + tex[j:]

intro = convert((D/"01_intro.md").read_text())
intro = list_enumerate(intro, "We contribute:", "All numbers regenerate") + "\n" + figenv("fig_s9_collapse") + "\\FloatBarrier\n"
methods = box_enumerate(convert((D/"02_methods.md").read_text())) + "\\FloatBarrier\n"
results = convert((D/"03_results_R1-R6.md").read_text())
# append figures at end of each subsection
chunks = re.split(r"(?=\\subsection\{)", results)
out = [chunks[0]]
keys = ["3.1","3.2","3.3","3.4","3.5","3.6"]
for k, ch in zip(keys, chunks[1:]):
    out.append(ch + "\n" + "".join(figenv(f) for f in SEC_FIGS[k]) + "\\FloatBarrier\n")
results = "".join(out)
discussion = convert((D/"04_discussion.md").read_text()) + "\\FloatBarrier\n"
limits = convert((D/"05_limitations_future.md").read_text())
appx = convert((D/"06_appendices.md").read_text())
appx = appx.replace("\\section*{Appendices and back matter (assembly spec)}",
  "\\section*{Back matter (assembly spec --- materialized at final build)}\n"
  "\\emph{Review-draft note: the sections below are the assembly specification; the final build replaces them with the referenced frozen content.}\n")

main = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx,amsmath,amssymb,placeins,enumitem,xcolor,microtype}
\usepackage[colorlinks=true,linkcolor=blue!50!black,urlcolor=blue!50!black]{hyperref}
\graphicspath{{../../analysis/figures/}{../../analysis/figures/other/}}
\setlength{\parskip}{2pt}
\title{Unresolved: Semantic Metastability in a Language Model\\ Under Context Shift}
\author{[author block --- Andrew]}
\date{Review draft --- \today}
\begin{document}
\maketitle
\begin{quote}\itshape``Two fish are in a tank. One looks to the other and asks: how do you drive this thing?''\end{quote}
\begin{abstract}
""" + abs_tex + r"""
\end{abstract}
\begin{center}\begin{minipage}{0.9\linewidth}\small\emph{""" + note_tex + r"""}\end{minipage}\end{center}
""" + intro + methods + results + discussion + limits + "\n" + appx + "\n\\end{document}\n"

pathlib.Path("main.tex").write_text(main)
print("main.tex written", len(main), "chars")
