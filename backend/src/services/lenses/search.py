"""Tuning a lens: the `lens_search` job (DESIGN.md B5, C3, C4).

A search over UMAP's settings and k, layer by layer, starting from a built lens, which fixes the
items, the site, the filters and the seed, and is the baseline. Stages:

1. **split:** a test portion the selection never sees. When every item names its family, about
   `test_share` of each label's families are drawn by the seed (at least two left per label for
   selection); otherwise a stratified share grouped by text, marked weaker. Then at most
   `n_folds` selection folds over the rest, families merged round-robin.
2. **self-check:** each setting must find structure planted in synthetic data (C4); settings
   that fail drop out.
3. **search:** for each layer and setting, every selection fold fits UMAP on its training items,
   places the held-out ones and cuts every k from one Ward tree, scored as validation scores
   (`validate.heldout_scores`).
4. **choose:** per layer, the highest held-out AMI on the target axis over (setting, k). Ties go to
   fewer nodes, then fewer dimensions, more neighbours, larger `min_dist`.
5. **test:** each layer's winner, and the source lens's own settings and k, fitted on the whole
   selection portion and scored on the test portion, beside the raw groupings at the winner's k
   and the supervised ceiling.
6. **build** the tuned lens from the winners (their settings per layer, their k as v1).
7. **validate** it as usual.

`search.json` records everything (nulls, never NaN): first in the job's folder, so a failed build
loses nothing, then in the tuned lens's folder. The test scores are the honest ones: the tuned
lens's own validation reuses items that chose its settings.
"""

from __future__ import annotations

import itertools
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from pydantic import BaseModel, Field

from services.lenses.store import UmapSettings

Array = np.ndarray[Any, Any]

MAX_SETTINGS = 60
SECONDS_PER_FIT = (0.005, 0.25)  # a fit, placement and cuts take about a·n + b seconds for n training items


class SearchGrid(BaseModel):
    """The settings searched: every combination of the three lists."""
    n_neighbors: List[int] = Field(default_factory=lambda: [5, 15, 50])
    dimensions: List[int] = Field(default_factory=lambda: [3, 6, 12])
    min_dist: List[float] = Field(default_factory=lambda: [0.1])

    def settings(self) -> List[UmapSettings]:
        found = [UmapSettings(n_neighbors=n, dimensions=d, min_dist=m)
                 for n, d, m in itertools.product(sorted(set(self.n_neighbors)), sorted(set(self.dimensions)),
                                                  sorted(set(self.min_dist)))]
        if not found:
            raise ValueError("the grid is empty")
        if len(found) > MAX_SETTINGS:
            raise ValueError(f"{len(found)} settings; a search takes at most {MAX_SETTINGS}")
        return found


class LensSearchParams(BaseModel):
    session_id: str
    source_lens: str
    name: Optional[str] = None  # the tuned lens; "<source>-tuned" when not given
    target_axis: str = "label"
    grid: SearchGrid = Field(default_factory=SearchGrid)
    k_min: int = Field(default=2, ge=2, le=10)
    k_max: int = Field(default=10, ge=2, le=10)
    test_share: float = Field(default=0.2, ge=0.1, le=0.5)
    family_field: str = "scene"
    whole_families: bool = False  # family names as they are, not their first two tokens
    n_folds: int = Field(default=5, ge=2, le=10)
    seed: Optional[int] = None  # the source lens's seed when not given
    workers: Optional[int] = None


def tuned_name(source: str, name: Optional[str]) -> str:
    return name or f"{source}-tuned"


def estimate_seconds(n_items: int, n_layers: int, n_settings: int, n_folds: int, workers: int,
                     test_share: float = 0.2) -> float:
    """About how long the search stage takes: one fit per setting, layer and fold."""
    train = n_items * (1 - test_share) * (1 - 1 / n_folds)
    a, b = SECONDS_PER_FIT
    return n_settings * n_layers * n_folds * (a * train + b) / max(1, workers)


