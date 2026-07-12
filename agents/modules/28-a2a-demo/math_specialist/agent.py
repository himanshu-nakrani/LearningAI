"""Math specialist — served over A2A from serve_math_specialist.py."""

from google.adk.agents.llm_agent import Agent


def add(a: float, b: float) -> dict:
    """Add two numbers exactly.

    Args:
        a: First addend.
        b: Second addend.
    """
    return {"status": "success", "sum": a + b}


def multiply(a: float, b: float) -> dict:
    """Multiply two numbers exactly.

    Args:
        a: First factor.
        b: Second factor.
    """
    return {"status": "success", "product": a * b}


root_agent = Agent(
    model="gemini-flash-latest",
    name="math_specialist",
    description="Remote math specialist that adds and multiplies numbers.",
    instruction="""
You are a math specialist exposed over A2A.
For arithmetic, call add or multiply tools. Reply with the numeric result clearly.
""".strip(),
    tools=[add, multiply],
)
