# Module 24 — Agent Skills

**Time:** 2 hours · **Package:** `google.adk.skills`

## Objectives

- Load skills from a directory (`SKILL.md` + frontmatter)  
- Register skills in `SkillRegistry`  
- Keep instructions lean by packing procedures into skills  

---

## Skill layout

```
skills_repo/research-brief/
  SKILL.md
```

`SKILL.md` example frontmatter + body (agentskills-style).

```python
from google.adk.skills import load_skill_from_dir, SkillRegistry

skill = load_skill_from_dir("path/to/research-brief")
registry = SkillRegistry()
# registry APIs: get_skill / search_skills — see installed package
```

---

## Lab

```bash
python modules/24-skills/run_skills_demo.py
adk run modules/24-skills/skill_agent   # agent instructed to follow skill steps
```

### Exercises

1. Add a second skill `incident-triage`.  
2. Measure prompt size with vs without inlined skill text.  

## Next

→ [Module 25 — Ecosystem](../25-ecosystem/README.md)
