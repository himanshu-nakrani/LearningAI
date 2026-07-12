# Module 05 — Multi-Agent Workflows

**Time:** 4–5 hours · **Difficulty:** Intermediate → Advanced

## Objectives

- Explain when to split one agent into many
- Build hierarchical parent + sub-agent systems
- Use workflow agents: Sequential, Parallel, Loop
- Share data with session state and `output_key`
- Compare transfer vs agent-as-tool delegation

---

## 1. Why multi-agent?

Split when you hit:

| Signal | Fix |
|--------|-----|
| Giant instructions, flaky compliance | Specialist agents with narrow jobs |
| Context window pressure | Isolate retrieval / drafting contexts |
| Need guaranteed order | Sequential workflow |
| Independent subtasks | Parallel workflow |
| Iterative quality | Loop + critic / escalate |

ADK treats multi-agent / multi-node apps as **workflows**.

---

## 2. Pattern catalog

### A. Hierarchical (LLM coordinator + sub_agents)

Parent agent has `sub_agents=[...]`. The model (or tools) can **transfer** to a child.

```
travel_coordinator
  ├── flight_agent
  ├── hotel_agent
  └── itinerary_agent
```

Best when routing is language-heavy and dynamic.

### B. Sequential pipeline

Fixed order: A → B → C. Great for research → draft → format.

### C. Parallel

Run independent agents concurrently; merge results via state.

### D. Loop

Repeat until quality gate or max iterations (`escalate` to stop).

### E. Agent-as-tool

Wrap a specialist as a tool so the parent *calls* it like a function (encapsulation, clearer I/O).

### F. Graph / dynamic workflows (ADK 2.0+)

Deterministic nodes + LLM nodes with explicit edges (see official [Graphs](https://adk.dev/graphs/) docs).

---

## 3. Sharing information between agents

1. **Conversation events** — automatic shared transcript in the session
2. **Session state** — tools write keys; others read via `{key?}` or tools
3. **`output_key`** — final response of an agent stored into state
4. **Artifacts** — files / large blobs

Example:

```python
researcher = Agent(
    ...,
    output_key="research_notes",
)
writer = Agent(
    instruction="Write a brief using notes: {research_notes?}",
    ...
)
```

---

## 4. Lab — Travel planner team

Package: `modules/05-multi-agent/travel_team`

Architecture:

```
root_agent (coordinator)
  ├── flight_specialist   → writes state["flights"]
  ├── hotel_specialist    → writes state["hotels"]
  └── itinerary_specialist → reads both, proposes day plan
```

```bash
adk run modules/05-multi-agent/travel_team
```

**Try:**

```
Plan a 3-day trip to Tokyo in April for two people who like food and culture.
Budget is moderate.
```

**Watch for:**

- Coordinator delegating to specialists
- State keys populated by tools
- Final itinerary that references flights + hotels

### Exercises

1. Add a `budget_guard` tool on the coordinator that rejects luxury if user said “budget”.
2. Add a fourth sub-agent `packing_specialist`.
3. Force a sequential path: always flights → hotels → itinerary (encode in coordinator instruction).
4. **Stretch:** rebuild as SequentialAgent workflow (see `sequential_research` package).

---

## 5. Lab B — Sequential research pipeline

Package: `modules/05-multi-agent/sequential_research`

Flow:

1. `outline_agent` → `output_key="outline"`
2. `draft_agent` reads `{outline?}`
3. `editor_agent` polishes final answer

```bash
adk run modules/05-multi-agent/sequential_research
```

Prompt:

```
Explain how multi-agent systems improve reliability in customer support.
```

---

## 5b. Lab C — Parallel research + merge

Package: `modules/05-multi-agent/parallel_research`

```bash
adk run modules/05-multi-agent/parallel_research
```

`ParallelAgent` runs three researchers concurrently; each writes an `output_key`.
A `SequentialAgent` then runs a synthesis agent that reads all keys.

**Key insight:** branches are independent during parallel execution; share data via **state keys**, not chat history.

---

## 5c. Lab D — Loop refine with escalate

Package: `modules/05-multi-agent/loop_refine`

```bash
adk run modules/05-multi-agent/loop_refine
```

Prompt: `Write a short story about a lighthouse AI.`

Pattern:

- `LoopAgent(max_iterations=5)` runs Critic → Refiner  
- Refiner calls `exit_loop` which sets `tool_context.actions.escalate = True`  
- Loop terminates early when quality gate passes  

---

## 5d. Lab E — Agent as tool

Package: `modules/05-multi-agent/agent_as_tool`

```bash
adk run modules/05-multi-agent/agent_as_tool
```

Parent uses `AgentTool(agent=policy_specialist)` so the specialist is **invoked like a function** (encapsulated) rather than a full conversational transfer.

| Pattern | Control | Best for |
|---------|---------|----------|
| `sub_agents` + transfer | Conversational handoff | Multi-turn specialist ownership |
| `AgentTool` | Call/return | Scoped capability without yielding the whole session |

**ADK 2.0+:** for graph/dynamic workflows see [Module 14](../14-graphs-workflows/README.md).

---

## 6. Design checklist

- [ ] Each agent has **one clear job** and short instruction
- [ ] Descriptions are **routing-friendly**
- [ ] State keys are **named and documented**
- [ ] Failure paths: unknown intent, tool error, escalate
- [ ] You evaluated **trajectory** (Module 07), not only final prose

---

## Checkpoint

1. When is Parallel better than Sequential?
2. What is the difference between sub-agent **transfer** and **agent-as-tool**?
3. How does `output_key` help a pipeline?
4. Why keep specialist instructions short?

---

## Next

→ [Module 06 — Advanced Patterns](../06-advanced/README.md)