def split_test(items: Sequence[Dict[str, Any]], codes: Array, family_field: str, share: float,
               seed: int, whole: bool = False) -> Tuple[Array, Dict[str, Any]]:
    """The test portion's item indices, and how they were drawn. Whole families per label when every
    item names one (and each label has at least three); whole families stratified by label when a
    family holds more than one label (as `make_folds` does); else a stratified share grouped by text."""
    from sklearn.model_selection import StratifiedGroupKFold

    from services.lenses.validate import crossing_families, family_keys

    labels = [str(item.get("label")) for item in items]
    keys = family_keys(items, family_field, whole)
    crossing = crossing_families(labels, keys) if keys is not None else []
    if keys is not None and crossing and len(set(keys)) >= 2:
        splitter = StratifiedGroupKFold(n_splits=min(len(set(keys)), max(2, round(1 / share))), shuffle=True,
                                        random_state=seed)
        _, drawn = next(splitter.split(np.zeros(len(items)), labels, groups=keys))
        grouped = np.sort(np.asarray(drawn))
        return grouped, {"kind": "whole scene families, grouped (a family holds more than one label)",
                         "field": family_field, "weaker": False, "families": None, "whole": whole,
                         "n_items": int(len(grouped)), "share": round(len(grouped) / len(items), 4)}
    if keys is not None:
        families: Dict[str, List[str]] = {}
        for label, key in zip(labels, keys):
            if key not in families.setdefault(label, []):
                families[label].append(key)
        if min(len(found) for found in families.values()) >= 3:
            rng = np.random.default_rng(seed)
            held: Dict[str, List[str]] = {}
            for label in sorted(families):
                found = sorted(families[label])
                take = min(len(found) - 2, max(1, round(share * len(found))))
                held[label] = sorted(found[i] for i in rng.permutation(len(found))[:take])
            test = np.array([j for j, (label, key) in enumerate(zip(labels, keys)) if key in held[label]])
            return test, {"kind": "scene families", "field": family_field, "weaker": False, "whole": whole,
                          "families": held, "n_items": int(len(test)), "share": round(len(test) / len(items), 4)}
    texts = [item.get("input_text") or item["probe_id"] for item in items]
    splitter = StratifiedGroupKFold(n_splits=max(2, round(1 / share)), shuffle=True, random_state=seed)
    _, test = next(splitter.split(np.zeros(len(items)), codes, groups=texts))
    test = np.sort(np.asarray(test))
    return test, {"kind": "stratified, identical texts kept together", "weaker": True, "families": None,
                  "n_items": int(len(test)), "share": round(len(test) / len(items), 4)}


def merge_folds(folds: List[Array], n_folds: int) -> Tuple[List[Array], Optional[int]]:
    """At most n_folds folds: family folds are merged round-robin (each still holds out whole
    families), so a set with many families doesn't multiply the search's cost."""
    if len(folds) <= n_folds:
        return folds, None
    return [np.sort(np.concatenate(folds[i::n_folds])) for i in range(n_folds)], len(folds)


