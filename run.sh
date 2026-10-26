#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ ! -f frontend/dist/index.html ]; then
  (cd frontend && npm ci && npm run build)
fi
exec python3 -m flood_drone.server --port 8106
