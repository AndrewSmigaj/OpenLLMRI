"""Tuning a lens: the `lens_search` job (DESIGN.md B5, C3, C4).

A search over UMAP's settings and k, layer by layer, starting from a built lens, which fixes the
items, the site, the filters and the seed, and is the baseline. Stages:

1. **split:** `draws` test portions the selection never sees (LENS-21), drawn by the seed. When
   every item names its family, about `test_share` of each label's families per draw (at least two
   left per label for selection), later draws taking the next families in the seeded order;
   otherwise a stratified share grouped by text, marked weaker. Draw 1 is the portion a single draw
   takes, which previews leave out too. Stages 3 to 5 run once per draw, each with at most
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
6. **build** the tuned lens from draw 1's winners (their settings per layer, their k as v1).
7. **validate** it as usual.

The other draws give the spread of the test scores: how much the tuning's honest score moves with
the test portion, which one small portion can't show. `lens_rescore` adds draws to a search made
before draws existed, building nothing (`rescore_search`).

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

from services.jobs.workers import default_workers
from services.lenses.store import Metric, UmapSettings
from services.lenses.validate import merge_folds

Array = np.ndarray[Any, Any]

MAX_SETTINGS = 60
SECONDS_PER_FIT = (0.005, 0.25)  # a fit, placement and cuts take about a·n + b seconds for n training items


class SearchGrid(BaseModel):
    """The settings searched: every combination of the lists. With no metrics named, the search keeps
    the source lens's own."""
    n_neighbors: List[int] = Field(default_factory=lambda: [5, 15, 50])
    dimensions: List[int] = Field(default_factory=lambda: [3, 6, 12])
    min_dist: List[float] = Field(default_factory=lambda: [0.1])
    metric: Optional[List[Metric]] = None

    def settings(self, default_metric: Metric = "euclidean") -> List[UmapSettings]:
        metrics = sorted(set(self.metric)) if self.metric else [default_metric]
        found = [UmapSettings(n_neighbors=n, dimensions=d, min_dist=m, metric=metric)
                 for n, d, m, metric in itertools.product(sorted(set(self.n_neighbors)), sorted(set(self.dimensions)),
                                                          sorted(set(self.min_dist)), metrics)]
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
    test_share: Optional[float] = Field(default=None, ge=0.1, le=0.5)  # the lens's hold-out design when not given
    family_field: Optional[str] = None  # the lens's hold-out design when not given
    whole_families: Optional[bool] = None  # family names as they are, not their first two tokens
    n_folds: int = Field(default=5, ge=2, le=10)
    seed: Optional[int] = None  # the source lens's seed when not given
    workers: Optional[int] = None
    draws: int = Field(default=5, ge=1, le=10)  # test portions; the tuned lens is built from the first


def tuned_name(source: str, name: Optional[str]) -> str:
    return name or f"{source}-tuned"


def estimate_seconds(n_items: int, n_layers: int, n_settings: int, n_folds: int, workers: int,
                     test_share: float = 0.2, draws: int = 1) -> float:
    """About how long the search stage takes: one fit per setting, layer, fold and draw."""
    train = n_items * (1 - test_share) * (1 - 1 / n_folds)
    a, b = SECONDS_PER_FIT
    return draws * n_settings * n_layers * n_folds * (a * train + b) / max(1, workers)


