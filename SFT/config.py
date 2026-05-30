"""
Configuration for DPO training pipeline.

Edit this file to customize training parameters, model selection, and output paths.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

# ============================================================================
# Hugging Face Configuration
# ============================================================================

# Your Hugging Face username - REQUIRED for pushing models
# Option 1: Set via environment variable (recommended)
# Option 2: Set directly here
HF_USERNAME = os.environ.get("HF_USERNAME", "himanshunakrani9")

# If HF_USERNAME is None, the pipeline will attempt to auto-detect from HF_TOKEN
# But explicit configuration is more reliable

# ============================================================================
# Model Configuration
# ============================================================================

# Primary base model to use
BASE_MODEL = "Qwen/Qwen3-4B-Instruct"

# Fallback model if primary fails to load
FALLBACK_BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

# Whether to allow automatic fallback
ALLOW_FALLBACK = True

# ============================================================================
# Dataset Configuration
# ============================================================================

DATASET_NAME = "argilla/ultrafeedback-binarized-preferences-cleaned"

# Number of examples to use for training
NUM_TRAIN_EXAMPLES = 10000

# Number of examples to use for evaluation
NUM_EVAL_EXAMPLES = 500

# ============================================================================
# Output Configuration
# ============================================================================

# Project name - used for output directories and HuggingFace model ID
PROJECT_NAME = "qwen2.5-3b-ultrafeedback-dpo"

# Local output directory (on Modal volume)
OUTPUT_DIR = f"/outputs/{PROJECT_NAME}"

# Hugging Face Hub model ID (will be auto-constructed if HF_USERNAME is set)
# Format: {HF_USERNAME}/{PROJECT_NAME}
HUB_MODEL_ID = None  # Auto-constructed in modal_app.py

# ============================================================================
# Training Hyperparameters
# ============================================================================

@dataclass
class TrainingConfig:
    """Full training configuration."""

    # Sequence lengths
    max_length: int = 2048
    max_prompt_length: int = 1024

    # DPO-specific
    beta: float = 0.1  # DPO temperature parameter

    # Optimization
    learning_rate: float = 5e-7
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    num_train_epochs: int = 1
    max_steps: int = -1  # -1 means use num_train_epochs

    # Learning rate schedule
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"

    # Optimizer
    optim: str = "paged_adamw_8bit"

    # Precision
    bf16: bool = True
    fp16: bool = False

    # Memory optimization
    gradient_checkpointing: bool = True

    # Logging and saving
    logging_steps: int = 10
    save_steps: int = 250
    eval_steps: int = 100
    save_total_limit: int = 3

    # Reproducibility
    seed: int = 42

    # Reporting
    report_to: str = "none"  # Change to "wandb" if you want W&B logging


@dataclass
class SmokeTestConfig:
    """Quick smoke test configuration."""

    # Tiny dataset
    num_train_examples: int = 32
    num_eval_examples: int = 8

    # Shorter sequences
    max_length: int = 1024
    max_prompt_length: int = 512

    # Quick training
    max_steps: int = 10

    # Frequent logging
    logging_steps: int = 2
    save_steps: int = 10
    eval_steps: int = 10

    # Same as full training for other params
    beta: float = 0.1
    learning_rate: float = 5e-7
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 4
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    optim: str = "paged_adamw_8bit"
    bf16: bool = True
    fp16: bool = False
    gradient_checkpointing: bool = True
    seed: int = 42
    report_to: str = "none"
    save_total_limit: int = 1


# ============================================================================
# LoRA Configuration
# ============================================================================

@dataclass
class LoRAConfig:
    """LoRA adapter configuration."""

    r: int = 32  # LoRA rank
    lora_alpha: int = 64  # LoRA alpha (scaling factor)
    lora_dropout: float = 0.05
    bias: str = "none"
    task_type: str = "CAUSAL_LM"

    # Target modules for Qwen/Llama-style architectures
    target_modules: list[str] = field(default_factory=lambda: [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ])


# ============================================================================
# Quantization Configuration
# ============================================================================

@dataclass
class QuantizationConfig:
    """4-bit quantization configuration."""

    load_in_4bit: bool = True
    bnb_4bit_compute_dtype: str = "bfloat16"  # Will be converted to torch.bfloat16
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_quant_type: str = "nf4"


# ============================================================================
# Generation Configuration
# ============================================================================

@dataclass
class GenerationConfig:
    """Configuration for model generation/inference."""

    max_new_tokens: int = 350
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True
    repetition_penalty: float = 1.05


# ============================================================================
# Evaluation Configuration
# ============================================================================

@dataclass
class EvalConfig:
    """Configuration for evaluation."""

    # Number of examples to evaluate (for logprob computation)
    num_eval_examples: int = 200

    # Batch size for evaluation
    eval_batch_size: int = 4


# ============================================================================
# Test Prompts for Generation Comparison
# ============================================================================

COMPARISON_PROMPTS = [
    "Explain gradient descent to a beginner using an analogy.",
    "Give me a 7-day plan to learn Python for data analysis.",
    "What are three common mistakes people make when fine-tuning LLMs?",
    "Explain the difference between precision and recall.",
    "Write a polite email asking for an extension on a project deadline.",
]


# ============================================================================
# Smoke Test Settings
# ============================================================================

# Whether to push smoke test results to Hub (usually False)
PUSH_SMOKE_TO_HUB = False

# Separate Hub ID for smoke test (if PUSH_SMOKE_TO_HUB is True)
SMOKE_HUB_MODEL_ID = None  # Will be auto-constructed as {HF_USERNAME}/{PROJECT_NAME}-smoke


# ============================================================================
# System Prompt
# ============================================================================

SYSTEM_PROMPT = "You are a helpful, honest, and clear assistant."


# ============================================================================
# Helper Functions
# ============================================================================

def get_hub_model_id(username: Optional[str] = None, smoke: bool = False) -> str:
    """
    Construct Hugging Face Hub model ID.

    Args:
        username: HF username (if None, uses HF_USERNAME from config)
        smoke: Whether this is for smoke test

    Returns:
        Full Hub model ID

    Raises:
        ValueError: If username cannot be determined
    """
    if username is None:
        username = HF_USERNAME

    if username is None:
        raise ValueError(
            "HF_USERNAME not set. Either:\n"
            "1. Set environment variable: export HF_USERNAME=your-username\n"
            "2. Set HF_USERNAME in config.py\n"
            "3. Pass username explicitly to this function"
        )

    from config import PROJECT_NAME
    model_name = PROJECT_NAME
    if smoke:
        model_name += "-smoke"

    return f"{username}/{model_name}"


def get_training_config(smoke: bool = False) -> TrainingConfig | SmokeTestConfig:
    """
    Get training configuration.

    Args:
        smoke: Whether to use smoke test config

    Returns:
        Training configuration dataclass
    """
    if smoke:
        return SmokeTestConfig()
    else:
        return TrainingConfig()
