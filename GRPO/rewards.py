"""
Reward functions for GRPO training on GSM8K.

These get called by the trainer for every generated completion. Each function
takes a list of completions and returns a list of floats (rewards).

We use two rewards that get summed:
  1. correctness_reward — +1.0 if final answer matches ground truth, else 0
  2. format_reward      — +0.2 if the completion uses <think>/<answer> tags

Splitting the reward like this is a common GRPO trick: the format reward gives
the model a denser, easier-to-learn signal early in training (you don't have to
solve the problem to get *some* reward), and the correctness reward is the
actual goal.
"""

import re


# The model is taught (via the system prompt in train_grpo.py) to use this format:
#   <think>...reasoning here...</think>
#   <answer>42</answer>
ANSWER_PATTERN = re.compile(r"<answer>\s*(.*?)\s*</answer>", re.DOTALL)
THINK_PATTERN = re.compile(r"<think>.*?</think>\s*<answer>.*?</answer>", re.DOTALL)


def extract_answer(text: str) -> str | None:
    """Pull the content of the last <answer>...</answer> tag, if present."""
    matches = ANSWER_PATTERN.findall(text)
    if not matches:
        return None
    return matches[-1].strip()


def extract_gsm8k_answer(answer_text: str) -> str:
    """
    GSM8K ground-truth answers are formatted like:
        '...some reasoning...\n#### 42'
    Pull the number after the ####.
    """
    return answer_text.split("####")[-1].strip().replace(",", "")


def normalize_number(s: str) -> str | None:
    """Strip $, commas, and trailing punctuation; return None if not numeric."""
    s = s.strip().replace(",", "").replace("$", "").rstrip(".")
    try:
        # Accept "42", "42.0", "-3.14" etc. Normalize so "42.0" == "42".
        f = float(s)
        if f.is_integer():
            return str(int(f))
        return str(f)
    except ValueError:
        return None


def correctness_reward(prompts, completions, answer, **kwargs) -> list[float]:
    """
    +1.0 if the model's <answer> matches the ground-truth GSM8K answer.

    `completions` comes from TRL as a list of either strings or chat-format
    list-of-dicts depending on config; we handle both.
    `answer` is the ground-truth column from the dataset, one per prompt.
    """
    rewards = []
    for completion, gt in zip(completions, answer):
        # Handle both chat-format and plain string completions
        text = completion if isinstance(completion, str) else completion[0]["content"]

        predicted = extract_answer(text)
        if predicted is None:
            rewards.append(0.0)
            continue

        pred_num = normalize_number(predicted)
        gt_num = normalize_number(extract_gsm8k_answer(gt))

        if pred_num is None or gt_num is None:
            rewards.append(0.0)
        elif pred_num == gt_num:
            rewards.append(1.0)
        else:
            rewards.append(0.0)
    return rewards


def format_reward(prompts, completions, **kwargs) -> list[float]:
    """
    +0.2 if the completion has a well-formed <think>...</think><answer>...</answer>.

    This is a "shaping" reward — small, dense, helps the model learn the
    output format quickly so the correctness reward becomes reachable.
    """
    rewards = []
    for completion in completions:
        text = completion if isinstance(completion, str) else completion[0]["content"]
        rewards.append(0.2 if THINK_PATTERN.search(text) else 0.0)
    return rewards
