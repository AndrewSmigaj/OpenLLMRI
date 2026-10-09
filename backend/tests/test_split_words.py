"""Words that split into several tokens (DESIGN.md C1). A sentence set's word is read at its last
token when none of its one-token forms is in the sentence, and the capture records how many tokens
it took. Words found in one token, and agent captures, keep today's path. The sentence route counts
only what it captured and reports the rest."""

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import torch

from core.parquet_reader import read_records
from core.parquet_writer import BatchWriter
from schemas.tokens import ProbeRecord, create_probe_record
from services.probes.probe_processor import ProbeProcessor

MODEL = Path(__file__).resolve().parents[2] / "data" / "models" / "gpt-oss-20b"
SETS = Path(__file__).resolve().parents[2] / "data" / "sentence_sets"
real_tokenizer = pytest.mark.skipif(not (MODEL / "tokenizer.json").exists(),
                                    reason="needs the local gpt-oss tokenizer")

VOCAB = ["<|start|>", "<|end|>", " jag", "uar", "uars", "s", "jag", "Jag", " Jag", "big", "(", ".",
         " The", " a", " and", "Tanks", " roll", ";", " tank", " waits", " eagle"]
FORMS = {" jaguar": [" jag", "uar"], "jaguar": ["jag", "uar"], " Jaguar": [" Jag", "uar"],
         "Jaguar": ["Jag", "uar"]}
UNKNOWN = len(VOCAB)  # any other text: two pieces of an id outside the vocabulary


def ids(*pieces: str) -> List[int]:
    return [VOCAB.index(p) for p in pieces]


class FakeTokenizer:
    chat_template = None

    def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
        if text in FORMS:
            return ids(*FORMS[text])
        return [VOCAB.index(text)] if text in VOCAB else [UNKNOWN, UNKNOWN]

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        return "".join(VOCAB[i] for i in token_ids
                       if i < UNKNOWN and not (skip_special_tokens and VOCAB[i].startswith("<|")))

    def apply_chat_template(self, messages: List[Dict[str, str]], **_: Any) -> Dict[str, torch.Tensor]:
        content = messages[-1]["content"]
        body = self.encode(content) if content in FORMS or content in VOCAB else [UNKNOWN, UNKNOWN]
        return {"input_ids": torch.tensor([ids("<|start|>") + body + ids("<|end|>")])}


