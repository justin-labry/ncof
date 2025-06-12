export PYTHONPATH=src
uv run uvicorn mockup.amf:app \
    --host 0.0.0.0 \
    --port 8082 \
    --reload \
    --log-config "$(dirname "$0")/log_config.ini"
