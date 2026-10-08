"""Flows through a lens view, for all its layers at once: nodes and links for the clusters, and
for the experts at any of the four ranks.

Nodes are named as today (`L12C3` for a cluster, `L12E17` for an expert), so the app and the
legacy reports' keys keep working. Every node and link carries its count and its counts on each
designed axis, which the app's colours blend.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional

import numpy as np

from services.lenses.view import Array, LensView


def _value(item: Dict[str, Any], axis: str) -> Optional[str]:
    raw = item.get("label") if axis == "label" else item.get("categories", {}).get(axis)
    return None if raw is None else str(raw)


def axes_of(view: LensView) -> Dict[str, List[str]]:
    """The designed axes (the label and every category) with their values."""
    names = ["label"] + sorted({key for item in view.items for key in item.get("categories", {})})
    found = {name: sorted({v for item in view.items if (v := _value(item, name)) is not None})
             for name in names}
    return {name: values for name, values in found.items() if values}


def _counts(view: LensView, members: Array, axes: Dict[str, List[str]]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {}
    for axis in axes:
        tally = Counter(v for i in members if (v := _value(view.items[int(i)], axis)) is not None)
        out[axis] = dict(sorted(tally.items()))
    return out


def _flows(view: LensView, codes: Array, prefix: str, kind: str,
           weights: Optional[Array] = None) -> Dict[str, Any]:
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
            "output": _output_column(view, codes, prefix, axes)}


def _output_column(view: LensView, codes: Array, prefix: str,
                   axes: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """The column after the last layer: each item's generated-output category, when captured."""
    outputs = [item.get("output_category") for item in view.items]
    if not any(outputs):
        return None
    last = view.layers[-1]
    nodes = [{"id": f"Out:{value}", "value": value, "count": n,
              "counts": _counts(view, np.array([i for i, o in enumerate(outputs) if o == value]), axes)}
             for value, n in sorted(Counter(o for o in outputs if o).items())]
    pairs = Counter((int(codes[i, -1]), o) for i, o in enumerate(outputs) if o)
    links = [{"source": f"L{last}{prefix}{code}", "target": f"Out:{value}", "count": n}
             for (code, value), n in sorted(pairs.items())]
    return {"nodes": nodes, "links": links}


def cluster_flows(view: LensView) -> Dict[str, Any]:
    return _flows(view, view.nodes, "C", "cluster")


def expert_flows(view: LensView, rank: int = 1) -> Dict[str, Any]:
    """Each item's expert at `rank` (1 to 4) per layer, with the model's own mean weight per node."""
    if not 1 <= rank <= view.experts.shape[-1]:
        raise ValueError(f"rank must be 1 to {view.experts.shape[-1]}, got {rank}")
    return _flows(view, view.experts[:, :, rank - 1], "E", "expert", view.weights[:, :, rank - 1])


def members(view: LensView, layer: int, node: Optional[int] = None, expert: Optional[int] = None,
            rank: int = 1, to_node: Optional[int] = None, offset: int = 0, limit: int = 50) -> Dict[str, Any]:
    """The items in a cluster (and, with `to_node`, those going on to a node at the next layer),
    or routed to an expert at a rank, a page at a time."""
    if layer not in view.layers:
        raise ValueError(f"layer {layer} is not in this lens")
    li = view.layers.index(layer)
    if expert is not None:
        mask = view.experts[:, li, rank - 1] == expert
    elif node is not None:
        mask = view.nodes[:, li] == node
        if to_node is not None and li + 1 < len(view.layers):
            mask &= view.nodes[:, li + 1] == to_node
    else:
        raise ValueError("give a node or an expert")
    found = np.flatnonzero(mask)
    page = found[offset:offset + limit]
    return {"total": int(found.size), "offset": offset,
            "items": [view.items[int(i)] for i in page]}
