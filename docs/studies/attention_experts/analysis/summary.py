"""The numbers the findings note quotes (docs/research/attention_and_experts.md), worked out from
results/ (read-only; run after account.py, splits.py and variance.py). Writes results/summary.json.

Conventions, as in the note:
- a share is below its band when it is under its random splits' 5th percentile, above when it is
  over their 95th, otherwise inside; along the discriminant, against the band measured that way;
- the middle layers are L4 to L20, and only targets (or branches) beyond their separation null
  count;
- a node split is read by attention's share at the layer where its branches part;
- a mark is a share outside its band along the mean difference; it holds when the discriminant
  puts it outside on the same side.

Usage, from the repo root: .venv/bin/python docs/studies/attention_experts/analysis/summary.py
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

import numpy as np
from common import CAPTURES, CONTEXT, RESULTS, SINGLE_WORDS, write_results

MAIN = {"tank": "vehicle against aquarium", "calibration": "vehicle against aquarium",
        "framing": "factual against roleplay", "words": "animal against the rest",
        "ontology": "danger: can kill against harmless", "objects": "harmful against benign",
        "friend_foe": "foe against friend"}
MIDDLE = range(4, 21)


def load(kind: str, name: str) -> Dict[str, Any]:
    return json.loads((RESULTS / f"{kind}_{name}.json").read_text(encoding="utf-8"))


def place(value: float, band: List[float]) -> str:
    return "below" if value < band[0] else ("above" if value > band[2] else "inside")


def r4(x: Any) -> Optional[float]:
    return None if x is None else round(float(x), 4)


def span(values: List[float]) -> List[Optional[float]]:
    return [r4(min(values)), r4(max(values))] if values else [None, None]


def middle(split: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [t for t in split["targets"] if t["layer"] in MIDDLE and t["separation"] > t["null_95"]]


def checks(accounts: Dict[str, Any]) -> Dict[str, Any]:
    targets = [(name, s["name"], t) for name, a in accounts.items() for s in a["splits"] for t in s["targets"]]
    flagged = [{"capture": n, "split": s, "layer": t["layer"], "rounding": t["rounding"]}
               for n, s, t in targets if t["rounding_flag"]]
    worst = max(targets, key=lambda x: x[2]["rounding"])
    return {
        "token_mismatches": {n: a["token_check"]["mismatches"] for n, a in accounts.items()},
        "targets": len(targets),
        "largest_gap_from_one": r4(max(abs(t["shares"]["embedding"] + t["shares"]["attention"] + t["shares"]["experts"] - 1)
                                       for _, _, t in targets)),
        "rounding_worst": {"capture": worst[0], "split": worst[1], "layer": worst[2]["layer"], "rounding": worst[2]["rounding"]},
        "rounding_flagged": flagged,
        "rounding_worst_by_capture": {n: max(t["rounding"] for m, _, t in targets if m == n) for n in accounts},
        "never_beyond_null": [f"{n}: {s['name']}" for n, a in accounts.items() for s in a["splits"] if not middle(s)],
    }


def designed(accounts: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for name, a in accounts.items():
        splits = []
        for s in a["splits"]:
            mid = middle(s)
            if not mid:
                continue
            raw = Counter(place(t["shares"]["attention"], t["random"]["attention"]) for t in mid)
            disc = Counter(place(t["discriminant"]["shares"]["attention"], t["discriminant"]["random"]["attention"]) for t in mid)
            splits.append({"split": s["name"], "targets": len(mid),
                           "mean_difference": {k: raw[k] for k in ("above", "inside", "below")},
                           "discriminant": {k: disc[k] for k in ("above", "inside", "below")}})
        mid_all = [t for s in a["splits"] for t in middle(s)]
        out[name] = {"experts_share": span([t["shares"]["experts"] for t in mid_all]),
                     "random_experts_median": span([t["random"]["experts"][1] for t in mid_all]),
                     "attention_share": span([t["shares"]["attention"] for t in mid_all]),
                     "splits": splits}
    return out


def two_directions(accounts: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for group, names in (("context", CONTEXT), ("single_words", SINGLE_WORDS)):
        pairs: Counter = Counter()
        gaps, random_gaps = [], []
        for name in names:
            for s in accounts[name]["splits"]:
                for t in middle(s):
                    d = t["discriminant"]
                    pairs[(place(t["shares"]["attention"], t["random"]["attention"]),
                           place(d["shares"]["attention"], d["random"]["attention"]))] += 1
                    gaps.append(d["shares"]["attention"] - t["shares"]["attention"])
                    random_gaps.append(d["random"]["attention"][1] - t["random"]["attention"][1])
        marks = sum(v for (raw, _), v in pairs.items() if raw != "inside")
        g, rg = np.array(gaps), np.array(random_gaps)
        out[group] = {
            "targets": int(sum(pairs.values())),
            "places": {f"{raw} / {disc}": v for (raw, disc), v in sorted(pairs.items())},
            "same_place": sum(v for (raw, disc), v in pairs.items() if raw == disc),
            "marks": marks,
            "marks_holding": sum(v for (raw, disc), v in pairs.items() if raw != "inside" and raw == disc),
            "discriminant_outside": sum(v for (_, disc), v in pairs.items() if disc != "inside"),
            "opposite": sum(v for (raw, disc), v in pairs.items() if {raw, disc} == {"above", "below"}),
            "attention_gap": {"median": r4(np.median(g)), "min": r4(g.min()), "max": r4(g.max()),
                              "abs_90th": r4(np.percentile(np.abs(g), 90))},
            "random_median_gap": {"median": r4(np.median(rg)), "min": r4(rg.min()), "max": r4(rg.max())},
        }
    return out


def main_splits(accounts: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for name, a in accounts.items():
        s = next(x for x in a["splits"] if x["name"] == MAIN[name])
        rows = {}
        for t in s["targets"]:
            d = t["discriminant"]
            rows[str(t["layer"])] = {
                "separation": t["separation"], "null_95": t["null_95"],
                "attention": t["shares"]["attention"], "interval": t["interval"]["attention"],
                "random": t["random"]["attention"], "experts": t["shares"]["experts"],
                "random_experts_median": t["random"]["experts"][1], "embedding": t["shares"]["embedding"],
                "attention_here": t["shares"]["attention_here"],
                "discriminant": d["shares"]["attention"], "discriminant_random": d["random"]["attention"],
                "place": place(t["shares"]["attention"], t["random"]["attention"]),
                "discriminant_place": place(d["shares"]["attention"], d["random"]["attention"]),
                "below_by_band_widths": r4((t["random"]["attention"][0] - t["shares"]["attention"])
                                           / (t["random"]["attention"][2] - t["random"]["attention"][0]))
                if t["shares"]["attention"] < t["random"]["attention"][0] else None,
            }
        out[name] = {"split": s["name"], "n_b": s["n_b"], "n_a": s["n_a"], "grain": s["grain"], "layers": rows}
    return out


def writing(accounts: Dict[str, Any]) -> Dict[str, Any]:
    """The share of each main split at a target written by the last few layers before it."""
    out: Dict[str, Any] = {}
    for target, first in ((12, 7), (12, 9), (20, 17)):
        values = {}
        for name, a in accounts.items():
            t = next(x for x in a["splits"] if x["name"] == MAIN[name])["targets"][target]
            values[name] = r4(sum(t["shares"]["attention_by_layer"][first:target + 1])
                              + sum(t["shares"]["experts_by_layer"][first:target + 1]))
        out[f"L{first}-L{target}"] = {"by_capture": values, "span": span(list(values.values()))}
    return out


def node_splits() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for name in CAPTURES:
        result = load("splits", name)
        branches = result["branches"]
        real = [b for b in branches if b["separation"] > b["null_95"]]
        verdicts, points = Counter(), defaultdict(list)
        for b in real:
            raw = place(b["shares"]["attention_here"], b["random"]["attention_here"])
            disc = place(b["discriminant"]["shares"]["attention_here"], b["discriminant"]["random"]["attention_here"])
            verdicts[(raw, disc)] += 1
            points[b["node"]].append((raw, disc, b["n_b"], b["n_a"], b["parts_at"]))
        width = [(b["discriminant"]["random"]["attention_here"][2] - b["discriminant"]["random"]["attention_here"][0])
                 / (b["random"]["attention_here"][2] - b["random"]["attention_here"][0]) for b in real]
        holding = sorted({(p[0][4], node, raw) for node, p in points.items() for raw, disc, *_ in p
                          if raw != "inside" and raw == disc})
        out[name] = {
            "lens": result["lens"], "version": result["version"],
            "branches": len(branches), "beyond_null": len(real),
            "split_points": len({b["node"] for b in branches}), "split_points_beyond": len(points),
            "mirror_pairs": sum(1 for p in points.values() if len(p) == 2 and p[0][2] == p[1][3] and p[0][3] == p[1][2]),
            "parting_layer_writes": r4(np.median([b["shares"]["attention_here"] + b["shares"]["experts_here"] for b in real])),
            "attention_here": r4(np.median([b["shares"]["attention_here"] for b in real])),
            "random_attention_here": r4(np.median([b["random"]["attention_here"][1] for b in real])),
            "experts_here": r4(np.median([b["shares"]["experts_here"] for b in real])),
            "mean_difference": {k: sum(v for (raw, _), v in verdicts.items() if raw == k) for k in ("above", "inside", "below")},
            "discriminant": {k: sum(v for (_, disc), v in verdicts.items() if disc == k) for k in ("above", "inside", "below")},
            "holding": sum(v for (raw, disc), v in verdicts.items() if raw != "inside" and raw == disc),
            "opposite": sum(v for (raw, disc), v in verdicts.items() if {raw, disc} == {"above", "below"}),
            "points_marked": sum(1 for p in points.values() if any(x[0] != "inside" for x in p)),
            "points_discriminant": sum(1 for p in points.values() if any(x[1] != "inside" for x in p)),
            "points_holding": sum(1 for p in points.values() if any(x[0] != "inside" and x[0] == x[1] for x in p)),
            "band_width_ratio": r4(np.median(width)),
            "holding_points": [{"parts_at": layer, "node": node, "place": raw} for layer, node, raw in holding],
        }
    totals = {key: sum(c[key] for c in out.values()) for key in
              ("branches", "beyond_null", "split_points", "split_points_beyond", "mirror_pairs", "holding",
               "opposite", "points_marked", "points_discriminant", "points_holding")}
    totals["marks"] = sum(c["mean_difference"]["above"] + c["mean_difference"]["below"] for c in out.values())
    totals["discriminant_outside"] = sum(c["discriminant"]["above"] + c["discriminant"]["below"] for c in out.values())
    return {"by_capture": out, "totals": totals}


def variance() -> Optional[Dict[str, Any]]:
    path = RESULTS / "variance.json"
    if not path.exists():
        return None
    result = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for name, rows in result.items():
        r = [row["ratio"] for row in rows]
        out[name] = {"span": span(r), "below_one_at": [row["layer"] for row in rows if row["ratio"] < 1],
                     "span_L0_L16": span(r[:17])}
    return out


def main() -> None:
    accounts = {name: load("account", name) for name in CAPTURES}
    summary = {"checks": checks(accounts), "designed": designed(accounts), "two_directions": two_directions(accounts),
               "main_splits": main_splits(accounts), "writing": writing(accounts), "node_splits": node_splits(),
               "variance": variance()}
    write_results("summary", summary)
    print(json.dumps({key: summary[key] for key in ("two_directions",)}, indent=1))
    print(json.dumps(summary["node_splits"]["totals"]))


if __name__ == "__main__":
    main()
