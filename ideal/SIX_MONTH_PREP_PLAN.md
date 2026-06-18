# 6-Month AI Engineer Preparation Plan
## Detailed, Week-by-Week Execution Guide

> **Audience:** Engineers treating this as a fresh start. Assumes ~25–35 productive hours/week (treat as a serious second job or a full-time-learner commitment).
>
> **Last verified: June 2026.** Comp numbers, interview process details, and model references in this plan are grounded in Levels.fyi JSON-LD (live company pages), Exponent's hiring guides (last updated 3 days before this writing), and Anthropic / OpenAI / Google AI's own documentation. See `AI_ENGINEER_MASTERY_ROADMAP.md` §26 for the full source list.
>
> **Outcome by month 6:**
> - A polished GitHub with 3 flagship projects (RAG system, fine-tuned LLM, agent) and 1 OSS contribution.
> - A public blog with 6 deep technical posts.
> - Able to derive backprop, implement a transformer, debug a training run, and design a RAG/agent system.
> - Ready to pass ML + system design + coding screens at top AI companies.
> - 150+ DSA problems solved with patterns internalized.
>
> **Conventions used below:**
> - **Build = write code, ship to GitHub.**
> - **Read = paper, chapter, or doc, with notes.**
> - **Reflect = write a short blog post or Twitter thread on what you learned.**
> - Each week has a **primary deliverable** in **bold**. If you ship only that, the week was a success.

---

