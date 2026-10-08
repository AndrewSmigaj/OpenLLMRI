"""LLM analysis of lenses (DESIGN.md E8): cards written in the background from evidence packets,
their numbers checked; questions about a card's subject; cards Claude Code writes through the
same checker; and the analyst tests."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()


class AnalysisRequest(BaseModel):
    cards: List[str] = Field(default_factory=list)  # card ids; empty for a save's plan
    budget: int = Field(default=25, ge=1, le=200)
    version: Optional[str] = None
    model: Optional[str] = None
    created_by: str = "app"


class QuestionRequest(BaseModel):
    card_id: str
    question: str = Field(min_length=3, max_length=2000)
    version: Optional[str] = None
    created_by: str = "app"


class CardSubmission(BaseModel):
    output: Dict[str, Any]  # title, pattern, summary, points, caveats
    model: str = "Claude Code"
    version: Optional[str] = None


class TestsRequest(BaseModel):
    session_id: str
    name: str
    layer: Optional[int] = None
    budget: int = Field(default=24, ge=4, le=100)
    model: Optional[str] = None
    created_by: str = "app"


def _lens(session_id: str, name: str) -> Any:
    """The lens's folder and manifest; 404 for no such lens, 400 for a mass-mean lens."""
    from services.lenses.store import lens_dir, read_manifest

    folder = lens_dir(session_id, name)
    if not (folder / "lens.json").exists():
        raise HTTPException(status_code=404, detail=f"Lens '{name}' not found in {session_id}")
    manifest = read_manifest(folder)
    if manifest.kind != "umap":
        raise HTTPException(status_code=400, detail=f"'{name}' is a {manifest.kind} lens: cards are for UMAP lenses")
    return folder, manifest


def _submit(request: Request, kind: str, params: Dict[str, Any], created_by: str) -> Dict[str, Any]:
    from services.jobs.scheduler import JobScheduler

    scheduler: JobScheduler = request.app.state.jobs
    job = scheduler.submit(kind, params, created_by=created_by)
    return {"job_id": job.id}


@router.post("/sessions/{session_id}/lenses/{name}/analysis", status_code=202)
def start_analysis(request: Request, session_id: str, name: str, body: AnalysisRequest) -> Dict[str, Any]:
    """Write cards in the background: the given card ids, or a save's plan (the lens report, the
    k advisor, split points, then the nodes at the best layer), within `budget` calls."""
    from services.llm.cards import valid_card_id

    _, manifest = _lens(session_id, name)
    bad = [card for card in body.cards if not valid_card_id(card)]
    if bad:
        raise HTTPException(status_code=400, detail=f"not card ids: {', '.join(bad)}")
    params = {"session_id": manifest.session_id, "name": name, "version": body.version, "cards": body.cards,
              "budget": body.budget, "model": body.model}
    return {**_submit(request, "lens_analysis", params, body.created_by), "session_id": manifest.session_id, "name": name}


@router.get("/sessions/{session_id}/lenses/{name}/cards")
def list_lens_cards(session_id: str, name: str, version: Optional[str] = None) -> Dict[str, Any]:
    """A version's cards in brief (the current version by default)."""
    from services.llm.cards import list_cards

    folder, manifest = _lens(session_id, name)
    chosen = version or manifest.current or ""
    return {"version": chosen, "cards": list_cards(folder, chosen)}


@router.get("/sessions/{session_id}/lenses/{name}/cards/{card_id}")
def get_lens_card(session_id: str, name: str, card_id: str, version: Optional[str] = None) -> Dict[str, Any]:
    """A card, with the facts it cites, whether its analyst passed the tests, and whether its
    evidence has changed since it was written (stale)."""
    from services.llm.cards import (
        card_text,
        current_check,
        passing_analysts,
        read_card,
        valid_card_id,
    )
    from services.llm.numbers import cited_ids
    from services.llm.packets import build_packet, load_evidence, packet_hash

    folder, manifest = _lens(session_id, name)
    chosen = version or manifest.current or ""
    card = read_card(folder, chosen, card_id) if valid_card_id(card_id) else None
    if card is None:
        raise HTTPException(status_code=404, detail=f"No card {card_id} for '{name}' {chosen} yet")
    packet = json.loads((folder / "analysis" / chosen / "packets" / f"{card['packet_hash']}.json").read_text(encoding="utf-8"))
    facts = {fact["id"]: fact for fact in packet["facts"]}
    cited = cited_ids(card_text(card["output"])) if card.get("output") else []
    try:
        current: Optional[str] = packet_hash(build_packet(load_evidence(session_id, name, chosen), card_id).as_dict())
    except (FileNotFoundError, ValueError):
        current = None
    return {**card, "check": current_check(folder, chosen, card), "facts": {fid: facts[fid] for fid in cited if fid in facts},
            "tested": (card["model"], card["prompt_version"]) in passing_analysts(),
            "stale": current != card["packet_hash"]}


