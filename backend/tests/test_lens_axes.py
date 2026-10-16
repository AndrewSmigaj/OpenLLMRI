"""The axes analysis (DESIGN.md C8): planted attributes on their own directions are recovered and a
designed but unencoded one isn't; attributes correlated by design but encoded apart keep partial
axes near 90°; an attribute carried only by family offsets isn't recovered held out; noise
recovers nothing; validation scores decoys without changing its own results."""

from typing import Any, Dict, List

import numpy as np
from test_lens_api import client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.lenses.axes import (
    attributes,
    decoy_sets,
    decoys,
    geometry,
    groups_of,
    partial_axes,
    score_layer,
    thresholds,
)
from services.lenses.validate import make_folds

DIM = 60


def items_of(rows: List[Dict[str, str]], family: List[str]) -> List[Dict[str, Any]]:
    return [{"probe_id": f"p{i}", "label": None, "input_text": f"text {i}",
             "categories": {**row, "scene": family[i]}} for i, row in enumerate(rows)]


def design(n: int, seed: int, correlated: bool = False) -> Any:
    """Three two-valued attributes: a and b encoded on their own directions, c designed but not
    encoded. With `correlated`, b follows a 90% of the time."""
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 2, n)
    b = np.where(rng.random(n) < 0.9, a, 1 - a) if correlated else rng.integers(0, 2, n)
    c = rng.integers(0, 2, n)
    basis = np.linalg.qr(rng.normal(size=(DIM, DIM)))[0]
    states = rng.normal(size=(n, DIM)) + 3.0 * np.outer(2 * a - 1, basis[0]) + 3.0 * np.outer(2 * b - 1, basis[1])
    rows = [{"a": "ab"[x], "b": "ab"[y], "c": "ab"[z]} for x, y, z in zip(a, b, c)]
    return states, rows, basis


