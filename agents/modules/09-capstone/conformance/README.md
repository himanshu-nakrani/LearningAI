# Capstone conformance tests

## Why

Conformance testing freezes a **golden** trajectory (LLM requests, tool calls, session)
and fails CI when agent behavior drifts unexpectedly.

## Required for deep-track pass

1. Keep `research_ops_basic/spec.yaml` (provided).
2. Generate golden files on your machine:

```bash
# Terminal A — enable recordings plugin (flag may vary by ADK version)
adk web -v modules/09-capstone --port 8000

# Terminal B
adk conformance create modules/09-capstone/conformance/research_ops_basic
```

3. Confirm files exist:

```
conformance/research_ops_basic/
  spec.yaml
  generated-recordings.yaml   # generated
  generated-session.yaml      # generated
```

4. Run:

```bash
adk conformance test modules/09-capstone/conformance
# or
adk conformance test
```

5. Paste pass/fail summary into `SUBMISSION.md`.

## If `adk conformance` is unavailable

Document the ADK version and instead provide:

- `adk eval` results for `evals/research_ops.evalset.json`
- A manual trajectory log from Dev UI Trace for one happy-path session

That satisfies the **fallback** path but not full distinction.
