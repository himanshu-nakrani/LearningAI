# Module 07 — Evaluation & Testing

**Time:** 2–3 hours · **Difficulty:** Intermediate → Advanced

## Objectives

- Explain why agent eval differs from unit tests
- Evaluate **trajectory** (tool path) and **final response**
- Author eval cases (`.test.json` / evalsets)
- Run evaluations via CLI, pytest, and Dev UI
- Pick metrics for CI vs qualitative review

---

## 1. Why classic tests are not enough

LLMs are stochastic. The same prompt can:

- Call tools in slightly different order
- Phrase answers differently
- Occasionally skip a tool

So we evaluate:

1. **Trajectory / tool use** — Did it call the right tools with right args?
2. **Final response quality** — Is the answer correct, safe, useful?

Automation still pays off: catch regressions before deploy.

---

## 2. Metrics (ADK built-ins)

| Metric | What it checks | Good for |
|--------|----------------|----------|
| `tool_trajectory_avg_score` | Exact tool trajectory match | CI / regression |
| `response_match_score` | ROUGE-like overlap vs reference | Fast smoke tests |
| `final_response_match_v2` | LLM semantic match | Softer wording |
| Rubric-based metrics | Custom quality attributes | Product polish |
| `hallucinations_v1` | Groundedness | RAG / tool agents |
| `safety_v1` | Harmlessness | User-facing bots |
| Multi-turn metrics | Goal completion over dialogue | Support agents |

Defaults often require **perfect tool trajectory** and ~0.8 response match.

Config example `test_config.json`:

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

---

## 3. Eval case shape

Each turn can include:

- `user_content` — query
- `intermediate_data.tool_uses` — expected tool calls
- `intermediate_data.intermediate_responses` — multi-agent steps
- `final_response` — reference answer
- `session_input` — app/user/state seed

See formal schemas in ADK (`EvalSet`, `EvalCase`).

---

## 4. How to run evals

### Dev UI

```bash
adk web modules/02-first-agent --port 8000
```

Chat → **Eval** tab → save session → run evaluation → inspect Pass/Fail + Trace.

### CLI

```bash
adk eval \
  modules/03-tools/weather_sentiment_agent \
  modules/07-evaluation/evals/weather_basic.evalset.json \
  --print_detailed_results
```

### pytest

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_weather_agent():
    await AgentEvaluator.evaluate(
        agent_module="weather_sentiment_agent",
        eval_dataset_file_path_or_dir="path/to/file.test.json",
    )
```

### Conformance tests

`adk conformance` records golden baselines and detects behavioral drift — excellent for CI gates.

---

## 5. Lab — Eval set for weather agent

Files live under `modules/07-evaluation/evals/`.

1. Read `weather_basic.evalset.json`
2. Run:

```bash
adk eval \
  modules/03-tools/weather_sentiment_agent \
  modules/07-evaluation/evals/weather_basic.evalset.json \
  --print_detailed_results
```

3. Intentionally break `get_weather_report` (rename city key) and re-run — expect trajectory failure.

### Exercises

1. Add an eval case for **Paris** sunny weather.
2. Add a case expecting `analyze_sentiment` after negative feedback.
3. Lower `response_match_score` to 0.5 and observe fewer failures on wording.
4. Export a session from Dev UI into a new eval case.

---

## 6. Eval design tips

| Tip | Why |
|-----|-----|
| Start with tool trajectory | Catches logic bugs fast |
| Keep unit evals short (1–3 turns) | Fast CI |
| Use multi-turn evalsets for journeys | Real user paths |
| Separate flaky creative agents | Don't block deploys on poetry |
| Version eval sets with code | Reproducible quality |

---

## 7. CI sketch

```yaml
# conceptual GitHub Actions step
- run: pip install -r requirements.txt
- run: adk eval modules/03-tools/weather_sentiment_agent modules/07-evaluation/evals/weather_basic.evalset.json
- run: pytest modules/07-evaluation/tests -q
```

Store API keys in CI secrets. Prefer cheaper models for eval volume.

---

## 8. Full criteria catalog (reference)

| Criteria | Use |
|----------|-----|
| `tool_trajectory_avg_score` | Exact tool path (CI) |
| `response_match_score` | Fast lexical similarity |
| `final_response_match_v2` | Semantic LLM judge vs reference |
| `rubric_based_final_response_quality_v1` | Custom quality attributes |
| `rubric_based_tool_use_quality_v1` | Tool reasoning quality |
| `hallucinations_v1` | Groundedness vs context |
| `safety_v1` | Harmlessness |
| `per_turn_user_simulator_quality_v1` | Simulator quality |
| `multi_turn_task_success_v1` | Goal completion |
| `multi_turn_trajectory_quality_v1` | Path efficiency |
| `multi_turn_tool_use_quality_v1` | Multi-turn tool quality |

**User simulation:** dynamic user turns when fixed scripts are too brittle (see eval user-sim docs).

**Conformance testing:**

```bash
adk conformance create tests/category/case
adk conformance test
adk conformance test --generate_report --report_dir=reports
```

Records golden LLM/tool interactions; fails CI on behavioral drift.

**Programmatic:**

```python
await AgentEvaluator.evaluate(
    agent_module="home_automation_agent",
    eval_dataset_file_path_or_dir="tests/.../case.test.json",
)
```

---

## Checkpoint

1. Name two layers of agent evaluation.
2. Why might `response_match_score` fail even when the answer is correct?
3. What metric is best for “must call refund tool before apologizing”?
4. When would you use user simulation instead of fixed prompts?

---

## Next

→ [Module 08 — Deployment & Production](../08-deployment/README.md)
