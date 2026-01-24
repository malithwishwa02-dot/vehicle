# Windows CI & Build Guide

This document explains the Windows CI workflow and optional automation for bundling RunAsDate.exe and Firefox for a portable `LucidEmpire.exe`.

## GitHub Actions Workflow
- Workflow: `/.github/workflows/windows-build.yml`
- What it does:
  - Installs Python and requirements
  - Installs Playwright browsers (Firefox)
  - Optionally downloads `RunAsDate.exe` if `RUN_AS_DATE_URL` secret is set
  - Runs `pyinstaller build_exe.spec` to produce `dist/LucidEmpire.exe`
  - Runs a smoke check: `python windows/lucid_launcher.py --check`
  - Uploads `dist/LucidEmpire.exe` as an artifact

## Secrets
- `RUN_AS_DATE_URL` (optional): a direct download URL for `RunAsDate.exe`. Due to distributor policies, prefer a vetted private URL or manual upload.

## Local Build Notes
- After installing Playwright and running `python -m playwright install firefox`, a helper script is available:
  - `scripts\copy_playwright_firefox.ps1` — copies Playwright's Firefox binaries into `bin\firefox` for portability (run on Windows host).
- You can also use `scripts\fetch_runasdate.ps1 -Url <url>` to download `RunAsDate.exe` into `./bin`.

## CI-friendly checks
- The launcher supports `--check` (exits 0 on success) so the workflow can validate the presence of `bin\RunAsDate.exe` and `bin\firefox\firefox.exe` without launching a GUI.

## Security & Compliance
- Do not store or expose untrusted binaries publicly. Use repository secrets or a private URL for `RUN_AS_DATE_URL`.
- Verify any third-party binary's checksum and licensing before bundling into a distributed EXE.
