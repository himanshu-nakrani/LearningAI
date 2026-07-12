# Module 25 — Ecosystem: A2A, Multi-Model, Agent Config, MCP Server, Optimization

**Time:** 3–4 hours · Survey + mini-labs

## 1. Agent-to-Agent (A2A) — `google.adk.a2a`

ADK includes converters and executors for **A2A protocol** (cross-process agent calls).

Study paths in the package:

- `a2a/executor/a2a_agent_executor.py`  
- `a2a/converters/*`  
- long-running function bridges  

**Lab (design):** Draw two services — Research Agent and Writer Agent — communicating over A2A with auth headers. List failure modes (timeout, partial results).

---

## 2. Multi-model (LiteLLM / Ollama)

ADK models layer supports connectors (see [Models](https://adk.dev/agents/models/)).

```bash
# Optional local:
# ollama pull llama3.2
# pip install litellm
python modules/25-ecosystem/multi_model/show_model_options.py
```

**Exercise:** Cost table — router on Flash, writer on Pro/local.

---

## 3. Agent Config (YAML)

Declarative authoring for some workflows ([Agent Config docs](https://adk.dev/agents/config/)).

**Exercise:** Write a YAML sketch for the Module 05 sequential research pipeline (even if not executed).

---

## 4. Expose ADK tools as MCP server

Reverse of Module 13: wrap ADK `FunctionTool`s behind an MCP stdio server so Claude Desktop / other MCP clients can call them.

Skeleton: `mcp_server_export/adk_mcp_server.py`

```bash
python modules/25-ecosystem/mcp_server_export/adk_mcp_server.py
# (listens on stdio — run under an MCP host)
```

---

## 5. Optimization — `google.adk.optimization`

Prompt/agent optimizers and eval samplers (GEPA-style). Use when you have eval sets and want automated instruction search.

**Exercise:** Define a success metric for the weather agent and outline an optimization loop (sample → score → mutate instruction).

---

## 6. Apps & compaction — `google.adk.apps`

`App` object packages agent + plugins; event summarizers compact long histories.

**Exercise:** When would you enable compaction for a support bot (token $, loss of detail)?

---

## Checkpoint

1. A2A vs sub_agents in one process?  
2. Why expose tools via MCP server?  
3. Risk of automated prompt optimization without eval gates?  

## Next

→ Capstone solution · CI · [ADK_COVERAGE.md](../../ADK_COVERAGE.md)
