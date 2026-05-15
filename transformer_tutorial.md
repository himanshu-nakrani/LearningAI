# Transformer from Scratch — A Step-by-Step Guide

> This document walks you through every component of the Transformer architecture
> (Vaswani et al., 2017 — "Attention Is All You Need"). Each section explains the
> concept, shows the math, and connects it to the code in `transformer.py`.

---

## Table of Contents

1. [Why Transformers?](#1-why-transformers)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Embeddings & Positional Encoding](#3-embeddings--positional-encoding)
4. [Self-Attention](#4-self-attention)
5. [Multi-Head Attention](#5-multi-head-attention)
6. [Feed-Forward Network](#6-feed-forward-network)
7. [Add & Norm](#7-add--norm)
8. [Encoder Stack](#8-encoder-stack)
9. [Decoder Stack](#9-decoder-stack)
10. [Masking](#10-masking)
11. [Putting It All Together](#11-putting-it-all-together)
12. [Training](#12-training)
13. [What's Next](#13-whats-next)

---

## 1. Why Transformers?

### The problem with RNNs

Before Transformers, sequence modeling was dominated by RNNs (and their variants — LSTMs, GRUs). RNNs process tokens **one at a time**, maintaining a hidden state:

```
h_t = f(x_t, h_{t-1})   // must wait for previous step
```

This creates two problems:

1. **Sequential bottleneck** — you can't parallelize across time steps. Training on a GPU with 1000s of cores wastes most of them.
2. **Long-range dependencies** — information must pass through every intermediate step. The gradient signal for token 1 must survive 100 steps to reach token 100.

### The Transformer insight

**"Attention is all you need"** — you don't need recurrence at all. Instead:

- Every token can attend to **every other token** directly (no sequential bottleneck)
- The path length between any two positions is **O(1)** (not O(n) like in RNNs)
- Everything can be **parallelized** across the sequence dimension

The cost: O(n^2) in sequence length for attention. But for typical sequence lengths (hundreds to thousands of tokens), this is a great tradeoff on modern hardware.

---

## 2. High-Level Architecture

The original Transformer is an **encoder-decoder** model designed for sequence-to-sequence tasks (like translation):

```
┌─────────────────────────────────────────────────────────────┐
│                      TRANSFORMER                            │
│                                                             │
│  src_tokens ──►┌──────────┐    ┌──────────┐──► logits      │
│                │ ENCODER   │───►│ DECODER   │               │
│  tgt_tokens ──►│  (N layers)│    │  (N layers)│               │
│                └──────────┘    └──────────┘               │
└─────────────────────────────────────────────────────────────┘
```

**Encoder**: reads the source sequence and produces contextual representations.
**Decoder**: generates the target sequence one token at a time, attending to:
  - Previous target tokens (masked self-attention)
  - The full encoder output (cross-attention)

### Data flow

```
Source: "I love AI"
  → Tokenize: [45, 12, 89]
  → Encoder: contextual embeddings for each position
  → Cross-attention: decoder queries the encoder

Target: "J'adore l'IA"
  → Tokenize: [<sos>, 67, 23, 91]
  → Decoder: generates [67, 23, 91, <eos>] autoregressively
  → Each position attends to all previous positions + encoder
```

---

## 3. Embeddings & Positional Encoding

### Input Embedding

The first step is converting token IDs into dense vectors:

```python
# transformer.py — InputEmbedding
class InputEmbedding(nn.Module):
    def __init__(self, vocab_size: int, d_model: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.d_model = d_model

    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
```

**Why multiply by sqrt(d_model)?** The embedding values are learned and typically O(1) in magnitude. Positional encodings are also O(1). Without scaling, the embeddings would dominate the positional signal. The paper scales embeddings up so they're on the same footing as positional encodings.

### Positional Encoding

Since the Transformer has no recurrence, it has **no inherent sense of order**. The token "dog bites man" and "man bites dog" would look identical without positional information.

The paper uses **sinusoidal encodings** — fixed (not learned) functions of position:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Where:
- `pos` = position in the sequence (0, 1, 2, ...)
- `i` = dimension index (0, 1, ..., d_model/2)
- Each dimension uses a different frequency

**Why sinusoids?**

1. Each position gets a unique encoding
2. The encoding for position `pos+k` can be expressed as a linear function of the encoding for `pos` (because sin(a+b) = sin(a)cos(b) + cos(a)sin(b)). This lets the model learn to attend to **relative** positions.
3. The values are bounded between -1 and 1, regardless of sequence length

```python
# transformer.py — PositionalEncoding
class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)  # even dimensions
        pe[:, 1::2] = torch.cos(position * div_term)  # odd dimensions
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]  # add PE to embeddings
        return self.dropout(x)
```

**Key detail:** `register_buffer` makes `pe` part of the model state (saved/loaded) but **not** a learnable parameter. The positional encoding is deterministic.

---

## 4. Self-Attention

This is the core mechanism. Let's build it up from intuition.

### The problem

Given a sentence, how should each word "think about" the other words? In "The cat sat on the mat", when processing "sat", the model should pay attention to "cat" (who is sitting) and "mat" (where).

### Query, Key, Value

The attention mechanism gives each token three roles:

- **Query (Q)**: "What am I looking for?"
- **Key (K)**: "What do I contain?"
- **Value (V)**: "What information do I provide?"

These are produced by three separate linear projections:

```
Q = X @ W_Q    (what each position wants to know)
K = X @ W_K    (what each position offers)
V = X @ W_V    (what each position actually gives)
```

### Scaled dot-product attention

```
Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V
```

Step by step:

1. **Q @ K^T**: compute similarity between every query and every key. Result is (seq_len, seq_len) — a grid of attention scores.

2. **/ sqrt(d_k)**: scaling prevents the dot products from becoming too large (which would push softmax into regions with tiny gradients). If Q and K are random unit vectors, their dot product has variance 1/d_k. Scaling by sqrt(d_k) keeps the variance at 1.

3. **softmax**: normalize each row to sum to 1. Now each position has a probability distribution over all other positions.

4. **@ V**: weighted sum of values. Each position gets a blend of all values, weighted by how relevant they are.

### Visual example

```
"The cat sat on the mat"

When processing "sat":
  Q(sat) @ K(cat)^T  = 0.8   ← high: "who is sitting?"
  Q(sat) @ K(mat)^T  = 0.5   ← medium: "where?"
  Q(sat) @ K(the)^T  = 0.1   ← low: determiners less relevant
  Q(sat) @ K(on)^T   = 0.05  ← low

After softmax: [0.1, 0.44, 0.28, 0.03, 0.06, 0.09]
  → output = 0.44*V(cat) + 0.28*V(mat) + ...
```

The output for "sat" now contains information weighted toward "cat" and "mat" — it knows *who* sat *where*.

---

## 5. Multi-Head Attention

A single attention head can only learn one type of relationship. But language has many simultaneous relationships: syntax (subject-verb), semantics (word meaning), position (adjacent words), etc.

**Solution**: run multiple attention heads in parallel, each with its own learned projections:

```
head_i = Attention(X @ W_Q_i, X @ W_K_i, X @ W_V_i)
MultiHead(X) = Concat(head_1, ..., head_h) @ W_O
```

Each head operates on d_k = d_model / h dimensions (so the total compute is the same as a single full-dimension head).

```python
# transformer.py — MultiHeadAttention
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        self.d_k = d_model // num_heads
        self.num_heads = num_heads

        self.W_q = nn.Linear(d_model, d_model)  # projects to all heads at once
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)  # output projection
```

**Why an output projection W_O?** The concatenation of heads creates a d_model-dimensional vector. W_O lets the model learn how to combine information from different heads — it's a learned mixing step.

### Implementation detail: batched heads

Instead of looping over heads, we reshape the tensor so heads are a batch dimension:

```python
# (batch, seq_len, d_model) → (batch, seq_len, num_heads, d_k) → (batch, num_heads, seq_len, d_k)
Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
```

Now the attention computation runs over all heads simultaneously using batched matrix multiply.

---

## 6. Feed-Forward Network

After attention mixes information across positions, each position goes through an independent two-layer MLP:

```
FFN(x) = max(0, x @ W1 + b1) @ W2 + b2
```

```python
# transformer.py — FeedForward
class FeedForward(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)   # expand: d_model → d_ff
        self.linear2 = nn.Linear(d_ff, d_model)    # compress: d_ff → d_model
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.linear2(self.dropout(F.relu(self.linear1(x))))
```

**Why d_ff = 4 * d_model?** The expansion gives the network more capacity to transform features. Think of it as: attention decides *which* positions to attend to, and the FFN decides *what to do* with that information.

**Key property**: the FFN is applied **independently** to each position. It's the same as a 1x1 convolution over the sequence dimension.

---

## 7. Add & Norm

Each sub-layer (attention or FFN) is wrapped with:

```
output = LayerNorm(x + Dropout(sublayer(x)))
```

Two things are happening here:

### Residual connections

`x + sublayer(x)` — the input is added directly to the output. This is crucial because:

1. **Gradient highway**: during backpropagation, gradients can flow directly through the skip connection, avoiding vanishing gradients in deep networks
2. **Easier learning**: the sublayer only needs to learn a *residual* correction, not a full transformation. Learning "adjust the input slightly" is easier than "reconstruct the output from scratch"

### Layer normalization

```python
# transformer.py — AddNorm
class AddNorm(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer_output):
        return self.norm(x + self.dropout(sublayer_output))
```

**LayerNorm vs BatchNorm**: BatchNorm normalizes across the batch dimension (depends on other samples). LayerNorm normalizes across the feature dimension (each sample independently). LayerNorm is preferred for:

- Variable-length sequences (batch statistics would be unreliable)
- Small batch sizes (batch statistics would be noisy)
- The Transformer's architecture (works better empirically)

---

## 8. Encoder Stack

The encoder is N identical layers stacked on top of each other:

```python
# transformer.py — EncoderLayer
class EncoderLayer(nn.Module):
    def forward(self, x, src_mask=None):
        # Sub-layer 1: self-attention (Q=K=V=x)
        attn_output = self.self_attention(x, x, x, src_mask)
        x = self.add_norm1(x, attn_output)

        # Sub-layer 2: feed-forward
        ff_output = self.feed_forward(x)
        x = self.add_norm2(x, ff_output)

        return x
```

**What does each layer learn?** Early layers tend to learn syntactic patterns (adjacent words, part-of-speech). Later layers learn semantic relationships (coreference, long-range dependencies). This emerges naturally from training — the architecture doesn't enforce it.

```
Input tokens
  → Embedding + Positional Encoding
  → Layer 1: self-attention → FFN
  → Layer 2: self-attention → FFN
  → ...
  → Layer N: self-attention → FFN
  → Encoder output (contextualized representations)
```

Each layer refines the representation. By layer N, each position's vector encodes information from the **entire** input sequence, weighted by learned relevance.

---

## 9. Decoder Stack

The decoder is similar to the encoder but has **three** sub-layers instead of two:

```python
# transformer.py — DecoderLayer
class DecoderLayer(nn.Module):
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # Sub-layer 1: MASKED self-attention (Q=K=V=x, causal mask)
        attn_output = self.self_attention(x, x, x, tgt_mask)
        x = self.add_norm1(x, attn_output)

        # Sub-layer 2: cross-attention (Q=x, K=V=encoder_output)
        cross_output = self.cross_attention(x, encoder_output, encoder_output, src_mask)
        x = self.add_norm2(x, cross_output)

        # Sub-layer 3: feed-forward
        ff_output = self.feed_forward(x)
        x = self.add_norm3(x, ff_output)

        return x
```

### The three sub-layers

1. **Masked self-attention**: same as encoder self-attention, but with a **causal mask** that prevents position `i` from attending to positions `> i`. This is essential during training — without it, the model could "cheat" by looking at future tokens.

2. **Cross-attention**: the decoder queries the encoder output. The queries come from the decoder, but the keys and values come from the encoder. This is how the decoder "reads" the source sentence.

   ```
   Q = decoder_state    (what does the decoder need?)
   K = encoder_output   (what's available in the source?)
   V = encoder_output   (the actual source information)
   ```

3. **Feed-forward**: same as the encoder.

### Autoregressive generation

During inference, the decoder generates one token at a time:

```
Step 1: [<sos>]                    → predict "J'"
Step 2: [<sos>, J']                → predict "adore"
Step 3: [<sos>, J', adore]         → predict "l'"
Step 4: [<sos>, J', adore, l']     → predict "IA"
Step 5: [<sos>, J', adore, l', IA] → predict "<eos>"
```

The causal mask ensures each step only sees previous tokens, matching how the model was trained.

---

## 10. Masking

The Transformer uses two types of masks:

### Padding mask

Sequences in a batch have different lengths, so shorter ones are padded with `<pad>` tokens. We don't want the model to attend to padding:

```python
# transformer.py — make_src_mask
def make_src_mask(src, pad_token_id=0):
    # (batch, seq_len) → (batch, 1, 1, seq_len)
    return (src != pad_token_id).unsqueeze(1).unsqueeze(2)
```

The mask is broadcast over the query positions and heads dimensions.

### Causal mask

Prevents the decoder from attending to future positions:

```python
# transformer.py — make_tgt_mask
def make_tgt_mask(tgt, pad_token_id=0):
    batch_size, tgt_len = tgt.size()

    pad_mask = (tgt != pad_token_id).unsqueeze(1).unsqueeze(2)
    causal_mask = torch.tril(torch.ones(tgt_len, tgt_len, device=tgt.device)).bool()

    return pad_mask & causal_mask
```

The causal mask is a lower-triangular matrix:

```
Position:  0  1  2  3  4
    0  [  1  0  0  0  0 ]   ← pos 0 only sees itself
    1  [  1  1  0  0  0 ]   ← pos 1 sees 0, 1
    2  [  1  1  1  0  0 ]   ← pos 2 sees 0, 1, 2
    3  [  1  1  1  1  0 ]   ← pos 3 sees 0, 1, 2, 3
    4  [  1  1  1  1  1 ]   ← pos 4 sees everything
```

### How masks are applied

In the attention computation, masked positions get `-inf` before softmax:

```python
scores = scores.masked_fill(mask == 0, float("-inf"))
# softmax(-inf) = 0, so those positions contribute nothing
```

---

## 11. Putting It All Together

The full `Transformer` class ties everything together:

```python
# transformer.py — Transformer
class Transformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=512, ...):
        self.encoder = Encoder(src_vocab_size, d_model, ...)
        self.decoder = Decoder(tgt_vocab_size, d_model, ...)
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        encoder_output = self.encoder(src, src_mask)
        decoder_output = self.decoder(tgt, encoder_output, src_mask, tgt_mask)
        logits = self.output_projection(decoder_output)
        return logits
```

### Complete data flow

```
src: [batch, src_len]          token IDs
  → InputEmbedding             (batch, src_len, d_model)
  → + PositionalEncoding       (batch, src_len, d_model)
  → Encoder (N layers)         (batch, src_len, d_model)
  = encoder_output

tgt: [batch, tgt_len]          token IDs
  → InputEmbedding             (batch, tgt_len, d_model)
  → + PositionalEncoding       (batch, tgt_len, d_model)
  → Decoder (N layers)         (batch, tgt_len, d_model)
      ↑ cross-attention to encoder_output
  → Linear(d_model, vocab)     (batch, tgt_len, vocab_size)
  = logits (raw scores per token)
```

### Parameters (paper default)

| Parameter    | Value  | Description                    |
|-------------|--------|--------------------------------|
| d_model     | 512    | Model dimension                |
| num_heads   | 8      | Attention heads                |
| d_ff        | 2048   | FFN inner dimension (4× d_model)|
| num_layers  | 6      | Encoder and decoder layers     |
| d_k = d_v   | 64     | Per-head dimension (512/8)     |
| dropout     | 0.1    | Dropout rate                   |

Total: ~65M parameters (base model).

---

## 12. Training

### Loss function

The paper uses **label smoothing** with cross-entropy:

```python
criterion = nn.CrossEntropyLoss(label_smoothing=0.1, ignore_index=0)
```

**Label smoothing**: instead of training toward hard targets (one-hot), we train toward soft targets. For label smoothing ε=0.1:
- Correct token: 0.9 (instead of 1.0)
- All other tokens: 0.1 / (vocab_size - 1) each

This prevents the model from becoming overconfident and improves generalization.

**ignore_index=0**: don't compute loss on padding tokens.

### Learning rate schedule (Noam)

The paper uses a custom schedule with warmup:

```python
lr = d_model^(-0.5) * min(step^(-0.5), step * warmup_steps^(-1.5))
```

```
         │      ╱╲
  lr     │     ╱  ╲
         │    ╱    ╲────────────
         │   ╱      ╲
         │  ╱        ╲
         │ ╱          ╲
         └──────────────────── step
           warmup    decay
```

1. **Warmup** (first ~4000 steps): linearly increase LR. This prevents large, unstable gradients at the start of training when weights are random.
2. **Decay** (after warmup): decrease LR proportional to 1/sqrt(step). This fine-tunes the model as it converges.

### Gradient clipping

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

Prevents exploding gradients by capping the total gradient norm.

### Optimizer

```python
optimizer = torch.optim.Adam(model.parameters(), lr=LR, betas=(0.9, 0.98), eps=1e-9)
```

The paper uses Adam with β1=0.9, β2=0.98 (lower than the default 0.999 — makes the optimizer more responsive to recent gradients).

---

## 13. What's Next

The Transformer has spawned many variants. Here's how to think about them:

### Decoder-only (GPT-style)

Remove the encoder and cross-attention. The decoder alone can do language modeling:

```
"The cat sat" → predict "on" → "The cat sat on" → predict "the"
```

Used in: GPT, LLaMA, Mistral, Claude, etc.

### Encoder-only (BERT-style)

Remove the decoder and causal mask. Use bidirectional attention for understanding tasks:

```
"The [MASK] sat on the mat" → predict "cat"
```

Used in: BERT, RoBERTa, sentence embeddings.

### Modern improvements

| Innovation | What it does |
|-----------|-------------|
| **RoPE** (Rotary Position Embeddings) | Better relative position encoding, used in LLaMA |
| **GQA** (Grouped Query Attention) | Shares K/V heads across query heads, saves memory |
| **Flash Attention** | IO-aware attention algorithm, 2-4x faster |
| **RMSNorm** | Simpler layer norm variant, slightly faster |
| **SwiGLU** | Better activation function than ReLU in FFN |
| **KV-Cache** | Stores past K/V during inference, avoids recomputation |
| **Sparse Attention** | Attend to subsets of positions (long sequences) |

### The big picture

Every modern LLM is a Transformer variant. Understanding this implementation gives you the mental model to read any of them. The core ideas — attention, residual connections, layer normalization — are universal. Everything else is optimization.

---

## Quick Reference: Key Formulas

```
Attention:    softmax(Q @ K^T / sqrt(d_k)) @ V
MultiHead:    Concat(head_1, ..., head_h) @ W_O
FFN:          max(0, x @ W1 + b1) @ W2 + b2
AddNorm:      LayerNorm(x + sublayer(x))
PE(pos,2i):   sin(pos / 10000^(2i/d_model))
PE(pos,2i+1): cos(pos / 10000^(2i/d_model))
```

---

## Running the Code

```bash
python transformer.py
```

This trains a small transformer on a toy task (reverse a sequence). You should see the loss decrease steadily:

```
Training on: mps
Epoch   1/ 50 | Loss: 3.2847
Epoch   5/ 50 | Loss: 1.8234
...
Epoch  50/ 50 | Loss: 0.4521

─── Evaluation ───
  Input:       [3, 7, 12, 5]
  Expected:    [5, 12, 7, 3]
  Predicted:   [1, 5, 12, 7, 3, 2]
```

The predicted output shows [<sos>, reversed tokens, <eos>], confirming the model learned to reverse sequences.
