"""Shared loading and the account for the attention-and-experts study (read-only; DESIGN.md C5,
LENS-30; docs/research/attention_and_experts.md).

Each decoder layer of gpt-oss adds two things to a token's state: attention's output and the
experts' output (the four gate-weighted experts' sum), nothing scaled. Captures store each layer's
output (residual_streams.parquet) and the experts' output (embeddings.parquet) at the read token, so
attention's part at layer l is output_l - output_(l-1) - experts_l, where the state before layer 0
is the read token's embedding row. For two groups of items, the difference of their mean states at a
target layer T is exactly the embedding's part plus every layer's attention and experts parts up to
T; projected on its own direction, it divides the separation (its length) into shares that add up
to one. Everything an account needs is linear in the items, so it runs on mean differences: a
weight row per split (1/n on one group, -1/n on the other) times each layer's states.

Every analysis runs from the repo root with the project's Python, for example
  .venv/bin/python docs/studies/attention_experts/analysis/account.py tank
and writes its numbers to results/ and its charts to figures/ beside this file.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend/src"))

HERE = Path(__file__).parent
FIGURES = HERE / "figures"
RESULTS = HERE / "results"
MODEL = ROOT / "data/models/gpt-oss-20b"
LAKE = ROOT / "data/lake"
SEED = 1
SEPARATION_NULL = 1000  # random splits for the separation's null
SHARE_NULL = 200  # of those, the ones that go through the whole account
BOOTSTRAPS = 500  # resamples of whole units for the designed splits' intervals
ROUNDING_FLAG = 0.05  # flag a target where fp16 rounding could move the separation by this share

# The captures (each read through one lens's items and nodes), the field naming each item's
# family (None: units are texts; "scenario": an agent run's scenario), and the named pairs
# (A, B: the account of B's mean minus A's)
CAPTURES: Dict[str, Dict[str, Any]] = {
    "tank": {"session": "session_1434a9be", "lens": "tank-k5-n15", "family": None,
             "pairs": [("aquarium", "vehicle"), ("aquarium", "septic")]},
    "calibration": {"session": "session_29a80932", "lens": "calibration-q1-k2-n15", "family": "scene",
                    "pairs": [("aquarium", "vehicle")]},
    "framing": {"session": "session_673360a5", "lens": "framing-k4-auto-levels", "family": None,
                "pairs": [("roleplay", "factual")]},
    "words": {"session": "session_8f536bea", "lens": "words-k8-n15-tuned", "family": "family", "pairs": []},
    "ontology": {"session": "session_5cd7091d", "lens": "onto-k8-n15", "family": "order", "whole": True,
                 "pairs": [], "axis_pairs": {"danger": ("harmless", "can kill")}},
    "objects": {"session": "session_2be574c4", "lens": "objects-k3-n15-tuned", "family": "domain", "whole": True,
                "pairs": [("benign", "harmful")]},
    "friend_foe": {"session": "session_b629b6c5", "lens": "friend-foe-t1", "family": "scenario",
                   "pairs": [("friend", "foe")]},
}
CONTEXT = ("tank", "calibration", "framing", "friend_foe")  # sentences and agent runs: context to bring in
SINGLE_WORDS = ("words", "ontology", "objects")


@dataclass
class Capture:
    """One capture as a lens reads it: its items in the lens's order, their labels and categories,
    the units resampled together (families, scenarios or texts), the read tokens, and per layer the
    layer's output and the experts' output at the lens's site (float32, fp16 values exactly)."""
    name: str
    session: str
    lens: str
    items: List[Dict[str, Any]]
    labels: np.ndarray
    units: np.ndarray
    unit_kind: str
    token_ids: np.ndarray
    layers: List[int]
    nodes: np.ndarray  # [items, layers]: each item's node in the lens's current version
    outputs: List[np.ndarray]  # per layer index: [items, hidden]
    experts: List[np.ndarray]
    embedding: Optional[np.ndarray]  # [items, hidden] float64, or None when every item reads one token
    version: str

    def category(self, field: str) -> np.ndarray:
        return np.array([str((item.get("categories") or {}).get(field)) for item in self.items])


