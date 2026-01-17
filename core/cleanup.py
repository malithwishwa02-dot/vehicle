import os
import atexit
import secrets
"""
Cleanup Module (MODULE 5: RESURRECTION - Cleanup)
System restoration and time synchronization validation.
Maps to CHRONOS_TASK.md Module 5 specifications.
"""

from core.isolation import IsolationManager
from core.chronos import Chronos
from core.safety import SafetyValidator
from utils.logger import get_logger
import subprocess
import requests
import time
from datetime import datetime
from typing import Optional, Dict, Any
import sys


class CleanupManager:
        def dod_5220_22m_overwrite(self, file_path: str):
            """
            DoD 5220.22-M: 3-pass overwrite (random, complement, zeros) for forensic scrubbing.
            """
            try:
                if not os.path.isfile(file_path):
                    self.logger.warning(f"File not found for DoD overwrite: {file_path}")
                    return
                length = os.path.getsize(file_path)
                with open(file_path, 'r+b') as f:
                    # Pass 1: Random bytes
                    f.seek(0)
                    f.write(secrets.token_bytes(length))
                    f.flush()
                    os.fsync(f.fileno())
                    # Pass 2: Complement bytes
                    f.seek(0)
                    f.write(bytes([~b & 0xFF for b in secrets.token_bytes(length)]))
                    f.flush()
                    os.fsync(f.fileno())
                    # Pass 3: Zeros
                    f.seek(0)
                    f.write(b'\x00' * length)
                    f.flush()
                    os.fsync(f.fileno())
                self.logger.info(f"DoD 5220.22-M overwrite complete: {file_path}")
            except Exception as e:
                self.logger.error(f"DoD overwrite failed: {e}")

        def register_dod_cleanup(self, file_path: str):
            """Register DoD overwrite to run at exit."""
            atexit.register(self.dod_5220_22m_overwrite, file_path)
    """
    Cleanup and Restoration (CHRONOS_TASK.md Module 5)
    
    Implements:
    - Restoration: Delete firewall rules, enable/start w32time, force resync
    - Validation: Query worldtimeapi.org, compare with local time
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.isolation_manager = IsolationManager(logger=self.logger)
        self.chronos = Chronos()
        self.safety_validator = SafetyValidator()
    
    def restore_system(self) -> bool:
        """
        Restoration (CHRONOS_TASK.md Module 5, Requirement 1)
        
        Steps:
        1. Delete netsh firewall rule
        2. Enable and Start w32time
        3. Force resync: w32tm /resync
        
        Returns:
            bool: Success status
        """
        self.logger.critical("INITIATING SYSTEM RESTORATION...")
        
        try:
            # Step 1: Delete netsh firewall rules
            if not self._delete_firewall_rules():
                self.logger.warning("Firewall rule deletion completed with warnings")
            
            # Step 2: Enable and Start w32time
            if not self._enable_w32time():
                self.logger.error("Failed to enable W32Time service")
                return False
            
            # Step 3: Force resync
            if not self._force_time_resync():
                self.logger.warning("Time resync completed with warnings")
            
            self.logger.success("System restoration COMPLETE")
            return True
            
        except Exception as e:
            self.logger.error(f"System restoration failed: {e}")
            return False
    
    def _delete_firewall_rules(self) -> bool:
        """
        Delete netsh firewall rules created by CHRONOS.
        (Module 5, Requirement 1, Step 1)
        """
        self.logger.info("Deleting firewall rules...")
        
        try:
            # Delete CHRONOS NTP block rules
            rules_to_delete = [
                "CHRONOS_NTP_BLOCK_OUT",
                "CHRONOS_NTP_BLOCK_IN",
                "PROMETHEUS_Block_NTP_Out",
                "PROMETHEUS_Block_NTP_In"
            ]
            
            for rule_name in rules_to_delete:
                try:
                    cmd = [
                        "netsh", "advfirewall", "firewall", "delete", "rule",
                        f"name={rule_name}"
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    
                    if "Ok" in result.stdout or result.returncode == 0:
                        self.logger.info(f"Firewall rule deleted: {rule_name}")
                    else:
                        self.logger.warning(f"Rule {rule_name} not found or already deleted")
                        
                except Exception as e:
                    self.logger.warning(f"Error deleting rule {rule_name}: {e}")
            
            self.logger.success("Firewall rules cleanup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Firewall cleanup failed: {e}")
            return False
    
    def _enable_w32time(self) -> bool:
        """
        Enable and Start w32time service.
        (Module 5, Requirement 1, Step 2)
        """
        self.logger.info("Enabling W32Time service...")
        
        try:
            # Set service to automatic startup
            result = subprocess.run(
                ["sc", "config", "w32time", "start=auto"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                self.logger.info("W32Time service set to automatic")
            else:
                self.logger.warning(f"Service config warning: {result.stderr}")
            
            # Start the service
            result = subprocess.run(
                ["net", "start", "w32time"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=30
            )
            
            if result.returncode == 0 or "already started" in result.stdout.lower():
                self.logger.success("W32Time service started")
                return True
            else:
                self.logger.warning(f"Service start warning: {result.stderr}")
                return True  # Non-critical if already running
                
        except subprocess.TimeoutExpired:
            self.logger.warning("W32Time start timeout - service may be starting")
            return True
            
        except Exception as e:
            self.logger.error(f"W32Time enable failed: {e}")
            return False
    
    def _force_time_resync(self) -> bool:
        """
        Force resync: w32tm /resync
        (Module 5, Requirement 1, Step 3)
        """
        self.logger.info("Forcing time resynchronization...")
        
        try:
            # Wait a moment for service to fully start
            time.sleep(2)
            
            # Force immediate resync
            result = subprocess.run(
                ["w32tm", "/resync", "/force"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=30
            )
            
            if result.returncode == 0 or "successfully" in result.stdout.lower():
                self.logger.success("Time resynchronization forced")
                return True
            else:
                self.logger.warning(f"Resync output: {result.stdout}")
                return True  # Non-critical
                
        except subprocess.TimeoutExpired:
            self.logger.warning("Resync timeout - may complete in background")
            return True
            
        except Exception as e:
            self.logger.error(f"Time resync failed: {e}")
            return False
    
    def validate_time_sync(self, max_skew_seconds: int = 1) -> bool:
        """
        Validation (CHRONOS_TASK.md Module 5, Requirement 2)
        
        Steps:
        1. Query http://worldtimeapi.org/api/ip
        2. Compare with local system time
        3. Raise SystemExit if skew > 1 second
        
        Args:
            max_skew_seconds: Maximum allowed time skew (default: 1)
            
        Returns:
            bool: True if validation passes
            
        Raises:
            SystemExit: If time skew exceeds threshold
        """
        self.logger.info("Validating time synchronization...")
        
        try:
            # Wait for time sync to complete
            time.sleep(5)
            
            # Query worldtimeapi.org (Module 5, Requirement 2, Step 1)
            response = requests.get(
                "http://worldtimeapi.org/api/ip",
                timeout=10
            )
            
            if response.status_code != 200:
                self.logger.error("Failed to query time API")
                raise SystemExit("Time validation failed: Unable to query time API")
            
            data = response.json()
            
            # Parse server time - support multiple formats for compatibility
            server_time_str = data.get('datetime', '')
            if not server_time_str:
                self.logger.error("Invalid time API response")
                raise SystemExit("Time validation failed: Invalid API response")
            
            # Parse ISO 8601 datetime with fallback for Python < 3.7
            try:
                # Python 3.7+
                server_time = datetime.fromisoformat(server_time_str.replace('Z', '+00:00'))
            except (AttributeError, ValueError):
                # Fallback for older Python versions
                from dateutil.parser import parse
                server_time = parse(server_time_str)
            
            # Get local system time (Module 5, Requirement 2, Step 2)
            local_time = datetime.utcnow()
            
            # Calculate skew
            skew_seconds = abs((server_time - local_time).total_seconds())
            
            self.logger.info(f"Server time: {server_time}")
            self.logger.info(f"Local time:  {local_time}")
            self.logger.info(f"Time skew:   {skew_seconds:.2f} seconds")
            
            # Check if skew exceeds threshold (Module 5, Requirement 2, Step 3)
            if skew_seconds > max_skew_seconds:
                self.logger.critical(f"TIME SKEW EXCEEDED THRESHOLD: {skew_seconds:.2f}s > {max_skew_seconds}s")
                self.logger.critical("System time is NOT synchronized!")
                
                # Raise SystemExit as specified in requirements
                raise SystemExit(
                    f"CRITICAL: Time skew ({skew_seconds:.2f}s) exceeds threshold ({max_skew_seconds}s). "
                    "System time is not properly synchronized with world time."
                )
            
            self.logger.success(f"Time synchronization VALIDATED (skew: {skew_seconds:.2f}s)")
            return True
            
        except SystemExit:
            raise  # Re-raise SystemExit
            
        except Exception as e:
            self.logger.error(f"Time validation exception: {e}")
            raise SystemExit(f"Time validation failed: {e}")
    
    def full_cleanup(self, validate: bool = True) -> bool:
        # Register DoD overwrite for isolation_state.json
        isolation_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'isolation_state.json')
        self.register_dod_cleanup(isolation_file)
        """
        Execute complete cleanup and restoration sequence.
        
        Args:
            validate: Whether to validate time sync after restoration
            
        Returns:
            bool: Success status
        """
        self.logger.critical("=" * 60)
        self.logger.critical("INITIATING FULL CLEANUP SEQUENCE")
        self.logger.critical("=" * 60)
        
        try:
            # Step 1: Restore original time
            self.logger.info("Step 1: Restoring original time...")
            if self.chronos.original_time:
                self.chronos.restore_original_time()
            
            # Step 2: Restore system (firewall, w32time, resync)
            self.logger.info("Step 2: Restoring system services...")
            if not self.restore_system():
                self.logger.error("System restoration failed")
                return False
            
            # Step 3: Restore network isolation
            self.logger.info("Step 3: Restoring network connectivity...")
            self.isolation_manager.disable_isolation()
            
            # Step 4: Validate time sync (if requested)
            if validate:
                self.logger.info("Step 4: Validating time synchronization...")
                time.sleep(5)  # Allow time for sync
                self.validate_time_sync()
            
            self.logger.success("=" * 60)
            self.logger.success("CLEANUP COMPLETE - System Restored")
            self.logger.success("=" * 60)
            
            return True
            
        except SystemExit as e:
            self.logger.critical(f"Cleanup validation failed: {e}")
            raise
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return False
    
    def emergency_cleanup(self):
        """
        Emergency cleanup - best effort restoration.
        Does not raise exceptions.
        """
        self.logger.critical("EMERGENCY CLEANUP INITIATED")
        
        try:
            # Restore time
            if self.chronos.original_time:
                self.chronos.restore_original_time()
        except:
            pass
        
        try:
            # Restore isolation
            self.isolation_manager.emergency_restore()
        except:
            pass
        
        try:
            # Delete firewall rules
            self._delete_firewall_rules()
        except:
            pass
        
        try:
            # Enable w32time
            self._enable_w32time()
        except:
            pass
        
        try:
            # Force resync
            self._force_time_resync()
        except:
            pass
        
        self.logger.info("Emergency cleanup completed (best effort)")


# Convenience functions
def cleanup_and_restore(validate: bool = True) -> CleanupManager:
    """
    Factory function to execute full cleanup and restoration.
    
    Example:
        cleanup = cleanup_and_restore(validate=True)
    
    Args:
        validate: Whether to validate time sync (raises SystemExit on failure)
    """
    manager = CleanupManager()
    manager.full_cleanup(validate=validate)
    return manager


def emergency_restore():
    """
    Execute emergency cleanup (best effort, no exceptions).
    
    Use when normal cleanup fails or in exception handlers.
    """
    manager = CleanupManager()
    manager.emergency_cleanup()
