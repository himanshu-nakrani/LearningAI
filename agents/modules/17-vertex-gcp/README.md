# Module 17 — Vertex AI / GCP Production Pack

**Time:** 4–6 hours · **Requires:** Google Cloud project with billing  
**Docs:** [Agent Runtime](https://adk.dev/deploy/agent-runtime/) · [Memory Bank](https://adk.dev/sessions/memory/) · [Sessions](https://adk.dev/sessions/session/) · [Google Cloud setup](https://adk.dev/get-started/google-cloud/)

## Objectives

- Authenticate to GCP (ADC) and enable required APIs  
- Wire **Vertex AI** models instead of AI Studio API keys  
- Use **VertexAiSessionService** for durable multi-instance sessions  
- Use **VertexAiMemoryBankService** (and optional RAG memory)  
- Deploy with `adk deploy agent_engine` and/or `adk deploy cloud_run`  
- Run a local “Vertex-shaped” sample that fails gracefully without GCP  

> **Cost warning:** Agent Runtime, Vertex sessions, and Memory Bank are paid beyond free tiers. Prefer a dedicated dev project and budgets/alerts.

---

## 1. Prerequisites checklist

| Step | Command / action |
|------|------------------|
| gcloud CLI | `gcloud --version` |
| Project | `gcloud config set project YOUR_PROJECT_ID` |
| Billing | Console → Billing linked |
| Auth | `gcloud auth application-default login` |
| APIs | Run `scripts/01_enable_apis.sh` |
| Python deps | `pip install 'google-adk[vertexai]' google-cloud-aiplatform` |

Environment (add to `.env` or export):

```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=your-gcp-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
# Optional for Memory Bank / sessions tied to Agent Runtime:
export AGENT_ENGINE_ID=your-reasoning-engine-id
```

---

## 2. Model auth: AI Studio vs Vertex

| Mode | Env | Best for |
|------|-----|----------|
| AI Studio | `GOOGLE_API_KEY` | Local learning (modules 00–16) |
| Vertex | `GOOGLE_GENAI_USE_VERTEXAI=TRUE` + project/location + ADC | Enterprise, IAM, VPC-SC |

```python
# Same agent code — backend switches via env
root_agent = Agent(
    model="gemini-flash-latest",  # or a Vertex-available model id
    name="vertex_demo",
    instruction="...",
)
```

---

## 3. Vertex sessions

```python
from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project=PROJECT_ID,
    location=LOCATION,
)
# app_name for create_session is often the Reasoning Engine resource name/id
```

Compare:

| Service | Multi-instance safe? | Setup |
|---------|----------------------|-------|
| InMemory | No | Zero |
| DatabaseSessionService | Yes (your DB) | Medium |
| VertexAiSessionService | Yes (managed) | Agent Platform |

---

## 4. Memory Bank

```python
from google.adk.memory import VertexAiMemoryBankService

memory_service = VertexAiMemoryBankService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID,
)

runner = Runner(
    agent=agent,
    app_name=APP,
    session_service=session_service,
    memory_service=memory_service,
)
```

CLI:

```bash
adk web path/to/agents --memory_service_uri="agentengine://ENGINE_ID"
```

RAG alternative:

```python
from google.adk.memory import VertexAiRagMemoryService

memory_service = VertexAiRagMemoryService(
    rag_corpus="projects/.../locations/.../ragCorpora/...",
    similarity_top_k=5,
    vector_distance_threshold=0.6,
)
```

---

## 5. Deploy scripts (this module)

| Script | Purpose |
|--------|---------|
| `scripts/01_enable_apis.sh` | Enable Vertex / related APIs |
| `scripts/02_set_env.sh` | Export Vertex env template |
| `scripts/03_deploy_agent_engine.sh` | `adk deploy agent_engine` |
| `scripts/04_deploy_cloud_run.sh` | `adk deploy cloud_run` |
| `scripts/05_smoke_vertex_session.py` | Create session via Vertex service (optional) |

```bash
chmod +x modules/17-vertex-gcp/scripts/*.sh
./modules/17-vertex-gcp/scripts/01_enable_apis.sh
source ./modules/17-vertex-gcp/scripts/02_set_env.sh   # edit first
# Create Agent Runtime resource per official deploy guide, then:
export AGENT_ENGINE_ID=...
./modules/17-vertex-gcp/scripts/03_deploy_agent_engine.sh modules/17-vertex-gcp/samples/vertex_hello
```

### Deploy payload notes

- Python deploy to Agent Runtime **does not** ship ADK Web UI — platform provides API server  
- Include `requirements.txt` / deps with your agent package  
- MCP agents: define tools **synchronously**; container must include Node if using npx MCP  

---

## 6. Sample agent

```bash
# Works with AI Studio OR Vertex depending on env
adk run modules/17-vertex-gcp/samples/vertex_hello
```

Programmatic Vertex wiring (skips cleanly if not configured):

```bash
python modules/17-vertex-gcp/samples/run_vertex_wired.py
```

---

## 7. Lab exercises

1. Switch one course agent from API key to Vertex-only env; re-run.  
2. Draw architecture: Cloud Run vs Agent Runtime for the capstone.  
3. Create a budget alert for the project.  
4. Wire Memory Bank + `preload_memory` on a tiny agent (after engine exists).  
5. Deploy `vertex_hello` to Cloud Run **or** Agent Engine; hit health/prompt once.  

---

## 8. Production checklist (Vertex)

- [ ] Dedicated GCP project + budget  
- [ ] Least-privilege service account for runtime  
- [ ] Secrets in Secret Manager (no keys in images)  
- [ ] Durable sessions (Vertex or Postgres)  
- [ ] Memory policy (what is ingested / retention)  
- [ ] Cloud Trace / logging enabled  
- [ ] Eval + conformance still run in CI before deploy  

---

## Checkpoint

1. Why is InMemorySessionService unsafe behind multi-replica Cloud Run?  
2. What identifier does Memory Bank typically need?  
3. Name one difference between Agent Runtime deploy and local `adk web`.  

## Next

→ Capstone with production notes · or [MCP lab](../13-mcp-integrations/README.md)
