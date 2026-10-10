"""Where the dual-purpose objects sit on the harm axis (the object study, 10d.6).

The mass-mean lens `harm-axis` puts benign objects at -1 and harmful ones at +1 at every layer
(fitted on those two classes only); the dual-purpose objects were never fitted, so their readings
are the measurement. For every layer: each class's median and middle half; the dual objects' median
by how they harm and by domain; and, at the layer where the axis separates its two classes best
held out, every dual object ranked from the harmful end to the benign end.

  .venv/bin/python docs/studies/objects_harm/analysis/harm_axis.py [SESSION] [LENS]

(defaults: session_2be574c4, harm-axis). Writes results/ and figures/ beside this file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend/src"))
HERE = Path(__file__).parent
SET = ROOT / "data/sentence_sets/lexical/objects_harm_v1.json"


def quartiles(values: np.ndarray) -> Dict[str, float]:
    return {"q1": float(np.percentile(values, 25)), "median": float(np.median(values)),
            "q3": float(np.percentile(values, 75)), "n": int(len(values))}


def main(session: str, lens: str) -> None:
    from services.lenses.massmean import readings
    from services.lenses.store import lens_dir

    found = readings(lens_dir(session, lens), session)
    validation = json.loads((lens_dir(session, lens) / "validation.json").read_text(encoding="utf-8"))
    entries = {e["text"]: {**e, "group": g["label"]}
               for g in json.loads(SET.read_text(encoding="utf-8"))["groups"] for e in g["sentences"]}
    import pyarrow.parquet as pq

    from services.lenses.data import session_dir
    text_of = {r["probe_id"]: r["input_text"] for r in
               pq.read_table(session_dir(session) / "tokens.parquet", columns=["probe_id", "input_text"]).to_pylist()}
    items = [entries[text_of[it["probe_id"]]] for it in found["items"]]
    values = np.array(found["readings"])  # [item, layer]
    layers = found["layers"]
    label = np.array([e["group"] for e in items])
    dual = np.flatnonzero(label == "dual")
    best = max(layers, key=lambda layer: validation["layers"][str(layer)]["accuracy"])
    bi = layers.index(best)
    by = {"harm": np.array([e["categories"]["harm"] for e in items]),
          "domain": np.array([e["categories"]["domain"] for e in items])}
    results: Dict[str, Any] = {
        "session": session, "lens": lens, "contrast": found["contrast"], "layers": layers,
        "heldout_accuracy": {layer: validation["layers"][str(layer)]["accuracy"] for layer in layers},
        "best_layer": best,
        "classes": {c: [quartiles(values[label == c, li]) for li in range(len(layers))]
                    for c in ("harmful", "dual", "benign")},
        "dual_above_zero": [int((values[dual, li] > 0).sum()) for li in range(len(layers))],
        "dual_by": {field: {v: [quartiles(values[dual[by[field][dual] == v], li]) for li in range(len(layers))]
                            for v in sorted(set(by[field][dual]))} for field in by},
        "dual_ranked_at_best": [{"word": items[i]["target_word"], "harm": items[i]["categories"]["harm"],
                                 "domain": items[i]["categories"]["domain"], "reading": round(float(values[i, bi]), 3)}
                                for i in dual[np.argsort(-values[dual, bi])]],
    }
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / f"harm_axis_{lens}.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    chart(results, lens, values, label, dual, items)
    print(f"best layer L{best} (held-out accuracy {results['heldout_accuracy'][best]:.3f}); "
          f"dual above 0 there: {results['dual_above_zero'][bi]} of {len(dual)}")
    for field in by:
        meds = {v: q[bi]["median"] for v, q in results["dual_by"][field].items()}
        print(f"  dual by {field} at L{best}: " + ", ".join(f"{v} {m:+.2f}" for v, m in sorted(meds.items(), key=lambda kv: -kv[1])))


def chart(results: Dict[str, Any], lens: str, values: np.ndarray, label: np.ndarray, dual: np.ndarray,
          items: list) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    layers = results["layers"]
    colours = {"harmful": "#e41a1c", "dual": "#377eb8", "benign": "#4daf4a"}
    fig, axes = plt.subplots(1, 2, figsize=(15, 7.5), gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axes[0]
    for c, qs in results["classes"].items():
        ax.fill_between(layers, [q["q1"] for q in qs], [q["q3"] for q in qs], color=colours[c], alpha=0.15, lw=0)
        ax.plot(layers, [q["median"] for q in qs], color=colours[c], lw=2, label=f"{c} ({qs[0]['n']})")
    for y in (-1, 1):
        ax.axhline(y, color="#9ca3af", lw=0.8, ls=":")
    ax.set_xlabel("layer")
    ax.set_ylabel(f"reading: {results['contrast']['label_a']} −1 to {results['contrast']['label_b']} +1")
    ax.set_title("Each class: median and middle half", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    ax = axes[1]
    best = results["best_layer"]
    ranked = results["dual_ranked_at_best"]
    harms = sorted({r["harm"] for r in ranked})
    palette = dict(zip(harms, ("#1d4ed8", "#d97706", "#059669", "#dc2626", "#7c3aed", "#0891b2", "#a65628", "#f781bf")))
    ys = np.arange(len(ranked))
    ax.barh(ys, [r["reading"] for r in ranked], color=[palette[r["harm"]] for r in ranked], height=0.8)
    ax.set_yticks(ys, [r["word"] for r in ranked], fontsize=5.5)
    ax.invert_yaxis()
    for y in (-1, 1):
        ax.axvline(y, color="#9ca3af", lw=0.8, ls=":")
    ax.axvline(0, color="#374151", lw=0.8)
    ax.set_xlabel(f"reading at L{best}")
    ax.set_title(f"The {len(ranked)} dual-purpose objects at L{best}, by how they harm", fontsize=11)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=palette[h], label=h) for h in harms], fontsize=8, loc="lower right")
    fig.suptitle(f"The harm axis ({lens}): benign at −1, harmful at +1; dual-purpose objects read, never fitted",
                 fontsize=12)
    fig.tight_layout()
    figures = HERE / "figures"
    figures.mkdir(exist_ok=True)
    fig.savefig(figures / f"harm_axis_{lens}.png", dpi=150)


if __name__ == "__main__":
    args = sys.argv[1:] or ["session_2be574c4", "harm-axis"]
    if len(args) != 2:
        raise SystemExit(__doc__)
    main(*args)
