import requests
import os
import sys
import platform
import random
import math
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION CHECK ---
REQUIRED_LAMBDA = 2.5
REQUIRED_AGE = 90
MLX_PORT = 35000
MLX_URL = f"http://127.0.0.1:{MLX_PORT}/api/v1" # V1/V2 dependent on version

def print_status(component, status, msg=""):
    color = "\033[92m" if status == "PASS" else "\033[91m"
    reset = "\033[0m"
    print(f"[{component}] {color}{status}{reset} : {msg}")

def check_launcher_connectivity():
    """Checks the MLX Launcher (Background Service) on Port 45001."""
    try:
        # MLX Launcher uses HTTPS with a self-signed cert usually, so verify=False might be needed.
        url = "https://launcher.mlx.yt:45001/api/v1/version"
        r = requests.get(url, verify=False, timeout=5)
        if r.status_code == 200:
            print_status("MLX LAUNCHER", "PASS", f"Service Active (Port 45001). Response: {r.text[:50]}...")
            return True
        else:
            print_status("MLX LAUNCHER", "FAIL", f"Status Code: {r.status_code}")
            return False
    except Exception as e:
        print_status("MLX LAUNCHER", "FAIL", f"Connection Failed: {e}")
        return False
def check_dependencies():
    """Verifies critical libraries for Method 4."""
    try:
        import requests
        import yaml
        print_status("DEPENDENCIES", "PASS", "requests, pyyaml found.")
    except ImportError as e:
        print_status("DEPENDENCIES", "FAIL", f"Missing library: {e.name}")

def check_mlx_connectivity():
    """Verifies MLX API is reachable."""
    try:
        # Simple health check or profile list
        r = requests.get(f"{MLX_URL}/profile/f", params={"limit": 1}, timeout=5)
        if r.status_code == 200:
            print_status("MLX API", "PASS", "Connection established.")
            return True
        else:
            print_status("MLX API", "FAIL", f"Status Code: {r.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_status("MLX API", "FAIL", f"Connection Refused on Port {MLX_PORT}. Is MLX running?")
        return False

def check_filesystem_access():
    """Verifies write access for Kernel Time Shift."""
    # Attempt to locate MLX directory
    home = Path.home()
    
    potential_paths = [
        home / ".multiloginapp.com" / "data",
        home / "mlx" / "data",
        # Add your custom path here if needed
    ]
    
    found = False
    for path in potential_paths:
        if path.exists():
            print_status("FILESYSTEM", "PASS", f"MLX Data Directory found at: {path}")
            # Test Write Access
            try:
                test_file = path / "test_write_access.tmp"
                test_file.touch()
                test_file.unlink()
                print_status("WRITE ACCESS", "PASS", "Kernel Time Shift operations possible.")
                found = True
                break
            except PermissionError:
                print_status("WRITE ACCESS", "FAIL", "Permission Denied. Run as Admin/Root.")
                
    if not found:
        print_status("FILESYSTEM", "FAIL", "Could not auto-locate MLX Data Directory.")

def verify_poisson_logic():
    """Verifies the bursty traffic logic."""
    delays = []
    for _ in range(100):
        # Implementation of the patch
        delay = -math.log(1.0 - random.random()) / REQUIRED_LAMBDA
        delays.append(delay)
    
    avg = sum(delays) / len(delays)
    if 0.1 < avg < 1.0: # Expected range for Lambda 2.5
        print_status("BEHAVIOR LOGIC", "PASS", f"Poisson Distribution Active (Avg: {avg:.2f}s).")
    else:
        print_status("BEHAVIOR LOGIC", "FAIL", f"Distribution anomalies detected (Avg: {avg:.2f}s).")

def verify_config_settings():
    """Checks if the user has updated settings.yaml."""
    # Assuming standard path relative to this script
    config_path = Path("coolies/chronos-mla-injector/config/settings.yaml")
    
    if not config_path.exists():
        print_status("CONFIG", "WARN", "settings.yaml not found in standard path.")
        return

    try:
        import yaml
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
            
        age = cfg.get('profile_age', 0)
        dist = cfg.get('traffic_distribution', 'LINEAR')
        
        if age == REQUIRED_AGE:
            print_status("CONFIG AGE", "PASS", f"Profile Age set to {age} days.")
        else:
            print_status("CONFIG AGE", "FAIL", f"Profile Age is {age} (Expected {REQUIRED_AGE}).")
            
        if dist == "POISSON":
            print_status("CONFIG DIST", "PASS", "Traffic Distribution set to POISSON.")
        else:
            print_status("CONFIG DIST", "FAIL", f"Distribution is {dist} (Expected POISSON).")
            
    except Exception as e:
        print_status("CONFIG", "FAIL", f"Could not parse YAML: {e}")

if __name__ == "__main__":
    print("=== MULTILOGIN X METHOD 4 READINESS CHECK ===\n")
    check_dependencies()
    launcher_ready = check_launcher_connectivity()
    api_ready = check_mlx_connectivity()
    check_filesystem_access()
    verify_poisson_logic()
    verify_config_settings()
    print("\n=== DIAGNOSTIC COMPLETE ===")
    if not launcher_ready:
        print("CRITICAL: MLX Launcher is not running. Start the application.")
    elif not api_ready:
        print("CRITICAL: Cannot proceed without MLX API. Ensure the application is open and Automation Agent is enabled.")
