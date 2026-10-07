"""parse_harmony_channels: the analysis channel is the reasoning, the final channel the action."""
from pathlib import Path

import pytest

from services.agent.harmony_parser import parse_harmony_channels

WITH_MARKERS = ("<|channel|>analysis<|message|>They are hiding something.<|end|>"
                "<|start|>assistant<|channel|>final<|message|>alert the bouncer<|return|>")


def test_channels_are_read_when_the_markers_are_kept():
    out = parse_harmony_channels(WITH_MARKERS)
    assert out["analysis"] == "They are hiding something."
    assert out["action"] == "alert the bouncer"


def test_without_the_markers_the_whole_output_becomes_the_action():
    # What a decode with skip_special_tokens=True leaves (the agent-run bug; the parser's fallback).
    stripped = "analysisThey are hiding something.assistantfinalalert the bouncer"
    out = parse_harmony_channels(stripped)
    assert out["analysis"] == "" and out["action"] == stripped


def test_a_final_channel_without_analysis():
    out = parse_harmony_channels("<|channel|>final<|message|>look<|return|>")
    assert out == {"analysis": "", "action": "look", "raw": "<|channel|>final<|message|>look<|return|>"}


MODEL = Path(__file__).resolve().parents[2] / "data" / "models" / "gpt-oss-20b"


@pytest.mark.skipif(not (MODEL / "tokenizer.json").exists(), reason="needs the local gpt-oss tokenizer")
def test_with_the_real_tokenizer_only_a_decode_that_keeps_the_markers_parses():
    # The channel markers are special tokens (ids 200005-200008): the agent's generation must be
    # decoded with skip_special_tokens=False, or the whole output becomes the action.
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL)
    ids = tok.encode(WITH_MARKERS, add_special_tokens=False)
    kept = parse_harmony_channels(tok.decode(ids, skip_special_tokens=False))
    assert kept["analysis"] == "They are hiding something."
    assert kept["action"] == "alert the bouncer"
    stripped = parse_harmony_channels(tok.decode(ids, skip_special_tokens=True))
    assert stripped["action"] != "alert the bouncer" and "hiding" in stripped["action"]
