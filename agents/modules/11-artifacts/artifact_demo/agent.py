"""CLI-facing artifact-aware agent (needs artifact_service at runtime)."""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="artifact_demo",
    description="Explains artifacts and how this course stores binary data.",
    instruction="""
You teach ADK Artifacts.
Explain: Part+Blob, versioning, session vs user: filenames, and
InMemoryArtifactService vs GcsArtifactService.
If the user asks to save files, remind them to run run_artifact_demo.py
which wires artifact_service into the Runner.
""".strip(),
)
