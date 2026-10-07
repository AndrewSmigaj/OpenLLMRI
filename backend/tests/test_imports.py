"""Every backend module imports.

Runs on CPU with no model, data or .env, so it catches a broken import (a module removed while
something still imports it, a misspelled name) before a server start would.
"""

import importlib
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"


def _module_names() -> list[str]:
    names = []
    for path in sorted(SRC.rglob("*.py")):
        parts = path.relative_to(SRC).with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if parts:
            names.append(".".join(parts))
    return names


@pytest.mark.parametrize("name", _module_names())
def test_module_imports(name: str) -> None:
    importlib.import_module(name)
