"""
Genesis Controller: Kernel-level time manipulation engine.
Implements Windows SetSystemTime API interface for temporal shifting.
"""

import ctypes
import ctypes.wintypes as wintypes
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging
import time


class SYSTEMTIME(ctypes.Structure):
    """Windows SYSTEMTIME structure for kernel time operations."""
    _fields_ = [
        ('wYear', ctypes.c_uint16),
        ('wMonth', ctypes.c_uint16),
        ('wDayOfWeek', ctypes.c_uint16),
        ('wDay', ctypes.c_uint16),
        ('wHour', ctypes.c_uint16),
        ('wMinute', ctypes.c_uint16),
        ('wSecond', ctypes.c_uint16),
        ('wMilliseconds', ctypes.c_uint16),
    ]


class GenesisController:
    """
    Controls system time manipulation at the kernel level.
    Requires administrator privileges and SE_SYSTEMTIME_NAME privilege.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize Genesis Controller with privilege verification."""
        self.logger = logger or logging.getLogger(__name__)
        self.kernel32 = ctypes.windll.kernel32
        self.original_time = None
        self.current_shifted_time = None
        
        # Verify SE_SYSTEMTIME_NAME privilege
        self._verify_privileges()
    
    def _verify_privileges(self) -> bool:
        """Verify SE_SYSTEMTIME_NAME privilege is available."""
        try:
            # Check if we can read system time
            st = SYSTEMTIME()
            self.kernel32.GetSystemTime(ctypes.byref(st))
            return True
        except Exception as e:
            self.logger.error(f"Privilege verification failed: {e}")
            raise PermissionError("SE_SYSTEMTIME_NAME privilege required")
    
    def shift_time(self, target_datetime: datetime) -> bool:
        """
        Shift system time to target datetime.
        
        Args:
            target_datetime: Target UTC datetime to shift to
            
        Returns:
            bool: Success status
        """
        try:
            # Store original time for restoration
            self.original_time = self._get_system_time()
            
            # Create SYSTEMTIME structure
            st = SYSTEMTIME()
            st.wYear = target_datetime.year
            st.wMonth = target_datetime.month
            st.wDay = target_datetime.day
            st.wHour = target_datetime.hour
            st.wMinute = target_datetime.minute
            st.wSecond = target_datetime.second
            st.wMilliseconds = target_datetime.microsecond // 1000
            
            # Calculate day of week (0 = Sunday)
            st.wDayOfWeek = (target_datetime.weekday() + 1) % 7
            
            # Set system time
            result = self.kernel32.SetSystemTime(ctypes.byref(st))
            
            if result:
                self.current_shifted_time = target_datetime
                self.logger.info(f"System time shifted to: {target_datetime}")
                
                # Verify the shift
                time.sleep(0.1)
                current = self._get_system_time()
                delta = abs((current - target_datetime).total_seconds())
                
                if delta > 5:
                    self.logger.warning(f"Time shift verification failed, delta: {delta}s")
                    return False
                
                return True
            else:
                error_code = ctypes.get_last_error()
                self.logger.error(f"SetSystemTime failed with error: {error_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Time shift failed: {e}")
            return False
    
    def advance_time(self, hours: float) -> bool:
        """
        Advance system time by specified hours from current shifted time.
        
        Args:
            hours: Number of hours to advance
            
        Returns:
            bool: Success status
        """
        if not self.current_shifted_time:
            self.logger.error("No shifted time set, cannot advance")
            return False
        
        new_time = self.current_shifted_time + timedelta(hours=hours)
        return self.shift_time(new_time)
    
    def _get_system_time(self) -> datetime:
        """Get current system time as datetime."""
        st = SYSTEMTIME()
        self.kernel32.GetSystemTime(ctypes.byref(st))
        
        return datetime(
            year=st.wYear,
            month=st.wMonth,
            day=st.wDay,
            hour=st.wHour,
            minute=st.wMinute,
            second=st.wSecond,
            microsecond=st.wMilliseconds * 1000
        )
    
    def restore_time(self) -> bool:
        """Restore system time to original or current real time."""
        try:
            if self.original_time:
                # Calculate elapsed time since shift
                elapsed = datetime.utcnow() - self.original_time
                
                # Restore to current real time
                real_time = self.original_time + elapsed
                result = self.shift_time(real_time)
                
                if result:
                    self.logger.info("System time restored successfully")
                    self.original_time = None
                    self.current_shifted_time = None
                
                return result
            else:
                # No original time stored, sync with NTP
                return self._sync_with_ntp()
                
        except Exception as e:
            self.logger.error(f"Time restoration failed: {e}")
            return False
    
    def _sync_with_ntp(self) -> bool:
        """Synchronize with NTP server (requires NTP service enabled)."""
        import subprocess
        try:
            # Start w32time service
            subprocess.run(['sc', 'config', 'w32time', 'start=', 'auto'], 
                         capture_output=True, check=False)
            subprocess.run(['net', 'start', 'w32time'], 
                         capture_output=True, check=False)
            
            # Force sync
            result = subprocess.run(['w32tm', '/resync', '/force'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("NTP synchronization successful")
                return True
            else:
                self.logger.warning(f"NTP sync failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"NTP sync error: {e}")
            return False
    
    def force_restore(self) -> bool:
        """Force restore time using all available methods."""
        # Try normal restoration
        if self.restore_time():
            return True
        
        # Try NTP sync
        if self._sync_with_ntp():
            return True
        
        # Last resort: Query time API and set manually
        try:
            import requests
            response = requests.get('http://worldtimeapi.org/api/ip', timeout=10)
            if response.status_code == 200:
                from dateutil.parser import parse
                server_time = parse(response.json()['datetime'])
                return self.shift_time(server_time)
        except:
            pass
        
        self.logger.critical("All restoration methods failed")
        return False
    
    def get_time_offset(self) -> Optional[timedelta]:
        """Get current time offset from real time."""
        if self.original_time and self.current_shifted_time:
            real_elapsed = datetime.utcnow() - self.original_time
            shifted_elapsed = self.current_shifted_time - self.original_time
            return shifted_elapsed - real_elapsed
        return None