#!/usr/bin/env python3
"""Quick Multilogin availability check.

This script pings the local MLA API to confirm the desktop agent is live
before launching Chronos operations.
"""

import sys
import requests

API_URL = "http://localhost:35000/api/v1/profile/active"


def main() -> int:
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            print("[+] MLA API reachable (200 OK). Ready for Chronos.")
            return 0
        print(f"[!] MLA API responded with {response.status_code}. Check the agent log.")
        return 1
    except requests.ConnectionError:
        print("[!] Cannot reach MLA API (connection refused). Start Multilogin and try again.")
        return 2
    except requests.Timeout:
        print("[!] MLA API request timed out. Confirm the agent is running on port 35000.")
        return 3
    except Exception as exc:  # catch-all for unexpected issues
        print(f"[!] Unexpected error: {exc}")
        return 4


if __name__ == "__main__":
    sys.exit(main())
