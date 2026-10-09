"""Atlas v1, the node catalogue (DESIGN.md H): every node of every saved lens version, layer by
layer, with what it holds, where its items come from and go, its experts, its worked-out details
and its report.

Each saved version's catalogue is a file in the repo, beside the version's records:
`data/lenses/<session>/<lens>/<version>/nodes.json`, with the version's expert pipelines, hubs and
experts involved beside it (`routes.json`, without the members' ids). Both are written when the
version is saved and again when its details or reports are worked out; `GET /api/atlas/nodes`
reads the nodes.
"""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

FORMAT = 1
TOP = 3  # nodes before and after, and experts, kept per entry


def _top(codes: Any, prefix: str) -> List[Dict[str, Any]]:
    return [{"id": f"{prefix}{code}", "items": n} for code, n in Counter(codes.tolist()).most_common(TOP)]


def _details(layer_details: Dict[str, Any], node: int) -> Optional[Dict[str, Any]]:
    """What the node's worked-out details say, in brief."""
    found = (layer_details.get("nodes") or {}).get(str(node))
    if not found:
        return None
    surface = found.get("surface") or {}
    return {"neurons": found["neurons"][:5],
            "tokens": [token for token, _ in found["logit_lens"]["distinctive"][:8]],
            "surface_flagged": bool(surface.get("flagged")), "surface_feature": surface.get("feature"),
            "routing": found.get("routing"), "layer_routing_effect": layer_details.get("routing_effect")}


def _report(folder: Path, version: str, card: Optional[Dict[str, Any]], tested: bool) -> Optional[Dict[str, Any]]:
    """The node's card in brief: its title, pattern and summary, the facts its summary cites (so the
    entry reads on its own), and how far to trust it."""
    from services.llm.cards import analysis_dir, current_check
    from services.llm.numbers import cited_ids

    output = (card or {}).get("output")
    if not card or not output:
        return None
    path = analysis_dir(folder, version) / "packets" / f"{card['packet_hash']}.json"
    facts = {f["id"]: f for f in json.loads(path.read_text(encoding="utf-8"))["facts"]} if path.exists() else {}
    check = current_check(folder, version, card)
    return {"title": output["title"], "pattern": output["pattern"], "summary": output["summary"],
            "facts": {fid: facts[fid] for fid in cited_ids(output["summary"]) if fid in facts},
            "numbers_checked": bool((check or {}).get("passed")), "tested_analyst": tested,
            "written_by": card.get("written_by"), "written_at": card.get("created_at")}


def _by_weight(view: Any, mask: Any, li: int, layer: int) -> List[Dict[str, Any]]:
    """The experts the node's items weight most at its layer, over all four ranks (mean weight)."""
    totals: Dict[int, float] = {}
    for experts, weights in zip(view.experts[mask, li, :], view.weights[mask, li, :]):
        for expert, weight in zip(experts.tolist(), weights.tolist()):
            totals[int(expert)] = totals.get(int(expert), 0.0) + float(weight)
    n = max(1, int(mask.sum()))
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP]
    return [{"id": f"L{layer}E{e}", "weight": round(w / n, 3)} for e, w in top]


def _pipelines_at(routes: Dict[str, Any], rows: Dict[str, Any], mask: Any, layer: int) -> List[Dict[str, Any]]:
    """The pipelines running through the node's layer that hold some of its items, most items first."""
    found = [{"id": p["id"], "items": int(mask[rows[p["id"]]].sum())} for p in routes["pipelines"]
             if layer in p["layers"] and rows[p["id"]].size]
    return sorted([f for f in found if f["items"]], key=lambda f: -f["items"])[:TOP]


