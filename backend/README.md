# Open LLMRI — Backend

FastAPI server that captures MoE routing patterns and provides analysis endpoints.

## Architecture

```
api/
├── main.py              # FastAPI app, lifespan (model loading, the job scheduler, the app's event stream), CORS
├── app_events.py        # The server-sent event stream open apps listen on (show, job, lens, ping)
├── dependencies.py      # The capture service and its model loading
├── schemas.py           # Pydantic request/response models
└── routers/
    ├── probes.py        # Sessions, captures, sentence experiments, legacy clustering schemas
    ├── lenses.py        # Lenses: build, versions, save, flows, members, fingerprints, validation, details
    ├── analysis.py      # LLM cards, packets, questions, the analyst tests
    ├── jobs.py          # Background jobs: list, status, cancel
    ├── commands.py      # The command interface (show, build) and the event stream
    ├── atlas.py         # The atlas's node catalogue
    ├── studies.py       # Study files
    ├── agent.py         # Agent runs in the MUD
    ├── generation.py    # Sentence set listing and generation
    ├── prompts.py       # Scaffold template delivery
    └── insights.py      # The experiments health check

services/
├── probes/              # Capture: sessions, model inference, routing capture, Parquet I/O
├── lenses/              # Lens build (UMAP + Ward per layer), versions, flows, experts, validation,
│                        #   raw space, mass-mean axes, node details, the model's weights, atlas entries
├── llm/                 # Analysts (claude -p), evidence packets, the number checker, cards, analyst tests
├── jobs/                # The job store, the scheduler (lanes) and the worker process
├── agent/               # The agent loop, the MUD client, the harmony parser, the scenario library
├── experiments/         # token_filters.py: last-occurrence and subsampling filters
├── generation/          # Sentence set loading and generation
└── studies.py           # Study files (docs/studies/<id>/study.yaml)

adapters/
├── base_adapter.py      # ModelAdapter ABC — abstracts model-specific behavior
├── gptoss_adapter.py    # gpt-oss-20b: 24 layers, 32 experts, top-4, TOPK_THEN_SOFTMAX
├── olmoe_adapter.py     # OLMoE-1B-7B: 16 layers, 64 experts, top-8, SOFTMAX_THEN_TOPK
└── registry.py          # Adapter registration and lookup

schemas/                  # Parquet data contracts (Pydantic models)
├── tokens.py            # ProbeRecord — input text, label, generated output
├── routing.py           # RoutingRecord — per-layer expert routing weights
├── embedding.py         # EmbeddingRecord — per-layer expert output embeddings
├── residual_stream.py   # ResidualStreamState — per-layer residual stream vectors
└── capture_manifest.py  # CaptureManifest — session provenance metadata

core/
├── parquet_reader.py    # Generic Parquet → Pydantic record reader
└── parquet_writer.py    # Batched Parquet writer with schema validation
```

## Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Model load state, GPU availability |
| `/api/probes` | GET | List all probe sessions |
| `/api/probes/{id}` | GET | Session details with sentences |
| `/api/probes/sentence-experiment` | POST | Run a full sentence capture experiment |
| `/api/lenses` | POST | Build a lens (a background job; 202 with the job) |
| `/api/sessions/{id}/lenses` | GET | A session's lenses, with legacy schemas |
| `/api/sessions/{id}/lenses/{name}/flows` | GET | Cluster or expert flows over every layer |
| `/api/sessions/{id}/lenses/{name}/validate` | POST | Held-out scores and the k profile (a job) |
| `/api/sessions/{id}/lenses/{name}/details` | POST | Neurons, logit lens, surface check, routing (a job) |
| `/api/sessions/{id}/lenses/{name}/save` | POST | Freeze a version; its reports follow (a job) |
| `/api/sessions/{id}/lenses/{name}/cards/{card}` | GET | An LLM-written card, its numbers checked |
| `/api/jobs/{id}` | GET | A background job's state and progress |
| `/api/commands` | POST | Show a view in the open apps, or build a lens |
| `/api/app/events` | GET | The open apps' event stream |
| `/api/atlas/nodes` | GET | The atlas's node catalogue |
| `/api/studies` | GET | The study files |
| `/api/probes/sessions/{id}/clusterings` | GET | List legacy clustering schemas |

The skills hold the full, copy-paste procedures: `/cluster` (lenses), `/analyze` (reports),
`/app` (commands), `/agent` (agent runs).

## Running

```bash
cd backend/src
../../.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Model loading takes a minute or more. Check `/health`: `model_loaded: true` means ready. After a
code change, restart fully (the `/server` skill); don't use `--reload`.

## The Adapter Pattern

All model-specific behavior (layer count, expert count, routing style, weight loading) is encapsulated in adapters. To add a new model:

1. Create `adapters/your_model_adapter.py` implementing `BaseModelAdapter`
2. Define a `ModelTopology` with the model's constants
3. Register it: `register_adapter("your-model", YourAdapter)`

The rest of the pipeline (capture, analysis, visualization) works unchanged.
