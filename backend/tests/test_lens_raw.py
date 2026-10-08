"""Raw space beside UMAP: neuron choice inside the fold, the supervised ceiling, the disagreement
marks, and mass-mean lenses (their readings and their API)."""

from pathlib import Path
from typing import Any, Dict

import numpy as np
from fastapi.testclient import TestClient
from test_lens_api import BODY, client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.fit import mass_mean_axis, mass_mean_reading
from services.lenses.raw import (
    NEURON_PCS,
    co_member_overlap,
    pca_features,
    relevant_neurons,
    ward_cuts,
)
from services.lenses.validate import _majority, _vote, compare_layer, make_folds


def _items(labels: Any) -> list:
    return [{"probe_id": f"p{i}", "label": str(v), "input_text": f"t{i}", "categories": {}} for i, v in enumerate(labels)]


def test_neurons_chosen_inside_the_fold_keep_a_null_at_chance_and_a_leak_inflates_it() -> None:
    inside, leaked = [], []
    for seed in range(3):
        rng = np.random.default_rng(seed)
        states, labels = rng.normal(size=(80, 2000)).astype(np.float32), rng.integers(0, 2, size=80)
        folds, _ = make_folds(_items(labels), "scene", 4, 42)
        for chosen_with_all in (False, True):
            accuracies = []
            for test in folds:
                train = np.setdiff1d(np.arange(80), test)
                keep = relevant_neurons(states, labels) if chosen_with_all else relevant_neurons(states[train], labels[train])
                tr, te = pca_features(states[train][:, keep], states[test][:, keep], 42, NEURON_PCS)
                cut = ward_cuts(tr, [2])[2]
                guess = _majority(cut, labels[train], 2)[_vote(te, tr, cut, 2)]
                accuracies.append(float((guess == labels[test]).mean()))
            (leaked if chosen_with_all else inside).append(np.mean(accuracies))
    assert np.mean(inside) < 0.65 and np.mean(leaked) > 0.9


def test_the_ceiling_is_at_least_as_good_as_the_unsupervised_groupings_on_linear_data() -> None:
    rng = np.random.default_rng(1)
    labels = np.arange(120) % 2
    direction = rng.normal(size=300)
    states = (rng.normal(size=(120, 300)) * 3 + np.outer(labels * 2 - 1, direction) * 0.6).astype(np.float32)
    folds, _ = make_folds(_items(labels), "scene", 4, 42)
    comparison, full = compare_layer(states, folds, labels, 15, 42)
    ceiling = comparison["ceiling"]["kappa"]
    assert all(ceiling >= comparison[m]["2"]["kappa"] for m in ("raw_ward", "raw_spectral"))
    assert set(full) == {"raw_ward", "raw_spectral"} and len(full["raw_ward"][2]) == 120


def test_marks_follow_the_co_member_overlap() -> None:
    lens = np.array([0, 0, 0, 1, 1, 1])
    raw = np.array([0, 0, 1, 1, 1, 1])
    assert np.allclose(co_member_overlap(lens, raw), [2 / 3, 2 / 3, 1 / 6, 3 / 4, 3 / 4, 3 / 4])
    assert np.allclose(co_member_overlap(lens, lens), 1.0)


def test_mass_mean_readings_match_the_retired_endpoints_formula() -> None:
    rng = np.random.default_rng(2)
    states = rng.normal(size=(50, 40)).astype(np.float32)
    is_b = np.arange(50) % 2 == 1
    states[is_b] += 1.5
    axis, mid, norm2 = mass_mean_axis(states, is_b)
    # the raw-axis endpoint (removed in 10b.8): axis = mean(B) - mean(A), midpoint rule, scaled to -1/+1
    mean_a, mean_b = states[~is_b].mean(0), states[is_b].mean(0)
    old = 2.0 * ((states - (mean_a + mean_b) / 2) @ (mean_b - mean_a)) / float((mean_b - mean_a) @ (mean_b - mean_a))
    reading = mass_mean_reading(states, axis, mid, norm2)
    assert np.allclose(reading, old, atol=1e-4)
    assert np.isclose(reading[~is_b].mean(), -1, atol=1e-4) and np.isclose(reading[is_b].mean(), 1, atol=1e-4)


def _run(client: TestClient, job_id: str, run: Any) -> Dict[str, Any]:  # noqa: F811
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    result: Dict[str, Any] = run(store.load(job_id).params, JobContext(store, job_id))
    return result


def test_mass_mean_lenses_build_validate_and_read_any_capture(client: TestClient, tmp_path: Path) -> None:  # noqa: F811
    from services.lenses.massmean import build_mass_mean

    started = client.post("/api/lenses/mass-mean", json={"session_id": SESSION, "name": "ab-axis",
                                                          "label_a": "a", "label_b": "b"})
    assert started.status_code == 202
    result = _run(client, started.json()["job_id"], build_mass_mean)
    assert result["best_accuracy"] > 0.95  # the synthetic classes sit far apart
    base = f"/api/sessions/{SESSION}/lenses/ab-axis"
    read = client.get(f"{base}/readings").json()
    assert read["layers"] == [0, 1, 2] and len(read["readings"]) == 40
    by_label = {lab: np.mean([r[0] for r, item in zip(read["readings"], read["items"]) if item["label"] == lab])
                for lab in ("a", "b")}
    assert np.isclose(by_label["a"], -1, atol=1e-3) and np.isclose(by_label["b"], 1, atol=1e-3)
    assert client.get(f"{base}/validation").json()["layers"]["0"]["accuracy"] > 0.95
    assert client.get(f"{base}/flows").status_code == 400  # no clusters
    assert client.post(f"{base}/validate", json={}).status_code == 400
    listed = {lens["name"]: lens for lens in client.get(f"/api/sessions/{SESSION}/lenses").json()}
    assert listed["ab-axis"]["kind"] == "mass_mean" and listed["ab-axis"]["validation"]["best"]["accuracy"] > 0.95


def test_marks_come_from_a_validated_umap_lens(client: TestClient) -> None:  # noqa: F811
    from services.lenses.validate import validate_lens

    run_job(client, client.post("/api/lenses", json=BODY).json()["job_id"])
    base = f"/api/sessions/{SESSION}/lenses/synth"
    assert client.get(f"{base}/marks").status_code == 404
    started = client.post(f"{base}/validate", json={"n_folds": 4, "seeds": 2, "workers": 1})
    _run(client, started.json()["job_id"], validate_lens)
    marks = client.get(f"{base}/marks").json()
    assert set(marks["layers"]) == {"0", "1", "2"}
    assert marks["layers"]["0"]["method"] in ("raw_ward", "raw_spectral") and marks["layers"]["0"]["k"] == 2
    comparison = client.get(f"{base}/validation").json()["comparison"]["0"]
    assert comparison["ceiling"]["kappa"] > 0.9 and comparison["raw_ward"]["2"]["kappa"] > 0.9
