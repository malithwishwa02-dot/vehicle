"""
NTFS Forensic Scrubber - MFT $FN Attribute Manipulation
Implements Move-and-Back logic to force MFT rewrite during time shift
"""

import os
import shutil
import logging
import tempfile
import time
from pathlib import Path
from typing import Optional, Tuple, List
import subprocess

logger = logging.getLogger(__name__)


class ForensicScrubber:
    """
    Forensic metadata scrubber for NTFS filesystem
    Manipulates $FN (FileName) attributes via forced MFT rewrites
    """
    
    def __init__(self):
        """Initialize forensic scrubber with temp directory management"""
        self.temp_base = Path(tempfile.gettempdir()) / "CHRONOS_TEMP"
        self.operations_log: List[Tuple[str, str, bool]] = []
        
        # Ensure temp directory exists
        self.temp_base.mkdir(exist_ok=True)
    
    def scrub_mft(self, profile_path: str) -> bool:
        """
        Scrub MFT $FN attributes using Move-and-Back technique
        Must be executed while system time is backdated
        
        Args:
            profile_path: Full path to Multilogin profile directory
            
        Returns:
            Success status
        """
        profile_path = Path(profile_path)
        
        if not profile_path.exists():
            logger.error(f"Profile path does not exist: {profile_path}")
            return False
        
        try:
            # Generate unique temp path (cross filesystem boundary)
            temp_path = self.temp_base / f"profile_{int(time.time() * 1000)}"
            
            logger.info(f"Starting MFT scrub for: {profile_path}")
            logger.info(f"Temp relocation path: {temp_path}")
            
            # Step 1: Move to temp location (forces MFT rewrite)
            self._move_directory(profile_path, temp_path)
            
            # Brief pause to ensure filesystem commits
            time.sleep(0.5)
            
            # Step 2: Move back to original location
            self._move_directory(temp_path, profile_path)
            
            # Log successful operation
            self.operations_log.append((str(profile_path), str(temp_path), True))
            
            logger.info("MFT scrub completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"MFT scrub failed: {str(e)}")
            self.operations_log.append((str(profile_path), "", False))
            return False
    
    def _move_directory(self, source: Path, destination: Path) -> None:
        """
        Move directory with NTFS attribute preservation disabled
        Forces new MFT entry creation
        
        Args:
            source: Source directory path
            destination: Destination directory path
        """
        # Use shutil.move for cross-filesystem moves
        # This forces a copy+delete operation which rewrites MFT
        shutil.move(str(source), str(destination))
        logger.debug(f"Moved: {source} -> {destination}")
    
    def deep_scrub(self, profile_path: str, iterations: int = 2) -> bool:
        """
        Perform multiple move operations for thorough MFT scrubbing
        
        Args:
            profile_path: Profile directory to scrub
            iterations: Number of move-and-back cycles
            
        Returns:
            Success status
        """
        profile_path = Path(profile_path)
        
        if not profile_path.exists():
            logger.error(f"Profile path does not exist: {profile_path}")
            return False
        
        try:
            for i in range(iterations):
                logger.info(f"Deep scrub iteration {i+1}/{iterations}")
                
                # Create unique temp path for each iteration
                temp_path = self.temp_base / f"deep_{int(time.time() * 1000)}_{i}"
                
                # Move to temp
                self._move_directory(profile_path, temp_path)
                time.sleep(0.3)
                
                # Move back
                self._move_directory(temp_path, profile_path)
                time.sleep(0.3)
            
            logger.info(f"Deep scrub completed: {iterations} iterations")
            return True
            
        except Exception as e:
            logger.error(f"Deep scrub failed: {str(e)}")
            return False
    
    def scrub_file_timestamps(self, file_path: str) -> bool:
        """
        Scrub individual file timestamps using copy-and-replace
        
        Args:
            file_path: Path to file requiring timestamp scrubbing
            
        Returns:
            Success status
        """
        file_path = Path(file_path)
        
        if not file_path.is_file():
            logger.error(f"Not a valid file: {file_path}")
            return False
        
        try:
            # Create temp copy
            temp_file = self.temp_base / f"file_{int(time.time() * 1000)}.tmp"
            
            # Copy to temp (creates new MFT entry with current backdated time)
            shutil.copy2(str(file_path), str(temp_file))
            
            # Delete original
            file_path.unlink()
            
            # Move temp back to original location
            shutil.move(str(temp_file), str(file_path))
            
            logger.info(f"File timestamp scrubbed: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File scrub failed: {str(e)}")
            return False
    
    def compact_volume(self, drive_letter: str = "C:") -> bool:
        """
        Run Windows compact command to force MFT optimization
        Requires Administrator privileges
        
        Args:
            drive_letter: Target volume (default C:)
            
        Returns:
            Success status
        """
        try:
            # Run compact command to optimize MFT
            cmd = f"compact /c /s:{drive_letter}\\ /i"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Volume compaction initiated on {drive_letter}")
                return True
            else:
                logger.warning(f"Compact command warning: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.warning("Volume compaction timeout - may still be running")
            return True
            
        except Exception as e:
            logger.error(f"Volume compaction error: {str(e)}")
            return False
    
    def clear_usn_journal(self, drive_letter: str = "C:") -> bool:
        """
        Clear USN (Update Sequence Number) Journal
        Removes forensic trail of file system changes
        Requires Administrator privileges
        
        Args:
            drive_letter: Target volume (default C:)
            
        Returns:
            Success status
        """
        try:
            # Delete USN journal
            cmd_delete = f"fsutil usn deletejournal /d {drive_letter}"
            
            result = subprocess.run(
                cmd_delete,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if "successfully" in result.stdout.lower():
                logger.info(f"USN journal cleared on {drive_letter}")
                
                # Recreate journal for continued operation
                cmd_create = f"fsutil usn createjournal m=1000 a=100 {drive_letter}"
                subprocess.run(cmd_create, shell=True, capture_output=True)
                
                return True
            else:
                logger.warning(f"USN journal clear warning: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"USN journal clear error: {str(e)}")
            return False
    
    def get_mft_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get MFT information for a file using fsutil
        
        Args:
            file_path: Path to analyze
            
        Returns:
            MFT metadata dictionary or None
        """
        try:
            # Query file info using fsutil
            cmd = f'fsutil file queryfileid "{file_path}"'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse output
                info = {}
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                
                return info
            else:
                logger.error(f"Failed to query MFT info: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"MFT query error: {str(e)}")
            return None
    
    def cleanup_temp(self) -> int:
        """
        Clean up temporary directories created during operations
        
        Returns:
            Number of temp directories removed
        """
        cleaned = 0
        
        try:
            if self.temp_base.exists():
                for temp_dir in self.temp_base.iterdir():
                    try:
                        if temp_dir.is_dir():
                            shutil.rmtree(temp_dir)
                            cleaned += 1
                    except Exception as e:
                        logger.warning(f"Failed to remove temp dir {temp_dir}: {str(e)}")
            
            logger.info(f"Cleaned {cleaned} temporary directories")
            return cleaned
            
        except Exception as e:
            logger.error(f"Temp cleanup error: {str(e)}")
            return cleaned
    
    def generate_report(self) -> str:
        """
        Generate forensic operations report
        
        Returns:
            Formatted report string
        """
        report = "=" * 60 + "\n"
        report += "FORENSIC SCRUBBER OPERATIONS REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += f"Total Operations: {len(self.operations_log)}\n"
        
        successful = sum(1 for _, _, success in self.operations_log if success)
        report += f"Successful: {successful}\n"
        report += f"Failed: {len(self.operations_log) - successful}\n\n"
        
        report += "Operation Details:\n"
        report += "-" * 40 + "\n"
        
        for source, temp, success in self.operations_log:
            status = "SUCCESS" if success else "FAILED"
            report += f"{status}: {source}\n"
            if temp:
                report += f"  Temp: {temp}\n"
        
        return report