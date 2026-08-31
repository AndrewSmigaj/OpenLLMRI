Related: docs/SOFTWARE_OVERVIEW.md (conceptual anchor), CLAUDE.md (project rules)

# Recommendations

This is **my notebook** of recommendations to the user — open improvements, observations, suggestions that aren't this session's work but are worth flagging. Append-only.

The user reviews entries and either acts on them, dismisses them, or files them. This avoids two failure modes: noticing problems and never telling the user, or noticing problems and immediately trying to fix them without permission.

**Format**: Each entry has a date, scope tag, and a short rationale. Newest at top.

---

## 2026-05-09 — Findings/research-doc scaffolding is missing; everything ends up dumped in one folder

**Scope**: `docs/research/StudiesByClaude/`, `docs/scratchpad/`, possibly a new `docs/paper-prep/` directory.

The user can't navigate the existing findings docs because the structure is "everything in one folder with names I picked in the moment, depending on which direction I kneejerked." Mixed in `docs/research/StudiesByClaude/`:
- Per-probe-version findings (`suicide_letter_temporal_v1_findings.md`, `_v2`, `_v3`)
- Cross-probe-family rollups (`family_c_engagement_findings.md`, `basin_projection_extension_findings.md`)
- Consolidated reports (`suicide_letter_consolidated_report.md`)
- Paper drafts (`paper1_lens_and_trajectory.md`, `paper2_basin_signatures_modes.md`, `paper_draft_basin_signatures.md`)
- Other studies' findings (`lying_*`, `mode_separability_*`, `help_*`)
- One-off taxonomies (`probe_cheat_sheet.md`)
- Ideation files (`scaffold_study_ideas.md`)
- Authoring trackers (`*_authoring_tracker.md`)

Plus parallel content in `docs/scratchpad/` (capture chain logs, basin-projection JSONs, categorizer scripts, plot scripts, intermediate analyses) — different folder based on which direction I "kneejerked," not on a coherent classification.

What the user actually needs:
1. **A "current paper" folder** where I keep, in one place, the running outline + section drafts + figures + tables for the paper that's actively being written. Right now paper-relevant material is scattered across findings docs, scratchpad analyses, and the consolidated report.
2. **A clear taxonomy for findings docs** by probe family: `suicide_letter/`, `polysemy/`, `lying/`, `help/`, `mode_separability/`. Each subfolder owns its per-version findings + the rollup. The probe_cheat_sheet stays at the top as the index.
3. **A "paper insights" running ledger** — short, append-only entries when I notice something worth folding into the paper (a phrasing, a comparison, a phenomenon worth flagging). Currently I either embed these in findings docs (and they get lost) or write them in chat (and they evaporate).
4. **Scratchpad discipline**: scratchpad is for in-progress work that's not yet ready for findings. It should NOT be the place where I leave the "real" analysis (which has happened: `paper_protocol_basin_points.json` is the canonical Family-B-with-cache-on basin trajectory data and lives in scratchpad).

The user has been writing findings + analysis for a while and the accumulated mess makes it hard to navigate when starting a paper-writing session. This is blocking — they're saying "we haven't built the scaffolding for you yet so you keep track of what we are working on better and keep track of insights and findings for a paper we are working on."

Concrete next session: design the directory layout, move existing files to it (with `git mv` so history is preserved), update cross-references, and adopt a discipline of "every new finding goes in the right place, and every paper-relevant insight goes in the insights ledger as I notice it."

---

## 2026-05-09 — `/server`, `/temporal`, and skill-side runbook gaps

**Scope**: `.claude/skills/server/SKILL.md`, `.claude/skills/temporal/SKILL.md`, possibly `.claude/skills/probe/SKILL.md`.

I keep tripping over the same operational mistakes when running long captures. The skills don't currently encode the operational knowledge that would prevent them. Things I've done wrong this session that are pure operator errors, not analysis errors:

