export PYTHONPATH=src
# uv run uvicorn mockup.nf:app \
#     --host 0.0.0.0 \
#     --port 8081 \
#     # --reload \
#     --log-config "$(dirname "$0")/log_config.ini"

uv run -m mockup.nf
