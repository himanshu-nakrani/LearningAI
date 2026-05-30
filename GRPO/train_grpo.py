"""
GRPO training on GSM8K with Qwen2.5-0.5B-Instruct, running on Modal.

What this does, top to bottom:
  1. Define a Modal container image with torch + transformers + trl + datasets
  2. Mount a persistent volume to save checkpoints
  3. On GPU (A10G), load Qwen 0.5B, load GSM8K, configure GRPO, train
  4. Save the trained LoRA adapter (and merged model) to the volume

Why LoRA? GRPO keeps a frozen reference model in memory in addition to the
policy. With LoRA, the "reference" is just the base model (LoRA disabled) and
the "policy" is the same base model with LoRA enabled — one set of weights
instead of two. Big memory win on a 24GB A10G.

Run:  modal run train_grpo.py
"""

import modal

# ──────────────────────────────────────────────────────────────────────────────
# Modal setup
# ──────────────────────────────────────────────────────────────────────────────

# Pin versions so this doesn't bit-rot under you. trl 0.14+ has GRPOTrainer.
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.5.1",
        "transformers==4.50.0",
        "trl>=0.15.0",
        "datasets==3.2.0",
        "accelerate==1.2.1",
        "peft==0.14.0",
        "bitsandbytes==0.45.0",
        "wandb==0.19.1",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .pip_install("hf_transfer==0.1.8")
    # Bring our reward functions into the image
    .add_local_python_source("rewards")
)

app = modal.App("grpo-gsm8k", image=image)

# Persistent volume — checkpoints survive across runs so eval.py can find them.
volume = modal.Volume.from_name("grpo-checkpoints", create_if_missing=True)
VOL_PATH = "/checkpoints"

# HF cache volume so we don't re-download the model on every run.
hf_cache = modal.Volume.from_name("hf-cache", create_if_missing=True)
HF_CACHE_PATH = "/root/.cache/huggingface"


# ──────────────────────────────────────────────────────────────────────────────
# The training function
# ──────────────────────────────────────────────────────────────────────────────

@app.function(
    gpu="A10G",                # ~$1.10/hr, 24GB VRAM — fits 0.5B + LoRA + ref
    timeout=60 * 60 * 3,       # 3 hour cap
    volumes={VOL_PATH: volume, HF_CACHE_PATH: hf_cache},
)
def train():
    import torch
    from datasets import load_dataset
    from peft import LoraConfig
    from transformers import AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    from rewards import correctness_reward, format_reward

    MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
    OUTPUT_DIR = f"{VOL_PATH}/qwen-0.5b-grpo-gsm8k"

    # ─────────────────────────────────────────────────────────
    # 1. Load + format the dataset
    # ─────────────────────────────────────────────────────────
    # GSM8K columns: 'question' (the math problem), 'answer' (reasoning + '#### N')
    print("Loading GSM8K...")
    raw = load_dataset("openai/gsm8k", "main", split="train")

    # The system prompt teaches the model to use <think>/<answer> tags.
    # GRPO will reward whichever completions actually follow this format
    # AND get the math right.
    SYSTEM = (
        "You are a helpful math assistant. Solve the problem step by step. "
        "Put your reasoning inside <think>...</think> tags. "
        "Put the final numerical answer inside <answer>...</answer> tags."
    )

    def to_chat(example):
        return {
            "prompt": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": example["question"]},
            ],
            "answer": example["answer"],  # keep raw GT for the reward fn
        }

    dataset = raw.map(to_chat, remove_columns=raw.column_names)
    print(f"Dataset size: {len(dataset)}")

    # ─────────────────────────────────────────────────────────
    # 2. Tokenizer + LoRA config
    # ─────────────────────────────────────────────────────────
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    # LoRA on attention projections — standard recipe, small footprint.
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    # ─────────────────────────────────────────────────────────
    # 3. GRPO config — the interesting knobs
    # ─────────────────────────────────────────────────────────
    grpo_config = GRPOConfig(
        output_dir=OUTPUT_DIR,

        # The group: how many completions to sample per prompt.
        # The whole GRPO advantage trick relies on having multiple samples
        # to compute a mean/std baseline. 8 is the standard choice.
        num_generations=8,

        # Generation params — temperature must be > 0 so the group has diversity
        # (otherwise all 8 completions are identical → std=0 → no signal).
        temperature=0.9,
        max_prompt_length=256,
        max_completion_length=512,

        # KL penalty — keeps the policy from drifting too far from the
        # reference (base) model. Higher = more conservative.
        beta=0.04,

        # PPO-style clipping range for the ratio.
        # epsilon=0.2,  # this is the default in TRL

        # Training schedule — small for a tutorial. Bump to ~500 for better results.
        max_steps=300,
        per_device_train_batch_size=2,     # 2 prompts × 8 generations = 16 sequences
        gradient_accumulation_steps=4,     # effective batch = 8 prompts
        learning_rate=5e-6,                # RL likes small LRs
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        weight_decay=0.01,
        max_grad_norm=1.0,

        # Memory / speed
        bf16=True,
        gradient_checkpointing=False,
        logging_steps=5,
        save_steps=100,
        save_total_limit=2,

        report_to="none",  # set to "wandb" if you have it configured
        remove_unused_columns=False,  # we need the 'answer' column for rewards!
    )

    # ─────────────────────────────────────────────────────────
    # 4. Build the trainer and go
    # ─────────────────────────────────────────────────────────
    print("Initializing GRPOTrainer...")
    trainer = GRPOTrainer(
        model=MODEL_ID,
        # Pass BOTH reward functions — TRL will sum them.
        reward_funcs=[correctness_reward, format_reward],
        args=grpo_config,
        train_dataset=dataset,
        peft_config=peft_config,
    )

    print("Training...")
    trainer.train()

    # ─────────────────────────────────────────────────────────
    # 5. Save final adapter + merged model
    # ─────────────────────────────────────────────────────────
    print("Saving final model...")
    trainer.save_model(OUTPUT_DIR)

    # Also save a merged (LoRA folded back into base weights) version for
    # easy loading at eval time. ~1GB on disk for 0.5B model.
    merged_dir = f"{OUTPUT_DIR}/merged"
    merged = trainer.model.merge_and_unload()
    merged.save_pretrained(merged_dir, safe_serialization=True)
    tokenizer.save_pretrained(merged_dir)

    volume.commit()
    print(f"Done. Model saved to {OUTPUT_DIR}")


@app.local_entrypoint()
def main():
    train.remote()
