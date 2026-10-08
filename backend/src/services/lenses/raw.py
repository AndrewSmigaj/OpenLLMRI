"""Raw space beside UMAP: the groupings of the fair comparison (DESIGN.md C4).

Each grouping is fitted on a fold's training items and gives (training features, held-out
features, the training items' cluster at every k), so held-out items are assigned exactly as
for UMAP lenses: by a vote of their nearest training items in that grouping's own space.

- **raw Ward:** centred and standardized states, reduced to 50 principal components, Ward;
- **raw spectral:** the same 50 components, a nearest-neighbour graph, its spectral embedding
  computed once, then k-means on the first k eigenvectors for every k;
- **relevant neurons:** the neurons whose values best separate the labels (ANOVA F), chosen inside
  the training fold, reduced to 10 components, Ward. It uses the labels, so it is compared only
  with the ceiling;
- **the ceiling:** logistic regression on the standardized states, trained on the labels: how
  separable the classes are at all, never a competitor.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

Array = np.ndarray[Any, Any]

RAW_PCS = 50
NEURONS = 200
NEURON_PCS = 10
SPECTRAL_EIGENVECTORS = 10


def pca_features(train: Array, test: Array, seed: int, components: int = RAW_PCS) -> Tuple[Array, Array]:
    """Standardized on the training items, then their principal components, for both sets."""
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler().fit(train)
    n = max(1, min(components, train.shape[0] - 1, train.shape[1]))
    pca = PCA(n_components=n, random_state=seed).fit(scaler.transform(train))
    return (np.asarray(pca.transform(scaler.transform(train)), dtype=np.float32),
            np.asarray(pca.transform(scaler.transform(test)), dtype=np.float32))


def ward_cuts(features: Array, ks: List[int]) -> Dict[int, Array]:
    from services.lenses.fit import cut, ward_tree

    tree = ward_tree(features)
    return {k: cut(tree, k) for k in ks}


def spectral_cuts(features: Array, ks: List[int], n_neighbors: int, seed: int) -> Dict[int, Array]:
    """Spectral clustering at every k from one embedding: k-means on its first k eigenvectors."""
    from sklearn.cluster import KMeans
    from sklearn.manifold import spectral_embedding
    from sklearn.neighbors import kneighbors_graph

    graph = kneighbors_graph(features, n_neighbors=max(2, min(n_neighbors, len(features) - 1)), include_self=False)
    graph = 0.5 * (graph + graph.T)
    vectors = spectral_embedding(graph, n_components=min(max(ks), SPECTRAL_EIGENVECTORS, len(features) - 1),
                                 drop_first=False, random_state=seed)
    return {k: KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(vectors[:, :min(k, vectors.shape[1])])
            for k in ks}


def relevant_neurons(train: Array, labels: Array, count: int = NEURONS) -> Array:
    """The neurons whose values best separate the labels (ANOVA F), from the given items only."""
    from sklearn.feature_selection import f_classif

    scores = np.nan_to_num(f_classif(train, labels)[0], nan=0.0)
    chosen: Array = np.argsort(-scores, kind="stable")[:count]
    return chosen


def neuron_features(train: Array, test: Array, labels: Array, seed: int) -> Tuple[Array, Array]:
    """The relevant neurons, chosen from the training items' labels only (-1: no label), reduced to
    10 components. Choosing them with the held-out labels would leak them into the score."""
    known = labels >= 0
    keep = relevant_neurons(train[known], labels[known])
    return pca_features(train[:, keep], test[:, keep], seed, NEURON_PCS)


def ceiling(train: Array, labels: Array, test: Array, seed: int) -> Array:
    """Logistic regression's predictions for the held-out items."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler().fit(train)
    model = LogisticRegression(max_iter=2000, random_state=seed).fit(scaler.transform(train), labels)
    predicted: Array = model.predict(scaler.transform(test))
    return predicted


MARK_BELOW = 0.5  # an item is marked when its co-members in the two groupings overlap less than this


def co_member_overlap(umap_nodes: Array, raw_clusters: Array) -> Array:
    """Each item's Jaccard overlap between the items sharing its UMAP node and those sharing its raw
    cluster: n_uv / (n_u + n_v - n_uv) from the two groupings' contingency table."""
    u = np.unique(umap_nodes, return_inverse=True)[1]
    v = np.unique(raw_clusters, return_inverse=True)[1]
    table = np.zeros((u.max() + 1, v.max() + 1))
    np.add.at(table, (u, v), 1)
    both = table[u, v]
    overlap: Array = both / (table.sum(axis=1)[u] + table.sum(axis=0)[v] - both)
    return overlap


def lens_marks(view: Any, folder: Path) -> Optional[Dict[str, Any]]:
    """Where a UMAP lens and raw space disagree, per layer: the items whose co-members in the
    lens's node and in the better raw grouping at the same k overlap less than MARK_BELOW
    (Jaccard), and how many sit in each node. None until the lens is validated (the raw
    groupings come from its validation)."""
    import json
    from collections import Counter

    if not (folder / "raw_cuts.npz").exists() or not (folder / "validation.json").exists():
        return None
    cuts = np.load(folder / "raw_cuts.npz")
    ks = [int(k) for k in cuts["ks"]]
    comparison = json.loads((folder / "validation.json").read_text(encoding="utf-8")).get("comparison", {})
    out: Dict[str, Any] = {"threshold": MARK_BELOW, "layers": {}}
    for li, layer in enumerate(view.layers):
        k = int(view.nodes[:, li].max()) + 1
        if k not in ks:
            continue
        scored = comparison.get(str(layer), {})
        best = max(("raw_ward", "raw_spectral"),
                   key=lambda m: (scored.get(m, {}).get(str(k)) or {}).get("kappa", -1.0))
        overlap = co_member_overlap(view.nodes[:, li], cuts[best][li, ks.index(k)])
        marked = np.flatnonzero(overlap < MARK_BELOW)
        nodes = Counter(int(view.nodes[i, li]) for i in marked)
        out["layers"][str(layer)] = {"method": best, "k": k, "marked": [view.items[int(i)]["probe_id"] for i in marked],
                                     "nodes": {f"L{layer}C{node}": n for node, n in sorted(nodes.items())}}
    return out
