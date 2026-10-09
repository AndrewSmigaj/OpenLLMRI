"""Settings by hand (DESIGN.md C4, E3): the distance metric reaches every fit and stays with the saved
reducers; settings record where they came from, and only a search's read as tuned; a lens records
its hold-out design, which later jobs use; family folds beyond a cap merge, still whole."""

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pyarrow.parquet as pq
import pytest
from fastapi.testclient import TestClient
from test_lens_api import client  # noqa: F401  (client is a fixture)
from test_lenses import SESSION, build, lake, lens  # noqa: F401  (lake is a fixture)

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.store import (
    HoldoutDesign,
    LensSettings,
    UmapSettings,
    holdout_of,
    read_manifest,
    resolve_holdout,
    summary,
)
from services.lenses.validate import make_folds


def run(root: Path, kind: str, params: Dict[str, Any]) -> Any:
    """Run a job in this process, as its worker would."""
    from services.jobs.kinds import KINDS

    store = JobStore(root / "_jobs")
    job = store.submit(kind, "cpu", params, created_by="test")
    return KINDS[kind].run(params, JobContext(store, job.id))


def test_the_metric_reaches_every_fit_and_stays_with_the_reducers(lake: Path, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F811
    import joblib

    import services.lenses.fit as fit
    from services.lenses.data import load_states

    metrics: List[str] = []
    original = fit.fit_reducer

    def spy(states: np.ndarray, settings: UmapSettings, seed: int) -> Any:
        metrics.append(settings.metric)
        return original(states, settings, seed)

    monkeypatch.setattr(fit, "fit_reducer", spy)
    build(lake, name="cos", metric="cosine")  # the build and its self-check
    run(lake, "lens_validate", {"session_id": SESSION, "name": "cos", "workers": 1, "seeds": 2})
    run(lake, "lens_search", {"session_id": SESSION, "source_lens": "cos", "workers": 1,
                              "grid": {"n_neighbors": [5], "dimensions": [3], "min_dist": [0.1]}})
    assert len(metrics) > 30 and set(metrics) == {"cosine"}  # search, test, tuned build and its validation too
    tuned = read_manifest(lens(lake, "cos-tuned")).settings
    assert {s.metric for s in tuned.per_layer or []} == {"cosine"} and tuned.origin() == "tuned"

    folder = lens(lake, "cos")
    reducer = joblib.load(folder / "fit" / "umap_L00.joblib")
    assert reducer.metric == "cosine"
    ids = [str(v) for v in pq.read_table(folder / "items.parquet", columns=["probe_id"]).column(0).to_pylist()]
    rows = np.ascontiguousarray(load_states(SESSION, ids)[0])
    reducer._raw_data = rows  # reattached as a reading does
    noisy = rows + np.random.default_rng(1).normal(size=rows.shape).astype(np.float32) * 0.05
    placed = reducer.transform(noisy)
    own = np.load(folder / "fit" / "embed.npz")["embedding"][0][:, :reducer.n_components]
    nearest = np.argmin(((placed[:, None, :] - own[None, :, :]) ** 2).sum(-1), axis=1)
    labels = np.arange(len(ids)) % 2
    assert (labels[nearest] == labels).mean() > 0.9  # read with its own metric, each lands among its class


def test_only_a_search_reads_as_tuned(lake: Path) -> None:  # noqa: F811
    per_layer = [{"n_neighbors": 5, "dimensions": 3}, {"n_neighbors": 10, "dimensions": 4},
                 {"n_neighbors": 8, "dimensions": 2, "metric": "correlation"}]
    build(lake, name="hand", per_layer=per_layer, sources=["table", "preview held out", "form"])
    folder = lens(lake, "hand")
    manifest = read_manifest(folder)
    assert [manifest.settings.source_at(li) for li in range(3)] == ["table", "preview held out", "form"]
    assert manifest.settings.at(2).metric == "correlation" and manifest.settings.at(0).metric == "euclidean"
    listed = summary(manifest, folder)
    assert listed["settings_origin"] == "by hand" and listed["selection_biased"]
    # Lenses built before sources existed: settings per layer came only from searches
    old = LensSettings.model_validate({"n_neighbors": 15, "dimensions": 6, "seed": 42,
                                       "per_layer": [{"n_neighbors": 5, "dimensions": 3}]})
    assert old.origin() == "tuned" and old.chosen_on_heldout() and old.at(0).metric == "euclidean"
    assert LensSettings().origin() == "form" and not LensSettings().chosen_on_heldout()
    with pytest.raises(ValueError, match="sources"):
        build(lake, name="short", per_layer=per_layer, sources=["table"])


def test_a_lens_records_its_hold_out_design_and_later_jobs_use_it(lake: Path) -> None:  # noqa: F811
    sessions = lake / "_sessions"
    sessions.mkdir(exist_ok=True)
    declared = {"family_field": "register", "whole_families": True}
    (sessions / f"{SESSION}.json").write_text(json.dumps({"session_id": SESSION, "holdout": declared}))
    build(lake, name="declared")
    folder = lens(lake, "declared")
    manifest = read_manifest(folder)
    assert manifest.holdout == HoldoutDesign(family_field="register", whole_families=True)  # cap 12, share 0.2
    routes = json.loads((folder / "routes.json").read_text())
    assert routes["rules"]["family_field"] == "register"  # the build's own routes used it
    assert resolve_holdout(folder, manifest, "label").family_field == "label"  # a request wins
    assert resolve_holdout(folder, manifest, "").family_field is None  # "" asks for no families

    # A lens built before the record: the field its validation used, with no cap
    old = manifest.model_copy(update={"holdout": None})
    (folder / "validation.json").write_text(json.dumps({"folds": {"field": "family", "whole": True}}))
    assert holdout_of(folder, old) == HoldoutDesign(family_field="family", whole_families=True, max_folds=None)
    (folder / "validation.json").write_text(json.dumps({"folds": {"kind": "stratified"}}))
    assert holdout_of(folder, old) == HoldoutDesign(family_field="register", whole_families=True, max_folds=None)


def test_family_folds_beyond_the_cap_merge_and_no_cap_keeps_todays() -> None:
    # Shaped like the calibration set: two labels, twelve scene families each
    items = [{"probe_id": f"p{label}{family}{i}", "label": label, "input_text": f"t{label}{family}{i}",
              "categories": {"scene": f"{label}_{family:02d}"}}
             for label in ("aquarium", "vehicle") for family in range(12) for i in range(3)]
    today, how = make_folds(items, "scene", 5, 42)
    capped, how12 = make_folds(items, "scene", 5, 42, max_folds=12)
    assert len(today) == 12 and "merged_from" not in how
    assert [f.tolist() for f in capped] == [f.tolist() for f in today] and "merged_from" not in how12
    five, how5 = make_folds(items, "scene", 5, 42, max_folds=5)
    assert len(five) == 5 and how5["merged_from"] == 12 and how5["n_folds"] == 5
    for fold in five:  # every family sits wholly in one fold
        held = {items[j]["categories"]["scene"] for j in fold}
        assert sum(item["categories"]["scene"] in held for item in items) == len(fold)
    assert make_folds(items, None, 4, 42)[1]["weaker"]  # no families field: stratified


def test_the_form_learns_the_metrics_fields_and_declared_design(client: TestClient) -> None:  # noqa: F811
    methods = client.get("/api/lenses/methods").json()
    assert methods["metrics"] == ["euclidean", "cosine", "correlation", "manhattan"]
    assert methods["defaults"]["metric"] == "euclidean" and methods["holdout"]["max_folds"] == 12
    options = client.get(f"/api/captures/{SESSION}/lens-options").json()
    assert options["category_fields"] == {"register": 2} and options["declared_holdout"] is None
    assert options["layers"] == [0, 1, 2]
