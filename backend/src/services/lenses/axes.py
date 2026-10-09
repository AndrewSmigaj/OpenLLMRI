"""How many designed axes a capture carries at a lens's site, layer by layer, and which techniques
find them (DESIGN.md C8; lens slice 1b).

For every layer and designed attribute (an axis with two values or more), each technique is scored
on held-out items over the lens's folds, by Cohen's kappa between the values it gives held-out
items and their real values, pooled over the folds. Kappa is corrected for chance and, unlike AMI,
counts a technique that swaps two values as wrong: a probe that gets every held-out family
backwards scores below zero, not one. The techniques:
- **UMAP**: the lens's own validation (each held-out item takes its voted node's majority value),
  at the version's k and at the attribute's best k; validation scores the decoys too, with no
  extra fits;
- **raw groupings**: Ward and spectral on standardized PCA-50 (the validation's recipe), at the
  version's k;
- **a linear probe** on the residual stream (logistic regression): the ceiling;
- **partial directions**: each attribute's own axis with the other attributes held fixed, from a
  joint least-squares fit on effect-coded attributes (the mass-mean axis in a balanced design), so
  design confounds don't read as one shared direction; an attribute nested with another (animacy
  above a category) is fitted without it; held-out items take the nearest training mean along the
  attribute's axes;
- **a principal component**: the one of the first 20 that best separates the attribute on the
  training items; held-out items take the nearest training mean along it.

Chance comes from decoys: random values given per family, or per text when the items name no
family, in each attribute's proportions, five per attribute, scored the same way. An attribute is
recovered by a technique at a layer when its score passes the 95th percentile of that technique's
decoy scores for the attribute, pooled over layers. The probe's decoys are scored at every fourth
layer, which keeps a run to minutes; the pool is still 30 scores.

Beside them, per layer: effective dimensionality (the participation ratio of the standardized PCA
spectrum) and the components holding half and 90% of the variance; the cosines between the partial
axes beside the design's own correlations; and the number of independent directions among the
partial axes. The cosines and the independent directions are judged against a null that permutes
whole design rows, which keeps the design's correlations: random axes in this space are far from
orthogonal, and two attributes correlated by design get partial axes whose errors are
anti-correlated.

`<lens>/axes.json` holds it all but the UMAP rows, which GET merges from the validation.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

Array = np.ndarray[Any, Any]

DECOYS = 5
PROBE_DECOY_EVERY = 4  # the probe's decoys are scored at every fourth layer
PCS = 20  # components a principal-component match chooses among
NULL_PERMUTATIONS = 50  # design-row permutations for the null of the angles and the independent directions
LEVEL = 0.95
TECHNIQUES = ("raw_ward", "raw_spectral", "probe", "directions", "component")
FORMAT_VERSION = 1


def attributes(items: Sequence[Dict[str, Any]], axes: Dict[str, List[str]]) -> Dict[str, Array]:
    """Each designed attribute's value index per item (-1 where an item has none), for axes with two
    values or more."""
    from services.lenses.flows import value_of

    out: Dict[str, Array] = {}
    for axis, values in axes.items():
        if len(values) < 2:
            continue
        out[axis] = np.array([values.index(v) if (v := value_of(item, axis)) in values else -1 for item in items])
    return out


def groups_of(items: Sequence[Dict[str, Any]], family_field: Optional[str], whole: bool = False) -> Tuple[Array, str]:
    """What a decoy value is given to: each item's family when every item names one, else its text;
    and which of the two it was."""
    from services.lenses.validate import family_keys

    families = family_keys(items, family_field, whole)
    keys = families if families is not None else [str(item.get("input_text") or item["probe_id"]) for item in items]
    index = {key: i for i, key in enumerate(sorted(set(keys)))}
    return np.array([index[k] for k in keys]), "families" if families is not None else "texts"


def decoys(codes: Array, groups: Array, rng: np.random.Generator, count: int = DECOYS) -> List[Array]:
    """Random values per group in the attribute's proportions; items without a value keep -1."""
    known = codes >= 0
    values, counts = np.unique(codes[known], return_counts=True)
    share = counts / counts.sum()
    out = []
    for _ in range(count):
        per_group = rng.choice(values, size=int(groups.max()) + 1, p=share)
        out.append(np.where(known, per_group[groups], -1))
    return out


