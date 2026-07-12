"""REFERENCE SOLUTION — Research Ops Assistant meeting deep-track R1–R9 patterns.

Compare against the learner package; do not submit this file as your only work.
"""

from __future__ import annotations

# Re-export the course package agent which already implements the deep track.
import sys
from pathlib import Path

_sys_parent = Path(__file__).resolve().parents[2]
if str(_sys_parent) not in sys.path:
    sys.path.insert(0, str(_sys_parent))

from research_ops_assistant.agent import root_agent  # noqa: E402

__all__ = ["root_agent"]
