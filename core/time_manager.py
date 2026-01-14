"""
Time Manager Module (MODULE 1: THE VOID - Time Control)
Wrapper for Chronos to provide kernel-level time manipulation.
Maps to CHRONOS_TASK.md Module 1, Requirement 3 specifications.
"""

from core.chronos import Chronos, SYSTEMTIME
from utils.logger import get_logger
from datetime import datetime, timedelta
import ctypes
from typing import Optional


class TimeManager:
    """
    Kernel Time Shift implementation as specified in CHRONOS_TASK.md Module 1.
    Provides interface to Windows kernel32.dll SetSystemTime functionality.
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.chronos = Chronos()
        self.kernel32 = ctypes.windll.kernel32
        self.original_time = None
    
    def shift_time(self, days_to_shift: int) -> bool:
        """
        Kernel Time Shift (CHRONOS_TASK.md Module 1, Requirement 3)
        
        Uses ctypes.windll.kernel32.SetSystemTime to shift system time.
        Defines SYSTEMTIME C-structure.
        
        Args:
            days_to_shift: Number of days to shift backwards
            
        Returns:
            bool: Success status
            
        Implementation Details:
        - Calculate Target Time: (Now - Days)
        - Convert to UTC
        - Apply to Kernel via SetSystemTime
        - Validate with GetSystemTime
        """
        self.logger.critical(f"KERNEL TIME SHIFT: T-{days_to_shift} days")
        
        try:
            # Store original time if not already stored
            if not self.original_time:
                self.original_time = self.chronos.original_time
                self.logger.info(f"Original time stored: {self.original_time}")
            
            # Calculate target time (Now - Days)
            current_time = datetime.utcnow()
            target_time = current_time - timedelta(days=days_to_shift)
            
            self.logger.info(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            self.logger.info(f"Target time: {target_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Execute time shift via Chronos
            success = self.chronos.time_jump(days_to_shift)
            
            if success:
                # Validate the shift
                validated = self.validate_time_shift(target_time)
                if validated:
                    self.logger.success(f"Time shift VALIDATED: System now at T-{days_to_shift}")
                else:
                    self.logger.warning("Time shift completed but validation uncertain")
                
                return True
            else:
                self.logger.error("Time shift FAILED")
                return False
                
        except Exception as e:
            self.logger.error(f"Time shift exception: {e}")
            return False
    
    def validate_time_shift(self, expected_time: datetime) -> bool:
        """
        Validation: Call GetSystemTime to verify the shift
        (CHRONOS_TASK.md Module 1, Requirement 3)
        """
        try:
            # Get current system time via kernel32
            sys_time = SYSTEMTIME()
            self.kernel32.GetSystemTime(ctypes.byref(sys_time))
            
            current_time = datetime(
                year=sys_time.wYear,
                month=sys_time.wMonth,
                day=sys_time.wDay,
                hour=sys_time.wHour,
                minute=sys_time.wMinute,
                second=sys_time.wSecond
            )
            
            # Compare with expected time (allow 5 second tolerance)
            time_diff = abs((current_time - expected_time).total_seconds())
            
            if time_diff <= 5:
                self.logger.info(f"Time shift validated: {current_time}")
                return True
            else:
                self.logger.warning(f"Time validation skew: {time_diff} seconds")
                return False
                
        except Exception as e:
            self.logger.error(f"Time validation failed: {e}")
            return False
    
    def get_current_time(self) -> datetime:
        """Get current system time via GetSystemTime"""
        return self.chronos.get_current_time()
    
    def restore_original_time(self) -> bool:
        """Restore system to original time before shifts"""
        self.logger.info("Restoring original time...")
        
        try:
            success = self.chronos.restore_original_time()
            
            if success:
                self.logger.success("Original time RESTORED")
            else:
                self.logger.error("Time restoration FAILED")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Time restoration exception: {e}")
            return False
    
    def multiple_time_jumps(self, jump_schedule: list) -> bool:
        """
        Execute multiple time jumps according to schedule.
        Used for Poisson distribution timing (Module 3).
        
        Args:
            jump_schedule: List of (days_ago, duration) tuples
            
        Returns:
            bool: Overall success status
        """
        self.logger.info(f"Executing {len(jump_schedule)} scheduled time jumps")
        
        for i, (days_ago, duration) in enumerate(jump_schedule):
            self.logger.info(f"Jump {i+1}/{len(jump_schedule)}: T-{days_ago} days")
            
            if not self.shift_time(days_ago):
                self.logger.error(f"Jump {i+1} failed, aborting sequence")
                return False
            
            # Note: Actual browser operations would happen here
            # This is just the time management component
            
        return True
    
    def cleanup(self):
        """Emergency cleanup - restore original time"""
        self.logger.critical("TIME MANAGER CLEANUP")
        
        try:
            self.chronos.cleanup()
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")


# Convenience functions
def shift_system_time(days: int) -> TimeManager:
    """
    Factory function to create TimeManager and shift time.
    
    Example:
        tm = shift_system_time(90)  # Shift back 90 days
    """
    manager = TimeManager()
    manager.shift_time(days)
    return manager


def get_systemtime_structure() -> type:
    """
    Return the SYSTEMTIME C-structure for direct manipulation.
    
    SYSTEMTIME structure (as per CHRONOS_TASK.md):
    - wYear: WORD
    - wMonth: WORD
    - wDayOfWeek: WORD
    - wDay: WORD
    - wHour: WORD
    - wMinute: WORD
    - wSecond: WORD
    - wMilliseconds: WORD
    """
    return SYSTEMTIME
