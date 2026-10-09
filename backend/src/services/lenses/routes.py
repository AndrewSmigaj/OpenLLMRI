"""Expert pipelines, hubs and the experts involved in a lens (DESIGN.md C7 and E8; lens slice 1b).

Built from all four of each item's experts at every layer, weighted by the model's own weights
(the top four of the router's softmax, scaled to sum to 1).

- **Pipelines** are found by following the bundle. Every (layer, expert) that at least 5% of the
  items (10 at least) have among their four is a seed. A chain grows one layer at a time toward
  the expert its members weight most there, keeps the members that have that expert among their
  four, and stops when too few are left; chains of three layers or more are kept. An item's credit
  is the geometric mean of its weights along the chain: a plain product shrinks by about a third a
  layer and would hide every long chain. Near-duplicates, which nowhere differ for three layers
  running, keep only the one with the larger credit times length. A pipeline replicates when
  following the bundle from its seed in each half of the folds finds it again, by the same rule.
- A **hub** is an expert whose items arrive from different sources, measured between items: the
  Jensen-Shannon part of the mixture of their sources at the layer before, so each item's own
  four-way split cancels, given as an effective number of sources. Identical routing gives one;
  two groups arriving from different experts give two.
- The **experts involved** in a designed value are those whose mean weight differs between the
  value's items and the rest beyond chance: beyond the 95th percentile of the largest difference
  over 200 permutations of the labels. Whole families move together when each family holds one
  value; otherwise items with the same text do. Each comes with the side it favours and how well
  its weight tells the value apart (AUC).

Written to `<lens>/routes.json`, the same for every version of the lens; the nodes a pipeline's
items sit in are added when it is served, at the version asked for.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from services.lenses.view import Array, LensView

MIN_SHARE = 0.05  # a seed or a chain needs this share of the items (MIN_ITEMS at least)
MIN_ITEMS = 10
MIN_LENGTH = 3  # layers
MAX_PIPELINES = 20
HUB_SOURCES = 2.0  # effective sources, between items
MAX_HUBS = 15
PERMUTATIONS = 200
MAX_INVOLVED = 10  # per value
FORMAT_VERSION = 1


def dense(view: LensView) -> Array:
    """[N, L, E]: each item's weight on every expert at every layer (0 outside its four)."""
    from services.lenses.experts import _n_experts

    n, layers, _ = view.experts.shape
    grid = np.zeros((n, layers, _n_experts(view)), dtype=np.float64)
    rows = np.repeat(np.arange(n), layers * 4)
    cols = np.tile(np.repeat(np.arange(layers), 4), n)
    grid[rows, cols, view.experts.reshape(-1).astype(int)] = view.weights.reshape(-1)
    return grid


def min_items(n: int) -> int:
    return max(MIN_ITEMS, int(np.ceil(MIN_SHARE * n)))


Chain = List[Tuple[int, int]]  # (layer index, expert)


def grow(weights: Array, start: Tuple[int, int], members: Array, floor: int) -> Tuple[Chain, Array]:
    """Follow the bundle from a seed: at each next layer, the expert the members weight most."""
    has = weights > 0
    chain: Chain = [start]
    members = members & has[:, start[0], start[1]]
    for li in range(start[0] + 1, weights.shape[1]):
        nxt = int(weights[members, li, :].sum(axis=0).argmax())
        keep = members & has[:, li, nxt]
        if keep.sum() < floor:
            break
        chain.append((li, nxt))
        members = keep
    return chain, members


def near_duplicates(a: Chain, b: Chain) -> bool:
    """Two chains that share three layers or more and nowhere differ for three layers running."""
    mine = dict(a)
    shared = [(li, e) for li, e in b if li in mine]
    if len(shared) < MIN_LENGTH:
        return False
    run = 0
    for li, e in shared:
        run = run + 1 if mine[li] != e else 0
        if run >= MIN_LENGTH:
            return False
    return True


def find_pipelines(weights: Array, floor: int) -> List[Tuple[Chain, Array, Array]]:
    """The pipelines, strongest first: each chain, its members (a mask) and their credits."""
    n = weights.shape[0]
    every = np.ones(n, dtype=bool)
    found: List[Tuple[float, Chain, Array, Array]] = []
    for li in range(weights.shape[1] - MIN_LENGTH + 1):
        for expert in np.flatnonzero((weights[:, li, :] > 0).sum(axis=0) >= floor):
            chain, members = grow(weights, (li, int(expert)), every, floor)
            if len(chain) < MIN_LENGTH:
                continue
            steps = np.stack([weights[:, at, e] for at, e in chain], axis=1)
            credit = np.where(members, np.exp(np.log(np.where(steps > 0, steps, 1.0)).mean(axis=1)), 0.0)
            found.append((float(credit.sum()) * len(chain), chain, members, credit))
    kept: List[Tuple[Chain, Array, Array]] = []
    for _, chain, members, credit in sorted(found, key=lambda f: -f[0]):
        if not any(near_duplicates(chain, other) for other, _, _ in kept):
            kept.append((chain, members, credit))
    return kept


