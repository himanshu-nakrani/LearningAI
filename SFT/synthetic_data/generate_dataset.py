"""
Synthetic Instruction Dataset Generation Pipeline.

Uses a large LLM (Qwen 2.5 72B) on Modal to generate high-quality
instruction-response pairs across multiple categories.

Setup:
    modal secret create huggingface-secret HF_TOKEN=hf_xxx

Run order:
    modal run generate_dataset.py::test_generation
    modal run generate_dataset.py::generate_dataset
    modal run generate_dataset.py::quality_check
    modal run generate_dataset.py::upload_to_hub
"""

import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import modal

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# ============================================================================
# Configuration
# ============================================================================

# Model selection - Qwen 2.5 72B is excellent for instruction generation
GENERATOR_MODEL = "Qwen/Qwen2.5-72B-Instruct"
FALLBACK_MODEL = "Qwen/Qwen2.5-32B-Instruct"  # Fallback if 72B too large

# Dataset configuration
DATASET_NAME = "instruction-dataset-qwen-synthetic"
TOTAL_EXAMPLES = 3000

# Generation parameters
TEMPERATURE = 0.8
TOP_P = 0.95
MAX_NEW_TOKENS_INSTRUCTION = 150
MAX_NEW_TOKENS_RESPONSE = 600

# GPU - 72B needs significant memory
GPU_CONFIG = "B200"  # B200 has plenty of memory for 72B with 4-bit

# ============================================================================
# Modal Setup
# ============================================================================

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.1.0",
        "transformers>=4.46.0",
        "accelerate>=0.34.0",
        "bitsandbytes>=0.44.0",
        "huggingface_hub>=0.26.0",
        "datasets>=2.14.0",
        "safetensors>=0.4.0",
        "sentencepiece>=0.2.0",
        "protobuf>=3.20.0",
        "einops>=0.8.0",
        "hf-transfer>=0.1.8",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .add_local_python_source("seed_prompts")
)

hf_cache_vol = modal.Volume.from_name("hf-cache", create_if_missing=True)
output_vol = modal.Volume.from_name("synthetic-data", create_if_missing=True)

app = modal.App("synthetic-data-gen")

_gen_kwargs = dict(
    image=image,
    gpu=GPU_CONFIG,
    timeout=60 * 60 * 4,  # 4 hours
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/hf-cache": hf_cache_vol, "/data": output_vol},
)

# ============================================================================
# Utilities
# ============================================================================

def _setup_env():
    os.environ["HF_HOME"] = "/hf-cache"
    os.environ["TRANSFORMERS_CACHE"] = "/hf-cache"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"


def _hf_login():
    from huggingface_hub import HfApi, login

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN not set in Modal secret")
    login(token=token)
    username = os.environ.get("HF_USERNAME") or HfApi().whoami(token=token)["name"]
    return token, username


