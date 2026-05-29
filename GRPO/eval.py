"""
Before/after eval on GSM8K test set.

Runs the base Qwen2.5-0.5B-Instruct AND the GRPO-trained model on the same
N test problems and prints accuracy + sample outputs side by side.

Run:  modal run eval.py
      modal run eval.py --n 50           # how many problems
      modal run eval.py --which base     # only eval one of them
"""

import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.5.1",
        "transformers==4.48.0",
        "datasets==3.2.0",
        "accelerate==1.2.1",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .pip_install("hf_transfer==0.1.8")
    .add_local_python_source("rewards")
)

app = modal.App("grpo-eval", image=image)

volume = modal.Volume.from_name("grpo-checkpoints", create_if_missing=True)
VOL_PATH = "/checkpoints"
hf_cache = modal.Volume.from_name("hf-cache", create_if_missing=True)
HF_CACHE_PATH = "/root/.cache/huggingface"

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
TRAINED_MODEL = f"{VOL_PATH}/qwen-0.5b-grpo-gsm8k/merged"

SYSTEM = (
    "You are a helpful math assistant. Solve the problem step by step. "
    "Put your reasoning inside <think>...</think> tags. "
    "Put the final numerical answer inside <answer>...</answer> tags."
)


def run_eval(model_id: str, label: str, n: int):
    """Evaluate one model on N GSM8K test problems. Returns accuracy + samples."""
    import torch
    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from rewards import extract_answer, extract_gsm8k_answer, normalize_number

    print(f"\n{'=' * 60}\nEvaluating: {label} ({model_id})\n{'=' * 60}")

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map="cuda"
    )
    model.eval()

    test = load_dataset("openai/gsm8k", "main", split="test").select(range(n))

    correct = 0
    samples = []  # save a few for printing

    for i, ex in enumerate(test):
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": ex["question"]},
        ]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,           # greedy for reproducible eval
                pad_token_id=tokenizer.eos_token_id,
            )
        completion = tokenizer.decode(
            out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True
        )

        predicted = extract_answer(completion)
        pred_num = normalize_number(predicted) if predicted else None
        gt_num = normalize_number(extract_gsm8k_answer(ex["answer"]))
        is_correct = pred_num is not None and pred_num == gt_num
        if is_correct:
            correct += 1

        if i < 3:  # save first 3 as samples
            samples.append({
                "question": ex["question"],
                "completion": completion,
                "predicted": pred_num,
                "ground_truth": gt_num,
                "correct": is_correct,
            })

        if (i + 1) % 10 == 0:
            print(f"  [{i + 1}/{n}] running accuracy: {correct / (i + 1):.1%}")

    acc = correct / n
    print(f"\n{label} accuracy: {correct}/{n} = {acc:.1%}\n")

    print(f"--- Sample outputs from {label} ---")
    for s in samples:
        print(f"\nQ: {s['question'][:150]}...")
        print(f"Completion: {s['completion'][:400]}")
        print(f"Predicted: {s['predicted']}  |  Truth: {s['ground_truth']}  |  ✓: {s['correct']}")

    # Free GPU before next model
    del model
    torch.cuda.empty_cache()

    return acc, samples


@app.function(
    gpu="A10G",
    timeout=60 * 60,
    volumes={VOL_PATH: volume, HF_CACHE_PATH: hf_cache},
)
def evaluate(n: int = 100, which: str = "both"):
    results = {}
    if which in ("base", "both"):
        results["base"] = run_eval(BASE_MODEL, "BASE (untrained)", n)[0]
    if which in ("trained", "both"):
        results["trained"] = run_eval(TRAINED_MODEL, "TRAINED (GRPO)", n)[0]

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for k, v in results.items():
        print(f"  {k:>8}: {v:.1%}")
    if "base" in results and "trained" in results:
        delta = results["trained"] - results["base"]
        print(f"  {'Δ':>8}: {delta:+.1%}")


@app.local_entrypoint()
def main(n: int = 100, which: str = "both"):
    """which: 'base', 'trained', or 'both'"""
    evaluate.remote(n=n, which=which)
