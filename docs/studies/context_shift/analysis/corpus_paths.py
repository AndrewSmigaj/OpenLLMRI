#!/usr/bin/env python3
"""One place for corpus-version paths (pre-registration v2, "Logs and paths").

Defaults are the v1 values, so every existing script reproduces v1 unchanged.
For v2, the chains write these same canonical log names (v1 logs are archived
under captures/v1/) and the calibration step overwrites AXES_* with the v2 axes
after the v1 axes are archived alongside the logs. Scripts import from here
instead of hardcoding session ids.
"""
CAP = "docs/studies/context_shift/captures"
AXD = "docs/studies/context_shift/analysis/axes"
LOG_TANK_D3D4 = f"{CAP}/tank_d3_d4_log.tsv"
LOG_FR_D3D4   = f"{CAP}/fr_d3_d4_log.tsv"
AXES_TANK_POS1 = f"{AXD}/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"
AXES_FR_POS1   = f"{AXD}/axes_session_5247081b_fictional_vs_real_pos1.npz"
