# Module 06 — Advanced Patterns

**Time:** 3–4 hours · **Difficulty:** Advanced

## Objectives

- Enforce structured outputs with Pydantic `output_schema`
- Store results with `output_key`
- Tune generation config (temperature, tokens, safety)
- Use planners for multi-step reasoning
- Introduce callbacks, artifacts, and code execution
- Control history with `include_contents`

---

## 1. Structured I/O

When downstream systems need JSON:

```python
from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import LlmAgent

class CapitalOutput(BaseModel):
    capital: str = Field(description="Capital city name")
    country: str = Field(description="Country name")

agent = LlmAgent(
    ...,
    instruction='Respond ONLY as JSON matching the schema.',
    output_schema=CapitalOutput,
    output_key="capital_info",
)
```

**Caveat:** Combining `output_schema` with tools is model-dependent. Prefer a separate formatting sub-agent when tools + strict JSON conflict.

---

## 2. Generation config

```python
from google.genai import types

agent = LlmAgent(
    ...,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=512,
    ),
)
```

| Setting | Guidance |
|---------|----------|
| Low temperature | Ops agents, routers, extractors |
| Higher temperature | Brainstorming, creative drafts |
| Token caps | Cost / latency control |

---

## 3. Planners

| Planner | Role |
|---------|------|
| `BuiltInPlanner` | Uses model thinking / budget (Gemini thinking) |
| `PlanReActPlanner` | Forces plan → action → reason → answer structure |

Use planners when tasks need deliberate multi-step tool use.

---

## 4. Callbacks

Callbacks hook the lifecycle without changing core agent logic:

- Log every tool call
- Redact PII before model calls
- Metrics / tracing
- Guardrail rejects

See official [Callbacks](https://adk.dev/callbacks/) docs for exact signatures in your ADK version.

Pattern:

```text
before_model → model → after_model
before_tool  → tool  → after_tool
```

---

## 5. Code execution

Attach `BuiltInCodeExecutor` (or tools) so the model can run Python for math/analysis. Always sandbox in production.

---

## 6. Context controls

```python
LlmAgent(..., include_contents="none")  # stateless step
```

Useful for pure transformers in a pipeline that should ignore chat banter.

---

## 7. Lab — Structured capital agent

Package: `modules/06-advanced/structured_capital_agent`

```bash
adk run modules/06-advanced/structured_capital_agent
```

**Try:**

```
France
What is the capital of Japan?
```

Inspect that the model returns schema-valid JSON (and state gets `capital_info` when using runners that expose state).

### Exercises

1. Extend schema with `population_estimate: int | None`.
2. Add a second pipeline agent that turns `capital_info` into a tourist blurb (sequential).
3. Add `generate_content_config` with `temperature=0`.
4. **Stretch:** Implement a before-tool callback that logs tool name + args.

### Lab B — Planning agent

Package: `modules/06-advanced/planning_agent`

```bash
adk run modules/06-advanced/planning_agent
```

Ask a multi-hop question requiring both tools.

---

## Checkpoint

1. When should you avoid pairing tools with `output_schema`?
2. What does `output_key` write to?
3. Why lower temperature for a billing router agent?
4. Name one production use for callbacks.

---

## Next

→ [Module 07 — Evaluation](../07-evaluation/README.md)
