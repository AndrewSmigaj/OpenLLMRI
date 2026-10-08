"""Background jobs: list them, read one (with its log's tail when it failed), cancel one.

Jobs are submitted by the endpoints that need them (lens builds, report runs); the scheduler
(`services.jobs.scheduler`) starts and watches them.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request

from services.jobs.scheduler import JobScheduler
from services.jobs.store import ACTIVE_STATES, Job

router = APIRouter()


class JobView(Job):
    log_tail: Optional[str] = None


def _scheduler(request: Request) -> JobScheduler:
    scheduler: JobScheduler = request.app.state.jobs
    return scheduler


def _view(scheduler: JobScheduler, job: Job) -> JobView:
    tail = scheduler.store.log_tail(job.id) if job.state in ("failed", "interrupted") else None
    return JobView(**job.model_dump(), log_tail=tail)


def _known(scheduler: JobScheduler, job_id: str) -> None:
    if not scheduler.store.exists(job_id):
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")


@router.get("/jobs", response_model=List[JobView])
def list_jobs(request: Request, active: bool = False) -> List[JobView]:
    """Every job, newest first; `active=true` keeps only queued and running ones."""
    scheduler = _scheduler(request)
    jobs = [j for j in reversed(scheduler.store.list()) if not active or j.state in ACTIVE_STATES]
    return [_view(scheduler, j) for j in jobs]


@router.get("/jobs/{job_id}", response_model=JobView)
def get_job(request: Request, job_id: str) -> JobView:
    scheduler = _scheduler(request)
    _known(scheduler, job_id)
    return _view(scheduler, scheduler.store.load(job_id))


@router.post("/jobs/{job_id}/cancel", response_model=JobView)
def cancel_job(request: Request, job_id: str) -> JobView:
    """Cancel a queued job at once, or stop a running one (its whole process group)."""
    scheduler = _scheduler(request)
    _known(scheduler, job_id)
    return _view(scheduler, scheduler.cancel(job_id))
