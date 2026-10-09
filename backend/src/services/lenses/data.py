"""Reading a capture for a lens: its items (filtered as today's clusterings filter them) and its
states, in capture order.

Captures store one row per probe, layer and token position, probe by probe, so the item order is
the same at every layer. A lens keeps that order: refitting today's settings reproduces today's
clusterings exactly.
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from pydantic import BaseModel

from api import config
from core.parquet_reader import read_records
from schemas.tokens import ProbeRecord
from services.experiments.token_filters import pick_last_occurrence, subsample_probes

Array = np.ndarray[Any, Any]

SOURCES: Dict[str, tuple[str, str]] = {
    "residual_stream": ("residual_streams.parquet", "residual_stream"),
    "expert_output": ("embeddings.parquet", "embedding"),
}


class LensFilters(BaseModel):
    labels: Optional[List[str]] = None
    steps: Optional[List[int]] = None
    last_occurrence_only: bool = True
    max_items: Optional[int] = None


def lake_root(lake: Optional[Path] = None) -> Path:
    """The lake to read: the one given, else the configured one, looked up at call time."""
    return lake if lake is not None else config.DATA_LAKE_PATH


def session_dir(session_id: str, lake: Optional[Path] = None) -> Path:
    root = lake_root(lake)
    for candidate in (root / f"session_{session_id}", root / session_id):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Session '{session_id}' not found")


# What the app shows beside an item, beyond what a lens keeps: its generated text, where the target
# word sits, and for agent runs the tick's game text, analysis channel and action.
DISPLAY_FIELDS = ("generated_text", "target_char_offset", "turn_id", "capture_type",
                  "game_text", "analysis", "action", "previous_action", "system_prompt", "run")


def display_fields(session_id: str, lake: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Each item's display fields, by probe id (cached while the capture's files are unchanged)."""
    folder = session_dir(session_id, lake)
    tokens, ticks = folder / "tokens.parquet", folder / "tick_log.jsonl"
    stamp = (tokens.stat().st_mtime_ns, ticks.stat().st_mtime_ns if ticks.exists() else 0)
    return _display_fields(str(folder), stamp)


@functools.lru_cache(maxsize=4)
def _display_fields(folder: str, stamp: tuple[int, int]) -> Dict[str, Dict[str, Any]]:
    from services.probes.scenario_actions import enrich_records_with_scenario_actions
    from services.probes.tick_log_enrichment import enrich_records_with_tick_log

    records = read_records(str(Path(folder) / "tokens.parquet"), ProbeRecord)
    enrich_records_with_scenario_actions(records, Path(folder))
    enrich_records_with_tick_log(records, Path(folder))
    return {r.probe_id: {f: getattr(r, f) for f in DISPLAY_FIELDS} for r in records}


def run_keys(session_id: str, lake: Optional[Path] = None) -> Dict[str, Optional[str]]:
    """Each item's run, by probe id: "<scenario>#<n>" for agent runs (a scenario played twice has
    runs #1 and #2), a sentence run's sequence id, or None."""
    return {pid: fields["run"] for pid, fields in display_fields(session_id, lake).items()}


def load_items(session_id: str, filters: LensFilters, lake: Optional[Path] = None) -> List[ProbeRecord]:
    """The capture's items after today's filters, in capture order.

    The filters run in today's order: labels, steps (turn or sentence index), the last occurrence
    of the target word, then a stratified subsample.
    """
    folder = session_dir(session_id, lake)
    records = read_records(str(folder / "tokens.parquet"), ProbeRecord)
    from services.probes.scenario_actions import enrich_records_with_scenario_actions
    from services.probes.tick_log_enrichment import enrich_records_with_tick_log
    enrich_records_with_scenario_actions(records, folder)
    enrich_records_with_tick_log(records, folder)
    if filters.labels:
        records = [r for r in records if r.label in filters.labels]
    if filters.steps:
        records = [r for r in records
                   if (r.turn_id if r.turn_id is not None else r.sentence_index) in filters.steps]
    if filters.last_occurrence_only:
        keep = pick_last_occurrence(records)
        records = [r for r in records if r.probe_id in keep]
    chosen = subsample_probes(records, filters.max_items)
    if chosen is not None:
        records = [r for r in records if r.probe_id in chosen]
    return records


