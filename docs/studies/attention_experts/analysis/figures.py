"""The attention-and-experts study's figures, from results/ (read-only; captures not worked out yet
are left out).

- shares_by_layer.png: for each capture's main split, attention's and the experts' total shares of
  the separation at every target layer, with the same shares for random splits (5th to 95th
  percentile, shaded) and the embedding's share;
- outside_bands.png: for every designed split, at how many of L4 to L20 attention's total share
  lies above or below its random band, along each direction, by capture (sets with context, then
  single words);
- two_directions.png: for each capture's main split, at every layer, attention's total share along
  the mean difference and along the shrinkage discriminant, each beside its random splits' band
  measured the same way;
- writing_layers.png: for three captures' main splits, which layers wrote attention's and the
  experts' parts of the split at each target layer;
- node_splits.png: for every capture's node splits, how many branches' attention share at the
  layer where they part lies above, inside or below its random band, along both directions.

Usage, from the repo root: .venv/bin/python docs/studies/attention_experts/analysis/figures.py
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import CAPTURES, CONTEXT, RESULTS, SINGLE_WORDS, figure_path  # noqa: E402

MAIN = {"tank": "vehicle against aquarium", "calibration": "vehicle against aquarium",
        "framing": "factual against roleplay", "words": "animal against the rest",
        "ontology": "danger: can kill against harmless", "objects": "harmful against benign",
        "friend_foe": "foe against friend"}
TITLES = {"tank": "tank senses (sentences)", "calibration": "tank: aquarium or vehicle (sentences)",
          "framing": "roleplay or factual framing (sentences)", "words": "single nouns: categories",
          "ontology": "single animal names", "objects": "single object names",
          "friend_foe": "friend or foe (agent runs, tick 1)"}
ATTENTION, EXPERTS, EMBEDDING, SECOND = "#5470c6", "#ee6666", "#888888", "#9a60b4"
WINDOW = (4, 20)  # the middle layers the counts look at
DIRECTIONS = ("mean difference", "discriminant")


def load(kind: str, name: str) -> Optional[Dict[str, Any]]:
    path = RESULTS / f"{kind}_{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def ordered() -> List[str]:
    return [name for name in (*CONTEXT, *SINGLE_WORDS) if name in CAPTURES]


def legend(axes: Any, n_used: int, **kwargs: Any) -> None:
    """The first panel's legend, in the first unused panel when there is one, so it covers no data."""
    handles, labels = axes.flat[0].get_legend_handles_labels()
    spare = axes.flat[n_used] if n_used < len(axes.flat) else None
    (spare or axes.flat[0]).legend(handles, labels, loc="center" if spare else "best", **kwargs)


def main_split(result: Dict[str, Any], name: str) -> Dict[str, Any]:
    wanted = MAIN.get(name)
    found = [s for s in result["splits"] if s["name"] == wanted]
    return found[0] if found else result["splits"][0]


def shares_by_layer() -> None:
    names = [n for n in ordered() if load("account", n)]
    cols = 2
    rows = (len(names) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(11, 2.9 * rows), squeeze=False, layout="constrained")
    for ax in axes.flat[len(names):]:
        ax.axis("off")
    for ax, name in zip(axes.flat, names):
        result = load("account", name)
        assert result is not None
        split = main_split(result, name)
        layers = [t["layer"] for t in split["targets"]]
        for key, colour, label in (("attention", ATTENTION, "attention"), ("experts", EXPERTS, "experts")):
            real = [t["shares"][key] for t in split["targets"]]
            low = [t["random"][key][0] for t in split["targets"]]
            high = [t["random"][key][2] for t in split["targets"]]
            ax.fill_between(layers, low, high, color=colour, alpha=0.15, linewidth=0)
            ax.plot(layers, real, color=colour, linewidth=1.8, label=f"{label} (shaded: random splits)")
        ax.plot(layers, [t["shares"]["embedding"] for t in split["targets"]], color=EMBEDDING, linestyle="--",
                linewidth=1, label="the read token's embedding")
        ax.set_title(f"{TITLES.get(name, name)}: {split['name']}", fontsize=9)
        ax.set_ylim(-0.2, 1.1)
        ax.set_xlim(0, max(layers))
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.2)
    legend(axes, len(names), fontsize=8)
    fig.supxlabel("target layer", fontsize=9)
    fig.supylabel("share of the separation written up to the target layer", fontsize=9)
    fig.savefig(figure_path("shares_by_layer"), dpi=150)
    plt.close(fig)


