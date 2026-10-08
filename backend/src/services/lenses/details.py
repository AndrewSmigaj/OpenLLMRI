"""What comes with each node and lens (DESIGN.md C5): the neurons behind a node, what it pushes
toward through the output vocabulary, whether surface features explain it, and how a lens bears
on routing.

- **Neurons:** the neurons whose values correlate most with membership of the node.
- **Logit lens:** the node's centre (its members' mean state) through the final norm and the
  unembedding: the tokens it favours, and the ones it favours more than the layer's average item.
- **Surface check:** how well length, the first word and sentence shape predict the node, held
  out; a node they predict well may be a split along sentence shape rather than a concept.
- **Routing effect:** how much of the item-to-item difference in the next layer's routing lines up
  with the lens's nodes (the between-node share of its variance). Read from the recorded routing,
  so it holds for any lens.
- **Router alignment** (mass-mean lenses): the routing change the axis predicts through the next
  layer's router, against random directions of the same length. Above the random 95th
  percentile the routers single the concept out; inside the range the concept rides in content
  the routers mostly ignore. The prediction skips that layer's attention (its effect on routing
  was small in the plan review: r = 0.96 to 0.998 with the recorded routing).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np

Array = np.ndarray[Any, Any]

TOP_NEURONS = 10
TOP_TOKENS = 12
RANDOM_DIRECTIONS = 1000


def node_neurons(states: Array, nodes: Array, top: int = TOP_NEURONS) -> Dict[int, List[Tuple[int, float]]]:
    """Each node's neurons, by the correlation of their values with membership (signed)."""
    z = (states - states.mean(axis=0)) / (states.std(axis=0) + 1e-8)
    out: Dict[int, List[Tuple[int, float]]] = {}
    for node in np.unique(nodes):
        member = (nodes == node).astype(np.float32)
        zm = (member - member.mean()) / (member.std() + 1e-8)
        r = (z * zm[:, None]).mean(axis=0)
        best = np.argsort(-np.abs(r), kind="stable")[:top]
        out[int(node)] = [(int(j), round(float(r[j]), 4)) for j in best]
    return out


def logit_lens(centres: Array, baseline: Array, final_gain: Array, eps: float,
               chunks: Iterable[Tuple[int, Array]], top: int = TOP_TOKENS) -> Tuple[Array, Array, Array, Array]:
    """For each centre [n, D]: its top tokens by logit, and its top tokens by logit above the
    baseline's (the layer's mean item, one row per centre). One pass over the unembedding's chunks.
    Returns (ids, logits, distinctive ids, logit differences), each [n, top]."""
    from services.lenses.model_weights import rms_norm

    h, base = rms_norm(centres, final_gain, eps), rms_norm(baseline, final_gain, eps)
    n = len(centres)
    best_ids, best = np.zeros((n, 0), dtype=np.int64), np.zeros((n, 0))
    lift_ids, lift = np.zeros((n, 0), dtype=np.int64), np.zeros((n, 0))
    for start, rows in chunks:
        logits: Array = h @ rows.T  # [n, chunk]
        diff: Array = logits - base @ rows.T
        ids = np.arange(start, start + rows.shape[0])
        best_ids, best = _keep_top(best_ids, best, ids, logits, top)
        lift_ids, lift = _keep_top(lift_ids, lift, ids, diff, top)
    return best_ids, best, lift_ids, lift


def _keep_top(kept_ids: Array, kept: Array, ids: Array, values: Array, top: int) -> Tuple[Array, Array]:
    pool_ids = np.concatenate([kept_ids, np.broadcast_to(ids, values.shape)], axis=1)
    pool = np.concatenate([kept, values], axis=1)
    order = np.argsort(-pool, axis=1, kind="stable")[:, :top]
    return np.take_along_axis(pool_ids, order, axis=1), np.take_along_axis(pool, order, axis=1)


SURFACE_FLAG_AUC = 0.75  # a numeric surface feature this far from 0.5 (either way) flags the node
SURFACE_FLAG_WORD = 0.4  # or a first word this much more common inside the node than outside


def surface_features(items: Sequence[Dict[str, Any]]) -> Tuple[Dict[str, Array], List[str]]:
    """Numeric surface features per item (length, punctuation, where the target word sits) and
    each item's first word."""
    texts = [str(item.get("input_text") or "") for item in items]
    targets = [str(item.get("target_word") or "").lower() for item in items]
    position = [t.lower().rfind(w) / max(len(t), 1) if w and w in t.lower() else -1.0 for t, w in zip(texts, targets)]
    numeric = {
        "words": np.array([len(t.split()) for t in texts], dtype=float),
        "characters": np.array([len(t) for t in texts], dtype=float),
        "commas": np.array([t.count(",") for t in texts], dtype=float),
        "question": np.array([t.rstrip().endswith("?") for t in texts], dtype=float),
        "target position": np.array(position, dtype=float),
    }
    first = [(t.split() or [""])[0].strip(".,!?\"'").lower() for t in texts]
    return numeric, first


