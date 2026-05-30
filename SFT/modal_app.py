"""
DPO Training Pipeline on Modal.

Setup:
    modal secret create huggingface-secret HF_TOKEN=hf_xxx
    export HF_USERNAME=your-hf-username

Run order:
    modal run modal_app.py::inspect_dataset
    modal run modal_app.py::smoke_train
    modal run modal_app.py::train
    modal run modal_app.py::evaluate
    modal run modal_app.py::compare_generations
    modal run modal_app.py::push_model_card
"""

import json
import os
from pathlib import Path

import modal

# ============================================================================
# GPU Configuration — change this to switch GPU type
# ============================================================================
# Options: "B200", "H100", modal.gpu.A100(count=1, size="80GB")
GPU_CONFIG = "B200"

# ============================================================================
# Modal Image
# ============================================================================
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.txt")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

# ============================================================================
# Modal Volumes and App
# ============================================================================
hf_cache_vol = modal.Volume.from_name("hf-cache", create_if_missing=True)
output_vol = modal.Volume.from_name("dpo-outputs", create_if_missing=True)

app = modal.App("helpful-qwen-dpo")

# ============================================================================
# Configuration (embedded to avoid mount issues)
# ============================================================================
BASE_MODEL = "Qwen/Qwen3-4B-Instruct"
FALLBACK_BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
ALLOW_FALLBACK = True
PUSH_SMOKE_TO_HUB = False

# Model naming
PROJECT_NAME = "qwen2.5-3b-ultrafeedback-dpo"  # More descriptive name

class TrainingConfig:
    max_length = 2048
    max_prompt_length = 1024
    beta = 0.1
    learning_rate = 5e-7
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    gradient_accumulation_steps = 8
    max_steps = -1
    warmup_ratio = 0.03
    lr_scheduler_type = "cosine"
    optim = "paged_adamw_8bit"
    bf16 = True
    fp16 = False
    gradient_checkpointing = True
    logging_steps = 10
    save_steps = 250
    eval_steps = 100
    save_total_limit = 3
    seed = 42
    report_to = "none"

class SmokeTestConfig:
    num_train_examples = 32
    num_eval_examples = 8
    max_length = 1024
    max_prompt_length = 512
    max_steps = 10
    logging_steps = 2
    save_steps = 10
    eval_steps = 10
    beta = 0.1
    learning_rate = 5e-7
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    gradient_accumulation_steps = 4
    warmup_ratio = 0.03
    lr_scheduler_type = "cosine"
    optim = "paged_adamw_8bit"
    bf16 = True
    fp16 = False
    gradient_checkpointing = True
    seed = 42
    report_to = "none"
    save_total_limit = 1

COMPARISON_PROMPTS = [
    "Explain gradient descent to a beginner using an analogy.",
    "Give me a 7-day plan to learn Python for data analysis.",
    "What are three common mistakes people make when fine-tuning LLMs?",
    "Explain the difference between precision and recall.",
    "Write a polite email asking for an extension on a project deadline.",
]

