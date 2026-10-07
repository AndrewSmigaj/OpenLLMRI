"""parse_harmony_channels: the analysis channel is the reasoning, the final channel the action."""
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
