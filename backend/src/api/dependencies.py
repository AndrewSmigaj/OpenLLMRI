#!/usr/bin/env python3
"""
Simple dependency injection for shared services.
"""

import logging
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Add backend to path
backend_src = Path(__file__).parent.parent  # backend/src
project_root = backend_src.parent.parent     # project root
sys.path.insert(0, str(backend_src))

from adapters.registry import get_adapter
from api import config
from api.config import DATA_LAKE_PATH
from services.probes.integrated_capture_service import IntegratedCaptureService
from services.probes.session_manager import SessionManager

# Global service instances (simple approach)
_capture_service = None

# A session store that only reads, for when there is no capture service (get_sessions)
_reader: Optional[SessionManager] = None
_reader_lock = threading.Lock()

# Loading stage tracking — readable by health endpoint while model loads in background thread.
# Stages: not_started → initializing → loading_model → creating_service → ready | failed;
# skipped when LOAD_MODEL is off (api/config.py)
_loading_stage = "not_started"
_loading_error = None
_loading_start_time = None


def _load_model_sync() -> None:
    """Load model in a background thread so the API can serve health checks immediately."""
    global _capture_service, _loading_stage, _loading_error, _loading_start_time

    _loading_start_time = time.time()
    _loading_stage = "initializing"
    logger.info("Initializing capture service")

    try:
        adapter = get_adapter("gpt-oss-20b")
        model_path = project_root / "data" / "models" / adapter.topology.model_dir

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at: {model_path}")

        _loading_stage = "loading_model"
        logger.info("Loading model from: %s (adapter: %s)", model_path, adapter.topology.model_name)
        model, tokenizer = adapter.load_model(str(model_path))

        _loading_stage = "creating_service"
        _capture_service = IntegratedCaptureService(
            model=model,
            tokenizer=tokenizer,
            layers_to_capture=adapter.layers_range(),
            data_lake_path=str(DATA_LAKE_PATH),
            adapter=adapter
        )

        elapsed = time.time() - _loading_start_time
        _loading_stage = "ready"
        logger.info("Model loaded successfully in %.0fs — capture service ready", elapsed)

    except Exception as e:
        elapsed = time.time() - _loading_start_time
        _loading_stage = "failed"
        _loading_error = str(e)
        logger.error("Model loading failed after %.0fs: %s", elapsed, e)
        logger.warning("API running in limited mode (analysis endpoints work, probe capture won't)")


async def initialize_capture_service() -> None:
    """Start model loading in a background thread. Returns immediately. With LOAD_MODEL off the
    model is left out, and the stage reads skipped."""
    global _loading_stage
    if _loading_stage != "not_started":
        return  # Already started or completed
    if not config.LOAD_MODEL:
        _loading_stage = "skipped"
        logger.info("LOAD_MODEL is off: the model isn't loaded; captures and agent runs answer 503")
        return

    thread = threading.Thread(target=_load_model_sync, daemon=True)
    thread.start()


def _why_no_model() -> str:
    """Why there is no capture service, for the 503's message."""
    if _loading_stage == "skipped":
        return ("The backend was started without the model (LOAD_MODEL=0); "
                "start it with the model to capture or run agents.")
    if _loading_stage == "failed":
        return f"The model failed to load: {_loading_error}"
    return "The model is still loading; try again once /health says ready."


def get_capture_service() -> IntegratedCaptureService:
    """The capture service, or 503 with the reason while there is none. An HTTPException keeps the
    response's CORS headers (an unhandled error loses them), so the app and the MUD can show it."""
    if _capture_service is None:
        raise HTTPException(status_code=503, detail=_why_no_model())

    return _capture_service


def get_sessions() -> SessionManager:
    """The session store. With the model loaded it is the capture service's own, which knows the
    captures in progress; without it, one that only reads the lake's session files. No capture can
    be in progress without the model, so the two never disagree."""
    global _reader
    if _capture_service is not None:
        return _capture_service.session_mgr
    with _reader_lock:
        if _reader is None:
            _reader = SessionManager(data_lake_path=str(config.DATA_LAKE_PATH), batch_size=1, layers_to_capture=[])
        return _reader


def is_model_loaded() -> bool:
    """Check if the capture service (and model) is initialized."""
    return _capture_service is not None


def get_loading_status() -> Dict[str, Any]:
    """Return current loading status for health endpoint."""
    elapsed = None
    if _loading_start_time is not None:
        elapsed = round(time.time() - _loading_start_time, 1)
    return {
        "stage": _loading_stage,
        "elapsed_seconds": elapsed,
        "error": _loading_error,
    }
