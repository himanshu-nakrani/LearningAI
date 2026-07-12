"""Module 06 — Agent with PlanReAct-style multi-step tools.

Run:
  adk run modules/06-advanced/planning_agent
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent

try:
    from google.adk.planners import PlanReActPlanner

    _PLANNER = PlanReActPlanner()
except Exception:  # pragma: no cover - older ADK builds
    _PLANNER = None


def lookup_company(name: str) -> dict:
    """Looks up a demo company profile by name.

    Args:
        name: Company name, e.g. "NovaTech" or "GreenGrid".

    Returns:
        Profile dict or error.
    """
    db = {
        "novatech": {
            "name": "NovaTech",
            "sector": "enterprise software",
            "hq": "Austin",
            "employees": 1200,
        },
        "greengrid": {
            "name": "GreenGrid",
            "sector": "renewable energy",
            "hq": "Copenhagen",
            "employees": 450,
        },
    }
    key = name.strip().lower()
    if key not in db:
        return {"status": "error", "error_message": f"Unknown company '{name}'."}
    return {"status": "success", "profile": db[key]}


def estimate_risk(sector: str, employees: int) -> dict:
    """Estimates a demo operational risk score.

    Args:
        sector: Industry sector string.
        employees: Headcount.

    Returns:
        Risk band and numeric score.
    """
    base = 0.3
    if "energy" in sector.lower():
        base += 0.2
    if employees > 1000:
        base += 0.15
    score = min(base, 0.95)
    band = "low" if score < 0.4 else "medium" if score < 0.7 else "high"
    return {
        "status": "success",
        "score": round(score, 2),
        "band": band,
        "sector": sector,
        "employees": employees,
    }


_kwargs = dict(
    model="gemini-flash-latest",
    name="planning_agent",
    description="Researches demo companies and estimates operational risk.",
    instruction="""
You analyze demo companies using tools.

For questions about a company:
1. Call lookup_company.
2. On success, call estimate_risk with sector and employees from the profile.
3. Summarize profile + risk band for the user.

Never invent company data if the lookup fails — say it is unknown.
Think step-by-step before acting.
""".strip(),
    tools=[lookup_company, estimate_risk],
)

if _PLANNER is not None:
    _kwargs["planner"] = _PLANNER

root_agent = Agent(**_kwargs)
