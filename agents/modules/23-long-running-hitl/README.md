# Module 23 — Long-Running Tools & Human-in-the-Loop

**Time:** 2–3 hours

## Objectives

- Design tools that **pause** for humans or external jobs  
- Use ADK patterns: long-running tools, auth interrupts, workflow `rerun_on_resume`  
- Never block the event loop on multi-hour work  

---

## Patterns

### 1. Approval gate (HITL)

```
agent proposes action → tool returns {status: pending_approval, ticket_id}
user → human approves in UI → client sends resume with ticket_id
→ tool completes side effect
```

### 2. FunctionNode auth interrupt

`FunctionNode(..., auth_config=..., rerun_on_resume=True)` yields credential request and resumes after user auth (ADK workflow HITL utils).

### 3. LongRunningFunctionTool

For operations that outlive a single model turn (batch jobs, webhooks). Store job IDs in session state; poll or webhook to complete.

### 4. A2A long-running converters

`google.adk.a2a.converters.long_running_functions` bridges long tasks across agent-to-agent protocols.

---

## Lab (design + stub)

Implement a **refund approval** tool:

1. `request_refund(order_id, amount)` → writes `state["pending_refund"]`, returns pending  
2. `approve_refund(decision)` → only succeeds if pending exists  
3. Agent refuses to claim refund completed without approval  

Skeleton: `refund_hitl_stub.py`

```bash
python modules/23-long-running-hitl/refund_hitl_stub.py
```

### Exercises

1. Add timeout: pending refunds expire after N minutes.  
2. Require dual approval for amount > 1000.  
3. Map this to Cloud Tasks / workflow engine.  

## Next

→ [Module 24 — Skills](../24-skills/README.md)
