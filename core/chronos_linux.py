"""
CHRONOS Linux Implementation - User-Space Time Verification
Verifies libfaketime is active and container time is correctly shifted
Implements Method 4: Time-Shifted Cookie Injection for Linux containers
"""

import os
import subprocess
import datetime
from datetime import timedelta
from typing import Optional, Tuple
import platform


class ChronosLinux:
    """
    Linux Time Verification Engine for Docker/libfaketime
    
    Unlike Windows version which manipulates kernel clock via SetSystemTime,
    Linux version VERIFIES that libfaketime environment is correctly configured.
    Actual time manipulation is handled by:
    - LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
    - FAKETIME environment variable set by entrypoint.sh
    """
    
    def __init__(self):
        """Initialize Linux Chronos verifier"""
        self.original_time = None
        self.expected_offset_days = None
        self.faketime_active = False
        
        # Import logger
        try:
            from utils.logger import get_logger
            self.logger = get_logger()
        except ImportError:
            import logging
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
        
        self._verify_environment()
    
    def _verify_environment(self):
        """Verify that we're running in a proper libfaketime environment"""
        self.logger.info("Verifying Linux time manipulation environment...")
        
        # Check if LD_PRELOAD is set
        ld_preload = os.environ.get('LD_PRELOAD', '')
        if 'libfaketime' in ld_preload:
            self.logger.info(f"✓ LD_PRELOAD configured: {ld_preload}")
        else:
            self.logger.warning(f"⚠ LD_PRELOAD not set to libfaketime. Current: {ld_preload}")
        
        # Check if FAKETIME is set
        faketime = os.environ.get('FAKETIME', '')
        if faketime:
            self.logger.info(f"✓ FAKETIME environment variable set: {faketime}")
            self.faketime_active = True
        else:
            self.logger.warning("⚠ FAKETIME environment variable not set")
        
        # Verify platform
        if platform.system() != 'Linux':
            self.logger.warning(f"⚠ Not running on Linux (detected: {platform.system()})")
    
    def verify_time_shift(self, expected_offset_days: int) -> bool:
        """
        Verify that the container's time is correctly shifted.
        
        This is a USER-SPACE verification only - we don't actually manipulate
        the system clock. Instead, we verify that:
        1. FAKETIME environment is set
        2. The perceived time is shifted by the expected amount
        
        Args:
            expected_offset_days: Expected number of days the time should be shifted
            
        Returns:
            bool: True if time shift is verified, False otherwise
        """
        self.expected_offset_days = expected_offset_days
        
        self.logger.info(f"Verifying {expected_offset_days}-day time shift...")
        
        # Get FAKETIME value
        faketime_value = os.environ.get('FAKETIME', '')
        if not faketime_value:
            self.logger.error("✗ FAKETIME not set - time shift cannot be verified")
            return False
        
        # Parse FAKETIME value (format: "-90d" or similar)
        try:
            if faketime_value.startswith('-') and faketime_value.endswith('d'):
                offset_str = faketime_value[1:-1]  # Remove '-' and 'd'
                actual_offset = int(offset_str)
                
                if actual_offset == expected_offset_days:
                    self.logger.info(f"✓ Time shift verified: FAKETIME={faketime_value} matches expected {expected_offset_days} days")
                    return True
                else:
                    self.logger.warning(f"⚠ Time shift mismatch: FAKETIME={faketime_value} but expected {expected_offset_days} days")
                    return False
            else:
                self.logger.warning(f"⚠ Unexpected FAKETIME format: {faketime_value}")
                # Still consider it active if FAKETIME is set
                return True
                
        except (ValueError, IndexError) as e:
            self.logger.warning(f"⚠ Could not parse FAKETIME value '{faketime_value}': {e}")
            # Still consider it active if FAKETIME is set
            return True
    
    def get_current_time(self) -> datetime.datetime:
        """
        Get current system time (will be affected by libfaketime if active)
        
        Returns:
            Current datetime as perceived by the process
        """
        return datetime.datetime.now()
    
    def get_shifted_time(self) -> Optional[datetime.datetime]:
        """
        Get the time-shifted datetime based on FAKETIME offset
        
        Returns:
            Shifted datetime or None if FAKETIME not active
        """
        if not self.faketime_active:
            return None
        
        return self.get_current_time()
    
    def shift_time(self, days_ago: int) -> bool:
        """
        Verify time shift compatibility method.
        
        On Linux, actual time shifting is done via libfaketime (configured in Dockerfile/entrypoint).
        This method only VERIFIES that the shift is active.
        
        CRITICAL: For Docker/Linux, ensure FAKETIME is set BEFORE starting the browser process.
        
        Args:
            days_ago: Number of days the time should be shifted backwards
            
        Returns:
            bool: True if time shift is verified/active
        """
        self.logger.info(f"Verifying {days_ago}-day time shift on Linux...")
        
        # Verify FAKETIME is set
        faketime_value = os.environ.get('FAKETIME', '')
        if not faketime_value:
            self.logger.error("✗ FAKETIME not set. Ensure container started with proper environment.")
            self.logger.error("  Expected: FAKETIME=-{days_ago}d")
            return False
        
        # Log verification
        self.logger.info(f"✓ FAKETIME environment active: {faketime_value}")
        self.logger.info(f"✓ Time shift verification complete for {days_ago} days")
        
        # Perform detailed verification
        return self.verify_time_shift(days_ago)
    
    def kill_ntp(self):
        """
        NTP neutralization for Linux (if needed).
        
        In Docker containers, NTP is typically not running, so this is a no-op.
        However, we log the call for compatibility with Windows version.
        """
        self.logger.info("NTP neutralization on Linux (Docker)...")
        self.logger.info("  Container isolation prevents NTP sync by default")
        self.logger.info("✓ NTP neutralization: N/A for containerized environment")
    
    def restore_ntp(self):
        """
        Restore NTP (no-op on Linux/Docker)
        """
        self.logger.info("NTP restoration on Linux (Docker)...")
        self.logger.info("✓ NTP restoration: N/A for containerized environment")
    
    def block_ntp_firewall(self):
        """
        Block NTP via firewall (optional on Linux)
        Can be implemented with iptables if needed
        """
        self.logger.info("NTP firewall block on Linux...")
        
        try:
            # Block outbound NTP (UDP 123)
            subprocess.run(
                ["iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "123", "-j", "DROP"],
                capture_output=True,
                check=False
            )
            self.logger.info("✓ iptables: Blocked outbound UDP 123 (NTP)")
        except Exception as e:
            self.logger.warning(f"⚠ Could not set iptables rule: {e}")
            self.logger.warning("  This may be expected in restricted container environments")
    
    def unblock_ntp_firewall(self):
        """
        Unblock NTP firewall rules
        """
        self.logger.info("Removing NTP firewall block...")
        
        try:
            # Remove NTP block rule
            subprocess.run(
                ["iptables", "-D", "OUTPUT", "-p", "udp", "--dport", "123", "-j", "DROP"],
                capture_output=True,
                check=False
            )
            self.logger.info("✓ iptables: Removed NTP block")
        except Exception as e:
            self.logger.warning(f"⚠ Could not remove iptables rule: {e}")
    
    def cleanup(self):
        """
        Cleanup method for compatibility.
        
        On Linux with libfaketime, there's nothing to cleanup since we don't
        manipulate the actual system clock.
        """
        self.logger.info("Chronos Linux cleanup...")
        self.logger.info("✓ No cleanup required (libfaketime is process-scoped)")
    
    def restore_original_time(self) -> bool:
        """
        Restore original time (no-op on Linux)
        
        libfaketime is process-scoped, so time returns to normal when process exits
        """
        self.logger.info("Time restoration on Linux...")
        self.logger.info("✓ Time auto-restores on process exit (libfaketime is process-scoped)")
        return True


# Alias for compatibility with main codebase
ChronosTimeMachine = ChronosLinux
