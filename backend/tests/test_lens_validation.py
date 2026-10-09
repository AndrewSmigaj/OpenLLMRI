"""Validating lenses: folds by scene family, held-out scores and the k profile, the self-check, and
the validate endpoints."""

from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient
from test_lens_api import BODY, client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.store import UmapSettings
from services.lenses.validate import axis_codes, make_folds, self_check, validate_layer


def test_the_self_check_finds_planted_classes_and_nothing_in_noise() -> None:
    check = self_check(100, 64, UmapSettings(n_neighbors=15, dimensions=6), 42)  # small, as CI runs it
    assert check["passed"] and check["planted"]["ari_k5"] >= 0.9 and check["null"]["ami_k5"] <= 0.05


def test_folds_hold_out_whole_scene_families_of_every_class() -> None:
    items = [{"probe_id": f"p{i}", "label": "ab"[i % 2], "input_text": f"text {i}",
              "categories": {"scene": f"{'ab'[i % 2]}scene_{i % 6 // 2}_batch{i % 3}"}} for i in range(60)]
    folds, how = make_folds(items, "scene", 5, 42)
    assert how["kind"] == "scene families" and not how["weaker"] and how["n_folds"] == 3
    for test in folds:
        held = {items[j]["categories"]["scene"].rsplit("_", 1)[0] for j in test}
        assert len(held) == 2 and {name[0] for name in held} == {"a", "b"}  # one family of each class
        train = set(range(60)) - set(test.tolist())
        assert not held & {items[j]["categories"]["scene"].rsplit("_", 1)[0] for j in train}
    assert sorted(np.concatenate(folds).tolist()) == list(range(60))


def test_a_family_holding_two_labels_is_held_out_whole() -> None:
    # every family holds both labels: holding out family i of each label would train on its other half
    items = [{"probe_id": f"p{i}", "label": "ab"[i % 2], "input_text": f"t{i}",
              "categories": {"scene": f"fam_{i // 10}"}} for i in range(80)]
    folds, how = make_folds(items, "scene", 4, 42)
    assert "grouped" in how["kind"] and not how["weaker"] and how["n_crossing"] == 8 and how["n_folds"] == 4
    for test in folds:
        held = {items[j]["categories"]["scene"] for j in test}
        assert not held & {items[j]["categories"]["scene"] for j in set(range(80)) - set(test.tolist())}
        assert {items[j]["label"] for j in test} == {"a", "b"}
    assert sorted(np.concatenate(folds).tolist()) == list(range(80))


def test_family_names_are_kept_whole_when_asked() -> None:
    # three-part names: the paper's rule reads both labels' four families as one each
    items = [{"probe_id": f"p{i}", "label": "ab"[i // 40], "input_text": f"t{i}",
              "categories": {"scene": f"{'ab'[i // 40]}_birds_{'xyzw'[i % 4]}"}} for i in range(80)]
    _, how = make_folds(items, "scene", 4, 42)
    assert how["n_folds"] == 1 and how["families"] == {"a": ["a_birds"], "b": ["b_birds"]}
    folds, how = make_folds(items, "scene", 4, 42, whole=True)
    assert how["n_folds"] == 4 and how["whole"] and len(how["families"]["a"]) == 4
    assert all({items[j]["label"] for j in test} == {"a", "b"} for test in folds)


def test_without_families_folds_keep_identical_texts_together_and_say_so() -> None:
    items = [{"probe_id": f"p{i}", "label": "ab"[i % 2], "input_text": f"text {i // 2}", "categories": {}}
             for i in range(40)]
    folds, how = make_folds(items, "scene", 4, 42)
    assert how["weaker"]
    for test in folds:
        texts = {items[j]["input_text"] for j in test}
        assert all(items[j]["input_text"] not in texts for j in set(range(40)) - set(test.tolist()))


def test_held_out_scores_tell_planted_classes_from_noise() -> None:
    rng = np.random.default_rng(0)
    labels = np.arange(80) % 2
    planted = (rng.normal(size=(2, 32)) * 6)[labels] + rng.normal(size=(80, 32))
    noise = rng.normal(size=(80, 32))
    items = [{"probe_id": f"p{i}", "label": "ab"[labels[i]], "input_text": f"t{i}", "categories": {}} for i in range(80)]
    folds, _ = make_folds(items, "scene", 4, 42)
    codes = axis_codes(items, {"label": ["a", "b"]})
    from services.lenses.fit import fit_reducer

    scores = {}
    for name, states in (("planted", planted), ("noise", noise)):
        settings = UmapSettings(n_neighbors=10, dimensions=4)
        embedding = fit_reducer(states.astype(np.float32), settings, 42)[1]
        profile = validate_layer(states.astype(np.float32), embedding, folds, codes, settings, 42, 2)
        scores[name] = profile["2"]
    assert scores["planted"]["heldout"]["label"]["kappa"] > 0.9
    assert scores["noise"]["heldout"]["label"]["kappa"] < 0.4
    assert set(scores["planted"]) == {"silhouette", "seed_ari", "agreement", "heldout"}


def test_validate_endpoint_writes_results_and_enables_the_held_out_k(client: TestClient, tmp_path: Path) -> None:  # noqa: F811
    run_job(client, client.post("/api/lenses", json=BODY).json()["job_id"])
    base = f"/api/sessions/{SESSION}/lenses/synth"
    assert client.get(f"{base}/validation").status_code == 404
    assert client.post(f"{base}/versions", json={"k_auto": "heldout"}).status_code == 400
    started = client.post(f"{base}/validate", json={"n_folds": 4, "seeds": 2, "workers": 1})
    assert started.status_code == 202
    from services.lenses.validate import validate_lens

    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    job_id = started.json()["job_id"]
    validate_lens(store.load(job_id).params, JobContext(store, job_id))
    result = client.get(f"{base}/validation").json()
    assert result["folds"]["weaker"] and set(result["layers"]) == {"0", "1", "2"}
    assert result["layers"]["0"]["2"]["heldout"]["label"]["kappa"] > 0.9
    listed = client.get(f"/api/sessions/{SESSION}/lenses").json()[0]
    assert set(listed["self_check"]) >= {"passed", "planted", "null"}  # 40 items: borderline by design
    assert listed["validation"]["best"]["kappa"] > 0.9
    made = client.post(f"{base}/versions", json={"k_auto": "heldout"}).json()
    assert made["k_source"][0] == "auto:heldout (selection-biased)"
