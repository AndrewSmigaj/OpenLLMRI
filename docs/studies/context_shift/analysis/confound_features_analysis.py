#!/usr/bin/env python3
"""Confound-ceiling analysis over the surface-feature battery (confound appendix).

The question §3.1 raises: is the reading tracking the intended contrast, or "some other
variance" the two pools happen to differ on? This script answers the descriptive half:
how far can a classifier separate the two classes on surface features ALONE. To make it a
true ceiling (the MOST surface features can explain, not the least), the classifier is a
standardized logistic regression — a stronger linear rule than the reading's own
difference-of-means — validated leave-one-scene-pair-out. Whatever that ceiling is, it is
disclosed:

  * a HIGH ceiling means the classes are surface-separable, so the reading is not doing
    anything a surface classifier could not — consistent with §3.1's scoped claim that
    the reading "tracks framing cues, not an abstract representation of the frame";
  * a LOW ceiling means the reading separates the classes better than surface features do.

Either way it is the honest number to print. This is the surface baseline only; deeper
(judgment) features would be a second confounded model reading, not a clean control.

Input : docs/studies/context_shift/analysis/confound_features.csv (feature_battery.py)
Output: docs/studies/context_shift/analysis/figures/fig_confound_features.png
        docs/studies/context_shift/findings/feature_table.md

Run from the repository root:
  .venv/bin/python docs/studies/context_shift/analysis/confound_features_analysis.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = Path("docs/studies/context_shift/analysis/confound_features.csv")
FIGDIR = Path("docs/studies/context_shift/analysis/figures")
TABLE = Path("docs/studies/context_shift/findings/feature_table.md")

# reading's own leave-one-scene-pair-out held-out accuracy, from Box 1 rule 2 of the paper
# (regenerable via scene_heldout_calibration.py at the calibrated layer). Referenced, not
# recomputed here, because that reads the raw calibration captures (not in the repo).
READING_ACC = {"tank": 0.905, "fr": 0.910}
CLASSES = {"tank": ("aquarium", "vehicle"), "fr": ("fictional", "real")}
TITLES = {"tank": "tank (aquarium vs vehicle)", "fr": "fiction/real"}

BLUE, ORANGE, INK, MUT, SURFACE, GRID = "#2a78d6", "#eb6834", "#222222", "#8a8a86", "#fcfcfb", "#e8e8e4"
SCALARS = ["n_tokens", "n_chars", "n_sentences", "ttr", "mean_word_len", "comma_rate",
           "semicolon_rate", "quote_present", "dash_present", "digit_rate", "within_scene_4gram"]
PRETTY = {"n_tokens": "token length", "n_chars": "char length", "n_sentences": "sentence count",
          "ttr": "type-token ratio", "mean_word_len": "mean word length", "comma_rate": "comma rate",
          "semicolon_rate": "semicolon rate", "quote_present": "has dialogue quote",
          "dash_present": "has dash", "digit_rate": "digit rate", "within_scene_4gram": "within-scene 4-gram overlap"}


def auc(scores: np.ndarray, pos: np.ndarray) -> float:
    """Rank AUC: P(score for a positive > score for a negative). pos is a boolean mask."""
    n1, n0 = int(pos.sum()), int((~pos).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(scores)
    return (r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def feat_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in ("task", "cls", "scene", "idx")]


def classify_task(df: pd.DataFrame, task: str) -> dict:
    """Leave-one-scene-pair-out logistic regression on standardized features — the confound
    ceiling (best a linear surface classifier does). class_weight balances fiction's 2:1."""
    a, b = CLASSES[task]
    sub = df[df.task == task].copy()
    cols = feat_cols(sub)
    X = sub[cols].to_numpy(dtype=np.float64)
    y = (sub.cls == b).to_numpy()  # positive class = b
    scenes_a = sorted(sub[sub.cls == a].scene.unique())
    scenes_b = sorted(sub[sub.cls == b].scene.unique())
    n_folds = min(len(scenes_a), len(scenes_b))
    assert n_folds == 12, f"{task}: expected 12 folds, got {n_folds}"
    scene = sub.scene.to_numpy()

    pred_all, score_all, y_all, fold_acc = [], [], [], []
    for i in range(n_folds):
        hold = (scene == scenes_a[i]) | (scene == scenes_b[i])
        tr, te = ~hold, hold
        clf = make_pipeline(StandardScaler(),
                            LogisticRegression(max_iter=2000, class_weight="balanced"))
        clf.fit(X[tr], y[tr])
        score = clf.predict_proba(X[te])[:, 1]
        pred = score > 0.5
        pred_all.append(pred); score_all.append(score); y_all.append(y[te])
        # balanced per-fold accuracy (fiction folds are imbalanced within a held-out pair too)
        yy = y[te]
        rb = float(pred[yy].mean()) if yy.any() else np.nan
        ra = float((~pred[~yy]).mean()) if (~yy).any() else np.nan
        fold_acc.append(np.nanmean([ra, rb]))
    pred = np.concatenate(pred_all); score = np.concatenate(score_all); yt = np.concatenate(y_all)
    rec_b = float((pred[yt]).mean()); rec_a = float((~pred[~yt]).mean())
    return {
        "balanced_acc": (rec_a + rec_b) / 2,
        "auc": auc(score, yt),
        "mean_fold_acc": float(np.nanmean(fold_acc)),
        "n": len(yt), "n_a": int((~yt).sum()), "n_b": int(yt.sum()),
    }


