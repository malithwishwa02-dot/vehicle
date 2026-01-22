# Aged Profile Generator 🔧

This utility creates a synthetic Chromium profile that appears "aged" — i.e., files and internal timestamps are backdated to simulate a profile that has been in use for some time. Useful for testing analytics, migration tools, parsers, and heuristics.

Quick start (Windows PowerShell):

- Create a demo profile (180 days old):

  python .\scripts\generate_aged_profile.py --out d:\vehicle\aged_profile_demo --age-days 180 --seed 42 --populate

Options:
- `--out` (required): output folder path for the generated profile
- `--age-days` (default 180): approximate age in days to apply to both file mtimes and DB timestamps
- `--seed` (default 42): RNG seed for reproducibility
- `--populate`: if provided, the script will try to execute any SQL dumps found in `reproduce_profile/dumps` to seed DBs

What it produces:
- `Default/History`, `Default/Cookies`, `Default/Login Data` sqlite DBs with synthetic rows and backdated timestamps
- `Local State` with a placeholder `os_crypt.encrypted_key`
- Files' modification times set to appear as if they were last used `--age-days` ago
- `AGED_PROFILE_README.md` summarizing the generation

Notes:
- This generator is intentionally non-sensitive: no real secrets are written, `encrypted_key` is a placeholder. Use only for testing and simulation.
- If you want to produce different distributions or types of data (e.g., more cookies, more logins), adjust the script's parameters.

---

See `scripts/generate_aged_profile.py` for implementation details.