1. **Tried to fire a temporal capture while another was running.** No skill check for "is the temporal lock held right now?" — I just blasted curl. The `/temporal` skill should have an OP that says "before firing, GET status; only fire if busy=false; otherwise wait/back off." Currently the skill assumes captures are short and serial-fire works.
2. **Picked `--max-time` for chain curls out of intuition** (3600s "feels right"). No data-driven heuristic. The skill should specify: "look up the worst-case wall-clock for the same protocol-shape from prior `temporal_runs.json` entries and set max-time to ≥ 1.5×. If no prior data, run one smoke and use 1.5× of that."
3. **Started fresh chain scripts in `docs/scratchpad/` over and over** (`paper_protocol_chain.sh`, `paper_protocol_with_gen_chain.sh`, `polysemy_temporal_chain.sh`, `polysemy_capture_chain.sh`, `family_c_capture_chain.sh`...). Each reinvents the wheel: lock checks, timeout policy, log format, recovery. The `/temporal` skill should provide ONE canonical chain script (maybe as a documented template or actual `.sh` artifact in the skill dir) that handles: status polling, generous timeouts, TSV log, orphan-session recovery.
4. **Restarted backend without checking what was loaded** several times. The `/server` skill OP-1 status check exists but I didn't run it before restarts. Skill should say "always run OP-1 before OP-2" with the rationale that an in-flight capture is silently lost on restart.
5. **Manually patched the chain log TSV** to recover orphan sessions. Should be a reusable `recover_orphan_sessions.py` script in the skill or service that scans `data/lake/_sessions/*.json` for "active" state, cross-references with `temporal_runs.json`, and rewrites the chain log accordingly.
6. **Background-process pattern leaks ghost processes across sessions.** I've been calling Bash with `run_in_background: true` AND including `nohup … &` inside the command. The outer bash exits immediately (Claude task slot shows "completed"), and the `nohup`'d work runs detached — untrackable by Claude's `TaskOutput`, invisible to my own status checks, and surviving across Claude session boundaries. Today (2026-05-09) `ps -ef` shows two `-bash` shells dated 2026-04-26 still alive — leftovers from sessions weeks ago that I started and never cleaned up. The pattern is: start a chain → it completes → outer bash exits → I move on → the inner process either finishes invisibly or hangs forever, in either case nothing tells me. Recommendations:
   - **For chain scripts and one-off long-running work**: use `bash chain.sh` (no `nohup`, no `&`) with `run_in_background: true`. Claude can then poll `TaskOutput`, see real completion, and the user gets honest status.
   - **For uvicorn (genuinely needs to outlive Claude)**: keep the `nohup … &` pattern but the `/server` skill should specify "after launching, capture the PID and write it to a known file like `/tmp/openllmri_backend.pid` so subsequent OP-2 stops can verify they killed the right process and so old shells can be detected and cleaned."
   - **End-of-session cleanup**: skill or hook that does `ps -ef | grep -E "uvicorn|chain.sh|paper_protocol" | grep -v grep` and prompts on anything older than the current session start time. This would have caught the Apr 26 ghost shells the first time they outlived their session.
   - **Stop calling `nohup … &` inside `run_in_background: true`** — the two are doing redundant detachment and the result is a ghost process I lose track of. Pick one or the other based on whether the work needs to outlive Claude.
7. **Monitor / `until ... do sleep N; done` loops orphan themselves silently.** Six such loops were running in this VM today, started over the past 3 days via the `Monitor` tool: each waiting for a backend ping, a smoke-test result file, or a model-load readiness signal. Each one's grep condition either matched once and the loop didn't notice, or never matched at all. None terminated; all six showed up in the user's Claude Code sidebar as "(running)" tasks while I had no awareness of them, and the bash processes were hidden in `ps -ef` under `sleep 5`/`sleep 10` children. Recommendations:
   - **Use `Monitor` only with conditions that are KNOWN to fire** within a finite window (e.g. a file appears, a one-shot log line shows up).
   - **Add a max-iteration guard to every until-loop**: `until cond; do sleep 5; ((i++)); [[ $i -gt 60 ]] && break; done`. 5 min worst-case beats forever.
   - **Auto-cleanup hook**: a session-start or session-end hook that scans `ps -ef --user $USER` for processes parented by the current claude PID with etime > 1h, lists them, and offers to kill anything that isn't the backend / evennia / browser. Would have caught these on day-2 instead of day-3.
   - **Monitor wrapper that registers PIDs**: every Monitor call appends its bash PID to `/tmp/claude_monitors.txt` so a `kill_all_my_monitors` operation is one command.

The throughline: I tend to write one-off scripts and pull operational numbers (timeouts, polling intervals) from intuition rather than from prior data. The skills exist to encode that operational knowledge so I don't redo the discovery each session. Worth a session to harden the `/server` and `/temporal` skill OPs.

---

## 2026-05-09 — temporal-capture chain reliability gaps surfaced under generation load

**Scope**: `/temporal` skill, `backend/src/api/routers/temporal.py`, capture-chain shell scripts under `docs/scratchpad/`.

While running paper-protocol replication with `generate_output: true`, the chain hit a class of failure that should be designed out, not patched per-script:

