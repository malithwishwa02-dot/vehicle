# Profile Analysis Package 📂

This folder collects all extracted artifacts, readable exports, and helper scripts for researching and reproducing the `37ab1612-c285-4314-b32a-6a06d35d6d84` Chromium profile.

Structure
- `reports/` — human-readable reports and summaries (markdown/PDF). ✅
- `data/` — CSV and JSON exports used for analysis (cookies, logins, autofill, inventory). ✅
- `scripts/` — Python utilities to load, inspect, and summarize the exported data. ✅

Quick access to generated files (already produced elsewhere in repo):
- Redacted SQL dumps: `d:\vehicle\reproduce_profile\dumps\` (Cookies.sql, History.sql, Login_Data.sql, Web_Data.sql, Top_Sites.sql, first_party_sets.sql)
- Extracted CSVs: `d:\vehicle\reproduce_profile\exports\` (cookies.csv, logins.csv, autofill.csv, credit_cards.csv, addresses.csv)
- Raw credential blobs: `d:\vehicle\reproduce_profile\exports\raw_files\` (trusted_vault.pb, passkey_enclave_state)
- Inventory JSON: `d:\vehicle\inventory.json`

How to use
1. Copy any CSVs you want into `analysis/data/` or run `scripts/prepare_data.py` to copy them automatically.
2. Run `scripts/preview.py` to see quick summaries (row counts, top domains, sample rows).
3. Read `reports/FINAL_REPORT.md` for the full reverse-engineering findings and reproduction instructions.

Security & privacy ⚠️
- Some fields remain encrypted (passwords/cookie AES-GCM blobs). Decryption requires DPAPI unwrapping on the same Windows user. Handle data with care.

Contact
- If you want me to re-run decryption attempts or populate the scaffold with sample rows, reply with **TRY_PY311** or **POPULATE SAMPLES**.
