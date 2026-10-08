"""Lenses: build one (a background job), list and open them, read their flows and members, choose
a new k, save a version.

Every lens endpoint takes `legacy=true` to open a clustering built the old way through the same
shapes. Responses that draw a view carry a `recipe`: what lens, version and settings made it, and
the commits that built and served it, so any figure can be made again exactly.
"""

import json
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from services.lenses.build import LensBuildParams
from services.lenses.view import LensView

router = APIRouter()


def _fail(error: Exception) -> HTTPException:
    if isinstance(error, FileNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, FileExistsError):
        return HTTPException(status_code=409, detail=str(error))
    return HTTPException(status_code=400, detail=str(error))


def _open(session_id: str, name: str, legacy: bool, version: Optional[str]) -> LensView:
    from services.lenses.view import open_legacy, open_lens

    try:
        return open_legacy(session_id, name) if legacy else open_lens(session_id, name, version)
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


def _axes_list(raw: Optional[str]) -> List[str]:
    return [axis for axis in (raw or "").split(",") if axis]


def _recipe(view: LensView, **params: Any) -> Dict[str, Any]:
    from services.lenses.store import git_state

    commit, dirty = git_state()
    return {"lens": {"session_id": view.session_id, "name": view.name, "legacy": view.legacy,
                     "version": view.version},
            "settings": view.settings, "built": view.provenance,
            "served": {"commit": commit, "dirty": dirty},
            "view": {key: value for key, value in params.items() if value is not None}}


def _legacy_summaries(session_id: str) -> List[Dict[str, Any]]:
    from services.lenses.data import session_dir

    root = session_dir(session_id) / "clusterings"
    if not root.exists():
        return []
    found = []
    for folder in sorted(p for p in root.iterdir() if (p / "probe_assignments.json").exists()):
        meta = json.loads((folder / "meta.json").read_text()) if (folder / "meta.json").exists() else {}
        found.append({"name": folder.name, "kind": "umap", "legacy": True, "session_id": session_id,
                      "n_items": meta.get("sample_size"), "settings": meta.get("params", {}),
                      "created_at": meta.get("created_at"), "created_by": meta.get("created_by")})
    return found


@router.get("/sessions/{session_id}/lenses")
def list_lenses(session_id: str) -> List[Dict[str, Any]]:
    """This capture's lenses, then its legacy clusterings (marked `legacy`)."""
    from services.lenses.store import lens_dir, summary
    from services.lenses.store import list_lenses as stored

    try:
        new = [summary(m, lens_dir(session_id, m.name)) for m in stored(session_id)]
        return new + _legacy_summaries(session_id)
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


@router.get("/sessions/{session_id}/lenses/{name}")
def get_lens(session_id: str, name: str, legacy: bool = False) -> Dict[str, Any]:
    """One lens: its manifest (or a legacy schema's settings), axes and layers."""
    from services.lenses.flows import axes_of
    from services.lenses.store import lens_dir, read_manifest

    view = _open(session_id, name, legacy, None)
    detail: Dict[str, Any] = {"name": name, "legacy": legacy, "layers": view.layers,
                              "axes": axes_of(view), "n_items": len(view.items)}
    if not legacy:
        detail["manifest"] = read_manifest(lens_dir(session_id, name)).model_dump()
    return detail


@router.get("/sessions/{session_id}/lenses/{name}/flows")
def lens_flows(session_id: str, name: str, legacy: bool = False, version: Optional[str] = None,
               output_axes: Optional[str] = None) -> Dict[str, Any]:
    """Cluster nodes and links for every layer, plus the output column (grouped by the
    comma-separated `output_axes` when given)."""
    from services.lenses.flows import cluster_flows

    view = _open(session_id, name, legacy, version)
    grouped = _axes_list(output_axes)
    return cluster_flows(view, grouped) | {"recipe": _recipe(view, kind="cluster", output_axes=grouped or None)}


@router.get("/sessions/{session_id}/lenses/{name}/expert-flows")
def lens_expert_flows(session_id: str, name: str, rank: int = 1, legacy: bool = False,
                      version: Optional[str] = None, output_axes: Optional[str] = None) -> Dict[str, Any]:
    """Expert nodes and links at one rank (1 to 4), with the model's own weights."""
    from services.lenses.flows import expert_flows

    view = _open(session_id, name, legacy, version)
    grouped = _axes_list(output_axes)
    try:
        return expert_flows(view, rank, grouped, _expert_order(view)) | {
            "recipe": _recipe(view, kind="expert", rank=rank, output_axes=grouped or None)}
    except ValueError as e:
        raise _fail(e)


