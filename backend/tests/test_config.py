"""api.config: where the data lake is (DATA_LAKE_PATH from the repo root's .env)."""
import importlib
from pathlib import Path

import pytest

import api.config as config

PROJECT_ROOT = Path(config.__file__).resolve().parents[3]


@pytest.fixture(autouse=True)
def _restore_config():
    yield
    importlib.reload(config)          # after monkeypatch has restored the environment


def _lake(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("DATA_LAKE_PATH", raising=False)
    else:
        monkeypatch.setenv("DATA_LAKE_PATH", value)
    return importlib.reload(config).DATA_LAKE_PATH


def test_a_relative_path_resolves_against_the_project_root(monkeypatch):
    assert _lake(monkeypatch, "data/lake/") == PROJECT_ROOT / "data" / "lake"


def test_an_absolute_path_is_kept(monkeypatch, tmp_path):
    assert _lake(monkeypatch, str(tmp_path)) == tmp_path


def test_unset_means_the_projects_own_lake(monkeypatch):
    assert _lake(monkeypatch, None) == PROJECT_ROOT / "data" / "lake"
