
import requests
import sys
import secrets
import time

PORT = 45000
PROFILE_ID = "37ab1612-c285-4314-b32a-6a06d35d6d84"

endpoints = [
    "/api/v1/profile/active",
    "/api/v1/profile/start",
    "/api/v1/profile/start?profileId={pid}",
    "/api/v1/profile/start?automation=true&puppeteer=true&profileId={pid}",
    "/api/v2/profile/start?profileId={pid}",
    "/api/v2/profile/active",
    "/api/v2/profile/{pid}/start",
    "/api/v3/profile/{pid}/start",
    "/profile/start?profileId={pid}",
    "/profile/{pid}/start",
    "/v1.0/profile/start?profileId={pid}",
    "/v2/profile/start?profileId={pid}",
    "/v3/profile/start?profileId={pid}",
    "/api/profile/start?profileId={pid}",
    "/api/profile/{pid}/start",
    "/api/profile/start",
    "/profile/start",
    "/profile/active",
    "/api/active",
    "/api/status",
    "/status",
]


MAX_RETRIES = 5

for ep in endpoints:
    url = f"http://127.0.0.1:{PORT}" + ep.replace("{pid}", PROFILE_ID)
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"{url} -> {r.status_code} | {r.text[:100]}")
                break
            else:
                print(f"{url} -> {r.status_code} | {r.text[:100]}")
                # Exponential backoff with jitter
                jitter = secrets.randbelow(1000) / 1000.0
                wait_time = (2 ** attempt) + jitter
                print(f"[WARN] {url} failed (status {r.status_code}), retrying in {wait_time:.2f}s...", file=sys.stderr)
                time.sleep(wait_time)
                attempt += 1
        except Exception as e:
            jitter = secrets.randbelow(1000) / 1000.0
            wait_time = (2 ** attempt) + jitter
            print(f"{url} -> ERROR: {e}", file=sys.stderr)
            print(f"[WARN] {url} exception, retrying in {wait_time:.2f}s...", file=sys.stderr)
            time.sleep(wait_time)
            attempt += 1
    else:
        print(f"[FAIL] {url} failed after {MAX_RETRIES} attempts.", file=sys.stderr)
