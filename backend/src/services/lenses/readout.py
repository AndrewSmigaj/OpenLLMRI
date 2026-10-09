"""Reading any capture through a saved UMAP lens (DESIGN.md B5 and D; lens slice 1b).

A reading places each item of a capture in the lens's own space, layer by layer, and keeps its 15
nearest lens items there. Its node is voted from them when the reading is served, the same vote
validation uses, so a new version of the lens (another k) reassigns a reading without placing it
again.

- The lens's own items (the same capture, probe and token position) keep their stored point and
  node exactly.
- Other items are placed by the saved reducer one item per call. UMAP's transform draws from one
  random stream per call, so a batch would make a reading depend on what else was read with it;
  Watch reads one tick at a time.
- The reducers were saved without their training rows. They are read back from the lens's
  capture, and the job refuses unless the rows match UMAP's own hash of them, the lens kept UMAP's
  exact-neighbour path (at most 4,095 items, whose transform needs nothing but the rows) and
  umap-learn is the version the lens was built with.
- How far out an item sits, in the residual stream as captured: its mean distance to its 15
  nearest lens items, as a percentile of each lens item's mean distance to its 15 nearest others.
  This is measured in raw space because the lens's own space can't show it: UMAP's transform
  places even a far-off item among its fitted points, and places held-out items of the lens's own
  kind farther from them than they sit from each other (held-out tank sentences landed at the
  86th to 96th percentile there). In raw space, held-out tank sentences sit at the 52nd to 61st
  percentile, sentences in the carrier format at the 83rd to 94th, and the calibration set's at
  the 73rd to 85th (L4, L12, L20). This is a check on the reading's context, not a measure of
  concepts: raw distances don't place or group items. The capture's median is reported per
  layer, with a warning above the 75th percentile (D2's rule 3: a lens is checked in the context
  it reads). Presence proper (D4) comes with time studies (slice 4).

`<lens>/readings/<key>/` holds:
- `read.npz`: `embedding` [N, L, D] float32 (zero-padded to the lens's widest layer), `near`
  [N, L, 15] (indices into the lens's items, nearest first), `dist` [N, L, 15], `in_lens` [N]
  (the item's index among the lens's items, else -1), `pct` [N, L], and each item's own top four
  `experts` [N, L, 4] and `weights` (the model's own, rank 1 first);
- `items.parquet`: the items read, in capture order;
- `reading.json`: the target, site, filters, counts, the medians and warning, provenance.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from pydantic import BaseModel, Field

from services.lenses.data import LensFilters
from services.lenses.validate import VOTE_NEIGHBOURS, nearest, vote

Array = np.ndarray[Any, Any]

FORMAT_VERSION = 1
FAR_OUT = 75.0  # a capture whose median item sits beyond this percentile of the lens's own is flagged
_KEY = re.compile(r"^[a-z0-9][a-z0-9_\-]{0,79}$")


class ReadParams(BaseModel):
    session_id: str  # the lens's capture
    name: str  # the lens
    target: str  # the capture read (the lens's own, to read its other steps)
    key: Optional[str] = None  # the reading's name; made from the target and filters when not given
    filters: LensFilters = Field(default_factory=LensFilters)
    position: Optional[int] = None  # the token position read; the lens's own by default


def reading_key(target: str, filters: LensFilters) -> str:
    """A reading's default name: the capture, then its step filter, e.g. "b629b6c5-steps-0"."""
    key = target.removeprefix("session_").lower()
    if filters.steps:
        key += "-steps-" + "-".join(str(s) for s in sorted(filters.steps))
    if not filters.last_occurrence_only:
        key += "-every-occurrence"
    if filters.max_items:
        key += f"-max-{filters.max_items}"
    return key


def valid_key(key: str) -> bool:
    return bool(_KEY.match(key))


def readings_dir(lens_folder: Path) -> Path:
    return lens_folder / "readings"


def _others_nearest(own: Array) -> Tuple[Array, Array]:
    """Each lens item's VOTE_NEIGHBOURS nearest other lens items (never itself, even when another
    item sits at the same point), nearest first: indices and distances."""
    from scipy.spatial.distance import cdist

    distance = cdist(own, own)  # no [N, N, D] intermediate: a lens can hold 4,095 items
    np.fill_diagonal(distance, np.inf)
    near = np.argsort(distance, axis=1)[:, :VOTE_NEIGHBOURS]
    return near, np.take_along_axis(distance, near, axis=1)


def _percentile(reference: Array, values: Array) -> Array:
    """Each value's percentile among the reference values (the share at or below it, times 100)."""
    ordered = np.sort(reference)
    pct: Array = 100.0 * np.searchsorted(ordered, values, side="right") / len(ordered)
    return pct


def _place(reducer: Any, states: Array) -> Array:
    """Items placed by a fitted reducer one item per call (see the module notes)."""
    return np.stack([np.asarray(reducer.transform(states[i:i + 1]), dtype=np.float32)[0] for i in range(len(states))])


