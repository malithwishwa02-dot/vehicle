import yaml
import argparse
import sys
from core.constructor import Constructor
from core.identity import IdentityEngine
from core.history import HistoryEngine
from tools.burner import Burner

def load_config(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[!] Config file not found: {path}")
        sys.exit(1)

def main():
    print("=== PROMETHEUS-CORE v3: MIDAS PROTOCOL ===")
    print("> AUTHORITY: Dva.12 | STATUS: ACTIVE")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/inputs.yaml", help="Path to YAML config")
    # Add CLI overrides here if needed
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    
    # Initialize Engines
    constructor = Constructor(cfg['profile']['output_dir'])
    identity = IdentityEngine()
    history = HistoryEngine()
    
    count = cfg['profile'].get('count', 1)
    
    for i in range(count):
        print(f"\n--- GENERATING PROFILE {i+1}/{count} ---")
        
        # 1. SCAFFOLDING
        profile_path, uuid_str = constructor.build_skeleton(cfg['proxy'], cfg['persona'])
        
        # 2. BURNER (Encrypted Data)
        # Use profile-bound burner to perform runtime injections (history/localStorage)
        try:
            burner = Burner(profile_path)
            burner.run_cycle()
        except Exception as e:
            print(f"[BURNER] Error: {e}")
        
        # 3. IDENTITY (Unencrypted Data)
        identity.inject_address(profile_path, cfg['persona'])
        
        # 4. HISTORY (Narrative)
        history.inject_timeline(profile_path, cfg['profile']['age_days'])
        
        print(f"[SUCCESS] Golden Profile Ready: {uuid_str}")
        print(f"Location: {profile_path}")

if __name__ == "__main__":
    main()
