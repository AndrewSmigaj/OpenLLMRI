#!/usr/bin/env python3
"""
The raw-axis projection endpoint.

The basin-era temporal capture and lag endpoints were retired on 2026-10-08 (DESIGN.md G). This
endpoint stays until saved mass-mean lenses replace it; then this module goes.
"""

import logging

from fastapi import APIRouter, HTTPException

from api.config import DATA_LAKE_PATH
from api.schemas import (
    RawAxisLayerReport,
    RawAxisPoint,
    RawAxisProjectionRequest,
    RawAxisProjectionResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/experiments/raw-axis-projection", response_model=RawAxisProjectionResponse)
async def raw_axis_projection(request: RawAxisProjectionRequest) -> RawAxisProjectionResponse:
    """Raw 2880-d difference-of-class-means projection (N1 instrument).

    Per layer: axis = mean(B) - mean(A) on raw residual streams at the requested
    semantic token position; projections normalized so class means land at -1/+1.
    Mirrors the validated study script docs/studies/context_shift/analysis/axis_projection.py.
    It retires when saved mass-mean lenses replace it (DESIGN.md G).
    """
    import numpy as np
    import pandas as pd

    def load(session_id: str) -> pd.DataFrame:
        lake = DATA_LAKE_PATH / session_id
        if not lake.exists():
            raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[res["token_position"] == request.token_position]
        tok = pd.read_parquet(lake / "tokens.parquet",
                              columns=["probe_id", "label", "sentence_index"])
        return res.merge(tok, on="probe_id", how="left")

    try:
        cal = load(request.calibration_session_id)
        cal = cal[cal["label"].isin([request.label_a, request.label_b])]
        if not len(cal):
            raise HTTPException(status_code=400,
                detail=f"No probes with labels '{request.label_a}'/'{request.label_b}' "
                       f"at token_position {request.token_position}")

        tgt = load(request.target_session_id) if request.target_session_id else cal

        layers = request.layers or sorted(cal["layer"].unique().tolist())
        report, points = [], []
        for L in layers:
            sub = cal[cal["layer"] == L]
            if not len(sub):
                continue
            X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            y = (sub["label"] == request.label_b).to_numpy()
            if y.all() or (~y).all():
                continue
            mean_a, mean_b = X[~y].mean(0), X[y].mean(0)
            axis = mean_b - mean_a
            denom = float(axis @ axis)
            if denom < 1e-12:
                continue
            mid = (mean_a + mean_b) / 2.0
            cal_proj = 2.0 * ((X - mid) @ axis) / denom
            report.append(RawAxisLayerReport(
                layer=int(L), n_a=int((~y).sum()), n_b=int(y.sum()),
                axis_norm=float(np.sqrt(denom)),
                mean_proj_a=float(cal_proj[~y].mean()), mean_proj_b=float(cal_proj[y].mean()),
                std_a=float(cal_proj[~y].std()), std_b=float(cal_proj[y].std()),
            ))
            tsub = tgt[tgt["layer"] == L]
            if not len(tsub):
                continue
            Xt = np.stack(tsub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            proj = 2.0 * ((Xt - mid) @ axis) / denom
            for pid, lab, sidx, pv in zip(tsub["probe_id"], tsub["label"],
                                          tsub["sentence_index"], proj):
                points.append(RawAxisPoint(
                    probe_id=pid, layer=int(L),
                    label=None if pd.isna(lab) else str(lab),
                    sentence_index=None if pd.isna(sidx) else int(sidx),
                    projection=float(pv),
                ))
        return RawAxisProjectionResponse(report=report, points=points)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Raw axis projection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Raw axis projection failed: {str(e)}")
