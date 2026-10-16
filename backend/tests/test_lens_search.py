"""Tuning lenses (DESIGN.md C3, C4): the test split, the selection folds, the choice, an end-to-end
search that never lets a test item into the selection, settings per layer, and the endpoints."""

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pytest
from fastapi.testclient import TestClient
from test_lens_api import client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION, build, lake, lens  # noqa: F401  (lake is a fixture)

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.search import (
    choose,
    merge_folds,
    rescore_search,
    run_search,
    split_test,
    split_tests,
    tuning_headline,
)
from services.lenses.store import LensSettings, UmapSettings


def family_items(labels: int = 3, families: int = 5, per_family: int = 4) -> List[Dict[str, Any]]:
    return [{"probe_id": f"p{label}{family}{i}", "label": f"c{label}", "input_text": f"w{label}{family}{i}",
             "categories": {"family": f"c{label}_f{family}"}}
            for label in range(labels) for family in range(families) for i in range(per_family)]


def test_the_test_portion_holds_whole_families_the_same_share_of_every_label() -> None:
    items = family_items()
    codes = np.array([int(item["label"][1]) for item in items])
    test, how = split_test(items, codes, "family", 0.2, 7)
    assert not how["weaker"] and how["kind"] == "scene families"
    held = {items[j]["categories"]["family"] for j in test}
    assert len(held) == 3 and {name.split("_")[0] for name in held} == {"c0", "c1", "c2"}  # one family per label
    rest = {items[j]["categories"]["family"] for j in set(range(len(items))) - set(test.tolist())}
    assert not held & rest  # no family on both sides
    again, _ = split_test(items, codes, "family", 0.2, 7)
    assert again.tolist() == test.tolist()  # the seed decides


def test_when_a_family_holds_several_labels_the_test_portion_takes_it_whole() -> None:
    items = [{"probe_id": f"p{i}", "label": f"c{i % 3}", "input_text": f"w{i}",
              "categories": {"family": f"fam_{i // 6}"}} for i in range(90)]  # 15 families, three labels each
    codes = np.arange(90) % 3
    test, how = split_test(items, codes, "family", 0.2, 7)
    assert "grouped" in how["kind"] and not how["weaker"] and 0.1 < len(test) / 90 < 0.35
    held = {items[j]["categories"]["family"] for j in test}
    assert not held & {items[j]["categories"]["family"] for j in set(range(90)) - set(test.tolist())}


def test_the_first_draw_is_the_single_split_of_before() -> None:
    from sklearn.model_selection import StratifiedGroupKFold

    items = family_items(families=6)
    codes = np.array([int(item["label"][1]) for item in items])
    # whole families per label, as the single split drew them: one seeded permutation per label in turn
    rng = np.random.default_rng(7)
    held = {}
    for label in sorted({item["label"] for item in items}):
        found = sorted({item["categories"]["family"] for item in items if item["label"] == label})
        take = min(len(found) - 2, max(1, round(0.2 * len(found))))
        held[label] = {found[i] for i in rng.permutation(len(found))[:take]}
    before = [j for j, item in enumerate(items) if item["categories"]["family"] in held[item["label"]]]
    first, _ = split_tests(items, codes, "family", 0.2, 7, draws=4)[0]
    assert first.tolist() == before
    # without families: the splitter's first fold
    flat = [{"probe_id": f"p{i}", "label": "ab"[i % 2], "input_text": f"text {i // 2}", "categories": {}}
            for i in range(60)]
    flat_codes = np.arange(60) % 2
    _, fold = next(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=3).split(
        np.zeros(60), flat_codes, groups=[item["input_text"] for item in flat]))
    assert split_tests(flat, flat_codes, None, 0.2, 3, draws=3)[0][0].tolist() == sorted(fold.tolist())


