"""Mass-mean lenses: one designed contrast per layer, read as a position (DESIGN.md B1, C4).

At each layer the axis is the difference of the two classes' mean states. A reading is the
projection scaled so the class means land at -1 and +1 (`fit.mass_mean_reading`). Validation
uses the paper's algorithm (`docs/studies/context_shift/analysis/scene_heldout_calibration.py`):
fold i holds out scene family i of each class, the axis is fitted on the rest, and held-out
items are classified by the sign of their reading. Without scene families the folds are
stratified (identical texts together) and marked weaker, as for UMAP lenses.

A lens folder holds `lens.json` (kind "mass_mean", its contrast), `items.parquet`,
`fit/axes.npz` (axis and midpoint per layer, and the axes' squared lengths) and `validation.json`.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

import numpy as np
from pydantic import BaseModel, Field

from services.lenses.data import LensFilters

Array = np.ndarray[Any, Any]


class MassMeanParams(BaseModel):
    session_id: str
    name: str
    label_a: str
    label_b: str
    source: str = "residual_stream"
    token_position: int = 1
    filters: LensFilters = Field(default_factory=LensFilters)
    family_field: str = "scene"
    whole_families: bool = False  # family names as they are, not their first two tokens
    n_folds: int = Field(5, ge=2, le=20)
    seed: int = 42


def heldout_layer(states: Array, is_b: Array, folds: List[Array]) -> Dict[str, Any]:
    """One layer's held-out scores: per fold an axis from the training items, the held-out items
    classified by the sign of their reading. `accuracy` is the mean over folds (the paper's
    figure); `pooled_accuracy` and `kappa` pool every held-out item."""
    from sklearn.metrics import cohen_kappa_score

    from services.lenses.fit import mass_mean_axis, mass_mean_reading

    n = len(states)
    accuracies: List[float] = []
    truth: List[Array] = []
    predicted: List[Array] = []
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        if is_b[train].all() or (~is_b[train]).all():
            continue
        axis, mid, norm2 = mass_mean_axis(states[train], is_b[train])
        guess = mass_mean_reading(states[test], axis, mid, norm2) > 0
        accuracies.append(float((guess == is_b[test]).mean()))
        truth.append(is_b[test])
        predicted.append(guess)
    every_truth, every_guess = np.concatenate(truth), np.concatenate(predicted)
    return {"accuracy": round(float(np.mean(accuracies)), 4),
            "pooled_accuracy": round(float((every_truth == every_guess).mean()), 4),
            "kappa": round(float(cohen_kappa_score(every_truth, every_guess)), 4),
            "worst_fold": round(float(min(accuracies)), 4), "folds": len(accuracies)}


def build_mass_mean(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `mass_mean_build` job: the contrast's axis at every layer, held-out scores, the lens."""
    from services.lenses.build import _session_info, _write_items
    from services.lenses.data import load_items, load_states, session_dir
    from services.lenses.fit import mass_mean_axis
    from services.lenses.store import (
        LensManifest,
        LensSite,
        Provenance,
        git_state,
        lens_dir,
        write_manifest,
    )
    from services.lenses.validate import make_folds
    from services.lenses.view import _item_dict

    started = time.time()
    p = MassMeanParams.model_validate(params)
    final = lens_dir(p.session_id, p.name)
    if final.exists():
        raise FileExistsError(f"lens {p.name!r} already exists in {p.session_id}")
    filters = p.filters.model_copy(update={"labels": [p.label_a, p.label_b]})
    ctx.progress("loading", 0, 1)
    items = load_items(p.session_id, filters)
    is_b = np.array([r.label == p.label_b for r in items])
    if len(items) < 10 or is_b.all() or not is_b.any():
        raise ValueError(f"{len(items)} items with labels {p.label_a!r} and {p.label_b!r}; "
                         "a mass-mean lens needs both labels and 10 items or more")
    states = load_states(p.session_id, [r.probe_id for r in items], p.source, p.token_position)
    layers = sorted(states)
    folds, folding = make_folds([_item_dict(vars(r)) for r in items], p.family_field, p.n_folds, p.seed,
                                p.whole_families)
    tmp = final.parent / f".tmp-{p.name}-{ctx.job_id}"
    ctx.add_temp_path(tmp)
    (tmp / "fit").mkdir(parents=True)
    axes, mids, norms, scores = [], [], [], {}
    for i, layer in enumerate(layers):
        axis, mid, norm2 = mass_mean_axis(states[layer], is_b)
        axes.append(axis)
        mids.append(mid)
        norms.append(norm2)
        scores[str(layer)] = heldout_layer(states[layer], is_b, folds) | {
            "n_a": int((~is_b).sum()), "n_b": int(is_b.sum()), "axis_norm": round(float(np.sqrt(norm2)), 4)}
        ctx.progress("fitting", i + 1, len(layers))
        ctx.check_cancelled()
    np.savez_compressed(tmp / "fit" / "axes.npz", axis=np.stack(axes), mid=np.stack(mids), norm2=np.array(norms))
    _write_items(tmp / "items.parquet", items)
    commit, dirty = git_state()
    provenance = Provenance(commit=commit, dirty=dirty, job_id=ctx.job_id,
                            created_by=ctx.store.load(ctx.job_id).created_by,
                            seconds=round(time.time() - started, 1), libraries={"numpy": np.__version__})
    contrast = {"label_a": p.label_a, "label_b": p.label_b}
    write_manifest(tmp, LensManifest(
        name=p.name, kind="mass_mean", contrast=contrast, session_id=session_dir(p.session_id).name,
        capture=_session_info(p.session_id), site=LensSite(source=p.source, token_position=p.token_position),
        filters=filters, n_items=len(items), layers=layers, provenance=provenance))
    record = {"format": 1, "kind": "mass_mean", "contrast": contrast, "folds": folding, "layers": scores,
              "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id,
                             "seconds": provenance.seconds, "created_at": provenance.created_at}}
    (tmp / "validation.json").write_text(json.dumps(record), encoding="utf-8")
    os.replace(tmp, final)
    best = max(scores.items(), key=lambda pair: pair[1]["accuracy"])
    return {"session_id": session_dir(p.session_id).name, "name": p.name, "n_items": len(items),
            "best_layer": int(best[0]), "best_accuracy": best[1]["accuracy"], "seconds": provenance.seconds}


