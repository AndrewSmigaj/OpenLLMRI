"""Tier-1: the scene-as-prose composer + the unified thing renderer (DR-23). Pure fixtures.

Golden-ish substring asserts (the prose is Andrew-tunable content; tests pin the STRUCTURE:
salience ordering, weighting-not-hiding, aggregation, state-conditioning, part weaving)."""
from world.scenarios.whiteout.appearance import APPEARANCE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator, presentation
from world.sim.contracts import EntityState, Part


def setup_module(_):
    narrator.load_responses(RESPONSES)          # attachment.hint.* phrases for part weaving
    presentation.load_appearance(APPEARANCE)


def _ent(id, name, state=None, parts=(), materials=("steel",), mass=100):
    return EntityState(id=id, name=name, materials=list(materials), parts=list(parts),
                       tags=[], mass_g=mass, state=dict(state or {}), provenance=[], owner=None)


PILOT = _ent("pilot", "the pilot")
RADIO = _ent("radio", "field radio")
WIRE = _ent("wire", "coil of copper wire", materials=("copper_wire",))
BOTTLE = _ent("bottle", "whisky bottle", materials=("glass",))
TINDER = _ent("tinder", "dry grass", materials=("dry_grass",))


def test_scene_is_prose_not_a_list():
    scene = presentation.compose_scene([PILOT, RADIO, WIRE, BOTTLE])
    assert "You see" not in scene
    # prominent anchors lead as full sentences, in authored order (pilot before radio)
    assert scene.index("pilot") < scene.index("radio") < scene.index("whisky")


def test_everything_is_mentioned_weighting_not_hiding():
    scene = presentation.compose_scene([PILOT, RADIO, WIRE, BOTTLE, TINDER])
    for word in ("pilot", "radio", "copper wire", "whisky", "dry grass"):
        assert word in scene, f"{word!r} must be mentioned — salience weights, it never hides"


def test_state_promotes_salience_and_switches_the_phrase():
    lit = _ent("tinder", "dry grass", state={"lit": True}, materials=("dry_grass",))
    scene = presentation.compose_scene([lit, BOTTLE])
    assert "fire cracks and spits" in scene
    assert scene.index("fire") < scene.index("whisky"), "a lit fire is promoted to prominent"


def test_identical_deriveds_aggregate_with_authored_phrase():
    shards = [_ent(f"bottle:shard{i}:loose", "glass shard", materials=("glass",)) for i in range(3)]
    scene = presentation.compose_scene(shards)
    assert "three sharp shards" in scene and scene.count("glass shard") == 0


def test_unknown_object_still_renders_via_fallback():
    mystery = _ent("x9", "unmarked crate", materials=("wood",))
    scene = presentation.compose_scene([mystery])
    assert "unmarked crate" in scene


def test_fallback_never_double_articles_determined_names():
    # regression (2026-07-03): an empty-registry login rendered "a the pilot"
    body = _ent("x1", "the pilot", materials=("flesh",))
    scene = presentation.compose_scene([body])
    assert "a the pilot" not in scene and "the pilot" in scene


def test_describe_weaves_parts_with_names_and_physical_attachments():
    seat = _ent("seat", "aircraft seat", state={"ident": "11B"},
                parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",)),
                       Part("cushion", "foam", 800, "clipped", ("loose_foam",))])
    out = presentation.describe(seat)
    assert "[11B]" in out
    assert "cover" in out and "held by stitching" in out
    assert "cushion" in out and "snapped into a frame" in out
    assert "(foam" not in out and "(synthetic_fabric" not in out, "attachments are prose, not data"


def test_describe_is_state_conditioned():
    out_cold = presentation.describe(_ent("tinder", "dry grass", materials=("dry_grass",)))
    out_lit = presentation.describe(_ent("tinder", "dry grass", state={"lit": True},
                                         materials=("dry_grass",)))
    assert "spark" in out_cold and "feeding" in out_lit and out_cold != out_lit
    assert "alight" in out_lit                       # the systemic condition line is woven in


def test_describe_fallback_for_unauthored_objects():
    out = presentation.describe(_ent("y1", "nylon webbing scrap", materials=("nylon_webbing",), mass=50))
    assert "nylon webbing scrap" in out and "nylon webbing" in out and "50" in out


# --- banded composition (DR-13a) ----------------------------------------------

def _pr(band, direction="to the north"):
    from world.sim.contracts import PerceptionBand, PerceptionResult
    return PerceptionResult(band=band, visible=band is not PerceptionBand.OUT_OF_SIGHT,
                            audible=False, reachable=band is PerceptionBand.SAME_ZONE,
                            direction_phrase="" if band is PerceptionBand.SAME_ZONE else direction)


def test_banded_scene_fades_by_distance_and_drops_out_of_sight():
    from world.sim.contracts import PerceptionBand as B
    seat = _ent("seat", "aircraft seat", state={"ident": "11B"})
    wire = _ent("wire", "coil of copper wire", materials=("copper_wire",))
    radio = _ent("radio", "field radio")
    gone = _ent("ghost", "hidden thing")
    scene = presentation.compose_scene(
        [seat, wire, radio, gone],
        {"seat": _pr(B.SAME_ZONE), "wire": _pr(B.NEAR_VISIBLE),
         "radio": _pr(B.DISTANT_VISIBLE, "to the south"), "ghost": _pr(B.OUT_OF_SIGHT)})
    assert "wrenched sideways" in scene, "same-zone keeps the full authored scene phrase"
    assert "make out coil of copper wire" in scene and "north" in scene
    assert "shape in the snow" in scene and "field radio" not in scene, "distant = vague, unnamed"
    assert "hidden thing" not in scene, "OUT_OF_SIGHT renders nothing"


def test_perceived_none_or_empty_is_the_pre_p3_render():
    ents = [_ent("seat", "aircraft seat"), _ent("bottle", "whisky bottle", materials=("glass",))]
    assert presentation.compose_scene(ents, None) == presentation.compose_scene(ents)
    assert presentation.compose_scene(ents, {}) == presentation.compose_scene(ents)