def test_later_draws_hold_out_other_families_until_a_label_runs_out() -> None:
    items = family_items(families=5)  # one family per label per draw: five disjoint draws, then round again
    codes = np.array([int(item["label"][1]) for item in items])
    draws = split_tests(items, codes, "family", 0.2, 7, draws=6)
    assert [info["draw"] for _, info in draws] == [1, 2, 3, 4, 5, 6]
    seen = [{items[j]["categories"]["family"] for j in test} for test, _ in draws]
    assert all(not seen[a] & seen[b] for a in range(5) for b in range(a + 1, 5))  # disjoint
    assert set().union(*seen[:5]) == {item["categories"]["family"] for item in items}  # every family once
    assert seen[5] == seen[0] and draws[5][1]["repeated"] == ["c0", "c1", "c2"] and not draws[4][1]["repeated"]
    for test, _ in draws:  # each still holds out whole families of every label
        assert {items[j]["label"] for j in test} == {"c0", "c1", "c2"}


def test_without_families_the_test_share_is_stratified_and_keeps_texts_together() -> None:
    items = [{"probe_id": f"p{i}", "label": "ab"[i % 2], "input_text": f"text {i // 2}", "categories": {}}
             for i in range(60)]
    codes = np.arange(60) % 2
    test, how = split_test(items, codes, "family", 0.2, 3)
    assert how["weaker"] and 0.1 < len(test) / 60 < 0.35
    texts = {items[j]["input_text"] for j in test}
    assert all(items[j]["input_text"] not in texts for j in set(range(60)) - set(test.tolist()))


def test_many_family_folds_merge_into_fewer_each_still_whole_families() -> None:
    folds = [np.array([3 * i, 3 * i + 1, 3 * i + 2]) for i in range(12)]
    merged, before = merge_folds(folds, 5)
    assert before == 12 and len(merged) == 5
    assert sorted(np.concatenate(merged).tolist()) == list(range(36))
    assert all(set(fold.tolist()) <= set(merged[i % 5].tolist()) for i, fold in enumerate(folds))
    same, none = merge_folds(folds[:4], 5)
    assert none is None and len(same) == 4


def test_the_choice_takes_the_best_ami_then_fewer_nodes_then_the_simpler_map() -> None:
    configs = [UmapSettings(n_neighbors=15, dimensions=6), UmapSettings(n_neighbors=15, dimensions=3),
               UmapSettings(n_neighbors=50, dimensions=3)]

    def s(ami: float) -> Dict[str, float]:
        return {"ami": ami, "kappa": 0.0, "accuracy": 0.0, "worst_fold": 0.0}

    scores = {0: {2: s(0.5), 3: s(0.6)}, 1: {3: s(0.6), 4: s(0.6)}, 2: {3: s(0.6)}}
    won, runners = choose(scores, configs, [0, 1, 2])
    # a three-way tie at k 3: fewer dimensions wins, then more neighbours
    assert won == (2, 3)
    assert runners == [(1, 3), (0, 3)]
    won, _ = choose(scores, configs, [0, 1])  # a setting that failed the self-check doesn't count
    assert won == (1, 3)


class _Ctx(JobContext):
    """A job context that remembers the stage, for the leakage spy."""
    stage = ""

    def progress(self, stage: str, done: int, total: int) -> None:
        type(self).stage = stage
        super().progress(stage, done, total)


