# Module 18 — Graph Workflows (ADK 2.x `google.adk.workflow`)

**Time:** 3–4 hours · **Requires:** google-adk ≥ 2.0  
**Package:** `google.adk.workflow` — `Workflow`, `FunctionNode`, `START`, routes

## Objectives

- Build a **graph** of deterministic function nodes with branching  
- Emit **routes** via `ctx.route` for conditional edges  
- Run graphs with `Runner(node=workflow, ...)` (not only `agent=`)  
- Compare graphs vs Sequential/Parallel/Loop templates  

---

## 1. Why graphs?

| Template agents | Graph workflows |
|-----------------|-----------------|
| Fixed Seq/Par/Loop shapes | Arbitrary DAGs + conditional routes |
| Mostly agent-centric | Mix **code nodes** + LLM nodes |
| Good for simple pipelines | Auditable business logic + AI where needed |

---

## 2. Core API

```python
from google.adk.workflow import Workflow, FunctionNode, START
from google.adk.agents.context import Context

def score(ctx: Context, amount: int = 0) -> dict:
    band = "low" if amount < 10_000 else "high"
    ctx.state["band"] = band
    ctx.route = band          # drives conditional edges
    return {"amount": amount, "band": band}

score_node = FunctionNode(func=score, name="score")
# edges: START → parse → score → {low: approve, high: review}
wf = Workflow(name="loan_graph", edges=[...])

runner = Runner(node=wf, app_name="loan", session_service=svc)
```

**Notes**

- Parameters bind from `ctx.state` by default (`parameter_binding='state'`)  
- Inject `ctx: Context` to write state / set route  
- User message is available via session events  
- CLI `adk run` expects `root_agent`; use the Python runner for pure graphs  

---

## 3. Lab — Loan decision graph

```bash
python modules/18-graphs/run_loan_graph.py
python modules/18-graphs/run_loan_graph.py --amount 50000
```

Flow:

```
START → parse_amount → score_risk
                          ├─ route "low"  → approve_low
                          └─ route "high" → review_high
```

### Exercises

1. Add a `fraud_check` node before score (always runs).  
2. Add `DEFAULT_ROUTE` fallback to `review_high`.  
3. Insert an `LlmAgent` node (wrapper) that explains the decision in prose.  
4. Draw your graph as mermaid in the lab journal.  

---

## 4. Dynamic workflows

Programmatic scheduling / dynamic nodes live under the same package (`DynamicNodeScheduler`, etc.). Use when topology depends on runtime data beyond simple routes — see [adk.dev/graphs/dynamic](https://adk.dev/graphs/dynamic/).

---

## Checkpoint

1. How does a FunctionNode choose the next edge?  
2. Why isn’t `Workflow` a `BaseAgent`?  
3. When keep SequentialAgent instead of a graph?  

## Next

→ [Module 19 — Auth](../19-auth/README.md)
