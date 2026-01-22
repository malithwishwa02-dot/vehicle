"""
PROMETHEUS-CORE v3.0 :: MODULE: DEPLOYER
AUTHORITY: Dva.13 | STATUS: OPERATIONAL
PURPOSE: Package generated artifacts for Multilogin/Vehicle injection.
"""

import os
import shutil
import zipfile
import json
from pathlib import Path

class ProfilePackager:
    def __init__(self, profile_path, output_name="mlx_import_package"):
        self.profile_path = Path(profile_path)
        self.output_name = output_name
        self.uuid = self.profile_path.name

    def sanitize(self):
        """Removes lock files that might cause import errors."""
        print(f"[DEPLOYER] Sanitizing artifact: {self.profile_path}")
        locks = list(self.profile_path.glob("**/*.lock"))
        for lock in locks:
            try:
                os.remove(lock)
                print(f"  > Removed lock: {lock.name}")
            except:
                pass

    def inject_metadata(self):
        """Creates the app.properties or metadata.json required by the target environment."""
        print("[DEPLOYER] Injecting operational metadata...")
        
        # Multilogin/Vehicle specific metadata
        metadata = {
            "profileId": self.uuid,
            "browserType": "mimic",
            "browserVersion": "120.0.6099.71", # Example version
            "os": "win" if os.name == 'nt' else "lin"
        }
        
        # Write to core root if needed (adjust based on specific vehicle docs)
        with open(self.profile_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

    def compress(self, exclude_sensitive: bool = True):
        """Zips the profile for transport.

        By default, a list of sensitive files is excluded to avoid accidental
        export of system-bound secrets (e.g., Local State / Login Data).
        Set `exclude_sensitive=False` to include everything (use with caution).
        """
        zip_filename = f"{self.output_name}_{self.uuid}.zip"
        print(f"[DEPLOYER] Compressing to {zip_filename} (exclude_sensitive={exclude_sensitive})...")

        sensitive_names = {
            'Local State',
            'Web Data',
            'History',
            'Cookies',
            'Login Data',
            'Preferences'
        }

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.profile_path):
                for file in files:
                    # Skip known sensitive files when requested
                    if exclude_sensitive and os.path.basename(file) in sensitive_names:
                        print(f"  > Skipping sensitive file: {file} (relative: {os.path.relpath(root, self.profile_path)})")
                        continue

                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.profile_path.parent)
                    zipf.write(file_path, arcname)

        print(f"[SUCCESS] Package ready: {zip_filename}")
        return zip_filename

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Package a generated Chromium profile for MLX import")
    ap.add_argument('--profile', '-p', default='generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84', help='Path to generated profile')
    ap.add_argument('--out', '-o', default='mlx_import_package', help='Base name for output zip')
    ap.add_argument('--include-sensitive', action='store_true', help='Include sensitive files (Local State, Web Data, Cookies)')
    args = ap.parse_args()

    target_profile = args.profile

    if os.path.exists(target_profile):
        packager = ProfilePackager(target_profile, output_name=args.out)
        packager.sanitize()
        packager.inject_metadata()
        packager.compress(exclude_sensitive=not args.include_sensitive)
    else:
        print(f"[ERROR] Path not found: {target_profile}")
