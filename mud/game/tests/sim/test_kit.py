"""Tier-1: the crash draw + luggage (players-and-kit.md; DR-25a) — every slot's rows are sound, the
pure world dresses an actor, the clothing system reads regions / wind / wet, wounds show."""
from world.scenarios.whiteout import characters, content
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.objects import OBJECT_TABLE
from world.sim.contracts import EntityState
from world.sim.materials import load_materials
from world.sim.operations._helpers import CUTTABLE_ATTACH, PRYABLE_ATTACH
from world.sim.systems import injury, warmth
from world.sim.testing.probes import run_probe
from world.sim.testing.pure_world import PureWorld

MATS = load_materials(MATERIAL_TABLE)


def _ent(id, materials, mass, **state):
    return EntityState(id=id, name=id, materials=list(materials), mass_g=mass, state=dict(state))


def test_every_slot_row_is_sound():
    ids = {r["sim_id"] for r in OBJECT_TABLE}
    for slot in characters.SLOTS:
        rows = characters.outfit(slot)
        seen = set()
        for r in rows:
            assert r["sim_id"] not in seen and r["sim_id"] not in ids, r["sim_id"]
            seen.add(r["sim_id"])
            for m in r["materials"]:
                assert m in MATERIAL_TABLE, (slot, r["sim_id"], m)
            for reg in (r.get("state") or {}).get("covers", []):
                assert reg in warmth.REGIONS or reg == "eyes", (slot, r["sim_id"], reg)
            if "in" in r:
                assert r["in"] in seen, (slot, r["sim_id"], r["in"])
        st = characters.character_state(slot)
        assert st["zone"] in content.ZONE_TABLE


def test_luggage_rows_are_placed_and_attachments_known():
    ids = {r["sim_id"] for r in OBJECT_TABLE}
    for r in OBJECT_TABLE:
        if "in" in r:
            assert r["in"] in ids, r["sim_id"]
        for p in r.get("parts", []):
            assert p["attachment"] in CUTTABLE_ATTACH | PRYABLE_ATTACH | {"fixed"}


def test_dressed_actor_sees_pockets_and_itself():
    content.load()
    w = PureWorld.from_table(OBJECT_TABLE, actor_zone="mid_cabin")
    w.dress(characters.outfit("townie"), characters.character_state("townie"))
    names = {r.name for r in w.reachables()}
    assert {"pockets", "phone", "wallet", "denim jacket"} <= names
    me = w.get("me")
    assert me.state["worn"] and "phone" in " ".join(w.get("pockets_townie").state.get("contents", []))
    r = run_probe({"id": "t", "slot": "townie", "steps": ["examine me"], "expect": "SUCCESS"},
                  OBJECT_TABLE, MATS, slots=characters)
    assert r.passed, r.reason
    said = r.steps[-1].narration
    assert "denim jacket" in said and "forearm is cut and bleeding" in said and "feet" not in said


def test_regions_wind_and_wet():
    parka = _ent("parka", ["nylon_shell", "down"], 1600, covers=["torso", "arms", "head"], wind=0.9)
    jeans = _ent("jeans", ["denim"], 600, covers=["legs"])
    boots = _ent("boots", ["rubber", "insulation_batting"], 1400, covers=["feet"], wind=0.9)
    bare = warmth.bare_regions([parka, jeans, boots], MATS)
    assert bare == ["hands"]
    assert warmth.exposure_fraction([parka, jeans, boots], MATS) < warmth.exposure_fraction([jeans], MATS)
    assert warmth.exposure_fraction([], MATS) == 1.0
    dry = warmth.insulation_units(parka, MATS)
    soaked = warmth.insulation_units(_ent("parka", ["nylon_shell", "down"], 1600, covers=["torso"], wet=400), MATS)
    assert soaked < dry * 0.15, (dry, soaked)                # soaked down is worth nothing
    wool = _ent("sweater", ["wool"], 600, covers=["torso"], wet=150)
    assert warmth.insulation_units(wool, MATS) > warmth.insulation_units(_ent("sweater", ["wool"], 600), MATS) * 0.6
    mitts = _ent("mittens", ["nylon_shell", "fleece"], 160, covers=["hands"], fine_work=False)
    assert not warmth.fine_work_ok([mitts]) and warmth.fine_work_ok([parka])
    line = warmth.worn_summary([parka, jeans, boots], MATS)
    assert "hands is bare" in line or "hands are bare" in line


def test_wounds_summary():
    me = _ent("me", ["flesh"], 70000, wounds=[{"kind": "cut", "part": "forearm", "severity": 2, "bleeding": 2}])
    assert injury.wounds_summary(me) == "Your forearm is cut and bleeding."
    me.state["wounds"][0]["bound"] = True
    assert injury.wounds_summary(me) == "Your forearm is cut, bound."
    assert injury.wounds_summary(_ent("x", [], 1)) == ""
