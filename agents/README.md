# Agentic AI with Google ADK — Complete Deep Course

**Build production-grade agents covering the full Google Agent Development Kit surface** — from first `LlmAgent` through multi-agent workflows, graphs, auth, telemetry, MCP, evaluation, and deploy.

| | |
|---|---|
| **Level** | Beginner → Expert |
| **Duration** | ~50–70 hours (full) · ~25–35 hours (core 00–09) |
| **Stack** | Python 3.10+, Google ADK **2.x**, Gemini |
| **Coverage map** | [ADK_COVERAGE.md](ADK_COVERAGE.md) |
| **CI** | [`.github/workflows/course-ci.yml`](.github/workflows/course-ci.yml) |
| **Docs** | [https://adk.dev](https://adk.dev) |

**Tested with:** `google-adk` **2.4.0**

---

## Tracks

| Track | Modules | Goal |
|-------|---------|------|
| **Core** | 00–09 | Multi-agent apps with tools, state, eval, deploy |
| **Deep ADK** | 10–17 | Memory, artifacts, plugins, MCP, Vertex |
| **Production ADK 2.x** | 18–28 | Graphs, auth, telemetry, live, OAuth, A2A |
| **Ship** | Capstone + CI | R1–R9 + automated gates |

---

## Module map

### Core (00–09)

| Module | Topic |
|--------|--------|
| [00](modules/00-setup/) | Setup |
| [01](modules/01-foundations/) | Foundations |
| [02](modules/02-first-agent/) | First agent |
| [03](modules/03-tools/) | Tools |
| [04](modules/04-sessions-state/) | Sessions & state |
| [05](modules/05-multi-agent/) | Multi-agent (seq/par/loop/AgentTool) |
| [06](modules/06-advanced/) | Schemas & planners |
| [07](modules/07-evaluation/) | Evaluation |
| [08](modules/08-deployment/) | Deployment |
| [09](modules/09-capstone/) | Capstone (+ [solutions](modules/09-capstone/solutions/)) |

### Deep (10–17)

| Module | Topic |
|--------|--------|
| [10](modules/10-memory/) | MemoryService |
| [11](modules/11-artifacts/) | Artifacts |
| [12](modules/12-callbacks-plugins/) | Callbacks & plugins |
| [13](modules/13-mcp-integrations/) | MCP (+ runnable filesystem lab) |
| [14](modules/14-graphs-workflows/) | Workflow concepts |
| [15](modules/15-streaming-live/) | Live / streaming |
| [16](modules/16-models-config-runtime/) | Models & runtime |
| [17](modules/17-vertex-gcp/) | Vertex / GCP deploy pack |

### Production ADK 2.x (18–28)

| Module | Topic | Smoke command |
|--------|--------|----------------|
| [18](modules/18-graphs/) | **Graph workflows** | `python modules/18-graphs/run_loan_graph.py` |
| [19](modules/19-auth/) | Auth & credentials | `python modules/19-auth/run_credential_demo.py` |
| [20](modules/20-telemetry/) | Telemetry / OTEL | `python modules/20-telemetry/run_telemetry_demo.py` |
| [21](modules/21-code-executors/) | Code executors | `adk run modules/21-code-executors/calculator_agent` |
| [22](modules/22-db-sessions/) | Database sessions | `python modules/22-db-sessions/run_db_session_demo.py` |
| [23](modules/23-long-running-hitl/) | Long-running / HITL | `python modules/23-long-running-hitl/refund_hitl_stub.py` |
| [24](modules/24-skills/) | Agent skills | `python modules/24-skills/run_skills_demo.py` |
| [25](modules/25-ecosystem/) | Ecosystem survey | see README |
| [26](modules/26-live-streaming/) | **Live / SSE streaming** | `python modules/26-live-streaming/run_live_offline_queue.py` |
| [27](modules/27-oauth-flow/) | **OAuth2 simulation** | `python modules/27-oauth-flow/run_oauth_simulation.py` |
| [28](modules/28-a2a-demo/) | **A2A two-process** | `python modules/28-a2a-demo/smoke_imports.py` |

---

## Quick start

```bash
cd agents
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set GOOGLE_API_KEY

python scripts/verify_course_imports.py
python modules/18-graphs/run_loan_graph.py --text "loan of 5000"

adk run modules/00-setup/setup_probe
```

---

## Capstone (deep track)

```bash
python modules/09-capstone/run_with_services.py   # memory + plugin
# eval + conformance: see modules/09-capstone/README.md
# reference: modules/09-capstone/solutions/
```

---

## CI

GitHub Actions runs import verify, pytest, graph/HITL/skills smokes (no API key required).  
Optional eval job is commented — enable with `GOOGLE_API_KEY` secret.

---

## Official resources

- [adk.dev](https://adk.dev/) · [adk-python](https://github.com/google/adk-python) · [adk-samples](https://github.com/google/adk-samples)
