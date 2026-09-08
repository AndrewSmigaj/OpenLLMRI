"""world.sim.validation.content_lint — the §44 content lint over the scenario TABLES (DR-17a). Pure.

`validate(scenario) -> (errors, warnings)` checks that the authored data is well-formed BEFORE it
loads: materials referenced exist; attachments are in the taxonomy; every object is placed (zone)
or stowed (in) — exactly one; parents and zones exist; masses are non-negative ints; sim_ids are
unique; every zone has a default space and every space frame carries its slots; every
`narrator.narrate("id")` literal in the handlers has a template; every probe cites a source. An
appearance entry is a WARNING when missing (the form-keyed generic is honest but dull). Runs in
milliseconds on the host: `make validate SCENARIO=<name>` → `python3 -m world.sim.validation`.
A rejection is a content bug, not a player failure — it fails the build.
"""
from __future__ import annotations

import os
import re

from world.sim.contracts import ORDINAL
from world.sim.operations._helpers import CUTTABLE_ATTACH, PRYABLE_ATTACH

KNOWN_ATTACH = frozenset(CUTTABLE_ATTACH) | frozenset(PRYABLE_ATTACH) | {"fixed"}
KNOWN_TAGS = {"flexible", "flammable", "fabric", "soft", "insulating", "strong", "cordage", "metal",
              "rigid", "conductive", "synthetic", "natural", "fuel", "tinder", "wire", "brittle",
              "frozen_water", "cold", "liquid", "extinguisher", "paper", "organic", "edible", "food",
              "absorbent", "potable"}
_NARRATE = re.compile(r"""narrate\(\s*["']([a-z_.]+)["']""")


def _handler_template_ids(sim_root: str) -> set:
    ids = set()
    for sub in ("operations/handlers", "resolver", "operations"):
        d = os.path.join(sim_root, sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".py"):
                with open(os.path.join(d, fn), encoding="utf-8") as fh:
                    ids |= set(_NARRATE.findall(fh.read()))
    return ids