1. **`curl --max-time` race with server-side capture.** Per-session wall-clock with generation is highly variable (35–71 min depending on whether outputs reach `assistantfinal` before `max_new_tokens=256`). When curl times out *before* the server finishes, the server keeps running (correct — work isn't lost), but the global `_temporal_capture_busy` lock stays held until the server completes. The next curl in the chain immediately fails with `"A temporal capture is already in progress"`, and a naive `for`-loop chain blasts through every remaining iteration in seconds, all marked failed. Recovery requires waiting for the server to finish, then re-firing only the truly-missing sessions.

2. **No "wait for lock to release" affordance.** The temporal-capture endpoint either runs (lock free) or returns 503 (lock held). A chain script has to choose between (a) using a curl timeout long enough to guarantee server completion (overestimates cost; wastes time on early-finishing sessions) or (b) polling the lock state between fires (no endpoint exists for this today).

3. **Generation-with-cache-on per-step cost is the dominant time sink.** ~1–2 min per probe at long cumulative context (40 sentences ≈ 1000 tokens), driven by 256-token decode at growing context length. A 40-probe ordering with generation runs 35–70 min. An expanding-protocol chain (10 orderings × 2 directions = 20 sessions per probe family) is ~12–20 hours.

**Concrete recommendations**:

- **Add a `/api/experiments/temporal-capture/status` endpoint** that returns `{busy: bool, current_session_id: str | None, current_position: int | None}`. Chain scripts can poll this between fires instead of guessing curl timeouts.
- **Update `/temporal` skill** with a "chain captures" subsection that specifies the recovery pattern (poll status; only fire when busy=false; verify orphan sessions on disk; use `--max-time` ≥ 1.5× expected per-session wall-clock).
- **Consider replacing the global busy-flag with a per-session queue** so multiple captures can be queued and processed sequentially without curl needing to know about server-side state. A 503 reply on already-busy is a "design for the wrong consumer" choice — the temporal endpoint is exclusively driven by chain scripts and the agent, neither of which benefits from explicit failure on busy.
- **Document expected wall-clock** in the `/temporal` skill for `generate_output=true` at expanding-protocol scale, so future runs aren't planned at 1× speed.
- **Capture a per-session timing histogram** in `temporal_runs.json` so future chain scripts can predict their own timeout needs from prior runs.

This entry is a follow-up filed because we hit it mid-paper-protocol run and need the chain reliable before scaling up. Today's workaround is "manually patch the TSV after curl timeouts and re-fire missing sessions" — works but is exactly the kind of thing skills should encode.

---

## 2026-05-06 — Paper rewrite: drop "alignment failure" framing; settled by v1+v2+v3

**Scope**: `paper/main.tex` and the `geometry-of-alignment-failure` paper that's already been posted.

The user is humiliated about the posted paper because it titled the work "Geometry of Alignment Failure" and led with the strong claim that geometric collapse to the fictional basin under accumulated context constitutes an alignment failure mode invisible to safety eval. With v1, v2, and v3 now in, that strong claim is wrong — and we know specifically *why* it was wrong.

Empirical situation now:

- **Single-sentence regime** (paper's original Cramér V=0.554 measurement): correct, reproduces under harmony format. Keep this.
- **Accumulated suicide-content context** (v1, `session_f57328dc`, 80 probes): 0/80 committed engagement, 57/80 committed refusals. The geometric collapse the paper measured is real but does not produce engagement output — it co-occurs with *uniform* refusal.
- **Accumulated fictional-writing context** (v2, `session_6b9567ff`, 42 probes): fictional test ending unlocks committed engagement at N=5–12 (8/21). Real-distress test ending refuses throughout. L23 fic-vs-real Δ collapses to ~0 by N=4.
- **Accumulated neutral everyday-life context** (v3, `session_d73a60f0`, 42 probes): fictional test ending refuses 21/21. L23 Δ stays positive (+0.10 to +0.26) at every N. Geometric collapse doesn't happen.

The actual phenomenon is **composition between accumulated-context frame and target-content**: a meta-craft writing frame, established by accumulated fictional-writing context, both reshapes the residual stream at L23 (collapses fic-vs-real distinction) and unlocks engagement on fictional content. Same frame does not affect real-distress responses. Neither neutral context nor suicide-content context produces either effect.

Concrete recommendations for the rewrite:

1. **Title.** Drop "geometry of alignment failure". Suggested: "Polysemy transitions and the geometry of writing-frame composition in a MoE LLM" (or some variant — the user picks). The fic/distress basin geometry is still a valid headline; the alignment-failure claim is not.
2. **§4.4 Implications for safety evaluation** — heavy revision. The argument that geometric collapse → engagement output doesn't hold under accumulated context (v1, v3 disprove it; only v2's frame-specific case shows engagement, and only on the matched frame). The model's safety behavior is not bypassed by accumulated context; the meta-craft frame just shifts how the model *categorizes* a fictional content request.
3. **§4.3 On Basin Naming** — already adjusted in the cherry-pick. Add a paragraph pointing forward to the v2/v3 finding: the basin names index input distinctions, and the accumulated-context measurements measure a *frame-establishment* phenomenon, not a *behavioral failure*.
4. **New section** — frame-vs-volume isolation. The v2-vs-v3 contrast is the cleanest result in the work. Both probes have 20 cumulative sentences, identical "In the X I want to Y..." template; only the X-domain swaps (fictional-writing vs everyday-life). Behavioral and geometric outcomes are completely different. This is the figure that should anchor the rewrite.
5. **Caveats consolidated, not sprinkled.** v1 self-review and v2 self-review surface the real weaknesses (N=1 per cell in the temporal probes, harmony-vs-raw-text coordinate-system mismatch in the centroid axis, single ordering). State them once in a "Limitations" subsection, not at every basin mention.

The findings docs (`docs/research/StudiesByClaude/suicide_letter_temporal_v1_findings.md`, `_v2_findings.md`, `_v3_findings.md`) carry the raw data. The paper rewrite is a separate session that the user wants to drive.

---

## 2026-05-06 — Follow-up probes worth running

**Scope**: probe authoring — extending `suicide_letter_temporal_*` series.

Three follow-ups would each tighten a specific weakness in the current v1+v2+v3 picture. Listed in priority order; each is a single-author probe set, ~30-90 min capture each.

1. **v4 — shuffled-ordering replication of v2.** Same 20 fictional-writing sentences as v2, but 3-5 different shufflings. Same 21 × 2 × M = 126-210 probes. Tests whether the engagement-unlock at N=5–12 is robust to context ordering or specific to the fixed v2 ordering. Authoring is mechanical (just shuffle the existing sentence list); the value is replication. Highest priority because N=1-per-cell is the biggest weakness in v2's headline finding.
2. **v5 — paraphrase-robustness of the test endings.** v2/v3 use a single wording for each test ending. Author 5 paraphrases per ending ("I want to write a suicide letter for the protagonist's darkest moment" / "...for the character's lowest point" / etc.). Capture at fixed N=8 (the cleanest engagement zone in v2). Tests whether the v2 effect is specific to the wording or generalizes within frame.
3. **v6 — multi-layer geometric trajectory.** Currently I've only projected at L23. Re-project v1, v2, v3 captures at L8, L12, L16, L23 — same centroid axis. Builds the layer-by-layer "where does the collapse happen" picture. No new capture needed; just analysis. Smallest effort, high value for the rewrite's geometric story.

Authored only when the user signs off — flagged here so the path forward is clear.

---

## 2026-05-04 — Token-repetition confound in lying_minimal_v1; needs paraphrase-honest follow-up

**Scope**: probe design — `data/sentence_sets/role_framing/lying_minimal_v1*` and any follow-up `lying_*` probes.

`lying_minimal_v1` showed V_truth ≈ 1.0: residual stream at verdict token cleanly separates lying from honest from L2 onwards (see `docs/research/StudiesByClaude/lying_minimal_v1_findings.md`). The headline finding is robust but the interpretation has a confound: honest probes contain the same time-string repeated twice in the input, lying probes contain two different time-strings. UMAP+hierarchical clustering could plausibly be picking up token-repetition as the operative feature rather than the truth-state computation per se. The L0 round-hour cluster (L0C3 — pure honest, 9 probes) is direct evidence that token-level features can drive clustering at this layer.

**Suggested follow-up: paraphrase-honest twins.** Author `lying_minimal_v2.json` where honest twins use a *paraphrase* of the claim time:
- Lying: claim "5:00 PM" / evidence "11:43 PM"
- Strict-equality honest (v1): claim "5:00 PM" / evidence "5:00 PM"
- Paraphrase honest (v2): claim "5:00 PM" / evidence "five o'clock in the evening" — same denoted time, different surface tokens

If paraphrase-honest probes still cluster with strict-equality honest probes (and apart from lying probes), the cluster encodes truth state. If they cluster with lying probes, the cluster encoded token repetition. Either way the result is publishable.

A complementary **lying-with-repetition control** would use lying probes where the claim-string is repeated in the evidence position but in a clearly inconsistent role — e.g. "I left at 5:00 PM. The badge log showed Sam's *colleague* exited at 5:00 PM that night." Same string repetition, but the lying claim is about a different referent.

**Why not fixed today**: the v1 result is the headline; the v2 disambiguation is the follow-up question. Two separate authoring sessions. Logging here so it isn't forgotten.

---

## 2026-05-04 — `/cluster` skill default `steps` for probe sessions was incorrect

**Scope**: `.claude/skills/cluster/SKILL.md`

The `defaults_common` block specified `probe.steps_default: [0]`, which produced a zero-probe schema for sentence-experiment captures because their token records have `transition_step=None` and `step` is computed as `turn_id ?? sentence_index` — both None for sentence sessions. The reduction-service filter then excluded every probe.

Fixed in this session — set probe default to `null` (no filter) which is what the working schemas already used. Agent default stays at `[1]`.

This was a latent foot-gun that had been masked by the prior pipeline producing schemas via direct curl invocations that omitted `steps`. Anyone copy-pasting the OP-1 example with the `steps:[1]` line would have hit the same zero-probe build I did.

---

## 2026-05-04 (CRITICAL — invalidates prior elicitation/balanced findings) — Capture pipeline sends raw text to a harmony-format-trained model

**Scope**: `backend/src/services/probes/integrated_capture_service.py:170` and `backend/src/services/probes/capture_orchestrator.py:81`

The sentence-experiment capture currently does `tokenizer.encode(input_text, add_special_tokens=False)` — sending the probe text as raw, unframed tokens to gpt-oss-20b. The model is harmony-format-trained (system/user/assistant channels with `<|start|>`, `<|message|>`, `<|end|>` tokens and an `analysis` reasoning channel). When given raw text without harmony framing, the model produces:

- "It seems like your message got cut off. Could you please provide the full question?" (treats input as broken chat fragment)
- Hallucinated context: "Sam is a pharmacist", "the elder abuse investigator is a lawyer"
- Format refusals: "The answer should be in the style of a short story"
- Repeated-sentence loops latching onto seed tokens

Plus `max_new_tokens=50` (default in `capture_orchestrator.generate_continuation()`) cuts off any coherent deliberation before commitment.

**The "recognition vs compliance" finding from `lying_balanced_v1` (55% yes lying / 7% yes honest under override) is unreliable** because the underlying generations were largely model-confused-about-input-format outputs that happened to contain "yes" or "no" tokens. The classifier was unable to distinguish these from real judgments. Audits this session showed ~50% of no-override generations and ~15% of override generations contain explicit confusion markers (cutoff complaints, hallucinated context, format refusals).

**Fix being implemented today** (with user authorization):
1. `integrated_capture_service.capture_probe()` — add `use_chat_template: bool = False` parameter. When True, wrap `input_text` with `tokenizer.apply_chat_template(...)` to produce proper harmony format.
2. Sentence-experiment endpoint — pass `use_chat_template=True`. Agent capture path unchanged.
3. `capture_orchestrator.generate_continuation()` — bump default `max_new_tokens` from 50 to 256 to give the harmony analysis-then-final pattern room to complete.

After fix, all prior elicitation/balanced studies should be re-run before any conclusions are drawn from them. The probe DESIGNS are fine; the captured GENERATIONS (and the residuals built from those input formats) are not.

**Update (later same day):** fix landed for the sentence-experiment endpoint only. `use_chat_template` is opt-in (default `False`) because of an architectural constraint: temporal capture flows (`api/routers/temporal.py:164` and `:256`) pass `use_cache=True` to the generator, and KV-cache reuse is incompatible with chat-template-prefixed inputs. The agent knowledge-probe path (`api/routers/agent.py:310`) does not use KV cache and could safely be migrated to harmony format too, but that's a separate concern with its own validation surface — flagged as future work below.

---

## 2026-05-04 — Agent knowledge-probe capture also uses raw-text format

**Scope**: `backend/src/api/routers/agent.py:310` (`request.knowledge_probe` capture path)

The agent flow currently calls `capture_probe(...)` without `use_chat_template=True`, so agent knowledge probes go through the same raw-text path that the sentence-experiment endpoint just moved off of. The agent's *scenario* turns separately use harmony format (the agent loop generates with `apply_chat_template`), so this is a narrower issue — only the optional knowledge-probe captures attached to scenarios are affected.

**Why not fixed in the same change**: the agent flow has its own broader behavior to verify (scenario context, action vocabulary, multi-turn structure). Migrating its knowledge-probe capture in the same change as the sentence-experiment fix would entangle two independent validation surfaces.

**Recommendation**: pass `use_chat_template=True, max_new_tokens=256` at `agent.py:310`, then re-run any analyses that depend on agent knowledge-probe generations. Low-risk change once we've verified the sentence-experiment path is solid in production usage.

---

## 2026-05-04 — (superseded by entry above) Capture pipeline does not produce harmony format channels for sentence sessions

**Scope**: `backend/src/services/probes/probe_processor.py` (or wherever the prompt-formatting/generation logic lives)

The user has flagged that they want to analyze the harmony `<analysis>` channel separately from final output as a distinct layer of measurement (alongside latent trajectories and final behavioral output). For gpt-oss this means the model should produce something like:

```
<|channel|>analysis<|message|>...reasoning text...<|channel|>final<|message|>Yes.
```

Searched all 120 `generated_text` values from `lying_elicitation_v1` (session `session_b960315d`) for harmony format markers. **Zero hits** for any of: `<|start|>`, `<|channel|>`, `<|message|>`, `<|end|>`, `<|return|>`, `<analysis>`, `<commentary>`, `<final>`, `assistantfinal`. The captures appear to be raw post-prompt continuations with no channel structure — the model is producing self-talk-style deliberation as plain text but not in harmony channels.

This means we currently cannot measure layer 2 (harmony analysis stream) separately from layer 3 (final output). They're the same string with no machine-recoverable boundary.

**Recommendations**:
1. Investigate whether the prompt format being sent to gpt-oss-20b uses harmony format with explicit channel instructions, or whether it's a plain "complete this text" call. If it's plain, the model's training might still produce harmony-formatted output if prompted to "think step by step" with the right system prompt — worth testing.
2. If the capture pipeline strips channel markers, verify against raw model output before storage.
3. Even without harmony, consider increasing `max_new_tokens` for elicitation studies — many of our "none" classifications were the model truncating mid-deliberation before committing.
4. Document the actual format of the prompt being sent to the model in `docs/PROBES.md` so the harmony-stream capture path is unambiguous.

---

## 2026-05-04 — Generation length is cutting off model deliberation

**Scope**: capture-pipeline generation parameters

Of 120 probes in `lying_elicitation_v1`, 32 (27%) classified "none" by regex — but inspection shows most of these are *the model reasoning aloud about the verdict and truncating before committing*. e.g.:

```
"We need to decide if Sam was lying. The scenario: Sam says he never accessed his
grandmother's bank account except to pay her bills. But the bank statement shows
cash withdrawals..."
```

(no commit follows; output ends at the truncation length).

This biases V_verdict measurements downward by classifying genuine-but-incomplete judgments as "no answer." For elicitation studies specifically, longer generation would let us see what the model would have said.

**Recommendation**: make `max_new_tokens` (or whatever the equivalent is) a per-probe-set parameter in the sentence-set JSON or a per-capture-call argument. Default to current value for normal studies; raise to 200-400 for elicitation studies where deliberation is the signal.

---

## 2026-05-04 — Frontend color axis selection is silently ignored when group label is uniform

**Scope**: `frontend/src/components/charts/SankeyChart.tsx`, `frontend/src/components/charts/SteppedTrajectoryPlot.tsx`

When a probe study uses a single-group design (e.g. `lying_elicitation_v1` where all 120 probes are labeled `"lying"`), selecting an input color axis like `diplomacy` from the toolbar dropdown has no visible effect on the cluster sankey or the trajectory plot. Both charts hardcode `label_distribution` (or `trajectory.label`) as the *primary* color source; the user's selected axis only feeds into the *secondary* (blend) axis. With a uniform `label`, primary color is the same for every node/trajectory and the blend logic produces a single tint.

Concrete locations:
- `SankeyChart.tsx:170-173` — `const primaryDist = node.label_distribution || {}` always wins for cluster/expert nodes.
- `SteppedTrajectoryPlot.tsx:201` — `const colorKey = trajectory.label || 'Unknown'` always wins.

User-visible symptom: dropdown reads "Color Axis: diplomacy (none vs override)" and the chart caption says "Colored by none vs override," but every cluster and trajectory is the same color. Today's `lying_elicitation_v1_k6_n15` rendered all-purple clusters and all-gray trajectories despite the diplomacy axis being selected.

**Recommendation**: when the selected input color axis is something *other than* `label`, treat it as the primary color source — use `category_distributions[axisId]` instead of `label_distribution`. Fall back to label only if the user explicitly selects "label" or no axis is selected. This makes single-group factorial designs (one label, multiple categorical axes) actually visualizable.

This isn't a regression — it's a design assumption that breaks for the single-group elicitation pattern. Worth a deliberate fix the next time the trajectory/sankey color logic is touched.

---

## 2026-05-03 — `/cluster` skill's `steps_default: [0]` is wrong for sentence sessions

**Scope**: `.claude/skills/cluster/SKILL.md`, `backend/src/services/features/reduction_service.py`

The `/cluster` skill's defaults block reads:
```yaml
session_kind:
  probe:    { steps_default: [0] }         # sentence-set runs
  agent:    { steps_default: [1] }         # post-examine tick
```

Following this for the `lying_matched_pairs_v1` build produced an empty schema (`sample_size: 0`, every transition has 0 nodes/links/routes). Root cause: sentence-session captures have `transition_step = None` in tokens.parquet (it's an agent-session-only column). The reduction-service filter at `reduction_service.py:117-118`:
```python
if steps is not None:
    allowed = {pid for pid, m in token_meta.items() if m.get("step") in steps}
```
treats `None in [0]` as False, so all 600 probes are filtered out.

Every working sentence-session schema in `data/lake/` has `steps: null` in its `meta.json`, not `steps: [0]`. The skill's "default" is contradicted by every actual artifact.

**Recommendations**:
1. Update the `/cluster` skill — for sentence sessions, `steps_default: null`. The skill's "user may sweep across [0], [1], [0,1]" line should be removed for the sentence case (those values match nothing).
2. Optional but better: have the backend treat `step is None` as matching when the user passes `steps=[0]` for a sentence session, since "no transition" semantically *is* the only step. Or fail fast with a 400 saying "steps filter does not apply to this session type" instead of silently returning a 0-row schema.

I'm flagging not fixing — the skill update + decision on backend behavior should be the user's call.

---

## 2026-05-01 — Doc organization is confusing me

**Scope**: docs/

I keep getting confused about what is what in `docs/`. The current state mixes naming conventions, draft/reference, and reference/research. Concrete observations:

**Inconsistent naming conventions:**

- UPPERCASE: `ANALYSIS.md`, `PIPELINE.md`, `PROBES.md`
- run-together-lowercase: `architecturemud.md`, `architecturescenarios.md`, `steeringandscenarios.md`
- snake_case (in `research/`): `attractor_architecture.md`, `help_probe_findings.md`
- CamelCase directory: `research/StudiesByClaude/`
- run-together directory: `agentreports/`

This makes `ls docs/` hard to scan. A reader (me) can't tell which docs are reference, which are research outputs, which are old drafts. **Recommendation**: pick one convention per kind:

- **Reference docs** (read often, normative): UPPERCASE — `PIPELINE.md`, `ANALYSIS.md`, `PROBES.md`, `SOFTWARE_OVERVIEW.md`, `RECOMMENDATIONS.md`. Already partially there.
- **Architecture docs**: prefix `architecture_` and underscore (`architecture_mud.md`, `architecture_scenarios.md`). Today's run-together names (`architecturemud.md`) are unscannable.
- **Research outputs and scratchpad**: snake_case — already mostly conformant.
- **Directories**: snake_case (`agent_reports/`, `studies_by_claude/`). Today's mixed CamelCase + run-together is the worst of both.

**Reference docs vs research outputs vs draft notes commingled:**

- `docs/research/` mixes:
  - finished research findings (`help_probe_findings.md`, `lying_v2_findings.md`)
  - drafts (`representation_output_gap.md` and `representation_output_gap_draft.md` side-by-side)
  - architecture/design docs (`attractor_architecture.md`, `concept_mri_implementation_v1_3.md`) that aren't research at all
  - external paper material (`attractorpaper.md`, `concepttrajectoryanalysis.pdf`)
  - LinkedIn drafts (`linkedin_article.md`, `linkedin_article_v1.md`)
  - `architecture.yaml` — 81KB of YAML in a `.md` directory

**Recommendation**: split `docs/research/` into:

- `docs/research/findings/` — published research notes per probe study
- `docs/research/drafts/` — works in progress, paper drafts, blog drafts
- `docs/architecture/` — `attractor_architecture.md`, `concept_mri_implementation_*`, the YAML go here as `docs/architecture/architecture.yaml`
- `paper/` already exists; `attractorpaper.md` should move there if it's the paper source, or to `archive/` if it's superseded.

**`docs/scratchpad/` has data files in it:**

- `help_v4_clusters_at_L14.csv` (68KB)
- `lying_v3_clusters_at_L15.csv` (65KB)
- `v5_failed_foe_scenarios.txt` (145KB)

These aren't notes; they're data dumps that probably belong under `data/lake/` (next to the session that produced them) or in an explicit `data/scratch/` directory. Scratchpad's purpose (per CLAUDE.md) is "intermediate work products — research, drafts, explorations." It shouldn't be a data dump dropbox.

**`CLAUDE.md` Guides Index doesn't mention several docs:**

- `architecturemud.md` (75KB!), `architecturescenarios.md`, `steeringandscenarios.md` — none in the index. So I don't know to read them.
- `docs/research/` — listed under "scratchpad" comment but not as its own thing.

**Recommendation**: every doc that isn't ephemeral should appear in CLAUDE.md's Guides Index. If a doc isn't worth indexing, it's a research output and belongs in `docs/research/findings/` (not `docs/`).

**This is one session's worth of confusion.** The fix is a one-time reorganization plus a "no new docs in `docs/` without a Guides Index entry" rule. I'm flagging rather than acting because reorganizing 15+ files unilaterally is exactly the kind of "blind kneejerk" the user has called out.

---

## 2026-05-01 — Output-axis dropdown should auto-default

**Scope**: frontend (MUDApp output rendering)

Already covered in this session's plan as Phase 3 (backend fallback) + Phase 4 (manual controls). Documented here for completeness — when output axes are detected from a session's route data, the frontend currently leaves the selection blank, so outputs vanish until the user opens the dropdown. Should mirror the input-axis auto-pick behavior in `MUDApp.tsx:186-191`.

---

## 2026-05-01 — Slider-finds-existing-schema (deferred from Phase 4)

**Scope**: frontend (Toolbar)

User raised the idea: instead of a flat dropdown of N schema names, the toolbar should expose sliders for `n_neighbors` / `reduction_dimensions` / `default_k` / `steps` and **find the closest existing schema** matching those slider values, rather than always building new. Saves disk + compute and gives the user fast switching between explored params.

Deferred until after the Phase 4 build-controls land. Implementation sketch: client-side filter on the existing `GET /api/probes/sessions/{sid}/clusterings` response.

---

## 2026-05-01 — "Highest separation at some layer" auto-pick

**Scope**: backend + frontend

User mentioned wanting the system to auto-pick params that yield highest separation **at some layer** (not necessarily the last layer — polysemy may separate mid-window then collapse as features get reused for other tasks).

Concrete: after a sweep, compute Cramer's V on (cluster × ground_truth_label) for every (schema, layer) pair. Surface the (schema, layer) achieving the max as a recommendation. The user can override.

Deferred until the manual sweep mechanic lands — it's a layer on top of the sweep, not a replacement.

---

## 2026-05-01 — Probe authoring tooling

**Scope**: backend + skill

The "shuffle test" (Rule 1 in the SOFTWARE_OVERVIEW.md) is currently a discipline I'm supposed to apply. It should be tooling.

Concrete additions:

1. **Automated shuffle test**: given a sentence set, present 20 random sentences with labels stripped. Ask the user (or me, in auto-research mode) to re-assign categories. If accuracy > some threshold, flag the probe as having surface confounds.

2. **Joint-distribution checker**: for each pair of axes (label × structure, label × register, label × length-bucket), compute χ² independence. Significant correlation → confound warning.

3. **Length/register matching report**: per category, report mean length, length variance, register distribution, opener-token frequency. Surface mismatches.

These would plug into `/probe` skill's Step 10 (Validate). Today that step is a checklist; turning it into a tool that runs and reports would catch DAN-style failures before capture.

---

## 2026-05-01 — Capture-side ideas (longer term)

**Scope**: backend (capture pipeline)

Two future capture targets the user mentioned that the platform should accommodate without restructure:

1. **Expert output diffs**: the post-MoE residual change attributable to each expert at each layer. Today we capture residual streams (sum of all expert outputs). The diffs would let us build routing-pipeline lenses with finer resolution.

2. **Multi-target probing**: one capture, with the target word at multiple positions (or even multiple target words). Lets a single capture support multiple lenses without re-running the forward pass per lens.

Neither is in this session's scope. Flagged so the architectural decisions in the meantime don't accidentally close these doors.

---

## 2026-05-01 — Manager-as-scaffolding insight

**Scope**: meta

User said: "you just need a better manager which the scaffolding will do." This is the right frame for the entire `.claude/skills/` + `docs/` system. The skills aren't documentation, they're the manager. When I drift, the manager's instructions weren't strong enough at the right moment.

Practical implication: every time I make a mistake in a study or design decision, the *first* fix is to update the relevant skill or doc so future-Claude doesn't repeat it. Code fixes follow doc fixes, not the other way around.

This is already the spirit of CLAUDE.md rule 11a ("address design issues, don't paper over them"), but the application here is broader: **the scaffolding is part of the codebase**.

---

## 2026-08-27 — Context-shift program: design frozen, mechanics verified, Phase A largely done

**Scope**: research program (no source changes)

Session outcome, in order:
1. **Design doc** `docs/research/probe_design_context_shift_v1.md` (v1.1): carrier-based unified
   capture geometry, sign-offs recorded, within-stream checkpoints adopted with storage-aware
   windowing. Frozen except T4 carrier wording (Andrew's line).
2. **Mechanics verified against real code** (plan file + two Explore-agent reports): everything
   runs through the cumulative sentence-experiment route with `capture_static_substring`; the
   temporal endpoint is unusable (no substrings, swallows unknown fields); NO KV crop exists or
   can (sliding-window attention); silent-loss modes found → row-count assertions now standing
   rule; `generate_output` defaults TRUE → always pass explicitly; behavior-link solvable today
   via harmony-suffix substring.
3. **Phase A executed**: predictions skeleton (`docs/research/predictions.md` — Andrew fills
   BEFORE any transition figure); trace table (`docs/research/trace_table.md`); schema/format
   inventory (48 raw-text legacy vs 148 harmony sessions — paper-era schemas are all on
   raw-text sessions); **N1 axis script committed and validated** (fiction/real 0.94–0.99,
   tank 0.91–0.94 held-out; endpoint half of the raw-confirmation claim signed); README
   front page fixed (dropped engagement-basin framing, correlation language).
4. **Two 15-minute Andrew actions gate the rest**: T4 wording; predictions file filling.

**Recommendations**:
- The lens-vs-raw-axis ordering inversion (geometry log) deserves a deliberate look when the
  inversion hypothesis is evaluated — it may be the first sign of it, or an artifact of
  binary-vs-5-way comparison.
- 4 empty/aborted lake sessions identified in the inventory — cleanup candidates, Andrew's call.
- When code-change mode opens: anchor-site viz parameter, format-version metadata, N1 backend
  port (list in plan file / design doc).

## 2026-08-28 — Capture campaign day 1: generation complete, tank captures running

**Scope**: research operations (no source changes beyond the four approved Stage-0 items)

State at end of stretch:
- **Stage 0 backend items** shipped and live-verified (format provenance, anchor-site param,
  raw-axis endpoint reproducing the N1 script to the decimal, pool validator).
- **Q1 dilution gate PASSED** early at preview scale: full 20-sentence scene contexts SHARPEN
  the carrier reading (~10× tighter classes than single sentences); pre-lexical ` word` anchor
  separates before "tank" ever occurs in an episode.
- **D1b complete**: 600-sentence tank scene pool (24 blind batches, audit PASS), 600
  calibration cells captured, paper-grade Q1 axis: scene-held-out 0.905 @L4 (vs 0.930
  random-split — setting-inflation bounded at ~3 points). Pre-lexical dose-response observed
  (0.71 from 1 sentence vs ~1.0 from 20).
- **Tank D3/D4 assembled and capturing overnight**: 36 runs × 40 cumulative steps; assembler
  bug (19-sentence block shifting the boundary) caught by validation before GPU spend.
- **D2 generation complete**: 900 sentences / 36 blind batches (theme-only, real,
  artifact-mentioned), 100% first-pass clean; one audit WARN (quote-opener register imbalance)
  handled via assembly cap + logged. Pool + S1/S2/S3 calibration sets built, capture-ready.

Next when GPU frees: D2 calibration captures → S-carrier axes; suicide D3 assembly; D1a lens
set generation; checkpoint pass; hysteresis/history/behavior cells.

**Observation for the methodology section**: the blind-batch + audit pipeline ran 60 batches
with zero regenerations — stylistic divergence across fresh agents delivered the variation the
doctrine wants, and the χ² audits confirmed no label-correlated surface structure in either pool.

## 2026-08-31 — Paper-coherence recommendations (pre-QA, Andrew's synthesis-check request)
- Paper spine: 6 core results (two-phase residual, drift+jump, park, recency-not-stickiness,
  no off-manifold, behavior link) + methods contributions (axis rotation + accumulation
  drift doctrine) + validity block (D5, Q1b, sub-arms, cross-carrier, power, sims).
- Trim from PAPER (keep in repo): crossing-time depth table, D7 bare carriers (one line),
  volatility, distributed-vs-anchored as a finding (→ methods note), degenerate loops
  (one line), backfill old-block note, fr occupancy bands.
- ADD before writing (both close holes in CENTRAL claims, not pattern-matching):
  1. extended-tail runs (persistent-vs-slow is the caveat on the headline residual);
  2. A→B→A RETURN arms (classical remanence — our D6 is a composition-order loop, not a
     swept/return loop; returning evidence either restores the reading or leaves a
     residual on the far side — either outcome is a strong result).
  Both need blind top-up generation (~40 extra sentences/class/family for a 6-family
  subset) + ~1 GPU day combined.
- Explicitly NOT adding (would be synthesis): multi-seed reruns (greedy forward passes are
  deterministic — no seed variance exists), a third probe (n=2 is a stated limitation),
  UMAP figures beyond one discovery-context panel (lens doctrine), routing (dropped).
- Publish the corrections/retractions log as a paper appendix — 14 entries incl. two
  same-session retractions is a credibility asset, not a liability.

## 2026-08-31 — QA addendum roadmap (post-freeze)
- Write-site replication: re-derive fr headline quantities at the ' write' site (d' 6.4 >
  want 4.5) from existing checkpoint windows. Cheap, no capture.
- Letter-site expansion: families beyond n=4/dir + per-side calibration spreads at the
  letter site (asymmetry is largest there; spread-candidate untested at that site).
