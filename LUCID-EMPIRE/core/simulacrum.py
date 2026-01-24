"""Simulacrum Engine (scaffold)
Combines Data Generation, Behavioral Simulation, Commerce, and Validation into a single class.
This scaffold is intentionally non-destructive and safe for CI tests: it will not perform real checkouts or remote calls.
"""
import os
import logging
from typing import Dict, Any, Optional

try:
    from tools.leveldb_writer import write_local_storage
except Exception:
    write_local_storage = None

try:
    from tools.burner import Burner
except Exception:
    Burner = None

try:
    from modules.human_mouse import HumanMouse
except Exception:
    HumanMouse = None

try:
    from core.constructor import Constructor
except Exception:
    Constructor = None

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Simulacrum:
    def __init__(self, persona: Dict[str, Any], scenario: str = "warmup", runtime_config: Optional[Dict[str, Any]] = None):
        self.persona = persona
        self.scenario = scenario
        self.runtime_config = runtime_config or {}
        self.profile_path = None
        self.burner = Burner(self.persona) if Burner else None

    def build_profile_skeleton(self, out_dir: str) -> str:
        """Create profile skeleton (non-destructive): uses Constructor if available."""
        if Constructor:
            c = Constructor()
            profile_path, _ = c.build_skeleton(proxy_config=self.runtime_config.get('proxy'), persona=self.persona)
            self.profile_path = profile_path
            logger.info(f"Profile skeleton built at {self.profile_path}")
            return str(self.profile_path)
        else:
            # Fallback to a temp folder
            os.makedirs(out_dir, exist_ok=True)
            self.profile_path = os.path.abspath(out_dir)
            logger.info(f"Fallback profile skeleton created at {self.profile_path}")
            return self.profile_path

    def inject_data(self) -> bool:
        """Inject cookies/localStorage using Burner or write_local_storage if available."""
        if self.burner:
            logger.info("Using Burner to inject data (safe-mode)")
            try:
                self.burner.profile_path = self.profile_path
                self.burner.simulate_profile(self.persona, dry_run=True)
                return True
            except Exception as e:
                logger.warning(f"Burner injection failed: {e}")
        if write_local_storage:
            logger.info("Using leveldb writer to create simulated local_storage snapshot.")
            data = {
                'autofill_name': self.persona.get('name', 'John Doe'),
                'autofill_email': self.persona.get('email', 'noreply@example.com')
            }
            lvl_dir = os.path.join(self.profile_path, 'Default', 'Local Storage', 'leveldb')
            os.makedirs(lvl_dir, exist_ok=True)
            ok = write_local_storage(lvl_dir, data)
            logger.info(f"LevelDB write ok={ok}")
            return True
        logger.warning("No injection mechanism available in this environment.")
        return False

    def simulate_behavior(self) -> bool:
        """Run non-network behavioral simulation (e.g., mouse paths) in dry-run mode."""
        if HumanMouse:
            logger.info("Simulating human mouse behavior (dry-run)")
            try:
                # Create a dummy HumanMouse with a mocked driver if necessary
                hm = HumanMouse(driver=None)
                path = hm._generate_mouse_path() if hasattr(hm, '_generate_mouse_path') else []
                logger.info(f"Generated mouse path length: {len(path)}")
                return True
            except Exception as e:
                logger.warning(f"HumanMouse simulation failed: {e}")
        else:
            logger.info("HumanMouse not available; skipping behavior simulation.")
        return False

    def run(self, out_dir: Optional[str] = None) -> Dict[str, Any]:
        """High-level run that builds skeleton, injects data, and simulates behavior. Returns a status dict."""
        logger.info(f"Simulacrum run started: scenario={self.scenario}")
        if out_dir is None:
            if os.name == 'nt':
                # Use AppData\Local\LucidEmpire\profiles on Windows
                out_dir = os.path.join(os.getenv('LOCALAPPDATA', os.path.expanduser('~')), 'LucidEmpire', 'profiles', 'simulacrum_profile')
            else:
                out_dir = '/tmp/simulacrum_profile'
        self.build_profile_skeleton(out_dir)
        injected = self.inject_data()
        behaved = self.simulate_behavior()
        return {'profile_path': self.profile_path, 'injected': injected, 'behavior_simulated': behaved}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='/tmp/simulacrum_profile')
    ap.add_argument('--name', default='John Doe')
    ap.add_argument('--scenario', default='warmup')
    args = ap.parse_args()

    persona = {'name': args.name, 'email': 'auto@example.com'}
    s = Simulacrum(persona, scenario=args.scenario)
    res = s.run(out_dir=args.out)
    print(res)
