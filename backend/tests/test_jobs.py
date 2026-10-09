"""Background jobs run in their own processes, one per lane slot, and can be cancelled.

These tests start real worker processes running the built-in `noop` job, so they need no model,
GPU or data. Each test uses its own job folder under pytest's tmp_path.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Iterator

import psutil
import pytest

from services.jobs.scheduler import JobScheduler
from services.jobs.store import Job, JobStore, ProcRecord


@pytest.fixture
def scheduler(tmp_path: Path) -> Iterator[JobScheduler]:
    sched = JobScheduler(JobStore(tmp_path / "jobs"), kill_after=1.0)
    yield sched
    for job in sched.store.list():  # leave no worker behind
        record = sched.store.proc(job.id)
        if record is not None:
            try:
                os.killpg(record.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass


def wait_until(sched: JobScheduler, ok: Callable[[], bool], timeout: float = 20.0) -> None:
    end = time.time() + timeout
    while time.time() < end:
        sched.tick()
        if ok():
            return
        time.sleep(0.1)
    raise AssertionError("timed out waiting")


def state(sched: JobScheduler, job: Job) -> str:
    return sched.store.load(job.id).state


def test_a_job_runs_and_records_its_result(scheduler: JobScheduler) -> None:
    job = scheduler.submit("noop", {"seconds": 0.2, "steps": 2}, created_by="test")
    assert state(scheduler, job) == "queued"
    wait_until(scheduler, lambda: state(scheduler, job) == "done")
    done = scheduler.store.load(job.id)
    assert done.result == {"waited": 0.2}
    assert (done.progress.stage, done.progress.done, done.progress.total) == ("done", 2, 2)
    assert done.started_at and done.finished_at
    wait_until(scheduler, lambda: scheduler.store.proc(job.id) is None)  # cleared once reaped


def test_a_lane_runs_one_job_at_a_time_and_lanes_are_independent(scheduler: JobScheduler) -> None:
    first = scheduler.submit("noop", {"seconds": 2}, created_by="test")
    second = scheduler.submit("noop", {"seconds": 0.1}, created_by="test")
    other_lane = scheduler.submit("noop_llm", {"seconds": 0.1}, created_by="test")
    scheduler.tick()
    assert scheduler.store.proc(first.id) is not None
    assert scheduler.store.proc(second.id) is None and state(scheduler, second) == "queued"
    assert scheduler.store.proc(other_lane.id) is not None  # the llm lane has its own slot
    wait_until(scheduler, lambda: state(scheduler, second) == "done")
    assert state(scheduler, first) == "done"


def test_a_failure_records_its_message_and_keeps_the_traceback_in_the_log(scheduler: JobScheduler) -> None:
    job = scheduler.submit("noop", {"fail": "boom"}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, job) == "failed")
    assert scheduler.store.load(job.id).error == "RuntimeError: boom"
    assert "RuntimeError: boom" in scheduler.store.log_tail(job.id)


def test_cancel_ends_the_whole_process_group(scheduler: JobScheduler) -> None:
    job = scheduler.submit("noop", {"seconds": 60, "steps": 600, "spawn_child": True}, created_by="test")
    child_file = scheduler.store.job_dir(job.id) / "child.pid"
    # the pid written, not just the file made (the two are separate steps)
    wait_until(scheduler, lambda: child_file.exists() and child_file.read_text().strip() != "")
    child = int(child_file.read_text())
    assert psutil.pid_exists(child)
    scheduler.cancel(job.id)
    wait_until(scheduler, lambda: state(scheduler, job) == "cancelled")
    wait_until(scheduler, lambda: not psutil.pid_exists(child)
               or psutil.Process(child).status() == psutil.STATUS_ZOMBIE)


def test_a_queued_job_is_cancelled_at_once(scheduler: JobScheduler) -> None:
    blocker = scheduler.submit("noop", {"seconds": 5}, created_by="test")
    queued = scheduler.submit("noop", {"seconds": 0.1}, created_by="test")
    scheduler.tick()
    assert scheduler.cancel(queued.id).state == "cancelled"
    scheduler.cancel(blocker.id)
    wait_until(scheduler, lambda: state(scheduler, blocker) == "cancelled")


def test_a_worker_that_dies_without_an_end_is_marked_interrupted(scheduler: JobScheduler) -> None:
    job = scheduler.submit("noop", {"seconds": 60, "steps": 600}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, job) == "running")
    record = scheduler.store.proc(job.id)
    assert record is not None
    os.kill(record.pid, signal.SIGKILL)
    wait_until(scheduler, lambda: state(scheduler, job) == "interrupted")
    assert scheduler.store.load(job.id).finished_at


def test_a_new_scheduler_re_adopts_a_live_worker(scheduler: JobScheduler) -> None:
    job = scheduler.submit("noop", {"seconds": 3, "steps": 30}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, job) == "running")
    restarted = JobScheduler(scheduler.store, kill_after=1.0)  # the backend after a restart
    restarted.adopt()
    later = restarted.submit("noop", {"seconds": 0.1}, created_by="test")
    restarted.tick()
    assert state(restarted, later) == "queued"  # the adopted worker still holds the cpu slot
    wait_until(restarted, lambda: state(restarted, job) == "done")
    wait_until(restarted, lambda: state(restarted, later) == "done")


def test_a_live_worker_is_re_adopted_after_the_clock_moves(scheduler: JobScheduler) -> None:
    # WSL2 steps its clock under load, which moves the start time psutil reports for a process
    # (the boot time plus ticks) by seconds; the live worker is still the job's after a restart
    job = scheduler.submit("noop", {"seconds": 3, "steps": 30}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, job) == "running")
    record = scheduler.store.proc(job.id)
    assert record is not None
    record.create_time -= 5.0
    scheduler.store.save_proc(job.id, record)
    restarted = JobScheduler(scheduler.store, kill_after=1.0)
    restarted.adopt()
    assert state(restarted, job) == "running"
    wait_until(restarted, lambda: state(restarted, job) == "done")


def test_a_reused_pid_is_not_taken_for_the_worker(scheduler: JobScheduler) -> None:
    # A live process that isn't the job's worker, even with the recorded start time
    stranger = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"], start_new_session=True)
    try:
        job = scheduler.submit("noop", {"seconds": 0.1}, created_by="test")
        scheduler.store.update(job.id, state="running")
        scheduler.store.save_proc(job.id, ProcRecord(pid=stranger.pid,
                                                     create_time=psutil.Process(stranger.pid).create_time()))
        restarted = JobScheduler(scheduler.store, kill_after=1.0)
        restarted.adopt()
        assert state(restarted, job) == "interrupted"
        assert stranger.poll() is None  # and it is left alone
    finally:
        stranger.kill()
        stranger.wait()


def test_an_interrupted_job_leaves_no_temporary_output(scheduler: JobScheduler, tmp_path: Path) -> None:
    leftover = tmp_path / "lens.tmp-x"
    leftover.mkdir()
    (leftover / "part.npz").write_text("partial")
    job = scheduler.submit("noop", {"seconds": 60, "steps": 600}, created_by="test")
    scheduler.store.update(job.id, temp_paths=[str(leftover)])
    wait_until(scheduler, lambda: state(scheduler, job) == "running")
    record = scheduler.store.proc(job.id)
    assert record is not None
    os.kill(record.pid, signal.SIGKILL)
    wait_until(scheduler, lambda: state(scheduler, job) == "interrupted")
    assert not leftover.exists()


def test_submitting_returns_at_once_while_a_cpu_job_runs(scheduler: JobScheduler) -> None:
    busy = scheduler.submit("noop", {"seconds": 3, "busy": True}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, busy) == "running")
    start = time.perf_counter()
    scheduler.submit("noop", {"seconds": 0.1}, created_by="test")
    assert time.perf_counter() - start < 1.0
    scheduler.cancel(busy.id)


def test_the_api_lists_reads_and_cancels_jobs(scheduler: JobScheduler) -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from api.routers import jobs

    app = FastAPI()
    app.include_router(jobs.router, prefix="/api")
    app.state.jobs = scheduler
    client = TestClient(app)

    failing = scheduler.submit("noop", {"fail": "boom"}, created_by="test")
    wait_until(scheduler, lambda: state(scheduler, failing) == "failed")
    queued = scheduler.submit("noop", {"seconds": 0.1}, created_by="test")

    listed = client.get("/api/jobs").json()
    assert [j["id"] for j in listed] == [queued.id, failing.id]  # newest first
    assert [j["id"] for j in client.get("/api/jobs?active=true").json()] == [queued.id]
    read = client.get(f"/api/jobs/{failing.id}").json()
    assert read["state"] == "failed" and "RuntimeError: boom" in read["log_tail"]
    assert client.post(f"/api/jobs/{queued.id}/cancel").json()["state"] == "cancelled"
    assert client.get("/api/jobs/job_20260101T000000000000_abcdef").status_code == 404
    assert client.get("/api/jobs/..%2Fsecrets").status_code == 404