def surface_check(numeric: Dict[str, Array], first: List[str], nodes: Array) -> Dict[str, Any]:
    """Held out: how well surface features alone predict the layer's nodes (Cohen's kappa), and per
    node the strongest surface feature, flagged when it separates the node strongly."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import cohen_kappa_score, roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.preprocessing import StandardScaler

    common = [w for w, _ in sorted(((w, first.count(w)) for w in set(first)), key=lambda p: -p[1])[:20]]
    features = np.column_stack([StandardScaler().fit_transform(np.column_stack(list(numeric.values())))]
                               + [np.array([f == w for f in first], dtype=float) for w in common])
    counts = np.bincount(nodes)
    folds = int(min(5, counts[counts > 0].min())) if len(counts) else 0
    kappa = None
    if folds >= 2 and len(np.unique(nodes)) > 1:
        guess = cross_val_predict(LogisticRegression(max_iter=2000), features, nodes,
                                  cv=StratifiedKFold(folds, shuffle=True, random_state=0))
        kappa = round(float(cohen_kappa_score(nodes, guess)), 4)
    per_node: Dict[int, Any] = {}
    for node in np.unique(nodes):
        inside = nodes == node
        if inside.all():
            continue
        aucs = {name: float(roc_auc_score(inside, values)) for name, values in numeric.items() if np.ptp(values) > 0}
        name, auc = max(aucs.items(), key=lambda p: abs(p[1] - 0.5)) if aucs else ("", 0.5)
        words = [f for f, i in zip(first, inside) if i]
        word = max(set(words), key=words.count) if words else ""
        share_in = words.count(word) / max(len(words), 1)
        share_out = sum(1 for f, i in zip(first, inside) if not i and f == word) / max(int((~inside).sum()), 1)
        flagged = abs(auc - 0.5) >= SURFACE_FLAG_AUC - 0.5 or share_in - share_out >= SURFACE_FLAG_WORD
        per_node[int(node)] = {
            "flagged": bool(flagged), "feature": name, "auc": round(auc, 3),
            "members_mean": round(float(numeric[name][inside].mean()), 3) if name else None,
            "others_mean": round(float(numeric[name][~inside].mean()), 3) if name else None,
            "first_word": {"word": word, "in_node": round(share_in, 3), "outside": round(share_out, 3)}}
    return {"kappa": kappa, "nodes": per_node}


def routing_effect(nodes: Array, routing: Array) -> Tuple[float, Dict[int, Dict[str, float]]]:
    """The between-node share of the routing's item-to-item variance (0: nodes route alike; 1: the
    nodes explain it all), and per node its share and how far its mean routing sits from the
    layer's, in units of the items' typical distance from it. `routing` is [items, experts]."""
    mean = routing.mean(axis=0)
    deviation = ((routing - mean) ** 2).sum(axis=1)
    total = float(deviation.sum())
    spread = float(np.sqrt(deviation.mean())) or 1.0
    per: Dict[int, Dict[str, float]] = {}
    between = 0.0
    for node in np.unique(nodes):
        inside = nodes == node
        centre = routing[inside].mean(axis=0)
        ss = float(inside.sum() * ((centre - mean) ** 2).sum())
        between += ss
        per[int(node)] = {"share": round(ss / total, 4) if total else 0.0,
                          "shift": round(float(np.linalg.norm(centre - mean)) / spread, 4)}
    return (round(between / total, 4) if total else 0.0), per


def router_alignment(axis: Array, router: Array, gain: Array, seed: int = 0,
                     n_random: int = RANDOM_DIRECTIONS) -> Dict[str, float]:
    """How strongly the next layer's router responds to the axis, against random directions of
    the same length: the spread across experts of the logit change it predicts (a shift of every
    logit alike changes nothing). The norm's 1/rms factor is common to all, so it cancels."""
    def effect(directions: Array) -> Array:
        change = (directions * gain) @ router.T
        spread: Array = np.linalg.norm(change - change.mean(axis=-1, keepdims=True), axis=-1)
        return spread

    length = float(np.linalg.norm(axis))
    rng = np.random.default_rng(seed)
    randoms = rng.normal(size=(n_random, axis.shape[0]))
    randoms *= length / np.linalg.norm(randoms, axis=1, keepdims=True)
    observed, baseline = float(effect(axis[None, :])[0]), effect(randoms)
    median = float(np.median(baseline)) or 1.0
    return {"ratio": round(observed / median, 4), "percentile": round(float((baseline < observed).mean() * 100), 1),
            "random_95": round(float(np.percentile(baseline, 95)) / median, 4)}


def _dense_routing(experts: Array, weights: Array, n_experts: int) -> Array:
    """[items, 4] expert ids and weights as [items, experts] (the model's own top-four weights)."""
    dense = np.zeros((experts.shape[0], n_experts), dtype=np.float32)
    np.put_along_axis(dense, experts.astype(np.int64), weights.astype(np.float32), axis=1)
    return dense


def _tokens(ids: Array, values: Array, decode: Any) -> List[List[Any]]:
    return [[decode(int(i)), round(float(v), 3)] for i, v in zip(ids, values)]


