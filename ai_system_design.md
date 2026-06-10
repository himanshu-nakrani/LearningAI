# AI System Design (High Level) — Interview Guide & Examples

> High-level interview-focused guide for designing AI systems clearly and confidently.
>
> Covers interview flow, reusable architecture blocks, AI lifecycle design, serving patterns, and worked examples you can adapt in real interviews.
>
> **Legend:**
> - **★ CORE** must know
> - **◆ CONCEPT** architectural idea
> - **EXAMPLE** worked scenario

## Table of Contents

- [Part 0 — How to answer an AI system design interview](#part-0)
- [Part 1 — Reusable building blocks for AI systems](#part-1)
- [Part 1.5 — AI-specific estimation](#part-1-5)
- [Part 2 — Core trade-offs interviewers expect](#part-2)
- [Part 3 — Generic AI architecture template](#part-3)
- [Part 3.5 — Data, model, and deployment lifecycle](#part-3-5)
- [Part 4 — Example: design a RAG assistant](#part-4)
- [Part 5 — Example: design an agentic workflow system](#part-5)
- [Part 6 — Example: design a recommendation system](#part-6)
- [Part 7 — Example: design a fraud / anomaly detection system](#part-7)
- [Part 8 — Example: design real-time voice AI](#part-8)
- [Part 8.5 — More common interview blueprints](#part-8-5)
- [Part 9 — Safety, evaluation, observability, and cost](#part-9)
- [Part 10 — Final interview checklist](#part-10)

## Part 0 — How to answer an AI system design interview **★ CORE**

AI system design interviews are usually not asking for low-level distributed-systems detail first. They want to see whether you can structure an ambiguous product into a sensible **data flow**, **model flow**, **serving architecture**, and **operations plan**. The best answers are simple, layered, and explicit about trade-offs.

### A simple interview flow

1. **Clarify the use case** — who uses it, what task, what success means.
2. **Define inputs and outputs** — text, image, audio, structured records, actions.
3. **Choose the AI pattern** — classification, ranking, retrieval, generation, agent, forecasting.
4. **Draw the high-level architecture** — clients, APIs, model layer, data stores, async workers.
5. **Discuss model lifecycle** — data collection, training/fine-tuning, deployment, evaluation.
6. **Discuss production concerns** — latency, cost, safety, monitoring, fallback paths.
7. **Close with trade-offs** — why this design over simpler or more advanced options.

> **💡 TIP: Lead with the product goal, not the model**
> In AI interviews, many candidates jump directly to "use an LLM" or "train a transformer." Strong candidates start with the user problem and the success metric. The model is one component of the system, not the whole answer.

### What to clarify early

- **Users:** internal employees, consumers, analysts, support agents, doctors, drivers?
- **Mode:** batch, near-real-time, real-time, interactive?
- **Output quality bar:** helpful suggestion, top-1 prediction, autonomous action, or human-reviewed draft?
- **Risk level:** low-risk summarization vs high-risk finance/healthcare decisioning.
- **Scale:** daily batch jobs, hundreds of QPS, or millions?

### A good one-line structure

```text
  User request / event
        -> data retrieval + context assembly
        -> model inference / decision engine
        -> post-processing + guardrails
        -> response / action
        -> logging + feedback + evaluation
```

### A 45-minute AI system design time budget

| Phase | Time | What to say |
| --- | --- | --- |
| Clarify | 5 min | Use case, users, risk, latency, scale, success metric |
| Choose pattern | 3 min | Predictive ML, RAG, agent, recommendation, multimodal, or hybrid |
| High-level design | 10 min | Online path, offline path, stores, model serving, safety layer |
| Deep dive | 15 min | Retrieval, ranking, feature freshness, agent tools, evals, or latency |
| Operations | 7 min | Monitoring, drift, cost, fallback, rollout, incident handling |
| Wrap | 5 min | Trade-offs, what you would build first, what you would defer |

> **💡 TIP: The strongest answer shape**
> Separate the **online serving path** from the **offline improvement path**. The online path answers users; the offline path improves the model, index, features, prompts, and evals. This single separation makes most AI designs sound production-ready.

### Requirements that matter specifically for AI

| Requirement | Why it matters | Design implication |
| --- | --- | --- |
| Quality target | AI output is probabilistic | Define eval metric, not just feature list |
| Latency target | LLMs, rerankers, speech, and tools add delay | Use streaming, caching, smaller models, async jobs |
| Risk level | Wrong actions can harm users or business | Add approval gates, audit logs, policy checks |
| Freshness | Knowledge, features, and fraud patterns change | Use event-driven indexing, streaming features, retraining cadence |
| Personalization | Context improves utility but increases privacy complexity | Use scoped profiles, consent, feature TTLs, access checks |
| Explainability | Analysts and regulators need reasons | Store evidence, citations, feature attributions, decision reasons |

---

## Part 1 — Reusable building blocks for AI systems **★ CORE**

Most AI systems are composed from the same small set of blocks. Interviewers usually want to hear these pieces named clearly.

| Block | Role | Examples |
| --- | --- | --- |
| Client / product surface | User or upstream system entry point | Web app, API, chat UI, internal tool |
| Application layer | Auth, routing, business logic, orchestration | API gateway, backend service |
| Feature / context layer | Prepares model inputs | Feature store, retrieval service, prompt builder |
| Model serving layer | Runs inference | LLM endpoint, classifier, ranker, speech model |
| State / storage | Stores source data and derived data | OLTP DB, object store, vector DB, cache |
| Async processing | Heavy or delayed work | Queues, stream processors, workers |
| Evaluation / feedback | Measures quality and drift | Offline evals, human review, A/B testing |
| Safety / governance | Controls bad behavior and compliance | Filters, policy engine, audit logs |
| Observability | Tracks health and cost | Tracing, metrics, logs, token usage |

### Common AI system types

- **Predictive ML:** classify, score, forecast, rank.
- **Search + retrieval:** semantic search, hybrid search, enterprise knowledge lookup.
- **Generative AI:** chat, summarization, drafting, code generation.
- **Agentic systems:** plan, use tools, fetch data, take actions across systems.
- **Decisioning systems:** fraud, abuse, recommendations, bidding, dynamic pricing.
- **Multimodal systems:** image understanding, OCR, speech, voice assistants.

### The online/offline split

This diagram is useful in almost every AI system design answer. Draw it early, then zoom into the risky part.

```text
                 OFFLINE / ASYNC PATH

  raw data -> cleaning -> labeling -> features -> train/eval -> registry
      |          |           |            |          |           |
      |          |           |            |          |           v
      |          +---------> data quality checks      deployment gate
      |                                                |
      +-----> indexing / embeddings / batch scores ----+

  ----------------------------------------------------------------

                 ONLINE / SERVING PATH

  request -> auth -> context/features/retrieval -> model/router
          -> guardrails/post-processing -> response/action -> logs
```

### Stores in AI systems

| Store | Holds | Interview notes |
| --- | --- | --- |
| Operational DB | Users, sessions, transactions, permissions | Source of truth for business state |
| Object store | Documents, media, raw logs, training data | Cheap durable storage for offline pipelines |
| Vector/search index | Embeddings, chunks, semantic/keyword indexes | RAG and candidate retrieval; must include metadata/ACLs |
| Feature store | Reusable ML features | Keep offline and online features consistent |
| Cache | Hot prompts, retrieved context, model outputs, rankings | Improves latency/cost, but watch staleness |
| Model registry | Model versions, artifacts, eval reports | Needed for controlled deployment and rollback |
| Trace/eval store | Prompts, tool calls, outputs, labels, feedback | Essential for debugging non-deterministic systems |

## Part 1.5 — AI-specific estimation **★ CORE**

AI system estimation includes normal system-design numbers plus model-specific numbers: tokens, retrieval fan-out, model calls, GPU/API cost, and feedback volume.

### What to estimate

- **Traffic:** QPS, daily active users, peak multiplier.
- **Input size:** tokens per prompt, audio seconds, image size, number of documents.
- **Model calls:** one model call vs router + retriever + reranker + generator + judge.
- **Retrieval fan-out:** top-k chunks, reranked candidates, metadata filters.
- **Latency budget:** retrieval, model first token, tool calls, post-processing.
- **Storage growth:** logs, embeddings, traces, raw data, labels.
- **Cost:** token/API cost, GPU cost, vector DB cost, human review cost.

### Worked estimate: internal RAG assistant

```text
  Assumptions:
    20,000 employees
    30% use assistant daily        -> 6,000 DAU
    8 questions / active user / day -> 48,000 queries/day
    Peak ~= 3x average

  Average QPS:
    48,000 / 86,400 ~= 0.56 QPS
    Peak ~= 1.7 QPS  (small traffic, quality matters more than scale)

  Per query:
    input prompt      ~= 1,500 tokens
    retrieved context ~= 4 chunks * 500 tokens = 2,000 tokens
    output            ~= 400 tokens
    total             ~= 3,900 tokens/query

  Daily token volume:
    48,000 * 3,900 ~= 187M tokens/day

  Design implication:
    The main problem is not QPS. It is grounding quality,
    permissions, token cost, evals, and trace/debug storage.
```

### Embedding storage estimate

```text
  1M document chunks
  embedding dimension: 1,536
  float32 size: 4 bytes

  raw vectors = 1M * 1,536 * 4 bytes ~= 6.1 GB
  plus metadata + ANN index overhead ~= 2-4x
  practical storage estimate ~= 12-25 GB

  If using float16 or quantized vectors, storage drops,
  but recall may change. Mention this as a tuning lever.
```

> **💡 TIP: Estimation signal**
> In AI interviews, a good estimate often shows that the hard part is not always traffic. Sometimes the hard part is token cost, eval quality, stale context, labeling throughput, or permission-safe retrieval.

---

## Part 2 — Core trade-offs interviewers expect **◆ CONCEPT**

### Accuracy vs latency vs cost

This is the central AI production triangle. Larger models often improve quality, but also raise latency and cost. Good answers explain how to tier the system: cheap model first, expensive model only when needed.

```text
  Better quality  -> usually larger model / more retrieval / more compute
  Lower latency   -> smaller model / caching / precomputation
  Lower cost      -> batching / routing / fallback / async processing

  In interviews: say which side you optimize first for this product.
```

### Online vs offline

- **Offline:** training, indexing, batch enrichment, feature computation, evaluation.
- **Online:** request-time retrieval, ranking, inference, safety checks, response formatting.

A common mistake is placing too much work in the online path. High-level designs should move expensive work offline whenever possible.

### Personalization vs simplicity

Personalization improves utility, but adds feature pipelines, privacy concerns, online feature freshness requirements, and harder debugging. Mention this explicitly for recommendations, assistants, and ranking systems.

### Automation vs human-in-the-loop

For low-risk tasks, fully automated AI may be acceptable. For high-risk workflows, a better architecture is AI draft → human review → audited final action. This is often the correct enterprise answer.

### Prompting vs RAG vs fine-tuning vs agents

| Approach | Use when | Avoid when |
| --- | --- | --- |
| Prompting | The task is simple and the model already knows enough | You need private/fresh knowledge or consistent behavior at scale |
| RAG | You need grounded answers over changing knowledge | The problem is style/format/skill rather than factual lookup |
| Fine-tuning | You need consistent format, domain style, or narrow repeated behavior | You mainly need up-to-date facts or citations |
| Agent/tools | The task requires multi-step actions, APIs, or decisions based on intermediate results | A fixed workflow or simple retrieval answer is enough |
| Classical ML | You need low-latency scoring, ranking, forecasting, or classification | The task requires open-ended reasoning or generation |

### Consistency in AI systems

AI systems have normal data consistency issues plus model/version consistency issues. Say which version of the prompt, model, retriever, feature set, and policy produced a result. Without that, debugging and rollback become guesswork.

```text
  User saw bad answer at 10:03
          |
          v
  Need to reconstruct:
    model version       = gpt-x / llama-y / ranker-v12
    prompt version      = support_prompt_2026_06_10
    retrieval index     = docs_index_184
    feature snapshot    = online_features_10:03
    policy version      = pii_policy_v7
    tool outputs        = account_api response IDs
    final output        = exact text/action returned
```

---

## Part 3 — Generic AI architecture template **★ CORE**

This template works for many interview questions. Adapt it rather than inventing a brand-new structure each time.

```text
  [User / App / Event]
          |
          v
    [API Gateway / Backend]
          |
          +--> [Auth / Rate limiting / Policy checks]
          |
          +--> [Context builder]
          |         |
          |         +--> [Operational DB]
          |         +--> [Object store / docs]
          |         +--> [Vector DB / search index]
          |         +--> [Feature store / profile store]
          |
          +--> [Model router / orchestrator]
                    |
                    +--> [Classifier / ranker / LLM / speech model]
                    +--> [Fallback model]
                    +--> [Tool calls / external APIs]
                    |
                    v
              [Post-processing + guardrails]
                    |
                    v
                [Response / action]
                    |
                    +--> [Logs, traces, prompts, outputs]
                    +--> [Feedback events]
                    +--> [Eval pipeline / retraining pipeline]
```

### How to explain it

- **Ingress:** request enters through app/API layer with auth and rate limits.
- **Context assembly:** gather the minimum context needed for good inference.
- **Inference/orchestration:** call one or more models or tools.
- **Guardrails:** validate response, redact sensitive data, check policy.
- **Feedback loop:** store interactions for analytics, evals, and future improvement.

> **💡 TIP: Say where training lives**
> Even in a high-level interview, mention that training and re-indexing live off the critical request path: scheduled pipelines in batch/stream processing, model registry, offline evaluation, then controlled deployment to serving.

### Model router pattern

A production AI system rarely sends every request to the largest model. A router can classify difficulty, risk, or domain and choose the cheapest reliable path.

```text
  request
    |
    v
  [intent + risk classifier]
    |             |              |
    | easy        | hard         | unsafe / restricted
    v             v              v
  small model   large model    refuse / human review
    |             |
    +-------> common response validator
                  |
                  v
              response
```

### Fallback patterns

| Failure | Fallback | Example |
| --- | --- | --- |
| LLM timeout | Smaller model or cached answer | Return concise answer with sources already retrieved |
| Retriever empty | Keyword search, broader query, or ask clarifying question | "I could not find a policy doc for that exact term" |
| Tool/API failure | Retry if idempotent, otherwise degrade to draft | Support copilot drafts but does not submit action |
| Safety uncertainty | Human review | Payment reversal, account closure, medical guidance |
| High cost pressure | Queue async job or summarize shorter | Long document analysis becomes background task |

## Part 3.5 — Data, model, and deployment lifecycle **★ CORE**

High-level AI design is not complete unless you describe how the system improves after launch. The lifecycle is the difference between a demo and a product.

### Lifecycle diagram

```text
  production traffic
        |
        v
  logs + traces + feedback + labels
        |
        +--> data quality checks
        +--> eval set construction
        +--> error taxonomy
        |
        v
  improve one layer:
    - prompt
    - retrieval/chunking
    - features
    - model/fine-tune
    - policy/guardrails
        |
        v
  offline evals -> canary -> A/B test -> full rollout
        |
        v
  monitor drift, cost, quality, incidents
```

### Training-serving skew

Training-serving skew happens when the model is trained on features or data transformations that differ from what online serving uses. This is common in recommendation, fraud, ranking, and personalization systems.

| Skew source | Example | Mitigation |
| --- | --- | --- |
| Feature calculation | Offline uses 30-day purchase count; online uses stale cache | Shared feature definitions, feature store, freshness SLAs |
| Label leakage | Training uses future data accidentally | Point-in-time joins, backtesting discipline |
| Different distributions | Training on historical users, serving new user cohort | Drift monitoring, shadow evaluation, fresh labels |
| Prompt/retrieval mismatch | Offline eval uses curated docs; production retrieval returns noisy chunks | End-to-end evals with real retriever |

### Deployment strategies

- **Shadow mode:** run new model beside production, do not affect users.
- **Canary:** send a small percentage of traffic to new version.
- **A/B test:** compare product metrics and quality metrics.
- **Human-reviewed rollout:** new AI output is visible only to reviewers first.
- **Rollback:** keep model, prompt, retriever, and policy versions separately rollbackable.

### Model registry and governance

```text
  training job / prompt change / retriever change
        |
        v
  artifact + config + eval report + owner
        |
        v
  model/prompt/index registry
        |
        +--> staging endpoint
        +--> canary endpoint
        +--> production endpoint
        |
        v
  rollback pointer: prod -> previous known-good version
```

> **⚠️ WARN: Do not ignore prompts and indexes**
> In LLM/RAG systems, the deployed artifact is not just the model. The prompt template, retrieval index, chunking strategy, reranker, tool schemas, and guardrail policy are all part of the deployable system.

---

## Part 4 — Example: design a RAG assistant **EXAMPLE**

### Goal

Build an internal enterprise assistant that answers employee questions using company documents with citations.

### Requirements

- Answers should be grounded in internal knowledge.
- Return citations and document links.
- Support permissions: users should only see docs they can access.
- Latency target around 2–5 seconds for interactive chat.

### API sketch

```json
POST /chat
{
  "conversation_id": "c_123",
  "message": "What is our parental leave policy?"
}

Response:
{
  "answer": "...",
  "citations": [
    {"doc_id": "hr_policy_2026", "title": "Leave Policy", "chunk_id": "..."}
  ],
  "confidence": "medium",
  "trace_id": "tr_abc"
}
```

### High-level design

```text
  Document sources -> ingestion pipeline -> chunking -> embeddings -> vector index
          |                                                    |
          |                                                    v
          +---------------------- metadata / ACLs --------> retriever

  User query -> API -> auth -> query rewrite (optional) -> retrieve top-k docs
             -> rerank (optional) -> prompt builder -> LLM -> answer + citations
             -> logs / feedback / eval
```

### Key components

- **Ingestion pipeline:** pulls docs from Drive, Confluence, PDFs, tickets, wiki.
- **Parsing/chunking:** split documents into useful chunks with metadata.
- **Embedding/indexing:** create embeddings and store them in vector DB.
- **Metadata filters:** enforce team, role, or document ACLs at retrieval time.
- **Retriever + reranker:** retrieve top-k chunks, optionally rerank for relevance.
- **Prompt builder:** inject user question + selected context + style rules.
- **LLM response:** generate grounded answer with citations.

### Ingestion details

```text
  connectors
    |  (Drive, Confluence, SharePoint, S3, Git, tickets)
    v
  parse / OCR / clean
    |
    v
  chunk by structure
    |  title, heading path, owner, ACL, timestamp
    v
  embed chunks
    |
    +--> vector index
    +--> keyword index
    +--> metadata store
    +--> dead-letter queue for parse failures
```

### Retrieval stack

| Layer | Purpose | Notes |
| --- | --- | --- |
| Query rewrite | Turn follow-up into standalone query | Use conversation summary, not entire chat history |
| Hybrid retrieval | Combine semantic and keyword search | Handles acronyms, names, exact policy terms |
| ACL filtering | Prevent unauthorized chunks | Filter during retrieval, not after answer generation |
| Reranking | Improve top-k precision | Useful when corpus is large/noisy; adds latency |
| Context packing | Fit best evidence into token budget | Dedupe, order by relevance, preserve headings |

### Trade-offs to mention

- **Pure fine-tuning vs RAG:** RAG is better when knowledge changes frequently.
- **Latency vs quality:** reranking improves relevance but adds delay.
- **Chunk size:** too small loses context; too large hurts retrieval precision.
- **Freshness:** need incremental indexing or event-driven reindexing.

### RAG evaluation

| Metric | Question it answers |
| --- | --- |
| Retrieval recall@k | Did we retrieve the document that contains the answer? |
| Context precision | Are the retrieved chunks actually relevant? |
| Faithfulness / groundedness | Is the answer supported by retrieved context? |
| Answer relevance | Did the answer address the user's question? |
| Citation accuracy | Do links point to the evidence actually used? |
| Permission leakage rate | Did unauthorized content appear? |

### RAG failure modes

- **Missing document:** connector or index freshness problem.
- **Bad chunking:** answer spans chunks or tables were parsed poorly.
- **Wrong retrieval:** embedding misses exact keyword or acronym.
- **Lost context:** relevant chunk retrieved but dropped during context packing.
- **Hallucinated synthesis:** model answers beyond supplied context.
- **ACL bug:** retrieval sees data the user cannot access.

  Good interview line:
  I would keep ingestion and indexing offline, and keep the online path limited to auth, retrieval, prompt construction, generation, and response validation. That keeps latency predictable while allowing the knowledge base to evolve independently.

---

## Part 5 — Example: design an agentic workflow system **EXAMPLE**

### Goal

Design an AI system that can analyze a support ticket, fetch account data, query internal tools, propose a resolution, and optionally take approved actions.

### High-level design

```text
  Ticket / user request
        -> orchestrator
            -> planner / policy layer
            -> tool registry
            -> identity / permissions
            -> memory / state store
            -> LLM reasoning loop
            -> action executor
        -> human approval (for sensitive actions)
        -> final response + audit log
```

### Agent state-machine view

```text
  START
    |
    v
  understand goal
    |
    v
  plan steps ---- invalid/unsafe ----> refuse or ask human
    |
    v
  execute next tool
    |
    +--> tool failed? -> retry / alternate / escalate
    |
    +--> needs approval? -> pause -> human approves/denies
    |
    v
  update task state
    |
    +--> done? no -> execute next tool
    |
    v
  final answer + audit log
```

### What the interviewer wants to hear

- **Tool use is constrained:** the model should not have unrestricted access.
- **State is explicit:** task state, tool outputs, retries, and memory are stored outside the model.
- **Approval gates exist:** high-risk actions need human confirmation.
- **Observability matters:** trace every tool call, prompt, result, and failure.

### Key design choices

| Choice | Recommended answer |
| --- | --- |
| Planning | Use structured plans or state-machine/graph workflow, not free-form endless loops |
| Tool access | Allowlisted tools with schemas, auth, and timeout budgets |
| Memory | Session memory for current task, long-term memory only if it adds clear value |
| Action safety | Human-in-the-loop for money movement, deletions, account changes |
| Retries | Idempotent actions, bounded retries, circuit breakers |

### Tool contracts

Tools should be typed, narrow, permission-aware, and observable. Avoid giving the model broad tools like `run_sql(any_query)` or `http_request(any_url)` unless heavily sandboxed.

```json
{
  "name": "create_refund_case",
  "description": "Open a refund review case. Does not issue refund.",
  "input_schema": {
    "customer_id": "string",
    "order_id": "string",
    "reason": "string",
    "evidence_ids": ["string"]
  },
  "requires_approval": false,
  "timeout_ms": 2000,
  "idempotency_key": "conversation_id + order_id"
}
```

### Agent observability

- Plan version and generated steps
- Tool selected, arguments, result, latency, error
- Permission decision and policy version
- Human approval decision and reviewer
- Loop count, token usage, total cost
- Final action IDs and rollback/compensation status

### Big risk

The main failure mode is not just hallucination — it is **incorrect action**. So the architecture should emphasize permissions, validation, and reversible workflows more than just answer quality.

> **⚠️ WARN: Interview trap**
> Do not design an agent as an infinite loop around an LLM. A production answer needs bounded iterations, state persistence, typed tools, policy checks, approval gates, idempotency, and traceability.

---

## Part 6 — Example: design a recommendation system **EXAMPLE**

### Goal

Recommend products, videos, or jobs personalized to each user.

### Standard two-stage architecture

```text
  User activity / item metadata / context
        -> feature pipelines
        -> candidate generation
        -> top-N candidates
        -> ranking model
        -> final recommendations
        -> feedback loop (clicks, dwell, purchases)
```

### Expanded recommendation architecture

```text
  OFFLINE
    events + catalog + user profiles
        -> feature pipelines
        -> embeddings / co-visitation / popularity tables
        -> candidate indexes
        -> train ranking model
        -> offline eval + model registry

  ONLINE
    user request
        -> fetch user/context features
        -> candidate generators in parallel
             - similar items
             - personalized ANN
             - trending/popular
             - business rules
        -> merge + dedupe + filter
        -> ranker
        -> diversity/exploration rules
        -> recommendations
        -> impression/click/purchase logs
```

### Why two-stage

You usually cannot score millions of items with an expensive model on every request. So you:

1. **Generate candidates** quickly using retrieval/ANN/heuristics/co-visitation.
2. **Rank candidates** with a stronger model using richer features.

### Data sources

- User profile and history
- Item metadata
- Context features: time, device, location, session intent
- Feedback labels: clicks, likes, watch time, purchases

### Candidate generation strategies

| Strategy | Good for | Weakness |
| --- | --- | --- |
| Popularity/trending | Cold start, robust fallback | Not personalized |
| Collaborative filtering | Users/items with interaction history | Weak for new users/items |
| Content similarity | New items with metadata/text/images | Can be narrow/repetitive |
| Embedding ANN | Large catalog semantic matching | Needs embedding quality and index freshness |
| Rules/business candidates | Promotions, compliance, inventory constraints | Can hurt relevance if overused |

### Ranking features

- **User features:** preferences, historical categories, price sensitivity, language.
- **Item features:** category, age, quality score, inventory, creator/seller reputation.
- **Interaction features:** user-item similarity, previous impressions, recency.
- **Context features:** time, device, location, session query, entry surface.
- **Business/safety features:** blocked categories, availability, policy flags.

### Production points to mention

- **Cold start:** new users and new items need fallback strategies.
- **Freshness:** trending items may need stream updates.
- **Exploration vs exploitation:** do not overfit to existing popular items only.
- **Bias/fairness:** recommendations can amplify popularity and creator imbalance.

### Recommendation metrics

| Metric | Use |
| --- | --- |
| Precision@k / Recall@k | Offline relevance quality |
| NDCG@k | Ranking quality with position weighting |
| CTR / conversion / watch time | Online product impact |
| Diversity / novelty | Avoid repetitive recommendations |
| Coverage | How much of catalog gets exposure |
| Guardrail metrics | Policy violations, unfair exposure, spam/abuse |

  Good interview line:
  I would separate offline feature generation and model training from online candidate retrieval and ranking. For online serving, I would cache partial results for heavy users and keep a simple popularity-based fallback path if the personalized ranker is unavailable.

---

## Part 7 — Example: design a fraud / anomaly detection system **EXAMPLE**

### Goal

Detect suspicious transactions in near-real-time and block or review them.

### Architecture

```text
  Transaction event stream
        -> stream ingestion
        -> online feature enrichment
        -> rules engine + ML risk model
        -> risk score / decision
        -> approve | challenge | block | manual review
        -> investigator tools + feedback labels
        -> retraining pipeline
```

### Fraud latency path

```text
  transaction request
      |
      v
  synchronous path, must be fast:
    validate -> online features -> rules + model -> decision
                                               |
                                               v
                               approve / challenge / block

  async path, can be slower:
    event stream -> graph features -> case linking -> investigator UI
                 -> confirmed labels -> retrain / rule tuning
```

### Good answer themes

- **Hybrid system:** rules + ML, not ML alone.
- **Feature freshness:** recent counts, recent devices, recent geos matter.
- **Low latency:** online scoring often must finish in tens or hundreds of milliseconds.
- **Human feedback loop:** investigator decisions create new labels.
- **Explainability:** risk reasons should be visible to analysts.

### Useful fraud features

- Transaction amount compared with user baseline
- Velocity: number/amount of transactions in last 1 min, 1 hour, 24 hours
- Device fingerprint and device age
- Geo distance from last known location
- Merchant/category risk
- Account age and recent profile changes
- Graph signals: shared device, shared card, shared address, suspicious cluster

### Modeling approach

| Layer | Purpose |
| --- | --- |
| Rules | Hard constraints, known attack patterns, compliance requirements |
| Supervised model | Risk score from labeled historical fraud/non-fraud |
| Anomaly model | Catch unusual behavior without labels |
| Graph features | Detect coordinated behavior and shared entities |
| Manual review | Handle uncertain cases and generate labels |

### Trade-off

False positives hurt customers, false negatives cost money. A mature design may have multiple thresholds: auto-approve low risk, manual-review medium risk, auto-block very high risk.

```text
  risk score
  0.0 ------------------------------------------------------ 1.0
       approve        challenge / review          block
       low friction   gather more signal          high confidence

  Tune thresholds by business cost:
    false positive cost = angry customer / lost sale
    false negative cost = fraud loss / abuse / compliance risk
```

---

## Part 8 — Example: design real-time voice AI **EXAMPLE**

### Goal

Build a voice assistant that supports live conversation with low perceived latency.

### High-level design

```text
  Audio input
    -> streaming ASR
    -> partial transcript
    -> dialogue manager / LLM
    -> tool calls (optional)
    -> response text
    -> streaming TTS
    -> audio output
```

### Voice session architecture

```text
  client microphone
      |
      v
  audio gateway / WebRTC
      |
      +--> voice activity detection
      +--> streaming ASR partials
               |
               v
          dialogue manager
               |
               +--> short-term conversation state
               +--> tool calls / retrieval
               +--> LLM response stream
               |
               v
          streaming TTS
               |
               v
          client speaker

  side channels:
    transcripts -> logs/evals
    latency metrics -> monitoring
    consent/PII policy -> governance
```

### Critical points

- **Streaming everywhere:** ASR, model output, and TTS should stream.
- **Turn-taking:** interruption handling and barge-in matter a lot.
- **Latency budget:** break down ASR, reasoning, tool calls, and TTS.
- **Fallbacks:** if one model is slow, use a smaller one or shorter response mode.

### Voice hard parts

| Problem | Design response |
| --- | --- |
| Barge-in | Allow user to interrupt TTS; cancel current generation and update state |
| Partial transcripts | Use stable partials for early intent, wait for final transcript for risky actions |
| Noisy audio | Noise suppression, confidence thresholds, clarification prompts |
| Tool latency | Give short acknowledgement, run tool, stream final answer |
| Privacy | Consent, retention policy, PII redaction in transcripts |

### Example latency budget

| Stage | Target |
| --- | --- |
| Streaming ASR partials | 100–300 ms |
| Dialogue/model first token | 300–800 ms |
| TTS start | 200–500 ms |
| Total perceived response start | For voice, perceived responsiveness often matters more than final full-answer quality.

---

## Part 8.5 — More common interview blueprints **EXAMPLE**

### Blueprint: document processing / extraction

Prompt: "Design a system that extracts structured fields from invoices, contracts, or medical forms."

```text
  document upload
      -> object store
      -> OCR / layout parser
      -> document classifier
      -> field extractor model / LLM
      -> schema validation
      -> confidence scoring
      -> human review for low confidence
      -> structured record + audit trail
```

- **Key trade-off:** automation rate vs extraction accuracy.
- **Hard part:** tables, handwriting, scans, domain-specific fields, hallucinated values.
- **Metrics:** field-level precision/recall, exact-match rate, review rate, turnaround time.
- **Safety:** never invent missing fields; mark unknown with confidence.

### Blueprint: semantic search

Prompt: "Design search over a large internal knowledge base or product catalog."

```text
  query
    -> query understanding / spell correction / filters
    -> hybrid retrieval
         + keyword index
         + vector index
         + business filters
    -> reranker
    -> snippet/highlight generation
    -> results page
    -> click logs + query reformulation analytics
```

- **Key trade-off:** exact keyword precision vs semantic recall.
- **Hard part:** ranking, freshness, permissions, synonyms, acronyms.
- **Metrics:** NDCG, MRR, zero-result rate, click-through, reformulation rate.

### Blueprint: content moderation

Prompt: "Design an AI system to detect harmful or policy-violating content."

```text
  user content
      -> lightweight rule checks
      -> ML classifier / moderation model
      -> policy decision engine
          | low risk      -> allow
          | uncertain     -> queue for review
          | high risk     -> block / limit distribution
      -> reviewer feedback
      -> policy + model updates
```

- **Key trade-off:** safety vs false positives and creator/user trust.
- **Hard part:** context, adversarial language, policy changes, multilingual content.
- **Metrics:** precision/recall by policy category, appeal overturn rate, review latency.
- **Safety:** policy versioning and explainable enforcement decisions.

### Blueprint: personalized copilot

Prompt: "Design a copilot that personalizes answers based on user history and preferences."

```text
  user request
      -> identity + consent check
      -> retrieve user profile / preferences
      -> retrieve task context
      -> assemble minimal personalized prompt
      -> model response
      -> user feedback
      -> memory write policy
           - what to store?
           - for how long?
           - can user inspect/delete it?
```

- **Key trade-off:** helpful personalization vs privacy and surprise.
- **Hard part:** stale memories, wrong assumptions, sensitive attributes.
- **Metrics:** task success, user correction rate, memory usefulness, deletion requests.

### Blueprint: demand forecasting

Prompt: "Design a system that forecasts demand, traffic, or inventory needs."

```text
  historical events + calendar + promotions + external signals
      -> data validation
      -> feature generation
      -> forecasting model
      -> prediction intervals
      -> business constraints / overrides
      -> dashboard + API
      -> actuals arrive later
      -> backtesting + drift monitoring
```

- **Key trade-off:** model complexity vs interpretability and stability.
- **Hard part:** seasonality, promotions, holidays, sparse products, cold starts.
- **Metrics:** MAPE, WAPE, RMSE, calibration of prediction intervals.

---

## Part 9 — Safety, evaluation, observability, and cost **★ CORE**

### Evaluation

- **Offline evals:** benchmark datasets, replay sets, golden prompts, ranking metrics.
- **Online evals:** A/B tests, user satisfaction, conversion, resolution rate.
- **Human review:** especially for correctness, harmful outputs, and action safety.

### Layered evaluation

Evaluate each layer separately, then evaluate the full end-to-end system. This helps you localize failures.

```text
  input quality eval
        |
        v
  retrieval / feature eval
        |
        v
  model output eval
        |
        v
  policy / safety eval
        |
        v
  product outcome eval

  Example RAG failure:
    bad answer could be retrieval failure, prompt failure,
    model failure, citation failure, or stale source data.
```

### Eval dataset design

| Slice | Why include it |
| --- | --- |
| Common happy path | Protect core user experience |
| Edge cases | Catch rare but important failures |
| Adversarial prompts | Test prompt injection, jailbreaks, unsafe requests |
| Permission cases | Ensure users cannot access forbidden content |
| Freshness cases | Verify recently changed docs/features are reflected |
| Regression cases | Examples from previous production failures |

### LLM-as-judge

LLM judges are useful for scale, but they need calibration. Use explicit rubrics, spot-check with humans, and keep judge prompts/versioning stable.

```
Rubric example:
Score 1-5 on faithfulness.
5 = every claim is directly supported by supplied evidence.
3 = mostly supported, but some vague or weakly supported claims.
1 = answer contradicts evidence or invents important facts.
```

> **⚠️ WARN: Eval warning**
> Never rely only on aggregate eval scores. Segment by query type, user group, language, document source, risk level, and model version. Many serious regressions hide inside a good-looking average.

### Observability

In AI systems, logs are not enough. You usually want:

- request traces
- model chosen
- prompt/version
- retrieved context IDs
- tool calls and durations
- token usage / compute cost
- user feedback and failure labels

### Observability diagram

```text
  request trace
    span: api
    span: auth
    span: retrieval
      attributes: index_version, top_k, doc_ids, scores
    span: reranker
    span: model_call
      attributes: model, prompt_version, tokens_in, tokens_out, cost
    span: guardrails
      attributes: policy_version, decision
    span: tool_call(s)
    span: response

  dashboards:
    latency p50/p95/p99
    cost per route/user/team
    error and fallback rate
    eval quality over time
    drift / freshness / stale index alerts
```

### Safety and governance

- PII detection and redaction
- content moderation
- policy enforcement for actions and data access
- audit logs for regulated workflows
- dataset and model versioning

### Safety layers

```text
  user input
      |
      v
  input checks
    - prompt injection
    - harmful request
    - PII / secrets
    - authorization
      |
      v
  model / agent / tool execution
      |
      v
  output checks
    - groundedness
    - PII leakage
    - policy violation
    - schema validation
      |
      v
  action gate
    - auto-allow
    - human approval
    - refuse
      |
      v
  audit log
```

### Cost controls

- cache common responses or retrieved context
- route easy queries to smaller/cheaper models
- use async pipelines for heavy jobs
- truncate irrelevant context
- batch where possible

### Cost breakdown

| Cost source | Controls |
| --- | --- |
| LLM input tokens | Context pruning, prompt compression, retrieval precision |
| LLM output tokens | Concise modes, streaming stop conditions, answer length limits |
| Multiple model calls | Routing, caching, fewer agent loops, batch evals offline |
| Vector/search infrastructure | Index compaction, quantization, TTLs for transient data |
| Human review | Confidence thresholds, active learning, reviewer tooling |
| GPU serving | Batching, quantization, autoscaling, smaller model distillation |

> **⚠️ WARN: A common weak answer**
> Saying "we'll just use GPT-4 for everything" is not a system design answer. A strong answer includes model routing, fallback behavior, caching, observability, and evaluation strategy.

---

## Part 10 — Final interview checklist **★ CORE**

- Did I clarify the product goal and risk level?
- Did I identify whether the system is predictive, retrieval-based, generative, or agentic?
- Did I separate offline pipelines from online serving?
- Did I name the main stores: operational DB, object store, vector/search index, cache?
- Did I cover latency, scale, and fallback behavior?
- Did I mention evaluation, feedback loops, and drift?
- Did I address safety, permissions, and auditability?
- Did I explain at least one concrete trade-off?

### A good closing answer

To summarize, I would start with a simple reliable baseline, keep expensive processing off the online path, use the smallest model that meets quality needs, add monitoring and human review for risky decisions, and evolve the system through offline evals plus controlled online experiments.

> **💡 TIP: How to practice**
> Practice giving the same structure across 5–6 prompts: RAG assistant, recommendation engine, fraud detection, support copilot, voice assistant, and autonomous agent workflow. Repetition makes your interview answers feel senior and calm.

