#!/usr/bin/env bash
# One-Click Demo for Lucid Empire (safe-by-default)
# Usage: ./scripts/one_click_demo.sh [--with-docker] [--check]

set -euo pipefail
SELF=$(realpath "$0")
ROOT=$(dirname "$SELF")/..
cd "$ROOT"

WITH_DOCKER=0
CHECK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-docker) WITH_DOCKER=1; shift ;;
    --check) CHECK=1; shift ;;
    -h|--help) echo "Usage: $0 [--with-docker] [--check]"; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [[ $CHECK -eq 1 ]]; then
  echo "DRY-RUN: One-Click Demo would perform the following steps:"
  echo "  1) pip install -r requirements.txt"
  echo "  2) (optional) docker build -t lucid-browser:v5 -f LUCID-EMPIRE/runtime/Dockerfile ."
  echo "  3) Run forensic verification: pytest -q tests/verify_sovereignty.py"
  echo "  4) Start Mission Control dashboard: python3 LUCID-EMPIRE/app.py"
  echo
  echo "To run for real, re-run without --check. To include Docker operations add --with-docker."
  exit 0
fi

echo "[1/4] Installing Python dependencies (this may modify your environment)"
python3 -m pip install -r requirements.txt

if [[ $WITH_DOCKER -eq 1 ]]; then
  echo "[2/4] Building the time-shifted runtime Docker image"
  docker build -t lucid-browser:v5 -f LUCID-EMPIRE/runtime/Dockerfile .
else
  echo "[2/4] Skipping Docker build (run with --with-docker to enable)"
fi

echo "[3/4] Running the forensic verification suite (safe by default)"
pytest -q tests/verify_sovereignty.py || {
  echo "Verification failed. Check tests/verify_sovereignty.py output."; exit 1
}

echo "[4/4] Launching the Mission Control dashboard (background)"
if pgrep -f "LUCID-EMPIRE/app.py" >/dev/null 2>&1; then
  echo "Dashboard already running"
else
  nohup python3 LUCID-EMPIRE/app.py >/tmp/lucid_dashboard.log 2>&1 &
  sleep 1
  echo "Dashboard started; tail /tmp/lucid_dashboard.log to see logs."
fi

echo
echo "✅ Lucid Empire demo launched. Visit: http://localhost:1337"