class FakeOrchestrator:
    """Stands in for the model: no hooks, and captured states that name their token position."""

    def __init__(self) -> None:
        self.model = SimpleNamespace(device="cpu")
        self.n = 0

    def initialize_hooks(self, session_id: str) -> None:
        pass

    def clear_captured_data(self) -> None:
        pass

    def cleanup_hooks(self) -> None:
        pass

    def run_forward_pass(self, input_tensor: torch.Tensor, past_kv: Optional[object] = None,
                         use_cache: bool = False) -> Tuple[Any, None]:
        self.n = int(input_tensor.shape[1])
        return SimpleNamespace(logits=None), None

    def get_captured_data(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        position = torch.arange(self.n, dtype=torch.float32)[None, :, None].repeat(1, 1, 4)
        return ({"layer_0": {"routing_weights": torch.full((1, self.n, 32), 1 / 32)}},
                {"layer_0": {"embedding": position}}, {"layer_0": {"residual_stream": position}})


def make_service(lake: Path, tokenizer: Any) -> Any:
    from services.probes.integrated_capture_service import IntegratedCaptureService

    service = IntegratedCaptureService(None, tokenizer, [0], data_lake_path=str(lake))  # type: ignore[arg-type]
    service.orchestrator = FakeOrchestrator()  # type: ignore[assignment]
    return service


def test_a_split_word_is_found_at_its_last_token() -> None:
    p = ProbeProcessor(FakeTokenizer(), None, [])  # type: ignore[arg-type]
    seq = ids("<|start|>", " The", " jag", "uar", ".", "<|end|>")
    assert p.find_all_word_token_positions(seq, "jaguar") == []
    assert p.find_split_word_positions(seq, "jaguar") == [(3, VOCAB.index("uar"), 2)]
    both = ids(" jag", "uar", " and", " a", " jag", "uar")
    assert [pos for pos, _, _ in p.find_split_word_positions(both, "jaguar")] == [1, 5]


def test_a_split_word_must_stand_alone() -> None:
    p = ProbeProcessor(FakeTokenizer(), None, [])  # type: ignore[arg-type]
    assert p.find_split_word_positions(ids(" The", " jag", "uar", "s"), "jaguar") == []  # " jaguars"
    assert p.find_split_word_positions(ids(" The", " jag", "uars"), "jaguar") == []
    assert p.find_split_word_positions(ids("big", "jag", "uar"), "jaguar") == []  # inside "bigjaguar"
    assert p.find_split_word_positions(ids("<|start|>", "Jag", "uar", "."), "jaguar") == [(2, VOCAB.index("uar"), 2)]
    assert p.find_split_word_positions(ids("(", "jag", "uar", "."), "jaguar") == [(2, VOCAB.index("uar"), 2)]


def test_the_capture_reads_a_split_word_only_when_asked(tmp_path: Path) -> None:
    service = make_service(tmp_path, FakeTokenizer())
    holdout = {"family_field": "order", "whole_families": True}
    sid = service.create_sentence_session("t", 1, "jaguar", ["animal"], sentence_set_name="s", holdout=holdout)
    seq = ids("<|start|>", " jag", "uar", "<|end|>")
    meta = {"label": "animal", "input_text": " jaguar"}
    assert service.capture_step(sid, seq, ["jaguar"], metadata=meta)[0] == []  # agent captures: as before
    [record], _ = service.capture_step(sid, seq, ["jaguar"], metadata=meta, split_words=True)
    assert (record.target_token_position, record.target_token_count, record.target_char_offset) == (2, 2, 1)
    service.finalize_session(sid)
    assert pq.read_table(tmp_path / sid / "tokens.parquet").column("target_token_count").to_pylist() == [2]
    stored = pq.read_table(tmp_path / sid / "residual_streams.parquet").to_pylist()
    target = next(row for row in stored if row["token_position"] == 1)
    assert target["residual_stream"][0] == 2.0  # the state of the word's last token
    assert json.loads((tmp_path / "_sessions" / f"{sid}.json").read_text())["holdout"] == holdout


def test_an_earlier_look_alike_does_not_move_the_offset(tmp_path: Path) -> None:
    # Counting the word's occurrences in the text found "Tanks" first; the token position doesn't.
    service = make_service(tmp_path, FakeTokenizer())
    sid = service.create_sentence_session("t", 1, "tank", ["vehicle"])
    text = "Tanks roll; a tank waits"
    seq = ids("<|start|>", "Tanks", " roll", ";", " a", " tank", " waits", "<|end|>")
    [record], _ = service.capture_step(sid, seq, ["tank"], split_words=True,
                                       metadata={"label": "vehicle", "input_text": text})
    assert (record.target_token_position, record.target_token_count) == (5, 1)
    assert record.target_char_offset == text.index(" tank") + 1


def test_the_route_counts_what_it_captured_and_reports_the_rest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from api.dependencies import get_capture_service
    from api.routers import probes
    from services.generation import sentence_set as sets

    words = sets.SentenceSet(
        name="words", version="1", target_word="(each item's own word)",
        groups=[sets.SentenceGroup("animal", "", [
            sets.SentenceEntry(" jaguar", "animal", "jaguar", {"order": "Carnivora"}),
            sets.SentenceEntry(" eagle", "animal", "eagle", {"order": "Accipitriformes"}),
            sets.SentenceEntry(" eagle", "animal", "okapi", {"order": "Artiodactyla"}),  # its word isn't there
        ])],
        metadata={"holdout": {"family_field": "order", "whole_families": True}})
    monkeypatch.setattr(sets, "load_sentence_set_by_name", lambda name, base: words)
    service = make_service(tmp_path, FakeTokenizer())
    app = FastAPI()
    app.include_router(probes.router, prefix="/api")
    app.dependency_overrides[get_capture_service] = lambda: service
    reply = TestClient(app).post("/api/probes/sentence-experiment",
                                 json={"sentence_set_name": "words", "generate_output": False}).json()
    assert reply["total_probes"] == 2 and reply["counts"] == {"animal": 2}
    assert [(d["word"], d["label"]) for d in reply["dropped"]] == [("okapi", "animal")]
    meta = json.loads((tmp_path / "_sessions" / f"{reply['session_id']}.json").read_text())
    assert (meta["completed_pairs"], meta["failed_pairs"]) == (2, 1)
    assert meta["failures"] == [reply["dropped"][0]["reason"]]
    assert meta["holdout"] == {"family_field": "order", "whole_families": True}
    counts = pq.read_table(tmp_path / reply["session_id"] / "tokens.parquet").column("target_token_count").to_pylist()
    assert counts == [2, 1]


def test_an_older_tokens_file_takes_new_records(tmp_path: Path) -> None:
    path = tmp_path / "tokens.parquet"
    old = create_probe_record("p0", "s", " eagle", "eagle", 1, 1, 3)
    row = {k: v for k, v in vars(old).items() if k != "target_token_count"}
    pq.write_table(pa.Table.from_pylist([row]), path)  # written before the field existed
    writer = BatchWriter(path)
    writer.add_record(create_probe_record("p1", "s", " jaguar", "jaguar", 2, 2, 4, target_token_count=2))
    writer.flush()
    assert [r.target_token_count for r in read_records(str(path), ProbeRecord)] == [1, 2]


@real_tokenizer
def test_with_the_real_tokenizer_kept_sets_never_take_the_split_path() -> None:
    """Every word of the tank and nouns sets is found in one token, so the split path never runs
    there and their captures keep their positions and tokens."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(MODEL)
    p = ProbeProcessor(tok, None, [])
    for name in ("polysemy/tank_polysemy_v3.json", "lexical/nouns_meaning_feeling_v1.json"):
        for group in json.loads((SETS / name).read_text())["groups"]:
            for entry in group["sentences"]:
                found = p.find_all_word_token_positions(tok.encode(entry["text"], add_special_tokens=False),
                                                        entry["target_word"])
                assert found, (name, entry["text"])


@real_tokenizer
def test_with_the_real_tokenizer_split_words_are_read_at_their_last_piece(tmp_path: Path) -> None:
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(MODEL)
    service = make_service(tmp_path, tok)
    sid = service.create_sentence_session("t", 1, "x", ["a"])

    def capture(text: str, word: str) -> List[ProbeRecord]:
        seq = list(tok.apply_chat_template([{"role": "user", "content": text}], tokenize=True,
                                           add_generation_prompt=True, return_dict=True)["input_ids"])
        records: List[ProbeRecord] = service.capture_step(sid, seq, [word], split_words=True,
                                                          metadata={"label": "a", "input_text": text})[0]
        for r in records:
            assert tok.decode(seq[r.target_token_position - r.target_token_count + 1:r.target_token_position + 1]
                              ).strip().lower() == word
        return records

    [alone] = capture(" jaguar", "jaguar")  # " jag" + "uar"
    assert (alone.target_token_count, alone.target_char_offset) == (2, 1)
    [inside] = capture("A jaguar rests in the shade.", "jaguar")
    assert (inside.target_token_count, inside.target_char_offset) == (2, 2)
    [first] = capture("Eagle owls hunt at dusk.", "eagle")  # " eagle" is one token, "Eagle" splits
    assert (first.target_token_count, first.target_char_offset) == (2, 0)
    assert capture("Two jaguars rest in the shade.", "jaguar") == []  # " jag" + "u" + "ars"
    text = ("Aluminum tanks are lighter on land but negatively buoyant when empty, unlike a steel tank "
            "which stays negative throughout.")  # an entry of tank_polysemy_v3
    [tank] = capture(text, "tank")
    assert tank.target_char_offset == text.index("steel tank") + len("steel ")  # counting gave 9, in "tanks"
