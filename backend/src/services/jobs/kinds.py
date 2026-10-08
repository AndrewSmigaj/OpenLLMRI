"""The kinds of background job, the lane each runs in, and what a running job can call.

A kind is a function `run(params, ctx) -> result`. It runs inside the worker process, reports its
progress through `ctx`, and checks `ctx.check_cancelled()` between steps. Kinds import their heavy
modules inside `run`, so the worker and the backend start quickly.

Lanes limit how many jobs of a kind run at once: `cpu` for builds that fill the processor, `llm`
for jobs that call Claude. Slice 2 adds a GPU lane.
"""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict

from services.jobs.store import JobStore, Progress

LANES: Dict[str, int] = {"cpu": 1, "llm": 1}


class JobCancelledError(Exception):
    """Raised by `JobContext.check_cancelled` once a cancel was asked for."""


class JobContext:
    """What a running job uses to report progress and notice a cancel."""

    def __init__(self, store: JobStore, job_id: str) -> None:
        self.store = store
        self.job_id = job_id
        self.job_dir = store.job_dir(job_id)

    def progress(self, stage: str, done: int, total: int) -> None:
        self.store.update(self.job_id, progress=Progress(stage=stage, done=done, total=total))

    def cancelled(self) -> bool:
        return self.store.cancel_flag(self.job_id).exists()

    def check_cancelled(self) -> None:
        if self.cancelled():
            raise JobCancelledError()

    def log(self, message: str) -> None:
        print(message, flush=True)

    def add_temp_path(self, path: Path) -> None:
        """Name an output written under a temporary name, so an unfinished run's leftovers are removed."""
        job = self.store.load(self.job_id)
        self.store.update(self.job_id, temp_paths=job.temp_paths + [str(path)])


@dataclass(frozen=True)
class JobKind:
    lane: str
    run: Callable[[Dict[str, Any], JobContext], Dict[str, Any]]


def _noop(params: Dict[str, Any], ctx: JobContext) -> Dict[str, Any]:
    """Wait, and optionally fail, burn CPU or start a child process. The jobs' own tests use it.

    params: seconds (total wait), steps (progress steps), fail (a message to raise),
    busy (spin instead of sleeping), spawn_child (start a sleeping child, its pid in child.pid).
    """
    if params.get("spawn_child"):
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
        (ctx.job_dir / "child.pid").write_text(str(child.pid), encoding="utf-8")
    steps = max(1, int(params.get("steps", 1)))
    seconds = float(params.get("seconds", 0.0))
    for i in range(steps):
        ctx.check_cancelled()
        ctx.progress("waiting", i, steps)
        end = time.time() + seconds / steps
        while time.time() < end:
            if not params.get("busy"):
                time.sleep(min(0.05, max(0.0, end - time.time())))
    if params.get("fail"):
        raise RuntimeError(str(params["fail"]))
    ctx.progress("done", steps, steps)
    return {"waited": seconds}


def _lens_build(params: Dict[str, Any], ctx: JobContext) -> Dict[str, Any]:
    from services.lenses.build import build_lens

    return build_lens(params, ctx)


def _lens_validate(params: Dict[str, Any], ctx: JobContext) -> Dict[str, Any]:
    from services.lenses.validate import validate_lens

    return validate_lens(params, ctx)


KINDS: Dict[str, JobKind] = {
    "noop": JobKind(lane="cpu", run=_noop),
    "noop_llm": JobKind(lane="llm", run=_noop),
    "lens_build": JobKind(lane="cpu", run=_lens_build),
    "lens_validate": JobKind(lane="cpu", run=_lens_validate),
}
