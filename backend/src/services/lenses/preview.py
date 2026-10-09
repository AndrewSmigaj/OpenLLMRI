"""A one-layer preview (DESIGN.md E3): one layer of a capture fitted with the form's settings, in
seconds, before all its layers are built: the layer's 3-D view, its nodes at k, and how well its
clusters match each designed axis, held out on request.

It is the `lens_preview` job, in a lane of its own so it never waits behind a search, and it runs
pinned like every job, so its points and nodes equal a build's for the same settings and seed.
`preview.json` in the job's folder holds what it found; `GET /api/lenses/previews/{job}` serves it.

No score that uses labels sees the test portion: the families a search would draw for its test,
by the hold-out design's share and the seed (`search.split_test`), are left out of the AMI and
the held-out scores. A search's test score of a lens built from previewed settings therefore stays
honest. The fit itself uses no labels and covers every item.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

import numpy as np
from pydantic import BaseModel, Field

from services.lenses.data import LensFilters
from services.lenses.store import HoldoutDesign, UmapSettings

Array = np.ndarray[Any, Any]
K_MAX = 10  # every k from 2 to this (or to the k asked for, if larger) is scored


class PreviewParams(BaseModel):
    session_id: str
    layer: int = Field(ge=0)
    settings: UmapSettings = Field(default_factory=UmapSettings)
    k: int = Field(default=6, ge=2, le=50)
    seed: int = 42
    source: str = "residual_stream"
    token_position: int = 1
    filters: LensFilters = Field(default_factory=LensFilters)
    holdout: Optional[HoldoutDesign] = None  # the capture's declared design when not given
    held_out: bool = False  # also score held out, on the selection portion's family folds
    n_folds: int = Field(default=5, ge=2, le=10)


def run_preview(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_preview` job: fit one layer, cut its tree at every k, score the cuts against the
    designed axes outside the test portion, and write `preview.json`."""
    from sklearn.metrics import adjusted_mutual_info_score as ami
    from sklearn.metrics import silhouette_score

    from services.lenses.build import MAX_ITEMS
    from services.lenses.data import load_items, load_states
    from services.lenses.fit import cut, fit_reducer, ward_tree
    from services.lenses.flows import axes_of_items
    from services.lenses.frame import principal
    from services.lenses.search import split_test
    from services.lenses.store import default_holdout
    from services.lenses.validate import axis_codes, heldout_scores, make_folds, merge_folds
    from services.lenses.view import _item_dict

    started = time.time()
    p = PreviewParams.model_validate(params)
    ctx.progress("loading", 0, 1)
    records = load_items(p.session_id, p.filters)
    n = len(records)
    if not 10 <= n <= MAX_ITEMS:
        raise ValueError(f"{n} items after the filters; a preview, like a lens, needs 10 to {MAX_ITEMS}")
    if p.k >= n:
        raise ValueError(f"k {p.k} needs more than {n} items")
    items = [_item_dict(vars(r)) for r in records]
    states = load_states(p.session_id, [r.probe_id for r in records], p.source, p.token_position, [p.layer])
    if p.layer not in states:
        raise ValueError(f"layer {p.layer} isn't in the capture")
    x = states[p.layer]
    design = p.holdout or default_holdout(p.session_id)
    axes = {axis: values for axis, values in axes_of_items(items).items()
            if axis != design.family_field and len(values) >= 2}
    codes = axis_codes(items, axes)
    labels = axis_codes(items, {"label": sorted({str(item["label"]) for item in items})})["label"]
    test, drawn = split_test(items, labels, design.family_field, design.test_share, p.seed, design.whole_families)
    keep = np.setdiff1d(np.arange(n), test)  # the selection portion: every label-based score stays here

    ctx.progress("fitting", 0, 1)
    ctx.check_cancelled()
    _, embedding = fit_reducer(x, p.settings, p.seed)
    tree = ward_tree(embedding)
    ks = [k for k in range(2, max(K_MAX, p.k) + 1) if k < n]
    cuts = {k: cut(tree, k) for k in ks}
    centred = embedding - embedding.mean(axis=0)
    basis, share = principal(centred)
    points = centred[:, :basis.shape[0]] @ basis

    in_sample: Dict[str, Dict[str, float]] = {}
    for axis, c in codes.items():
        known = keep[c[keep] >= 0]
        if known.size:
            in_sample[axis] = {str(k): round(float(ami(c[known], cuts[k][known])), 4) for k in ks}
    silhouette = {str(k): round(float(silhouette_score(embedding, cuts[k])), 4)
                  for k in ks if 1 < len(np.unique(cuts[k])) < n}

    heldout: Optional[Dict[str, Any]] = None
    folding: Optional[Dict[str, Any]] = None
    if p.held_out:
        ctx.progress("holding out", 0, 1)
        ctx.check_cancelled()
        folds, folding = make_folds([items[int(i)] for i in keep], design.family_field, p.n_folds, p.seed,
                                    design.whole_families)
        folds, merged = merge_folds(folds, p.n_folds)
        folding = {key: value for key, value in folding.items() if key != "families"} | {"n_folds": len(folds)}
        if merged:
            folding["merged_from"] = merged
        scores = heldout_scores(x[keep], folds, {axis: c[keep] for axis, c in codes.items()}, p.settings, p.seed, ks)
        heldout = {str(k): {axis: {m: found[m] for m in ("ami", "kappa", "accuracy")} for axis, found in scores[k].items()}
                   for k in scores}

    record = {
        "format": 1, "session_id": p.session_id, "layer": p.layer, "settings": p.settings.model_dump(),
        "k": p.k, "seed": p.seed, "site": {"source": p.source, "token_position": p.token_position},
        "filters": p.filters.model_dump(), "holdout": design.model_dump(), "n_items": n,
        "axes": axes, "share": round(share, 4), "ks": ks,
        "items": [{key: item[key] for key in ("probe_id", "label", "categories", "input_text")} for item in items],
        "points": np.round(points, 4).tolist(),
        "nodes": cuts[p.k].tolist(),
        "in_sample": {"ami": in_sample, "silhouette": silhouette},
        "test": drawn,  # left out of every label-based score
        "heldout": heldout, "folds": folding,
        "seconds": round(time.time() - started, 1),
    }
    tmp = ctx.job_dir / ".preview.json.tmp"
    tmp.write_text(json.dumps(record), encoding="utf-8")
    os.replace(tmp, ctx.job_dir / "preview.json")
    ctx.progress("done", 1, 1)
    return {"session_id": p.session_id, "layer": p.layer, "k": p.k, "n_items": n, "held_out": p.held_out,
            "seconds": record["seconds"]}
