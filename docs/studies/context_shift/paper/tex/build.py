#!/usr/bin/env python3
"""Build main.tex from the draft md sections + figure captions, then run tectonic."""
import re, pathlib, subprocess, sys
sys.path.insert(0, ".")
from md2tex import convert

D = pathlib.Path("../draft")
CAP = {
 "fig_s9_collapse": "The central result: both transition directions, both tasks, at each task's calibrated site (tank: ' tank' token, layer 4; fiction/real: ' want' token, layer 14). Solid: transition means $\\pm$1 sd, midpoint-referenced. Dotted with bands: position-matched no-shift references $\\pm$1 sd. Green: the unresolved band between the references. Readings cross the midpoint quickly; neither direction reaches the opposite reference within twenty counter-sentences.",
 "fig_r3_heatmap_secondary_fr": "Fiction/real readings by layer (0--23) and position under per-layer secondary axes (class means at $\\pm$1): class signal at every depth, no off-band regime. Left pair: no-shift controls. Right pair: transitions, shift after sentence 20.",
 "fig_r3_axis_rotation": "Axis rotation: cosine between each layer's accumulated-context (secondary) axis and the single-sentence calibration axis. Tank stays at 0.78--0.97; fiction/real declines to 0.57--0.63 at layers 10--23 --- depth claims require refit axes.",
 "fig_r2_carrier_dprime": "Class signal by carrier token, identity matched (the nine tank-carrier tokens appear verbatim in every checkpoint window): $d' = 11.7$ at ' tank' against a context-token median of 1.4 ($n = 6$ runs per class; non-peak orderings not interpretable at this $n$).",
 "fig_s9_d5_pairs": "Minimal pairs: 150 sentence pairs, content held within pair, framing cue varied. Framing cues alone move the reading $+0.99$ axis units (half the class separation), 95\\% of pairs in the predicted direction.",
 "fig_r6_carrier_dprime_fr": "Fiction/real class signal across carrier tokens: distributed over the request's content words (' write' 6.4, ' suicide' 6.2, ' want' 4.5) against a context-token median of 3.6 --- a framing contrast lives across the utterance.",
 "fig_r1_residual_gap": "The remnant gap: distance between each run's post-shift plateau and the position-matched no-shift level (axis units from the reference midpoint), family-clustered 95\\% CIs. All four task-by-direction conditions positive; real$\\rightarrow$fictional demotes to suggestive when reference uncertainty is propagated.",
 "fig_s13_collapse_layers": "The collapse view across depth (per-layer secondary axes; class means $\\pm$1, midpoint 0). Shallow fiction/real layers flip suddenly and completely; mid and deep layers cross partially and dwell; tank aquarium$\\rightarrow$vehicle stays on the origin side of the midpoint through the final layer. The calibrated sites are single rows of this progression.",
 "fig_s9_asymmetry": "Direction asymmetry: transitions into the broader class stop farther short; the pattern replicates under the replicate carrier and appears at the ' letter' site ($n = 4$ per direction, exploratory); per-side calibration spreads differ (vehicle broader than aquarium at every layer tested).",
 "fig_s9_model_classes": "Per-run model selection (BIC with an indeterminacy band) over five candidate processes, with simulation-calibrated identifiability: drift-plus-jump dominates among classifiable runs; the two-timescale integrator wins zero runs, and two-timescale truth cannot masquerade as hybrid.",
 "fig_r1_fit_gallery_tank": "Per-run fits (tank): the best single-$\\gamma$ recency integrator underpredicts the early rise and overpredicts late convergence; drift-plus-jump hybrids capture the paths.",
 "spaghetti_L4": "Raw per-run trajectories (tank, layer 4): the heterogeneity behind the means --- some runs glide, some step.",
 "fig_r2_within_stream": "Within-stream readings (tank): post-shift-block tokens --- 100\\% destination-class content --- read about half their no-shift reference (trimmed means; the two transition directions), recovering only partially by twenty sentences.",
 "fig_s9_within_stream_fr": "Within-stream replication in fiction/real with a tighter instrument: the same history-driven suppression of the new evidence's own tokens.",
 "fig_r2_mode_track": "The dwell (tank aquarium$\\rightarrow$vehicle): the central tendency of the run distribution is stationary at mid-axis for $\\geq$10 consecutive steps, $\\geq$2.9 across-run standard deviations from both endpoint references, spread flat; Gaussian-mixture comparison favors one component in every time bin.",
 "fig_r6_behavior_bands": "Behavior by reading band (tank): side bands answer their side (56\\%/66\\%); the mid band answers ``both'' in 45\\% of cells --- roughly double either side. Zero of 96 completions ask which sense is meant.",
 "fig_s9_behavior_matchedk": "Behavior at matched context composition: mid-transition, decided answers come from runs with more extreme readings (pooled $k \\in \\{6,12\\}$, graded suggestive); in fiction/real the reading separates response types at $k = 2$ only; safe-completion rates run 50$\\rightarrow$80$\\rightarrow$91\\% across bands (fiction-side endpoint $n = 4$).",
 "fig_s14_behavior_by_layer": "EXPLORATORY (post-freeze): reading$\\rightarrow$behavior association by layer (rank AUC, family-clustered 95\\% bands). Roughly flat from mid-stack to the final layer in both tasks; nothing singles out the deep layers. Blunt instrument: band-level association, imbalanced outcomes.",
 "fig_r6_d6_loop_tank": "Hysteresis without stickiness (tank): static-mixture sweeps in two block orders produce loop area $+14.4$ [12.2, 16.8]; a one-parameter recency integrator fitted to the same cells reproduces it ($+14.3$) --- excess ``stickiness'' $+0.1$, ns.",
 "fig_r5_geometry": "Per-state geometry: jump steps ($1.06\\times$/$1.12\\times$ the null) and dwell states ($0.96\\times$) sit inside the no-shift null's spread; positive controls (calibration states, position-mismatched states) are detected.",
 "fig_s9_shift_marker": "The mixed-context marker: mean out-of-subspace reconstruction error of transition states against a family-block bootstrap null --- a shared displacement of 25\\%/38\\% (tank/fiction-real) of class separation, orthogonal to the class axis, rising over $\\approx$5 post-shift sentences, persisting to twenty, largest during the dwell.",
}
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

intro = convert((D/"01_intro.md").read_text()) + "\n" + figenv("fig_s9_collapse") + "\\FloatBarrier\n"
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
