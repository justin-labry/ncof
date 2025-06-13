export PYTHONPATH=src
uv run uvicorn mockup.smf:app \
    --host 0.0.0.0 \
    --port 8083 \
    --reload \
    --log-config "$(dirname "$0")/log_config.ini"
