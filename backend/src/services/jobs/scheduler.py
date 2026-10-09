"""Start queued jobs as their lanes free up, and watch the worker processes.

The backend ticks the scheduler once a second. Each tick:
1. marks a job whose worker exited without recording an end as interrupted (or cancelled, when a
   cancel was asked for), and removes the temporary outputs an unfinished job left behind;
2. force-kills a cancelled job whose process group outlived the grace period;
3. starts queued jobs, oldest first, while their lane has a free slot.

Jobs outlive a backend restart. On start, `adopt` takes over every worker still alive (the same
pid, running the worker on its job's folder) and marks the rest interrupted. A worker runs in its
own session, so a cancel ends its whole process group, children included.
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

import psutil

from services.jobs.kinds import KINDS, LANES
from services.jobs.store import ACTIVE_STATES, Job, JobStore, ProcRecord, now_iso

logger = logging.getLogger(__name__)

SRC_DIR = Path(__file__).resolve().parents[2]  # scheduler.py → jobs/ → services/ → src/

# One thread each for BLAS and numba inside a worker: lens builds spread layers over processes
# instead, which keeps results identical whatever the number of workers.
_THREAD_PINS = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMBA_NUM_THREADS": "1",
    "PYTHONUNBUFFERED": "1",
}


@dataclass
class _Running:
    lane: str
    process: Union["subprocess.Popen[bytes]", psutil.Process]

    def alive(self) -> bool:
        if isinstance(self.process, subprocess.Popen):
            return self.process.poll() is None
        try:
            return bool(self.process.is_running()) and self.process.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False


class JobScheduler:
    """Runs the store's jobs: lanes, process watching, cancels and restarts."""

    def __init__(
        self,
        store: JobStore,
        lanes: Optional[Mapping[str, int]] = None,
        python: str = sys.executable,
        kill_after: float = 5.0,
    ) -> None:
        self.store = store
        self.lanes = dict(lanes or LANES)
        self.python = python
        self.kill_after = kill_after
        self._running: Dict[str, _Running] = {}
        self._lock = threading.Lock()

    def submit(self, kind: str, params: Dict[str, Any], created_by: str) -> Job:
        """Queue a job; it starts on a later tick. Returns at once."""
        if kind not in KINDS:
            raise KeyError(f"unknown job kind: {kind!r}")
        with self._lock:
            return self.store.submit(kind, KINDS[kind].lane, params, created_by)

    def adopt(self) -> None:
        """Take over the workers a previous backend left running; mark the rest interrupted."""
        with self._lock:
            for job in self.store.list():
                if job.state not in ACTIVE_STATES or job.id in self._running:
                    continue
                record = self.store.proc(job.id)
                if record is None:
                    if job.state == "running":
                        self._finish(job.id, cancelled=False)
                    continue
                process = self._same_process(job.id, record)
                if process is not None:
                    self._running[job.id] = _Running(job.lane, process)
                    logger.info("Re-adopted job %s (pid %d)", job.id, record.pid)
                else:
                    self._finish(job.id, cancelled=record.cancel_requested_at is not None)

    def tick(self) -> None:
        """Reap finished workers, enforce cancels, then start what the lanes allow."""
        with self._lock:
            for job_id, running in list(self._running.items()):
                if running.alive():
                    continue
                del self._running[job_id]
                record = self.store.proc(job_id)
                cancelled = self.store.cancel_flag(job_id).exists() or (
                    record is not None and record.cancel_requested_at is not None)
                self._finish(job_id, cancelled=cancelled)
            for job_id in list(self._running):
                record = self.store.proc(job_id)
                if (record is not None and record.cancel_requested_at is not None
                        and time.time() - record.cancel_requested_at > self.kill_after):
                    self._signal_group(job_id, record, signal.SIGKILL)
            busy: Dict[str, int] = {}
            for running in self._running.values():
                busy[running.lane] = busy.get(running.lane, 0) + 1
            for job in self.store.list():
                if job.state != "queued" or job.id in self._running:
                    continue
                if busy.get(job.lane, 0) >= self.lanes.get(job.lane, 1):
                    continue
                self._start(job)
                busy[job.lane] = busy.get(job.lane, 0) + 1

    def cancel(self, job_id: str) -> Job:
        """Cancel a queued job at once; ask a running one to stop, then end its process group."""
        with self._lock:
            job = self.store.load(job_id)
            if job.state == "queued" and job_id not in self._running:
                return self.store.update(job_id, state="cancelled", finished_at=now_iso())
            if job.state not in ACTIVE_STATES and job_id not in self._running:
                return job
            self.store.cancel_flag(job_id).touch()
            record = self.store.proc(job_id)
            if record is not None:
                record.cancel_requested_at = time.time()
                self.store.save_proc(job_id, record)
                self._signal_group(job_id, record, signal.SIGTERM)
            return self.store.load(job_id)

    async def run(self, interval: float = 1.0) -> None:
        """Tick forever; the backend starts this as a task in its lifespan."""
        while True:
            try:
                self.tick()
            except Exception:
                logger.exception("Job scheduler tick failed")
            await asyncio.sleep(interval)

    def _start(self, job: Job) -> None:
        job_dir = self.store.job_dir(job.id)
        env = dict(os.environ)
        env.update(_THREAD_PINS)
        with open(self.store.log_path(job.id), "ab") as log:
            process = subprocess.Popen(
                [self.python, "-m", "services.jobs.worker", str(job_dir)],
                cwd=SRC_DIR, env=env, stdout=log, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL, start_new_session=True,
            )
        try:
            create_time = float(psutil.Process(process.pid).create_time())
        except psutil.NoSuchProcess:
            create_time = 0.0
        self.store.save_proc(job.id, ProcRecord(pid=process.pid, create_time=create_time))
        self._running[job.id] = _Running(job.lane, process)
        logger.info("Started job %s (%s, pid %d)", job.id, job.kind, process.pid)

    def _finish(self, job_id: str, cancelled: bool) -> None:
        """Record the end of a job whose worker is gone, unless the worker recorded it itself."""
        job = self.store.load(job_id)
        if job.state in ACTIVE_STATES:
            job = self.store.update(job_id, state="cancelled" if cancelled else "interrupted",
                                    finished_at=now_iso())
        if job.state in ("cancelled", "interrupted", "failed"):
            for raw in job.temp_paths:
                path = Path(raw)
                if ".tmp-" in path.name and path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
        self.store.clear_proc(job_id)

    def _same_process(self, job_id: str, record: ProcRecord) -> Optional[psutil.Process]:
        """The live worker a record names, or None once its pid is gone or reused. A worker is known
        by its command line, which ends with its job's folder: the start time psutil reports is the
        boot time plus ticks, and the boot time moves when the clock is stepped (WSL2 steps it by
        seconds under load), so it can't tell a worker from a stranger across a restart."""
        try:
            process = psutil.Process(record.pid)
            if process.status() == psutil.STATUS_ZOMBIE:
                return None
            args = process.cmdline()
            if not args or Path(args[-1]).resolve() != self.store.job_dir(job_id).resolve():
                return None
            return process
        except psutil.Error:  # gone, a zombie, or another user's process
            return None

    def _signal_group(self, job_id: str, record: ProcRecord, sig: int) -> None:
        """Signal a worker's whole process group, after checking the pid is still that worker."""
        if self._same_process(job_id, record) is None:
            return
        try:
            os.killpg(record.pid, sig)
        except (ProcessLookupError, PermissionError):
            pass
