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
from services.lenses.data import LensFilters
from services.lenses.search import SearchGrid
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


def _announce(request: Request, session_id: str, name: str, change: str) -> None:
    """Tell the open apps a lens changed (the event stream's `lens` event)."""
    events = getattr(request.app.state, "events", None)
    if events is not None:
        events.publish("lens", {"session_id": session_id, "name": name, "change": change})


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
        if job.kind in ("lens_build", "lens_search") and job.state in ("queued", "running") and same:
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
    analysis_budget: int = Field(default=25, ge=0, le=200)  # calls for the version's reports; 0 for none
    created_by: str = "app"


@router.post("/sessions/{session_id}/lenses/{name}/versions")
def new_lens_version(request: Request, session_id: str, name: str, body: VersionRequest) -> Dict[str, Any]:
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
        record = new_version(folder, ks, sources).model_dump()
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    _announce(request, manifest.session_id, name, "version")
    return record


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
    from services.lenses.store import lens_dir, read_manifest

    try:
        session = session_dir(session_id).name
        if not (lens_dir(session, name) / "lens.json").exists():
            raise FileNotFoundError(f"Lens '{name}' not found in {session}")
        if read_manifest(lens_dir(session, name)).kind != "umap":
            raise ValueError(f"'{name}' is a mass-mean lens: it is validated when it is built")
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


class TuneRequest(BaseModel):
    name: Optional[str] = None  # the tuned lens; "<lens>-tuned" when not given
    target_axis: str = "label"
    grid: Optional[SearchGrid] = None
    k_min: int = Field(2, ge=2, le=10)
    k_max: int = Field(10, ge=2, le=10)
    test_share: float = Field(0.2, ge=0.1, le=0.5)
    family_field: str = "scene"
    n_folds: int = Field(5, ge=2, le=10)
    seed: Optional[int] = None
    workers: Optional[int] = None
    created_by: str = "app"


