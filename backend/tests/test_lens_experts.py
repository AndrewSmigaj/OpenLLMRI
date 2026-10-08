"""The expert Sankey's fixed order and the fingerprints, on synthetic lens views."""

import numpy as np

from services.lenses.experts import crossings, expert_order, fingerprint, pooled_flows, population
from services.lenses.view import LensView


def planted_view(lanes: int = 6, items: int = 240, layers: int = 5, seed: int = 0):
    """Items travel down lanes, a third of them stepping into the next lane at each layer, so lane
    k feeds lanes k and k+1: between two layers each rank's flows form one chain, whose only
    drawings without crossings keep the lanes in order (or reversed). Each rank has its own
    experts, shuffled ids out of the 32."""
    rng = np.random.default_rng(seed)
    lane = np.zeros((items, layers), dtype=int)
    lane[:, 0] = np.arange(items) % lanes
    for li in range(1, layers):
        step = (rng.random(items) < 1 / 3) & (lane[:, li - 1] < lanes - 1)
        lane[:, li] = lane[:, li - 1] + step
    ids = [rng.permutation(32)[:4 * lanes].reshape(4, lanes) for _ in range(layers)]  # [rank, lane] -> expert
    experts = np.stack([np.stack([ids[li][r][lane[:, li]] for r in range(4)], axis=1)
                        for li in range(layers)], axis=1).astype(np.int16)
    weights = rng.random((items, layers, 4)).astype(np.float32)
    weights /= weights.sum(axis=-1, keepdims=True)
    view = LensView(session_id="s", name="planted", legacy=False, version="v1", layers=list(range(layers)),
                    items=[{"probe_id": f"p{i}", "label": "ab"[i % 2], "categories": {}} for i in range(items)],
                    nodes=(lane % 3).astype(np.int16), experts=experts, weights=weights)
    return view, ids


def test_crossings_weigh_each_crossing_pair_by_both_flows() -> None:
    flow = np.zeros((2, 2))
    flow[0, 1], flow[1, 0] = 2, 3  # two flows that swap places
    assert crossings(flow, [0, 1], [0, 1]) == 6
    assert crossings(flow, [0, 1], [1, 0]) == 0


def test_the_order_recovers_a_planted_layout_with_no_crossings() -> None:
    view, ids = planted_view()
    order = expert_order(view)
    flows = pooled_flows(view)
    assert sum(crossings(flows[li], order[li], order[li + 1]) for li in range(len(order) - 1)) == 0
    for li, column in enumerate(order):
        assert sorted(column) == list(range(32))  # every expert has a place
        for rank in range(4):
            mine = [e for e in column if e in set(ids[li][rank].tolist())]
            lanes = [int(np.flatnonzero(ids[li][rank] == e)[0]) for e in mine]
            assert lanes in (sorted(lanes), sorted(lanes, reverse=True))  # each rank's lanes in order


def test_fingerprint_rows_sum_to_one_for_any_population() -> None:
    view, _ = planted_view()
    for mask in (None, population(view, layer=2, node=1), population(view, axis="label", value="a")):
        grid = fingerprint(view, mask)
        assert grid.shape == (5, 32)
        assert np.allclose(grid.sum(axis=1), 1.0)
    assert not fingerprint(view, np.zeros(len(view.items), dtype=bool)).any()