def readings(lens_folder: Any, target_session: str, position: Optional[int] = None,
             filters: Optional[LensFilters] = None) -> Dict[str, Any]:
    """Any capture read through a saved mass-mean lens at its site: each item's position along
    the contrast at every layer (the class means of the lens's own items sit at -1 and +1)."""
    from services.lenses.data import load_items, load_states
    from services.lenses.fit import mass_mean_reading
    from services.lenses.store import read_manifest
    from services.lenses.view import _item_dict

    manifest = read_manifest(lens_folder)
    fitted = np.load(lens_folder / "fit" / "axes.npz")
    items = load_items(target_session, filters or LensFilters())
    at = manifest.site.token_position if position is None else position
    states = load_states(target_session, [r.probe_id for r in items], manifest.site.source, at)
    values = {layer: mass_mean_reading(states[layer], fitted["axis"][li], fitted["mid"][li], float(fitted["norm2"][li]))
              for li, layer in enumerate(manifest.layers) if layer in states}
    shown = [_item_dict(vars(r)) for r in items]
    return {"lens": manifest.name, "contrast": manifest.contrast, "target": target_session, "position": at,
            "layers": sorted(values), "items": [{k: d[k] for k in ("probe_id", "label", "categories", "step")} for d in shown],
            "readings": [[round(float(values[layer][i]), 4) for layer in sorted(values)] for i in range(len(items))]}
