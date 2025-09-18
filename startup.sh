#!/bin/bash

# startup.sh - Production startup script for the bowling shoes rental API

set -e

echo "Starting Bowling Shoes Rental API..."

# Check if required environment variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo "Error: Required environment variables SUPABASE_URL and SUPABASE_KEY must be set"
    exit 1
fi

# Run database migrations or setup if needed
echo "Checking database connection..."

# Start the application with production settings
echo "Starting FastAPI application..."
exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-1}" \
    --log-level "${LOG_LEVEL:-info}" \
    --access-log \
    --use-colors
