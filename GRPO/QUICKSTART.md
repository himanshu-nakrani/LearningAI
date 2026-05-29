# Quickstart — run GRPO training on Modal

You should have already read `README.md` for the theory. This file is just commands.

## 1. One-time setup

```bash
# Install Modal client (Python 3.10+)
pip install modal

# Authenticate (opens a browser, ~30 sec)
modal token new

# Confirm you have credits
modal profile current
```

You should see your account with credit balance. We expect to burn about **$3-5** on training and **$1-2** on eval.

## 2. Sanity check — run the base-model eval first (~$0.30)

This confirms the Modal setup works AND gives you a baseline number to compare against.

```bash
cd /Users/himanshu/Git/LearningAI/GRPO

modal run eval.py --which base --n 50
```

Expected: ~5-15% accuracy. The model will probably mostly *not* use the `<think>`/`<answer>` format.

## 3. Train (~1.5-2 hours, ~$2-3)

```bash
modal run train_grpo.py
```

You'll see logs like:

```
{'loss': 0.012, 'reward': 0.15, 'reward_std': 0.18, 'kl': 0.001, ...}
```

What to watch:
- **`reward`** — should climb from ~0.2 (just format reward) toward ~0.6+ (format + correctness on some problems)
- **`reward_std`** — the spread *within a group*. If this collapses to near zero, all 8 completions are identical and GRPO can't learn — bump temperature.
- **`kl`** — should stay small (< 0.1ish). If it explodes, the policy is drifting too far from the reference; lower the LR or increase `beta`.

The checkpoint lands in the persistent Modal volume `grpo-checkpoints` at `/checkpoints/qwen-0.5b-grpo-gsm8k/`.

## 4. Eval the trained model (~$0.30)

```bash
modal run eval.py --n 100
```

This runs **both** base and trained on the same 100 problems and prints a summary. Hopefully you'll see a clear bump.

## 5. Iterate

Common things to try:
- More steps: edit `max_steps=300` → `500` in `train_grpo.py`
- Bigger group: `num_generations=8` → `16` (more memory, better baseline estimate)
- Different model: swap `MODEL_ID` to `Qwen/Qwen2.5-1.5B-Instruct` (needs L4 GPU instead of A10G)
- Custom reward: edit `rewards.py`, e.g. reward shorter answers, penalize repeated tokens, etc.

## Troubleshooting

| Problem | Fix |
|---|---|
| OOM on A10G | Drop `num_generations` to 4, or `max_completion_length` to 384 |
| `reward_std` collapses to 0 | Raise `temperature` to 1.0, or lower it if completions are gibberish |
| Loss explodes | Lower `learning_rate` (try 1e-6) |
| `KL` explodes | Raise `beta` (try 0.1) |
| Modal can't find `rewards.py` | Make sure you run from the `GRPO/` directory |

## Cost breakdown (estimated, A10G at $1.10/hr)

| Step | Time | Cost |
|---|---|---|
| Base eval (50 problems) | ~10 min | $0.20 |
| Training (300 steps) | ~90 min | $1.65 |
| Both-model eval (100 problems) | ~20 min | $0.40 |
| **Total** | **~2 hours** | **~$2.25** |

You have ~$25 of headroom for iteration. Suggested next experiments:
1. Train for 500 steps instead of 300 (~$1 more, check if accuracy keeps climbing)
2. Try Qwen 1.5B on L4 (~$3-5 for same step count, much better baseline)
3. Add a "concise answer" reward and see if completions shrink
