"""
CHRONOS Time Manager - Windows System Time Manipulation via kernel32.dll
Implements NTP blocking and precise temporal shifts for synthetic aging
"""

import ctypes
import ctypes.wintypes
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
import sys

logger = logging.getLogger(__name__)


class SYSTEMTIME(ctypes.Structure):
    """Windows SYSTEMTIME structure for kernel32.SetSystemTime"""
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


class ChronosTimeManager:
    """
    System Time Manager with NTP safety lock
    Requires Administrator privileges for kernel32.SetSystemTime access
    """
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.shell32 = ctypes.windll.shell32
        self.original_time: Optional[datetime] = None
        self.ntp_blocked = False
        
        # Verify administrator privileges
        if not self._check_admin():
            raise PermissionError(
                "Administrator privileges required for time manipulation. "
                "Run script as Administrator."
            )
    
    def _check_admin(self) -> bool:
        """Verify if process has Administrator privileges"""
        try:
            return self.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            # Fallback for older Windows versions
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    def block_ntp(self) -> bool:
        """
        Create Windows Firewall rule to block UDP Port 123 (NTP)
        Safety lock to prevent automatic time sync during manipulation
        """
        try:
            # Block outbound NTP traffic
            cmd_block = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name="CHRONOS_NTP_BLOCK"',
                'dir=out', 'action=block',
                'protocol=UDP', 'remoteport=123',
                'enable=yes'
            ]
            
            result = subprocess.run(
                cmd_block, 
                capture_output=True, 
                text=True, 
                shell=True
            )
            
            if result.returncode == 0:
                self.ntp_blocked = True
                logger.info("NTP blocked successfully via firewall rule")
                return True
            else:
                logger.error(f"Failed to block NTP: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error blocking NTP: {str(e)}")
            return False
    
    def unblock_ntp(self) -> bool:
        """Remove NTP blocking firewall rule"""
        try:
            cmd_unblock = [
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                'name="CHRONOS_NTP_BLOCK"'
            ]
            
            result = subprocess.run(
                cmd_unblock,
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                self.ntp_blocked = False
                logger.info("NTP unblocked successfully")
                return True
            else:
                logger.warning(f"NTP unblock warning: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error unblocking NTP: {str(e)}")
            return False
    
    def get_system_time(self) -> datetime:
        """Get current Windows system time"""
        system_time = SYSTEMTIME()
        self.kernel32.GetSystemTime(ctypes.byref(system_time))
        
        return datetime(
            year=system_time.wYear,
            month=system_time.wMonth,
            day=system_time.wDay,
            hour=system_time.wHour,
            minute=system_time.wMinute,
            second=system_time.wSecond,
            microsecond=system_time.wMilliseconds * 1000
        )
    
    def set_system_time(self, target_time: datetime) -> bool:
        """
        Set Windows system time using kernel32.SetSystemTime
        Time must be in UTC
        """
        try:
            # Convert to UTC if needed
            utc_time = target_time.replace(tzinfo=None)
            
            # Create SYSTEMTIME structure
            system_time = SYSTEMTIME()
            system_time.wYear = utc_time.year
            system_time.wMonth = utc_time.month
            system_time.wDay = utc_time.day
            system_time.wHour = utc_time.hour
            system_time.wMinute = utc_time.minute
            system_time.wSecond = utc_time.second
            system_time.wMilliseconds = utc_time.microsecond // 1000
            system_time.wDayOfWeek = utc_time.weekday()
            
            # Set system time via kernel32
            result = self.kernel32.SetSystemTime(ctypes.byref(system_time))
            
            if result != 0:
                logger.info(f"System time set to: {target_time}")
                return True
            else:
                error_code = ctypes.GetLastError()
                logger.error(f"SetSystemTime failed with error code: {error_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting system time: {str(e)}")
            return False
    
    def shift_time(self, days_offset: int) -> Tuple[bool, datetime]:
        """
        Shift system time by specified number of days
        Negative values shift to past, positive to future
        """
        # Store original time if not already stored
        if self.original_time is None:
            self.original_time = self.get_system_time()
            logger.info(f"Original time stored: {self.original_time}")
        
        current_time = self.get_system_time()
        target_time = current_time + timedelta(days=days_offset)
        
        success = self.set_system_time(target_time)
        return success, target_time
    
    def restore_original_time(self) -> bool:
        """Restore system to original time before shifts"""
        if self.original_time is None:
            logger.warning("No original time stored")
            return False
        
        success = self.set_system_time(self.original_time)
        if success:
            logger.info(f"Time restored to: {self.original_time}")
            self.original_time = None
        return success
    
    def resync_time(self) -> bool:
        """Force Windows time resync with NTP servers"""
        try:
            # First ensure NTP is unblocked
            if self.ntp_blocked:
                self.unblock_ntp()
            
            # Force time resync
            cmd_resync = ['w32tm', '/resync', '/force']
            result = subprocess.run(
                cmd_resync,
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                logger.info("Time resynchronized with NTP servers")
                return True
            else:
                logger.error(f"Time resync failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error resyncing time: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup operations - restore time and unblock NTP"""
        try:
            if self.original_time:
                self.restore_original_time()
            
            if self.ntp_blocked:
                self.unblock_ntp()
            
            # Attempt resync
            self.resync_time()
            
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")


# Context manager support
class ChronosContext:
    """Context manager for safe time manipulation"""
    
    def __init__(self, days_offset: int):
        self.days_offset = days_offset
        self.manager = ChronosTimeManager()
    
    def __enter__(self):
        self.manager.block_ntp()
        self.manager.shift_time(self.days_offset)
        return self.manager
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.manager.cleanup()