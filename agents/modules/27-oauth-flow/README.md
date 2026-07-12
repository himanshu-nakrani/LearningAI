# Module 27 — OAuth2 Credential Flow (HITL)

**Time:** 2–3 hours · **APIs:** `AuthConfig`, `AuthScheme`, `AuthCredential`, credential services, FunctionNode `auth_config`

## Objectives

- Model an **OAuth2 authorization-code** style flow with ADK auth objects  
- Simulate browser redirect → auth code → exchanged token without real IdP  
- Store credentials via `InMemoryCredentialService` / state  
- Wire a tool that refuses to run until credentials exist  

---

## 1. ADK auth flow (conceptual)

```
Tool/Node needs AuthConfig(auth_scheme=OAuth2, raw_auth_credential=client_id/secret)
        │
        ▼
ADK emits adk_request_credential (client shows browser / consent UI)
        │
        ▼
User completes OAuth; client fills exchanged_auth_credential (code/tokens)
        │
        ▼
CredentialService stores credential_key → tokens
        │
        ▼
Tool uses access token for API call
```

In real apps the **client** (web UI / mobile) owns the browser redirect. ADK agents request credentials; they don’t embed browser chrome.

---

## 2. Lab — Simulated OAuth dance

```bash
python modules/27-oauth-flow/run_oauth_simulation.py
```

This offline lab:

1. Builds an `AuthConfig` for a fake OAuth2 scheme  
2. Simulates “user authorized” by writing a mock token into the credential service  
3. Calls a protected tool that requires the token  

### With real Google OAuth (stretch)

1. Create OAuth client in Google Cloud Console  
2. Set redirect URI `http://localhost:8765/callback`  
3. Export:

```bash
export OAUTH_CLIENT_ID=...
export OAUTH_CLIENT_SECRET=...
export OAUTH_SCOPES=openid,email
python modules/27-oauth-flow/run_oauth_local_server.py
```

Opens a tiny local HTTP server that completes the code exchange (teaching server only).

---

## 3. Exercises

1. Add token expiry + refresh path (store `expires_at`).  
2. Map scopes to tool permissions matrix.  
3. Document Secret Manager layout for client secrets.  

## Next

→ [Module 28 — A2A demo](../28-a2a-demo/README.md)
