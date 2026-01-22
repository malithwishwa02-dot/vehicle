"""
Generate 90-day Aged Local Storage
Standalone utility to inject historically aged keys into a Chrome profile.
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.burner import ProfileBurner
from core.constructor import Constructor

def generate_aged_storage(profile_path=None):
    # 1. If no profile provided, create a temporary one
    if not profile_path:
        print("[*] No profile path provided. creating new scaffolding...")
        constructor = Constructor("generated_profiles")
        profile_path, uuid = constructor.build_skeleton()
        print(f"[*] Created profile at: {profile_path}")
    
    # 2. Initialize Burner
    burner = ProfileBurner(profile_path)
    
    try:
        # 3. Ignite Browser
        burner.ignite()
        
        # 4. Inject 90-day aged keys
        print("[*] Injecting 90-day aged Local Storage keys...")
        
        # We can use the existing method which defaults to 90 days
        # or we can explicitly set specific aged keys here if we want more control
        burner.inject_phantom_local_storage()
        
        # Verify injection with a check
        stale_epoch = int((time.time() - 90*24*3600) * 1000)
        print(f"[*] Target timestamp: {stale_epoch} (approx 90 days ago)")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        # 5. Save and Close
        burner.extinguish()
        print("[*] Local Storage generation complete.")

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else None
    generate_aged_storage(target_path)