## Table of Contents
- [How to Use This Plan](#how-to-use-this-plan)
- [Daily Operating System](#daily-operating-system)
- [Tooling Setup (Do This First)](#tooling-setup-do-this-first)
- [Month 1 — Math, Python, and the Foundations Reset](#month-1--math-python-and-the-foundations-reset-weeks-1-4)
- [Month 2 — Classical ML + First Real Project](#month-2--classical-ml--first-real-project-weeks-5-8)
- [Month 3 — Deep Learning, Transformers, LLMs from Scratch](#month-3--deep-learning-transformers-llms-from-scratch-weeks-9-12)
- [Month 4 — RAG, Agents, and Fine-Tuning](#month-4--rag-agents-and-fine-tuning-weeks-13-16)
- [Month 5 — Production, MLOps, and System Design](#month-5--production-mlops-and-system-design-weeks-17-20)
- [Month 6 — Interview Loop, Portfolio Polish, and Applications](#month-6--interview-loop-portfolio-polish-and-applications-weeks-21-24)
- [Weekly Review Template](#weekly-review-template)
- [Backup / Catch-up Strategy](#backup--catch-up-strategy)
- [Final 2-Week Sprint Before Interviews](#final-2-week-sprint-before-interviews)

---

## How to Use This Plan

1. **Print it or pin it.** You should see this every day.
2. **Do the week's primary deliverable first** when you sit down to work. Everything else is supporting.
3. **Time-box ruthlessly.** If a topic is taking 3x longer than budgeted, switch to a different resource and circle back.
4. **Build in public.** Push to GitHub daily. Tweet/blog weekly. Visibility compounds.
5. **Track everything** in a single Notion/Obsidian doc or `progress.md` in your repo.
6. **Sleep 7+ hours, exercise 4x/week, walk daily.** Burnout is the #1 killer of these plans.

---

## Daily Operating System

You have ~25–35 productive hours/week. A typical weekday = 4–5 hrs, weekend = 6–8 hrs.

### Weekday (4–5 hrs)
| Block | Time | Activity |
|---|---|---|
| Warm-up | 20 min | 1 DSA problem (review prior week's mistakes) |
| Deep work 1 | 90 min | The week's primary topic (read or build) |
| Deep work 2 | 90 min | The week's project work |
| Reading | 30 min | Paper / blog / chapter |
| Reflection | 15 min | Write 3–5 bullets about what clicked |

### Weekend (6–8 hrs, split Sat/Sun)
- **Saturday:** Heavy build day (3–4 hrs deep project work) + 1 hr paper reading.
- **Sunday:** Plan the week (30 min), 1 hr DSA contest or system design, light project work, **weekly review** (30 min — see template at bottom).

### The 4 Non-Negotiables
1. **Push code every weekday** (even a small commit).
2. **Solve 1 DSA problem every weekday**, contest on weekends.
3. **Read 1 paper/chapter every week**, deeply.
4. **Write 1 blog post every month**, ship it.

---

## Tooling Setup (Do This First)

Spend one weekend (4–6 hrs) on this. Get it right once.

### Hardware
- **GPU access (in priority order):**
  1. Local NVIDIA GPU (RTX 3060+ with 12GB+ VRAM). Best for learning.
  2. Cloud credits: Lambda Labs, RunPod, Vast.ai, Modal, or your employer's credits.
  3. Free: Google Colab (T4, limited), Kaggle (P100, 30h/week), Lightning AI Studios.
- **Disk:** 200GB+ free (models, datasets).
- **RAM:** 32GB recommended, 16GB minimum.

### Software Stack
```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Core tools
brew install git gh jq fzf ripgrep fd bat tmux htop
brew install --cask docker visual-studio-code cursor

# Python env
uv python install 3.11
uv venv .venv
source .venv/bin/activate
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Dev tools
uv pip install numpy pandas scikit-learn matplotlib seaborn plotly
uv pip install jupyter ipython
uv pip install ruff mypy pytest pre-commit
uv pip install transformers datasets accelerate peft trl bitsandbytes
uv pip install langchain langgraph langsmith langfuse
uv pip install fastapi uvicorn pydantic httpx
uv pip install wandb mlflow tensorboard
uv pip install vllm  # inference
uv pip install sentence-transformers  # embeddings
uv pip install instructor outlines  # structured generation
uv pip install modal replicate  # serverless GPU

# Set up pre-commit
pre-commit init
# Add hooks: ruff, ruff-format, mypy, trailing-whitespace
```

### Accounts to Create
- [ ] GitHub (with a clean, professional profile + pinned repos)
- [ ] Hugging Face (request access to gated models early: Llama, Mistral)
- [ ] Weights & Biases (free academic plan)
- [ ] LangSmith + Langfuse (free tiers)
- [ ] OpenAI, Anthropic, Google AI Studio API keys (small spend — $20–50 total)
- [ ] Modal account ($30 free/month)
- [ ] Discord: PyTorch, HuggingFace, LangChain, EleutherAI

### Repo Setup
```
your-name/
  ├── ai-engineer-roadmap/        # this prep plan, your progress log
  ├── ml-from-scratch/            # tiny GPT, diffusion, etc.
  ├── rag-system/                 # flagship RAG project
  ├── llm-finetuning/             # flagship fine-tuning project
  ├── agent-system/               # flagship agent project
  ├── dsa-practice/               # LeetCode solutions, organized by pattern
  ├── system-design/              # designs, written up
  └── blog/                       # Astro or simple markdown site
```

---

## India-Specific Plan: 6 Months from India

> **Last verified: June 2026.** All INR comp numbers are pulled live from Levels.fyi JSON-LD on India-specific company pages. The plan below extends the base plan with India-specific tactics, comp benchmarks, and target-company lists.
>
> **Read `AI_ENGINEER_MASTORY_ROADMAP.md` §1A first** for the verified India comp table, interview process differences, target companies, and negotiation tactics.

### India Comp Reality (Verified Levels.fyi, June 2026)

**Top of the Indian market is ~₹1Cr TC** at the P90 mark:
- **Google India P90 = ₹1.23Cr** (n=73).
- **CRED P90 = ₹1.02Cr** (n=51).
- **Microsoft India P90 = ₹96.4L** (n=107).
- **Amazon India P90 = ₹98.4L** (n=87).

**A senior AI engineer at one of these companies in Bengaluru can expect ₹80L–₹1.2Cr+ TC.** With AI/ML premium, add 20–40% on top of generic SWE numbers.

For context, ₹1Cr ≈ $120K USD at typical June 2026 FX. Direct US L5 roles at OpenAI/Google/Meta/Apple pay $400K–$800K (₹3.3–₹6.7Cr). The US comp gap is real, but cost-of-lifestyle-adjusted in India is often comparable for senior+ roles. See the roadmap §1A.6 for the full trade-off analysis.

### India Interview Process — What Changes

1. **DSA round count is higher.** Most Indian companies run **5–6 rounds** with 2–3 pure LeetCode-style coding rounds in early stages. Plan **30% more DSA time** than the base plan.
2. **OpenAI / Anthropic India follow the US process.** Direct US-AI-lab targets use practical coding + system design + project walkthrough, not pure LeetCode.
3. **College signal matters in early rounds.** IITs/BITS/IIIT-Hyderabad/IISc/top NITs get direct interview slots. From non-elite colleges, **competitive programming ranks (CodeChef, Codeforces), OSS contributions, and referrals** are the break-in path.
4. **AI tool use in interview:** generally permitted. Use it.
5. **Indic-language AI roles are a unique India play.** If you're interested, **Sarvam AI, AI4Bharat, Bhashini** are the major employers, and the open-source **Sarvam-1, Airavata, OpenHathi, IndicBERT** are the models to know.

### India-Specific DSA / CP Sources

- **Codeforces** + **CodeChef** (competitive programming, ratings) — primary signal for non-elite-college candidates.
- **LeetCode** — 200–250 problems (not 150), with 60% medium + 25% hard + 15% easy.
- **GeeksforGeeks** — India-specific interview experiences for Google/Amazon/Microsoft India.
- **InterviewBit** — SDE-sheet structured prep, used by most Indian CS students.
- **Striver (takeuforward.org)** — A2Z and SDE sheet, the de-facto Indian DSA roadmap.
- **Love Babbar** — 450 DSA problems sheet.

**Add to base plan:** Solve 4–5 problems/week on Codeforces/CodeChef **in addition to** the LeetCode routine. The competitive programming style (multi-test, time pressure, edge cases) maps better to the actual Indian interview experience than pure LeetCode.

### India Target Companies (apply in this order)

**Wave 1 — Apply broadly in Months 4–5 (alongside interview prep):**
1. **OpenAI India** (Bengaluru) — entry: applied/AI engineer. Highest comp ceiling.
2. **Google DeepMind India** (Bengaluru) — research engineer.
3. **Google India** (Bengaluru/Hyderabad/Gurugram) — SWE ML / AI.
4. **Microsoft Research India** (Bengaluru) — research engineer.
5. **Microsoft India** (Hyderabad/Bengaluru/Pune) — SWE AI.
6. **Amazon India** (Bengaluru/Hyderabad) — AWS Bedrock / Alexa AI.
7. **Meta India** (Bengaluru/Hyderabad) — FAIR/GenAI.
8. **NVIDIA India** (Bengaluru/Pune) — AI infra.
9. **Adobe India** (Noida/Bengaluru) — Firefly/Sensei.
10. **Salesforce India** (Hyderabad/Bengaluru) — Agentforce.

**Wave 2 — Indian AI unicorns (apply in Month 5–6):**
1. **Sarvam AI** (Bengaluru) — flagship Indian AI company, $1.5B Series B.
2. **Krutrim** (Bengaluru) — Indian multilingual LLM.
3. **CRED** (Bengaluru) — premium comp ₹88L P75.
4. **Meesho** (Bengaluru) — ₹71L P75.
5. **PhonePe** (Bengaluru) — payments + AI.
6. **Flipkart** (Bengaluru) — e-commerce AI.
7. **Razorpay** (Bengaluru) — fintech.
8. **Yellow.ai / Observe.AI / Fractal** (Bengaluru) — domain AI.

**Wave 3 — Service / consulting (if you need a safety net or first role):**
- TCS, Infosys, Wipro, HCL, Accenture — AI/ML roles at ₹6L–₹25L for freshers, up to ₹40L–₹60L for senior. Not the high-end target, but a real entry path for non-elite-college candidates or those who need a job first.

### India Comp Negotiation Tactics (Verified)

1. **Pull Levels.fyi data before the recruiter screen.** Cite it: *"Google India P75 for this role is ₹80.9L; I'm targeting at least the P50 of this band."* This is normal and expected.
2. **Always counter.** First offers are 10–30% below max.
3. **Run multiple offers in parallel.** Apply to at least 5 companies in Wave 1 + 3 in Wave 2 simultaneously. Time your final-round asks so offers arrive in a 2-week window.
4. **Ask about RSU refresh grants.** Indian RSU grants are often 1–4 year vest; refreshes are critical for compounding comp.
5. **Service-company caveat:** TCS/Infosys/Wipro fixed CTC includes a variable component (5–15%) and "flexi-pay" you can opt out of. Negotiate **fixed base**, not the headline CTC. If the offer is ₹18L CTC with ₹14L fixed, you should treat it as a ₹14L offer, not ₹18L.
6. **ESOPs at Indian unicorns are lottery tickets.** Sarvam, CRED, Meesho ESOPs *can* be worth 5–50x base, but most don't. Don't price them into your decision at face value.
7. **Relocation bonus:** ₹1L–₹5L is standard for out-of-city hires. Ask.
8. **US transfer is the highest-leverage move.** Plan to apply to US roles directly, or to position for an internal L4→L5 transfer after 12–18 months at India office. L5 US comp ($500K–$800K) is materially higher than India P90 (₹1.23Cr ≈ $147K).

### India-Specific Reading (Add to base plan)

- **Sarvam AI's open-source models** (Sarvam-1) on Hugging Face — read the model cards, play with the API.
- **AI4Bharat / Bhashini** — open Indic datasets and models.
- **IndiaAI Compute Portal** (indiaai.gov.in) — apply for GPU credits.
- **Papers from Microsoft Research India, Google DeepMind India, AI4Bharat** — these are the local research output.
- **Analytics India Magazine, YourStory, Inc42** — Indian AI ecosystem news.

---

## Month 1 — Math, Python, and the Foundations Reset (Weeks 1–4)

> **Theme:** Build the floor. No flashy projects yet. Resist the urge to skip this.

### Week 1 — Linear Algebra + Python Hardening

**Daily:** 1 hr 3Blue1Brown LA videos, 1 hr MIT 18.06 (Strang), 1 hr NumPy implementation, 30 min DSA.

**Tasks:**
- **Mon–Wed:** Watch 3Blue1Brown Essence of Linear Algebra (all 16 videos, ~3 hrs total). Take notes in your own words.
- **Thu–Fri:** MIT 18.06 Lectures 1–3 (vectors, matrix multiplication, inverse, transpose).
- **Sat:** Implement from scratch in NumPy (no library shortcuts):
  - Matrix multiplication (naive triple loop → vectorized with `@`).
  - Transpose, trace, Frobenius norm, L2 norm.
  - Solve linear system `Ax = b` with `np.linalg.solve` and via `A⁻¹b`.
  - Verify each against `np.linalg` and torch.
- **Sun:** 1 hr DSA warm-up (2 easy + 1 medium problem on arrays/strings).

**Deliverable:** `ml-from-scratch/linalg/` with `matmul.py`, `solve.py`, `notebook.ipynb` showing each op + tests. Push to GitHub. **Reflect:** blog post "Linear algebra, demystified: 5 operations you actually use in ML."

**Time budget:** ~25 hrs.

---

### Week 2 — More LA + Calculus + Probability Kickoff

**Daily:** 1 hr LA, 1 hr calculus (3Blue1Brown), 1 hr coding, 30 min DSA.

**Tasks:**
- **Mon–Tue:** SVD (3Blue1Brown has a great one), eigendecomposition. Implement SVD on a 5x5 matrix and verify `U Σ Vᵀ = A`.
- **Wed–Thu:** 3Blue1Brown Calculus series (essentials). Focus on chain rule and partial derivatives.
- **Fri:** Implement sigmoid, softmax, log-sum-exp, cross-entropy, MSE in NumPy. **Derive** the gradient of softmax cross-entropy on paper first.
- **Sat:** Prob/Stats intro. Watch StatQuest: probability, Bayes, distributions (8 videos, ~2 hrs).
- **Sun:** DSA — 1 array/string problem + 1 hash map problem.

**Deliverable:** `ml-from-scratch/calculus/` with `softmax_ce.py` (forward + backward), gradient checks via finite differences. **Push + reflect.**

**Time budget:** ~25 hrs.

---

### Week 3 — Probability & Statistics Deep Dive

**Daily:** 1 hr probability reading, 1 hr coding, 30 min DSA.

**Tasks:**
- **Read:** Chapters 1–4 of *Introduction to Statistical Learning* (ISLR) — free PDF. Do the labs in R or Python.
- **Code:**
  - Implement MLE for a Gaussian (fit mean/variance to data).
  - Implement logistic regression from scratch (forward, BCE loss, gradient, train on toy 2D dataset).
  - Visualize decision boundary, loss curve, accuracy.
- **Math:** Understand KL divergence, cross-entropy, mutual information intuitively. Implement KL between two Gaussians.

**Deliverable:** `ml-from-scratch/logistic_regression/` with a working model on synthetic data + a notebook. **Push + reflect.**

**Time budget:** ~25 hrs.

---

### Week 4 — DSA Foundations + Python Tooling + Git Polish

**Daily:** 1.5 hr DSA (patterns!), 1.5 hr Python tooling, 30 min reading.

**Tasks:**
- **DSA:** Solve 10 problems this week. Focus on these patterns:
  - Two pointers, sliding window, hash map, basic recursion.
  - Use NeetCode roadmap, group by pattern in `dsa-practice/`.
  - For each: write brute force → optimize → retype from memory 3 days later.
- **Python tooling:**
  - Refactor a small project (your logistic regression code) to use:
    - Type hints + `mypy --strict` clean.
    - `pytest` with fixtures and parametrize.
    - `ruff` + `ruff format` + pre-commit hooks.
    - `pyproject.toml` with proper packaging (`uv`).
  - Add a `Makefile` or `taskfile` for `test`, `lint`, `format`.
- **Git:** Squash, rebase, interactive rebase. Make your repo history clean.
- **Read:** *Designing Data-Intensive Applications* chapters 1, 2, 4 (or skim if tight on time).

**Deliverable:** A perfectly-set-up Python project with CI (GitHub Actions) running tests + lint on PRs. **Push + reflect:** blog post "My Python tooling stack for ML."

**Time budget:** ~28 hrs.

**End of Month 1 Checkpoint:**
- [ ] Can derive gradients on paper for softmax cross-entropy, MSE, logistic regression.
- [ ] Implemented linear/logistic regression from scratch.
- [ ] 25+ DSA problems solved, patterns starting to form.
- [ ] Clean Python repo with tests, types, CI.
- [ ] 2 blog posts published.

---

## Month 2 — Classical ML + First Real Project (Weeks 5–8)

> **Theme:** Learn classical ML deeply, ship your first end-to-end real project.

### Week 5 — Classical ML: Regression, Regularization, Trees

**Daily:** 1.5 hr course/reading, 1.5 hr code, 30 min DSA.

**Tasks:**
- **Read/Watch:** Andrew Ng ML course, weeks 1–4 (or finish ISLR chapters 3, 6, 8). Or Géron book chapters 1–4.
- **Code:**
  - Implement linear regression with L1/L2 regularization from scratch.
  - Use scikit-learn for decision trees, random forests.
  - **End-to-end pipeline:** load a real tabular dataset (California housing, Titanic, or Kaggle's "House Prices"), split, train multiple models, evaluate, log to W&B.
- **DSA:** 5 problems on trees (BFS, DFS, BST operations).

**Deliverable:** `ml-from-scratch/regularized_regression/` and a Kaggle-style notebook with proper eval. **Push + reflect.**

**Time budget:** ~28 hrs.

---

### Week 6 — Gradient Boosting + Project Selection

**Daily:** 1.5 hr XGBoost/LightGBM, 2 hr project, 30 min DSA.

**Tasks:**
- **Boosting deep dive:**
  - Understand the math: why gradient boosting works, second-order gradients (XGBoost), histogram-based split finding (LightGBM).
  - Train XGBoost and LightGBM on a tabular dataset. Compare.
  - Use Optuna for hyperparameter search.
- **Project selection (CRITICAL):** Pick your Month 2–6 flagship project. Options:
  - **Predictive:** loan default, churn, fraud, customer LTV, housing prices, energy forecasting.
  - **Recommendation:** movie/product recsys on MovieLens or retail dataset.
  - **Time series:** forecasting demand, M5 competition-style.
  - **NLP classic:** sentiment, NER, classification on a domain corpus.
- Pick something with **public impact, real data, and clear metrics**. Document the choice in your repo's `README.md`.

**Deliverable:** `projects/01-tabular-ml/` repo with proper structure, XGBoost baseline + tuned model, W&B logs. **Push.**

**Time budget:** ~30 hrs.

---

### Week 7 — First Flagship Project: Build, Evaluate, Iterate

**Daily:** 3–4 hr project work, 30 min DSA, 30 min reading.

**Tasks:**
- **Build:** EDA → feature engineering → model → cross-validation → hyperparameter search → error analysis → final model.
- **Eval:** Use proper metrics (not just accuracy). For imbalanced: PR-AUC, F1, calibration. For regression: RMSE, MAE, residual analysis.
- **Error analysis:** Look at the worst predictions. Why did the model fail? Document 3 patterns.
- **Serving:** Wrap the model in a FastAPI app with `/predict` endpoint. Add basic tests.
- **DSA:** 5 problems on graphs (BFS, DFS, topological sort, Dijkstra).

**Deliverable:** Working FastAPI service with tests, README with results, error analysis write-up. **Push + reflect (start of blog series on the project).**

**Time budget:** ~32 hrs.

---

### Week 8 — Project Polish + Intro to Deep Learning Theory

**Daily:** 2 hr project, 1.5 hr DL theory, 30 min DSA.

**Tasks:**
- **Project polish:** Add Docker, GitHub Actions CI, model card, demo notebook. **Deploy to Modal or Hugging Face Spaces** (free).
- **DL theory:**
  - Read Goodfellow Ch. 6 (Feedforward Nets) and Ch. 8 (Optimization).
  - Watch 3Blue1Brown's "Neural Networks" series.
  - Understand activation functions, initialization, backprop intuitively.
- **DSA:** 5 problems mixing dynamic programming basics (1D, 2D).

**Deliverable:** Deployed ML service with public URL. **First flagship project DONE.** Reflect: blog post "From notebook to production: my first end-to-end ML service."

**Time budget:** ~30 hrs.

**End of Month 2 Checkpoint:**
- [ ] Understand gradient boosting, can use it on any tabular problem.
- [ ] 1 deployed ML service.
- [ ] 50+ DSA problems solved.
- [ ] 3 blog posts published.
- [ ] Comfortable with PyTorch tensors, autograd basics.

---

## Month 3 — Deep Learning, Transformers, LLMs from Scratch (Weeks 9–12)

> **Theme:** Build the engine from the inside. This is the most intellectually rewarding month.

### Week 9 — PyTorch + Build a Tiny CNN

**Daily:** 2 hr PyTorch, 1.5 hr project, 30 min DSA.

**Tasks:**
- **PyTorch fluency:**
  - Work through the official PyTorch "Learn the Basics" tutorial (60 min quickstart + 60 min tensor/nn).
  - Build a small MLP for MNIST from scratch. Train, eval, log to W&B.
- **CNNs from scratch:**
  - Implement a basic CNN (Conv2d, ReLU, MaxPool, Linear) in PyTorch.
  - Train on CIFAR-10 to >80% (this is easy — do it first to learn the loop).
  - Then upgrade to a small ResNet (or copy from torchvision) and push to >93%.
- **DSA:** 5 problems on heaps and tries.

**Deliverable:** `ml-from-scratch/cnn-cifar10/` — a clean training script with config, W&B logs, results table. **Push + reflect.**

**Time budget:** ~30 hrs.

---

### Week 10 — Transformers from Scratch (Karpathy-Style)

**Daily:** 2 hr Karpathy "Let's build GPT", 1.5 hr coding, 30 min DSA.

**Tasks:**
- **Watch:** Andrej Karpathy's "Let's build GPT from scratch" (2 hrs) and "Let's build the GPT Tokenizer" (1.5 hrs).
- **Reimplement:**
  - Build a BPE tokenizer (minbpe-style, ~200 lines).
  - Build a small GPT (nanoGPT-style): attention, MLP, residuals, LayerNorm, RoPE if ambitious.
  - Train on a tiny text dataset (e.g., Shakespeare, TinyStories). Watch loss decrease.
- **Read:** The "Attention Is All You Need" paper (skim, focus on the figures and equations).
- **DSA:** 5 problems on backtracking + divide & conquer.

**Deliverable:** `ml-from-scratch/tiny-gpt/` — your own BPE + GPT implementation trained on a small dataset, with a generation script. **Push + reflect.** This is a portfolio anchor.

**Time budget:** ~32 hrs.

---

### Week 11 — Training a Real LLM: nanoGPT / llm.c

**Daily:** 2 hr training, 1 hr reading, 30 min DSA.

**Tasks:**
- **Run Karpathy's nanoGPT on a real (small) dataset.** Or use the Hugging Face `trl` library to SFT-train a tiny base model (e.g., SmolLM, Pythia-160M).
- **Profile and understand:**
  - Mixed precision (AMP).
  - Gradient accumulation.
  - Learning rate warmup + cosine.
  - Gradient clipping.
  - W&B logging of train/val loss, gradient norms, learning rate.
- **DSA:** 5 problems on graphs (shortest path, MST, union-find).

**Deliverable:** `projects/02-tiny-llm/` — a working training run with configs, logs, loss curves, sample generations at different checkpoints. **Push + reflect.**

**Time budget:** ~30 hrs.

---

### Week 12 — LLM Inference + Serving

**Daily:** 2 hr inference, 1.5 hr reading, 30 min DSA.

**Tasks:**
- **Inference stack:**
  - Implement greedy, top-k, top-p, temperature, and min-p sampling from scratch.
  - Implement a basic KV-cache (in your tiny GPT).
  - Use vLLM to serve a real model (Llama 3 8B, Mistral 7B, or Qwen 2.5). Benchmark throughput.
  - Quantize a small model with bitsandbytes (INT8, INT4) and compare.
- **Read:** vLLM paper, FlashAttention paper (skim, focus on ideas).
- **DSA:** 5 problems mixing patterns + 1 mock interview (interviewing.io free).

**Deliverable:** `projects/02-tiny-llm/` extended with inference + vLLM serving notes. **Push + reflect:** blog post "How LLMs actually generate text: a hands-on tour."

**Time budget:** ~30 hrs.

**End of Month 3 Checkpoint:**
- [ ] Can implement a Transformer and train it.
- [ ] Understand KV-cache, sampling, quantization.
- [ ] Served an LLM with vLLM.
- [ ] 90+ DSA problems solved.
- [ ] 4 blog posts published.
- [ ] 2 flagship projects done.

---

## Month 4 — RAG, Agents, and Fine-Tuning (Weeks 13–16)

> **Theme:** Build the most in-demand applied AI systems. These are the projects that get you hired.

### Week 13 — Embeddings + Vector Search

**Daily:** 2 hr coding, 1 hr reading, 30 min DSA.

**Tasks:**
- **Embeddings:**
  - Use sentence-transformers (BGE, E5, GTE) to embed a corpus.
  - Compare cosine vs. dot product vs. L2 distance.
  - Visualize embeddings with t-SNE/UMAP. Notice semantic clusters.
- **Vector DBs:**
  - Spin up Qdrant or Weaviate locally. Index 10K+ documents.
  - Also try pgvector with PostgreSQL.
  - Implement hybrid search (BM25 + dense) using `rank_bm25` + vector DB.
- **Read:** Survey of dense retrieval (Karpukhin et al., DPR).
- **DSA:** 5 problems on DP (more complex).

**Deliverable:** `notes/embeddings-and-vector-search/` with a working hybrid retrieval pipeline + benchmark notebook (BM25 vs. dense vs. hybrid on a small QA dataset). **Push + reflect.**

**Time budget:** ~30 hrs.

---

### Week 14 — RAG System v1 (Flagship Project #3)

**Daily:** 3 hr building, 1 hr reading.

**Tasks:**
- **Architecture:** Ingestion → chunking (multiple strategies) → embedding → indexing → query → retrieval → reranking → generation → citation.
- **Build:**
  - Pick a domain: your notes, a research corpus, a documentation site, public company filings, etc.
  - Implement multiple chunking strategies and benchmark them.
  - Add query rewriting (HyDE or multi-query).
  - Add a cross-encoder reranker.
  - Use an LLM with structured output (via Instructor) to produce cited answers.
  - **Evals:** build a small golden set (20–50 Q&A pairs) and measure retrieval recall@k, answer faithfulness, citation accuracy.
- **Tools:** LangChain or LlamaIndex as a thin orchestration layer (or roll your own — better for learning).

**Deliverable:** `projects/03-rag-system/` — working RAG with eval harness, multiple chunking strategies compared, README with architecture diagram (Excalidraw). **Push.**

**Time budget:** ~35 hrs.

---

### Week 15 — RAG v2: GraphRAG, Advanced Patterns, Evals

**Daily:** 3 hr building, 1 hr reading.

**Tasks:**
- **Advanced patterns:**
  - Add GraphRAG (Microsoft's approach with knowledge graphs).
  - Add agentic RAG (a small ReAct loop that decides when to retrieve).
  - Try long-context RAG (stuffed context) vs. retrieval for comparison.
- **Real evals:**
  - Use RAGAS or TruLens for automated evals.
  - Build a small LLM-as-judge for answer quality.
  - Compare your system against raw GPT-4o on the golden set.
- **DSA:** 5 problems on advanced DP (bitmask, trees).

**Deliverable:** `projects/03-rag-system/` v2 with GraphRAG, agentic loop, and rigorous evals. **Push + reflect:** blog post "Building a production-grade RAG system: 10 lessons from 50 iterations."

**Time budget:** ~35 hrs.

---

### Week 16 — Fine-Tuning + DPO (Flagship Project #4)

**Daily:** 3 hr building, 1 hr reading.

**Tasks:**
- **Pick a base model:** Llama 3.1 8B, Qwen 2.5 7B, or Mistral 7B.
- **Pick a domain:** legal, medical, code, finance, customer support — something with available instruction data.
- **Pipeline:**
  - Build/curate a SFT dataset (~5K–20K examples). Use synthetic data generation if needed.
  - Fine-tune with QLoRA (4-bit) using `trl` or `axolotl`.
  - Evaluate on a held-out set + a public benchmark (MMLU subset, domain-specific).
  - Compare base vs. SFT vs. DPO.
- **Bonus:** Add DPO training on a preference dataset (synthetic or UltraFeedback-style).
- **DSA:** 5 problems mixed + 1 system design mini-mock.

**Deliverable:** `projects/04-llm-finetuning/` — full pipeline, W&B logs, eval comparison, model card. **Push + reflect:** blog post "Fine-tuning Llama 3 for [your domain]: what worked, what didn't."

**Time budget:** ~35 hrs.

**End of Month 4 Checkpoint:**
- [ ] Built a serious RAG system with evals.
- [ ] Fine-tuned a real LLM with QLoRA + DPO.
- [ ] 120+ DSA problems solved.
- [ ] 5 blog posts published.
- [ ] 3 flagship projects shipped.

---

## Month 5 — Production, MLOps, and System Design (Weeks 17–20)

> **Theme:** Turn your projects into systems. This is what separates seniors from mid-level.

### Week 17 — Deploy RAG to Production

**Daily:** 3 hr production engineering, 1 hr reading.

**Tasks:**
- **Containerize:** Dockerfile for the RAG app, multi-stage builds, slim images.
- **Orchestrate:** docker-compose with API + vector DB + Redis cache.
- **Cloud deploy:** Choose one:
  - **Modal** (easiest, GPU available): deploy RAG as serverless function.
  - **Fly.io / Railway / Render** for the API + Qdrant Cloud / Pinecone free tier.
  - **AWS/GCP** if you have credits: ECS or GKE.
- **Observability:**
  - Add OpenTelemetry tracing.
  - Add Langfuse for LLM-specific traces.
  - Log latency, token usage, retrieval recall, answer quality.
- **Reliability:**
  - Add retries with backoff.
  - Add a fallback model.
  - Add a semantic cache (GPTCache).
  - Add rate limiting.
- **DSA:** 5 problems on system-design-flavored problems (LRU cache, rate limiter, etc.).

**Deliverable:** Live RAG app with public URL, dashboards, traces. **Push + reflect:** blog post "From notebook to production RAG: 7 things I learned the hard way."

**Time budget:** ~35 hrs.

---

### Week 18 — Production-Grade Agent (Flagship Project #5)

**Daily:** 3 hr agent building, 1 hr reading.

**Tasks:**
- **Build a real agent.** Pick one:
  - **Coding agent** that can read/edit/run code in a sandboxed repo.
  - **Research agent** that searches, reads, synthesizes, cites.
  - **Data analyst agent** that queries a SQL DB, runs Python, and produces reports.
- **Components:**
  - Tool use via Anthropic/OpenAI function calling.
  - ReAct or Plan-and-Execute loop.
  - Memory: short-term (in-context) + long-term (vector store for past interactions).
  - Sandbox for code execution (E2B, Modal, or Docker).
  - MCP server integration if appropriate.
  - Evals: AgentBench-style tasks, custom evals, human evaluation of 20 traces.
- **DSA:** 5 problems + 1 system design mock.

**Deliverable:** `projects/05-agent-system/` — a real, demoable agent with eval results. **Push + reflect.**

**Time budget:** ~35 hrs.

---

### Week 19 — System Design Deep Dive (AI Systems)

**Daily:** 2 designs/week (90 min each), 1 hr reading, 30 min DSA.

**Tasks:**
- **Practice these designs** (write up each in `system-design/` with diagram + trade-offs):
  1. **RAG system for enterprise search** at 10M docs, 1K QPS, p95 < 1s.
  2. **Coding agent** like Cursor: editor integration, retrieval, sandboxed execution, iter loops.
  3. **Multi-tenant LLM gateway:** auth, rate limits, cost tracking, model routing, caching, fallbacks.
  4. **Real-time recommendation system:** candidates → ranking → embeddings → online learning.
- **For each design, cover:** latency budget, cost per request, failure modes, caching, batching, privacy, evals, observability, rollback.
- **Read:** Chip Huyen's *AI Engineering* chapters on system design.
- **DSA:** 5 problems + 1 mock interview.

**Deliverable:** 4 written system designs with diagrams, each ~2–3 pages. **Push + reflect: a "design notes" public doc.**

**Time budget:** ~32 hrs.

---

### Week 20 — MLOps + Observability Sprint

**Daily:** 3 hr ops, 1 hr reading.

**Tasks:**
- **For your RAG or agent project, add:**
  - Experiment tracking with W&B or MLflow (track all evals, configs, prompts).
  - Data versioning with DVC or lakeFS (for your eval sets and prompts).
  - Prompt versioning (Langfuse or your own).
  - A/B testing harness (even simulated, with statistical significance).
  - Drift detection on inputs and outputs.
  - Cost dashboards (per-tenant or per-feature cost).
- **Read:** Designing Machine Learning Systems chapters 6–8 (data engineering, model deployment, data distribution shifts).
- **DSA:** 5 problems + 1 mock.

**Deliverable:** Production-quality observability on your flagship. **Push + reflect.**

**Time budget:** ~32 hrs.

**End of Month 5 Checkpoint:**
- [ ] 5 flagship projects shipped.
- [ ] 1 OSS contribution (start now if not done).
- [ ] 150+ DSA problems solved.
- [ ] 6 blog posts published.
- [ ] 4 system designs written up.
- [ ] Live demo URLs for at least 2 projects.

---

## Month 6 — Interview Loop, Portfolio Polish, and Applications (Weeks 21–24)

> **Theme:** Convert the work into offers. Grind the loop deliberately.

### Week 21 — OSS Contribution + Resume + Portfolio

**Daily:** 2 hr OSS work, 1 hr portfolio polish, 1 hr DSA, 30 min apps.

**Tasks:**
- **OSS contribution:**
  - Pick a project (vLLM, TRL, LangChain, DSPy, Instructor, etc.).
  - Find a "good first issue" or a small bug/feature.
  - Submit a real PR. Iterate on review feedback.
  - If you can't land one in 2 weeks, write a well-documented external tool/integration that references the project (still counts as a contribution).
- **Resume rewrite:**
  - One page, impact-driven. Quantify everything (latency reduced X%, eval improved Y points, cost cut $Z).
  - 3 projects featured with: problem, what you built, tech stack, results, link to code/demo.
  - Have 2–3 trusted reviewers (AI engineers at target companies) tear it apart.
- **Portfolio polish:**
  - Clean READMEs for all repos: GIF/video demo, architecture diagram, quickstart, results, what you learned.
  - Polish GitHub profile, pinned repos, profile README.
  - Make 1 short demo video (3 min) for your best project.
- **DSA:** Daily problems + 1 mock interview.

**Deliverable:** Landed OSS PR (or equivalent). Polished resume. Demo video. **Push everything.**

**Time budget:** ~32 hrs.

---

### Week 22 — Interview Prep: ML Knowledge + Coding

**Daily:** 2 hr ML knowledge review, 2 hr DSA, 30 min mock prep.

**Tasks:**
- **ML knowledge review (be able to explain each, derive from scratch):**
  - Backprop, optimizers (SGD, Adam, AdamW), LR schedules.
  - Transformers end-to-end (attention, MLP, residuals, RoPE, KV-cache, GQA, MoE routing).
  - Diffusion (DDPM forward/reverse process, classifier-free guidance, flow matching).
  - Fine-tuning (LoRA math, DPO loss, RLHF pipeline, PRMs for reasoning).
  - Tokenization (BPE, why it matters for multilingual/code; tiktoken, SentencePiece).
  - Evaluation (MMLU, SWE-bench Verified, OSWorld, MMMU, IFEval; metrics, A/B testing, LLM-as-judge calibration).
  - Common debugging: loss not decreasing, NaN losses, OOM, slow training, attention sink, context-length degradation.
  - **Current SOTA (June 2026):** Claude Sonnet 4.5 = 77.2% SWE-bench Verified, 61.4% OSWorld, 30+ hour focus; GPT-5.5 is OpenAI's current API default; Gemini 3.5 leads Google's lineup; DeepSeek-R1 is the open-weight reasoning benchmark.
- **DSA:** Contests, hard problems, focus on weak areas.
- **Mock interviews:**
  - 1x ML coding (implement a transformer block, sampler, or LoRA layer on a shared doc).
  - 1x system design (RAG or batch inference API).
  - 1x behavioral (use your STAR bank).
- **Project deep-dive prep:** for each flagship, prepare to discuss trade-offs, latency, cost, and at least one decision you'd reverse.

**Deliverable:** Study guide of 50 ML Q&A in your own words + 1 recorded mock. **Push.**

**Time budget:** ~35 hrs.

---

### Week 23 — Interview Prep: System Design + Behavioral (Verified Loop Details)

**Daily:** 2 hr system design practice, 1 hr behavioral prep, 1 hr DSA, 30 min apps.

**Tasks:**
- **System design mocks:** Do 2–3 full mocks (use Pramp, interviewing.io, Exponent, or a friend). Practice narrating trade-offs. For AI roles, expect **LLM-infrastructure and distributed-systems** problems (batch inferencing APIs, GPU usage optimization with batching, distributing large model files). For SWE-applied roles, expect scale-focused design (multi-tenant LLM gateway, recsys, RAG at 10M+ docs).
- **Coding interview prep — verified format:**
  - **Anthropic-style problems are NOT LeetCode.** Practice multi-tiered practical problems: build a web crawler → multi-thread it → add a filtered dictionary. Or: in-memory DB → add TTL → add advanced queries. Get comfortable layering constraints on a working solution. For ML roles: **MCP tooling, error diagnosis, model reliability for long-running tasks**.
  - **OpenAI SWE coding may include OOP / class design** (e.g., a layered object-oriented problem built around a chatbot interface), not just DSA. Practice both.
  - **OpenAI research engineer bar:** *"graduate-level machine learning and information theory."* Be ready to derive the cross-entropy loss, explain KL divergence, sketch a sampler, write a small transformer on a shared doc.
- **Behavioral prep — this is where most candidates fail at top AI companies:**
  - At Anthropic, **culture fit is the highest-failure round**. At OpenAI, the recruiter screen itself is *"a real behavioral interview, not a lightweight intro call"* — full STAR in 30 min.
  - Write **6 polished STAR-format stories**: a hard technical project, a conflict, a failure, a leadership moment, a disagreement, a measurement-driven decision. Rehearse out loud.
  - For each flagship project, be ready to go **10 minutes deep** on every design decision, including the trade-offs and what you'd reverse. **OpenAI: expect a ~1-hour project walkthrough.**
- **"Why us" answer:** every interviewer at Anthropic and OpenAI will ask *"Why [company]?"* — be specific. Read the company's engineering blog, recent papers, recent product launches, and have an informed opinion.
- **Comp negotiation primer:**
  - At Anthropic, recruiters present **two comp bands early as a negotiation tactic** — treat them as informational, not as a final offer.
  - Pull Levels.fyi data for your target role, level, and location before the recruiter screen. **Anthropic SWE median = $665K, P75 = $870K** (June 2026, n=20). **Google SWE P75 = $410K, P90 = $547K** (n=149).
  - Always counter; build multiple offers before deciding.
- **Target list:**
  - Spreadsheet of 20+ target companies with: role, comp range (from Levels.fyi), referrer status, application status.
  - Reach out to 10 people at target companies for chats (LinkedIn, Twitter, alumni networks).
  - Apply to 5 companies this week.
- **DSA:** Daily + 1 mock.

**Deliverable:** Behavioral bank, 1 recorded system design mock, 1 recorded behavioral mock, 5 applications out, 5 referral chats booked. **Push.**

**Time budget:** ~35 hrs.

---

### Week 24 — Final Polish, Applications Blitz, Onsites

**Daily:** 2 hr interviews / apps, 1 hr targeted prep, 1 hr reflection, 1 hr DSA.

**Tasks:**
- **Apply broadly:** 3–5 applications/day. Aim for 30+ applications total.
- **Tailor resume** to each role. Mention specific tech the job uses.
- **Continue mocks:** 2x system design, 1x ML coding this week.
- **Run the final 2-week sprint checklist** (see below).
- **Update blog:** "What I learned in 6 months of becoming an AI engineer."
- **DSA:** Maintain, don't cram.

**Deliverable:** 30+ applications out, multiple interview loops started.

**Time budget:** ~35 hrs.

**End of Month 6 Checkpoint:**
- [ ] 3–5 flagship public projects.
- [ ] 1+ OSS contribution.
- [ ] 6 blog posts.
- [ ] 150–200+ DSA problems solved.
- [ ] Resume polished, portfolio polished.
- [ ] Multiple interviews scheduled.
- [ ] Comfortable with ML, system design, coding, behavioral rounds.

---

## Weekly Review Template

Every Sunday, 30 min. Save in `progress.md` in your main repo.

```markdown
# Week N Review (Dates)

## What I shipped
- [ ] Code/push/feature/learning artifact

## What I learned (3 bullets max)
- 
- 
- 

## Where I struggled
- 

## What I'll do differently next week
- 

## Hours logged
- Study: __
- Build: __
- Reading: __
- DSA: __

## Mood / Energy (1–5)
- 

## Next week's #1 deliverable
- 
```

---

## Backup / Catch-up Strategy

You will fall behind. That's normal. Here's how to recover:

### If you fall 1 week behind
- Drop optional fluff (some reading, some blog posts).
- Keep the weekly primary deliverable.
- Cut weekend hours to 4 hrs.

### If you fall 2 weeks behind
- Skip the current week's secondary project work.
- Drop one blog post.
- Increase weekday hours by 1 hr.
- Skip a DSA contest.

### If you fall 3+ weeks behind
- **Re-evaluate the plan.** Are you over-committing? Are you stuck on one topic?
- Drop Month 1 depth items you can come back to (extra reading).
- Consider a structured break (3–5 days off) to reset.
- Ask for help: post in study groups, find an accountability partner.
- **Do not abandon the plan.** Adjust it.

### Anti-recovery traps
- Re-doing topics you already know to feel productive.
- Switching to "easier" resources when stuck.
- Reading more blogs when you should be coding.

---

## Final 2-Week Sprint Before Interviews

Use this in the last 2 weeks before your first big onsites.

### Day-by-Day Outline

**Week A (before interview)**

| Day | Morning (2 hr) | Afternoon (2 hr) | Evening (1 hr) |
|---|---|---|---|
| Mon | DSA hard problems (2) | ML knowledge: derivations (transformer, backprop, LoRA) | 1 behavioral STAR story polish |
| Tue | DSA contest (1.5 hr) + review | System design: 1 full mock (RAG system) | Read 1 paper you've cited in projects |
| Wed | DSA medium-hard (3) | ML coding: implement sampling + KV-cache in your tiny GPT | 1 system design: coding agent |
| Thu | DSA: review last 30 days of problems | Behavioral: 3 STAR stories refined, get feedback | Light reading |
| Fri | DSA contest (1.5 hr) + review | System design: 1 full mock (multi-tenant LLM gateway) | Reflect + early sleep |
| Sat | Walk + light DSA (1 hr) | Review 3 flagship project READMEs, be ready to deep-dive | Early sleep |
| Sun | Walk + no work | **No work.** Recharge. | **No work.** |

**Week B (interview week)**

| Day | Activity |
|---|---|
| Mon | 1 final system design mock + 1 final ML coding practice |
| Tue | Light review: 30 min ML flashcards, 30 min STAR bullets |
| Wed | **The interview.** Sleep 8+ hrs the night before. |
| Thu | (Post-interview) Debrief what went well/poorly. Adjust for next. |
| Fri | Next interview prep, or back to applying. |
| Weekend | Rest + targeted weak-area work. |

### The Night-Before Checklist
- [ ] Print out or pin the 50 ML Q&A.
- [ ] Re-read 1 project README end-to-end.
- [ ] Prep questions for the interviewer (3–5 thoughtful ones).
- [ ] Charge laptop, test mic/cam, water bottle ready.
- [ ] Outfit ready, calm playlist queued.
- [ ] **Sleep 8 hours.** This is the highest-leverage prep you can do.

### The Morning-Of Checklist
- [ ] Eat real food (protein, complex carbs).
- [ ] 10-min walk or stretch.
- [ ] Review 1 page of notes (don't cram).
- [ ] Smile before you join. Energy is read in the first 5 seconds.

---

## Closing Thoughts

This plan is **deliberately ambitious**. Treat it as a stretch goal, not a minimum bar. If you hit 80% of this, you will be in the top decile of AI engineering candidates. If you hit 100%, you will be a top-1% candidate by the time you're done.

The single biggest predictor of success isn't talent or background — it's **consistency over 6 months**. Showing up 5 days a week, every week, for 26 weeks, compounds in ways that 80-hour hero weeks never can.

Stay honest about what you know. Stay kind to yourself when you fall behind. Stay dangerous when you ship.

---

## Verification & Sources (June 2026)

This plan was checked against live primary sources on the day of writing. Key verifications:

**Compensation (Levels.fyi JSON-LD, lastReviewed 2026-06-18):**
- **Anthropic SWE:** P25 $570K · median $665K · P75 $870K · P90 $920K. Base P25 $320K; equity P75 $550K. (n=20)
- **Google SWE:** P25 $215K · P75 $410K · P90 $547K. (n=149)
- **OpenAI / Meta / NVIDIA:** Levels.fyi JSON-LD was bot-blocked at scrape time; ranges cross-referenced with public reporting and recruiter data. Treat ±20%.

**Interview process (Exponent guides, last updated 3 days before this writing):**
- **Anthropic:** recruiter screen (15–30 min, comp discussed here) → 60–90 min technical phone screen (CodeSignal / Replit / Colab, **practical multi-tiered problems, not LeetCode**) → 2-day onsite split into Loop 1 (system design, coding, culture fit) and Loop 2 (experiences, project deep-dive). If you don't pass Loop 1, Loop 2 is cancelled. **Culture fit is the highest-failure round.**
- **OpenAI:** recruiter / hiring manager screen (30 min, *"a real behavioral interview, not a lightweight intro call"*) → technical assessment (coding + system design, or 48-hr take-home for data/design/growth) → 4–6 session final loop (1–2 days) with a **~1 hour project walkthrough** and sometimes **4–5 slides about a system you built**. **L5 at OpenAI ≈ L6 at Meta/Google.** Recruiters may down-level candidates 1–2 levels.
- **AI tool use in interview:** permitted for ML/prompt-engineering roles, **not permitted for SWE or AI Safety Fellowship roles.**

**Models (June 2026, verified from provider docs):**
- OpenAI: GPT-5.5 (current API default), GPT-5, o-series reasoning, GPT-4.1, GPT-4o.
- Anthropic: Claude Mythos 5, Claude Fable 5, Claude Opus 4.8, **Claude Sonnet 4.5** (SOTA on SWE-bench Verified at **77.2%**, OSWorld **61.4%**, 30+ hour focus, $3/$15 per M tokens), Claude Haiku 4.5.
- Google: Gemini 3.5, Gemini 2.5 Pro/Flash, Gemma 3, Veo, Imagen "Nano Banana", Lyria.
- Meta: Llama 3.3 70B, Llama 3.1 (8B/70B/405B), Llama 4 (multimodal).
- Mistral, DeepSeek (V3, R1), xAI (Grok 3), Qwen 3 (incl. Qwen3-235B-A22B MoE), Moonshot (Kimi K2), Phi (Microsoft), Command R (Cohere).

**India-specific sources (Levels.fyi JSON-LD, all lastReviewed 2026-06-18):**
- **Google India SWE (n=73):** P25 ₹36.5L · P75 ₹80.9L · P90 ₹1.23Cr.
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
- **OpenAI India (n=0):** single data point ₹55.8L. **Anthropic India (n=0):** no data yet.
- **Sarvam AI** (Bengaluru) — $1.5B Series B (June 2026), verified from sarvam.ai.

**What I did NOT verify (and you should treat with skepticism):**
- Specific leveling / TC for OpenAI L4–L6 and Meta E5–E6 (US and India) — public reporting varies; treat ranges as ±20%.
- OpenAI India and Anthropic India comp — n=0 at scrape time, so the ₹55.8L OpenAI India point is a single data anchor, not a median.
- Indic-AI specific salaries at Sarvam/Krutrim — public reporting is sparse.
- Hiring bar shifts month-to-month at these companies.
- Any claim about a specific team's culture or process — those vary by org.
- Projections beyond the public roadmap.

> If a number in this plan contradicts something on Levels.fyi or in a recent blog post, the live source wins. This is a snapshot, not gospel.

— *Adapted from the AI_ENGINEER_MASTERY_ROADMAP.md. Treat this as a working document — adjust, edit, make it yours.*
