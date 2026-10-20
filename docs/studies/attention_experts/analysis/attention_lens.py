"""Attention's write as a population: a lens on what attention adds, beside the lens on the state.

Andrew asked (2026-10-20) for an attention Sankey over the population, so that a lens's items can be
read from three sources: the state (the latent nodes), the expert routes, and attention. A first
check grouped items by where attention reads from (by role and by distance): those groups follow
where the read word sits in the sentence, not its meaning. This script tests the other reading:
what attention writes.

At every layer, three sources at the lens's read token, each held out exactly as the lens's own
validation holds out the state (`services.lenses.validate.heldout_scores`: UMAP with the lens's
settings and Ward fitted on the training folds, held-out items placed and voted into nodes):
- the state: the layer's output (what the lens itself reads);
- attention's write: the layer's output minus its input minus the experts' write;
- the experts' write: the gate-weighted sum of the four experts' outputs.
Every designed axis is scored at every k from 2 to 10, with the validation's decoys (drawn within
each label value) as the chance line. The folds are the lens's own (its hold-out design).

Usage (from the repo root): .venv/bin/python docs/studies/attention_experts/analysis/attention_lens.py
       [capture ...] [--workers N]
Results: results/attention_lens_<capture>.json; figure: figures/attention_lens.png (figure()).
"""
import argparse
import json
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict, List, Tuple

import numpy as np

import common

SOURCES = ("state", "attention", "experts")
K_RANGE = list(range(2, 11))
CAPTURES = ("framing", "calibration", "friend_foe", "tank")
LINE = 95  # the decoy line: this percentile of the decoys' held-out AMI, pooled over layers


def _score(task: Tuple[np.ndarray, List[np.ndarray], Dict[str, np.ndarray], Any, int]) -> Dict[int, Dict[str, Dict[str, float]]]:
    from services.lenses.validate import heldout_scores

    states, folds, codes, settings, seed = task
    return heldout_scores(states, folds, codes, settings, seed, ks=K_RANGE)


def run(name: str, workers: int) -> Dict[str, Any]:
    from services.lenses.axes import decoy_sets, decoy_units
    from services.lenses.flows import axes_of
    from services.lenses.store import lens_dir, read_manifest, resolve_holdout
    from services.lenses.validate import axis_codes, make_folds
    from services.lenses.view import open_lens

    started = time.time()
    cap = common.load_capture(name)
    folder = lens_dir(cap.session, cap.lens)
    manifest = read_manifest(folder)
    design = resolve_holdout(folder, manifest)
    view = open_lens(cap.session, cap.lens)
    axes = {axis: values for axis, values in axes_of(view).items() if axis != design.family_field}
    codes = axis_codes(cap.items, axes)
    folds, folding = make_folds(cap.items, design.family_field, 5, manifest.settings.seed,
                                design.whole_families, design.max_folds)
    families, texts = decoy_units(cap.items, design.family_field, design.whole_families)
    decoys, _ = decoy_sets({axis: c for axis, c in codes.items() if len(axes[axis]) >= 2},
                           families, texts, manifest.settings.seed)
    scored = dict(codes)
    for axis, draws in decoys.items():
        for i, draw in enumerate(draws):
            scored[f"{axis}~decoy{i}"] = draw

    keys, tasks = [], []
    before = cap.embedding if cap.embedding is not None else np.zeros_like(cap.outputs[0], dtype=np.float64)
    for li, layer in enumerate(cap.layers):
        out = cap.outputs[li].astype(np.float64)
        experts = cap.experts[li].astype(np.float64)
        attention = out - before - experts
        before = out
        for source, states in zip(SOURCES, (out, attention, experts)):
            keys.append((layer, source))
            tasks.append((states.astype(np.float32), folds, scored, manifest.settings.at(li), manifest.settings.seed))
    with ProcessPoolExecutor(workers) as pool:
        results = list(pool.map(_score, tasks))

    scores: Dict[str, Dict[str, Any]] = {source: {} for source in SOURCES}
    for (layer, source), result in zip(keys, results):
        scores[source][str(layer)] = {str(k): by_axis for k, by_axis in result.items()}
    record = {"capture": name, "session": cap.session, "lens": cap.lens, "n_items": len(cap.items),
              "axes": axes, "folds": {key: value for key, value in folding.items() if key != "families"},
              "settings": manifest.settings.model_dump(), "layers": cap.layers, "k_range": K_RANGE,
              "scores": scores, "summary": summarize(scores, axes, cap.layers),
              "seconds": round(time.time() - started, 1)}
    path = common.RESULTS / f"attention_lens_{name}.json"
    path.write_text(json.dumps(record, indent=1))
    return record


