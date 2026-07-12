#!/usr/bin/env bash
# Source this file after editing values:
#   source modules/17-vertex-gcp/scripts/02_set_env.sh

export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-YOUR_PROJECT_ID}"
export GOOGLE_CLOUD_LOCATION="${GOOGLE_CLOUD_LOCATION:-us-central1}"

# From Agent Runtime / Reasoning Engine create flow:
export AGENT_ENGINE_ID="${AGENT_ENGINE_ID:-}"

# Unset AI Studio key mode for Vertex-only runs (optional):
# unset GOOGLE_API_KEY

echo "Vertex env:"
echo "  GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI}"
echo "  GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}"
echo "  GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}"
echo "  AGENT_ENGINE_ID=${AGENT_ENGINE_ID:-<empty>}"
