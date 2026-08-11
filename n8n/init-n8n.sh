#!/bin/sh

# Path to the marker file that indicates if auto-import has already run
MARKER_FILE="/home/node/.n8n/init_done"

if [ ! -f "$MARKER_FILE" ]; then
  echo "First run detected. Preparing to import workflows and credentials..."

  # Generate temporary credentials JSON file if API key is provided
  # Support IA_API_KEY, GEMINI_API_KEY, and legacy groq_key
  ACTIVE_KEY="${IA_API_KEY:-${GEMINI_API_KEY:-$groq_key}}"

  if [ -n "$ACTIVE_KEY" ]; then
    echo "AI API Key is defined. Generating credentials JSON..."
    cat <<EOF > /tmp/credentials.json
[
  {
    "id": "gemini-api-cred-id",
    "name": "Google Gemini account",
    "type": "googlePalmApi",
    "data": {
      "host": "https://generativelanguage.googleapis.com",
      "apiKey": "${ACTIVE_KEY}"
    }
  }
]
EOF
    echo "Importing Gemini credentials..."
    n8n import:credentials --input=/tmp/credentials.json
    rm -f /tmp/credentials.json
  else
    echo "WARNING: IA_API_KEY, GEMINI_API_KEY, or groq_key is not defined. Credentials will not be pre-configured."
  fi

  # Import workflow
  if [ -f "/etc/n8n/flujo.json" ]; then
    echo "Importing n8n workflow from /etc/n8n/flujo.json..."
    n8n import:workflow --input=/etc/n8n/flujo.json
    
    echo "Activating workflow 1..."
    n8n publish:workflow --id=1
  else
    echo "ERROR: /etc/n8n/flujo.json not found!"
  fi

  # Touch the marker file to prevent importing again on subsequent restarts
  touch "$MARKER_FILE"
  echo "Initialization complete."
else
  echo "Auto-import already completed previously. Skipping."
fi

# Start n8n normally
echo "Starting n8n..."
exec n8n start
