# GRPO from scratch — theory + hands-on training

You're going to train a 0.5B-parameter LLM to solve grade-school math problems using **GRPO** (Group Relative Policy Optimization), the algorithm DeepSeek used to train R1.

By the end you'll understand:
1. What RL is, in the LLM context
2. Why PPO was the standard, and what's annoying about it
3. What GRPO changes — and why that change is clever
4. How to actually run a GRPO training job

---

## Part 1 — RL for LLMs, the 30-second version

You already know **supervised fine-tuning (SFT)**: show the model input/output pairs, minimize cross-entropy. The model learns to imitate.

**RL fine-tuning** is different. You don't tell the model *what* to say. You let it generate something, then **score** it (high score = good, low score = bad), and update the model to make high-scoring outputs more likely.

The pieces:

| Term | Meaning in LLM-land |
|---|---|
| **Policy** $\pi_\theta$ | Your LLM. Given a prompt (state), it outputs token probabilities (actions). |
| **Trajectory** | A full generated sequence: prompt → token₁ → token₂ → ... → EOS |
| **Reward** $r$ | A scalar score for the whole trajectory. e.g. "did it get the math answer right?" |
| **Advantage** $A$ | How much better was this trajectory than expected? (Reward minus a baseline.) |

The **policy gradient** update — the foundational RL idea — is:

$$
\nabla_\theta J(\theta) = \mathbb{E}\Big[ A \cdot \nabla_\theta \log \pi_\theta(\text{trajectory}) \Big]
$$

In words: **increase the log-probability of good trajectories, decrease it for bad ones, weighted by how good/bad they were**. That's it. That's the whole game. Everything else (PPO, GRPO) is just refinements to make this stable in practice.

---

## Part 2 — Why we need a baseline (and the "value function" problem)

Look at the advantage $A = r - b$ where $b$ is some baseline.

Why subtract a baseline? Because if all rewards are positive (say, 0.1 to 1.0), every gradient pushes *up*. You'd just be amplifying everything. By subtracting a baseline (often the *expected* reward), you get: "this trajectory was **better than average** by X" — and only above-average trajectories get reinforced.

**Classic RL approach:** train a separate **value network** $V_\phi(s)$ that predicts expected reward from state $s$. Then $A = r - V_\phi(s)$. This is what **PPO** does.

The catch: that value network is **a second model the same size as your LLM**. For a 7B policy, you're training a 7B critic alongside it. Memory cost: 2x. Compute cost: significant. And the value network is hard to train well for LLMs because reward signals are sparse (one scalar per long sequence).

This is the pain point GRPO solves.

---

## Part 3 — PPO in one paragraph

PPO (Proximal Policy Optimization) adds two things on top of vanilla policy gradient:

1. **Clipping**: don't let the policy change too much in one step. Specifically, clip the *ratio* $\rho = \pi_\theta(a)/\pi_{\theta_{\text{old}}}(a)$ to $[1-\epsilon, 1+\epsilon]$. This prevents catastrophic updates.
2. **A value network** for the baseline (the part we just complained about).

PPO loss:

$$
L_{\text{PPO}} = \mathbb{E}\Big[ \min\big(\rho \cdot A, \; \text{clip}(\rho, 1-\epsilon, 1+\epsilon) \cdot A\big) \Big]
$$

PPO works. It's what trained ChatGPT. But the value network is expensive.

---

## Part 4 — GRPO's clever trick

**Insight:** instead of training a value network to estimate "expected reward from this state," just **sample multiple completions for the same prompt and use their mean as the baseline**.

Concretely, for each prompt:
1. Generate $G$ completions (typically G = 4, 8, or 16) with the current policy.
2. Score each: $r_1, r_2, \ldots, r_G$.
3. Compute group-relative advantage for completion $i$:

$$
A_i = \frac{r_i - \text{mean}(r_1, \ldots, r_G)}{\text{std}(r_1, \ldots, r_G)}
$$

That's it. **No value network.** The other completions in the group serve as the baseline. Completions that scored above the group average get positive advantage; below-average ones get negative.

Then plug $A_i$ into the PPO clipped objective, plus a KL penalty against a reference model (to prevent the policy from drifting too far from the original):

$$
L_{\text{GRPO}} = \mathbb{E}\Big[ \min(\rho \cdot A, \; \text{clip}(\rho, 1-\epsilon, 1+\epsilon) \cdot A) \Big] - \beta \cdot \text{KL}\big(\pi_\theta \,\|\, \pi_{\text{ref}}\big)
$$

### Why this is great for LLMs

- **Memory:** drop the value network → halve the GPU memory needed.
- **Stability:** the baseline is computed from *actual rollouts*, not a learned estimator that might be wrong.
- **Verifiable rewards:** works beautifully when reward is computed by a programmatic checker (e.g., "is the answer correct?") rather than a learned reward model.

This last point is why GRPO took off for math/code: you don't need a reward model at all. You just check the answer.

---

## Part 5 — What we're going to train

**Setup:**
- Model: `Qwen/Qwen2.5-0.5B-Instruct` (small enough to fit + iterate on an A10G)
- Dataset: **GSM8K** — 8.5K grade-school math word problems with verified answers
- Reward function: two parts
  - **Correctness reward** (+1.0 if the final numeric answer matches, else 0)
  - **Format reward** (+0.2 if the model wraps reasoning in `<think>...</think>` and answer in `<answer>...</answer>`)
- Group size G = 8 (generate 8 attempts per problem)
- ~300 training steps on an A10G ≈ **1-2 hours, ~$2**

### What we expect to see

The base 0.5B model gets maybe 5-15% on GSM8K (it's tiny). After GRPO, we hope to see:
- Accuracy bump (maybe to 25-40%)
- The model learning to use the `<think>`/`<answer>` format
- Longer reasoning chains over time (the famous "thinking gets longer" pattern)

It's a small model so don't expect miracles — the point is to **see GRPO actually working** and understand every piece.

---

## Part 6 — Run it

See [`QUICKSTART.md`](QUICKSTART.md) for the actual commands. The training code lives in [`train_grpo.py`](train_grpo.py) with comments explaining each piece. Eval in [`eval.py`](eval.py).

### Files

- `README.md` — this file (theory)
- `QUICKSTART.md` — commands to run
- `train_grpo.py` — Modal app that runs GRPO training
- `eval.py` — Modal app that benchmarks base vs trained
- `rewards.py` — the reward functions (correctness + format)

---

## Glossary cheat-sheet

- **Rollout / completion**: one generated sequence from the model.
- **Group**: the G completions for the same prompt — GRPO's key innovation.
- **KL divergence**: distance between two probability distributions. Used to keep the new policy close to the original ("don't change too much").
- **Reference model**: a frozen copy of the original model. The KL penalty measures distance from *this*.
- **Old policy** vs **new policy**: in PPO/GRPO you generate with the policy at step N (old), then do several gradient steps on that data updating the policy (new). The ratio $\rho$ tracks how much it's changed.

---

## References for after you've finished this

- DeepSeekMath paper (introduces GRPO): https://arxiv.org/abs/2402.03300
- DeepSeek-R1 paper (scales GRPO to reasoning): https://arxiv.org/abs/2501.12948
- TRL library's GRPOTrainer: https://huggingface.co/docs/trl/grpo_trainer
