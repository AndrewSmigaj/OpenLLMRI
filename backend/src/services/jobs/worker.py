"""Run one background job in its own process: `python -m services.jobs.worker <job folder>`.

The scheduler starts the worker in a new session, so cancelling can end the whole process group,
with BLAS and numba pinned to one thread each. The worker lowers its own priority, marks the job
running, runs its kind and records the result. A failure is recorded with its message, and the
traceback goes to the job's log.
"""

from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path
from typing import List

from services.jobs.kinds import KINDS, JobCancelledError, JobContext
from services.jobs.store import JobStore, now_iso


def main(argv: List[str]) -> int:
    job_dir = Path(argv[1])
    store = JobStore(job_dir.parent)
    job_id = job_dir.name
    try:
        os.nice(10)
    except OSError:
        pass
    job = store.update(job_id, state="running", started_at=now_iso())
    try:
        kind = KINDS[job.kind]
        result = kind.run(job.params, JobContext(store, job_id))
    except JobCancelledError:
        store.update(job_id, state="cancelled", finished_at=now_iso())
        return 0
    except Exception as e:
        traceback.print_exc()
        store.update(job_id, state="failed", error=f"{type(e).__name__}: {e}", finished_at=now_iso())
        return 1
    store.update(job_id, state="done", result=result, finished_at=now_iso())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
