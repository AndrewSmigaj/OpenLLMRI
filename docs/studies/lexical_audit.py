"""The checks every single-word set gets before its capture (data/sentence_sets/lexical/), shared by
the studies' own audits (docs/studies/animals/analysis/audit_set.py,
docs/studies/objects_harm/analysis/audit_set.py). Read-only: problems are collected and printed,
and fixes are made by hand in the set.

  - shape: each entry is " <word>" with one lower-case word, its group is its group's label, its
    categories have exactly the set's fields, and each value is one of its axis's values;
  - duplicates: no text or word twice;
  - tokens: `categories.tokens` is "one" exactly when " <word>" is one token;
  - the capture's own reading: each entry through the sentence route's prompt (its date pinned) and
    the real capture_step with a stand-in model in a temporary lake: one record, at the user's word
    (the next token ends the message), with its token count and offset 1 in the stored text;
  - the prompt's own text: no word appears in the prompt outside the user's message;
  - counts per group and axis, words that split per group, held-out families per group.
"""
from __future__ import annotations

import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "data/models/gpt-oss-20b"
PIN_DATE = "2026-09-16"  # the date the lexical captures pin (nouns_meaning_feeling_v1 too)


def entries(data: Dict[str, Any]) -> Iterator[Tuple[str, Dict[str, Any]]]:
    for g in data["groups"]:
        for e in g["sentences"]:
            yield g["label"], e


def check_shape(data: Dict[str, Any], category_fields: Sequence[str], problems: List[str]) -> None:
    axes = {a["id"]: set(a["values"]) for a in data.get("axes") or []}
    texts, words = Counter(), Counter()
    for label, e in entries(data):
        word = e["target_word"]
        texts[e["text"]] += 1
        words[word] += 1
        if e["text"] != " " + word or not re.fullmatch(r"[a-z]+", word):
            problems.append(f"shape: {e['text']!r} is not ' ' plus one lower-case word ({word!r})")
        if e["group"] != label:
            problems.append(f"shape: {word} is in group {label} but says {e['group']}")
        cats = e.get("categories") or {}
        if set(cats) != set(category_fields):
            problems.append(f"shape: {word}'s categories are {sorted(cats)}")
        for axis, values in axes.items():
            if cats.get(axis) not in values:
                problems.append(f"shape: {word}'s {axis} {cats.get(axis)!r} is not one of {sorted(values)}")
    problems.extend(f"duplicate text: {t!r} x{n}" for t, n in texts.items() if n > 1)
    problems.extend(f"duplicate word: {w} x{n}" for w, n in words.items() if n > 1)


class StandInModel:
    """The capture's forward pass without the model: zeros of the right shapes."""

    def __init__(self) -> None:
        self.model = SimpleNamespace(device="cpu")
        self.n = 0

    def initialize_hooks(self, session_id: str) -> None:
        pass

    def clear_captured_data(self) -> None:
        pass

    def cleanup_hooks(self) -> None:
        pass

    def run_forward_pass(self, tokens: Any, kv: Any = None, use_cache: bool = False) -> Any:
        self.n = int(tokens.shape[1])
        return SimpleNamespace(logits=None), None

    def get_captured_data(self) -> Any:
        import torch
        zeros = torch.zeros(1, self.n, 4)
        return ({"layer_0": {"routing_weights": torch.zeros(1, self.n, 32)}},
                {"layer_0": {"embedding": zeros}}, {"layer_0": {"residual_stream": zeros}})


def prompt_ids(tokenizer: Any, text: str) -> Tuple[str, List[int]]:
    """The sentence route's prompt for one item, with its date pinned (api/routers/probes.py)."""
    rendered = tokenizer.apply_chat_template([{"role": "user", "content": text}], tokenize=False,
                                             add_generation_prompt=True)
    rendered = re.sub(r"Current date: \d{4}-\d{2}-\d{2}", f"Current date: {PIN_DATE}", rendered)
    return rendered, tokenizer.encode(rendered, add_special_tokens=False)


