"""Cards (DESIGN.md E8): an analyst's report on one thing in a lens, written from its evidence
packet, with every number checked against the packet.

A card has one analyst and says so; the lens report is two independent drafts, reconciled. A
card whose numbers don't trace is retried once with the failures listed, then kept and flagged.
Cards live with the lens version they describe, `<lens>/analysis/<version>/cards/<id>.json`,
beside the packets they were written from (`packets/<hash>.json`) and the questions asked about
them (`questions/<id>.json`).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.llm.numbers import check_numbers
from services.llm.packets import LensEvidence, fact_values, packet_hash, render, split_points
from services.llm.prompts import (
    CARD_SCHEMA,
    PROMPT_VERSION,
    RECONCILED_SCHEMA,
    card_prompt,
    reconcile_prompt,
    retry_prompt,
)
from services.llm.runner import ClaudeRunner, Runner, RunResult

TEXT_FIELDS = ("title", "summary", "points", "caveats", "disagreements")
DEFAULT_BUDGET = 25  # calls a save may make (DESIGN.md E8)


class Budget:
    """The calls a job may still make."""

    def __init__(self, calls: int) -> None:
        self.left, self.used = calls, 0

    def take(self) -> bool:
        if self.left <= 0:
            return False
        self.left, self.used = self.left - 1, self.used + 1
        return True


def card_text(output: Dict[str, Any]) -> str:
    """A card's sentences as one text for the number check, one field or list entry a line."""
    lines: List[str] = []
    for key in TEXT_FIELDS:
        value = output.get(key)
        lines += [str(v) for v in value] if isinstance(value, list) else ([str(value)] if value else [])
    return "\n".join(lines)


def _stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _record(packet: Dict[str, Any], output: Optional[Dict[str, Any]], check: Optional[Dict[str, Any]],
            runs: List[RunResult], analysts: int, drafts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    last = runs[-1]
    return {
        "format": 1, "card_id": packet["card_id"], "kind": packet["kind"], "subject": packet["subject"],
        "lens": packet["lens"], "packet_hash": packet_hash(packet), "prompt_version": PROMPT_VERSION,
        "model": last.model, "written_by": "claude -p", "analysts": analysts,
        "output": output, "check": check, "error": None if output is not None else last.error,
        "drafts": drafts or [], "calls": len(runs), "seconds": round(sum(r.seconds for r in runs), 1),
        "safety_stops": sum(r.safety_stops for r in runs), "created_at": _stamp(),
    }


def _checked(runner: Runner, prompt: str, schema: Dict[str, Any], packet: Dict[str, Any],
             budget: Budget, runs: List[RunResult]) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """One call and its number check, retried once (budget allowing) when numbers don't trace."""
    evidence, facts = render(packet), fact_values(packet)
    first = runner.run(prompt, schema)
    runs.append(first)
    if first.output is None:
        return None, None
    check = {**check_numbers(card_text(first.output), facts), "retried": False}
    if check["passed"] or not budget.take():
        return first.output, check
    second = runner.run(retry_prompt(evidence, packet["kind"], first.output, check["failures"]), schema)
    runs.append(second)
    if second.output is None:
        return first.output, check
    return second.output, {**check_numbers(card_text(second.output), facts), "retried": True,
                           "first_failures": check["failures"]}


def write_card(runner: Runner, packet: Dict[str, Any], budget: Budget) -> Optional[Dict[str, Any]]:
    """One analyst's card on a packet, or None when the budget has no call left."""
    if not budget.take():
        return None
    runs: List[RunResult] = []
    output, check = _checked(runner, card_prompt(render(packet), packet["kind"]), CARD_SCHEMA, packet, budget, runs)
    return _record(packet, output, check, runs, analysts=1)


def write_report(runner: Runner, packet: Dict[str, Any], budget: Budget) -> Optional[Dict[str, Any]]:
    """The lens report (DESIGN.md C7): two independent drafts, then one card reconciling them.
    When a draft fails or the budget runs out, the first draft stands as a one-analyst card."""
    drafts: List[Dict[str, Any]] = []
    for _ in range(2):
        draft = write_card(runner, packet, budget)
        if draft is None or draft["output"] is None:
            return drafts[0] if drafts else draft
        drafts.append(draft)
    if not budget.take():
        return drafts[0]
    runs: List[RunResult] = []
    prompt = reconcile_prompt(render(packet), packet["kind"], [d["output"] for d in drafts])
    output, check = _checked(runner, prompt, RECONCILED_SCHEMA, packet, budget, runs)
    if output is None:
        return drafts[0]
    card = _record(packet, output, check, runs, analysts=2, drafts=[d["output"] for d in drafts])
    card["calls"] += sum(d["calls"] for d in drafts)
    card["seconds"] = round(card["seconds"] + sum(d["seconds"] for d in drafts), 1)
    return card


def valid_card_id(card_id: str) -> bool:
    return bool(card_id) and len(card_id) <= 40 and all(c.isalnum() or c == "-" for c in card_id)


def analysis_dir(folder: Path, version: str) -> Path:
    return folder / "analysis" / version


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(data), encoding="utf-8")
    os.replace(tmp, path)


