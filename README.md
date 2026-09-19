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

## The platform

![MUDApp — the bus stop scenario after the agent has examined the person, layers 17–23, with the 99%-foe cluster L23C1 selected and its card open](docs/images/hero-mudapp-bus-stop.png)

The main view is one page. The toolbar at the top-left names the session and the clustering schema, and prints the schema as a sentence (number of probes, filters, clustering method, reduction, embedding source, each parameter color-coded). Below it are two rows of Sankey diagrams, one per layer transition in the selected six-layer window: **Expert Routes** shows which MoE expert each probe's target token was routed to at each layer, **Clusters & Routes** shows which cluster of the residual stream it fell into. The rightmost column of each row is the outcome: for a sentence probe, the category the model's delivered answer was classified into; for an agent run, the action the agent chose. The top-right panel sets the visual encoding: a Color Axis for the primary label, a Blend Axis for a second one, and separate color and blend axes for the output column. The analysis panel on the right holds the per-window contingency table with χ² and Cramér's V, the window synthesis written by Claude Code, and the card for whatever node or route was last clicked. The MUD terminal sits at the bottom-left for live agent runs.

The three shots below come from a September 2026 recapture of two sentence probes in the model's chat format, with the paper's carrier question appended to every sentence and the capture taken at the carrier's own token, so the delivered answer is a direct commitment the classifier can read.

**Cluster routes and stepped UMAP trajectories.** The probe is the five-sense tank set: 500 sentences, 100 each for the aquarium, armored vehicle, scuba cylinder, septic or storage tank, and sleeveless-top senses, each followed by "What is the meaning of the word tank?". Every probe's residual stream at that token is projected with UMAP at each layer and drawn as a polyline across the window, colored by its design sense. The Sankeys above the plot show the same probes as flows between per-layer clusters, ending in the sense the model's answer settled on. Aquarium, vehicle and clothing each hold a clean basin from layer 17 to 23; scuba and septic never get basins of their own at this cluster count, because the model groups them by register instead, technical pressure-vessel language in one basin and narrative handling and storage in another, and the generic "container" answer is the single most common answer in the run.

![Cluster-route Sankeys for layers 17–23 above the stepped UMAP trajectories of the five senses of "tank"](docs/images/tour-umap-tank.png)

**Route cards.** Hovering a ribbon in a Sankey highlights that route and shows its flow; clicking it opens the card. The card gives the route's token count, coverage and confidence, stacked bars for the composition of its members on the design label and on every secondary category (here structure and register), a description written by Claude Code through the analyze skill, and the member sentences with the model's full completion, reasoning channel followed by the delivered answer. The route shown is the aquarium basin carrying itself from layer 22 to 23: 82 sentences, 93% aquarium-labeled, and 77 of them answered "aquarium".

![The hovered route highlighted in the last transition with its tooltip, and its card below: composition bars, description, and example completions](docs/images/tour-route-card-tank.png)

**Color blending.** The probe is the threatened-framing set: 400 sentences that use "threatened" in either a roleplay frame (fantasy, science fiction, myth) or a factual one (courts, politics, crime), balanced on grammatical voice, scale and specificity, each followed by "Is the word threatened used here in fiction or in a factual account?". The Color Axis carries the frame and the Blend Axis carries voice, which gives the four corner colors in the legend. Each Sankey node takes a weighted mix of its members' colors, so a cluster pure on both axes is saturated and a mixed cluster sits between, and the trajectory plot draws every probe's path in the same blended color. The blend exposes structure the primary axis hides: the six late-layer clusters are frame by voice, three roleplay and three factual, and nearly every one is also pure on active versus passive. Voice was chosen by trying each balanced axis in the toolbar and keeping the one whose blended nodes separated most visibly, which is what the feature is for.

![Color blending — factual vs roleplay as the color axis and active vs passive blended in, on the Sankeys and on the trajectory plot](docs/images/tour-blend-threatened.png)

---

## How UMAP Works Here

