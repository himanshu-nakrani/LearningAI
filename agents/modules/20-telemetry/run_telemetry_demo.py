#!/usr/bin/env python3
"""Show ADK + OpenTelemetry wiring and a traced tool call path."""

from __future__ import annotations

import asyncio
import os

from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai.types import Content, Part
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


def setup_console_tracing() -> None:
    resource = Resource.create({"service.name": "adk-course-telemetry-demo"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)


def traced_add(a: int, b: int, tool_context: ToolContext) -> dict:
    """Adds two integers inside a custom OTEL span."""
    tracer = trace.get_tracer("adk.course.telemetry")
    with tracer.start_as_current_span("traced_add") as span:
        span.set_attribute("args.a", a)
        span.set_attribute("args.b", b)
        result = a + b
        span.set_attribute("result", result)
        return {"status": "success", "sum": result}


root_agent = Agent(
    model="gemini-flash-latest",
    name="telemetry_math_agent",
    instruction="Use traced_add for addition questions. Be brief.",
    tools=[traced_add],
)


async def main() -> None:
    setup_console_tracing()
    print("Console span exporter enabled (service.name=adk-course-telemetry-demo)\n")

    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print("No API key — emitting a manual span only")
        tracer = trace.get_tracer("adk.course.telemetry")
        with tracer.start_as_current_span("offline_demo"):
            print(traced_add(2, 40, None))  # type: ignore[arg-type]
        return

    sessions = InMemorySessionService()
    await sessions.create_session(app_name="tel", user_id="u", session_id="s", state={})
    runner = Runner(agent=root_agent, app_name="tel", session_service=sessions)
    msg = Content(role="user", parts=[Part(text="What is 19 + 23?")])
    async for event in runner.run_async(user_id="u", session_id="s", new_message=msg):
        if event.is_final_response() and event.content and event.content.parts:
            print("AGENT:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