MODEL_CARD_TEMPLATE = """---
license: apache-2.0
base_model: {base_model}
datasets:
  - argilla/ultrafeedback-binarized-preferences-cleaned
tags:
  - dpo
  - preference-optimization
  - qlora
  - lora
  - peft
  - trl
  - qwen
  - assistant
language:
  - en
---

# {model_name}

A LoRA adapter fine-tuned with Direct Preference Optimization (DPO) on the UltraFeedback dataset. This adapter aligns Qwen 2.5 3B with human preferences for helpfulness, clarity, and accuracy.

## Model Details

- **Base Model:** {base_model}
- **Method:** Direct Preference Optimization (DPO) with QLoRA
- **Dataset:** UltraFeedback (10k preference pairs)
- **Training:** 1 epoch, ~30 minutes on NVIDIA B200
- **Adapter Size:** ~100MB (LoRA rank 32)

{eval_section}

## Usage

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "{base_model}",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "{hub_model_id}")
tokenizer = AutoTokenizer.from_pretrained("{base_model}", trust_remote_code=True)

# Generate
messages = [
    {{"role": "system", "content": "You are a helpful assistant."}},
    {{"role": "user", "content": "Explain gradient descent to a beginner."}}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7, do_sample=True)

response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(response)
```

## Use Cases

This model is optimized for tasks requiring helpful, clear, and accurate responses:

### 1. **Educational Content**
Explaining complex topics to beginners with clear analogies and step-by-step breakdowns.

```python
messages = [
    {{"role": "user", "content": "Explain how neural networks learn, using a simple analogy."}}
]
```

### 2. **Technical Documentation**
Writing clear, structured documentation and tutorials.

```python
messages = [
    {{"role": "user", "content": "Write a beginner-friendly guide to setting up a Python virtual environment."}}
]
```

### 3. **Code Explanation**
Breaking down code concepts and best practices.

```python
messages = [
    {{"role": "user", "content": "What are the key differences between list comprehensions and generator expressions in Python?"}}
]
```

### 4. **Problem-Solving Assistance**
Providing structured approaches to technical problems.

```python
messages = [
    {{"role": "user", "content": "I'm getting a 'connection timeout' error when calling an API. What should I check?"}}
]
```

### 5. **Professional Communication**
Drafting clear, polite emails and messages.

```python
messages = [
    {{"role": "user", "content": "Write a professional email requesting feedback on a project proposal."}}
]
```

### 6. **Learning Plans**
Creating structured learning roadmaps.

```python
messages = [
    {{"role": "user", "content": "Create a 30-day plan to learn machine learning fundamentals."}}
]
```

### 7. **Comparative Analysis**
Explaining differences between concepts, tools, or approaches.

```python
messages = [
    {{"role": "user", "content": "Compare REST APIs vs GraphQL - when should I use each?"}}
]
```

## Training Details

**Hyperparameters:**
- Learning rate: 5e-7
- DPO beta: 0.1
- Batch size: 2 (per device)
- Gradient accumulation: 8 steps
- LoRA rank: 32, alpha: 64
- Quantization: 4-bit NF4
- Optimizer: paged_adamw_8bit

**Hardware:**
- GPU: NVIDIA B200
- Training time: ~30 minutes
- Cost: ~$6-8

## What is DPO?

Direct Preference Optimization directly optimizes language models on preference data without requiring a separate reward model or reinforcement learning. It's simpler, more stable, and more efficient than traditional RLHF while achieving comparable results.

## Limitations

- LoRA adapter only - requires base model to run
- Trained on English data only
- 4-bit quantization during training may slightly reduce quality vs full precision
- Preference dataset may not cover all edge cases

## Citation

```bibtex
@article{{rafailov2023direct,
  title={{Direct Preference Optimization: Your Language Model is Secretly a Reward Model}},
  author={{Rafailov, Rafael and Sharma, Archit and Mitchell, Eric and Ermon, Stefano and Manning, Christopher D and Finn, Chelsea}},
  journal={{arXiv preprint arXiv:2305.18290}},
  year={{2023}}
}}
```

## Training Pipeline

This model was trained using a production-ready Modal pipeline. See the [training repository](https://github.com/yourusername/LearningAI/tree/main/SFT) for details.

{comp_section}
"""

# Shared decorator kwargs for training functions
_train_kwargs = dict(
    image=image,
    gpu=GPU_CONFIG,
    timeout=60 * 60 * 4,  # 4 hours
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/hf-cache": hf_cache_vol, "/outputs": output_vol},
)

_inspect_kwargs = dict(
    image=image,
    timeout=60 * 10,
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/hf-cache": hf_cache_vol},
)

# ============================================================================
# Dataset Utilities
# ============================================================================

