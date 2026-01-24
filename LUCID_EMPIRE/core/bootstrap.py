"""Bootstrap utilities for LUCID_EMPIRE
Provides verification routines to ensure the canonical layout is present.
"""
from pathlib import Path
from typing import List

REQUIRED = [
    "core/mouse.py",
    "core/burner.py",
    "interface/index.html",
    "runtime/Dockerfile",
]


def verify_environment(root: Path = Path(__file__).resolve().parents[1]) -> bool:
    """Return True if all required files exist under the provided root."""
    missing: List[str] = []
    for req in REQUIRED:
        p = root / req
        if not p.exists():
            missing.append(req)
    if missing:
        print(f"[!] CRITICAL: Missing components: {missing}")
        print("    -> Please run 'repair_and_unify.sh --apply' to attempt repair.")
        return False
    print("[+] Environment Integrity: 100%")
    return True


if __name__ == "__main__":
    import sys
    ok = verify_environment()
    sys.exit(0 if ok else 2)