def _kappa(truth: List[Array], predicted: List[Array]) -> float:
    """Cohen's kappa over every held-out item, the folds pooled (0 when only one value is held out)."""
    from sklearn.metrics import cohen_kappa_score

    t, p = np.concatenate(truth), np.concatenate(predicted)
    return float(cohen_kappa_score(t, p)) if len(set(t.tolist())) > 1 else 0.0


def effect_design(codes: Dict[str, Array]) -> Tuple[Array, List[Tuple[str, int]]]:
    """Effect-coded design columns for the attributes (deviation coding: each value but the last
    against the grand mean), and which attribute and value each column stands for. Items without a
    value get zeros in that attribute's columns."""
    columns: List[Array] = []
    names: List[Tuple[str, int]] = []
    for axis, c in codes.items():
        values = int(c.max()) + 1
        for v in range(values - 1):
            columns.append(np.where(c < 0, 0.0, np.where(c == v, 1.0, np.where(c == values - 1, -1.0, 0.0))))
            names.append((axis, v))
    return np.stack(columns, axis=1), names


def nested_with(codes: Dict[str, Array]) -> Dict[str, List[str]]:
    """For each attribute, the others it nests with: one is a function of the other wherever both
    are known (animacy above a semantic category, say). Holding a category fixed leaves animacy
    nothing to vary, so the two are never fitted together."""
    def function_of(a: str, b: str) -> bool:
        known = (codes[a] >= 0) & (codes[b] >= 0)
        pairs = set(zip(codes[b][known].tolist(), codes[a][known].tolist()))
        return len(pairs) == len({x for x, _ in pairs})

    return {a: [b for b in codes if b != a and (function_of(a, b) or function_of(b, a))] for a in codes}


def partial_axes(states: Array, codes: Dict[str, Array]) -> Dict[str, Array]:
    """Each attribute's directions with the others held fixed: for a two-valued attribute, the
    difference of its values' means (one row); for more values, each value's mean against the
    grand mean (one row per value), from a joint least-squares fit. An attribute's fit leaves out
    the attributes it nests with (`nested_with`); without nesting, all share one fit. An attribute
    with one value among these items (a decoy, say, on one fold's training items) has no axis: a
    row of zeros."""
    live = {a: c for a, c in codes.items() if len(np.unique(c[c >= 0])) >= 2}
    nested = nested_with(live)
    centred = states - states.mean(axis=0)
    fits: Dict[Tuple[str, ...], Tuple[Array, List[Tuple[str, int]]]] = {}
    out: Dict[str, Array] = {}
    for axis in codes:
        if axis not in live:
            out[axis] = np.zeros((1, states.shape[1]))
            continue
        included = tuple(a for a in live if a == axis or a not in nested[axis])
        if included not in fits:
            design, names = effect_design({a: live[a] for a in included})
            coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(states)), design]), centred, rcond=None)
            fits[included] = (coef[1:], names)
        effects, names = fits[included]
        mine = effects[[i for i, (a, _) in enumerate(names) if a == axis]]
        full = np.vstack([mine, -mine.sum(axis=0, keepdims=True)])  # every value's effect
        out[axis] = (full[0] - full[1])[None, :] if len(full) == 2 else full
    return out


def _nearest_mean(train: Array, labels: Array, test: Array) -> Array:
    """Each held-out point's class: the nearest training class mean."""
    classes = np.unique(labels)
    means = np.stack([train[labels == c].mean(axis=0) for c in classes])
    distance = ((test[:, None, :] - means[None, :, :]) ** 2).sum(axis=-1)
    predicted: Array = classes[distance.argmin(axis=1)]
    return predicted


def _best_component(train: Array, labels: Array) -> int:
    """The component (column) whose values best separate the classes on the training items (F)."""
    from sklearn.feature_selection import f_classif

    f, _ = f_classif(train, labels)
    return int(np.nan_to_num(f, nan=-1.0).argmax())


