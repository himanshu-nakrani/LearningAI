# Synthetic Instruction Dataset Generation

High-quality instruction-response dataset generation using large language models on Modal.

## Overview

Generate diverse, high-quality instruction-following examples for fine-tuning smaller models.

**Target:** 10,000 instruction-response pairs  
**Model:** Qwen 2.5 72B Instruct (best open-source as of May 2026)  
**Time:** ~2-3 hours on B200  
**Cost:** ~$10-15  

## Dataset Categories

1. **Coding & Programming** (25%)
   - Algorithm implementation
   - Code explanation
   - Debugging assistance
   - Best practices

2. **Mathematics & Reasoning** (20%)
   - Problem solving
   - Step-by-step explanations
   - Word problems
   - Logic puzzles

3. **Creative Writing** (15%)
   - Story generation
   - Poetry
   - Content creation
   - Dialogue writing

4. **Technical Explanation** (20%)
   - Concept explanations
   - How-to guides
   - Comparisons
   - Tutorials

5. **Professional Communication** (10%)
   - Email drafting
   - Report writing
   - Presentations
   - Documentation

6. **General Knowledge & QA** (10%)
   - Factual questions
   - Explanations
   - Summaries
   - Analysis

## Quality Criteria

- Clear, specific instructions
- Detailed, helpful responses
- Diverse topics and formats
- Natural language variation
- Appropriate length (50-500 tokens)
- No toxic or harmful content

## Pipeline Steps

1. **Seed Generation** - Create diverse instruction seeds
2. **Instruction Expansion** - Generate full instructions
3. **Response Generation** - Generate high-quality responses
4. **Quality Filtering** - Remove low-quality examples
5. **Deduplication** - Remove near-duplicates
6. **Formatting** - Convert to HuggingFace dataset format
7. **Upload** - Push to HuggingFace Hub

## Usage

```bash
# Generate dataset
modal run generate_dataset.py::generate --num_examples 10000

# Quality check
modal run generate_dataset.py::quality_check

# Upload to HuggingFace
modal run generate_dataset.py::upload_to_hub
```

## Output Format

```json
{
  "instruction": "Explain how binary search works with a simple example.",
  "response": "Binary search is an efficient algorithm...",
  "category": "coding",
  "difficulty": "medium",
  "metadata": {
    "model": "Qwen/Qwen2.5-72B-Instruct",
    "temperature": 0.7,
    "generated_at": "2026-05-31"
  }
}
```

## Expected Output

- **Total examples:** 10,000
- **Average instruction length:** 20-50 tokens
- **Average response length:** 150-400 tokens
- **Dataset size:** ~50-80MB (JSON)
- **Quality score:** >90% (human evaluation on sample)
