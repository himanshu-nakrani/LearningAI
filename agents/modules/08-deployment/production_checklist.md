# Production readiness checklist

Copy this for each agent system you ship.

## Product

- [ ] Success metrics defined (task completion, CSAT, deflection)
- [ ] Out-of-scope behaviors documented
- [ ] Human escalation path exists

## Architecture

- [ ] Agent boundaries clear (single vs multi-agent justified)
- [ ] State keys documented
- [ ] Tool inventory reviewed (least privilege)
- [ ] Max steps / timeouts configured

## Reliability

- [ ] Eval set covers happy path + critical failures
- [ ] CI runs trajectory evals on PR
- [ ] Session backend is durable and multi-instance safe
- [ ] Idempotent tools for retries

## Security

- [ ] Secrets not in git
- [ ] Auth in front of agent endpoint
- [ ] Input validation on tools
- [ ] Prompt-injection review for untrusted content
- [ ] Audit log for sensitive actions

## Operations

- [ ] Structured logging + request IDs
- [ ] Dashboards for latency, errors, cost
- [ ] On-call runbook for model/tool outages
- [ ] Rollback plan (image pin / feature flag)

## Compliance

- [ ] Data retention policy for sessions
- [ ] PII handling reviewed
- [ ] Model safety settings documented
