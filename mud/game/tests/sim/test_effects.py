"""Tier-1: effect constructors produce the right Effect kinds/args (DR-10, P1.1)."""
from world.sim import effects
from world.sim.contracts import Effect, EffectKind


def test_set_and_adjust():
    e = effects.set_attr("seat", "wetness", 0.5)
    assert isinstance(e, Effect) and e.kind == EffectKind.SET_ATTR and e.target_id == "seat"
    assert e.args == {"key": "wetness", "value": 0.5}
    a = effects.adjust_attr("char", "warmth", -1)
    assert a.kind == EffectKind.ADJUST_ATTR and a.args["delta"] == -1


def test_remove_part_and_create_object_conserve_args():
    r = effects.remove_part("seat", "cover")
    assert r.kind == EffectKind.REMOVE_PART and r.args["part_id"] == "cover"
    c = effects.create_object("loose_fabric", "loose_fabric#1",
                              {"material": "synthetic_fabric", "mass_g": 200})
    assert c.kind == EffectKind.CREATE_OBJECT and c.target_id == "loose_fabric#1"
    assert c.args["template"] == "loose_fabric"
    assert c.args["material"] == "synthetic_fabric" and c.args["mass_g"] == 200


def test_consume_move_owner():
    assert effects.consume("rag", 50).args["mass_g"] == 50
    assert effects.move_zone("char", "north").kind == EffectKind.MOVE_ZONE
    assert effects.set_owner("knife", None).args["owner"] is None
