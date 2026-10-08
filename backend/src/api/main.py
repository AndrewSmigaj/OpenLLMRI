#!/usr/bin/env python3
"""
FastAPI server for Concept MRI - MoE interpretability through Concept Trajectory Analysis.
"""

from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root BEFORE importing anything that reads env vars
# at module-import time. `api.schemas.AgentStartRequest` evaluates
# `os.environ.get("EVENNIA_AGENT_PASS", "")` as a Pydantic field default at
# import time, so the dotenv load must happen before the router imports
# below. Without this, the backend can't authenticate as the agent unless
# the launching shell manually exported the env vars.
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_PROJECT_ROOT / ".env")

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app_events import AppEvents, watch_jobs
from api.config import JOBS_PATH
from api.dependencies import get_loading_status, initialize_capture_service, is_model_loaded
from api.routers import (
    agent,
    analysis,
    clustering,
    commands,
    generation,
    insights,
    jobs,
    lenses,
    probes,
    prompts,
    routes,
)
from services.jobs.scheduler import JobScheduler
from services.jobs.store import JobStore

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting Concept MRI API")
    await initialize_capture_service()  # starts background thread, returns immediately
    logger.info("API serving — model loading in background")
    scheduler = JobScheduler(JobStore(JOBS_PATH))
    scheduler.adopt()  # workers outlive a restart
    app.state.jobs = scheduler
    app.state.events = AppEvents()  # the open apps' event stream (GET /api/app/events)
    ticking = asyncio.create_task(scheduler.run())
    watching = asyncio.create_task(watch_jobs(scheduler, app.state.events))
    yield
    ticking.cancel()  # running workers carry on; the next start re-adopts them
    watching.cancel()
    logger.info("Shutting down Concept MRI API")

# Create FastAPI app
app = FastAPI(title="Concept MRI API", version="1.0", lifespan=lifespan)

# Only the app may call the API from a browser (APP_ORIGINS in the root .env, comma separated). The
# MUD calls it from its server and Claude Code with curl, neither of which CORS concerns.
APP_ORIGINS = [origin.strip() for origin in
               os.environ.get("APP_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(probes.router, prefix="/api")
app.include_router(routes.router, prefix="/api")
app.include_router(clustering.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(generation.router, prefix="/api")
app.include_router(prompts.router, prefix="/api")
app.include_router(agent.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(lenses.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(commands.router, prefix="/api")

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Concept MRI API", "status": "running"}

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "model_loaded": is_model_loaded(),
        "loading": get_loading_status(),
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "sessions_available": True,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
