#!/usr/bin/env python3
"""
MLA Integration Example Script
Demonstrates the complete Multilogin integration with Chronos time-shifting
and manual handover protocol.

This script shows how to:
1. Initialize Chronos for time manipulation
2. Start an MLA profile
3. Perform cookie generation
4. Stop the profile with proper cookie sync
5. Restore system time

IMPORTANT: Run as Administrator for time manipulation to work.
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.chronos import ChronosTimeMachine
from core.mla_bridge import MLABridge
from config.settings import Config
from utils.logger import get_logger

logger = get_logger()


def main():
    """Example MLA integration flow"""
    
    print("="*60)
    print("MLA INTEGRATION EXAMPLE")
    print("="*60)
    
    # Configuration
    profile_id = "example_profile_001"
    age_days = 90
    
    # Initialize components
    chronos = None
    mla_bridge = None
    
    try:
        # Step 1: Initialize Chronos
        print("\n[Step 1] Initializing Chronos Time Machine...")
        chronos = ChronosTimeMachine()
        
        # Step 2: Kill NTP and shift time
        print(f"[Step 2] Shifting time backwards by {age_days} days...")
        chronos.kill_ntp()
        
        if not chronos.shift_time(days_ago=age_days):
            print("ERROR: Time shift failed!")
            return 1
        
        print(f"✓ Time shifted to T-{age_days} days")
        
        # Step 3: Initialize MLA Bridge
        print(f"\n[Step 3] Initializing MLA Bridge for profile: {profile_id}")
        mla_bridge = MLABridge(profile_id=profile_id)
        
        # Step 4: Start MLA Profile
        # CRITICAL: This happens AFTER time shift so browser spawns with shifted time
        print("[Step 4] Starting MLA profile...")
        
        if not mla_bridge.start_profile():
            print("ERROR: Failed to start MLA profile!")
            print("Make sure Multilogin is running on port", Config.MLA_PORT)
            return 1
        
        print(f"✓ Profile started on debugging port: {mla_bridge.remote_port}")
        
        # Step 5: Attach WebDriver
        print("[Step 5] Attaching WebDriver...")
        driver = mla_bridge.attach_webdriver()
        
        if not driver:
            print("ERROR: Failed to attach WebDriver!")
            return 1
        
        print("✓ WebDriver attached successfully")
        
        # Step 6: Perform Cookie Generation
        print("\n[Step 6] Performing cookie generation...")
        
        # Example: Visit some trust anchors
        trust_anchors = [
            "https://www.google.com",
            "https://www.amazon.com",
            "https://www.wikipedia.org"
        ]
        
        for url in trust_anchors:
            print(f"  - Visiting: {url}")
            driver.get(url)
            time.sleep(3)  # Dwell time
            
            # Scroll randomly
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
        
        print("✓ Cookie generation complete")
        
        # Step 7: Stop Profile (syncs cookies)
        print("\n[Step 7] Stopping profile and syncing cookies to MLA...")
        mla_bridge.stop_profile()
        print("✓ Profile stopped - cookies synced to MLA cloud/disk")
        
        # Step 8: Restore Time
        print("\n[Step 8] Restoring system time...")
        chronos.restore_original_time()
        chronos.restore_ntp()
        print("✓ System time restored to reality")
        
        # Success message
        print("\n" + "="*60)
        print("[+] CHRONOS: Time restored. Cookies synced to MLA.")
        print(">>> PROFILE READY FOR MANUAL TAKEOVER <<<")
        print(f"Profile ID: {profile_id}")
        print("="*60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n[ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        # Emergency cleanup
        print("\n[Cleanup] Ensuring resources are released...")
        
        if mla_bridge:
            try:
                mla_bridge.stop_profile()
            except:
                pass
        
        if chronos:
            try:
                chronos.cleanup()
            except:
                pass


if __name__ == "__main__":
    # Check if running as administrator (Windows)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("WARNING: Not running as Administrator!")
            print("Time manipulation requires Administrator privileges.")
            print("Please run this script as Administrator.")
            sys.exit(1)
    except:
        print("Note: Admin check not available on this platform")
    
    sys.exit(main())
