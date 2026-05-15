"""
Transformer from Scratch — "Attention Is All You Need" (Vaswani et al., 2017)

Full encoder-decoder implementation in PyTorch, built component-by-component.
Run this file directly to train on a toy sequence-reversal task.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ─────────────────────────────────────────────
# 1. Input Embedding
# ─────────────────────────────────────────────

class InputEmbedding(nn.Module):
    """Maps token IDs to vectors of dimension d_model.

    The paper scales embeddings by sqrt(d_model) to keep their magnitude
    comparable to positional encodings (which are O(1) in magnitude).
    """

    def __init__(self, vocab_size: int, d_model: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.d_model = d_model

    def forward(self, x):
        # x: (batch, seq_len) of token IDs
        return self.embedding(x) * math.sqrt(self.d_model)


# ─────────────────────────────────────────────
# 2. Positional Encoding
# ─────────────────────────────────────────────

class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding from the paper (Section 3.5).

    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    These are added (not concatenated) to the input embeddings.
    """

    def __init__(self, d_model: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)  # (max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()  # (max_len, 1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )  # (d_model/2,)

        pe[:, 0::2] = torch.sin(position * div_term)  # even indices
        pe[:, 1::2] = torch.cos(position * div_term)  # odd indices
        pe = pe.unsqueeze(0)  # (1, max_len, d_model) for broadcasting

        self.register_buffer("pe", pe)

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


# ─────────────────────────────────────────────
# 3. Multi-Head Attention
# ─────────────────────────────────────────────

class MultiHeadAttention(nn.Module):
    """Multi-head scaled dot-product attention.

    Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

    The input is projected into h heads (each of dimension d_k = d_model / h),
    attention is computed independently per head, then the heads are concatenated
    and projected back to d_model.

    This single class handles all three attention types:
      - Encoder self-attention:  Q=K=V=encoder_output
      - Decoder self-attention:  Q=K=V=decoder_input (with causal mask)
      - Cross-attention:         Q=decoder, K=V=encoder_output
    """

    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # dimension per head

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        self.dropout = nn.Dropout(dropout)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """Compute attention scores and apply to values.

        Args:
            Q, K, V: (batch, heads, seq_len, d_k)
            mask:    (batch, 1, 1, seq_len) or (batch, 1, seq_len, seq_len)
        """
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        return torch.matmul(attention_weights, V), attention_weights

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        # 1) Linear projections: (batch, seq_len, d_model)
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)

        # 2) Reshape to (batch, num_heads, seq_len, d_k)
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # 3) Attention
        attn_output, attn_weights = self.scaled_dot_product_attention(Q, K, V, mask)

        # 4) Concatenate heads: (batch, seq_len, d_model)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        # 5) Final linear projection
        return self.W_o(attn_output)


# ─────────────────────────────────────────────
# 4. Feed-Forward Network
# ─────────────────────────────────────────────

class FeedForward(nn.Module):
    """Position-wise feed-forward network.

    FFN(x) = max(0, x @ W1 + b1) @ W2 + b2

    The inner dimension (d_ff) is typically 4x d_model.
    Applied independently to each position.
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.linear2(self.dropout(F.relu(self.linear1(x))))


# ─────────────────────────────────────────────
# 5. Add & Norm
# ─────────────────────────────────────────────

class AddNorm(nn.Module):
    """Residual connection followed by layer normalization.

    output = LayerNorm(x + sublayer(x))

    Residual connections allow gradients to flow directly through the network,
    enabling training of deeper models.
    """

    def __init__(self, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer_output):
        return self.norm(x + self.dropout(sublayer_output))


# ─────────────────────────────────────────────
# 6. Encoder Layer
# ─────────────────────────────────────────────

class EncoderLayer(nn.Module):
    """A single transformer encoder layer.

    Two sub-layers:
      1. Multi-head self-attention  (Q=K=V=encoder_input)
      2. Position-wise feed-forward network
    Each sub-layer has a residual connection + layer norm.
    """

    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.self_attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.add_norm1 = AddNorm(d_model, dropout)
        self.add_norm2 = AddNorm(d_model, dropout)

    def forward(self, x, src_mask=None):
        # Sub-layer 1: self-attention
        attn_output = self.self_attention(x, x, x, src_mask)
        x = self.add_norm1(x, attn_output)

        # Sub-layer 2: feed-forward
        ff_output = self.feed_forward(x)
        x = self.add_norm2(x, ff_output)

        return x


# ─────────────────────────────────────────────
# 7. Encoder
# ─────────────────────────────────────────────

class Encoder(nn.Module):
    """Stack of N encoder layers on top of embeddings + positional encoding."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        num_heads: int,
        d_ff: int,
        num_layers: int,
        max_len: int = 5000,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = InputEmbedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_len, dropout)
        self.layers = nn.ModuleList(
            [EncoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)]
        )

    def forward(self, x, src_mask=None):
        x = self.embedding(x)
        x = self.positional_encoding(x)
        for layer in self.layers:
            x = layer(x, src_mask)
        return x


