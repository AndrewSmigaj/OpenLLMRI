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


def _vote(test_emb: Array, train_emb: Array, train_cut: Array, k: int) -> Array:
    """Each held-out item's cluster: a vote of its nearest training items, weighted by 1/distance."""
    distance = np.linalg.norm(test_emb[:, None, :] - train_emb[None, :, :], axis=-1)
    near = np.argsort(distance, axis=1)[:, :VOTE_NEIGHBOURS]
    weight = 1.0 / (np.take_along_axis(distance, near, axis=1) + 1e-9)
    votes = np.zeros((len(test_emb), k))
    np.add.at(votes, (np.repeat(np.arange(len(test_emb)), near.shape[1]), train_cut[near].ravel()), weight.ravel())
    assigned: Array = votes.argmax(axis=1)
    return assigned


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


def validate_layer(states: Array, embedding: Array, folds: List[Array], codes: Dict[str, Array],
                   n_neighbors: int, dimensions: int, seed: int, seeds: int) -> Dict[str, Any]:
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
        tree = ward_tree(fit_reducer(states, n_neighbors, dimensions, seed + extra)[1])
        seed_cuts.append({k: cut(tree, k) for k in ks})
    joint = {f"{a}×{b}": np.where((codes[a] >= 0) & (codes[b] >= 0), codes[a] * 1000 + codes[b], -1)
             for a, b in itertools.combinations(codes, 2)}
    every = {**codes, **joint}

    held: Dict[int, Dict[str, Dict[str, List[Any]]]] = {
        k: {axis: {"truth": [], "pred": [], "acc": [], "ami": []} for axis in codes} for k in ks}
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        reducer, train_emb = fit_reducer(states[train], n_neighbors, dimensions, seed)
        test_emb = np.asarray(reducer.transform(states[test]), dtype=np.float32)
        train_tree = ward_tree(train_emb)
        for k in ks:
            train_cut = cut(train_tree, k)
            assigned = _vote(test_emb, train_emb, train_cut, k)
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

    profile: Dict[str, Any] = {}
    for k in ks:
        profile[str(k)] = {
            "silhouette": round(float(silhouette_score(embedding, cuts[k])), 4),
            "seed_ari": round(float(np.mean([ari(cuts[k], other[k]) for other in seed_cuts])), 4) if seed_cuts else None,
            "agreement": {name: round(float(ami(v[v >= 0], cuts[k][v >= 0])), 4) for name, v in every.items() if (v >= 0).any()},
            "heldout": {axis: _scores(np.concatenate(r["truth"]), np.concatenate(r["pred"]), r["acc"], r["ami"])
                        for axis, r in held[k].items() if r["truth"]},
        }
    return profile


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


def self_check(n: int, dim: int, n_neighbors: int, dimensions: int, seed: int) -> Dict[str, Any]:
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
    embedding = fit_reducer(planted, n_neighbors, dimensions, seed)[1]
    tree = ward_tree(embedding)
    found5 = float(ari(classes, cut(tree, 5)))
    found2 = float(ari(np.array([0, 0, 1, 1, 1])[classes], cut(tree, 2)))
    null_ami = float(ami(labels, cut(ward_tree(fit_reducer(null, n_neighbors, dimensions, seed)[1]), 5)))
    planted_ok, null_ok = found5 >= PLANTED_PASS, null_ami <= NULL_PASS
    return {"passed": bool(planted_ok and null_ok), "items": n, "dims": dim,
            "planted": {"ari_k5": round(found5, 4), "passed": bool(planted_ok),
                        "groups_ari_k2": round(found2, 4), "levels": suggest_k(embedding, tree)["levels"]},
            "null": {"ami_k5": round(null_ami, 4), "passed": bool(null_ok)},
            "thresholds": {"planted_ari": PLANTED_PASS, "null_ami": NULL_PASS}}


def _validate_one(folder: str, layer: int, embedding: Array, folds: List[Array], codes: Dict[str, Array],
                  n_neighbors: int, dimensions: int, seed: int, seeds: int) -> Tuple[int, Dict[str, Any]]:
    """One layer, in a worker process: its states come from the job's work folder."""
    from pathlib import Path

    states = np.load(Path(folder) / f"X_L{layer:02d}.npy")
    return layer, validate_layer(states, embedding, folds, codes, n_neighbors, dimensions, seed, seeds)


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
    tasks = (delayed(_validate_one)(str(work), layer, embeddings[li], folds, codes, s.n_neighbors,
                                    s.dimensions, s.seed, p.seeds) for li, layer in enumerate(view.layers))
    profiles: Dict[str, Any] = {}
    ctx.progress("validating", 0, len(view.layers))
    for layer, profile in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(tasks):
        profiles[str(layer)] = profile
        ctx.progress("validating", len(profiles), len(view.layers))
        ctx.check_cancelled()
    commit, dirty = git_state()
    record: Dict[str, Any] = {"format": 1, "folds": folding, "axes": axes, "seeds": p.seeds, "vote_neighbours": VOTE_NEIGHBOURS,
              "layers": {str(layer): profiles[str(layer)] for layer in view.layers},
              "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id,
                             "seconds": round(time.time() - started, 1),
                             "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    tmp = folder / ".validation.json.tmp"
    tmp.write_text(json.dumps(record), encoding="utf-8")
    os.replace(tmp, folder / "validation.json")
    shutil.rmtree(work)
    return {"session_id": manifest.session_id, "name": p.name, "folds": folding["n_folds"],
            "weaker": folding["weaker"], "seconds": record["provenance"]["seconds"]}
