"""LLM analysis with a fake analyst: the number checker, the runner's environment and result
parsing, packets, cards (checked, retried, reconciled, budgeted), questions, Claude Code's cards,
and the analyst tests."""

import json
import re
from types import SimpleNamespace
from typing import Any, Dict, Optional

import numpy as np
import pytest

from services.llm.numbers import check_numbers
from services.llm.runner import analyst_env, parse_result

FACTS = {"F1": 89, "F2": 0.843, "F3": -0.72, "F4": 0.33, "F5": 0.79}


@pytest.mark.parametrize("text, passed", [
    ("It holds 89 items [F1], 84% of them aquarium [F2].", True),
    ("Shares run 0.33–0.79 [F4, F5] and 0.33-0.79 [F4, F5].", True),
    ("A correlation of −0.72 [F3], or 0.72 [F3] unsigned.", True),
    ("Layer 12, rank 2, L12C0 and n2092 hold \"3 fish\" [F1].", True),
    ("A correlation of +0.72 [F3].", False),  # a written sign must match
    ("It holds 90 items [F1].", False),  # 89 isn't 90 at the precision written
    ("It holds 89. Then [F1].", False),  # the citation must sit in the number's sentence
    ("See [F9].", False),  # no such fact
    ("Twice as many: 178 [F1].", False),  # computed numbers don't trace
    ("The rank-1 expert takes 89 items [F1]; Card 2 and draft 1 agree.", True),  # identifiers
])
def test_every_numeral_must_trace_to_a_cited_fact(text: str, passed: bool) -> None:
    assert check_numbers(text, FACTS)["passed"] is passed


def test_the_runner_keeps_the_api_key_out_and_reads_the_structured_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setenv("HOME", "/home/someone")
    env = analyst_env()
    assert "ANTHROPIC_API_KEY" not in env and env["HOME"] == "/home/someone"
    good = {"type": "result", "subtype": "success", "is_error": False, "structured_output": {"answer": 5},
            "modelUsage": {"claude-x": {}}, "safety_stops": 0, "session_id": "s"}
    found = parse_result(0, json.dumps(good), "", 1.0)
    assert found.output == {"answer": 5} and found.model == "claude-x" and found.error is None
    failed = parse_result(1, json.dumps({**good, "is_error": True, "result": "limit reached"}), "", 1.0)
    assert failed.output is None and failed.error == "limit reached"
    assert parse_result(1, "not json", "boom", 1.0).error.startswith("claude exited 1")  # type: ignore[union-attr]


SHARE = re.compile(r"share of (.+?) with label = (\S+): ([\d.]+)")
BLANK = {"title": "", "pattern": "none", "summary": "", "points": [], "caveats": []}


def sound_analyst(prompt: str, schema: Dict[str, Any], overclaim: bool = False) -> Optional[Dict[str, Any]]:
    """An analyst in miniature. Cards: a pattern is clear when one label's share stands well
    above its share of all items, and the card names it. Picks: the sentences of the described
    class. Answers: a sentence citing the first fact."""
    if "members" in schema["properties"]:
        wanted = re.search(r"Description: class (\S+)\.", prompt)
        listed = re.findall(r"^(\d+)\. (.*)$", prompt, flags=re.M)
        return {"members": [int(n) for n, text in listed if wanted and f"class {wanted[1]} " in text]}
    first = re.search(r"^F1  .*: (\S+)$", prompt, flags=re.M)
    if "answer" in schema["properties"]:
        return {"answer": f"It holds {first[1] if first else 'no'} items [F1]."}
    shares: Dict[str, Dict[str, float]] = {}
    for name, value, share in SHARE.findall(prompt.split("Evidence:")[-1]):
        shares.setdefault(value, {})["all" if name == "all items" else "subject"] = float(share)
    pairs = [(v, d["subject"], d["subject"] - d["all"]) for v, d in shares.items() if len(d) == 2]
    best = max(pairs, key=lambda p: p[2], default=None)
    clear = overclaim or (best is not None and best[1] >= 0.65 and best[2] >= 0.15)
    named = best[0] if best else "nothing"
    card = {**BLANK, "title": f"class {named}" if clear else "a mix", "pattern": "clear" if clear else "none",
            "summary": f"Mostly class {named}." if clear else "No pattern stands out."}
    return {**card, "disagreements": []} if "disagreements" in schema["properties"] else card


