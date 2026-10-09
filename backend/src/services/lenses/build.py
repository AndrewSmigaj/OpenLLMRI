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
from pydantic import Field, model_validator

from services.lenses.data import LensFilters
from services.lenses.store import HoldoutDesign, SettingsSource, UmapSettings

MAX_ITEMS = 4095  # UMAP's exact small-data path, which keeps its training rows


class LensBuildParams(UmapSettings):
    """A build: the lens-wide UMAP settings (n_neighbors, dimensions, min_dist, metric), or each
    layer's own in `per_layer` (one per layer in capture order) with where each came from in
    `sources`, the k for v1, and the hold-out design later jobs use (the capture's declared one
    when not given)."""
    session_id: str
    name: str
    per_layer: Optional[List[UmapSettings]] = None
    sources: Optional[List[SettingsSource]] = None
    holdout: Optional[HoldoutDesign] = None
    k: Optional[int] = Field(None, ge=1, le=50)
    k_per_layer: Optional[List[int]] = None
    k_auto: Optional[str] = None
    k_source: Optional[str] = None  # where k_per_layer came from (a tuning), instead of "manual"
    source: str = "residual_stream"
    token_position: int = 1
    filters: LensFilters = Field(default_factory=LensFilters)
    seed: int = 42
    workers: Optional[int] = None

    def layer_settings(self, n_layers: int) -> List[UmapSettings]:
        """Each layer's settings: its own when tuned per layer, else the lens-wide ones."""
        if self.per_layer is None:
            return [UmapSettings.of(self)] * n_layers
        if len(self.per_layer) != n_layers:
            raise ValueError(f"per_layer has {len(self.per_layer)} settings for {n_layers} layers")
        return list(self.per_layer)

    @model_validator(mode="after")
    def _one_source_per_setting(self) -> "LensBuildParams":
        wanted = len(self.per_layer) if self.per_layer is not None else 1
        if self.sources is not None and len(self.sources) != wanted:
            raise ValueError(f"sources has {len(self.sources)} entries for {wanted} settings: one per layer of "
                             "per_layer, or one for the lens-wide settings")
        return self


def _fit_one(folder: str, layer: int, settings: Dict[str, Any], seed: int) -> Dict[str, Any]:
    """Fit one layer in a worker process; save its reducer without the training rows.

    The rows are re-read from the capture when the reducer is loaded, and checked against UMAP's
    own hash of them, so a lens stays small and can't silently read a changed capture.
    """
    import joblib

    from services.lenses.fit import fit_reducer, suggest_k, ward_tree

    states = np.load(Path(folder) / "work" / f"X_L{layer:02d}.npy")
    reducer, embedding = fit_reducer(states, UmapSettings.of(settings), seed)
    reducer._raw_data = None
    joblib.dump(reducer, Path(folder) / "fit" / f"umap_L{layer:02d}.joblib", compress=3)
    tree = ward_tree(embedding)
    return {"layer": layer, "embedding": embedding, "tree": tree, "suggestions": suggest_k(embedding, tree)}


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
    settings = p.layer_settings(len(layers))
    dim = int(states[layers[0]].shape[1])
    for layer in layers:
        np.save(tmp / "work" / f"X_L{layer:02d}.npy", states[layer])
    del states
    ctx.check_cancelled()
    fits = _fit_layers(str(tmp), layers, settings, p, ctx)
    ctx.progress("self-check", 0, 1)
    check = _self_checks(len(items), dim, settings, p)
    ctx.log(f"self-check: {'passed' if check['passed'] else 'FAILED'} {check['planted']} {check['null']}")
    _write_lens(tmp, p, items, layers, fits, ctx, started, check)
    shutil.rmtree(tmp / "work")
    os.replace(tmp, final)
    _write_routes(p.session_id, p.name, ctx)
    return {"session_id": p.session_id, "name": p.name, "version": "v1",
            "n_items": len(items), "seconds": round(time.time() - started, 1)}


def _write_routes(session_id: str, name: str, ctx: Any) -> None:
    """The new lens's pipelines, hubs and experts involved (seconds). The lens is already whole, so
    a failure is logged and leaves it to the `lens_routes` job."""
    import traceback

    from services.lenses.routes import write_routes

    ctx.progress("routes", 0, 1)
    try:
        write_routes(session_id, name)
    except Exception:
        traceback.print_exc()


def _workers(p: LensBuildParams) -> int:
    return p.workers or max(1, min(6, (os.cpu_count() or 2) - 2))


