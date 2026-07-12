# Module 14 — Graph Workflows, Dynamic Workflows & Custom Agents (ADK 2.0+)

**Time:** 3–4 hours · **Docs:** [Workflows](https://adk.dev/workflows/) · [Graphs](https://adk.dev/graphs/) · [Dynamic](https://adk.dev/graphs/dynamic/) · [Template workflows](https://adk.dev/agents/workflow-agents/)

## Objectives

- Know when template workflows (Seq/Par/Loop) are enough  
- Understand **graph workflows**: explicit nodes + edges + branching  
- Understand **dynamic workflows**: full programmatic control  
- Place **collaborative** multi-agent patterns  
- Sketch custom `BaseAgent` when templates don’t fit  

---

## 1. Workflow decision tree

```
Need fixed A→B→C?
  → SequentialAgent (template) or graph path

Independent concurrent work?
  → ParallelAgent then merge

Iterative refine until quality?
  → LoopAgent + escalate / max_iterations

Language-driven specialist routing?
  → Hierarchical sub_agents / collaborative coordinator

Complex branching + deterministic code mixed with LLM?
  → Graph workflow (ADK 2.0)

Fully code-defined control flow?
  → Dynamic workflow
```

Official note: ADK 2.0 promotes graphs/dynamic as more flexible successors to pure templates — templates remain valid and are used heavily in this course.

---

## 2. Graph workflows (conceptual API)

Graphs weave:

- **LLM agent nodes** (reasoning)  
- **Deterministic function/code nodes**  
- **Conditional edges** (branch on state)  
- Explicit execution paths for reliability  

Benefits:

- Predictable control flow  
- Easier auditing than free-form multi-agent chat  
- Mix AI only where needed  

Study: [adk.dev/graphs](https://adk.dev/graphs/) for language-specific constructors (`workflow.NewAgentNode`, Python graph builders).

**Lab task (design):** Draw a graph for loan approval:

```
[collect_docs] → [risk_score_code] → decision
                      │ low  → [auto_approve_agent]
                      │ high → [human_review_agent]
```

Implement as Sequential + tools first; re-express as graph once you upgrade to ADK 2.0 graph APIs in your environment.

---

## 3. Dynamic workflows

Dynamic workflows let you compose agents/nodes with **ordinary control flow** (if/else, loops, try/except) instead of a static graph definition. Use when logic is highly conditional or data-dependent.

---

## 4. Collaborative workflows

A coordinator agent dynamically assigns work among a set of specialists (similar to hierarchical transfer, with ADK 2.0 collaborative primitives). Compare with:

- Transfer (conversation handoff)  
- AgentTool (encapsulated call)  
- Parallel specialists + merger  

---

## 5. Custom agents

When you need behavior that isn’t LlmAgent or a template:

- Subclass `BaseAgent`  
- Implement run lifecycle  
- Emit Events consistently  

Use sparingly — prefer composition of stock agents.

---

## 6. Agent routing (experimental)

Runtime selection among agents for A/B tests, fallbacks, auto-routing. See [Agent routing](https://adk.dev/agents/routing/).

---

## 7. Course labs already covering templates

| Pattern | Package |
|---------|---------|
| Sequential | `05-multi-agent/sequential_research` |
| Parallel | `05-multi-agent/parallel_research` |
| Loop | `05-multi-agent/loop_refine` |
| Hierarchy | `05-multi-agent/travel_team` |
| AgentTool | `05-multi-agent/agent_as_tool` |

### Exercises

1. Re-read loop_refine; add a third quality criterion.  
2. Parallel_research: add a fourth researcher.  
3. Design (on paper) a graph with a code node that validates JSON schema before writer agent.  
4. List three workflows better as graphs than free hierarchy.  

---

## Checkpoint

1. Why are graphs more auditable than pure LLM routing?  
2. How does LoopAgent stop without infinite loops?  
3. When is AgentTool better than sub_agent transfer?  

## Next

→ [Module 15 — Streaming / Live](../15-streaming-live/README.md)
