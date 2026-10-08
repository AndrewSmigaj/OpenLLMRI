"""Building a UMAP lens: the `lens_build` background job.

Stages: load the capture's states at the site, fit every layer once (layers spread over worker
processes), save each layer's reducer and Ward tree, record the model's own top-4 routing, write
the manifest, and cut version v1 at the requested k. Everything is written into a temporary
folder and renamed into place at the end, so a lens is either whole or absent.
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from pydantic import BaseModel, Field

from services.lenses.data import LensFilters

MAX_ITEMS = 4095  # UMAP's exact small-data path, which keeps its training rows


class LensBuildParams(BaseModel):
    session_id: str
    name: str
    n_neighbors: int = Field(15, ge=2, le=200)
    dimensions: int = Field(6, ge=2, le=50)
    k: Optional[int] = Field(None, ge=1, le=50)
    k_per_layer: Optional[List[int]] = None
    k_auto: Optional[str] = None
    source: str = "residual_stream"
    token_position: int = 1
    filters: LensFilters = Field(default_factory=LensFilters)
    seed: int = 42
    workers: Optional[int] = None


def _fit_one(folder: str, layer: int, n_neighbors: int, dimensions: int, seed: int) -> Dict[str, Any]:
    """Fit one layer in a worker process; save its reducer without the training rows.

    The rows are re-read from the capture when the reducer is loaded, and checked against UMAP's
    own hash of them, so a lens stays small and can't silently read a changed capture.
    """
    import joblib

    from services.lenses.fit import fit_layer, suggest_k, ward_tree

    states = np.load(Path(folder) / "work" / f"X_L{layer:02d}.npy")
    reducer, embedding, view = fit_layer(states, n_neighbors, dimensions, seed)
    reducer._raw_data = None
    joblib.dump(reducer, Path(folder) / "fit" / f"umap_L{layer:02d}.joblib", compress=3)
    tree = ward_tree(embedding)
    return {"layer": layer, "embedding": embedding, "view": view, "tree": tree,
            "suggestions": suggest_k(embedding, tree)}


def build_lens(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_build` job: build a lens from `params` (LensBuildParams); ctx is a JobContext."""
    from services.lenses.data import load_items, load_states
    from services.lenses.store import lens_dir

    started = time.time()
    p = LensBuildParams.model_validate(params)
    final = lens_dir(p.session_id, p.name)
    if final.exists():
        raise FileExistsError(f"lens {p.name!r} already exists in {p.session_id}")
    tmp = final.parent / f".tmp-{p.name}-{ctx.job_id}"
    ctx.add_temp_path(tmp)
    (tmp / "work").mkdir(parents=True)
    (tmp / "fit").mkdir()

    ctx.progress("loading", 0, 1)
    items = load_items(p.session_id, p.filters)
    if not 10 <= len(items) <= MAX_ITEMS:
        raise ValueError(f"{len(items)} items after the filters; a lens needs 10 to {MAX_ITEMS} "
                         "(set filters.max_items to subsample a larger capture)")
    ids = [r.probe_id for r in items]
    states = load_states(p.session_id, ids, p.source, p.token_position)
    layers = sorted(states)
    dim = int(states[layers[0]].shape[1])
    for layer in layers:
        np.save(tmp / "work" / f"X_L{layer:02d}.npy", states[layer])
    del states
    ctx.check_cancelled()
    fits = _fit_layers(str(tmp), layers, p, ctx)
    ctx.progress("self-check", 0, 1)
    from services.lenses.validate import self_check

    check = self_check(len(items), dim, p.n_neighbors, p.dimensions, p.seed)
    ctx.log(f"self-check: {'passed' if check['passed'] else 'FAILED'} {check['planted']} {check['null']}")
    _write_lens(tmp, p, items, layers, fits, ctx, started, check)
    shutil.rmtree(tmp / "work")
    os.replace(tmp, final)
    return {"session_id": p.session_id, "name": p.name, "version": "v1",
            "n_items": len(items), "seconds": round(time.time() - started, 1)}


