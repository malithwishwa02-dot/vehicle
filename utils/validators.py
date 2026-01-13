"""
System validators and privilege checks
Ensures environment meets requirements for CHRONOS operations
"""

import ctypes
import platform
import sys
import subprocess
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SystemValidator:
    """Validates system requirements and privileges"""
    
    @staticmethod
    def check_os() -> Tuple[bool, str]:
        """
        Check if running on supported Windows version
        
        Returns:
            Tuple of (is_valid, os_info)
        """
        system = platform.system()
        version = platform.version()
        
        if system != "Windows":
            return False, f"Unsupported OS: {system}. Windows 10/11 required."
        
        # Parse Windows version
        try:
            major_version = int(version.split('.')[0])
            build_number = int(version.split('.')[2])
            
            # Windows 10: build 10240+
            # Windows 11: build 22000+
            if build_number >= 10240:
                os_name = "Windows 11" if build_number >= 22000 else "Windows 10"
                return True, f"{os_name} (Build {build_number})"
            else:
                return False, f"Windows version too old: Build {build_number}"
                
        except Exception as e:
            logger.error(f"Failed to parse Windows version: {str(e)}")
            return False, f"Unknown Windows version: {version}"
    
    @staticmethod
    def check_admin_privileges() -> bool:
        """
        Check if script has Administrator privileges
        
        Returns:
            True if running as Administrator
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            return False
    
    @staticmethod
    def check_python_version() -> Tuple[bool, str]:
        """
        Verify Python version meets requirements
        
        Returns:
            Tuple of (is_valid, version_string)
        """
        version_info = sys.version_info
        version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        if version_info.major == 3 and version_info.minor >= 10:
            return True, version_string
        else:
            return False, f"Python {version_string} (3.10+ required)"
    
    @staticmethod
    def check_multilogin_api() -> Tuple[bool, str]:
        """
        Check if Multilogin Local API is accessible
        
        Returns:
            Tuple of (is_accessible, status_message)
        """
        try:
            import requests
            
            response = requests.get(
                "http://127.0.0.1:35000/api/v2/profile",
                timeout=3
            )
            
            if response.status_code in [200, 401]:
                return True, "Multilogin API accessible"
            else:
                return False, f"API returned status {response.status_code}"
                
        except requests.ConnectionError:
            return False, "Multilogin not running or API disabled"
        except Exception as e:
            return False, f"API check failed: {str(e)}"
    
    @staticmethod
    def check_time_service_status() -> Dict[str, Any]:
        """
        Check Windows Time Service status
        
        Returns:
            Dict with service status information
        """
        try:
            # Query Windows Time service
            result = subprocess.run(
                ["sc", "query", "W32Time"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            status = {
                "service_exists": "STATE" in result.stdout,
                "is_running": "RUNNING" in result.stdout,
                "raw_output": result.stdout
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to check time service: {str(e)}")
            return {"service_exists": False, "is_running": False, "error": str(e)}
    
    @staticmethod
    def validate_all() -> Dict[str, Any]:
        """
        Run all validation checks
        
        Returns:
            Dict with all validation results
        """
        results = {}
        
        # OS Check
        os_valid, os_info = SystemValidator.check_os()
        results["os"] = {
            "valid": os_valid,
            "info": os_info
        }
        
        # Admin privileges
        results["admin"] = {
            "valid": SystemValidator.check_admin_privileges(),
            "info": "Administrator" if SystemValidator.check_admin_privileges() else "Standard User"
        }
        
        # Python version
        py_valid, py_version = SystemValidator.check_python_version()
        results["python"] = {
            "valid": py_valid,
            "info": py_version
        }
        
        # Multilogin API
        mla_valid, mla_status = SystemValidator.check_multilogin_api()
        results["multilogin"] = {
            "valid": mla_valid,
            "info": mla_status
        }
        
        # Time service
        results["time_service"] = SystemValidator.check_time_service_status()
        
        # Overall validation
        results["all_valid"] = all([
            results["os"]["valid"],
            results["admin"]["valid"],
            results["python"]["valid"],
            results["multilogin"]["valid"]
        ])
        
        return results
    
    @staticmethod
    def print_validation_report(results: Dict[str, Any]) -> None:
        """Print formatted validation report"""
        print("=" * 60)
        print("CHRONOS SYSTEM VALIDATION REPORT")
        print("=" * 60)
        
        for key, value in results.items():
            if key == "all_valid":
                continue
            
            if isinstance(value, dict) and "valid" in value:
                status = "✓" if value["valid"] else "✗"
                print(f"{status} {key.upper()}: {value.get('info', 'N/A')}")
            elif key == "time_service":
                status = "✓" if value.get("is_running") else "✗"
                print(f"{status} TIME SERVICE: {'Running' if value.get('is_running') else 'Stopped'}")
        
        print("=" * 60)
        
        if results["all_valid"]:
            print("✓ All checks passed - System ready for CHRONOS operations")
        else:
            print("✗ Some checks failed - Please resolve issues before proceeding")
        
        print("=" * 60)