def load_generator_model():
    """Load 72B model with 4-bit quantization."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )

    model_name = GENERATOR_MODEL
    try:
        print(f"Loading {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"Failed to load {model_name}: {e}")
        print(f"Falling back to {FALLBACK_MODEL}")
        model_name = FALLBACK_MODEL
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model.eval()

    return model, tokenizer, model_name


def generate_text_batch(model, tokenizer, prompts: list[tuple[str, str]],
                         max_new_tokens: int = 500, temperature: float = 0.8) -> list[str]:
    """Generate text for multiple prompts in parallel.

    Args:
        prompts: List of (system_prompt, user_prompt) tuples
    Returns:
        List of generated responses
    """
    import torch

    texts = []
    for system_prompt, user_prompt in prompts:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        texts.append(text)

    inputs = tokenizer(
        texts, return_tensors="pt", padding=True, truncation=True, max_length=2048
    ).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )

    responses = []
    input_len = inputs["input_ids"].shape[1]
    for i in range(len(prompts)):
        new_tokens = outputs[i][input_len:]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        responses.append(response)

    return responses


def generate_text(model, tokenizer, system_prompt: str, user_prompt: str,
                  max_new_tokens: int = 500, temperature: float = 0.8) -> str:
    """Generate text using the chat template."""
    import torch

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    return response


def parse_generated_instruction(text: str) -> str:
    """Clean and extract instruction from generated text."""
    # Remove markdown headers
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Skip markdown headers
        if line.startswith("#"):
            continue
        # Remove common prefixes
        for prefix in ["Instruction:", "Question:", "Task:", "Prompt:", "User:", "Request:"]:
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
        if line:
            cleaned_lines.append(line)

    if not cleaned_lines:
        return ""

    # Take meaningful content (first 1-3 lines)
    text = " ".join(cleaned_lines[:3]).strip()

    # Remove surrounding quotes
    if (text.startswith('"') and text.endswith('"')) or \
       (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()

    return text


# ============================================================================
# Modal Functions
# ============================================================================

@app.function(**_gen_kwargs)
def test_generation():
    """Quick test: generate 5 examples to verify pipeline works."""
    from seed_prompts import CATEGORIES

    _setup_env()
    _hf_login()

    model, tokenizer, model_name = load_generator_model()

    print(f"\n{'='*60}")
    print(f"Testing with {model_name}")
    print(f"{'='*60}\n")

    for category, config in list(CATEGORIES.items())[:3]:
        topic = random.choice(config["topics"])

        # Generate instruction
        instruction_prompt = config["instruction_template"].format(topic=topic)
        instruction = generate_text(
            model, tokenizer,
            config["system_prompt"],
            instruction_prompt,
            max_new_tokens=MAX_NEW_TOKENS_INSTRUCTION,
            temperature=0.9,
        )
        instruction = parse_generated_instruction(instruction)

        # Generate response
        response = generate_text(
            model, tokenizer,
            "You are a helpful, knowledgeable assistant. Provide clear, accurate, and detailed responses.",
            instruction,
            max_new_tokens=MAX_NEW_TOKENS_RESPONSE,
            temperature=0.7,
        )

        print(f"\n--- Category: {category} ---")
        print(f"Topic: {topic}")
        print(f"Instruction: {instruction[:200]}")
        print(f"Response: {response[:300]}...")
        print()


@app.function(**_gen_kwargs)
def generate_dataset_batched(num_examples: int = TOTAL_EXAMPLES, batch_size: int = 8):
    """Generate dataset using batched generation (much faster)."""
    from seed_prompts import CATEGORIES, get_category_distribution

    _setup_env()
    _hf_login()

    model, tokenizer, model_name = load_generator_model()
    distribution = get_category_distribution(num_examples)

    print(f"\n{'='*60}")
    print(f"Generating {num_examples} examples with {model_name}")
    print(f"Batch size: {batch_size}")
    print(f"{'='*60}")
    for cat, count in distribution.items():
        print(f"  {cat}: {count}")
    print()

    output_dir = Path("/data/dataset")
    output_dir.mkdir(parents=True, exist_ok=True)

    examples = []
    save_path = output_dir / "synthetic_instructions.jsonl"

    # Resume support
    if save_path.exists():
        with open(save_path, "r") as f:
            examples = [json.loads(line) for line in f if line.strip()]
        print(f"Resuming: loaded {len(examples)} existing examples")

    completed_per_cat = {cat: 0 for cat in CATEGORIES.keys()}
    for ex in examples:
        if ex.get("category") in completed_per_cat:
            completed_per_cat[ex["category"]] += 1

    total_target = sum(distribution.values())
    response_system = "You are a helpful, knowledgeable assistant. Provide clear, accurate, and detailed responses."

    with open(save_path, "a") as f:
        for category, target_count in distribution.items():
            config = CATEGORIES[category]

            while completed_per_cat[category] < target_count:
                batch_topics = []
                for _ in range(min(batch_size, target_count - completed_per_cat[category])):
                    batch_topics.append(random.choice(config["topics"]))

                # Stage 1: Batch generate instructions
                instruction_prompts = [
                    (config["system_prompt"], config["instruction_template"].format(topic=t))
                    for t in batch_topics
                ]
                try:
                    raw_instructions = generate_text_batch(
                        model, tokenizer, instruction_prompts,
                        max_new_tokens=MAX_NEW_TOKENS_INSTRUCTION,
                        temperature=0.9,
                    )
                except Exception as e:
                    print(f"  Batch instruction error: {e}")
                    continue

                # Parse and filter
                valid_pairs = []
                for topic, raw_inst in zip(batch_topics, raw_instructions):
                    inst = parse_generated_instruction(raw_inst)
                    if 20 <= len(inst) <= 500:
                        valid_pairs.append((topic, inst))

                if not valid_pairs:
                    continue

                # Stage 2: Batch generate responses
                response_prompts = [(response_system, inst) for _, inst in valid_pairs]
                try:
                    raw_responses = generate_text_batch(
                        model, tokenizer, response_prompts,
                        max_new_tokens=MAX_NEW_TOKENS_RESPONSE,
                        temperature=0.7,
                    )
                except Exception as e:
                    print(f"  Batch response error: {e}")
                    continue

                # Save valid examples
                for (topic, instruction), response in zip(valid_pairs, raw_responses):
                    if len(response) < 50:
                        continue

                    example = {
                        "instruction": instruction,
                        "response": response,
                        "category": category,
                        "seed_topic": topic,
                        "metadata": {
                            "model": model_name,
                            "temperature": TEMPERATURE,
                            "generated_at": datetime.utcnow().isoformat(),
                        }
                    }
                    examples.append(example)
                    f.write(json.dumps(example, ensure_ascii=False) + "\n")
                    f.flush()
                    completed_per_cat[category] += 1

                total_done = sum(completed_per_cat.values())
                print(f"  Progress: {total_done}/{total_target} "
                      f"({100*total_done/total_target:.1f}%) - "
                      f"category: {category} ({completed_per_cat[category]}/{target_count})")

                # Commit volume periodically
                if total_done % 50 == 0:
                    output_vol.commit()

    output_vol.commit()
    print(f"\nGenerated {len(examples)} total examples")
    print(f"Saved to: {save_path}")

    summary = {
        "total_examples": len(examples),
        "model": model_name,
        "categories": completed_per_cat,
        "generated_at": datetime.utcnow().isoformat(),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    output_vol.commit()


@app.function(**_gen_kwargs)
def generate_dataset(num_examples: int = TOTAL_EXAMPLES):
    """Generate the full synthetic dataset."""
    from seed_prompts import CATEGORIES, get_category_distribution

    _setup_env()
    _hf_login()

    model, tokenizer, model_name = load_generator_model()
    distribution = get_category_distribution(num_examples)

    print(f"\n{'='*60}")
    print(f"Generating {num_examples} examples with {model_name}")
    print(f"{'='*60}")
    for cat, count in distribution.items():
        print(f"  {cat}: {count}")
    print()

    output_dir = Path("/data/dataset")
    output_dir.mkdir(parents=True, exist_ok=True)

    examples = []
    save_path = output_dir / "synthetic_instructions.jsonl"

    # Resume support: load existing examples
    if save_path.exists():
        with open(save_path, "r") as f:
            examples = [json.loads(line) for line in f if line.strip()]
        print(f"Resuming: loaded {len(examples)} existing examples")

    completed_per_cat = {cat: 0 for cat in CATEGORIES.keys()}
    for ex in examples:
        if ex.get("category") in completed_per_cat:
            completed_per_cat[ex["category"]] += 1

    total_target = sum(distribution.values())
    pbar_step = max(10, total_target // 100)

    with open(save_path, "a") as f:
        for category, target_count in distribution.items():
            config = CATEGORIES[category]
            current = completed_per_cat[category]

            while current < target_count:
                topic = random.choice(config["topics"])

                try:
                    # Generate instruction
                    instruction_prompt = config["instruction_template"].format(topic=topic)
                    instruction = generate_text(
                        model, tokenizer,
                        config["system_prompt"],
                        instruction_prompt,
                        max_new_tokens=MAX_NEW_TOKENS_INSTRUCTION,
                        temperature=0.9,
                    )
                    instruction = parse_generated_instruction(instruction)

                    # Skip if too short or too long
                    if len(instruction) < 20 or len(instruction) > 500:
                        continue

                    # Generate response
                    response = generate_text(
                        model, tokenizer,
                        "You are a helpful, knowledgeable assistant. Provide clear, accurate, and detailed responses.",
                        instruction,
                        max_new_tokens=MAX_NEW_TOKENS_RESPONSE,
                        temperature=0.7,
                    )

                    # Quality filter
                    if len(response) < 50:
                        continue

                    example = {
                        "instruction": instruction,
                        "response": response,
                        "category": category,
                        "seed_topic": topic,
                        "metadata": {
                            "model": model_name,
                            "temperature": TEMPERATURE,
                            "generated_at": datetime.utcnow().isoformat(),
                        }
                    }

                    examples.append(example)
                    f.write(json.dumps(example, ensure_ascii=False) + "\n")
                    f.flush()

                    current += 1
                    completed_per_cat[category] = current

                    total_done = sum(completed_per_cat.values())
                    if total_done % pbar_step == 0:
                        print(f"  Progress: {total_done}/{total_target} "
                              f"({100*total_done/total_target:.1f}%) - "
                              f"latest: {category}")
                        output_vol.commit()

                except Exception as e:
                    print(f"  Error in {category}: {e}")
                    continue

    output_vol.commit()
    print(f"\nGenerated {len(examples)} total examples")
    print(f"Saved to: {save_path}")

    # Summary
    summary = {
        "total_examples": len(examples),
        "model": model_name,
        "categories": completed_per_cat,
        "generated_at": datetime.utcnow().isoformat(),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    output_vol.commit()


@app.function(
    image=image,
    timeout=60 * 30,
    volumes={"/data": output_vol},
)
def quality_check():
    """Analyze generated dataset quality."""
    data_path = Path("/data/dataset/synthetic_instructions.jsonl")
    if not data_path.exists():
        print("No dataset found. Run generate_dataset first.")
        return

    examples = []
    with open(data_path, "r") as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    print(f"\n{'='*60}")
    print(f"Quality Check: {len(examples)} examples")
    print(f"{'='*60}\n")

    # Category distribution
    from collections import Counter
    cat_counts = Counter(ex["category"] for ex in examples)
    print("Category distribution:")
    for cat, count in cat_counts.most_common():
        print(f"  {cat}: {count} ({100*count/len(examples):.1f}%)")

    # Length statistics
    inst_lengths = [len(ex["instruction"]) for ex in examples]
    resp_lengths = [len(ex["response"]) for ex in examples]

    print(f"\nInstruction length:")
    print(f"  Min: {min(inst_lengths)}, Max: {max(inst_lengths)}, "
          f"Mean: {sum(inst_lengths)/len(inst_lengths):.0f}")
    print(f"\nResponse length:")
    print(f"  Min: {min(resp_lengths)}, Max: {max(resp_lengths)}, "
          f"Mean: {sum(resp_lengths)/len(resp_lengths):.0f}")

    # Deduplication check
    unique_instructions = set(ex["instruction"] for ex in examples)
    print(f"\nUnique instructions: {len(unique_instructions)} "
          f"({100*len(unique_instructions)/len(examples):.1f}%)")

    # Show samples
    print(f"\n--- Sample examples ---")
    for ex in random.sample(examples, min(3, len(examples))):
        print(f"\n[{ex['category']}]")
        print(f"Instruction: {ex['instruction'][:200]}")
        print(f"Response: {ex['response'][:300]}...")

    # Save quality report
    report = {
        "total": len(examples),
        "categories": dict(cat_counts),
        "instruction_length": {
            "min": min(inst_lengths),
            "max": max(inst_lengths),
            "mean": sum(inst_lengths) / len(inst_lengths),
        },
        "response_length": {
            "min": min(resp_lengths),
            "max": max(resp_lengths),
            "mean": sum(resp_lengths) / len(resp_lengths),
        },
        "unique_instructions": len(unique_instructions),
        "duplicate_rate": 1 - len(unique_instructions) / len(examples),
    }

    Path("/data/dataset/quality_report.json").write_text(json.dumps(report, indent=2))
    output_vol.commit()
    print(f"\nQuality report saved to /data/dataset/quality_report.json")


@app.function(
    image=image,
    timeout=60 * 30,
    secrets=[modal.Secret.from_name("huggingface-secret")],
    volumes={"/data": output_vol},
)
def upload_to_hub():
    """Upload generated dataset to HuggingFace Hub."""
    from datasets import Dataset
    from huggingface_hub import HfApi

    _setup_env()
    _, username = _hf_login()

    data_path = Path("/data/dataset/synthetic_instructions.jsonl")
    if not data_path.exists():
        print("No dataset found.")
        return

    examples = []
    with open(data_path, "r") as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    print(f"Loaded {len(examples)} examples")

    # Create HF dataset
    ds = Dataset.from_list(examples)

    # Train/test split
    ds_split = ds.train_test_split(test_size=0.05, seed=42)
    print(f"Train: {len(ds_split['train'])}, Test: {len(ds_split['test'])}")

    repo_id = f"{username}/{DATASET_NAME}"

    # Push to hub
    print(f"Uploading to: {repo_id}")
    ds_split.push_to_hub(repo_id, private=False)

    # Generate dataset card
    card_content = f"""---