def _unit_keys(name: str, spec: Dict[str, Any], items: List[Dict[str, Any]], session: str) -> Tuple[np.ndarray, str]:
    from services.lenses.validate import family_keys

    field = spec.get("family")
    if field == "scenario":
        table = pq.read_table(LAKE / session / "tokens.parquet", columns=["probe_id", "scenario_id"]).to_pylist()
        scenario = {row["probe_id"]: row["scenario_id"] for row in table}
        keys: Optional[List[str]] = [str(scenario[item["probe_id"]]) for item in items]
        kind = "scenarios"
    else:
        keys = family_keys(items, field, bool(spec.get("whole"))) if field else None
        kind = "families" if keys is not None else "texts"
        if keys is None:
            keys = [str(item.get("input_text") or item["probe_id"]) for item in items]
    index = {key: i for i, key in enumerate(sorted(set(keys)))}
    return np.array([index[key] for key in keys]), kind


def embedding_rows(token_ids: Sequence[int]) -> np.ndarray:
    """The rows of `model.embed_tokens.weight` for these token ids, read alone from the safetensors
    file (BF16), cast to fp16 as the model loads them, as float64: the state before layer 0."""
    from safetensors import safe_open

    shard = json.loads((MODEL / "model.safetensors.index.json").read_text())["weight_map"]["model.embed_tokens.weight"]
    rows: Dict[int, np.ndarray] = {}
    with safe_open(str(MODEL / shard), framework="pt") as f:
        table = f.get_slice("model.embed_tokens.weight")
        for token in sorted(set(int(t) for t in token_ids)):
            rows[token] = table[token:token + 1].float().numpy()[0]
    return np.stack([rows[int(t)] for t in token_ids]).astype(np.float16).astype(np.float64)


def load_capture(name: str) -> Capture:
    from services.lenses.data import load_states
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.view import open_lens

    spec = CAPTURES[name]
    session, lens = spec["session"], spec["lens"]
    manifest = read_manifest(lens_dir(session, lens))
    view = open_lens(session, lens)
    items = view.items
    ids = [item["probe_id"] for item in items]
    site = manifest.site.token_position
    tokens = pq.read_table(LAKE / session / "tokens.parquet", columns=["probe_id", "target_token_id"]).to_pylist()
    token_of = {row["probe_id"]: row["target_token_id"] for row in tokens}
    token_ids = np.array([int(token_of[i]) for i in ids])
    outputs = load_states(session, ids, "residual_stream", site, view.layers)
    experts = load_states(session, ids, "expert_output", site, view.layers)
    units, kind = _unit_keys(name, spec, items, session)
    embedding = None if len(set(token_ids.tolist())) == 1 else embedding_rows(token_ids)
    return Capture(name=name, session=session, lens=lens, items=items,
                   labels=np.array([str(item["label"]) for item in items]), units=units, unit_kind=kind,
                   token_ids=token_ids, layers=list(view.layers), nodes=np.asarray(view.nodes),
                   outputs=[np.asarray(outputs[layer], dtype=np.float32) for layer in view.layers],
                   experts=[np.asarray(experts[layer], dtype=np.float32) for layer in view.layers],
                   embedding=embedding, version=str(view.version))


def token_check(capture: Capture) -> Dict[str, Any]:
    """Each read token decodes to the end of its item's target word (a word's last piece when it
    splits): the token whose embedding row the account starts from."""
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(MODEL / "tokenizer.json"))
    wrong = []
    for item, token in zip(capture.items, capture.token_ids.tolist()):
        piece = tokenizer.decode([token]).strip().lower()
        word = str(item.get("target_word") or "").strip().lower()
        if not piece or not word.endswith(piece):
            wrong.append({"probe_id": item["probe_id"], "word": word, "piece": piece})
    return {"items": len(capture.items), "distinct_tokens": int(len(set(capture.token_ids.tolist()))),
            "mismatches": len(wrong), "examples": wrong[:5]}