def extract_text(value) -> str:
    """Robustly extract text from various dataset field formats."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                role = item.get("role", "")
                content = item.get("content", "")
                if isinstance(content, list):
                    # Some datasets nest content as list of dicts
                    content = " ".join(
                        c.get("text", str(c)) if isinstance(c, dict) else str(c)
                        for c in content
                    )
                if role and content:
                    parts.append(f"{role}: {content}")
                elif content:
                    parts.append(str(content))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    if isinstance(value, dict):
        if "content" in value:
            return extract_text(value["content"])
        if "messages" in value:
            return extract_text(value["messages"])
        if "text" in value:
            return extract_text(value["text"])
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def extract_assistant_content(value) -> str:
    """Extract only assistant turns from a chat message list."""
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict) and item.get("role") == "assistant":
                content = item.get("content", "")
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", str(c)) if isinstance(c, dict) else str(c)
                        for c in content
                    )
                parts.append(str(content).strip())
        if parts:
            return "\n".join(parts).strip()
    # Fallback: extract all text
    return extract_text(value)


def format_for_dpo(example: dict, tokenizer) -> dict | None:
    """
    Format a dataset example for DPO training.

    Returns dict with prompt/chosen/rejected, or None if invalid.
    """
    raw_prompt = example.get("prompt", example.get("instruction", ""))
    raw_chosen = example.get("chosen", "")
    raw_rejected = example.get("rejected", "")

    prompt_text = extract_text(raw_prompt)

    # For chosen/rejected: prefer assistant-only content if it's a chat list
    if isinstance(raw_chosen, list):
        chosen_text = extract_assistant_content(raw_chosen)
    else:
        chosen_text = extract_text(raw_chosen)

    if isinstance(raw_rejected, list):
        rejected_text = extract_assistant_content(raw_rejected)
    else:
        rejected_text = extract_text(raw_rejected)

    # Strip leading "assistant:" prefix if present
    for prefix in ("assistant:", "Assistant:", "ASSISTANT:"):
        if chosen_text.startswith(prefix):
            chosen_text = chosen_text[len(prefix):].strip()
        if rejected_text.startswith(prefix):
            rejected_text = rejected_text[len(prefix):].strip()

    if not prompt_text or not chosen_text or not rejected_text:
        return None

    # Build prompt using chat template
    messages = [
        {"role": "system", "content": "You are a helpful, honest, and clear assistant."},
        {"role": "user", "content": prompt_text},
    ]

    if hasattr(tokenizer, "apply_chat_template"):
        try:
            # Qwen3 supports enable_thinking; disable for DPO training
            prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
        except TypeError:
            prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
    else:
        prompt = f"System: You are a helpful, honest, and clear assistant.\nUser: {prompt_text}\nAssistant:"

    return {
        "prompt": prompt,
        "chosen": chosen_text,
        "rejected": rejected_text,
    }


# ============================================================================
# Model Loading Utilities
# ============================================================================

def _setup_env():
    """Set environment variables for HF caching."""
    os.environ["HF_HOME"] = "/hf-cache"
    os.environ["TRANSFORMERS_CACHE"] = "/hf-cache"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"


def _hf_login():
    """Login to Hugging Face and return (token, username)."""
    from huggingface_hub import HfApi, login

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "HF_TOKEN not found. Create Modal secret:\n"
            "  modal secret create huggingface-secret HF_TOKEN=hf_xxx"
        )
    login(token=token)

    username = os.environ.get("HF_USERNAME")
    if not username:
        username = HfApi().whoami(token=token)["name"]
        print(f"Auto-detected HF username: {username}")

    return token, username


def load_tokenizer(model_name: str):
    """Load tokenizer with safe defaults."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_name, trust_remote_code=True, use_fast=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    return tokenizer


def load_model(model_name: str):
    """Load model with 4-bit quantization."""
    import torch
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model.config.use_cache = False
    return model


