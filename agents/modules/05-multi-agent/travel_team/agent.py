"""Module 05 — Hierarchical multi-agent travel team.

Run:
  adk run modules/05-multi-agent/travel_team
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext


def save_flight_options(
    destination: str,
    summary: str,
    tool_context: ToolContext,
) -> dict:
    """Stores flight recommendation summary in session state.

    Args:
        destination: Trip destination city or country.
        summary: Concise flight options the specialist recommends.
        tool_context: Injected by ADK.

    Returns:
        Status and stored payload.
    """
    payload = {"destination": destination, "summary": summary}
    tool_context.state["flights"] = payload
    return {"status": "success", "flights": payload}


def save_hotel_options(
    destination: str,
    summary: str,
    tool_context: ToolContext,
) -> dict:
    """Stores hotel recommendation summary in session state.

    Args:
        destination: Trip destination.
        summary: Concise hotel options.
        tool_context: Injected by ADK.

    Returns:
        Status and stored payload.
    """
    payload = {"destination": destination, "summary": summary}
    tool_context.state["hotels"] = payload
    return {"status": "success", "hotels": payload}


def save_itinerary(
    destination: str,
    plan: str,
    tool_context: ToolContext,
) -> dict:
    """Stores the day-by-day itinerary in session state.

    Args:
        destination: Trip destination.
        plan: Multi-day itinerary text.
        tool_context: Injected by ADK.

    Returns:
        Status and stored plan.
    """
    payload = {"destination": destination, "plan": plan}
    tool_context.state["itinerary"] = payload
    return {"status": "success", "itinerary": payload}


flight_specialist = Agent(
    model="gemini-flash-latest",
    name="flight_specialist",
    description="Finds and summarizes plausible flight options for a destination.",
    instruction="""
You are a flight specialist (demo — no live booking APIs).
Given the user's trip request, invent 2-3 realistic *demo* flight options
(airline-style names, rough times, cabin). Keep it clearly fictional.

After composing the summary, call save_flight_options with destination and summary.
Reply to the user with the same summary briefly.
""".strip(),
    tools=[save_flight_options],
)

hotel_specialist = Agent(
    model="gemini-flash-latest",
    name="hotel_specialist",
    description="Recommends demo hotels matching budget and interests.",
    instruction="""
You are a hotel specialist (demo data only).
Propose 2-3 fictional hotels with area, vibe, and rough price band.
Call save_hotel_options with destination and summary, then present them.
""".strip(),
    tools=[save_hotel_options],
)

itinerary_specialist = Agent(
    model="gemini-flash-latest",
    name="itinerary_specialist",
    description="Builds a day-by-day itinerary using saved flights and hotels.",
    instruction="""
You create trip itineraries.

State available:
- Flights: {flights?}
- Hotels: {hotels?}

If flights or hotels are missing, say what is missing and suggest the coordinator
gather them first.

Otherwise draft a day-by-day plan that references the chosen areas/hotels and
interests from the user. Call save_itinerary, then show the plan.
""".strip(),
    tools=[save_itinerary],
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="travel_coordinator",
    description="Coordinates flight, hotel, and itinerary specialists for trip planning.",
    instruction="""
You are the travel coordinator for a multi-agent demo.

Sub-agents:
- flight_specialist — flights
- hotel_specialist — lodging
- itinerary_specialist — day plans (needs flights + hotels in state)

Process for a new trip request:
1. Clarify destination, duration, interests, budget if missing (ask briefly).
2. Transfer / delegate to flight_specialist first.
3. Then hotel_specialist.
4. Then itinerary_specialist to synthesize.
5. Return a final consolidated answer to the user.

Be explicit when handing off. Do not invent flights/hotels yourself —
use specialists. Keep the experience friendly and structured.
""".strip(),
    sub_agents=[flight_specialist, hotel_specialist, itinerary_specialist],
)
