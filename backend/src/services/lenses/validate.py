"""Validating a lens: held-out scores, the k profile, and the self-check (DESIGN.md C3, C4).

**Folds.** When items name their scene family (a categories field, `scene` by default), fold i
holds out family i of every class: the paper's scheme, which tests the lens on settings it never
saw. Families are keyed by the first two tokens of their name, the paper's rule (it repaired a
leak between batches). Without families, stratified folds keep identical texts together, and the
result is marked weaker.

**Held-out scoring,** per layer and fold: UMAP and Ward are fitted on the training items, the
held-out items are transformed into that space and each is assigned by a distance-weighted vote
of its 15 nearest training items; a cluster predicts the majority value of its training items on
each axis. Reported per axis: Cohen's kappa and accuracy over all held-out items, the worst
fold's accuracy, and the adjusted mutual information between assigned clusters and true values.

**The k profile,** per layer, for every k from 2 to 10: the silhouette of the lens's own
embedding, agreement across three UMAP seeds (mean ARI), agreement with each designed axis and
each pair of axes (in-sample AMI), and the held-out scores above.

**The self-check** runs in every build: the build's settings must find structure planted in a
synthetic layer shaped like residuals (5 classes in 2 groups), and find none in a null layer.
"""

from __future__ import annotations

import itertools
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from pydantic import BaseModel, Field

Array = np.ndarray[Any, Any]

K_RANGE = range(2, 11)
VOTE_NEIGHBOURS = 15


class ValidateParams(BaseModel):
    session_id: str
    name: str
    family_field: str = "scene"  # the categories field naming each item's scene family
    n_folds: int = Field(5, ge=2, le=20)  # stratified folds, used when there are no families
    seeds: int = Field(3, ge=1, le=10)  # the lens's own seed and the ones after it
    workers: Optional[int] = None


def family_key(name: str) -> str:
    """A scene family from a scene name: its first two tokens (the paper's rule)."""
    return "_".join(str(name).split("_")[:2])


def make_folds(items: Sequence[Dict[str, Any]], family_field: str, n_folds: int,
               seed: int) -> Tuple[List[Array], Dict[str, Any]]:
    """Each fold's held-out item indices, and how the folds were made."""
    labels = [str(item.get("label")) for item in items]
    scenes = [item.get("categories", {}).get(family_field) for item in items]
    if all(scene is not None for scene in scenes):
        keys = [family_key(scene) for scene in scenes]
        families: Dict[str, List[str]] = {}
        for label, key in zip(labels, keys):
            if key not in families.setdefault(label, []):
                families[label].append(key)
        for label in families:
            families[label].sort()
        count = max(len(found) for found in families.values())
        folds = []
        for i in range(count):
            held = {(label, found[i]) for label, found in families.items() if i < len(found)}
            folds.append(np.array([j for j, pair in enumerate(zip(labels, keys)) if pair in held]))
        return folds, {"kind": "scene families", "field": family_field, "n_folds": count,
                       "weaker": False, "families": families}
    from sklearn.model_selection import StratifiedGroupKFold

    texts = [item.get("input_text") or item["probe_id"] for item in items]
    splitter = StratifiedGroupKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    folds = [np.asarray(test) for _, test in splitter.split(np.zeros(len(items)), labels, groups=texts)]
    return folds, {"kind": "stratified, identical texts kept together", "n_folds": n_folds, "weaker": True}


def axis_codes(items: Sequence[Dict[str, Any]], axes: Dict[str, List[str]]) -> Dict[str, Array]:
    """Each designed axis as integer codes per item (-1 where an item has no value)."""
    from services.lenses.flows import value_of

    return {axis: np.array([values.index(v) if (v := value_of(item, axis)) in values else -1 for item in items])
            for axis, values in axes.items()}


def nearest(points: Array, reference: Array, n: int = VOTE_NEIGHBOURS) -> Tuple[Array, Array]:
    """Each point's `n` nearest reference points, nearest first: their indices and distances."""
    distance = np.linalg.norm(points[:, None, :] - reference[None, :, :], axis=-1)
    near = np.argsort(distance, axis=1)[:, :n]
    return near, np.take_along_axis(distance, near, axis=1)