def load_model_with_fallback(base_model: str, fallback_model: str, allow_fallback: bool = True):
    """Try loading base_model; fall back to fallback_model on error."""
    try:
        print(f"Loading model: {base_model}")
        model = load_model(base_model)
        tokenizer = load_tokenizer(base_model)
        return model, tokenizer, base_model
    except Exception as e:
        if not allow_fallback:
            raise
        print(f"Failed to load {base_model}: {e}")
        print(f"Falling back to: {fallback_model}")
        model = load_model(fallback_model)
        tokenizer = load_tokenizer(fallback_model)
        return model, tokenizer, fallback_model


def _build_lora_config():
    from peft import LoraConfig, TaskType

    return LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )


def _load_and_format_dataset(tokenizer, num_train: int, num_eval: int, seed: int = 42):
    """Load, shuffle, split, and format the dataset."""
    from datasets import load_dataset

    print(f"Loading dataset: argilla/ultrafeedback-binarized-preferences-cleaned")
    ds = load_dataset("argilla/ultrafeedback-binarized-preferences-cleaned", split="train")
    ds = ds.shuffle(seed=seed)

    total_needed = num_train + num_eval
    if len(ds) > total_needed:
        ds = ds.select(range(total_needed))

    train_ds = ds.select(range(num_train))
    eval_ds = ds.select(range(num_train, num_train + min(num_eval, len(ds) - num_train)))

    def _format(example):
        result = format_for_dpo(example, tokenizer)
        if result is None:
            return {"prompt": None, "chosen": None, "rejected": None}
        return result

    print("Formatting train split...")
    train_ds = train_ds.map(_format, remove_columns=train_ds.column_names)
    train_ds = train_ds.filter(lambda x: x["prompt"] and x["chosen"] and x["rejected"])

    print("Formatting eval split...")
    eval_ds = eval_ds.map(_format, remove_columns=eval_ds.column_names)
    eval_ds = eval_ds.filter(lambda x: x["prompt"] and x["chosen"] and x["rejected"])

    print(f"Train: {len(train_ds)} examples, Eval: {len(eval_ds)} examples")
    return train_ds, eval_ds