def _score(found: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
    return {key: found[key] for key in ("ami", "kappa", "accuracy", "worst_fold")} if found else None


def _search_one(folder: str, layer: int, li: int, config: int, settings: Dict[str, Any], selection: Array,
                folds: List[Array], codes: Array, seed: int, ks: List[int]) -> Tuple[int, int, Dict[int, Any]]:
    """One layer and setting, in a worker process: held-out scores for every k on the selection folds."""
    from services.lenses.validate import heldout_scores

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")[selection]
    scores = heldout_scores(states, folds, {"target": codes}, settings["n_neighbors"], settings["dimensions"],
                            seed, settings["min_dist"], ks)
    return li, config, {k: _score(scores[k].get("target")) for k in scores}


def _test_one(folder: str, layer: int, li: int, test: Array, codes: Array, winner: Dict[str, Any], k: int,
              baseline: Dict[str, Any], baseline_k: int, seed: int) -> Tuple[int, Dict[str, Any]]:
    """One layer, in a worker process: the winner and the baseline fitted on the selection portion and
    scored on the test portion, with the raw groupings at the winner's k and the ceiling."""
    from services.lenses.validate import compare_layer, heldout_scores

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")
    target = {"target": codes}
    won = heldout_scores(states, [test], target, winner["n_neighbors"], winner["dimensions"], seed,
                         winner["min_dist"], [k]).get(k, {}).get("target")
    base = heldout_scores(states, [test], target, baseline["n_neighbors"], baseline["dimensions"], seed,
                          baseline["min_dist"], [baseline_k]).get(baseline_k, {}).get("target")
    comparison, _ = compare_layer(states, [test], codes, winner["n_neighbors"], seed, full_cuts=False)
    raw = {method: _score((comparison.get(method) or {}).get(str(k))) for method in ("raw_ward", "raw_spectral", "neurons")}
    return li, {"test": _score(won), "baseline": _score(base), "comparison": {"k": k, **raw, "ceiling": _score(comparison.get("ceiling"))}}


def choose(scores: Dict[int, Dict[int, Optional[Dict[str, float]]]], configs: List[UmapSettings],
           eligible: Sequence[int]) -> Tuple[Optional[Tuple[int, int]], List[Tuple[int, int]]]:
    """The (setting, k) with the highest held-out AMI, and up to three runners-up (each another
    setting at its own best k). Ties go to fewer nodes, then fewer dimensions, more neighbours and a
    larger min_dist: each a smoother, smaller map."""
    def key(config: int, k: int) -> Tuple[float, int, int, int, float]:
        s = configs[config]
        found = scores[config][k]
        return (round(found["ami"], 4) if found else -1.0, -k, -s.dimensions, s.n_neighbors, s.min_dist)

    best: List[Tuple[Tuple[float, int, int, int, float], int, int]] = []
    for config in eligible:
        ks = [k for k, found in scores.get(config, {}).items() if found]
        if ks:
            k = max(ks, key=lambda kk: key(config, kk))
            best.append((key(config, k), config, k))
    best.sort(reverse=True)
    if not best:
        return None, []
    return (best[0][1], best[0][2]), [(config, k) for _, config, k in best[1:4]]


class _Prefixed:
    """A job context whose progress stages carry a prefix, so one job can run another's stages."""

    def __init__(self, ctx: Any, prefix: str) -> None:
        self._ctx, self._prefix = ctx, prefix

    def progress(self, stage: str, done: int, total: int) -> None:
        self._ctx.progress(f"{self._prefix}: {stage}", done, total)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._ctx, name)


def _clean(value: Any) -> Any:
    """NaN and infinities as null: the browser's JSON parser rejects them."""
    if isinstance(value, float):
        return value if np.isfinite(value) else None
    if isinstance(value, dict):
        return {key: _clean(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(item) for item in value]
    if isinstance(value, np.generic):
        return _clean(value.item())
    return value


def _write_json(path: Path, record: Dict[str, Any]) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(_clean(record), allow_nan=False), encoding="utf-8")
    os.replace(tmp, path)


