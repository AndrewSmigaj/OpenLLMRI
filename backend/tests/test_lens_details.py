"""Node details, with a fake unembedding, tokenizer and router: neurons, the logit lens, the surface
check, the routing effect and router alignment, and the details job through the API."""

from typing import Any, Dict, Iterator, Tuple

import numpy as np
import pytest
from fastapi.testclient import TestClient
from test_lens_api import BODY, client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.details import (
    logit_lens,
    node_neurons,
    router_alignment,
    routing_effect,
    surface_check,
    surface_features,
)


class FakeWeights:
    """A tiny model: hidden size 64, 100 tokens, 32 experts per router."""

    def __init__(self) -> None:
        rng = np.random.default_rng(0)
        self.eps = 1e-5
        self.unembedding = rng.normal(size=(100, 64)).astype(np.float32)
        self.routers = {layer: rng.normal(size=(32, 64)).astype(np.float32) for layer in range(4)}

    def final_norm(self) -> Any:
        return np.ones(64, dtype=np.float32)

    def unembedding_chunks(self, rows: int = 30) -> Iterator[Tuple[int, Any]]:
        for start in range(0, 100, rows):
            yield start, self.unembedding[start:start + rows]

    def decoder(self) -> Any:
        return lambda token_id: f"tok{token_id}"

    def router(self, layer: int) -> Tuple[Any, Any]:
        return self.routers[layer], np.zeros(32, dtype=np.float32)

    def pre_router_norm(self, layer: int) -> Any:
        return np.ones(64, dtype=np.float32)


def test_a_planted_neuron_is_found_for_its_node() -> None:
    rng = np.random.default_rng(1)
    nodes = np.arange(100) % 2
    states = rng.normal(size=(100, 50))
    states[nodes == 1, 7] += 3
    found = node_neurons(states, nodes)
    assert found[1][0][0] == 7 and found[1][0][1] > 0.7 and found[0][0] == (7, -found[1][0][1])


def test_the_logit_lens_reads_the_tokens_a_centre_favours() -> None:
    fake = FakeWeights()
    centre = fake.unembedding[42] * 5
    baseline = fake.unembedding.mean(axis=0, keepdims=True)
    ids, _, lift_ids, _ = logit_lens(centre[None, :], baseline, fake.final_norm(), fake.eps, fake.unembedding_chunks())
    assert ids[0][0] == 42 and lift_ids[0][0] == 42 and len(ids[0]) == 12


def test_an_axis_in_the_routers_row_space_aligns_and_one_outside_does_not() -> None:
    rng = np.random.default_rng(2)
    basis = rng.normal(size=(6, 64))
    router = rng.normal(size=(32, 6)) @ basis  # the router reads only a 6-dimensional subspace
    inside = basis[0] * 3
    q, _ = np.linalg.qr(basis.T)
    outside = rng.normal(size=64)
    outside -= q @ (q.T @ outside)  # orthogonal to everything the router reads
    gain = np.ones(64)
    assert router_alignment(inside, router, gain)["percentile"] > 95
    found = router_alignment(outside, router, gain)
    assert found["ratio"] < 0.05 and found["percentile"] == 0


def test_a_length_confound_is_flagged() -> None:
    rng = np.random.default_rng(3)
    nodes = np.arange(60) % 2
    items = [{"input_text": " ".join(["word"] * (int(rng.integers(18, 24)) if n else int(rng.integers(4, 8)))) + " tank",
              "target_word": "tank"} for n in nodes]
    numeric, first = surface_features(items)
    found = surface_check(numeric, first, nodes)
    assert found["nodes"][1]["flagged"] and found["nodes"][1]["feature"] in ("words", "characters")
    assert found["kappa"] is not None and found["kappa"] > 0.9


def test_the_routing_effect_tells_routing_nodes_from_indifferent_ones() -> None:
    rng = np.random.default_rng(4)
    nodes = np.arange(80) % 2
    routing = rng.random((80, 32)) * 0.1
    routing[nodes == 1, 5] += 1.0  # node 1 sends its items to expert 5
    strong, per = routing_effect(nodes, routing)
    weak, _ = routing_effect(rng.integers(0, 2, size=80), routing)
    assert strong > 0.8 and weak < 0.1 and per[1]["shift"] > per[0]["shift"] * 0.5


def _work_out(client: TestClient, base: str) -> Dict[str, Any]:  # noqa: F811
    from services.lenses.details import build_details

    started = client.post(f"{base}/details", json={})
    assert started.status_code == 202
    job_id = started.json()["job_id"]
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    build_details(store.load(job_id).params, JobContext(store, job_id))
    found: Dict[str, Any] = client.get(f"{base}/details").json()
    return found


def _listed(client: TestClient, name: str) -> Dict[str, Any]:  # noqa: F811
    lens: Dict[str, Any] = next(lens for lens in client.get(f"/api/sessions/{SESSION}/lenses").json() if lens["name"] == name)
    return lens


def test_the_details_job_writes_every_node(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F811
    import services.lenses.model_weights as weights

    monkeypatch.setattr(weights, "ModelWeights", FakeWeights)
    run_job(client, client.post("/api/lenses", json=BODY).json()["job_id"])
    base = f"/api/sessions/{SESSION}/lenses/synth"
    assert client.get(f"{base}/details").status_code == 404 and _listed(client, "synth")["details"] == []
    details = _work_out(client, base)
    node = details["layers"]["0"]["nodes"]["0"]
    assert set(node) == {"neurons", "surface", "routing", "logit_lens"}
    assert node["logit_lens"]["top"][0][0].startswith("tok") and details["layers"]["2"]["routing_effect"] is None
    assert _listed(client, "synth")["details"] == ["v1"]


def test_a_mass_mean_lens_gets_router_alignment_and_tokens(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F811
    import services.lenses.model_weights as weights
    from services.lenses.massmean import build_mass_mean

    monkeypatch.setattr(weights, "ModelWeights", FakeWeights)
    started = client.post("/api/lenses/mass-mean", json={"session_id": SESSION, "name": "ab-axis",
                                                          "label_a": "a", "label_b": "b"}).json()["job_id"]
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    build_mass_mean(store.load(started).params, JobContext(store, started))
    details = _work_out(client, f"/api/sessions/{SESSION}/lenses/ab-axis")
    assert details["kind"] == "mass_mean"
    assert set(details["layers"]["1"]["router_alignment"]) == {"ratio", "percentile", "random_95"}
    assert "router_alignment" not in details["layers"]["2"]  # no next layer
    assert len(details["layers"]["2"]["logit_lens"]["b_over_a"]) == 12
    assert _listed(client, "ab-axis")["details"] == ["mass_mean"]
