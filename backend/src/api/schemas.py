#!/usr/bin/env python3
"""
Simple Pydantic schemas for API requests/responses.
"""

import os
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProgressInfo(BaseModel):
    """Session progress details."""
    completed: int
    total: int
    failed: int
    percent: float


class SentenceEntry(BaseModel):
    """A single sentence within a sentence set."""
    text: str
    group: str
    target_word: Optional[str] = None
    categories: Optional[Dict[str, str]] = None


class SentenceSetSummary(BaseModel):
    """Summary info for a sentence set."""
    name: str
    target_word: str
    labels: List[str]
    counts: Dict[str, int]
    total: int


class ExecutionResponse(BaseModel):
    """Response after starting session execution."""
    started: bool
    probe_ids: List[str]
    status_url: str
    estimated_time: Optional[str] = None


class StatusResponse(BaseModel):
    """Session status response."""
    session_id: str
    state: str
    progress: ProgressInfo
    manifest: Optional[Dict[str, Any]] = None
    data_lake_paths: Optional[Dict[str, str]] = None


class SessionListResponse(BaseModel):
    """Response for listing sessions."""
    session_id: str
    session_name: str
    created_at: str
    probe_count: int
    target_word: Optional[str] = None
    labels: Optional[List[str]] = None
    state: str


class SessionDetailResponse(BaseModel):
    """Response for session details."""
    manifest: Dict[str, Any]
    data_lake_paths: Dict[str, str]
    labels: List[str]
    target_word: Optional[str] = None
    sentences: Optional[List['ProbeExample']] = None


# --- A capture's sentences ---

class ProbeExample(BaseModel):
    """Example probe for route display."""
    target_word: str
    label: Optional[str] = None
    input_text: str
    probe_id: str
    generated_text: Optional[str] = None
    output_category: Optional[str] = None
    target_char_offset: Optional[int] = None
    turn_id: Optional[int] = None
    capture_type: Optional[str] = None
    step: Optional[int] = None
    game_text: Optional[str] = None
    analysis: Optional[str] = None
    action: Optional[str] = None
    system_prompt: Optional[str] = None

# Resolve forward reference in SessionDetailResponse
SessionDetailResponse.model_rebuild()


# --- Sentence Generation Schemas ---

class GenerateSentenceSetRequest(BaseModel):
    """Request to generate a sentence set via LLM."""
    name: str
    target_word: str = "said"
    label_a: str = "narrative"
    label_b: str = "factual"
    description_a: str = "Narrative storytelling context"
    description_b: str = "Factual reporting context"
    count_per_group: int = 20
    neutral_count: int = 5
    api_key: Optional[str] = None
    provider: str = "openai"
    save: bool = True


class SentenceSetResponse(BaseModel):
    """Response with sentence set summary."""
    name: str
    version: str
    target_word: str
    label_a: str
    label_b: str
    count_a: int
    count_b: int
    count_neutral: int


class SentenceSetDetailResponse(BaseModel):
    """Full sentence set with all sentences."""
    name: str
    version: str
    target_word: str
    label_a: str
    label_b: str
    description_a: str
    description_b: str
    sentences_a: List[SentenceEntry]
    sentences_b: List[SentenceEntry]
    sentences_neutral: List[SentenceEntry]
    metadata: Dict[str, Any]


class SentenceSetListResponse(BaseModel):
    """Response listing available sentence sets."""
    sentence_sets: List[SentenceSetSummary]


# --- Sentence Experiment Schemas ---