_ORDERS: Dict[Tuple[str, str, bool], List[List[int]]] = {}


def _expert_order(view: LensView) -> List[List[int]]:
    """The lens's fixed expert order, computed once per lens (it doesn't depend on the version,
    only on the routing of its items)."""
    from services.lenses.experts import expert_order

    key = (view.session_id, view.name, view.legacy)
    if key not in _ORDERS:
        if len(_ORDERS) >= 16:
            _ORDERS.pop(next(iter(_ORDERS)))
        _ORDERS[key] = expert_order(view)
    return _ORDERS[key]


@router.get("/sessions/{session_id}/lenses/{name}/fingerprint")
def lens_fingerprint(session_id: str, name: str, legacy: bool = False, version: Optional[str] = None,
                     layer: Optional[int] = None, node: Optional[int] = None,
                     axis: Optional[str] = None, value: Optional[str] = None) -> Dict[str, Any]:
    """A population's mean gate weight on each expert at each layer (each row sums to 1): every
    item, a node (`layer` and `node`), or an axis value (`axis` and `value`)."""
    from services.lenses.experts import fingerprint, population

    view = _open(session_id, name, legacy, version)
    try:
        mask = population(view, layer=layer, node=node, axis=axis, value=value)
    except ValueError as e:
        raise _fail(e)
    grid = fingerprint(view, mask)
    who: Dict[str, Any] = ({"layer": layer, "node": node} if node is not None
                           else {"axis": axis, "value": value} if axis else {})
    return {"layers": view.layers, "experts": grid.shape[1], "grid": grid.round(5).tolist(),
            "n_items": int(len(view.items) if mask is None else mask.sum()),
            "recipe": _recipe(view, kind="fingerprint", **who)}


@router.get("/sessions/{session_id}/lenses/{name}/members")
def lens_members(session_id: str, name: str, layer: int, node: Optional[int] = None,
                 expert: Optional[int] = None, rank: int = 1, to_node: Optional[int] = None,
                 to_expert: Optional[int] = None, output: Optional[str] = None,
                 offset: int = 0, limit: int = 50, legacy: bool = False,
                 version: Optional[str] = None) -> Dict[str, Any]:
    """The items in a node or routed to an expert at a rank; with `to_node` or `to_expert`, a link;
    with `output`, those whose generated output is that category."""
    from services.lenses.data import display_fields
    from services.lenses.flows import members

    view = _open(session_id, name, legacy, version)
    try:
        page = members(view, layer, node=node, expert=expert, rank=rank, to_node=to_node,
                       to_expert=to_expert, output=output, offset=offset, limit=min(limit, 500))
    except ValueError as e:
        raise _fail(e)
    shown = display_fields(view.session_id)
    page["items"] = [item | shown.get(item["probe_id"], {}) for item in page["items"]]
    return page


@router.get("/captures/{session_id}/lens-options")
def capture_lens_options(session_id: str) -> Dict[str, Any]:
    """What a capture offers a lens: its labels and steps, sources and token positions, and how
    many items the default filters keep."""
    from services.lenses.options import capture_options

    try:
        return capture_options(session_id)
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


@router.get("/lenses/methods")
def lens_build_methods() -> Dict[str, Any]:
    """The reductions, groupings and automatic k methods a lens build can use, with defaults."""
    from services.lenses.options import lens_methods

    return lens_methods()


class LensBuildRequest(LensBuildParams):
    created_by: str = "app"