def contrast(capture: Capture, b: np.ndarray, a: np.ndarray) -> np.ndarray:
    """The weight row of a split: 1/|B| on B's items, -1/|A| on A's, 0 elsewhere."""
    w = np.zeros(len(capture.items))
    w[b] = 1.0 / len(b)
    w[a] = -1.0 / len(a)
    return w


def mean_differences(capture: Capture, weights: np.ndarray,
                     up_to: Optional[int] = None) -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    """For each weight row (one per split): the difference of means of every layer's output (up to
    layer index `up_to`), of every layer's experts' output, and of the embedding rows, in float64.
    [splits, hidden] each."""
    w = np.atleast_2d(weights)
    last = len(capture.outputs) if up_to is None else up_to + 1
    outputs = [w @ x.astype(np.float64) for x in capture.outputs[:last]]
    experts = [w @ x.astype(np.float64) for x in capture.experts[:last]]
    embedding = (w @ capture.embedding) if capture.embedding is not None else np.zeros_like(outputs[0])
    return outputs, experts, embedding


def account(outputs: List[np.ndarray], experts: List[np.ndarray], embedding: np.ndarray, target: int,
            direction: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """The split at layer index `target`, along its own direction (or `direction`): its separation,
    and the shares of the embedding and of attention and the experts at each layer up to the
    target, which add up to one. Arrays over the splits: [splits] and [splits, target + 1]."""
    gap = outputs[target]
    d = gap / np.linalg.norm(gap, axis=1, keepdims=True) if direction is None else np.atleast_2d(direction)
    along = (gap * d).sum(axis=1)
    attention, expert = [], []
    before = embedding
    for li in range(target + 1):
        attention.append(((outputs[li] - before - experts[li]) * d).sum(axis=1) / along)
        expert.append((experts[li] * d).sum(axis=1) / along)
        before = outputs[li]
    return {"separation": np.linalg.norm(gap, axis=1), "along": along,
            "embedding": (embedding * d).sum(axis=1) / along,
            "attention": np.stack(attention, axis=1), "experts": np.stack(expert, axis=1)}


TOTALS = ("embedding", "attention", "experts", "attention_here", "experts_here")


def totals_of(got: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """An account's summary shares per split (TOTALS): the embedding's, attention's and the
    experts' in total up to the target, and attention's and the experts' at the target itself."""
    return {"embedding": got["embedding"], "attention": got["attention"].sum(axis=1),
            "experts": got["experts"].sum(axis=1), "attention_here": got["attention"][:, -1],
            "experts_here": got["experts"][:, -1]}


def share_totals(capture: Capture, rows: np.ndarray, targets: Sequence[int], chunk: int = 100) -> Dict[int, Dict[str, np.ndarray]]:
    """For many weight rows (random splits, bootstraps): at each target layer index, every row's
    separation and its TOTALS shares. Worked out `chunk` rows at a time, so memory stays at a few
    hundred megabytes."""
    found: Dict[int, Dict[str, List[np.ndarray]]] = {t: {key: [] for key in ("separation", *TOTALS)} for t in targets}
    for start in range(0, len(rows), chunk):
        outputs, experts, embedding = mean_differences(capture, rows[start:start + chunk], max(targets))
        for t in targets:
            got = account(outputs, experts, embedding, t)
            found[t]["separation"].append(got["separation"])
            for key, values in totals_of(got).items():
                found[t][key].append(values)
    return {t: {key: np.concatenate(values) for key, values in by.items()} for t, by in found.items()}


def band(values: np.ndarray) -> List[float]:
    """The 5th, 50th and 95th percentiles."""
    return [round(float(v), 4) for v in np.percentile(values, [5, 50, 95])]


def precision(capture: Capture, b: np.ndarray, a: np.ndarray, li: int) -> np.ndarray:
    """The inverse of the Ledoit-Wolf shrinkage covariance of B's and A's states at layer index
    `li`, each group centred on its own mean: the discriminant's metric."""
    from sklearn.covariance import LedoitWolf

    xb = capture.outputs[li][b].astype(np.float64)
    xa = capture.outputs[li][a].astype(np.float64)
    within = np.vstack([xb - xb.mean(axis=0), xa - xa.mean(axis=0)])
    # store_precision=False: the estimator's own inverse (an eigendecomposition) would only be
    # thrown away, and it took 2 to 20 s a split
    return np.linalg.inv(LedoitWolf(store_precision=False).fit(within).covariance_)


def discriminant_shares(capture: Capture, b: np.ndarray, a: np.ndarray, t: int, null_rows: np.ndarray) -> Dict[str, Any]:
    """The second direction: the split's TOTALS shares along its shrinkage discriminant at layer
    index `t` (the mean difference weighed by the inverse within-group covariance, so that
    directions in which each group's items vary little count more), and the same shares for the
    random splits, each along its own discriminant in the same metric, so their bands compare."""
    metric = precision(capture, b, a, t)
    rows = np.vstack([contrast(capture, b, a), null_rows])
    outputs, experts, embedding = mean_differences(capture, rows, t)
    directions = outputs[t] @ metric
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    totals = totals_of(account(outputs, experts, embedding, t, direction=directions))
    return {"shares": {key: round(float(values[0]), 4) for key, values in totals.items()},
            "random": {key: band(values[1:]) for key, values in totals.items()}}


def random_splits(capture: Capture, b: np.ndarray, a: np.ndarray, count: int,
                  rng: np.random.Generator, by_units: bool = True) -> Tuple[np.ndarray, str]:
    """`count` weight rows for random splits of the same items at the real split's grain: whole
    units drawn for B (as many units as B holds) when no unit straddles the split, else items;
    always items when `by_units` is off (the branches of a node)."""
    members = np.concatenate([b, a])
    unit_b, unit_a = set(capture.units[b].tolist()), set(capture.units[a].tolist())
    rows = np.zeros((count, len(capture.items)))
    if by_units and not unit_b & unit_a and len(unit_b) > 1 and len(unit_a) > 1:
        pool = np.array(sorted(unit_b | unit_a))
        for r in range(count):
            chosen = rng.choice(pool, size=len(unit_b), replace=False)
            is_b = np.isin(capture.units[members], chosen)
            rows[r, members[is_b]] = 1.0 / is_b.sum()
            rows[r, members[~is_b]] = -1.0 / (~is_b).sum()
        return rows, capture.unit_kind
    for r in range(count):
        shuffled = rng.permutation(members)
        rows[r, shuffled[:len(b)]] = 1.0 / len(b)
        rows[r, shuffled[len(b):]] = -1.0 / len(a)
    return rows, "items"


def bootstraps(capture: Capture, b: np.ndarray, a: np.ndarray, count: int, rng: np.random.Generator) -> np.ndarray:
    """`count` weight rows resampling whole units with replacement within B and within A."""
    rows = np.zeros((count, len(capture.items)))
    for group, sign in ((b, 1.0), (a, -1.0)):
        units = np.unique(capture.units[group])
        members = {u: group[capture.units[group] == u] for u in units}
        for r in range(count):
            picked = rng.choice(units, size=len(units), replace=True)
            items = np.concatenate([members[u] for u in picked])
            np.add.at(rows[r], items, sign / len(items))
    return rows


def rounding_bound(capture: Capture, b: np.ndarray, a: np.ndarray, direction: np.ndarray, target: int) -> float:
    """The most that fp16 rounding of the two additions in each layer up to `target` can move the
    split along `direction`, summed over those layers (the attention parts carry it; the stored
    experts' outputs are exact)."""
    total = 0.0
    for li in range(target + 1):
        out = capture.outputs[li].astype(np.float64)
        mid = out - capture.experts[li]
        ulp = (np.spacing(np.abs(mid).astype(np.float16)).astype(np.float64)
               + np.spacing(np.abs(out).astype(np.float16)).astype(np.float64)) / 2
        total += float(np.abs(direction) @ (ulp[b].mean(axis=0) + ulp[a].mean(axis=0)))
    return total


def stream(*parts: int) -> np.random.Generator:
    """A seeded random stream of its own (capture, split, purpose)."""
    return np.random.default_rng([SEED, *parts])


def write_results(name: str, payload: Dict[str, Any]) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return path


def figure_path(name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    return FIGURES / f"{name}.png"