def vote(near: Array, dist: Array, cut: Array, k: int) -> Tuple[Array, Array]:
    """Each point's cluster by a vote of its nearest reference points (`nearest`), weighted by
    1/distance, and the winning cluster's share of the vote. Held-out items in validation and
    items read through a lens are assigned the same way."""
    weight = 1.0 / (dist + 1e-9)
    votes = np.zeros((len(near), k))
    np.add.at(votes, (np.repeat(np.arange(len(near)), near.shape[1]), cut[near].ravel()), weight.ravel())
    assigned: Array = votes.argmax(axis=1)
    share: Array = votes.max(axis=1) / votes.sum(axis=1)
    return assigned, share


def _majority(cut: Array, codes: Array, k: int) -> Array:
    """Each cluster's most common value on an axis among its (training) items; -1 if it has none."""
    out = np.full(k, -1)
    for c in range(k):
        values = codes[(cut == c) & (codes >= 0)]
        if values.size:
            out[c] = np.bincount(values).argmax()
    return out


def _scores(truth: Array, predicted: Array, fold_acc: List[float], fold_ami: List[Tuple[float, int]]) -> Dict[str, float]:
    """Kappa and accuracy over every held-out item; the worst fold; AMI per fold, averaged by size
    (cluster numbers from different folds don't compare, axis values do)."""
    from sklearn.metrics import cohen_kappa_score

    kappa = cohen_kappa_score(truth, predicted) if len(set(truth.tolist())) > 1 else 0.0
    sizes = sum(size for _, size in fold_ami)
    return {"kappa": round(float(kappa), 4), "accuracy": round(float((truth == predicted).mean()), 4),
            "worst_fold": round(float(min(fold_acc)), 4) if fold_acc else 0.0,
            "ami": round(float(sum(a * size for a, size in fold_ami) / sizes), 4) if sizes else 0.0}


def heldout_scores(states: Array, folds: List[Array], codes: Dict[str, Array], n_neighbors: int,
                   dimensions: int, seed: int, min_dist: float = 0.1,
                   ks: Optional[Sequence[int]] = None) -> Dict[int, Dict[str, Dict[str, float]]]:
    """Held-out scores per k and axis (see the module notes): for each fold, UMAP and Ward fitted on
    the training items, the held-out items placed and assigned by the vote. Validation and lens
    search score the same way. Every k is a cut of one tree per fold."""
    from sklearn.metrics import adjusted_mutual_info_score as ami

    from services.lenses.fit import cut, fit_reducer, ward_tree

    n = len(states)
    ks = [k for k in (ks if ks is not None else K_RANGE) if k < n]
    held: Dict[int, Dict[str, Dict[str, List[Any]]]] = {
        k: {axis: {"truth": [], "pred": [], "acc": [], "ami": []} for axis in codes} for k in ks}
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        reducer, train_emb = fit_reducer(states[train], n_neighbors, dimensions, seed, min_dist)
        test_emb = np.asarray(reducer.transform(states[test]), dtype=np.float32)
        train_tree = ward_tree(train_emb)
        near, dist = nearest(test_emb, train_emb)
        for k in ks:
            train_cut = cut(train_tree, k)
            assigned = vote(near, dist, train_cut, k)[0]
            for axis, c in codes.items():
                keep = c[test] >= 0
                if not keep.any():
                    continue
                truth, predicted = c[test][keep], _majority(train_cut, c[train], k)[assigned][keep]
                record = held[k][axis]
                record["truth"].append(truth)
                record["pred"].append(predicted)
                record["acc"].append(float((truth == predicted).mean()))
                record["ami"].append((float(ami(truth, assigned[keep])), int(keep.sum())))
    return {k: {axis: _scores(np.concatenate(r["truth"]), np.concatenate(r["pred"]), r["acc"], r["ami"])
                for axis, r in held[k].items() if r["truth"]} for k in ks}