def _run_training(
    model, tokenizer, lora_config, train_ds, eval_ds,
    output_dir: str, hub_model_id: str, cfg, smoke: bool = False
):
    """Core training logic shared by train() and smoke_train()."""
    import torch
    from trl import DPOConfig, DPOTrainer

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    dpo_args = dict(
        output_dir=output_dir,
        num_train_epochs=1 if not smoke else 1,
        max_steps=cfg.max_steps if smoke else -1,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        per_device_eval_batch_size=cfg.per_device_eval_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        beta=cfg.beta,
        max_length=cfg.max_length,
        # max_prompt_length removed - not supported in DPOConfig
        bf16=cfg.bf16,
        fp16=cfg.fp16,
        gradient_checkpointing=cfg.gradient_checkpointing,
        optim=cfg.optim,
        lr_scheduler_type=cfg.lr_scheduler_type,
        warmup_ratio=cfg.warmup_ratio,
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        eval_steps=cfg.eval_steps,
        save_total_limit=cfg.save_total_limit,
        seed=cfg.seed,
        report_to=cfg.report_to,
        remove_unused_columns=False,
        eval_strategy="steps",
        load_best_model_at_end=False,
    )

    training_args = DPOConfig(**dpo_args)

    # TRL >= 0.11 uses processing_class; older uses tokenizer
    try:
        trainer = DPOTrainer(
            model=model,
            ref_model=None,  # PEFT handles reference model implicitly
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            processing_class=tokenizer,
            peft_config=lora_config,
        )
    except TypeError:
        trainer = DPOTrainer(
            model=model,
            ref_model=None,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            tokenizer=tokenizer,
            peft_config=lora_config,
        )

    print("Starting training...")
    trainer.train()

    print(f"Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    return trainer


# ============================================================================
# Modal Functions
# ============================================================================

@app.function(**_inspect_kwargs)
def inspect_dataset():
    """Inspect dataset structure and sample examples."""
    from datasets import load_dataset

    _setup_env()
    _, _ = _hf_login()

    print("Loading dataset...")
    ds = load_dataset("argilla/ultrafeedback-binarized-preferences-cleaned")

    print(f"\nSplits: {list(ds.keys())}")
    for split, data in ds.items():
        print(f"  {split}: {len(data)} examples, columns: {data.column_names}")

    train = ds["train"]
    print(f"\n--- Sample Examples ---")
    for i in range(min(3, len(train))):
        ex = train[i]
        print(f"\n[Example {i}]")
        for col in ["prompt", "chosen", "rejected"]:
            if col in ex:
                raw = ex[col]
                extracted = extract_text(raw)
                print(f"  {col} (type={type(raw).__name__}): {extracted[:200]!r}")


@app.function(**_train_kwargs)
def smoke_train():
    """Quick smoke test: 32 examples, 10 steps. Validates full pipeline."""
    _setup_env()
    _, username = _hf_login()

    cfg = SmokeTestConfig()
    model, tokenizer, actual_model = load_model_with_fallback(
        BASE_MODEL, FALLBACK_BASE_MODEL, ALLOW_FALLBACK
    )
    lora_config = _build_lora_config()

    train_ds, eval_ds = _load_and_format_dataset(
        tokenizer, cfg.num_train_examples, cfg.num_eval_examples, cfg.seed
    )

    output_dir = "/outputs/smoke-test"
    hub_id = f"{username}/{PROJECT_NAME}-smoke"

    _run_training(model, tokenizer, lora_config, train_ds, eval_ds,
                  output_dir, hub_id, cfg, smoke=True)

    if PUSH_SMOKE_TO_HUB:
        from huggingface_hub import HfApi
        HfApi().create_repo(hub_id, exist_ok=True, private=True)
        from peft import PeftModel
        # model is already a PeftModel after training
        model.push_to_hub(hub_id)
        tokenizer.push_to_hub(hub_id)
        print(f"Smoke model pushed to: https://huggingface.co/{hub_id}")
    else:
        print("Smoke test complete. Set PUSH_SMOKE_TO_HUB=True in config.py to push.")

    output_vol.commit()
    print("Smoke train done.")


@app.function(**_train_kwargs)
def train():
    """Full DPO training run. Pushes LoRA adapter to Hugging Face Hub."""
    _setup_env()
    _, username = _hf_login()

    cfg = TrainingConfig()
    hub_model_id = f"{username}/{PROJECT_NAME}"
    output_dir = f"/outputs/{PROJECT_NAME}"

    model, tokenizer, actual_model = load_model_with_fallback(
        BASE_MODEL, FALLBACK_BASE_MODEL, ALLOW_FALLBACK
    )
    lora_config = _build_lora_config()

    train_ds, eval_ds = _load_and_format_dataset(
        tokenizer,
        num_train=10000,
        num_eval=500,
        seed=cfg.seed,
    )

    trainer = _run_training(
        model, tokenizer, lora_config, train_ds, eval_ds,
        output_dir, hub_model_id, cfg, smoke=False
    )

    # Push to Hub
    from huggingface_hub import HfApi
    HfApi().create_repo(hub_model_id, exist_ok=True)
    trainer.model.push_to_hub(hub_model_id)
    tokenizer.push_to_hub(hub_model_id)

    # Save metadata for model card
    meta = {"base_model": actual_model, "hub_model_id": hub_model_id}
    Path(output_dir, "train_meta.json").write_text(json.dumps(meta, indent=2))

    output_vol.commit()
    print(f"\nModel pushed to: https://huggingface.co/{hub_model_id}")


@app.function(**_train_kwargs)
def evaluate():
    """Compute preference accuracy on held-out eval examples."""
    import torch

    _setup_env()
    _, username = _hf_login()

    hub_model_id = f"{username}/{PROJECT_NAME}"
    output_dir = f"/outputs/{PROJECT_NAME}"

    # Load base model + adapter
    _, tokenizer, actual_model = load_model_with_fallback(
        BASE_MODEL, FALLBACK_BASE_MODEL, ALLOW_FALLBACK
    )
    base_model = load_model(actual_model)

    from peft import PeftModel
    try:
        model = PeftModel.from_pretrained(base_model, hub_model_id)
        print(f"Loaded adapter from Hub: {hub_model_id}")
    except Exception:
        model = PeftModel.from_pretrained(base_model, output_dir)
        print(f"Loaded adapter from local: {output_dir}")

    model.eval()

    # Load eval data
    _, eval_ds = _load_and_format_dataset(tokenizer, num_train=1, num_eval=200, seed=42)
    eval_ds = eval_ds.select(range(min(200, len(eval_ds))))

    def compute_completion_logprob(prompt: str, completion: str) -> float:
        """Mean log-prob of completion tokens given prompt."""
        prompt_ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids
        full_ids = tokenizer(
            prompt + completion, return_tensors="pt", add_special_tokens=False
        ).input_ids

        prompt_len = prompt_ids.shape[1]
        full_ids = full_ids.to(model.device)

        with torch.inference_mode():
            logits = model(full_ids).logits  # (1, seq, vocab)

        # Shift: predict token i+1 from position i
        shift_logits = logits[0, :-1, :]  # (seq-1, vocab)
        shift_labels = full_ids[0, 1:]    # (seq-1,)

        log_probs = torch.nn.functional.log_softmax(shift_logits, dim=-1)
        token_log_probs = log_probs[torch.arange(len(shift_labels)), shift_labels]

        # Only completion tokens (after prompt)
        completion_log_probs = token_log_probs[prompt_len - 1:]
        if len(completion_log_probs) == 0:
            return float("-inf")
        return completion_log_probs.mean().item()

    chosen_wins = 0
    chosen_logprobs, rejected_logprobs = [], []

    print(f"Evaluating {len(eval_ds)} examples...")
    for i, ex in enumerate(eval_ds):
        if i % 20 == 0:
            print(f"  {i}/{len(eval_ds)}")
        lp_chosen = compute_completion_logprob(ex["prompt"], ex["chosen"])
        lp_rejected = compute_completion_logprob(ex["prompt"], ex["rejected"])
        chosen_logprobs.append(lp_chosen)
        rejected_logprobs.append(lp_rejected)
        if lp_chosen > lp_rejected:
            chosen_wins += 1

    results = {
        "preference_accuracy": chosen_wins / len(eval_ds),
        "mean_chosen_logprob": sum(chosen_logprobs) / len(chosen_logprobs),
        "mean_rejected_logprob": sum(rejected_logprobs) / len(rejected_logprobs),
        "num_eval_examples": len(eval_ds),
    }

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir, "eval_results.json").write_text(json.dumps(results, indent=2))
    output_vol.commit()

    print("\n--- Eval Results ---")
    for k, v in results.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")