def find_hubs(weights: Array, floor: int) -> List[Dict[str, Any]]:
    """Experts whose items arrive from different sources, most sources first."""
    def entropy(p: Array) -> Array:
        safe = np.where(p > 0, p, 1.0)
        result: Array = -(p * np.log(safe)).sum(axis=-1)
        return result

    hubs: List[Dict[str, Any]] = []
    for li in range(1, weights.shape[1]):
        sources = weights[:, li - 1, :]
        own = entropy(sources)
        for expert in range(weights.shape[2]):
            w = weights[:, li, expert]
            if w.sum() < floor:
                continue
            share = w / w.sum()
            mixture = share @ sources
            between = float(entropy(mixture) - share @ own)
            effective = float(np.exp(max(between, 0.0)))
            if effective < HUB_SOURCES - 1e-6:  # two wholly separate streams make exactly two
                continue
            after = share @ weights[:, li + 1, :] if li + 1 < weights.shape[1] else None
            hubs.append({"li": li, "expert": expert, "weighted": round(float(w.sum()), 2), "items": int((w > 0).sum()),
                         "sources": round(effective, 3),
                         "from": [{"expert": int(e), "share": round(float(mixture[e]), 3)} for e in np.argsort(-mixture)[:3]],
                         "to": [] if after is None else
                         [{"expert": int(e), "share": round(float(after[e]), 3)} for e in np.argsort(-after)[:3]]})
    return sorted(hubs, key=lambda h: -h["sources"])[:MAX_HUBS]


def _groups(items: Sequence[Dict[str, Any]], family_field: str, codes: Array,
            whole: bool = False) -> Tuple[Array, str]:
    """What moves together under permutation: whole families when each family holds one value,
    else items with the same text. Returns each item's group index and the kind of grouping."""
    from services.lenses.validate import family_keys

    keys = family_keys(items, family_field, whole)
    if keys is not None:
        pure = all(len({int(c) for c, k in zip(codes, keys) if k == key}) == 1 for key in set(keys))
        if pure:
            index = {key: i for i, key in enumerate(sorted(set(keys)))}
            return np.array([index[k] for k in keys]), "families"
    texts = [str(item.get("input_text") or item["probe_id"]) for item in items]
    index = {t: i for i, t in enumerate(sorted(set(texts)))}
    return np.array([index[t] for t in texts]), "texts"


def find_involved(weights: Array, items: Sequence[Dict[str, Any]], axes: Dict[str, List[str]],
                  family_field: str, seed: int, whole: bool = False) -> Dict[str, Any]:
    """Per designed axis and value: the experts whose mean weight differs from the rest's beyond the
    permutation threshold, largest difference first."""
    from sklearn.metrics import roc_auc_score

    from services.lenses.flows import value_of

    n, layers, experts = weights.shape
    flat = weights.reshape(n, layers * experts)
    rng = np.random.default_rng(seed)
    out: Dict[str, Any] = {}
    for axis, values in axes.items():
        raw = [value_of(item, axis) for item in items]
        known = np.array([v is not None for v in raw])
        codes = np.array([values.index(v) if v in values else -1 for v in raw])
        if known.sum() < 2 * MIN_ITEMS or len(set(codes[known].tolist())) < 2:
            continue
        groups, kind = _groups([items[i] for i in np.flatnonzero(known)], family_field, codes[known], whole)
        x, c = flat[known], codes[known]
        found: Dict[str, Any] = {}
        for vi, value in enumerate(values):
            y = c == vi
            if y.sum() < MIN_ITEMS or (~y).sum() < MIN_ITEMS:
                continue
            diff = x[y].mean(axis=0) - x[~y].mean(axis=0)
            group_y = np.array([y[groups == g][0] for g in range(groups.max() + 1)])
            largest = []
            for _ in range(PERMUTATIONS):
                shuffled = rng.permutation(group_y)[groups]
                largest.append(np.abs(x[shuffled].mean(axis=0) - x[~shuffled].mean(axis=0)).max())
            threshold = float(np.quantile(largest, 0.95))
            cells = [int(i) for i in np.argsort(-np.abs(diff)) if abs(diff[i]) > threshold][:MAX_INVOLVED]
            found[value] = {
                "n": int(y.sum()), "threshold": round(threshold, 4), "permuted": kind,
                "experts": [{"li": cell // experts, "expert": cell % experts, "diff": round(float(diff[cell]), 4),
                             "favours": value if diff[cell] > 0 else "rest",
                             "auc": round(float(roc_auc_score(y, x[:, cell])), 3)} for cell in cells]}
        out[axis] = found
    return out


def _halves(items: Sequence[Dict[str, Any]], family_field: str, seed: int, whole: bool = False) -> List[Array]:
    from services.lenses.search import merge_folds
    from services.lenses.validate import make_folds

    folds, _ = make_folds(items, family_field, 2, seed, whole)
    return merge_folds(folds, 2)[0]


