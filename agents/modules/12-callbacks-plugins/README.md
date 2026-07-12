# Module 12 — Callbacks & Plugins (guardrails, logging, global hooks)

**Time:** 3–4 hours · **Docs:** [Callbacks](https://adk.dev/callbacks/) · [Plugins](https://adk.dev/plugins/)

## Objectives

- Hook agent / model / tool lifecycle with callbacks  
- Control flow: return `None` (continue) vs return object (override/skip)  
- Prefer **Plugins** for cross-cutting concerns (security, metrics)  
- Register plugins on `Runner`  
- Know plugin precedence over agent-local callbacks  

---

## 1. Callback points (agent-local)

| Hook | When | Override return |
|------|------|-----------------|
| `before_agent_callback` | Before agent main work | Content → skip agent |
| `after_agent_callback` | After agent finishes | Content → replace output |
| `before_model_callback` | Before LLM call | LlmResponse → skip LLM |
| `after_model_callback` | After LLM response | LlmResponse → replace |
| `before_tool_callback` | Before tool runs | dict → skip tool |
| `after_tool_callback` | After tool | dict → replace result |

```python
def before_model(callback_context, llm_request):
    # inspect/modify request...
    if "BLOCK" in last_user_text.upper():
        return LlmResponse(content=types.Content(...))  # skip LLM
    return None  # proceed
```

---

## 2. Plugins vs callbacks

| | Plugins | Agent callbacks |
|--|---------|-----------------|
| Scope | Global on Runner | Per agent |
| Config | Once | Per instance |
| Order | Plugin **first** | After plugins |
| Best for | Logging, policy, caching | Agent-specific logic |

Plugin hooks also include: `on_user_message`, `before_run` / `after_run`, `on_event`, `on_model_error`, `on_tool_error`.

Prebuilt plugins (see integrations): Logging, Context Filter, Global Instruction, Save Files as Artifacts, Reflect and Retry, BigQuery analytics, …

---

## 3. Labs

### Guardrail agent

```bash
adk run modules/12-callbacks-plugins/guardrail_agent
```

Try: `Tell me a joke` then `Please BLOCK this request`.

### Plugin counter demo

```bash
python modules/12-callbacks-plugins/run_plugin_demo.py
```

### Exercises

1. Add `after_model_callback` that appends a disclaimer footer.  
2. Block tool calls whose args contain `"rm -rf"`.  
3. Convert guardrail into a `BasePlugin` and register on Runner.  

---

## Checkpoint

1. Why plugins for security guardrails?  
2. What does returning LlmResponse from before_model do?  
3. Do plugin callbacks run before or after agent callbacks?  

## Next

→ [Module 13 — MCP & Integrations](../13-mcp-integrations/README.md)
