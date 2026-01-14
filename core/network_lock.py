"""
Network Lock Module (MODULE 1: THE VOID - Network Control)
Wrapper for IsolationManager to provide network-level time synchronization blocking.
Maps to CHRONOS_TASK.md Module 1 specifications.
"""

from core.isolation import IsolationManager
from utils.logger import get_logger
import subprocess
import ctypes


class NetworkLock:
    """
    Network-level NTP blocking as specified in CHRONOS_TASK.md Module 1.
    Implements W32Time Kill Switch and NTP Blockade.
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.isolation_manager = IsolationManager(logger=self.logger)
        self._check_admin_privileges()
    
    def _check_admin_privileges(self) -> bool:
        """
        Check for Administrator privileges.
        Requirement from Module 1: W32Time Kill Switch
        """
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                self.logger.error("ERROR: Administrator privileges required!")
                self.logger.error("Please run this script as Administrator")
                raise PermissionError("Administrator privileges required for network operations")
            
            self.logger.info("Administrator privileges verified")
            return True
            
        except Exception as e:
            self.logger.error(f"Privilege check failed: {e}")
            return False
    
    def kill_w32time(self) -> bool:
        """
        W32Time Kill Switch (CHRONOS_TASK.md Module 1, Requirement 1)
        - Set w32time service to DISABLED
        - Stop the service
        - Inject registry key for NoSync
        """
        self.logger.critical("Executing W32Time Kill Switch...")
        
        try:
            # Stop and disable W32Time service
            if not self.isolation_manager._disable_w32time():
                return False
            
            # Inject registry key (HKLM\...\W32Time\Parameters -> Type: NoSync)
            if not self.isolation_manager._disable_ntp_registry():
                return False
            
            self.logger.success("W32Time Kill Switch: COMPLETE")
            return True
            
        except Exception as e:
            self.logger.error(f"W32Time kill failed: {e}")
            return False
    
    def block_ntp(self) -> bool:
        """
        NTP Blockade (CHRONOS_TASK.md Module 1, Requirement 2)
        - Create OUTBOUND BLOCK rule for UDP Port 123
        - Ensure rule takes precedence
        """
        self.logger.critical("Engaging NTP Blockade...")
        
        try:
            if not self.isolation_manager._create_firewall_rules():
                return False
            
            self.logger.success("NTP Blockade: UDP Port 123 BLOCKED")
            return True
            
        except Exception as e:
            self.logger.error(f"NTP blockade failed: {e}")
            return False
    
    def enable_full_isolation(self) -> bool:
        """
        Enable complete network isolation (combines all Module 1 requirements)
        """
        self.logger.critical("INITIATING NETWORK LOCK...")
        
        try:
            # Execute full isolation (includes W32Time kill, registry, firewall, hypervisor)
            success = self.isolation_manager.enable_isolation()
            
            if success:
                self.logger.success("NETWORK LOCK: ENGAGED")
                self.logger.info("System is now temporally isolated from NTP consensus")
            else:
                self.logger.error("NETWORK LOCK: FAILED")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Network lock failed: {e}")
            return False
    
    def verify_isolation(self) -> bool:
        """Verify that network isolation is active"""
        return self.isolation_manager.verify_isolation()
    
    def restore_network(self) -> bool:
        """
        Restore network connectivity and time synchronization
        Part of MODULE 5: RESURRECTION
        """
        self.logger.info("Restoring network connectivity...")
        
        try:
            success = self.isolation_manager.disable_isolation()
            
            if success:
                self.logger.success("Network connectivity RESTORED")
            else:
                self.logger.warning("Network restoration completed with warnings")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Network restoration failed: {e}")
            return False
    
    def emergency_restore(self):
        """Emergency restoration of all network services"""
        self.logger.critical("EMERGENCY NETWORK RESTORATION")
        self.isolation_manager.emergency_restore()


# Convenience function for backward compatibility
def engage_network_lock() -> NetworkLock:
    """Factory function to create and engage network lock"""
    lock = NetworkLock()
    lock.enable_full_isolation()
    return lock
