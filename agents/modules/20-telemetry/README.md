# Module 20 — Telemetry & Observability

**Time:** 2–3 hours · **Package:** `google.adk.telemetry`  
**Also:** OpenTelemetry (`opentelemetry-sdk` comes with google-adk)

## Objectives

- Enable ADK tracing for model and tool spans  
- Configure `TelemetryConfig` / env-based OTEL exporters  
- Know what to log vs what must never be logged (secrets, PII)  
- Connect to Google Cloud Trace or local OTLP  

---

## 1. ADK hooks

```python
from google.adk.telemetry import TelemetryConfig, tracer
from google.adk.telemetry.setup import maybe_set_otel_providers, OTelHooks
```

Common env vars:

| Env | Purpose |
|-----|---------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Generic OTLP collector |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Traces only |
| `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` | Include message content (careful!) |
| `OTEL_SERVICE_NAME` | Service name in traces |

---

## 2. Lab

```bash
python modules/20-telemetry/run_telemetry_demo.py
```

Prints span-oriented console output and shows how a plugin + runner produce observable steps.

### Exercises

1. Export spans to Jaeger/OTLP locally (Docker) using OTEL env vars.  
2. Add a plugin that increments a Prometheus-style counter (conceptual OK).  
3. Redact emails in logs before export.  

---

## 3. What to measure in production

| Signal | Why |
|--------|-----|
| Tool error rate | Broken integrations |
| p95 latency per tool | UX |
| Tokens / cost per request | Budget |
| Trajectory eval pass rate | Quality gate |
| Auth failures | Security |

---

## Checkpoint

1. Why is capturing full prompts in spans risky?  
2. Where does `TelemetryConfig` attach in ADK?  

## Next

→ [Module 21 — Code executors](../21-code-executors/README.md)
