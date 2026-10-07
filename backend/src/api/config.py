#!/usr/bin/env python3
"""
Centralized configuration for the ConceptMRI backend.
"""

import os
from pathlib import Path

_project_root = Path(__file__).resolve().parents[3]  # config.py → api/ → src/ → backend/ → project_root
_raw_lake = os.environ.get("DATA_LAKE_PATH", "")
DATA_LAKE_PATH = (_project_root / _raw_lake) if _raw_lake and not Path(_raw_lake).is_absolute() else Path(_raw_lake or str(_project_root / "data" / "lake"))

# The MUD's websocket on this host: the repo root's .env sets the port (MUD_WS_PORT) for compose,
# Evennia's web client, the app and this backend; Evennia's 4002 otherwise.
MUD_WS_URL = f"ws://localhost:{os.environ.get('MUD_WS_PORT') or '4002'}"

# The scenario library: one copy, read by the MUD (mounted into its container) and by the runner.
SCENARIO_LIBRARY = _project_root / "data" / "scenarios"