def measured(entry: Dict[str, Any], direction: str) -> Optional[Dict[str, Any]]:
    """A target's or branch's shares and random bands along one direction, or None when that
    direction wasn't measured."""
    return entry if direction == "mean difference" else entry.get("discriminant")


def two_directions() -> None:
    names = [n for n in ordered() if load("account", n)]
    cols = 2
    rows = (len(names) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(11, 2.6 * rows), squeeze=False, layout="constrained")
    for ax in axes.flat[len(names):]:
        ax.axis("off")
    for ax, name in zip(axes.flat, names):
        result = load("account", name)
        assert result is not None
        split = main_split(result, name)
        targets = [t for t in split["targets"] if "discriminant" in t]
        for direction, offset, colour, marker, label in (
                ("mean difference", -0.2, ATTENTION, "o", "along the mean difference (the node card's)"),
                ("discriminant", 0.2, SECOND, "D", "along the shrinkage discriminant")):
            xs = [t["layer"] + offset for t in targets]
            got = [measured(t, direction) for t in targets]
            bands = [m["random"]["attention"] for m in got if m]
            ax.vlines(xs, [b[0] for b in bands], [b[2] for b in bands], color=colour, alpha=0.35, linewidth=3)
            ax.scatter(xs, [b[1] for b in bands], marker="_", color=colour, s=25, linewidths=1)
            ax.scatter(xs, [m["shares"]["attention"] for m in got if m], marker=marker, color=colour, s=12, zorder=3,
                       label=label)
        ax.set_title(f"{TITLES.get(name, name)}: {split['name']}", fontsize=9)
        ax.set_xticks(range(0, 24, 4))
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.2)
    legend(axes, len(names), fontsize=8, title="attention's share (bars: random splits, 5th–95th)", title_fontsize=8)
    fig.supxlabel("target layer", fontsize=9)
    fig.supylabel("attention's share of the split up to the target layer", fontsize=9)
    fig.savefig(figure_path("two_directions"), dpi=150)
    plt.close(fig)


def outside_bands() -> None:
    names = [n for n in ordered() if load("account", n)]
    labels: List[str] = []
    counts: Dict[str, List[List[int]]] = {direction: [] for direction in DIRECTIONS}
    for name in names:
        result = load("account", name)
        assert result is not None
        for split in result["splits"]:
            middle = [t for t in split["targets"]
                      if WINDOW[0] <= t["layer"] <= WINDOW[1] and t["separation"] > t["null_95"]]
            if not middle:  # never beyond its separation null: left out, as in the note
                continue
            labels.append(f"{name}: {split['name']}")
            for direction in DIRECTIONS:
                got = [m for m in (measured(t, direction) for t in middle) if m]
                counts[direction].append([sum(m["shares"]["attention"] > m["random"]["attention"][2] for m in got),
                                          sum(m["shares"]["attention"] < m["random"]["attention"][0] for m in got)])
    y = np.arange(len(labels))
    span = WINDOW[1] - WINDOW[0] + 1
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.22 * len(labels) + 1.4), sharey=True, layout="constrained")
    for ax, direction in zip(axes, DIRECTIONS):
        above, below = (np.array(column) for column in zip(*counts[direction]))
        ax.barh(y, above, color=ATTENTION, label="attention writes more than in random splits")
        ax.barh(y, -below, color=EXPERTS, label="attention writes less (the experts more)")
        ax.set_xlim(-span, span)
        ax.axvline(0, color="#333333", linewidth=0.8)
        ax.set_title(f"along the {direction}", fontsize=9)
        ax.tick_params(axis="x", labelsize=7)
    axes[0].set_yticks(y, labels, fontsize=7)
    axes[0].invert_yaxis()
    axes[1].legend(fontsize=7, loc="lower right")
    fig.supxlabel(f"layers of L{WINDOW[0]}–L{WINDOW[1]} where attention's share is outside its random band", fontsize=8)
    fig.savefig(figure_path("outside_bands"), dpi=150)
    plt.close(fig)


