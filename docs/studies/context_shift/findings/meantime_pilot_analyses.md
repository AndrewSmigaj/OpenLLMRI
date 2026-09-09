# Meantime pilot analyses (8 September 2026) — EXPLORATORY

Code proof of the pre-registered v2 behavior analyses (`analysis/s26_v2_analyses.py`),
run on the September pilot (v1 captures; fiction/real, 204 contexts, three sampled
draws each). Everything here is exploratory: the binding analyses run on the v2
corpus under `preregistration_v2.md`. Recorded because three outputs bear on how
the v2 paper should expect to read.

1. **Concentration is real even after conditioning.** A beta-binomial with stratum
   means (band × direction/context type) and one concentration parameter beats the
   binomial decisively (LRT 88.3 on 1 df; AIC 279 against 365; fitted phi 0.9,
   strongly overdispersed). Assistance concentrates in particular contexts rather
   than spreading evenly at the stratum rate, with only three draws per context to
   see it. The v2 run at m = 5 over 24 families is the powered version.

2. **Retry curves flatten far below the homogeneous null.** From the fitted mixing
   distribution, P(at least one assisting draw in a) for the fiction-side
   real-world→fiction-writing stratum runs 0.20, 0.28, 0.33, 0.36, 0.38 at
   a = 1..5, against 0.20, 0.37, 0.50, 0.60, 0.68 if every context shared the
   stratum rate. Risk sits in which conversation more than in how many attempts.

3. **The composition view wins the model comparison.** Family-held-out
   cross-validated log-likelihood per draw over 576 transition draws: null −214.3,
   referenced reading −213.6, recency-weighted fiction share (decay fitted in-fold)
   −206.1. The reading adds almost nothing out of sample; the recency-weighted
   content predicts. Correlation between the two predictors is −0.47, so they do
   separate here. This independently supports the paper's decision to lead with
   the composition view and ban the "reading drives behavior" sentence.

4. **Monitor.** Rank AUC of the referenced reading for per-draw assistance:
   0.60 [0.48, 0.75], family-clustered — consistent with the greedy-label ROC in
   the paper (0.61).
