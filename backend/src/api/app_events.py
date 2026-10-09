"""The app's event stream (DESIGN.md E7): what open apps hear without polling.

- `show`: a command asked the open apps to show a view;
- `job`: a background job changed state or progress;
- `lens`: a lens changed (built, validated, worked out, reported on, cut or saved);
- `ping`: every 15 seconds, so a quiet stream stays open.

Each connected app has a queue, and publishing puts the event on every queue. Publishing is safe
from any thread (FastAPI runs plain route functions in a thread pool). An app that falls too far
behind misses events, and like a reconnecting app it catches up by reading the jobs list.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

Event = Tuple[str, Dict[str, Any]]
QUEUE_SIZE = 500
LENS_KINDS = {"lens_build", "mass_mean_build", "lens_validate", "lens_details", "lens_analysis", "lens_search",
              "lens_read", "lens_routes", "lens_axes"}


class AppEvents:
    def __init__(self) -> None:
        self._subscribers: List[Tuple[asyncio.AbstractEventLoop, "asyncio.Queue[Event]"]] = []

    def subscribe(self) -> "asyncio.Queue[Event]":
        """A queue for one connected app; call from the event loop."""
        queue: "asyncio.Queue[Event]" = asyncio.Queue(maxsize=QUEUE_SIZE)
        self._subscribers.append((asyncio.get_running_loop(), queue))
        return queue

    def unsubscribe(self, queue: "asyncio.Queue[Event]") -> None:
        self._subscribers = [(loop, q) for loop, q in self._subscribers if q is not queue]

    @property
    def listeners(self) -> int:
        return len(self._subscribers)

    def publish(self, kind: str, data: Dict[str, Any]) -> int:
        """Send an event to every connected app; returns how many there are."""
        for loop, queue in list(self._subscribers):
            loop.call_soon_threadsafe(_offer, queue, (kind, data))
        return len(self._subscribers)


def _offer(queue: "asyncio.Queue[Event]", event: Event) -> None:
    try:
        queue.put_nowait(event)
    except asyncio.QueueFull:
        pass  # a stalled app misses this one; it catches up when it reconnects


async def watch_jobs(scheduler: Any, events: AppEvents, interval: float = 1.0) -> None:
    """Publish each job's changes of state or progress, and a `lens` event when a lens job ends
    well. Jobs that had already ended when the backend started aren't announced."""
    from api.routers.jobs import job_view

    seen: Dict[str, str] = {}
    first = True
    while True:
        try:
            for job in scheduler.store.list():
                view = job_view(scheduler, job).model_dump(mode="json")
                mark = json.dumps([view["state"], view["progress"]], sort_keys=True)
                if seen.get(job.id) == mark:
                    continue
                seen[job.id] = mark
                if first and job.state not in ("queued", "running"):
                    continue
                events.publish("job", view)
                if job.state == "done" and job.kind in LENS_KINDS:
                    events.publish("lens", {"session_id": job.params.get("session_id"),
                                            "name": job.params.get("name"), "change": job.kind})
            first = False
        except Exception:
            logger.exception("The job watcher failed a round")
        await asyncio.sleep(interval)


PING_SECONDS = 15.0


async def stream(events: AppEvents, request: Any) -> Any:
    """Server-sent events for one app until it goes away."""
    queue = events.subscribe()
    try:
        yield "retry: 3000\n\n"
        while not await request.is_disconnected():
            try:
                kind, data = await asyncio.wait_for(queue.get(), timeout=PING_SECONDS)
            except asyncio.TimeoutError:
                kind, data = "ping", {}
            yield f"event: {kind}\ndata: {json.dumps(data)}\n\n"
    finally:
        events.unsubscribe(queue)
