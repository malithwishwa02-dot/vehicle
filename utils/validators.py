"""
System validators and environment checks for CHRONOS-MULTILOGIN v2.0
Ensures operational safety and prerequisites
"""

import platform
import sys
import subprocess
import requests
from typing import Tuple, Dict, Any

# Conditional import for Windows-specific modules
if platform.system() == "Windows":
    import ctypes

def is_admin() -> bool:
    """Check if script has Administrator privileges"""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # On Linux, check if running as root
            import os
            return os.geteuid() == 0
    except (AttributeError, ImportError):
        return False

def check_mla_connection() -> bool:
    """Verify Multilogin Local API is accessible"""
    from config.settings import Config
    from utils.logger import log
    
    try:
        # Try v2 API first
        resp = requests.get(f"http://127.0.0.1:{Config.MLA_PORT}/api/v2/profile", timeout=3)
        if resp.status_code in [200, 401]:
            log("Multilogin Connection: ACTIVE (v2 API)", "SUCCESS")
            return True
        
        # Fallback to v1 API
        resp = requests.get(f"http://127.0.0.1:{Config.MLA_PORT}/api/v1/profile/list", timeout=3)
        if resp.status_code == 200:
            log("Multilogin Connection: ACTIVE (v1 API)", "SUCCESS")
            return True
        
        log(f"Multilogin returned status: {resp.status_code}", "ERROR")
        return False
    except requests.ConnectionError:
        log("Multilogin is NOT running. Please start the application.", "ERROR")
        return False
    except Exception as e:
        log(f"MLA connection check failed: {str(e)}", "ERROR")
        return False

def check_windows_version() -> Tuple[bool, str]:
    """Verify Windows version compatibility"""
    if platform.system() != "Windows":
        return False, f"Unsupported OS: {platform.system()}"
    
    version = platform.version()
    try:
        build = int(version.split('.')[2])
        if build >= 10240:  # Windows 10 minimum
            os_name = "Windows 11" if build >= 22000 else "Windows 10"
            return True, f"{os_name} (Build {build})"
        return False, f"Windows version too old: Build {build}"
    except:
        return False, f"Unknown Windows version: {version}"

def check_python_version() -> Tuple[bool, str]:
    """Verify Python version meets requirements"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 10:
        return True, version_str
    return False, f"Python {version_str} (3.10+ required)"

def check_time_service() -> Dict[str, Any]:
    """Check Windows Time Service status"""
    try:
        result = subprocess.run(
            ["sc", "query", "W32Time"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        return {
            "exists": "STATE" in result.stdout,
            "running": "RUNNING" in result.stdout,
            "status": "Running" if "RUNNING" in result.stdout else "Stopped"
        }
    except Exception as e:
        return {"exists": False, "running": False, "error": str(e)}

def check_dependencies() -> Dict[str, bool]:
    """Check required Python packages"""
    dependencies = {
        "requests": False,
        "selenium": False,
        "pywin32": False
    }
    
    for package in dependencies:
        try:
            __import__(package.replace("pywin32", "win32api"))
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    return dependencies

def validate_environment() -> Dict[str, Any]:
    """Run all validation checks"""
    from utils.logger import get_logger
    logger = get_logger()
    
    results = {
        "admin": is_admin(),
        "multilogin": check_mla_connection(),
        "windows": check_windows_version(),
        "python": check_python_version(),
        "time_service": check_time_service(),
        "dependencies": check_dependencies()
    }
    
    # Print validation report
    print("\n" + "="*60)
    print("   CHRONOS-MULTILOGIN v2.0 | SYSTEM VALIDATION")
    print("="*60)
    
    status = "✓" if results["admin"] else "✗"
    print(f"{status} Administrator Privileges: {'Granted' if results['admin'] else 'Required'}")
    
    status = "✓" if results["multilogin"] else "✗"
    print(f"{status} Multilogin API: {'Connected' if results['multilogin'] else 'Offline'}")
    
    os_valid, os_info = results["windows"]
    status = "✓" if os_valid else "✗"
    print(f"{status} Operating System: {os_info}")
    
    py_valid, py_info = results["python"]
    status = "✓" if py_valid else "✗"
    print(f"{status} Python Version: {py_info}")
    
    time_svc = results["time_service"]
    status = "✓" if time_svc.get("exists") else "✗"
    print(f"{status} Time Service: {time_svc.get('status', 'Unknown')}")
    
    print("\nDependencies:")
    for pkg, installed in results["dependencies"].items():
        status = "✓" if installed else "✗"
        print(f"  {status} {pkg}: {'Installed' if installed else 'Missing'}")
    
    print("="*60)
    
    # Overall status
    all_valid = (
        results["admin"] and 
        results["multilogin"] and 
        results["windows"][0] and 
        results["python"][0] and
        all(results["dependencies"].values())
    )
    
    if all_valid:
        print("✓ SYSTEM READY: All checks passed")
    else:
        print("✗ SYSTEM NOT READY: Resolve issues above")
    
    print("="*60 + "\n")
    
    return {"all_valid": all_valid, "details": results}