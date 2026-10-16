"""How much attention's part and the experts' part vary from one item to the next, layer by layer
(read-only; common.py has the parts). For each capture and layer: the summed variance across items
of the experts' output and of attention's part, and their ratio. The experts take most of any
difference between groups, random ones included, when their part varies more.

Usage, from the repo root:
  .venv/bin/python docs/studies/attention_experts/analysis/variance.py [CAPTURE ...]   (all by default)
Writes results/variance.json.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

import numpy as np
from common import CAPTURES, RESULTS, load_capture, write_results


def ratios(name: str) -> List[Dict[str, Any]]:
    capture = load_capture(name)
    found = []
    for li, layer in enumerate(capture.layers):
        out = capture.outputs[li].astype(np.float64)
        experts = capture.experts[li].astype(np.float64)
        before = capture.outputs[li - 1].astype(np.float64) if li else (
            capture.embedding if capture.embedding is not None else 0.0)  # a read token shared by all adds a constant
        attention = out - before - experts
        e, a = float(experts.var(axis=0).sum()), float(attention.var(axis=0).sum())
        found.append({"layer": layer, "experts": round(e, 2), "attention": round(a, 2), "ratio": round(e / a, 4)})
    return found


def main(names: List[str]) -> None:
    path = RESULTS / "variance.json"
    result: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for name in names:
        result[name] = ratios(name)
        r = [row["ratio"] for row in result[name]]
        print(f"{name}: the experts' variance over attention's {min(r):.2f} to {max(r):.2f}", flush=True)
    write_results("variance", result)


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAPTURES))
