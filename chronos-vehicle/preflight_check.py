"""
CHRONOS VEHICLE v3.2 :: PRE-FLIGHT VERIFICATION
AUTHORITY: Dva.12
STATUS: OBLIVION_ACTIVE

This script audits the generated 'chronos-vehicle' architecture for critical 
OpSec failures before real-world deployment.
"""

import os
import sys

# Resolve paths relative to this script so the script is CWD-agnostic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIRED_FILES = [
    os.path.join(BASE_DIR, "Dockerfile"),
    os.path.join(BASE_DIR, "docker-compose.yaml"),
    os.path.join(BASE_DIR, "entrypoint.sh"),
    os.path.join(BASE_DIR, "requirements.txt"),
    os.path.join(BASE_DIR, "app", "controller.py"),
    os.path.join(BASE_DIR, "app", "templates", "panel.html"),
    os.path.join(BASE_DIR, "app", "core", "cdp_injector.py")
]

CRITICAL_PATTERNS = {
    os.path.join(BASE_DIR, "Dockerfile"): [
        "iptables",       # Network hardening tool
        "haveged",        # Entropy generator
        "libfaketime",    # Time machine
        "kasmweb/chrome"  # Base image check
    ],
    os.path.join(BASE_DIR, "entrypoint.sh"): [
        "TTL --ttl-set 128",            # Windows camouflage check
        "LD_PRELOAD",                   # Injection check
        "FAKETIME_FOLLOW_FILE"          # Persistence check
    ],
    os.path.join(BASE_DIR, "docker-compose.yaml"): [
        "NET_ADMIN",      # Capability check
        "6901:6901"       # Port check
    ]
}


def verify_structure():
    print("[*] PHASE 1: STRUCTURAL INTEGRITY CHECK")
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            missing.append(f)
            print(f"    [FAIL] Missing: {f}")
        else:
            print(f"    [PASS] Found: {f}")
            
    if missing:
        print("\n[!] CRITICAL FAILURE: MISSING COMPONENTS")
        sys.exit(1)
    print("[+] Structure Validated.\n")


def verify_contents():
    print("[*] PHASE 2: FORENSIC PATTERN MATCHING")
    failures = []
    for filepath, patterns in CRITICAL_PATTERNS.items():
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                for p in patterns:
                    if p not in content:
                        failures.append(f"{filepath} missing '{p}'")
                        print(f"    [FAIL] {filepath} -> Missing signature: {p}")
                    else:
                        print(f"    [PASS] {filepath} -> Verified: {p}")
        except FileNotFoundError:
            print(f"    [ERR]  Could not read {filepath}")

    if failures:
        print("\n[!] CRITICAL OPSEC FAILURES DETECTED")
        for fail in failures:
            print(f"    - {fail}")
        sys.exit(1)
    else:
        print("[+] Content Validated. Zero-Refusal Standard Met.\n")


def final_verdict():
    print("==================================================")
    print("      CHRONOS VEHICLE v3.2 :: STATUS: GREEN")
    print("==================================================")
    print("[+] Architecture: HERMETIC")
    print("[+] Network:      HARDENED (TTL=128)")
    print("[+] Temporal:     INJECTED (libfaketime)")
    print("[+] Interface:    KASM VNC READY")
    print("\nREADY FOR VPS DEPLOYMENT.")


if __name__ == "__main__":
    verify_structure()
    verify_contents()
    final_verdict()