def test_a_search_never_fits_on_test_items_and_finds_the_planted_k(lake: Path, monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F811
    import services.lenses.fit as fit

    build(lake)
    fits: List[tuple] = []
    original = fit.fit_reducer

    def spy(states: np.ndarray, *args: Any, **kwargs: Any) -> Any:
        fits.append((_Ctx.stage, {row.tobytes() for row in np.asarray(states, dtype=np.float32)}))
        return original(states, *args, **kwargs)

    monkeypatch.setattr(fit, "fit_reducer", spy)
    store = JobStore(lake / "_jobs")
    params = {"session_id": SESSION, "source_lens": "synth", "workers": 1, "draws": 2,
              "grid": {"n_neighbors": [5, 10], "dimensions": [3], "min_dist": [0.1]}}
    job = store.submit("lens_search", "cpu", params, created_by="test")
    result = run_search(params, _Ctx(store, job.id))
    assert result["name"] == "synth-tuned" and result["draws"] == 2

    record = json.loads((lens(lake, "synth-tuned") / "search.json").read_text())
    from services.lenses.data import load_states

    assert record["draws"][0]["test"]["probe_ids"] == record["split"]["test"]["probe_ids"]  # draw 1 is the split
    for draw in record["draws"]:  # no draw's selection or test-stage fit holds its own test items
        test_rows = {row.tobytes() for layer_rows in load_states(SESSION, draw["test"]["probe_ids"]).values()
                     for row in np.asarray(layer_rows, dtype=np.float32)}
        stage = f"draw {draw['draw']} of 2: "
        searched = [rows for name, rows in fits if name == f"{stage}searching"]
        assert searched and all(not rows & test_rows for rows in searched)
        tested = [rows for name, rows in fits if name == f"{stage}testing"]
        assert tested and all(not rows & test_rows for rows in tested)
    assert not set(record["draws"][0]["test"]["probe_ids"]) & set(record["draws"][1]["test"]["probe_ids"])
    spread = record["spread"][0]["winner"]["ami"]
    assert spread["n"] == 2 and spread["min"] <= spread["mean"] <= spread["max"]
    assert record["split"]["test"]["weaker"]  # the synthetic capture names no families
    for winner in record["winners"]:
        assert winner["k"] == 2 and winner["test"]["ami"] > 0.9  # two planted classes, found on the test items
    manifest = json.loads((lens(lake, "synth-tuned") / "lens.json").read_text())
    assert len(manifest["settings"]["per_layer"]) == 3
    version = json.loads((lens(lake, "synth-tuned") / "v1" / "version.json").read_text())
    assert version["k_per_layer"] == [2, 2, 2] and version["k_source"][0].startswith("tuned")
    assert (lens(lake, "synth-tuned") / "validation.json").exists()


def test_settings_per_layer_survive_the_build_and_old_lenses_read_as_before(lake: Path) -> None:  # noqa: F811
    import joblib

    per_layer = [{"n_neighbors": 5, "dimensions": 3, "min_dist": 0.0},
                 {"n_neighbors": 10, "dimensions": 4, "min_dist": 0.1},
                 {"n_neighbors": 8, "dimensions": 2, "min_dist": 0.2}]
    build(lake, name="perlayer", per_layer=per_layer)
    folder = lens(lake, "perlayer")
    manifest = json.loads((folder / "lens.json").read_text())
    assert manifest["settings"]["per_layer"] == [dict(s, metric="euclidean") for s in per_layer]
    for li, wanted in enumerate(per_layer):
        reducer = joblib.load(folder / "fit" / f"umap_L{li:02d}.joblib")
        assert (reducer.n_neighbors, reducer.n_components, reducer.min_dist) == \
            (wanted["n_neighbors"], wanted["dimensions"], wanted["min_dist"])
    embedding = np.load(folder / "fit" / "embed.npz")["embedding"]
    assert embedding.shape[2] == 4 and not embedding[2, :, 2:].any()  # padded to the widest with zeros
    assert len(manifest["self_check"]["per_settings"]) == 3  # one check per distinct setting
    old = LensSettings.model_validate({"n_neighbors": 15, "dimensions": 6, "min_dist": 0.1, "seed": 42})
    assert old.at(0) == UmapSettings(n_neighbors=15, dimensions=6, min_dist=0.1) and old.per_layer is None


def test_the_held_out_best_k_follows_ami() -> None:
    from services.lenses.versions import heldout_best

    def k_entry(kappa: float, ami: float) -> Dict[str, Any]:
        return {"heldout": {"label": {"kappa": kappa, "ami": ami, "accuracy": 0.0, "worst_fold": 0.0}}}

    validation = {"layers": {"0": {"2": k_entry(0.5, 0.6), "9": k_entry(0.7, 0.4)}}}
    assert heldout_best(validation) == {"0": 2}


def test_tuning_endpoints(client: TestClient) -> None:  # noqa: F811
    from test_lens_api import BODY

    assert client.post("/api/sessions/session_synth/lenses/nothing/tune", json={}).status_code == 404
    run_job(client, client.post("/api/lenses", json=BODY).json()["job_id"])
    assert client.post("/api/sessions/session_synth/lenses/synth/tune", json={"target_axis": "colour"}).status_code == 400
    assert client.post("/api/sessions/session_synth/lenses/synth/tune", json={"k_min": 5, "k_max": 3}).status_code == 400
    too_many = {"grid": {"n_neighbors": list(range(2, 30)), "dimensions": [2, 3, 4], "min_dist": [0.1]}}
    assert client.post("/api/sessions/session_synth/lenses/synth/tune", json=too_many).status_code == 400
    assert client.get("/api/sessions/session_synth/lenses/synth/search").status_code == 404
    started = client.post("/api/sessions/session_synth/lenses/synth/tune", json={"workers": 1})
    assert started.status_code == 202 and started.json()["name"] == "synth-tuned"
    assert client.post("/api/sessions/session_synth/lenses/synth/tune", json={}).status_code == 409  # already queued


def _tune(root: Path, name: str, workers: int, draws: int) -> Dict[str, Any]:
    store = JobStore(root / "_jobs")
    params = {"session_id": SESSION, "source_lens": "synth", "name": name, "workers": workers, "draws": draws,
              "grid": {"n_neighbors": [5, 10], "dimensions": [3], "min_dist": [0.1]}}
    run_search(params, JobContext(store, store.submit("lens_search", "cpu", params, created_by="test").id))
    return json.loads((lens(root, name) / "search.json").read_text())


def test_a_search_gives_the_same_result_with_one_worker_or_two(lake: Path) -> None:  # noqa: F811
    build(lake)
    one, two = _tune(lake, "synth-one", 1, 1), _tune(lake, "synth-two", 2, 1)
    assert one["selection"] == two["selection"]
    assert [(w["settings"], w["k"], w["test"]) for w in one["winners"]] == \
        [(w["settings"], w["k"], w["test"]) for w in two["winners"]]


def test_a_rescore_adds_draws_when_the_first_reproduces_and_refuses_otherwise(lake: Path) -> None:  # noqa: F811
    build(lake)
    before = _tune(lake, "synth-tuned", 1, 1)
    store = JobStore(lake / "_jobs")
    params = {"session_id": SESSION, "name": "synth-tuned", "draws": 3, "workers": 1}
    rescore_search(params, JobContext(store, store.submit("lens_rescore", "cpu", params, created_by="test").id))
    after = json.loads((lens(lake, "synth-tuned") / "search.json").read_text())
    assert len(after["draws"]) == 3 and after["rescored"]["earlier"] == "search.single.json"
    assert after["split"]["test"]["probe_ids"] == before["split"]["test"]["probe_ids"]
    assert [(w["settings"], w["k"]) for w in after["winners"]] == [(w["settings"], w["k"]) for w in before["winners"]]
    assert json.loads((lens(lake, "synth-tuned") / "search.single.json").read_text()) == before

    altered = dict(after, winners=[dict(w, k=w["k"] + 1) for w in after["winners"]])  # a record it can't reproduce
    (lens(lake, "synth-tuned") / "search.json").write_text(json.dumps(altered))
    with pytest.raises(ValueError, match="doesn't reproduce"):
        rescore_search(params, JobContext(store, store.submit("lens_rescore", "cpu", params, created_by="test").id))


def test_an_older_search_record_reads_with_one_draw(tmp_path: Path) -> None:
    record = {"source": {"name": "a", "version": "v1"}, "target_axis": "label",
              "winners": [{"layer": 3, "k": 2, "selection": {"ami": 0.5}, "test": {"ami": 0.4}}],
              "split": {"test": {"n_items": 10, "weaker": True}}}
    (tmp_path / "search.json").write_text(json.dumps(record))
    headline = tuning_headline(tmp_path)
    assert headline is not None and headline["draws"] == 1 and headline["test_spread"] is None
