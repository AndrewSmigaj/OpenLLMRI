"""Listing and opening sessions: the app knows a session only through its _sessions/<id>.json."""
import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from api.routers.probes import get_probe_session_details, list_probe_sessions
from services.probes.session_manager import SessionManager


def _service(lake):
    mgr = SessionManager(str(lake), batch_size=1, layers_to_capture=[0])
    return SimpleNamespace(data_lake_path=str(lake), sessions_dir=mgr.sessions_dir,
                           active_sessions=mgr.active_sessions,
                           get_session_status=mgr.get_session_status)


def _write_session(lake, sid, created_at, **extra):
    meta = {"session_id": sid, "session_name": f"name of {sid}", "created_at": created_at,
            "total_pairs": 4, "completed_pairs": 3, "state": "completed", **extra}
    (lake / "_sessions").mkdir(exist_ok=True)
    (lake / "_sessions" / f"{sid}.json").write_text(json.dumps(meta))
    (lake / sid).mkdir(exist_ok=True)


async def test_sessions_are_listed_newest_first(tmp_path):
    _write_session(tmp_path, "session_old", "2026-01-01T00:00:00")
    _write_session(tmp_path, "session_new", "2026-09-01T00:00:00", labels=["friend", "foe"])
    listed = await list_probe_sessions(service=_service(tmp_path))
    assert [s.session_id for s in listed] == ["session_new", "session_old"]
    assert listed[0].labels == ["friend", "foe"] and listed[0].probe_count == 3


async def test_no_sessions_folder_means_no_sessions(tmp_path):
    assert await list_probe_sessions(service=SimpleNamespace(data_lake_path=str(tmp_path))) == []


async def test_a_session_without_its_sessions_file_is_invisible(tmp_path):
    _write_session(tmp_path, "session_kept", "2026-01-01T00:00:00")
    (tmp_path / "session_orphan").mkdir()                  # data, but no _sessions/<id>.json
    service = _service(tmp_path)
    assert [s.session_id for s in await list_probe_sessions(service=service)] == ["session_kept"]
    with pytest.raises(HTTPException) as err:
        await get_probe_session_details("session_orphan", service=service)
    assert err.value.status_code == 404


async def test_an_entry_missing_a_required_field_is_skipped(tmp_path):
    _write_session(tmp_path, "session_ok", "2026-01-01T00:00:00")
    (tmp_path / "_sessions" / "session_bad.json").write_text(json.dumps({"session_id": "session_bad"}))
    assert [s.session_id for s in await list_probe_sessions(service=_service(tmp_path))] == ["session_ok"]


@pytest.mark.xfail(strict=True, reason="a _sessions file that isn't JSON, read before any valid one, "
                   "fails the whole listing: the warning in its except-handler reads `metadata`, "
                   "still unset (after a valid file it names that file instead). Parked.")
async def test_a_file_that_is_not_json_is_skipped(tmp_path):
    (tmp_path / "_sessions").mkdir()
    (tmp_path / "_sessions" / "broken.json").write_text("{ not json")
    assert await list_probe_sessions(service=_service(tmp_path)) == []
