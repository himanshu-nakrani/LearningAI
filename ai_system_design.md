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
- [Part 1.7 — LLM inference internals every interviewer expects](#part-1-7)
- [Part 2 — Core trade-offs interviewers expect](#part-2)
- [Part 2.5 — Retrieval, embeddings, and reranking choices](#part-2-5)
- [Part 3 — Generic AI architecture template](#part-3)
- [Part 3.5 — Data, model, and deployment lifecycle](#part-3-5)
- [Part 3.7 — AI gateway, model routing, and multi-tenancy](#part-3-7)
- [Part 4 — Example: design a RAG assistant](#part-4)
- [Part 5 — Example: design an agentic workflow system](#part-5)
- [Part 6 — Example: design a recommendation system](#part-6)
- [Part 7 — Example: design a fraud / anomaly detection system](#part-7)
- [Part 8 — Example: design real-time voice AI](#part-8)
- [Part 8.5 — More common interview blueprints](#part-8-5)
- [Part 9 — Safety, evaluation, observability, and cost](#part-9)
- [Part 9.5 — GPU capacity planning and inference economics](#part-9-5)
- [Part 10 — Final interview checklist](#part-10)
- [Part 11 — Question catalog with approach hints](#part-11)
- [Part 12 — Anti-patterns that fail AI system design interviews](#part-12)
- [Part 13 — Training infrastructure at scale](#part-13)
- [Part 13.5 — Advanced inference: MoE, long context, reasoning models](#part-13-5)
- [Part 14 — Leadership scenarios for Lead/Staff/Principal rounds](#part-14)
- [Part 15 — Behavioral story bank (STAR scaffolds)](#part-15)
- [Part 16 — Post-mortem case studies](#part-16)

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

## Part 1.7 — LLM inference internals every interviewer expects **★ CORE**

For senior AI system design rounds, interviewers expect you to talk about LLM serving with the same fluency you would talk about database indexes. You do not need to derive attention from scratch, but you do need to explain the runtime cost shape, how serving frameworks exploit it, and how those properties show up in your design.

### Prefill vs decode: the two phases that drive everything

An LLM forward pass during generation has two distinct phases with different cost shapes. Almost every serving optimization is about exploiting this asymmetry.

```text
  PREFILL (process the prompt)              DECODE (generate tokens, one at a time)
  -------------------------------            -----------------------------------------
  parallel over all input tokens             sequential, one token per step
  compute-bound (matmul heavy)               memory-bandwidth-bound (load KV cache)
  good GPU utilization                       low GPU utilization unless batched
  cost ~ O(N_in)                             cost ~ O(N_out) per request
  affects: time-to-first-token (TTFT)        affects: tokens-per-second (TPS / TPOT)
```

| Metric | What it measures | User-visible effect |
| --- | --- | --- |
| TTFT (time to first token) | Prefill time + queueing + first decode step | How "snappy" the response feels |
| TPOT (time per output token) | Inverse of decode throughput per request | How fast the answer streams |
| End-to-end latency | TTFT + N_out * TPOT | Total wait for a complete answer |
| Throughput (tokens/sec/GPU) | Aggregate across all concurrent requests | Cost per million tokens |

### KV cache: why it dominates memory

During autoregressive decoding, attention needs the keys and values of every prior token. Recomputing them each step would be quadratic, so they are cached. The KV cache is the largest dynamic memory consumer on the GPU during inference, and it scales with *tokens in flight*, not parameter count.

```text
  KV cache size per request:
    2 * n_layers * n_heads * head_dim * seq_len * dtype_bytes

  Concrete example (Llama-like, 70B class):
    n_layers = 80, n_kv_heads = 8, head_dim = 128, dtype = fp16 (2 bytes)
    per token:  2 * 80 * 8 * 128 * 2 = ~320 KB / token
    8k context: ~2.5 GB per request just for KV cache

  Why it matters in design:
    batch size at serving time is gated by KV memory, not FLOPs.
    longer contexts -> fewer concurrent users per GPU -> higher cost/token.
```

### Batching strategies

| Strategy | How it works | Trade-off |
| --- | --- | --- |
| Static batching | Wait for N requests, run them together to completion | Easy, but slow requests block fast ones (head-of-line blocking) |
| Dynamic batching | Bucket by length, flush on timer or size | Better utilization, still suffers from variable output length |
| Continuous batching (in-flight) | New requests join the batch every decode step; finished requests leave | Standard for vLLM, TensorRT-LLM, TGI; 2–10x throughput gain |
| Chunked prefill | Split long prompts into chunks interleaved with decode steps of other requests | Keeps decode latency low while serving long-context prefills |

### Paged attention and memory fragmentation

Naive KV cache allocates one contiguous block per request sized to `max_seq_len`, wasting most of it. Paged attention (vLLM) treats KV cache like virtual memory: small fixed-size blocks, allocated on demand, addressed by a per-request block table. Result: 2–4x more concurrent requests on the same GPU.

```text
  Without paging:                       With paged attention:
  [Req A: 8192 reserved | used 200 ]    blocks: [A0][B0][A1][C0][B1][A2]...
  [Req B: 8192 reserved | used 100 ]    A's table: [0, 2, 5, ...]
  [Req C: 8192 reserved | used 50  ]    B's table: [1, 4, ...]
                                        C's table: [3, ...]

  internal fragmentation high           internal fragmentation ~ 1 block / req
  rejects requests early                packs many short requests densely
```

### Speculative decoding

A small "draft" model proposes K tokens; the large "verifier" model checks them in one forward pass and accepts the longest matching prefix. Net effect: decode throughput goes up because the expensive model does fewer sequential steps. Acceptance rate determines the speedup (typical 2–3x for similar-distribution drafters).

```text
  draft model (small) -> proposes: "the cat sat on the"
  target model (big)  -> verifies all 5 in parallel
                         accepts "the cat sat on" (4), rejects "the", resamples 5th

  Variants:
    - Medusa heads (extra heads on the same model predict multiple tokens)
    - EAGLE (uses target model's hidden state to draft)
    - Lookahead decoding (no draft model, uses Jacobi iteration)
```

### Quantization choices

| Format | Bits | When to use | Caveat |
| --- | --- | --- | --- |
| FP16 / BF16 | 16 | Default for training and high-quality inference | BF16 has wider range, better for training stability |
| FP8 (E4M3 / E5M2) | 8 | H100/H200 inference for new training runs | Requires recent hardware and calibration |
| INT8 (SmoothQuant, W8A8) | 8 | 2x throughput on most GPUs, small quality drop | Outlier channels need handling |
| INT4 (GPTQ, AWQ) | 4 weight / 16 act | Fits 70B on a single 80GB GPU; on-device deploys | Weight-only; activations stay fp16 |
| KV cache quant (FP8 / INT4) | varies | Doubles concurrent requests at long context | Long-context tasks regress more |

### Distributed inference parallelism

- **Tensor parallel (TP):** shard each layer's matmuls across GPUs in a node. Low latency, high bandwidth required (NVLink). Used for models that don't fit on one GPU.
- **Pipeline parallel (PP):** split layers across nodes. Higher latency but cheaper interconnect; usually combined with TP, not used alone for serving.
- **Expert parallel (EP):** for MoE models, route each expert to a different GPU. Activates only top-k experts per token; saves compute, increases routing/comm complexity.
- **Sequence/context parallel:** shard the sequence dimension; useful for very long context (>100k tokens).
- **Replication:** for throughput scaling, just replicate the whole model across GPUs and load-balance.

### Prefix caching

If many requests share a prefix (system prompt, few-shot examples, long document), reuse the KV cache for the shared portion across requests. Cuts TTFT dramatically for chat apps and RAG with stable system prompts. Most modern serving stacks (vLLM, TensorRT-LLM, SGLang) support this.

> **💡 TIP: Interview shortcut**
> When asked about LLM latency, lead with: "There are two phases — prefill (compute-bound, sets TTFT) and decode (memory-bound, sets TPOT). I'd optimize TTFT with prefix caching and chunked prefill, optimize TPOT with continuous batching and speculative decoding, and reduce KV memory with paged attention plus KV quantization to raise concurrency." That single sentence signals seniority.

### Serving stack choices

| Option | Best for | Note |
| --- | --- | --- |
| vLLM | Open-source default; paged attention + continuous batching | Strong throughput, broad model support |
| TensorRT-LLM | Maximum throughput on NVIDIA GPUs | Per-model engine build; less flexible |
| TGI (HuggingFace) | Easy ops, broad model support | Good for medium-scale production |
| SGLang | Programs/agents with shared prefixes, structured output | RadixAttention for prefix sharing |
| Hosted API (Anthropic / OpenAI / Bedrock) | You don't want to run GPUs at all | Pay per token; opaque latency variance |

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

## Part 2.5 — Retrieval, embeddings, and reranking choices **★ CORE**

Retrieval is where most production RAG systems succeed or fail. Interviewers want you to name specific algorithms and explain the trade-offs, not just say "use a vector DB."

### ANN index choices

| Index | How it works | When to pick | Caveats |
| --- | --- | --- | --- |
| Flat / brute force | Exact cosine/L2 over all vectors | < 100k vectors, or eval ground truth | O(N) per query; doesn't scale |
| HNSW (graph) | Layered proximity graph, greedy descent | General default; high recall at low latency | Memory hungry; rebuilds slow; updates degrade graph |
| IVF + PQ | Coarse cluster (IVF) then product-quantized codes | Very large corpora (100M+) where memory matters | Recall drops with aggressive quantization |
| ScaNN | Anisotropic quantization + tree search | Billion-scale, Google ecosystem | Less common outside Google stack |
| DiskANN / Vamana | Graph index on SSD | Vectors don't fit in RAM | Higher tail latency than in-memory |

### Vector database options

- **Postgres + pgvector:** small to medium corpora, transactional consistency with your app data. Easiest if you already run Postgres.
- **Elastic / OpenSearch:** hybrid keyword + vector in one index, mature ACL/aggregation story.
- **Pinecone / Weaviate / Qdrant / Milvus:** dedicated vector stores with managed sharding and replication; pick when scale outgrows pgvector or you need namespaces/multi-tenancy.
- **FAISS:** library, not a service. Wrap it in your own server when you need full control.
- **LanceDB / Chroma:** embedded; good for local agents and notebooks.

### Chunking strategies

| Strategy | Good for | Risk |
| --- | --- | --- |
| Fixed-size with overlap (e.g. 800 tok / 100 overlap) | Generic prose, default starting point | Cuts mid-sentence; loses structure |
| Recursive structural (by heading then paragraph) | Wiki, docs, contracts | Needs a good parser per format |
| Sentence-window | QA on dense text | Many small chunks; reranker becomes critical |
| Semantic chunking (cluster sentences by embedding distance) | Long-form articles, transcripts | Slower to ingest; non-deterministic |
| Page or row level | PDFs, tables, spreadsheets | One chunk may be much larger than others |
| Parent-child (small for retrieval, large for context) | When retrieval precision and context fullness conflict | Doubles storage |

### Bi-encoder vs cross-encoder

```text
  BI-ENCODER (used for retrieval)              CROSS-ENCODER (used for reranking)
  embed(query) and embed(doc) separately       feed [query; doc] together into model
  similarity = cosine(q_vec, d_vec)            output a relevance score directly
  fast: precompute doc vectors, ANN lookup     slow: must run per (q, d) pair
  use to fetch top-100 candidates              use to rerank top-100 -> top-5
  example: sentence-transformers, OpenAI       example: cohere-rerank, BGE-reranker,
           text-embedding-3, e5, bge                    monoT5, ColBERT (late-interact)
```

### Hybrid retrieval (almost always wins)

BM25 (sparse, keyword) and dense embeddings (semantic) have complementary failure modes. Combining them beats either alone on most enterprise corpora because acronyms, IDs, product codes, and rare names don't embed well.

```text
  query
    |
    +---> BM25 / keyword search  -> top-50 (sparse)
    +---> dense vector search    -> top-50 (semantic)
            |
            v
       fusion: RRF (reciprocal rank fusion) or weighted score
            |
            v
       reranker (cross-encoder) on top-50
            |
            v
       top-5 passed to LLM with citations
```

### Advanced RAG patterns worth naming

- **Query rewriting / decomposition:** turn "compare our PTO policy to Acme's" into two sub-queries.
- **HyDE (hypothetical document embedding):** ask the LLM to draft a hypothetical answer, embed that, use it as the retrieval query. Helps short queries with sparse vocabulary overlap.
- **Multi-vector / ColBERT-style:** store one vector per token (late interaction). Higher recall, much more storage.
- **Self-querying:** LLM emits a structured filter (date range, owner, doc type) alongside the semantic query, executed as metadata filter + vector search.
- **GraphRAG:** build an entity/relationship graph from the corpus offline; retrieve subgraphs for queries that need multi-hop reasoning ("who reports to the person who owns project X").
- **Contextual retrieval (prefix each chunk with a short LLM-generated summary of its surroundings):** cheap quality lift, popularized by Anthropic.

### Model adaptation menu (what's actually being tuned)

| Technique | What it changes | When to use | Trade-off |
| --- | --- | --- | --- |
| Prompting / few-shot | Nothing (inference only) | Fastest iteration; small behavior tweaks | Token cost grows with examples |
| RAG | Context, not weights | Knowledge changes frequently | Retrieval quality is the new bottleneck |
| Supervised fine-tuning (SFT) | All weights, full precision | Domain-specific style or skill | Expensive, needs labeled data |
| LoRA / QLoRA (PEFT) | Small adapter matrices; base frozen | Many narrow variants on one base model | Quality usually within a few % of full SFT |
| DPO / KTO / ORPO | Aligns to preference pairs | Tone, refusal behavior, safety nudges | Needs preference data, not just labels |
| RLHF / RLAIF | Optimizes against a reward model | Complex behaviors hard to describe by examples | Highest complexity; reward hacking risk |
| Distillation | Train smaller model on larger model's outputs | Cut serving cost after quality is solved | Caps at teacher quality on covered cases |
| Continued pretraining | Base weights, on raw domain text | Truly new vocabulary or modality | Most expensive option |

> **💡 TIP: The ladder**
> In interviews, walk up this ladder: "Start with prompting + RAG. If style/format is the problem, do LoRA SFT. If tone/safety is the problem, layer DPO. Only do full fine-tuning or continued pretraining if those fail." This sequencing is what staff-level candidates say.

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

## Part 3.7 — AI gateway, model routing, and multi-tenancy **★ CORE**

Any non-trivial AI product ends up putting a gateway between application code and model providers. Interviewers asking "how would you scale this across the company?" expect you to describe this layer.

### Gateway responsibilities

| Responsibility | Why it lives here |
| --- | --- |
| Provider abstraction | Swap Anthropic/OpenAI/Bedrock/in-house without changing app code |
| Auth and key vaulting | App services hold app credentials; provider keys never leak past the gateway |
| Per-tenant quotas and rate limits | Stops one team or customer from exhausting org-level rate limits |
| Cost attribution | Token usage tagged by team, feature, environment for chargeback |
| Caching | Exact-match and semantic cache for popular prompts |
| Prompt and policy enforcement | Inject system prompts, redact PII, enforce content policies centrally |
| Observability | Trace IDs, token counts, latencies, retries, fallbacks in one place |
| Failover and circuit breaking | If primary provider degrades, route to secondary; trip circuit on error rate |

### Gateway architecture

```text
  application services
        |
        v
  AI GATEWAY
    auth + tenant resolution
    request shaping (prompt template, redaction)
    cache lookup
        |  miss
        v
    model router
      +--- by intent (cheap classifier on prompt)
      +--- by cost budget for this tenant
      +--- by latency SLO (small model if user is waiting)
      +--- by capability (only some models do tool use, vision, JSON mode)
        |
        v
    provider client(s)        --->  OpenAI / Anthropic / Bedrock / vLLM cluster
        |
        v
    response normalization (unified schema, token usage, finish reasons)
        |
        v
    output guardrails
        |
        v
    cache write + audit log + metrics
        |
        v
    application

  side outputs:
    - usage events -> billing/metering
    - traces -> observability backend
    - flagged outputs -> review queue
```

### Caching tiers

- **Exact-match cache:** hash of (model, prompt, params). High hit rate on repeated tool prompts and system messages.
- **Semantic cache:** embed the query, look up nearest cached queries above a similarity threshold. Risky for personalized or stateful answers; great for FAQ-like traffic.
- **Provider-side prompt cache:** Anthropic/OpenAI/Bedrock all expose a cache-breakpoint mechanism that reuses KV for stable prefixes; often the biggest single cost win for chat apps and agents.
- **Retrieval cache:** memoize embedding + retrieval results for identical queries within a TTL.

> **💡 TIP: Cache layering rule**
> When asked to cut LLM cost, name the layers in order: exact-match → provider prompt cache → retrieval cache → semantic cache → distillation to a smaller model. Each layer is cheaper to build than the next and usually buys 20–60% on its own.

### Multi-tenancy patterns

| Concern | Design choice |
| --- | --- |
| Data isolation | Per-tenant index/namespace in vector DB; row-level security in feature/profile stores; per-tenant encryption keys for regulated data |
| Compute isolation | Shared model pool for most; dedicated endpoints for noisy/regulated tenants; separate clusters for "BYOC" deployments |
| Quota fairness | Token-bucket per tenant with burst allowance; global circuit breaker for provider-level limits |
| Prompt isolation | Never concatenate tenant-supplied text into another tenant's system prompt; treat user text as data, not instructions |
| Model selection | Allowlist of models per tenant (some can't use frontier models for data-residency reasons) |
| Audit and retention | Per-tenant retention policy; signed audit logs for regulated industries |

### Rate limiting in token-shaped traffic

Standard request-per-second limits don't fit LLMs because a single request can consume 100x more tokens than another. Use **token-per-minute** (TPM) and **requests-per-minute** (RPM) buckets together, mirroring how provider APIs charge.

```text
  on request:
    estimate input_tokens (count locally) + max_output_tokens (param)
    check: tenant TPM bucket has capacity?
    check: tenant RPM bucket has capacity?
    check: global provider TPM has capacity?
        any miss -> 429 with retry-after, or fall through to smaller/cheaper model

  on response:
    refund unused output tokens (we reserved max, used less)
    record actual usage for billing
```

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

### Blueprint: code copilot / IDE assistant

Prompt: "Design an IDE autocomplete and chat assistant like Copilot or Cursor."

```text
  IDE event (keystroke / chat / accept)
      -> client-side debounce + context window builder
           - current file (cursor +/- N lines)
           - open tabs, recently edited files
           - repo-level retrieval (BM25 over symbols + embedding over chunks)
           - LSP signals (types, definitions, diagnostics)
      -> server: prompt assembly + speculative cache lookup
      -> small fast model (FIM-trained) for completions
         large model for chat / refactor
      -> stream tokens back
      -> client: ghost-text render, telemetry on accept/reject
      -> offline: train acceptance reward model, retrain ranker
```

- **Key trade-off:** latency vs context size; completions need ~200ms TTFT or users disable the feature.
- **Hard part:** repo context selection (which files to send), FIM (fill-in-the-middle) prompt format, deduping low-value suggestions.
- **Metrics:** accept rate, retained-in-IDE-after-N-seconds, characters-per-accepted-suggestion, server cost per accept.
- **Safety:** license-aware filtering of training and outputs; never echo secrets pasted into prompt.

### Blueprint: image generation service

Prompt: "Design a text-to-image generation service like Midjourney or DALL-E."

```text
  prompt + style + reference image (optional)
      -> safety: prompt classifier (CSAM, IP, named persons)
      -> prompt rewriter (expand style, add negative prompts)
      -> queue (image gen is seconds-to-minutes, not interactive)
      -> GPU worker pool (batched diffusion)
           - choose model variant by tier (fast / quality)
           - apply LoRAs / control nets if requested
      -> output safety: NSFW classifier, watermark, C2PA signing
      -> object store + CDN
      -> notify client (websocket / poll)
      -> feedback: upvotes, regenerations, reports
```

- **Key trade-off:** latency (steps, resolution) vs quality vs GPU cost.
- **Hard part:** async UX (long jobs), abuse prevention, copyright and likeness policy, GPU spot-instance reliability.
- **Metrics:** queue wait, success rate, regeneration rate, safety filter precision/recall.

### Blueprint: multimodal document understanding

Prompt: "Design a system that answers questions over PDFs that include text, tables, and figures."

```text
  PDF upload
      -> layout parser (Mathpix / Unstructured / proprietary)
           - text blocks + reading order
           - table extraction -> structured rows
           - figure crops -> stored separately
      -> per-element embeddings
           - text -> text embedding
           - figure -> CLIP / vision-language embedding
           - table -> serialized cells + text embedding
      -> index (vector + metadata: page, element type)
      -> query path: hybrid retrieval -> rerank -> VLM
         (vision-language model sees crops + text together)
      -> answer with element-level citations (page, bbox)
```

- **Key trade-off:** parsing fidelity vs ingestion latency and cost.
- **Hard part:** tables that span pages, figure-text alignment, multi-column layouts, handwritten annotations.
- **Metrics:** answer accuracy stratified by element type, table-cell exactness, bbox citation precision.

### Blueprint: ads / sponsored content ranking

Prompt: "Design a system that ranks ads for a feed or search results page."

```text
  request (user, context, query/feed slot)
      -> retrieval: targeting filters (campaign, budget remaining, eligibility)
      -> candidate generation: bidding-aware ANN over ad embeddings
      -> pCTR / pCVR model (online inference, strict latency budget)
      -> auction: bid * pCTR * quality_score (eCPM ranking)
      -> pacing / budget controller (offline + online feedback)
      -> impression logging, attributed conversions
      -> offline: train pCTR, calibrate, detect click fraud, fairness audits
```

- **Key trade-off:** revenue (eCPM) vs user experience vs advertiser ROI.
- **Hard part:** calibration of pCTR (must reflect true probability, not just rank well), budget pacing, position bias in training data.
- **Metrics:** revenue per mille (RPM), CTR, advertiser ROAS, calibration error, budget utilization.

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

## Part 9.5 — GPU capacity planning and inference economics **★ CORE**

If the interviewer asks "how many GPUs?" or "what does this cost at 1M users?", they want a back-of-envelope grounded in real numbers. Memorize a few anchor figures and a derivation pattern.

### Anchor figures to remember (2025-era)

| GPU | VRAM | Mem BW | Rough use |
| --- | --- | --- | --- |
| A100 80GB | 80 GB HBM2e | ~2 TB/s | 13B–70B serving (with TP); workhorse |
| H100 80GB | 80 GB HBM3 | ~3.4 TB/s | Frontier serving and training; FP8 support |
| H200 / B200 | 141 GB / 192 GB | 4.8+ TB/s | Frontier 100B+ models, very long context |
| L40S / L4 | 48 GB / 24 GB | ~864 GB/s / 300 GB/s | Cost-efficient inference for < 13B models, embedding |

### Memory budget on a single GPU

```text
  total VRAM (e.g. 80 GB)
    - model weights        (params * bytes_per_param)
    - activations          (small at inference)
    - KV cache             (the big variable)
    - framework overhead
  = headroom for concurrent requests

  example: 70B model, fp16 weights
    weights: 70e9 * 2  = 140 GB  -> needs TP across 2x80GB or quantize
    int4 weights: 70e9 * 0.5 = ~35 GB -> fits one 80GB, plenty of KV headroom

  example: 8B model, fp16 weights, 80GB GPU
    weights:  ~16 GB
    headroom: ~64 GB
    KV per token (Llama-3-8B):  ~128 KB
    at 8k context -> ~1 GB/req -> ~60 concurrent requests
```

### Throughput derivation pattern

```text
  Step 1: pick a target model and quantization
  Step 2: compute max concurrent requests = headroom / (KV per token * avg seq_len)
  Step 3: measure or look up tokens/sec/GPU at that concurrency
            (typical: 8B fp16 ~ 3-6k tok/s; 70B int4 ~ 1-2k tok/s on H100)
  Step 4: tokens/day = tok/s * 86,400
  Step 5: divide by tokens/day from workload estimate -> GPU count
  Step 6: multiply by ~1.5x for peak headroom and ~1.2x for failures/maintenance
```

### Worked example: chatbot at 1M DAU

```text
  Workload:
    1M DAU * 6 sessions/day * 4 turns * 800 output tokens = ~19B output tokens/day
    Plus input tokens ~3x output during prefill (but prefill is cheap with prefix cache)

  Serving choice: Llama-3-70B int4, H100, vLLM
    decode throughput per H100 ~= 1,500 tok/s in batched steady state
    daily tokens per H100      ~= 1,500 * 86,400 ~= 130M tokens

  GPUs needed for decode:
    19B / 130M ~= 146 H100s steady state
    peak (3x avg) -> 440 H100s, or burst to provider API for overflow

  Cost order of magnitude (rented H100 ~ $2-3/hr):
    146 * 24 * 2.5 ~= $8,760/day steady, ~$3.2M/year
    At $3 per million tokens hosted equivalent: 19B * $3/M = $57k/day
    Self-hosting wins at this scale; below ~10B tok/day, hosted is usually cheaper.

  Levers if budget is tight:
    - speculative decoding -> 1.5-2x throughput
    - smaller model for easy queries (router) -> 30-60% of traffic offloaded
    - prefix cache + answer cache -> 20-40% of input tokens skipped
    - distill 70B answers into 8B for narrow domains
```

> **💡 TIP: When to self-host**
> Rule of thumb: below ~5–10B tokens/day, the per-token cost of a hosted API beats running your own GPUs once you factor on-call, capacity headroom, and engineer time. Above that, self-hosting (or reserved cloud capacity) usually wins — and you also get latency, privacy, and customization control. Say this trade-off explicitly when asked "build vs buy."

### Autoscaling GPU workloads

- **Cold start is the enemy:** loading a 70B model takes 1–5 minutes. Pre-warm pools; don't scale to zero for latency-sensitive tiers.
- **Scale on tokens, not requests:** queue depth in tokens or expected decode-seconds is a better signal than HTTP RPS.
- **Right-size by tier:** separate pools for premium (low latency, low utilization) and batch (high utilization, queued).
- **Spot instances for batch and training only:** reclaim risk is unacceptable for synchronous serving unless you have hot standby capacity.

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

---

## Part 11 — Question catalog with approach hints **EXAMPLE**

These are the AI system design prompts that come up most often. For each, the first move is to disambiguate the goal and pick the pattern; the second move is to draw the online/offline split. The hints below are the headline trade-off the interviewer is looking for, not the full answer.

### Retrieval / LLM

| Prompt | Lead with |
| --- | --- |
| Design an internal "ask the docs" assistant | Hybrid retrieval + ACL-aware index; citations and faithfulness evals |
| Design ChatGPT / a consumer chatbot | Streaming, prefix cache, model routing, abuse mitigation at scale |
| Design a customer support copilot | RAG over tickets + KB; agent for actions; human-in-the-loop for refunds |
| Design "talk to your data" / NL-to-SQL | Schema retrieval, validated query generation, sandboxed execution, result summarization |
| Design a long-context summarization system | Map-reduce or hierarchical summarization; cite source spans; eval against human summaries |
| Design an enterprise search engine | Hybrid index, permission propagation, freshness pipeline, reranker |

### Agents and workflows

| Prompt | Lead with |
| --- | --- |
| Design an autonomous coding agent | Sandboxed execution, plan trees, tool typing, reversible actions, budget caps |
| Design a meeting assistant that books follow-ups | Calendar tools with approval gates, idempotent action keys, privacy of transcripts |
| Design a browser-using agent | DOM/screenshot dual signal, action allowlist, anti-exfiltration on tool outputs |
| Design a multi-agent orchestrator | Roles, message bus, deterministic supervisor, total cost cap, escape hatches |

### Classical ML / decisioning

| Prompt | Lead with |
| --- | --- |
| Design YouTube/TikTok video recs | Two-stage retrieval + ranker, watch-time vs engagement, exploration, freshness |
| Design news feed ranking | Multi-objective ranker, integrity signals, position-bias correction, rapid retraining |
| Design fraud detection | Rules + ML, online features, low latency, investigator feedback loop |
| Design Uber/DoorDash ETA | Real-time features, calibrated regression, geo-shard models, drift on weather/events |
| Design dynamic pricing | Elasticity models, business constraints, fairness audit, A/B with holdouts |
| Design ads ranking | pCTR calibration, eCPM auction, pacing, position bias, anti-fraud |

### Multimodal and media

| Prompt | Lead with |
| --- | --- |
| Design real-time voice AI | Streaming ASR/LLM/TTS pipeline, barge-in, sub-1.5s perceived response |
| Design a text-to-image service | Async job queue, GPU pool, prompt/output safety, watermarking |
| Design Shazam / audio identification | Fingerprint extraction, inverted hash index, robust to noise, latency target |
| Design visual search (image-to-product) | CLIP-like embeddings, ANN, attribute filters, ranking by inventory and price |
| Design document understanding for invoices | OCR + layout + extractor, confidence gating, human review queue, audit trail |
| Design content moderation at scale | Tiered classifiers, policy versioning, reviewer workflow, appeal path |

### Platform and infra

| Prompt | Lead with |
| --- | --- |
| Design an LLM serving platform for the company | AI gateway, model router, multi-tenant quotas, observability, eval harness |
| Design a feature store | Offline/online consistency, point-in-time joins, freshness SLAs, monitoring |
| Design an ML experimentation platform | Trial registry, dataset/version pinning, offline+online evals, deployment gates |
| Design a vector database | HNSW/IVF, sharding, replication, hybrid filters, snapshot+WAL durability |
| Design a training data pipeline | Dedup, decontamination, PII handling, lineage, dataset versioning |

---

## Part 12 — Anti-patterns that fail AI system design interviews **◆ CONCEPT**

These are the moves interviewers flag as junior. Read them once before any AI design round.

| Anti-pattern | Why it fails | What to say instead |
| --- | --- | --- |
| "Use GPT-4 / Claude for everything" | No routing, no cost story, no fallback | Tier by intent and risk; small model first, large model on escalation |
| Jumping to architecture without clarifying | Misses the actual product constraint | Spend 3–5 min on users, mode, risk, latency, scale, success metric |
| "Just embed it and put it in a vector DB" | Ignores hybrid retrieval, ACLs, chunking, freshness | Hybrid (BM25 + dense) + reranker + ACL filter + incremental ingestion |
| Infinite agent loop with broad tools | Unbounded cost, unsafe actions, no observability | Bounded steps, typed tools, idempotency, approval gates, audit log |
| Treating prompts as ephemeral | No rollback, no eval, no incident response | Versioned prompts in a registry alongside models and indexes |
| "We'll evaluate with vibes / spot checks" | Quality regressions ship silently | Layered evals: retrieval, output, safety, product outcome; segment by slice |
| Online path doing training-time work | Latency and cost explode | Push embedding, indexing, feature recompute offline; cache aggressively |
| One global rate limit on requests | Doesn't protect against a single tenant burning all tokens | Per-tenant TPM + RPM, plus global circuit breaker per provider |
| Skipping permission checks at retrieval | Data leakage from the index | Filter ACLs during retrieval, not after generation |
| "We'll fine-tune to fix it" | Slow loop, wrong tool for knowledge problems | Climb the ladder: prompt → RAG → LoRA → DPO → full FT, only if needed |
| No drift or freshness monitoring | Silent quality decay on changing data | Index-age dashboards, feature freshness SLAs, periodic re-evals |
| "Hallucinations are an LLM problem, not a system problem" | Abdicates the design | Ground with retrieval, validate with rubric, gate risky outputs with humans |
| Treating LLM output as instruction-safe input to next tool | Prompt injection chains | Schema-validate tool args, restrict tool capabilities, sandbox execution |
| One giant prompt that does everything | Impossible to debug or roll back partial regressions | Decompose into classifier → retriever → composer → validator stages |

> **💡 TIP: Final framing**
> The senior signal in AI system design is treating the LLM as one stage in a versioned, monitored, multi-stage pipeline — not as a magic box. Show that you separate online from offline, that you name specific algorithms and trade-offs, and that you can reason about latency, cost, and safety as concrete numbers and gates. That combination is what passes a staff-level bar.

---

## Part 13 — Training infrastructure at scale **★ CORE**

Lead-level interviews probe whether you can reason about training systems, not just serving. You won't be asked to derive backprop, but you will be asked how a 70B model gets trained on 1k+ GPUs without melting, what happens when a node dies mid-run, and where the bottlenecks actually live.

### Training memory: where it actually goes

Inference memory is dominated by weights and KV cache. Training memory is a different beast — gradients, optimizer states, and activations each rival the model size.

```text
  For Adam/AdamW with mixed precision (bf16 compute, fp32 master):
    weights (bf16)            : 2 bytes/param
    gradients (bf16)          : 2 bytes/param
    optimizer state m, v (fp32): 8 bytes/param
    master weights (fp32)     : 4 bytes/param
    --------------------------------------------
    total                     : ~16 bytes/param

  70B model -> ~1.1 TB just for state, before any activations.
  H100 has 80 GB. That's why training is inherently distributed.

  Activation memory (per layer, per token):
    O(batch * seq_len * hidden_dim * n_layers)
    For 70B at seq_len=8192, batch=4 micro: 100s of GB more.
    Mitigated by gradient (activation) checkpointing.
```

### The 4D parallelism cheat sheet

| Strategy | What gets sharded | Comm pattern | When to use |
| --- | --- | --- | --- |
| Data parallel (DP) | Batch across replicas | All-reduce gradients per step | Default; scales linearly until comm dominates |
| Tensor parallel (TP) | Each layer's matmuls split across GPUs | All-reduce inside every layer | Model doesn't fit on one GPU; needs NVLink |
| Pipeline parallel (PP) | Layer groups across nodes | Point-to-point activations between stages | Cross-node scaling; needs careful microbatching |
| Sequence parallel (SP) | Sequence dim of activations | Reduce-scatter / all-gather | Long-context training (32k+) |
| Expert parallel (EP) | MoE experts across GPUs | All-to-all for token routing | Only for MoE architectures |
| Context parallel (CP) | Attention computed in chunks across GPUs | Ring all-reduce on K/V | Very long context (128k+, ring attention) |

```text
  Typical 3D recipe for a 70B dense model on 512 H100s:
    TP = 8   (inside one DGX node, NVLink)
    PP = 8   (across nodes, IB or RoCE)
    DP = 8   (remaining replicas for throughput)
    8 * 8 * 8 = 512 GPUs

  Microbatching for pipeline:
    global batch = micro_batch * grad_accum * DP
    grad_accum must be >= PP to keep the pipeline full (otherwise bubbles)
    1F1B (one-forward-one-backward) interleaved schedule reduces bubble
```

### ZeRO / FSDP: the memory unlock

ZeRO (DeepSpeed) and FSDP (PyTorch) shard optimizer state, gradients, and weights across the data-parallel group. Conceptually they trade more communication for dramatically less per-GPU memory.

| Stage | What's sharded | Per-GPU memory cost | Comm overhead |
| --- | --- | --- | --- |
| ZeRO-1 | Optimizer state | ~8x reduction on optimizer | Slight (reduce-scatter) |
| ZeRO-2 | Optimizer + gradients | ~4x further | Modest |
| ZeRO-3 / FSDP | Optimizer + gradients + weights | ~Nx (N = DP size) | All-gather weights per fwd/bwd pass |
| ZeRO-Infinity | + CPU/NVMe offload | Train far larger than VRAM | Much slower; for research, not production |

### Checkpointing and fault tolerance

- **Async checkpointing:** snapshot GPU state to host, write to object store from CPU. Foreground training continues. PyTorch's DCP, Megatron's distributed checkpointer.
- **Cadence:** typical 30 min – 4 hours depending on cluster MTBF. Cost of a restart = (interval / 2) + restart overhead.
- **Sharded checkpoints:** each rank writes its shard; replay tools resharded on restore (lets you change parallelism on resume).
- **Resilient training:** torchelastic / Megatron-LM with auto-replace of dead nodes; spot/preemptible instances need extra care.

```text
  Failure math at scale:
    Per-GPU MTBF ~ 10,000 hours
    Cluster of 1,024 GPUs -> expected failure every ~10 hours
    -> checkpoint every 1-2 hours, or lose >5% of compute to restarts

  Common failure modes:
    - GPU ECC errors (silent data corruption -> NaN losses)
    - NVLink/IB transient errors
    - PSU / cooling events
    - Stragglers (one slow GPU drags global step latency)
```

### Training data pipeline

```text
  Raw sources (web crawl, code, books, internal data)
    -> language ID + quality filtering (Gopher rules, FastText)
    -> dedup
         - exact (hash)
         - near-dup (MinHash LSH at document and paragraph level)
    -> PII redaction (regex + NER)
    -> decontamination against eval sets (n-gram overlap check)
    -> domain tagging + sampling weights
    -> tokenization (BPE/SentencePiece) into shards
    -> versioned dataset in object store with manifest + lineage
    -> streamed via WebDataset / Mosaic StreamingDataset
    -> per-rank deterministic shuffle with seed in checkpoint
```

### Training observability

- **Loss curves, gradient norms, weight norms** per layer — diverging norms predict instability hours before NaN.
- **Throughput in tokens/sec/GPU and MFU** (model FLOPs utilization) — 40–60% MFU on H100 is healthy; below 30% means a comm or data bottleneck.
- **Loss spike alerting** with automatic rollback to last good checkpoint and learning-rate reduction.
- **Per-rank profiling** for stragglers (NCCL kernel times, host-side dataloader latency).
- **Eval during training** on a frozen holdout every N steps, not just at end — catches overfitting to recent data shards.

> **⚠️ WARN: The hidden cost of failed runs**
> At 1,000+ GPUs, a single bad config (wrong learning rate schedule, broken data shard, NaN in mixed precision) can burn $50k–500k before someone notices. Lead-level answers mention dry-run policies, automatic loss-spike detection, deterministic restart, and human review gates before launching multi-week runs.

### Post-training: SFT, DPO, RLHF

```text
  Base model
    -> SFT (supervised fine-tune on curated instruction data)
         dataset: 10k - 1M high-quality (prompt, response) pairs
         loss: standard next-token, masked on prompt tokens
    -> Preference data collection
         pairs of (chosen, rejected) responses from human raters or stronger model
    -> DPO / KTO / IPO (direct preference optimization, no reward model)
         OR
    -> Reward model training -> PPO/RLHF rollout
         PPO is finicky at scale; most teams now ship DPO first
    -> Safety tuning (rule-based + adversarial red team data)
    -> Eval gauntlet (capability + safety + regression)
    -> Release candidate
```

### Cluster and network topology

- **Intra-node:** NVLink/NVSwitch — 600–900 GB/s between GPUs in a DGX/HGX box. TP lives here.
- **Inter-node:** InfiniBand NDR/HDR or RoCE — 400 Gbps per NIC, often multiple NICs per node. PP/DP lives here.
- **Topology matters:** rail-aligned fat-tree (one rail per NIC) keeps all-reduce collectives on dedicated links; blocking ratios under 1:1 hurt at scale.
- **Storage:** NVMe-backed parallel filesystem (Weka, Lustre) for dataset streaming + checkpoint writes; object store (S3/GCS) for archive.

---

## Part 13.5 — Advanced inference: MoE, long context, reasoning models **◆ CONCEPT**

### Mixture-of-Experts serving

MoE models (Mixtral, DeepSeek-V3, Grok, Llama-4) have far more parameters than active compute per token. They are cheaper to serve at quality but harder to operate.

| Aspect | Dense model | MoE model |
| --- | --- | --- |
| Params vs compute | All params active per token | Top-k experts (usually 2 of 8–256) active |
| Memory | Modest weights, big KV | Huge weights (must hold all experts), normal KV |
| Throughput | Predictable batched | Imbalanced; depends on routing |
| Parallelism | TP / PP | Add expert parallel (EP); all-to-all dominant cost |

```text
  MoE failure modes the interviewer expects you to name:
    - Routing collapse (a few experts get all traffic, rest are dead)
       fix: load-balancing loss during training; capacity factor at inference
    - Token drop (expert at capacity; tokens skip MLP layer)
       fix: tune capacity factor; expert-choice routing instead of token-choice
    - All-to-all bottleneck (every token must route across the EP group)
       fix: keep EP within a high-bandwidth domain (single node or NVLink switch)
    - Cold cache on rare experts (first request after warmup is slow)
       fix: pin all experts in VRAM; don't offload to CPU at serving time
```

### Long-context serving (100k–1M tokens)

- **KV memory dominates everything:** at 1M tokens, a single request can need 100+ GB of KV cache. Quantize KV to FP8 or INT4 to fit.
- **Ring attention:** shard the sequence across GPUs; each GPU computes attention against a rotating slice of K/V from peers. Enables training and inference past single-GPU memory.
- **Attention sinks / StreamingLLM:** keep the first few tokens plus a sliding window of recent tokens; drops middle KV. Works for chat but lossy for retrieval-style long context.
- **Sparse/hybrid attention:** Mamba/RWKV-style state-space layers interleaved with attention reduce O(N²) cost for very long inputs.
- **Prefill chunking is mandatory:** a 1M-token prefill held single-threaded would block every other user for tens of seconds. Chunk into 4–16k pieces interleaved with decode.

### Reasoning models and test-time compute

"Reasoning" models (o1, o3, Claude with extended thinking, DeepSeek-R1) trade more inference compute for higher accuracy by generating long internal chains of thought before answering. This changes the cost model and the latency model.

```text
  Latency profile of a reasoning model:
    classical chat:  TTFT 300ms, 80 tok/s -> answer in 1-3s
    reasoning model: TTFT 300ms, 60 tok/s, BUT generates 2k-30k thinking tokens
                     -> visible answer in 10s - 5min

  Design implications:
    - UX needs progress hints ("thinking..." or stream the trace)
    - Token budget per request must be explicit (compute caps)
    - Async pattern: enqueue task, poll/webhook on completion
    - Caching: thinking traces are expensive; cache by problem signature
    - Routing: only route to reasoning model when difficulty justifies cost
       (a small classifier on the prompt is a 10x cost lever)
```

### Structured output and constrained decoding

- **Grammar-constrained decoding** (outlines, LMQL, vLLM guided decoding): force outputs to match a regex / JSON schema / context-free grammar by masking invalid tokens at sampling time. Reliability bump, ~5–15% latency cost.
- **Function-calling / tool-use** APIs use a similar mechanism under the hood; prefer the provider's native mode over freeform JSON-in-text parsing.
- **Speculative + structured:** some stacks combine speculative decoding with grammar constraints by re-validating drafted tokens against the grammar.

### Evaluation rigor at the lead level

| Pitfall | What it looks like | Mitigation |
| --- | --- | --- |
| Underpowered comparison | "New model wins by 2%" on 100 examples | Pre-register sample size; paired bootstrap CIs; require Δ > 2× CI width |
| Eval-set contamination | Training corpus contains the benchmark | n-gram decontamination at build time; held-out private evals |
| Judge bias | LLM judge prefers verbose answers / its own family | Rotate judges; calibrate against human labels; rubric-based not pairwise |
| Goodharting one metric | BLEU goes up, users hate it | Multi-metric dashboard with product KPI gating release |
| Aggregate hides regressions | +1% average, -15% on safety slice | Per-slice eval as a release gate, not just headline |
| Win-rate without Elo | Pairwise A>B reported without transitivity check | Bradley-Terry or Elo on a tournament of versions |

> **💡 TIP: Lead signal on evals**
> When asked "how do you know the new model is better?", the senior answer is "pre-registered eval set, slice-level metrics with paired bootstrap CIs, human-judged head-to-head on a fixed rubric, plus a live A/B with a product KPI as the primary outcome." Saying just "MMLU went up" is a junior tell.

---

## Part 14 — Leadership scenarios for Lead/Staff/Principal rounds **★ CORE**

Lead-level interviews spend 30–50% of the loop on judgment, organization, and prioritization questions. The answers below are not scripts — they're shapes for how to reason out loud.

### How to structure an AI org

```text
  Common four-team split at a 50-200 person AI org:

    APPLIED AI / PRODUCT TEAMS
      own feature surfaces, prompts, evals, integration
      report into product or engineering org
      success metric: product KPIs

    AI PLATFORM
      owns gateway, model registry, eval harness, training infra
      one team enables all applied teams
      success metric: applied teams shipping faster, lower $/token

    RESEARCH / MODEL TEAM
      owns base model training, fine-tuning recipes
      tight loop with platform on infra
      success metric: capability + safety eval lifts

    SAFETY / RESPONSIBLE AI
      owns policy, red team, deployment gates
      independent reporting line (often to legal or CTO)
      success metric: incident rate, gate-pass rate

  Anti-patterns:
    - "Every team trains its own model"  -> wasted GPUs, fragmented evals
    - "Safety is everyone's job"          -> in practice nobody owns it
    - "Research ships features"           -> research timelines kill products
```

### Build vs buy framework

| Question | Lean BUY (hosted API) | Lean BUILD (self-host / train) |
| --- | --- | --- |
| Volume | < 5B tokens/day | > 10B tokens/day sustained |
| Latency SLO | ≥ 1s acceptable | Sub-300ms TTFT required |
| Data sensitivity | OK to leave premises (with BAA/DPA) | Regulated / customer-isolated |
| Differentiation | Capability is table stakes | Capability is the moat |
| Team strength | No GPU SRE on staff | You have ML infra engineers |
| Time-to-market | Weeks matter | Quarters are OK |

> **💡 TIP: Hybrid is usually the right answer**
> Most mature orgs end up with: hosted APIs for prototyping and burst traffic, self-hosted open-weight for high-volume / regulated paths, and one or two fine-tuned models for the narrow domains where it matters. Saying "we'll be hybrid and here's the routing logic" is a stronger answer than picking one side.

### Roadmapping when the next frontier model ships in 3 months

- **Layer your bets:** ship today on current best model; have a "snap-in" plan for the next one; keep an exploratory bet on something disruptive (open-weight, on-device).
- **Build moats that compound:** evals, data, distribution, trust. These survive a model swap.
- **Avoid model-specific moats:** heavy prompt engineering against one model's quirks becomes a liability when it's deprecated.
- **Be honest about wait-vs-build:** if next quarter's frontier model trivially solves your problem, your roadmap item should be "be ready to integrate it" not "spend 2 quarters fine-tuning around current limits."
- **Capability ladders:** design product surfaces that get better automatically as models improve (e.g., longer context = better summaries) without code changes.

### Safety governance for product launches

```text
  Pre-launch gate checklist (use this almost verbatim in an interview):

    1. Threat model
        what can go wrong? misuse, hallucination, bias, privacy leak,
        action abuse, prompt injection, IP infringement
    2. Red team
        domain experts try to break the system; results documented
    3. Eval gauntlet
        capability + safety + regression sets, with release thresholds
    4. Reversibility
        which actions can we undo? which are permanent?
    5. Blast radius
        who is affected if the worst case happens?
    6. Monitoring plan
        what would tell us something is wrong in production?
    7. Rollback plan
        prompt / model / index / policy independently revertable
    8. Disclosure
        what does the user see? consent, limitations, escalation path
    9. Cross-functional sign-off
        legal, security, policy, customer support trained

  Decision: launch / canary / hold / iterate
```

### AI incident response

- **Detect:** automatic safety/quality drift alerts; user reports; reviewer queue spikes.
- **Mitigate first, root-cause later:** revert prompt/model/index, narrow scope, increase human review threshold. Buy time before debugging.
- **Triage roles:** incident commander, comms lead, eng lead. Same as classical SRE but with an extra "model owner" role.
- **Post-mortem within 72h:** what was the failure mode (data, model, prompt, retrieval, policy)? Add to eval set so it can't regress silently.
- **Learning loop:** incident corpus becomes a permanent eval slice; lead engineers review monthly.

### What to look for when hiring

| Role | Strong signal | Weak signal |
| --- | --- | --- |
| ML Engineer (applied) | Has shipped a model end-to-end; pragmatic about evals; product instinct | Only Kaggle / papers; can't describe a real production trade-off |
| Research Engineer | Reproduces papers, debugs training instability, reads CUDA kernels | Can describe but not implement; needs a roadmap to start |
| AI Platform / Infra | Distributed systems background + LLM-specific knowledge (KV cache, vLLM) | Pure backend with no exposure to GPU economics |
| AI Product Engineer | Writes prompts *and* evals; iterates on UX given probabilistic outputs | Treats LLM as a black box; no eval discipline |
| Safety / Red Team | Adversarial mindset; familiar with policy frameworks; can write evals | Pure policy background with no engineering vocabulary |

### Economics conversations with non-technical leaders

- **Unit economics:** $ per successful task, not $ per token. Maps cost to product value.
- **Gross margin shape:** AI features often start at low/negative margin and improve via routing, caching, distillation. Communicate the trajectory.
- **Capacity commitments:** reserved GPU contracts trade flexibility for unit cost. Worth it once usage is predictable within ~30%.
- **The "cheaper next quarter" problem:** token prices drop ~3–5x/year. Build with this in mind — features uneconomic today may be obvious next year.

---

## Part 15 — Behavioral story bank (STAR scaffolds) **EXAMPLE**

Lead/Staff loops include 2–4 behavioral rounds. Prepare 6–8 stories that flex across multiple prompts. Each story should hit Situation → Task → Action → Result and end with one sentence on what you'd do differently.

### Story prompts to have a real answer for

| Prompt | What the interviewer is testing | Story shape |
| --- | --- | --- |
| "Tell me about an AI system you took from 0 to production" | End-to-end ownership; ability to ship | Problem → MVP → metrics → scale milestone |
| "Tell me about a model rollback or production incident" | Judgment under pressure; blameless culture | Detection → mitigation → root cause → permanent fix |
| "When did you say no to a feature request?" | Prioritization; strategic thinking | Request → analysis → reframe → outcome |
| "Tell me about a time your eval missed a real problem" | Humility; eval rigor | Shipped → user feedback → gap in eval → new eval added |
| "How did you handle a cost overrun on an AI feature?" | Business judgment; pragmatism | Spike → root cause → routing/caching/distillation → 60–80% reduction |
| "Tell me about a hard cross-functional disagreement" | Influence without authority | Tension → listening → data → compromise / decision |
| "When did you push back on a leader's direction?" | Courage + judgment | Concern → evidence → escalation → outcome |
| "Describe mentoring an engineer through an AI project" | People growth; technical leadership | Skill gap → structured support → measurable growth |
| "Tell me about a safety / responsible-AI tradeoff you made" | Values + execution | Risk identified → gate added → product impact accepted |
| "What's the hardest technical bug you debugged?" | Depth; debugging methodology | Symptom → hypotheses → bisection → root cause → systemic fix |

### Reusable STAR scaffold

```text
  SITUATION (1 sentence)
    Where, when, scale, stakes — anchor the listener.
    "At <company>, our <product> hit ~<scale> and we noticed <problem>."

  TASK (1 sentence)
    Your specific role — singular "I", not "we".
    "As <role>, I owned <scope> and was asked to <objective>."

  ACTION (2-4 sentences)
    What YOU did, decisions and trade-offs, not a tutorial.
    Include one non-obvious choice and why.
    "I considered X and Y; I chose Z because <reason>.
     I led <team>, set up <process>, shipped <thing>."

  RESULT (1-2 sentences)
    Numbers when possible. Connect to business or user outcome.
    "<metric> moved by <amount>, <user/$ outcome>."

  REFLECTION (1 sentence)
    What you'd do differently. Shows growth, not weakness.
    "Looking back, I'd <change>; the lesson was <generalization>."
```

### AI-specific anchors that make stories land

- **Mention an eval you built or insisted on** — this single signal distinguishes ML-mature engineers from prompt-tinkerers.
- **Mention a rollback or kill switch you designed in advance** — shows you treat AI as probabilistic and plan for failure.
- **Mention a cost lever you pulled** (routing, caching, distillation, smaller model) with a concrete % reduction.
- **Mention a safety/policy decision** where you blocked or scoped a launch, even when it slowed you down.
- **Mention an org change you drove** (eval team, gateway, model-of-record process) — Lead is about leverage, not just hands-on work.

> **⚠️ WARN: Behavioral red flags interviewers downgrade for**
> Constant "we" (no individual contribution), no numbers, no failure stories, blaming teammates or vendors, no reflection, claiming you single-handedly built things that obviously needed a team. Be specific, be honest about constraints, give credit, and own the call that didn't work.

---

## Part 16 — Post-mortem case studies **EXAMPLE**

Lead-level pattern recognition comes from incidents. The five vignettes below are composites of real production failure modes. Each ends with the systemic fix that would have prevented it — that systemic fix is the senior signal.

### Incident 1 — The silent retrieval regression

**Symptom:** Internal RAG assistant satisfaction drops from 78% to 64% over two weeks. No deploys. No model changes.

**Investigation:** Ingestion pipeline had been silently failing on a connector update, so new docs (including a major policy revision) never reached the index. Retrieval still returned *something*, so eval headline numbers stayed flat; the regression hid in the "recent docs" slice.

**Root cause:** No index-age dashboards. No per-source ingestion success rate alerts. Eval set had no freshness slice.

**Systemic fix:**

- Alert on per-source last-successful-ingest age (red after 2× expected cadence).
- Freshness slice in the eval set (queries whose answers depend on docs < 7 days old).
- Synthetic canary: inject a known doc nightly, query for it, alert if not retrieved.

### Incident 2 — The cost spike at 3am

**Symptom:** Daily LLM bill spikes 12× overnight. On-call paged.

**Investigation:** A customer integration started sending PDFs with embedded HTML that produced 200k-token prompts. The agent looped up to 30 tool calls per request. Per-tenant TPM limit existed but was set generously and the global circuit breaker hadn't tripped.

**Root cause:** No per-request token cap. No per-tenant cost alert. Agent loop bound was step count, not token total.

**Systemic fix:**

- Hard max_tokens per request, enforced at gateway.
- Per-tenant dollar-per-hour alert with auto-throttle at 5× baseline.
- Agent budget cap measured in tokens AND steps AND wallclock.
- Input-token preview check before expensive route (refuse or downgrade if > threshold).

### Incident 3 — The eval that lied

**Symptom:** New model wins offline evals by 8%, ships, A/B test shows users prefer the *old* model 60–40.

**Investigation:** Offline judge was the new model's own family. It rewarded verbose, hedged answers. Real users wanted concise direct ones. The eval optimized for what the model liked, not what users wanted.

**Root cause:** Single-judge eval, no human calibration, no product KPI in the release gate.

**Systemic fix:**

- Rotate two different judge families; require both to agree on wins.
- Calibrate judge against 200 human-labeled examples; report judge accuracy.
- Release gate requires offline win AND online A/B on product KPI (not satisfaction proxy).
- Add length-bias eval: pairs of (concise, verbose) answers with same content; judge must not always prefer the longer one.

### Incident 4 — The agent that emailed a customer's lawyer

**Symptom:** Support copilot, used by trained agents, autonomously composed and sent a reply to opposing counsel on a legal matter. Reply contained internal-only context.

**Investigation:** The "send reply" tool was approval-gated for first-time recipients but cached as "approved" once a recipient had been confirmed earlier in the day. A different ticket from the same email thread reused the cached approval and skipped the gate.

**Root cause:** Approval cached at the wrong scope (recipient instead of ticket). Audit log existed but wasn't reviewed proactively.

**Systemic fix:**

- Approvals scoped per-action, not per-recipient. No carry-over.
- Recipient-classification on every send (legal, executive, regulator → always human-approval).
- Daily sample audit of agent-sent emails by a human reviewer.
- "Anti-exfiltration" check: outbound content scanned against internal-only context that was injected by retrieval.

### Incident 5 — The training run that quietly diverged

**Symptom:** Two-week 1,024-GPU pretraining run completed; downstream eval crashed by 30% vs the prior run.

**Investigation:** A single data shard had a tokenization bug (BOM character corrupted ~0.4% of sequences). Loss curves looked fine — within noise. Per-shard loss telemetry didn't exist.

**Root cause:** No data validation step between tokenization and training. No per-shard loss tracking. No "smoke" eval during training, only at end.

**Systemic fix:**

- Per-shard checksum and sample-decode validation before training launch.
- Per-shard loss curves; alert on shards that drift > 2σ from cohort.
- Mini-eval gauntlet every N steps; auto-pause if any capability eval drops > 10%.
- Mandatory dry-run on 1% of compute before launching a multi-week run.

> **💡 TIP: Pattern across all five**
> Every senior-level incident has the same shape: **a guardrail existed but at the wrong scope, the monitoring metric existed but didn't include the failing slice, the eval covered the happy path but not the failure mode.** When you describe AI systems in interviews, name the slices and scopes explicitly — that's what tells the interviewer you've actually run these systems in production.

