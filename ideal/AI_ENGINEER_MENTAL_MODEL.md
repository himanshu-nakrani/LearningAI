# AI Engineer Mental Model — Visual Maps

> Mermaid diagrams for every major domain in the AI Engineer Mastery Roadmap. Use these to navigate the roadmap, see how pieces connect, and plan your study path.
>
> Render in any Markdown viewer that supports Mermaid (GitHub, VS Code with Mermaid extension, Obsidian, Notion, etc.).

---

## Table of Contents
- [0. The Whole System (Start Here)](#0-the-whole-system-start-here)
- [1. The Learning Path (How to Walk It)](#1-the-learning-path-how-to-walk-it)
- [2. Foundations Map](#2-foundations-map)
- [3. Math Prerequisite Map](#3-math-prerequisite-map)
- [4. Classical ML Mental Model](#4-classical-ml-mental-model)
- [5. Deep Learning Architecture Map](#5-deep-learning-architecture-map)
- [6. Transformer Anatomy (Single Block)](#6-transformer-anatomy-single-block)
- [7. LLM Inference Flow](#7-llm-inference-flow)
- [8. RAG System Map](#8-rag-system-map)
- [9. AI Agent Loop](#9-ai-agent-loop)
- [10. Fine-Tuning & Alignment Tree](#10-fine-tuning--alignment-tree)
- [11. Multimodal AI Map](#11-multimodal-ai-map)
- [12. MLOps / LLMOps Production Stack](#12-mlops--llmops-production-stack)
- [13. Distributed Training Strategies](#13-distributed-training-strategies)
- [14. GPU Memory Hierarchy (Performance)](#14-gpu-memory-hierarchy-performance)
- [15. The AI Engineer Interview Loop](#15-the-ai-engineer-interview-loop)
- [16. Project Portfolio Map](#16-project-portfolio-map)
- [17. Compensation Strategy Tree (India)](#17-compensation-strategy-tree-india)
- [18. The Career-Compounding Loop](#18-the-career-compounding-loop)
- [19. 24-Month Execution Flow](#19-24-month-execution-flow)

---

## 0. The Whole System (Start Here)

The single map. Everything in the roadmap is here. Top-down: what you build on top of, what sits in the middle, what you ship on top.

```mermaid
graph TD
    YOU["<b>YOU (AI Engineer)</b><br/>Senior / Staff at top company"]:::goal

    %% Foundation layer
    subgraph FOUNDATION["<b>FOUNDATIONS</b><br/>Months 0–2"]
        F1[Programming & SE]:::foundation
        F2[Math: LA, Calculus, Prob/Stat]:::foundation
        F3[Linux, Git, OS, Networking]:::foundation
        F4[SQL & Databases]:::foundation
    end

    %% Core ML
    subgraph CORE_ML["<b>CORE ML / DL</b><br/>Months 2–4"]
        C1[Classical ML<br/>XGBoost, sklearn]:::core
        C2[Deep Learning<br/>CNN, RNN, Training]:::core
        C3[Transformers<br/>The central engine]:::core
    end

    %% Applied AI
    subgraph APPLIED["<b>APPLIED AI</b><br/>Months 4–6"]
        A1[LLMs: APIs + Internals]:::applied
        A2[RAG Systems]:::applied
        A3[AI Agents]:::applied
        A4[Fine-Tuning & RLHF/DPO]:::applied
        A5[Multimodal: VLM, Audio, Video]:::applied
    end

    %% Production
    subgraph PROD["<b>PRODUCTION</b><br/>Months 6+"]
        P1[MLOps / LLMOps]:::prod
        P2[System Design for AI]:::prod
        P3[GPU Kernels, Quantization]:::prod
        P4[Distributed Training & Serving]:::prod
        P5[Eval, Safety, Security]:::prod
    end

    %% Outputs
    subgraph OUT["<b>OUTPUTS / LEVERAGE</b>"]
        O1[3-5 Flagship Public Projects]:::output
        O2[Open-Source Contributions]:::output
        O3[Blog / Public Presence]:::output
        O4[Interview Loop Mastery]:::output
    end

    YOU -.->|ships| O1
    YOU -.->|ships| O2
    YOU -.->|compounds via| O3
    YOU -.->|clears| O4

    FOUNDATION --> CORE_ML
    CORE_ML --> APPLIED
    APPLIED --> PROD
    FOUNDATION --> APPLIED
    CORE_ML --> PROD
    O1 & O2 & O3 & O4 --> YOU

    classDef goal fill:#ffd54f,stroke:#333,stroke-width:3px,color:#000
    classDef foundation fill:#90caf9,stroke:#333,color:#000
    classDef core fill:#81c784,stroke:#333,color:#000
    classDef applied fill:#ffb74d,stroke:#333,color:#000
    classDef prod fill:#e57373,stroke:#333,color:#000
    classDef output fill:#ce93d8,stroke:#333,color:#000
```

---

## 1. The Learning Path (How to Walk It)

What depends on what. **You must be solid on the boxes below a given box before you attempt it.** This is the dependency graph.

```mermaid
graph LR
    A[Python Mastery] --> B[NumPy & Pandas]
    A --> C[Testing & Tooling]
    B --> D[Linear Algebra]
    A --> E[DSA: Patterns]
    D --> F[Calculus & Backprop]
    D --> G[Probability & Stats]
    F --> H[Classical ML]
    G --> H
    H --> I[Deep Learning]
    I --> J[CNNs]
    I --> K[RNNs / Seq2Seq]
    I --> L[Transformers]
    L --> M[LLM Internals]
    L --> N[Fine-Tuning]
    M --> O[Inference & Serving]
    M --> P[RAG]
    M --> Q[Agents]
    O --> R[Production / MLOps]
    P --> R
    Q --> R
    R --> S[System Design]
    L --> S
    S --> T[Senior / Staff Role]

    classDef prereq fill:#bbdefb,stroke:#333
    classDef core fill:#c8e6c9,stroke:#333
    classDef applied fill:#fff9c4,stroke:#333
    classDef prod fill:#ffccbc,stroke:#333
    classDef goal fill:#d1c4e9,stroke:#333,stroke-width:3px

    class A,B,C,D,F,G,E prereq
    class H,I,J,K,L core
    class M,N,O,P,Q applied
    class R,S prod
    class T goal
```

---

## 2. Foundations Map

The things you cannot skip. Each is a small dependency graph of its own.

```mermaid
graph TD
    subgraph COMPUTER["<b>How Computers Work</b>"]
        C1[Memory hierarchy] --> C2[CPU vs GPU vs TPU]
        C2 --> C3[Why GPUs dominate ML]
    end

    subgraph LINUX["<b>Linux / CLI</b>"]
        L1[Shell, pipes, grep, awk] --> L2[SSH, tmux, servers]
        L1 --> L3[Permissions & env vars]
    end

    subgraph GIT["<b>Git</b>"]
        G1[Branch, merge, rebase] --> G2[Interactive rebase]
        G2 --> G3[Clean history habits]
    end

    subgraph DSA["<b>Data Structures & Algorithms</b>"]
        D1[Arrays, hash maps] --> D2[Trees, heaps, tries]
        D1 --> D3[Graphs: BFS/DFS/Dijkstra]
        D2 --> D4[DP: 1D, 2D, on trees]
        D1 --> D5[Sorting, binary search]
        D3 --> D6[Contest-level problems]
    end

    subgraph DB["<b>Databases</b>"]
        DB1[PostgreSQL: joins, indexes, EXPLAIN] --> DB2[Transactions, isolation]
        DB1 --> DB3[Vector DBs: pgvector, Qdrant, Pinecone]
    end

    classDef block fill:#e3f2fd,stroke:#1976d2
    class C1,C2,C3,L1,L2,L3,G1,G2,G3,D1,D2,D3,D4,D5,D6,DB1,DB2,DB3 block
```

---

## 3. Math Prerequisite Map

The math you must own, with the order in which to learn it.

```mermaid
graph TD
    LA["<b>Linear Algebra</b><br/>30–50 hrs"]:::math
    CALC["<b>Multivariable Calculus</b><br/>20–30 hrs"]:::math
    PROB["<b>Probability & Statistics</b><br/>60–80 hrs"]:::math
    OPT["<b>Optimization</b><br/>20–30 hrs"]:::math
    NUM["<b>Numerical Computing</b><br/>10–20 hrs"]:::math

    LA --> CALC
    LA --> NUM
    CALC --> OPT
    PROB --> OPT
    LA --> PROB
    OPT --> LITMUS{ "<b>Litmus test</b><br/>Derive softmax cross-entropy<br/>forward + backward in NumPy<br/>with finite-difference check" }:::goal
    LA --> LITMUS
    PROB --> LITMUS
    NUM --> LITMUS

    classDef math fill:#b3e5fc,stroke:#01579b
    classDef goal fill:#fff176,stroke:#f57f17,stroke-width:3px
    class LA,CALC,PROB,OPT,NUM math
```

---

## 4. Classical ML Mental Model

The ML workflow, end to end, with the algorithms that go in each box.

```mermaid
graph TD
    DATA["<b>Data</b><br/>Tabular / text / image"]:::data
    SPLIT["<b>Split</b><br/>train/val/test<br/>k-fold, time-based"]:::step
    FEAT["<b>Feature Engineering</b><br/>scale, encode, missing,<br/>interactions, leakage check"]:::step
    MODEL["<b>Model</b>"]:::model
    EVAL["<b>Evaluation</b><br/>classification, regression,<br/>ranking, calibration"]:::eval
    SHIP["<b>Ship</b><br/>FastAPI, monitoring,<br/>drift detection"]:::ship

    LINEAR["Linear / Logistic Regression"]:::alg
    TREES["Decision Trees, Random Forest"]:::alg
    BOOST["Gradient Boosting<br/><b>XGBoost / LightGBM / CatBoost</b><br/>(default for tabular)"]:::alg
    KNN["k-NN, Naive Bayes, SVM"]:::alg
    CLUST["Clustering: k-means, GMM, DBSCAN"]:::alg
    PCA["PCA, t-SNE, UMAP"]:::alg
    ANOM["Anomaly Detection<br/>Isolation Forest, AE"]:::alg

    DATA --> SPLIT --> FEAT --> MODEL --> EVAL --> SHIP
    FEAT -.-> LINEAR & TREES & BOOST & KNN
    FEAT -.-> CLUST
    FEAT -.-> PCA
    MODEL -.-> ANOM

    classDef data fill:#ffccbc,stroke:#333
    classDef step fill:#fff9c4,stroke:#333
    classDef model fill:#c5e1a5,stroke:#333
    classDef eval fill:#b39ddb,stroke:#333
    classDef ship fill:#80deea,stroke:#333
    classDef alg fill:#f5f5f5,stroke:#666,stroke-dasharray: 5 5
```

---

## 5. Deep Learning Architecture Map

The progression of architectures, with what each was solving.

```mermaid
graph TD
    MLP["<b>MLP / Fully Connected</b><br/>Universal but parameter-heavy"]:::arch
    CNN["<b>CNN</b><br/>LeNet → AlexNet → VGG → ResNet → ConvNeXt<br/>(spatial inductive bias)"]:::arch
    RNN["<b>RNN / LSTM / GRU</b><br/>Sequential, slow to train,<br/>vanishing gradients"]:::arch
    TRANS["<b>Transformer</b><br/>Attention is all you need<br/>Parallel, long-range, scalable"]:::arch
    DIFF["<b>Diffusion Models</b><br/>DDPM, Score-based, Flow matching<br/>(generative vision/audio)"]:::arch
    MOE["<b>Mixture of Experts (MoE)</b><br/>Sparse routing for scale<br/>(Mixtral, Qwen3-A22B)"]:::arch
    SSM["<b>State-Space Models (SSM)</b><br/>Mamba, S4<br/>(alternative to attention)"]:::arch

    MLP --> CNN
    MLP --> RNN
    RNN -->|"overtaken by"| TRANS
    CNN -->|"replaced by"| TRANS
    TRANS -->|"scaled with"| MOE
    TRANS -.->|"alt path"| SSM
    TRANS -->|"for images"| DIFF

    classDef arch fill:#d1c4e9,stroke:#333
    class MLP,CNN,RNN,TRANS,DIFF,MOE,SSM arch
```

---

## 6. Transformer Anatomy (Single Block)

What is actually inside one decoder block. Memorize this.

```mermaid
graph TD
    INPUT["Input token IDs<br/>(batch, seq_len)"]:::in
    EMB["Token Embedding<br/>+ Rotary Position Embedding (RoPE)"]:::embed
    NORM1["RMSNorm<br/>(pre-LN, modern)"]:::norm
    ATTN["<b>Multi-Head Self-Attention</b><br/>Q, K, V projections<br/>+ causal mask<br/>+ KV-cache (GQA / MQA)"]:::attn
    RES1["Residual connection"]:::res
    NORM2["RMSNorm"]:::norm
    MLP["<b>MLP Block</b><br/>SwiGLU / GeLU<br/>up → down projection"]:::mlp
    RES2["Residual connection"]:::res
    OUT["Hidden states<br/>(batch, seq_len, d_model)"]:::out

    INPUT --> EMB --> NORM1 --> ATTN --> RES1
    RES1 --> NORM2 --> MLP --> RES2
    EMB -.-> RES1
    RES1 -.-> RES2

    SAMPLING["<b>Next: Sampling</b><br/>greedy / top-k / top-p / min-p<br/>+ temperature"]:::sample
    LOGITS["<b>LM Head</b>→ logits over vocab"]:::logits
    OUT --> LOGITS --> SAMPLING

    classDef in fill:#b3e5fc,stroke:#333
    classDef embed fill:#c5e1a5,stroke:#333
    classDef norm fill:#fff9c4,stroke:#333
    classDef attn fill:#ffcdd2,stroke:#333,stroke-width:2px
    classDef mlp fill:#f8bbd0,stroke:#333,stroke-width:2px
    classDef res fill:#cfd8dc,stroke:#333
    classDef out fill:#b3e5fc,stroke:#333
    classDef sample fill:#d1c4e9,stroke:#333,stroke-width:2px
    classDef logits fill:#ffe0b2,stroke:#333
```

---

## 7. LLM Inference Flow

What happens when you call `client.chat.completions.create()`.

```mermaid
graph LR
    A["<b>Client</b><br/>Prompt + tools + system"]:::client
    B["<b>Tokenize</b><br/>BPE / tiktoken"]:::step
    C["<b>KV-cache lookup</b><br/>(prefix cache, paged)"]:::cache
    D["<b>Prefill</b><br/>Parallel forward pass<br/>on input tokens"]:::step
    E["<b>Decode loop</b><br/>1 token at a time<br/>(or speculative draft)"]:::step
    F["<b>Sampling</b><br/>temperature, top-p, top-k, min-p"]:::sample
    G["<b>Detokenize</b><br/>→ text token"]:::step
    H["<b>Tool call / function call?</b>"]:::tool
    I["<b>Stream / Final response</b>"]:::out

    A --> B --> C --> D --> E --> F --> G
    G -->|EOS| I
    G -->|tool| H
    H -->|yes| A
    H -->|no| I

    QUANT["<b>Optimizations</b><br/>FP8/INT8/INT4 quant<br/>continuous batching<br/>speculative decoding<br/>paged attention (vLLM)"]:::opt
    QUANT -.-> D
    QUANT -.-> E

    classDef client fill:#b3e5fc,stroke:#333
    classDef step fill:#fff9c4,stroke:#333
    classDef cache fill:#c5e1a5,stroke:#333
    classDef sample fill:#f8bbd0,stroke:#333
    classDef tool fill:#ffcdd2,stroke:#333
    classDef out fill:#d1c4e9,stroke:#333
    classDef opt fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
```

---

## 8. RAG System Map

The anatomy of a production RAG system.

```mermaid
graph TD
    subgraph OFFLINE["<b>OFFLINE INDEXING</b>"]
        D1["Raw documents<br/>(PDFs, HTML, code, DBs)"]:::data
        D2["<b>Chunking</b><br/>fixed / semantic / recursive<br/>late chunking / propositional"]:::step
        D3["<b>Embedder</b><br/>BGE / E5 / GTE / OpenAI / Voyage"]:::embed
        D4["<b>Vector Index</b><br/>Qdrant / Weaviate / pgvector<br/>HNSW / IVF-PQ"]:::index
        D5["<b>Keyword Index</b><br/>BM25"]:::index
    end

    subgraph ONLINE["<b>ONLINE QUERY</b>"]
        Q1["User query"]:::data
        Q2["<b>Query rewriting</b><br/>HyDE / multi-query / step-back"]:::step
        Q3["<b>Hybrid retrieval</b><br/>dense + BM25 + metadata filter"]:::step
        Q4["<b>Reranking</b><br/>cross-encoder / ColBERT / LLM"]:::step
        Q5["<b>Context packing</b><br/>+ token budget"]:::step
        Q6["<b>LLM generation</b><br/>with citations<br/>(Instructor / Outlines for JSON)"]:::gen
        Q7["<b>Eval</b><br/>RAGAS / TruLens / custom"]:::eval
    end

    D1 --> D2 --> D3 --> D4
    D1 --> D2 --> D5
    D4 --> Q3
    D5 --> Q3
    Q1 --> Q2 --> Q3 --> Q4 --> Q5 --> Q6
    Q6 --> Q7

    classDef data fill:#b3e5fc,stroke:#333
    classDef step fill:#fff9c4,stroke:#333
    classDef embed fill:#f8bbd0,stroke:#333
    classDef index fill:#c5e1a5,stroke:#333
    classDef gen fill:#ffcdd2,stroke:#333,stroke-width:2px
    classDef eval fill:#d1c4e9,stroke:#333
```

---

## 9. AI Agent Loop

The ReAct / tool-use pattern that powers modern agents.

```mermaid
graph TD
    G["<b>Goal</b><br/>User request + system prompt"]:::goal
    T["<b>Think</b><br/>Reason about next step<br/>(chain-of-thought)"]:::think
    A{"<b>Action?</b>"}:::decide
    TOOL["<b>Tool call</b><br/>code, web search, file,<br/>browser, MCP server,<br/>RAG retrieve, SQL, etc."]:::tool
    OBS["<b>Observe</b><br/>tool result, error, exception"]:::obs
    MEM["<b>Update memory</b><br/>short-term: scratchpad<br/>long-term: vector store / KG"]:::mem
    DONE{"<b>Done?</b>"}:::decide
    RESP["<b>Final response</b>"]:::out

    G --> T --> A
    A -->|"yes"| TOOL --> OBS --> MEM --> T
    A -->|"no, answer"| DONE
    DONE -->|"yes"| RESP
    DONE -->|"no, more work"| T

    PAR["<b>Patterns</b>"]:::opt
    PAR -.->|"ReAct, Plan-Execute,<br/>Reflexion, LATS,<br/>multi-agent supervisor"| G
    SAFETY["<b>Guardrails</b>"]:::opt
    SAFETY -.->|"sandboxed code exec,<br/>tool allowlist,<br/>cost limit, time limit,<br/>prompt-injection defense"| TOOL

    classDef goal fill:#fff176,stroke:#f57f17,stroke-width:2px
    classDef think fill:#fff9c4,stroke:#333
    classDef decide fill:#ffccbc,stroke:#333
    classDef tool fill:#ffcdd2,stroke:#333,stroke-width:2px
    classDef obs fill:#c5e1a5,stroke:#333
    classDef mem fill:#b3e5fc,stroke:#333
    classDef out fill:#d1c4e9,stroke:#333
    classDef opt fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
```

---

## 10. Fine-Tuning & Alignment Tree

How to specialize a base model.

```mermaid
graph TD
    BASE["<b>Pre-trained base model</b><br/>Llama 3.1 / Qwen 3 / Mistral<br/>(foundation, not chat-aligned)"]:::base

    BASE --> CPT["<b>Continued Pre-Training (CPT)</b><br/>domain corpus, no instruction format<br/>adds knowledge"]:::stage
    CPT --> SFT["<b>Supervised Fine-Tuning (SFT)</b><br/>instruction-following data<br/>(Alpaca, Tulu, evol-instruct)"]:::stage
    SFT --> ALIGN{"<b>Alignment stage</b>"}:::decide

    ALIGN -->|RLHF| RLHF["<b>RLHF</b><br/>reward model + PPO<br/>(InstructGPT)"]:::alg
    ALIGN -->|DPO| DPO["<b>DPO</b><br/>direct preference optimization<br/>(simpler, often as good)"]:::alg
    ALIGN -->|KTO/IPO/SimPO/ORPO| OTHER["<b>Other preference methods</b><br/>KTO, IPO, SimPO, ORPO"]:::alg
    ALIGN -->|RLAIF| RLAIF["<b>RLAIF / Constitutional AI</b><br/>AI feedback + principles"]:::alg
    ALIGN -->|Reasoning| REASON["<b>Reasoning models</b><br/>PRM + RL on chains<br/>(o1, DeepSeek-R1)"]:::alg

    SFT --> PEFT["<b>PEFT (parameter-efficient)</b><br/>LoRA, QLoRA, DoRA<br/>(don't fine-tune all params)"]:::peft

    classDef base fill:#b3e5fc,stroke:#333
    classDef stage fill:#fff9c4,stroke:#333
    classDef decide fill:#ffccbc,stroke:#333
    classDef alg fill:#c5e1a5,stroke:#333
    classDef peft fill:#f8bbd0,stroke:#333,stroke-width:2px
```

---

## 11. Multimodal AI Map

The architectures and tasks across vision, audio, video.

```mermaid
graph TD
    VISION["<b>Vision</b>"]:::vision
    AUDIO["<b>Audio</b>"]:::audio
    VIDEO["<b>Video</b>"]:::video

    subgraph VENC["<b>Encoders</b>"]
        V1[ResNet / ConvNeXt]:::arch
        V2[ViT / Swin / DeiT]:::arch
    end

    subgraph VGEN["<b>Generative</b>"]
        V3[Stable Diffusion / SDXL / Flux]:::gen
        V4[ControlNet, IP-Adapter]:::gen
    end

    subgraph VLM["<b>Vision-Language Models (VLMs)</b>"]
        V5["LLaVA / Qwen-VL / InternVL<br/>Llama 3.2 Vision / Pixtral<br/>Molmo / GPT-4o / Claude with vision"]:::vlm
    end

    DET["<b>Detection & Segmentation</b><br/>YOLO, SAM / SAM 2, Grounding DINO"]:::det

    CLIP["<b>CLIP / SigLIP</b><br/>image-text contrastive"]:::vlm

    A1["<b>ASR (speech → text)</b><br/>Whisper, Conformer, Canary"]:::audio
    A2["<b>TTS (text → speech)</b><br/>VITS, XTTS, CosyVoice, CSM"]:::audio
    A3["<b>Audio LLMs</b><br/>Qwen2-Audio, SALMONN"]:::audio

    V1 --> V5
    V2 --> V5
    CLIP --> V5
    V3 --> V5
    V4 --> V3
    V1 --> DET
    V2 --> DET

    classDef vision fill:#b3e5fc,stroke:#333
    classDef audio fill:#f8bbd0,stroke:#333
    classDef video fill:#d1c4e9,stroke:#333
    classDef arch fill:#fff9c4,stroke:#333
    classDef gen fill:#ffcdd2,stroke:#333
    classDef vlm fill:#c5e1a5,stroke:#333,stroke-width:2px
    classDef det fill:#ffccbc,stroke:#333
```

---

## 12. MLOps / LLMOps Production Stack

The layers between "model trained" and "system in production."

```mermaid
graph TD
    EXP["<b>Experiment Tracking</b><br/>W&B, MLflow, TensorBoard<br/>code + data + config + env"]:::obs
    DATA["<b>Data</b><br/>Pipelines: Airflow, Dagster, Ray Data<br/>Storage: S3, Parquet, Delta, Iceberg<br/>Feature stores: Feast, Tecton"]:::data
    TRAIN["<b>Training</b><br/>PyTorch / JAX<br/>DDP / FSDP / TP / PP"]:::train
    EVAL["<b>Eval</b><br/>golden sets, LLM-as-judge<br/>A/B, human eval, drift"]:::eval
    SERVE["<b>Serving</b><br/>Triton, BentoML, vLLM, TGI<br/>TensorRT-LLM, SGLang, llama.cpp"]:::serve
    API["<b>API Layer</b><br/>FastAPI, gRPC, GraphQL<br/>rate limit, auth, retries"]:::serve
    OBS["<b>Observability</b><br/>Prometheus, Grafana, OpenTelemetry<br/>Langfuse, Arize, Phoenix<br/>(latency, drift, hallucination rate)"]:::obs
    CACHE["<b>Cache & Cost</b><br/>prompt cache, semantic cache<br/>spot GPUs, autoscaling"]:::serve
    MON["<b>Monitor + Iterate</b><br/>retraining triggers<br/>rollback, canary deploys"]:::mon

    EXP --> TRAIN
    DATA --> TRAIN
    TRAIN --> EVAL --> SERVE --> API --> OBS
    API --> CACHE
    OBS --> MON
    MON -->|"feedback"| EXP
    MON -->|"feedback"| DATA

    classDef exp fill:#fff9c4,stroke:#333
    classDef data fill:#b3e5fc,stroke:#333
    classDef train fill:#c5e1a5,stroke:#333
    classDef eval fill:#d1c4e9,stroke:#333
    classDef serve fill:#ffcdd2,stroke:#333
    classDef obs fill:#ffccbc,stroke:#333
    classDef mon fill:#f8bbd0,stroke:#333,stroke-width:2px
```

---

## 13. Distributed Training Strategies

How to scale training across many GPUs.

```mermaid
graph TD
    MODEL["<b>Single model</b><br/>F params, B bytes/param"]:::model

    subgraph PARALLEL["<b>Parallelism strategies</b>"]
        DP["<b>Data Parallel (DDP)</b><br/>replicate model, split data<br/>AllReduce gradients"]:::strat
        Z1["<b>ZeRO-1</b><br/>shard optimizer state"]:::strat
        Z2["<b>ZeRO-2</b><br/>+ shard gradients"]:::strat
        Z3["<b>ZeRO-3 / FSDP</b><br/>+ shard parameters"]:::strat
        TP["<b>Tensor Parallel</b><br/>split each layer's matmul<br/>across GPUs (Megatron)"]:::strat
        PP["<b>Pipeline Parallel</b><br/>split layers across GPUs<br/>(GPipe, 1F1B)"]:::strat
        SP["<b>Sequence / Context Parallel</b><br/>split long sequences"]:::strat
        EP["<b>Expert Parallel (MoE)</b><br/>route tokens to experts"]:::strat
    end

    COMB["<b>3D Parallelism</b><br/>DP × TP × PP"]:::strat
    COMB2["<b>4D / 5D</b><br/>+ SP + EP for MoE / long ctx"]:::strat

    MODEL --> DP
    DP --> Z1 --> Z2 --> Z3
    MODEL --> TP
    MODEL --> PP
    TP & PP --> COMB
    Z3 & SP & EP --> COMB2

    FA["<b>Optimizations</b>"]:::opt
    FA -.->|"gradient checkpointing,<br/>AMP, FlashAttention,<br/>activation recompute"| DP
    FA -.-> COMB

    classDef model fill:#b3e5fc,stroke:#333
    classDef strat fill:#c5e1a5,stroke:#333
    classDef opt fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
```

---

## 14. GPU Memory Hierarchy (Performance)

What the hardware looks like, and why kernel optimization matters.

```mermaid
graph TD
    HBM["<b>HBM / VRAM</b><br/>~3 TB/s on H100<br/>~80 GB on H100 SXM<br/>(the bandwidth wall)"]:::mem
    L2["<b>L2 Cache</b><br/>~50 MB on H100"]:::cache
    SMEM["<b>Shared Memory</b><br/>~228 KB per SM, software-managed"]:::cache
    REG["<b>Registers</b><br/>~64K per SM, fastest"]:::cache
    COMPUTE["<b>Tensor / CUDA cores</b><br/>(the actual math)"]:::compute

    HBM -->|coalesced loads| L2 --> SMEM --> REG --> COMPUTE
    COMPUTE -.->|store back| HBM

    ROOF["<b>Roofline model</b>"]:::opt
    ROOF -.->|"memory-bound vs compute-bound<br/>decides which knob to turn"| HBM
    ROOF -.-> COMPUTE

    TECH["<b>Kernel techniques</b>"]:::opt
    TECH -.->|"tiling, fusion,<br/>FlashAttention,<br/>persistent kernels,<br/>Triton, CUTLASS"| SMEM
    TECH -.->|"mixed precision (FP8/BF16/FP16),<br/>quantization (INT8/INT4)"| HBM

    classDef mem fill:#ffccbc,stroke:#333
    classDef cache fill:#fff9c4,stroke:#333
    classDef compute fill:#c5e1a5,stroke:#333,stroke-width:2px
    classDef opt fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
```

---

## 15. The AI Engineer Interview Loop

Verified June 2026: Anthropic and OpenAI process specifics.

```mermaid
graph TD
    APP["<b>Application / Referral</b>"]:::start
    REC["<b>Recruiter screen</b><br/>15–30 min, behavior + comp chat<br/>(treat any number as informational)"]:::step
    PHONE["<b>Technical phone screen</b><br/>60–90 min, CodeSignal/Replit/Colab<br/><b>multi-tiered practical problems</b><br/>(web crawler → multi-thread → filter;<br/>or in-memory DB with TTL)<br/>ML roles: MCP, model reliability"]:::step

    L1["<b>Onsite Loop 1 (Anthropic)</b><br/>system design, coding, culture fit"]:::loop
    L2["<b>Onsite Loop 2 (Anthropic)</b><br/>only if Loop 1 passed<br/>project deep-dive, goals"]:::loop

    FINAL["<b>Final loop (OpenAI)</b><br/>4–6 sessions, 1–2 days<br/>2nd coding, 2nd design,<br/>behavioral, cross-functional,<br/><b>~1 hour project walkthrough</b>"]:::loop

    OOP["<b>OpenAI SWE coding</b><br/>may include OOP / class design<br/>(e.g., layered chatbot interface)<br/>not just DSA"]:::note
    RESEARCH["<b>OpenAI research eng bar</b><br/>'graduate-level ML and info theory'<br/>(derivations, samplers, transformers)"]:::note

    DEC["<b>Decision</b>"]:::decision
    OFFER["<b>Offer + Comp negotiation</b><br/>Anthropic P50 ₹/TC, Google P75,<br/>Anthropic median SWE = $665K"]:::offer

    APP --> REC --> PHONE

    PHONE -->|Anthropic| L1
    L1 -->|pass| L2
    L2 --> DEC
    L1 -->|fail| REJ["<b>Rejected</b>"]:::reject

    PHONE -->|OpenAI| FINAL
    FINAL --> DEC
    OOP -.-> FINAL
    RESEARCH -.-> FINAL

    DEC -->|yes| OFFER
    DEC -->|no| REJ

    classDef start fill:#fff176,stroke:#f57f17,stroke-width:2px
    classDef step fill:#b3e5fc,stroke:#333
    classDef loop fill:#ffcdd2,stroke:#333
    classDef decision fill:#ffccbc,stroke:#333
    classDef offer fill:#c5e1a5,stroke:#333,stroke-width:3px
    classDef note fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
    classDef reject fill:#eeeeee,stroke:#999
```

---

## 16. Project Portfolio Map

The 5 flagship projects that anchor a senior+ portfolio. Build in this order.

```mermaid
graph LR
    P0["<b>P0: Tiny GPT from scratch</b><br/>Karpathy-style<br/>BPE + transformer + training<br/>(depth proof)"]:::p0
    P1["<b>P1: Tabular ML service</b><br/>XGBoost + FastAPI + deployed<br/>(engineering basics proof)"]:::p1
    P2["<b>P2: RAG system</b><br/>hybrid retrieval + reranking + evals<br/>(applied AI proof)"]:::p2
    P3["<b>P3: Fine-tuned LLM</b><br/>QLoRA + DPO on domain<br/>(customization proof)"]:::p3
    P4["<b>P4: AI agent</b><br/>tool use + memory + sandbox<br/>(autonomy proof)"]:::p4
    P5["<b>P5: Production-deployed system</b><br/>observability + cost + scaling<br/>(staff proof)"]:::p5

    OSS["<b>OSS contribution</b><br/>vLLM / TRL / LangChain / Instructor<br/>(collaboration proof)"]:::oss

    P0 --> P1 --> P2 --> P3 --> P4 --> P5
    P2 -.-> OSS
    P3 -.-> OSS
    P4 -.-> OSS

    classDef p0 fill:#b3e5fc,stroke:#333
    classDef p1 fill:#c5e1a5,stroke:#333
    classDef p2 fill:#fff9c4,stroke:#333
    classDef p3 fill:#ffccbc,stroke:#333
    classDef p4 fill:#ffcdd2,stroke:#333
    classDef p5 fill:#d1c4e9,stroke:#333,stroke-width:3px
    classDef oss fill:#cfd8dc,stroke:#333
```

---

## 17. Compensation Strategy Tree (India)

Where you can land, what it pays, and how to move up.

```mermaid
graph TD
    A["<b>Where you are</b>"]:::start

    A --> B{"<b>Where to aim</b>"}:::decision

    B -->|Tier 1: US AI labs| T1["OpenAI India<br/>Google DeepMind India<br/>Google India · Microsoft Research<br/>Meta India · Amazon India<br/>NVIDIA India · Apple India"]:::tier1

    B -->|Tier 2: Indian AI unicorns| T2["Sarvam AI ($1.5B Series B)<br/>Krutrim<br/>CRED · PhonePe · Flipkart<br/>Meesho · Razorpay<br/>Yellow.ai · Observe.AI · Fractal"]:::tier2

    B -->|Tier 3: Service safety net| T3["TCS / Infosys / Wipro / HCL<br/>Accenture / Capgemini / Cognizant<br/>(₹6L–₹60L, high volume)"]:::tier3

    T1 --> COMP1["<b>Verified comp</b><br/>Google India P75 = ₹80.9L<br/>Microsoft India P75 = ₹68.0L<br/>Amazon India P75 = ₹73.0L<br/>OpenAI India anchor = ₹55.8L"]:::comp
    T2 --> COMP2["<b>Verified comp</b><br/>CRED P75 = ₹88.0L · P90 = ₹1.02Cr<br/>Meesho P75 = ₹71.4L<br/>PhonePe P75 = ₹58.1L<br/>Flipkart P75 = ₹53.5L"]:::comp
    T3 --> COMP3["<b>Typical comp</b><br/>₹6–25L fresher<br/>₹30–60L senior"]:::comp

    UP["<b>Move up: L4 → L5 → L6</b><br/>(internal promo)"]:::up
    US["<b>US transfer: highest leverage</b><br/>L5 US = $500K–$800K = ₹4.2–6.7Cr<br/>Plan: 12–18 mo India → transfer<br/>or direct US application"]:::up

    T1 --> UP
    T2 --> UP
    UP --> US

    NEG["<b>Negotiation tactics</b><br/>cite Levels.fyi P50–P75<br/>always counter 10–30%<br/>multiple offers in parallel<br/>RSU refresh, relocation bonus"]:::neg

    T1 --> NEG
    T2 --> NEG

    classDef start fill:#fff176,stroke:#f57f17,stroke-width:2px
    classDef decision fill:#ffccbc,stroke:#333
    classDef tier1 fill:#c5e1a5,stroke:#333,stroke-width:2px
    classDef tier2 fill:#b3e5fc,stroke:#333
    classDef tier3 fill:#eeeeee,stroke:#999
    classDef comp fill:#fff9c4,stroke:#333
    classDef up fill:#d1c4e9,stroke:#333,stroke-width:2px
    classDef neg fill:#cfd8dc,stroke:#333,stroke-dasharray:5 5
```

---

## 18. The Career-Compounding Loop

The positive-feedback cycle that turns senior engineers into staff+.

```mermaid
graph LR
    P["<b>Pick hard, high-leverage problems</b>"]:::step
    S["<b>Ship them in public</b><br/>(GitHub, blog, OSS)"]:::step
    R["<b>Reputation for closing the loop</b>"]:::step
    H["<b>Pulled into higher-visibility work</b>"]:::step
    N["<b>Use leverage for the next role</b>"]:::step
    P2["<b>Pick harder problems...</b>"]:::step

    P --> S --> R --> H --> N --> P2
    P2 -.->|"compounds"| P

    classDef step fill:#c5e1a5,stroke:#333,stroke-width:2px
```

---

## 19. 24-Month Execution Flow

The phased plan, condensed.

```mermaid
graph LR
    P0["<b>Phase 0</b><br/>Foundations<br/>Weeks 1–8"]:::p0
    P1["<b>Phase 1</b><br/>Classical ML + DL<br/>Weeks 9–24"]:::p1
    P2["<b>Phase 2</b><br/>LLMs + RAG + Agents<br/>Weeks 25–48"]:::p2
    P3["<b>Phase 3</b><br/>Production + Specialize<br/>Weeks 49–72"]:::p3
    P4["<b>Phase 4</b><br/>Interview + Compounding<br/>Weeks 73–96"]:::p4

    SHIP1["<b>Ship #1</b><br/>Tabular ML service"]:::ship
    SHIP2["<b>Ship #2</b><br/>Tiny GPT + RAG"]:::ship
    SHIP3["<b>Ship #3</b><br/>Fine-tune + Agent + OSS"]:::ship
    SHIP4["<b>Ship #4</b><br/>Production system + specialty"]:::ship
    OFFER["<b>Outcome</b><br/>Multiple offers,<br/>$400K+ US / ₹1Cr+ India"]:::goal

    P0 --> P1 --> P2 --> P3 --> P4 --> OFFER
    P1 --> SHIP1
    P2 --> SHIP2
    P3 --> SHIP3
    P4 --> SHIP4

    PAR["<b>Always running</b><br/>1 paper/wk · 1 blog/mo<br/>1 chat/wk with someone ahead<br/>sleep 7+ hrs"]:::parallel

    PAR -.-> P0 & P1 & P2 & P3 & P4

    classDef p0 fill:#b3e5fc,stroke:#333
    classDef p1 fill:#c5e1a5,stroke:#333
    classDef p2 fill:#fff9c4,stroke:#333
    classDef p3 fill:#ffccbc,stroke:#333
    classDef p4 fill:#ffcdd2,stroke:#333
    classDef ship fill:#cfd8dc,stroke:#333
    classDef parallel fill:#eeeeee,stroke:#666,stroke-dasharray:5 5
    classDef goal fill:#d1c4e9,stroke:#333,stroke-width:3px
```

---

## How to Use These Maps

1. **Open the roadmap (`AI_ENGINEER_MASTERY_ROADMAP.md`) and this file side-by-side.** When you read a section, glance at the matching map first to anchor the mental model.
2. **Print the 24-Month Execution Flow and the Whole System map.** Pin them.
3. **Use the Foundation / DSA / Math maps to identify gaps.** Be honest — if you can't derive backprop on paper, the math map is calling.
4. **Use the Interview Loop map** during Weeks 22–24 of the 6-month plan to rehearse the actual flow.
5. **Use the Project Portfolio map** to track which flagships you have shipped.
6. **Use the India Compensation Tree** to plan your application strategy in months 5–6.

> These are living documents. As you learn, you will redraw them in your own words. That is the point.
