# Module 08 — Deployment & Production

**Time:** 2–3 hours · **Difficulty:** Advanced

## Objectives

- Choose a runtime: local process, container, Cloud Run, Agent Runtime
- Select a production session backend
- Apply security, observability, and cost controls
- Use a production readiness checklist

---

## 1. Deploy philosophy

ADK aims for **develop locally → deploy without rewriting agent logic**.

Typical path:

```
adk web / adk run   →   containerize   →   Cloud Run / GKE / Agent Runtime
```

Official: [adk.dev deploy docs](https://adk.dev/) (Deploy section).

---

## 2. Runtime options

| Target | Pros | Cons |
|--------|------|------|
| **Local / VM process** | Simple debug | Ops burden, no autoscale |
| **Docker + any host** | Portable | You manage scaling |
| **Cloud Run** | Scale to zero, HTTP | Cold starts; wire sessions |
| **GKE** | Full control | Heavier ops |
| **Agent Runtime / Agent Platform** | Native sessions, enterprise | GCP-centric |

CLI family (exact flags evolve — check `adk deploy --help`):

```bash
adk deploy cloud_run --help
adk deploy agent_engine --help
adk api_server --help
```

### Example deploy commands (from official patterns)

```bash
# Cloud Run
adk deploy cloud_run \
  --project=<gcp-project> \
  --region=<region> \
  --service_name=<name> \
  ./path/to/agent_dir

# Agent Runtime / Agent Engine
adk deploy agent_engine \
  --project=<gcp-project> \
  --region=<region> \
  --staging_bucket="gs://<bucket>" \
  --display_name="My Agent" \
  ./path/to/agent_dir
```

**MCP note:** agents using `McpToolset` must define tools **synchronously** in `agent.py` for deploy; include Node/npx in the image if using stdio community servers.

---

## 3. Production sessions

| Stage | Service |
|-------|---------|
| Dev | `InMemorySessionService` |
| Single region app | `DatabaseSessionService` (Postgres + async driver) |
| GCP Agent Platform | `VertexAiSessionService` |

Requirements for DB sessions:

- Async driver (`asyncpg`, `aiosqlite`, etc.)
- Backup & migration plan (schema can change across ADK versions)

---

## 4. Configuration management

**Do:**

- Secrets in Secret Manager / env injected at runtime
- Model name + temperature as config, not hard-coded forever
- Separate dev / staging / prod projects

**Don't:**

- Commit API keys
- Use `adk web` as the production frontend
- Give tools unrestricted shell/network without review

---

## 5. Observability

Minimum viable production telemetry:

1. **Request IDs** per user turn
2. **Trace** of model + tool spans (ADK Dev UI Trace is the learning version)
3. **Logs**: tool name, latency, success/error (redact PII)
4. **Metrics**: tokens, cost estimate, tool error rate, p95 latency
5. **Alerts**: error spikes, cost spikes, eval regression in CI

Cloud Trace / OpenTelemetry integrations are preferred on GCP.

---

## 6. Safety & security checklist

- [ ] Tool allowlist; no arbitrary code exec in prod without sandbox
- [ ] AuthN/Z in front of the agent HTTP API
- [ ] Validate/sanitize tool arguments
- [ ] Treat retrieved content as untrusted (prompt injection)
- [ ] Rate limit per user
- [ ] Human-in-the-loop for irreversible actions (payments, deletes)
- [ ] Safety settings on model config
- [ ] Data retention policy for sessions

---

## 7. Cost control

| Lever | Technique |
|-------|-----------|
| Model | Flash for routers; Pro only when needed |
| Context | Summarize; `include_contents`; trim tools |
| Steps | Max tool iterations / timeouts |
| Caching | Cache stable system instructions where supported |
| Eval traffic | Separate cheaper eval keys/projects |

---

## 8. Lab — Production readiness pack

This module ships templates (not a live cloud deploy, to avoid billing accidents):

| File | Purpose |
|------|---------|
| `Dockerfile` | Containerize an agent service entrypoint |
| `cloudrun.example.yaml` | Example Cloud Run service shape |
| `production_checklist.md` | Go/no-go list |
| `sample_agent/` | Tiny agent suitable for container demos |

### Exercises

1. Build the Docker image locally (optional; requires Docker).
2. Fill production checklist for the Module 05 travel team.
3. Write a one-page incident runbook: “tool API 500s”.
4. **Stretch:** Deploy to Cloud Run with your GCP project following official ADK deploy guide.

---

## Checkpoint

1. Why is InMemorySessionService wrong for multi-instance prod?
2. Name three observability signals you would alert on.
3. What is a safer pattern than letting an agent run raw shell commands?
4. When is Agent Runtime preferable to plain Cloud Run?

---

## Next

→ [Module 09 — Capstone](../09-capstone/README.md)
