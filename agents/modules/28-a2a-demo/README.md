# Module 28 — A2A Two-Process Demo

**Time:** 2–3 hours · **Status:** Experimental ADK A2A  
**Deps:** `a2a-sdk==0.3.26` (API expected by google-adk 2.4), `uvicorn`

## Objectives

- Expose an ADK agent as an **A2A Starlette app** via `to_a2a`  
- Call it from another process with **`RemoteA2aAgent`**  
- Understand agent cards, ports, and failure modes  

---

## Architecture

```
Terminal A                          Terminal B
math_specialist ──HTTP/A2A──► coordinator (RemoteA2aAgent)
:9001 uvicorn                         adk run / python client
```

---

## Setup

```bash
pip install 'a2a-sdk==0.3.26' uvicorn
export GOOGLE_API_KEY=...
```

## Run

**Terminal 1 — specialist server**

```bash
python modules/28-a2a-demo/serve_math_specialist.py
# listens http://127.0.0.1:9001
```

**Terminal 2 — coordinator client**

```bash
python modules/28-a2a-demo/run_coordinator_client.py
# or after server is up:
adk run modules/28-a2a-demo/coordinator
```

Offline smoke (no network server required for import check):

```bash
python modules/28-a2a-demo/smoke_imports.py
```

---

## Files

| Path | Role |
|------|------|
| `math_specialist/agent.py` | Specialist agent definition |
| `serve_math_specialist.py` | `to_a2a` + uvicorn |
| `coordinator/agent.py` | Root with `RemoteA2aAgent` sub-agent |
| `run_coordinator_client.py` | One-shot programmatic client |
| `smoke_imports.py` | CI-friendly import check |

---

## Failure modes (study)

| Failure | Mitigation |
|---------|------------|
| Specialist down | Timeout + fallback message |
| Schema drift | Version agent cards |
| Auth missing | mTLS / bearer between services |
| Long tools | A2A long-running converters |

## Checkpoint

1. Why is A2A useful vs in-process `sub_agents`?  
2. What does `to_a2a` return?  
