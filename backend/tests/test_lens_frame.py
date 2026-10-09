"""The 3-D view's frame (DESIGN.md E5): a lens's own embedding on its three main directions, each
layer turned onto the one before by a rotation or a reflection, read items in the same frame."""

from typing import Any

import numpy as np
from fastapi.testclient import TestClient
from scipy.spatial.distance import pdist
from test_lens_api import client, run_job  # noqa: F401  (client is a fixture)
from test_lenses import SESSION

from services.jobs.kinds import JobContext
from services.jobs.store import JobStore
from services.lenses.frame import lens_frame, procrustes


def orthogonal(rng: Any, reflect: bool) -> Any:
    q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if (np.linalg.det(q) < 0) != reflect:
        q[:, 0] *= -1
    return q


def test_procrustes_recovers_a_rotation_and_a_reflection() -> None:
    rng = np.random.default_rng(0)
    points = rng.normal(size=(50, 3))
    for reflect in (False, True):
        turn = orthogonal(rng, reflect)
        assert np.allclose(procrustes(points, points @ turn), turn, atol=1e-8)


def test_bases_are_orthonormal_and_keep_every_distance_of_the_main_directions() -> None:
    from sklearn.decomposition import PCA

    rng = np.random.default_rng(1)
    three = rng.normal(size=(40, 3)) * [3.0, 2.0, 1.0]
    six = rng.normal(size=(40, 6)) * [5.0, 3.0, 2.0, 0.5, 0.3, 0.1]
    frame = lens_frame([three, six])
    for li, points in enumerate((three, six)):
        basis = frame.bases[li]
        assert np.allclose(basis.T @ basis, np.eye(3), atol=1e-8)
    # at three dimensions the embedding itself, turned; above it, the PCA scores, turned
    assert np.allclose(pdist(frame.project(0, three)), pdist(three), atol=1e-8)
    assert np.allclose(pdist(frame.project(1, six)), pdist(PCA(3).fit_transform(six)), atol=1e-6)
    assert frame.shares[0] == 1.0 and 0.9 < frame.shares[1] < 1.0
    again = lens_frame([three, six])
    assert all(np.array_equal(a, b) for a, b in zip(again.bases, frame.bases))  # it repeats


def test_a_turned_copy_of_a_layer_lines_up_with_it() -> None:
    rng = np.random.default_rng(2)
    first = rng.normal(size=(60, 3)) * [3.0, 2.0, 1.0]
    second = first @ orthogonal(rng, True) + 5.0  # moved and turned, with a reflection
    frame = lens_frame([first, second])
    assert np.allclose(frame.project(1, second), frame.project(0, first), atol=1e-8)


def test_the_trajectory_route_serves_the_frame_and_a_reading_in_it(client: TestClient) -> None:  # noqa: F811
    from services.lenses.readout import read_lens

    run_job(client, client.post("/api/lenses", json={"session_id": SESSION, "name": "synth", "n_neighbors": 10,
                                                     "k": 2, "workers": 1}).json()["job_id"])
    route = f"/api/sessions/{SESSION}/lenses/synth/trajectory"
    served = client.get(route).json()
    assert served["fit"] == "lens" and served["layers"] == [0, 1, 2] and len(served["share"]) == 3
    points = np.array(served["points"])
    assert points.shape == (40, 3, 3) and len(served["items"]) == 40
    store: JobStore = client.app.state.jobs.store  # type: ignore[attr-defined]
    started = client.post(f"/api/sessions/{SESSION}/lenses/synth/readings", json={"created_by": "test"}).json()
    read_lens(store.load(started["job_id"]).params, JobContext(store, started["job_id"]))
    with_read = client.get(route, params={"reading": started["key"]}).json()
    assert np.allclose(np.array(with_read["read"]["points"]), points, atol=1e-3)  # the lens's own items, read
    assert client.get(route, params={"reading": "nope"}).status_code == 404
