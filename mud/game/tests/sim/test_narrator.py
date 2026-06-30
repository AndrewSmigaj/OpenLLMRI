"""Tier-1: the narrator renders templates deterministically, never blank (P1.1)."""
from world.sim import narrator


def test_render_fills_and_is_safe():
    assert narrator.render("You saw the {target} free.", {"target": "cover"}) == "You saw the cover free."
    # unknown placeholders are left literal, not crashing
    assert narrator.render("{a} {b}", {"a": "x"}) == "x {b}"


def test_narrate_uses_registry_and_falls_back():
    narrator.load_responses({"cut.success": "You cut the {target}.", "__fallback__": "It gives way."})
    assert narrator.narrate("cut.success", {"target": "strap"}) == "You cut the strap."
    assert narrator.narrate("missing.id", {}) == "It gives way."
