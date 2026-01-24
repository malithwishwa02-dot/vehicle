"""LUCID EMPIRE :: Simulacrum Engine

Safe-by-default engine that combines profile generation, behavior simulation,
and data injection. All network and destructive operations are disabled in
"dry_run" mode; tests should use dry_run=True.
"""
import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SimulacrumEngine:
    def __init__(self, profile_root: str = "./profiles", dry_run: bool = True):
        self.profile_root = profile_root
        self.dry_run = dry_run
        os.makedirs(self.profile_root, exist_ok=True)

    def _calculate_genesis(self, age_days: int) -> str:
        genesis_date = datetime.utcnow() - timedelta(days=age_days)
        return genesis_date.strftime("%Y-%m-%d %H:%M:%S")

    def _build_profile_skeleton(self, operation_id: str) -> str:
        out = os.path.join(self.profile_root, operation_id)
        os.makedirs(out, exist_ok=True)
        # Create minimal Default dir structure
        default = os.path.join(out, "Default")
        os.makedirs(os.path.join(default, "Local Storage", "leveldb"), exist_ok=True)
        # metadata placeholder
        return out

    def genesis(self, operation_id: str, fullz: Dict[str, Any], proxy: Optional[str], age_days: int = 90) -> Dict[str, Any]:
        """Create a profile artifact and return metadata.

        Returns a dict with keys: status, path, config
        """
        logger.info(f"Simulacrum genesis start: op={operation_id} age={age_days} dry_run={self.dry_run}")
        path = self._build_profile_skeleton(operation_id)
        faketime = self._calculate_genesis(age_days)

        # metadata file
        meta = {
            "id": operation_id,
            "created": datetime.utcnow().isoformat() + "Z",
            "age_days": age_days,
            "faketime": faketime,
            "proxy": proxy
        }
        with open(os.path.join(path, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # Simulate injecting deterministic fingerprint and local storage snapshot
        sample_ls = {
            "autofill_name": fullz.get("name", "Test User"),
            "autofill_email": fullz.get("email", "test@example.com"),
            "previous_purchases": "3"
        }
        lvl_dir = os.path.join(path, "Default", "Local Storage", "leveldb")
        try:
            from tools.leveldb_writer import write_local_storage
            write_local_storage(lvl_dir, sample_ls)
            injected = True
        except Exception:
            # If leveldb writer isn't available, write a JSON snapshot
            os.makedirs(lvl_dir, exist_ok=True)
            with open(os.path.join(lvl_dir, "local_storage_simulated.json"), "w", encoding="utf-8") as f:
                json.dump(sample_ls, f, indent=2)
            injected = False

        result = {
            "status": "OK",
            "path": path,
            "config": {
                "faketime": faketime,
                "proxy": proxy,
                "fingerprint": {
                    "navigator": {"platform": "Windows NT", "userAgent": "Camoufox/Genesis"}
                },
                "injected": injected
            }
        }

        logger.info(f"Simulacrum genesis complete: {result}")
        return result


if __name__ == "__main__":
    # quick smoke check
    s = SimulacrumEngine(dry_run=True)
    r = s.genesis("smoke-001", {"name": "Smoke", "email": "smoke@example.com"}, proxy=None, age_days=90)
    print(r)
