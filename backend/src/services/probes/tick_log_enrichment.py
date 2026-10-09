"""
Tick log enrichment for agent sessions.

Agent sessions write a `tick_log.jsonl` file with one entry per game tick, in order
({scenario_name, turn_id, game_text, analysis, action, probes_written, ...}; written by
agent_loop.py). This module matches each captured record to its tick, and gives it the tick's
game text, analysis channel and action, the previous tick's action, the scenario's system prompt,
and its run.

A scenario can be played more than once in a session (the friend/foe session played most of
them on two days), so ticks are matched by run, never by (scenario, turn) alone: that key made a
scenario's later run overwrite the earlier one's text. A run is numbered within its scenario
("bus_stop_x#2" is its second run). Records carry no run id (a real one belongs in the capture
recipe, DESIGN.md slice 2), so:
- when every tick says how many records it wrote and those counts add up to the records, each
  record takes its tick in order (exact);
- otherwise records and ticks are matched by scenario, run and turn, a new run starting when the
  scenario changes or the turn goes back.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Sequence, Tuple

if TYPE_CHECKING:
    from schemas.tokens import ProbeRecord


def read_ticks(session_dir: Path) -> List[Dict[str, Any]]:
    """The tick log's entries in order ([] without one); malformed lines and entries without a
    scenario or turn are skipped."""
    path = session_dir / "tick_log.jsonl"
    if not path.exists():
        return []
    ticks: List[Dict[str, Any]] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if data.get("scenario_name") is None or data.get("turn_id") is None:
            continue
        ticks.append(data)
    return ticks


def tick_runs(ticks: Sequence[Dict[str, Any]]) -> List[int]:
    """Each tick's run within its scenario, from 1: a run starts when the scenario changes or the
    turn doesn't move on (each tick of a run has the next turn)."""
    runs: List[int] = []
    count: Dict[str, int] = {}
    previous: Optional[Tuple[str, int]] = None
    for tick in ticks:
        scenario, turn = tick["scenario_name"], tick["turn_id"]
        if previous is None or previous[0] != scenario or turn <= previous[1]:
            count[scenario] = count.get(scenario, 0) + 1
        runs.append(count[scenario])
        previous = (scenario, turn)
    return runs


def _record_runs(records: Sequence["ProbeRecord"]) -> List[Optional[int]]:
    """Each record's run within its scenario when the ticks can't be followed exactly: a run
    starts when the scenario changes or the turn goes back (a tick can write several records)."""
    runs: List[Optional[int]] = []
    count: Dict[str, int] = {}
    previous: Optional[Tuple[str, int]] = None
    for r in records:
        if r.scenario_id is None or r.turn_id is None:
            runs.append(None)
            continue
        if previous is None or previous[0] != r.scenario_id or r.turn_id < previous[1]:
            count[r.scenario_id] = count.get(r.scenario_id, 0) + 1
        runs.append(count[r.scenario_id])
        previous = (r.scenario_id, r.turn_id)
    return runs


def record_ticks(records: Sequence["ProbeRecord"], ticks: Sequence[Dict[str, Any]]) -> List[Optional[int]]:
    """Each record's tick (an index into `ticks`), or None. `records` must be the capture's records
    in capture order, unfiltered."""
    agent = [i for i, r in enumerate(records) if r.scenario_id is not None and r.turn_id is not None]
    out: List[Optional[int]] = [None] * len(records)
    counts = [c for c in (t.get("probes_written") for t in ticks) if isinstance(c, int)]
    if agent and len(counts) == len(ticks) and sum(counts) == len(agent):
        claimed = [t for t, n in enumerate(counts) for _ in range(n)]
        if all(records[i].scenario_id == ticks[t]["scenario_name"] and records[i].turn_id == ticks[t]["turn_id"]
               for i, t in zip(agent, claimed)):
            for i, t in zip(agent, claimed):
                out[i] = t
            return out
    runs = tick_runs(ticks)
    by_key = {(t["scenario_name"], run, t["turn_id"]): j for j, (t, run) in enumerate(zip(ticks, runs))}
    for i, (r, run) in enumerate(zip(records, _record_runs(records))):
        if run is not None:
            out[i] = by_key.get((r.scenario_id, run, r.turn_id))
    return out


def record_runs(records: Sequence["ProbeRecord"], ticks: Sequence[Dict[str, Any]]) -> List[Optional[str]]:
    """Each record's run key: "<scenario>#<n>" for agent records, the sequence id for a sentence
    run, None for a record that belongs to no run. `records` in capture order, unfiltered; `ticks`
    the session's tick log (read_ticks)."""
    if ticks:
        runs = tick_runs(ticks)
        matched = record_ticks(records, ticks)
        fallback = _record_runs(records)
        keys: List[Optional[str]] = []
        for r, t, own in zip(records, matched, fallback):
            if r.scenario_id is None:
                keys.append(r.sequence_id)
            else:
                run = runs[t] if t is not None else own
                keys.append(f"{r.scenario_id}#{run}" if run is not None else None)
        return keys
    fallback = _record_runs(records)
    return [r.sequence_id if r.scenario_id is None else (f"{r.scenario_id}#{run}" if run is not None else None)
            for r, run in zip(records, fallback)]


def enrich_records_with_tick_log(
    records: Iterable["ProbeRecord"],
    session_dir: Path,
) -> None:
    """Populate game_text / analysis / action / previous_action / system_prompt and run on each
    record, from its own tick. `records` in capture order, unfiltered.

    Mutates records in place. Records of sessions without a tick log keep None, apart from their
    run (a sentence run's sequence id). The system prompt is logged only on a scenario's first
    tick, so it applies to all of that scenario's records.
    """
    records = list(records)
    ticks = read_ticks(session_dir)
    for r, key in zip(records, record_runs(records, ticks)):
        r.run = key
    if not ticks:
        return
    system_prompts: Dict[str, str] = {}
    for t in ticks:
        if t.get("system_prompt"):
            system_prompts[t["scenario_name"]] = t["system_prompt"]
    runs = tick_runs(ticks)
    for r, j in zip(records, record_ticks(records, ticks)):
        if j is not None:
            tick = ticks[j]
            r.game_text = tick.get("game_text")
            r.analysis = tick.get("analysis")
            r.action = tick.get("action")
            before = j - 1
            if tick["turn_id"] > 0 and before >= 0 and runs[before] == runs[j] \
                    and ticks[before]["scenario_name"] == tick["scenario_name"]:
                r.previous_action = ticks[before].get("action")
        sp = system_prompts.get(r.scenario_id) if r.scenario_id is not None else None
        if sp:
            r.system_prompt = sp
