"""Offline tests for capstone plugin + HITL-style tools (no LLM)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from plugins.research_ops_plugin import ResearchOpsPlugin  # noqa: E402


def test_plugin_constructs():
    p = ResearchOpsPlugin()
    assert p.name == "research_ops_plugin"
    assert p.agent_count == 0


def test_knowledge_search_hit_and_miss():
    sys.path.insert(0, str(ROOT / "research_ops_assistant"))
    from agent import search_knowledge_base

    hit = search_knowledge_base("evaluation")
    assert hit["status"] == "success"
    miss = search_knowledge_base("quantum teleportation recipes")
    assert miss["status"] == "error"
