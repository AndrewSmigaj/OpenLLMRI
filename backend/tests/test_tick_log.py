"""Records join their own tick, so a scenario played twice keeps each run's text apart, and every
record knows its run."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from schemas.tokens import ProbeRecord
from services.probes.tick_log_enrichment import (
    enrich_records_with_tick_log,
    read_ticks,
    record_runs,
)


def record(pid: str, scenario: Optional[str], turn: Optional[int], sequence: Optional[str] = None) -> ProbeRecord:
    return ProbeRecord(probe_id=pid, session_id="s", input_text="text", target_word="person", target_token_id=1,
                       target_token_position=0, total_tokens=3, scenario_id=scenario, turn_id=turn,
                       sequence_id=sequence)


def write_ticks(folder: Path, ticks: List[Dict[str, Any]]) -> None:
    (folder / "tick_log.jsonl").write_text("".join(json.dumps(t) + "\n" for t in ticks))


def tick(scenario: str, turn: int, action: str, written: Optional[int]) -> Dict[str, Any]:
    entry: Dict[str, Any] = {"scenario_name": scenario, "turn_id": turn, "game_text": f"{action} text", "action": action}
    if written is not None:
        entry["probes_written"] = written
    return entry


# Scenario a played twice around scenario b; a tick can write several records
TICKS = [("a", 0, "examine", 2), ("a", 1, "flee", 1), ("b", 0, "examine", 1), ("a", 0, "look", 1), ("a", 1, "help", 2)]
RECORDS = [("p1", "a", 0), ("p2", "a", 0), ("p3", "a", 1), ("p4", "b", 0), ("p5", "a", 0), ("p6", "a", 1), ("p7", "a", 1)]


def joined(tmp_path: Path, counts: bool) -> List[ProbeRecord]:
    write_ticks(tmp_path, [tick(s, t, a, n if counts else None) for s, t, a, n in TICKS])
    records = [record(pid, s, t) for pid, s, t in RECORDS]
    enrich_records_with_tick_log(records, tmp_path)
    return records


def test_each_record_takes_its_own_runs_tick(tmp_path: Path) -> None:
    for counts in (True, False):  # exact by the ticks' record counts, or matched by scenario, run and turn
        records = joined(tmp_path, counts)
        assert [r.action for r in records] == ["examine", "examine", "flee", "examine", "look", "help", "help"]
        assert [r.run for r in records] == ["a#1", "a#1", "a#1", "b#1", "a#2", "a#2", "a#2"]
        assert records[2].previous_action == "examine" and records[5].previous_action == "look"
        assert records[0].previous_action is None and records[4].previous_action is None


def test_the_exact_join_survives_a_one_tick_run_played_twice_in_a_row(tmp_path: Path) -> None:
    write_ticks(tmp_path, [tick("a", 0, "first", 1), tick("a", 0, "second", 1)])
    records = [record("p1", "a", 0), record("p2", "a", 0)]
    enrich_records_with_tick_log(records, tmp_path)
    assert [r.action for r in records] == ["first", "second"]
    assert [r.run for r in records] == ["a#1", "a#2"]


def test_a_sentence_run_is_its_sequence_and_a_lone_sentence_has_none(tmp_path: Path) -> None:
    records = [record("p1", None, None, "seq_1"), record("p2", None, None, "seq_1"), record("p3", None, None)]
    assert record_runs(records, read_ticks(tmp_path)) == ["seq_1", "seq_1", None]
    enrich_records_with_tick_log(records, tmp_path)  # no tick log: runs only
    assert [r.run for r in records] == ["seq_1", "seq_1", None] and records[0].game_text is None