@router.post("/lenses", status_code=202)
def build_lens(request: Request, body: LensBuildRequest) -> Dict[str, Any]:
    """Start building a lens in the background; returns the job at once."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.data import session_dir
    from services.lenses.store import lens_dir

    try:
        session = session_dir(body.session_id).name
        if lens_dir(session, body.name).exists():
            raise FileExistsError(f"Lens '{body.name}' already exists in {session}")
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        raise _fail(e)
    scheduler: JobScheduler = request.app.state.jobs
    for job in scheduler.store.list():
        same = job.params.get("name") == body.name and job.params.get("session_id") in (session, body.session_id)
        if job.kind == "lens_build" and job.state in ("queued", "running") and same:
            raise HTTPException(status_code=409, detail=f"Lens '{body.name}' is already being built ({job.id})")
    params = body.model_dump(exclude={"created_by"}) | {"session_id": session}
    job = scheduler.submit("lens_build", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "name": body.name}


class VersionRequest(BaseModel):
    k: Optional[int] = Field(None, ge=1, le=50)
    k_per_layer: Optional[List[int]] = None
    k_auto: Optional[str] = None


class SaveRequest(BaseModel):
    version: str
    keywords: List[str] = Field(default_factory=list)


@router.post("/sessions/{session_id}/lenses/{name}/versions")
def new_lens_version(session_id: str, name: str, body: VersionRequest) -> Dict[str, Any]:
    """Cut the saved trees at a new k (by hand, per layer, or a named method): a new draft version."""
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.versions import heldout_best, new_version, resolve_k

    try:
        folder = lens_dir(session_id, name)
        manifest = read_manifest(folder)
        suggestions = manifest.suggestions
        if body.k_auto == "heldout" and (folder / "validation.json").exists():
            best = heldout_best(json.loads((folder / "validation.json").read_text(encoding="utf-8")))
            suggestions = {layer: found | ({"heldout": best[layer]} if layer in best else {})
                           for layer, found in suggestions.items()}
        ks, sources = resolve_k(manifest.layers, suggestions, body.k, body.k_per_layer, body.k_auto)
        return new_version(folder, ks, sources).model_dump()
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


class ValidateRequest(BaseModel):
    family_field: str = "scene"
    n_folds: int = Field(5, ge=2, le=20)
    seeds: int = Field(3, ge=1, le=10)
    workers: Optional[int] = None
    created_by: str = "app"


@router.post("/sessions/{session_id}/lenses/{name}/validate", status_code=202)
def start_validation(request: Request, session_id: str, name: str, body: ValidateRequest) -> Dict[str, Any]:
    """Score the lens on held-out data, with its k profile, in the background; returns the job."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.data import session_dir
    from services.lenses.store import lens_dir

    try:
        session = session_dir(session_id).name
        if not (lens_dir(session, name) / "lens.json").exists():
            raise FileNotFoundError(f"Lens '{name}' not found in {session}")
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    scheduler: JobScheduler = request.app.state.jobs
    for job in scheduler.store.list():
        if job.kind == "lens_validate" and job.state in ("queued", "running") and \
                job.params.get("name") == name and job.params.get("session_id") == session:
            raise HTTPException(status_code=409, detail=f"Lens '{name}' is already being validated ({job.id})")
    params = body.model_dump(exclude={"created_by"}) | {"session_id": session, "name": name}
    job = scheduler.submit("lens_validate", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "name": name}


@router.get("/sessions/{session_id}/lenses/{name}/validation")
def lens_validation(session_id: str, name: str) -> Dict[str, Any]:
    """The lens's held-out scores and k profile, per layer and k (404 until it is validated)."""
    from services.lenses.store import lens_dir

    try:
        path = lens_dir(session_id, name) / "validation.json"
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Lens '{name}' has not been validated")
    result: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return result


@router.post("/sessions/{session_id}/lenses/{name}/save")
def save_lens_version(session_id: str, name: str, body: SaveRequest) -> Dict[str, Any]:
    """Freeze a version, with its keywords, and copy its records into the repo."""
    from services.lenses.store import save_version

    try:
        return save_version(session_id, name, body.version, body.keywords).model_dump()
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


@router.get("/sessions/{session_id}/lenses/{name}/trajectory")
def lens_trajectory(session_id: str, name: str, legacy: bool = False) -> Dict[str, Any]:
    """The 3-D points per layer for the trajectory view, in the legacy endpoint's shape."""
    import numpy as np

    from services.lenses.data import session_dir
    from services.lenses.store import lens_dir

    try:
        if legacy:
            folder = session_dir(session_id) / "clusterings" / name
            points = json.loads((folder / "trajectory_points.json").read_text())
            meta = json.loads((folder / "meta.json").read_text()) if (folder / "meta.json").exists() else {}
            return {"schema_name": name, "sample_size": int(meta.get("sample_size") or 0),
                    "layers": sorted(int(k) for k in points), "points_by_layer": points}
        view = _open(session_id, name, False, None)
        view3d = np.load(lens_dir(session_id, name) / "fit" / "embed.npz")["view3d"]
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    by_layer: Dict[str, List[Dict[str, Any]]] = {}
    for li, layer in enumerate(view.layers):
        by_layer[str(layer)] = [
            {"probe_id": item["probe_id"], "x": float(p[0]), "y": float(p[1]), "z": float(p[2]),
             "label": item["label"], "target_word": item["target_word"], "step": item.get("step"),
             "categories_json": json.dumps(item["categories"]) if item["categories"] else None}
            for item, p in zip(view.items, view3d[li])]
    return {"schema_name": name, "sample_size": len(view.items), "layers": view.layers,
            "points_by_layer": by_layer}
