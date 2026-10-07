"""world.sim.affordances — derived capabilities from material × form × state (DR-26). Pure.

A **capability** is a named, levelled affordance a thing offers to a verb: `edge`, `point`, `heft`,
`leverage`, `abrasive`, `ignition`, `flame`, `ember`, `tinder`, `cordage`, `sheet`, `vessel`,
`insulating`, `absorbent`, `reflective`. Verbs require a level (`capability(ref, world, axis,
materials)` in `operations._helpers`); they never name a tool. That is what closes the ontology:
anything the world mints — a shard, a strip, a shaving — is a full participant.

`derive(entity, materials)` computes the levels from the entity's PRIMARY material (its intensive
props + tags), its `state["form"]` (the shape the material is in — the second axis beside material),
and its state (a wet match has no ignition). Rules:
  * **authored wins** — an explicit numeric `state[axis]` overrides the derived value (the caller,
    `_helpers.capability`, reads it first); the golden tools stay hand-tuned;
  * **capped** — every factor is ≤ 1.0, so a derived level never exceeds min(material, form);
  * **closed** — every form a minting handler produces is a key of FORMS, and
    `form_for_template()` maps the authored `outputs_when_removed` ids onto forms.
Levels are floats in [0, 1] on the same scale as the material ordinals (contracts.ORDINAL).
"""
from __future__ import annotations

# The taught forms vocabulary (v1; extend by evidence, never speculatively — ontology-closure.md §2).
FORMS = frozenset({
    "blade", "shard", "flake", "piece", "scrap", "strip", "sheet", "slab", "board", "rod", "stick",
    "bar", "pole", "spindle", "point", "stake", "bow", "shavings", "bundle", "cord", "block",
    "vessel", "ember", "ash", "liquid", "cloth",
})

_HARD_EDGE_MIN = 0.6          # a material must resist cutting at least this much to HOLD an edge
_EDGE_FORM = {"blade": 1.0, "shard": 0.85, "flake": 0.85, "sheet": 0.6, "piece": 0.3, "slab": 0.2}
_POINT_FORM = {"point": 1.0, "stake": 1.0, "spindle": 0.6, "shard": 0.8, "blade": 0.7, "flake": 0.5}
_LEVERAGE_FORM = {"bar": 0.9, "pole": 0.9, "rod": 0.8, "stick": 0.8, "blade": 0.5, "piece": 0.4,
                  "board": 0.3, "slab": 0.3, "spindle": 0.3}
_HEFT_FORM = {"block": 1.0, "piece": 0.7, "slab": 0.6, "rod": 0.6, "stick": 0.6, "board": 0.5,
              "bar": 0.7, "blade": 0.4, "shard": 0.2}
_ABRASIVE_FORM = {"piece": 0.6, "block": 0.6, "flake": 0.5, "shard": 0.3}
_CORD_FORMS = frozenset({"cord", "strip"})
_SHEET_FORMS = frozenset({"sheet", "cloth"})
_REFLECT_FORMS = frozenset({"sheet", "shard", "flake", "blade"})
_VESSEL_FORMS = frozenset({"vessel"})
_TINDER_FORMS = frozenset({"shavings", "bundle", "strip", "scrap"})
_SHINY = frozenset({"glass", "ice"})     # material ids that reflect besides anything tagged metal


def _leverage_mass_gate(mass_g: int) -> float:
    """A toothpick is rigid and lends no leverage; a wrist-thick branch does."""
    if mass_g >= 300:
        return 1.0
    if mass_g >= 100:
        return 0.5
    return 0.0


def _heft_mass_gate(mass_g: int) -> float:
    if mass_g >= 800:
        return 1.0
    if mass_g >= 300:
        return 0.6
    if mass_g >= 100:
        return 0.3
    return 0.0


def _clamp(x: float) -> float:
    return 0.0 if x <= 0 else (1.0 if x >= 1 else float(x))


