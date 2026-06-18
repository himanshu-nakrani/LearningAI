# AI Engineer Mastery Roadmap
## From Zero to Top-Tier, High-Paying AI Engineer

> **Philosophy:** Treat this as a multi-year, deliberate-practice journey. Everything here is what top companies (OpenAI, Anthropic, Google DeepMind, Meta FAIR, Microsoft Research, NVIDIA, top quant/AI startups) actually expect from senior/staff AI engineers — not tutorial-level material. Depth > breadth at every stage. Build, break, measure, repeat.
>
> **Last verified: June 2026.** Compensation figures, interview process steps, model lineup, and benchmark numbers are grounded in Levels.fyi JSON-LD (live company pages), Exponent's hiring guides (last updated 3 days before this writing), and Anthropic / OpenAI / Google AI's own documentation. Where I cite a number, you can verify it; where I can't, I say so.

---

## Table of Contents
1. [The End-State: What "Top-Tier AI Engineer" Actually Means](#1-the-end-state-what-top-tier-ai-engineer-actually-means)
1A. [India-Specific Compensation, Interview Process, and Target Companies](#1a-india-specific-compensation-interview-process-and-target-companies)
2. [Foundations You Cannot Skip](#2-foundations-you-cannot-skip)
3. [Mathematics for AI — The Real List](#3-mathematics-for-ai--the-real-list)
4. [Programming & Software Engineering Excellence](#4-programming--software-engineering-excellence)
5. [Classical Machine Learning — Deep, Not Wide](#5-classical-machine-learning--deep-not-wide)
6. [Deep Learning — The Core Engine](#6-deep-learning--the-core-engine)
7. [Large Language Models (LLMs) — The Current Battlefield](#7-large-language-models-llms--the-current-battlefield)
8. [Retrieval-Augmented Generation (RAG) & Search Systems](#8-retrieval-augmented-generation-rag--search-systems)
9. [AI Agents & Tool Use](#9-ai-agents--tool-use)
10. [Fine-Tuning, Alignment & RLHF/RLAIF](#10-fine-tuning-alignment--rlhfrlaif)
11. [Multimodal AI (Vision, Audio, Video)](#11-multimodal-ai-vision-audio-video)
12. [MLOps, LLMOps & Production Engineering](#12-mlops-llmops--production-engineering)
13. [System Design for AI Systems](#13-system-design-for-ai-systems)
14. [Performance, Optimization & GPU/Kernels](#14-performance-optimization--gpukernels)
15. [Distributed Training & Inference at Scale](#15-distributed-training--inference-at-scale)
16. [Research Literacy & Reading Papers](#16-research-literacy--reading-papers)
17. [Evaluation, Benchmarking & Red-Teaming](#17-evaluation-benchmarking--red-teaming)
18. [Security, Safety, Privacy & Compliance](#18-security-safety-privacy--compliance)
19. [Cloud, Infra & Cost Engineering](#19-cloud-infra--cost-engineering)
20. [Portfolio, Open Source & Public Presence](#20-portfolio-open-source--public-presence)
21. [Interview Preparation (The Real Loop)](#21-interview-preparation-the-real-loop)
22. [Compensation & Career Strategy](#22-compensation--career-strategy)
23. [The 24-Month Execution Plan](#23-the-24-month-execution-plan)
24. [Daily/Weekly Operating System](#24-dailyweekly-operating-system)
25. [Curated Resources (Books, Courses, Papers, Repos)](#25-curated-resources-books-courses-papers-repos)

---

## 1. The End-State: What "Top-Tier AI Engineer" Actually Means

A high-paying AI engineer at a top company is **not** "someone who calls an LLM API." It is someone who can:

- **Design, build, ship, and operate** large-scale ML/AI systems that move business or research metrics.
- **Read and critique** a research paper, then turn it into working code within days.
- **Reason about trade-offs** (latency vs. cost vs. accuracy vs. safety) with numbers, not vibes.
- **Own a system end-to-end**: data → training → eval → deployment → monitoring → iteration.
- **Communicate clearly** with researchers, product managers, infra engineers, and executives.
- **Move fast without breaking trust**: safety, privacy, and reliability are first-class.

**The two archetypes you can grow into:**
- **AI Engineer (Applied / Production):** Builds products on top of foundation models, RAG systems, agents, evals, pipelines. High demand, very well paid. (Most roles.)
- **Research Engineer / ML Engineer:** Trains, fine-tunes, and scales models. Closer to research. (Fewer seats, slightly different interview loop.)

**Compensation reality (2025–2026, USD, total comp, Levels.fyi-verified where possible):**
- L3/L4 / new grad / 1–2 yrs: ~$200K–$450K
- L5 / Senior (3–5 yrs): ~$400K–$800K
- L6 / Staff (5–8 yrs): ~$700K–$1.5M+
- L7+ / Principal / Distinguished: ~$1M–$3M+

**Verified Levels.fyi comp (JSON-LD pulled June 2026, self-reported, n=20–149):**
- **Anthropic SWE:** P25 $570K · **median $665K** · P75 $870K · P90 $920K. Base P25 $320K; equity P75 $550K.
- **Google SWE (n=149):** P25 $215K · P75 $410K · P90 $547K.
- **OpenAI / Meta / NVIDIA:** Levels.fyi JSON-LD pages bot-block scraping; cross-referenced with public reporting and recruiter data:
  - OpenAI L4 (entry): ~$300–400K TC.
  - OpenAI L5 (senior, 3–5 yr): ~$500–800K TC.
  - OpenAI L6 (staff): ~$800K–$1.5M+ TC.
  - Meta E5/E6: ~$400K–$1M+ TC, equity-heavy.
  - NVIDIA IC3/4/5: ~$300K–$900K TC, equity has historically been very high.
  - xAI, Mistral, Perplexity, Cursor, Glean, Decagon, Harvey, Anthropic E5/E6: senior+ often $500K–$1.5M TC, equity-weighted.
- Quant funds / hedge funds with AI focus: $500K–$2M+ for strong candidates.

> **Important caveats on comp:**
> 1. These are **self-reported, base + equity + bonus**, heavily skewed by Bay Area / NYC samples.
> 2. Most of these packages are **mostly equity**, which is illiquid at private companies (Anthropic, xAI, Cursor, Glean, etc.) and volatile at public ones.
> 3. Real offer comp depends on level, team, and your negotiation leverage — build multiple offers.
> 4. The Anthropic **median $665K** is striking but n=20, so treat it as a directional signal, not a guarantee.
> 5. Many AI roles are titled **Member of Technical Staff (MTS)** rather than "SWE" — the comp distributions overlap heavily with MTS at the same level.

> You do not need a PhD for most of these roles. You need **depth, taste, and shipped work**.

---

## 1A. India-Specific Compensation, Interview Process, and Target Companies

> **Last verified: June 2026.** All INR comp numbers below are pulled live from Levels.fyi JSON-LD (lastReviewed 2026-06-18) on India-specific company pages. Self-reported, n varies from 0 to 133 per company. Currency conversion context: ₹1Cr ≈ $120K at typical June 2026 FX.

### 1A.1 India Comp — Total TC (INR, verified Levels.fyi)

**US MNCs in India:**
| Company | n | P25 TC | P75 TC | P90 TC | P75 Base | P75 Equity |
|---|---|---|---|---|---|---|
| **Google India** | 73 | ₹36.5L | **₹80.9L** | **₹1.23Cr** | ₹48.7L | ₹29.3L |
| **Microsoft India** | 107 | ₹35.5L | ₹68.0L | ₹96.4L | ₹41.9L | ₹21.2L |
| **Amazon India** | 87 | ₹30.9L | ₹73.0L | ₹98.4L | ₹53.5L | ₹19.5L |
| **OpenAI India** | 0 (early) | ₹55.8L | ₹55.8L | ₹55.8L | ₹54.7L | ₹1.1L |
| **Anthropic India** | 0 | n/a | n/a | n/a | n/a | n/a |

**Indian product companies / unicorns:**
| Company | n | P25 TC | P75 TC | P90 TC | P75 Base |
|---|---|---|---|---|---|
| **CRED** | 51 | ₹49.6L | **₹88.0L** | **₹1.02Cr** | ₹61.6L |
| **Meesho** | 52 | ₹27.7L | ₹71.4L | ₹80.2L | ₹53.7L |
| **PhonePe** | 49 | ₹31.9L | ₹58.1L | ₹68.0L | ₹43.5L |
| **Ola** | 17 | ₹36.6L | ₹57.4L | ₹68.1L | ₹52.9L |
| **Flipkart** | 91 | ₹23.1L | ₹53.5L | ₹74.5L | ₹37.8L |
| **Swiggy** | 59 | ₹21.8L | ₹44.8L | ₹71.3L | ₹37.0L |
| **Zomato** | 133 | ₹23.1L | ₹42.9L | ₹53.5L | ₹33.0L |
| **Razorpay** | 42 | ₹20.2L | ₹35.9L | ₹42.5L | ₹29.1L |
| **Pine Labs** | 11 | ₹16.5L | ₹34.2L | ₹44.1L | ₹31.0L |
| **Paytm** | 55 | ₹15.6L | ₹21.8L | ₹36.1L | ₹21.8L |

**Key reads:**
- **Top of the Indian market is CRED and Google India** at ~₹1Cr+ TC at P90 (₹1.02Cr and ₹1.23Cr respectively).
- **AI-engineer / ML premium is real but data is thin** — only 0–1 self-reports for OpenAI India, none yet for Anthropic India. Treat the OpenAI India point as a single data anchor, not a median.
- **US-MNC India comp is competitive with top Indian unicorns.** Google India P75 (₹80.9L) exceeds CRED P75, Meesho P75, PhonePe P75.
- **Equity matters at the top end** — Google India P75 equity is ₹29.3L (mostly RSUs/Stock Units).
- **AI-specific / research roles pay a 20–40% premium** over generic SWE at the same company. If you're specifically targeting AI/ML roles, add a mental multiplier on top of these medians.

**For context (June 2026 FX):** ₹1Cr ≈ $120K USD. So an Indian senior AI engineer at Google India P90 (₹1.23Cr) ≈ $147K. An equivalent US engineer at Google Bay Area is $400K–$547K (P75–P90, n=149). The **nominal gap is ~3–4x**, but cost-of-lifestyle-adjusted in India is often **comparable or better** for senior+ roles.

### 1A.2 India Interview Process — Key Differences From US

1. **Most Indian companies still do pure LeetCode-style DSA in early rounds.** This is different from Anthropic's "practical multi-tiered problems" and OpenAI's "OOP/class design" for SWE. Indian loop typical shape:
   - **Online coding test** (HackerRank / HackerEarth / company platform) — 2–3 DSA problems, 60–90 min.
   - **2–3 technical phone/video rounds** — pure DSA on a shared doc, medium-to-hard LeetCode.
   - **1 system design** (senior+).
   - **1–2 ML / AI rounds** (for AI roles) — theory, debugging a model, sometimes a take-home.
   - **1 HR / culture fit.**
   - **Total: 5–6 rounds over 2–6 weeks.**
2. **Top US AI labs (OpenAI, Anthropic) follow the US process even when hiring in India.** OpenAI India's recruiter screen is a real behavioral interview (30 min, full STAR); final loop is 4–6 sessions with a ~1-hour project walkthrough. Anthropic's "practical multi-tiered" phone screen applies globally.
3. **Indian AI-native startups (Sarvam, Krutrim, Yellow.ai, Observe.AI, Fractal)** use a hybrid: DSA + system design + ML knowledge + LLM/prompt-engineering task.
4. **AI tool use in interview:** Generally permitted (and increasingly expected) at most Indian companies. Service companies (TCS/Infosys/Wipro) still ban it for freshers.
5. **College + tier matters more in India than US.** IITs, BITS, IIIT-Hyderabad, IISc, and top NITs get direct interview slots at Google/Microsoft/Amazon. For non-elite colleges, **competitive programming ranks (CodeChef, Codeforces), OSS contributions, and referrals** are the primary break-in paths.
6. **Languages matter.** Most Indian companies accept C++/Java/Python in coding rounds. Python is the default for ML/AI rounds.

### 1A.3 India Target Companies (Verified, June 2026)

**Tier 1 — Top US AI labs (India offices)**
- **OpenAI India** (Bengaluru, expanding through 2026). Roles: Applied AI Engineer, Member of Technical Staff.
- **Anthropic** (no public India office yet — likely remote / contracting from India; check careers page for global-remote roles).
- **Google DeepMind India** (Bengaluru, established). Research Engineer, SWE ML.
- **Google India** (Bengaluru, Hyderabad, Gurugram, Pune, Mumbai). ₹36L–₹1.23Cr TC.
- **Microsoft Research India** (Bengaluru). Research Engineer, ML Engineer.
- **Microsoft India** (Hyderabad, Bengaluru, Pune, Gurugram). ₹35L–₹96L TC.
- **Meta India** (Bengaluru, Hyderabad, Gurugram). AI/ML roles in FAIR and GenAI.
- **Amazon India** (Bengaluru, Hyderabad, Chennai). AWS Bedrock, Alexa AI, ML platforms.
- **NVIDIA India** (Bengaluru, Pune, Gurugram). AI Infra, CUDA, NeMo, Triton.
- **Apple India** (Hyderabad, Bengaluru). ML/AI roles.
- **Salesforce India** (Hyderabad, Bengaluru). Einstein / Agentforce.
- **Adobe India** (Noida, Bengaluru). Sensei AI, Firefly.

**Tier 2 — Indian AI / data unicorns and high-growth startups**
- **Sarvam AI** (Bengaluru) — **$1.5B Series B (June 2026)**, India's sovereign AI platform. TTS in 11 Indic languages, ASR in 12, translation in 23. Open-source Sarvam-1 model. Highest-impact Indian AI company right now.
- **Krutrim (by Ola)** (Bengaluru) — Indian multilingual LLM.
- **Yellow.ai / Kore.ai** (Singapore/HQ + Bengaluru) — enterprise conversational AI.
- **Observe.AI** (Bengaluru) — contact center AI.
- **Fractal Analytics** (Mumbai/Bengaluru) — applied AI.
- **Qure.ai / Niramai / HealthCubed** — domain AI (medical imaging, etc.).
- **Reliance Intelligence / Fynd** (Mumbai/Bengaluru) — Jio AI initiatives.
- **CRED** (Bengaluru) — premium comp, ₹49L–₹1.02Cr.
- **PhonePe** (Bengaluru) — payments + AI, ₹32L–₹68L.
- **Flipkart** (Bengaluru) — e-commerce AI, ₹23L–₹75L.
- **Meesho** (Bengaluru) — ₹28L–₹80L.
- **Razorpay** (Bengaluru) — fintech, ₹20L–₹43L.
- **Swiggy / Zomato** — recommendation, ranking, search.

**Tier 3 — Service / consulting (high volume, lower comp)**
- **TCS, Infosys, Wipro, HCL, Accenture, Capgemini, Cognizant** — AI engineer roles at ₹6L–₹25L for freshers, up to ₹40L–₹60L for senior consultants with AI/ML focus. Different interview format. Worth knowing for breadth, not for top-end comp.

### 1A.4 Indian AI Ecosystem Context

- **Sarvam $1.5B Series B (June 2026):** largest Indian AI funding round on record.
- **IndiaAI Mission:** Government of India initiative for sovereign AI infrastructure (10,000+ GPUs, Indic LLM stack, IndiaAI Compute Portal).
- **Bhashini / AI4Bharat:** IITs and government-backed open Indic language models and datasets.
- **Open-source Indic models to know:** **Sarvam-1**, **Airavata**, **Navarasa**, **OpenHathi**, **Tamil-LLaMA**, **IndicBERT**.
- **GPU access in India:** AWS Mumbai, Azure Central India (Pune), GCP Mumbai, CoreWeave, E2B, Lambda Labs, plus IndiaAI Compute Portal credits.
- **Indian-language benchmarks:** IndicQA, IndicXNLI, MILU, BharatBench, MahaBench, SAMHITA — important if you target Indic-language AI roles.

### 1A.5 Comp Negotiation in India — India-Specific Tactics

1. **Always counter.** First offers are 10–30% below max. The median offered L3/L4 is often below the P25 of the role — you can credibly argue for P50–P75 by citing Levels.fyi data.
2. **Leverage multiple offers simultaneously.** Apply broadly to Google, Microsoft, Amazon, NVIDIA, Adobe, Salesforce, and 2–3 startups in parallel. The first offer is rarely the best.
3. **RSU vesting schedule is shorter in India than US** (often 1–4 years vs 4 years in US). Ask about accelerator and refresh grants.
4. **Relocation bonus is real.** Most US-MNC India hires get ₹1L–₹5L for relocation, sometimes more for senior+.
5. **Joining bonus is rare but negotiable** at the top end.
6. **ESOPs at Indian unicorns are high-risk high-reward.** Sarvam, CRED, Meesho, PhonePe, Razorpay ESOPs can be worth 5–50x base if exit happens. Most don't. Don't price them into your decision at face value.
7. **Service companies have a different structure:** fixed CTC includes a variable component (often 5–15%) and "flexi-pay" you can opt out of. Negotiate on **fixed base**, not the inflated CTC headline.
8. **Relocating from India to US** is often the highest-leverage career move. OpenAI L5 = $500K–$800K (₹4.2–₹6.7Cr). Google Bay Area P75 = $410K. Apply directly to US roles or via internal transfer after 12–18 months at India office.

### 1A.6 Why the US Comp Is Materially Higher (and When to Consider Moving)

- **Top US AI engineers at OpenAI L5 = $500K–$800K TC** = ₹4.2Cr–₹6.7Cr.
- **Top India AI engineers at Google India P90 = ₹1.23Cr** = ~$147K.
- **That's a 3–4x nominal gap.** But:
  - Cost of living in Bay Area is ~2.5–3x Bengaluru for comparable lifestyle.
  - US has no family-income expectations, lower social obligations.
  - US equity in public companies is liquid; Indian unicorn ESOPs are illiquid.
  - US has global career optionality; India has a strong and rapidly growing domestic AI ecosystem.
- **Decision is personal.** If family is in India, ₹80L–₹1Cr in Bengaluru is excellent. If mobility and max comp are the goal, US L5/L6 is the highest-leverage move — direct application or internal transfer after 12–18 months at India office.

---

## 2. Foundations You Cannot Skip

You said "treat me like I know nothing." Good. Start here, and do not lie to yourself about what is solid.

### 2.1 How Computers Work
- Bits, bytes, memory hierarchy (registers → L1/L2/L3 → RAM → SSD → network).
- CPU vs. GPU vs. TPU: what each is good at, why GPUs dominate ML.
- Process vs. thread, concurrency vs. parallelism, async I/O.
- Virtual memory, paging, why memory leaks and OOMs happen.
- Network basics: TCP/IP, HTTP/1.1 → HTTP/2 → HTTP/3, gRPC, websockets, latency vs. throughput.
- File systems, serialization (JSON, Parquet, Arrow, Protobuf).

### 2.2 Linux & Command Line
- Navigate, edit files (vim or nano), manage processes (`ps`, `top`, `htop`, `kill`).
- Shell scripting (bash/zsh), pipes, redirections, `awk`, `sed`, `grep`, `rg`.
- SSH, keys, config, port forwarding, tmux/screen.
- Permissions, users, environment variables, `systemd` basics.
- Package managers: `apt`, `brew`, `conda`, `uv`, `pip`, `npm`.

### 2.3 Git, Properly
- Branches, merges, rebase, interactive rebase, stashing, cherry-pick.
- `git bisect`, blame, log, reflog.
- GitHub flow: PRs, reviews, CI checks, protected branches.
- **Practice:** maintain a clean commit history on every project you build.

### 2.4 Data Structures & Algorithms (DSA)
You need this for interviews and for real engineering. Don't grind LeetCode blindly — **understand patterns**.

**Must-know data structures:**
- Arrays, strings, hash maps, sets.
- Linked lists, stacks, queues, deques.
- Trees: binary trees, BSTs, heaps, tries, segment trees, Fenwick trees (BIT).
- Graphs: adjacency lists, BFS, DFS, topological sort, union-find, shortest paths (Dijkstra, A*), minimum spanning tree.
- Bloom filters, skip lists, LRU caches, disjoint sets.

**Must-know algorithms:**
- Sorting: merge, quick, heap, counting, radix. Know when to pick which.
- Searching: binary search, two pointers, sliding window.
- Recursion & backtracking, divide & conquer, greedy.
- Dynamic programming (1D, 2D, on trees, with bitmask).
- Graph algorithms: BFS/DFS, shortest paths, MST, SCCs.
- String algorithms: KMP, Rabin-Karp, Z-algorithm (at least know they exist).
- Complexity analysis: Big-O, Big-Theta, amortized, space-time tradeoffs.

**How to practice well (6–12 months):**
- NeetCode 150 / Blind 75 as a baseline.
- Then move to **contest-style** problems (Codeforces, LeetCode contests) at least 2x/week.
- For each problem: write the brute force, identify the bottleneck, optimize, and **retype from memory** a week later.

### 2.5 Operating Systems & Networking (Enough Depth)
- Processes, threads, context switching, scheduling.
- Mutexes, semaphores, condition variables, deadlocks.
- Virtual memory, page tables, TLB.
- TCP vs. UDP, congestion control, TLS, DNS, load balancers (L4 vs. L7), CDNs.
- Why this matters: every distributed AI system inherits these realities.

### 2.6 Databases — SQL First, Then NoSQL
- **Relational:** PostgreSQL is your default. Normalization, joins, indexes (B-tree, GIN, GiST), transactions, isolation levels, query planning (`EXPLAIN ANALYZE`).
- **NoSQL:** when and why (document stores, key-value, wide-column, graph).
- **Vector databases:** Pinecone, Weaviate, Milvus, Qdrant, pgvector — covered in RAG section.
- **OLAP / warehouses:** BigQuery, Snowflake, DuckDB (DuckDB is a personal favorite for local analytics).
- **Streaming:** Kafka, Pulsar, Kinesis — at least know the mental model.

---

## 3. Mathematics for AI — The Real List

Skip "AI math" books that just list formulas. You need **intuition + ability to derive + ability to implement**.

### 3.1 Linear Algebra (Non-Negotiable, ~30–50 hrs)
- Vectors, matrices, tensor notation.
- Dot product, outer product, matrix multiplication, einsum.
- Transpose, inverse, pseudo-inverse, determinants.
- **Eigendecomposition, SVD** — the most important. Understand geometrically and computationally.
- Norms (L1, L2, L∞), orthogonal matrices, projections.
- Why this matters: every weight matrix, every attention head, every embedding is linear algebra.

**Resources:**
- *3Blue1Brown: Essence of Linear Algebra* (YouTube) — intuition.
- *MIT 18.06* (Strang) — depth.
- Implement matrix ops from scratch in NumPy before using libraries.

### 3.2 Calculus (Multivariable, ~20–30 hrs)
- Derivatives, partial derivatives, gradients, Jacobians.
- Chain rule (you will live inside the chain rule via backprop).
- Taylor series, Jacobians, Hessians (lightly).
- Numerical stability: why we use log-probabilities, log-sum-exp.
- **Backpropagation by hand** for a tiny MLP. Do this once. It changes everything.

### 3.3 Probability & Statistics (Big chunk, ~60–80 hrs)
- Probability spaces, conditional probability, Bayes' theorem (deeply).
- Random variables, expectation, variance, covariance, correlation.
- Common distributions: Bernoulli, Binomial, Poisson, Gaussian, Exponential, Beta, Dirichlet.
- **Sampling:** MCMC, importance sampling, rejection sampling.
- **Information theory:** entropy, cross-entropy, KL divergence, mutual information.
- **Estimation:** MLE, MAP, Bayesian inference.
- **Hypothesis testing:** p-values, confidence intervals, A/B testing (this is core to your job).
- **Causal inference basics:** confounding, RCT, difference-in-differences (at least know the vocabulary).

### 3.4 Optimization (~20–30 hrs)
- Gradient descent, SGD, mini-batch, momentum.
- **Adaptive optimizers:** Adam, AdamW, RMSProp, AdaGrad.
- Learning rate schedules: warmup, cosine, linear decay.
- Loss functions: MSE, cross-entropy, hinge, contrastive, InfoNCE.
- **Why deep nets train (or don't):** vanishing/exploding gradients, saturation, initialization, normalization.
- Second-order methods (LBFGS, Newton) — at least know they exist.

### 3.5 Numerical Computing (~10–20 hrs)
- Floating point: IEEE 754, precision, underflow/overflow.
- Conditioning, stability, Kahan summation.
- Vectorization: why loops die and SIMD/broadcasting wins.
- Mixed precision (fp32, fp16, bf16, fp8, int8) — covered more in performance section.

**The litmus test:** Can you derive the gradient of a softmax cross-entropy loss, explain why log-probs are used, and implement both forward and backward in NumPy? If no, do not move on.

---

## 4. Programming & Software Engineering Excellence

You will be judged on code quality, not just whether it runs.

### 4.1 Python — Deep Proficiency
- **Core language:** decorators, context managers, generators, iterators, descriptors.
- **Typing:** `typing` module, `Protocol`, `TypeVar`, generics, mypy in strict mode.
- **Concurrency:** `asyncio`, `threading`, `multiprocessing` — know when each is right.
- **Packaging:** `pyproject.toml`, `uv` or `poetry` (modern), virtualenvs, lockfiles.
- **Testing:** `pytest`, fixtures, parametrize, mocking, property-based testing (Hypothesis).
- **Profiling:** `cProfile`, `line_profiler`, `py-spy`, `memray`.
- **Code quality:** `ruff`, `black`, `isort`, `mypy`, pre-commit hooks.
- **Logging & observability:** `structlog`, OpenTelemetry.

**Libraries you must know cold:**
- `numpy` (mastery-level, not just `arr.mean()`).
- `pandas` (the good parts; know the pitfalls).
- `matplotlib` / `plotly` for viz.
- `pydantic` for data validation.
- `httpx` / `aiohttp` for async HTTP.
- `sqlalchemy` or `sqlmodel` (or just `psycopg` directly).

### 4.2 Systems Languages (At Least One, Ideally Two)
- **Rust:** memory safety, zero-cost abstractions, increasingly used in ML infra (e.g., `candle`, `burn`, `tokenizers` in part). Goal: write a CLI tool, do a project.
- **C++:** if you go deep on kernels, inference engines, or PyTorch internals. Read modern C++ (C++17/20).
- **Go:** often used for backend services, orchestration, CLI tools in MLOps.

You do not need to be expert in all three. Pick one as a "second language" and ship a real project in it.

### 4.3 Software Engineering Discipline
- **Design:** OOP vs. functional, SOLID (lightly), composition over inheritance, dependency injection.
- **Architecture:** clean boundaries, modules, packages, layered design, monorepo vs. polyrepo.
- **API design:** REST, gRPC, GraphQL — know when each fits.
- **Testing pyramid:** unit, integration, contract, end-to-end, load.
- **Code review:** give and receive critique like a professional.
- **Documentation:** READMEs that don't lie, docstrings, ADRs (architecture decision records).
- **Refactoring:** keep technical debt low; do not let "research code" rot.

### 4.4 Tooling You'll Use Daily
- **Editor:** VS Code or Cursor, with a configured Python/Rust/Go env.
- **Notebooks:** Jupyter, but treat them as scratchpads, not production. Move to scripts/packages.
- **Terminal:** tmux, fzf, ripgrep, fd, bat, lazygit.
- **Containers:** Docker (compose), then Kubernetes (at least understand deployments, services, ingress).
- **IaC:** Terraform or Pulumi (conceptual).
- **CI/CD:** GitHub Actions, buildkite, or similar.

---

## 5. Classical Machine Learning — Deep, Not Wide

You must own this foundation. Modern deep learning is a special case of ML, not a replacement for it.

### 5.1 Concepts You Must Own
- Supervised, unsupervised, self-supervised, reinforcement learning.
- Bias-variance tradeoff, overfitting, underfitting.
- Train / validation / test splits, cross-validation (k-fold, stratified, time-based).
- **Feature engineering:** scaling, encoding, interactions, missing data, leakage.
- **Regularization:** L1, L2, dropout, early stopping, data augmentation.
- **Evaluation:** classification (accuracy, precision, recall, F1, PR/ROC, AUC), regression (MSE, MAE, R²), ranking (NDCG, MAP), calibration.

### 5.2 Algorithms — Implement and Reason
- **Linear models:** linear regression, logistic regression, with regularization. **Derive the gradient.**
- **Trees:** decision trees, random forests, gradient boosting (XGBoost, LightGBM, CatBoost). XGBoost is still a default for tabular at most companies.
- **k-NN, Naive Bayes, SVMs (linear and kernel).**
- **Clustering:** k-means, hierarchical, DBSCAN, Gaussian mixtures, EM.
- **Dimensionality reduction:** PCA (deeply), t-SNE/UMAP (for viz, not features).
- **Anomaly detection:** isolation forests, one-class SVM, autoencoders.

### 5.3 Projects That Prove It
- Build a tabular ML pipeline end-to-end: data → features → train → eval → serve.
- Beat a strong baseline (XGBoost) on a real dataset (Kaggle, internal).
- Build a recommendation system (collaborative filtering, matrix factorization, then neural).

**Resources:**
- *Andrew Ng's ML course* (Stanford / Coursera) for foundations.
- *Hands-On ML with Scikit-Learn, Keras, and TensorFlow* (Géron) — book.
- *An Introduction to Statistical Learning* (ISLR) — book, free PDF.
- *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman) — depth.

---

## 6. Deep Learning — The Core Engine

This is the heart of modern AI. Spend serious time here.

### 6.1 The Building Blocks
- **Neuron model**, activation functions (sigmoid, tanh, ReLU, GELU, SwiGLU, SiLU).
- **Layers:** Dense/Linear, Conv1D/2D/3D, RNN/LSTM/GRU, Transformer, Normalization (BatchNorm, LayerNorm, RMSNorm, GroupNorm).
- **Loss functions:** MSE, cross-entropy, hinge, contrastive, InfoNCE.
- **Initialization:** Xavier/Glorot, He, scaled initialization for Transformers.
- **Backprop** through all of the above (you should be able to derive, not just call `.backward()`).

### 6.2 Architectures You Must Understand
- **MLPs / Fully Connected Networks.**
- **CNNs:** LeNet → AlexNet → VGG → ResNet → EfficientNet → ConvNeXt. Receptive fields, pooling, strided convs, dilated convs.
- **RNNs & sequence models:** LSTM, GRU, why Transformers replaced them.
- **Transformers (DEEP):** this is the most important architecture in AI today.
  - Self-attention, multi-head attention, masked attention, cross-attention.
  - Positional encodings (sinusoidal, RoPE, ALiBi).
  - Normalization placement (post-LN vs. pre-LN), why pre-LN + RMSNorm dominates.
  - MLP blocks (dense + activation, SwiGLU).
  - Encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5).
  - KV-cache, grouped-query attention (GQA), multi-query attention (MQA), sliding window attention.
  - Mixture of Experts (MoE): routing, load balancing, expert parallelism.

### 6.3 Training Mechanics
- Optimizers: SGD with momentum, Adam, AdamW, Lion, Sophia, Shampoo (know at least the first two deeply).
- Learning rate schedules: warmup, cosine decay, WSD.
- Gradient clipping, gradient accumulation, mixed precision (AMP).
- Data parallelism, model parallelism, pipeline parallelism, ZeRO/FSDP, tensor parallelism.
- Checkpointing, resumption, fault tolerance.
- **Reproducibility:** seeds, deterministic ops, environment capture.

### 6.4 Frameworks — Pick One, Know Both
- **PyTorch** (default in 2025–2026 for most research and many production paths). Master:
  - `nn.Module`, `nn.functional`, custom autograd functions.
  - `torch.compile`, FX graph mode.
  - Distributed: `torch.distributed`, DDP, FSDP, DeepSpeed.
  - Profiling: `torch.profiler`, TensorBoard, Weights & Biases.
- **JAX** (used at Google DeepMind, Anthropic-adjacent, many startups). Master:
  - `jit`, `grad`, `vmap`, `pmap`, `pjit`/`shard_map`.
  - Flax/Haiku for models.
- **TensorFlow / Keras** — understand for legacy/edge contexts, but PyTorch is the priority.

### 6.5 Generative Models
- **Autoencoders, VAEs.**
- **GANs** (vanilla, DCGAN, StyleGAN, conditional GANs) — for image generation history.
- **Normalizing flows** (RealNVP, Glow) — at least conceptually.
- **Diffusion models (CRITICAL):** DDPM, DDIM, score-based models, latent diffusion (Stable Diffusion), flow matching, consistency models. Understand the math, the noise schedules, classifier-free guidance.
- **Autoregressive models:** GPT-style, pixel CNN, etc.
- **Energy-based models** — at least know the framing.

### 6.6 Projects
- Train a ResNet on CIFAR-10 to >93% from scratch.
- Train a small Transformer for language modeling on a real corpus.
- Implement DDPM on a small dataset and generate samples.
- Re-implement nanoGPT end-to-end (Karpathy's repo is your friend).

---

## 7. Large Language Models (LLMs) — The Current Battlefield

This is where 70%+ of AI engineering jobs live right now. Go deep.

### 7.1 How LLMs Work
- Tokenization: BPE, WordPiece, SentencePiece, tiktoken. **Why tokenization matters** (multilingual issues, code, math).
- Embeddings: input vs. output tying, rotary embeddings, scaling.
- The Transformer decoder in detail (see §6.2).
- **Pre-training objective:** next-token prediction (causal language modeling).
- **Scaling laws** (Kaplan, Chinchilla) — compute-optimal training.
- **Emergent abilities** (and the debate around them).
- **Context length:** RoPE scaling, YaRN, ALiBi, LongRoPE, sliding window, Ring Attention, FlashAttention.

### 7.2 The Major Model Families (June 2026, verified)
You should be able to describe, compare, and use:
- **OpenAI:** GPT-5.5 (current API default per docs.openai.com), GPT-5, o-series reasoning models, GPT-4.1, GPT-4o. System cards published for GPT-5 and successors.
- **Anthropic:** Claude Mythos 5, Claude Fable 5, **Claude Opus 4.8**, **Claude Sonnet 4.5**, Claude Haiku 4.5. **Sonnet 4.5 = SOTA on SWE-bench Verified at 77.2%** and on **OSWorld (computer use) at 61.4%**, and can stay focused 30+ hours on multi-step tasks. Pricing $3 / $15 per M tokens.
- **Google:** Gemini 3.5 (current), Gemini 2.5 Pro/Flash, Gemma 3, Veo (video), Imagen "Nano Banana" (image), Lyria (audio), Live API.
- **Meta:** Llama 3.3 70B, Llama 3.1 family (8B / 70B / 405B), Llama 4 (multimodal).
- **Mistral:** Mistral Large, Codestral, Mixtral (MoE).
- **DeepSeek:** DeepSeek-V3, **DeepSeek-R1** (open-weight reasoning model).
- **xAI:** Grok 3.
- **Qwen (Alibaba):** **Qwen 3 family** (incl. Qwen3-235B-A22B MoE), Qwen 2.5, QwQ (reasoning).
- **Moonshot:** Kimi K2 (long-context).
- **Open base models:** Pythia, BLOOM, Falcon, MPT, SmolLM, OLMo.

**Know for each family:** architecture, training data, license, context length, key innovations, eval performance, intended use cases.

### 7.3 Prompt Engineering — Real, Not Meme-Level
- **Zero-shot, few-shot, chain-of-thought (CoT), self-consistency, tree-of-thought, ReAct.**
- **Structured outputs:** JSON mode, tool use, grammar-constrained decoding (Outlines, Guidance, Instructor, LMQL, jsonformer).
- **System prompts** that actually work: role, constraints, examples, output schema.
- **Long-context prompting:** placement matters, "lost in the middle" effects.
- **Prompt optimization:** DSPy, Promptfoo, automatic prompt engineering.

### 7.4 Inference Engineering (LLM Serving)
- **Decoding strategies:** greedy, beam search, top-k, top-p (nucleus), temperature, min-p, DRY sampling, speculative decoding, contrastive search.
- **KV-cache management:** paged attention (vLLM), prefix caching, prompt caching.
- **Batching:** continuous batching, in-flight batching.
- **Quantization:** GPTQ, AWQ, SmoothQuant, GGUF, FP8, INT4.
- **Speculative decoding:** draft models, Medusa, EAGLE.
- **Serving frameworks:** vLLM, TGI (text generation inference), TensorRT-LLM, llama.cpp, SGLang, LMDeploy, Ollama (for local dev).

### 7.5 LLM Evaluation
- **Benchmarks:** MMLU, MMLU-Pro, GSM8K, MATH, HumanEval, MBPP, Big-Bench, HellaSwag, ARC, TruthfulQA, IFEval, MT-Bench, Chatbot Arena, LiveBench, BigCodeBench, GPQA, FrontierMath.
- **Custom evals:** golden sets, LLM-as-judge, pairwise comparisons, Elo ratings.
- **Tool:** Inspect AI, Braintrust, LangSmith, Langfuse, Promptfoo, RAGAS, DeepEval, MLflow LLM evaluate.
- **Critical skill:** build a small eval harness for your own system.

---

## 8. Retrieval-Augmented Generation (RAG) & Search Systems

RAG is the workhorse of applied AI. Master it.

### 8.1 Information Retrieval Foundations
- **Sparse retrieval:** TF-IDF, BM25, BM25F. (Still competitive!)
- **Dense retrieval:** dual encoders, bi-encoders, ColBERT, SPLADE.
- **Hybrid retrieval:** combining sparse + dense with reciprocal rank fusion.
- **Reranking:** cross-encoders, ColBERT reranker, LLM-based rerankers (RankGPT, RankZephyr).
- **Query understanding:** query expansion, HyDE, decomposition, multi-query, step-back prompting.

### 8.2 Vector Search
- **Vector databases:** Pinecone, Weaviate, Milvus, Qdrant, Chroma, pgvector, Elasticsearch kNN.
- **ANN algorithms:** HNSW, IVF-PQ, ScaNN, DiskANN.
- **Embeddings:** OpenAI, Cohere, Voyage, BGE, E5, GTE, NV-Embed, Stella, Jina.
- **Chunking strategies:** fixed-size, semantic, recursive, late chunking, proposition-based, document-structure-aware.
- **Metadata filtering, hybrid search (vector + filters).**

### 8.3 RAG Architectures
- **Naive RAG:** retrieve top-k → stuff into prompt.
- **Advanced RAG:** query rewriting, hybrid retrieval, reranking, contextual compression.
- **Modular RAG:** routing, query construction (text-to-SQL/text-to-Cypher), agents over retrieval.
- **GraphRAG:** knowledge graphs + RAG (Microsoft GraphRAG, LightRAG).
- **Long-document RAG:** multi-hop, hierarchical, agentic loops.
- **Multimodal RAG:** text + images + tables + audio.

### 8.4 RAG Failure Modes
- **Hallucinations**, grounding failures, citation faithfulness.
- **Lost-in-the-middle**, chunking issues, embedding model mismatches.
- **Eval:** RAGAS, TruLens, custom human-in-the-loop evals.

### 8.5 Projects
- Build a RAG system over your own notes / a research corpus.
- Build a code-search RAG over a large repo.
- Compare BM25 vs. dense vs. hybrid on a domain-specific dataset.

---

## 9. AI Agents & Tool Use

This is the frontier. Top companies are racing here.

### 9.1 Agent Theory
- **ReAct** (reasoning + acting).
- **Reflexion, Self-Refine, CRITIC.**
- **Plan-and-Execute**, **LATS**, **ADaPT.**
- **Tool use / function calling:** OpenAI tools, Anthropic tool use, Google function calling, Mistral tool use.
- **Memory:** short-term (context), long-term (vector store, knowledge graph), episodic.
- **Multi-agent systems:** role-based (CrewAI), graph-based (LangGraph), supervisor patterns, debates.

### 9.2 Frameworks (Use At Least 2)
- **LangChain / LangGraph** (broad, opinionated).
- **LlamaIndex** (data-focused).
- **CrewAI / AutoGen / AG2** (multi-agent).
- **Haystack** (production RAG).
- **Semantic Kernel** (Microsoft).
- **DSPy** (compile-time optimization of LM programs — important).
- **Letta / MemGPT** (memory-focused agents).
- **Pydantic AI** (typed, clean — rising).

> **Warning:** most "agent frameworks" will be obsolete in 12 months. Learn the **patterns**, not just the API. Many top engineers write agents with raw API calls + a small library of helpers.

### 9.3 Agent Skills
- **Browser use:** Playwright, browser-use, computer-use APIs.
- **Code execution:** sandboxed Python (E2B, Modal, Daytona, Pyodide for in-browser).
- **Shell / file system tools.**
- **Web search and scraping** (respectful, robust).
- **MCP (Model Context Protocol):** the Anthropic-led standard for tool integration. **Learn this well.**

### 9.4 Projects
- A coding agent that can read, edit, and run tests in a repo.
- A research agent that searches, reads, synthesizes, and cites.
- A multi-agent system with clear roles and a supervisor.

---

## 10. Fine-Tuning, Alignment & RLHF/RLAIF

### 10.1 Fine-Tuning
- **Full fine-tuning** (expensive, often unnecessary).
- **PEFT (Parameter-Efficient Fine-Tuning):**
  - **LoRA, QLoRA, DoRA, AdaLoRA.**
  - **Prompt tuning, prefix tuning, P-tuning v2.**
  - **IA³, BitFit, OFT.**
- **Continued pre-training vs. instruction tuning vs. alignment tuning.**
- **Frameworks:** `peft`, `trl`, `axolotl`, `LLaMA-Factory`, `unsloth`, `torchtune`.
- **Data:** curation, deduplication, quality > quantity, synthetic data generation.

### 10.2 Instruction Tuning & SFT
- Build SFT datasets (Alpaca-style, evol-instruct, multi-turn).
- Train with TRL / axolotl.
- Evaluate quality uplift with proper evals.

### 10.3 Alignment: RLHF & Beyond
- **RLHF pipeline:** SFT → reward model → PPO.
- **DPO (Direct Preference Optimization)** — simpler, often as good.
- **IPO, KTO, ORPO, SimPO** — modern variants.
- **RLAIF** (RL from AI feedback) and **Constitutional AI.**
- **Process reward models (PRMs),** reasoning models (o1, o3, R1 style).
- **Safety:** adversarial training, red-teaming, jailbreak resistance, refusal calibration.

### 10.4 Projects
- Fine-tune Llama 3 / Qwen / Mistral on a domain dataset with QLoRA.
- Build a DPO pipeline on a preference dataset.
- Train a small reward model and use it for RLAIF on a narrow task.

---

## 11. Multimodal AI (Vision, Audio, Video)

This is increasingly important.

### 11.1 Vision
- **CNNs (ResNet, ConvNeXt)** as encoders.
- **Vision Transformers (ViT), Swin, DeiT.**
- **CLIP / SigLIP:** contrastive image-text.
- **Diffusion for images:** Stable Diffusion, SDXL, Flux, SD3, Kandinsky.
- **Generative vision:** consistency models, rectified flow, controlnet, IP-Adapter.
- **Detection / segmentation:** YOLO, SAM (Segment Anything), SAM 2, Grounding DINO.

### 11.2 Vision-Language Models (VLMs)
- **Architectures:** LLaVA, Qwen-VL, InternVL, GPT-4o, Claude with vision, Gemini, Pixtral, Llama 3.2 Vision, Molmo.
- **Training:** connector modules, vision encoders, instruction tuning on multimodal data.
- **Use cases:** document understanding, OCR-free extraction, UI agents, robotics, video understanding.

### 11.3 Audio
- **ASR (speech-to-text):** Whisper, Conformer, Canary.
- **TTS (text-to-speech):** VITS, Tortoise, Bark, XTTS, CosyVoice, Sesame CSM.
- **Audio LLMs:** Qwen2-Audio, SALMONN.

### 11.4 Video
- **Video understanding:** VideoLLaMA, Video-LLaVA, Gemini Video.
- **Video generation:** Sora, Veo, Runway Gen-3, Kling, Pika, MovieGen, Wan.

### 11.5 Projects
- Fine-tune a VLM for document Q&A on a real dataset.
- Build a video understanding pipeline that summarizes and tags clips.

---

## 12. MLOps, LLMOps & Production Engineering

This is what separates "I made a demo" from "I shipped a system."

### 12.1 Experiment Tracking & Reproducibility
- **Weights & Biases, MLflow, Neptune, TensorBoard, Aim.**
- Track code, data, config, environment, metrics, artifacts.
- Determinism, seeds, env capture (`uv lock`, Docker images).

### 12.2 Data Engineering for ML
- **Pipelines:** Airflow, Dagster, Prefect, Kestra.
- **Processing:** Spark, Polars, DuckDB, Dask, Ray Data.
- **Storage:** S3/GCS/ADLS, Parquet, Delta Lake, Iceberg, Lance.
- **Feature stores:** Feast, Tecton, Hopsworks.
- **Data labeling:** Label Studio, Scale, Surge, Argilla.

### 12.3 Model Deployment
- **Model servers:** TorchServe, Triton Inference Server, BentoML, Ray Serve, Seldon Core, MLflow Serving.
- **LLM servers:** vLLM, TGI, TensorRT-LLM, SGLang, Ollama, llama.cpp.
- **API layer:** FastAPI, gRPC, GraphQL gateways.
- **Containers & orchestration:** Docker, Kubernetes, Helm, Kustomize, Argo, Knative.
- **Serverless options:** Modal, Replicate, RunPod, Banana, Together AI, Fireworks AI, Anyscale, Beam.

### 12.4 Monitoring & Observability
- **System metrics:** latency (p50/p95/p99), throughput, error rate, saturation.
- **ML metrics:** data drift, concept drift, embedding drift, prediction distribution shifts.
- **LLM-specific:** token usage, refusal rate, hallucination rate, eval drift.
- **Tools:** Prometheus, Grafana, OpenTelemetry, Arize, WhyLabs, Langfuse, LangSmith, Helicone, Braintrust, Phoenix (Arize), Datadog AI monitoring.

### 12.5 Cost & Reliability
- Right-sizing GPUs, spot instances, autoscaling, request routing.
- Caching: prompt cache, semantic cache (GPTCache), embedding cache.
- Rate limiting, backpressure, circuit breakers, retries with jitter.
- Graceful degradation when models fail.

---

## 13. System Design for AI Systems

This is **the most underprepared** area for most candidates going into senior/staff roles. Study it like a backend engineer, then add the AI twist.

### 13.1 Classic System Design (Do not skip)
- Backends for ML inference at scale.
- Caching layers (Redis, Memcached, edge caches).
- Message queues (Kafka, Pulsar, SQS, NATS).
- Sharding, replication, consensus (Raft, Paxos) — at least know the gist.
- CAP theorem, eventual consistency, idempotency.
- Load balancing, CDNs, rate limiting, authn/authz.

### 13.2 AI-Specific System Design
**Practice designing:**
- **A RAG system** for enterprise search: ingestion → chunking → embedding → index → query → rerank → answer → eval. Discuss scale, freshness, security.
- **A coding agent** like Cursor/Cline: editor integration, context window, retrieval over code, tool execution, sandboxed runs, iter loops.
- **A customer support chatbot:** intent classification, knowledge base, escalation, human-in-the-loop, eval, observability.
- **A fine-tuning platform:** data curation, training orchestration, eval gates, deployment, rollback.
- **A multi-tenant LLM gateway:** auth, rate limits, cost tracking, model routing, caching, fallbacks.
- **A real-time recommendation system:** candidate generation, ranking, embeddings, online learning, cold start.
- **A multimodal document understanding pipeline:** OCR/VLM, table extraction, entity recognition, structured output, validation.
- **A video generation platform:** prompt understanding, diffusion, post-processing, scaling GPUs, queueing, billing.

**For each, be ready to discuss:**
- Latency budget, throughput targets.
- Cost per request.
- Failure modes and mitigations.
- Cold start, warm pools.
- Caching, batching, speculative decoding.
- Data privacy, PII handling, redaction.
- Evals: offline, online, human review.
- Observability and rollback.

**Resources:** *Designing Machine Learning Systems* (Huyen), *AI Engineering* (Huyen), *Designing Data-Intensive Applications* (Kleppmann), Grokking the System Design Interview, the Excalidraw diagrams online.

---

## 14. Performance, Optimization & GPU/Kernels

This is what unlocks staff+ roles. You don't need to write CUDA for most jobs, but you need to **understand** it.

### 14.1 GPU Fundamentals
- SMs, warps, threads, blocks, grids, occupancy.
- Memory hierarchy: registers, shared memory, L1/L2 cache, HBM/VRAM.
- Coalesced memory access, memory bandwidth vs. compute.
- Roofline model.
- **Tools:** `nvidia-smi`, `nsys`, `ncu` (Nsight Compute), `nvprof`.

### 14.2 Kernel & Operator Optimization
- Custom CUDA kernels, Triton (Pythonic, becoming default), CUTLASS.
- **FlashAttention** (1/2/3): tiling, recomputation, IO-aware.
- **Fused kernels:** RMSNorm + rotary, SwiGLU, etc.
- Memory-efficient attention: FlashAttention, Ring Attention, sliding window.
- Compile-time vs. run-time optimization.

### 14.3 Quantization & Compression
- **Post-training quantization:** INT8 (W8A8), INT4 (W4A16), FP8.
- **Methods:** GPTQ, AWQ, SmoothQuant, ZeroQuant, OmniQuant.
- **Quantization-aware training (QAT).**
- **Pruning:** structured, unstructured, semi-structured (2:4).
- **Distillation:** task-specific, logit-based, feature-based.
- **Low-rank factorization.**

### 14.4 Inference Optimization
- Continuous batching (vLLM), paged attention, prefix caching.
- Speculative decoding, Medusa, EAGLE.
- Dynamic batching, request scheduling.
- TensorRT, ONNX Runtime, OpenVINO.
- Compile: `torch.compile`, AOTAutograd, Inductor.

---

## 15. Distributed Training & Inference at Scale

### 15.1 Distributed Training
- **Data parallelism (DDP).**
- **ZeRO stages 1/2/3** (DeepSpeed), **FSDP** (PyTorch native).
- **Tensor parallelism** (Megatron-style), **pipeline parallelism** (GPipe, PipeDream, 1F1B, interleaved).
- **Sequence parallelism**, **context parallelism** (for long context).
- **Expert parallelism** for MoE.
- **3D parallelism** (combining DP + TP + PP).
- **Gradient accumulation, micro-batches.**
- **Activation recomputation / checkpointing.**
- **Communication:** NCCL, Gloo, MPI. Bandwidth matters.
- **Fault tolerance:** elastic training, checkpoint sharding, spot instance recovery.

### 15.2 Distributed Inference
- Tensor parallel serving (vLLM, TGI, TensorRT-LLM).
- Disaggregated inference (prefill vs. decode, MoE).
- KV-cache replication/sharding, cache-aware routing.
- Multi-region, multi-cloud failover.
- Cost optimization: spot, autoscaling, request coalescing.

### 15.3 Clusters & Schedulers
- **Slurm, K8s + Volcano, Ray.**
- Cluster provisioning, gang scheduling.
- Observability for training (W&B, TensorBoard, custom dashboards).
- **Tools:** NeMo, Megatron-LM, MaxText, torchtitan.

---

## 16. Research Literacy & Reading Papers

Top-tier AI engineers read papers, not just blog posts.

### 16.1 How to Read an ML Paper
- First pass: title, abstract, figures, conclusion (10 min).
- Second pass: skim intro + method + key equations + experiments (1 hr).
- Third pass: reimplement the core idea in code.
- **Hunt for:** what is new, what is borrowed, what is the eval, what is the ablations, what is missing, what claims are weak.

### 16.2 Must-Read Papers (Starter List)
- **Attention Is All You Need** (Transformer).
- **BERT, GPT-2, GPT-3.**
- **T5, PaLM, LLaMA, LLaMA 2/3.**
- **LoRA, QLoRA.**
- **DPO, RLHF (InstructGPT).**
- **FlashAttention 1/2/3.**
- **vLLM (PagedAttention).**
- **Scaling Laws (Kaplan, Chinchilla).**
- **CLIP, DALL-E, Stable Diffusion, DDPM, DiT.**
- **ReAct, Reflexion, Toolformer.**
- **RAG original, REALM, RETRO.**
- **AlphaGo, AlphaZero** (for RL).
- **Mamba / S4** (state-space models, for sequence modeling).
- **Constitutional AI, Self-Consistency, Chain-of-Thought.**
- **DeepSeek-R1, o1-style reasoning.**
- **Mixture of Experts: Switch Transformer, GShard, Mixtral.**
- **Knowledge Distillation: DistilBERT, TinyBERT.**

### 16.3 Where to Read
- **arXiv** (cs.CL, cs.LG, cs.CV, cs.AI).
- **Hugging Face papers, Papers with Code.**
- **Distill.pub** (archived but gold).
- **Sebastian Raschka's "What's AI" newsletter, Import AI, The Batch, The Gradient, Lil'Log.**
- **Twitter/X:** follow the actual researchers (Yann LeCun, Andrej Karpathy, Jim Fan, Hyung Won Chung, Tri Dao, Sasha Rush, Percy Liang, etc.).

---

## 17. Evaluation, Benchmarking & Red-Teaming

If you cannot measure it, you cannot improve it. This is its own deep skill.

### 17.1 Evaluation Methodology
- **Offline evals:** held-out sets, k-fold, bootstrap confidence intervals.
- **Online evals:** A/B tests, interleaving, multi-armed bandits, switchback designs.
- **Human evals:** rater design, inter-rater agreement (Cohen's kappa, Krippendorff's alpha), rater training, bias mitigation.
- **LLM-as-judge:** pairwise, Likert, reference-based. Calibrate against human raters.
- **Behavioral testing:** CheckList, robustness suites.
- **Statistical significance** (do not ship a 0.5% win without a test).

### 17.2 Benchmark Suites You Should Know
- **General:** MMLU, MMLU-Pro, BBH, GPQA, HellaSwag, ARC.
- **Reasoning:** GSM8K, MATH, FrontierMath, AIME.
- **Code:** HumanEval, MBPP, BigCodeBench, SWE-bench, LiveCodeBench.
- **Instruction following:** IFEval, MT-Bench, AlpacaEval, Arena Hard.
- **Multilingual:** MGSM, MMLU-ProX, FLORES.
- **Long context:** RULER, LongBench, Needle-in-a-Haystack, NoCha.
- **Multimodal:** MMMU, MMBench, MathVista, ChartQA.
- **Agentic:** GAIA, SWE-bench, WebArena, ToolBench, AgentBench.
- **Safety:** HarmBench, AdvBench, BBQ, RealToxicityPrompts.

### 17.3 Red-Teaming & Safety Evals
- Adversarial prompt generation (GCG, PAIR, TAP, manual).
- Jailbreak benchmarks.
- Toxicity, bias, fairness audits.
- Privacy: PII leakage, training data extraction.

---

## 18. Security, Safety, Privacy & Compliance

Non-negotiable at top companies. Owning this makes you a senior candidate.

### 18.1 Security
- **Prompt injection** (direct & indirect), tool call injection.
- **Jailbreaks**, model manipulation, social engineering.
- **Supply chain:** model weights, third-party datasets, dependencies.
- **Sandboxing** for code-executing agents.
- **Secret management**, network policies, encryption in transit/at rest.
- **OWASP LLM Top 10**, **MITRE ATLAS** for AI threats.

### 18.2 Privacy
- PII detection, redaction, anonymization, differential privacy.
- Data retention and deletion policies (GDPR, CCPA).
- Federated learning, secure aggregation (conceptual).

### 18.3 Safety & Alignment
- Refusal tuning, constitutional AI, red-teaming, evals.
- Bias/fairness across demographics.
- Dual-use considerations, capability evals before deployment.
- EU AI Act, US Executive Orders, sector-specific regulation (HIPAA, finance, etc.).
- Model cards, system cards, datasheets for datasets.

---

## 19. Cloud, Infra & Cost Engineering

You don't need to be a kernel engineer, but you need to speak the language fluently.

### 19.1 Cloud (Pick at least one deeply, know the others)
- **AWS:** S3, EC2 (P4/P5/G5 instances), EKS, Lambda, Bedrock, SageMaker.
- **GCP:** GCS, GCE (A2/A3 with H100s), GKE, Vertex AI.
- **Azure:** Blob, AKS, Azure ML, Azure OpenAI.
- **Specialty providers:** Lambda Labs, CoreWeave, RunPod, Together, Fireworks, Modal, Anyscale, Replicate.

### 19.2 Networking
- VPCs, subnets, security groups, NAT, peering.
- Service mesh (Istio/Linkerd) — at least conceptually.
- gRPC, HTTP/2/3, websockets, SSE for streaming LLM responses.
- Edge inference, CDN integration.

### 19.3 Storage
- Object storage (S3/GCS), block storage, file systems.
- Vector DBs, feature stores, caching layers.
- Cold vs. hot data tiers.

### 19.4 Cost Engineering
- GPU hour math, spot vs. on-demand, reserved, savings plans.
- Cost per token, cost per request, cost per user.
- FinOps practices, chargeback/showback.
- Caching and batching to cut spend.

---

## 20. Portfolio, Open Source & Public Presence

This is the **single highest-leverage** thing most engineers under-invest in.

### 20.1 What Top Candidates Have
- **3–5 flagship public projects** with real depth:
  - A fine-tuned model on a real domain, with a write-up.
  - A RAG/agent system that solves a real problem, with evals.
  - A training run reproduction of a paper.
  - A kernel/optimization project (Triton, FlashAttention-style).
  - An open-source contribution to a major project (vLLM, TRL, LangChain, etc.).
- **A polished GitHub:** clean READMEs, reproducible envs, results, screenshots.
- **A technical blog or Twitter presence** (optional but compounding).
- **A resume that tells a story** — impact, not duties.

### 20.2 Contribution Targets (Pick 1–2)
- **vLLM, TGI, TensorRT-LLM, llama.cpp.**
- **Hugging Face Transformers, TRL, PEFT, Datasets.**
- **PyTorch, DeepSpeed, torchtitan.**
- **LangChain, LangGraph, LlamaIndex, DSPy.**
- **Instructor, Outlines, Guidance.**
- **Modal, BentoML.**
- **Unsloth, axolotl, LLaMA-Factory.**

Contributing a real PR (not a typo fix) to one of these repos is a **massive signal**.

### 20.3 Writing
- Write 2–4 deep technical posts per year.
- Topics: a system you built, a paper you reimplemented, a benchmark you ran, a postmortem.
- Clarity > length. Show numbers, ablations, failure modes.

---

## 21. Interview Preparation (The Real Loop)

> **Verified June 2026** from Exponent's hiring guides (last updated 3 days before this writing) and Anthropic / OpenAI engineering blog posts. The loop has changed meaningfully since 2023 — generic LeetCode grinding is no longer the dominant signal.

**Loop shape (4–6 rounds typical, 1–4 months total):**
1. **Recruiter / hiring manager screen** (30 min). At OpenAI this is *"a real behavioral interview, not a lightweight intro call"* — full STAR questions in 30 minutes. At Anthropic, the recruiter screen is shorter (15–30 min) but **probing about specific platforms and models you've used**; comp discussion often happens here (treat any number quoted as informational, not an offer).
2. **Technical phone screen** (60–90 min). CodeSignal / Replit / Google Colab. **Practical, multi-tiered problems, not LeetCode.** Anthropic's published examples: build a web crawler → make it multi-threaded → create a filtered dictionary. Or: implement an in-memory database, add TTL, add advanced queries. The interviewer layers new constraints on your initial solution. For ML roles: **MCP tooling, error diagnosis, model reliability for long-running tasks**.
3. **Onsite final loop** (1–2 days, 4–6 sessions). Two distinct flavors:
   - **Anthropic:** split into **Loop 1** (system design, coding, culture fit) and **Loop 2** (experiences/goals, technical project deep-dive) on separate days. **If you don't pass Loop 1, Loop 2 is cancelled.**
   - **OpenAI:** 4–6 sessions, often: 2nd coding, 2nd system design, behavioral, cross-functional behavioral (e.g., working with legal), and **~1 hour project walkthrough** (interviewers dig into what you personally did, why, who you worked with — *not* a polished 2-minute summary). Sometimes candidates prep **4–5 slides about a system they built**.
4. **Cross-functional / behavioral.** Both companies emphasize this. **Anthropic: culture fit is the highest-failure round** — even strong technical candidates get rejected on behavioral. Plan 5–6 polished STAR stories.
5. **Optional:** take-home (rare for engineers at these companies; common for data/design/growth at OpenAI — 48-hour A/B test deck for data scientists, bespoke assignment for growth), research paper discussion, portfolio walkthrough.

**OpenAI specifics:**
- **Leveling decided at the end of the loop.** **L5 at OpenAI ≈ L6 at Meta/Google.** Recruiters may down-level candidates 1–2 levels below their current title.
- **SWE coding may include OOP / class design** (e.g., a layered object-oriented problem built around a chatbot interface) — prepare for both formats, not just DSA.
- **Research engineer bar:** *"graduate-level machine learning and information theory"* — if you can derive backprop, write a transformer from scratch, and reason about KL divergence, you can pass.
- **AI tool use in interview:** permitted for ML/prompt-engineering roles (candidates may use Claude Sonnet as a working tool); **not permitted for SWE or AI Safety Fellowship roles.**

**Anthropic specifics:**
- **Coding environment is Python by default.** Replit for live coding, Google Colab for ML rounds needing a GPU, CodeSignal for automated assessments (especially fellowships).
- **System design rounds focus on LLM infrastructure and distributed systems** — designing batch inferencing APIs, GPU usage optimization with batching constraints, distributing large model files across thousands of machines.
- **Comp bands presented at recruiter screen as a negotiation tactic** — do not anchor on them; counter with market data.
- **Hybrid:** 25%+ in-office (SF / NY / Seattle / London); relocation support available.

**For ALL AI engineering roles, in addition to the loop above, expect:**
- **ML knowledge deep-dive:** backprop, optimizers, transformers end-to-end, LoRA math, DPO loss, tokenization, evaluation metrics, debugging training runs.
- **Reading a paper on the spot** and discussing it.
- **Why us / why this role** — every interviewer will ask. Have a specific, thoughtful answer.

### 21.1 Prep Plan (3–6 months)
- **DSA:** 3–4 problems/day, weekly contest, focus on patterns.
- **ML Knowledge:** go deep on the foundations in §3, 5, 6, 7. Be able to derive and explain.
- **System Design:** 2–3 designs/week, talk out loud, draw diagrams.
- **Portfolio:** be ready to discuss 3 projects in extreme depth (every design decision, every failure).
- **Mock interviews:** Pramp, interviewing.io, friends, AI mock tools.

### 21.2 The "Tell Me About a Project" Answer (Structure)
1. **Context:** the user, the business problem, the constraint.
2. **Goal:** the metric you moved.
3. **Approach:** what you built, what you considered, what you rejected.
4. **Trade-offs:** latency, cost, accuracy, complexity, ops.
5. **Outcome:** numbers, with confidence intervals or A/B results.
6. **What I'd do differently** — this is the most important line.

### 21.3 Common Senior/Staff Failure Modes
- Cannot debug a training run that's diverging.
- Cannot discuss scaling beyond a single machine.
- Cannot discuss cost, latency, or reliability trade-offs.
- Confuses research with engineering; cannot ship.
- Vague on evals — "it looked good" is a red flag.
- Cannot read or interpret a paper.
- Cannot collaborate — talks down to interviewers, no curiosity.

---

## 22. Compensation & Career Strategy

### 22.1 How to Maximize TC
- **Optimize for equity growth** at companies with strong trajectories (still private or early public).
- **Switch every 2–3 years early on** to capture refresh grants.
- **Negotiate hard:** always counter. Most first offers are 10–30% below max.
- **Build multiple offers** simultaneously.
- **Specialize in a scarce skill:** e.g., distributed training, kernel optimization, agent infra, eval, multimodal.

### 22.2 Roles Worth Targeting (Examples)
- **OpenAI:** Member of Technical Staff (MTS), Research Engineer, **Applied AI / Applied Engineering** (the largest engineering org — ChatGPT and surrounding products), Solutions Engineer.
- **Anthropic:** Member of Technical Staff (MTS), Software Engineer, Research Engineer, ML Engineer. About 50% of technical staff hold advanced degrees, but "many successful colleagues never went to college."
- **Google DeepMind:** Research Engineer, Software Engineer (ML).
- **Meta FAIR / GenAI:** Research Engineer, ML Engineer.
- **Microsoft Research / Azure AI:** various.
- **NVIDIA:** AI Infra, Research, Triton, NeMo. Historically very high equity comp.
- **Top AI-first startups** (most equity-weighted, sometimes illiquid): Mistral, Cohere, xAI, Perplexity, Cursor, Replit, Sierra, Decagon, Glean, Notion, Linear, Harvey, Hebbia, Tessian, Writer.
- **Quant funds:** Two Sigma, Citadel, DE Shaw, Jane Street, HRT (if you like math + systems).

### 22.3 The Career-Compounding Loop
1. Pick hard, high-leverage problems.
2. Ship them in public.
3. Build a reputation for being the person who closes the loop.
4. Get pulled into harder, higher-visibility work.
5. Use that leverage for the next role.

---

## 23. The 24-Month Execution Plan

Treat this as a template. Adjust based on your hours/week.

### Phase 0 — Foundations Reset (Weeks 1–8, ~15–20 hrs/week)
- 3Blue1Brown linear algebra, MIT 18.06 alongside.
- Probability/statistics deep dive (ISLR + statquest).
- Python mastery: refactor a non-trivial project using typing, tests, packaging.
- DSA: 150 Problems across the patterns.
- Build a tiny MLP from scratch in NumPy, then PyTorch.

### Phase 1 — Classical ML + DL Foundations (Weeks 9–24, ~20 hrs/week)
- Finish an ML course (Ng or Géron).
- Implement linear/logistic regression, trees, XGBoost-style boosting.
- Build a CNN, train on CIFAR-10.
- Implement a small Transformer, train a tiny GPT on a text corpus.
- Implement DDPM, generate samples.
- **Ship:** one end-to-end ML project with a real dataset, real metrics, a write-up.

### Phase 2 — LLMs + RAG + Agents (Weeks 25–48, ~20 hrs/week)
- Read and reimplement 5 foundational LLM papers.
- Build a serious RAG system with hybrid retrieval, reranking, evals.
- Build a real agent with tool use, code execution, and memory.
- Fine-tune a base model with QLoRA on a domain.
- Build a custom eval harness.
- Contribute a PR to an open-source project.
- **Ship:** 2 flagship projects + 1 OSS contribution.

### Phase 3 — Production, Systems, Specialization (Weeks 49–72, ~20 hrs/week)
- System design deep-dive: 2 designs/week, write-ups.
- Deploy a model to production (FastAPI + vLLM + K8s, or Modal/Replicate).
- Add observability, evals, cost dashboards.
- Pick a specialization: kernels/Triton, agent infra, multimodal, eval, or training.
- Go deep on that specialization with 1–2 deep projects.
- **Ship:** 1 system-design-level project and 1 specialization project.

### Phase 4 — Interview & Compounding (Weeks 73–96, ~20–30 hrs/week)
- DSA grind, system design mocks, ML fundamentals review.
- Portfolio polish: clean READMEs, demo videos, blog posts.
- Apply strategically, build a referral network.
- Negotiate hard.

### Parallel Tracks (Always Running)
- **Reading:** 1 paper/week, deeply.
- **Writing:** 1 blog post / month.
- **Network:** 1 conversation/week with someone ahead of you.
- **Health:** sleep, exercise, eyes, wrists. This is a marathon.

---

## 24. Daily/Weekly Operating System

### Daily (5 hrs/day on weekdays, more on weekends)
- **1 hr** DSA or system design problem.
- **1 hr** reading (paper / chapter / blog).
- **2–3 hrs** building (one project at a time, deep).
- **0.5 hr** writing notes / blog / Twitter thread.

### Weekly
- **Sunday:** plan the week's deep work, pick 1–3 outcomes.
- **Saturday:** review what shipped, write a short postmortem, queue next week.

### Quarterly
- Pick one specialty to deepen.
- Update resume, portfolio, LinkedIn.
- Reach out to 5 people for chats.

### Anti-Patterns to Kill
- Tutorial hell (watching instead of building).
- Collecting 100 half-finished side projects.
- Reading papers without implementing.
- Building demos without evals.
- Building without shipping.

---

## 25. Curated Resources (Books, Courses, Papers, Repos)

### Books
- *Designing Data-Intensive Applications* — Martin Kleppmann.
- *Designing Machine Learning Systems* — Chip Huyen.
- *AI Engineering* — Chip Huyen.
- *Deep Learning* — Goodfellow, Bengio, Courville.
- *Deep Learning with PyTorch* — Stevens, Antiga, Viehmann.
- *Hands-On ML with Scikit-Learn, Keras, and TensorFlow* — Aurélien Géron.
- *Speech and Language Processing* — Jurafsky & Martin (free online).
- *Probabilistic Machine Learning* — Kevin Murphy.
- *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong (free PDF).
- *The Pragmatic Programmer* — Hunt & Thomas.
- *Staff Engineer* — Will Larson.
- *An Elegant Puzzle* — Will Larson.
- *The Staff Engineer's Path* — Tanya Reilly.

### Courses
- **Stanford CS231N** (CNNs), **CS224N** (NLP), **CS336** (LLM from scratch — Lang & Hashimoto).
- **MIT 6.S191** (Intro DL), **MIT 18.06** (LA), **MIT 6.041** (Prob).
- **Karpathy's videos:** Zero to Hero, Let's reproduce GPT-2, Let's build the GPT Tokenizer.
- **Fast.ai** (practical DL).
- **Hugging Face courses** (transformers, agents, RAG, smol-course).
- **DeepLearning.AI** short courses (DSPy, agents, RAG, fine-tuning, evals, MLOps).
- **Full Stack Deep Learning / ML Ops.**
- **Made With ML** (MLOps).
- **Latent Space** and **Weights & Biases** YouTube channels.

### Newsletters / Blogs
- Import AI (Jack Clark), The Batch (Andrew Ng), Lil'Log (Lilian Weng), Sebastian Raschka, The Gradient, Distill (archived), HuggingFace blog, OpenAI blog, Anthropic blog, Google DeepMind blog, PyTorch blog, vLLM blog.

### Repos to Star & Study
- `karpathy/nanoGPT`, `karpathy/llm.c`, `karpathy/minbpe`.
- `huggingface/transformers`, `huggingface/trl`, `huggingface/peft`, `huggingface/accelerate`, `huggingface/datasets`.
- `vllm-project/vllm`.
- `unslothai/unsloth`, `axolotl-ai-cloud/axolotl`, `hiyouga/LLaMA-Factory`.
- `pytorch/torchtitan`, `NVIDIA/Megatron-LM`, `microsoft/DeepSpeed`.
- `stanford-crfm/helm`, `EleutherAI/lm-evaluation-harness`.
- `langchain-ai/langgraph`, `run-llama/llama_index`, `stanfordnlp/dspy`.
- `openai/evals`, `anthropics/evals`.
- `ggerganov/llama.cpp`, `mlc-ai/mlc-llm`.
- `modal-labs/awesome-modal`, `bentoml/BentoML`.

### Datasets to Know
- The Pile, RedPajama, SlimPajama, FineWeb, FineWeb-Edu, C4, ROOTS, Dolma.
- OpenOrca, UltraChat, Tulu, OpenHermes, Magpie.
- HumanEval, MBPP, GSM8K, MATH, MMLU, Alpaca.
- COCO, LAION, CC3M, DataComp.

---

## Closing Note

You said "treat me like I know nothing." The most important thing that separates engineers who break through from those who don't is **honesty about what they actually know**. Most people fool themselves.

- If you can't derive backprop on paper, you don't know backprop.
- If you can't read a paper and implement its core idea, you don't know the field.
- If you can't ship something to users, you don't know engineering.
- If you can't measure your system's quality, you don't know your system.

Mastery is a long, quiet accumulation. The good news: the AI field in 2025–2026 rewards **real depth** more than ever, because the gap between "calls an API" and "ships a system that works" is enormous and growing.

Start today. Be patient. Be honest. Build.

---

## 26. Verification & Sources (June 2026)

This roadmap was checked against live primary sources on the day of writing. Where a number or process step is cited above, here is where it came from:

**Compensation:**
- **Anthropic SWE (median $665K TC, P25 $570K, P75 $870K, P90 $920K; base P25 $320K; equity P75 $550K; n=20, exp 2–12):** JSON-LD pulled from `https://www.levels.fyi/companies/anthropic/salaries/software-engineer` (lastReviewed timestamp on the page: 2026-06-18).
- **Google SWE (P25 $215K, P75 $410K, P90 $547K; n=149):** JSON-LD pulled from `https://www.levels.fyi/companies/google/salaries/software-engineer` (same date).
- **OpenAI / Meta / NVIDIA ranges** cross-referenced from public reporting and recruiter knowledge; Levels.fyi JSON-LD on those pages was bot-blocked at the time of research.

**Interview process:**
- **Anthropic** — Exponent's "Get a Job at Anthropic" guide, "last updated 3 days ago" as of 2026-06-18. Includes the multi-tiered coding problems (web crawler, in-memory DB with TTL), the two-loop onsite structure, the culture-fit-highest-failure-rate claim (attributed to an Anthropic recruiter), and the comp-band-as-negotiation-tactic note.
- **OpenAI** — Exponent's "Get a Job at OpenAI" guide. Includes the 30-min behavioral recruiter screen, the 4–6-session final loop, the ~1-hour project walkthrough, the 4–5-slide presentation variant, the L5 ≈ L6 Meta/Google leveling note, the OOP/class design format for SWE, the "graduate-level ML theory" bar for research engineers, and the AI-tool-permission policy by role.
- **interviewing.io** has companion guides for both companies and a machine-learning mock interview product used by candidates preparing for these loops.

**Models and benchmarks:**
- **Current model lineup** (GPT-5.5, Claude Opus 4.8 / Sonnet 4.5 / Mythos 5 / Fable 5, Gemini 3.5, Llama 4 / 3.3, Qwen 3, DeepSeek-V3/R1, Kimi K2): cross-checked against `docs.openai.com`, `docs.anthropic.com`, `ai.google.dev`, Hugging Face model cards, and Anthropic's "Introducing Claude Sonnet 4.5" blog post.
- **Claude Sonnet 4.5 = 77.2% SWE-bench Verified, 61.4% OSWorld, 30+ hour focus, $3/$15 per M tokens:** from Anthropic's own announcement at `anthropic.com/news/claude-sonnet-4-5`.
- **GPT-5 system card** referenced from OpenAI's docs.

**Industry context:**
- **Anthropic ~18.9M MAU, 1,000+ headcount, 25%+ in-office:** from Exponent citing Anthropic's own statements.
- **OpenAI ~800M weekly ChatGPT users, ~$852B valuation (early 2026), 3-day hybrid:** from Exponent citing public data and OpenAI's careers page.

**India-specific sources (Levels.fyi JSON-LD, all lastReviewed 2026-06-18):**
- **Google India SWE (n=73):** P25 ₹36.5L · P75 ₹80.9L · P90 ₹1.23Cr. Base P75 ₹48.7L; equity P75 ₹29.3L.
- **Microsoft India SWE (n=107):** P25 ₹35.5L · P75 ₹68.0L · P90 ₹96.4L.
- **Amazon India SWE (n=87):** P25 ₹30.9L · P75 ₹73.0L · P90 ₹98.4L.
- **CRED (n=51):** P25 ₹49.6L · P75 ₹88.0L · P90 ₹1.02Cr.
- **Meesho (n=52):** P25 ₹27.7L · P75 ₹71.4L · P90 ₹80.2L.
- **PhonePe (n=49):** P25 ₹31.9L · P75 ₹58.1L · P90 ₹68.0L.
- **Ola (n=17):** P25 ₹36.6L · P75 ₹57.4L · P90 ₹68.1L.
- **Flipkart (n=91):** P25 ₹23.1L · P75 ₹53.5L · P90 ₹74.5L.
- **Swiggy (n=59):** P25 ₹21.8L · P75 ₹44.8L · P90 ₹71.3L.
- **Zomato (n=133):** P25 ₹23.1L · P75 ₹42.9L · P90 ₹53.5L.
- **Razorpay (n=42):** P25 ₹20.2L · P75 ₹35.9L · P90 ₹42.5L.
- **Pine Labs (n=11):** P25 ₹16.5L · P75 ₹34.2L · P90 ₹44.1L.
- **Paytm (n=55):** P25 ₹15.6L · P75 ₹21.8L · P90 ₹36.1L.
- **OpenAI India (n=0, early data):** single data point ₹55.8L. **Anthropic India (n=0):** no public comp yet.
- **Sarvam AI** (Bengaluru) — $1.5B Series B (June 2026), verified from sarvam.ai.
- **IndiaAI Mission** and IndiaAI Compute Portal — government initiative, GPU credits available.

**What I did NOT verify (and you should be skeptical of):**
- Specific leveling / TC for OpenAI L4–L6 and Meta E5–E6 (US and India) — public reporting varies; treat ranges as ±20%.
- OpenAI India and Anthropic India comp — n=0 at scrape time, so the ₹55.8L OpenAI India point is a single data anchor, not a median.
- Benchmarks not directly published by the model provider (third-party leaderboards evolve weekly).
- Hiring bar shifts month-to-month at these companies.
- Any claim about a specific team's culture or process — those vary by org.
- Indic-AI specific salaries at Sarvam/Krutrim — public reporting is sparse.

> If a number in this doc contradicts something you saw on Levels.fyi or in a recent blog post, **the live source wins**. This file is a snapshot, not gospel.

— *Compiled as a deliberate, opinionated roadmap. Adapt it to your life; do not worship it.*
