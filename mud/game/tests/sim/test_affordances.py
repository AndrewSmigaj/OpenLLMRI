"""Tier-1: derived capabilities (DR-26 closure) — material × form × state → levels; authored wins;
capped; the minted-template → form map is closed over what the handlers produce."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim.affordances import FORMS, derive, form_for_template
from world.sim.contracts import EntityState, NounRef
from world.sim.materials import load_materials
from world.sim.operations._helpers import capability

MATS = load_materials(MATERIAL_TABLE)


class W:
    seed_state = 0
    def __init__(self, ents):
        self._e = {e.id: e for e in ents}
    def get(self, i):
        return self._e.get(i)
    def reachable(self, a):
        return list(self._e)
    def in_zone(self, z):
        return list(self._e)


def _ent(id, material, mass_g, **state):
    return EntityState(id=id, name=id.replace("_", " "), materials=[material], mass_g=mass_g, state=state)


def test_glass_shard_holds_an_edge_but_foam_does_not():
    shard = derive(_ent("shard", "glass", 166, form="shard"), MATS)
    assert 0.5 < shard["edge"] < 0.7                      # cut_resistance(high .7) × shard .85
    assert shard["point"] > 0 and shard["reflective"] > 0
    assert "edge" not in derive(_ent("lump", "foam", 166, form="shard"), MATS)
    assert "edge" not in derive(_ent("chip", "wood", 166, form="piece"), MATS)   # wood is not hard


def test_a_torn_metal_sheet_has_a_lesser_edge_and_reflects():
    sheet = derive(_ent("skin", "aluminum", 900, form="sheet"), MATS)
    assert 0.35 < sheet["edge"] < 0.5 and sheet["reflective"] > 0
    assert "sheet" not in sheet                           # metal is not flexible → no cover


def test_leverage_needs_rigidity_and_mass():
    branch = derive(_ent("branch", "wood", 800, form="rod"), MATS)
    assert branch["leverage"] > 0.5 and branch["heft"] > 0
    assert "leverage" not in derive(_ent("twig", "wood", 20, form="rod"), MATS)   # a toothpick lends none
    assert "leverage" not in derive(_ent("rag", "cotton_cloth", 800, form="rod"), MATS)


def test_fabric_strip_is_cordage_and_a_sheet_is_a_cover():
    strip = derive(_ent("strip", "synthetic_fabric", 40, form="strip"), MATS)
    assert strip["cordage"] >= 0.2 and strip["sheet"] > 0 and strip["tinder"] > 0
    sheet = derive(_ent("cover", "synthetic_fabric", 200, form="sheet"), MATS)
    assert sheet["sheet"] == 1.0
    cord = derive(_ent("paracord", "nylon_webbing", 90), MATS)   # material-tagged cordage, any form
    assert cord["cordage"] >= 0.5


def test_fire_sources_are_state_and_wet_kills_ignition():
    assert derive(_ent("lighter", "plastic", 20, ignition=True), MATS)["ignition"] == 1.0
    assert "ignition" not in derive(_ent("matchbox", "plastic", 80, ignition=True, wet=True), MATS)
    assert derive(_ent("fire", "wood", 2000, lit=True), MATS)["flame"] == 1.0
    assert derive(_ent("coal", "wood", 5, ember=True), MATS)["ember"] > 0
    assert "tinder" not in derive(_ent("log", "wood", 2000, form="rod"), MATS)
    assert derive(_ent("curls", "wood", 30, form="shavings"), MATS)["tinder"] > 0


def test_levels_are_capped_and_authored_wins():
    for f in FORMS:
        for mid in MATS:
            for axis, v in derive(_ent("x", mid, 1000, form=f), MATS).items():
                assert 0.0 < v <= 1.0, (f, mid, axis, v)
    blade = _ent("multitool", "steel", 150, form="blade", edge=0.8)
    w = W([blade])
    assert capability(NounRef("multitool"), w, "edge", MATS) == 0.8            # authored, not derived 1.0
    shard = _ent("shard", "glass", 166, form="shard")
    w = W([shard])
    assert capability(NounRef("shard"), w, "edge", MATS) > 0.5                 # derived
    assert capability(NounRef("shard"), w, "edge") == 0.0                      # no materials → no derivation
    assert capability(None, w, "edge", MATS) == 0.0                            # bare hands


def test_minted_templates_map_onto_forms():
    assert form_for_template("glass_shard") == "shard"
    assert form_for_template("synthetic_fabric_strip") == "strip"
    assert form_for_template("foam_scrap") == "scrap"
    assert form_for_template("wood_piece") == "piece"
    assert form_for_template("loose_fabric") == "sheet"
    assert form_for_template("loose_webbing") == "cord"
    assert form_for_template("loose_branch") == "rod"
    assert form_for_template("rubber_tubing") == "cord"
    assert form_for_template("ash") == "ash" and form_for_template("water") == "liquid"
    assert form_for_template("loose_latch") == "piece"
    assert form_for_template("radio") is None
    for t in ("glass_shard", "loose_fabric", "foam_scrap", "wood_piece", "ash"):
        assert form_for_template(t) in FORMS
