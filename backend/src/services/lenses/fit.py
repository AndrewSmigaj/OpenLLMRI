"""Fitting one layer of a UMAP lens, cutting its Ward tree at any k, and suggesting k.

A layer is fitted once. Its Ward tree is saved whole, so every k is a cut of the same tree and a
new k needs no refit. Settings and seeds match today's clusterings (UMAP seed 42, min_dist 0.1,
n_neighbors clamped to the item count), so a lens reproduces a clustering built the old way.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.metrics import silhouette_score

Array = np.ndarray[Any, Any]


def _neighbours(n_neighbors: int, n_items: int) -> int:
    return max(2, min(n_neighbors, n_items - 1))


def fit_reducer(states: Array, n_neighbors: int, dimensions: int, seed: int,
                min_dist: float = 0.1) -> Tuple[Any, Array]:
    """The layer's UMAP, saved with the lens, and its embedding [N, dims] float32 (validation
    refits it per fold)."""
    import umap

    n = _neighbours(n_neighbors, len(states))
    dims = max(1, min(dimensions, len(states) - 1, states.shape[1]))
    reducer = umap.UMAP(n_components=dims, n_neighbors=n, min_dist=min_dist, random_state=seed).fit(states)
    return reducer, np.asarray(reducer.embedding_, dtype=np.float32)


def ward_tree(embedding: Array) -> Array:
    return np.asarray(linkage(embedding, "ward"), dtype=np.float64)


def cut(tree: Array, k: int) -> Array:
    """Node ids 0..k-1 for a cut of the tree, numbered by first appearance in item order."""
    raw = fcluster(tree, t=k, criterion="maxclust")
    first: Dict[int, int] = {}
    for label in raw:
        first.setdefault(int(label), len(first))
    return np.array([first[int(label)] for label in raw], dtype=np.int16)


def suggest_k(embedding: Array, tree: Array, k_max: int = 10,
              level_ratio: float = 1.5, min_share: float = 0.02) -> Dict[str, Any]:
    """In-sample suggestions for one layer, each named by its method.

    - elbow: the k after which the within-cluster sum of squares stops falling steeply;
    - silhouette: the k with the best silhouette;
    - levels: every k where the tree has a clear level: the merge into k-1 clusters is at least
      `level_ratio` times the merge into k, and every cluster holds at least `min_share` of the
      items (for example 2 and 5 when five clusters pair into two groups).

    These are suggestions; the k profile (validation) shows how each k agrees with the designed
    axes. On the tank set, elbow chose 2 and silhouette wandered (plan review, 2026-10-08).
    """
    n = len(embedding)
    top = max(2, min(k_max, n - 1))
    heights = tree[::-1, 2]  # heights[j] is the merge from j+2 clusters into j+1
    cuts = {k: cut(tree, k) for k in range(1, top + 1)}
    sse = np.array([sum(float(((embedding[c == j] - embedding[c == j].mean(0)) ** 2).sum())
                        for j in np.unique(c)) for c in cuts.values()])
    elbow = int(np.argmax(sse[:-2] - 2 * sse[1:-1] + sse[2:])) + 2 if top >= 3 else 2
    silhouettes = {k: float(silhouette_score(embedding, cuts[k])) for k in range(2, top + 1)}
    levels: List[int] = []
    for k in range(2, top + 1):
        if k - 1 < len(heights) and heights[k - 1] > 0 and heights[k - 2] / heights[k - 1] >= level_ratio:
            if np.bincount(cuts[k]).min() >= min_share * n:
                levels.append(k)
    return {
        "elbow": elbow,
        "silhouette": max(silhouettes, key=lambda k: silhouettes[k]),
        "levels": levels,
        "silhouette_by_k": {str(k): round(v, 4) for k, v in silhouettes.items()},
    }


def mass_mean_axis(states: Array, is_b: Array) -> Tuple[Array, Array, float]:
    """A contrast's axis at one layer: the difference of the two classes' mean states (B minus A),
    their midpoint, and the axis's squared length."""
    mean_a, mean_b = states[~is_b].mean(axis=0), states[is_b].mean(axis=0)
    axis = (mean_b - mean_a).astype(np.float32)
    return axis, ((mean_a + mean_b) / 2).astype(np.float32), float(axis @ axis)


def mass_mean_reading(states: Array, axis: Array, mid: Array, norm2: float) -> Array:
    """Positions along the axis, scaled so the class means land at -1 and +1:
    2 (x - mid) . axis / |axis|^2 (the paper's formula, and the retired raw-axis endpoint's)."""
    reading: Array = 2.0 * ((states - mid) @ axis) / max(norm2, 1e-12)
    return reading
