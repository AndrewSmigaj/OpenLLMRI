"""The backend without the model (LOAD_MODEL=0): the stage reads skipped, routes that need the model
answer 503 and say why (with the app's CORS headers), the capture list and session details work
from the lake's session files, and JOB_WORKERS sets how many workers a job uses."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from api import config
from api import dependencies as deps
from api.routers import probes
from services.jobs.workers import default_workers

APP_ORIGIN = "http://localhost:5173"


@pytest.fixture
def no_model(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A backend state with LOAD_MODEL off, no capture service, and a lake in tmp_path."""
    lake = tmp_path / "lake"
    monkeypatch.setattr(config, "LOAD_MODEL", False)
    monkeypatch.setattr(config, "DATA_LAKE_PATH", lake)
    monkeypatch.setattr(deps, "_capture_service", None)
    monkeypatch.setattr(deps, "_reader", None)
    monkeypatch.setattr(deps, "_loading_stage", "not_started")
    monkeypatch.setattr(deps, "_loading_error", None)
    return lake


def _write_session(lake: Path, sid: str, state: str = "completed") -> None:
    meta = {"session_id": sid, "session_name": f"name of {sid}", "created_at": "2026-10-16T00:00:00",
            "total_pairs": 4, "completed_pairs": 4, "state": state}
    (lake / "_sessions").mkdir(parents=True, exist_ok=True)
    (lake / "_sessions" / f"{sid}.json").write_text(json.dumps(meta))
    (lake / sid).mkdir(exist_ok=True)


async def test_with_load_model_off_the_stage_reads_skipped_and_no_loader_starts(
        no_model: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse() -> None:
        raise AssertionError("the model loader started")
    monkeypatch.setattr(deps, "_load_model_sync", refuse)
    await deps.initialize_capture_service()
    assert deps.get_loading_status()["stage"] == "skipped"
    assert not deps.is_model_loaded()


@pytest.mark.parametrize("stage, error, says", [
    ("skipped", None, "LOAD_MODEL=0"),
    ("loading_model", None, "still loading"),
    ("failed", "out of memory", "failed to load: out of memory"),
])
def test_a_route_that_needs_the_model_answers_503_saying_why_with_cors(
        no_model: Path, monkeypatch: pytest.MonkeyPatch, stage: str, error: str, says: str) -> None:
    monkeypatch.setattr(deps, "_loading_stage", stage)
    monkeypatch.setattr(deps, "_loading_error", error)
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=[APP_ORIGIN], allow_methods=["*"], allow_headers=["*"])

    @app.get("/needs-model")
    def needs_model(service: object = Depends(deps.get_capture_service)) -> dict:
        return {"ok": True}

    answer = TestClient(app).get("/needs-model", headers={"Origin": APP_ORIGIN})
    assert answer.status_code == 503
    assert says in answer.json()["detail"]
    assert answer.headers.get("access-control-allow-origin") == APP_ORIGIN


def test_the_capture_list_and_details_work_without_the_model(no_model: Path) -> None:
    _write_session(no_model, "session_done")
    _write_session(no_model, "session_broken", state="failed")
    app = FastAPI()
    app.include_router(probes.router, prefix="/api")
    client = TestClient(app)

    listed = client.get("/api/probes")
    assert listed.status_code == 200
    assert sorted(s["session_id"] for s in listed.json()) == ["session_broken", "session_done"]

    details = client.get("/api/probes/session_done")
    assert details.status_code == 200
    assert details.json()["manifest"]["session_name"] == "name of session_done"

    status = client.get("/api/probes/session_broken/status")
    assert status.status_code == 200 and status.json()["state"] == "failed"


def test_with_a_capture_service_the_session_store_is_its_own(no_model: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    own = object()
    monkeypatch.setattr(deps, "_capture_service", SimpleNamespace(session_mgr=own))
    assert deps.get_sessions() is own


def test_without_one_the_session_store_reads_the_lake_and_is_made_once(no_model: Path) -> None:
    first = deps.get_sessions()
    assert Path(first.data_lake_path) == no_model
    assert deps.get_sessions() is first


def test_job_workers_sets_the_default_number_of_workers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JOB_WORKERS", "2")
    assert default_workers() == 2
    monkeypatch.setenv("JOB_WORKERS", "0")
    assert default_workers() == 1
    monkeypatch.delenv("JOB_WORKERS")
    usual = default_workers()
    assert 1 <= usual <= 6
    monkeypatch.setenv("JOB_WORKERS", "two")
    assert default_workers() == usual


def test_the_503_is_an_http_exception(no_model: Path) -> None:
    deps._loading_stage = "skipped"
    with pytest.raises(HTTPException) as raised:
        deps.get_capture_service()
    assert raised.value.status_code == 503
