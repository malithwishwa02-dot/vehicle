"""
CHRONOS-MULTILOGIN Main Orchestrator
Implements Method 4: Time-Shifted Injection journey workflow
"""

import sys
import argparse
import logging
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.chronos import ChronosTimeManager
from core.mla_handler import MultiloginController
from core.forensics import ForensicScrubber
from config.settings import CONFIG
from utils.logger import setup_logger
from utils.validators import SystemValidator


class ChronosJourney:
    """
    Orchestrates the complete time-shifted profile aging journey
    Implements the temporal manipulation workflow for synthetic patina generation
    """
    
    def __init__(self, profile_id: str, profile_path: str = None):
        """
        Initialize journey orchestrator
        
        Args:
            profile_id: Multilogin profile identifier
            profile_path: Optional path to profile directory
        """
        self.profile_id = profile_id
        self.profile_path = profile_path or self._detect_profile_path(profile_id)
        
        # Initialize components
        self.chronos = ChronosTimeManager()
        self.mla = MultiloginController()
        self.forensics = ForensicScrubber()
        
        # Setup logging
        self.logger = setup_logger(
            name="CHRONOS_JOURNEY",
            log_dir=CONFIG["paths"]["logs"],
            level=CONFIG["logging"]["level"]
        )
        
        self.journey_log: List[Dict[str, Any]] = []
    
    def _detect_profile_path(self, profile_id: str) -> str:
        """
        Attempt to detect Multilogin profile path
        Default locations for MLA profiles
        """
        possible_paths = [
            Path.home() / ".multiloginapp.com" / "profiles" / profile_id,
            Path("C:/Users") / Path.home().name / ".multiloginapp.com" / "profiles" / profile_id,
            CONFIG["paths"]["profiles"] / profile_id
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Return default if not found
        return str(CONFIG["paths"]["profiles"] / profile_id)
    
    def execute_genesis_phase(self) -> bool:
        """
        Genesis Phase: Initial profile creation at T-90 days
        Seeds foundational cookies and browsing patterns
        """
        self.logger.info("=" * 60)
        self.logger.info("GENESIS PHASE: T-90 Days")
        self.logger.info("=" * 60)
        
        try:
            # Shift time to 90 days ago
            success, target_time = self.chronos.shift_time(CONFIG["time_shifts"]["genesis"])
            if not success:
                raise RuntimeError("Failed to shift time for genesis phase")
            
            self.logger.info(f"Time shifted to: {target_time}")
            
            # Start profile
            self.mla.start_profile(self.profile_id)
            driver = self.mla.connect_selenium()
            
            # Initial fingerprint test
            self.logger.info("Performing initial fingerprint test...")
            for url in CONFIG["urls"]["fingerprint_test"][:2]:
                self.mla.navigate_to(url, wait_time=random.randint(3, 6))
            
            # Seed organic browsing
            self.logger.info("Seeding organic browsing history...")
            urls_to_visit = random.sample(CONFIG["urls"]["organic_browsing"], 4)
            results = self.mla.generate_browsing_history(urls_to_visit, dwell_time=3)
            
            # Log results
            self.journey_log.append({
                "phase": "genesis",
                "timestamp": target_time.isoformat(),
                "urls_visited": len([r for r in results.values() if r]),
                "success": True
            })
            
            # Stop profile
            self.mla.stop_profile()
            
            # Forensic scrub while time is shifted
            self.logger.info("Performing forensic scrub...")
            self.forensics.scrub_mft(self.profile_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Genesis phase failed: {str(e)}")
            self.journey_log.append({
                "phase": "genesis",
                "error": str(e),
                "success": False
            })
            return False
    
    def execute_aging_phase(self, phase_name: str, days_offset: int, urls_category: str) -> bool:
        """
        Execute an aging phase at specified temporal offset
        
        Args:
            phase_name: Name of the phase
            days_offset: Days to shift from present
            urls_category: URL category to browse
            
        Returns:
            Success status
        """
        self.logger.info("=" * 60)
        self.logger.info(f"{phase_name.upper()}: T{days_offset} Days")
        self.logger.info("=" * 60)
        
        try:
            # Shift time
            success, target_time = self.chronos.shift_time(days_offset - self._get_current_offset())
            if not success:
                raise RuntimeError(f"Failed to shift time for {phase_name}")
            
            self.logger.info(f"Time shifted to: {target_time}")
            
            # Start profile
            self.mla.start_profile(self.profile_id)
            driver = self.mla.connect_selenium()
            
            # Generate browsing activity
            urls = CONFIG["urls"].get(urls_category, CONFIG["urls"]["organic_browsing"])
            urls_to_visit = random.sample(urls, min(5, len(urls)))
            
            self.logger.info(f"Generating {urls_category} browsing history...")
            results = self.mla.generate_browsing_history(
                urls_to_visit, 
                dwell_time=random.randint(2, 5)
            )
            
            # Random scrolling and interactions
            for _ in range(3):
                driver.execute_script(f"window.scrollTo(0, {random.randint(100, 800)});")
                time.sleep(random.uniform(0.5, 2))
            
            # Log phase results
            self.journey_log.append({
                "phase": phase_name,
                "timestamp": target_time.isoformat(),
                "urls_visited": len([r for r in results.values() if r]),
                "success": True
            })
            
            # Stop profile
            self.mla.stop_profile()
            
            # Forensic scrub
            self.forensics.scrub_mft(self.profile_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"{phase_name} failed: {str(e)}")
            self.journey_log.append({
                "phase": phase_name,
                "error": str(e),
                "success": False
            })
            return False
    
    def _get_current_offset(self) -> int:
        """Calculate current temporal offset from journey log"""
        if not self.journey_log:
            return 0
        
        # Sum all successful time shifts
        total_offset = 0
        for entry in self.journey_log:
            if entry.get("success") and "phase" in entry:
                phase_key = entry["phase"].replace(" ", "_").lower()
                if phase_key in CONFIG["time_shifts"]:
                    total_offset = CONFIG["time_shifts"][phase_key]
        
        return total_offset
    
    def execute_complete_journey(self) -> bool:
        """
        Execute the complete time-shifted injection journey
        Implements all phases of synthetic profile aging
        """
        self.logger.info("INITIATING CHRONOS JOURNEY")
        self.logger.info(f"Profile ID: {self.profile_id}")
        self.logger.info(f"Profile Path: {self.profile_path}")
        
        try:
            # Step 1: Block NTP
            self.logger.info("Blocking NTP synchronization...")
            if not self.chronos.block_ntp():
                raise RuntimeError("Failed to block NTP")
            
            # Step 2: Genesis Phase (T-90)
            if not self.execute_genesis_phase():
                raise RuntimeError("Genesis phase failed")
            
            time.sleep(2)
            
            # Step 3: Phase 1 (T-45)
            if not self.execute_aging_phase(
                "phase_1", 
                CONFIG["time_shifts"]["phase_1"],
                "news_sites"
            ):
                self.logger.warning("Phase 1 failed, continuing...")
            
            time.sleep(2)
            
            # Step 4: Phase 2 (T-21)
            if not self.execute_aging_phase(
                "phase_2",
                CONFIG["time_shifts"]["phase_2"],
                "social_media"
            ):
                self.logger.warning("Phase 2 failed, continuing...")
            
            time.sleep(2)
            
            # Step 5: Phase 3 (T-7)
            if not self.execute_aging_phase(
                "phase_3",
                CONFIG["time_shifts"]["phase_3"],
                "organic_browsing"
            ):
                self.logger.warning("Phase 3 failed, continuing...")
            
            # Step 6: Deep forensic scrub
            self.logger.info("Performing deep forensic scrub...")
            self.forensics.deep_scrub(self.profile_path, iterations=2)
            
            # Step 7: Clear USN Journal
            if CONFIG["forensics"]["clear_usn_journal"]:
                self.logger.info("Clearing USN journal...")
                self.forensics.clear_usn_journal()
            
            # Step 8: Restore time and cleanup
            self.logger.info("Restoring original time...")
            self.chronos.restore_original_time()
            
            # Step 9: Unblock NTP and resync
            self.logger.info("Unblocking NTP and resyncing...")
            self.chronos.unblock_ntp()
            self.chronos.resync_time()
            
            # Generate report
            self._generate_journey_report()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Journey failed: {str(e)}")
            return False
            
        finally:
            # Ensure cleanup happens
            self.chronos.cleanup()
            self.mla.cleanup()
            self.forensics.cleanup_temp()
    
    def _generate_journey_report(self):
        """Generate and save journey report"""
        report = "=" * 60 + "\n"
        report += "CHRONOS JOURNEY REPORT\n"
        report += "=" * 60 + "\n\n"
        report += f"Profile ID: {self.profile_id}\n"
        report += f"Execution Time: {datetime.now()}\n\n"
        
        report += "Journey Phases:\n"
        report += "-" * 40 + "\n"
        
        for entry in self.journey_log:
            phase = entry.get("phase", "unknown")
            success = "SUCCESS" if entry.get("success") else "FAILED"
            report += f"{phase}: {success}\n"
            
            if entry.get("urls_visited"):
                report += f"  URLs visited: {entry['urls_visited']}\n"
            if entry.get("error"):
                report += f"  Error: {entry['error']}\n"
        
        report += "\n" + self.forensics.generate_report()
        
        # Save report
        report_path = CONFIG["paths"]["logs"] / f"journey_{self.profile_id}_{int(time.time())}.txt"
        report_path.write_text(report)
        
        self.logger.info(f"Journey report saved: {report_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CHRONOS-MULTILOGIN - Method 4 Time-Shifted Injection"
    )
    
    parser.add_argument(
        "--profile-id",
        required=True,
        help="Multilogin profile ID"
    )
    
    parser.add_argument(
        "--profile-path",
        help="Optional: Path to profile directory"
    )
    
    parser.add_argument(
        "--journey",
        choices=["standard", "genesis-only", "validate-only"],
        default="standard",
        help="Journey type to execute"
    )
    
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip system validation checks"
    )
    
    args = parser.parse_args()
    
    # System validation
    if not args.skip_validation:
        print("Performing system validation...")
        validator = SystemValidator()
        results = validator.validate_all()
        validator.print_validation_report(results)
        
        if not results["all_valid"]:
            print("\nSystem validation failed. Use --skip-validation to bypass.")
            sys.exit(1)
    
    # Execute based on journey type
    if args.journey == "validate-only":
        print("Validation complete.")
        sys.exit(0)
    
    # Initialize journey
    journey = ChronosJourney(
        profile_id=args.profile_id,
        profile_path=args.profile_path
    )
    
    # Execute journey
    if args.journey == "genesis-only":
        success = journey.execute_genesis_phase()
    else:
        success = journey.execute_complete_journey()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()