def derive(ent, materials) -> dict:
    """The derived capability levels of `ent` (an EntityState), keyed by axis. Only NONZERO axes are
    returned; callers `.get(axis, 0.0)`. Pure: no world access, no RNG."""
    st = ent.state or {}
    mid = ent.materials[0] if ent.materials else None
    mat = (materials or {}).get(mid) if mid else None
    props = dict(mat.props) if mat is not None else {}
    tags = set(mat.tags) if mat is not None else set()
    form = st.get("form")
    mass = int(ent.mass_g or 0)

    cut_res = float(props.get("cut_resistance", 0.0))
    tear_res = float(props.get("tear_resistance", 0.0))
    rigidity = float(props.get("rigidity", 0.0))
    flexible = "flexible" in tags
    hard = cut_res >= _HARD_EDGE_MIN
    out: dict[str, float] = {}

    def put(axis, value):
        v = _clamp(value)
        if v > 0:
            out[axis] = v

    # --- mechanical: what the shape of a hard/rigid material lends -------------------------------
    if hard and form in _EDGE_FORM:
        put("edge", cut_res * _EDGE_FORM[form])
    if form in _POINT_FORM and (cut_res >= 0.5 or rigidity >= 0.5):
        put("point", max(cut_res, rigidity) * _POINT_FORM[form])
    if rigidity >= 0.5 and form in _LEVERAGE_FORM:
        put("leverage", rigidity * _LEVERAGE_FORM[form] * _leverage_mass_gate(mass))
    if rigidity >= 0.5 and form in _HEFT_FORM:
        put("heft", rigidity * _HEFT_FORM[form] * _heft_mass_gate(mass))
    if rigidity >= 0.5 and form in _ABRASIVE_FORM and not flexible:
        put("abrasive", rigidity * _ABRASIVE_FORM[form])

    # --- fabric & fibre: what a flexible material lends -------------------------------------------
    if "cordage" in tags or "wire" in tags:
        put("cordage", max(0.5, tear_res))
    elif flexible and form in _CORD_FORMS:
        put("cordage", max(0.2, tear_res))
    if flexible and form in _SHEET_FORMS:
        put("sheet", 1.0)
    elif flexible and form == "strip":
        put("sheet", 0.5)
    if form in _VESSEL_FORMS and not flexible:
        put("vessel", 1.0)

    # --- optical -----------------------------------------------------------------------------------
    if form in _REFLECT_FORMS and ("metal" in tags or mid in _SHINY):
        put("reflective", 0.8)

    # --- intensive pass-throughs (so verbs can ask the thing, not the table) ----------------------
    put("insulating", float(props.get("insulation", 0.0)))
    put("absorbent", float(props.get("absorbency", 0.0)))

    # --- fire: sources are STATE; tinder-readiness is material × thinness ------------------------
    wet = bool(st.get("wet") or st.get("wetness"))
    if (st.get("ignition") or "ignition" in (ent.tags or [])) and not wet:
        put("ignition", 1.0)
    if st.get("lit") or "lit" in (ent.tags or []):
        put("flame", 1.0)
    if st.get("ember"):
        put("ember", 0.6)
    burn = float(props.get("burnability", 0.0))
    if burn > 0 and not wet and ("tinder" in tags or form in _TINDER_FORMS):
        put("tinder", burn)
    return out


# --- the authored output templates → forms (closure for `outputs_when_removed`) -------------------
_TEMPLATE_FORMS = {
    "loose_fabric": "sheet", "loose_foam": "block", "loose_webbing": "cord", "loose_branch": "rod",
    "loose_bough": "rod", "loose_cup": "vessel", "loose_latch": "piece", "rubber_tubing": "cord",
    "ash": "ash", "water": "liquid",
}
_SUFFIX_FORMS = (
    ("_shard", "shard"), ("_flake", "flake"), ("_piece", "piece"), ("_scrap", "scrap"),
    ("_strip", "strip"), ("_sheet", "sheet"), ("_shavings", "shavings"), ("_slab", "slab"),
    ("_board", "board"), ("_rod", "rod"), ("_cord", "cord"), ("_wire", "cord"), ("_tubing", "cord"),
    ("_bundle", "bundle"), ("_block", "block"), ("_ember", "ember"), ("_ash", "ash"),
)


def form_for_template(template: str) -> "str | None":
    """The form a minted template id denotes (`glass_shard` → shard, `loose_fabric` → sheet), or
    None when the template carries no shape information."""
    if not template:
        return None
    if template in _TEMPLATE_FORMS:
        return _TEMPLATE_FORMS[template]
    for suffix, form in _SUFFIX_FORMS:
        if template.endswith(suffix):
            return form
    if template.startswith("loose_"):
        return "piece"
    return None
