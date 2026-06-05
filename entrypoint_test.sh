#!/bin/sh

echo "[INFO] Checking config file existing"
if [ ! -f "/app/data/config.yaml" ]; then
  echo "[WARN] Config file not found, copying default config..."
  cp /app/config.template.yaml /app/data/config.yaml
else
  echo "[INFO] Config file found, skipping copy."
fi

echo "[INFO] Starting Unit Tests"
exec python -m pytest