def split_tests(items: Sequence[Dict[str, Any]], codes: Array, family_field: Optional[str], share: float,
                seed: int, whole: bool = False, draws: int = 1) -> List[Tuple[Array, Dict[str, Any]]]:
    """The test portions of `draws` draws (DESIGN.md C4, LENS-21), each with how it was drawn. Draw
    1 is the portion a single split draws, the one previews keep out of their scores; the later
    draws hold out other families, or other items without families.

    Whole families per label when every item names one (and each label has at least three): each
    label's families in a seeded order, `take` of them per draw, wrapping round when a label runs out
    (`repeated` names the labels whose families come round again). Whole families in balanced groups
    when a family holds more than one label (as `make_folds` does), one group per draw. Otherwise a
    stratified share grouped by text, one fold per draw, marked weaker. Drawing more portions than
    a branch has folds gives that many, and no more."""
    from sklearn.model_selection import StratifiedGroupKFold

    from services.lenses.validate import (
        balanced_groups,
        class_balance,
        crossing_families,
        family_keys,
    )

    labels = [str(item.get("label")) for item in items]
    keys = family_keys(items, family_field, whole)
    crossing = crossing_families(labels, keys) if keys is not None else []
    out: List[Tuple[Array, Dict[str, Any]]] = []
    if keys is not None and crossing and len(set(keys)) >= 2:
        groups = balanced_groups(labels, keys, min(len(set(keys)), max(2, round(1 / share))), seed)
        for r, grouped in enumerate(groups[:draws]):
            out.append((grouped, {"kind": "whole scene families, grouped (a family holds more than one label)",
                                  "field": family_field, "weaker": False, "families": None, "whole": whole,
                                  "n_items": int(len(grouped)), "share": round(len(grouped) / len(items), 4),
                                  "balance": class_balance(labels, [grouped]), "draw": r + 1}))
        return out
    if keys is not None:
        families: Dict[str, List[str]] = {}
        for label, key in zip(labels, keys):
            if key not in families.setdefault(label, []):
                families[label].append(key)
        if min(len(found) for found in families.values()) >= 3:
            rng = np.random.default_rng(seed)
            order: Dict[str, Tuple[List[str], Array, int]] = {}
            for label in sorted(families):
                found = sorted(families[label])
                take = min(len(found) - 2, max(1, round(share * len(found))))
                order[label] = (found, rng.permutation(len(found)), take)
            for r in range(draws):
                held = {label: sorted(found[perm[(r * take + j) % len(found)]] for j in range(take))
                        for label, (found, perm, take) in order.items()}
                repeated = sorted(label for label, (found, _, take) in order.items() if (r + 1) * take > len(found))
                test = np.array([j for j, (label, key) in enumerate(zip(labels, keys)) if key in held[label]])
                out.append((test, {"kind": "scene families", "field": family_field, "weaker": False, "whole": whole,
                                   "families": held, "n_items": int(len(test)),
                                   "share": round(len(test) / len(items), 4), "draw": r + 1,
                                   "repeated": repeated}))
            return out
    texts = [item.get("input_text") or item["probe_id"] for item in items]
    splitter = StratifiedGroupKFold(n_splits=max(2, round(1 / share)), shuffle=True, random_state=seed)
    for r, (_, test) in enumerate(splitter.split(np.zeros(len(items)), codes, groups=texts)):
        if r >= draws:
            break
        test = np.sort(np.asarray(test))
        out.append((test, {"kind": "stratified, identical texts kept together", "weaker": True, "families": None,
                           "n_items": int(len(test)), "share": round(len(test) / len(items), 4), "draw": r + 1}))
    return out


def split_test(items: Sequence[Dict[str, Any]], codes: Array, family_field: Optional[str], share: float,
               seed: int, whole: bool = False) -> Tuple[Array, Dict[str, Any]]:
    """The first draw's test portion (`split_tests`): the one a tuned lens is built and scored on,
    and the one a layer preview keeps out of its label-based scores."""
    return split_tests(items, codes, family_field, share, seed, whole, draws=1)[0]


