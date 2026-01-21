"""
Genesis Controller: Cross-Platform Time Manipulation Engine.
Supports Windows (SetSystemTime) and Linux (libfaketime/env).
"""
import sys
import os
import logging
import platform
import subprocess
from datetime import datetime, timedelta
import time

class GenesisController:
    """
    Controls system time manipulation.
    On Windows: Uses Kernel API (requires Admin).
    On Linux: Uses libfaketime environment variables for child processes.
    """
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger("Genesis")
        self.os_type = platform.system().lower()
        self.shifted_time = None
        self.libfaketime_path = os.getenv("LIBFAKETIME_PATH", "/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1")

    def shift_time(self, target_datetime: datetime) -> bool:
        """
        Shifts the time.
        On Windows: Changes system clock (Global).
        On Linux: Sets environment variables for next process launch (Local).
        """
        self.logger.info(f"[GENESIS] Shifting time to: {target_datetime}")
        
        if self.os_type == "windows":
            return self._shift_windows(target_datetime)
        else:
            return self._shift_linux(target_datetime)

    def restore_time(self) -> bool:
        """
        Restores time.
        On Windows: Syncs with NTP.
        On Linux: Clears environment variables.
        """
        self.logger.info("[GENESIS] Restoring time...")
        if self.os_type == "windows":
            return self._restore_windows()
        else:
            return self._restore_linux()

    def get_browser_env(self) -> dict:
        """
        Returns the environment variables needed for the browser to see the shifted time.
        Only relevant for Linux/libfaketime.
        """
        if self.os_type != "windows" and self.shifted_time:
            # Calculate offset string for FAKETIME
            # libfaketime supports absolute dates: "@2024-01-01 12:00:00"
            faketime_str = f"@{self.shifted_time.strftime('%Y-%m-%d %H:%M:%S')}"
            return {
                "LD_PRELOAD": self.libfaketime_path,
                "FAKETIME": faketime_str,
                "DONT_FAKE_MONOTONIC": "1" # Important for Chrome/Node
            }
        return {}

    # --- Windows Implementation ---
    def _shift_windows(self, target_datetime: datetime) -> bool:
        try:
            import ctypes
            
            class SYSTEMTIME(ctypes.Structure):
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

            st = SYSTEMTIME()
            st.wYear = target_datetime.year
            st.wMonth = target_datetime.month
            st.wDay = target_datetime.day
            st.wHour = target_datetime.hour
            st.wMinute = target_datetime.minute
            st.wSecond = target_datetime.second
            st.wMilliseconds = target_datetime.microsecond // 1000
            
            kernel32 = ctypes.windll.kernel32
            if kernel32.SetSystemTime(ctypes.byref(st)):
                self.shifted_time = target_datetime
                return True
            return False
        except Exception as e:
            self.logger.error(f"Windows Time Shift Failed: {e}")
            return False

    def _restore_windows(self) -> bool:
        try:
            subprocess.run(['w32tm', '/resync', '/force'], capture_output=True)
            self.shifted_time = None
            return True
        except:
            return False

    # --- Linux Implementation ---
    def _shift_linux(self, target_datetime: datetime) -> bool:
        # On Linux (Container), we don't change system clock usually.
        # We just set the internal state so get_browser_env() returns the right values.
        self.shifted_time = target_datetime
        # Check if libfaketime exists
        if not os.path.exists(self.libfaketime_path):
             self.logger.warning(f"libfaketime not found at {self.libfaketime_path}. Time shift may fail for child processes.")
        return True

    def _restore_linux(self) -> bool:
        self.shifted_time = None
        return True
