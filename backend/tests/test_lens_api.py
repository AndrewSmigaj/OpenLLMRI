"""The lens endpoints: start a build, open lenses and legacy schemas through one shape, read flows
and members, cut a new k, save a version."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from test_lenses import SESSION, make_capture

from api import config
from api.routers import jobs, lenses
from services.jobs.kinds import JobContext
from services.jobs.scheduler import JobScheduler
from services.jobs.store import JobStore


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(config, "DATA_LAKE_PATH", tmp_path / "lake")
    monkeypatch.setattr(config, "LENS_RECORDS_PATH", tmp_path / "records")
    make_capture(tmp_path / "lake")
    app = FastAPI()
    app.include_router(jobs.router, prefix="/api")
    app.include_router(lenses.router, prefix="/api")
    app.state.jobs = JobScheduler(JobStore(tmp_path / "lake" / "_jobs"))
    return TestClient(app)


def run_job(client: TestClient, job_id: str) -> Dict[str, Any]:
    """Run a submitted build here, as the worker would (a worker process wouldn't see tmp_path)."""
    from services.lenses.build import build_lens

    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    return build_lens(store.load(job_id).params, JobContext(store, job_id))


BODY = {"session_id": SESSION, "name": "synth", "n_neighbors": 10, "k": 2, "workers": 1}


def test_a_build_starts_as_a_job_and_the_lens_then_opens(client: TestClient) -> None:
    started = client.post("/api/lenses", json=BODY)
    assert started.status_code == 202
    job_id = started.json()["job_id"]
    assert client.post("/api/lenses", json=BODY).status_code == 409  # already being built
    run_job(client, job_id)
    listed = client.get(f"/api/sessions/{SESSION}/lenses").json()
    assert [(item["name"], item["legacy"], item["current"]) for item in listed] == [("synth", False, "v1")]
    assert client.post("/api/lenses", json=BODY).status_code == 409  # the name is taken
    flows = client.get(f"/api/sessions/{SESSION}/lenses/synth/flows").json()
    assert len(flows["nodes"]) == 6 and flows["axes"]["label"] == ["a", "b"]
    assert flows["recipe"]["lens"] == {"session_id": SESSION, "name": "synth", "legacy": False, "version": "v1"}
    assert len(client.get(f"/api/sessions/{SESSION}/lenses/synth/expert-flows?rank=4").json()["nodes"]) > 0
    assert client.get(f"/api/sessions/{SESSION}/lenses/synth/expert-flows?rank=5").status_code == 400
    page = client.get(f"/api/sessions/{SESSION}/lenses/synth/members?layer=0&node=0&limit=5").json()
    assert page["total"] == 20 and len(page["items"]) == 5


def test_a_new_k_and_a_save(client: TestClient) -> None:
    run_job(client, client.post("/api/lenses", json=BODY).json()["job_id"])
    made = client.post(f"/api/sessions/{SESSION}/lenses/synth/versions", json={"k": 3}).json()
    assert made["version"] == "v2" and made["k_per_layer"] == [3, 3, 3]
    saved = client.post(f"/api/sessions/{SESSION}/lenses/synth/save", json={"version": "v2", "keywords": ["tank"]})
    assert saved.json()["state"] == "saved"
    again = client.post(f"/api/sessions/{SESSION}/lenses/synth/save", json={"version": "v2"})
    assert again.status_code == 400


def test_a_legacy_schema_opens_through_the_same_shapes(client: TestClient, tmp_path: Path) -> None:
    folder = tmp_path / "lake" / SESSION / "clusterings" / "old_k2"
    folder.mkdir(parents=True)
    ids = [f"p{i:03d}" for i in range(40)]
    assignments = {pid: {str(layer): i % 2 for layer in range(3)} for i, pid in enumerate(ids)}
    (folder / "probe_assignments.json").write_text(json.dumps(assignments))
    (folder / "meta.json").write_text(json.dumps({"sample_size": 40, "params": {"n_neighbors": 15}}))
    listed = client.get(f"/api/sessions/{SESSION}/lenses").json()
    assert [(item["name"], item["legacy"]) for item in listed] == [("old_k2", True)]
    flows = client.get(f"/api/sessions/{SESSION}/lenses/old_k2/flows?legacy=true").json()
    assert sum(n["count"] for n in flows["nodes"] if n["layer"] == 0) == 40
    assert flows["recipe"]["lens"]["legacy"] is True


def test_errors_name_what_is_missing(client: TestClient) -> None:
    assert client.get("/api/sessions/session_nothere/lenses").status_code == 404
    assert client.get(f"/api/sessions/{SESSION}/lenses/nothing/flows").status_code == 404
    assert client.post("/api/lenses", json=BODY | {"name": "Bad Name"}).status_code == 400
    assert client.post("/api/lenses", json=BODY | {"session_id": "session_nothere"}).status_code == 404
