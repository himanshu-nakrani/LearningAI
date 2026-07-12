#!/usr/bin/env bash
# Enable common APIs for ADK + Vertex Agent Platform workflows.
set -euo pipefail

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null)}"
if [[ -z "${PROJECT_ID}" || "${PROJECT_ID}" == "(unset)" ]]; then
  echo "Set GOOGLE_CLOUD_PROJECT or gcloud config set project ..."
  exit 1
fi

echo "Enabling APIs on project: ${PROJECT_ID}"

gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  secretmanager.googleapis.com \
  --project="${PROJECT_ID}"

echo "Done. Verify: gcloud services list --enabled --project=${PROJECT_ID}"
