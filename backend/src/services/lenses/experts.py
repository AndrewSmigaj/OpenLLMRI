"""Experts across a lens's layers: one fixed vertical order for the expert Sankey, and fingerprints.

The order is computed once from the pooled flows of all four ranks and kept for every rank and
condition, so a difference between two charts is real rather than layout (DESIGN.md: expert
Sankeys keep one layout). It is a layered barycentre ordering (Sugiyama's heuristic): sweeps
down and up the layers place each expert at the weighted mean position of the experts its items
come from or go to, keeping the order with the fewest weighted crossings.

A fingerprint is a population's mean gate weight on each expert at each layer, from the model's
own top-four weights, so each layer's row sums to 1.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from services.lenses.view import Array, LensView

N_EXPERTS = 32  # gpt-oss-20b's experts per layer


def _n_experts(view: LensView) -> int:
    return max(N_EXPERTS, int(view.experts.max()) + 1) if view.experts.size else N_EXPERTS


def rank_flows(view: LensView) -> Array:
    """[R, L-1, E, E]: at each rank, how many items go from expert a at a layer to expert b at the
    next (rank r to rank r): what each rank's chart draws."""
    n = _n_experts(view)
    ranks, layers = view.experts.shape[2], view.experts.shape[1]
    flows = np.zeros((ranks, max(0, layers - 1), n, n))
    for r in range(ranks):
        for li in range(layers - 1):
            np.add.at(flows[r, li], (view.experts[:, li, r], view.experts[:, li + 1, r]), 1)
    return flows


def pooled_flows(view: LensView) -> Array:
    """[L-1, E, E]: the four ranks' flows added together."""
    pooled: Array = rank_flows(view).sum(axis=0)
    return pooled


def chart_crossings(flows: Array, order: List[List[int]]) -> float:
    """The crossings every rank's chart would draw in this order, added up. (Crossings between two
    ranks' flows don't count: no chart shows two ranks.)"""
    return sum(crossings(flows[r, li], order[li], order[li + 1])
               for r in range(flows.shape[0]) for li in range(flows.shape[1]))


def crossings(flow: Array, left: List[int], right: List[int]) -> float:
    """Weighted crossings between two columns in the given orders: for every pair of flows that
    cross, the product of their sizes."""
    w = flow[np.ix_(left, right)]  # rows and columns in drawing order
    # beyond[a, b]: the flow leaving rows above a for columns below b
    above = np.cumsum(w, axis=0) - w
    beyond = np.flip(np.cumsum(np.flip(above, axis=1), axis=1), axis=1) - above
    return float((w * beyond).sum())


def _reorder(flow: Array, fixed: List[int], current: List[int], downward: bool) -> List[int]:
    """One column ordered by the weighted mean position of its partners in the fixed column;
    experts without flow keep their place after the others."""
    n = flow.shape[0]
    pos = np.empty(n)
    pos[fixed] = np.arange(n)
    w = flow if downward else flow.T  # rows: the fixed column; columns: the one being ordered
    weight = w.sum(axis=0)
    centre = np.where(weight > 0, (pos @ w) / np.maximum(weight, 1e-12), np.inf)
    previous = np.empty(n)
    previous[current] = np.arange(n)
    return [int(e) for e in np.lexsort((previous, centre))]


def _transpose(order: List[List[int]], flows: Array, used: List[Array], passes: int = 8) -> None:
    """Swap neighbours in a column while that cuts the ranks' crossings on both sides (flows are
    per rank: [R, L-1, E, E])."""
    layers = len(order)
    for _ in range(passes):
        improved = False
        for li in range(layers):
            # each rank's flows to the neighbouring columns: rows by expert id, columns in drawing order
            sides = [m for r in range(flows.shape[0]) for m in
                     ([flows[r, li - 1].T[:, order[li - 1]]] if li > 0 else []) +
                     ([flows[r, li][:, order[li + 1]]] if li < layers - 1 else [])]
            column = order[li]
            for j in range(len(column) - 1):
                u, v = column[j], column[j + 1]
                if not (used[li][u] or used[li][v]):
                    continue
                # u above v: their flows cross where u's partner sits below v's
                above = sum(float(m[u] @ (np.cumsum(m[v]) - m[v])) for m in sides)
                below = sum(float(m[v] @ (np.cumsum(m[u]) - m[u])) for m in sides)
                if below < above:
                    column[j], column[j + 1] = v, u
                    improved = True
        if not improved:
            return