def validate_layer(states: Array, embedding: Array, folds: List[Array], codes: Dict[str, Array],
                   n_neighbors: int, dimensions: int, seed: int, seeds: int,
                   min_dist: float = 0.1) -> Dict[str, Any]:
    """One layer's k profile: in-sample measures on the lens's own embedding, agreement across
    seeds, and held-out scores, for every k."""
    from sklearn.metrics import adjusted_mutual_info_score as ami
    from sklearn.metrics import adjusted_rand_score as ari
    from sklearn.metrics import silhouette_score

    from services.lenses.fit import cut, fit_reducer, ward_tree

    n = len(states)
    ks = [k for k in K_RANGE if k < n]
    cuts = {k: cut(ward_tree(embedding), k) for k in ks}
    seed_cuts = []
    for extra in range(1, seeds):
        tree = ward_tree(fit_reducer(states, n_neighbors, dimensions, seed + extra, min_dist)[1])
        seed_cuts.append({k: cut(tree, k) for k in ks})
    joint = {f"{a}×{b}": np.where((codes[a] >= 0) & (codes[b] >= 0), codes[a] * 1000 + codes[b], -1)
             for a, b in itertools.combinations(codes, 2)}
    every = {**codes, **joint}
    held = heldout_scores(states, folds, codes, n_neighbors, dimensions, seed, min_dist, ks)

    profile: Dict[str, Any] = {}
    for k in ks:
        profile[str(k)] = {
            "silhouette": round(float(silhouette_score(embedding, cuts[k])), 4),
            "seed_ari": round(float(np.mean([ari(cuts[k], other[k]) for other in seed_cuts])), 4) if seed_cuts else None,
            "agreement": {name: round(float(ami(v[v >= 0], cuts[k][v >= 0])), 4) for name, v in every.items() if (v >= 0).any()},
            "heldout": held[k],
        }
    return profile


RAW_METHODS = ("raw_ward", "raw_spectral", "neurons")


def compare_layer(states: Array, folds: List[Array], labels: Array, n_neighbors: int,
                  seed: int, full_cuts: bool = True) -> Tuple[Dict[str, Any], Dict[str, Dict[int, Array]]]:
    """The fair comparison at one layer, on the label: raw groupings scored on the same folds and
    at every k as the UMAP lens (held-out items assigned by the same vote), the supervised
    ceiling, and every item's raw cluster at every k on all the data (for disagreement marks;
    skipped with `full_cuts=False`)."""
    from sklearn.metrics import adjusted_mutual_info_score as ami

    from services.lenses.raw import ceiling, neuron_features, pca_features, spectral_cuts, ward_cuts

    n = len(states)
    ks = [k for k in K_RANGE if k < n]
    records: Dict[str, Dict[int, Dict[str, List[Any]]]] = {
        m: {k: {"truth": [], "pred": [], "acc": [], "ami": []} for k in ks} for m in RAW_METHODS}
    top: Dict[str, List[Any]] = {"truth": [], "pred": [], "acc": [], "ami": []}
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        y_train, y_test = labels[train], labels[test]
        keep = y_test >= 0
        if not keep.any() or len(set(y_train[y_train >= 0].tolist())) < 2:
            continue
        tr50, te50 = pca_features(states[train], states[test], seed)
        trn, ten = neuron_features(states[train], states[test], y_train, seed)
        groupings = {"raw_ward": (tr50, te50, ward_cuts(tr50, ks)),
                     "raw_spectral": (tr50, te50, spectral_cuts(tr50, ks, n_neighbors, seed)),
                     "neurons": (trn, ten, ward_cuts(trn, ks))}
        for method, (tr, te, cuts) in groupings.items():
            near, dist = nearest(te, tr)
            for k in ks:
                assigned = vote(near, dist, cuts[k], k)[0]
                truth, predicted = y_test[keep], _majority(cuts[k], y_train, k)[assigned][keep]
                record = records[method][k]
                record["truth"].append(truth)
                record["pred"].append(predicted)
                record["acc"].append(float((truth == predicted).mean()))
                record["ami"].append((float(ami(truth, assigned[keep])), int(keep.sum())))
        known = y_train >= 0
        predicted = ceiling(states[train][known], y_train[known], states[test], seed)[keep]
        top["truth"].append(y_test[keep])
        top["pred"].append(predicted)
        top["acc"].append(float((y_test[keep] == predicted).mean()))
        top["ami"].append((float(ami(y_test[keep], predicted)), int(keep.sum())))

    def score(r: Dict[str, List[Any]]) -> Optional[Dict[str, float]]:
        return _scores(np.concatenate(r["truth"]), np.concatenate(r["pred"]), r["acc"], r["ami"]) if r["truth"] else None

    comparison: Dict[str, Any] = {m: {str(k): score(records[m][k]) for k in ks} for m in RAW_METHODS}
    comparison["ceiling"] = score(top)
    if not full_cuts:
        return comparison, {}
    everything, _ = pca_features(states, states, seed)
    full = {"raw_ward": ward_cuts(everything, ks), "raw_spectral": spectral_cuts(everything, ks, n_neighbors, seed)}
    return comparison, full


