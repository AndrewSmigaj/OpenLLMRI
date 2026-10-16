"""How many worker processes a job's parallel stages use (lens builds, validation, tuning searches,
the axes analysis), when the request doesn't say.

JOB_WORKERS sets it, for example to 2 while other programs need the memory; otherwise up to six,
leaving two cores free. Results don't depend on it, since each worker pins BLAS and numba to one
thread (services/jobs/scheduler.py); only the time and the memory do.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


def default_workers() -> int:
    """JOB_WORKERS when it is a whole number of at least 1, else max(1, min(6, cores - 2))."""
    raw = os.environ.get("JOB_WORKERS", "").strip()
    if raw:
        try:
            return max(1, int(raw))
        except ValueError:
            logger.warning("JOB_WORKERS=%r isn't a whole number; using the default", raw)
    return max(1, min(6, (os.cpu_count() or 2) - 2))