@router.post("/sessions/{session_id}/lenses/{name}/tune", status_code=202)
def start_tuning(request: Request, session_id: str, name: str, body: TuneRequest) -> Dict[str, Any]:
    """Tune a UMAP lens in the background (DESIGN.md C4): search its settings and k per layer, build
    the tuned lens and validate it. Returns the job at once."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.data import session_dir
    from services.lenses.flows import axes_of
    from services.lenses.search import tuned_name
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.view import open_lens

    grid = body.grid or SearchGrid()
    try:
        session = session_dir(session_id).name
        if not (lens_dir(session, name) / "lens.json").exists():
            raise FileNotFoundError(f"Lens '{name}' not found in {session}")
        if read_manifest(lens_dir(session, name)).kind != "umap":
            raise ValueError(f"'{name}' is a mass-mean lens; only UMAP lenses are tuned")
        tuned = tuned_name(name, body.name)
        if lens_dir(session, tuned).exists():
            raise FileExistsError(f"Lens '{tuned}' already exists in {session}")
        grid.settings()  # an empty or oversized grid is refused here, not in the job
        if body.k_min > body.k_max:
            raise ValueError(f"k_min {body.k_min} is above k_max {body.k_max}")
        axes = axes_of(open_lens(session, name))
        if body.target_axis not in axes or len(axes[body.target_axis]) < 2:
            raise ValueError(f"'{name}' has no axis '{body.target_axis}' with two values or more")
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        raise _fail(e)
    scheduler: JobScheduler = request.app.state.jobs
    for job in scheduler.store.list():
        if job.kind in ("lens_build", "lens_search") and job.state in ("queued", "running") and \
                job.params.get("session_id") == session and job.params.get("name") == tuned:
            raise HTTPException(status_code=409, detail=f"Lens '{tuned}' is already being built or tuned ({job.id})")
    params = body.model_dump(exclude={"created_by", "grid"}) | {
        "session_id": session, "source_lens": name, "name": tuned, "grid": grid.model_dump()}
    job = scheduler.submit("lens_search", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "source": name, "name": tuned}


@router.get("/sessions/{session_id}/lenses/{name}/search")
def lens_search_record(session_id: str, name: str) -> Dict[str, Any]:
    """A tuned lens's search: every candidate's scores, the winners and their test scores (404 for
    a lens that wasn't tuned)."""
    from services.lenses.store import lens_dir

    try:
        path = lens_dir(session_id, name) / "search.json"
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Lens '{name}' was not made by a tuning")
    result: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return result


class MassMeanRequest(BaseModel):
    session_id: str
    name: str
    label_a: str
    label_b: str
    token_position: int = 1
    family_field: str = "scene"
    created_by: str = "app"


@router.post("/lenses/mass-mean", status_code=202)
def build_mass_mean_lens(request: Request, body: MassMeanRequest) -> Dict[str, Any]:
    """Start building a mass-mean lens (one contrast, label A against label B) in the background."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.data import session_dir
    from services.lenses.store import lens_dir, valid_name

    try:
        session = session_dir(body.session_id).name
        if not valid_name(body.name):
            raise ValueError(f"not a lens name: {body.name!r} (lower-case letters, digits, - and _)")
        if lens_dir(session, body.name).exists():
            raise FileExistsError(f"Lens '{body.name}' already exists in {session}")
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        raise _fail(e)
    scheduler: JobScheduler = request.app.state.jobs
    params = body.model_dump(exclude={"created_by"}) | {"session_id": session}
    job = scheduler.submit("mass_mean_build", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "name": body.name}


class ReadRequest(BaseModel):
    target: Optional[str] = None  # the capture to read; the lens's own (its other steps) by default
    key: Optional[str] = None  # the reading's name; made from the target and filters when not given
    filters: LensFilters = Field(default_factory=LensFilters)
    position: Optional[int] = None  # the token position read; the lens's own by default
    created_by: str = "app"


@router.post("/sessions/{session_id}/lenses/{name}/readings", status_code=202)
def start_reading(request: Request, session_id: str, name: str, body: ReadRequest) -> Dict[str, Any]:
    """Read a capture through a saved UMAP lens in the background (DESIGN.md B5): each item placed
    in the lens's space at every layer, with its nearest lens items. Returns the job at once."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.data import session_dir
    from services.lenses.readout import reading_key, readings_dir, valid_key
    from services.lenses.store import lens_dir, read_manifest

    try:
        session = session_dir(session_id).name
        folder = lens_dir(session, name)
        if not (folder / "lens.json").exists():
            raise FileNotFoundError(f"Lens '{name}' not found in {session}")
        if read_manifest(folder).kind != "umap":
            raise ValueError(f"'{name}' is a mass-mean lens: GET its readings with ?target=<capture>")
        target = session_dir(body.target or session).name
        key = body.key or reading_key(target, body.filters)
        if not valid_key(key):
            raise ValueError(f"not a reading name: {key!r} (lowercase letters, digits, '_' and '-')")
        if (readings_dir(folder) / key).exists():
            raise FileExistsError(f"Lens '{name}' already has a reading {key!r}")
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        raise _fail(e)
    scheduler: JobScheduler = request.app.state.jobs
    for job in scheduler.store.list():
        if job.kind == "lens_read" and job.state in ("queued", "running") and job.params.get("session_id") == session \
                and job.params.get("name") == name and job.params.get("key") == key:
            raise HTTPException(status_code=409, detail=f"Reading {key!r} is already being made ({job.id})")
    params = body.model_dump(exclude={"created_by", "target", "key"}) | {
        "session_id": session, "name": name, "target": target, "key": key, "created_by": body.created_by}
    job = scheduler.submit("lens_read", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "name": name, "key": key}


@router.get("/sessions/{session_id}/lenses/{name}/readings")
def lens_readings(session_id: str, name: str, target: Optional[str] = None, position: Optional[int] = None,
                  key: Optional[str] = None, version: Optional[str] = None, rank: int = 1) -> Dict[str, Any]:
    """A lens's readings. A mass-mean lens reads any capture (`target`, its own by default) at once:
    each item's position along the contrast at every layer, class means at -1 and +1. A UMAP lens
    serves a reading made by POST (`key`; the summary lists them): each item's node at every
    layer at `version`, its share of the vote, how far out it sits, and its expert at `rank`."""
    from services.lenses.massmean import readings
    from services.lenses.readout import list_readings, serve_reading
    from services.lenses.store import lens_dir, read_manifest

    try:
        folder = lens_dir(session_id, name)
        if read_manifest(folder).kind == "mass_mean":
            return readings(folder, target or session_id, position)
        if key is None:
            made = [r["key"] for r in list_readings(folder)]
            raise ValueError(f"name a reading with ?key= ({', '.join(made) if made else 'none made yet: POST one'})")
        return serve_reading(folder, key, version, rank)
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)


@router.get("/sessions/{session_id}/lenses/{name}/marks")
def lens_marks(session_id: str, name: str, version: Optional[str] = None) -> Dict[str, Any]:
    """Where the UMAP lens and raw space disagree: per layer, the items whose co-members in the
    lens's node and in the best raw grouping at the same k overlap less than half (Jaccard), and
    how many sit in each node. Needs the lens validated (the raw groupings come from it)."""
    from services.lenses.raw import lens_marks as find_marks
    from services.lenses.store import lens_dir

    view = _open(session_id, name, False, version)
    found = find_marks(view, lens_dir(session_id, name))
    if found is None:
        raise HTTPException(status_code=404, detail=f"Lens '{name}' has no raw groupings yet: validate it first")
    return found


class DetailsRequest(BaseModel):
    version: Optional[str] = None
    created_by: str = "app"


@router.post("/sessions/{session_id}/lenses/{name}/details", status_code=202)
def start_details(request: Request, session_id: str, name: str, body: DetailsRequest) -> Dict[str, Any]:
    """Work out what comes with each node (or each layer of a mass-mean lens) in the background:
    neurons, the logit lens, the surface check and the routing measures."""
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
    params = {"session_id": session, "name": name, "version": body.version}
    job = scheduler.submit("lens_details", params, created_by=body.created_by)
    return {"job_id": job.id, "session_id": session, "name": name}


