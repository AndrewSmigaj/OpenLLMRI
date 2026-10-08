"""Job records on disk: one folder per job under the lake's `_jobs/`.

A job's folder holds:
- `job.json`: what to run, its state, progress, result or error;
- `proc.json`: the process the scheduler started for it (pid and start time);
- `log.txt`: everything the worker printed, tracebacks included;
- `cancel`: a flag file, present once a cancel was asked for.

Only one writer touches `job.json` at a time. The store writes it when a job is submitted; the
worker writes it while the job runs; the scheduler writes it only once the worker has exited
without recording an end. Every write is atomic (a temporary file, then a rename), so a reader
never sees half a file.
"""

from __future__ import annotations

import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

JobState = Literal["queued", "running", "done", "failed", "cancelled", "interrupted"]
ACTIVE_STATES = ("queued", "running")

_JOB_ID = re.compile(r"^job_\d{8}T\d{12}_[0-9a-f]{6}$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Progress(BaseModel):
    stage: str = ""
    done: int = 0
    total: int = 0


class Job(BaseModel):
    id: str
    kind: str
    lane: str
    params: Dict[str, Any] = Field(default_factory=dict)
    state: JobState = "queued"
    created_by: str = "unknown"
    created_at: str = Field(default_factory=now_iso)
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    progress: Progress = Field(default_factory=Progress)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    # Outputs a job writes under a temporary name (containing ".tmp-") and renames when it
    # succeeds; whatever is left after an interrupted or cancelled run is removed.
    temp_paths: List[str] = Field(default_factory=list)


class ProcRecord(BaseModel):
    pid: int
    create_time: float
    started_at: str = Field(default_factory=now_iso)
    cancel_requested_at: Optional[float] = None


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


class JobStore:
    """The job folders under one root, usually the lake's `_jobs/`."""

    def __init__(self, root: Path) -> None:
        self.root = root

    @staticmethod
    def valid_id(job_id: str) -> bool:
        return bool(_JOB_ID.match(job_id))

    def job_dir(self, job_id: str) -> Path:
        if not self.valid_id(job_id):
            raise KeyError(f"not a job id: {job_id!r}")
        return self.root / job_id

    def exists(self, job_id: str) -> bool:
        return self.valid_id(job_id) and (self.root / job_id / "job.json").exists()

    def submit(self, kind: str, lane: str, params: Dict[str, Any], created_by: str) -> Job:
        """Record a queued job; the scheduler starts it when its lane has room."""
        # Microseconds in the id keep ids in submission order, so "oldest first" is a sort by id.
        job_id = f"job_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%f}_{secrets.token_hex(3)}"
        folder = self.root / job_id
        folder.mkdir(parents=True)
        job = Job(id=job_id, kind=kind, lane=lane, params=params, created_by=created_by)
        self.save(job)
        return job

    def load(self, job_id: str) -> Job:
        return Job.model_validate_json((self.job_dir(job_id) / "job.json").read_text(encoding="utf-8"))

    def save(self, job: Job) -> None:
        _write_atomic(self.job_dir(job.id) / "job.json", job.model_dump_json(indent=2))

    def update(self, job_id: str, **changes: Any) -> Job:
        job = self.load(job_id).model_copy(update=changes)
        self.save(job)
        return job

    def list(self) -> List[Job]:
        """Every job, oldest first (ids start with their creation time)."""
        if not self.root.exists():
            return []
        return [self.load(p.name) for p in sorted(self.root.iterdir())
                if self.valid_id(p.name) and (p / "job.json").exists()]

    def proc(self, job_id: str) -> Optional[ProcRecord]:
        path = self.job_dir(job_id) / "proc.json"
        if not path.exists():
            return None
        return ProcRecord.model_validate_json(path.read_text(encoding="utf-8"))

    def save_proc(self, job_id: str, record: ProcRecord) -> None:
        _write_atomic(self.job_dir(job_id) / "proc.json", record.model_dump_json(indent=2))

    def clear_proc(self, job_id: str) -> None:
        (self.job_dir(job_id) / "proc.json").unlink(missing_ok=True)

    def log_path(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "log.txt"

    def log_tail(self, job_id: str, lines: int = 40) -> str:
        path = self.log_path(job_id)
        if not path.exists():
            return ""
        return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:])

    def cancel_flag(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "cancel"