PLANTED_PASS = 0.9  # ARI of the planted layer's 5-cut with its classes
NULL_PASS = 0.1  # AMI of the null layer's 5-cut with labels that carry no signal (it wanders to ~0.08 at 100 items)
LATENT = 8  # the planted structure lives in a small space, so its clarity doesn't depend on the layer's width


def planted_layers(n: int, dim: int, seed: int) -> Tuple[Array, Array, Array, Array]:
    """A planted layer (5 classes in 2 groups) and a null layer, both shaped like residuals: the
    structure lives in an 8-dimensional space mapped into the layer's width, under a large shared
    component and uneven dimension scales, with a little noise in every dimension.
    Returns (planted, classes, null, null labels)."""
    rng = np.random.default_rng(seed)
    mean = rng.normal(size=dim) * 8
    scale = np.exp(rng.normal(size=dim) * 0.5)
    mapping = rng.normal(size=(LATENT, dim)) / np.sqrt(LATENT)
    classes = np.arange(n) % 5
    groups = np.array([0, 0, 1, 1, 1])[classes]
    latent = (rng.normal(size=(2, LATENT))[groups] * 4.0 + rng.normal(size=(5, LATENT))[classes] * 1.2
              + rng.normal(size=(n, LATENT)) * 0.35)
    planted = mean + (latent @ mapping) * scale + rng.normal(size=(n, dim)) * 0.05 * scale
    null = mean + ((rng.normal(size=(n, LATENT)) * 0.35) @ mapping) * scale + rng.normal(size=(n, dim)) * 0.05 * scale
    return planted.astype(np.float32), classes, null.astype(np.float32), rng.integers(0, 5, size=n)


def self_check(n: int, dim: int, n_neighbors: int, dimensions: int, seed: int,
               min_dist: float = 0.1) -> Dict[str, Any]:
    """The build's own settings must find the planted classes, and nothing in a null layer.

    It runs at the lens's own item count, so settings too coarse for classes of that size (more
    neighbours than a class has items) fail it. The planted classes sit in two groups; whether the
    2-cut also finds the groups is reported, not required: UMAP keeps local structure, and the
    groups' distances can be lost (both levels show only when class and group separations are
    comparable)."""
    from sklearn.metrics import adjusted_mutual_info_score as ami
    from sklearn.metrics import adjusted_rand_score as ari

    from services.lenses.fit import cut, fit_reducer, suggest_k, ward_tree

    planted, classes, null, labels = planted_layers(n, dim, seed)
    embedding = fit_reducer(planted, n_neighbors, dimensions, seed, min_dist)[1]
    tree = ward_tree(embedding)
    found5 = float(ari(classes, cut(tree, 5)))
    found2 = float(ari(np.array([0, 0, 1, 1, 1])[classes], cut(tree, 2)))
    null_ami = float(ami(labels, cut(ward_tree(fit_reducer(null, n_neighbors, dimensions, seed, min_dist)[1]), 5)))
    planted_ok, null_ok = found5 >= PLANTED_PASS, null_ami <= NULL_PASS
    return {"passed": bool(planted_ok and null_ok), "items": n, "dims": dim,
            "planted": {"ari_k5": round(found5, 4), "passed": bool(planted_ok),
                        "groups_ari_k2": round(found2, 4), "levels": suggest_k(embedding, tree)["levels"]},
            "null": {"ami_k5": round(null_ami, 4), "passed": bool(null_ok)},
            "thresholds": {"planted_ari": PLANTED_PASS, "null_ami": NULL_PASS}}


