"""
MODULE: core/resilient_api.py
STATUS: NEW (Prometheus v2.1)
AUTHORITY: Dva.12

PURPOSE:
Drop-in replacement for brittle API calls. 
Prevents 'ConnectionRefused' and 429 Rate Limits using exponential backoff.
"""

import time
import secrets
import requests
import logging
from typing import Optional, Dict, Any

# Configure Logger
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("API_RESILIENCE")

class ResilientClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Prometheus/2.1)"
        }
        self.rng = secrets.SystemRandom()

    def _get_jitter(self) -> float:
        """Returns random jitter between 0.1s and 1.0s"""
        return 0.1 + (self.rng.random() * 0.9)

    def request(self, method: str, endpoint: str, data: Optional[Dict] = None, max_retries: int = 5) -> Optional[Dict]:
        """
        Executes an API request with exponential backoff.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(max_retries):
            try:
                if method.upper() == "GET":
                    resp = requests.get(url, headers=self.headers, timeout=10)
                elif method.upper() == "POST":
                    resp = requests.post(url, json=data, headers=self.headers, timeout=10)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Success Case
                if resp.status_code in [200, 201]:
                    return resp.json()
                
                # Rate Limit Case (429)
                if resp.status_code == 429:
                    wait_time = (2 ** attempt) + self._get_jitter()
                    logger.warning(f"[!] Rate Limit Hit. Cooling down for {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue

                # Server Error Case (5xx)
                if 500 <= resp.status_code < 600:
                    wait_time = (2 ** attempt) + self._get_jitter()
                    logger.error(f"[!] Server Error {resp.status_code}. Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue
                
                # Client Error Case (4xx) - Do not retry usually, but logging it
                logger.error(f"[X] Client Error {resp.status_code}: {resp.text}")
                return None

            except requests.exceptions.RequestException as e:
                wait_time = (2 ** attempt) + self._get_jitter()
                logger.warning(f"[!] Network Error: {e}. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)

        logger.critical(f"[FATAL] Max retries ({max_retries}) exceeded for {endpoint}.")
        return None

# Example usage function to replace standard requests
def safe_post(url, json_data):
    # Quick wrapper for backward compatibility
    # Assumes URL includes base
    client = ResilientClient(url, "dummy_key") # Key should be handled via config
    return client.request("POST", "", data=json_data)
