"""The runner's view of the scenario library: a scenario by its key, with its set reference and its
file's hash; a set's keys and a subset's; and the library in the repo."""
import hashlib

import pytest

from services.agent.scenario_library import ScenarioNotFoundError, load_scenario, scenario_keys

FILE = "name: one\ncondition: friend\ntarget_words: [person]\n"


@pytest.fixture
def library(tmp_path):
    (tmp_path / "s" / "scenarios").mkdir(parents=True)
    (tmp_path / "s" / "set.yaml").write_text("id: s\nversion: 3\nkind: staged\nsubsets:\n  a: [one]\n")
    (tmp_path / "s" / "scenarios" / "one.yaml").write_text(FILE)
    (tmp_path / "s" / "scenarios" / "two.yaml").write_text(FILE.replace("one", "two"))
    return tmp_path


def test_a_key_names_a_file_in_its_set(library):
    sc = load_scenario("s/one", library)
    assert sc.key == "s/one" and sc.set_ref == "s@3" and sc.condition == "friend"
    assert sc.file_hash == hashlib.sha256(FILE.encode()).hexdigest()
    assert sc.target_words == ["person"]


def test_bad_keys_missing_sets_and_missing_files_are_errors(library):
    for key, message in (("one", "<set_id>/<file>"), ("t/one", "no scenario set"),
                         ("s/three", "no scenario 'three'")):
        with pytest.raises(ScenarioNotFoundError, match=message):
            load_scenario(key, library)


def test_a_sets_keys_and_a_subsets(library):
    assert scenario_keys("s", root=library) == ["s/one", "s/two"]
    assert scenario_keys("s", "a", root=library) == ["s/one"]
    with pytest.raises(ScenarioNotFoundError, match="no subset"):
        scenario_keys("s", "b", root=library)


def test_the_library_in_the_repo():
    sc = load_scenario("bus_stop_friend_foe_v2/bus_stop_autistic_meltdown_friend")
    assert sc.set_ref == "bus_stop_friend_foe_v2@1" and sc.condition == "friend"
    assert len(scenario_keys("bus_stop_friend_foe_v2")) == 250
