"""
CHRONOS Time Engine v2.1 - Kernel-Level Time Manipulation
Direct interface with Windows kernel32.dll for temporal shifts
FULLY COMPLIANT with Report Section 3.1 & 3.2
"""

import ctypes
import ctypes.wintypes
import subprocess
import datetime
from datetime import timedelta
import time
from typing import Optional, Tuple

class SYSTEMTIME(ctypes.Structure):
    """Windows SYSTEMTIME structure for kernel32 API"""
    _fields_ = [
        ('wYear', ctypes.wintypes.WORD),
        ('wMonth', ctypes.wintypes.WORD),
        ('wDayOfWeek', ctypes.wintypes.WORD),
        ('wDay', ctypes.wintypes.WORD),
        ('wHour', ctypes.wintypes.WORD),
        ('wMinute', ctypes.wintypes.WORD),
        ('wSecond', ctypes.wintypes.WORD),
        ('wMilliseconds', ctypes.wintypes.WORD),
    ]

class Chronos:
    """
    Time Manipulation Engine with NTP neutralization
    Implements Method 4: Time-Shifted Injection protocol
    REPORT COMPLIANT: Sections 3.1, 3.2, 4.1
    """
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.original_time = None
        self.ntp_killed = False
        self.firewall_locked = False
        self._store_original_time()
        
        from utils.logger import get_logger
        self.logger = get_logger()
    
    def _store_original_time(self):
        """Store current system time for restoration"""
        system_time = SYSTEMTIME()
        self.kernel32.GetSystemTime(ctypes.byref(system_time))
        
        self.original_time = datetime.datetime(
            year=system_time.wYear,
            month=system_time.wMonth,
            day=system_time.wDay,
            hour=system_time.wHour,
            minute=system_time.wMinute,
            second=system_time.wSecond,
            microsecond=system_time.wMilliseconds * 1000
        )
        
        self.logger.info(f"Original time stored: {self.original_time}")
    
    def block_ntp_firewall(self):
        """
        REPORT SECTION 3.2: Network Firewall Blockade
        Hermetically seal UDP Port 123 to prevent NTP leakage
        """
        self.logger.warning("Engaging FIREWALL LOCK on UDP Port 123...")
        
        try:
            # Rule 1: Block outbound UDP 123 (NTP requests)
            cmd_out = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                "name=CHRONOS_NTP_BLOCK_OUT",
                "protocol=UDP", "dir=out", 
                "remoteport=123", "action=block",
                "enable=yes"
            ]
            result = subprocess.run(cmd_out, capture_output=True, shell=True)
            
            # Rule 2: Block inbound UDP 123 (NTP responses)
            cmd_in = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                "name=CHRONOS_NTP_BLOCK_IN",
                "protocol=UDP", "dir=in",
                "localport=123", "action=block",
                "enable=yes"
            ]
            subprocess.run(cmd_in, capture_output=True, shell=True)
            
            self.firewall_locked = True
            self.logger.success("Firewall: NTP traffic hermetically sealed (UDP 123 blocked)")
            
        except Exception as e:
            self.logger.error(f"Firewall lock failed: {e}")
            raise RuntimeError("Critical: Unable to establish firewall blockade")
    
    def unblock_ntp_firewall(self):
        """Remove firewall rules blocking NTP"""
        self.logger.info("Disengaging firewall lock...")
        
        try:
            # Remove outbound rule
            cmd_out = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                "name=CHRONOS_NTP_BLOCK_OUT"
            ]
            subprocess.run(cmd_out, capture_output=True, shell=True)
            
            # Remove inbound rule
            cmd_in = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                "name=CHRONOS_NTP_BLOCK_IN"
            ]
            subprocess.run(cmd_in, capture_output=True, shell=True)
            
            self.firewall_locked = False
            self.logger.success("Firewall lock removed - NTP traffic restored")
            
        except Exception as e:
            self.logger.warning(f"Firewall unlock warning: {e}")
    
    def kill_ntp(self):
        """
        REPORT SECTION 3.1: W32Time Kill Switch
        Neutralize Windows Time Service AND block network traffic
        """
        self.logger.critical("NEUTRALIZING Windows Time Service...")
        
        try:
            # Step 1: Stop Windows Time service
            subprocess.run(["net", "stop", "w32time"], 
                         capture_output=True, shell=True, timeout=10)
            
            # Step 2: Disable service startup
            subprocess.run(["sc", "config", "w32time", "start=", "disabled"], 
                         capture_output=True, shell=True)
            
            # Step 3: CRITICAL - Engage firewall blockade (Report 3.2)
            self.block_ntp_firewall()
            
            # Step 4: Kill any lingering time sync processes
            subprocess.run(["taskkill", "/F", "/IM", "w32tm.exe"],
                         capture_output=True, shell=True)
            
            self.ntp_killed = True
            self.logger.success("NTP Service KILLED + Firewall LOCKED. System time detached from consensus reality.")
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Service stop timeout - forcing continuation")
            self.ntp_killed = True
            
        except Exception as e:
            self.logger.error(f"Failed to kill NTP: {e}")
            raise RuntimeError("Critical: NTP neutralization failed")
    
    def restore_ntp(self):
        """
        Restore Windows Time Service and remove ALL blockades
        """
        self.logger.info("RESTORING Windows Time Service...")
        
        try:
            # Step 1: Remove firewall blockade FIRST
            if self.firewall_locked:
                self.unblock_ntp_firewall()
            
            # Step 2: Re-enable time service
            subprocess.run(["sc", "config", "w32time", "start=", "auto"], 
                         capture_output=True, shell=True)
            
            # Step 3: Start service
            subprocess.run(["net", "start", "w32time"], 
                         capture_output=True, shell=True, timeout=10)
            
            # Step 4: Force immediate resync
            time.sleep(1)
            subprocess.run(["w32tm", "/resync", "/force"], 
                         capture_output=True, shell=True)
            
            self.ntp_killed = False
            self.logger.success("Time synchronization RESTORED to consensus reality.")
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Service start timeout - may require manual intervention")
            
        except Exception as e:
            self.logger.error(f"Failed to restore NTP: {e}")
    
    def time_jump(self, days_ago: int) -> bool:
        """
        REPORT SECTION 4.1: Kernel-Level Time Shift
        Execute temporal shift to specified days in the past
        
        Args:
            days_ago: Number of days to shift backwards
            
        Returns:
            Success status
        """
        if not self.ntp_killed:
            self.logger.critical("WARNING: NTP not killed! Time jump WILL be reverted!")
            return False
        
        if not self.firewall_locked:
            self.logger.critical("WARNING: Firewall not locked! Background apps may leak NTP!")
        
        target_date = self.original_time - timedelta(days=days_ago)
        self.logger.critical(f"INITIATING TEMPORAL JUMP: T-{days_ago} Days")
        self.logger.info(f"Target: {target_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        try:
            # Create SYSTEMTIME structure (UTC required)
            sys_time = SYSTEMTIME()
            sys_time.wYear = target_date.year
            sys_time.wMonth = target_date.month
            sys_time.wDay = target_date.day
            sys_time.wHour = target_date.hour
            sys_time.wMinute = target_date.minute
            sys_time.wSecond = target_date.second
            sys_time.wMilliseconds = target_date.microsecond // 1000
            sys_time.wDayOfWeek = target_date.weekday()
            
            # Execute kernel-level time shift via kernel32.dll
            result = self.kernel32.SetSystemTime(ctypes.byref(sys_time))
            
            if result != 0:
                self.logger.success(f"TEMPORAL SHIFT COMPLETE. Reality now at: T-{days_ago}")
                time.sleep(1)  # Allow system to stabilize
                return True
            else:
                error_code = ctypes.GetLastError()
                self.logger.error(f"SetSystemTime failed. Win32 Error: {error_code}")
                
                # Common error codes
                if error_code == 1314:
                    self.logger.error("ERROR 1314: Privilege not held. Run as Administrator!")
                elif error_code == 87:
                    self.logger.error("ERROR 87: Invalid parameter in SYSTEMTIME structure")
                    
                return False
                
        except Exception as e:
            self.logger.error(f"Time jump exception: {e}")
            return False
    
    def restore_original_time(self) -> bool:
        """Restore system to original time before shifts"""
        if not self.original_time:
            self.logger.warning("No original time stored!")
            return False
        
        self.logger.info("RESTORING original timeline...")
        
        try:
            sys_time = SYSTEMTIME()
            sys_time.wYear = self.original_time.year
            sys_time.wMonth = self.original_time.month
            sys_time.wDay = self.original_time.day
            sys_time.wHour = self.original_time.hour
            sys_time.wMinute = self.original_time.minute
            sys_time.wSecond = self.original_time.second
            sys_time.wMilliseconds = self.original_time.microsecond // 1000
            sys_time.wDayOfWeek = self.original_time.weekday()
            
            result = self.kernel32.SetSystemTime(ctypes.byref(sys_time))
            
            if result != 0:
                self.logger.success("Original timeline RESTORED.")
                return True
            else:
                error_code = ctypes.GetLastError()
                self.logger.error(f"Failed to restore time! Win32 Error: {error_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Time restoration exception: {e}")
            return False
    
    def get_current_time(self) -> datetime.datetime:
        """Get current system time"""
        system_time = SYSTEMTIME()
        self.kernel32.GetSystemTime(ctypes.byref(system_time))
        
        return datetime.datetime(
            year=system_time.wYear,
            month=system_time.wMonth,
            day=system_time.wDay,
            hour=system_time.wHour,
            minute=system_time.wMinute,
            second=system_time.wSecond,
            microsecond=system_time.wMilliseconds * 1000
        )
    
    def cleanup(self):
        """Emergency cleanup - restore time and NTP"""
        self.logger.critical("EMERGENCY CLEANUP INITIATED")
        
        try:
            # Restore time first
            if self.original_time:
                self.restore_original_time()
            
            # Remove firewall blocks
            if self.firewall_locked:
                self.unblock_ntp_firewall()
            
            # Restore NTP service
            if self.ntp_killed:
                self.restore_ntp()
                
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
            # Best effort - try individual components
            try:
                self.unblock_ntp_firewall()
            except:
                pass
            try:
                subprocess.run(["sc", "config", "w32time", "start=", "auto"], 
                             capture_output=True, shell=True)
            except:
                pass