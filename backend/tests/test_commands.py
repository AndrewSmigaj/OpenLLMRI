"""The command interface and the app's event stream: `show` reaches the open apps, `build` queues a
lens job at once, every command is logged, events cross threads, and job changes are announced."""

import asyncio
import threading
from pathlib import Path
from typing import Any, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from test_lenses import SESSION, make_capture

from api import config
from api.app_events import AppEvents, stream, watch_jobs
from api.routers import commands, jobs, lenses
from services.jobs.scheduler import JobScheduler
from services.jobs.store import JobStore


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(config, "DATA_LAKE_PATH", tmp_path / "lake")
    monkeypatch.setattr(config, "LENS_RECORDS_PATH", tmp_path / "records")
    make_capture(tmp_path / "lake")
    app = FastAPI()
    for module in (jobs, lenses, commands):
        app.include_router(module.router, prefix="/api")
    app.state.jobs = JobScheduler(JobStore(tmp_path / "lake" / "_jobs"))
    app.state.events = AppEvents()
    return TestClient(app)


def test_show_reaches_the_open_apps_and_build_queues_a_job(client: TestClient) -> None:
    async def heard() -> List[Any]:
        events: AppEvents = client.app.state.events  # type: ignore[attr-defined]
        queue = events.subscribe()
        sent = client.post("/api/commands", json={"verb": "show", "by": "test",
                                                  "view": {"session": SESSION, "lens": "synth", "layer": 4}})
        assert sent.status_code == 200 and sent.json()["delivered"] == 1
        return [await asyncio.wait_for(queue.get(), 1)]
    (kind, data), = asyncio.run(heard())
    assert kind == "show" and data == {"view": {"session": SESSION, "lens": "synth", "layer": 4}, "by": "test"}
    assert client.post("/api/commands", json={"verb": "show", "view": {"lens": "x"}}).status_code == 400
    assert client.post("/api/commands", json={"verb": "show", "view": {"session": SESSION, "colour": "x"}}).status_code == 400
    build = {"session_id": SESSION, "name": "from-command", "k": 2, "n_neighbors": 10, "workers": 1}
    started = client.post("/api/commands", json={"verb": "build", "lens": build, "by": "mud:Ada"})
    assert started.status_code == 202
    job = client.get(f"/api/jobs/{started.json()['job_id']}").json()
    assert job["kind"] == "lens_build" and job["state"] == "queued" and job["created_by"] == "mud:Ada"
    assert client.post("/api/commands", json={"verb": "build", "lens": build}).status_code == 409  # already building
    assert client.post("/api/commands", json={"verb": "build", "lens": {"name": "x"}}).status_code == 422
    log = client.get("/api/commands").json()
    assert [entry["verb"] for entry in log] == ["show", "build", "build"]  # refusals before validation aren't logged
    assert log[1]["result"]["job_id"] == started.json()["job_id"] and "error" in log[2]["result"]


class _Request:
    """A request that disconnects after a few checks."""

    def __init__(self, checks: int) -> None:
        self.checks = checks

    async def is_disconnected(self) -> bool:
        self.checks -= 1
        return self.checks < 0


def test_the_stream_sends_events_published_from_any_thread() -> None:
    async def read() -> List[str]:
        events = AppEvents()
        lines = stream(events, _Request(checks=2))
        out = [await lines.__anext__()]  # the reconnect delay, and the app is subscribed
        threading.Thread(target=events.publish, args=("lens", {"name": "synth"})).start()
        out.append(await asyncio.wait_for(lines.__anext__(), 2))
        await lines.aclose()
        assert events.listeners == 0  # closing the stream unsubscribes the app
        return out
    first, event = asyncio.run(read())
    assert first.startswith("retry:") and event == 'event: lens\ndata: {"name": "synth"}\n\n'


def test_job_changes_are_announced_and_a_finished_lens_build_announces_its_lens(tmp_path: Path) -> None:
    store = JobStore(tmp_path / "_jobs")
    old = store.submit("lens_build", "cpu", {"session_id": SESSION, "name": "old"}, created_by="test")
    store.update(old.id, state="done")

    async def watch() -> List[Any]:
        events = AppEvents()
        queue = events.subscribe()
        task = asyncio.create_task(watch_jobs(SimpleScheduler(store), events, interval=0.01))
        await asyncio.sleep(0.05)
        job = store.submit("lens_build", "cpu", {"session_id": SESSION, "name": "new"}, created_by="test")
        await asyncio.sleep(0.05)
        store.update(job.id, state="done")
        await asyncio.sleep(0.05)
        task.cancel()
        heard = []
        while not queue.empty():
            heard.append(queue.get_nowait())
        return heard
    heard = asyncio.run(watch())
    assert [kind for kind, _ in heard] == ["job", "job", "lens"]  # the job ended before the start isn't announced
    assert heard[0][1]["state"] == "queued" and heard[1][1]["state"] == "done"
    assert heard[2][1] == {"session_id": SESSION, "name": "new", "change": "lens_build"}


class SimpleScheduler:
    def __init__(self, store: JobStore) -> None:
        self.store = store