UMAP (Uniform Manifold Approximation and Projection) compresses high-dimensional activation vectors (2,048 dimensions in a 20B parameter model) down to 2D or 3D for visualization. It works on distances between points, not on the activation values themselves. It asks which points are neighbors in the original space, then arranges them so those neighborhoods are preserved in the projection.

The axes in a UMAP plot don't correspond to interpretable directions the way PCA components do. But the geometry is meaningful. Centroid distances in UMAP space show how far apart clusters sit, where boundaries fall between concepts, and how membership shifts as context changes.

To identify which neurons drive a separation, correlate each neuron's activation values with the cluster labels. The neurons with the highest correlation are the ones driving the structure UMAP revealed.

UMAP finds whatever structure dominates the dataset. Friend/foe probes surface friend/foe geometry. Polysemy probes surface word-sense geometry. The model's internal space contains all of these organizations simultaneously. Each probe family is a different lens on the same geometry. With too few samples, individual wording-level quirks dominate and the projection looks scattered. As samples accumulate, the category-level differences become the dominant structure and the lens focuses.

---

## Research Findings

### Friend or foe: the signal forms only after the agent looks

In the bus-stop scenarios the agent arrives at a stop where a person is doing something ambiguous, such as searching frantically through a bag. At the first tick the agent has only that description. At the second tick it has examined the person and received the clarifying detail: looking around to make sure no one sees them, or wheezing and saying they need their inhaler. The same scenario family is written in a friend version and a foe version, and the activations at the token "person" are captured at each tick. With 479 varied scenarios, clustering the residual stream in layers 17 to 23 gives the two pictures below.

![Tick 0, before the agent examines the person: cluster routes, stepped UMAP trajectories, and the cluster-by-action contingency table](docs/images/tour-busstop-tick0.png)

![Tick 1, after the examination: the same views, now split into friend and foe](docs/images/tour-busstop-tick1.png)

At tick 0 the clusters are a purple tangle of both labels and the contingency table reports a Cramér's V of 0.14. At tick 1 two of the five clusters are nearly pure, one 99% foe and one 98% friend, and between them they hold half the probes; the same statistic is 0.70. Nothing about the sample changed between the two pictures; the information did. Structure that UMAP can bring into focus with enough samples has to exist in the representation first, and here it appears only once the agent has looked.

### Five senses of one word, read at a single token

The tank probe above also measures how the model's internal grouping relates to what it says. For every sentence the delivered answer was classified into the sense it settled on, and the table ties each late-layer cluster to those answers.

![Cluster → delivered-answer contingency table for the five-sense tank probe, layers 17–23](docs/images/tour-contingency-tank.png)

The aquarium, clothing and vehicle clusters answer their own sense in 94% to 100% of cases. The two container clusters split between "scuba" and the generic "container" answer, and the mixed casual-register cluster holds most of the hedged and looped answers. Where the design label and the cluster disagree, the answer follows the cluster: aquarium sentences that mention only hardware are filed with storage tanks and answered "container", and clothing sentences about "the front of the tank" are filed with vehicles and answered "vehicle".

### Genuine and fictional requests separate as single sentences

In the **suicide letter probe**, 198 single sentences ask to write a suicide letter, half inside a fictional frame and half about the speaker's real circumstances. Genuine and non-genuine requests fall into distinct geometric regions, and the regions covary with what the model does: the fictional basin (99% non-genuine input) co-occurs with engagement 81% of the time, and the distress basin (99% genuine input) with refusal 80% of the time (Cramér's V = 0.554, p < 0.001).

![Suicide letter probe basin identification — genuine and non-genuine requests in distinct geometric regions](paper/suicidebasins.png)

![Contingency table — basin membership covaries with engagement vs refusal](paper/fictionrealindividualsentencesoutputcontigency.png)

The legacy paper below uses "basin" vocabulary; the current program studies these as metastable states, see docs/research/research_briefing_metastable_states.md.

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

## License

Open LLMRI is licensed under [Apache 2.0](LICENSE).

The model (gpt-oss-20b) is Apache 2.0 licensed by OpenAI.