def _fit_layers(folder: str, layers: List[int], settings: List[UmapSettings], p: LensBuildParams,
                ctx: Any) -> Dict[int, Dict[str, Any]]:
    """Fit every layer with its own settings, spread over worker processes; results are identical
    whatever the count."""
    from joblib import Parallel, delayed

    ctx.progress("fitting", 0, len(layers))
    results: Dict[int, Dict[str, Any]] = {}
    jobs = (delayed(_fit_one)(folder, layer, settings[li].model_dump(), p.seed) for li, layer in enumerate(layers))
    for fitted in Parallel(n_jobs=_workers(p), backend="loky", return_as="generator_unordered")(jobs):
        results[int(fitted["layer"])] = fitted
        ctx.progress("fitting", len(results), len(layers))
        ctx.check_cancelled()
    return results


def _self_checks(n: int, dim: int, settings: List[UmapSettings], p: LensBuildParams) -> Dict[str, Any]:
    """The self-check for each distinct setting (C4). One setting keeps today's record; several give
    the same shape with the worst planted and null results, passing only if every setting passes."""
    from joblib import Parallel, delayed

    from services.lenses.validate import self_check

    distinct = list({s.model_dump_json(): s for s in settings}.values())  # whole settings, metric included
    checks = Parallel(n_jobs=min(_workers(p), len(distinct)), backend="loky")(
        delayed(self_check)(n, dim, s, p.seed) for s in distinct)
    if len(checks) == 1:
        only: Dict[str, Any] = checks[0]
        return only
    worst = dict(checks[0])
    worst["passed"] = all(check["passed"] for check in checks)
    worst["planted"] = min((check["planted"] for check in checks), key=lambda c: c["ari_k5"])
    worst["null"] = max((check["null"] for check in checks), key=lambda c: c["ami_k5"])
    worst["per_settings"] = [s.model_dump() | {"passed": check["passed"], "planted": check["planted"],
                                                "null": check["null"]} for s, check in zip(distinct, checks)]
    return worst


def _write_lens(tmp: Path, p: LensBuildParams, items: List[Any], layers: List[int],
                fits: Dict[int, Dict[str, Any]], ctx: Any, started: float, check: Dict[str, Any]) -> None:
    from services.lenses.data import load_routing, own_top4

    ctx.progress("writing", 0, 1)
    # Layers tuned to different dimensions are zero-padded to the widest: zero columns change no
    # distance, so the Ward trees, silhouettes and votes are the same
    width = max(int(fits[layer]["embedding"].shape[1]) for layer in layers)
    padded = [np.pad(fits[layer]["embedding"], ((0, 0), (0, width - fits[layer]["embedding"].shape[1])))
              for layer in layers]
    np.savez_compressed(tmp / "fit" / "embed.npz", embedding=np.stack(padded))  # the 3-D view draws this (frame.py)
    np.savez_compressed(tmp / "fit" / "ward.npz", trees=np.stack([fits[layer]["tree"] for layer in layers]))
    experts, weights = own_top4(load_routing(p.session_id, [r.probe_id for r in items], p.token_position))
    np.savez_compressed(tmp / "fit" / "top4.npz", experts=experts, weights=weights.astype(np.float16))
    _write_items(tmp / "items.parquet", items)
    _write_manifest(tmp, p, items, layers, {str(layer): fits[layer]["suggestions"] for layer in layers},
                    ctx, started, check)
    from services.lenses.versions import new_version, resolve_k

    k_per_layer, k_source = resolve_k(layers, {str(layer): fits[layer]["suggestions"] for layer in layers},
                                      p.k, p.k_per_layer, p.k_auto)
    if p.k_per_layer is not None and p.k_source:
        k_source = [p.k_source] * len(layers)
    new_version(tmp, k_per_layer, k_source)


_ITEM_FIELDS = ("probe_id", "label", "categories_json", "output_category", "output_category_json",
                "input_text", "target_word", "sentence_index", "turn_id", "scenario_id", "capture_type",
                "target_token_count")


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
        default_holdout,
        git_state,
        write_manifest,
    )

    commit, dirty = git_state()
    manifest = LensManifest(
        name=p.name, session_id=session_dir(p.session_id).name, capture=_session_info(p.session_id),
        site=LensSite(source=p.source, token_position=p.token_position), filters=p.filters,
        settings=LensSettings(**UmapSettings.of(p).model_dump(), seed=p.seed, per_layer=p.per_layer,
                              sources=p.sources),
        holdout=p.holdout or default_holdout(p.session_id),
        n_items=len(items), layers=layers, suggestions=suggestions, self_check=check,
        provenance=Provenance(
            commit=commit, dirty=dirty, job_id=ctx.job_id,
            created_by=ctx.store.load(ctx.job_id).created_by,
            seconds=round(time.time() - started, 1),
            libraries={"umap-learn": umap.__version__, "scikit-learn": sklearn.__version__,
                       "numpy": np.__version__}))
    write_manifest(tmp, manifest)
