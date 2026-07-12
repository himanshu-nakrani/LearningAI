# Module 16 — Models, Agent Config, Runtime, Events & Context

**Time:** 3–4 hours · **Docs:** [Models](https://adk.dev/agents/models/) · [Agent config](https://adk.dev/agents/config/) · [About ADK](https://adk.dev/get-started/about/) · [Runtime](https://adk.dev/runtime/)

## Objectives

- Choose model integration style (string registry vs connector)  
- Configure multi-provider setups (Gemini, Claude, LiteLLM, Ollama, vLLM)  
- Author agents via **Agent Config** (YAML) where supported  
- Explain Runner, Events, InvocationContext  
- Tune context management  

---

## 1. Models

### Direct string / registry

```python
LlmAgent(model="gemini-flash-latest", ...)
# Vertex / Agent Platform endpoint resource strings also supported
```

### Connectors

| Connector | Use |
|-----------|-----|
| LiteLLM | Many hosted providers behind one interface |
| Ollama | Local models |
| vLLM | Self-hosted high throughput |
| Apigee LLM | Enterprise API management front door |
| LiteRT-LM | On-device oriented stacks |

### Model routing

Dynamic selection + failover on error — see [model routing](https://adk.dev/agents/models/routing/).

### Auth patterns

- `GOOGLE_API_KEY` — AI Studio  
- `GOOGLE_GENAI_USE_VERTEXAI` + ADC — Vertex  
- Provider-specific keys for LiteLLM  

---

## 2. Agent Config (YAML)

ADK can author workflows via config files (tools subset supported: google_search, AgentTool, LongRunningFunctionTool, McpToolset, …).

Use cases:

- Non-Python authoring  
- Declarative multi-agent graphs  
- Faster iteration for product  

Study: [Agent Config](https://adk.dev/agents/config/) for schema + CLI run.

---

## 3. Runtime core objects

### Runner

Orchestrates:

- Load session  
- Invoke agent(s)  
- Append events  
- Apply state/artifact deltas  
- Stream results to client  

Variants: `Runner`, `InMemoryRunner`.

### Event

Atomic history unit: user message, model message, function call/response, partials, actions (state_delta, artifact_delta, transfer, escalate).

### InvocationContext

Per-run bag of services + session + agent references used by tools/callbacks.

### Services on Runner

```python
Runner(
  agent=...,
  app_name=...,
  session_service=...,
  memory_service=...,      # optional
  artifact_service=...,    # optional
  plugins=[...],           # optional
)
```

---

## 4. Context management (ADK differentiator)

ADK treats context like managed source code:

- Filter irrelevant events  
- Summarize older turns  
- Lazy-load artifacts  
- Track token usage  

Plugins like **Context Filter** and instruction templating help keep prompts lean.

Design rules:

1. Prefer state keys over pasting huge blobs into instructions  
2. Put files in artifacts  
3. Use `include_contents='none'` for pure pipeline steps  
4. Cap tool result sizes  

---

## 5. CLI surface (full)

| Command | Purpose |
|---------|---------|
| `adk create` | Scaffold |
| `adk run` | CLI chat |
| `adk web` | Dev UI + traces + eval |
| `adk api_server` | HTTP API for agents |
| `adk eval` | Evaluation |
| `adk conformance` | Golden replay tests |
| `adk deploy cloud_run` | Cloud Run |
| `adk deploy agent_engine` | Agent Runtime |

Always run `adk --help` and subcommand `--help` for your installed version.

---

## 6. Exercises

1. Compare Flash vs Pro for router vs writer in a cost table.  
2. Draft a YAML Agent Config skeleton for the travel team.  
3. Log every Event type during one `run_async` turn.  
4. Propose a context budget: max history turns, max tool JSON bytes.  

---

## Checkpoint

1. String model vs LiteLlm wrapper — when each?  
2. What four services can a Runner wire?  
3. Name two context-saving techniques.  

## Next

→ Capstone [Module 09](../09-capstone/README.md) or revisit [ADK_COVERAGE.md](../../ADK_COVERAGE.md)