def codes_of(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    return attributes(items_of(rows, ["f"] * len(rows)), {"a": ["a", "b"], "b": ["a", "b"], "c": ["a", "b"]})


def test_planted_attributes_are_recovered_and_an_unencoded_one_is_not() -> None:
    n = 200
    states, rows, _ = design(n, 1)
    items = items_of(rows, [f"f{i % 10}" for i in range(n)])
    real = codes_of(rows)
    groups, _ = groups_of(items, "scene")
    rng = np.random.default_rng(0)
    sets = {"real": real, **{f"decoy{d}": {axis: decoys(c, groups, rng, 1)[0] for axis, c in real.items()} for d in range(5)}}
    folds = [np.arange(n)[i::5] for i in range(5)]
    scores = score_layer(states.astype(np.float32), folds, sets, k=4, n_neighbors=10, seed=0, probe_sets=list(sets))
    limits = thresholds([scores], ["a", "b", "c"])
    for technique in ("probe", "directions"):
        found = scores[technique]["real"]
        assert found["a"] > limits[technique]["a"] and found["b"] > limits[technique]["b"], technique
        assert found["a"] > 0.8 and found["b"] > 0.8, technique
        assert found["c"] < 0.2, technique  # at chance: one layer's five decoys set too rough a line to test against


def test_attributes_correlated_by_design_but_encoded_apart_keep_their_axes_apart() -> None:
    states, rows, basis = design(400, 2, correlated=True)
    axes = partial_axes(states, codes_of(rows))
    cos = abs(float(axes["a"][0] @ axes["b"][0]) / (np.linalg.norm(axes["a"][0]) * np.linalg.norm(axes["b"][0])))
    assert cos < 0.2  # near 90°, although a and b agree 90% of the time
    found = geometry(states, codes_of(rows), {"a": ["a", "b"], "b": ["a", "b"], "c": ["a", "b"]}, np.random.default_rng(0))
    assert found["names"] == ["a", "b", "c"] and len(found["null"]) == 3
    # under permuted design rows the two attributes' errors are anti-correlated, so their null band
    # sits well below zero, and the real axes, near 90°, lie above it
    assert found["null_cosines"]["high"][0][1] < -0.4 < found["cosines"][0][1]


def test_a_nested_attribute_gets_its_whole_effect_not_a_share_of_the_category() -> None:
    rng = np.random.default_rng(5)
    n = 400
    category = rng.integers(0, 4, n)
    animate = (category < 2).astype(int)  # a function of the category, as animacy is
    basis = np.linalg.qr(rng.normal(size=(DIM, DIM)))[0]
    own = 2.0 * np.stack([basis[1], -basis[1], basis[2], -basis[2]])  # each category's own offset, none for animacy
    states = rng.normal(size=(n, DIM)) + 3.0 * np.outer(2 * animate - 1, basis[0]) + own[category]
    found = partial_axes(states, {"category": category, "animacy": animate})["animacy"][0]
    assert abs(found @ basis[0]) / np.linalg.norm(found) > 0.95
    assert abs(np.linalg.norm(found) - 6.0) < 0.6  # the planted difference, not a share of it


def test_an_attribute_carried_only_by_family_offsets_is_not_recovered_held_out() -> None:
    rng = np.random.default_rng(3)
    n, families = 240, 24
    family = np.arange(n) % families
    value = (family < families // 2).astype(int)  # each family holds one value
    offsets = rng.normal(size=(families, DIM)) * 3.0  # each family sits apart, the value adds nothing
    states = (rng.normal(size=(n, DIM)) + offsets[family]).astype(np.float32)
    rows = [{"v": "ab"[x]} for x in value]
    items = items_of(rows, [f"{'ab'[v]}_f{f}" for v, f in zip(value, family)])
    folds, how = make_folds(items, "scene", 5, 0)
    assert not how["weaker"]
    real = attributes(items, {"v": ["a", "b"]})
    groups, given_per = groups_of(items, "scene")
    assert given_per == "families"
    sets = {"real": real, **{f"decoy{d}": {"v": decoys(real["v"], groups, rng, 1)[0]} for d in range(19)}}
    scores = score_layer(states, folds, sets, k=2, n_neighbors=10, seed=0, probe_sets=list(sets))
    limits = thresholds([scores], ["v"])
    for technique in ("probe", "directions"):  # within what decoys carried by the same families reach
        assert scores[technique]["real"]["v"] <= limits[technique]["v"], technique


def test_noise_recovers_nothing() -> None:
    rng = np.random.default_rng(4)
    n = 150
    states = rng.normal(size=(n, DIM)).astype(np.float32)
    rows = [{"a": "ab"[x], "b": "ab"[y], "c": "ab"[z]} for x, y, z in rng.integers(0, 2, (n, 3))]
    items = items_of(rows, [f"f{i % 10}" for i in range(n)])
    real = codes_of(rows)
    groups, _ = groups_of(items, "scene")
    sets = {"real": real, **{f"decoy{d}": {axis: decoys(c, groups, rng, 1)[0] for axis, c in real.items()} for d in range(5)}}
    folds = [np.arange(n)[i::5] for i in range(5)]
    scores = score_layer(states, folds, sets, k=3, n_neighbors=10, seed=0, probe_sets=list(sets))
    assert all(abs(v) < 0.2 for technique in ("probe", "directions", "component") for v in scores[technique]["real"].values())


def test_decoys_keep_proportions_and_families_together() -> None:
    codes = np.array([0] * 30 + [1] * 10 + [-1] * 2)
    groups = np.arange(42) // 2  # pairs
    found = decoys(codes, groups, np.random.default_rng(0), 3)
    for d in found:
        assert (d[-2:] == -1).all() and (d[:40] >= 0).all()
        assert all(d[i] == d[i + 1] for i in range(0, 40, 2))  # a group shares its value


def _word_design() -> tuple:
    """160 words in 8 families, four under each of two labels: mood follows the label (mostly 1 under
    label 1) and varies within families; kind is constant within each family, either way under each
    label; living is the label itself (nested in it)."""
    rng = np.random.default_rng(0)
    label = np.repeat([0, 1], 80)
    families = np.repeat(np.arange(8), 20)
    mood = np.where(label == 1, rng.random(160) < 0.8, rng.random(160) < 0.2).astype(int)
    kind = np.repeat([0, 1, 0, 1, 1, 0, 1, 0], 20)
    return {"label": label, "mood": mood, "kind": kind, "living": label.copy()}, families, np.arange(160)


def test_decoys_keep_each_attributes_link_to_the_label_at_its_own_grain() -> None:
    codes, families, texts = _word_design()
    sets, record = decoy_sets(codes, families, texts, seed=1)
    assert record["within"] == "label" and record["nested"] == ["living"]
    assert record["grain"] == {"kind": "families", "label": "families", "living": "families", "mood": "texts"}
    label = codes["label"]
    for decoy in sets["mood"]:  # per word, in mood's proportions within each label value
        for value in (0, 1):
            assert abs(decoy[label == value].mean() - codes["mood"][label == value].mean()) < 0.15
    for decoy in sets["kind"]:  # one value per family
        assert all(len(set(decoy[families == f].tolist())) == 1 for f in range(8))
    again, _ = decoy_sets(codes, families, texts, seed=1)  # validation and the axes analysis draw the same
    assert all((a == b).all() for axis in sets for a, b in zip(sets[axis], again[axis]))


def test_a_reader_of_the_label_alone_earns_mood_no_credit_beyond_its_decoys() -> None:
    from sklearn.metrics import cohen_kappa_score

    codes, families, texts = _word_design()
    guess = codes["label"].copy()  # knows only the label: label 1 means mood 1
    real = cohen_kappa_score(codes["mood"], guess)
    within, _ = decoy_sets(codes, families, texts, seed=2, count=200)
    fair = [cohen_kappa_score(d, guess) for d in within["mood"]]
    old = [cohen_kappa_score(d, guess) for d in decoys(codes["mood"], texts, np.random.default_rng(2), 200)]
    assert np.percentile(fair, 5) < real < np.percentile(fair, 95)  # the label's credit is shared
    assert real > np.percentile(old, 95)  # decoys in overall proportions would have counted it


def test_the_stricter_line_counts_fewer_and_drops_a_weak_attribute() -> None:
    from services.lenses.axes import recovered, strict_limits

    analysis = {"attributes": {"strong": ["a", "b"], "weak": ["a", "b"]},
                "scores": {"probe": [{"real": {"strong": 0.9, "weak": 0.8}}, {"real": {"strong": 0.6, "weak": 0.3}}],
                           "raw_ward": [{"real": {"strong": 0.7, "weak": 0.2}}, {"real": {"strong": 0.3, "weak": 0.1}}]},
                "thresholds": {"probe": {"strong": 0.1, "weak": 0.1}, "raw_ward": {"strong": 0.05, "weak": 0.05}}}
    strict = strict_limits(analysis)
    assert strict == {"strong": 0.45, "weak": 0.4}
    lenient, firm = recovered(analysis), recovered(analysis, strict)
    assert lenient["raw_ward"] == [2, 2] and firm["raw_ward"] == [1, 0]
    assert lenient["probe"] == [2, 2] and firm["probe"] == [2, 1]  # the probe falls below its own best
    assert all(f <= n for t in firm for f, n in zip(firm[t], lenient[t]))


def test_validation_scores_decoys_and_keeps_its_own_results(client: Any) -> None:  # noqa: F811
    from services.jobs.kinds import JobContext
    from services.lenses.validate import validate_lens

    run_job(client, client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10,
                                                     "k": 2, "workers": 1}).json()["job_id"])
    started = client.post(f"/api/sessions/{SESSION}/lenses/synth/validate", json={"seeds": 1, "workers": 1})
    store = client.app.state.jobs.store
    validate_lens(store.load(started.json()["job_id"]).params, JobContext(store, started.json()["job_id"]))
    record = client.get(f"/api/sessions/{SESSION}/lenses/synth/validation").json()
    entry = record["layers"]["0"]["2"]
    assert set(entry["heldout"]) == {"label", "register"}  # the real axes only
    assert len(entry["decoys"]["label"]["kappa"]) == 5 and record["decoys"]["count"] == 5


def test_the_family_field_groups_items_and_is_never_an_attribute(client: Any) -> None:  # noqa: F811
    from services.jobs.kinds import JobContext
    from services.lenses.axes import run_axes

    run_job(client, client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10,
                                                     "k": 2, "workers": 1}).json()["job_id"])
    started = client.post(f"/api/sessions/{SESSION}/lenses/synth/axes", json={"family_field": "register", "workers": 1})
    store = client.app.state.jobs.store
    run_axes(store.load(started.json()["job_id"]).params, JobContext(store, started.json()["job_id"]))
    found = client.get(f"/api/sessions/{SESSION}/lenses/synth/axes").json()
    assert list(found["attributes"]) == ["label"] and found["decoys"]["given_per"] == "families"
    assert "grouped" in found["folds"]["kind"]  # each register holds both labels, so whole registers are held out
    assert found["umap"] is None and found["recovered"]["probe"]  # not validated: no UMAP rows