def summarize(scores: Dict[str, Dict[str, Any]], axes: Dict[str, List[str]], layers: List[int]) -> Dict[str, Any]:
    """Per source and axis: held-out AMI per layer at k = the axis's number of values and at the
    layer's best k, the decoy line at each, and the layers beyond it."""
    out: Dict[str, Any] = {}
    for source, by_layer in scores.items():
        out[source] = {}
        for axis, values in axes.items():
            if len(values) < 2:
                continue
            k_own = str(min(max(len(values), 2), 10))
            own = [by_layer[str(layer)][k_own][axis]["ami"] for layer in layers]
            best = [max(by_layer[str(layer)][str(k)][axis]["ami"] for k in K_RANGE) for layer in layers]
            decoy_own = [entry["ami"] for layer in layers for name, entry in by_layer[str(layer)][k_own].items()
                         if name.startswith(f"{axis}~decoy")]
            decoy_best = [max(by_layer[str(layer)][str(k)][name]["ami"] for k in K_RANGE)
                          for layer in layers for name in by_layer[str(layer)][k_own] if name.startswith(f"{axis}~decoy")]
            line_own = float(np.percentile(decoy_own, LINE)) if decoy_own else 0.0
            line_best = float(np.percentile(decoy_best, LINE)) if decoy_best else 0.0
            out[source][axis] = {
                "k": int(k_own), "ami_at_k": own, "line_at_k": round(line_own, 4),
                "beyond_at_k": [layer for layer, a in zip(layers, own) if a > line_own],
                "ami_best_k": best, "line_best_k": round(line_best, 4),
                "beyond_best_k": [layer for layer, a in zip(layers, best) if a > line_best]}
    return out


def figure(names: List[str]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colours = {"state": "#2b6cb0", "attention": "#d97706", "experts": "#2f855a"}
    fig, axs = plt.subplots(1, len(names), figsize=(4.6 * len(names), 3.6), squeeze=False)
    for ax, name in zip(axs[0], names):
        record = json.loads((common.RESULTS / f"attention_lens_{name}.json").read_text())
        layers = record["layers"]
        for source in SOURCES:
            label = record["summary"][source]["label"]
            ax.plot(layers, label["ami_at_k"], color=colours[source], lw=1.8, label=source)
            ax.axhline(label["line_at_k"], color=colours[source], lw=0.8, ls=":")
        ax.set_title(f"{name}: the label, k = {record['summary']['state']['label']['k']}", fontsize=10)
        ax.set_xlabel("layer")
        ax.set_ylim(-0.05, 1.0)
        ax.grid(alpha=0.3)
    axs[0][0].set_ylabel("held-out AMI with the label")
    axs[0][0].legend(fontsize=8, title="lens on", title_fontsize=8)
    fig.suptitle("A lens on each source, held out as the lens's validation is (dotted: the decoy line)", fontsize=10)
    fig.tight_layout()
    common.FIGURES.mkdir(exist_ok=True)
    fig.savefig(common.FIGURES / "attention_lens.png", dpi=150)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("captures", nargs="*", default=list(CAPTURES))
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    for name in args.captures:
        record = run(name, args.workers)
        label = record["summary"]
        print(f"== {name} ({record['n_items']} items, {record['seconds']} s); folds: {record['folds'].get('kind')}")
        for source in SOURCES:
            s = label[source]["label"]
            print(f"  {source:9s} label AMI at k={s['k']}: "
                  + " ".join(f"{a:.2f}" for a in s["ami_at_k"]) + f"  (line {s['line_at_k']:.2f})")
    figure([name for name in CAPTURES if (common.RESULTS / f"attention_lens_{name}.json").exists()])


if __name__ == "__main__":
    main()
