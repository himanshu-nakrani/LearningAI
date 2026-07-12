# Module 19 — Auth & Credentials

**Time:** 2–3 hours · **Package:** `google.adk.auth`  
**Docs:** auth modules in adk-python (`AuthCredential`, credential services, OAuth2 exchanger)

## Objectives

- Explain why tools need **credential services** separate from session state  
- Use `InMemoryCredentialService` / session-state credential patterns  
- Understand `AuthConfig`, `AuthScheme`, OAuth2 exchange/refresh  
- Design least-privilege tool auth for production  

---

## 1. Concepts

| Piece | Role |
|-------|------|
| `AuthScheme` | How to auth (API key, OAuth2, OIDC, …) |
| `AuthCredential` | Concrete secret/token material |
| `AuthConfig` | Declares what a tool/node needs |
| `CredentialService` | Stores/retrieves credentials for the runner |
| `CredentialExchanger` / refresher | OAuth code → tokens, refresh |

Wire on Runner:

```python
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)

runner = Runner(
    agent=agent,
    app_name="app",
    session_service=sessions,
    credential_service=InMemoryCredentialService(),
)
```

FunctionNodes can also take `auth_config=` (HITL: pause until user provides creds).

---

## 2. Lab — API-key style credential demo

```bash
python modules/19-auth/run_credential_demo.py
```

Simulates a tool that reads a demo API key from the credential service / state.

### Exercises

1. Swap to `SessionStateCredentialService` and show isolation per session.  
2. Design OAuth scopes for a “read calendar + create event” agent.  
3. Document where secrets must live (Secret Manager vs session).  

---

## 3. Production checklist

- [ ] No long-lived secrets in prompts or git  
- [ ] Credential service behind runner, not global env only  
- [ ] Refresh tokens rotated; short access token TTL  
- [ ] Tool-level scopes (calendar.read ≠ drive.full)  
- [ ] Audit log on credential use  

---

## Checkpoint

1. Difference between `GOOGLE_API_KEY` for Gemini vs tool OAuth?  
2. Why inject credentials via service instead of hardcoding in tools?  

## Next

→ [Module 20 — Telemetry](../20-telemetry/README.md)
