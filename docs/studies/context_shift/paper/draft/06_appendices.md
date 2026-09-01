<!-- Section 6: Appendices + back matter skeleton. Content assembled from existing
frozen docs at tex time; this file specifies exactly what goes where. -->

# Appendices and back matter (assembly spec)

## Acknowledgments
[Agreed AI-assistance line — exact text from Andrew/chat side, placeholder.] Personal
acknowledgments: Andrew adds.

## Related work (arXiv default: standalone section, drafted from handoff §6 anchors)
Probing validity: Alain & Bengio; Hewitt & Liang (control tasks — our D5 + label-shuffle
audits presented as the selectivity answer); Belinkov survey. Directions & steering:
Marks & Tegmark; Arditi et al. (refusal direction — nearest cousin of the fiction/real
behavior link). In-context dynamics: Xie et al. (ICL as implicit Bayesian inference —
the standing theory our integrator null speaks to); Hendel; Todd (function vectors);
Olsson et al. (induction heads). Safety: many-shot jailbreaking; Crescendo-style
multi-turn escalation. Psycholinguistics: Christianson & Ferreira; Slattery et al.; van
Schijndel & Linzen. Verbalized uncertainty & ambiguity (grounds the intro's scoped
claim): Kadavath et al.; Lin et al. (verbalized confidence); Xiong et al. (calibration
of verbalized confidence); Liu et al. (ambiguity modeling). Internal encoding vs
expression (grounds Discussion's "represented but not consulted"): Azaria & Mitchell
(internal state predicts truthfulness); Orgad et al. (models encode more than they
express). Long-context artifacts: attention sinks (the "is the offset positional?"
question; midpoint referencing makes our findings robust either way). Dynamics: Sussillo
& Barak; Kelso; Rabinovich et al. Motivating
case (intro + discussion): Raine v. OpenAI, Cal. Super. Ct. (S.F.), filed
2025-08-26; contemporaneous reporting (CNN 2025-08-26; NBC News; TechCrunch
2025-11-26 on OpenAI's answer denying causation). Contested litigation — the paper
characterizes only what the filing and reporting describe.

## Appendix A — Corrections record (presented as method)
The 18 entries verbatim from FINDINGS_FINAL §3, one line each, with the two same-session
retractions (D6 stickiness; fr durability) called out; one framing paragraph: every
claim in this paper survived an explicit attempt to kill it, and these are the ones that
did not.

## Appendix B — Synthesis audit
The earns/borderline/ornament table from FINDINGS_FINAL §4, with its one framing
sentence (every element justified or named as ornament — nothing kept silently).

## Appendix C — QA and reproducibility
Regeneration audit summary (bit-identical axes; 23-script diff green; seeded bootstraps
exact); 9/9 fixture suite; sign/boundary/join/shuffle audits; the two logged post-freeze
additions (s12 response counts, 0/96; s11 monitor ROC, AUC 0.61 [0.43,0.76]); repository
pointer + regeneration instructions. Terminology map for repository readers: the paper's
*remnant* is the repository's "residual"; the dwelling within the unresolved zone is the
repository's "park"; *accumulation offset* is "accumulation drift"; *tasks* are the
repository's "probes"/"probe arms"; corpus directories D3/D4/D5/D6 are the transition,
no-shift, minimal-pair, and mixture-sweep corpora; the repository's "K=1" label names an
analysis convention for a routing track this study dropped.

## Appendix D — Supplementary figures
figures/other/ (12): fr fit gallery, fr D6 loop, tank secondary heatmap, matched-k panel
is MAIN (fig_s9_behavior_matchedk) — supplement gets: raw + midref heatmap generations
(the instrument story's "before" pictures), prelexical_L4, occupancy_bands_L4,
jumpiness, norm_vs_alignment, calibration_layers, plus fig_s11_monitor_roc. fig_s13_collapse_layers is MAIN (cited
in 3.2's depth paragraph; committed script s13_collapse_by_layer.py).
