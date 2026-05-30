---
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

# helpful-qwen3-4b-dpo-lora

A LoRA adapter fine-tuned with Direct Preference Optimization (DPO) on human preference data to produce a more helpful, honest, and clear assistant.

## Model Details

| Property | Value |
|----------|-------|
| Base Model | `{base_model}` |
| Method | DPO + QLoRA |
| Dataset | argilla/ultrafeedback-binarized-preferences-cleaned |
| Training Examples | 10,000 |
| Eval Examples | 500 |
| LoRA Rank | 32 |
| LoRA Alpha | 64 |
| DPO Beta | 0.1 |
| Learning Rate | 5e-7 |
| Trained On | {date} |
| Hub ID | `{hub_model_id}` |

{eval_section}

## Usage

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model_id = "{base_model}"
adapter_id = "{hub_model_id}"

tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
)
model = PeftModel.from_pretrained(base_model, adapter_id)
model.eval()

messages = [
    {{"role": "system", "content": "You are a helpful, honest, and clear assistant."}},
    {{"role": "user", "content": "Explain gradient descent to a beginner."}},
]
input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

with torch.inference_mode():
    output = model.generate(**inputs, max_new_tokens=300, temperature=0.7, do_sample=True)

print(tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

## Training

Trained using Modal with the [helpful-qwen3-4b-dpo-lora](https://github.com/himanshu-nakrani/LearningAI) pipeline:

```bash
modal run modal_app.py::train
```

## Limitations

- This is a LoRA adapter, not a standalone model. Requires the base model to run.
- Trained on English preference data; may not generalize well to other languages.
- 4-bit quantization used during training may slightly reduce quality vs full-precision training.
- DPO with a small dataset may not fully eliminate all undesirable behaviors.

{comp_section}