def writing_layers() -> None:
    names = [n for n in ("tank", "friend_foe", "objects") if load("account", n)]
    if not names:
        return
    fig, axes = plt.subplots(len(names), 2, figsize=(10, 3.2 * len(names)), squeeze=False)
    for row, name in zip(axes, names):
        result = load("account", name)
        assert result is not None
        split = main_split(result, name)
        n = len(split["targets"])
        for ax, key, title in ((row[0], "attention_by_layer", "attention"), (row[1], "experts_by_layer", "experts")):
            grid = np.full((n, n), np.nan)
            for t, target in enumerate(split["targets"]):
                grid[t, :t + 1] = target["shares"][key]
            image = ax.imshow(grid, origin="lower", cmap="RdBu_r", vmin=-0.4, vmax=0.4, aspect="auto")
            ax.set_title(f"{TITLES.get(name, name)}: {split['name']}: {title}", fontsize=8)
            ax.set_xlabel("writing layer", fontsize=8)
            ax.set_ylabel("target layer", fontsize=8)
            ax.tick_params(labelsize=7)
            fig.colorbar(image, ax=ax, fraction=0.04).ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(figure_path("writing_layers"), dpi=150)
    plt.close(fig)


def node_splits() -> None:
    names = [n for n in ordered() if load("splits", n)]
    if not names:
        return
    counts: Dict[str, List[List[int]]] = {direction: [] for direction in DIRECTIONS}
    for name in names:
        result = load("splits", name)
        assert result is not None
        real = [b for b in result["branches"] if b["separation"] > b["null_95"]]
        for direction in DIRECTIONS:
            got = [measured(b, direction) for b in real]
            if not all(got):  # results from before the second direction
                counts[direction].append([0, 0, 0])
                continue
            above = sum(m["shares"]["attention_here"] > m["random"]["attention_here"][2] for m in got if m)
            below = sum(m["shares"]["attention_here"] < m["random"]["attention_here"][0] for m in got if m)
            counts[direction].append([above, len(real) - above - below, below])
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(9, 3.6), layout="constrained")
    for direction, shift, hatch in (("mean difference", -0.2, None), ("discriminant", 0.2, "///")):
        above, inside, below = (np.array(column) for column in zip(*counts[direction]))
        ax.bar(x + shift, above, width=0.38, color=ATTENTION, hatch=hatch, edgecolor="white", linewidth=0)
        ax.bar(x + shift, inside, width=0.38, bottom=above, color="#cccccc", hatch=hatch, edgecolor="white", linewidth=0)
        ax.bar(x + shift, below, width=0.38, bottom=above + inside, color=EXPERTS, hatch=hatch, edgecolor="white",
               linewidth=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ATTENTION, label="attention above its random band"),
                       Patch(color="#cccccc", label="inside"),
                       Patch(color=EXPERTS, label="below (the experts more)"),
                       Patch(facecolor="white", edgecolor="#555555", label="left: mean difference"),
                       Patch(facecolor="white", edgecolor="#555555", hatch="///", label="right: discriminant")],
              fontsize=7, ncols=2)
    ax.set_xticks(x, [TITLES.get(n, n) for n in names], fontsize=7, rotation=20, ha="right")
    ax.set_ylabel("branches beyond their separation null", fontsize=8)
    ax.set_title("Node splits: attention's share at the layer where the branch parts", fontsize=9)
    ax.tick_params(axis="y", labelsize=7)
    fig.savefig(figure_path("node_splits"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    shares_by_layer()
    two_directions()
    outside_bands()
    writing_layers()
    node_splits()
    print("figures in", figure_path("x").parent)
