"""Code-execution calculator agent."""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="calculator_agent",
    description="Solves math using the built-in code executor.",
    code_executor=BuiltInCodeExecutor(),
    instruction="""
You are a calculator agent.
When given a mathematical expression, write and execute Python code.
Return only the final numerical result as plain text when possible.
""".strip(),
)
