"""Tier-1 pure tests for the scenario library (world.staged.library), on a small library in a tmp dir."""
import pytest

from world.staged import library
from world.staged.scenario import ScenarioError
from tests.staged.test_engine import FIXTURE

MANIFEST = """\
id: fixture_set
version: 1
kind: staged
purpose: A fixture for the tests.
subsets:
  just_one: [fixture_stranger]
"""


@pytest.fixture
def root(tmp_path):
    (tmp_path / "fixture_set" / "scenarios").mkdir(parents=True)
    (tmp_path / "fixture_set" / "set.yaml").write_text(MANIFEST)
    for stem in ("fixture_stranger", "fixture_other"):
        (tmp_path / "fixture_set" / "scenarios" / f"{stem}.yaml").write_text(
            FIXTURE.replace("fixture_stranger", stem))
    (tmp_path / "_parked" / "scenarios").mkdir(parents=True)
    return tmp_path


def test_sets_are_listed_and_cited_by_id_and_version(root):
    [s] = library.list_sets(root)                       # _parked is skipped
    assert s.id == "fixture_set" and s.ref == "fixture_set@1" and s.kind == "staged"


def test_keys_are_set_and_file_never_a_room_name(root):
    s = library.load_set("fixture_set", root)
    assert s.keys() == ["fixture_set/fixture_other", "fixture_set/fixture_stranger"]
    assert s.keys("just_one") == ["fixture_set/fixture_stranger"]
    with pytest.raises(ScenarioError, match="no subset"):
        s.keys("missing")


def test_a_loaded_scenario_carries_its_set_and_file_hash(root):
    loaded = library.load("fixture_set/fixture_stranger", root)
    assert loaded.scenario.key == "fixture_set/fixture_stranger"
    assert loaded.set.ref == "fixture_set@1" and len(loaded.file_hash) == 64
    path = root / "fixture_set" / "scenarios" / "fixture_stranger.yaml"
    assert loaded.file_hash == library.file_hash(path)


@pytest.mark.parametrize("key, problem", [
    ("fixture_set", "<set_id>/<file>"),
    ("no_such_set/x", "no scenario set"),
    ("fixture_set/no_such_file", "no scenario 'no_such_file'"),
])
def test_a_bad_key_fails_with_the_reason(root, key, problem):
    with pytest.raises(ScenarioError, match=problem):
        library.load(key, root)


@pytest.mark.parametrize("manifest, problem", [
    (MANIFEST.replace("id: fixture_set", "id: other"), "does not match its folder"),
    (MANIFEST.replace("kind: staged", "kind: novel"), "kind must be one of"),
    (MANIFEST.replace("version: 1\n", ""), "needs a version"),
])
def test_a_bad_manifest_fails_with_the_reason(root, manifest, problem):
    (root / "fixture_set" / "set.yaml").write_text(manifest)
    with pytest.raises(ScenarioError, match=problem):
        library.load_set("fixture_set", root)
