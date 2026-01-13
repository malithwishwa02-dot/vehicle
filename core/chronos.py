"""
CHRONOS Time Engine v2.0 - Kernel-Level Time Manipulation
Direct interface with Windows kernel32.dll for temporal shifts
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
    """
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.original_time = None
        self.ntp_killed = False
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
    
    def kill_ntp(self):
        """Neutralize Windows Time Service and block NTP via firewall"""
        self.logger.warning("Neutralizing Windows Time Service (NTP)...")
        
        try:
            # Stop Windows Time service
            subprocess.run(["net", "stop", "w32time"], 
                         capture_output=True, shell=True)
            
            # Disable service startup
            subprocess.run(["sc", "config", "w32time", "start=", "disabled"], 
                         capture_output=True, shell=True)
            
            # Create firewall rule to block NTP (UDP 123)
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                "name=CHRONOS_NTP_BLOCK",
                "dir=out", "action=block",
                "protocol=UDP", "remoteport=123",
                "enable=yes"
            ], capture_output=True, shell=True)
            
            self.ntp_killed = True
            self.logger.success("NTP Service KILLED. System time detached from reality.")
            
        except Exception as e:
            self.logger.error(f"Failed to kill NTP: {e}")
            raise
    
    def restore_ntp(self):
        """Restore Windows Time Service and remove firewall blocks"""
        self.logger.info("Restoring Windows Time Service...")
        
        try:
            # Remove firewall rule
            subprocess.run([
                "netsh", "advfirewall", "firewall", "delete", "rule",
                "name=CHRONOS_NTP_BLOCK"
            ], capture_output=True, shell=True)
            
            # Re-enable time service
            subprocess.run(["sc", "config", "w32time", "start=", "auto"], 
                         capture_output=True, shell=True)
            
            # Start service
            subprocess.run(["net", "start", "w32time"], 
                         capture_output=True, shell=True)
            
            # Force resync
            subprocess.run(["w32tm", "/resync", "/force"], 
                         capture_output=True, shell=True)
            
            self.ntp_killed = False
            self.logger.success("Time synchronization restored to consensus reality.")
            
        except Exception as e:
            self.logger.error(f"Failed to restore NTP: {e}")
    
    def time_jump(self, days_ago: int) -> bool:
        """
        Execute temporal shift to specified days in the past
        
        Args:
            days_ago: Number of days to shift backwards
            
        Returns:
            Success status
        """
        if not self.ntp_killed:
            self.logger.warning("NTP not killed! Time jump may be reverted.")
        
        target_date = self.original_time - timedelta(days=days_ago)
        self.logger.critical(f"INITIATING TEMPORAL JUMP: T-{days_ago} Days")
        self.logger.info(f"Target: {target_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Create SYSTEMTIME structure
            sys_time = SYSTEMTIME()
            sys_time.wYear = target_date.year
            sys_time.wMonth = target_date.month
            sys_time.wDay = target_date.day
            sys_time.wHour = target_date.hour
            sys_time.wMinute = target_date.minute
            sys_time.wSecond = target_date.second
            sys_time.wMilliseconds = target_date.microsecond // 1000
            sys_time.wDayOfWeek = target_date.weekday()
            
            # Execute kernel-level time shift
            result = self.kernel32.SetSystemTime(ctypes.byref(sys_time))
            
            if result != 0:
                self.logger.success(f"TEMPORAL SHIFT COMPLETE. Now at: T-{days_ago}")
                time.sleep(1)  # Allow system to stabilize
                return True
            else:
                error_code = ctypes.GetLastError()
                self.logger.error(f"SetSystemTime failed. Error code: {error_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Time jump failed: {e}")
            return False
    
    def restore_original_time(self) -> bool:
        """Restore system to original time before shifts"""
        if not self.original_time:
            self.logger.warning("No original time stored!")
            return False
        
        self.logger.info("Restoring original timeline...")
        
        try:
            sys_time = SYSTEMTIME()
            sys_time.wYear = self.original_time.year
            sys_time.wMonth = self.original_time.month
            sys_time.wDay = self.original_time.day
            sys_time.wHour = self.original_time.hour
            sys_time.wMinute = self.original_time.minute
            sys_time.wSecond = self.original_time.second
            sys_time.wMilliseconds = self.original_time.microsecond // 1000
            
            result = self.kernel32.SetSystemTime(ctypes.byref(sys_time))
            
            if result != 0:
                self.logger.success("Original timeline restored.")
                return True
            else:
                self.logger.error("Failed to restore original time!")
                return False
                
        except Exception as e:
            self.logger.error(f"Time restoration failed: {e}")
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
        try:
            if self.original_time:
                self.restore_original_time()
            if self.ntp_killed:
                self.restore_ntp()
        except:
            pass  # Best effort cleanup