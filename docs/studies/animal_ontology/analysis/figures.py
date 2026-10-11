"""The study's figures, from results/ (read-only; run after ways.py and held_out.py).

  figures/neighbours.png  agreement beyond chance of each axis with the 10 nearest neighbours, by
                          layer, in raw space and the lens's space; grey where the score is inside
                          the middle 95% of the shuffles (within each token count)
  figures/shares.png      each axis's share of the pairwise distances, as % of the variance the
                          controls (token count, name length) leave: fitted alone (top) and with
                          every other axis held fixed (bottom; grey where p >= 0.05, permutations)
  figures/held_out.png    κ on held-out orders for a linear probe and the lens's nodes; grey under
                          the decoy line
  figures/leading.png     the leading axis at each layer for each measure, coloured by its way

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/figures.py
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from ontology_common import AXES, AXIS_NAMES, RESULTS, WAY_OF_AXIS, figure_path  # noqa: E402

WAYS = ["descent", "everyday kind", "body covering", "size", "legs", "where people meet it",
        "relation to people", "danger and feeling", "way of life"]
WAY_COLOURS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1",
               "#ff9da7", "#9c755f"]
GREY = "#d9d9d9"


def load(name: str) -> Optional[Dict[str, Any]]:
    path = RESULTS / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def heatmap(ax: Any, values: np.ndarray, faded: np.ndarray, rows: List[str], title: str,
            vmax: float, unit: str) -> Any:
    cmap = matplotlib.colormaps["viridis"].copy()
    shown = np.ma.masked_array(values, mask=faded)
    ax.imshow(np.where(faded, 1, np.nan), cmap=ListedColormap([GREY]), aspect="auto", vmin=0, vmax=1)
    image = ax.imshow(shown, cmap=cmap, aspect="auto", vmin=0, vmax=vmax)
    ax.set_yticks(range(len(rows)), rows, fontsize=8)
    ax.set_xticks(range(0, values.shape[1], 2), [f"L{i}" for i in range(0, values.shape[1], 2)], fontsize=7)
    ax.set_title(title, fontsize=10)
    bar = plt.colorbar(image, ax=ax, fraction=0.035, pad=0.02)
    bar.set_label(unit, fontsize=8)
    bar.ax.tick_params(labelsize=7)
    return image


def neighbours_figure(spaces: Dict[str, Dict[str, Any]]) -> None:
    fig, axes = plt.subplots(1, len(spaces), figsize=(7 * len(spaces), 5.2), constrained_layout=True)
    axes = np.atleast_1d(axes)
    rows = [AXIS_NAMES[a] for a in AXES]
    grids = {}
    for space, result in spaces.items():
        score = np.array([[layer["neighbours"][a]["score"] for layer in result["layers"]] for a in AXES])
        upper = np.array([[layer["neighbours"][a]["band"][1] for layer in result["layers"]] for a in AXES])
        grids[space] = (score, score <= upper)
    vmax = max(float(np.nanmax(s)) for s, _ in grids.values())
    for ax, (space, (score, faded)) in zip(axes, grids.items()):
        heatmap(ax, score, faded, rows, f"Neighbours sharing the value, beyond chance ({space} space)",
                vmax, "agreement beyond chance")
    fig.suptitle("Which axes an animal's 10 nearest neighbours share, by layer "
                 "(grey: inside the shuffles' middle 95%, within each token count)", fontsize=11)
    fig.savefig(figure_path("neighbours"), dpi=150)
    plt.close(fig)


def shares_figure(spaces: Dict[str, Dict[str, Any]], alone: Dict[str, Dict[str, Any]]) -> None:
    """Top: each axis alone over the controls; bottom: its own share, the others held fixed. Both
    as % of the variance the controls leave, so the gap is what an axis shares with the others."""
    names = [s for s in spaces if s in alone]
    fig, axes = plt.subplots(2, len(names), figsize=(7 * len(names), 9.6), constrained_layout=True,
                             squeeze=False)
    rows = [AXIS_NAMES[a] for a in AXES]
    for col, space in enumerate(names):
        left = np.array([1.0 - layer["r2_controls"] for layer in alone[space]["layers"]])
        by_alone = 100 * np.array([[layer["alone"][a] for layer in alone[space]["layers"]] for a in AXES])
        own = 100 * np.array([[layer["own_share"][a]["share"] for layer in spaces[space]["layers"]]
                              for a in AXES]) / left
        p = np.array([[layer["own_share"][a]["p"] for layer in spaces[space]["layers"]] for a in AXES])
        heatmap(axes[0, col], by_alone, np.zeros_like(by_alone, dtype=bool), rows,
                f"Each axis alone ({space} space)", float(by_alone.max()), "% of what the controls leave")
        heatmap(axes[1, col], own, p >= 0.05, rows,
                f"Each axis with the others held fixed ({space} space)", float(own.max()),
                "% of what the controls leave")
    fig.suptitle("How much of the distance between two animals each axis explains, beyond the token "
                 "count and name length (grey: p ≥ 0.05, 1,000 permutations within each token count)",
                 fontsize=11)
    fig.savefig(figure_path("shares"), dpi=150)
    plt.close(fig)


def held_out_figure(result: Dict[str, Any]) -> None:
    present = {("group" if a == "label" else a): a for a in result["attributes"] if a != "tokens"}
    attributes = [present[a] for a in AXES if a in present]  # in the order of the ways
    names = [AXIS_NAMES["group" if a == "label" else a] for a in attributes]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.0), constrained_layout=True)
    for ax, reader, title in ((axes[0], "probe", "a linear probe"), (axes[1], "lens", "the lens's nodes")):
        kappa = np.array([[layer[a] if layer[a] is not None else np.nan for layer in result[reader]]
                          for a in attributes])
        line = np.array([result[f"{reader}_line"][a] for a in attributes])[:, None]
        heatmap(ax, np.clip(kappa, 0, None), ~(kappa > line), names,
                f"Read on orders never seen: {title}", 1.0, "κ (agreement beyond chance)")
    fig.suptitle("How well each axis is read on held-out taxonomic orders, by layer "
                 "(grey: under the decoy line)", fontsize=11)
    fig.savefig(figure_path("held_out"), dpi=150)
    plt.close(fig)


def leading_figure(spaces: Dict[str, Dict[str, Any]], alone: Dict[str, Dict[str, Any]],
                   held: Optional[Dict[str, Any]]) -> None:
    rows: List[tuple] = []  # (label, leading axis per layer, whether each lead is beyond chance)
    for space, result in spaces.items():
        lead = [layer["leading"]["neighbours"]["axis"] for layer in result["layers"]]
        rows.append((f"neighbours, {space}", lead,
                     [layer["neighbours"][a]["score"] > layer["neighbours"][a]["band"][1]
                      for layer, a in zip(result["layers"], lead)]))
        if space in alone:
            lead = [max(AXES, key=lambda a: layer["alone"][a]) for layer in alone[space]["layers"]]
            rows.append((f"alone, {space}", lead, [True] * len(lead)))
        lead = [layer["leading"]["own_share"]["axis"] for layer in result["layers"]]
        rows.append((f"own share, {space}", lead,
                     [layer["own_share"][a]["p"] < 0.05 for layer, a in zip(result["layers"], lead)]))
    if held:
        for reader, label in (("probe", "held out, probe"), ("lens", "held out, lens nodes")):
            leads, beyond = [], []
            for layer in held[reader]:
                scores = {a: v for a, v in layer.items() if a != "tokens" and v is not None}
                best = max(scores, key=scores.get)
                leads.append("group" if best == "label" else best)
                beyond.append(scores[best] > held[f"{reader}_line"][best])
            rows.append((label, leads, beyond))
    n_layers = max(len(r[1]) for r in rows)
    fig, ax = plt.subplots(figsize=(15, 0.55 * len(rows) + 1.6), constrained_layout=True)
    for y, (label, leads, beyond) in enumerate(rows):
        for x, (axis, real) in enumerate(zip(leads, beyond)):
            way = WAY_OF_AXIS[axis]
            colour = WAY_COLOURS[WAYS.index(way)] if real else GREY
            ax.add_patch(plt.Rectangle((x, y), 0.96, 0.9, color=colour))
            dark = real and way in ("descent", "body covering", "relation to people", "way of life")
            ax.text(x + 0.48, y + 0.45, AXIS_NAMES[axis].split(" (")[0][:9], ha="center", va="center",
                    fontsize=5.5, color="white" if dark else "black")
    ax.set_xlim(0, n_layers)
    ax.set_ylim(len(rows), 0)
    ax.set_yticks([y + 0.45 for y in range(len(rows))], [r[0] for r in rows], fontsize=8)
    ax.set_xticks([x + 0.48 for x in range(0, n_layers, 2)], [f"L{x}" for x in range(0, n_layers, 2)], fontsize=7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(handles=[Patch(color=c, label=w) for w, c in zip(WAYS, WAY_COLOURS)], ncol=5, fontsize=7,
              loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
    ax.set_title("The axis that leads at each layer, by measure, coloured by its way "
                 "(grey: the lead is not beyond chance)", fontsize=10)
    fig.savefig(figure_path("leading"), dpi=150)
    plt.close(fig)


def main() -> None:
    spaces = {space: r for space in ("raw", "lens") if (r := load(f"ways_{space}"))}
    alone = {space: r for space in ("raw", "lens") if (r := load(f"alone_{space}"))}
    held = load("held_out")
    if spaces:
        neighbours_figure(spaces)
        shares_figure(spaces, alone)
    if held:
        held_out_figure(held)
    if spaces:
        leading_figure(spaces, alone, held)
    print("figures written to", figure_path("x").parent)


if __name__ == "__main__":
    main()