license: apache-2.0
language:
  - en
size_categories:
  - 10K<n<100K
task_categories:
  - text-generation
  - question-answering
tags:
  - synthetic
  - instruction-tuning
  - qwen
---

# Synthetic Instruction Dataset

A high-quality synthetic instruction-response dataset generated using Qwen 2.5 72B Instruct.

## Dataset Details

- **Total Examples:** {len(examples)}
- **Train/Test Split:** {len(ds_split['train'])}/{len(ds_split['test'])}
- **Generator Model:** Qwen 2.5 72B Instruct
- **Generated:** {datetime.utcnow().strftime('%Y-%m-%d')}

## Categories

The dataset covers diverse categories:

- **Coding & Programming** - Algorithm implementation, code explanation, debugging
- **Mathematics & Reasoning** - Problem solving with step-by-step explanations
- **Creative Writing** - Stories, poems, dialogue
- **Technical Explanation** - Clear explanations of complex concepts
- **Professional Communication** - Emails, reports, documentation
- **General Knowledge** - Educational content across many fields

## Format

Each example contains:

```json
{{
  "instruction": "Clear, specific task or question",
  "response": "Detailed, helpful response",
  "category": "coding|math_reasoning|creative_writing|...",
  "seed_topic": "Original seed topic used for generation",
  "metadata": {{
    "model": "Qwen/Qwen2.5-72B-Instruct",
    "temperature": 0.8,
    "generated_at": "ISO timestamp"
  }}
}}
```

## Usage

```python
from datasets import load_dataset

ds = load_dataset("{repo_id}")
print(ds)

# Use for fine-tuning
example = ds["train"][0]
print(example["instruction"])
print(example["response"])
```

## Generation Pipeline

The dataset was generated using a Modal-based pipeline that:

1. Uses diverse seed topics across 6 categories
2. Generates instructions using category-specific prompts
3. Generates detailed responses with the same model
4. Filters out low-quality examples
5. Tracks metadata for reproducibility

## Limitations

- Generated by AI - may contain inaccuracies
- English language only
- May reflect biases of the generator model
- Should be used with appropriate validation

## License

Apache 2.0
"""

    api = HfApi()
    api.upload_file(
        path_or_fileobj=card_content.encode(),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )

    print(f"\n✅ Dataset uploaded to: https://huggingface.co/datasets/{repo_id}")
