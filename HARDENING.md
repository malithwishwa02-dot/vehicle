# Repo Hardening Checklist

This document summarizes the automated hardening applied and next manual steps.

What I added:
- GitHub Actions: `.github/workflows/security.yml` — runs format checks, linting, bandit, dependency audits, tests. ✅
- CodeQL analysis workflow: `.github/workflows/codeql-analysis.yml` — static code scanning. ✅
- Dependabot: `.github/dependabot.yml` — weekly dependency update PRs. ✅
- Pre-commit: `.pre-commit-config.yaml` — black, isort, flake8, bandit, detect-secrets. ✅
- Dev requirements: `requirements-dev.txt` with tools used in CI. ✅
- Local hardening scripts: `scripts/harden.sh` and `scripts/harden.ps1`. ✅
- Security policy: `SECURITY.md`. ✅
- .gitignore updated to exclude generated profiles and environment files. ✅
- `deploy_to_mlx.py` updated to *skip* sensitive files by default when packaging. ✅

Recommended manual steps:
1. Remove sensitive runtime artifacts from repo and history:
   - git rm -r --cached generated_profiles/
   - Commit and push, or use BFG/Git filter-repo to purge historical files.
2. Run `scripts/harden.sh` locally and fix any issues reported.
3. Run `detect-secrets scan` and commit baseline if appropriate.
4. Update `CODEOWNERS` with your real security mailing list or team.
5. Consider storing golden profiles in a private artifact repository rather than in the git repo.

If you want, I can run the local hardening checks now and produce a report of failures to fix next.