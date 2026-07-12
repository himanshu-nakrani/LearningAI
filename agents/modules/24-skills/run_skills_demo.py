#!/usr/bin/env python3
"""Load a skill from disk using google.adk.skills."""

from __future__ import annotations

from pathlib import Path

from google.adk.skills import load_skill_from_dir

SKILL_DIR = Path(__file__).resolve().parent / "skills_repo" / "research-brief"


def main() -> None:
    skill = load_skill_from_dir(str(SKILL_DIR))
    fm = skill.frontmatter
    print("Loaded skill:", getattr(fm, "name", fm))
    print("Description:", getattr(fm, "description", None))
    print("Instructions preview:\n", (skill.instructions or "")[:400])
    print("OK — skill package load works")
    print(
        "Note: SkillRegistry is abstract; agents typically load skills from dirs "
        "or a concrete registry implementation."
    )


if __name__ == "__main__":
    main()
