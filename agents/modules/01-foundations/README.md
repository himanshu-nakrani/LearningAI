# Module 01 — Agentic AI Foundations

**Time:** 2–3 hours · **Difficulty:** Beginner · **Code:** Conceptual (no ADK required)

## Objectives

- Define agentic systems vs chatbots
- Name core building blocks: model, instructions, tools, state, sessions, runners
- Understand trajectories and the agent loop
- Know common multi-agent patterns
- Decide when *not* to build an agent

---

## 1. Chatbot vs agent vs multi-agent

| | Chatbot | Single agent | Multi-agent system |
|--|---------|--------------|--------------------|
| **Main job** | Generate replies | Achieve a goal with steps | Divide goals across specialists |
| **Tools** | Rare / none | Central | Shared or specialized |
| **Memory** | Short context | Session + state | Shared state / handoffs |
| **Control** | Prompt-only | Loop: reason → act → observe | Orchestration patterns |
| **Example** | FAQ bot | “Book me a flight under $400” | Research + writer + critic team |

**Agent (working definition):**

> An AI system that can **perceive** context, **decide** next actions (often via an LLM), **use tools** to affect the world or fetch data, and **iterate** until a goal is met or it escalates.

---

## 2. The agent loop

Most tool-using agents follow a cycle similar to **ReAct** (Reason + Act):

```
User goal
   │
   ▼
┌──────────────┐
│  Reason      │  LLM reads instruction + history + tool results
└──────┬───────┘
       │ choose tool OR final answer
       ▼
┌──────────────┐
│  Act         │  Execute tool / call API / write code
└──────┬───────┘
       │ observation
       ▼
┌──────────────┐
│  Observe     │  Append tool output to context
└──────┬───────┘
       │
       └──► loop until done
```

In ADK this loop is managed by the **Runner** + event system. You mostly configure:

- **Agent** (model + instruction + tools)
- **Session** (history + state)
- **Tools** (side effects / retrieval)

---

## 3. Core vocabulary (map to ADK)

| Concept | Meaning | ADK map |
|---------|---------|---------|
| **Model** | LLM powering reasoning | `model="gemini-flash-latest"` |
| **Instruction** | System policy / persona / procedure | `instruction=...` |
| **Tool** | Deterministic function the model can call | Python functions / `FunctionTool` |
| **Session** | One conversation thread | `Session` + `SessionService` |
| **State** | Scratchpad / shared working memory | `session.state`, `ToolContext.state` |
| **Event** | Message, tool call, or result in the log | `Event` stream from `Runner` |
| **Trajectory** | Ordered steps the agent took | Tool-use sequence (eval target) |
| **Workflow** | Multi-agent or multi-node graph | Sequential/Parallel/Loop, graphs |
| **Artifact** | Persistent file-like output | Artifact services |
| **Evaluation** | Quality of path + final answer | `adk eval`, eval sets |

Read the full glossary: [resources/glossary.md](../../resources/glossary.md)

---

## 4. Why frameworks (why ADK)?

You *could* hand-roll function calling. Frameworks help with:

1. **Session & context management** — history, state prefixes, summarization
2. **Tool schemas** — auto from signatures/docstrings
3. **Multi-agent orchestration** — hierarchies, workflows, transfer
4. **Dev tooling** — `adk web` traces, eval CLI
5. **Deploy paths** — same agent code → Cloud Run / Agent Runtime

ADK philosophy (from docs): start with a simple agent; grow into workflows when instructions get long, context overflows, or you need deterministic steps mixed with LLM reasoning.

---

## 5. When *not* to use an agent

Prefer plain code / classic automation when:

- Input/output mapping is **fully deterministic**
- Latency and cost of LLM rounds are unjustified
- You need **hard guarantees** without probabilistic decisions
- A single SQL query or form validation solves the problem

Prefer a **single LLM call** (no tools) when:

- Pure rewrite / classify / summarize tasks with all data already in the prompt

Prefer an **agent** when:

- Multi-step goals need external data or actions
- Branching depends on intermediate results
- Human language is the control interface

---

## 6. Multi-agent patterns (preview of Module 05)

```
1. Hierarchical (manager + specialists)
   Router/Coordinator
        ├── BillingAgent
        ├── SupportAgent
        └── SalesAgent

2. Sequential pipeline
   Research → Outline → Draft → Edit

3. Parallel fan-out
   PriceA ∥ PriceB ∥ PriceC → Merge

4. Loop / critique
   Draft ⇄ Critic until quality gate

5. Agent-as-tool
   Root calls Specialist as a tool (encapsulation)
```

---

## 7. Safety & reliability mindset

Agents increase power **and** risk:

| Risk | Mitigation |
|------|------------|
| Hallucinated tool args | Validate inputs; typed tools; constraints |
| Destructive actions | Human approval; dry-run modes; allowlists |
| Prompt injection via tool data | Treat tool output as untrusted |
| Cost spirals | Max steps, token budgets, caching |
| Non-determinism | Eval suites, lower temperature for ops agents |

---

## 8. Architecture sketch for this course

```
                    ┌─────────────────┐
   User ──────────► │  Runner / UI    │
                    └────────┬────────┘
                             │ events
                    ┌────────▼────────┐
                    │  root_agent     │
                    │  (LlmAgent)     │
                    └───┬─────────┬───┘
                        │         │
                   tools│         │sub_agents / workflows
                        ▼         ▼
                   APIs/DBs    specialists
                        │
                    ┌───▼────────────┐
                    │ SessionService │
                    │ state + events │
                    └────────────────┘
```

---

## Checkpoint

1. In one sentence, how does an agent differ from a chatbot?
2. Name the three phases of the ReAct-style loop.
3. What is a **trajectory**, and why evaluate it separately from the final answer?
4. Give one problem that should *not* use an agent.
5. Map: ADK `instruction` ↔ which classic LLM concept?

**Stretch:** Write a ½-page design for a “personal finance coach” agent: goals, tools, state keys, and whether multi-agent is justified.

---

## Next

→ [Module 02 — Your First ADK Agent](../02-first-agent/README.md)
