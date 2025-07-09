#!/bin/bash
export PYTHONPATH=src
# export UV_PROJECT_ENVIRONMENT=.venv
uv run uvicorn openapi_server.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --reload \
    --log-config "$(dirname "$0")/log_config.ini" 

# uv run -m openapi_server.main
