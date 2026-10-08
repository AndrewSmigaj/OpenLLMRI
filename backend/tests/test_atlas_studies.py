"""Atlas v1 and study files: a saved version's node entries are written beside its records, read
back by GET /api/atlas/nodes and narrowed by its filters; study files load, report references that
don't resolve, and show a broken file's error; the repo's own studies load."""

from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from test_lens_api import BODY, run_job
from test_lenses import SESSION, make_capture

from api import config
from api.routers import atlas, jobs, lenses, studies
from services.jobs.scheduler import JobScheduler
from services.jobs.store import JobStore


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(config, "DATA_LAKE_PATH", tmp_path / "lake")
    monkeypatch.setattr(config, "LENS_RECORDS_PATH", tmp_path / "records")
    make_capture(tmp_path / "lake")
    app = FastAPI()
    for module in (jobs, lenses, atlas, studies):
        app.include_router(module.router, prefix="/api")
    app.state.jobs = JobScheduler(JobStore(tmp_path / "lake" / "_jobs"))
    built = TestClient(app)
    run_job(built, built.post("/api/lenses", json=BODY).json()["job_id"])
    return built


def test_a_saved_version_joins_the_atlas_node_by_node(client: TestClient, tmp_path: Path) -> None:
    base = f"/api/sessions/{SESSION}/lenses/synth"
    assert client.post(f"/api/atlas/nodes/{SESSION}/synth/v1").status_code == 400  # a draft isn't in the atlas
    saved = client.post(f"{base}/save", json={"version": "v1", "keywords": ["tank"], "analysis_budget": 0})
    assert saved.status_code == 200 and "analysis_job_id" not in saved.json()
    assert (tmp_path / "records" / SESSION / "synth" / "v1" / "nodes.json").exists()
    entries = client.get("/api/atlas/nodes").json()
    assert {e["layer"] for e in entries} == {0, 1, 2}
    for layer in (0, 1, 2):
        assert sum(e["items"] for e in entries if e["layer"] == layer) == 40  # every item in one node
    one = client.get("/api/atlas/nodes", params={"layer": 1, "lens": "synth"}).json()
    assert len(one) == 2 and all(e["majority"]["share"] == 1.0 for e in one)  # the two classes, apart
    assert one[0]["from"] and one[0]["to"] and one[0]["experts"] and one[0]["report"] is None
    assert client.get("/api/atlas/nodes", params={"validated": True}).json() == []  # not validated yet
    assert len(client.get("/api/atlas/nodes", params={"q": "b"}).json()) == 3  # the label-b node at each layer


GOOD = """id: probe_one
title: A study
question: Does it work?
started: 2026-10-08
sets: [tank_polysemy_v3, no_such_set]
captures: [session_test, session_gone]
lenses: [session_test/synth@v1, session_test/synth@v9]
findings: [docs/DESIGN.md]
ledger:
  - idea: It works.
    experiment: Try it.
    finding: It works.
    evidence: [docs/nowhere.md]
"""


def test_studies_load_name_what_doesnt_resolve_and_show_a_broken_file(client: Any, tmp_path: Path,
                                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    import services.studies as module

    root = tmp_path / "studies"
    (root / "probe_one").mkdir(parents=True)
    (root / "probe_one" / "study.yaml").write_text(GOOD.replace("session_test", SESSION))
    (root / "misnamed").mkdir()
    (root / "misnamed" / "study.yaml").write_text("id: other\ntitle: t\nquestion: q\n")
    (root / "typo").mkdir()
    (root / "typo" / "study.yaml").write_text("id: typo\ntitle: t\nquestion: q\nlense: []\n")
    (root / "notes_only").mkdir()  # a study folder without a study file isn't listed
    monkeypatch.setattr(module, "studies_root", lambda: root)
    listed = {s["id"]: s for s in client.get("/api/studies").json()}
    assert set(listed) == {"probe_one", "misnamed", "typo"}
    assert sorted(listed["probe_one"]["problems"]) == sorted([
        "no set no_such_set", "no capture session_gone in the lake", f"no lens {SESSION}/synth@v9",
        "no file docs/nowhere.md"])
    assert listed["probe_one"]["ledger"][0]["status"] == "proposed" and listed["probe_one"]["started"] == "2026-10-08"
    assert "folder's name" in listed["misnamed"]["error"] and "lense" in listed["typo"]["error"]
    assert client.get("/api/studies/probe_one").json()["title"] == "A study"
    assert client.get("/api/studies/nothing").status_code == 404


def test_the_repos_studies_load() -> None:
    from services.studies import load_study, studies_root

    folders = [f for f in studies_root().iterdir() if (f / "study.yaml").exists()]
    assert folders and all(load_study(f).id == f.name for f in folders)
