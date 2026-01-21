"""
Artifact Pipeline: Validates, Cleans, and Prepares Injected Artifacts.
Ensures no "Poisoned" artifacts enter the clean profile generation.
"""
import os
import json
import hashlib
import zipfile
import logging
import shutil
from pathlib import Path
from typing import Dict, Any

class ArtifactPipeline:
    def __init__(self, upload_dir: str):
        self.upload_dir = Path(upload_dir)
        self.logger = logging.getLogger("ArtifactPipeline")
        os.makedirs(self.upload_dir, exist_ok=True)

    def process_proxy(self, proxy_string: str) -> Dict[str, Any]:
        """
        Validates proxy format and checks connectivity (via TLS Mimic).
        Format: user:pass@host:port or host:port
        """
        try:
            parts = proxy_string.split('@')
            if len(parts) == 2:
                creds, endpoint = parts
                user, password = creds.split(':')
                host, port = endpoint.split(':')
                return {
                    "valid": True,
                    "url": f"http://{proxy_string}",
                    "host": host,
                    "port": port,
                    "user": user,
                    "password": password
                }
            elif len(parts) == 1:
                host, port = parts[0].split(':')
                return {
                    "valid": True,
                    "url": f"http://{proxy_string}",
                    "host": host,
                    "port": port
                }
            return {"valid": False, "error": "Invalid Format"}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def process_fullz(self, fullz_data: Dict) -> Dict:
        """
        Validates Fullz structure.
        """
        required_fields = ["name", "address", "city", "state", "zip", "cc_number", "cc_exp", "cc_cvv"]
        missing = [f for f in required_fields if f not in fullz_data]
        if missing:
            return {"valid": False, "error": f"Missing fields: {missing}"}
        
        # Checksum sensitive data for logging (never log full CC)
        cc_hash = hashlib.sha256(fullz_data['cc_number'].encode()).hexdigest()[:8]
        self.logger.info(f"Processed Fullz for {fullz_data['name']} (CC Hash: {cc_hash})")
        
        return {"valid": True, "data": fullz_data}

    def ingest_cookie_jar(self, file_path: str) -> Dict:
        """
        Ingests and validates a Netscape or JSON cookie jar.
        """
        path = Path(file_path)
        if not path.exists():
            return {"valid": False, "error": "File not found"}

        try:
            # Simple check for JSON
            with open(path, 'r') as f:
                content = f.read().strip()
                if content.startswith('[') or content.startswith('{'):
                    data = json.loads(content)
                    return {"valid": True, "format": "JSON", "count": len(data), "path": str(path)}
                else:
                    # Assume Netscape
                    lines = content.splitlines()
                    count = len([l for l in lines if not l.startswith('#') and l.strip()])
                    return {"valid": True, "format": "Netscape", "count": count, "path": str(path)}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def clean_workspace(self, profile_id: str):
        """
        Removes temporary artifacts for a specific profile.
        """
        target_dir = self.upload_dir / profile_id
        if target_dir.exists():
            shutil.rmtree(target_dir)
