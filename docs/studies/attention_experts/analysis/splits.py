"""The attention-and-experts account at every node split of each lens (read-only; common.py has the
account).

A split point is a node whose items part ways at the next layer, by the report cards' rule: the
branches are the next layer's nodes holding at least max(5, 15%) of the node's items
(services/lenses/splits.py). For each branch, its items against the node's other items,
at the layer where they part:
- the separation, and its null: 1,000 random splits of the node's items (items, not units);
- the shares at that layer and in total up to it, beside 200 random splits' shares;
- the same shares along the second direction (the shrinkage discriminant, beside the same 200
  random splits in its metric), as the designed splits have at every layer (account.py);
- the branch's and the rest's commonest label, for reading the result.

Usage, from the repo root:
  .venv/bin/python docs/studies/attention_experts/analysis/splits.py [CAPTURE ...]   (all by default)
Writes results/splits_<capture>.json.
"""
from __future__ import annotations

import sys
import time
from collections import Counter
from typing import Any, Dict, List

import numpy as np
from common import (
    CAPTURES,
    SEPARATION_NULL,
    SHARE_NULL,
    TOTALS,
    Capture,
    account,
    band,
    contrast,
    discriminant_shares,
    load_capture,
    mean_differences,
    random_splits,
    share_totals,
    stream,
    totals_of,
    write_results,
)

MIN_REST = 5  # a branch needs at least this many of the node's other items to compare with


def r4(x: Any) -> float:
    return round(float(x), 4)


def commonest(capture: Capture, items: np.ndarray) -> Dict[str, Any]:
    value, n = Counter(capture.labels[items].tolist()).most_common(1)[0]
    return {"label": value, "share": r4(n / len(items))}


def branch_accounts(capture: Capture, index: int) -> List[Dict[str, Any]]:
    from services.lenses.splits import branches_of, split_points

    found: List[Dict[str, Any]] = []
    for which, (layer, node, _) in enumerate(split_points(capture), start=1):
        li = capture.layers.index(layer)
        members = np.flatnonzero(capture.nodes[:, li] == node)
        t = li + 1
        for branch, _ in branches_of(capture, li, node):
            b = members[capture.nodes[members, t] == branch]
            a = members[capture.nodes[members, t] != branch]
            if len(a) < MIN_REST:
                continue
            outputs, experts, embedding = mean_differences(capture, contrast(capture, b, a), t)
            got = account(outputs, experts, embedding, t)
            rows, _ = random_splits(capture, b, a, SEPARATION_NULL, stream(index, 1000 + which, branch), by_units=False)
            null_separation = np.linalg.norm(rows @ capture.outputs[t].astype(np.float64), axis=1)
            null = share_totals(capture, rows[:SHARE_NULL], [t])[t]
            separation = float(got["separation"][0])
            found.append({
                "node": f"L{layer}C{node}", "branch": f"L{capture.layers[t]}C{branch}", "parts_at": capture.layers[t],
                "n_b": int(len(b)), "n_a": int(len(a)),
                "b": commonest(capture, b), "a": commonest(capture, a),
                "separation": r4(separation), "null_95": r4(np.percentile(null_separation, 95)),
                "p": r4((1 + (null_separation >= separation).sum()) / (1 + len(null_separation))),
                "shares": {key: r4(values[0]) for key, values in totals_of(got).items()},
                "random": {key: band(null[key]) for key in TOTALS},
                "discriminant": discriminant_shares(capture, b, a, t, rows[:SHARE_NULL]),
            })
    return found


def main(names: List[str]) -> None:
    for name in names:
        started = time.time()
        index = list(CAPTURES).index(name) + 1
        capture = load_capture(name)
        branches = branch_accounts(capture, index)
        beyond = [row for row in branches if row["separation"] > row["null_95"]]
        print(f"{name}: {len(branches)} branches at {len({row['node'] for row in branches})} split points, "
              f"{len(beyond)} beyond their null; {time.time() - started:.0f} s", flush=True)
        write_results(f"splits_{name}", {
            "capture": name, "session": capture.session, "lens": capture.lens, "version": capture.version,
            "layers": capture.layers, "separation_null": SEPARATION_NULL, "share_null": SHARE_NULL,
            "branches": branches, "seconds": round(time.time() - started, 1)})
        del capture


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAPTURES))
