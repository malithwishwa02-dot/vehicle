"""
CHRONOS-MULTILOGIN v2.0 | Method 4: Time-Shifted Injection
Main orchestrator for synthetic profile aging operations
Authority: Dva.12-CARD | Status: ZERO_REFUSAL
"""

import sys
import argparse
import time
import random
import signal
from datetime import datetime
from typing import List, Dict, Any

# Core imports
from core.chronos import Chronos
from core.mla_handler import MLAHandler
from core.forensics import ForensicScrubber
from config.settings import Config
from utils.validators import validate_environment, is_admin
from utils.logger import get_logger

class ChronosOrchestrator:
    """
    Primary orchestrator for time-shifted aging operations
    Implements complete Method 4 protocol with safety mechanisms
    """
    
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.logger = get_logger()
        
        # Initialize components
        self.chronos = Chronos()
        self.forensics = ForensicScrubber()
        self.mla = None  # Initialized per phase
        
        # Operation tracking
        self.phases_completed = []
        self.start_time = datetime.now()
        
        # Safety handler
        signal.signal(signal.SIGINT, self._emergency_cleanup)
    
    def _emergency_cleanup(self, signum, frame):
        """Emergency cleanup on interrupt"""
        print("\n\n[!] EMERGENCY ABORT DETECTED")
        self.logger.critical("Emergency cleanup initiated")
        
        try:
            if self.mla:
                self.mla.cleanup()
            self.chronos.cleanup()
            self.forensics.cleanup()
        except:
            pass
        
        print("[*] Cleanup complete. Exiting.")
        sys.exit(1)
    
    def execute_phase(self, days_ago: int, phase_name: str, deep_seed: bool = False) -> bool:
        """
        Execute a single aging phase
        
        Args:
            days_ago: Temporal offset in days
            phase_name: Name of the phase for logging
            deep_seed: Use extended trust anchors
            
        Returns:
            Success status
        """
        self.logger.info("="*60)
        self.logger.info(f"PHASE: {phase_name} | T-{days_ago} DAYS")
        self.logger.info("="*60)
        
        try:
            # 1. Time jump
            if not self.chronos.time_jump(days_ago):
                raise RuntimeError("Time jump failed")
            
            # 2. Start browser profile
            self.mla = MLAHandler(self.profile_id)
            if not self.mla.start_profile():
                raise RuntimeError("Failed to start profile")
            
            # 3. Seed cookies
            self.mla.seed_cookies(deep_seed=deep_seed)
            
            # 4. Execute journey for natural history
            journey_types = ["standard", "shopping", "social", "news"]
            selected_journey = random.choice(journey_types)
            self.mla.execute_journey(selected_journey)
            
            # 5. Stop profile
            self.mla.stop_profile()
            self.mla = None
            
            # 6. Forensic scrub
            self.forensics.scrub_timestamps(self.profile_id)
            
            # 7. Additional cookie database scrub
            self.forensics.scrub_cookies_db(self.profile_id)
            
            # Track completion
            self.phases_completed.append({
                "phase": phase_name,
                "days_ago": days_ago,
                "timestamp": self.chronos.get_current_time(),
                "success": True
            })
            
            self.logger.success(f"Phase {phase_name} completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Phase {phase_name} failed: {e}")
            self.phases_completed.append({
                "phase": phase_name,
                "days_ago": days_ago,
                "error": str(e),
                "success": False
            })
            return False
    
    def execute_journey(self) -> bool:
        """
        Execute complete time-shifted aging journey
        
        Returns:
            Overall success status
        """
        print("""
        ╔══════════════════════════════════════════════════════════╗
        ║   CHRONOS-MULTILOGIN v2.0 | METHOD 4 PROTOCOL           ║
        ║   AUTHORITY: Dva.12-CARD | STATUS: ZERO_REFUSAL         ║
        ╚══════════════════════════════════════════════════════════╝
        """)
        
        self.logger.critical("INITIATING TEMPORAL MANIPULATION SEQUENCE")
        
        try:
            # Kill NTP service
            self.chronos.kill_ntp()
            
            # Wait for system stabilization
            time.sleep(2)
            
            # Execute aging phases
            phases = [
                (90, "GENESIS", True),      # Deep seed at genesis
                (45, "ENTROPY", False),     # Standard seeding
                (21, "MATURATION", False),  # Standard seeding
                (7, "WARMUP", False),       # Standard seeding
                (1, "FINAL", True)          # Deep seed before completion
            ]
            
            for days_ago, phase_name, deep_seed in phases:
                if not self.execute_phase(days_ago, phase_name, deep_seed):
                    self.logger.warning(f"Phase {phase_name} failed, continuing...")
                
                # Inter-phase delay
                time.sleep(random.uniform(2, 4))
            
            # Final deep forensic scrub
            self.logger.info("Executing final forensic protocol...")
            for _ in range(Config.DEEP_SCRUB_ITERATIONS):
                self.forensics.scrub_timestamps(self.profile_id)
                time.sleep(0.5)
            
            # Clear USN journal if configured
            if Config.CLEAR_USN_JOURNAL:
                self.forensics._clear_usn_journal()
            
            self.logger.success("AGING SEQUENCE COMPLETE")
            return True
            
        except Exception as e:
            self.logger.error(f"Journey failed: {e}")
            return False
            
        finally:
            # Restoration sequence
            self.logger.info("Initiating restoration sequence...")
            
            # Restore original time
            self.chronos.restore_original_time()
            
            # Restore NTP
            self.chronos.restore_ntp()
            
            # Cleanup
            self.forensics.cleanup()
            
            # Generate report
            self._generate_report()
    
    def _generate_report(self):
        """Generate and display operation report"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "="*60)
        print("OPERATION REPORT")
        print("="*60)
        print(f"Profile ID: {self.profile_id}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Phases Completed: {len([p for p in self.phases_completed if p['success']])}/{len(self.phases_completed)}")
        
        print("\nPhase Details:")
        for phase in self.phases_completed:
            status = "✓" if phase['success'] else "✗"
            print(f"  {status} {phase['phase']}: T-{phase.get('days_ago', '?')} days")
            if phase.get('error'):
                print(f"     Error: {phase['error']}")
        
        # Forensic report
        print("\n" + self.forensics.generate_report())
        print("="*60)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CHRONOS-MULTILOGIN v2.0 | Method 4: Time-Shifted Injection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --profile-id YOUR_PROFILE_UUID
  python main.py --profile-id YOUR_PROFILE_UUID --validate-only
  python main.py --profile-id YOUR_PROFILE_UUID --skip-validation
        """
    )
    
    parser.add_argument(
        '--profile-id',
        required=True,
        help='Multilogin Profile UUID'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only run validation checks'
    )
    
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip system validation (dangerous)'
    )
    
    args = parser.parse_args()
    
    # System validation
    if not args.skip_validation:
        validation = validate_environment()
        
        if args.validate_only:
            sys.exit(0 if validation["all_valid"] else 1)
        
        if not validation["all_valid"]:
            print("\n[!] System validation failed. Use --skip-validation to override.")
            sys.exit(1)
    
    # Check admin privileges explicitly
    if not is_admin():
        print("\n[!] ERROR: Administrator privileges required.")
        print("[!] Right-click and select 'Run as Administrator'")
        sys.exit(1)
    
    # Execute journey
    orchestrator = ChronosOrchestrator(args.profile_id)
    success = orchestrator.execute_journey()
    
    # Exit status
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()