def check_capture(data: Dict[str, Any], problems: List[str]) -> Dict[str, int]:
    """Tokens, the capture's reading and the prompt's own words. Returns each word's token count."""
    sys.path.insert(0, str(ROOT / "backend/src"))
    from transformers import AutoTokenizer

    from services.probes.integrated_capture_service import IntegratedCaptureService

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    end_id = tokenizer.convert_tokens_to_ids("<|end|>")
    counts = {}
    with tempfile.TemporaryDirectory() as lake:
        service = IntegratedCaptureService(None, tokenizer, [0], data_lake_path=lake)
        service.orchestrator = StandInModel()
        session = service.create_sentence_session("audit", 1, "audit", ["audit"])
        for label, e in entries(data):
            word, text = e["target_word"], e["text"]
            n = len(tokenizer.encode(text, add_special_tokens=False))
            counts[word] = n
            if (n == 1) != (e["categories"]["tokens"] == "one"):
                problems.append(f"tokens: {word} is {n} tokens but says {e['categories']['tokens']!r}")
            rendered, ids = prompt_ids(tokenizer, text)
            outside = rendered.replace(f"<|message|>{text}<|end|>", "<|message|><|end|>", 1)
            if re.search(rf"\b{re.escape(word)}\b", outside, re.IGNORECASE):
                problems.append(f"prompt: {word!r} also appears in the prompt outside the user's message")
            records, _ = service.capture_step(session, ids, [word], split_words=True,
                                              metadata={"label": label, "input_text": text})
            if len(records) != 1:
                problems.append(f"capture: {word} gave {len(records)} records")
                continue
            r = records[0]
            if r.target_token_position + 1 >= len(ids) or ids[r.target_token_position + 1] != end_id:
                problems.append(f"capture: {word} was read at position {r.target_token_position}, not at the user's word")
            if r.target_token_count != n:
                problems.append(f"capture: {word} recorded {r.target_token_count} tokens, the tokenizer gives {n}")
            if r.target_char_offset != 1:
                problems.append(f"capture: {word}'s offset is {r.target_char_offset}, not 1")
        service.finalize_session(session)
    return counts


def report_counts(data: Dict[str, Any], axes: Sequence[str], family_field: Optional[str],
                  problems: List[str], min_families: int = 3) -> None:
    """Counts per group: items, words that split, held-out families, and each axis's values."""
    by_group: Dict[str, Counter] = defaultdict(Counter)
    families: Dict[str, Counter] = defaultdict(Counter)
    lengths: Dict[str, List[int]] = defaultdict(list)
    for label, e in entries(data):
        cats = e["categories"]
        by_group[label]["items"] += 1
        by_group[label]["split"] += cats["tokens"] == "several"
        lengths[label].append(len(e["target_word"]))
        if family_field:
            families[label][cats[family_field]] += 1
        for axis in axes:
            by_group[label][f"{axis}={cats[axis]}"] += 1
    total = sum(c["items"] for c in by_group.values())
    print(f"\n{total} items in {len(by_group)} groups")
    for label, c in by_group.items():
        line = (f"  {label:20s} {c['items']:4d} items, {c['split']:3d} split ({c['split'] / c['items']:.0%}), "
                f"mean length {sum(lengths[label]) / len(lengths[label]):.1f}")
        if family_field:
            line += f", {len(families[label])} held-out families"
            if len(families[label]) < min_families:
                problems.append(f"families: {label} has {len(families[label])} held-out families, fewer than {min_families}")
        print(line)
    for axis in axes:
        values = sorted({k.split("=", 1)[1] for c in by_group.values() for k in c if k.startswith(axis + "=")})
        print(f"\n{axis}:")
        print(f"  {'':20s}" + "  ".join(f"{v[:14]:>14s}" for v in values))
        for label, c in by_group.items():
            print(f"  {label:20s}" + "  ".join(f"{c[f'{axis}={v}']:14d}" for v in values))


def finish(problems: List[str]) -> None:
    print(f"\n{len(problems)} problems" + (":" if problems else ""))
    for p in problems:
        print("  " + p)
    sys.exit(1 if problems else 0)
