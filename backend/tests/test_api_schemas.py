"""The API's response models keep the fields the app reads."""
from api.schemas import TemporalLagDataResponse


def test_temporal_lag_data_keeps_the_run_id_and_the_basin_separation():
    # The temporal panel reads both (TemporalAnalysisSection.tsx). When the model lacked them,
    # pydantic dropped them silently and the panel crashed on basin_separation.toFixed.
    r = TemporalLagDataResponse(points=[], regime_boundary=3, processing_mode="expanding_cache_on",
                                temporal_run_id="trun_1", basin_separation=4.5)
    assert r.model_dump() == {"points": [], "regime_boundary": 3,
                              "processing_mode": "expanding_cache_on",
                              "temporal_run_id": "trun_1", "basin_separation": 4.5}