def umap_details(view: Any, states: Dict[int, Array], weights: Any, ctx: Any) -> Dict[str, Any]:
    """Every node of a UMAP lens version: neurons, logit lens, surface check, routing effect."""
    numeric, first = surface_features(view.items)
    n_experts = max(32, int(view.experts.max()) + 1)
    layers: Dict[str, Any] = {}
    centres, baselines, where = [], [], []
    for li, layer in enumerate(view.layers):
        nodes = view.nodes[:, li].astype(np.int64)
        neurons = node_neurons(states[layer], nodes)
        surface = surface_check(numeric, first, nodes)
        effect, per_node = (routing_effect(nodes, _dense_routing(view.experts[:, li + 1], view.weights[:, li + 1], n_experts))
                            if li + 1 < len(view.layers) and view.layers[li + 1] == layer + 1 else (None, {}))
        layers[str(layer)] = {"surface_kappa": surface["kappa"], "routing_effect": effect, "nodes": {}}
        for node in np.unique(nodes):
            layers[str(layer)]["nodes"][str(node)] = {
                "neurons": neurons[int(node)], "surface": surface["nodes"].get(int(node)),
                "routing": per_node.get(int(node))}
            centres.append(states[layer][nodes == node].mean(axis=0))
            baselines.append(states[layer].mean(axis=0))
            where.append((str(layer), str(node)))
        ctx.progress("nodes", li + 1, len(view.layers))
    ctx.progress("logit lens", 0, 1)
    ids, logits, lift_ids, lift = logit_lens(np.stack(centres), np.stack(baselines), weights.final_norm(),
                                             weights.eps, weights.unembedding_chunks())
    decode = weights.decoder()
    for i, (layer, node) in enumerate(where):
        layers[layer]["nodes"][node]["logit_lens"] = {"top": _tokens(ids[i], logits[i], decode),
                                                      "distinctive": _tokens(lift_ids[i], lift[i], decode)}
    return {"kind": "umap", "layers": layers}


def mass_mean_details(folder: Any, layers: List[int], weights: Any, ctx: Any) -> Dict[str, Any]:
    """Every layer of a mass-mean lens: the next layer's router alignment, and the tokens each
    class's mean favours over the other's."""
    fitted = np.load(folder / "fit" / "axes.npz")
    out: Dict[str, Any] = {}
    for li, layer in enumerate(layers):
        axis = fitted["axis"][li]
        record: Dict[str, Any] = {}
        if layer + 1 in layers:
            router, _ = weights.router(layer + 1)
            record["router_alignment"] = router_alignment(axis, router, weights.pre_router_norm(layer + 1))
        out[str(layer)] = record
        ctx.progress("routers", li + 1, len(layers))
    mids, axes = fitted["mid"], fitted["axis"]
    means_b, means_a = mids + axes / 2, mids - axes / 2
    _, _, b_ids, b_lift = logit_lens(means_b, means_a, weights.final_norm(), weights.eps, weights.unembedding_chunks())
    _, _, a_ids, a_lift = logit_lens(means_a, means_b, weights.final_norm(), weights.eps, weights.unembedding_chunks())
    decode = weights.decoder()
    for li, layer in enumerate(layers):
        out[str(layer)]["logit_lens"] = {"b_over_a": _tokens(b_ids[li], b_lift[li], decode),
                                         "a_over_b": _tokens(a_ids[li], a_lift[li], decode)}
    return {"kind": "mass_mean", "layers": out}


def build_details(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_details` job: a UMAP lens version's node details, or a mass-mean lens's layer
    details, written to the lens's `details/<version>.json` (`details/mass_mean.json`)."""
    import json
    import os
    import time

    from services.lenses.data import load_states
    from services.lenses.model_weights import ModelWeights
    from services.lenses.store import git_state, lens_dir, read_manifest
    from services.lenses.view import open_lens

    started = time.time()
    session, name, version = params["session_id"], params["name"], params.get("version")
    folder = lens_dir(session, name)
    manifest = read_manifest(folder)
    weights = ModelWeights()
    if manifest.kind == "mass_mean":
        record, key = mass_mean_details(folder, manifest.layers, weights, ctx), "mass_mean"
    else:
        view = open_lens(session, name, version)
        ctx.progress("loading", 0, 1)
        states = load_states(manifest.session_id, [item["probe_id"] for item in view.items],
                             manifest.site.source, manifest.site.token_position)
        record, key = umap_details(view, states, weights, ctx), str(view.version)
    commit, dirty = git_state()
    record["provenance"] = {"commit": commit, "dirty": dirty, "job_id": ctx.job_id,
                            "seconds": round(time.time() - started, 1),
                            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (folder / "details").mkdir(exist_ok=True)
    tmp = folder / "details" / f".{key}.json.tmp"
    tmp.write_text(json.dumps(record), encoding="utf-8")
    os.replace(tmp, folder / "details" / f"{key}.json")
    if manifest.kind != "mass_mean":
        from services.llm.cards import refresh_catalogue

        refresh_catalogue(manifest.session_id, name, key)
    return {"session_id": manifest.session_id, "name": name, "version": key,
            "seconds": record["provenance"]["seconds"]}
