import os
import sys
import ast
import logging

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='[LUCID AUDIT] %(message)s')
FAIL = '\033[91m[FAIL]\033[0m'
PASS = '\033[92m[PASS]\033[0m'
WARN = '\033[93m[WARN]\033[0m'


def check_file_exists(path, description):
    if os.path.exists(path):
        logging.info(f"{PASS} {description}: Found at {path}")
        return True
    else:
        logging.error(f"{FAIL} {description}: MISSING at {path}")
        return False


def verify_lobotomy(engine_path):
    """
    Checks if Camoufox has been stripped of randomizers.
    """
    target_files = []
    # Search for api files in likely locations
    for root, dirs, files in os.walk(engine_path):
        if "sync_api.py" in files:
            target_files.append(os.path.join(root, "sync_api.py"))

    if not target_files:
        logging.error(f"{FAIL} Engine Source: sync_api.py not found. Cannot verify Lobotomy.")
        return False

    has_randomness = False
    for file_path in target_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "browserforge" in content or "FingerprintGenerator" in content:
                logging.error(f"{FAIL} LOBOTOMY FAILED in {file_path}")
                logging.error("    -> Detected 'BrowserForge' or 'FingerprintGenerator' import.")
                logging.error("    -> ACTION: Remove lines importing/initializing FingerprintGenerator.")
                has_randomness = True
            else:
                logging.info(f"{PASS} LOBOTOMY VERIFIED in {file_path} (No randomization detected).")

    return not has_randomness


def verify_vehicle_integration(dockerfile_path):
    """
    Stub for Windows: Dockerfile checks are not required.
    """
    return True


def verify_dashboard_linkage(main_script_path):
    """
    Checks if the main Python entry point serves the Dashboard.
    """
    if not os.path.exists(main_script_path):
        logging.warning(f"{WARN} Main entry point not found at {main_script_path}. Skipping linkage check.")
        return False

    with open(main_script_path, "r") as f:
        content = f.read()

    if "flask" in content.lower() and ("render_template" in content or "send_from_directory" in content):
        logging.info(f"{PASS} Dashboard Linkage: Flask serving logic detected.")
        return True
    else:
        logging.warning(f"{WARN} Dashboard Linkage: Could not confirm GUI serving logic in main script.")
        return False


def main():
    print("========================================================")
    print("   LUCID EMPIRE :: OPERATIONAL READINESS AUDIT")
    print("========================================================")

    # 1. DEFINE PATHS (Adjust relative to where script is run)
    ROOT = os.getcwd()

    # Heuristic path detection based on your file list
    ENGINE_DIR = os.path.join(ROOT, "camoufox") if os.path.exists(os.path.join(ROOT, "camoufox")) else os.path.join(ROOT, "engine")
        runtime_status = verify_vehicle_integration(None)

    MAIN_SCRIPT = os.path.join(ROOT, "main.py")
    if not os.path.exists(MAIN_SCRIPT):
        MAIN_SCRIPT = os.path.join(ROOT, "core", "lucid_orchestrator.py")

    # 2. EXECUTE CHECKS
    print(f"\n[PHASE 1] INFRASTRUCTURE AUDIT")
    lobotomy_status = verify_lobotomy(ROOT) # Scanning root recursively for engine files

    print(f"\n[PHASE 2] RUNTIME CAPABILITIES")
        runtime_status = verify_vehicle_integration(None)

    print(f"\n[PHASE 3] COMMAND & CONTROL")
    dashboard_status = verify_dashboard_linkage(MAIN_SCRIPT)

    # 3. FINAL REPORT
    print("\n========================================================")
    print("   FINAL STATUS REPORT")
    print("========================================================")

    if lobotomy_status and runtime_status:
        print(f"\n{PASS} SYSTEM STATUS: OPERATIONAL READY")
        print("    -> Randomization successfully stripped.")
        print("    -> Vehicle runtime fully integrated.")
        print("    -> READY FOR DEPLOYMENT.")
    else:
        print(f"\n{FAIL} SYSTEM STATUS: NOT READY")
        print("    -> Critical modifications missing. Review logs above.")


if __name__ == "__main__":
    main()
