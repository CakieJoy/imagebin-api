#!/bin/sh

echo "[INFO] Checking config file existing"
if [ ! -f "/app/data/config.yaml" ]; then
  echo "[WARN] Config file not found, copying default config..."
  cp /app/config.template.yaml /app/data/config.yaml
else
  echo "[INFO] Config file found, skipping copy."
fi

echo "[INFO] Starting API"
exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 1 \
  --loop uvloop \
  --http httptools \
  --no-access-log \
  --limit-concurrency 1000 \
  --timeout-keep-alive 10
