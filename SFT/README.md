# Qwen 2.5 3B UltraFeedback DPO

Production-ready pipeline for training preference-aligned language models using Direct Preference Optimization (DPO) on Modal's serverless GPU infrastructure.

## Overview

This project demonstrates end-to-end DPO fine-tuning of Qwen 2.5 3B on the UltraFeedback preference dataset. The pipeline handles everything from dataset preprocessing to model deployment on Hugging Face Hub.

**Key Features:**
- 🚀 Serverless training on Modal (B200/H100/A100)
- 🎯 Direct Preference Optimization with QLoRA
- 📊 Automated evaluation and comparison
- 🤗 One-command deployment to Hugging Face
- 💰 Cost-efficient: ~$6-9 for full training run
- ⚡ Fast: 30-40 minutes end-to-end

## What is DPO?

Direct Preference Optimization (DPO) is a simpler, more stable alternative to RLHF for aligning language models with human preferences. Instead of training a separate reward model and using reinforcement learning, DPO directly optimizes the model on preference pairs (chosen vs rejected responses).

**Advantages over RLHF:**
- No separate reward model needed
- More stable training (no RL instability)
- Faster and more compute-efficient
- Comparable or better results

## Results

**Model:** [`himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo`](https://huggingface.co/himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo)

| Metric | Value |
|--------|-------|
| Base Model | Qwen/Qwen2.5-3B-Instruct |
| Training Examples | 9,998 |
| Training Time | ~30 minutes (B200) |
| Preference Accuracy | 57.5% |
| Mean Chosen Log-Prob | -1.56 |
| Mean Rejected Log-Prob | -2.19 |
| Final Train Loss | 0.6728 |
| Final Eval Loss | 0.6626 |

The model successfully learned to prefer chosen responses over rejected ones, with a clear separation in log-probabilities.

## Quick Start

### 1. Prerequisites

```bash
# Install Modal
pip install modal

# Authenticate with Modal (opens browser)
modal setup
```

### 2. Configure Secrets

Create a Hugging Face token with **write** permissions at https://huggingface.co/settings/tokens

```bash
# Create Modal secret
modal secret create huggingface-secret HF_TOKEN=hf_your_token_here
```

### 3. Run the Pipeline

```bash
# Clone and navigate
cd /path/to/SFT

# Activate virtual environment (if using one)
source .venv/bin/activate

# 1. Inspect dataset (optional, 1 min)
modal run modal_app.py::inspect_dataset

# 2. Smoke test (5-10 min, ~$0.15)
modal run modal_app.py::smoke_train

# 3. Full training (30-40 min, ~$6-9)
modal run modal_app.py::train

# 4. Evaluate (3 min, ~$0.50)
modal run modal_app.py::evaluate

# 5. Compare generations (2 min, ~$0.30)
modal run modal_app.py::compare_generations

# 6. Push model card (30 sec, ~$0.05)
modal run modal_app.py::push_model_card
```

## Project Structure

```
SFT/
├── modal_app.py              # Main training pipeline (all Modal functions)
├── config.py                 # Hyperparameter configuration
├── requirements.txt          # Python dependencies
├── model_card_template.md    # HuggingFace model card template
├── README.md                 # This file
├── .gitignore
└── scripts/
    ├── inspect_dataset.py    # Local dataset inspection
    └── local_smoke_test.py   # Local testing utilities
```

## Configuration

All hyperparameters are defined in `modal_app.py` under the Configuration section. Key settings:

### Model Selection

```python
BASE_MODEL = "Qwen/Qwen3-4B-Instruct"  # Primary (will fallback if unavailable)
FALLBACK_BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
PROJECT_NAME = "qwen2.5-3b-ultrafeedback-dpo"
```

### Training Hyperparameters

```python
class TrainingConfig:
    max_length = 2048
    beta = 0.1                    # DPO temperature
    learning_rate = 5e-7
    per_device_train_batch_size = 2
    gradient_accumulation_steps = 8
    num_train_epochs = 1
    lora_r = 32
    lora_alpha = 64
```

### GPU Configuration

```python
GPU_CONFIG = "B200"  # Change to "H100" or modal.gpu.A100(count=1, size="80GB")
```

## Pipeline Details

### 1. Dataset Preprocessing

- **Dataset:** argilla/ultrafeedback-binarized-preferences-cleaned
- **Format:** Prompt + Chosen + Rejected response pairs
- **Preprocessing:** 
  - Robust text extraction from various formats
  - Chat template application
  - Filtering of invalid examples
  - Train/eval split (10k/500)

### 2. Model Training

- **Method:** DPO with QLoRA
- **Quantization:** 4-bit NF4 with double quantization
- **LoRA Config:**
  - Rank: 32
  - Alpha: 64
  - Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Optimizer:** paged_adamw_8bit
- **Precision:** bfloat16

### 3. Evaluation

- **Preference Accuracy:** Percentage of examples where chosen response has higher log-probability
- **Log-Probability Analysis:** Mean log-probs for chosen vs rejected responses
- **Qualitative Comparison:** Side-by-side generations on test prompts

### 4. Deployment

- Automatic push to Hugging Face Hub
- Comprehensive model card with metrics
- LoRA adapter (~100MB) + tokenizer

## Cost & Time Breakdown

| Step | Time | Cost (B200) | Cost (H100) |
|------|------|-------------|-------------|
| Smoke Test | 5-10 min | ~$0.15 | ~$0.10 |
| Full Training | 30-40 min | ~$6-8 | ~$4-6 |
| Evaluation | 3 min | ~$0.50 | ~$0.30 |
| Generation | 2 min | ~$0.30 | ~$0.20 |
| Model Card | 30 sec | ~$0.05 | ~$0.03 |
| **Total** | **~45 min** | **~$7-9** | **~$5-7** |

## Customization Guide

### Change Base Model

Edit `modal_app.py`:

```python
BASE_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
FALLBACK_BASE_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
PROJECT_NAME = "llama-3.2-3b-ultrafeedback-dpo"
```

### Adjust Training Size

```python
# In _load_and_format_dataset calls
train_ds, eval_ds = _load_and_format_dataset(
    tokenizer,
    num_train=5000,   # Reduce for faster training
    num_eval=250,
    seed=cfg.seed,
)
```

### Change Dataset

```python
# In _load_and_format_dataset function
ds = load_dataset("your-dataset-name", split="train")
```

Ensure your dataset has `prompt`, `chosen`, and `rejected` fields (or modify `format_for_dpo` accordingly).

### Tune Hyperparameters

Common adjustments:

```python
class TrainingConfig:
    learning_rate = 1e-6        # Lower for more stable training
    beta = 0.2                  # Higher for stronger preference signal
    lora_r = 64                 # Higher for more capacity
    per_device_train_batch_size = 1  # Lower if OOM
    gradient_accumulation_steps = 16  # Increase to maintain effective batch size
```

## Troubleshooting

### CUDA Out of Memory

**Symptoms:** `torch.cuda.OutOfMemoryError`

**Solutions:**
1. Reduce batch size:
   ```python
   per_device_train_batch_size = 1
   gradient_accumulation_steps = 16
   ```
2. Reduce sequence length:
   ```python
   max_length = 1536
   ```
3. Reduce LoRA rank:
   ```python
   lora_r = 16
   lora_alpha = 32
   ```
4. Use smaller base model or switch to H100/A100

### Model Not Found

**Symptoms:** `OSError: model_name is not a valid model identifier`

**Solution:** The pipeline automatically falls back to `Qwen/Qwen2.5-3B-Instruct`. If both fail, check:
- Model name spelling
- Model availability on Hugging Face
- Access permissions (some models require approval)

### Dataset Format Mismatch

**Symptoms:** `KeyError: 'prompt'` or similar

**Solution:** 
1. Run `modal run modal_app.py::inspect_dataset` to see actual schema
2. Update `format_for_dpo()` function to match your dataset structure
3. The `extract_text()` function handles most common formats

### HuggingFace Push Failed

**Symptoms:** `403 Forbidden` when pushing

**Solutions:**
1. Verify token has **write** permissions
2. Recreate Modal secret:
   ```bash
   modal secret create huggingface-secret HF_TOKEN=hf_new_token --force
   ```
3. Check rate limits on Hugging Face

### Slow Training

**Symptoms:** Training takes much longer than expected

**Solutions:**
1. Verify GPU type: `GPU_CONFIG = "B200"` (not "H100" or A100)
2. Check Modal dashboard for actual GPU allocated
3. Reduce dataset size for testing
4. Ensure gradient checkpointing is enabled

## Advanced Usage

### Merge LoRA Adapter

To create a standalone merged model:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load base model (full precision)
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# Load and merge adapter
model = PeftModel.from_pretrained(
    base_model, 
    "himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo"
)
merged_model = model.merge_and_unload()

# Save
merged_model.save_pretrained("./merged-model")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
tokenizer.save_pretrained("./merged-model")

# Push to Hub
merged_model.push_to_hub("himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo-merged")
tokenizer.push_to_hub("himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo-merged")
```

**Note:** Merged model will be ~6GB vs ~100MB for LoRA adapter.

### Local Inference

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# Load base + adapter
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
model = PeftModel.from_pretrained(
    base_model,
    "himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")

# Generate
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain gradient descent simply."}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7)

print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

### Enable W&B Logging

1. Add W&B API key to Modal secret:
   ```bash
   modal secret create huggingface-secret \
     HF_TOKEN=hf_xxx \
     WANDB_API_KEY=your_wandb_key
   ```

2. Update config in `modal_app.py`:
   ```python
   class TrainingConfig:
       report_to = "wandb"  # Change from "none"
   ```

## Technical Details

### Why QLoRA?

QLoRA (Quantized LoRA) enables efficient fine-tuning by:
- Using 4-bit quantization for base model weights
- Training only LoRA adapters in full precision
- Reducing memory usage by ~4x
- Maintaining comparable performance to full fine-tuning

### Why Modal?

Modal provides:
- Serverless GPU compute (no infrastructure management)
- Pay-per-second billing
- Automatic scaling
- Built-in volume management
- Easy secret management

### Dataset Quality

UltraFeedback is a high-quality preference dataset with:
- 60k+ preference pairs
- Multiple models' responses rated by GPT-4
- Diverse prompts across domains
- Clean, well-formatted data

## Citation

If you use this pipeline or the trained model, please cite:

```bibtex
@article{rafailov2023direct,
  title={Direct Preference Optimization: Your Language Model is Secretly a Reward Model},
  author={Rafailov, Rafael and Sharma, Archit and Mitchell, Eric and Ermon, Stefano and Manning, Christopher D and Finn, Chelsea},
  journal={arXiv preprint arXiv:2305.18290},
  year={2023}
}

@article{cui2023ultrafeedback,
  title={UltraFeedback: Boosting Language Models with High-quality Feedback},
  author={Cui, Ganqu and Yuan, Lifan and Ding, Ning and Yao, Guanming and Zhu, Wei and Ni, Yuan and Xie, Guotong and Liu, Zhiyuan and Sun, Maosong},
  journal={arXiv preprint arXiv:2310.01377},
  year={2023}
}
```

## License

- **Code:** Apache 2.0
- **Qwen 2.5 Model:** Apache 2.0 (verify specific model license)
- **UltraFeedback Dataset:** MIT
- **Trained Adapter:** Inherits base model license (Apache 2.0)

## Acknowledgments

- **Hugging Face** - Transformers, PEFT, TRL libraries
- **Modal** - Serverless GPU infrastructure
- **Argilla** - Cleaned UltraFeedback dataset
- **Alibaba Cloud** - Qwen model family

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/LearningAI/issues)
- **Model:** [HuggingFace Model Card](https://huggingface.co/himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo)
- **Modal Docs:** https://modal.com/docs

## Related Projects

- [TRL (Transformer Reinforcement Learning)](https://github.com/huggingface/trl)
- [PEFT (Parameter-Efficient Fine-Tuning)](https://github.com/huggingface/peft)
- [Qwen Models](https://github.com/QwenLM/Qwen)
- [UltraFeedback Dataset](https://huggingface.co/datasets/openbmb/UltraFeedback)
