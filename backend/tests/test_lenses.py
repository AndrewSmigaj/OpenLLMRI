"""UMAP lenses: built as a background job, kept small, cut at any k, and true to today's clusterings.

Each test writes a small synthetic capture (two planted classes) into its own lake under
tmp_path, so no model, GPU or real data is needed.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from api import config
from core.parquet_writer import write_records_batch
from schemas.tokens import ProbeRecord
from services.jobs.kinds import JobContext
from services.jobs.store import JobStore

SESSION = "session_synth"


def make_capture(lake: Path, per_class: int = 20, layers: int = 3, dim: int = 64) -> List[str]:
    """Two classes far apart in every layer, plus noise; returns the probe ids in capture order."""
    rng = np.random.default_rng(0)
    folder = lake / SESSION
    folder.mkdir(parents=True)
    centres = rng.normal(size=(2, dim)) * 6
    records, states, routes = [], [], []
    for i in range(2 * per_class):
        pid = f"p{i:03d}"
        records.append(ProbeRecord(
            probe_id=pid, session_id=SESSION, input_text=f"item {i} with a tank", target_word="tank",
            target_token_id=1, target_token_position=4, total_tokens=6, label="ab"[i % 2],
            categories_json=json.dumps({"register": "formal" if i % 3 else "casual"})))
        for layer in range(layers):
            states.append({"probe_id": pid, "layer": layer, "token_position": 1,
                           "residual_stream": (centres[i % 2] + rng.normal(size=dim)).tolist()})
            weights = rng.random(32)
            routes.append({"probe_id": pid, "layer": layer, "token_position": 1,
                           "routing_weights": (weights / weights.sum()).tolist()})
    write_records_batch(records, str(folder / "tokens.parquet"))
    pq.write_table(pa.Table.from_pylist(states), folder / "residual_streams.parquet")
    pq.write_table(pa.Table.from_pylist(routes), folder / "routing.parquet")
    return [r.probe_id for r in records]


@pytest.fixture
def lake(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "lake"
    monkeypatch.setattr(config, "DATA_LAKE_PATH", root)
    monkeypatch.setattr(config, "LENS_RECORDS_PATH", tmp_path / "records")
    make_capture(root)
    return root


def build(lake: Path, **params: Any) -> Dict[str, Any]:
    """Run the build job in this process, as the worker would."""
    from services.lenses.build import build_lens

    store = JobStore(lake / "_jobs")
    full = {"session_id": SESSION, "name": "synth", "n_neighbors": 10, "k": 2, "workers": 1, **params}
    job = store.submit("lens_build", "cpu", full, created_by="test")
    return build_lens(full, JobContext(store, job.id))


def lens(lake: Path, name: str = "synth") -> Path:
    return lake / SESSION / "lenses" / name


def labels_of(folder: Path) -> List[str]:
    return [str(v) for v in pq.read_table(folder / "items.parquet", columns=["label"]).column("label").to_pylist()]


def test_a_build_recovers_the_planted_classes_and_leaves_a_whole_lens(lake: Path) -> None:
    from sklearn.metrics import adjusted_rand_score

    result = build(lake)
    assert (result["n_items"], result["version"]) == (40, "v1")
    folder = lens(lake)
    nodes = np.load(folder / "v1" / "assign.npz")["nodes"]
    assert nodes.shape == (40, 3)
    assert all(adjusted_rand_score(labels_of(folder), nodes[:, layer]) == 1.0 for layer in range(3))
    assert not [p for p in folder.parent.iterdir() if p.name.startswith(".tmp-")]
    assert not (folder / "work").exists()
    manifest = json.loads((folder / "lens.json").read_text())
    assert manifest["versions"] == ["v1"] and manifest["current"] == "v1"
    assert manifest["layers"] == [0, 1, 2] and manifest["n_items"] == 40
    weights = np.load(folder / "fit" / "top4.npz")["weights"].astype(np.float32)
    assert np.allclose(weights.sum(-1), 1.0, atol=1e-2)


def test_a_saved_reducer_is_stripped_and_reads_new_data_once_reattached(lake: Path) -> None:
    import joblib

    from services.lenses.data import load_states

    build(lake)
    folder = lens(lake)
    reducer = joblib.load(folder / "fit" / "umap_L00.joblib")
    assert reducer._raw_data is None
    ids = pq.read_table(folder / "items.parquet", columns=["probe_id"]).column("probe_id").to_pylist()
    rows = np.ascontiguousarray(load_states(SESSION, ids)[0])
    reducer._raw_data = rows
    assert joblib.hash(rows) == reducer._input_hash  # the capture is the one the lens was fitted on
    embedding = np.load(folder / "fit" / "embed.npz")["embedding"][0]
    nodes = np.load(folder / "v1" / "assign.npz")["nodes"][:, 0]
    noisy = rows[:6] + np.random.default_rng(1).normal(scale=0.1, size=rows[:6].shape).astype(np.float32)
    placed = reducer.transform(noisy)
    nearest = np.argmin(((placed[:, None, :] - embedding[None, :, :]) ** 2).sum(-1), axis=1)
    assert list(nodes[nearest]) == list(nodes[:6])


def test_partitions_match_the_legacy_clustering(lake: Path) -> None:
    from sklearn.metrics import adjusted_rand_score

    from services.experiments.cluster_route_analysis import ClusterRouteAnalysisService
    from services.lenses.data import load_states

    build(lake, k=3)
    folder = lens(lake)
    ids = pq.read_table(folder / "items.parquet", columns=["probe_id"]).column("probe_id").to_pylist()
    states = load_states(SESSION, ids)
    embeddings = [{"probe_id": pid, "layer": layer, "vector": states[layer][i]}
                  for layer in range(3) for i, pid in enumerate(ids)]
    legacy = ClusterRouteAnalysisService(str(lake))._perform_clustering(
        embeddings, [0, 1, 2],
        {"clustering_method": "hierarchical", "layer_cluster_counts": {0: 3, 1: 3, 2: 3}, "n_neighbors": 10},
        reduction_method="umap", reduction_dims=6)
    nodes = np.load(folder / "v1" / "assign.npz")["nodes"]
    for layer in range(3):
        old = [legacy["assignments"][pid][layer]["cluster_id"] for pid in ids]
        assert adjusted_rand_score(old, nodes[:, layer]) == 1.0


def test_the_number_of_workers_does_not_change_the_lens(lake: Path) -> None:
    build(lake, name="one", workers=1)
    build(lake, name="two", workers=2)
    for file, key in (("fit/embed.npz", "embedding"), ("fit/ward.npz", "trees"), ("v1/assign.npz", "nodes")):
        assert np.array_equal(np.load(lens(lake, "one") / file)[key], np.load(lens(lake, "two") / file)[key])


def test_a_new_k_cuts_the_saved_trees_without_refitting(lake: Path) -> None:
    from services.lenses.versions import new_version

    build(lake)
    folder = lens(lake)
    before = (folder / "fit" / "embed.npz").stat().st_mtime_ns
    record = new_version(folder, [2, 3, 4], ["manual"] * 3)
    assert record.version == "v2" and record.state == "draft"
    nodes = np.load(folder / "v2" / "assign.npz")["nodes"]
    assert [int(nodes[:, layer].max()) + 1 for layer in range(3)] == [2, 3, 4]
    assert json.loads((folder / "lens.json").read_text())["current"] == "v2"
    assert (folder / "fit" / "embed.npz").stat().st_mtime_ns == before


def test_saving_freezes_a_version_and_copies_its_records_into_the_repo(lake: Path, tmp_path: Path) -> None:
    from services.lenses.store import save_version

    build(lake)
    saved = save_version(SESSION, "synth", "v1", ["tank"])
    assert saved.state == "saved" and saved.keywords == ["tank"]
    copied = tmp_path / "records" / SESSION / "synth"
    assert (copied / "lens.json").exists() and (copied / "v1" / "version.json").exists()
    with pytest.raises(ValueError):
        save_version(SESSION, "synth", "v1", ["tank"])


def test_a_build_refuses_a_name_already_used(lake: Path) -> None:
    build(lake)
    with pytest.raises(FileExistsError):
        build(lake)


def test_k_is_chosen_by_hand_or_by_a_named_method() -> None:
    from services.lenses.versions import resolve_k

    found: Dict[str, Dict[str, object]] = {
        "0": {"elbow": 2, "silhouette": 3, "levels": [2, 5]},
        "1": {"elbow": 2, "silhouette": 4, "levels": []},
    }
    assert resolve_k([0, 1], found, k=5) == ([5, 5], ["manual", "manual"])
    assert resolve_k([0, 1], found, k_per_layer=[3, 7]) == ([3, 7], ["manual", "manual"])
    assert resolve_k([0, 1], found, k_auto="silhouette") == ([3, 4], ["auto:silhouette"] * 2)
    assert resolve_k([0, 1], found, k_auto="levels") == ([5, 4], ["auto:levels", "auto:silhouette (no clear level)"])
    with pytest.raises(ValueError):
        resolve_k([0, 1], found, k_per_layer=[3])
    with pytest.raises(ValueError):
        resolve_k([0, 1], found, k_auto="magic")


def test_items_follow_todays_filters(lake: Path) -> None:
    from services.lenses.data import LensFilters, load_items

    assert len(load_items(SESSION, LensFilters())) == 40
    assert {r.label for r in load_items(SESSION, LensFilters(labels=["a"]))} == {"a"}
    small = load_items(SESSION, LensFilters(max_items=10))
    larger = load_items(SESSION, LensFilters(max_items=12))
    assert len(small) == 10 and {r.probe_id for r in small} <= {r.probe_id for r in larger}


def test_members_follow_a_link_an_expert_link_and_the_output_column(lake: Path) -> None:
    from services.lenses.flows import members
    from services.lenses.view import open_lens

    build(lake)
    view = open_lens(SESSION, "synth")
    for i, item in enumerate(view.items):
        item["output_category"] = "yes" if i % 2 else "no"
    nodes, experts = view.nodes, view.experts[:, :, 0]
    a, b = int(nodes[0, 0]), int(nodes[0, 1])
    link = members(view, 0, node=a, to_node=b, limit=500)
    assert link["total"] == int(((nodes[:, 0] == a) & (nodes[:, 1] == b)).sum())
    e, f = int(experts[0, 0]), int(experts[0, 1])
    expert_link = members(view, 0, expert=e, to_expert=f, limit=500)
    assert expert_link["total"] == int(((experts[:, 0] == e) & (experts[:, 1] == f)).sum())
    assert members(view, 2, output="yes")["total"] == sum(i % 2 for i in range(len(view.items)))
    both = members(view, 2, node=int(nodes[1, 2]), output="yes", limit=500)
    assert all(item["output_category"] == "yes" for item in both["items"])
    with pytest.raises(ValueError):
        members(view, 0)


def test_the_output_column_groups_by_output_axes_and_counts_them(lake: Path) -> None:
    from services.lenses.flows import cluster_flows
    from services.lenses.view import open_lens

    build(lake)
    view = open_lens(SESSION, "synth")
    for i, item in enumerate(view.items):
        item["output_category"] = "go" if i % 2 else "stay"
        item["output_categories"] = {"move": item["output_category"], "fast": "yes" if i < 10 else "no"}
    plain = cluster_flows(view)["output"]
    assert plain["axes"] == {"fast": ["no", "yes"], "move": ["go", "stay"]}
    assert [(n["value"], n["count"]) for n in plain["nodes"]] == [("go", 20), ("stay", 20)]
    assert plain["nodes"][0]["output_counts"]["fast"] == {"no": 15, "yes": 5}
    grouped = cluster_flows(view, ["move", "fast"])["output"]
    assert {n["value"]: n["count"] for n in grouped["nodes"]} == {
        "go_no": 15, "go_yes": 5, "stay_no": 15, "stay_yes": 5}
    assert sum(link["count"] for link in grouped["links"]) == 40
    for i, item in enumerate(view.items[:10]):  # combinations nobody takes still get a node
        item["output_categories"]["fast"] = "yes" if i % 2 == 0 else "no"
    regrouped = cluster_flows(view, ["move", "fast"])["output"]["nodes"]
    assert {n["value"]: n["count"] for n in regrouped} == {"go_no": 20, "go_yes": 0, "stay_no": 15, "stay_yes": 5}
