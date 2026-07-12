#!/usr/bin/env bash
# Deploy an ADK agent package to Agent Runtime (Agent Engine).
# Usage:
#   ./modules/17-vertex-gcp/scripts/03_deploy_agent_engine.sh path/to/agent_dir
set -euo pipefail

AGENT_DIR="${1:-}"
if [[ -z "${AGENT_DIR}" || ! -d "${AGENT_DIR}" ]]; then
  echo "Usage: $0 path/to/agent_dir"
  exit 1
fi

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT}"
: "${GOOGLE_CLOUD_LOCATION:?Set GOOGLE_CLOUD_LOCATION}"

STAGING_BUCKET="${STAGING_BUCKET:-gs://${GOOGLE_CLOUD_PROJECT}-adk-staging}"
DISPLAY_NAME="${DISPLAY_NAME:-adk-course-agent}"

echo "Ensuring staging bucket exists: ${STAGING_BUCKET}"
if ! gsutil ls "${STAGING_BUCKET}" &>/dev/null; then
  gsutil mb -l "${GOOGLE_CLOUD_LOCATION}" "${STAGING_BUCKET}" || true
fi

echo "Deploying ${AGENT_DIR} as ${DISPLAY_NAME}..."
adk deploy agent_engine \
  --project="${GOOGLE_CLOUD_PROJECT}" \
  --region="${GOOGLE_CLOUD_LOCATION}" \
  --staging_bucket="${STAGING_BUCKET}" \
  --display_name="${DISPLAY_NAME}" \
  "${AGENT_DIR}"

echo "Deploy submitted. Capture AGENT_ENGINE_ID from console/CLI output."
