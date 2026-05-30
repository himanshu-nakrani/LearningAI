# Migration Guide: Model Rename

## What Changed

**Old Name:** `himanshunakrani9/helpful-qwen3-4b-dpo-lora`  
**New Name:** `himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo`

## Why the Change?

The new name is more descriptive and professional:
- ✅ Clearly indicates base model: **Qwen 2.5 3B**
- ✅ Shows dataset used: **UltraFeedback**
- ✅ Specifies method: **DPO**
- ✅ More searchable and discoverable

## Current Status

✅ **New model card created:** https://huggingface.co/himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo

⚠️ **Old model still exists:** https://huggingface.co/himanshunakrani9/helpful-qwen3-4b-dpo-lora

## Next Steps

### Option 1: Keep Both (Recommended for Now)

Keep the old model for backward compatibility and let the new one be the primary:

1. ✅ New model card already pushed
2. Add deprecation notice to old model:
   - Go to https://huggingface.co/himanshunakrani9/helpful-qwen3-4b-dpo-lora
   - Edit README.md
   - Add at top:
     ```markdown
     > **⚠️ DEPRECATED:** This model has been renamed to [`qwen2.5-3b-ultrafeedback-dpo`](https://huggingface.co/himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo). Please use the new repository.
     ```

### Option 2: Delete Old Model

If you want to clean up:

1. Go to https://huggingface.co/himanshunakrani9/helpful-qwen3-4b-dpo-lora/settings
2. Scroll to bottom
3. Click "Delete this model"
4. Confirm deletion

**Note:** This will break any existing links or code using the old name.

### Option 3: Rename Old Model (Cleanest)

This preserves the repository history and creates a redirect:

1. Go to https://huggingface.co/himanshunakrani9/helpful-qwen3-4b-dpo-lora/settings
2. Find "Rename or transfer this model"
3. Enter new name: `qwen2.5-3b-ultrafeedback-dpo-old` (or delete it)
4. Click "Rename"

Then the new model at `qwen2.5-3b-ultrafeedback-dpo` becomes the primary.

## Updated Code Examples

### Old Usage (Still Works)
```python
model = PeftModel.from_pretrained(
    base_model, 
    "himanshunakrani9/helpful-qwen3-4b-dpo-lora"
)
```

### New Usage (Recommended)
```python
model = PeftModel.from_pretrained(
    base_model, 
    "himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo"
)
```

## Repository Updates

All code in this repository now uses the new name:
- ✅ `modal_app.py` - Updated `PROJECT_NAME`
- ✅ `config.py` - Updated naming
- ✅ `README.md` - Updated all references
- ✅ Model card template - Updated

## Recommendation

**For now:** Keep both models, add deprecation notice to old one.

**After 1-2 weeks:** Delete or rename the old model once you're confident the new one is working correctly.

## Verification

Check that the new model works:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load with new name
base = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True
)
model = PeftModel.from_pretrained(
    base,
    "himanshunakrani9/qwen2.5-3b-ultrafeedback-dpo"
)
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    trust_remote_code=True
)

# Test generation
messages = [{"role": "user", "content": "Hello!"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=50)

print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

If this works, the migration is successful! ✅