# ─────────────────────────────────────────────
# 8. Decoder Layer
# ─────────────────────────────────────────────

class DecoderLayer(nn.Module):
    """A single transformer decoder layer.

    Three sub-layers:
      1. Masked multi-head self-attention  (Q=K=V=decoder_input, causal mask)
      2. Multi-head cross-attention        (Q=decoder, K=V=encoder_output)
      3. Position-wise feed-forward network
    Each sub-layer has a residual connection + layer norm.
    """

    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.self_attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.add_norm1 = AddNorm(d_model, dropout)
        self.add_norm2 = AddNorm(d_model, dropout)
        self.add_norm3 = AddNorm(d_model, dropout)

    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # Sub-layer 1: masked self-attention (prevents attending to future tokens)
        attn_output = self.self_attention(x, x, x, tgt_mask)
        x = self.add_norm1(x, attn_output)

        # Sub-layer 2: cross-attention (decoder attends to encoder output)
        cross_output = self.cross_attention(x, encoder_output, encoder_output, src_mask)
        x = self.add_norm2(x, cross_output)

        # Sub-layer 3: feed-forward
        ff_output = self.feed_forward(x)
        x = self.add_norm3(x, ff_output)

        return x


# ─────────────────────────────────────────────
# 9. Decoder
# ─────────────────────────────────────────────

