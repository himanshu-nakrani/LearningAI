#!/usr/bin/env python3
"""Human-in-the-loop refund approval stub (no LLM required)."""

from __future__ import annotations


class FakeState(dict):
    pass


def request_refund(order_id: str, amount: float, state: dict) -> dict:
    """Opens a pending refund that must be approved."""
    if amount <= 0:
        return {"status": "error", "error_message": "amount must be positive"}
    state["pending_refund"] = {
        "order_id": order_id,
        "amount": amount,
        "status": "pending_approval",
    }
    return {
        "status": "pending_approval",
        "message": "Refund staged. Call approve_refund with decision=approve|reject.",
        "pending": state["pending_refund"],
    }


def approve_refund(decision: str, state: dict) -> dict:
    """Completes or cancels a pending refund (human gate)."""
    pending = state.get("pending_refund")
    if not pending or pending.get("status") != "pending_approval":
        return {"status": "error", "error_message": "No pending refund to approve."}
    decision = decision.strip().lower()
    if decision not in {"approve", "reject"}:
        return {"status": "error", "error_message": "decision must be approve|reject"}
    pending["status"] = "approved" if decision == "approve" else "rejected"
    state["last_refund_result"] = pending
    state.pop("pending_refund", None)
    return {"status": "success", "result": pending}


def main() -> None:
    state: dict = {}
    print(request_refund("ORD-9", 42.5, state))
    print("pending:", state)
    print(approve_refund("approve", state))
    print("final:", state)
    print(approve_refund("approve", state))  # should error


if __name__ == "__main__":
    main()
