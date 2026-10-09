"""Flows through a lens view, for all its layers at once: nodes and links for the clusters, and
for the experts at any of the four ranks.

Nodes are named as today (`L12C3` for a cluster, `L12E17` for an expert), so the app and the
legacy reports' keys keep working. Every node and link carries its count and its counts on each
designed axis, which the app's colours blend.
"""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from services.lenses.view import Array, LensView


def value_of(item: Dict[str, Any], axis: str) -> Optional[str]:
    """An item's value on a designed axis (the label, or one of its categories)."""
    raw = item.get("label") if axis == "label" else item.get("categories", {}).get(axis)
    return None if raw is None else str(raw)


def axes_of(view: LensView) -> Dict[str, List[str]]:
    """The designed axes (the label and every category) with their values."""
    return axes_of_items(view.items)


def axes_of_items(items: Sequence[Dict[str, Any]]) -> Dict[str, List[str]]:
    """The designed axes of any items (a lens's, or a capture's before a lens is built)."""
    names = ["label"] + sorted({key for item in items for key in item.get("categories", {})})
    found = {name: sorted({v for item in items if (v := value_of(item, name)) is not None})
             for name in names}
    return {name: values for name, values in found.items() if values}


def _counts(view: LensView, members: Array, axes: Dict[str, List[str]]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {}
    for axis in axes:
        tally = Counter(v for i in members if (v := value_of(view.items[int(i)], axis)) is not None)
        out[axis] = dict(sorted(tally.items()))
    return out


def _flows(view: LensView, codes: Array, prefix: str, kind: str,
           weights: Optional[Array] = None, output_axes: Sequence[str] = ()) -> Dict[str, Any]:
    """Nodes and links from one code per item and layer (a cluster, or an expert at one rank)."""
    axes = axes_of(view)
    nodes: List[Dict[str, Any]] = []
    links: List[Dict[str, Any]] = []
    for li, layer in enumerate(view.layers):
        for code in sorted(set(int(c) for c in codes[:, li])):
            members = np.flatnonzero(codes[:, li] == code)
            node: Dict[str, Any] = {"id": f"L{layer}{prefix}{code}", "layer": layer, "index": code,
                                    "count": int(members.size), "counts": _counts(view, members, axes)}
            if weights is not None:
                node["weight"] = round(float(weights[members, li].mean()), 4)
            nodes.append(node)
        if li + 1 < len(view.layers):
            nxt = view.layers[li + 1]
            for (a, b), n in sorted(Counter(zip(codes[:, li].tolist(), codes[:, li + 1].tolist())).items()):
                members = np.flatnonzero((codes[:, li] == a) & (codes[:, li + 1] == b))
                links.append({"source": f"L{layer}{prefix}{a}", "target": f"L{nxt}{prefix}{b}",
                              "count": n, "counts": _counts(view, members, axes)})
    return {"kind": kind, "layers": view.layers, "axes": axes, "nodes": nodes, "links": links,
            "output": _output_column(view, codes, prefix, axes, output_axes)}


def output_axes_of(view: LensView) -> Dict[str, List[str]]:
    """The generated outputs' own axes (from their categorization), with their values."""
    names = sorted({key for item in view.items for key in item.get("output_categories", {})})
    return {name: sorted({str(v) for item in view.items
                          if (v := item.get("output_categories", {}).get(name)) is not None})
            for name in names}


def _output_key(item: Dict[str, Any], group_by: Sequence[str]) -> Optional[str]:
    """An item's output node: its output category, or its values on the chosen output axes."""
    if not group_by:
        return item.get("output_category") or None
    values = item.get("output_categories") or {}
    return "_".join(str(values.get(axis, "unknown")) for axis in group_by) if values else None


def _output_counts(view: LensView, members: Array, out_axes: Dict[str, List[str]]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {}
    for axis in out_axes:
        tally = Counter(str(v) for i in members
                        if (v := view.items[int(i)].get("output_categories", {}).get(axis)) is not None)
        out[axis] = dict(sorted(tally.items()))
    return out


def _output_column(view: LensView, codes: Array, prefix: str, axes: Dict[str, List[str]],
                   group_by: Sequence[str] = ()) -> Optional[Dict[str, Any]]:
    """The column after the last layer: each item's generated output, by its category or by its
    values on the chosen output axes (every combination of their values gets a node, as before).
    Nodes and links count the designed axes (`counts`) and the output axes (`output_counts`)."""
    keys = [_output_key(item, group_by) for item in view.items]
    if not any(keys):
        return None
    out_axes = output_axes_of(view)
    totals = Counter(k for k in keys if k)
    if group_by:
        for combo in itertools.product(*(out_axes.get(axis, ["unknown"]) for axis in group_by)):
            totals.setdefault("_".join(combo), 0)
    last = view.layers[-1]

    def side(members: Array) -> Dict[str, Any]:
        return {"counts": _counts(view, members, axes), "output_counts": _output_counts(view, members, out_axes)}

    nodes = [{"id": f"Generated:{value}", "value": value, "count": n,
              **side(np.array([i for i, k in enumerate(keys) if k == value], dtype=int))}
             for value, n in sorted(totals.items())]
    pairs = Counter((int(codes[i, -1]), k) for i, k in enumerate(keys) if k)
    links = [{"source": f"L{last}{prefix}{code}", "target": f"Generated:{value}", "count": n,
              **side(np.array([i for i, k in enumerate(keys) if k == value and int(codes[i, -1]) == code], dtype=int))}
             for (code, value), n in sorted(pairs.items())]
    return {"axes": out_axes, "nodes": nodes, "links": links}


def cluster_flows(view: LensView, output_axes: Sequence[str] = ()) -> Dict[str, Any]:
    """Cluster flows, plus each item's node at every layer (for route cards, trajectories and lit
    paths) and its output node. `output_axes` groups the output column by those output axes
    instead of the output category."""
    out = _flows(view, view.nodes, "C", "cluster", output_axes=output_axes)
    out["assignments"] = {item["probe_id"]: {str(layer): int(view.nodes[i, li])
                                              for li, layer in enumerate(view.layers)}
                          for i, item in enumerate(view.items)}
    if out["output"]:
        out["output_of"] = {item["probe_id"]: key for item in view.items
                            if (key := _output_key(item, output_axes)) is not None}
    return out


def expert_flows(view: LensView, rank: int = 1, output_axes: Sequence[str] = (),
                 order: Optional[List[List[int]]] = None) -> Dict[str, Any]:
    """Each item's expert at `rank` (1 to 4) per layer, with the model's own mean weight per node.
    With `order` (each layer's experts top to bottom), the nodes come in that order."""
    if not 1 <= rank <= view.experts.shape[-1]:
        raise ValueError(f"rank must be 1 to {view.experts.shape[-1]}, got {rank}")
    out = _flows(view, view.experts[:, :, rank - 1], "E", "expert", view.weights[:, :, rank - 1], output_axes)
    # each item's expert at this rank, layer by layer (for lit paths)
    out["assignments"] = {item["probe_id"]: {str(layer): int(view.experts[i, li, rank - 1])
                                              for li, layer in enumerate(view.layers)}
                          for i, item in enumerate(view.items)}
    if order is not None:
        place = {(layer, expert): i for li, layer in enumerate(view.layers) for i, expert in enumerate(order[li])}
        out["nodes"].sort(key=lambda node: (node["layer"], place.get((node["layer"], node["index"]), 10**6)))
        out["order"] = order
    return out


LINK_FLOOR = 0.5  # a weighted link carries at least half an item's worth of weight


def weighted_expert_flows(view: LensView, output_axes: Sequence[str] = (),
                          order: Optional[List[List[int]]] = None) -> Dict[str, Any]:
    """All four ranks at once (DESIGN.md E5), weighted by the model's own weights: an expert node
    holds the gate weight its items give it, and a link between experts at consecutive layers the
    weight that flows along it (each item's weight on the first times its weight on the second),
    so a pipeline is drawn wherever all its steps exist. Axis counts are weighted the same way.
    Each item's path, for lighting, follows its rank-1 expert."""
    from services.lenses.routes import dense

    weights = dense(view)
    axes = axes_of(view)
    values = {axis: [value_of(item, axis) for item in view.items] for axis in axes}

    def counts(w: Array) -> Dict[str, Dict[str, float]]:
        out: Dict[str, Dict[str, float]] = {}
        for axis in axes:
            tally: Dict[str, float] = {}
            for v, x in zip(values[axis], w):
                if v is not None and x > 0:
                    tally[v] = tally.get(v, 0.0) + float(x)
            out[axis] = {v: round(x, 3) for v, x in sorted(tally.items())}
        return out

    nodes: List[Dict[str, Any]] = []
    links: List[Dict[str, Any]] = []
    for li, layer in enumerate(view.layers):
        for expert in np.flatnonzero(weights[:, li, :].sum(axis=0) > 0):
            w = weights[:, li, expert]
            nodes.append({"id": f"L{layer}E{expert}", "layer": layer, "index": int(expert),
                          "count": round(float(w.sum()), 3), "weight": round(float(w[w > 0].mean()), 4),
                          "counts": counts(w)})
        if li + 1 < len(view.layers):
            flow = weights[:, li, :].T @ weights[:, li + 1, :]  # [E, E]: weight flowing from a to b
            for a, b in zip(*np.nonzero(flow >= LINK_FLOOR)):
                links.append({"source": f"L{layer}E{a}", "target": f"L{view.layers[li + 1]}E{b}",
                              "count": round(float(flow[a, b]), 3),
                              "counts": counts(weights[:, li, a] * weights[:, li + 1, b])})
    out: Dict[str, Any] = {"kind": "expert", "weighted": True, "layers": view.layers, "axes": axes, "nodes": nodes,
                           "links": links, "output": _weighted_output(view, weights, axes, counts, output_axes)}
    out["assignments"] = {item["probe_id"]: {str(layer): int(view.experts[i, li, 0]) for li, layer in enumerate(view.layers)}
                          for i, item in enumerate(view.items)}
    if order is not None:
        place = {(layer, expert): i for li, layer in enumerate(view.layers) for i, expert in enumerate(order[li])}
        out["nodes"].sort(key=lambda node: (node["layer"], place.get((node["layer"], node["index"]), 10**6)))
        out["order"] = order
    return out


def _weighted_output(view: LensView, weights: Array, axes: Dict[str, List[str]], counts: Any,
                     group_by: Sequence[str]) -> Optional[Dict[str, Any]]:
    """The output column for the weighted view: each item reaches its output with all its weight
    on the last layer's experts."""
    keys = [_output_key(item, group_by) for item in view.items]
    if not any(keys):
        return None
    out_axes = output_axes_of(view)
    last = view.layers[-1]
    nodes = []
    links = []
    for value in sorted({k for k in keys if k}):
        mask = np.array([k == value for k in keys], dtype=float)
        members = np.flatnonzero(mask)
        nodes.append({"id": f"Generated:{value}", "value": value, "count": int(members.size),
                      "counts": counts(mask), "output_counts": _output_counts(view, members, out_axes)})
        flow = mask @ weights[:, -1, :]
        for expert in np.flatnonzero(flow >= LINK_FLOOR):
            w = weights[:, -1, expert] * mask
            links.append({"source": f"L{last}E{expert}", "target": f"Generated:{value}", "count": round(float(flow[expert]), 3),
                          "counts": counts(w), "output_counts": _output_counts(view, np.flatnonzero(w > 0), out_axes)})
    return {"axes": out_axes, "nodes": nodes, "links": links}


def members(view: LensView, layer: int, node: Optional[int] = None, expert: Optional[int] = None,
            rank: int = 1, to_node: Optional[int] = None, to_expert: Optional[int] = None,
            output: Optional[str] = None, offset: int = 0, limit: int = 50) -> Dict[str, Any]:
    """The items in a cluster or routed to an expert at a rank (rank 0: at any of the four, as the
    weighted view draws them), a page at a time. `to_node` and `to_expert` keep those going on to
    that node or expert at the next layer (a link); `output` keeps those whose generated output is
    that category (the output column)."""
    if layer not in view.layers:
        raise ValueError(f"layer {layer} is not in this lens")
    li = view.layers.index(layer)
    has_next = li + 1 < len(view.layers)

    def routed(at: int, chosen: int) -> Array:
        found: Array = (view.experts[:, at, :] == chosen).any(axis=1) if rank == 0 else view.experts[:, at, rank - 1] == chosen
        return found

    if expert is not None:
        mask = routed(li, expert)
        if to_expert is not None and has_next:
            mask &= routed(li + 1, to_expert)
    elif node is not None:
        mask = view.nodes[:, li] == node
        if to_node is not None and has_next:
            mask &= view.nodes[:, li + 1] == to_node
    elif output is not None:
        mask = np.ones(len(view.items), dtype=bool)
    else:
        raise ValueError("give a node, an expert or an output")
    if output is not None:
        mask &= np.array([item.get("output_category") == output for item in view.items], dtype=bool)
    found = np.flatnonzero(mask)
    page = found[offset:offset + limit]
    return {"total": int(found.size), "offset": offset,
            "items": [view.items[int(i)] for i in page]}