@router.get("/sessions/{session_id}/lenses/{name}/packets/{card_id}")
def get_packet(session_id: str, name: str, card_id: str, version: Optional[str] = None) -> Dict[str, Any]:
    """A card id's evidence packet, as analysts read it; Claude Code reads the same."""
    from services.llm.packets import build_packet, load_evidence, packet_hash, render

    _lens(session_id, name)
    try:
        packet = build_packet(load_evidence(session_id, name, version), card_id).as_dict()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"hash": packet_hash(packet), "packet": packet, "text": render(packet)}


@router.post("/sessions/{session_id}/lenses/{name}/cards/{card_id}")
def submit_lens_card(session_id: str, name: str, card_id: str, body: CardSubmission) -> Dict[str, Any]:
    """A card Claude Code wrote from the packet (the /analyze skill): kept when every number
    traces to a cited fact; otherwise 422, with the failures to fix."""
    from services.llm.cards import submit_card

    _lens(session_id, name)
    try:
        found = submit_card(session_id, name, card_id, body.output, body.model, body.version)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not found["stored"]:
        raise HTTPException(status_code=422, detail={"message": "some numbers don't trace to the packet's facts",
                                                     "check": found["check"]})
    return found


@router.post("/sessions/{session_id}/lenses/{name}/ask", status_code=202)
def ask_about_card(request: Request, session_id: str, name: str, body: QuestionRequest) -> Dict[str, Any]:
    """Ask an analyst a question about a card's subject, in the background."""
    from services.llm.cards import valid_card_id

    _, manifest = _lens(session_id, name)
    if not valid_card_id(body.card_id):
        raise HTTPException(status_code=400, detail=f"not a card id: {body.card_id}")
    params = {"session_id": manifest.session_id, "name": name, "version": body.version, "card_id": body.card_id,
              "question": body.question}
    return _submit(request, "lens_question", params, body.created_by)


@router.get("/sessions/{session_id}/lenses/{name}/questions")
def list_questions(session_id: str, name: str, card_id: Optional[str] = None,
                   version: Optional[str] = None) -> Dict[str, Any]:
    """The questions asked about a version (one card's, given its id), newest first."""
    folder, manifest = _lens(session_id, name)
    chosen = version or manifest.current or ""
    root = folder / "analysis" / chosen / "questions"
    found = [json.loads(path.read_text(encoding="utf-8")) for path in root.glob("*.json")] if root.exists() else []
    found = [q for q in found if card_id is None or q["card_id"] == card_id]
    for q in found:
        q["facts"] = _cited(folder / "analysis" / chosen, q["packet_hash"], q.get("answer") or "")
    return {"version": chosen, "questions": sorted(found, key=lambda q: str(q["created_at"]), reverse=True)}


def _cited(base: Any, packet: str, text: str) -> Dict[str, Any]:
    """The facts a text cites, from the packet it was written from."""
    from services.llm.numbers import cited_ids

    path = base / "packets" / f"{packet}.json"
    facts = {f["id"]: f for f in json.loads(path.read_text(encoding="utf-8"))["facts"]} if path.exists() else {}
    return {fid: facts[fid] for fid in cited_ids(text) if fid in facts}


@router.post("/analysts/tests", status_code=202)
def start_analyst_tests(request: Request, body: TestsRequest) -> Dict[str, Any]:
    """Test the analysts at one layer of a lens (its best layer by default): decoys, planted
    findings and predictive descriptions."""
    _, manifest = _lens(body.session_id, body.name)
    params = {"session_id": manifest.session_id, "name": body.name, "layer": body.layer, "budget": body.budget,
              "model": body.model}
    return _submit(request, "analyst_tests", params, body.created_by)


@router.get("/analysts/tests")
def analyst_tests() -> Dict[str, Any]:
    """The latest analyst test run, the (model, prompt version) pairs that have passed, and the
    prompt version cards are written with now."""
    from services.llm.analyst_tests import latest_tests
    from services.llm.cards import passing_analysts
    from services.llm.prompts import PROMPT_VERSION

    return {"latest": latest_tests(), "prompt_version": PROMPT_VERSION,
            "passing": [{"model": model, "prompt_version": version} for model, version in sorted(passing_analysts())]}