def validate(objects, materials, zones, spaces, appearance, responses, probes=None, sim_root=None):
    """Lint the tables. Returns (errors, warnings) as lists of strings."""
    errors, warnings = [], []
    mats = set(materials)
    zone_ids = set(zones)
    ids = [r.get("sim_id") for r in objects]
    seen = set()

    # --- materials -------------------------------------------------------------------------
    for mid, spec in materials.items():
        for axis, val in (spec.get("props") or {}).items():
            if isinstance(val, bool) or not (isinstance(val, (int, float)) or val in ORDINAL):
                errors.append(f"material {mid!r}: prop {axis}={val!r} is not an ordinal word or number")
        for t in spec.get("tags", ()):
            if t not in KNOWN_TAGS:
                warnings.append(f"material {mid!r}: unknown tag {t!r}")
        tags = set(spec.get("tags", ()))
        props = spec.get("props") or {}
        if "flammable" in tags and "burnability" not in props:
            errors.append(f"material {mid!r}: tagged flammable but has no burnability")
        if "brittle" in tags and "rigidity" not in props:
            errors.append(f"material {mid!r}: tagged brittle but has no rigidity")

    # --- zones & spaces --------------------------------------------------------------------
    for zid, z in zones.items():
        if not z.get("name"):
            errors.append(f"zone {zid!r}: no name")
        for other in (z.get("adjacent") or {}):
            if other not in zone_ids:
                errors.append(f"zone {zid!r}: adjacent to unknown zone {other!r}")
    for zid, layout in (spaces or {}).items():
        if zid not in zone_ids:
            errors.append(f"spaces: layout for unknown zone {zid!r}")
        defaults = [sid for sid, s in (layout or {}).items() if s.get("default")]
        if len(defaults) != 1:
            errors.append(f"zone {zid!r}: needs exactly one default space, has {defaults}")
        for sid, s in (layout or {}).items():
            fr = s.get("frame", "")
            if fr and ("{items}" not in fr or "{be}" not in fr):
                errors.append(f"space {zid}/{sid}: frame must carry {{be}} and {{items}}: {fr!r}")
    for zid in zone_ids:
        if zid not in (spaces or {}):
            warnings.append(f"zone {zid!r}: no spaces authored (renders spaceless)")

    # --- objects ---------------------------------------------------------------------------
    for r in objects:
        sid = r.get("sim_id")
        where = f"object {sid!r}"
        if not sid:
            errors.append(f"object row without sim_id: {r.get('name')!r}")
            continue
        if sid in seen:
            errors.append(f"{where}: duplicate sim_id")
        seen.add(sid)
        if not r.get("name"):
            errors.append(f"{where}: no name")
        for m in r.get("materials") or []:
            if m not in mats:
                errors.append(f"{where}: unknown material {m!r}")
        if not r.get("materials"):
            warnings.append(f"{where}: no materials (operations will find nothing to act on)")
        mg = r.get("mass_g", 0)
        if isinstance(mg, bool) or not isinstance(mg, int) or mg < 0:
            errors.append(f"{where}: mass_g must be a non-negative int, got {mg!r}")
        has_zone, has_in = "zone" in r, "in" in r
        if has_zone == has_in:
            errors.append(f"{where}: exactly one of zone / in is required")
        if has_zone and r["zone"] not in zone_ids:
            errors.append(f"{where}: unknown zone {r['zone']!r}")
        if has_in and r["in"] not in ids:
            errors.append(f"{where}: stowed in unknown parent {r['in']!r}")
        st = r.get("state") or {}
        sp = st.get("space")
        if sp and has_zone and sp not in (spaces.get(r["zone"]) or {}):
            errors.append(f"{where}: space {sp!r} not in zone {r['zone']!r}")
        for p in r.get("parts") or []:
            pw = f"{where} part {p.get('id')!r}"
            if p.get("material") not in mats:
                errors.append(f"{pw}: unknown material {p.get('material')!r}")
            if p.get("attachment", "fixed") not in KNOWN_ATTACH:
                errors.append(f"{pw}: unknown attachment {p.get('attachment')!r}")
            pm = p.get("mass_g", 0)
            if isinstance(pm, bool) or not isinstance(pm, int) or pm < 0:
                errors.append(f"{pw}: mass_g must be a non-negative int")
        if sid not in appearance and r.get("name") not in appearance:
            warnings.append(f"{where}: no appearance entry (generic fallback)")
        entry = appearance.get(sid) or appearance.get(r.get("name")) or {}
        home = entry.get("space")
        if home and has_zone and home not in (spaces.get(r["zone"]) or {}):
            errors.append(f"{where}: appearance home space {home!r} not in zone {r['zone']!r}")

    # --- responses ---------------------------------------------------------------------------
    for tid, tmpl in responses.items():
        if re.search(r"\b(a|an|the)\s+\{tool\}", str(tmpl)):
            errors.append(f"response {tid!r}: writes an article before {{tool}} (it arrives pre-articled)")
    if sim_root:
        for tid in sorted(_handler_template_ids(sim_root)):
            if tid not in responses:
                warnings.append(f"handler narrates {tid!r} but no template exists (falls back)")
    for kind in ("explain", "hint", "residue"):
        if f"attachment.{kind}._" not in responses:
            warnings.append(f"no attachment.{kind}._ fallback phrase")

    # --- probes ------------------------------------------------------------------------------
    pids = set()
    for p in probes or []:
        pid = p.get("id")
        if not pid or pid in pids:
            errors.append(f"probe {pid!r}: missing or duplicate id")
        pids.add(pid)
        if not p.get("source"):
            errors.append(f"probe {pid!r}: no source (no self-graded probes)")
        if p.get("status") not in ("pass", "todo"):
            errors.append(f"probe {pid!r}: status must be pass|todo")
        if not p.get("steps"):
            errors.append(f"probe {pid!r}: no steps")
        if p.get("zone") and p["zone"] not in zone_ids:
            errors.append(f"probe {pid!r}: unknown zone {p['zone']!r}")
        for h in p.get("holds", ()):
            if h not in ids:
                errors.append(f"probe {pid!r}: holds unknown object {h!r}")
        if str(p.get("expect", "SUCCESS")).upper() not in ("SUCCESS", "REDIRECT", "PARTIAL", "PARSED"):
            errors.append(f"probe {pid!r}: bad expect {p.get('expect')!r}")
    return errors, warnings
