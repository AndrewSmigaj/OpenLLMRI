"""Expert pipelines, hubs and the experts involved (DESIGN.md C7, E8), on planted routing: a planted
chain is found with its members and replicates, a trunk everyone shares is one pipeline, a branch
is two, random routing has none; converging groups make a hub and identical routing doesn't; a
planted expert is found beyond chance and shuffled labels find none."""

from typing import Any, Dict, List, Optional

import numpy as np
from test_lens_api import client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.jobs.kinds import JobContext
from services.lenses.routes import (
    compute_routes,
    dense,
    find_hubs,
    find_involved,
    find_pipelines,
    min_items,
)
from services.lenses.view import LensView

LAYERS = 10
EXPERTS = 32


def view(experts: np.ndarray, weights: np.ndarray, labels: List[str], families: Optional[List[str]] = None) -> LensView:  # type: ignore[type-arg]
    n = len(labels)
    items = [{"probe_id": f"p{i:03d}", "label": labels[i], "input_text": f"text {i}",
              "categories": {"scene": families[i]} if families else {}} for i in range(n)]
    return LensView(session_id="s", name="routes", legacy=False, version="v1", layers=list(range(LAYERS)), items=items,
                    nodes=np.zeros((n, LAYERS), dtype=np.int16), experts=experts.astype(np.int16),
                    weights=weights.astype(np.float32))


def routing(n: int, seed: int, main: Optional[Dict[int, Dict[int, int]]] = None, top: float = 0.55) -> Any:
    """Each item's four experts at every layer: random, unless `main[item][layer]` names its first,
    which then takes `top` of the weight."""
    rng = np.random.default_rng(seed)
    experts = np.zeros((n, LAYERS, 4), dtype=int)
    weights = np.zeros((n, LAYERS, 4))
    for i in range(n):
        for layer in range(LAYERS):
            first = (main or {}).get(i, {}).get(layer)
            others = rng.choice([e for e in range(EXPERTS) if e != first], size=4, replace=False)
            if first is None:
                experts[i, layer] = others
                weights[i, layer] = rng.dirichlet(np.ones(4))
            else:
                experts[i, layer] = [first, *others[:3]]
                weights[i, layer] = [top, *(np.ones(3) * (1 - top) / 3)]
    return experts, weights


def test_a_planted_chain_is_found_with_its_members_and_replicates() -> None:
    n = 200
    planted = {i: {layer: 7 for layer in range(2, 10)} for i in range(80)}
    experts, weights = routing(n, 1, planted)
    labels = ["a" if i < 80 else "b" for i in range(n)]
    routes = compute_routes(view(experts, weights, labels))
    found = [p for p in routes["pipelines"] if p["experts"] == [7] * len(p["experts"])]
    assert found, routes["pipelines"]
    chain = found[0]
    assert chain["layers"][0] == 2 and chain["layers"][-1] == 9
    assert abs(chain["members"] - 80) <= 8 and chain["replicated"]
    assert chain["makeup"]["label"]["a"] >= 0.9 * chain["members"]
    assert chain["rank1"] == 80  # each planted item has expert 7 first at every layer of the chain


def test_a_trunk_everyone_shares_is_one_pipeline_even_with_a_near_tie() -> None:
    n = 120
    experts = np.zeros((n, LAYERS, 4), dtype=int)
    weights = np.zeros((n, LAYERS, 4))
    rng = np.random.default_rng(2)
    for i in range(n):
        for layer in range(LAYERS):
            others = rng.choice(range(5, EXPERTS), size=2, replace=False)
            experts[i, layer] = [3, 4, *others]  # 3 and 4 almost tie, for every item
            weights[i, layer] = [0.36, 0.34, 0.15, 0.15]
    pipelines = find_pipelines(dense(view(experts, weights, ["a"] * n)), min_items(n))
    assert len(pipelines) == 1 and len(pipelines[0][0]) == LAYERS


def test_a_branch_is_two_pipelines_each_with_its_make_up() -> None:
    n = 160
    main = {i: {layer: 1 for layer in range(LAYERS)} for i in range(100)}  # a: expert 1 throughout
    main |= {i: {layer: (1 if layer < 4 else 2) for layer in range(LAYERS)} for i in range(100, 160)}  # b branches off
    experts, weights = routing(n, 3, main)
    labels = ["a" if i < 100 else "b" for i in range(n)]
    routes = compute_routes(view(experts, weights, labels))
    by_first = {p["experts"][-1]: p for p in routes["pipelines"]}
    assert set(by_first) == {1, 2}
    assert by_first[1]["makeup"]["label"].get("a", 0) >= 0.9 * by_first[1]["members"]
    assert by_first[2]["makeup"]["label"].get("b", 0) >= 0.9 * by_first[2]["members"]


