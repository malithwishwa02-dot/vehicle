#!/usr/bin/env python3
"""
PROFILE LOADER - Manual Takeover Helper
Loads generated Level 9 profiles with correct settings
"""

import sys
import json
import subprocess
from pathlib import Path
import argparse


def load_profile(profile_id: str, proxy_url: str = None, launch: bool = True, force_windows: bool = False):
    """
    Load a generated profile for manual takeover.
    
    Args:
        profile_id: Profile directory name or path
        proxy_url: Proxy URL (uses config if not provided)
        launch: If False, do not actually spawn the browser; return commands for inspection
        force_windows: If True, behave as-if running on Windows (for testing)
    """
    
    # Find profile path
    if Path(profile_id).exists():
        profile_path = Path(profile_id).absolute()
    elif Path(f"profiles/{profile_id}").exists():
        profile_path = Path(f"profiles/{profile_id}").absolute()
    else:
        print(f"[!] Profile not found: {profile_id}")
        print("\nAvailable profiles:")
        profiles_dir = Path("profiles")
        if profiles_dir.exists():
            for p in profiles_dir.iterdir():
                if p.is_dir():
                    print(f"  - {p.name}")
        return False
    
    print(f"\n[*] Loading profile: {profile_path}")
    
    # Load metadata
    metadata_file = profile_path / "metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        print(f"[+] Profile age: {metadata.get('age_days')} days")
        print(f"[+] Target site: {metadata.get('target_url')}")
        print(f"[+] Created: {metadata.get('created')}")
    
    # Load cookies info
    cookies_file = profile_path / "cookies.json"
    if cookies_file.exists():
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
        print(f"[+] Cookies loaded: {len(cookies)} cookies")
    
    # Get proxy from config if not provided
    if not proxy_url:
        try:
            import yaml
            with open('config/level9_config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            proxy_url = config.get('PROXY_URL')
            print(f"[+] Using proxy from config: {proxy_url}")
        except:
            print("[!] No proxy specified and config not found")
            print("    Provide proxy with --proxy flag")
            return False
    
    # Build Chrome launch command
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "chrome"
    ]
    
    chrome_exe = None
    for path in chrome_paths:
        if Path(path).exists():
            chrome_exe = path
            break
    
    if not chrome_exe:
        if not launch:
            chrome_exe = 'chrome'  # placeholder for tests/dry-run
        else:
            print("[!] Chrome not found. Install Google Chrome.")
            return False
    
    # Launch command
    cmd = [
        chrome_exe,
        f"--user-data-dir={profile_path}",
    ]
    
    if proxy_url and proxy_url != "http://user123:pass456@192.168.1.1:8080":
        cmd.append(f"--proxy-server={proxy_url}")
    
    print("\n" + "="*60)
    print("LAUNCHING CHROME WITH LEVEL 9 PROFILE")
    print("="*60)
    
    print("\nREMEMBER THE RULES:")
    print("1. IP CONSISTENCY - Use the same proxy")
    print("2. SILENCE WINDOW - Browse 3-5 minutes before checkout")
    print("3. ACT NATURAL - You're a 60+ day old user returning")
    
    print("\nLaunch command:")
    print(" ".join(cmd))
    
    print("\n[*] Opening Chrome...")
    
    # Build runasdate wrapper if on Windows
    runner_exe = None
    runas_cmd = None
    try:
        import platform
        is_windows = (platform.system() == 'Windows') or force_windows
    except Exception:
        is_windows = bool(force_windows)

    if is_windows:
        # Look for bundled RunAsDate first
        candidates = [Path('bin') / 'RunAsDate.exe', Path('RunAsDate.exe')]
        for c in candidates:
            if c.exists():
                runner_exe = str(c)
                break
        if runner_exe and metadata_file.exists():
            try:
                meta = json.loads(metadata_file.read_text())
                faketime = meta.get('faketime')
                if faketime:
                    date_part, time_part = faketime.split(' ')
                    runas_cmd = f'"{runner_exe}" /immediate /movetime /date {date_part} /time {time_part} "{chrome_exe}" '
            except Exception:
                runas_cmd = None

    if not launch:
        return {'cmd': cmd, 'runner': runner_exe, 'runas_cmd': runas_cmd}

    try:
        # Launch Chrome (optionally via RunAsDate on Windows)
        if runas_cmd:
            # Append args to the runas string
            args_str = ' '.join([f'--user-data-dir="{profile_path}"'] + ([f'--proxy-server={proxy_url}'] if proxy_url else []))
            full_cmd = runas_cmd + args_str
            subprocess.Popen(full_cmd, shell=True)
        else:
            subprocess.Popen(cmd)
        
        print("[+] Chrome launched successfully")
        print("\nProfile is ready for manual takeover!")
        return True
        
    except Exception as e:
        print(f"[!] Failed to launch Chrome: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Load Level 9 profile for manual takeover"
    )
    
    parser.add_argument('profile', type=str,
                       help='Profile ID or path')
    parser.add_argument('--proxy', type=str, default=None,
                       help='Proxy URL (uses config if not specified)')
    
    args = parser.parse_args()
    
    success = load_profile(args.profile, args.proxy)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())