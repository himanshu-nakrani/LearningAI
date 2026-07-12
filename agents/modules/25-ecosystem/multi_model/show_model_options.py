#!/usr/bin/env python3
"""Print model integration options for ADK (no network required)."""

OPTIONS = [
    ("Gemini string", 'LlmAgent(model="gemini-flash-latest", ...)'),
    ("Vertex", "GOOGLE_GENAI_USE_VERTEXAI=TRUE + ADC"),
    ("LiteLLM", "LiteLlm(model='openai/gpt-4o-mini')  # pip install litellm"),
    ("Ollama", "Local OpenAI-compatible endpoint via connector"),
    ("vLLM", "Self-hosted high throughput"),
    ("Model routing", "Failover / A-B between models — see adk.dev models/routing"),
]


def main() -> None:
    print("ADK model integration options:\n")
    for name, snippet in OPTIONS:
        print(f"- {name}: {snippet}")
    print("\nPick cheaper models for routers; stronger models for hard writing/reasoning.")


if __name__ == "__main__":
    main()
