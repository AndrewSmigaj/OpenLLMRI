# Retired numerals

Numerals present in the frozen draft (draft_v2) that the paper no longer prints, each
with the reason. The preservation check in number_check.py skips these; anything else
that disappears is still reported as LOST.

| Numeral | Where it was | Why retired |
|---|---|---|
| 96 | tank transition completions ("zero of 96") | the count now covers all 108 tank / 312 completions (6 Sept 2026 regeneration) |
| 56, 66 | tank side bands answering their side | superseded by the 2,048-token pass (52%/59%; 62%/63% delivered) |
| 80 | fiction/real middle-band safe rate | superseded (89% of delivered answers) |
| 91, 50 | fiction/real safe-completion gradient | superseded; the gradient was an artifact of truncated reasoning |
| 0.72, 0.0138 | pooled matched-composition test (tank) | superseded (0.67 vs 0.55, p = 0.10) |
| 1.13, 0.010 | fiction/real k=2 separation | superseded (+0.99, p = 0.065, against delivered safe completions) |
| 0.76 | monitor ROC interval upper bound [0.43, 0.76] | superseded ([0.37, 0.81]) |
