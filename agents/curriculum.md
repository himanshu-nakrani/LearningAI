# Curriculum — Complete Agentic AI with Google ADK

## Course identity

| Field | Value |
|-------|--------|
| Title | Agentic AI with Google ADK (Deep / Complete) |
| Framework | [Google ADK](https://adk.dev/) — Python labs |
| Completeness | [ADK_COVERAGE.md](ADK_COVERAGE.md) |
| Duration | 40–60h deep · 25–35h core |

---

## Tracks

1. **Core (00–09):** production multi-agent competence  
2. **Deep (10–16):** full ADK subsystem literacy  

---

## Learning outcomes by module

| # | Outcomes |
|---|----------|
| 00 | Install ADK; API keys; `adk create/run/web` |
| 01 | Agent loop, trajectories, when not to use agents |
| 02 | LlmAgent fields; first tool; Dev UI traces |
| 03 | Tool taxonomy; contracts; ToolContext actions |
| 04 | Session/Event/State; services; prefixes; templating |
| 05 | Hierarchy, Sequential, Parallel, Loop, AgentTool |
| 06 | Schemas, planners, gen config, code exec intro |
| 07 | All major eval metrics; eval CLI; conformance |
| 08 | Deploy Cloud Run / Agent Runtime; prod checklist |
| 09 | Capstone multi-agent system + eval |
| 10 | MemoryService; load/preload memory; Memory Bank vs RAG |
| 11 | Artifacts; versioning; namespaces; GCS vs memory |
| 12 | Callbacks control flow; Plugins global hooks |
| 13 | MCP client/server patterns; integrations map |
| 14 | Graphs, dynamic workflows, custom agents |
| 15 | Live streaming architecture & RunConfig themes |
| 16 | Models connectors; Agent Config; Runner/Events/context |
| 17 | Vertex sessions, Memory Bank, deploy agent_engine/cloud_run |
| 18 | Graph workflows (`Workflow`, routes, `Runner(node=…)`) |
| 19 | Auth & credential services |
| 20 | Telemetry / OpenTelemetry |
| 21 | Code executors |
| 22 | DatabaseSessionService |
| 23 | Long-running tools & HITL |
| 24 | Agent skills |
| 25 | A2A, multi-model, MCP export, optimization survey |
| 26 | LiveRequestQueue, SSE, run_live BIDI |
| 27 | OAuth2 AuthConfig simulation + local redirect server |
| 28 | A2A to_a2a server + RemoteA2aAgent client |
| CI | GitHub Actions verify + smokes |
| 09† | Capstone requires memory + plugin + conformance + solution ref |

† Expanded requirements beyond the original core track.

---

## Capstone rubric (100)

Unchanged from core: architecture, tools, multi-agent, state, eval, docs, stretch.  
**Deep-track distinction (+):** add memory or artifacts or plugin or MCP stretch in submission.

---

## Version policy

APIs evolve. Prefer [adk.dev](https://adk.dev/) if a symbol moves. Course code targets current Python ADK patterns (`root_agent`, `LlmAgent`/`Agent`, workflow agents, sessions, tools, eval CLI).
