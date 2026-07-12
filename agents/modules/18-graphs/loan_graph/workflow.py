"""Loan approval graph — pure FunctionNodes + conditional routes."""

from __future__ import annotations

from google.adk.agents.context import Context
from google.adk.workflow import START, FunctionNode, Workflow


def parse_amount(ctx: Context) -> dict:
    """Parse a dollar amount from the latest user message into state."""
    text = ""
    session = ctx._invocation_context.session
    for event in reversed(list(session.events or [])):
        content = getattr(event, "content", None)
        if content and getattr(content, "role", None) == "user":
            parts = content.parts or []
            if parts and parts[0].text:
                text = parts[0].text
                break
    digits = "".join(c for c in text if c.isdigit())
    amount = int(digits) if digits else int(ctx.state.get("amount", 5000))
    ctx.state["amount"] = amount
    return {"amount": amount}


def score_risk(ctx: Context, amount: int = 0) -> dict:
    """Score risk band and emit route low|high."""
    amount = amount or int(ctx.state.get("amount", 0))
    band = "low" if amount < 10_000 else "high"
    ctx.state["band"] = band
    ctx.route = band
    return {"amount": amount, "band": band}


def approve_low(ctx: Context, amount: int = 0) -> dict:
    """Auto-approve low-risk loans."""
    amount = amount or int(ctx.state.get("amount", 0))
    decision = {
        "decision": "auto_approve",
        "amount": amount,
        "reason": "Amount under 10000 threshold.",
    }
    ctx.state["decision"] = decision
    return decision


def review_high(ctx: Context, amount: int = 0) -> dict:
    """Send high-risk loans to human review."""
    amount = amount or int(ctx.state.get("amount", 0))
    decision = {
        "decision": "human_review",
        "amount": amount,
        "reason": "Amount at or above 10000 threshold.",
    }
    ctx.state["decision"] = decision
    return decision


parse_node = FunctionNode(func=parse_amount, name="parse_amount")
score_node = FunctionNode(func=score_risk, name="score_risk")
approve_node = FunctionNode(func=approve_low, name="approve_low")
review_node = FunctionNode(func=review_high, name="review_high")

loan_workflow = Workflow(
    name="loan_graph",
    description="Parse amount, score risk, branch to approve or human review.",
    edges=[
        (START, parse_node),
        (parse_node, score_node),
        (score_node, {"low": approve_node, "high": review_node}),
    ],
)