class SentenceExperimentRequest(BaseModel):
    """Request to run a sentence experiment capture."""
    sentence_set_name: str
    session_name: Optional[str] = None
    layers: Optional[List[int]] = None  # defaults to adapter's layer list
    generate_output: bool = True  # generate continuation text for each probe
    capture_static_substring: Optional[str] = None
    # When set, residuals + routing + embeddings are also stored at every token
    # position of the LAST occurrence of this substring in each probe's tokenized
    # input (semantic positions 2, 3, ... in addition to target=1). Enables
    # per-token separation analysis without re-engineering the capture pipeline.
    logit_token_sets: Optional[Dict[str, List[str]]] = None
    # When set, the next-token logprob at the final input position (the
    # pre-generation distribution) is stored per named token set, as
    # first_token_logprobs_json on each probe record.
    logit_forced_final: bool = False
    # With logit_token_sets: append the harmony forced-final-channel scaffold
    # ("<|channel|>final<|message|>") before capture, so the logprob position is
    # the FIRST VISIBLE ANSWER TOKEN instead of the channel scaffold token.
    # Causal attention leaves all captured positions unchanged.
    max_new_tokens: int = 256
    # Generation cap for generate_output. The context-shift study's frozen
    # behavior captures used 256; the regeneration uses 2048.
    pin_date: Optional[str] = None
    # ISO date (YYYY-MM-DD). When set, the chat template's "Current date:" line is
    # rendered with this date instead of today's, so a capture can reproduce a
    # prior day's input token stream exactly (only the date tokens differ across
    # days; positions are unchanged).
    do_sample: bool = False
    # Sampled decoding for generate_output. False keeps greedy decoding (the frozen
    # and regenerated behavior captures); True samples with temperature and top_p
    # below and no top-k truncation (the model's config leaves top_k unset).
    temperature: float = 1.0
    top_p: float = 1.0
    seed: Optional[int] = None
    # RNG seed set immediately before generation when given, so a sampled draw is
    # reproducible and recorded with its session.


class SentenceExperimentResponse(BaseModel):
    """Response after running a sentence experiment."""
    session_id: str
    session_name: str
    total_probes: int
    labels: List[str]
    counts: Dict[str, int]


# --- Trajectory Points (cached UMAP-3D from a clustering schema) ---

class TrajectoryPoint(BaseModel):
    """A single 3D-reduced point baked into a clustering schema."""
    probe_id: str
    x: float
    y: float
    z: float
    label: Optional[str] = None
    target_word: Optional[str] = None
    step: Optional[int] = None
    categories_json: Optional[str] = None


class TrajectoryPointsResponse(BaseModel):
    """All cached trajectory points for a clustering schema, keyed by layer."""
    schema_name: str
    sample_size: int
    layers: List[int]
    points_by_layer: Dict[str, List[TrajectoryPoint]]


# --- Agent session schemas ---
# CLAUDE: Do NOT pass evennia_username or evennia_password in curl calls.
# They default from .env via load_dotenv() in main.py. Use the /agent skill
# OP-1/OP-1B curl templates which omit credentials entirely.

class AgentStartRequest(BaseModel):
    """Request to start a new agent capture session."""
    session_name: str
    scenario_id: str
    target_words: List[str]
    bootstrap_session_id: str = ""
    agent_name: str = "agent"
    capture_type_config: Optional[List[str]] = None
    auto_start: bool = False
    system_prompt: Optional[str] = None
    evennia_username: str = os.environ.get("EVENNIA_AGENT_USER", "agent")  # from .env — do NOT override
    evennia_password: str = os.environ.get("EVENNIA_AGENT_PASS", "")  # from .env — do NOT override
    scenario_list: Optional[List[str]] = None
    # Scenario keys from the library, "<set_id>/<file>" (data/scenarios/README.md).
    pin_date: Optional[str] = None
    # ISO date (YYYY-MM-DD) the chat template shows on every turn; today when not given. Stored
    # with the session, so a resumed run, or one on another day, sends the same prompt.


class AgentResumeRequest(BaseModel):
    """Resume an existing agent session with additional scenarios."""
    session_id: str
    scenario_list: List[str]  # scenario keys, "<set_id>/<file>"
    system_prompt: Optional[str] = None
    evennia_username: str = os.environ.get("EVENNIA_AGENT_USER", "agent")  # from .env — do NOT override
    evennia_password: str = os.environ.get("EVENNIA_AGENT_PASS", "")  # from .env — do NOT override


class AgentStartResponse(BaseModel):
    """Response from starting an agent session."""
    session_id: str
    session_name: str
    target_words: List[str]
    scenario_id: str

class AgentStopRequest(BaseModel):
    """Request to stop an agent session."""
    session_id: str

class AgentStopResponse(BaseModel):
    """Response from stopping an agent session."""
    session_id: str
    state: str
    total_turns: int

class AgentGenerateRequest(BaseModel):
    """Request for a single agent generate tick."""
    session_id: str
    prompt: str
    target_words: List[str]
    knowledge_probe: Optional[str] = None
    max_new_tokens: int = 200

class AgentGenerateResponse(BaseModel):
    """Response from an agent generate tick."""
    analysis: str
    action: str
    capture_id: str
    generated_text: str
    turn_id: int
    knowledge_capture_id: Optional[str] = None
