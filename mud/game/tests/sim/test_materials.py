"""Tier-1: the material loader maps ordinals→numbers and preserves tags (DR-04, P1.1)."""
import pytest

from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim.contracts import ORDINAL, Material
from world.sim.materials import load_materials


def test_table_loads_to_materials():
    mats = load_materials(MATERIAL_TABLE)
    assert mats, "material table is empty"
    assert all(isinstance(m, Material) for m in mats.values())


def test_ordinal_words_mapped_to_numbers():
    mats = load_materials({"x": {"props": {"cut_resistance": "high", "burnability": "none"}, "tags": ("t",)}})
    m = mats["x"]
    assert m.props["cut_resistance"] == ORDINAL["high"]
    assert m.props["burnability"] == ORDINAL["none"]
    assert m.tags == ("t",)


def test_numbers_pass_through_and_unknown_rejected():
    assert load_materials({"y": {"props": {"insulation": 0.42}}})["y"].props["insulation"] == 0.42
    with pytest.raises(ValueError):
        load_materials({"z": {"props": {"insulation": "bogus"}}})


def test_slice_materials_present():
    mats = load_materials(MATERIAL_TABLE)
    for need in ("synthetic_fabric", "foam", "nylon_webbing", "steel"):
        assert need in mats, f"missing slice material {need}"
