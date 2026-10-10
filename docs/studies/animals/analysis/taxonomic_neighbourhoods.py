"""Taxonomic neighbourhoods, layer by layer (the animal study, 10d.5).

For every animal and layer: the share of its 10 nearest neighbours that share its group, and its
phylum, class, order, family and genus. A rank counts only the neighbours that have that rank, for
animals that have it (a bat has no family). Averaged over the animals, each share sits beside its
chance level: the same average with the animals' taxonomy shuffled over the same neighbours, 200
times (the line is the shuffles' mean, the band their middle 95%).

Two spaces: the lens's own embedding (where its nodes are cut), and the residual stream in the
validation's raw recipe (standardized, 50 principal components).

  .venv/bin/python docs/studies/animals/analysis/taxonomic_neighbourhoods.py SESSION LENS
"""
from __future__ import annotations

import sys

import numpy as np
from common import (
    NEIGHBOURS,
    RANKS,
    SEED,
    band,
    figure_path,
    lens_embedding,
    lens_items,
    neighbours,
    raw_layers,
    write_results,
)

LEVELS = ("group",) + RANKS
SHUFFLES = 200


def values_of(items):
    """{level: [items] integer codes, -1 where the animal has no taxon at that rank}."""
    out = {}
    for level in LEVELS:
        names = [it["entry"]["group"] if level == "group" else it["entry"]["taxonomy"][level] for it in items]
        codes = {name: i for i, name in enumerate(sorted({n for n in names if n}))}
        out[level] = np.array([codes[n] if n else -1 for n in names], dtype=np.int64)
    return out


def shared_share(nn: np.ndarray, values: np.ndarray) -> float:
    """The mean, over animals with a value, of the share of their neighbours with a value that
    share it."""
    theirs = values[nn]
    counted = theirs >= 0
    same = (theirs == values[:, None]) & counted
    n = counted.sum(axis=1)
    keep = (values >= 0) & (n > 0)
    return float(np.mean(same.sum(axis=1)[keep] / n[keep])) if keep.any() else float("nan")


def level_scores(nn: np.ndarray, vals, rng) -> dict:
    out = {}
    for level in LEVELS:
        observed = shared_share(nn, vals[level])
        null = np.array([shared_share(nn, rng.permutation(vals[level])) for _ in range(SHUFFLES)])
        out[level] = {"observed": observed, "chance": float(null.mean()), "band": band(null)}
    return out


def main(session: str, lens: str) -> None:
    items = lens_items(session, lens)
    vals = values_of(items)
    embedding = lens_embedding(session, lens)
    layers = list(range(embedding.shape[0]))
    raw = raw_layers(session, [it["probe_id"] for it in items], layers)
    rng = np.random.default_rng(SEED)
    results = {"session": session, "lens": lens, "items": len(items), "neighbours": NEIGHBOURS,
               "shuffles": SHUFFLES, "levels": list(LEVELS),
               "counted": {level: int((vals[level] >= 0).sum()) for level in LEVELS},
               "spaces": {"lens": {}, "raw": {}}}
    for layer in layers:
        results["spaces"]["lens"][layer] = level_scores(neighbours(embedding[layer]), vals, rng)
        results["spaces"]["raw"][layer] = level_scores(neighbours(raw[layer]), vals, rng)
        print(f"L{layer:02d} lens " + " ".join(f"{lv} {results['spaces']['lens'][layer][lv]['observed']:.2f}" for lv in LEVELS))
    path = write_results(f"taxonomic_neighbourhoods_{lens}", results)
    chart(results, lens)
    print(f"wrote {path}")


def chart(results: dict, lens: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colours = dict(zip(LEVELS, ("#6b7280", "#1d4ed8", "#0891b2", "#059669", "#d97706", "#dc2626")))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
    for ax, space, title in zip(axes, ("lens", "raw"), ("the lens's embedding", "raw: standardized, 50 PCs")):
        by_layer = results["spaces"][space]
        layers = sorted(int(k) for k in by_layer)
        for level in LEVELS:
            obs = [by_layer[layer][level]["observed"] for layer in layers]
            chance = [by_layer[layer][level]["chance"] for layer in layers]
            ax.plot(layers, obs, color=colours[level], lw=2, label=level)
            ax.plot(layers, chance, color=colours[level], lw=1, ls=":")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("layer")
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.25)
    axes[0].set_ylabel(f"share of {results['neighbours']} nearest neighbours sharing it")
    axes[1].legend(title="shared", fontsize=9, loc="upper right")
    fig.suptitle(f"Taxonomic neighbourhoods: {lens} ({results['items']} animals; dotted: shuffled taxonomy)", fontsize=12)
    fig.tight_layout()
    fig.savefig(figure_path(f"taxonomic_neighbourhoods_{lens}"), dpi=150)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