class Decoder(nn.Module):
    """Stack of N decoder layers on top of embeddings + positional encoding."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        num_heads: int,
        d_ff: int,
        num_layers: int,
        max_len: int = 5000,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = InputEmbedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_len, dropout)
        self.layers = nn.ModuleList(
            [DecoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)]
        )

    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        x = self.embedding(x)
        x = self.positional_encoding(x)
        for layer in self.layers:
            x = layer(x, encoder_output, src_mask, tgt_mask)
        return x


# ─────────────────────────────────────────────
# 10. Full Transformer
# ─────────────────────────────────────────────

class Transformer(nn.Module):
    """Complete encoder-decoder transformer.

    Architecture:
      src_tokens → Encoder → encoder_output
      tgt_tokens + encoder_output → Decoder → decoder_output
      decoder_output → Linear(vocab_size) → logits
    """

    def __init__(
        self,
        src_vocab_size: int,
        tgt_vocab_size: int,
        d_model: int = 512,
        num_heads: int = 8,
        d_ff: int = 2048,
        num_encoder_layers: int = 6,
        num_decoder_layers: int = 6,
        max_len: int = 5000,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.encoder = Encoder(
            src_vocab_size, d_model, num_heads, d_ff, num_encoder_layers, max_len, dropout
        )
        self.decoder = Decoder(
            tgt_vocab_size, d_model, num_heads, d_ff, num_decoder_layers, max_len, dropout
        )
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)

    def encode(self, src, src_mask=None):
        return self.encoder(src, src_mask)

    def decode(self, tgt, encoder_output, src_mask=None, tgt_mask=None):
        return self.decoder(tgt, encoder_output, src_mask, tgt_mask)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        encoder_output = self.encode(src, src_mask)
        decoder_output = self.decode(tgt, encoder_output, src_mask, tgt_mask)
        logits = self.output_projection(decoder_output)
        return logits


# ─────────────────────────────────────────────
# 11. Masking Helpers
# ─────────────────────────────────────────────

def make_src_mask(src, pad_token_id=0):
    """Padding mask: prevents attention to padding tokens.

    Returns: (batch, 1, 1, src_len) — broadcastable over heads and query positions.
    """
    return (src != pad_token_id).unsqueeze(1).unsqueeze(2)


def make_tgt_mask(tgt, pad_token_id=0):
    """Combined padding + causal mask for the decoder.

    Causal mask ensures position i can only attend to positions <= i
    (prevents "cheating" by looking at future tokens during training).

    Returns: (batch, 1, tgt_len, tgt_len)
    """
    batch_size, tgt_len = tgt.size()

    # Padding mask: (batch, 1, 1, tgt_len)
    pad_mask = (tgt != pad_token_id).unsqueeze(1).unsqueeze(2)

    # Causal mask: (1, 1, tgt_len, tgt_len) — lower triangular
    causal_mask = torch.tril(torch.ones(tgt_len, tgt_len, device=tgt.device)).bool()
    causal_mask = causal_mask.unsqueeze(0).unsqueeze(0)

    # Both conditions must be true
    return pad_mask & causal_mask


# ─────────────────────────────────────────────
# 12. Toy Training Example
# ─────────────────────────────────────────────

def generate_reverse_data(num_samples=1000, seq_len=10, vocab_start=3):
    """Generate a toy dataset: reverse the input sequence.

    Special tokens:
      0 = <pad>
      1 = <sos> (start of sequence)
      2 = <eos> (end of sequence)
      3+ = data tokens

    Input:  [1, a, b, c, 2, 0, 0, ...]
    Target: [1, c, b, a, 2, 0, 0, ...]
    """
    data = torch.randint(vocab_start, vocab_start + 20, (num_samples, seq_len))
    src = torch.cat([torch.ones(num_samples, 1), data, 2 * torch.ones(num_samples, 1)], dim=1).long()
    tgt_input = torch.cat([torch.ones(num_samples, 1), data.flip(dims=[1]), 2 * torch.ones(num_samples, 1)], dim=1).long()
    # tgt_output is tgt_input shifted left by 1 (what we predict)
    tgt_output = tgt_input[:, 1:]
    tgt_input = tgt_input[:, :-1]
    return src, tgt_input, tgt_output


def train():
    """Train the transformer on a toy sequence reversal task."""
    # Hyperparameters (small for quick demo)
    VOCAB_SIZE = 25
    D_MODEL = 128
    NUM_HEADS = 4
    D_FF = 512
    NUM_LAYERS = 3
    DROPOUT = 0.1
    BATCH_SIZE = 64
    EPOCHS = 50
    LR = 1e-3

    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Training on: {device}")

    # Create dataset
    src, tgt_in, tgt_out = generate_reverse_data(num_samples=2000, seq_len=8, vocab_start=3)
    dataset = torch.utils.data.TensorDataset(src, tgt_in, tgt_out)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Build model
    model = Transformer(
        src_vocab_size=VOCAB_SIZE,
        tgt_vocab_size=VOCAB_SIZE,
        d_model=D_MODEL,
        num_heads=NUM_HEADS,
        d_ff=D_FF,
        num_encoder_layers=NUM_LAYERS,
        num_decoder_layers=NUM_LAYERS,
        dropout=DROPOUT,
    ).to(device)

    # Label smoothing loss from the paper
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1, ignore_index=0)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, betas=(0.9, 0.98), eps=1e-9)

    # Noam learning rate schedule (warmup then decay)
    def noam_schedule(step, d_model, warmup_steps=400):
        step = max(step, 1)
        return d_model ** (-0.5) * min(step ** (-0.5), step * warmup_steps ** (-1.5))

    model.train()
    step = 0
    for epoch in range(EPOCHS):
        total_loss = 0
        for batch_src, batch_tgt_in, batch_tgt_out in dataloader:
            batch_src = batch_src.to(device)
            batch_tgt_in = batch_tgt_in.to(device)
            batch_tgt_out = batch_tgt_out.to(device)

            # Apply learning rate schedule
            step += 1
            lr = noam_schedule(step, D_MODEL)
            for param_group in optimizer.param_groups:
                param_group["lr"] = lr

            # Forward pass
            src_mask = make_src_mask(batch_src)
            tgt_mask = make_tgt_mask(batch_tgt_in)
            logits = model(batch_src, batch_tgt_in, src_mask, tgt_mask)

            # Compute loss: reshape for cross-entropy
            loss = criterion(logits.reshape(-1, VOCAB_SIZE), batch_tgt_out.reshape(-1))

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:3d}/{EPOCHS} | Loss: {avg_loss:.4f}")

    # Quick evaluation: reverse a test sequence
    print("\n─── Evaluation ───")
    model.eval()
    with torch.no_grad():
        test_data = torch.tensor([[3, 7, 12, 5]])  # sequence to reverse
        test_src = torch.cat([torch.ones(1, 1), test_data, 2 * torch.ones(1, 1)], dim=1).long().to(device)

        # Greedy decoding (autoregressive)
        tgt_tokens = torch.ones(1, 1).long().to(device)  # start with <sos>
        for _ in range(12):
            src_mask = make_src_mask(test_src)
            tgt_mask = make_tgt_mask(tgt_tokens)
            logits = model(test_src, tgt_tokens, src_mask, tgt_mask)
            next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            tgt_tokens = torch.cat([tgt_tokens, next_token], dim=1)
            if next_token.item() == 2:  # <eos>
                break

        src_tokens = test_data[0].tolist()
        pred_tokens = tgt_tokens[0].cpu().tolist()
        print(f"  Input:       {src_tokens}")
        print(f"  Expected:    {list(reversed(src_tokens))}")
        print(f"  Predicted:   {pred_tokens}")


if __name__ == "__main__":
    train()
