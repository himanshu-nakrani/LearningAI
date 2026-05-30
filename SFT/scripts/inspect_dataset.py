"""
Local dataset inspection script (no GPU needed).

Usage:
    pip install datasets huggingface_hub
    python scripts/inspect_dataset.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datasets import load_dataset

from modal_app import extract_text


def main():
    print("Loading dataset (first 100 examples)...")
    ds = load_dataset(
        "argilla/ultrafeedback-binarized-preferences-cleaned",
        split="train[:100]",
    )

    print(f"\nColumns: {ds.column_names}")
    print(f"Total loaded: {len(ds)}\n")

    for i in range(min(3, len(ds))):
        ex = ds[i]
        print(f"{'='*60}")
        print(f"Example {i}")
        print(f"{'='*60}")
        for col in ["prompt", "chosen", "rejected"]:
            if col not in ex:
                print(f"  [{col}] MISSING")
                continue
            raw = ex[col]
            extracted = extract_text(raw)
            print(f"\n[{col}]")
            print(f"  type: {type(raw).__name__}")
            if isinstance(raw, (list, dict)):
                print(f"  raw (truncated): {json.dumps(raw, ensure_ascii=False)[:300]}")
            print(f"  extracted: {extracted[:400]}")
        print()


if __name__ == "__main__":
    main()
