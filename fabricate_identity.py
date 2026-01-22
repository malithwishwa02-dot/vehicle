"""
PROMETHEUS-CORE v3.0 :: MODULE: ORCHESTRATOR
AUTHORITY: Dva.13 | STATUS: OPERATIONAL
PURPOSE: Master Execution Script for 'OP-MIDAS-CONSTRUCTOR-V4'.
         Chains the Constructor and Burner to produce a Multilogin-ready profile.
"""

import os
from pathlib import Path
from core.constructor import ProfileConstructor

from tools.burner import ProfileBurner
from core.identity import Persona

import argparse

def execute_midas_protocol(args):
    print("==========================================================")
    print("   P R O M E T H E U S - C O R E   v 3 . 0")
    print("   OPERATION MIDAS: IDENTITY FABRICATION SEQUENCE")
    print("==========================================================\n")

    # PHASE 1: CONSTRUCTION
    print("[PHASE 1] STRUCTURAL SYNTHESIS")
    constructor = ProfileConstructor(output_dir='generated_profiles', uuid=args.uuid)
    artifact_path = constructor.run(force=args.force)
    
    print("\n----------------------------------------------------------\n")

    # PHASE 2A: SYNTHETIC POPULATION (DBs & Preferences)
    print("[PHASE 2A] SYNTHETIC POPULATION (DBs & PREFERENCES)")
    try:
        from reproduce_profile.scripts.generate_aged_profile import create_aged_profile
        create_aged_profile(Path(artifact_path), age_days=args.age_days, seed=args.seed, populate=True)
    except Exception as e:
        print(f"[PHASE 2A] Synthetic population failed: {e}")



    # PHASE 2B: BURNING (browser-driven writes with persona)
    print("[PHASE 2B] DATA INJECTION (THE BURN)")
    persona = Persona(seed=args.seed)
    burner = ProfileBurner(artifact_path, persona=persona)
    try:
        burner.run_cycle(persona=persona)
    except Exception as e:
        print('[PHASE 2B] Burner run failed:', e)

    # PHASE 2C: TEMPORAL INJECTION (TIME DILATOR)
    print("[PHASE 2C] TEMPORAL INJECTION (TIME DILATOR)")
    try:
        from time_dilator import TimeDilator
        td = TimeDilator(artifact_path)
        td.inject_history()
    except Exception as e:
        print(f'[PHASE 2C] Time Dilator failed: {e}')

    # If burner could not create LevelDB entries and user requested real_leveldb, attempt direct write
    if args.real_leveldb:
        from tools.leveldb_writer import write_local_storage
        leveldb_dir = os.path.join(artifact_path, 'Default', 'Local Storage', 'leveldb')
        data = {
            "cart_abandoned": "false",
            "previous_purchases": "3",
            "user_trust_score": "0.95",
            "stripe_mid": "guid_12345_mock",
            "has_logged_in": "true"
        }
        ok = write_local_storage(leveldb_dir, data)
        if ok:
            print('[PHASE 2] Direct LevelDB write succeeded.')
        else:
            print('[PHASE 2] Direct LevelDB write failed; simulation may be present instead.')

    # Finalize: re-apply aging timestamps after any burner activity that may have updated file mtimes
    try:
        from reproduce_profile.scripts.generate_aged_profile import touch_aged_files
        touch_aged_files(Path(artifact_path), args.age_days)
        print(f"[PHASE 2] Applied aging timestamps ({args.age_days} days) to artifact files.")
    except Exception as e:
        print(f"[PHASE 2] Aging timestamps could not be applied: {e}")

    print("\n----------------------------------------------------------\n")

    # PHASE 3: FINALIZATION
    print("[PHASE 3] ARTIFACT VERIFICATION")

    required_files = [
        "Default/Cookies",
        "Default/History",
        "Default/Local Storage/leveldb",
        "Default/Web Data"
    ]
    success = True
    for f in required_files:
        full_path = os.path.join(artifact_path, f)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                print(f"  [OK] {f} found. Size: {size} bytes.")
            else:
                # LevelDB is a folder, check if it has content
                try:
                    entries = os.listdir(full_path)
                except Exception:
                    entries = []
                if "leveldb" in f and entries:
                    print(f"  [OK] {f} (LevelDB) found and populated. entries={len(entries)}")
                    # Validate injected keys
                    sim_json = os.path.join(full_path, 'local_storage_simulated.json')
                    if os.path.exists(sim_json):
                        import json
                        with open(sim_json, 'r', encoding='utf-8') as fjson:
                            data = json.load(fjson)
                        for k in ["__stripe_mid", "shopify_checkout_token", "completed_checkout", "last_order_id"]:
                            if k not in data:
                                print(f"  [!!] CRITICAL: {k} missing from local_storage_simulated.json")
                                success = False
                else:
                    print(f"  [!!] CRITICAL FAILURE: {f} is missing or empty.")
                    success = False
        else:
            print(f"  [!!] CRITICAL FAILURE: {f} is missing or empty.")
            success = False

    if success:
        print("\n[SUCCESS] GOLDEN PROFILE GENERATED.")
        print(f"LOCATION: {artifact_path}")
        print("READY FOR MULTILOGIN INJECTION.")
    else:
        print("\n[FAILURE] PROFILE GENERATION INCOMPLETE.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--uuid', default='37ab1612-c285-4314-b32a-6a06d35d6d84', help='Target profile UUID (folder name)')
    ap.add_argument('--force', action='store_true', help='Force remove existing artifact (kill Chrome, move aside locked folder)')
    ap.add_argument('--real-leveldb', action='store_true', help='Attempt real LevelDB write using plyvel if available')
    ap.add_argument('--age-days', type=int, default=180, help='Approximate age in days for timestamps')
    ap.add_argument('--seed', type=int, default=42, help='RNG seed for deterministic generation')
    args = ap.parse_args()
    execute_midas_protocol(args)

