# FINAL REPORT — Profile Reverse-Engineering

## Executive summary
- Profile root: `d:/vehicle/37ab1612-c285-4314-b32a-6a06d35d6d84`.
- Chrome version recorded: `143.0.7499.41`.
- Key extractions: cookies (367 rows), logins (2 rows), autofill (2 rows). Raw credential blobs saved (trusted_vault.pb, passkey_enclave_state).
- Decryption status: Local State AES key unwrap failed in current environment; AES-GCM `v10` blobs remain encrypted.

## Where to find the data
- Inventory JSON: `d:/vehicle/inventory.json`
- CSV exports: `d:/vehicle/reproduce_profile/exports/`
- Redacted SQL dumps: `d:/vehicle/reproduce_profile/dumps/`
- Analysis package: `d:/vehicle/reproduce_profile/analysis/` (this folder)

## Reproduction plan (exact)
1. For testing and code development: run `recreate_profile_scaffold.py` to generate full folder tree and schema DBs.
2. To create a functioning profile (sessions preserved): copy the entire folder into the target Windows user account (same user) so DPAPI unwrapping preserves secrets, or export + rewrap Local State AES key on destination.
3. To decrypt secrets on this host: run DPAPI unwrapping under same user with compatible Python + pywin32 or using native PowerShell/ProtectedData in full .NET runtime (I can retry if you request).

## Notes & next steps
- If you want the final packaged ZIP with all CSVs, SQL dumps, inventory JSON, and this report, reply **PACKAGE ZIP**.
- If you want me to attempt DPAPI unwrapping again using a different method or Python version, reply **TRY_PY311** or **TRY_WINPS**.

---
Generated for researcher use. Treat extracted data confidentially.