def _label_the_texts(path: Any) -> None:
    """Texts that name each item's class, so descriptions can predict members."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    table = pq.read_table(path)
    labels = table.column("label").to_pylist()
    texts = pa.array([f"a class {label} tank, item {i}" for i, label in enumerate(labels)])
    pq.write_table(table.set_column(table.schema.get_field_index("input_text"), "input_text", texts), path)


@pytest.fixture
def client(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> Any:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from test_lens_api import BODY, run_job
    from test_lenses import SESSION, make_capture

    from api import config
    from api.routers import analysis, jobs, lenses
    from services.jobs.scheduler import JobScheduler
    from services.jobs.store import JobStore

    monkeypatch.setattr(config, "DATA_LAKE_PATH", tmp_path / "lake")
    monkeypatch.setattr(config, "LENS_RECORDS_PATH", tmp_path / "records")
    make_capture(tmp_path / "lake")
    _label_the_texts(tmp_path / "lake" / SESSION / "tokens.parquet")
    app = FastAPI()
    for module in (jobs, lenses, analysis):
        app.include_router(module.router, prefix="/api")
    app.state.jobs = JobScheduler(JobStore(tmp_path / "lake" / "_jobs"))
    built = TestClient(app)
    run_job(built, built.post("/api/lenses", json=BODY).json()["job_id"])
    return built


def _evidence() -> Any:
    from test_lenses import SESSION

    from services.llm.packets import load_evidence

    return load_evidence(SESSION, "synth")


def test_packets_build_for_every_card_type_and_split_points_are_found(client: Any) -> None:
    from services.llm.packets import build_packet, split_points

    ev = _evidence()
    e0, e1 = int(ev.view.experts[0, 0, 0]), int(ev.view.experts[0, 1, 0])
    for card in ["lens", "L1C0", f"L0E{e0}r1", "L0C0-L1C0", f"L0E{e0}-L1E{e1}r1"]:
        packet = build_packet(ev, card).as_dict()
        assert packet["card_id"] == card and packet["facts"][0]["value"] > 0
    with pytest.raises(ValueError, match="validate"):
        build_packet(ev, "k")
    with pytest.raises(ValueError, match="card id"):
        build_packet(ev, "L1X0")
    nodes = np.array([[0, 0]] * 20 + [[0, 1]] * 12 + [[1, 2]] * 30 + [[1, 3]] * 2)
    assert split_points(SimpleNamespace(layers=[4, 5], nodes=nodes)) == [(4, 0, 12)]  # 2 items is no branch


def _card_runner(answers: Any) -> Any:
    from services.llm.runner import FakeRunner

    def answer(prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        value = re.search(r"^F1  .*: (\S+)$", prompt, flags=re.M)[1]  # type: ignore[index]
        written = answers(prompt, value)
        card = {**BLANK, "title": "a node", "summary": written}
        return {**card, "disagreements": []} if "disagreements" in schema["properties"] else card
    return FakeRunner(answer)


def test_cards_are_checked_retried_once_and_flagged(client: Any) -> None:
    from services.llm.cards import Budget, write_card, write_report
    from services.llm.packets import build_packet

    packet = build_packet(_evidence(), "L1C0").as_dict()
    right = write_card(_card_runner(lambda p, v: f"It holds {v} items [F1]."), packet, Budget(5))
    assert right and right["check"]["passed"] and right["calls"] == 1 and right["analysts"] == 1
    wrong = write_card(_card_runner(lambda p, v: "It holds 12345 items [F1]."), packet, Budget(5))
    assert wrong and not wrong["check"]["passed"] and wrong["check"]["retried"] and wrong["calls"] == 2
    fixed = write_card(_card_runner(lambda p, v: f"It holds {v} items [F1]." if "don't trace" in p
                                    else "It holds 12345 items [F1]."), packet, Budget(5))
    assert fixed and fixed["check"]["passed"] and fixed["check"]["retried"]
    report = write_report(_card_runner(lambda p, v: f"It holds {v} items [F1]."), build_packet(_evidence(), "lens").as_dict(), Budget(5))
    assert report and report["analysts"] == 2 and len(report["drafts"]) == 2 and report["calls"] == 3
    assert write_card(_card_runner(lambda p, v: ""), packet, Budget(0)) is None  # no call left


def _run(client: Any, job_id: str, fn: Any) -> Dict[str, Any]:
    from services.jobs.kinds import JobContext

    store = client.app.state.jobs.store
    result: Dict[str, Any] = fn(store.load(job_id).params, JobContext(store, job_id))
    return result


def _fake(monkeypatch: pytest.MonkeyPatch, answer: Any) -> Any:
    import services.llm.analyst_tests as tests
    import services.llm.cards as cards
    from services.llm.runner import FakeRunner

    runner = FakeRunner(answer)
    monkeypatch.setattr(cards, "ClaudeRunner", lambda model=None: runner)
    monkeypatch.setattr(tests, "ClaudeRunner", lambda model=None: runner)
    return runner


def test_an_analysis_job_keeps_to_its_budget_and_its_cards_read_back(client: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    from test_lenses import SESSION

    from services.llm.cards import answer_question, build_analysis

    runner = _fake(monkeypatch, sound_analyst)
    base = f"/api/sessions/{SESSION}/lenses/synth"
    started = client.post(f"{base}/analysis", json={"budget": 2})
    assert started.status_code == 202
    result = _run(client, started.json()["job_id"], build_analysis)
    assert result["calls"] == 2 == len(runner.prompts) and "lens" in result["skipped"]  # the report needs 3
    listed = client.get(f"{base}/cards").json()
    assert listed["version"] == "v1" and len(listed["cards"]) == 2
    card_id = listed["cards"][0]["card_id"]
    card = client.get(f"{base}/cards/{card_id}").json()
    assert card["written_by"] == "claude -p" and card["tested"] is False and card["stale"] is False
    assert client.get(f"{base}/cards/L9C9").status_code == 404
    packet = client.get(f"{base}/packets/L1C0").json()
    assert packet["text"].startswith("Subject: cluster node L1C0") and len(packet["hash"]) == 16
    bad = client.post(f"{base}/cards/L1C0", json={"output": {**BLANK, "summary": "It holds 12345 items [F1]."}})
    assert bad.status_code == 422 and bad.json()["detail"]["check"]["failures"]
    good_value = packet["packet"]["facts"][0]["value"]
    good = client.post(f"{base}/cards/L1C0", json={"output": {**BLANK, "summary": f"It holds {good_value} items [F1]."}})
    assert good.status_code == 200 and good.json()["card"]["written_by"] == "Claude Code"
    asked = client.post(f"{base}/ask", json={"card_id": "L1C0", "question": "How many items?"}).json()["job_id"]
    _run(client, asked, answer_question)
    answers = client.get(f"{base}/questions", params={"card_id": "L1C0"}).json()["questions"]
    assert answers[0]["answer"].endswith("[F1].") and answers[0]["check"]["passed"]
    saved = client.post(f"{base}/save", json={"version": "v1", "keywords": ["tank"]}).json()
    assert saved["analysis_job_id"]  # a save queues its reports


def test_a_sound_analyst_passes_the_tests_and_an_overclaiming_one_fails(client: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    from test_lenses import SESSION

    from services.llm.analyst_tests import run_tests
    from services.llm.cards import build_analysis

    body = {"session_id": SESSION, "name": "synth", "layer": 1}
    _fake(monkeypatch, lambda prompt, schema: sound_analyst(prompt, schema, overclaim=True))
    loose = _run(client, client.post("/api/analysts/tests", json=body).json()["job_id"], run_tests)
    assert loose["passed"] is False
    latest = client.get("/api/analysts/tests").json()["latest"]
    assert all(d["clear"] for d in latest["decoys"])  # it calls every decoy a clear pattern
    _fake(monkeypatch, sound_analyst)
    sound = _run(client, client.post("/api/analysts/tests", json=body).json()["job_id"], run_tests)
    latest = client.get("/api/analysts/tests").json()
    record = latest["latest"]
    assert sound["passed"], record
    assert not any(d["clear"] for d in record["decoys"]) and all(p["found"] for p in record["planted"])
    assert all(p["accuracy"] == 1.0 for p in record["predicted"]) and record["predicted"][0]["baseline"] == 1.0
    assert latest["passing"] == [{"model": "fake-model", "prompt_version": latest["prompt_version"]}]
    base = f"/api/sessions/{SESSION}/lenses/synth"
    _run(client, client.post(f"{base}/analysis", json={"cards": ["L1C0"], "budget": 2}).json()["job_id"], build_analysis)
    assert client.get(f"{base}/cards/L1C0").json()["tested"] is True
