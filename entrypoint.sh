#!/bin/sh

echo "[INFO] Checking config file existing"
if [ ! -f "/app/data/config.yaml" ]; then
  echo "[WARN] Config file not found, copying default config..."
  cp /app/config.template.yaml /app/data/config.yaml
else
  echo "[INFO] Config file found, skipping copy."
fi

echo "[INFO] Checking 404.html file existing"
if [ ! -f "/app/data/templates/404.html" ]; then
  echo "[WARN] 404.html file not found, copying default..."
  mkdir -p /app/data/templates
  cp /app/404.template.html /app/data/templates/404.html
else
  echo "[INFO] 404.html file found, skipping copy."
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
