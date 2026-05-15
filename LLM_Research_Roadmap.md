# Everything You Need to Learn to Get Into LLM Research

> A comprehensive, opinionated roadmap — from zero to publishing research.
> Organized in the order you should learn things, not alphabetical.

---

## Table of Contents

- [Phase 1: Mathematical Foundations](#phase-1-mathematical-foundations)
- [Phase 2: Programming & Tools](#phase-2-programming--tools)
- [Phase 3: Machine Learning Fundamentals](#phase-3-machine-learning-fundamentals)
- [Phase 4: Deep Learning](#phase-4-deep-learning)
- [Phase 5: NLP & Sequence Modeling](#phase-5-nlp--sequence-modeling)
- [Phase 6: Transformer Architecture (Deep)](#phase-6-transformer-architecture-deep)
- [Phase 7: Large Language Models](#phase-7-large-language-models)
- [Phase 8: Training Infrastructure & Systems](#phase-8-training-infrastructure--systems)
- [Phase 9: Data Engineering](#phase-9-data-engineering)
- [Phase 10: Alignment & Safety](#phase-10-alignment--safety)
- [Phase 11: Evaluation & Benchmarks](#phase-11-evaluation--benchmarks)
- [Phase 12: Efficient Inference & Deployment](#phase-12-efficient-inference--deployment)
- [Phase 13: Agents & Tool Use](#phase-13-agents--tool-use)
- [Phase 14: Research Skills](#phase-14-research-skills)
- [Phase 15: Frontier Topics (2025–2026)](#phase-15-frontier-topics-20252026)
- [Reading List: The Papers That Matter](#reading-list-the-papers-that-matter)
- [Weekly Study Plan](#weekly-study-plan)

---

## Phase 1: Mathematical Foundations

You don't need to be a mathematician, but you need to be comfortable with the math that shows up in every paper. Learn these in order — each builds on the previous.

### 1.1 Linear Algebra

**Why**: Every neural network operation is a matrix multiplication. Attention is literally Q·K^T. If you don't understand matrix math, you can't read any paper.

| Topic | What to learn | Why it matters |
|-------|--------------|----------------|
| Vectors & matrices | Addition, multiplication, transpose | Basic operations everywhere |
| Dot product | Geometric interpretation | Core of attention mechanism |
| Matrix multiplication | Why (m×n)·(n×p) = (m×p), not commutative | Every layer in a transformer |
| Eigenvalues/eigenvectors | What they represent, how to compute | PCA, understanding representations |
| SVD (Singular Value Decomposition) | Factorize A = UΣV^T | Low-rank approximations, LoRA |
| Norms | L1, L2, Frobenius | Regularization, gradient clipping |
| Softmax | exp(x_i) / Σexp(x_j) | Attention weights, classification |

**Resources**:
- 3Blue1Brown — "Essence of Linear Algebra" (YouTube, ~3 hours)
- Gilbert Strang — MIT 18.06 (full semester, optional but deep)
- "Mathematics for Machine Learning" — Deisenroth, Faisal, Ong (free PDF, Chapters 2–4)

### 1.2 Calculus

**Why**: Backpropagation is the chain rule applied recursively. Optimization is gradient descent. You need calculus to understand how models learn.

| Topic | What to learn | Why it matters |
|-------|--------------|----------------|
| Derivatives | Rate of change, slope | Gradient = direction of steepest ascent |
| Partial derivatives | ∂f/∂x when f depends on multiple variables | Every parameter update |
| Chain rule | d/dx f(g(x)) = f'(g(x))·g'(x) | Backpropagation is this, applied recursively |
| Jacobians | Matrix of all partial derivatives | Understanding gradients of vector functions |
| Gradient descent | x_new = x - lr · ∇f | The learning algorithm |
| Multivariable optimization | Saddle points, local minima, convexity | Why training is hard |

**Resources**:
- Khan Academy — Multivariable Calculus
- 3Blue1Brown — "Essence of Calculus" (YouTube)
- "The Matrix Calculus You Need for Deep Learning" — Parr & Howard (free paper)

### 1.3 Probability & Statistics

**Why**: Language models are probability distributions over tokens. Loss functions are cross-entropy (a concept from information theory). Sampling strategies (temperature, top-k, top-p) are probabilistic.

| Topic | What to learn | Why it matters |
|-------|--------------|----------------|
| Probability distributions | Gaussian, Bernoulli, Categorical | Weight initialization, sampling |
| Bayes' theorem | P(A|B) = P(B|A)·P(A) / P(B) | Bayesian reasoning, priors |
| Expectation & variance | E[X], Var(X) | Batch normalization, initialization |
| Maximum Likelihood Estimation | argmax_θ P(data | θ) | How LLMs are trained |
| KL divergence | D_KL(P || Q) = Σ P(x) log(P(x)/Q(x)) | Loss functions, distillation |
| Entropy | H(X) = -Σ P(x) log P(x) | Perplexity = 2^H |
| Cross-entropy | H(P, Q) = -Σ P(x) log Q(x) | THE loss function for language models |

**Resources**:
- StatQuest with Josh Starmer (YouTube — great for intuition)
- "Probabilistic Machine Learning" — Kevin Murphy (free PDF)
- Khan Academy — Statistics and Probability

### 1.4 Information Theory

**Why**: Perplexity, cross-entropy loss, mutual information — these are the vocabulary of LLM research.

| Concept | Formula | LLM connection |
|---------|---------|----------------|
| Shannon entropy | H = -Σ p log p | Average surprise of a distribution |
| Cross-entropy | H(p,q) = -Σ p log q | Training loss |
| KL divergence | D_KL(p‖q) = Σ p log(p/q) | Distillation, alignment |
| Perplexity | PP = 2^H | How we measure language model quality |
| Mutual information | I(X;Y) = H(X) - H(X|Y) | How much X tells you about Y |

---

## Phase 2: Programming & Tools

### 2.1 Python (Must be fluent)

Not "can read" — fluent. You need to write, debug, and prototype quickly.

| Topic | Level needed |
|-------|-------------|
| Data structures | dicts, lists, sets, tuples — when to use each |
| OOP | Classes, inheritance, dunder methods |
| Functional | map, filter, lambda, list comprehensions |
| Type hints | `def f(x: list[int]) -> Tensor` |
| Debugging | pdb, print debugging, reading tracebacks |
| Virtual environments | venv, conda, pip |
| Profiling | cProfile, line_profiler, memory_profiler |

### 2.2 PyTorch (The research framework)

Every major lab uses PyTorch. Learn it deeply, not just `model(x)`.

| Topic | What to learn |
|-------|--------------|
| Tensors | Creation, indexing, broadcasting, device management |
| Autograd | How `.backward()` works, computation graphs |
| nn.Module | Building custom layers, `forward()`, parameter registration |
| Optimizers | SGD, Adam, AdamW — what each hyperparameter does |
| Data loading | Dataset, DataLoader, custom collate functions |
| Training loops | Forward, loss, backward, step — the basic loop |
| Mixed precision | `torch.cuda.amp`, FP16/BF16 training |
| Distributed | `torch.distributed`, DDP, FSDP |

**Resources**:
- Official PyTorch tutorials (pytorch.org/tutorials)
- Andrej Karpathy — "Neural Networks: Zero to Hero" (YouTube, 8 lectures)
- "Programming PyTorch for Deep Learning" — Ian Pointer

### 2.3 Essential Tools

| Tool | Why |
|------|-----|
| Git | Version control (branching, merging, rebasing) |
| Linux/CLI | Most training happens on Linux servers |
| Docker | Reproducible environments |
| Weights & Biases (wandb) | Experiment tracking (industry standard) |
| Hugging Face Hub | Model hosting, datasets, spaces |
| SSH + tmux | Running long experiments on remote machines |
| nvtop / nvidia-smi | GPU monitoring |

---

## Phase 3: Machine Learning Fundamentals

Before diving into neural networks, understand the foundations.

### 3.1 Core Concepts

| Concept | What to learn |
|---------|--------------|
| Supervised learning | Classification, regression, loss functions |
| Train/dev/test splits | Why, how to do it right |
| Bias-variance tradeoff | Underfitting vs overfitting |
| Regularization | L1, L2, dropout — why they help |
| Cross-validation | k-fold, stratified |
| Feature engineering | Why it matters less with deep learning |
| Evaluation metrics | Accuracy, precision, recall, F1, AUC |

### 3.2 Classic ML Algorithms (know them, don't master them)

- Linear regression, logistic regression
- Decision trees, random forests, gradient boosting (XGBoost)
- SVM (the kernel trick is a beautiful idea)
- k-NN, k-means clustering
- PCA (dimensionality reduction)

**Resources**:
- Andrew Ng — CS229 (Stanford, YouTube)
- fast.ai — "Practical Deep Learning for Coders" (top-down approach)
- "Hands-On Machine Learning" — Aurélien Géron

---

## Phase 4: Deep Learning

### 4.1 Neural Network Fundamentals

| Topic | What to learn |
|-------|--------------|
| Perceptrons → MLPs | Single neuron to multi-layer networks |
| Activation functions | ReLU, GELU, SwiGLU, SiLU — when to use which |
| Backpropagation | Chain rule applied to computation graphs |
| Weight initialization | Xavier, He, why it matters |
| Batch normalization | What it does, why it works, train vs eval mode |
| Layer normalization | Why Transformers use this instead of BatchNorm |
| Dropout | Training vs inference behavior |
| Gradient problems | Vanishing/exploding gradients, gradient clipping |

### 4.2 Optimization

| Topic | What to learn |
|-------|--------------|
| SGD | Stochastic gradient descent, momentum |
| Adam | Adaptive learning rates, bias correction |
| AdamW | Weight decay decoupled from gradient update |
| Learning rate schedules | Cosine, linear warmup, Noam schedule |
| Gradient clipping | Max norm, when to use it |
| Warmup | Why starting with small LR helps |

### 4.3 CNNs (know the concepts)

You won't use CNNs in LLM research, but understanding them builds intuition for:
- Convolution as a local attention pattern
- Pooling as downsampling
- Residual connections (ResNet → Transformer)

**Resources**:
- Stanford CS231n — Computer Vision (YouTube)
- Andrej Karpathy — "Neural Networks: Zero to Hero" (YouTube)
- "Deep Learning" — Goodfellow, Bengio, Courville (free online)

---

## Phase 5: NLP & Sequence Modeling

### 5.1 Text Representation (Historical)

Understand where we came from to appreciate why Transformers won.

| Era | Model | Key idea |
|-----|-------|----------|
| 2000s | Bag of Words, TF-IDF | Count words, ignore order |
| 2013 | Word2Vec | Words as vectors, semantic arithmetic |
| 2014 | GloVe | Global vector statistics |
| 2015 | FastText | Subword embeddings |

### 5.2 Sequence Models (Pre-Transformer)

| Model | Key idea | Limitation |
|-------|----------|------------|
| RNN | Hidden state h_t = f(x_t, h_{t-1}) | Vanishing gradients, slow |
| LSTM | Gates control information flow | Still sequential |
| GRU | Simplified LSTM | Still sequential |
| Seq2Seq | Encoder-decoder for translation | Bottleneck in fixed-size context |
| Attention (Bahdanau 2014) | Let decoder attend to all encoder states | Still uses RNNs |

### 5.3 Tokenization

**This is more important than most people realize.** A lot of LLM weirdness traces back to tokenization.

| Method | Used by | How it works |
|--------|---------|-------------|
| BPE (Byte Pair Encoding) | GPT-2/3/4, LLaMA | Bottom-up: merge most frequent character pairs |
| WordPiece | BERT, DistilBERT | Like BPE but merges based on likelihood, not frequency |
| Unigram | T5, mBART | Top-down: start with large vocab, remove tokens |
| SentencePiece | LLaMA, T5 | Framework that implements BPE/Unigram, language-agnostic |
| Byte-level BPE | GPT-2, LLaMA | Operates on raw bytes, handles any Unicode |

**Key insight**: Tokenization determines what the model can and cannot learn easily. A model that tokenizes "1234" as ["12", "34"] can't do arithmetic on individual digits.

**Resources**:
- Andrej Karpathy — "Let's build the GPT Tokenizer" (YouTube, 2h13m)
- Hugging Face Tokenizers library documentation
- "byte pair encoding" — Sennrich et al., 2016 (original paper)

### 5.4 Word Embeddings → Contextual Embeddings

| Model | Embedding type |
|-------|---------------|
| Word2Vec/GloVe | Static — same vector for "bank" in all contexts |
| ELMo (2018) | Contextual — bidirectional LSTM generates different embeddings |
| BERT (2018) | Contextual — Transformer encoder, bidirectional |
| GPT (2018) | Contextual — Transformer decoder, left-to-right |

---

## Phase 6: Transformer Architecture (Deep)

You've already built one. Now go deeper.

### 6.1 The Original Paper

"Attention Is All You Need" — Vaswani et al., 2017

Read it. Then read it again. Understand every equation.

| Component | Section | Key formula |
|-----------|---------|-------------|
| Scaled dot-product attention | 3.2.1 | softmax(QK^T / √d_k) · V |
| Multi-head attention | 3.2.2 | Concat(head_1,...,head_h) · W_O |
| Position-wise FFN | 3.3 | max(0, xW_1 + b_1)W_2 + b_2 |
| Positional encoding | 3.5 | sin/cos at different frequencies |
| Residual + LayerNorm | 3.1, 3.4 | LayerNorm(x + Sublayer(x)) |

### 6.2 Transformer Variants

| Variant | Type | Key difference |
|---------|------|----------------|
| Original | Encoder-decoder | Full architecture, for seq2seq |
| GPT | Decoder-only | Causal (left-to-right) attention only |
| BERT | Encoder-only | Bidirectional attention, masked LM |
| T5 | Encoder-decoder | Text-to-text framing |
| LLaMA | Decoder-only | RMSNorm, SwiGLU, RoPE, GQA |
| Mistral | Decoder-only | Sliding window attention, GQA |

### 6.3 Attention Mechanism Variants

| Variant | Key idea | Paper |
|---------|----------|-------|
| Multi-Head Attention | Parallel attention heads | Vaswani 2017 |
| Multi-Query Attention | Share K/V across heads | Shazeer 2019 |
| Grouped-Query Attention | Groups of heads share K/V | Ainslie 2023 |
| Multi-Latent Attention | Compress KV to latent space | DeepSeek-V2 2024 |
| Flash Attention | IO-aware exact attention | Dao 2022 |
| Sliding Window Attention | Attend only to local window | Beltagy 2020 (Longformer) |
| Sparse Attention | Fixed patterns | Child 2019 |
| Linear Attention | Approximate softmax with random features | Choromanski 2021 (Performer) |

### 6.4 Positional Encoding Deep Dive

| Method | Type | Properties |
|--------|------|-----------|
| Sinusoidal | Fixed | Absolute, extrapolates poorly |
| Learned | Trainable | Absolute, doesn't extrapolate |
| Relative (Shaw) | Learned | Relative distance, clipped |
| ALiBi | Fixed | Additive bias, extrapolates |
| RoPE | Fixed | Rotary, encodes relative position, extrapolates with NTK scaling |
| YaRN | Modified RoPE | Extended context via NTK-aware interpolation |

**Resources**:
- Lilian Weng — "The Transformer Family v2.0" (excellent survey)
- "Efficient Transformers: A Survey" — Tay et al., 2022
- Jay Alammar — "The Illustrated Transformer" (visual guide)

---

## Phase 7: Large Language Models

### 7.1 The GPT Lineage

| Model | Year | Parameters | Key contribution |
|-------|------|-----------|------------------|
| GPT-1 | 2018 | 117M | Transformer decoder for language modeling |
| GPT-2 | 2019 | 1.5B | "Language Models are Unsupervised Multitask Learners" |
| GPT-3 | 2020 | 175B | In-context learning, few-shot prompting |
| InstructGPT | 2022 | 175B | RLHF for alignment |
| GPT-4 | 2023 | ~1.8T (rumored MoE) | Multimodal, better reasoning |

### 7.2 The Open-Source LLM Lineage

| Model | Year | Key contribution |
|-------|------|------------------|
| LLaMA | 2023 | Open-weight foundation models |
| Mistral 7B | 2023 | Sliding window attention, efficient |
| LLaMA 2 | 2023 | GQA, longer context |
| Mixtral 8x7B | 2024 | Sparse MoE |
| LLaMA 3 | 2024 | 128K context, better data |
| DeepSeek-V2 | 2024 | Multi-Latent Attention, MLA |
| Qwen 2.5 | 2024 | Strong multilingual |
| LLaMA 4 | 2025 | MoE, native multimodal |
| DeepSeek-R1 | 2025 | RL-based reasoning |

### 7.3 Scaling Laws

The most important empirical discovery in LLM research.

**Kaplan et al. (2020)** — "Scaling Laws for Neural Language Models":
- Loss follows a power law with model size, dataset size, and compute
- Bigger models are sample-efficient (need fewer tokens per parameter)
- Implication: invest in scaling, not architecture search

**Chinchilla (Hoffmann et al., 2022)** — "Training Compute-Optimal Large Language Models":
- The Kaplan scaling was wrong about data
- Optimal: tokens ≈ 20× parameters
- Chinchilla (70B) beat Gopher (280B) because it used more data
- Implication: data is as important as model size

**Post-Chinchilla (2024–2025)**:
- Inference cost matters too, not just training FLOPs
- Over-training (tokens >> 20× params) is practical for inference-heavy deployments
- Data-constrained scaling: what if you run out of data?
- Scaling laws for fine-tuning and alignment

### 7.4 Key Training Concepts

| Concept | What it is |
|---------|-----------|
| Pre-training | Next-token prediction on trillions of tokens |
| Causal Language Modeling | Predict token_t given tokens_{<t} |
| Masked Language Modeling | Predict masked tokens from context (BERT) |
| Curriculum learning | Ordering training data by difficulty |
| Data mixing | Ratios of code, math, web, books, etc. |
| Tokenizer training | BPE/SentencePiece on the training corpus |

### 7.5 Emergent Abilities

Certain capabilities appear suddenly at scale (not gradually):
- In-context learning (GPT-3 scale)
- Chain-of-thought reasoning (~100B+)
- Instruction following (fine-tuned models)
- Tool use (GPT-4 scale)

**Controversy**: Some researchers argue "emergence" is a measurement artifact, not a real phenomenon.

---

## Phase 8: Training Infrastructure & Systems

You can't do LLM research without understanding the systems.

### 8.1 GPU Architecture (for ML)

| Concept | What to know |
|---------|-------------|
| CUDA cores | Parallel compute units |
| Tensor cores | Matrix multiply hardware (FP16/BF16/FP8) |
| HBM (High Bandwidth Memory) | Why memory bandwidth is the bottleneck |
| NVLink | GPU-to-GPU interconnect |
| FLOPS | How to compute theoretical peak FLOPS |
| Memory hierarchy | Registers → shared memory → L2 → HBM |

### 8.2 Mixed Precision Training

| Precision | Bits | Use case |
|-----------|------|----------|
| FP32 | 32 | Baseline, slow |
| FP16 | 16 | Faster but can overflow |
| BF16 | 16 | Best for training (wider range than FP16) |
| FP8 | 8 | Newest, H100+ hardware |

**How it works**: Store weights in FP16/BF16, compute in FP16/BF16, keep a FP32 copy of weights for the optimizer update.

### 8.3 Distributed Training

| Strategy | What it does |
|----------|-------------|
| Data Parallel (DP) | Each GPU has full model, different data |
| Distributed Data Parallel (DDP) | Like DP but with gradient synchronization |
| ZeRO (DeepSpeed) | Shard optimizer states, gradients, or parameters across GPUs |
| FSDP (PyTorch) | PyTorch's native implementation of ZeRO-like sharding |
| Tensor Parallel | Split individual layers across GPUs |
| Pipeline Parallel | Split model layers across GPUs |
| Expert Parallel | For MoE — different experts on different GPUs |

**Frameworks**:
- **DeepSpeed** (Microsoft) — ZeRO optimization, most popular for large-scale
- **Megatron-LM** (NVIDIA) — Tensor/pipeline parallel for massive models
- **FSDP** (PyTorch native) — Good default for most research
- **Colossal-AI** — Another option, good documentation
- **Accelerate** (Hugging Face) — Simplifies distributed training

### 8.4 Memory Optimization

| Technique | How it saves memory |
|-----------|-------------------|
| Gradient checkpointing | Recompute activations in backward pass instead of storing |
| CPU offloading | Move optimizer states to CPU when not needed |
| Mixed precision | Half-precision weights and activations |
| Gradient accumulation | Simulate larger batch sizes |
| Activation recomputation | Recompute instead of storing |

### 8.5 Compute Requirements (Ballpark)

| Model size | Min GPUs | Training time | Cost estimate |
|-----------|---------|---------------|---------------|
| 1B | 1-2 A100 | Days | ~$1K |
| 7B | 4-8 A100 | 1-2 weeks | ~$10K |
| 70B | 64-128 A100 | 1-2 months | ~$500K |
| 400B+ | 1000+ H100 | Months | $10M+ |

---

## Phase 9: Data Engineering

Data is arguably more important than architecture. "Textbooks Are All You Need" showed that curated data can beat 100× more web data.

### 9.1 Pre-training Data Sources

| Source | Quality | Volume | Notes |
|--------|---------|--------|-------|
| Web crawls (Common Crawl) | Low-Medium | Massive | Needs heavy filtering |
| Books | High | Medium | Copyright issues |
| Wikipedia | High | Small | Good for factual knowledge |
| Code (GitHub) | Medium-High | Large | Improves reasoning |
| Scientific papers | High | Medium | ArXiv, PubMed |
| Math (stack exchange, textbooks) | High | Small | Improves math reasoning |

### 9.2 Data Processing Pipeline

```
Raw web crawl
  → URL filtering (remove adult/spam domains)
  → Language identification (fastText lid.176)
  → Text extraction (trafilatura, jusText)
  → Quality filtering (classifier or heuristics)
  → Deduplication (MinHash + LSH)
  → PII removal
  → Tokenization
  → Shuffle and shard
```

### 9.3 Quality Filtering

| Method | How it works |
|--------|-------------|
| Heuristic rules | Document length, word count, repetition rate, symbol ratios |
| Classifier-based | Train on "high quality" (Wikipedia) vs "random web" |
| Perplexity filtering | Use a reference LM, filter low-perplexity (too simple) or high-perplexity (garbage) |
| Language ID score | Filter documents with low language ID confidence |

### 9.4 Deduplication

| Method | Type | Library |
|--------|------|---------|
| URL dedup | Exact | Simple hash |
| Hash dedup | Exact | SHA-256 of documents |
| MinHash + LSH | Near-duplicate | datatrove, text-dedup |
| SemDedup | Semantic | Embedding-based clustering |

### 9.5 Notable Datasets

| Dataset | Size | Key feature |
|---------|------|-------------|
| The Pile | 800GB | 22 diverse sources, curated |
| RedPajama v2 | 30T+ tokens | Quality signals per document |
| FineWeb (HuggingFace) | 15T tokens | Quality-filtered web data |
| Dolma (AI2) | 3T tokens | Open pipeline documentation |
| RefinedWeb (Falcon) | 5T tokens | High-quality filtered web |
| StarCoder Data | 1T+ tokens | Code-focused |
| Proof-Pile | Medium | Math-focused |

### 9.6 Data Mixing

The ratio of different data sources matters enormously. Typical recipe:
- ~60-70% web text
- ~15-20% code
- ~5-10% books
- ~5% academic papers
- ~3-5% math
- ~2-3% Wikipedia

**Key papers**:
- "Textbooks Are All You Need" — Gunasekar et al. (data quality > quantity)
- "DataComp-LM" — Li et al. (benchmarking data curation)
- "Scaling Data-Constrained Language Models" — Muennighoff et al.

---

## Phase 10: Alignment & Safety

Pre-training gives you a language model. Alignment makes it useful and safe.

### 10.1 The Alignment Pipeline

```
Pre-trained base model
  → Supervised Fine-Tuning (SFT) on instruction-response pairs
  → RLHF / DPO / Constitutional AI
  → Red teaming and safety filters
  → Deployment
```

### 10.2 Supervised Fine-Tuning (SFT)

- Collect (instruction, response) pairs from humans
- Fine-tune the base model to predict the response given the instruction
- This teaches the model to follow instructions

### 10.3 RLHF (Reinforcement Learning from Human Feedback)

| Step | What happens |
|------|-------------|
| 1. Collect preferences | Humans rank model outputs (A > B > C) |
| 2. Train reward model | Learn to predict human preferences |
| 3. RL optimization | PPO optimizes the policy to maximize reward while staying close to SFT model (KL penalty) |

**Challenges**: Reward hacking, expensive human annotation, training instability.

### 10.4 DPO (Direct Preference Optimization)

**Key insight**: You can skip the reward model entirely. DPO directly optimizes the policy on preference data using a closed-form loss.

```
L_DPO = -E[log σ(β · (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))]
```

Where y_w = preferred response, y_l = rejected response, π_ref = reference (SFT) model.

**DPO variants (2024–2025)**:
| Variant | Key difference |
|---------|---------------|
| IPO | Removes the sigmoid, uses identity |
| KTO | Uses Kahneman-Tversky prospect theory (doesn't need pairs) |
| ORPO | Combines SFT and preference in one step |
| SimPO | Reference-free, simpler |
| SPPO | Self-play for iterative improvement |

### 10.5 Constitutional AI (Anthropic)

1. Define a set of principles (the "constitution")
2. Have the AI critique its own responses against these principles
3. Use AI-generated preferences for training (RLAIF — RL from AI Feedback)
4. Reduces reliance on human labelers

### 10.6 Safety Techniques

| Technique | What it does |
|-----------|-------------|
| Red teaming | Adversarial testing to find failure modes |
| Circuit breakers | Stop harmful outputs at the representation level |
| Safety classifiers | Filter inputs/outputs |
| Guardrails (Llama Guard) | Separate model to evaluate safety |
| Representation engineering | Modify internal representations to remove harmful behaviors |

### 10.7 Scalable Oversight

How do we align models smarter than us?

| Approach | Key idea |
|----------|---------|
| Debate | Two AI systems argue, human judges |
| Weak-to-strong | Use weak model to supervise strong one |
| Process reward models (PRMs) | Reward each reasoning step, not just final answer |
| Recursive reward modeling | Use AI to help humans evaluate AI |

**Key papers**:
- "Training language models to follow instructions with human feedback" — Ouyang et al. (InstructGPT)
- "Direct Preference Optimization" — Rafailov et al.
- "Constitutional AI" — Bai et al. (Anthropic)
- "Weak-to-Strong Generalization" — Burns et al. (OpenAI)
- "DeepSeek-R1" — DeepSeek (RL for reasoning)

---

## Phase 11: Evaluation & Benchmarks

### 11.1 Perplexity

The most basic metric. Measures how well the model predicts text.

```
Perplexity = 2^(cross-entropy loss)
```

Lower is better. A model with perplexity 10 is "surprised" by ~10 equally likely next tokens.

### 11.2 Standard Benchmarks

| Benchmark | What it tests | Format |
|-----------|---------------|--------|
| MMLU | 57 subjects, broad knowledge | Multiple choice |
| HellaSwag | Commonsense reasoning | Sentence completion |
| ARC | Science questions (grade 3-9) | Multiple choice |
| WinoGrande | Coreference resolution | Binary choice |
| GSM8K | Grade school math | Open-ended |
| MATH | Competition math | Open-ended |
| HumanEval | Code generation | pass@k |
| MBPP | Basic Python programming | pass@k |
| TruthfulQA | Factuality | Multiple choice |
| IFEval | Instruction following | Constraint checking |
| GPQA | Graduate-level science | Multiple choice |

### 11.3 Arena-style Evaluation

| Platform | Method |
|----------|--------|
| Chatbot Arena | Human preference ELO rankings (LMSYS) |
| AlpacaEval | LLM-as-judge win rates |
| MT-Bench | Multi-turn conversation quality |
| LMSYS Arena | Live human preference voting |

### 11.4 Research Methodology Concerns

| Problem | Description |
|---------|-------------|
| Data contamination | Training data may include benchmark answers |
| Benchmark saturation | Models exceed human performance, benchmarks become useless |
| Prompt sensitivity | Results vary significantly with prompt format |
| Overfitting to benchmarks | Models optimized for specific evaluations |
| Reproducibility | Different hardware, random seeds, prompting give different results |

### 11.5 Evaluation for Research

When evaluating your own research:
- Always compare to a strong baseline
- Report multiple metrics, not just one
- Show ablation studies (what happens when you remove your contribution)
- Report variance across random seeds
- Test on held-out benchmarks, not just the ones you optimized for

---

## Phase 12: Efficient Inference & Deployment

### 12.1 Quantization

| Method | Bits | Quality impact |
|--------|------|---------------|
| FP16/BF16 | 16 | None |
| INT8 | 8 | Minimal |
| INT4 | 4 | Noticeable for small models |
| GPTQ | 4 | Post-training, good quality |
| AWQ | 4 | Activation-aware, better than GPTQ |
| GGUF (llama.cpp) | 2-8 | Variable, CPU-friendly |
| FP8 | 8 | Minimal, needs H100+ |

### 12.2 KV-Cache

During autoregressive generation, previously computed K and V are cached to avoid recomputation.

- Memory: O(batch_size × num_layers × seq_len × d_model)
- This is why long contexts are expensive
- KV-cache compression is an active research area

### 12.3 Speculative Decoding

Use a small "draft" model to generate candidate tokens, then verify with the large model in parallel. If the draft model is right (often 70-90% of the time), you get multiple tokens for the cost of one large model forward pass.

### 12.4 Inference Frameworks

| Framework | Key feature |
|-----------|------------|
| vLLM | PagedAttention, continuous batching |
| TensorRT-LLM | NVIDIA-optimized, fastest on NVIDIA GPUs |
| llama.cpp | CPU inference, quantization |
| SGLang | Structured generation, RadixAttention |
| TGI (Hugging Face) | Easy deployment |
| MLC-LLM | Cross-platform (mobile, browser) |

### 12.5 Mixture of Experts (MoE)

Instead of a dense FFN, use multiple "expert" FFNs and a router that selects which experts to activate per token.

```
Router(x) → top-k expert indices
Output = Σ router_weight_i * Expert_i(x)
```

- Mixtral 8x7B: 8 experts, activate 2 per token → 47B total, ~13B active
- Advantages: more parameters without proportional compute increase
- Challenges: load balancing, training stability, expert collapse

---

## Phase 13: Agents & Tool Use

### 13.1 LLM Agent Architecture

```
User Request
  → LLM (reasoning/planning)
  → Tool selection & invocation
  → Observe results
  → Iterate or respond
```

### 13.2 Key Techniques

| Technique | What it does |
|-----------|-------------|
| Chain of Thought (CoT) | "Let's think step by step" |
| Tree of Thoughts (ToT) | Explore multiple reasoning paths (BFS/DFS) |
| ReAct | Thought → Action → Observation loop |
| Reflexion | Self-reflection and memory across attempts |
| Toolformer | Fine-tune LMs to use APIs |
| Function calling | Structured tool invocation |

### 13.3 Retrieval-Augmented Generation (RAG)

```
Query → Retrieve relevant documents → LLM generates with context
```

| Component | Options |
|-----------|---------|
| Embedding model | text-embedding-3, E5, BGE, GTE |
| Vector store | FAISS, Pinecone, Weaviate, Chroma |
| Chunking | Fixed size, semantic, recursive |
| Reranking | Cross-encoder, Cohere rerank |

### 13.4 Memory Systems

| Type | Implementation |
|------|---------------|
| Short-term | In-context learning (within prompt) |
| Long-term | Vector store with retrieval |
| Working | Scratchpad / chain-of-thought |
| Episodic | Past interaction logs |

---

## Phase 14: Research Skills

### 14.1 How to Read Papers

**The three-pass approach**:

1. **First pass (5-10 min)**: Title, abstract, figures, conclusion. Should you care?
2. **Second pass (1 hour)**: Read without proving equations. Understand the method, experiments, results.
3. **Third pass (4-5 hours)**: Reimplement from scratch. Understand every detail.

### 14.2 How to Find Research Problems

| Strategy | Example |
|----------|---------|
| Reproduce and extend | "The paper claims X, but what about Y?" |
| Identify limitations | "This doesn't work when..." |
| Combine ideas | "What if we apply A to problem B?" |
| Scale down | "Can we get 90% of the benefit at 10% of the cost?" |
| Improve baselines | "The baseline is weak, what if we..." |

### 14.3 Experiment Design

| Component | What to do |
|-----------|-----------|
| Hypothesis | "We hypothesize that..." |
| Baseline | Strong, well-known baseline |
| Ablation | Remove one thing at a time |
| Controlled variables | Change one thing, keep everything else fixed |
| Multiple seeds | Report mean ± std across 3-5 seeds |
| Statistical significance | Is the improvement real or noise? |

### 14.4 Paper Writing

| Section | Content |
|---------|---------|
| Abstract | Problem → method → result (in 150 words) |
| Introduction | Why this matters, what's missing, what we do |
| Related work | What others did, how we differ |
| Method | Enough detail to reproduce |
| Experiments | Fair comparison, ablations, analysis |
| Discussion | Limitations, future work |

### 14.5 Where to Publish

| Venue | Focus |
|-------|-------|
| NeurIPS | Broad ML |
| ICML | Broad ML |
| ICLR | Representation learning |
| ACL | NLP |
| EMNLP | NLP (empirical) |
| NAACL | NLP (North America) |
| COLM | Language modeling (new, 2024) |
| arXiv cs.CL | Pre-prints (how most LLM research is shared) |

---

## Phase 15: Frontier Topics (2025–2026)

### 15.1 Reasoning & Chain-of-Thought

| Technique | Key idea |
|-----------|---------|
| Chain of Thought | Explicit reasoning steps in the prompt |
| Self-Consistency | Sample multiple reasoning paths, majority vote |
| Tree of Thoughts | BFS/DFS over reasoning tree |
| Process Reward Models | Reward each step, not just final answer |
| Outcome Reward Models | Reward final answer only |
| DeepSeek-R1 | RL-trained reasoning without supervised CoT data |
| o1/o3 (OpenAI) | Test-time compute scaling |

### 15.2 Test-Time Compute Scaling

Instead of scaling model size, scale computation at inference time:
- Generate more candidate solutions
- Use verifiers to select the best one
- Search over reasoning trees
- Budget forcing (controlling how long the model "thinks")

### 15.3 Multimodal Models

| Type | Examples |
|------|---------|
| Vision-Language | GPT-4V, LLaVA, Qwen-VL |
| Audio-Language | Whisper, Qwen-Audio |
| Video-Language | Video-LLaVA, Gemini |
| Native multimodal | Gemini, GPT-4o (joint training) |

### 15.4 Long Context

| Technique | Context length |
|-----------|---------------|
| RoPE + NTK scaling | 32K → 128K |
| YaRN | 64K → 256K+ |
| Ring Attention | Distributed, near-infinite |
| Sparse attention | Longformer-style |
| Compression | AutoCompressor, Gisting |

### 15.5 Code Generation

| Model | Focus |
|-------|-------|
| Codex/GitHub Copilot | Code completion |
| StarCoder | Open-source code |
| DeepSeek-Coder | Strong open-source |
| Cursor/Devin | Full IDE integration |

### 15.6 Mixture of Experts (MoE)

The architecture choice for frontier models (GPT-4, Mixtral, DeepSeek-V2, LLaMA 4):
- Sparse activation: only a subset of parameters are used per token
- Scaling law: more total parameters, same compute per token
- Challenges: load balancing, expert collapse, communication overhead

### 15.7 Mechanistic Interpretability

Understanding what's happening inside models:
- **Superposition**: models represent more features than dimensions
- **Circuit analysis**: tracing specific behaviors through the network
- **Sparse autoencoders**: decomposing activations into interpretable features
- **Activation patching**: causal interventions on internal representations

### 15.8 Synthetic Data

Using LLMs to generate training data:
- Self-instruct: LLM generates instructions for itself
- Evol-Instruct: evolve instructions to be more complex
- Self-play: model trains against itself
- Distillation: strong model generates data for weak model

---

## Reading List: The Papers That Matter

### Tier 1 — Read These First (Foundational)

| # | Paper | Year | Why |
|---|-------|------|-----|
| 1 | "Attention Is All You Need" — Vaswani et al. | 2017 | The Transformer |
| 2 | "BERT" — Devlin et al. | 2018 | Encoder-only, pre-training |
| 3 | "Language Models are Unsupervised Multitask Learners" — Radford et al. | 2019 | GPT-2 |
| 4 | "Language Models are Few-Shot Learners" — Brown et al. | 2020 | GPT-3, in-context learning |
| 5 | "Scaling Laws for Neural Language Models" — Kaplan et al. | 2020 | Scaling laws |
| 6 | "Training Compute-Optimal Large Language Models" — Hoffmann et al. | 2022 | Chinchilla scaling |

### Tier 2 — Read These Next (Architecture & Training)

| # | Paper | Year | Why |
|---|-------|------|-----|
| 7 | "LLaMA" — Touvron et al. | 2023 | Open-weight foundation model |
| 8 | "FlashAttention" — Dao et al. | 2022 | IO-aware attention |
| 9 | "GQA: Training Generalized Multi-Query Transformer Models" — Ainslie et al. | 2023 | Grouped-query attention |
| 10 | "RoFormer: Enhanced Transformer with Rotary Position Embedding" — Su et al. | 2021 | RoPE |
| 11 | "Training language models to follow instructions" — Ouyang et al. | 2022 | InstructGPT, RLHF |
| 12 | "Direct Preference Optimization" — Rafailov et al. | 2023 | DPO |

### Tier 3 — Read These for Depth

| # | Paper | Year | Why |
|---|-------|------|-----|
| 13 | "Constitutional AI" — Bai et al. | 2022 | Alignment without humans |
| 14 | "Textbooks Are All You Need" — Gunasekar et al. | 2023 | Data quality |
| 15 | "Mixture of Experts" — Shazeer et al. | 2017 | MoE architecture |
| 16 | "Longformer" — Beltagy et al. | 2020 | Efficient long-context |
| 17 | "Reformer" — Kitaev et al. | 2020 | Efficient attention |
| 18 | "Chain of Thought Prompting" — Wei et al. | 2022 | Reasoning |
| 19 | "Tree of Thoughts" — Yao et al. | 2023 | Structured reasoning |
| 20 | "DeepSeek-R1" — DeepSeek | 2025 | RL for reasoning |
| 21 | "Attention is Not Explanation" — Jain & Wallace | 2019 | Critical view on attention |
| 22 | "A Survey of Efficient Transformers" — Tay et al. | 2022 | Comprehensive survey |
| 23 | "The Transformer Family v2.0" — Lilian Weng | 2023 | Blog survey |
| 24 | "Scaling Data-Constrained Language Models" — Muennighoff et al. | 2023 | Data scaling |

### Tier 4 — Blogs & Supplementary

| Resource | Author | Why |
|----------|--------|-----|
| lilianweng.github.io | Lilian Weng | Best LLM blog, rigorously cited |
| The Illustrated Transformer | Jay Alammar | Visual explanations |
| Andrej Karpathy YouTube | Karpathy | "Neural Networks: Zero to Hero" |
| Sebastian Raschka's blog | Raschka | Practical LLM research |
| Cameron Wolfe's Substack | Wolfe | LLM research summaries |
| Yannic Kilcher YouTube | Kilcher | Paper explanations |
| Two Minute Papers YouTube | Károly Zsolnai-Fehér | Quick paper summaries |

---

## Weekly Study Plan

### Months 1–2: Foundations

| Week | Focus | Resources |
|------|-------|-----------|
| 1-2 | Linear algebra | 3Blue1Brown, Khan Academy |
| 3-4 | Calculus + optimization | 3Blue1Brown, Khan Academy |
| 5-6 | Probability & information theory | StatQuest, Khan Academy |
| 7-8 | Python + PyTorch basics | Official tutorials, Karpathy |

### Months 3–4: ML & Deep Learning

| Week | Focus | Resources |
|------|-------|-----------|
| 9-10 | ML fundamentals | CS229 or fast.ai |
| 11-12 | Neural networks, backprop | Karpathy "Zero to Hero" |
| 13-14 | CNNs, RNNs, optimization | CS231n |
| 15-16 | NLP fundamentals | CS224n |

### Months 5–6: Transformers & LLMs

| Week | Focus | Resources |
|------|-------|-----------|
| 17-18 | Transformer architecture | "Attention Is All You Need", this repo |
| 19-20 | BERT, GPT lineage | Original papers |
| 21-22 | Scaling laws, Chinchilla | Papers + Lilian Weng blog |
| 23-24 | Training systems | DeepSpeed, FSDP docs |

### Months 7–8: Alignment & Advanced Topics

| Week | Focus | Resources |
|------|-------|-----------|
| 25-26 | RLHF, DPO, alignment | Papers + HuggingFace TRL |
| 27-28 | Efficient inference | Flash Attention, quantization |
| 29-30 | Agents, RAG, tool use | Papers + LangChain |
| 31-32 | Mechanistic interpretability | Anthropic research |

### Months 9–12: Research

| Week | Focus |
|------|-------|
| 33-36 | Reproduce a recent paper from scratch |
| 37-40 | Identify a research question, run experiments |
| 41-44 | Write up results, get feedback |
| 45-48 | Submit to workshop or arXiv |

---

## Final Advice

1. **Build things.** Reading papers without implementing is like watching cooking videos without cooking. Implement everything.

2. **Read papers, not just blogs.** Blog posts are summaries. Papers have the details you need for research.

3. **Start small.** Don't try to train a 7B model. Reproduce a small result first.

4. **Join the community.** Follow researchers on Twitter/X (Andrej Karpathy, Yann LeCun, Sebastian Raschka, Lilian Weng). Join r/MachineLearning, r/LocalLLaMA.

5. **The field moves fast.** This document will be partially outdated in 6 months. That's normal. Learn the fundamentals — they don't change.

6. **You don't need a PhD.** Many impactful contributions come from engineers and independent researchers. What you need is deep understanding, good taste in problems, and persistence.
