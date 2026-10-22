"""Held-out groupings for one capture: at every layer and fold, the UMAP lens (UMAP and Ward on the
training items), raw Ward (standardized PCA-50 and Ward) and raw spectral (the same components, a
nearest-neighbour graph, spectral clustering), each cut at every k from 2 to 10. Held-out items are
placed in each grouping's own space and assigned by the vote of their 15 nearest training items,
exactly as validation does (services/lenses/validate.py `heldout_scores`, `compare_layer`), with the
same library functions, settings, seed and folds.

What is stored is the groupings, not scores: per layer, `cuts[fold, method, k, item]` holds each
training item's cluster and each held-out item's assigned cluster, so `summary.py` can score any
attribute or combination of attributes without fitting again.

  .venv/bin/python docs/studies/umap_vs_raw/analysis/heldout.py <capture> [workers]
"""
from __future__ import annotations

import os

# One thread each, as the job workers pin them, so results don't depend on the number of workers
for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_var] = "1"

import sys  # noqa: E402
import time  # noqa: E402
from typing import Any, List  # noqa: E402

import numpy as np  # noqa: E402

from common import KS, METHODS, ROOT, cuts_dir, folds_of, open_capture, pair_codes, single_codes, units_of, write_json  # noqa: E402

# Workers start fresh interpreters: they find the backend through the environment
os.environ["PYTHONPATH"] = str(ROOT / "backend/src")


def layer_cuts(path: str, folds: List[np.ndarray], settings: Any, seed: int, n_neighbors: int) -> np.ndarray:
    """[fold, method, k, item]: training items' clusters and held-out items' assigned clusters."""
    from services.lenses.fit import cut, fit_reducer, ward_tree
    from services.lenses.raw import pca_features, spectral_cuts, ward_cuts
    from services.lenses.validate import nearest, vote

    states = np.load(path)
    n = len(states)
    out = np.full((len(folds), len(METHODS), len(KS), n), -1, dtype=np.int8)
    for f, test in enumerate(folds):
        train = np.setdiff1d(np.arange(n), test)
        reducer, train_emb = fit_reducer(states[train], settings, seed)
        test_emb = np.asarray(reducer.transform(states[test]), dtype=np.float32)
        tree = ward_tree(train_emb)
        spaces = {"umap": (train_emb, test_emb, {k: cut(tree, k) for k in KS})}
        tr50, te50 = pca_features(states[train], states[test], seed)
        spaces["raw_ward"] = (tr50, te50, ward_cuts(tr50, KS))
        spaces["raw_spectral"] = (tr50, te50, spectral_cuts(tr50, KS, n_neighbors, seed))
        for m, method in enumerate(METHODS):
            tr, te, cuts = spaces[method]
            near, dist = nearest(te, tr)
            for j, k in enumerate(KS):
                out[f, m, j, train] = cuts[k]
                out[f, m, j, test] = vote(near, dist, cuts[k], k)[0]
    return out


def main(name: str, workers: int) -> None:
    from joblib import Parallel, delayed

    from services.lenses.data import load_states

    started = time.time()
    view, manifest, spec = open_capture(name)
    codes, axes = single_codes(view, spec["family"])
    joint, about = pair_codes(codes)
    folds, folding = folds_of(view, manifest, spec)
    folding = {key: value for key, value in folding.items() if key != "families"}
    out = cuts_dir(name)
    work = out / "states"
    work.mkdir(exist_ok=True)
    ids = [item["probe_id"] for item in view.items]
    for layer in view.layers:
        target = work / f"X_L{layer:02d}.npy"
        if not target.exists():
            np.save(target, load_states(manifest.session_id, ids, manifest.site.source, manifest.site.token_position,
                                        layers=[layer])[layer])
    s = manifest.settings
    todo = [(li, layer) for li, layer in enumerate(view.layers) if not (out / f"cuts_L{layer:02d}.npy").exists()]
    print(f"{name}: {len(ids)} items, {len(folds)} folds, {len(todo)} layers to fit", flush=True)
    jobs = (delayed(lambda li, layer: (layer, layer_cuts(str(work / f"X_L{layer:02d}.npy"), folds, s.at(li),
                                                          s.seed, s.at(li).n_neighbors)))(li, layer)
            for li, layer in todo)
    for layer, cuts in Parallel(n_jobs=workers, backend="loky", return_as="generator_unordered")(jobs):
        np.save(out / f"cuts_L{layer:02d}.npy", cuts)
        print(f"  L{layer:02d} done ({time.time() - started:.0f} s)", flush=True)
    write_json(out / "design.json", {
        "capture": name, "session": spec["session"], "lens": spec["lens"], "items": ids,
        "layers": view.layers, "methods": list(METHODS), "ks": KS,
        "settings": [s.at(li).model_dump() for li in range(len(view.layers))], "seed": s.seed,
        "folding": folding, "folds": [fold.tolist() for fold in folds],
        "units": units_of(view, spec),
        "axes": axes, "codes": {axis: c.tolist() for axis, c in codes.items()},
        "pairs": about, "pair_codes": {pair: c.tolist() for pair, c in joint.items()},
        "seconds": round(time.time() - started, 1)})
    for path in work.glob("X_L*.npy"):
        path.unlink()
    work.rmdir()
    print(f"{name}: done in {time.time() - started:.0f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4)
