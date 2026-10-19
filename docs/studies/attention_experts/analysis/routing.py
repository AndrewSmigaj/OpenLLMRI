"""Attention and routing: how much each layer's attention changes the experts the router picks,
layer by layer and for each expert node (read-only; LENS-30; docs/research/attention_and_experts.md,
"Attention and routing"; the proposal in docs/design/design.md#attention).

At layer L the router reads RMSNorm(h_(L-1) + attn_L) and picks four experts. The captures store
the layer's output h_L and the experts' output moe_L at the read token, so the router's input is
h_L - moe_L, and the state before that layer's attention is h_(L-1) (the read token's embedding row
before layer 0). With each router's weight and bias and the norm's gain read from the model's files
on the CPU, the routing is worked out three ways at every layer:
- as captured, from h_L - moe_L, and checked against the stored routing;
- without the item's own attention at L: attn_L replaced by its mean over the lens's items, so what
  attention adds to every item alike stays and what it adds to this item in particular goes;
- without attention at L at all (attn_L removed), for reference.
For each expert node at rank 1 (the items whose first expert at layer L is e), it counts the items
that the item's own attention at L brought there (without it their first expert would be another),
with the labels of the node's items and of the brought ones,
and compares that share with the layer's share over all items: a two-sided binomial test, with the
Benjamini-Hochberg correction over every node of the capture. Items of one family or scenario are
not independent, so the test is a first look, not a final count.

This is a computation on the router alone: it changes nothing downstream of layer L and says
nothing about what the model would do with that layer's attention removed.

Usage, from the repo root:
  .venv/bin/python docs/studies/attention_experts/analysis/routing.py [capture ...]
writes results/routing_<capture>.json, then figures/attention_routing.png from every result.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

import numpy as np
from common import (
    CAPTURES,
    CONTEXT,
    RESULTS,
    SINGLE_WORDS,
    embedding_rows,
    figure_path,
    load_capture,
    write_results,
)
from scipy.stats import binomtest
from sklearn.metrics import adjusted_mutual_info_score

MIN_NODE = 20  # items in an expert node before its share is tested
FDR = 0.05


def router_input(x: np.ndarray, gain: np.ndarray, eps: float) -> np.ndarray:
    """RMSNorm as gpt-oss applies it before the router (no mean subtracted; the gain after)."""
    x = x.astype(np.float64)
    return x / np.sqrt((x * x).mean(axis=1, keepdims=True) + eps) * gain


def first_four(logits: np.ndarray) -> np.ndarray:
    return np.argsort(-logits, axis=1, kind="stable")[:, :4]


def swapped(a: np.ndarray, b: np.ndarray) -> float:
    """Mean number of the four experts that differ between two choices, per item."""
    return float(np.mean([4 - len(set(x) & set(y)) for x, y in zip(a.tolist(), b.tolist())]))


def benjamini_hochberg(p: np.ndarray, q: float) -> np.ndarray:
    order = np.argsort(p)
    ranked = p[order] * len(p) / (np.arange(len(p)) + 1)
    passed = np.zeros(len(p), dtype=bool)
    below = np.nonzero(ranked <= q)[0]
    if len(below):
        passed[order[: below.max() + 1]] = True
    return passed


def run(name: str) -> Dict[str, Any]:
    from services.lenses.data import load_routing
    from services.lenses.model_weights import ModelWeights
    from services.lenses.store import lens_dir, read_manifest

    cap = load_capture(name)
    weights = ModelWeights()
    site = read_manifest(lens_dir(cap.session, cap.lens)).site.token_position
    stored = load_routing(cap.session, [item["probe_id"] for item in cap.items], site)
    stored_layers = sorted(range(stored.shape[1]))
    before0 = cap.embedding if cap.embedding is not None else embedding_rows(cap.token_ids)
    labels = cap.labels
    rows: List[Dict[str, Any]] = []
    nodes: List[Dict[str, Any]] = []
    for li, layer in enumerate(cap.layers):
        w, b = (np.asarray(t, dtype=np.float64) for t in weights.router(layer))
        gain = np.asarray(weights.pre_router_norm(layer), dtype=np.float64)
        out = cap.outputs[li].astype(np.float64)
        before = before0 if li == 0 else cap.outputs[li - 1].astype(np.float64)
        read = out - cap.experts[li].astype(np.float64)  # h_(L-1) + attn_L
        attention = read - before
        own = first_four(router_input(read, gain, weights.eps) @ w.T + b)
        common = first_four(router_input(before + attention.mean(axis=0), gain, weights.eps) @ w.T + b)
        none = first_four(router_input(before, gain, weights.eps) @ w.T + b)
        captured = np.argsort(-stored[:, stored_layers.index(layer), :], axis=1, kind="stable")[:, :4]
        moved = own[:, 0] != common[:, 0]
        rate = float(moved.mean())
        rows.append({
            "layer": layer,
            "match_four": float(np.mean([set(x) == set(y) for x, y in zip(own.tolist(), captured.tolist())])),
            "match_first": float(np.mean(own[:, 0] == captured[:, 0])),
            "own_swapped_of_four": swapped(own, common),
            "own_first_changed": rate,
            "all_swapped_of_four": swapped(own, none),
            "all_first_changed": float(np.mean(own[:, 0] != none[:, 0])),
            "ami_first_label": float(adjusted_mutual_info_score(labels, own[:, 0])),
            "ami_first_label_without_own": float(adjusted_mutual_info_score(labels, common[:, 0])),
            "own_first_changed_by_label": {str(v): float(moved[labels == v].mean()) for v in sorted(set(labels))},
        })
        for expert in np.unique(own[:, 0]):
            members = own[:, 0] == expert
            n = int(members.sum())
            brought = int((members & moved).sum())
            pushed_out = int(((common[:, 0] == expert) & moved).sum())
            entry = {"layer": layer, "expert": int(expert), "items": n, "brought": brought,
                     "pushed_out": pushed_out, "share": brought / n, "layer_share": rate,
                     "labels": {str(v): int((members & (labels == v)).sum()) for v in sorted(set(labels))},
                     "brought_labels": {str(v): int((members & moved & (labels == v)).sum()) for v in sorted(set(labels))}}
            if n >= MIN_NODE and 0.0 < rate < 1.0:
                entry["p"] = float(binomtest(brought, n, rate).pvalue)
            nodes.append(entry)
    tested = [node for node in nodes if "p" in node]
    passed = benjamini_hochberg(np.array([node["p"] for node in tested]), FDR) if tested else np.array([])
    for node, beyond in zip(tested, passed.tolist()):
        node["beyond_chance"] = bool(beyond)
    payload = {
        "capture": name, "session": cap.session, "lens": cap.lens, "version": cap.version,
        "items": len(cap.items), "min_node": MIN_NODE, "fdr": FDR, "layers": rows, "nodes": nodes,
        "summary": {
            "match_four_min": min(r["match_four"] for r in rows),
            "match_first_min": min(r["match_first"] for r in rows),
            "own_first_changed_range": [min(r["own_first_changed"] for r in rows), max(r["own_first_changed"] for r in rows)],
            "own_swapped_range": [min(r["own_swapped_of_four"] for r in rows), max(r["own_swapped_of_four"] for r in rows)],
            "all_first_changed_range": [min(r["all_first_changed"] for r in rows), max(r["all_first_changed"] for r in rows)],
            "nodes_tested": len(tested),
            "nodes_beyond_chance": int(sum(node.get("beyond_chance", False) for node in tested)),
            "nodes_beyond_above": int(sum(node.get("beyond_chance", False) and node["share"] > node["layer_share"] for node in tested)),
        },
    }
    write_results(f"routing_{name}", payload)
    return payload


def figure() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [n for n in (*CONTEXT, *SINGLE_WORDS) if (RESULTS / f"routing_{n}.json").exists()]
    fig, axes = plt.subplots(2, 4, figsize=(17, 7.6), sharey=True)
    for ax, name in zip(axes.flat, names):
        data = json.loads((RESULTS / f"routing_{name}.json").read_text(encoding="utf-8"))
        layers = [r["layer"] for r in data["layers"]]
        ax.plot(layers, [r["all_first_changed"] for r in data["layers"]], color="#999999", ls="--", lw=1.2,
                label="first expert changed without attention at that layer")
        ax.plot(layers, [r["own_first_changed"] for r in data["layers"]], color="#5470c6", lw=2,
                label="first expert changed without the item's own attention")
        for node in data["nodes"]:
            if node["items"] < MIN_NODE:
                continue
            colour = "#ee6666" if node.get("beyond_chance") else "#bbbbbb"
            ax.scatter(node["layer"], node["share"], s=8 + node["items"] / 6, color=colour, alpha=0.7, lw=0)
        s = data["summary"]
        ax.set_title(f"{name}: {s['nodes_beyond_chance']} of {s['nodes_tested']} expert nodes beyond chance", fontsize=10)
        ax.set_xlabel("layer")
        ax.set_ylim(-0.02, 1.02)
        ax.grid(alpha=0.25)
    for ax in axes.flat[len(names):]:
        ax.axis("off")
    axes[0, 0].set_ylabel("share of items")
    axes[1, 0].set_ylabel("share of items")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    handles.append(plt.Line2D([], [], marker="o", ls="", color="#ee6666"))
    labels.append("an expert node (first expert), beyond the layer's share (Benjamini-Hochberg 5%)")
    handles.append(plt.Line2D([], [], marker="o", ls="", color="#bbbbbb"))
    labels.append(f"an expert node within chance (dot size: items; nodes of {MIN_NODE} items or more)")
    axes[1, 3].legend(handles, labels, loc="center", fontsize=9, frameon=False)
    fig.suptitle("Items whose first expert at a layer would differ without attention's output at that layer "
                 "(the router alone, recomputed on the CPU)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(figure_path("attention_routing"), dpi=130)


if __name__ == "__main__":
    for capture in sys.argv[1:] or list(CAPTURES):
        result = run(capture)
        print(capture, json.dumps(result["summary"]))
    figure()
