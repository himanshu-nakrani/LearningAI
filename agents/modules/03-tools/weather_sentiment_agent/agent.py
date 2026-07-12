"""Module 03 — Weather + sentiment tools lab.

Run:
  adk run modules/03-tools/weather_sentiment_agent
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent


def get_weather_report(city: str) -> dict:
    """Retrieves a mock current weather report for a city.

    Args:
        city: City name such as London, Paris, or Tokyo.

    Returns:
        On success: {status, city, report, conditions}.
        On error: {status, error_message}.
    """
    catalog = {
        "london": {
            "report": (
                "Cloudy in London, 18°C, with a chance of light rain."
            ),
            "conditions": "rainy",
        },
        "paris": {
            "report": "Sunny in Paris, 25°C, clear skies.",
            "conditions": "sunny",
        },
        "tokyo": {
            "report": "Humid in Tokyo, 29°C, partly cloudy.",
            "conditions": "humid",
        },
        "new york": {
            "report": "Windy in New York, 22°C, overcast.",
            "conditions": "windy",
        },
    }
    key = city.strip().lower()
    if key not in catalog:
        return {
            "status": "error",
            "error_message": (
                f"Weather for '{city}' is not available in the demo dataset."
            ),
        }
    item = catalog[key]
    return {
        "status": "success",
        "city": city.strip().title(),
        "report": item["report"],
        "conditions": item["conditions"],
    }


def analyze_sentiment(text: str) -> dict:
    """Analyzes simple sentiment of user feedback text.

    Args:
        text: The user's free-text feedback.

    Returns:
        Dict with sentiment (positive|negative|neutral) and confidence.
    """
    lowered = text.lower()
    if any(w in lowered for w in ("good", "great", "love", "sunny", "nice")):
        return {"status": "success", "sentiment": "positive", "confidence": 0.8}
    if any(w in lowered for w in ("bad", "hate", "rain", "awful", "terrible")):
        return {"status": "success", "sentiment": "negative", "confidence": 0.75}
    return {"status": "success", "sentiment": "neutral", "confidence": 0.55}


def suggest_activity(conditions: str) -> dict:
    """Suggests an activity based on weather conditions keyword.

    Args:
        conditions: Short condition label such as rainy, sunny, windy, humid.

    Returns:
        A suggested activity string with status.
    """
    ideas = {
        "rainy": "Visit a museum or a cozy café.",
        "sunny": "Take a walk in a park or outdoor café.",
        "windy": "Try an indoor climbing gym or a bookstore crawl.",
        "humid": "Find air-conditioned attractions or a short morning outing.",
    }
    key = conditions.strip().lower()
    idea = ideas.get(key, "Check a local events app for indoor options.")
    return {"status": "success", "conditions": key, "suggestion": idea}


root_agent = Agent(
    model="gemini-flash-latest",
    name="weather_sentiment_agent",
    description=(
        "Provides demo weather reports, analyzes user sentiment, "
        "and suggests activities."
    ),
    instruction="""
You help users with demo weather information.

Workflow:
1. If the user asks about weather in a city, call get_weather_report.
2. On success, share the report clearly.
3. Optionally call suggest_activity using the conditions field from the tool.
4. If the user then gives emotional feedback about the weather, call
   analyze_sentiment and briefly acknowledge their sentiment.
5. On weather errors, explain unavailability and invite another city.

Rules:
- Always use tools for weather, sentiment, and activity suggestions.
- Do not invent weather data.
- Keep replies concise (2–5 sentences).
""".strip(),
    tools=[get_weather_report, analyze_sentiment, suggest_activity],
)