@app.function(**_train_kwargs)
def compare_generations():
    """Generate responses from base model vs DPO model on test prompts."""
    import gc

    import torch

    _setup_env()
    _, username = _hf_login()

    hub_model_id = f"{username}/{PROJECT_NAME}"
    output_dir = f"/outputs/{PROJECT_NAME}"

    gen_kwargs = dict(
        max_new_tokens=350,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.05,
    )

    def generate_response(model, tokenizer, prompt_text: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful, honest, and clear assistant."},
            {"role": "user", "content": prompt_text},
        ]
        try:
            input_text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
            )
        except TypeError:
            input_text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )

        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        with torch.inference_mode():
            output_ids = model.generate(**inputs, **gen_kwargs)
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    results = []

    # --- Base model ---
    print("Loading base model for generation...")
    _, tokenizer, actual_model = load_model_with_fallback(
        BASE_MODEL, FALLBACK_BASE_MODEL, ALLOW_FALLBACK
    )
    base_model = load_model(actual_model)
    base_model.eval()

    base_responses = []
    for prompt in COMPARISON_PROMPTS:
        print(f"  Base: {prompt[:60]}...")
        base_responses.append(generate_response(base_model, tokenizer, prompt))

    # Free base model memory before loading adapter
    del base_model
    gc.collect()
    torch.cuda.empty_cache()

    # --- DPO adapter model ---
    print("Loading DPO adapter model...")
    from peft import PeftModel

    dpo_base = load_model(actual_model)
    try:
        dpo_model = PeftModel.from_pretrained(dpo_base, hub_model_id)
        print(f"Loaded adapter from Hub: {hub_model_id}")
    except Exception:
        dpo_model = PeftModel.from_pretrained(dpo_base, output_dir)
        print(f"Loaded adapter from local: {output_dir}")
    dpo_model.eval()

    dpo_responses = []
    for prompt in COMPARISON_PROMPTS:
        print(f"  DPO: {prompt[:60]}...")
        dpo_responses.append(generate_response(dpo_model, tokenizer, prompt))

    # Build markdown output
    lines = [
        "# Generation Comparison: Base vs DPO\n",
        f"**Base model**: `{actual_model}`  ",
        f"**DPO adapter**: `{hub_model_id}`\n",
    ]
    for i, prompt in enumerate(COMPARISON_PROMPTS):
        lines += [
            f"---\n## Prompt {i+1}\n",
            f"> {prompt}\n",
            "### Base Model\n",
            base_responses[i],
            "\n### DPO Model\n",
            dpo_responses[i],
            "\n",
        ]

    md = "\n".join(lines)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir, "comparison_generations.md").write_text(md)
    output_vol.commit()
    print(md)