def score_layer(states: Array, folds: List[Array], code_sets: Dict[str, Dict[str, Array]], k: int,
                n_neighbors: int, seed: int, probe_sets: Sequence[str]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """Held-out kappa per technique, code set ("real", "decoy1", ...) and attribute at one layer.
    `probe_sets` names the code sets the probe is scored on (it is the costly one)."""
    from services.lenses.raw import ceiling, pca_features, spectral_cuts, ward_cuts
    from services.lenses.validate import _majority, nearest, vote

    n = len(states)
    record: Dict[str, Dict[str, Dict[str, Tuple[List[Array], List[Array]]]]] = {
        technique: {name: {axis: ([], []) for axis in codes} for name, codes in code_sets.items()}
        for technique in TECHNIQUES}
    chosen: Dict[str, List[int]] = {axis: [] for axis in code_sets.get("real", {})}  # each fold's component
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        tr50, te50 = pca_features(states[train], states[test], seed)
        cuts = {"raw_ward": ward_cuts(tr50, [k])[k], "raw_spectral": spectral_cuts(tr50, [k], n_neighbors, seed)[k]}
        near, dist = nearest(te50, tr50)
        assigned = {method: vote(near, dist, cut, k)[0] for method, cut in cuts.items()}
        trpc, tepc = pca_features(states[train], states[test], seed, PCS)
        for name, codes in code_sets.items():
            known_train = {axis: c[train] >= 0 for axis, c in codes.items()}
            directions = partial_axes(states[train], {axis: c[train] for axis, c in codes.items()})
            for axis, c in codes.items():
                keep = c[test] >= 0
                if not keep.any() or len(set(c[train][known_train[axis]].tolist())) < 2:
                    continue
                truth = c[test][keep]
                for method, cut in cuts.items():
                    predicted = _majority(cut, c[train], k)[assigned[method]][keep]
                    record[method][name][axis][0].append(truth)
                    record[method][name][axis][1].append(predicted)
                kt = known_train[axis]
                basis = directions[axis] / np.maximum(np.linalg.norm(directions[axis], axis=1, keepdims=True), 1e-12)
                along = _nearest_mean(states[train][kt] @ basis.T, c[train][kt], states[test][keep] @ basis.T)
                record["directions"][name][axis][0].append(truth)
                record["directions"][name][axis][1].append(along)
                best = _best_component(trpc[kt], c[train][kt])
                if name == "real":
                    chosen[axis].append(best)
                comp = _nearest_mean(trpc[kt][:, [best]], c[train][kt], tepc[keep][:, [best]])
                record["component"][name][axis][0].append(truth)
                record["component"][name][axis][1].append(comp)
                if name in probe_sets:
                    predicted = ceiling(states[train][kt], c[train][kt], states[test][keep], seed)
                    record["probe"][name][axis][0].append(truth)
                    record["probe"][name][axis][1].append(predicted)
    scores: Dict[str, Any] = {technique: {name: {axis: round(_kappa(*pair), 4) for axis, pair in by_axis.items() if pair[0]}
                                          for name, by_axis in by_name.items() if any(pair[0] for pair in by_axis.values())}
                              for technique, by_name in record.items()}
    # the component each attribute most often matched, numbered from 1 (folds differ a little)
    scores["chosen_component"] = {axis: int(np.bincount(found).argmax()) + 1 for axis, found in chosen.items() if found}
    return scores


def spectrum(states: Array, top: int = 50) -> Dict[str, Any]:
    """The standardized PCA spectrum: the first `top` shares of variance, the participation ratio,
    and the components holding half and 90% of the variance."""
    centred = (states - states.mean(axis=0)) / np.maximum(states.std(axis=0), 1e-8)
    singular = np.linalg.svd(centred, compute_uv=False)
    eig = singular ** 2
    share = eig / eig.sum()
    cumulative = np.cumsum(share)
    return {"shares": [round(float(s), 5) for s in share[:top]],
            "participation_ratio": round(float(eig.sum() ** 2 / (eig ** 2).sum()), 3),
            "for_half": int(np.searchsorted(cumulative, 0.5) + 1), "for_90": int(np.searchsorted(cumulative, 0.9) + 1)}


def _direction_rows(directions: Dict[str, Array], values: Dict[str, List[str]]) -> Tuple[Array, List[str]]:
    rows, names = [], []
    for axis, matrix in directions.items():
        for i, row in enumerate(matrix):
            rows.append(row / max(float(np.linalg.norm(row)), 1e-12))
            names.append(axis if len(matrix) == 1 else f"{axis}={values[axis][i]}")
    return np.stack(rows), names


def effective_rank(unit_rows: Array) -> float:
    """How many independent directions a set of unit vectors spans: the participation ratio of the
    squared singular values."""
    singular = np.linalg.svd(unit_rows, compute_uv=False) ** 2
    return float(singular.sum() ** 2 / (singular ** 2).sum())


def geometry(states: Array, codes: Dict[str, Array], values: Dict[str, List[str]], rng: np.random.Generator) -> Dict[str, Any]:
    """The partial axes' cosines and independent directions on all the lens's items, each against
    permuted design rows (the design's own correlations kept): the cosines' 5th and 95th
    percentiles per pair, and the independent directions' 5th, 50th and 95th."""
    rows, names = _direction_rows(partial_axes(states, codes), values)
    known = np.all(np.stack([c >= 0 for c in codes.values()]), axis=0)
    null, null_cosines = [], []
    for _ in range(NULL_PERMUTATIONS):
        order = rng.permutation(np.flatnonzero(known))
        shuffled = {axis: c.copy() for axis, c in codes.items()}
        for axis in shuffled:
            shuffled[axis][np.flatnonzero(known)] = codes[axis][order]  # whole design rows move together
        permuted = _direction_rows(partial_axes(states, shuffled), values)[0]
        null.append(effective_rank(permuted))
        null_cosines.append(permuted @ permuted.T)
    band = np.quantile(np.stack(null_cosines), [0.05, 0.95], axis=0)
    return {"names": names, "cosines": np.round(rows @ rows.T, 3).tolist(),
            "null_cosines": {"low": np.round(band[0], 3).tolist(), "high": np.round(band[1], 3).tolist()},
            "independent": round(effective_rank(rows), 3),
            "null": [round(float(np.quantile(null, q)), 3) for q in (0.05, 0.5, 0.95)]}


def design_correlations(codes: Dict[str, Array], values: Dict[str, List[str]]) -> Dict[str, Any]:
    """The designed attributes' own correlations: each value's indicator against every other's, in
    the same rows as the cosines."""
    columns, names = [], []
    for axis, c in codes.items():
        vals = values[axis]
        if len(vals) == 2:
            columns.append((c == 0).astype(float) - (c == 1).astype(float))
            names.append(axis)
        else:
            for i, v in enumerate(vals):
                columns.append((c == i).astype(float))
                names.append(f"{axis}={v}")
    matrix = np.nan_to_num(np.corrcoef(np.stack(columns)))
    return {"names": names, "correlations": np.round(matrix, 3).tolist()}


def _axes_one(folder: str, layer: int, li: int, folds: List[Array], code_sets: Dict[str, Dict[str, Array]],
              k: int, n_neighbors: int, seed: int, with_probe_decoys: bool, values: Dict[str, List[str]]) -> Dict[str, Any]:
    """One layer, in a worker process."""
    from pathlib import Path

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")
    probe_sets = list(code_sets) if with_probe_decoys else ["real"]
    rng = np.random.default_rng(seed + li)
    return {"layer": layer, "scores": score_layer(states, folds, code_sets, k, n_neighbors, seed, probe_sets),
            "spectrum": spectrum(states), "geometry": geometry(states, code_sets["real"], values, rng)}


def run_axes(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_axes` job: the axes analysis of a UMAP lens's capture (see the module notes)."""
    import shutil

    from joblib import Parallel, delayed

    from services.lenses.data import load_states
    from services.lenses.flows import axes_of
    from services.lenses.store import (
        git_state,
        lens_dir,
        read_manifest,
        read_version,
        resolve_holdout,
    )
    from services.lenses.validate import make_folds
    from services.lenses.view import open_lens

    started = time.time()
    session, name = params["session_id"], params["name"]
    folder = lens_dir(session, name)
    manifest = read_manifest(folder)
    if manifest.kind != "umap":
        raise ValueError(f"'{name}' is a {manifest.kind} lens: the axes analysis reads a UMAP lens's capture")
    design = resolve_holdout(folder, manifest, params.get("family_field"), params.get("whole_families"))
    family_field, whole = design.family_field, design.whole_families
    view = open_lens(session, name)
    # the family field groups items for folds and decoys; held out whole, it is never an attribute
    values = {axis: v for axis, v in axes_of(view).items() if len(v) >= 2 and axis != family_field}
    real = attributes(view.items, values)
    if not real:
        raise ValueError("the items carry no designed attribute with two values or more")
    seed = manifest.settings.seed
    rng = np.random.default_rng(seed)
    groups, given_per = groups_of(view.items, family_field, whole)
    code_sets: Dict[str, Dict[str, Array]] = {"real": real}
    for d in range(DECOYS):
        code_sets[f"decoy{d + 1}"] = {axis: decoys(c, groups, rng, 1)[0] for axis, c in real.items()}
    folds, how = make_folds(view.items, family_field, int(params.get("n_folds", 5)), seed, whole, design.max_folds)
    k_per_layer = read_version(folder, str(view.version)).k_per_layer

    work = folder / f".tmp-axes-{ctx.job_id}"
    ctx.add_temp_path(work)
    work.mkdir(parents=True)
    ctx.progress("loading", 0, 1)
    states = load_states(session, [item["probe_id"] for item in view.items], manifest.site.source,
                         manifest.site.token_position)
    for layer in view.layers:
        np.save(work / f"X_L{layer:02d}.npy", states[layer])
    del states
    ctx.progress("scoring", 0, len(view.layers))
    workers = int(params.get("workers") or max(1, min(6, (os.cpu_count() or 2) - 2)))
    jobs = (delayed(_axes_one)(str(work), layer, li, folds, code_sets, k_per_layer[li],
                               manifest.settings.at(li).n_neighbors, seed, li % PROBE_DECOY_EVERY == 0, values)
            for li, layer in enumerate(view.layers))
    per_layer: Dict[int, Dict[str, Any]] = {}
    for found in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(jobs):
        per_layer[int(found["layer"])] = found
        ctx.progress("scoring", len(per_layer), len(view.layers))
        ctx.check_cancelled()
    shutil.rmtree(work)
    layers = [per_layer[layer] for layer in view.layers]
    commit, dirty = git_state()
    result = {
        "format_version": FORMAT_VERSION, "lens": name, "version": view.version, "layers": view.layers,
        "attributes": values, "folds": how, "holdout": design.model_dump(), "techniques": list(TECHNIQUES),
        "level": LEVEL,
        "decoys": {"count": DECOYS, "given_per": given_per},
        "probe_decoy_layers": [view.layers[li] for li in range(len(view.layers)) if li % PROBE_DECOY_EVERY == 0],
        "scores": {technique: [layer["scores"][technique] for layer in layers] for technique in TECHNIQUES},
        "chosen_component": [layer["scores"]["chosen_component"] for layer in layers],
        "thresholds": thresholds([layer["scores"] for layer in layers], list(real)),
        "spectrum": [layer["spectrum"] for layer in layers], "geometry": [layer["geometry"] for layer in layers],
        "design": design_correlations(real, values),
        "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id, "seconds": round(time.time() - started, 1)},
    }
    tmp = folder / ".axes.json.tmp"
    tmp.write_text(json.dumps(_clean(result), indent=1), encoding="utf-8")
    os.replace(tmp, folder / "axes.json")
    return {"session_id": session, "name": name, "seconds": result["provenance"]["seconds"]}


def thresholds(per_layer: List[Dict[str, Dict[str, Dict[str, float]]]], attrs: List[str]) -> Dict[str, Dict[str, Optional[float]]]:
    """Per technique and attribute: the 95th percentile of its decoy scores, pooled over layers."""
    out: Dict[str, Dict[str, Optional[float]]] = {}
    for technique in TECHNIQUES:
        out[technique] = {}
        for axis in attrs:
            pool = [scores[technique][name][axis] for scores in per_layer for name in scores[technique]
                    if name != "real" and axis in scores[technique][name]]
            out[technique][axis] = round(float(np.quantile(pool, LEVEL)), 4) if pool else None
    return out


def _clean(value: Any) -> Any:
    if isinstance(value, float):
        return None if not np.isfinite(value) else value
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_clean(v) for v in value]
    return value


def recovered(analysis: Dict[str, Any]) -> Dict[str, List[int]]:
    """Per technique: how many attributes pass their decoy threshold at each layer."""
    out: Dict[str, List[int]] = {}
    for technique, layers in analysis["scores"].items():
        limits = analysis["thresholds"].get(technique, {})
        out[technique] = [sum(1 for axis, score in (layer.get("real") or {}).items()
                              if limits.get(axis) is not None and score > limits[axis]) for layer in layers]
    return out


def umap_rows(validation: Optional[Dict[str, Any]], layers: List[int], k_per_layer: List[int],
              attrs: List[str]) -> Optional[Dict[str, Any]]:
    """The UMAP lens's held-out kappa per layer and attribute from its validation, at the version's k
    and at the attribute's best k, with decoy thresholds pooled over layers (the best-k pool takes
    each decoy's own best k, so choosing k is charged to both). None without a validation."""
    if not validation:
        return None
    at_k: List[Dict[str, float]] = []
    best_k: List[Dict[str, Dict[str, float]]] = []
    pool_at: Dict[str, List[float]] = {axis: [] for axis in attrs}
    pool_best: Dict[str, List[float]] = {axis: [] for axis in attrs}
    for layer, k in zip(layers, k_per_layer):
        profile = validation["layers"].get(str(layer), {})
        here = profile.get(str(k)) or {}
        at_k.append({axis: round(float(here["heldout"][axis]["kappa"]), 4) for axis in attrs
                     if axis in (here.get("heldout") or {})})
        best: Dict[str, Dict[str, float]] = {}
        for axis in attrs:
            found = {int(kk): e["heldout"][axis]["kappa"] for kk, e in profile.items() if axis in (e.get("heldout") or {})}
            if found:
                kk = max(found, key=lambda x: (found[x], -x))
                best[axis] = {"k": kk, "kappa": round(float(found[kk]), 4)}
            pool_at[axis] += list(((here.get("decoys") or {}).get(axis) or {}).get("kappa", []))
            decoy_best = [((e.get("decoys") or {}).get(axis) or {}).get("kappa", []) for e in profile.values()]
            decoy_best = [d for d in decoy_best if d]
            if decoy_best:
                pool_best[axis] += [max(values) for values in zip(*decoy_best)]
        best_k.append(best)

    def limit(pool: Dict[str, List[float]]) -> Dict[str, Optional[float]]:
        return {axis: round(float(np.quantile(values, LEVEL)), 4) if values else None for axis, values in pool.items()}

    return {"at_k": at_k, "best_k": best_k, "thresholds": {"at_k": limit(pool_at), "best_k": limit(pool_best)},
            "decoys": any(pool_at[axis] for axis in attrs)}


def serve_axes(folder: Any, view: Any) -> Dict[str, Any]:
    """axes.json with the UMAP lens's rows merged in, at the view's version, and the attributes each
    technique recovers per layer."""
    from services.lenses.store import read_version

    path = folder / "axes.json"
    if not path.exists():
        raise FileNotFoundError("the axes analysis hasn't run on this lens: POST to run it")
    analysis: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    validation_path = folder / "validation.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8")) if validation_path.exists() else None
    k_per_layer = read_version(folder, str(view.version)).k_per_layer
    attrs = list(analysis["attributes"])
    umap = umap_rows(validation, analysis["layers"], k_per_layer, attrs)
    analysis["umap"] = umap
    analysis["k_per_layer"] = k_per_layer
    counted = recovered(analysis)
    if umap and umap["decoys"]:
        for which in ("at_k", "best_k"):
            limits = umap["thresholds"][which]

            def kappa(row: Dict[str, Any], axis: str, which: str = which) -> Optional[float]:
                value = row.get(axis)
                found: Optional[float] = value if which == "at_k" else (value or {}).get("kappa")
                return found

            counted[f"umap_{which}"] = [
                sum(1 for axis in attrs if limits.get(axis) is not None and (v := kappa(row, axis)) is not None and v > limits[axis])
                for row in umap[which]]
    analysis["recovered"] = counted
    return analysis