@router.get("/sessions/{session_id}/lenses/{name}/details")
def lens_details(session_id: str, name: str, version: Optional[str] = None) -> Dict[str, Any]:
    """A lens version's node details (a mass-mean lens's layer details); 404 until worked out."""
    from services.lenses.store import lens_dir, read_manifest

    try:
        folder = lens_dir(session_id, name)
        manifest = read_manifest(folder)
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    key = "mass_mean" if manifest.kind == "mass_mean" else (version or manifest.current or "")
    path = folder / "details" / f"{key}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"No details for '{name}' {key} yet")
    result: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return result


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
def save_lens_version(request: Request, session_id: str, name: str, body: SaveRequest) -> Dict[str, Any]:
    """Freeze a version, with its keywords, and copy its records into the repo. Its reports are
    then written in the background within `analysis_budget` calls (DESIGN.md E8; 0 for none)."""
    from services.jobs.scheduler import JobScheduler
    from services.lenses.store import save_version

    try:
        record = save_version(session_id, name, body.version, body.keywords).model_dump()
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    if body.analysis_budget > 0:
        scheduler: JobScheduler = request.app.state.jobs
        job = scheduler.submit("lens_analysis", {"session_id": session_id, "name": name, "version": body.version,
                                                 "budget": body.analysis_budget}, created_by=body.created_by)
        record["analysis_job_id"] = job.id
    _write_catalogue(session_id, name, body.version)
    _announce(request, session_id, name, "saved")
    return record


def _write_catalogue(session_id: str, name: str, version: str) -> None:
    """A saved version's atlas entries (DESIGN.md H); a failure is logged, never fails the save."""
    import logging

    from services.lenses.atlas import write_nodes

    try:
        write_nodes(session_id, name, version)
    except Exception:
        logging.getLogger(__name__).exception("Couldn't write the atlas entries of %s %s", name, version)


@router.get("/sessions/{session_id}/lenses/{name}/trajectory")
def lens_trajectory(session_id: str, name: str, legacy: bool = False, reading: Optional[str] = None) -> Dict[str, Any]:
    """The 3-D view's points (DESIGN.md E5): every item at every layer in the lens's own space, on
    its three main directions, each layer turned to line up with the one before (frame.py), with
    the items of a reading (`reading`, its key) placed in the same frame. A legacy schema's own
    3-D fit is lined up the same way, and said to be a separate fit."""
    import numpy as np

    from services.lenses.data import session_dir
    from services.lenses.frame import lens_frame
    from services.lenses.readout import readings_dir, valid_key
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.view import _item_dict

    view = _open(session_id, name, legacy, None)
    try:
        if legacy:
            points = json.loads((session_dir(session_id) / "clusterings" / name / "trajectory_points.json").read_text())
            at = [{p["probe_id"]: (p["x"], p["y"], p["z"]) for p in points.get(str(layer), [])} for layer in view.layers]
            items = [item for item in view.items if all(item["probe_id"] in layer for layer in at)]
            embeddings = [np.array([layer[item["probe_id"]] for item in items], dtype=np.float64) for layer in at]
        else:
            folder = lens_dir(session_id, name)
            manifest = read_manifest(folder)
            embed = np.load(folder / "fit" / "embed.npz")["embedding"].astype(np.float64)
            items = view.items
            embeddings = [embed[li][:, :min(manifest.settings.at(li).dimensions, len(items) - 1)]
                          for li in range(len(view.layers))]
        frame = lens_frame(embeddings)

        def shown(item: Dict[str, Any]) -> Dict[str, Any]:
            return {key: item.get(key) for key in ("probe_id", "label", "categories", "step", "target_word")}

        out: Dict[str, Any] = {
            "lens": name, "legacy": legacy, "fit": "separate" if legacy else "lens", "layers": view.layers,
            "share": frame.shares, "items": [shown(item) for item in items],
            "points": np.round(np.stack([frame.project(li, e) for li, e in enumerate(embeddings)], axis=1), 4).tolist()}
        if reading is not None:
            if legacy or not valid_key(reading) or not (readings_dir(folder) / reading / "read.npz").exists():
                raise FileNotFoundError(f"Lens '{name}' has no reading {reading!r}")
            import pyarrow.parquet as pq

            placed = np.load(readings_dir(folder) / reading / "read.npz")["embedding"].astype(np.float64)
            read_items = [_item_dict(row) for row in pq.read_table(readings_dir(folder) / reading / "items.parquet").to_pylist()]
            out["read"] = {"key": reading, "items": [shown(item) for item in read_items],
                           "points": np.round(np.stack([frame.project(li, placed[:, li]) for li in range(len(view.layers))],
                                                       axis=1), 4).tolist()}
    except (FileNotFoundError, ValueError) as e:
        raise _fail(e)
    return out
