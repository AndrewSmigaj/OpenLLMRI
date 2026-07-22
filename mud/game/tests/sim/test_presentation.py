"""Tier-1: the scene-as-prose composer (the scene-space model) + the unified thing renderer. Pure.

Golden-ish substring asserts (the prose is Andrew-tunable content; tests pin the STRUCTURE:
space grouping + survey order, empty-space omission, frame number-agreement, overflow cap,
aggregation, state-conditioning, part weaving, and the banded cross-zone fade)."""
from world.scenarios.whiteout.appearance import APPEARANCE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.scenarios.whiteout.spaces import SPACE_TABLE
from world.sim import narrator, presentation
from world.sim.contracts import EntityState, Part
from world.sim.space import spaces


def setup_module(_):
    narrator.load_responses(RESPONSES)          # attachment.hint.* phrases for part weaving
    presentation.load_appearance(APPEARANCE)
    spaces.load_spaces(SPACE_TABLE)


def _ent(id, name, state=None, parts=(), materials=("steel",), mass=100):
    return EntityState(id=id, name=name, materials=list(materials), parts=list(parts),
                       tags=[], mass_g=mass, state=dict(state or {}), provenance=[], owner=None)


def _cockpit(id, name, materials=("steel",), **state):
    return _ent(id, name, state={"zone": "cockpit", **state}, materials=materials)


PILOT = _cockpit("pilot", "the pilot")            # anchor of left_seat
RADIO = _cockpit("radio", "field radio")          # anchor of cradle
MANUAL = _cockpit("manual", "flight manual", materials=("paper",))    # a floor object
CHART = _cockpit("chart", "sectional chart", materials=("paper",))    # a floor object


def test_scene_groups_into_spaces_in_survey_order():
    scene = presentation.compose_scene([MANUAL, RADIO, PILOT])   # deliberately out of order
    assert "You see" not in scene
    # anchors lead their spaces, spaces in survey order: left_seat(pilot) < cradle(radio) < floor
    assert scene.index("pilot") < scene.index("field radio") < scene.index("flight manual")
    assert "Across the cockpit floor is a flight manual" in scene   # frame = position, not history


def test_empty_spaces_render_nothing():
    scene = presentation.compose_scene([MANUAL])          # only a floor object is present
    assert "Across the cockpit floor" in scene
    for gone in ("Below the cradle", "footwell", "seat back"):
        assert gone not in scene, f"an empty space must render nothing, got {gone!r}"


def test_frame_number_agreement_and_overflow_cap():
    floor = [_cockpit(f"j{i}", f"crate{i}", space="floor") for i in range(5)]   # cap is 3
    scene = presentation.compose_scene(floor)
    assert " are " in scene                                # plural agreement
    assert "a scatter of smaller debris" in scene          # the overflow absorbs beyond the cap
    solo = _cockpit("solo", "a lone strut", space="floor")
    assert " is " in presentation.compose_scene([solo])    # singular agreement


def test_runtime_space_overrides_the_authored_home():
    # the manual's home is the floor; a player who set it on the seat back renders it THERE
    moved = _cockpit("manual", "flight manual", materials=("paper",), space="left_seat")
    scene = presentation.compose_scene([moved])
    assert "Slung over the seat back beside him is a flight manual" in scene
    assert "Across the cockpit floor" not in scene


def test_scene_phrase_switches_on_state():
    dead = _cockpit("pilot", "the pilot", dead=True)
    alive = _cockpit("pilot", "the pilot")
    assert "lies still against the forward bulkhead" in presentation.compose_scene([dead])
    assert "breathing shallow and slow" in presentation.compose_scene([alive])


def test_identical_deriveds_aggregate_within_a_space():
    shards = [_cockpit(f"bottle:shard{i}:loose", "glass shard", materials=("glass",), space="floor")
              for i in range(3)]
    scene = presentation.compose_scene(shards)
    assert "three sharp shards" in scene and scene.count("glass shard") == 0


def test_unknown_object_renders_via_spaceless_fallback():
    # no zone → the unzoned one-zone render; every object still shows, no frames
    mystery = _ent("x9", "unmarked crate", materials=("wood",))
    assert "unmarked crate" in presentation.compose_scene([mystery])


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
    assert "make out a coil of copper wire" in scene and "north" in scene
    assert "shape in the snow" in scene and "field radio" not in scene, "distant = vague, unnamed"
    assert "hidden thing" not in scene, "OUT_OF_SIGHT renders nothing"


def test_read_text_is_state_conditioned_content():
    manual = _ent("manual", "flight manual", materials=("paper",))
    text = presentation.read_text(manual)
    assert text and "121.5" in text, "the manual carries the §38 GUARD-frequency clue"
    assert presentation.read_text(_ent("bottle", "whisky bottle")) is None


def test_perceived_none_or_empty_is_the_pre_p3_render():
    ents = [_ent("seat", "aircraft seat"), _ent("bottle", "whisky bottle", materials=("glass",))]
    assert presentation.compose_scene(ents, None) == presentation.compose_scene(ents)
    assert presentation.compose_scene(ents, {}) == presentation.compose_scene(ents)


# --- placement: the drop/look-at-space resolvers (box B) -----------------------

def test_resolve_space_by_id_alias_and_overflow_word():
    assert spaces.resolve_space("cockpit", "footwell") == "footwell"     # a plain alias
    assert spaces.resolve_space("cockpit", "cockpit floor") == "floor"   # a multi-word alias
    assert spaces.resolve_space("cockpit", "debris") == "floor"          # a word from the overflow
    assert spaces.resolve_space("cockpit", "nonsense") is None
    assert spaces.resolve_space(None, "floor") is None                   # unzoned → no spaces


def test_look_space_lists_every_item_uncapped():
    floor = [_cockpit(f"j{i}", f"crate{i}", space="floor") for i in range(5)]   # cap is 3
    capped = presentation.compose_scene(floor)
    uncapped = presentation.look_space("cockpit", "floor", floor)
    assert "a scatter of smaller debris" in capped        # the room look absorbs beyond the cap
    assert "a scatter of smaller debris" not in uncapped   # look-at-space names them all
    for i in range(5):
        assert f"crate{i}" in uncapped
    assert presentation.look_space("cockpit", "not-a-space", floor) is None
