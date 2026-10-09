"""The one-layer preview (DESIGN.md E3): it equals a build's layer for the same settings and seed,
finds planted classes, keeps the test portion out of every score that uses labels, and refuses
what it can't do. Run through its job and its two endpoints."""

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pytest
from fastapi.testclient import TestClient
from test_lens_api import client  # noqa: F401  (client is a fixture)
from test_lenses import SESSION, build, lake, lens  # noqa: F401  (lake is a fixture)

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.preview import run_preview

SETTINGS = {"n_neighbors": 10, "dimensions": 3, "min_dist": 0.1, "metric": "euclidean"}


def preview(root: Path, **params: Any) -> Dict[str, Any]:
    """Run a preview job here, as its worker would; returns its preview.json."""
    store = JobStore(root / "_jobs")
    full = {"session_id": SESSION, "layer": 0, "settings": SETTINGS, "k": 2, **params}
    job = store.submit("lens_preview", "preview", full, created_by="test")
    run_preview(full, JobContext(store, job.id))
    found: Dict[str, Any] = json.loads((store.job_dir(job.id) / "preview.json").read_text())
    return found


def test_a_preview_equals_the_same_layer_of_a_build(lake: Path) -> None:  # noqa: F811
    from services.lenses.frame import principal

    build(lake, **SETTINGS)
    folder = lens(lake)
    found = preview(lake)
    nodes = np.load(folder / "v1" / "assign.npz")["nodes"][:, 0]
    assert found["nodes"] == nodes.tolist()  # the same cut of the same tree
    embedding = np.load(folder / "fit" / "embed.npz")["embedding"][0][:, :3].astype(np.float64)
    centred = embedding - embedding.mean(axis=0)
    basis, _ = principal(centred)
    assert np.allclose(np.array(found["points"]), centred @ basis, atol=1e-3)
    assert found["n_items"] == 40 and found["ks"][0] == 2 and found["share"] == 1.0


def test_planted_classes_score_high_outside_the_test_portion(lake: Path, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F811
    import sklearn.metrics

    import services.lenses.validate as validate

    sizes: List[int] = []
    original_ami, original_heldout = sklearn.metrics.adjusted_mutual_info_score, validate.heldout_scores

    def ami_spy(truth: Any, predicted: Any, **kwargs: Any) -> float:
        sizes.append(len(truth))
        return float(original_ami(truth, predicted, **kwargs))

    def heldout_spy(states: np.ndarray, *args: Any, **kwargs: Any) -> Any:
        sizes.append(len(states))
        return original_heldout(states, *args, **kwargs)

    monkeypatch.setattr(sklearn.metrics, "adjusted_mutual_info_score", ami_spy)
    monkeypatch.setattr(validate, "heldout_scores", heldout_spy)
    found = preview(lake, held_out=True, holdout={"family_field": None, "test_share": 0.2})
    left_out = found["test"]["n_items"]
    assert 4 <= left_out <= 14 and found["test"]["weaker"]  # a stratified 20% (no families here)
    assert sizes and max(sizes) <= 40 - left_out  # no score that uses labels saw the test portion
    assert found["in_sample"]["ami"]["label"]["2"] > 0.9
    assert found["heldout"]["2"]["label"]["ami"] > 0.9 and found["folds"]["n_folds"] == 5
    assert "register" in found["axes"] and found["holdout"]["family_field"] is None


def test_what_a_preview_refuses(lake: Path) -> None:  # noqa: F811
    with pytest.raises(ValueError, match="k 40"):
        preview(lake, k=40)
    with pytest.raises(ValueError, match="layer 7"):
        preview(lake, layer=7)


def test_the_preview_endpoints(client: TestClient) -> None:  # noqa: F811
    started = client.post("/api/lenses/preview", json={"session_id": SESSION, "layer": 1, "settings": SETTINGS, "k": 2})
    assert started.status_code == 202
    job_id = started.json()["job_id"]
    assert client.get(f"/api/lenses/previews/{job_id}").status_code == 404  # not finished
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    job = store.load(job_id)
    assert job.kind == "lens_preview" and job.lane == "preview"
    run_preview(job.params, JobContext(store, job_id))
    found = client.get(f"/api/lenses/previews/{job_id}").json()
    assert found["layer"] == 1 and len(found["points"]) == 40 and set(found["nodes"]) == {0, 1}
    assert client.post("/api/lenses/preview", json={"session_id": "session_none", "layer": 0}).status_code == 404
    assert client.get("/api/lenses/previews/not-a-job").status_code == 404
