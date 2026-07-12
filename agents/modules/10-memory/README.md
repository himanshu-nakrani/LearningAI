# Module 10 — Long-Term Memory (`MemoryService`)

**Time:** 3–4 hours · **Depth:** Complete ADK memory stack  
**Docs:** [Memory](https://adk.dev/sessions/memory/) · [Sessions overview](https://adk.dev/sessions/)

## Objectives

- Separate **Session/State** (this chat) from **Memory** (searchable cross-session knowledge)
- Configure `InMemoryMemoryService` and wire it into `Runner`
- Ingest sessions with `add_session_to_memory`
- Recall with `load_memory` / `preload_memory` tools
- Search memory from custom tools via `tool_context.search_memory`
- Compare Memory Bank vs RAG memory (GCP)

---

## 1. Mental model

| | Session / State | Memory |
|--|-----------------|--------|
| Scope | One conversation thread | Across sessions / external knowledge |
| Access | Automatic history + state keys | Explicit search / preload |
| Analogy | Whiteboard in the room | Company wiki / CRM archive |

`MemoryService` operations:

1. `add_session_to_memory(session)` — ingest completed session  
2. `add_events_to_memory(...)` — incremental (if supported)  
3. `add_memory(...)` — direct entries (if supported)  
4. `search_memory(app_name, user_id, query)` — retrieval  

---

## 2. Implementations

| Service | Persistence | Search | Use when |
|---------|-------------|--------|----------|
| `InMemoryMemoryService` | No | Keyword | Local demos |
| `VertexAiMemoryBankService` | Yes (Agent Platform) | Semantic, LLM-extracted | Product memory |
| `VertexAiRagMemoryService` | Yes (Knowledge Engine) | Vector similarity | RAG corpora |

CLI hook (when configured):

```bash
adk web agents/ --memory_service_uri="agentengine://ENGINE_ID"
```

---

## 3. Tools ADK provides

```python
from google.adk.tools import load_memory, preload_memory

# On demand when the model chooses:
tools=[load_memory]

# Always inject memory each turn (callback-like):
tools=[preload_memory]
```

Auto-save pattern via after-agent callback:

```python
async def auto_save(callback_context):
    await callback_context.add_session_to_memory()

agent = Agent(..., tools=[preload_memory], after_agent_callback=auto_save)
```

---

## 4. Lab — Capture then recall

Package: `memory_recall_demo` (programmatic scenario + CLI agent)

```bash
# Programmatic two-session demo (needs API key):
python modules/10-memory/run_memory_scenario.py

# Interactive agent that uses load_memory when possible:
adk run modules/10-memory/memory_recall_demo
```

**Scenario:**

1. Session A: user states a favorite project  
2. Ingest session into memory  
3. Session B: ask “What is my favorite project?” → tool recall  

### Exercises

1. Store two facts in session A; recall each in session B.  
2. Implement custom `search_past_conversations(query, tool_context)`.  
3. Document when you’d choose Memory Bank vs RAG memory.  

---

## 5. Multiple memory services

Framework configures **one** memory service on the Runner.  
You may still instantiate a **second** service inside a custom tool (docs corpus + chat history). See official dual-memory example on adk.dev.

---

## Checkpoint

1. Why doesn’t session state alone solve “last week’s preference”?  
2. Difference between `load_memory` and `preload_memory`?  
3. What happens to InMemory memory on process restart?  

## Next

→ [Module 11 — Artifacts](../11-artifacts/README.md)