def _raw_reach(lens_rows: Array, rows: Array, in_lens: Array) -> Array:
    """Each item's percentile in raw space (see the module notes): its mean distance to its 15
    nearest lens items (others, for the lens's own items) against each lens item's to its 15
    nearest others."""
    from scipy.spatial.distance import cdist

    own = cdist(lens_rows, lens_rows)
    np.fill_diagonal(own, np.inf)
    reference = np.sort(own, axis=1)[:, :VOTE_NEIGHBOURS].mean(axis=1)
    distance = cdist(rows, lens_rows)
    mine = in_lens >= 0
    distance[np.flatnonzero(mine), in_lens[mine]] = np.inf  # a lens item is not its own neighbour
    return _percentile(reference, np.sort(distance, axis=1)[:, :VOTE_NEIGHBOURS].mean(axis=1))


def read_lens(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_read` job: read a capture through a saved UMAP lens (see the module notes)."""
    import joblib
    import pyarrow.parquet as pq
    import umap

    from services.lenses.build import _write_items
    from services.lenses.data import load_items, load_routing, load_states, own_top4, session_dir
    from services.lenses.store import git_state, lens_dir, read_manifest

    started = time.time()
    p = ReadParams.model_validate(params)
    folder = lens_dir(p.session_id, p.name)
    manifest = read_manifest(folder)
    if manifest.kind != "umap":
        raise ValueError(f"'{p.name}' is a {manifest.kind} lens: its readings need no job")
    built_with = manifest.provenance.libraries.get("umap-learn")
    if built_with and built_with != umap.__version__:
        raise ValueError(f"the lens was built with umap-learn {built_with} and this is {umap.__version__}: rebuild it")
    key = p.key or reading_key(session_dir(p.target).name, p.filters)
    if not valid_key(key):
        raise ValueError(f"not a reading name: {key!r} (lowercase letters, digits, '_' and '-')")
    final = readings_dir(folder) / key
    if final.exists():
        raise FileExistsError(f"lens {p.name!r} already has a reading {key!r}")
    tmp = readings_dir(folder) / f".tmp-{key}-{ctx.job_id}"
    ctx.add_temp_path(tmp)
    tmp.mkdir(parents=True)

    ctx.progress("loading", 0, 1)
    lens_ids = pq.read_table(folder / "items.parquet", columns=["probe_id"]).column("probe_id").to_pylist()
    items = load_items(p.target, p.filters)
    if not items:
        raise ValueError("no items to read after the filters")
    ids = [r.probe_id for r in items]
    position = manifest.site.token_position if p.position is None else p.position
    same = session_dir(p.target).name == session_dir(p.session_id).name and position == manifest.site.token_position
    index = {pid: i for i, pid in enumerate(lens_ids)}
    in_lens = np.array([index.get(pid, -1) if same else -1 for pid in ids], dtype=np.int32)
    lens_states = load_states(p.session_id, lens_ids, manifest.site.source, manifest.site.token_position)
    states = load_states(p.target, ids, manifest.site.source, position)
    embed = np.load(folder / "fit" / "embed.npz")["embedding"]
    layers = manifest.layers
    n, width = len(ids), int(embed.shape[2])
    out = {"embedding": np.zeros((n, len(layers), width), dtype=np.float32),
           "near": np.zeros((n, len(layers), VOTE_NEIGHBOURS), dtype=np.int32),
           "dist": np.zeros((n, len(layers), VOTE_NEIGHBOURS), dtype=np.float32),
           "pct": np.zeros((n, len(layers)), dtype=np.float32)}
    medians: List[float] = []
    outside = np.flatnonzero(in_lens < 0)
    for li, layer in enumerate(layers):
        ctx.progress("placing", li, len(layers))
        ctx.check_cancelled()
        reducer = joblib.load(folder / "fit" / f"umap_L{layer:02d}.joblib")
        rows = np.ascontiguousarray(lens_states[layer])
        if joblib.hash(rows) != reducer._input_hash:
            raise ValueError(f"layer {layer}: the lens's capture has changed since the lens was built: rebuild it")
        if not getattr(reducer, "_small_data", False):
            raise ValueError(f"layer {layer}: the lens was fitted without UMAP's exact-neighbour path, "
                             "whose saved form can't place new items: rebuild it with at most 4,095 items")
        reducer._raw_data = rows
        dims = int(reducer.n_components)
        own = embed[li][:, :dims]
        own_near, own_dist = _others_nearest(own)
        placed = np.zeros((n, dims), dtype=np.float32)
        near = np.zeros((n, VOTE_NEIGHBOURS), dtype=np.int64)
        dist = np.zeros((n, VOTE_NEIGHBOURS), dtype=np.float32)
        mine = in_lens >= 0
        placed[mine] = own[in_lens[mine]]
        near[mine], dist[mine] = own_near[in_lens[mine]], own_dist[in_lens[mine]]
        if outside.size:
            placed[outside] = _place(reducer, states[layer][outside])
            near[outside], dist[outside] = nearest(placed[outside], own)
        pct = _raw_reach(rows, states[layer], in_lens)
        out["embedding"][:, li, :dims] = placed
        out["near"][:, li] = near
        out["dist"][:, li] = dist
        out["pct"][:, li] = pct
        medians.append(round(float(np.median(pct)), 1))
    ctx.progress("writing", 0, 1)
    experts, weights = own_top4(load_routing(p.target, ids, position))
    np.savez_compressed(tmp / "read.npz", in_lens=in_lens, experts=experts[:, layers],
                        weights=weights[:, layers].astype(np.float16), **out)
    _write_items(tmp / "items.parquet", items)
    commit, dirty = git_state()
    record: Dict[str, Any] = {
        "format_version": FORMAT_VERSION, "key": key, "lens": p.name, "lens_session": manifest.session_id,
        "target": session_dir(p.target).name, "site": {"source": manifest.site.source, "token_position": position},
        "filters": p.filters.model_dump(), "n_items": n, "n_in_lens": int((in_lens >= 0).sum()), "layers": layers,
        "distance": {"median_percentile": medians, "far_out": [m > FAR_OUT for m in medians],
                     "threshold": FAR_OUT,
                     "measure": "in the residual stream: mean distance to the 15 nearest lens items, as a "
                                "percentile of each lens item's to its 15 nearest others"},
        "provenance": {"commit": commit, "dirty": dirty, "job_id": ctx.job_id,
                       "created_by": params.get("created_by", "unknown"),
                       "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
                       "seconds": round(time.time() - started, 1), "libraries": {"umap-learn": umap.__version__}},
    }
    (tmp / "reading.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    os.replace(tmp, final)
    return {"session_id": p.session_id, "name": p.name, "key": key, "n_items": n,
            "n_in_lens": record["n_in_lens"], "median_percentile": medians, "seconds": record["provenance"]["seconds"]}


def list_readings(lens_folder: Path) -> List[Dict[str, Any]]:
    """The lens's readings, as its summary lists them: name, capture, counts, how far out."""
    found = []
    for path in sorted(readings_dir(lens_folder).glob("*/reading.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        medians = record["distance"]["median_percentile"]
        found.append({"key": record["key"], "target": record["target"], "n_items": record["n_items"],
                      "n_in_lens": record["n_in_lens"], "filters": record["filters"],
                      "steps": record["filters"].get("steps"), "far_out": any(record["distance"]["far_out"]),
                      "max_median_percentile": max(medians) if medians else None,
                      "created_at": record["provenance"]["created_at"]})
    return found


def serve_reading(lens_folder: Path, key: str, version: Optional[str] = None, rank: int = 1) -> Dict[str, Any]:
    """A reading at one of the lens's versions: each item's node at every layer (voted from its
    nearest lens items, or stored for the lens's own items) with the winner's share of the vote,
    how far out it sits, and its expert at `rank`."""
    import pyarrow.parquet as pq

    from services.lenses.data import display_fields
    from services.lenses.store import read_manifest, read_version
    from services.lenses.view import _item_dict

    manifest = read_manifest(lens_folder)
    folder = readings_dir(lens_folder) / key
    if not valid_key(key) or not (folder / "reading.json").exists():
        raise FileNotFoundError(f"Lens '{manifest.name}' has no reading {key!r}")
    chosen = version or manifest.current
    if chosen not in manifest.versions:
        raise FileNotFoundError(f"Lens '{manifest.name}' has no version {chosen!r}")
    if not 1 <= rank <= 4:
        raise ValueError(f"rank must be 1 to 4, got {rank}")
    record = json.loads((folder / "reading.json").read_text(encoding="utf-8"))
    data = np.load(folder / "read.npz")
    lens_nodes = np.load(lens_folder / str(chosen) / "assign.npz")["nodes"]
    k_per_layer = read_version(lens_folder, str(chosen)).k_per_layer
    in_lens = data["in_lens"]
    mine = in_lens >= 0
    nodes = np.zeros(data["pct"].shape, dtype=np.int16)
    shares = np.zeros(data["pct"].shape, dtype=np.float32)
    for li in range(len(manifest.layers)):
        voted, share = vote(data["near"][:, li], data["dist"][:, li], lens_nodes[:, li], k_per_layer[li])
        nodes[:, li] = voted
        shares[:, li] = share
        nodes[mine, li] = lens_nodes[in_lens[mine], li]
    shown = display_fields(record["target"])
    items = [_item_dict(row) for row in pq.read_table(folder / "items.parquet").to_pylist()]
    items = [item | {"run": shown.get(item["probe_id"], {}).get("run")} for item in items]
    return {
        "key": key, "lens": manifest.name, "version": chosen, "target": record["target"], "site": record["site"],
        "layers": manifest.layers, "rank": rank, "items": items, "in_lens": in_lens.tolist(),
        "nodes": nodes.tolist(),
        "shares": [[None if mine[i] else round(float(v), 3) for v in row] for i, row in enumerate(shares)],
        "pct": np.round(data["pct"], 1).tolist(),
        "experts": data["experts"][:, :, rank - 1].tolist(),
        "distance": record["distance"], "provenance": record["provenance"],
    }