def save_card(folder: Path, version: str, card: Dict[str, Any], packet: Dict[str, Any]) -> None:
    base = analysis_dir(folder, version)
    write_json(base / "packets" / f"{card['packet_hash']}.json", packet)
    write_json(base / "cards" / f"{card['card_id']}.json", card)


def read_card(folder: Path, version: str, card_id: str) -> Optional[Dict[str, Any]]:
    path = analysis_dir(folder, version) / "cards" / f"{card_id}.json"
    card: Optional[Dict[str, Any]] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    return card


def current_check(folder: Path, version: str, card: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """A card's number check by the current checker, against the packet it was written from, so a
    checker fix applies to stored cards; whether it was retried stays as written."""
    path = analysis_dir(folder, version) / "packets" / f"{card['packet_hash']}.json"
    if not card.get("output") or not path.exists():
        found: Optional[Dict[str, Any]] = card.get("check")
        return found
    packet = json.loads(path.read_text(encoding="utf-8"))
    return {**(card.get("check") or {}), **check_numbers(card_text(card["output"]), fact_values(packet))}


def list_cards(folder: Path, version: str) -> List[Dict[str, Any]]:
    """A version's cards in brief: id, kind, title, pattern, whether its numbers passed."""
    found = []
    for path in sorted((analysis_dir(folder, version) / "cards").glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        output = card.get("output") or {}
        found.append({"card_id": card["card_id"], "kind": card["kind"], "title": output.get("title"),
                      "pattern": output.get("pattern"), "passed": (current_check(folder, version, card) or {}).get("passed"),
                      "error": card.get("error"), "analysts": card["analysts"], "created_at": card["created_at"]})
    return found


def tests_root() -> Path:
    from api import config

    return Path(config.DATA_LAKE_PATH) / "_analysts" / "tests"


def passing_analysts() -> set[tuple[str, str]]:
    """The (model, prompt version) pairs with a passing analyst test run (DESIGN.md E8)."""
    passed = set()
    for path in tests_root().glob("*.json"):
        run = json.loads(path.read_text(encoding="utf-8"))
        if run.get("passed"):
            passed.add((str(run["model"]), str(run["prompt_version"])))
    return passed


SPLIT_CARDS = 5  # split points a save writes, the biggest second branch first


def best_layer(ev: LensEvidence) -> int:
    """The layer a save writes node cards for: the best held-out AMI with the label at the version's
    k (DESIGN.md C3), or, before validation, the best in-sample agreement of the nodes with the label."""
    from sklearn.metrics import adjusted_mutual_info_score

    view, scores = ev.view, {}
    for li, layer in enumerate(view.layers):
        k = int(view.nodes[:, li].max()) + 1
        entry = (ev.validation or {}).get("layers", {}).get(str(layer), {}).get(str(k)) or {}
        held = (entry.get("heldout") or {}).get("label")
        if held:
            scores[layer] = float(held["ami"])
    if not scores:
        labels = [str(item.get("label")) for item in view.items]
        scores = {layer: float(adjusted_mutual_info_score(labels, view.nodes[:, li]))
                  for li, layer in enumerate(view.layers)}
    return int(max(scores, key=lambda layer: scores[layer]))


def plan_cards(ev: LensEvidence) -> List[str]:
    """What a save writes, in order, until its budget runs out (DESIGN.md E8): the lens report,
    the k advisor once the lens is validated, the biggest split points, then the nodes at the
    best layer."""
    view = ev.view
    order = ["lens"] + (["k"] if ev.validation else [])
    order += [f"split-L{layer}C{node}" for layer, node, _ in split_points(view)[:SPLIT_CARDS]]
    layer = best_layer(ev)
    order += [f"L{layer}C{node}" for node in sorted(set(view.nodes[:, view.layers.index(layer)].tolist()))]
    return order


def build_analysis(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_analysis` job: cards for the given card ids (a save's plan by default), within a
    budget of calls."""
    from services.lenses.store import lens_dir
    from services.llm.packets import build_packet, load_evidence

    session, name = params["session_id"], params["name"]
    ev = load_evidence(session, name, params.get("version"))
    folder, version = lens_dir(session, name), str(ev.view.version)
    runner = ClaudeRunner(model=params.get("model"))
    budget = Budget(int(params.get("budget") or DEFAULT_BUDGET))
    wanted = list(params.get("cards") or plan_cards(ev))
    written: List[str] = []
    failed: List[str] = []
    skipped: List[str] = []
    for i, card_id in enumerate(wanted):
        ctx.progress(card_id, i, len(wanted))
        if budget.left < (3 if card_id == "lens" else 1):
            skipped.append(card_id)
            continue
        try:
            packet = build_packet(ev, card_id).as_dict()
        except ValueError as e:
            failed.append(f"{card_id}: {e}")
            continue
        card = (write_report if card_id == "lens" else write_card)(runner, packet, budget)
        if card is None:
            skipped.append(card_id)
            continue
        save_card(folder, version, card, packet)
        if card["output"] is not None:
            written.append(card_id)
        else:
            failed.append(f"{card_id}: {card['error']}")
    refresh_catalogue(ev.view.session_id, name, version)
    ctx.progress("done", len(wanted), len(wanted))
    return {"session_id": ev.view.session_id, "name": name, "version": version, "written": written,
            "failed": failed, "skipped": skipped, "calls": budget.used}


def refresh_catalogue(session_id: str, name: str, version: str) -> None:
    """A saved version's atlas entries pick up new reports or details; a failure is printed to the
    job's log and never fails the job, whose own work is done."""
    import traceback

    from services.lenses.atlas import write_nodes

    try:
        write_nodes(session_id, name, version)
    except Exception:
        traceback.print_exc()


def answer_question(params: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """The `lens_question` job: an analyst answers a question about a card's subject from its
    packet; the answer's numbers are checked and the answer is kept with the version."""
    from services.lenses.store import lens_dir
    from services.llm.packets import build_packet, load_evidence
    from services.llm.prompts import ANSWER_SCHEMA, question_prompt

    session, name = params["session_id"], params["name"]
    ev = load_evidence(session, name, params.get("version"))
    folder, version = lens_dir(session, name), str(ev.view.version)
    packet = build_packet(ev, params["card_id"]).as_dict()
    ctx.progress("asking", 0, 1)
    run = ClaudeRunner(model=params.get("model")).run(question_prompt(render(packet), params["question"]), ANSWER_SCHEMA)
    answer = (run.output or {}).get("answer")
    record = {"id": ctx.job_id, "card_id": params["card_id"], "question": params["question"], "answer": answer,
              "error": run.error, "check": check_numbers(answer, fact_values(packet)) if answer else None,
              "packet_hash": packet_hash(packet), "prompt_version": PROMPT_VERSION, "model": run.model,
              "seconds": round(run.seconds, 1), "created_at": _stamp()}
    write_json(analysis_dir(folder, version) / "packets" / f"{record['packet_hash']}.json", packet)
    write_json(analysis_dir(folder, version) / "questions" / f"{ctx.job_id}.json", record)
    return {"session_id": ev.view.session_id, "name": name, "version": version, "question_id": ctx.job_id}


def submit_card(session: str, name: str, card_id: str, output: Dict[str, Any], model: str,
                version: Optional[str] = None) -> Dict[str, Any]:
    """A card Claude Code wrote (the /analyze skill), checked like any other and kept only when
    every number traces; otherwise the failures come back, to fix and send again."""
    from services.lenses.store import lens_dir
    from services.llm.packets import build_packet, load_evidence

    missing = [key for key in CARD_SCHEMA["required"] if key not in output]
    if missing:
        raise ValueError(f"the card needs {', '.join(missing)}")
    ev = load_evidence(session, name, version)
    packet = build_packet(ev, card_id).as_dict()
    check = {**check_numbers(card_text(output), fact_values(packet)), "retried": False}
    if not check["passed"]:
        return {"stored": False, "check": check}
    card = {**_record(packet, output, check, [RunResult(output, model=model)], analysts=1),
            "written_by": "Claude Code", "prompt_version": "claude-code", "calls": 0}
    save_card(lens_dir(session, name), str(ev.view.version), card, packet)
    return {"stored": True, "check": check, "card": card}
