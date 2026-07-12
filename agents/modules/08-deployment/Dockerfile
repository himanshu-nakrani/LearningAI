# Example production image for an ADK agent package.
# Build from course root:
#   docker build -f modules/08-deployment/Dockerfile -t adk-sample-agent .
#
# Run (API key required):
#   docker run --rm -e GOOGLE_API_KEY -p 8080:8080 adk-sample-agent

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy a small demo agent + this module's sample
COPY modules/08-deployment/sample_agent ./sample_agent

# Default: ADK API server pattern may vary by version.
# Prefer the documented `adk api_server` / deploy entrypoint for your ADK release.
# Fallback learning entry: run CLI is not ideal in containers; use api_server when available.
EXPOSE 8080

CMD ["sh", "-c", "adk api_server sample_agent --host 0.0.0.0 --port ${PORT} || adk web sample_agent --port ${PORT}"]
