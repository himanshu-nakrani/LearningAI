# Module 21 — Code Executors

**Time:** 2 hours · **Package:** `google.adk.code_executors`

## Objectives

- Attach a code executor to an LlmAgent  
- Compare `BuiltInCodeExecutor` vs `UnsafeLocalCodeExecutor` vs sandboxed options  
- Never use unsafe local exec in multi-tenant prod  

---

## Executors

| Class | Safety | Use |
|-------|--------|-----|
| `BuiltInCodeExecutor` | Model-integrated sandbox (Gemini) | Preferred for math/analysis |
| `UnsafeLocalCodeExecutor` | **None** — runs on host | Local experiments only |
| Container / GKE / Vertex executors | Sandboxed remote | Production |

```python
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents.llm_agent import LlmAgent

agent = LlmAgent(
    name="calculator_agent",
    model="gemini-flash-latest",
    code_executor=BuiltInCodeExecutor(),
    instruction="Solve math by writing and executing Python. Return the number.",
)
```

---

## Lab

```bash
adk run modules/21-code-executors/calculator_agent
# Try: Calculate 17! and (5+7)*3
```

### Exercises

1. Compare results with pure-tool calculator vs code executor.  
2. List attack prompts you must block if using UnsafeLocal.  
3. Sketch GKE executor networking policy.  

## Next

→ [Module 22 — Database sessions](../22-db-sessions/README.md)
