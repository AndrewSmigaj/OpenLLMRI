"""Reading captures through a saved UMAP lens (DESIGN.md B5, lens slice 1b): placed items vote for
their nodes, the lens's own items keep theirs, a far capture is flagged, one item read alone lands
where it lands among others, a changed capture is refused, a new version re-votes without a
re-read; and the expert flows give each item's own expert."""

from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from fastapi.testclient import TestClient
from test_lens_api import client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION, build, lake, lens  # noqa: F401  (lake is a fixture)

from core.parquet_reader import read_records
from core.parquet_writer import write_records_batch
from schemas.tokens import ProbeRecord
from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.data import load_states
from services.lenses.readout import read_lens, serve_reading


def copy_capture(lake: Path, name: str, shift: float = 0.0, noise: float = 0.3, keep: int = 40) -> None:  # noqa: F811
    """A second capture of the synthetic items under new probe ids: their states plus noise, or
    moved far away (`shift`), keeping the first `keep` items."""
    source = lake / SESSION
    folder = lake / name
    folder.mkdir()
    records = read_records(str(source / "tokens.parquet"), ProbeRecord)[:keep]
    ids = [r.probe_id for r in records]
    states = load_states(SESSION, ids)
    rng = np.random.default_rng(5)
    rows, routes = [], []
    for i, r in enumerate(records):
        r.probe_id, r.session_id = f"{name}_{r.probe_id}", name
        for layer, matrix in states.items():
            moved = matrix[i] + shift + rng.normal(scale=noise, size=matrix.shape[1])
            rows.append({"probe_id": r.probe_id, "layer": layer, "token_position": 1, "residual_stream": moved.tolist()})
            weights = np.arange(32, dtype=float) + i
            routes.append({"probe_id": r.probe_id, "layer": layer, "token_position": 1,
                           "routing_weights": (weights / weights.sum()).tolist()})
    write_records_batch(records, str(folder / "tokens.parquet"))
    pq.write_table(pa.Table.from_pylist(rows), folder / "residual_streams.parquet")
    pq.write_table(pa.Table.from_pylist(routes), folder / "routing.parquet")


def read(lake: Path, target: str, key: str, **params: Any) -> Dict[str, Any]:  # noqa: F811
    """Run the reading job in this process, as the worker would."""
    store = JobStore(lake / "_jobs")
    full = {"session_id": SESSION, "name": "synth", "target": target, "key": key, **params}
    job = store.submit("lens_read", "cpu", full, created_by="test")
    return read_lens(full, JobContext(store, job.id))


def stored_nodes(root: Path, version: str = "v1") -> Any:
    return np.load(lens(root) / version / "assign.npz")["nodes"]


def test_noisy_copies_vote_for_their_own_items_nodes(lake: Path) -> None:  # noqa: F811
    build(lake)
    copy_capture(lake, "session_copies")
    result = read(lake, "session_copies", "copies")
    assert result["n_items"] == 40 and result["n_in_lens"] == 0
    served = serve_reading(lens(lake), "copies")
    nodes = np.array(served["nodes"])
    assert (nodes == stored_nodes(lake)).mean() >= 0.95
    assert all(share is not None and 0.5 <= share <= 1.0 for row in served["shares"] for share in row)
    assert not any(served["distance"]["far_out"])


def test_the_lens_own_items_keep_their_nodes_and_a_far_capture_is_flagged(lake: Path) -> None:  # noqa: F811
    build(lake)
    read(lake, SESSION, "own")
    own = serve_reading(lens(lake), "own")
    assert all(i >= 0 for i in own["in_lens"]) and all(s is None for row in own["shares"] for s in row)
    assert (np.array(own["nodes"]) == stored_nodes(lake)).all()
    copy_capture(lake, "session_far", shift=40.0)
    far = read(lake, "session_far", "far")
    assert min(far["median_percentile"]) > 75
    assert all(serve_reading(lens(lake), "far")["distance"]["far_out"])


