"""One thread each for BLAS and numba in the tests, as inside a job's worker (services/jobs/scheduler.py).
On many cores, threaded BLAS on the tests' small matrices is far slower than one thread (the axes
tests took 99 s instead of 2), and results no longer depend on the machine's core count."""

import os

from threadpoolctl import threadpool_limits

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_name, "1")
threadpool_limits(1)  # for libraries loaded before the pins