def compute_routes(view: LensView, family_field: str = "scene", seed: int = 42,
                   whole: bool = False) -> Dict[str, Any]:
    """Pipelines, hubs and the experts involved, as `routes.json` holds them (layers by number)."""
    from services.lenses.flows import axes_of, value_of

    weights = dense(view)
    n = len(view.items)
    floor = min_items(n)
    axes = {axis: values for axis, values in axes_of(view).items() if axis != family_field}  # families group, not describe
    halves = _halves(view.items, family_field, seed, whole)

    def makeup(mask: Array) -> Dict[str, Dict[str, int]]:
        out: Dict[str, Dict[str, int]] = {}
        for axis in axes:
            counts: Dict[str, int] = {}
            for i in np.flatnonzero(mask):
                value = value_of(view.items[int(i)], axis)
                if value is not None:
                    counts[value] = counts.get(value, 0) + 1
            out[axis] = counts
        return out

    def neighbours(mask: Array, li: int) -> List[Dict[str, Any]]:
        if not 0 <= li < weights.shape[1]:
            return []
        totals = weights[mask, li, :].sum(axis=0)
        share = totals / max(totals.sum(), 1e-12)
        return [{"layer": view.layers[li], "expert": int(e), "share": round(float(share[e]), 3)}
                for e in np.argsort(-share)[:3] if share[e] > 0]

    pipelines = []
    for chain, members, credit in find_pipelines(weights, floor)[:MAX_PIPELINES]:
        lis = [li for li, _ in chain]
        experts = [e for _, e in chain]
        top = view.experts[:, lis, 0] == np.array(experts)
        replicated = []
        for half in halves:
            mask = np.zeros(n, dtype=bool)
            mask[half] = True
            again, _ = grow(weights, chain[0], mask, max(2, floor // 2))
            replicated.append(again == chain or near_duplicates(again, chain))
        pipelines.append({
            "layers": [view.layers[li] for li in lis], "experts": experts,
            "members": int(members.sum()), "weighted": round(float(credit.sum()), 2),
            "mean_weight": round(float(credit[members].mean()), 3),
            "rank1": int((top.all(axis=1) & members).sum()),
            "makeup": makeup(members), "replicated": all(replicated),
            "before": neighbours(members, lis[0] - 1), "after": neighbours(members, lis[-1] + 1),
            "member_ids": [view.items[int(i)]["probe_id"] for i in np.flatnonzero(members)],
        })
    for i, pipeline in enumerate(pipelines):
        pipeline["id"] = f"P{i + 1}"
    hubs = [{"id": f"H{i + 1}", "layer": view.layers[h.pop("li")], **h} for i, h in enumerate(find_hubs(weights, floor))]
    involved = find_involved(weights, view.items, axes, family_field, seed, whole)
    for found in involved.values():
        for value in found.values():
            for cell in value["experts"]:
                cell["layer"] = view.layers[cell.pop("li")]
    return {"format_version": FORMAT_VERSION, "n_items": n, "layers": view.layers, "min_items": floor,
            "base": makeup(np.ones(n, dtype=bool)), "pipelines": pipelines, "hubs": hubs, "involved": involved,
            "rules": {"min_share": MIN_SHARE, "min_items": MIN_ITEMS, "min_length": MIN_LENGTH,
                      "hub_sources": HUB_SOURCES, "permutations": PERMUTATIONS, "family_field": family_field,
                      "whole_families": whole}}


def write_routes(session_id: str, name: str, family_field: str = "scene", whole: bool = False) -> Dict[str, Any]:
    """Work out a lens's routes and write `routes.json` (atomically); returns what was written."""
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.view import open_lens

    folder = lens_dir(session_id, name)
    manifest = read_manifest(folder)
    started = time.time()
    routes = compute_routes(open_lens(session_id, name), family_field, manifest.settings.seed, whole)
    routes["seconds"] = round(time.time() - started, 2)
    tmp = folder / ".routes.json.tmp"
    tmp.write_text(json.dumps(routes, indent=1), encoding="utf-8")
    os.replace(tmp, folder / "routes.json")
    return routes


def routes_job(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_routes` job: write a lens's routes."""
    ctx.progress("routes", 0, 1)
    routes = write_routes(params["session_id"], params["name"], params.get("family_field", "scene"),
                          bool(params.get("whole_families", False)))
    return {"session_id": params["session_id"], "name": params["name"], "pipelines": len(routes["pipelines"]),
            "hubs": len(routes["hubs"]), "seconds": routes["seconds"]}


def serve_routes(view: LensView, routes: Dict[str, Any], version: Optional[str] = None) -> Dict[str, Any]:
    """The routes with, for each pipeline, the nodes its items sit in at each of its layers (at the
    view's version)."""
    index = {item["probe_id"]: i for i, item in enumerate(view.items)}
    served = dict(routes)
    served["version"] = view.version
    pipelines = []
    for pipeline in routes["pipelines"]:
        rows = np.array([index[p] for p in pipeline["member_ids"] if p in index], dtype=int)
        nodes = []
        for layer in pipeline["layers"]:
            li = view.layers.index(layer)
            counts = np.bincount(view.nodes[rows, li]) if rows.size else np.zeros(0, dtype=int)
            nodes.append({str(int(node)): int(count) for node, count in enumerate(counts) if count})
        pipelines.append(pipeline | {"nodes": nodes})
    served["pipelines"] = pipelines
    return served