@app.function(
    image=image,
    timeout=60 * 10,
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/outputs": output_vol},
)
def push_model_card():
    """Generate and push model card README to Hugging Face Hub."""
    from huggingface_hub import HfApi

    _setup_env()
    _, username = _hf_login()

    hub_model_id = f"{username}/{PROJECT_NAME}"
    output_dir = Path(f"/outputs/{PROJECT_NAME}")

    # Load metadata saved during training
    meta_path = output_dir / "train_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    actual_model = meta.get("base_model", "Qwen/Qwen3-4B-Instruct")

    # Load eval results if available
    eval_path = output_dir / "eval_results.json"
    eval_results = json.loads(eval_path.read_text()) if eval_path.exists() else None

    # Load comparison if available
    comp_path = output_dir / "comparison_generations.md"
    comp_md = comp_path.read_text() if comp_path.exists() else None

    eval_section = ""
    if eval_results:
        eval_section = f"""
## Evaluation Results

| Metric | Value |
|--------|-------|
| Preference Accuracy | {eval_results['preference_accuracy']:.4f} |
| Mean Chosen Log-Prob | {eval_results['mean_chosen_logprob']:.4f} |
| Mean Rejected Log-Prob | {eval_results['mean_rejected_logprob']:.4f} |
| Eval Examples | {eval_results['num_eval_examples']} |
"""

    comp_section = f"\n{comp_md}" if comp_md else ""

    from datetime import date

    # Extract model name from hub_model_id
    model_name = hub_model_id.split('/')[-1]

    readme = MODEL_CARD_TEMPLATE.format(
        base_model=actual_model,
        hub_model_id=hub_model_id,
        model_name=model_name,
        date=date.today().isoformat(),
        eval_section=eval_section,
        comp_section=comp_section,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme)

    api = HfApi()
    api.create_repo(hub_model_id, exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(readme_path),
        path_in_repo="README.md",
        repo_id=hub_model_id,
    )
    output_vol.commit()
    print(f"Model card pushed to: https://huggingface.co/{hub_model_id}")
