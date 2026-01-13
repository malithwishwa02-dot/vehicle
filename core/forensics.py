"""
Forensic Scrubber v2.0 - NTFS Metadata Manipulation
Implements Move-and-Back protocol for MFT timestamp alignment
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
    Aligns file system timestamps with shifted temporal frame
    """
    
    def __init__(self):
        from utils.logger import get_logger
        from config.settings import Config
        
        self.logger = get_logger()
        self.config = Config
        
        # Temp directory for move operations
        self.temp_base = Path(tempfile.gettempdir()) / "CHRONOS_FORENSIC"
        self.temp_base.mkdir(exist_ok=True)
        
        self.operations_log = []
    
    def scrub_timestamps(self, profile_id: str) -> bool:
        """
        Apply forensic lock to profile artifacts
        Aligns all timestamps to current (shifted) system time
        
        Args:
            profile_id: Multilogin profile UUID
            
        Returns:
            Success status
        """
        self.logger.warning("Applying Forensic Lock to Profile Artifacts...")
        
        # Attempt to locate profile directory
        profile_path = self._locate_profile_path(profile_id)
        
        if not profile_path or not profile_path.exists():
            self.logger.error(f"Profile path not found: {profile_id}")
            return False
        
        try:
            # Execute Move-and-Back protocol
            temp_path = self.temp_base / f"profile_{int(time.time() * 1000)}"
            
            self.logger.info("Executing MFT rewrite protocol...")
            
            # Step 1: Move to temp (forces MFT rewrite)
            shutil.move(str(profile_path), str(temp_path))
            time.sleep(0.5)  # Allow filesystem to commit
            
            # Step 2: Move back (creates new MFT entries with current time)
            shutil.move(str(temp_path), str(profile_path))
            
            self.operations_log.append({
                "profile": profile_id,
                "operation": "MFT_REWRITE",
                "success": True,
                "timestamp": time.time()
            })
            
            self.logger.success("Forensic Lock Applied: Metadata aligned to temporal frame")
            
            # Deep scrub if enabled
            if self.config.FORENSIC_SCRUB and self.config.DEEP_SCRUB_ITERATIONS > 1:
                self._deep_scrub(profile_path)
            
            # Clear USN Journal if enabled
            if self.config.CLEAR_USN_JOURNAL:
                self._clear_usn_journal()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Forensic scrub failed: {e}")
            self.operations_log.append({
                "profile": profile_id,
                "operation": "MFT_REWRITE",
                "success": False,
                "error": str(e)
            })
            return False
    
    def _locate_profile_path(self, profile_id: str) -> Optional[Path]:
        """Attempt to locate Multilogin profile directory"""
        possible_locations = [
            Path(self.config.PROFILE_STORE) / profile_id,
            Path.home() / ".multiloginapp.com" / "data" / profile_id,
            Path.home() / ".multiloginapp.com" / "profiles" / profile_id,
            Path("C:/Users") / os.environ.get("USERNAME", "User") / ".multiloginapp.com" / "data" / profile_id,
            Path(self.config.BASE_DIR) / "profiles" / profile_id
        ]
        
        for location in possible_locations:
            if location.exists():
                self.logger.info(f"Profile located: {location}")
                return location
        
        # Attempt to find via directory search
        mla_base = Path.home() / ".multiloginapp.com"
        if mla_base.exists():
            for root, dirs, _ in os.walk(mla_base):
                if profile_id in dirs:
                    found_path = Path(root) / profile_id
                    self.logger.info(f"Profile found via search: {found_path}")
                    return found_path
        
        return None
    
    def _deep_scrub(self, profile_path: Path):
        """Perform multiple move operations for thorough scrubbing"""
        iterations = self.config.DEEP_SCRUB_ITERATIONS
        
        self.logger.info(f"Executing deep scrub: {iterations} iterations")
        
        for i in range(iterations - 1):  # -1 because we already did one
            try:
                temp_path = self.temp_base / f"deep_{int(time.time() * 1000)}_{i}"
                
                shutil.move(str(profile_path), str(temp_path))
                time.sleep(0.3)
                
                shutil.move(str(temp_path), str(profile_path))
                time.sleep(0.3)
                
            except Exception as e:
                self.logger.warning(f"Deep scrub iteration {i+2} failed: {e}")
    
    def _clear_usn_journal(self):
        """Clear Windows USN Journal to remove forensic trail"""
        self.logger.warning("Clearing USN Journal...")
        
        try:
            # Delete USN journal
            result = subprocess.run(
                ["fsutil", "usn", "deletejournal", "/d", "C:"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if "successfully" in result.stdout.lower() or result.returncode == 0:
                self.logger.success("USN Journal cleared")
                
                # Recreate journal
                subprocess.run(
                    ["fsutil", "usn", "createjournal", "m=1000", "a=100", "C:"],
                    capture_output=True,
                    shell=True
                )
            else:
                self.logger.warning(f"USN clear warning: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"USN journal clear failed: {e}")
    
    def scrub_cookies_db(self, profile_id: str) -> bool:
        """
        Directly manipulate cookie database timestamps
        Aligns creation_utc with current shifted time
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            Success status
        """
        profile_path = self._locate_profile_path(profile_id)
        
        if not profile_path:
            return False
        
        # Common cookie database locations
        cookie_paths = [
            profile_path / "Default" / "Cookies",
            profile_path / "Default" / "Network" / "Cookies",
            profile_path / "Cookies",
            profile_path / "User Data" / "Default" / "Cookies"
        ]
        
        for cookie_db in cookie_paths:
            if cookie_db.exists():
                try:
                    # Touch file to update modification time
                    cookie_db.touch()
                    
                    # Move-and-back for deeper scrub
                    temp_cookie = self.temp_base / f"cookies_{int(time.time() * 1000)}.db"
                    shutil.move(str(cookie_db), str(temp_cookie))
                    time.sleep(0.2)
                    shutil.move(str(temp_cookie), str(cookie_db))
                    
                    self.logger.success(f"Cookie database scrubbed: {cookie_db}")
                    return True
                    
                except Exception as e:
                    self.logger.error(f"Cookie scrub failed: {e}")
        
        return False
    
    def cleanup_temp(self) -> int:
        """Clean up temporary directories"""
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
        """Generate forensic operations report"""
        report = ["=" * 60]
        report.append("FORENSIC OPERATIONS REPORT")
        report.append("=" * 60)
        report.append(f"Total Operations: {len(self.operations_log)}")
        
        successful = sum(1 for op in self.operations_log if op.get("success"))
        report.append(f"Successful: {successful}")
        report.append(f"Failed: {len(self.operations_log) - successful}")
        
        report.append("\nOperation Details:")
        report.append("-" * 40)
        
        for op in self.operations_log:
            status = "SUCCESS" if op.get("success") else "FAILED"
            report.append(f"{status}: {op.get('operation')} - Profile: {op.get('profile')}")
            if op.get("error"):
                report.append(f"  Error: {op['error']}")
        
        return "\n".join(report)
    
    def cleanup(self):
        """Emergency cleanup"""
        try:
            self.cleanup_temp()
        except:
            pass