def test_an_item_read_alone_lands_where_it_lands_among_others(lake: Path) -> None:  # noqa: F811
    build(lake)
    copy_capture(lake, "session_copies")
    copy_capture(lake, "session_one", keep=1)  # the same first item, the same noise
    read(lake, "session_copies", "all")
    read(lake, "session_one", "one")
    together = np.load(lens(lake) / "readings" / "all" / "read.npz")["embedding"]
    alone = np.load(lens(lake) / "readings" / "one" / "read.npz")["embedding"]
    assert np.array_equal(alone[0], together[0])


def test_a_changed_capture_is_refused(lake: Path) -> None:  # noqa: F811
    build(lake)
    path = lake / SESSION / "residual_streams.parquet"
    table = pq.read_table(path).to_pylist()
    table[0]["residual_stream"] = [v + 1.0 for v in table[0]["residual_stream"]]
    pq.write_table(pa.Table.from_pylist(table), path)
    copy_capture(lake, "session_copies")
    with pytest.raises(ValueError, match="changed since the lens was built"):
        read(lake, "session_copies", "copies")


def test_a_new_version_re_votes_without_a_re_read(lake: Path) -> None:  # noqa: F811
    from services.lenses.versions import new_version

    build(lake)
    copy_capture(lake, "session_copies")
    read(lake, "session_copies", "copies")
    placed = (lens(lake) / "readings" / "copies" / "read.npz").stat().st_mtime_ns
    new_version(lens(lake), [3, 3, 3], ["test"] * 3)
    v2 = serve_reading(lens(lake), "copies", version="v2")
    nodes = np.array(v2["nodes"])
    assert v2["version"] == "v2" and nodes.max() == 2  # the third node is voted for
    # most copies follow their originals' v2 nodes (k = 3 splits a blob, whose boundary is arbitrary)
    assert (nodes == stored_nodes(lake, "v2")).mean() >= 0.8
    assert (lens(lake) / "readings" / "copies" / "read.npz").stat().st_mtime_ns == placed


def test_the_expert_flows_give_each_items_own_expert(lake: Path) -> None:  # noqa: F811
    from services.lenses.flows import expert_flows
    from services.lenses.view import open_lens

    build(lake)
    view = open_lens(SESSION, "synth")
    for rank in (1, 4):
        given = expert_flows(view, rank)["assignments"]
        for i, item in enumerate(view.items):
            assert [given[item["probe_id"]][str(layer)] for layer in view.layers] == view.experts[i, :, rank - 1].tolist()


def test_the_reading_endpoints(client: TestClient) -> None:  # noqa: F811
    from services.lenses.readout import read_lens as job

    run_job(client, client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10,
                                                     "k": 2, "workers": 1}).json()["job_id"])
    base = f"/api/sessions/{SESSION}/lenses/synth/readings"
    assert client.post(f"/api/sessions/{SESSION}/lenses/nope/readings", json={}).status_code == 404
    assert client.get(base).status_code == 400  # a UMAP lens names its reading
    started = client.post(base, json={"filters": {"steps": None}, "created_by": "test"})
    assert started.status_code == 202 and started.json()["key"] == "synth"
    assert client.post(base, json={"created_by": "test"}).status_code == 409  # already being made
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    job_id = started.json()["job_id"]
    job(store.load(job_id).params, JobContext(store, job_id))
    assert client.post(base, json={"created_by": "test"}).status_code == 409  # the name is taken
    served = client.get(base, params={"key": "synth", "rank": 2})
    assert served.status_code == 200 and served.json()["rank"] == 2 and len(served.json()["nodes"]) == 40
    listed = client.get(f"/api/sessions/{SESSION}/lenses").json()
    readings: List[Dict[str, Any]] = listed[0]["readings"]
    assert [(r["key"], r["n_items"], r["n_in_lens"]) for r in readings] == [("synth", 40, 40)]
    assert client.get(base, params={"key": "other"}).status_code == 404