def test_random_routing_has_no_pipeline() -> None:
    n = 300
    experts, weights = routing(n, 4)
    assert find_pipelines(dense(view(experts, weights, ["a"] * n)), min_items(n)) == []


def test_converging_groups_make_a_hub_and_identical_routing_does_not() -> None:
    n = 100
    experts = np.zeros((n, LAYERS, 4), dtype=int)
    weights = np.zeros((n, LAYERS, 4))
    for i in range(n):
        for layer in range(LAYERS):
            if layer == 4:  # the two groups arrive from different experts
                experts[i, layer] = [1, 2, 3, 4] if i < 50 else [11, 12, 13, 14]
            else:
                experts[i, layer] = [20, 21, 22, 23]  # then meet at expert 20, as at every other layer
            weights[i, layer] = [0.7, 0.1, 0.1, 0.1]
    hubs = find_hubs(dense(view(experts, weights, ["a"] * n)), min_items(n))
    assert {h["li"] for h in hubs} == {5} and (5, 20) in [(h["li"], h["expert"]) for h in hubs]  # each item's four meet there
    assert all(h["sources"] > 1.9 for h in hubs)
    experts[50:, 4] = [1, 2, 3, 4]  # now every item arrives the same way
    assert find_hubs(dense(view(experts, weights, ["a"] * n)), min_items(n)) == []


def test_a_planted_expert_is_found_beyond_chance_and_shuffled_labels_find_none() -> None:
    n = 160
    main = {i: {6: 9} for i in range(80)}  # class a leans on expert 9 at layer 6
    experts, weights = routing(n, 5, main, top=0.7)
    labels = ["a" if i < 80 else "b" for i in range(n)]
    found = find_involved(dense(view(experts, weights, labels)), view(experts, weights, labels).items,
                          {"label": ["a", "b"]}, "scene", 0)
    top = found["label"]["a"]["experts"][0]
    assert (top["li"], top["expert"], top["favours"]) == (6, 9, "a") and top["auc"] > 0.9
    shuffled = list(np.random.default_rng(6).permutation(labels))
    none = find_involved(dense(view(experts, weights, shuffled)), view(experts, weights, shuffled).items,
                         {"label": ["a", "b"]}, "scene", 0)
    assert none["label"]["a"]["experts"] == [] and none["label"]["b"]["experts"] == []


def test_families_move_together_when_each_holds_one_value() -> None:
    n = 120
    experts, weights = routing(n, 7)
    labels = ["a" if i < 60 else "b" for i in range(n)]
    families = [f"{labels[i]}_f{i % 6}" for i in range(n)]
    found = find_involved(dense(view(experts, weights, labels, families)), view(experts, weights, labels, families).items,
                          {"label": ["a", "b"]}, "scene", 0)
    assert found["label"]["a"]["permuted"] == "families"


def test_a_build_writes_its_routes_and_the_routes_are_served_with_nodes(client: Any) -> None:  # noqa: F811
    from services.lenses.routes import routes_job

    built = client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10, "k": 2,
                                              "workers": 1})
    run_job(client, built.json()["job_id"])
    served = client.get(f"/api/sessions/{SESSION}/lenses/synth/routes")
    assert served.status_code == 200
    body = served.json()
    assert body["version"] == "v1" and body["n_items"] == 40 and "involved" in body
    for pipeline in body["pipelines"]:
        assert len(pipeline["nodes"]) == len(pipeline["layers"])
        assert all(sum(at.values()) == pipeline["members"] for at in pipeline["nodes"])
    again = client.post(f"/api/sessions/{SESSION}/lenses/synth/routes", json={"created_by": "test"})
    assert again.status_code == 202
    store = client.app.state.jobs.store
    assert routes_job(store.load(again.json()["job_id"]).params, JobContext(store, again.json()["job_id"]))["seconds"] >= 0
    assert client.post(f"/api/sessions/{SESSION}/lenses/nope/routes", json={}).status_code == 404


def test_the_weighted_expert_view_holds_every_items_whole_weight(client: Any) -> None:  # noqa: F811
    run_job(client, client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10,
                                                     "k": 2, "workers": 1}).json()["job_id"])
    flows = client.get(f"/api/sessions/{SESSION}/lenses/synth/expert-flows", params={"rank": 0}).json()
    assert flows["weighted"] is True
    for layer in flows["layers"]:
        assert abs(sum(n["count"] for n in flows["nodes"] if n["layer"] == layer) - 40) < 0.05  # four weights sum to 1
    assert all(link["count"] >= 0.5 for link in flows["links"])
