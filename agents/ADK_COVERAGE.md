# Google ADK — Complete Coverage Matrix

This course maps **every major ADK surface** documented at [adk.dev](https://adk.dev/) (Python-first, 2026). Use this as a checklist that nothing important is skipped.

**Languages:** Python (labs) · TypeScript / Go / Java / Kotlin (concepts + doc pointers)  
**Version focus:** ADK Python current + ADK 2.0 graph/workflow notes where marked

---

## Coverage legend

| Status | Meaning |
|--------|---------|
| ✅ Lab | Runnable package in this repo |
| 📘 Deep lesson | Full module README with API detail |
| 🧭 Pointer | Official docs + design guidance (env/billing dependent) |

---

## A. Core primitives

| Topic | Status | Where |
|-------|--------|-------|
| Agent / LlmAgent | ✅ + 📘 | M02, M06 |
| name, description, model, instruction | ✅ | M02 |
| tools list | ✅ | M02–M03 |
| sub_agents hierarchy | ✅ | M05 |
| global_instruction | 📘 | M06, M12 |
| generate_content_config | ✅ | M06 |
| input_schema / output_schema / output_key | ✅ | M06 |
| include_contents | ✅ | M05 loop, M06 |
| planner (BuiltIn / PlanReAct) | ✅ | M06 |
| code_executor | 📘 + pattern | M06, M13 |
| managed agents | 🧭 | M13 integrations |
| Agent routing (experimental) | 🧭 | M14 |

## B. Tools ecosystem

| Topic | Status | Where |
|-------|--------|-------|
| Function tools + docstrings | ✅ | M03 |
| ToolContext state / actions | ✅ | M03–M04 |
| transfer_to_agent / escalate / skip_summarization | ✅ | M05, M05-loop |
| FunctionTool wrapper | 📘 | M03 |
| LongRunningFunctionTool | 📘 | M03, M13 |
| AgentTool (agent-as-tool) | ✅ | M05 `agent_as_tool` |
| Built-ins: google_search | 📘 + pattern | M05 parallel, M13 |
| Code execution tools | 📘 | M06, M13 |
| load_memory / preload_memory | ✅ | M10 |
| load_artifacts | 📘 | M11 |
| MCP McpToolset (stdio/SSE/HTTP) | 📘 + scaffold | M13 |
| Expose ADK tools as MCP server | 🧭 | M13 |
| Third-party integrations catalog | 🧭 | M13, resources |

## C. Context: Session / State / Memory / Artifacts

| Topic | Status | Where |
|-------|--------|-------|
| Session object & lifecycle | 📘 | M04 |
| Events | 📘 | M04, M16 |
| State prefixes (session / user: / app: / temp:) | ✅ | M04 |
| Instruction `{var}` / `{var?}` / `{artifact.x}` | ✅ | M04–M05 |
| InMemorySessionService | ✅ | M04 |
| DatabaseSessionService | 📘 | M04, M08 |
| VertexAiSessionService | 🧭 | M08, M10 |
| MemoryService role | 📘 + ✅ demo | M10 |
| InMemoryMemoryService | ✅ | M10 |
| VertexAiMemoryBankService | 🧭 | M10 |
| VertexAiRagMemoryService | 🧭 | M10 |
| Artifacts + Part/Blob | 📘 + ✅ | M11 |
| InMemoryArtifactService / GcsArtifactService | 📘 | M11 |
| user: artifact namespace | 📘 | M11 |
| Context management (filter, summarize, tokens) | 📘 | M16, M12 plugins |

## D. Orchestration & workflows

| Topic | Status | Where |
|-------|--------|-------|
| Hierarchical coordinator | ✅ | M05 travel_team |
| SequentialAgent | ✅ | M05 sequential_research |
| ParallelAgent | ✅ | M05 parallel_research |
| LoopAgent + escalate exit | ✅ | M05 loop_refine |
| AgentTool composition | ✅ | M05 agent_as_tool |
| Collaborative workflows | 📘 | M05, M14 |
| Graph-based workflows (ADK 2.0) | 📘 | M14 |
| Dynamic workflows (ADK 2.0) | 📘 | M14 |
| Custom agents / BaseAgent | 📘 | M14 |

## E. Extensibility

| Topic | Status | Where |
|-------|--------|-------|
| before/after agent callbacks | ✅ | M12 |
| before/after model callbacks | ✅ | M12 |
| before/after tool callbacks | ✅ | M12 |
| Callback control (None vs override) | 📘 | M12 |
| Plugins (BasePlugin, Runner-global) | ✅ | M12 |
| Prebuilt plugins (logging, filter, reflect-retry…) | 🧭 | M12, M13 |
| Skills / Agent Skills | 🧭 | M13 |
| Agent Config (YAML) | 📘 | M16 |

## F. Models & auth

| Topic | Status | Where |
|-------|--------|-------|
| Gemini via API key | ✅ | M00 |
| Vertex / Agent Platform models | 📘 | M16 |
| LiteLLM / Ollama / vLLM connectors | 🧭 | M16 |
| Model routing / failover | 🧭 | M16 |
| Safety settings | 📘 | M12, M15 |

## G. Runtime & developer experience

| Topic | Status | Where |
|-------|--------|-------|
| adk create / run / web | ✅ | M00–M02 |
| Runner / InMemoryRunner | ✅ | M04, M10–M12 |
| Events stream | 📘 | M16 |
| InvocationContext | 📘 | M16 |
| adk api_server | 📘 | M08 |
| Agents CLI / coding with AI | 🧭 | M00, resources |
| Trace UI | 📘 | M02, M07 |

## H. Evaluation

| Topic | Status | Where |
|-------|--------|-------|
| Trajectory vs final response | 📘 | M07 |
| .test.json / evalset schema | ✅ | M07 |
| Criteria matrix (all metrics) | 📘 | M07 |
| adk eval CLI | 📘 | M07 |
| AgentEvaluator + pytest | 📘 | M07 |
| Conformance tests | 📘 | M07 |
| User simulation | 🧭 | M07 |
| Web UI eval | 📘 | M07 |

## I. Streaming & multimodal

| Topic | Status | Where |
|-------|--------|-------|
| Gemini Live / bidirectional streaming | 📘 | M15 |
| run_live / RunConfig | 📘 | M15 |
| Streaming tools | 🧭 | M15 |
| Audio/video modalities | 🧭 | M15 |

## J. Deployment & ops

| Topic | Status | Where |
|-------|--------|-------|
| Local process | ✅ | all labs |
| Docker | ✅ template | M08 |
| Cloud Run (`adk deploy cloud_run`) | 📘 | M08 |
| Agent Runtime / agent_engine | 📘 | M08 |
| GKE | 🧭 | M08 |
| Secrets / auth / checklist | ✅ | M08 |
| Observability (logs, traces, metrics) | 📘 | M08, M12 |
| Safety & guardrails | 📘 | M12, M15 |

## K. Capstone

| Topic | Status | Where |
|-------|--------|-------|
| Multi-agent + tools + state + eval | ✅ required | M09 |
| Memory integration | ✅ | M09 `run_with_services.py` |
| Plugin integration | ✅ | M09 `plugins/research_ops_plugin.py` |
| Conformance specs | ✅ | M09 `conformance/` |
| Production readiness | ✅ | M08–M09 |

## L. Vertex / GCP pack

| Topic | Status | Where |
|-------|--------|-------|
| Vertex env / ADC | 📘 + scripts | M17 |
| VertexAiSessionService | 📘 + smoke script | M17 |
| VertexAiMemoryBankService | 📘 + wiring sample | M17 |
| `adk deploy agent_engine` | ✅ script | M17 scripts/03 |
| `adk deploy cloud_run` | ✅ script | M17 scripts/04 |
| Enable APIs | ✅ script | M17 scripts/01 |

## M. MCP runnable lab

| Topic | Status | Where |
|-------|--------|-------|
| McpToolset stdio filesystem | ✅ | M13 `mcp_filesystem_agent` |
| Read-only tool_filter | ✅ | same |
| Setup guide (Node/npx) | ✅ | M13 SETUP_MCP.md |
| Sandbox content | ✅ | sandbox/ |
| Expose ADK tools as MCP server | 📘 skeleton | M25 |

## N. Production ADK 2.x (modules 18–25)

| Topic | Status | Where |
|-------|--------|-------|
| Workflow graphs + routes | ✅ | M18 loan_graph |
| Runner(node=workflow) | ✅ | M18 |
| Auth / credential services | ✅ pattern | M19 |
| Telemetry / OTEL console | ✅ | M20 |
| BuiltInCodeExecutor | ✅ | M21 |
| DatabaseSessionService SQLite | ✅ | M22 |
| Long-running / HITL stubs | ✅ | M23 |
| Skills load_skill_from_dir | ✅ | M24 |
| A2A / multi-model / optimization | 📘 | M25 |
| GitHub Actions CI | ✅ | `.github/workflows/course-ci.yml` |
| Capstone reference solution | ✅ | M09 solutions/ |

## O. Advanced runtime (26–28)

| Topic | Status | Where |
|-------|--------|-------|
| LiveRequestQueue offline | ✅ | M26 |
| SSE streaming RunConfig | ✅ | M26 `run_sse_stream.py` |
| BIDI run_live text lab | ✅ | M26 `run_live_text_session.py` |
| OAuth AuthConfig simulation | ✅ | M27 |
| Local OAuth code exchange server | ✅ | M27 `run_oauth_local_server.py` |
| `to_a2a` Starlette server | ✅ | M28 serve_math_specialist |
| RemoteA2aAgent client | ✅ | M28 coordinator |

---

## Recommended full path (deep track)

```
00 Setup → 01 Foundations → 02 First agent → 03 Tools (all types)
→ 04 Sessions/State → 10 Memory → 11 Artifacts
→ 05 Multi-agent (seq/par/loop/agent-tool) → 14 Graphs
→ 06 Advanced LlmAgent → 12 Callbacks & Plugins
→ 13 MCP & Integrations → 16 Models/Config/Runtime
→ 07 Evaluation → 15 Streaming → 08 Deployment → 09 Capstone
```

Fast track (original 00–09) still works; deep modules 10–16 are the “complete ADK” layer.
