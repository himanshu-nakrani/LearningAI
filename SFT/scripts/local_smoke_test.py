"""
Local smoke test for dataset formatting and tokenizer logic (no GPU needed).

Usage:
    pip install transformers datasets sentencepiece
    python scripts/local_smoke_test.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datasets import load_dataset
from transformers import AutoTokenizer

from modal_app import extract_text, format_for_dpo

MODEL = "Qwen/Qwen2.5-3B-Instruct"  # Use smaller model for local test


def test_extract_text():
    print("--- test_extract_text ---")
    cases = [
        ("string", "hello world", "hello world"),
        ("list of messages", [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}], "user: hi\nassistant: hello"),
        ("dict with content", {"content": "some text"}, "some text"),
        ("dict with messages", {"messages": [{"role": "user", "content": "q"}]}, "user: q"),
    ]
    for name, inp, expected in cases:
        result = extract_text(inp)
        status = "PASS" if expected in result else "FAIL"
        print(f"  [{status}] {name}: {result[:80]!r}")
    print()


def test_format_for_dpo():
    print("--- test_format_for_dpo ---")
    print(f"Loading tokenizer: {MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    print("Loading 5 dataset examples...")
    ds = load_dataset(
        "argilla/ultrafeedback-binarized-preferences-cleaned",
        split="train[:5]",
    )

    for i, ex in enumerate(ds):
        result = format_for_dpo(ex, tokenizer)
        if result is None:
            print(f"  [SKIP] Example {i}: format_for_dpo returned None")
            continue
        p_len = len(result["prompt"])
        c_len = len(result["chosen"])
        r_len = len(result["rejected"])
        print(f"  [OK] Example {i}: prompt={p_len}ch, chosen={c_len}ch, rejected={r_len}ch")
        if i == 0:
            print(f"    prompt[:200]: {result['prompt'][:200]!r}")
            print(f"    chosen[:100]: {result['chosen'][:100]!r}")
            print(f"    rejected[:100]: {result['rejected'][:100]!r}")
    print()


if __name__ == "__main__":
    test_extract_text()
    test_format_for_dpo()
    print("Local smoke test complete.")
