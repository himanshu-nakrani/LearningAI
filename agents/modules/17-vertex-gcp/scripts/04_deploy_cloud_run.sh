#!/usr/bin/env bash
# Deploy an ADK agent package to Cloud Run via ADK CLI.
# Usage:
#   ./modules/17-vertex-gcp/scripts/04_deploy_cloud_run.sh path/to/agent_dir [service_name]
set -euo pipefail

AGENT_DIR="${1:-}"
SERVICE_NAME="${2:-adk-course-agent}"
if [[ -z "${AGENT_DIR}" || ! -d "${AGENT_DIR}" ]]; then
  echo "Usage: $0 path/to/agent_dir [service_name]"
  exit 1
fi

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT}"
: "${GOOGLE_CLOUD_LOCATION:?Set GOOGLE_CLOUD_LOCATION}"

echo "Deploying ${AGENT_DIR} to Cloud Run service ${SERVICE_NAME}..."
adk deploy cloud_run \
  --project="${GOOGLE_CLOUD_PROJECT}" \
  --region="${GOOGLE_CLOUD_LOCATION}" \
  --service_name="${SERVICE_NAME}" \
  "${AGENT_DIR}"

echo "Done. Check Cloud Run URL in gcloud/console."
