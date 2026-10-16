"""The attention-and-experts account of each designed split, layer by layer (read-only; see
common.py for the account itself).

For each capture: every label value against the rest (when there are more than two), the named
pairs, and the ontology's danger pair. At every layer as the target:
- the separation (the length of the difference between the groups' mean states), and its null:
  1,000 random splits of the same items at the split's grain (whole units when no unit straddles
  the split, else items), with a seeded stream for each capture and split;
- the shares: the embedding's, and attention's and the experts' in total and at the target layer
  itself, and by layer; beside them, the same shares for 200 of the random splits (their 5th,
  50th and 95th percentiles), since the experts write larger updates than attention everywhere;
- 500 bootstraps over whole units (families, scenarios or texts) for intervals;
- a second direction at every layer: the shares along the split's shrinkage (Ledoit-Wolf)
  discriminant, which counts directions where each group's items vary little more, beside the same
  200 random splits measured the same way (one covariance per split and layer, so their bands are
  comparable);
- the most that fp16 rounding could move the separation, as a share of it.

Usage, from the repo root:
  .venv/bin/python docs/studies/attention_experts/analysis/account.py [CAPTURE ...]   (all by default)
Writes results/account_<capture>.json and, per capture, the read-token check.
"""
from __future__ import annotations

import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np
from common import (
    BOOTSTRAPS,
    CAPTURES,
    ROUNDING_FLAG,
    SEPARATION_NULL,
    SHARE_NULL,
    TOTALS,
    Capture,
    account,
    band,
    bootstraps,
    contrast,
    discriminant_shares,
    load_capture,
    mean_differences,
    random_splits,
    rounding_bound,
    share_totals,
    stream,
    token_check,
    totals_of,
    write_results,
)


def designed_splits(capture: Capture) -> List[Tuple[str, np.ndarray, np.ndarray]]:
    """(name, B's items, A's items): each label value against the rest when there are more than
    two values, then the named pairs (B minus A)."""
    spec = CAPTURES[capture.name]
    out = []
    values = sorted(set(capture.labels.tolist()))
    if len(values) > 2:
        for value in values:
            out.append((f"{value} against the rest", np.flatnonzero(capture.labels == value),
                        np.flatnonzero(capture.labels != value)))
    for a, b in spec.get("pairs", []):
        out.append((f"{b} against {a}", np.flatnonzero(capture.labels == b), np.flatnonzero(capture.labels == a)))
    for axis, (a, b) in spec.get("axis_pairs", {}).items():
        values_of = capture.category(axis)
        out.append((f"{axis}: {b} against {a}", np.flatnonzero(values_of == b), np.flatnonzero(values_of == a)))
    return out


def r4(x: Any) -> float:
    return round(float(x), 4)


def analyse(capture: Capture, index: int, which: int, name: str, b: np.ndarray, a: np.ndarray) -> Dict[str, Any]:
    layers = range(len(capture.layers))
    outputs, experts, embedding = mean_differences(capture, contrast(capture, b, a))
    real = {t: account(outputs, experts, embedding, t) for t in layers}

    null_rows, grain = random_splits(capture, b, a, SEPARATION_NULL, stream(index, which, 1))
    null_separation = np.stack([np.linalg.norm(null_rows @ x.astype(np.float64), axis=1)
                                for x in capture.outputs], axis=1)
    null_shares = share_totals(capture, null_rows[:SHARE_NULL], list(layers))
    boots = share_totals(capture, bootstraps(capture, b, a, BOOTSTRAPS, stream(index, which, 2)), list(layers))

    targets = []
    for t in layers:
        got = real[t]
        separation = float(got["separation"][0])
        null = null_separation[:, t]
        direction = outputs[t][0] / np.linalg.norm(outputs[t][0])
        rounding = rounding_bound(capture, b, a, direction, t) / separation
        row: Dict[str, Any] = {
            "layer": capture.layers[t],
            "separation": r4(separation),
            "null_95": r4(np.percentile(null, 95)),
            "p": r4((1 + (null >= separation).sum()) / (1 + len(null))),
            "shares": {**{key: r4(values[0]) for key, values in totals_of(got).items()},
                       "attention_by_layer": [r4(v) for v in got["attention"][0]],
                       "experts_by_layer": [r4(v) for v in got["experts"][0]]},
            "random": {key: band(null_shares[t][key]) for key in TOTALS},
            "interval": {key: band(boots[t][key])[::2] for key in TOTALS},
            "rounding": r4(rounding),
            "rounding_flag": bool(rounding > ROUNDING_FLAG),
            "discriminant": discriminant_shares(capture, b, a, t, null_rows[:SHARE_NULL]),
        }
        targets.append(row)
    return {"name": name, "n_b": int(len(b)), "n_a": int(len(a)), "grain": grain, "targets": targets}


def main(names: List[str]) -> None:
    for name in names:
        started = time.time()
        index = list(CAPTURES).index(name) + 1
        capture = load_capture(name)
        check = token_check(capture)
        print(f"{name}: {len(capture.items)} items, units {capture.unit_kind} "
              f"({len(set(capture.units.tolist()))}), read tokens {check['distinct_tokens']} "
              f"(mismatches {check['mismatches']}), loaded in {time.time() - started:.0f} s", flush=True)
        splits = []
        for which, (split, b, a) in enumerate(designed_splits(capture), start=1):
            t0 = time.time()
            splits.append(analyse(capture, index, which, split, b, a))
            last = splits[-1]["targets"][-1]
            print(f"  {split}: L{last['layer']} separation {last['separation']:.1f} (null 95th {last['null_95']:.1f}); "
                  f"attention {last['shares']['attention']:.2f} [random {last['random']['attention'][1]:.2f}], "
                  f"experts {last['shares']['experts']:.2f} [random {last['random']['experts'][1]:.2f}]; "
                  f"{time.time() - t0:.0f} s", flush=True)
        write_results(f"account_{name}", {
            "capture": name, "session": capture.session, "lens": capture.lens, "version": capture.version,
            "n_items": len(capture.items), "units": capture.unit_kind, "n_units": int(len(set(capture.units.tolist()))),
            "layers": capture.layers, "token_check": check, "embedding_shared": capture.embedding is None,
            "separation_null": SEPARATION_NULL, "share_null": SHARE_NULL, "bootstraps": BOOTSTRAPS,
            "splits": splits, "seconds": round(time.time() - started, 1)})
        del capture


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAPTURES))