def per_feature_deltas(df: pd.DataFrame, task: str) -> dict:
    """Cliff's delta (= 2*AUC - 1) per scalar feature between the two classes."""
    a, b = CLASSES[task]
    sub = df[df.task == task]
    pos = (sub.cls == b).to_numpy()
    return {f: 2 * auc(sub[f].to_numpy(dtype=np.float64), pos) - 1 for f in SCALARS}


def figure(df: pd.DataFrame, results: dict, deltas: dict):
    fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.6), facecolor=SURFACE,
                            gridspec_kw={"width_ratios": [1.35, 1]})

    # panel 1: per-feature Cliff's delta, both tasks, sorted by max |delta|
    order = sorted(SCALARS, key=lambda f: max(abs(deltas["tank"][f]), abs(deltas["fr"][f])))
    yy = np.arange(len(order))
    axs[0].barh(yy + 0.19, [deltas["tank"][f] for f in order], height=0.36, color=BLUE, label="tank")
    axs[0].barh(yy - 0.19, [deltas["fr"][f] for f in order], height=0.36, color=ORANGE, label="fiction/real")
    axs[0].axvline(0, color=MUT, lw=0.9)
    axs[0].set_yticks(yy); axs[0].set_yticklabels([PRETTY[f] for f in order], fontsize=8)
    axs[0].set_xlabel("Cliff's delta between classes  (0 = no separation, ±1 = full)", fontsize=8.5, color=INK)
    axs[0].set_xlim(-1, 1)
    axs[0].set_title("Some surface features differ by class; many overlap", fontsize=9.5, color=INK)
    axs[0].legend(fontsize=8, frameon=False, loc="lower right")

    # panel 2: confound ceiling vs the reading's own held-out accuracy
    tasks = ["tank", "fr"]
    xx = np.arange(len(tasks))
    ceil = [results[t]["balanced_acc"] for t in tasks]
    read = [READING_ACC[t] for t in tasks]
    axs[1].bar(xx - 0.2, ceil, width=0.38, color="#9db9d8", label="surface features (confound ceiling)")
    axs[1].bar(xx + 0.2, read, width=0.38, color=BLUE, label="the reading (Box 1)")
    for x, v in zip(xx - 0.2, ceil):
        axs[1].text(x, v + 0.012, f"{v:.2f}", ha="center", fontsize=8, color=INK)
    for x, v in zip(xx + 0.2, read):
        axs[1].text(x, v + 0.012, f"{v:.2f}", ha="center", fontsize=8, color=INK)
    axs[1].axhline(0.5, color=MUT, lw=0.9, ls="--")
    axs[1].text(1.36, 0.505, "chance", fontsize=7.5, color=MUT, va="bottom")
    axs[1].set_xticks(xx); axs[1].set_xticklabels([TITLES[t] for t in tasks], fontsize=8.5)
    axs[1].set_ylim(0.44, 1.16)
    axs[1].set_ylabel("held-out class accuracy", fontsize=8.5, color=INK)
    axs[1].set_title("What surface features alone recover, vs the reading", fontsize=9.5, color=INK)
    axs[1].legend(fontsize=7.5, frameon=False, loc="upper center", ncol=1)

    for ax in axs:
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(colors=MUT, labelsize=8)
        ax.grid(True, lw=0.4, color=GRID, axis="x" if ax is axs[0] else "y")
        ax.set_axisbelow(True)
    fig.suptitle("Surface-feature confound baseline: how much of each class contrast a "
                 "surface classifier alone recovers", fontsize=10.5, color=INK)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGDIR / "fig_confound_features.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print("saved fig_confound_features.png")


def write_table(df: pd.DataFrame, results: dict, deltas: dict):
    lines = ["# Surface-feature confound baseline (v1 pools)", "",
             "Deterministic surface features only (feature_battery.py); no judgment tags.",
             "Cliff's delta is 2·AUC − 1 between the two classes (0 = full overlap, ±1 = full separation).",
             "The confound-ceiling classifier is a standardized logistic regression (class-weight",
             "balanced), leave-one-scene-pair-out (12 folds) — a stronger linear rule than the reading's",
             "own difference-of-means, so it is an upper bound on what surface features explain.",
             "Reading accuracies are the paper's Box 1 held-out values.", ""]
    for t in ("tank", "fr"):
        r = results[t]
        lines += [f"## {TITLES[t]}", "",
                  f"- Confound-ceiling balanced accuracy: **{r['balanced_acc']:.3f}** "
                  f"(AUC {r['auc']:.3f}; mean per-fold accuracy {r['mean_fold_acc']:.3f}; "
                  f"n={r['n']}, {CLASSES[t][0]} {r['n_a']} / {CLASSES[t][1]} {r['n_b']}).",
                  f"- The reading's held-out accuracy (Box 1): **{READING_ACC[t]:.3f}**.", "",
                  "| feature | Cliff's delta |", "|---|---|"]
        for f in sorted(SCALARS, key=lambda f: -abs(deltas[t][f])):
            lines.append(f"| {PRETTY[f]} | {deltas[t][f]:+.2f} |")
        lines.append("")
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    TABLE.write_text("\n".join(lines))
    print(f"wrote {TABLE}")


def main():
    df = pd.read_csv(CSV)
    results = {t: classify_task(df, t) for t in ("tank", "fr")}
    deltas = {t: per_feature_deltas(df, t) for t in ("tank", "fr")}
    for t in ("tank", "fr"):
        r = results[t]
        print(f"{t}: confound-ceiling balanced acc {r['balanced_acc']:.3f}, AUC {r['auc']:.3f}, "
              f"mean-fold {r['mean_fold_acc']:.3f}  vs reading {READING_ACC[t]:.3f}")
    figure(df, results, deltas)
    write_table(df, results, deltas)


if __name__ == "__main__":
    main()
