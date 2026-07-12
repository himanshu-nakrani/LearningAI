"""Module 02 — Time agent lab.

Run:
  adk run modules/02-first-agent/time_agent
  adk web modules/02-first-agent --port 8000
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from google.adk.agents.llm_agent import Agent

# Mock / real hybrid: known cities map to IANA timezones.
CITY_TZ: dict[str, str] = {
    "new york": "America/New_York",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "paris": "Europe/Paris",
    "sydney": "Australia/Sydney",
    "san francisco": "America/Los_Angeles",
}


def get_current_time(city: str) -> dict:
    """Returns the current local time in a specified city.

    Args:
        city: Name of the city (e.g. "New York", "Tokyo", "London").

    Returns:
        A dict with keys:
          - status: "success" or "error"
          - city: normalized city name (on success)
          - time: human-readable local time string (on success)
          - timezone: IANA timezone (on success)
          - error_message: explanation (on error)
    """
    key = city.strip().lower()
    tz_name = CITY_TZ.get(key)
    if not tz_name:
        supported = ", ".join(sorted(CITY_TZ))
        return {
            "status": "error",
            "error_message": (
                f"No timezone data for '{city}'. "
                f"Supported cities: {supported}."
            ),
        }

    now = datetime.now(ZoneInfo(tz_name))
    return {
        "status": "success",
        "city": city.strip().title(),
        "time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "timezone": tz_name,
    }


def list_supported_cities() -> dict:
    """Lists cities this agent can report local time for.

    Returns:
        A dict with status and a list of city names.
    """
    cities = sorted(name.title() for name in CITY_TZ)
    return {"status": "success", "cities": cities}


root_agent = Agent(
    model="gemini-flash-latest",
    name="time_agent",
    description="Tells the current local time in supported world cities.",
    instruction="""
You are a precise world-clock assistant.

When the user asks for the time in a city:
1. Call get_current_time with that city.
2. If status is "success", reply in one short sentence with city and time.
3. If status is "error", apologize briefly and mention supported cities
   (you may call list_supported_cities).

When the user asks which cities you support, call list_supported_cities.

Rules:
- Never invent a time without calling get_current_time.
- Stay on topic (time and cities). For unrelated questions, politely redirect.
- Be concise and friendly.
""".strip(),
    tools=[get_current_time, list_supported_cities],
)
