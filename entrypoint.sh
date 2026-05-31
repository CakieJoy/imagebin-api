#!/usr/bin/bash

#!/bin/sh

# Geçici klasördeki güncel kaynak kodları,
# dışarıdan bağlanan /app klasörünün içine kopyala (mevcut config ve uploadlara dokunmaz)
echo "Source code copying on volume"
cp -r /app_tmp/. /app/

# Sunucuyu başlat
echo "Starting API"
exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 1 \
  --loop uvloop \
  --http httptools \
  --no-access-log \
  --limit-concurrency 1000 \
  --timeout-keep-alive 10