def _spectral_start(flows: Array, used: List[Array]) -> List[List[int]]:
    """A starting order from the whole layered graph: each connected component laid out by its
    Fiedler vector (the second eigenvector of its normalized Laplacian), which keeps chains of
    flow in order; components stack, largest first; unused experts go last."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components, laplacian

    layers, n = len(used), flows.shape[1] if flows.size else N_EXPERTS
    index = {(li, e): k for k, (li, e) in enumerate((li, int(e)) for li in range(layers)
                                                     for e in np.flatnonzero(used[li]))}
    rows: List[int] = []
    cols: List[int] = []
    vals: List[float] = []
    for li in range(layers - 1):
        a, b = np.nonzero(flows[li])
        for x, y in zip(a, b):
            if (li, x) in index and (li + 1, y) in index:
                rows.append(index[(li, int(x))])
                cols.append(index[(li + 1, int(y))])
                vals.append(float(flows[li][x, y]))
    size = len(index)
    graph = coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()
    graph = graph + graph.T
    count, labels = connected_components(graph, directed=False)
    key = np.zeros(size)
    sizes = np.bincount(labels, minlength=count)
    for rank, comp in enumerate(np.argsort(-sizes, kind="stable")):
        members = np.flatnonzero(labels == comp)
        position = np.zeros(len(members))
        if len(members) > 2:
            lap = laplacian(graph[members][:, members].toarray(), normed=True)
            position = np.linalg.eigh(lap)[1][:, 1]
            position = (position - position.min()) / max(np.ptp(position), 1e-12)  # 0 to 1
        key[members] = rank + position * 0.999  # components stay apart
    starts: List[List[int]] = []
    for li in range(layers):
        mine = [(key[index[(li, int(e))]], int(e)) for e in np.flatnonzero(used[li])]
        rest = [int(e) for e in range(n) if not used[li][e]]
        starts.append([e for _, e in sorted(mine)] + rest)
    return starts


def expert_order(view: LensView, sweeps: int = 4) -> List[List[int]]:
    """Each layer's experts top to bottom (all of them, by id): one order for every rank."""
    per_rank = rank_flows(view)
    flows = per_rank.sum(axis=0)  # the barycentres average over every rank's flows
    n = _n_experts(view)
    layers = view.experts.shape[1]
    load = [np.bincount(view.experts[:, li, :].ravel(), minlength=n) for li in range(layers)]
    used = [lo > 0 for lo in load]

    def total(o: List[List[int]]) -> float:
        return chart_crossings(per_rank, o)

    best: List[List[int]] = []
    best_cost = np.inf
    starts = (_spectral_start(flows, used),
              [[int(e) for e in np.argsort(-load[li], kind="stable")] for li in range(layers)])
    for start in starts:
        order = [column[:] for column in start]
        for _ in range(sweeps):
            for li in range(1, layers):
                order[li] = _reorder(flows[li - 1], order[li - 1], order[li], downward=True)
            for li in range(layers - 2, -1, -1):
                order[li] = _reorder(flows[li], order[li + 1], order[li], downward=False)
            _transpose(order, per_rank, used)
            cost = total(order)
            if cost < best_cost:
                best, best_cost = [column[:] for column in order], cost
    return best


def fingerprint(view: LensView, mask: Optional[Array] = None) -> Array:
    """[L, E]: the population's mean gate weight on each expert at each layer; rows sum to 1."""
    chosen = np.arange(len(view.items)) if mask is None else np.flatnonzero(mask)
    grid = np.zeros((view.experts.shape[1], _n_experts(view)))
    if chosen.size == 0:
        return grid
    for li in range(grid.shape[0]):
        np.add.at(grid[li], view.experts[chosen, li, :].ravel(), view.weights[chosen, li, :].ravel())
    return grid / chosen.size


def population(view: LensView, layer: Optional[int] = None, node: Optional[int] = None,
               axis: Optional[str] = None, value: Optional[str] = None) -> Optional[Array]:
    """A population's mask: a node at a layer, or an axis value; None is every item."""
    from services.lenses.flows import value_of

    if node is not None:
        if layer not in view.layers:
            raise ValueError(f"layer {layer} is not in this lens")
        mask: Array = view.nodes[:, view.layers.index(layer)] == node
        return mask
    if axis is not None:
        return np.array([value_of(item, axis) == value for item in view.items], dtype=bool)
    return None