def _score(found: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
    return {key: found[key] for key in ("ami", "kappa", "accuracy", "worst_fold")} if found else None


def _search_one(folder: str, layer: int, li: int, config: int, settings: Dict[str, Any], selection: Array,
                folds: List[Array], codes: Array, seed: int, ks: List[int]) -> Tuple[int, int, Dict[int, Any]]:
    """One layer and setting, in a worker process: held-out scores for every k on the selection folds."""
    from services.lenses.validate import heldout_scores

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")[selection]
    scores = heldout_scores(states, folds, {"target": codes}, UmapSettings.of(settings), seed, ks)
    return li, config, {k: _score(scores[k].get("target")) for k in scores}


def _test_one(folder: str, layer: int, li: int, test: Array, codes: Array, winner: Dict[str, Any], k: int,
              baseline: Dict[str, Any], baseline_k: int, seed: int) -> Tuple[int, Dict[str, Any]]:
    """One layer, in a worker process: the winner and the baseline fitted on the selection portion and
    scored on the test portion, with the raw groupings at the winner's k and the ceiling."""
    from services.lenses.validate import compare_layer, heldout_scores

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")
    target = {"target": codes}
    won = heldout_scores(states, [test], target, UmapSettings.of(winner), seed, [k]).get(k, {}).get("target")
    base = heldout_scores(states, [test], target, UmapSettings.of(baseline), seed,
                          [baseline_k]).get(baseline_k, {}).get("target")
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


def _run_draw(work: Path, view: Any, codes: Array, configs: List[UmapSettings], eligible: List[int],
              test: Array, p: LensSearchParams, design: Any, seed: int, workers: int,
              baselines: List[Dict[str, Any]], baseline_k: List[int], ctx: Any, stage: str) -> Dict[str, Any]:
    """Stages 3 to 5 for one draw: selection folds over the items outside its test portion, the
    search, the choice and the test. `stage` prefixes the progress stages ("draw 2 of 5: ")."""
    from joblib import Parallel, delayed

    from services.lenses.validate import make_folds

    layers = view.layers
    seconds: Dict[str, float] = {}
    selection = np.setdiff1d(np.arange(len(view.items)), test)
    folds, folding = make_folds([view.items[int(i)] for i in selection], design.family_field, p.n_folds, seed,
                                design.whole_families)
    folds, merged = merge_folds(folds, p.n_folds)
    folding = {key: value for key, value in folding.items() if key != "families"} | {"n_folds": len(folds)}
    if merged:
        folding["merged_from"] = merged
    n_train = int(len(selection) - max(len(fold) for fold in folds))
    ks = [k for k in range(p.k_min, p.k_max + 1) if k < n_train]

    t = time.time()
    tasks = [(li, layer, c) for c in sorted(eligible, key=lambda c: -configs[c].n_neighbors * configs[c].dimensions)
             for li, layer in enumerate(layers)]
    scores: Dict[int, Dict[int, Dict[int, Any]]] = {li: {} for li in range(len(layers))}
    ctx.progress(f"{stage}searching", 0, len(tasks))
    for li, config, found in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(
            delayed(_search_one)(str(work), layer, li, c, configs[c].model_dump(), selection, folds,
                                 codes[selection], seed, ks) for li, layer, c in tasks):
        scores[li][config] = found
        ctx.progress(f"{stage}searching", sum(len(by) for by in scores.values()), len(tasks))
        ctx.check_cancelled()
    seconds["search"] = round(time.time() - t, 1)

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
    ctx.progress(f"{stage}testing", 0, len(layers))
    tested: Dict[int, Dict[str, Any]] = {}
    for li, result in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(
            delayed(_test_one)(str(work), layer, li, test, codes, winners[li]["settings"], winners[li]["k"],
                               baselines[li], baseline_k[li], seed)
            for li, layer in enumerate(layers)):
        tested[li] = result
        ctx.progress(f"{stage}testing", len(tested), len(layers))
        ctx.check_cancelled()
    for li, winner in enumerate(winners):
        winner["test"] = tested[li]["test"]
    seconds["test"] = round(time.time() - t, 1)
    return {"selection": selection, "folding": folding, "ks": ks, "scores": scores, "winners": winners,
            "tested": tested, "seconds": seconds}


SPREAD_MEASURES = ("ami", "kappa", "accuracy")


def _spread(values: List[Optional[Dict[str, Any]]]) -> Optional[Dict[str, Dict[str, float]]]:
    """Each score's mean, minimum and maximum over the draws that have it, and how many they are."""
    out: Dict[str, Dict[str, float]] = {}
    for measure in SPREAD_MEASURES:
        found = [float(v[measure]) for v in values if v and v.get(measure) is not None and np.isfinite(v[measure])]
        if found:
            out[measure] = {"mean": round(float(np.mean(found)), 4), "min": round(min(found), 4),
                            "max": round(max(found), 4), "n": len(found)}
    return out or None


def _search(p: LensSearchParams, manifest: Any, view: Any, design: Any, codes: Array, values: List[str],
            work: Path, ctx: Any, started: float) -> Dict[str, Any]:
    """Stages 1 to 5 (the module notes) for every draw: the search record. Its top-level keys describe
    draw 1, the one the tuned lens is built from; `draws` holds every draw and `spread` each layer's
    scores over them."""
    from joblib import Parallel, delayed

    from services.lenses.data import load_states
    from services.lenses.store import git_state
    from services.lenses.validate import self_check

    stage_seconds: Dict[str, Any] = {}
    configs = p.grid.settings(manifest.settings.metric)
    seed = p.seed if p.seed is not None else manifest.settings.seed
    workers = p.workers or default_workers()
    layers = view.layers

    ctx.progress("split", 0, 1)
    portions = split_tests(view.items, codes, design.family_field, design.test_share, seed,
                           design.whole_families, p.draws)

    ctx.progress("loading", 0, 1)
    ctx.add_temp_path(work)
    work.mkdir()
    states = load_states(manifest.session_id, [item["probe_id"] for item in view.items],
                         manifest.site.source, manifest.site.token_position)
    dim = int(states[layers[0]].shape[1])
    for layer in layers:
        np.save(work / f"X_L{layer:02d}.npy", states[layer])
    del states
    stage_seconds["load"] = round(time.time() - started, 1)

    t = time.time()
    ctx.progress("self-check", 0, len(configs))
    checks = Parallel(n_jobs=min(workers, len(configs)), backend="loky")(
        delayed(self_check)(len(view.items), dim, s, seed) for s in configs)
    eligible = [i for i, check in enumerate(checks) if check["passed"]]
    if not eligible:
        raise ValueError("no setting in the grid passed the self-check: none finds the planted structure")
    stage_seconds["self_check"] = round(time.time() - t, 1)

    baselines = [manifest.settings.at(li).model_dump() for li in range(len(layers))]
    baseline_k = [int(view.nodes[:, li].max()) + 1 for li in range(len(layers))]
    # previews chose a hand-set source lens's settings on items outside draw 1's portion, which the
    # other draws hold out: its scores there are optimistic
    biased_after_first = bool(manifest.settings.chosen_on_heldout())
    runs: List[Dict[str, Any]] = []
    for r, (test, _) in enumerate(portions):
        stage = f"draw {r + 1} of {len(portions)}: " if len(portions) > 1 else ""
        runs.append(_run_draw(work, view, codes, configs, eligible, test, p, design, seed, workers,
                              baselines, baseline_k, ctx, stage))
    shutil.rmtree(work)
    stage_seconds["search"] = round(sum(run["seconds"]["search"] for run in runs), 1)
    stage_seconds["test"] = round(sum(run["seconds"]["test"] for run in runs), 1)

    def ids(test: Array) -> List[str]:
        return [view.items[int(i)]["probe_id"] for i in test]

    first, (test, test_info) = runs[0], portions[0]
    draws = [{"draw": r + 1,
              "test": info | {"probe_ids": ids(portion)},
              "selection": {"n_items": int(len(run["selection"])), "folds": run["folding"]},
              "winners": [{key: w[key] for key in ("layer", "config", "settings", "k", "selection", "test")}
                          for w in run["winners"]],
              "baseline": [run["tested"][li]["baseline"] for li in range(len(layers))],
              "baseline_selection_biased": r > 0 and biased_after_first,
              "comparison": [run["tested"][li]["comparison"] for li in range(len(layers))]}
             for r, ((portion, info), run) in enumerate(zip(portions, runs))]
    spread = [{"layer": layer,
               "winner": _spread([run["tested"][li]["test"] for run in runs]),
               "baseline": _spread([run["tested"][li]["baseline"] for run in runs]),
               **{method: _spread([run["tested"][li]["comparison"].get(method) for run in runs])
                  for method in ("raw_ward", "raw_spectral", "neurons", "ceiling")}}
              for li, layer in enumerate(layers)]
    commit, dirty = git_state()
    return {
        "format": 2, "kind": "lens_search",
        "source": {"name": p.source_lens, "version": view.version}, "tuned": tuned_name(p.source_lens, p.name),
        "site": manifest.site.model_dump(), "filters": manifest.filters.model_dump(), "n_items": len(view.items),
        "target_axis": p.target_axis, "values": values, "seed": seed,
        "grid": p.grid.model_dump(), "ks": first["ks"],
        "configs": [{"id": i, **s.model_dump(), "eligible": i in eligible,
                     "self_check": {"passed": checks[i]["passed"], "ari_k5": checks[i]["planted"]["ari_k5"],
                                    "ami_k5": checks[i]["null"]["ami_k5"]}} for i, s in enumerate(configs)],
        "split": {"test": test_info | {"probe_ids": ids(test)},
                  "selection": {"n_items": int(len(first["selection"])), "folds": first["folding"]}},
        "holdout": design.model_dump(),
        "layers": layers,
        "selection": {measure: [[[((first["scores"][li].get(c) or {}).get(k) or {}).get(measure) for k in first["ks"]]
                                 for c in range(len(configs))] for li in range(len(layers))]
                      for measure in ("ami", "kappa", "accuracy", "worst_fold")},
        "winners": first["winners"],
        "baseline": {"name": p.source_lens, "version": view.version,
                     "layers": [{"settings": baselines[li], "k": baseline_k[li],
                                 "test": first["tested"][li]["baseline"]} for li in range(len(layers))]},
        "comparison": [first["tested"][li]["comparison"] for li in range(len(layers))],
        "draws_requested": p.draws, "draws": draws, "spread": spread,
        "notes": ["the test portion never entered the selection; its scores are the honest ones",
                  "the tuned lens is built from draw 1; the other draws repeat the search on other test "
                  "portions, so the spread is the tuning's, not this lens's own",
                  "the tuned lens's own validation reuses items that chose its settings, so it is partly "
                  "selection-biased"],
        "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id, "stage_seconds": stage_seconds,
                       "seconds": round(time.time() - started, 1),
                       "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
    }


def run_search(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_search` job: see the module notes."""
    from services.lenses.build import build_lens
    from services.lenses.flows import axes_of
    from services.lenses.store import lens_dir, read_manifest, resolve_holdout
    from services.lenses.validate import axis_codes, validate_lens
    from services.lenses.view import open_lens

    started = time.time()
    p = LensSearchParams.model_validate(params)
    source = lens_dir(p.session_id, p.source_lens)
    manifest = read_manifest(source)
    if manifest.kind != "umap":
        raise ValueError(f"'{p.source_lens}' is a mass-mean lens; only UMAP lenses are tuned")
    design = resolve_holdout(source, manifest, p.family_field, p.whole_families)
    if p.test_share is not None:
        design = design.model_copy(update={"test_share": p.test_share})
    name = tuned_name(p.source_lens, p.name)
    if lens_dir(manifest.session_id, name).exists():
        raise FileExistsError(f"lens {name!r} already exists in {manifest.session_id}")
    if p.k_min > p.k_max:
        raise ValueError(f"k_min {p.k_min} is above k_max {p.k_max}")
    view = open_lens(manifest.session_id, p.source_lens)
    axes = axes_of(view)
    if p.target_axis not in axes or len(axes[p.target_axis]) < 2:
        raise ValueError(f"the lens has no axis {p.target_axis!r} with two values or more; it has {sorted(axes)}")
    codes = axis_codes(view.items, {p.target_axis: axes[p.target_axis]})[p.target_axis]

    record = _search(p, manifest, view, design, codes, axes[p.target_axis],
                     source.parent / f".tmp-search-{ctx.job_id}", ctx, started)
    _write_json(Path(ctx.job_dir) / "search.json", record)
    winners = record["winners"]
    build_lens(UmapSettings.of(manifest.settings).model_dump() | {
        "session_id": manifest.session_id, "name": name,
        "per_layer": [w["settings"] for w in winners], "sources": ["tuned"] * len(winners),
        "k_per_layer": [w["k"] for w in winners], "k_source": f"tuned: held-out AMI on {p.target_axis}",
        "source": manifest.site.source, "token_position": manifest.site.token_position,
        "filters": manifest.filters.model_dump(), "seed": record["seed"], "holdout": design.model_dump(),
        "workers": p.workers}, _Prefixed(ctx, "build"))
    record["provenance"]["seconds"] = round(time.time() - started, 1)
    _write_json(lens_dir(manifest.session_id, name) / "search.json", record)
    validate_lens({"session_id": manifest.session_id, "name": name, "n_folds": p.n_folds, "workers": p.workers},
                  _Prefixed(ctx, "validate"))  # with the tuned lens's own hold-out design: the source's
    return {"session_id": manifest.session_id, "source": p.source_lens, "name": name,
            "test_items": record["split"]["test"]["n_items"], "draws": len(record["draws"]),
            "seconds": round(time.time() - started, 1)}


class RescoreParams(BaseModel):
    session_id: str
    name: str  # a tuned lens: one with a search.json
    draws: int = Field(default=5, ge=1, le=10)
    workers: Optional[int] = None


def rescore_search(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_rescore` job (DESIGN.md C4, LENS-21): a tuned lens's stored search run again with
    several draws, building nothing. It takes the stored grid, k range, test share, folds, seed and
    target, and the family design from the record's `holdout` (or, in searches made before hold-out
    records, from its test portion's `field` and `whole`). Draw 1 must reproduce the stored test
    portion and winners, else it refuses; the earlier record is kept as search.single.json."""
    from services.lenses.flows import axes_of
    from services.lenses.store import HoldoutDesign, lens_dir, read_manifest
    from services.lenses.validate import axis_codes
    from services.lenses.view import open_lens

    started = time.time()
    p = RescoreParams.model_validate(params)
    folder = lens_dir(p.session_id, p.name)
    path = folder / "search.json"
    if not path.exists():
        raise FileNotFoundError(f"lens {p.name!r} wasn't made by a tuning: it has no search.json")
    old: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    tested = old["split"]["test"]
    design = HoldoutDesign(**old["holdout"]) if old.get("holdout") else HoldoutDesign(
        family_field=tested.get("field"), whole_families=bool(tested.get("whole", False)))
    session = old.get("session_id") or p.session_id
    search = LensSearchParams(
        session_id=session, source_lens=old["source"]["name"], name=p.name, target_axis=old["target_axis"],
        grid=SearchGrid(**old["grid"]), k_min=min(old["ks"]), k_max=max(old["ks"]),
        test_share=design.test_share, family_field=design.family_field, whole_families=design.whole_families,
        n_folds=old["split"]["selection"]["folds"]["n_folds"], seed=old["seed"], workers=p.workers, draws=p.draws)
    source = lens_dir(session, search.source_lens)
    manifest = read_manifest(source)
    view = open_lens(manifest.session_id, search.source_lens, old["source"]["version"])
    values = axes_of(view).get(search.target_axis)
    if values != old["values"]:
        raise ValueError(f"the source lens's {search.target_axis!r} values changed since the search: "
                         f"{old['values']} then, {values} now")
    codes = axis_codes(view.items, {search.target_axis: values})[search.target_axis]
    record = _search(search, manifest, view, design, codes, values,
                     source.parent / f".tmp-rescore-{ctx.job_id}", ctx, started)

    if sorted(record["split"]["test"]["probe_ids"]) != sorted(tested["probe_ids"]):
        raise ValueError("draw 1 doesn't reproduce the stored test portion; tune the lens again instead")
    for new, before in zip(record["winners"], old["winners"]):
        same = UmapSettings.of(new["settings"]) == UmapSettings.of(before["settings"]) and new["k"] == before["k"]
        if not same:
            raise ValueError(f"draw 1 doesn't reproduce the stored winner at L{before['layer']} "
                             f"({before['settings']}, k {before['k']}); tune the lens again instead")
    record["tuned"] = old.get("tuned", p.name)
    record["rescored"] = {"job_id": ctx.job_id, "earlier": "search.single.json"}
    kept = folder / "search.single.json"
    if not kept.exists():
        _write_json(kept, old)
    _write_json(path, record)
    return {"session_id": manifest.session_id, "name": p.name, "draws": len(record["draws"]),
            "seconds": round(time.time() - started, 1)}


def tuning_headline(folder: Path) -> Optional[Dict[str, Any]]:
    """A tuned lens's headline: its layer picked by selection AMI (never by test), with that layer's
    test scores, the test portion's size, and, when the search drew several test portions, the
    spread of the winner's test scores over them."""
    path = folder / "search.json"
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    winners = [w for w in record.get("winners", []) if w.get("selection")]
    if not winners:
        return None
    top = max(winners, key=lambda w: w["selection"]["ami"])
    spread = next((row.get("winner") for row in record.get("spread") or [] if row.get("layer") == top["layer"]), None)
    return {"source": record["source"], "target_axis": record["target_axis"], "layer": top["layer"], "k": top["k"],
            "test": top.get("test"), "test_items": record["split"]["test"]["n_items"],
            "weaker": record["split"]["test"]["weaker"],
            "test_spread": spread, "draws": len(record.get("draws") or []) or 1}
