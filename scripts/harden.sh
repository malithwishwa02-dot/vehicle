#!/usr/bin/env bash
set -euo pipefail

echo "[HARDEN] Installing dev dependencies..."
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

echo "[HARDEN] Running pre-commit hooks..."
pre-commit run --all-files || true

echo "[HARDEN] Running static analysis"
black --check . || true
isort --check-only . || true
flake8 || true
bandit -r . -x .venv,generated_profiles || true

echo "[HARDEN] Running dependency checks"
pip-audit -r requirements.txt || true
safety check -r requirements.txt || true

echo "[HARDEN] Complete — review output and fix any failures."