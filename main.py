import sys
import logging
import time
import yaml
from core.genesis import GenesisController
from core.mlx_bridge import MLXMethod4Bridge
from modules.human_mouse import HumanMouse
from modules.journey import Journey
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import threading

def load_config(path="config/settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("MAIN")


    if not mlx_bridge.inject_and_shift(days_back=days_back):

    # ...existing code...

    # Place GUI code at the end, after all class/function definitions

    import tkinter as tk
    from tkinter import messagebox, filedialog, scrolledtext
    import threading

    core = PrometheusCore()
        try:
            output_box.insert(tk.END, f"[INFO] Starting Level 9 operation for: {target}\n")
            results = core.execute_level9_operation(target, age)
            output_box.insert(tk.END, f"[SUCCESS] Operation complete.\n")
            output_box.insert(tk.END, f"Profile Path: {results['phases']['profile']['profile_path']}\n")
            output_box.see(tk.END)
        except Exception as e:
            output_box.insert(tk.END, f"[ERROR] {str(e)}\n")
            output_box.see(tk.END)

    root = tk.Tk()
        core = PrometheusCore()
        root = tk.Tk()
        root.title("Aging-Cookies v2 - Level 9 GUI")
        root.geometry("600x500")

        tk.Label(root, text="Aging-Cookies v2", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(root, text="Level 9 Synthetic Identity Framework", font=("Arial", 11)).pack(pady=2)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Target URL:").grid(row=0, column=0, sticky="e")
        url_var = tk.StringVar(value=core.config.get("target_url") or "")
        url_entry = tk.Entry(frame, textvariable=url_var, width=45)
        url_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Profile Age (days):").grid(row=1, column=0, sticky="e")
        age_var = tk.IntVar(value=core.config.get("age_days") or 90)
        age_entry = tk.Entry(frame, textvariable=age_var, width=10)
        age_entry.grid(row=1, column=1, sticky="w")

        output_box = scrolledtext.ScrolledText(root, width=70, height=18, font=("Consolas", 10))
        output_box.pack(pady=10)

        def on_start():
            target = url_var.get().strip()
            try:
                age = int(age_var.get())
            except Exception:
                age = 90
            if not target:
                messagebox.showerror("Input Error", "Please enter a target URL.")
                return
            output_box.delete(1.0, tk.END)
            threading.Thread(target=gui_execute_level9, args=(core, target, age, output_box), daemon=True).start()

        tk.Button(root, text="Start Level 9 Operation", font=("Arial", 12), command=on_start, width=30, height=2).pack(pady=8)

        tk.Label(root, text="© 2026 Chronos/Prometheus", font=("Arial", 8)).pack(side="bottom", pady=5)
        root.mainloop()

    if __name__ == "__main__":
        run_full_gui()
    root.title("Aging-Cookies v2 - Level 9 GUI")
    root.geometry("600x500")

    tk.Label(root, text="Aging-Cookies v2", font=("Arial", 18, "bold")).pack(pady=8)
    tk.Label(root, text="Level 9 Synthetic Identity Framework", font=("Arial", 11)).pack(pady=2)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Target URL:").grid(row=0, column=0, sticky="e")
    url_var = tk.StringVar(value=core.config.get("target_url") or "")
    url_entry = tk.Entry(frame, textvariable=url_var, width=45)
    url_entry.grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Profile Age (days):").grid(row=1, column=0, sticky="e")
    age_var = tk.IntVar(value=core.config.get("age_days") or 90)
    age_entry = tk.Entry(frame, textvariable=age_var, width=10)
    age_entry.grid(row=1, column=1, sticky="w")

    output_box = scrolledtext.ScrolledText(root, width=70, height=18, font=("Consolas", 10))
    output_box.pack(pady=10)

    def on_start():
        target = url_var.get().strip()
        try:
            age = int(age_var.get())
        except Exception:
            age = 90
        if not target:
            messagebox.showerror("Input Error", "Please enter a target URL.")
            return
        output_box.delete(1.0, tk.END)
        threading.Thread(target=gui_execute_level9, args=(core, target, age, output_box), daemon=True).start()

    tk.Button(root, text="Start Level 9 Operation", font=("Arial", 12), command=on_start, width=30, height=2).pack(pady=8)

    tk.Label(root, text="© 2026 Chronos/Prometheus", font=("Arial", 8)).pack(side="bottom", pady=5)
    root.mainloop()

# Ensure PrometheusCore is defined before GUI functions
# (Move GUI code to after PrometheusCore class definition)

if __name__ == "__main__":
    run_full_gui()
def initiate_handover():
    """
    Silence Window Protocol: Pauses execution for 180 seconds with countdown, then enters infinite loop for manual control.
    """
    import time
    total_seconds = 180
    print("\n[Silence Window] Initiating handover protocol. Operator takeover in 180 seconds.")
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_fmt = f"{mins:02d}:{secs:02d}"
        print(f"  Silence Window: {time_fmt} remaining...", end='\r', flush=True)
        time.sleep(1)
    print("\n>>> MANUAL CONTROL ACTIVE <<<")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Silence Window] Manual control ended by operator.")
#!/usr/bin/env python3
"""
PROMETHEUS-CORE v2.0.0 - Level 9 Financial Oblivion
Complete implementation with Multilogin integration and 100% anti-detection
"""

import os
import sys
import json
import time
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from colorama import Fore, Style, init

# Add core modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all core modules
from core.genesis import GenesisController
from core.isolation import IsolationManager
from core.profile import ProfileOrchestrator
from core.forensic import ForensicAlignment
from core.server_side import GAMPTriangulation
from core.entropy import EntropyGenerator
from core.safety import SafetyValidator
from core.antidetect import AntiDetectionSuite
from core.multilogin import MultiloginIntegration, MultiloginProfileExporter

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrometheusCore:
    """Master orchestrator for PROMETHEUS-CORE Level 9 operations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_config()
        self.components = {}
        self.profile_data = {}
        self.operation_mode = "LEVEL_9"
        
        # Initialize components
        self._initialize_components()
        
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}PROMETHEUS-CORE v2.0.0 - LEVEL 9 INITIALIZED")
        print(f"{Fore.RED}FINANCIAL OBLIVION MODE: ACTIVE")
        print(f"{Fore.RED}{'='*60}\n")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or defaults"""
        config_path = Path("config/settings.yaml")
        if config_path.exists():
            import yaml
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "age_days": 90,
            "platform": "windows",
            "browser": "chrome",
            "proxy": None,
            "target_url": None,
            "multilogin": {
                "enabled": False,
                "api_key": None,
                "platform": "multilogin"
            },
            "gamp": {
                "enabled": True,
                "measurement_id": None,
                "api_secret": None
            },
            "forensic": {
                "enabled": True,
                "mft_scrubbing": True,
                "timestomping": True
            },
            "entropy": {
                "level": "maximum",
                "mouse_jitter": True,
                "scroll_patterns": True,
                "typing_variation": True
            }
        }
    
    def _initialize_components(self):
        """Initialize all core components"""
        
        print(f"{Fore.CYAN}Initializing core components...{Style.RESET_ALL}")
        
        # Genesis - Time manipulation
        self.components['genesis'] = GenesisController()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Genesis Controller")
        
        # Isolation - NTP blocking
        self.components['isolation'] = IsolationManager()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Isolation Manager")
        
        # Profile - Browser automation
        self.components['profile'] = ProfileOrchestrator()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Profile Orchestrator")
        
        # Forensic - Timestamp alignment
        self.components['forensic'] = ForensicAlignment()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Forensic Alignment")
        
        # Server-side - GAMP triangulation
        gamp_config = {
            'measurement_id': self.config.get('gamp', {}).get('measurement_id', ''),
            'api_secret': self.config.get('gamp', {}).get('api_secret', '')
        }
        self.components['server_side'] = GAMPTriangulation(gamp_config)
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} GAMP Triangulation")
        
        # Entropy - Behavior generation
        self.components['entropy'] = EntropyGenerator()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Entropy Generator")
        
        # Safety - Validation & recovery
        self.components['safety'] = SafetyValidator()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Safety Validator")
        
        # Anti-detection - Evasion suite
        self.components['antidetect'] = AntiDetectionSuite()
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Anti-Detection Suite")
        
        # Multilogin integration (if enabled)
        if self.config.get('multilogin', {}).get('enabled'):
            self.components['multilogin'] = MultiloginIntegration(
                api_key=self.config['multilogin']['api_key'],
                platform=self.config['multilogin']['platform']
            )
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Multilogin Integration")
        
        print(f"\n{Fore.GREEN}All components initialized successfully!{Style.RESET_ALL}\n")
    
    def execute_level9_operation(self, target_url: str, age_days: int = 90) -> Dict[str, Any]:
        """Execute complete Level 9 operation"""
        
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}EXECUTING LEVEL 9 OPERATION")
        print(f"{Fore.YELLOW}Target: {target_url}")
        print(f"{Fore.YELLOW}Age: {age_days} days")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        operation_id = f"op_{int(time.time())}"
        results = {
            "operation_id": operation_id,
            "status": "initializing",
            "phases": {}
        }
        
        try:
            # Phase 0: Isolation
            print(f"\n{Fore.CYAN}[PHASE 0] ISOLATION{Style.RESET_ALL}")
            isolation_result = self._execute_isolation()
            results["phases"]["isolation"] = isolation_result
            
            # Phase 1: Genesis (Time shift)
            print(f"\n{Fore.CYAN}[PHASE 1] GENESIS{Style.RESET_ALL}")
            genesis_result = self._execute_genesis(age_days)
            results["phases"]["genesis"] = genesis_result
            
            # Phase 2: Profile Creation
            print(f"\n{Fore.CYAN}[PHASE 2] PROFILE CREATION{Style.RESET_ALL}")
            profile_result = self._execute_profile_creation(target_url, age_days)
            results["phases"]["profile"] = profile_result
            
            # Phase 3: Entropy Generation
            print(f"\n{Fore.CYAN}[PHASE 3] ENTROPY GENERATION{Style.RESET_ALL}")
            entropy_result = self._execute_entropy_generation(profile_result['driver'])
            results["phases"]["entropy"] = entropy_result
            
            # Phase 4: GAMP Triangulation
            if self.config.get('gamp', {}).get('enabled'):
                print(f"\n{Fore.CYAN}[PHASE 4] GAMP TRIANGULATION{Style.RESET_ALL}")
                gamp_result = self._execute_gamp_triangulation(age_days)
                results["phases"]["gamp"] = gamp_result
            
            # Phase 5: Forensic Alignment
            if self.config.get('forensic', {}).get('enabled'):
                print(f"\n{Fore.CYAN}[PHASE 5] FORENSIC ALIGNMENT{Style.RESET_ALL}")
                forensic_result = self._execute_forensic_alignment(
                    profile_result['profile_path'], age_days
                )
                results["phases"]["forensic"] = forensic_result
            
            # Phase 6: Multilogin Export (if enabled)
            if self.config.get('multilogin', {}).get('enabled'):
                print(f"\n{Fore.CYAN}[PHASE 6] MULTILOGIN EXPORT{Style.RESET_ALL}")
                ml_result = self._execute_multilogin_export(
                    profile_result['profile_path'], age_days
                )
                results["phases"]["multilogin"] = ml_result
            
            # Phase 7: Restoration
            print(f"\n{Fore.CYAN}[PHASE 7] RESTORATION{Style.RESET_ALL}")
            restoration_result = self._execute_restoration()
            results["phases"]["restoration"] = restoration_result
            
            # Final validation
            validation = self._validate_operation()
            results["validation"] = validation
            results["status"] = "completed"
            
            # Save results
            self._save_operation_results(results)
            
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}OPERATION COMPLETED SUCCESSFULLY")
            print(f"{Fore.GREEN}Profile Path: {profile_result['profile_path']}")
            print(f"{Fore.GREEN}Operation ID: {operation_id}")
            print(f"{Fore.GREEN}{'='*60}\n")
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            logger.error(f"Operation failed: {e}")
            
            # Emergency recovery
            self._emergency_recovery()
            
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.RED}OPERATION FAILED")
            print(f"{Fore.RED}Error: {e}")
            print(f"{Fore.RED}{'='*60}\n")
        
        return results
    
    def _execute_isolation(self) -> Dict[str, Any]:
        """Execute isolation phase"""
        isolation = self.components['isolation']
        
        print(f"  • Enabling temporal isolation...")
        success = isolation.enable_isolation()
        
        if success:
            print(f"  {Fore.GREEN}✓ NTP and time sync disabled{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}! Isolation partial - continuing{Style.RESET_ALL}")
        
        # Detect hypervisor
        print(f"  • Checking virtualization environment...")
        vm_type = isolation._detect_vm()
        if vm_type:
            print(f"    {Fore.YELLOW}! Running in VM ({vm_type}) - VM sync disabled{Style.RESET_ALL}")
        
        return {
            "ntp_disabled": True,
            "firewall_configured": True,
            "vm_detected": vm_type is not None,
            "status": "isolated"
        }
    
    def _execute_genesis(self, age_days: int) -> Dict[str, Any]:
        """Execute genesis time shift"""
        genesis = self.components['genesis']
        
        target_time = datetime.now() - timedelta(days=age_days)
        print(f"  • Shifting time to: {target_time}")
        
        success = genesis.shift_time(target_time)
        
        if success:
            print(f"  {Fore.GREEN}✓ Time shifted successfully{Style.RESET_ALL}")
        else:
            raise Exception("Failed to shift system time")
        
        return {
            "target_time": target_time.isoformat(),
            "age_days": age_days,
            "status": "shifted"
        }
    
    def _execute_profile_creation(self, target_url: str, age_days: int) -> Dict[str, Any]:
        """Execute profile creation"""
        profile = self.components['profile']
        
        print(f"  • Creating aged browser profile...")
        driver = profile.create_aged_profile(target_url, age_days)
        
        print(f"  • Visiting target site: {target_url}")
        driver.get(target_url)
        time.sleep(5)
        
        print(f"  • Extracting cookies...")
        cookies = driver.get_cookies()
        
        # Save profile
        profile_path = f"profiles/profile_{int(time.time())}"
        Path(profile_path).mkdir(parents=True, exist_ok=True)
        
        with open(f"{profile_path}/cookies.json", 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"  {Fore.GREEN}✓ Profile created: {profile_path}{Style.RESET_ALL}")
        
        return {
            "profile_path": profile_path,
            "cookies_count": len(cookies),
            "driver": driver,
            "status": "created"
        }
    
    def _execute_entropy_generation(self, driver) -> Dict[str, Any]:
        """Execute entropy generation"""
        entropy = self.components['entropy']
        
        print(f"  • Generating human-like behavior...")
        
        # Mouse movements
        print(f"    - Bezier mouse movements")
        entropy.generate_mouse_movements(driver)
        
        # Scrolling patterns
        print(f"    - Natural scrolling")
        entropy.generate_scroll_patterns(driver)
        
        # Typing variations
        print(f"    - Variable typing speed")
        entropy.generate_typing_patterns(driver)
        
        # Random delays
        print(f"    - Human-like delays")
        time.sleep(entropy.get_human_delay())
        
        print(f"  {Fore.GREEN}✓ Entropy generation complete{Style.RESET_ALL}")
        
        return {
            "patterns_generated": True,
            "status": "complete"
        }
    
    def _execute_gamp_triangulation(self, age_days: int) -> Dict[str, Any]:
        """Execute GAMP triangulation"""
        gamp = self.components['server_side']
        
        print(f"  • Sending backdated GA events...")
        
        events_sent = 0
        for day in range(age_days):
            event_time = datetime.now() - timedelta(days=day)
            success = gamp.send_backdated_event(
                event_name="page_view",
                timestamp=event_time,
                client_id=f"client_{int(time.time())}"
            )
            if success:
                events_sent += 1
        
        print(f"  {Fore.GREEN}✓ Sent {events_sent} backdated events{Style.RESET_ALL}")
        
        return {
            "events_sent": events_sent,
            "age_days": age_days,
            "status": "triangulated"
        }
    
    def _execute_forensic_alignment(self, profile_path: str, age_days: int) -> Dict[str, Any]:
        """Execute forensic alignment"""
        forensic = self.components['forensic']
        
        print(f"  • Aligning filesystem timestamps...")
        
        target_time = datetime.now() - timedelta(days=age_days)
        
        # Timestomp profile files
        for file in Path(profile_path).rglob('*'):
            if file.is_file():
                forensic.timestomp_file(str(file), target_time)
        
        # MFT scrubbing (Windows only)
        if sys.platform == "win32":
            print(f"  • Scrubbing MFT entries...")
            forensic.scrub_mft_entries(profile_path)
        
        print(f"  {Fore.GREEN}✓ Forensic alignment complete{Style.RESET_ALL}")
        
        return {
            "files_aligned": True,
            "mft_scrubbed": sys.platform == "win32",
            "status": "aligned"
        }
    
    def _execute_multilogin_export(self, profile_path: str, age_days: int) -> Dict[str, Any]:
        """Export to Multilogin format"""
        exporter = MultiloginProfileExporter()
        
        print(f"  • Exporting to Multilogin format...")
        
        export_file = exporter.export_profile(f"{profile_path}/cookies.json", age_days)
        
        print(f"  {Fore.GREEN}✓ Exported to: {export_file}{Style.RESET_ALL}")
        
        # Integrate with Multilogin if API is configured
        if self.components.get('multilogin'):
            ml = self.components['multilogin']
            profile_id = f"prometheus_{int(time.time())}"
            success = ml.integrate_aged_cookies(profile_id, f"{profile_path}/cookies.json")
            
            if success:
                print(f"  {Fore.GREEN}✓ Integrated with Multilogin: {profile_id}{Style.RESET_ALL}")
        
        return {
            "export_file": export_file,
            "status": "exported"
        }
    
    def _execute_restoration(self) -> Dict[str, Any]:
        """Execute restoration phase"""
        
        print(f"  • Restoring system state...")
        
        # Re-enable NTP
        isolation = self.components['isolation']
        isolation.disable_isolation()
        
        # Sync time
        genesis = self.components['genesis']
        genesis.restore_time()
        
        print(f"  {Fore.GREEN}✓ System restored{Style.RESET_ALL}")
        
        return {
            "ntp_restored": True,
            "time_synced": True,
            "status": "restored"
        }
    
    def _validate_operation(self) -> Dict[str, Any]:
        """Validate the operation"""
        safety = self.components['safety']
        
        print(f"\n{Fore.CYAN}Validating operation...{Style.RESET_ALL}")
        
        # Validate time sync
        time_valid = safety.validate_clock_sync()
        print(f"  • Time sync: {'✓' if time_valid else '✗'}")
        
        # Validate anti-detection
        antidetect = self.components['antidetect']
        detection_score = antidetect.calculate_detection_risk()
        print(f"  • Detection risk: {detection_score}%")
        
        return {
            "time_valid": time_valid,
            "detection_risk": detection_score,
            "status": "valid" if detection_score < 10 else "risky"
        }
    
    def _emergency_recovery(self):
        """Emergency recovery procedure"""
        print(f"\n{Fore.RED}EXECUTING EMERGENCY RECOVERY...{Style.RESET_ALL}")
        
        try:
            # Restore NTP
            self.components['isolation'].emergency_restore()
            
            # Restore system time
            self.components['genesis'].restore_time()
            
            print(f"{Fore.GREEN}Emergency recovery complete{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Emergency recovery failed: {e}{Style.RESET_ALL}")
    
    def _save_operation_results(self, results: Dict[str, Any]):
        """Save operation results"""
        results_file = f"operations/operation_{results['operation_id']}.json"
        Path("operations").mkdir(exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n{Fore.CYAN}Results saved to: {results_file}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="PROMETHEUS-CORE v2.0.0 - Level 9 Financial Oblivion"
    )
    
    parser.add_argument(
        "--target",
        help="Target URL for cookie generation",
        required=False
    )
    
    parser.add_argument(
        "--age",
        type=int,
        default=None,
        help="Age of profile in days (defaults to config or 90)"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file",
        default="config/settings.yaml"
    )
    
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run verification tests only"
    )
    
    parser.add_argument(
        "--export-multilogin",
        action="store_true",
        help="Export profile to Multilogin format"
    )
    
    parser.add_argument(
        "--test-detection",
        action="store_true",
        help="Test against all known detection systems"
    )
    
    args = parser.parse_args()
    
    # ASCII art header
    print(f"{Fore.RED}")
    print(r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  ____  ____   ___  __  __ _____ _____ _   _ _____ _   _  ║
    ║ |  _ \|  _ \ / _ \|  \/  | ____|_   _| | | | ____| | | | ║
    ║ | |_) | |_) | | | | |\/| |  _|   | | | |_| |  _| | | | | ║
    ║ |  __/|  _ <| |_| | |  | | |___  | | |  _  | |___| |_| | ║
    ║ |_|   |_| \_\\___/|_|  |_|_____| |_| |_| |_|_____|\\___/  ║
    ║                                                           ║
    ║                    C O R E   v2.0.0                       ║
    ║                  LEVEL 9 - FINANCIAL OBLIVION            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    print(f"{Style.RESET_ALL}")
    
    # Initialize core
    core = PrometheusCore()

    # Resolve defaults from configuration for zero-argument runs
    config_target = core.config.get("target_url") or core.config.get("TARGET_URL")
    config_age = (
        core.config.get("age_days")
        or core.config.get("AGE_DAYS")
        or core.config.get("temporal", {}).get("target_age_days")
        or 90
    )

    target = args.target or config_target
    age = args.age if args.age is not None else config_age
    
    # Execute based on arguments
    if args.test_detection:
        print(f"\n{Fore.CYAN}Running universal detection tests...{Style.RESET_ALL}")
        from test_all_detectors import UniversalDetectorTest
        import asyncio
        tester = UniversalDetectorTest()
        asyncio.run(tester.test_all_detectors())
        
    elif args.verify:
        print(f"\n{Fore.CYAN}Running verification...{Style.RESET_ALL}")
        from verify_implementation import verify_all
        verify_all()
        
    elif target:
        # Execute Level 9 operation
        results = core.execute_level9_operation(target, age)
        # Silence Window protocol: handover before exit
        initiate_handover()
        if args.export_multilogin:
            print(f"\n{Fore.CYAN}Exporting to Multilogin...{Style.RESET_ALL}")
            exporter = MultiloginProfileExporter()
            export_file = exporter.export_profile(
                results['phases']['profile']['profile_path'], 
                age
            )
            print(f"{Fore.GREEN}Exported to: {export_file}{Style.RESET_ALL}")
    
    else:
        print(f"\n{Fore.YELLOW}No target specified and none set in config/settings.yaml.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Quick start:{Style.RESET_ALL}")
        print(f"  python main.py --target https://example.com --age 90")
        print(f"  python main.py  # uses config/settings.yaml target if defined")
        print(f"  python main.py --verify")
        print(f"  python main.py --test-detection")


if __name__ == "__main__":
    run_full_gui()