#!/bin/bash
# Railway startup script

# Use Railway's PORT or default to 8000
export PORT=${PORT:-8000}

echo "Starting uvicorn on port $PORT"
exec uvicorn backend.app:app --host 0.0.0.0 --port $PORT
