"""Charts from results/summary.json (`summary.py`).

- `best_k_by_layer.png`: per capture, the UMAP lens's best held-out kappa minus each raw grouping's,
  the median over its attributes and over its crossed pairs, layer by layer;
- `scatter.png`: every cell (capture, attribute or pair, layer), the UMAP lens's best kappa against
  the better raw grouping's, by kind;
- `heatmap_<capture>.png`: per attribute and pair, the difference from raw Ward and from raw
  spectral at each method's best k, layer by layer.

  .venv/bin/python docs/studies/umap_vs_raw/analysis/figures.py
"""
from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import FIGURES, METHODS, RESULTS  # noqa: E402

RAW = METHODS[1:]
NAMES = {"raw_ward": "raw Ward", "raw_spectral": "raw spectral"}
KIND_COLOURS = {"attribute": "#1f5f8b", "crossed pair": "#c0532b", "correlated pair": "#8a8a8a"}


def best_diff(cell: dict, method: str) -> float:
    return float(cell["best"]["umap"]["kappa"] - cell["best"][method]["kappa"])


def by_layer(summary: dict, kind: str, method: str) -> tuple[list[int], list[float]]:
    layers = sorted({int(layer) for cells in summary["codes"].values() for layer in cells})
    medians = []
    for layer in layers:
        found = [best_diff(cells[str(layer)], method) for code, cells in summary["codes"].items()
                 if summary["kinds"][code] == kind]
        medians.append(float(np.median(found)) if found else np.nan)
    return layers, medians


def main() -> None:
    data = json.loads((RESULTS / "summary.json").read_text())
    captures = data["captures"]
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=True)
    for ax, (name, summary) in zip(axes.ravel(), captures.items()):
        for method, style in zip(RAW, ("-", "--")):
            for kind in ("attribute", "crossed pair"):
                layers, medians = by_layer(summary, kind, method)
                if not np.all(np.isnan(medians)):
                    ax.plot(layers, medians, style, color=KIND_COLOURS[kind], label=f"{kind}s, vs {NAMES[method]}")
        ax.axhline(0, color="black", lw=0.8)
        ax.axhspan(-0.05, 0.05, color="#dddddd", zorder=0)
        ax.set_title(f"{name} ({summary['items']} items)")
        ax.set_xlabel("layer")
    axes[0, 0].set_ylabel("UMAP best κ − raw best κ (median)")
    axes[1, 0].set_ylabel("UMAP best κ − raw best κ (median)")
    handles, labels = axes.ravel()[2].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4)
    fig.suptitle("Held-out κ, each method at its best k: the UMAP lens against raw space (above 0: UMAP ahead)")
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    fig.savefig(FIGURES / "best_k_by_layer.png", dpi=130)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
    for ax, kind in zip(axes, ("attribute", "crossed pair", "correlated pair")):
        xs, ys = [], []
        for summary in captures.values():
            for code, cells in summary["codes"].items():
                if summary["kinds"][code] != kind:
                    continue
                for cell in cells.values():
                    xs.append(max(cell["best"][m]["kappa"] for m in RAW))
                    ys.append(cell["best"]["umap"]["kappa"])
        ax.scatter(xs, ys, s=6, alpha=0.35, color=KIND_COLOURS[kind])
        ax.plot([-0.2, 1], [-0.2, 1], color="black", lw=0.8)
        ax.set_title(f"{kind}s ({len(xs)} cells)")
        ax.set_xlabel("better raw grouping, best κ")
    axes[0].set_ylabel("UMAP lens, best κ")
    fig.suptitle("Every capture, attribute or pair, and layer (above the line: UMAP ahead)")
    fig.tight_layout()
    fig.savefig(FIGURES / "scatter.png", dpi=130)
    plt.close(fig)

    for name, summary in captures.items():
        codes = [c for c in summary["codes"] if summary["kinds"][c] != "correlated pair"]
        layers = sorted({int(layer) for cells in summary["codes"].values() for layer in cells})
        fig, axes = plt.subplots(1, 2, figsize=(14, 1.2 + 0.22 * len(codes)), sharey=True)
        for ax, method in zip(axes, RAW):
            grid = np.array([[best_diff(summary["codes"][c][str(layer)], method) for layer in layers] for c in codes])
            image = ax.imshow(grid, cmap="RdBu", vmin=-0.4, vmax=0.4, aspect="auto")
            ax.set_xticks(range(len(layers)), [str(layer) for layer in layers], fontsize=7)
            ax.set_yticks(range(len(codes)), codes, fontsize=7)
            ax.set_title(f"UMAP − {NAMES[method]} (best k each)")
            ax.set_xlabel("layer")
        fig.colorbar(image, ax=axes, shrink=0.8, label="held-out κ difference (blue: UMAP ahead)")
        fig.suptitle(f"{name}: attributes and crossed pairs")
        fig.savefig(FIGURES / f"heatmap_{name}.png", dpi=130, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
