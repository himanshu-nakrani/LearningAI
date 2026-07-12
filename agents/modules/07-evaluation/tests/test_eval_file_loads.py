"""Smoke tests that do not call the live model."""

from __future__ import annotations

import json
from pathlib import Path

EVALS = Path(__file__).resolve().parents[1] / "evals"


def test_evalset_json_is_valid():
    path = EVALS / "weather_basic.evalset.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["eval_set_id"] == "weather_sentiment_basic"
    assert len(data["eval_cases"]) >= 1
    case = data["eval_cases"][0]
    assert "conversation" in case
    assert case["conversation"][0]["user_content"]["parts"][0]["text"]


def test_test_config_has_criteria():
    path = EVALS / "test_config.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "criteria" in data
    assert "tool_trajectory_avg_score" in data["criteria"]