def _scan(path: Path, column: str, probe_ids: Sequence[str], token_position: int,
          layers: Optional[Sequence[int]]) -> Dict[int, Array]:
    """Rows of `column` for the given probes at one token position, as {layer: [N, d] float32}."""
    index = {pid: i for i, pid in enumerate(probe_ids)}
    wanted = pa.array(list(probe_ids), type=pa.string())
    pf = pq.ParquetFile(path)
    names = set(pf.schema_arrow.names)
    columns = ["probe_id", "layer", column] + (["token_position"] if "token_position" in names else [])
    out: Dict[int, Array] = {}
    for batch in pf.iter_batches(columns=columns, batch_size=4096):
        mask = pc.is_in(batch.column("probe_id"), value_set=wanted)
        if "token_position" in names:
            mask = pc.and_(mask, pc.equal(batch.column("token_position"), token_position))
        if layers is not None:
            mask = pc.and_(mask, pc.is_in(batch.column("layer"), value_set=pa.array(list(layers), type=pa.int64())))
        rows = batch.filter(mask)
        if rows.num_rows == 0:
            continue
        flat = np.asarray(rows.column(column).flatten().to_numpy(zero_copy_only=False), dtype=np.float32)
        dim = flat.size // rows.num_rows
        matrix = flat.reshape(rows.num_rows, dim)
        for pid, layer, vector in zip(rows.column("probe_id").to_pylist(), rows.column("layer").to_pylist(), matrix):
            if int(layer) not in out:
                out[int(layer)] = np.full((len(probe_ids), dim), np.nan, dtype=np.float32)
            out[int(layer)][index[pid]] = vector
    for layer, matrix in out.items():
        missing = int(np.isnan(matrix[:, 0]).sum())
        if missing:
            raise ValueError(f"{path.name}: {missing} of {len(probe_ids)} items have no row at layer {layer}")
    return out


def load_states(session_id: str, probe_ids: Sequence[str], source: str = "residual_stream",
                token_position: int = 1, layers: Optional[Sequence[int]] = None,
                lake: Optional[Path] = None) -> Dict[int, Array]:
    """{layer: [N, 2880] float32} for the items, in their order. The captures hold fp16 values,
    so float32 loses nothing."""
    if source not in SOURCES:
        raise ValueError(f"unknown source {source!r}; one of {sorted(SOURCES)}")
    file, column = SOURCES[source]
    return _scan(session_dir(session_id, lake) / file, column, probe_ids, token_position, layers)


def load_routing(session_id: str, probe_ids: Sequence[str], token_position: int = 1,
                 lake: Optional[Path] = None) -> Array:
    """[N, layers, experts] float32: the router's softmax over all experts, as captured."""
    by_layer = _scan(session_dir(session_id, lake) / "routing.parquet", "routing_weights",
                     probe_ids, token_position, None)
    return np.stack([by_layer[layer] for layer in sorted(by_layer)], axis=1)


def own_top4(routing: Array) -> tuple[Array, Array]:
    """The model's own choice from the stored routing: each item's top four experts per layer,
    and their weights scaled to sum to 1 (the softmax over the top four, as the model takes it).

    Returns (experts [N, L, 4] int16, weights [N, L, 4] float32), rank 1 first.
    """
    order = np.argsort(-routing, axis=-1, kind="stable")[..., :4]
    top = np.take_along_axis(routing, order, axis=-1)
    return order.astype(np.int16), (top / top.sum(axis=-1, keepdims=True)).astype(np.float32)