def run_search(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_search` job: see the module notes."""
    from joblib import Parallel, delayed

    from services.lenses.build import build_lens
    from services.lenses.data import load_states
    from services.lenses.flows import axes_of
    from services.lenses.store import git_state, lens_dir, read_manifest
    from services.lenses.validate import axis_codes, make_folds, self_check, validate_lens
    from services.lenses.view import open_lens

    started, stage_seconds = time.time(), {}
    p = LensSearchParams.model_validate(params)
    source = lens_dir(p.session_id, p.source_lens)
    manifest = read_manifest(source)
    if manifest.kind != "umap":
        raise ValueError(f"'{p.source_lens}' is a mass-mean lens; only UMAP lenses are tuned")
    name = tuned_name(p.source_lens, p.name)
    if lens_dir(manifest.session_id, name).exists():
        raise FileExistsError(f"lens {name!r} already exists in {manifest.session_id}")
    if p.k_min > p.k_max:
        raise ValueError(f"k_min {p.k_min} is above k_max {p.k_max}")
    configs = p.grid.settings()
    view = open_lens(manifest.session_id, p.source_lens)
    axes = axes_of(view)
    if p.target_axis not in axes or len(axes[p.target_axis]) < 2:
        raise ValueError(f"the lens has no axis {p.target_axis!r} with two values or more; it has {sorted(axes)}")
    codes = axis_codes(view.items, {p.target_axis: axes[p.target_axis]})[p.target_axis]
    seed = p.seed if p.seed is not None else manifest.settings.seed
    workers = p.workers or max(1, min(6, (os.cpu_count() or 2) - 2))

    ctx.progress("split", 0, 1)
    test, test_info = split_test(view.items, codes, p.family_field, p.test_share, seed, p.whole_families)
    selection = np.setdiff1d(np.arange(len(view.items)), test)
    folds, folding = make_folds([view.items[int(i)] for i in selection], p.family_field, p.n_folds, seed,
                                p.whole_families)
    folds, merged = merge_folds(folds, p.n_folds)
    folding = {key: value for key, value in folding.items() if key != "families"} | {"n_folds": len(folds)}
    if merged:
        folding["merged_from"] = merged
    n_train = int(len(selection) - max(len(fold) for fold in folds))
    ks = [k for k in range(p.k_min, p.k_max + 1) if k < n_train]

    ctx.progress("loading", 0, 1)
    work = source.parent / f".tmp-search-{ctx.job_id}"
    ctx.add_temp_path(work)
    work.mkdir()
    states = load_states(manifest.session_id, [item["probe_id"] for item in view.items],
                         manifest.site.source, manifest.site.token_position)
    layers = view.layers
    dim = int(states[layers[0]].shape[1])
    for layer in layers:
        np.save(work / f"X_L{layer:02d}.npy", states[layer])
    del states
    stage_seconds["load"] = round(time.time() - started, 1)

    t = time.time()
    ctx.progress("self-check", 0, len(configs))
    checks = Parallel(n_jobs=min(workers, len(configs)), backend="loky")(
        delayed(self_check)(len(view.items), dim, s.n_neighbors, s.dimensions, seed, s.min_dist) for s in configs)
    eligible = [i for i, check in enumerate(checks) if check["passed"]]
    if not eligible:
        raise ValueError("no setting in the grid passed the self-check: none finds the planted structure")
    stage_seconds["self_check"] = round(time.time() - t, 1)

    t = time.time()
    tasks = [(li, layer, c) for c in sorted(eligible, key=lambda c: -configs[c].n_neighbors * configs[c].dimensions)
             for li, layer in enumerate(layers)]
    scores: Dict[int, Dict[int, Dict[int, Any]]] = {li: {} for li in range(len(layers))}
    ctx.progress("searching", 0, len(tasks))
    for li, config, found in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(
            delayed(_search_one)(str(work), layer, li, c, configs[c].model_dump(), selection, folds,
                                 codes[selection], seed, ks) for li, layer, c in tasks):
        scores[li][config] = found
        ctx.progress("searching", sum(len(by) for by in scores.values()), len(tasks))
        ctx.check_cancelled()
    stage_seconds["search"] = round(time.time() - t, 1)

    winners: List[Dict[str, Any]] = []
    for li, layer in enumerate(layers):
        won, runners = choose(scores[li], configs, eligible)
        if won is None:
            raise ValueError(f"no setting scored at L{layer}")
        config, k = won
        winners.append({"layer": layer, "config": config, "settings": configs[config].model_dump(), "k": k,
                        "selection": scores[li][config][k],
                        "runners_up": [{"config": c, "settings": configs[c].model_dump(), "k": kk,
                                        "ami": scores[li][c][kk]["ami"]} for c, kk in runners]})

    t = time.time()
    baseline_k = [int(view.nodes[:, li].max()) + 1 for li in range(len(layers))]
    ctx.progress("testing", 0, len(layers))
    tested: Dict[int, Dict[str, Any]] = {}
    for li, result in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(
            delayed(_test_one)(str(work), layer, li, test, codes, winners[li]["settings"], winners[li]["k"],
                               manifest.settings.at(li).model_dump(), baseline_k[li], seed)
            for li, layer in enumerate(layers)):
        tested[li] = result
        ctx.progress("testing", len(tested), len(layers))
        ctx.check_cancelled()
    for li, winner in enumerate(winners):
        winner["test"] = tested[li]["test"]
    stage_seconds["test"] = round(time.time() - t, 1)
    shutil.rmtree(work)

    commit, dirty = git_state()
    record: Dict[str, Any] = {
        "format": 1, "kind": "lens_search",
        "source": {"name": p.source_lens, "version": view.version}, "tuned": name,
        "site": manifest.site.model_dump(), "filters": manifest.filters.model_dump(), "n_items": len(view.items),
        "target_axis": p.target_axis, "values": axes[p.target_axis], "seed": seed,
        "grid": p.grid.model_dump(), "ks": ks,
        "configs": [{"id": i, **s.model_dump(), "eligible": i in eligible,
                     "self_check": {"passed": checks[i]["passed"], "ari_k5": checks[i]["planted"]["ari_k5"],
                                    "ami_k5": checks[i]["null"]["ami_k5"]}} for i, s in enumerate(configs)],
        "split": {"test": test_info | {"probe_ids": [view.items[int(i)]["probe_id"] for i in test]},
                  "selection": {"n_items": int(len(selection)), "folds": folding}},
        "layers": layers,
        "selection": {measure: [[[((scores[li].get(c) or {}).get(k) or {}).get(measure) for k in ks]
                                 for c in range(len(configs))] for li in range(len(layers))]
                      for measure in ("ami", "kappa", "accuracy", "worst_fold")},
        "winners": winners,
        "baseline": {"name": p.source_lens, "version": view.version,
                     "layers": [{"settings": manifest.settings.at(li).model_dump(), "k": baseline_k[li],
                                 "test": tested[li]["baseline"]} for li in range(len(layers))]},
        "comparison": [tested[li]["comparison"] for li in range(len(layers))],
        "notes": ["the test portion never entered the selection; its scores are the honest ones",
                  "the tuned lens's own validation reuses items that chose its settings, so it is partly "
                  "selection-biased"],
        "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id, "stage_seconds": stage_seconds,
                       "seconds": round(time.time() - started, 1),
                       "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
    }
    _write_json(Path(ctx.job_dir) / "search.json", record)

    build_lens({"session_id": manifest.session_id, "name": name, "n_neighbors": manifest.settings.n_neighbors,
                "dimensions": manifest.settings.dimensions, "min_dist": manifest.settings.min_dist,
                "per_layer": [w["settings"] for w in winners], "k_per_layer": [w["k"] for w in winners],
                "k_source": f"tuned: held-out AMI on {p.target_axis}", "source": manifest.site.source,
                "token_position": manifest.site.token_position, "filters": manifest.filters.model_dump(),
                "seed": seed, "workers": p.workers}, _Prefixed(ctx, "build"))
    record["provenance"]["seconds"] = round(time.time() - started, 1)
    _write_json(lens_dir(manifest.session_id, name) / "search.json", record)
    validate_lens({"session_id": manifest.session_id, "name": name, "family_field": p.family_field,
                   "whole_families": p.whole_families,
                   "n_folds": p.n_folds, "workers": p.workers}, _Prefixed(ctx, "validate"))
    return {"session_id": manifest.session_id, "source": p.source_lens, "name": name,
            "test_items": int(len(test)), "seconds": round(time.time() - started, 1)}


def tuning_headline(folder: Path) -> Optional[Dict[str, Any]]:
    """A tuned lens's headline: its layer picked by selection AMI (never by test), with that layer's
    test scores and the test portion's size."""
    path = folder / "search.json"
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    winners = [w for w in record.get("winners", []) if w.get("selection")]
    if not winners:
        return None
    top = max(winners, key=lambda w: w["selection"]["ami"])
    return {"source": record["source"], "target_axis": record["target_axis"], "layer": top["layer"], "k": top["k"],
            "test": top.get("test"), "test_items": record["split"]["test"]["n_items"],
            "weaker": record["split"]["test"]["weaker"]}