def node_entries(session_id: str, name: str, version: str) -> Dict[str, Any]:
    """One saved version's node catalogue."""
    from services.lenses.flows import axes_of, value_of
    from services.lenses.store import lens_dir, read_manifest, read_version, validation_headline
    from services.lenses.view import open_lens
    from services.llm.cards import passing_analysts, read_card

    view = open_lens(session_id, name, version)
    folder = lens_dir(session_id, name)
    manifest = read_manifest(folder)
    path = folder / "details" / f"{view.version}.json"
    details = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    passing, axes, entries = passing_analysts(), axes_of(view), []
    routes_path = folder / "routes.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8")) if routes_path.exists() else None
    index = {item["probe_id"]: i for i, item in enumerate(view.items)}
    pipeline_rows = {p["id"]: np.array([index[m] for m in p["member_ids"] if m in index], dtype=int)
                     for p in (routes or {}).get("pipelines", [])}
    for li, layer in enumerate(view.layers):
        codes = view.nodes[:, li]
        layer_details = (details.get("layers") or {}).get(str(layer), {})
        for node in sorted(set(codes.tolist())):
            mask = codes == node
            members = np.flatnonzero(mask)
            makeup = {axis: dict(Counter(v for i in members if (v := value_of(view.items[int(i)], axis)) is not None))
                      for axis in axes}
            top = max((makeup.get("label") or {"": 0}).items(), key=lambda kv: kv[1])
            card_id = f"L{layer}C{node}"
            card = read_card(folder, str(view.version), card_id)
            tested = card is not None and (card["model"], card["prompt_version"]) in passing
            entries.append({
                "id": card_id, "layer": layer, "node": int(node), "items": int(members.size), "makeup": makeup,
                "majority": {"axis": "label", "value": top[0] or None, "share": round(top[1] / members.size, 3)},
                "from": _top(view.nodes[mask, li - 1], f"L{view.layers[li - 1]}C") if li > 0 else [],
                "to": _top(view.nodes[mask, li + 1], f"L{view.layers[li + 1]}C") if li + 1 < len(view.layers) else [],
                "experts": _top(view.experts[mask, li, 0], f"L{layer}E"),
                "experts_by_weight": _by_weight(view, mask, li, layer),
                "pipelines": None if routes is None else _pipelines_at(routes, pipeline_rows, mask, layer),
                "details": _details(layer_details, int(node)),
                "report": _report(folder, str(view.version), card, tested)})
    return {"format": FORMAT,
            "lens": {"session_id": view.session_id, "name": name, "version": view.version, "items": len(view.items),
                     "site": manifest.site.model_dump(), "settings": manifest.settings.model_dump()},
            "validation": validation_headline(folder, manifest, read_version(folder, str(view.version))),
            "nodes": entries}


def nodes_path(session_id: str, name: str, version: str, records: Optional[Path] = None) -> Path:
    from api import config

    return (records or Path(config.LENS_RECORDS_PATH)) / session_id / name / version / "nodes.json"


def write_nodes(session_id: str, name: str, version: str, records: Optional[Path] = None) -> Optional[Path]:
    """Write a saved version's catalogue beside its records in the repo; nothing for a draft. The
    file holds no time stamp, so writing it again unchanged leaves no difference for git."""
    from services.lenses.store import lens_dir, read_version

    if read_version(lens_dir(session_id, name), version).state != "saved":
        return None
    catalogue = node_entries(session_id, name, version)
    path = nodes_path(catalogue["lens"]["session_id"], name, version, records)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(".nodes.json.tmp")
    tmp.write_text(json.dumps(catalogue, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    _write_routes_record(session_id, name, version, path.parent)
    return path


def _write_routes_record(session_id: str, name: str, version: str, folder: Path) -> None:
    """The version's routes beside its nodes, with the nodes each pipeline's items sit in at this
    version and without the members' ids (the lake keeps those)."""
    from services.lenses.routes import serve_routes
    from services.lenses.store import lens_dir
    from services.lenses.view import open_lens

    source = lens_dir(session_id, name) / "routes.json"
    if not source.exists():
        return
    served = serve_routes(open_lens(session_id, name, version), json.loads(source.read_text(encoding="utf-8")))
    served["pipelines"] = [{k: v for k, v in p.items() if k != "member_ids"} for p in served["pipelines"]]
    served.pop("seconds", None)  # no time stamps: writing again unchanged leaves no difference for git
    tmp = folder / ".routes.json.tmp"
    tmp.write_text(json.dumps(served, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, folder / "routes.json")


def atlas_nodes(records: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Every saved version's node entries, each with its lens and whether the lens is validated."""
    from api import config

    found: List[Dict[str, Any]] = []
    for path in sorted((records or Path(config.LENS_RECORDS_PATH)).glob("*/*/*/nodes.json")):
        catalogue = json.loads(path.read_text(encoding="utf-8"))
        lens = catalogue["lens"]
        found += [{"session_id": lens["session_id"], "lens": lens["name"], "version": lens["version"],
                   "validated": catalogue.get("validation") is not None, **entry} for entry in catalogue["nodes"]]
    return found
