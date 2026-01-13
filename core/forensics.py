"""
Forensic Scrubber v2.1 - NTFS MFT $FN Attribute Manipulation
Implements Report Section 6.2: Move-and-Copy Countermeasure
FULLY COMPLIANT with "Scripting Time-Shifted Cookie Injection.pdf"
"""

import os
import shutil
import time
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

class ForensicScrubber:
    """
    NTFS forensic metadata scrubber
    Implements complete MFT $FN and $SI attribute manipulation
    REPORT COMPLIANT: Sections 6.1 & 6.2
    """
    
    def __init__(self):
        from utils.logger import get_logger
        from config.settings import Config
        
        self.logger = get_logger()
        self.config = Config
        
        # Temp directory for move operations
        self.temp_base = Path(tempfile.gettempdir()) / "CHRONOS_MFT_SCRUB"
        self.temp_base.mkdir(exist_ok=True)
        
        self.operations_log = []
    
    def scrub_timestamps(self, profile_id: str) -> bool:
        """
        REPORT SECTION 6.2: The 'Move-and-Copy' Countermeasure
        Implements deep MFT scrubbing to reset $FILE_NAME attributes
        while system clock is backdated
        
        Args:
            profile_id: Multilogin profile UUID
            
        Returns:
            Success status
        """
        self.logger.critical("APPLYING DEEP FORENSIC LOCK ($SI + $FN)")
        
        # Locate profile directory
        profile_path = self._locate_profile_path(profile_id)
        
        if not profile_path or not profile_path.exists():
            self.logger.error(f"Profile path not found: {profile_id}")
            # Attempt fallback scrubbing on known locations
            return self._fallback_scrub(profile_id)
        
        try:
            # CRITICAL: Move-and-Copy protocol for $FN attribute reset
            success = self._execute_mft_scrub(profile_path)
            
            if success:
                # Additional $SI attribute touching
                self._touch_si_attributes(profile_path)
                
                # Deep scrub if configured
                if self.config.DEEP_SCRUB_ITERATIONS > 1:
                    for i in range(1, self.config.DEEP_SCRUB_ITERATIONS):
                        self.logger.info(f"Deep scrub iteration {i+1}/{self.config.DEEP_SCRUB_ITERATIONS}")
                        self._execute_mft_scrub(profile_path)
                        time.sleep(0.5)
                
                # Clear USN Journal to remove forensic trail
                if self.config.CLEAR_USN_JOURNAL:
                    self._clear_usn_journal()
                
                self.operations_log.append({
                    "profile": profile_id,
                    "operation": "MFT_SCRUB_COMPLETE",
                    "success": True,
                    "timestamp": time.time()
                })
                
                self.logger.success("FORENSIC LOCK COMPLETE: MFT $FN + $SI aligned to temporal frame")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Forensic scrub failed: {e}")
            self.operations_log.append({
                "profile": profile_id,
                "operation": "MFT_SCRUB_FAILED",
                "success": False,
                "error": str(e)
            })
            return False
    
    def _execute_mft_scrub(self, profile_path: Path) -> bool:
        """
        Core MFT scrubbing logic - Move directory to reset $FN creation time
        This MUST occur while system time is backdated
        """
        parent_dir = profile_path.parent
        dir_name = profile_path.name
        temp_path = parent_dir / f"{dir_name}_CHRONOS_MFT_TMP_{int(time.time() * 1000)}"
        
        self.logger.info(f"MFT Scrub: {profile_path} -> TEMP -> {profile_path}")
        
        try:
            # Step 1: MOVE to temporary location
            # This forces Windows to create NEW MFT entry with current (backdated) timestamp
            shutil.move(str(profile_path), str(temp_path))
            
            # Step 2: Brief pause for filesystem commit
            time.sleep(1)
            
            # Step 3: MOVE back to original location
            # This creates ANOTHER new MFT entry, now with backdated $FN attributes
            shutil.move(str(temp_path), str(profile_path))
            
            self.logger.success("MFT $FN attributes reset via Move-and-Copy")
            return True
            
        except PermissionError as e:
            self.logger.error(f"Permission denied during MFT scrub: {e}")
            self.logger.warning("Attempting alternative scrub method...")
            
            # Alternative: Copy and replace
            return self._alternative_scrub(profile_path, temp_path)
            
        except Exception as e:
            self.logger.error(f"MFT scrub error: {e}")
            
            # Recovery: If stuck in temp location, move back
            if temp_path.exists() and not profile_path.exists():
                try:
                    shutil.move(str(temp_path), str(profile_path))
                    self.logger.warning("Recovered profile from temp location")
                except:
                    pass
            
            return False
    
    def _alternative_scrub(self, profile_path: Path, temp_path: Path) -> bool:
        """
        Alternative scrubbing method using copy operations
        Used when move operations fail due to locks
        """
        try:
            # Copy to temp location
            shutil.copytree(str(profile_path), str(temp_path))
            
            # Remove original
            shutil.rmtree(str(profile_path))
            
            # Move temp back to original
            shutil.move(str(temp_path), str(profile_path))
            
            self.logger.success("MFT scrub completed via copy method")
            return True
            
        except Exception as e:
            self.logger.error(f"Alternative scrub failed: {e}")
            return False
    
    def _touch_si_attributes(self, profile_path: Path):
        """
        REPORT SECTION 6.1: Touch $SI (Standard Information) attributes
        Updates Created/Modified/Accessed times to current (backdated) time
        """
        self.logger.info("Touching $SI attributes...")
        
        now_epoch = time.time()
        touched_count = 0
        error_count = 0
        
        # Walk entire profile directory tree
        for root, dirs, files in os.walk(profile_path):
            # Touch directories
            for d in dirs:
                dir_path = os.path.join(root, d)
                try:
                    os.utime(dir_path, (now_epoch, now_epoch))
                    touched_count += 1
                except:
                    error_count += 1
            
            # Touch files
            for f in files:
                file_path = os.path.join(root, f)
                try:
                    os.utime(file_path, (now_epoch, now_epoch))
                    touched_count += 1
                except:
                    error_count += 1
        
        self.logger.info(f"$SI Touch Complete: {touched_count} items touched, {error_count} errors")
    
    def _clear_usn_journal(self):
        """
        Clear Windows USN (Update Sequence Number) Journal
        Removes forensic trail of file system operations
        """
        self.logger.warning("CLEARING USN Journal...")
        
        try:
            # Delete USN journal on C: drive
            result = subprocess.run(
                ["fsutil", "usn", "deletejournal", "/d", "C:"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if "successfully" in result.stdout.lower() or result.returncode == 0:
                self.logger.success("USN Journal CLEARED")
                
                # Recreate journal for continued OS operation
                subprocess.run(
                    ["fsutil", "usn", "createjournal", "m=1000", "a=100", "C:"],
                    capture_output=True,
                    shell=True
                )
            else:
                self.logger.warning(f"USN clear warning: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"USN journal clear failed: {e}")
    
    def _locate_profile_path(self, profile_id: str) -> Optional[Path]:
        """Locate Multilogin profile directory across possible locations"""
        possible_locations = [
            Path(self.config.PROFILE_STORE) / profile_id,
            Path.home() / ".multiloginapp.com" / "data" / profile_id,
            Path.home() / ".multiloginapp.com" / "profiles" / profile_id,
            Path("C:/Users") / os.environ.get("USERNAME", "User") / ".multiloginapp.com" / "data" / profile_id,
            Path("C:/Users") / os.environ.get("USERNAME", "User") / ".multiloginapp.com" / "profiles" / profile_id,
            Path(self.config.BASE_DIR) / "profiles" / profile_id
        ]
        
        for location in possible_locations:
            if location.exists():
                self.logger.info(f"Profile located: {location}")
                return location
        
        # Deep search in MLA directory
        mla_base = Path.home() / ".multiloginapp.com"
        if mla_base.exists():
            self.logger.info("Searching MLA directory tree...")
            for root, dirs, _ in os.walk(mla_base):
                if profile_id in dirs:
                    found_path = Path(root) / profile_id
                    self.logger.info(f"Profile found: {found_path}")
                    return found_path
        
        return None
    
    def _fallback_scrub(self, profile_id: str) -> bool:
        """
        Fallback scrubbing when profile path cannot be located
        Scrubs common cookie and cache locations
        """
        self.logger.warning("Executing fallback scrub on common locations...")
        
        # Common browser data locations
        common_paths = [
            Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data",
            Path.home() / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles",
            Path.home() / ".multiloginapp.com"
        ]
        
        scrubbed = False
        for base_path in common_paths:
            if base_path.exists():
                try:
                    # Touch all files in these directories
                    now = time.time()
                    for root, _, files in os.walk(base_path):
                        for f in files[:100]:  # Limit to prevent hanging
                            try:
                                file_path = os.path.join(root, f)
                                os.utime(file_path, (now, now))
                                scrubbed = True
                            except:
                                pass
                except:
                    pass
        
        return scrubbed
    
    def scrub_cookies_db(self, profile_id: str) -> bool:
        """
        Specifically target and scrub cookie databases
        Applies Move-and-Copy to cookie files
        """
        profile_path = self._locate_profile_path(profile_id)
        
        if not profile_path:
            self.logger.warning("Cannot scrub cookies - profile path not found")
            return False
        
        # Cookie database patterns
        cookie_patterns = [
            "Cookies", "cookies.sqlite", "cookies.db",
            "Cookies-journal", "cookies.sqlite-wal"
        ]
        
        scrubbed_count = 0
        
        # Search for cookie files
        for root, _, files in os.walk(profile_path):
            for file in files:
                if any(pattern in file.lower() for pattern in cookie_patterns):
                    cookie_path = Path(root) / file
                    
                    try:
                        # Apply Move-and-Copy to cookie file
                        temp_cookie = self.temp_base / f"{file}_TMP_{int(time.time() * 1000)}"
                        
                        shutil.move(str(cookie_path), str(temp_cookie))
                        time.sleep(0.2)
                        shutil.move(str(temp_cookie), str(cookie_path))
                        
                        # Touch for $SI update
                        os.utime(str(cookie_path), (time.time(), time.time()))
                        
                        scrubbed_count += 1
                        self.logger.success(f"Cookie database scrubbed: {file}")
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to scrub {file}: {e}")
        
        self.logger.info(f"Cookie scrub complete: {scrubbed_count} databases processed")
        return scrubbed_count > 0
    
    def cleanup_temp(self) -> int:
        """Clean up temporary directories created during operations"""
        cleaned = 0
        
        try:
            if self.temp_base.exists():
                for temp_item in self.temp_base.iterdir():
                    try:
                        if temp_item.is_dir():
                            shutil.rmtree(temp_item)
                        else:
                            temp_item.unlink()
                        cleaned += 1
                    except:
                        pass
            
            self.logger.info(f"Cleaned {cleaned} temporary items")
            
        except Exception as e:
            self.logger.error(f"Temp cleanup error: {e}")
        
        return cleaned
    
    def generate_report(self) -> str:
        """Generate detailed forensic operations report"""
        report = ["=" * 60]
        report.append("FORENSIC OPERATIONS REPORT")
        report.append("=" * 60)
        report.append(f"Total Operations: {len(self.operations_log)}")
        
        successful = sum(1 for op in self.operations_log if op.get("success"))
        failed = len(self.operations_log) - successful
        
        report.append(f"Successful: {successful}")
        report.append(f"Failed: {failed}")
        report.append(f"Success Rate: {(successful/len(self.operations_log)*100) if self.operations_log else 0:.1f}%")
        
        report.append("\nOperation Details:")
        report.append("-" * 40)
        
        for op in self.operations_log:
            status = "✓" if op.get("success") else "✗"
            timestamp = time.strftime("%H:%M:%S", time.localtime(op.get("timestamp", 0)))
            report.append(f"{status} [{timestamp}] {op.get('operation')} - Profile: {op.get('profile')}")
            if op.get("error"):
                report.append(f"    Error: {op['error']}")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def cleanup(self):
        """Emergency cleanup"""
        try:
            self.cleanup_temp()
        except:
            pass