def _fit_layers(folder: str, layers: List[int], p: LensBuildParams, ctx: Any) -> Dict[int, Dict[str, Any]]:
    """Fit every layer, spread over worker processes; results are identical whatever the count."""
    from joblib import Parallel, delayed

    workers = p.workers or max(1, min(6, (os.cpu_count() or 2) - 2))
    ctx.progress("fitting", 0, len(layers))
    results: Dict[int, Dict[str, Any]] = {}
    jobs = (delayed(_fit_one)(folder, layer, p.n_neighbors, p.dimensions, p.seed) for layer in layers)
    for fitted in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(jobs):
        results[int(fitted["layer"])] = fitted
        ctx.progress("fitting", len(results), len(layers))
        ctx.check_cancelled()
    return results


def _write_lens(tmp: Path, p: LensBuildParams, items: List[Any], layers: List[int],
                fits: Dict[int, Dict[str, Any]], ctx: Any, started: float, check: Dict[str, Any]) -> None:
    from services.lenses.data import load_routing, own_top4

    ctx.progress("writing", 0, 1)
    np.savez_compressed(tmp / "fit" / "embed.npz",
                        embedding=np.stack([fits[layer]["embedding"] for layer in layers]),
                        view3d=np.stack([fits[layer]["view"] for layer in layers]))
    np.savez_compressed(tmp / "fit" / "ward.npz", trees=np.stack([fits[layer]["tree"] for layer in layers]))
    experts, weights = own_top4(load_routing(p.session_id, [r.probe_id for r in items], p.token_position))
    np.savez_compressed(tmp / "fit" / "top4.npz", experts=experts, weights=weights.astype(np.float16))
    _write_items(tmp / "items.parquet", items)
    _write_manifest(tmp, p, items, layers, {str(layer): fits[layer]["suggestions"] for layer in layers},
                    ctx, started, check)
    from services.lenses.versions import new_version, resolve_k

    k_per_layer, k_source = resolve_k(layers, {str(layer): fits[layer]["suggestions"] for layer in layers},
                                      p.k, p.k_per_layer, p.k_auto)
    new_version(tmp, k_per_layer, k_source)


_ITEM_FIELDS = ("probe_id", "label", "categories_json", "output_category", "output_category_json",
                "input_text", "target_word", "sentence_index", "turn_id", "scenario_id", "capture_type")


def _write_items(path: Path, items: List[Any]) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    table = pa.table({field: [getattr(r, field) for r in items] for field in _ITEM_FIELDS})
    pq.write_table(table, path)


def _session_info(session_id: str) -> Dict[str, Any]:
    from services.lenses.data import session_dir

    folder = session_dir(session_id)
    path = folder.parent / "_sessions" / f"{folder.name}.json"
    if not path.exists():
        return {}
    meta = json.loads(path.read_text(encoding="utf-8"))
    return {key: meta.get(key) for key in ("sentence_set_name", "model_name", "prompt_format", "target_word")}


def _write_manifest(tmp: Path, p: LensBuildParams, items: List[Any], layers: List[int],
                    suggestions: Dict[str, Dict[str, Any]], ctx: Any, started: float,
                    check: Dict[str, Any]) -> None:
    import sklearn
    import umap

    from services.lenses.data import session_dir
    from services.lenses.store import (
        LensManifest,
        LensSettings,
        LensSite,
        Provenance,
        git_state,
        write_manifest,
    )

    commit, dirty = git_state()
    manifest = LensManifest(
        name=p.name, session_id=session_dir(p.session_id).name, capture=_session_info(p.session_id),
        site=LensSite(source=p.source, token_position=p.token_position), filters=p.filters,
        settings=LensSettings(n_neighbors=p.n_neighbors, dimensions=p.dimensions, seed=p.seed),
        n_items=len(items), layers=layers, suggestions=suggestions, self_check=check,
        provenance=Provenance(
            commit=commit, dirty=dirty, job_id=ctx.job_id,
            created_by=ctx.store.load(ctx.job_id).created_by,
            seconds=round(time.time() - started, 1),
            libraries={"umap-learn": umap.__version__, "scikit-learn": sklearn.__version__,
                       "numpy": np.__version__}))
    write_manifest(tmp, manifest)
