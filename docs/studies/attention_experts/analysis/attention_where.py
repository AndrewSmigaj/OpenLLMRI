"""Where attention reads from, as a population (Andrew's attention Sankey, first reading, 2026-10-20).

For the tank sentences, from the CPU pass (`cpu_pass.py`): each item's profile of where attention's
output at " tank" came from, at each layer, by role (the word itself, the token before it, the first
token, the other words) and by distance (the word itself, 1, 2-3, 4-7 and 8 or more tokens back, the
first token). Per layer: Ward groups of the profiles at k = 5 (the senses), and their agreement (AMI)
with the sense, with the lens's nodes and with where " tank" sits in the sentence (its position,
binned); and a logistic probe (5 folds, stratified) for the sense from the profile, from the
position alone, and from both.

Usage (from the repo root): .venv/bin/python docs/studies/attention_experts/analysis/attention_where.py
Result: results/attention_where_tank.json.
"""
import json
from typing import Dict, List

import numpy as np

import common

ROLE_BINS = [("self", 0, 0), ("previous", 1, 1), ("first", None, None), ("other", 2, 10_000)]
DISTANCE_BINS = [("self", 0, 0), ("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8+", 8, 10_000), ("first", None, None)]
POSITION_EDGES = [3, 5, 8, 12]


def profiles(amount: np.ndarray, reads: np.ndarray, bins) -> np.ndarray:
    """[items, layers, sources] amounts -> [items, layers, bins] shares (the first token as its own
    bin once the read word is two or more tokens in)."""
    first = [name for name, _, _ in bins].index("first")
    out = np.zeros((amount.shape[0], amount.shape[1], len(bins)))
    for b, r in enumerate(reads.tolist()):
        a = amount[b, :, : r + 1].astype(np.float64)
        a = a / a.sum(axis=1, keepdims=True)
        for j in range(r + 1):
            if j == 0 and r >= 2:
                k = first
            else:
                d = r - j
                k = next(i for i, (_, lo, hi) in enumerate(bins) if lo is not None and lo <= d <= hi)
            out[b, :, k] += a[:, j]
    return out


def main() -> None:
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import adjusted_mutual_info_score as ami
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    from services.lenses.view import open_lens

    z = np.load(common.LAKE / "session_1434a9be/studies/attention_cpu_pass.npz")
    view = open_lens("session_1434a9be", "tank-k5-n15")
    index = {item["probe_id"]: i for i, item in enumerate(view.items)}
    order = np.array([index[p] for p in z["probe_ids"]])
    labels = np.array([str(view.items[i]["label"]) for i in order])
    nodes = np.asarray(view.nodes)[order]
    reads = z["reads"]
    position = np.digitize(reads, POSITION_EDGES)
    onehot = np.eye(len(POSITION_EDGES) + 1)[position]
    cv = StratifiedKFold(5, shuffle=True, random_state=common.SEED)

    def probe(X: np.ndarray) -> float:
        predicted = cross_val_predict(LogisticRegression(max_iter=3000), X, labels, cv=cv)
        return float(balanced_accuracy_score(labels, predicted))

    position_only = probe(onehot)
    out: Dict[str, object] = {"capture": "tank", "n_items": int(len(labels)), "k": 5,
                              "position_edges": POSITION_EDGES, "probe_position_only": round(position_only, 4),
                              "profiles": {}}
    for name, bins in (("role", ROLE_BINS), ("distance", DISTANCE_BINS)):
        P = profiles(z["amount"], reads, bins)
        rows: List[Dict[str, float]] = []
        for li in range(P.shape[1]):
            groups = AgglomerativeClustering(5, linkage="ward").fit_predict(P[:, li])
            rows.append({"layer": li,
                         "ami_sense": round(float(ami(groups, labels)), 4),
                         "ami_lens_nodes": round(float(ami(groups, nodes[:, li])), 4),
                         "ami_position": round(float(ami(groups, position)), 4),
                         "ami_lens_nodes_sense": round(float(ami(nodes[:, li], labels)), 4),
                         "probe_profile": round(probe(P[:, li]), 4),
                         "probe_profile_and_position": round(probe(np.column_stack([P[:, li], onehot])), 4)})
        out["profiles"][name] = {"bins": [b[0] for b in bins], "layers": rows}
    (common.RESULTS / "attention_where_tank.json").write_text(json.dumps(out, indent=1))
    for name, record in out["profiles"].items():
        rows = record["layers"]
        print(name, "sense", min(r["ami_sense"] for r in rows), max(r["ami_sense"] for r in rows),
              "| position", min(r["ami_position"] for r in rows), max(r["ami_position"] for r in rows),
              "| probe", min(r["probe_profile"] for r in rows), max(r["probe_profile"] for r in rows),
              "| both", min(r["probe_profile_and_position"] for r in rows), max(r["probe_profile_and_position"] for r in rows),
              "| position only", position_only)


if __name__ == "__main__":
    main()
