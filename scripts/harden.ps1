Write-Host "[HARDEN] Installing dev dependencies..."
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

Write-Host "[HARDEN] Running pre-commit hooks..."
pre-commit run --all-files -v

Write-Host "[HARDEN] Running static analysis"
black --check .
isort --check-only .
flake8
bandit -r . -x .venv,generated_profiles

Write-Host "[HARDEN] Running dependency checks"
pip-audit -r requirements.txt
safety check -r requirements.txt

Write-Host "[HARDEN] Complete — review output and fix any failures."