def _validate_one(folder: str, layer: int, embedding: Array, folds: List[Array], codes: Dict[str, Array],
                  n_neighbors: int, dimensions: int, seed: int, seeds: int,
                  min_dist: float = 0.1) -> Tuple[int, Dict[str, Any], Dict[str, Any], Dict[str, Dict[int, Array]]]:
    """One layer, in a worker process: its states come from the job's work folder."""
    from pathlib import Path

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")
    profile = validate_layer(states, embedding[:, :dimensions], folds, codes, n_neighbors, dimensions, seed,
                             seeds, min_dist)
    comparison, full = compare_layer(states, folds, codes["label"], n_neighbors, seed) \
        if "label" in codes and (codes["label"] >= 0).any() else ({}, {})
    return layer, profile, comparison, full


def _write_raw_cuts(folder: Any, layers: List[int], full: Dict[int, Dict[str, Dict[int, Array]]]) -> None:
    """Every item's raw cluster at every layer and k, on all the data: `raw_cuts.npz` holds, per
    method, an array [layers, k from 2, items] (for the disagreement marks)."""
    first = next((cuts for cuts in full.values() if cuts), None)
    if first is None:
        return
    ks = sorted(next(iter(first.values())))
    arrays = {method: np.stack([np.stack([full[layer][method][k] for k in ks]) for layer in layers]).astype(np.int16)
              for method in first}
    tmp = folder / ".raw_cuts.tmp.npz"
    np.savez_compressed(tmp, ks=np.array(ks), **arrays)
    tmp.replace(folder / "raw_cuts.npz")


def validate_lens(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_validate` job: every layer's k profile and held-out scores, written to the lens's
    `validation.json` (it doesn't depend on the version: every k from 2 to 10 is scored)."""
    import json
    import os
    import shutil
    import time

    from joblib import Parallel, delayed

    from services.lenses.data import load_states
    from services.lenses.flows import axes_of
    from services.lenses.store import git_state, lens_dir, read_manifest
    from services.lenses.view import open_lens

    started = time.time()
    p = ValidateParams.model_validate(params)
    folder = lens_dir(p.session_id, p.name)
    manifest = read_manifest(folder)
    view = open_lens(p.session_id, p.name)
    axes = axes_of(view)
    codes = axis_codes(view.items, axes)
    folds, folding = make_folds(view.items, p.family_field, p.n_folds, manifest.settings.seed)
    ctx.progress("loading", 0, 1)
    work = folder / f".tmp-validate-{ctx.job_id}"
    ctx.add_temp_path(work)
    work.mkdir()
    states = load_states(manifest.session_id, [item["probe_id"] for item in view.items],
                         manifest.site.source, manifest.site.token_position)
    for layer in view.layers:
        np.save(work / f"X_L{layer:02d}.npy", states[layer])
    del states
    embeddings = np.load(folder / "fit" / "embed.npz")["embedding"]
    s = manifest.settings
    workers = p.workers or max(1, min(6, (os.cpu_count() or 2) - 2))
    tasks = (delayed(_validate_one)(str(work), layer, embeddings[li], folds, codes, s.at(li).n_neighbors,
                                    s.at(li).dimensions, s.seed, p.seeds, s.at(li).min_dist)
             for li, layer in enumerate(view.layers))
    profiles: Dict[str, Any] = {}
    comparisons: Dict[str, Any] = {}
    full: Dict[int, Dict[str, Dict[int, Array]]] = {}
    ctx.progress("validating", 0, len(view.layers))
    for layer, profile, comparison, cuts in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(tasks):
        profiles[str(layer)], comparisons[str(layer)], full[layer] = profile, comparison, cuts
        ctx.progress("validating", len(profiles), len(view.layers))
        ctx.check_cancelled()
    _write_raw_cuts(folder, view.layers, full)
    commit, dirty = git_state()
    record: Dict[str, Any] = {"format": 1, "folds": folding, "axes": axes, "seeds": p.seeds, "vote_neighbours": VOTE_NEIGHBOURS,
              "layers": {str(layer): profiles[str(layer)] for layer in view.layers},
              "comparison": {str(layer): comparisons[str(layer)] for layer in view.layers},
              "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id,
                             "seconds": round(time.time() - started, 1),
                             "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    tmp = folder / ".validation.json.tmp"
    tmp.write_text(json.dumps(record), encoding="utf-8")
    os.replace(tmp, folder / "validation.json")
    shutil.rmtree(work)
    return {"session_id": manifest.session_id, "name": p.name, "folds": folding["n_folds"],
            "weaker": folding["weaker"], "seconds": record["provenance"]["seconds"]}
