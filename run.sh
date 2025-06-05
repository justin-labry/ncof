#!/bin/bash
# PYTHONPATH=src uv run uvicorn openapi_server.main:app --host 0.0.0.0 --port 8080 --reload --log-config log_config.ini

export PYTHONPATH=src
uv run uvicorn openapi_server.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --reload \
    --log-config "$(dirname "$0")/log_config.ini"
