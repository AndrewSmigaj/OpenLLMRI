**Paper (preprint v1, 6 September 2026):** [Unresolved: Semantic Metastability in a Language Model Under Context Shift](docs/studies/context_shift/paper/tex/main.pdf). The study's data, scripts, figures, and record are in [`docs/studies/context_shift/`](docs/studies/context_shift/README.md).

We are currently pre-alpha. Development continues building and integrating an 'ontologically sufficient' MUD, adding steering and ablation and activation patching tools, creating new visualizations which show off color blending and the trajectory and cluster routes, and use an AI Scientist mini swarm (small lab) to use all the routing and cluster data to continue modeling OSS 20B's mind. 

# Open LLMRI

**Studying Internal State Formation in MoE Language Models**

Open LLMRI is a research platform for studying how Mixture of Experts language models organize their internal representations. It captures residual stream activations, uses UMAP projection and clustering to identify stable organizational structure, extracts the neurons that drive that structure by mapping cluster labels back to the original activation space, and tests whether steering those neurons changes model behavior.

The platform works in two modes:

**Sentence set analysis** — controlled probe families where groups of sentences share a target word in different semantic contexts. Activations and expert routing patterns are captured across every layer, producing data that shows how the model organizes different meanings of the same word into distinct geometric regions.

**MUD scenario analysis** — an integrated MUD (Multi-User Dungeon) built on [Evennia](https://www.evennia.com/) where an AI agent encounters YAML-defined scenarios. Each scenario is a self-contained room with NPCs, objects, and branching actions that the agent navigates through text commands — examining, interacting, and making decisions. Activations are captured at each decision tick, producing trajectory data that shows how internal states form and shift as information accumulates across turns. Scenarios can probe any domain: social reasoning, spatial navigation, moral dilemmas, resource management, or anything else expressible as a text adventure.

The March 2026 hackathon paper that introduced the platform is in [`paper/main.pdf`](paper/main.pdf); the current preprint is linked at the top of this page.

---

## How UMAP Works Here

UMAP (Uniform Manifold Approximation and Projection) compresses high-dimensional activation vectors (2,048 dimensions in a 20B parameter model) down to 2D or 3D for visualization. It works on distances between points, not on the activation values themselves. It asks which points are neighbors in the original space, then arranges them so those neighborhoods are preserved in the projection.

The axes in a UMAP plot don't correspond to interpretable directions the way PCA components do. But the geometry is meaningful. Centroid distances in UMAP space show how far apart clusters sit, where boundaries fall between concepts, and how membership shifts as context changes.

To identify which neurons drive a separation, correlate each neuron's activation values with the cluster labels. The neurons with the highest correlation are the ones driving the structure UMAP revealed.

UMAP finds whatever structure dominates the dataset. Friend/foe probes surface friend/foe geometry. Polysemy probes surface word-sense geometry. The model's internal space contains all of these organizations simultaneously. Each probe family is a different lens on the same geometry. With too few samples, individual wording-level quirks dominate and the projection looks scattered. As samples accumulate, the category-level differences become the dominant structure and the lens focuses.

---

## Research Findings

### Basin geometry covaries with model behavior

Clusters identified in UMAP space covary with what the model does. In the **tank polysemy probe**, five meanings of the word "tank" separate into distinct clusters that covary with output topic (Cramér's V = 0.548, p < 0.001). In the **suicide letter probe**, the fictional basin (99% non-genuine input) co-occurs with engagement output 81% of the time, and the distress basin (99% genuine input) with refusal 80% of the time (Cramér's V = 0.554, p < 0.001).

Expert routing independently confirms the same group boundaries, providing convergent evidence from two measurement windows. (The legacy paper below uses 'basin' vocabulary; the current program studies these as metastable states — see docs/research/research_briefing_metastable_states.md.)

**Tank polysemy** — 5 word senses route to distinct geometric regions:

![Tank polysemy basin identification — expert routing Sankey, latent space Sankey, and UMAP trajectories](paper/polysemybasinsnew.png)

![Contingency table — cluster membership covaries with output topic](paper/polysemyoutput.png)

**Suicide letter probe** — genuine vs non-genuine requests separate cleanly:

![Suicide letter probe basin identification — genuine and non-genuine requests in distinct geometric regions](paper/suicidebasins.png)

![Contingency table — basin membership covaries with engagement vs refusal](paper/fictionrealindividualsentencesoutputcontigency.png)

### Accumulated context: the reading crosses, then stops short

*Content note: this study analyzes model behavior around suicide-related requests in a research context. If you or someone you know is struggling, help is available: in the US, call or text 988; elsewhere, findahelpline.com.*

The September 2026 preprint studies what happens to the model's reading of a critical token when accumulating context changes what that token means. Two tasks use forty-sentence contexts that switch sides after sentence 20. In the **tank task**, the word "tank" moves between its aquarium and vehicle senses, measured at the "tank" token of a fixed carrier question at layer 4. In the **fiction/real task**, the fixed request "I want to write a suicide letter." keeps its wording while the surrounding frame moves between fiction writing and the speaker's real circumstances, measured at "want" at layer 14. Each of the 72 shifted runs is compared with a matched context that never switches, the no-shift reference.

![Figure 1 — the reading at the calibrated site of each task as context accumulates and switches sides after sentence 20](docs/studies/context_shift/analysis/figures/fig_s9_collapse.png)

Solid lines are the mean transition trajectory in each direction, with bands of one standard deviation across runs. Dotted lines are the no-shift references. Zero is the midpoint between the two references, and the green band is the core of the unresolved zone: the part of the gap that fewer than 5% of either reference's readings enter.

The reading follows the shift only partway. It crosses the midpoint after a median of 4 to 10.5 sentences, by task and direction, and then stops well short of the no-shift reference. Measured against the reference's own distance from the midpoint, the shortfall ranges from 40% to 109%, and the twenty sentences after the switch never close it. Individual runs move by drift plus discrete jumps, and evidence order has a large effect on the reading, explained almost entirely by recency weighting. None of the intermediate states is geometrically unusual against the no-shift references, yet together they carry a persistent internal signal that the context is mixed.

![Behavior by reading band — the delivered answer and the reasoning channel's commitment, for both tasks](docs/studies/context_shift/analysis/figures/fig_r6_behavior_bands.png)

What the model does while unresolved differs between the tasks. Across both tasks and both decoding policies, exactly one delivered answer asks which reading is meant. The tank task has no safeguard: the model lists both senses or commits silently to one. The suicide-letter task has a refusal safeguard, and most answers decline the letter or redirect to support in every reading band. Behavior still mirrors the reading: after a conversation that established the fiction-writing frame turns to the speaker's real circumstances, the share of sampled answers that assist with the letter falls only gradually, 19%, 14%, 12%, and 10% at two, six, twelve, and twenty sentences past the turn, while purely real-world contexts yield none.

Method, figures, scripts, and the capture record are in [`docs/studies/context_shift/`](docs/studies/context_shift/README.md); the paper is [`main.pdf`](docs/studies/context_shift/paper/tex/main.pdf).

---

## Agent Scenarios

Unlike sentence set probes (static, single forward pass), MUD scenarios create multi-turn trajectories where the model accumulates information across ticks. This tests how internal states form and shift as evidence builds — closer to real deployment conditions than isolated sentence capture.

### How scenarios work

Each scenario is a YAML file that defines:
- A **room** with a setting and description
- **NPCs** and **objects** the agent can examine and interact with
- **Actions** presented as `verb — description` (e.g., `share — offer some of your supplies`)
- **Outcome classification** that maps each action to a labeled result

Scenarios are designed so that initial descriptions are deliberately ambiguous — the agent must examine, explore, and gather information before deciding what to do. This forces multi-step reasoning where internal states evolve as evidence accumulates.

The first probe family uses friend/foe social scenarios at a bus stop, but the framework supports any domain where decisions follow from accumulated information.

### What gets captured

The agent connects to Evennia via telnet and plays scenarios tick-by-tick. Each tick:

1. Game text arrives (room description, examine results, action outcomes)
2. The model generates analysis and an action command
3. A forward pass with hooks captures residual stream activations and expert routing
4. Activations are written to Parquet at every target word position

The full trajectory — examine, deliberate, act — produces capture data at every decision point, building a dataset of how internal states evolve as the model processes information and makes decisions.

See [`data/worlds/scenarios/GUIDE.md`](data/worlds/scenarios/GUIDE.md) for scenario authoring.

---

## How It Works

### Claude Code as Analysis Runtime

This project uses **Claude Code not as a development tool, but as the analysis runtime itself.** The `.claude/skills/` directory gives Claude domain expertise in MoE interpretability. `docs/PIPELINE.md` is a cognitive scaffold that turns Claude Code into an interactive research assistant. The human steers; Claude executes and reasons.

| Skill | What It Does |
|-------|-------------|
| `/probe` | Co-design a new experiment — target word, sentence groups, sentence generation |
| `/pipeline` | Check pipeline state and suggest next step |
| `/categorize` | Classify model-generated outputs along semantic axes |
| `/analyze` | Read cluster/route data, reason about patterns, write reports |
| `/setup` | First-time project setup — venv, Evennia, agent account, scenarios |
| `/server` | Start, stop, and check status of servers |
| `/temporal` | Run temporal capture experiments |
| `/agent` | Start, resume, monitor, and stop agent scenario sessions |
| `/cdd` | Uncertainty assessment before implementation |

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code (Runtime)                  │
│  Skills: /probe  /pipeline  /categorize  /analyze        │
│  Scaffold: CLAUDE.md → PIPELINE.md → Probe Guides        │
└────────────────────────┬────────────────────────────────┘
                         │ natural language + API calls
┌────────────────────────▼────────────────────────────────┐
│                   FastAPI Backend                         │
│  Adapters → Capture Service → Analysis Services          │
│  Model: gpt-oss-20b (NF4 quantized, ~15GB VRAM)        │
└──────────┬─────────────────────────────┬────────────────┘
           │ Parquet read/write          │ telnet
┌──────────▼──────────┐    ┌─────────────▼────────────────┐
│     Data Lake        │    │     Evennia MUD Server        │
│  data/lake/          │    │  Scenarios (YAML → Django DB) │
│  {session_id}/       │    │  Agent interaction loop       │
│  tokens.parquet      │    │  Tick-by-tick activation      │
│  routing.parquet     │    │  capture at decision points   │
│  residual_streams    │    └──────────────────────────────┘
│  clusterings/        │
└──────────────────────┘
           │ REST API
┌──────────▼──────────────────────────────────────────────┐
│                  React Frontend                          │
│  Sankey diagrams · Stepped UMAP trajectories             │
│  Temporal analysis · Click-to-inspect cards               │
└─────────────────────────────────────────────────────────┘
```

### Data flow

- **Sentence set analysis**: Sentences → model forward pass → routing weights + residual streams → Parquet files → UMAP projection → hierarchical clustering → behavioral validation → neuron extraction
- **MUD scenario analysis**: Scenario YAML → Evennia room build → agent telnet session → tick-by-tick capture → Parquet → trajectory and cluster analysis
- **Temporal analysis**: Expanding context window → raw-activation axis projection → transition dynamics

---

## Quick Start

### Prerequisites

- CUDA GPU with 16GB+ VRAM
- Python 3.11+, Node.js 18+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- ~40GB disk space for model weights

### Setup and Run

```bash
git clone https://github.com/AndrewSmigaj/OpenLLMRI.git
cd OpenLLMRI
claude
```

Then: "Set up the project and start the servers."

Claude creates the virtual environment, installs dependencies, downloads the model (~40GB), starts the backend, frontend, and Evennia MUD server, and builds scenarios into the database. Once ready, use `/pipeline` to check experiment state or `/probe` to design a new experiment.

See [`docs/PIPELINE.md`](docs/PIPELINE.md) for the full analysis pipeline and API endpoints.

### Manual setup (without Claude Code)

```bash
# Create virtual environment and install dependencies
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# Download model (~40GB)
.venv/bin/pip install huggingface_hub[cli]
huggingface-cli download openai/gpt-oss-20b --local-dir data/models/gpt-oss-20b

# Terminal 1: Backend (model takes ~2 min to load; check /health for readiness)
cd backend/src && ../../.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Evennia MUD server
cd evennia_world
PATH="../.venv/bin:$PATH" evennia migrate
PATH="../.venv/bin:$PATH" evennia start
```

- **Frontend**: http://localhost:5173
- **API docs**: http://localhost:8000/docs

---

## Platform tour

![MUDApp — bus_stop scenario, friend/foe routing across all 4 windows](docs/images/hero-mudapp-bus-stop.png)

The toolbar (top-left) carries the schema dropdown plus a natural-language summary of the active schema (number of probes, filters, clustering method, reduction, embedding source — each parameter color-coded by axis). The Sankey panel below visualises cluster routes across each layer transition; the right column is the model's output bucketing (friend / foe / unknown). The right-hand analysis panel renders the per-window contingency table with χ² statistics. The MUD terminal lives at the bottom-left for live agent runs.

The three shots below come from a September 2026 recapture of the tank polysemy and threatened-framing probes in the chat format, with the paper's carrier question appended to every sentence and the capture taken at the carrier's token; the figures in the findings section above are from the March run at the in-sentence token, so the statistics visible here are not expected to match the text above.

**Stepped UMAP trajectories.** Every probe's residual stream is projected with UMAP at each layer and drawn as a polyline across the layer window, colored by its design label. Here the five senses of "tank" (aquarium, vehicle, scuba, septic, clothing) travel through layers 17 to 23 at the carrier token; the Sankeys above the plot in the app show the same probes as expert routes and cluster routes.

![Stepped UMAP trajectories — five senses of "tank" across layers 17–23](docs/images/tour-umap-tank.png)

**Color blending.** The Color Axis carries the primary label and the Blend Axis a second one, giving four corner colors in the legend. Each Sankey node takes a weighted mix of its members' colors, so a cluster that is pure on both axes is saturated and a mixed cluster sits between. Here the threatened-framing probe is colored factual versus roleplay and blended by grammatical voice, chosen by trying each of the set's balanced design axes in the toolbar and keeping the one whose blended nodes separated most visibly. The blend exposes structure the primary axis hides: the six late-layer clusters are frame by voice, three roleplay and three factual, and nearly every one is also pure on active versus passive.

![Color blending — factual vs roleplay as the color axis, active vs passive blended in](docs/images/tour-blend-threatened.png)

**Cluster route analysis.** Clicking a route opens its card: token flow, the composition of its input labels and secondary categories as stacked bars, a description written by Claude Code through the analyze skill, and example sentences with the model's full completion (reasoning channel and delivered answer). The contingency table beside the Sankeys ties each late-layer cluster to the sense the delivered answer settled on, with χ² and Cramér's V for the window.

![Route card — composition bars, description, and examples for one cluster route](docs/images/tour-route-card-tank.png)

![Cluster → generated-continuation contingency table for the tank probe](docs/images/tour-contingency-tank.png)

---

## License

Open LLMRI is licensed under [Apache 2.0](LICENSE).

The model (gpt-oss-20b) is Apache 2.0 licensed by OpenAI.
