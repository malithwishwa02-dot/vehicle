import requests
import sys
import time
from datetime import datetime

# CONFIGURATION
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:5000/health"

class PrometheusVerifier:
    def __init__(self):
        self.logs = []

    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{status}] {message}"
        print(entry)
        self.logs.append(entry)

    def check_service(self, name, url):
        self.log(f"Pinging {name} at {url}...")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.log(f"{name} is ONLINE. (Status: {response.status_code})", "SUCCESS")
                return True
            else:
                self.log(f"{name} returned unexpected status: {response.status_code}", "WARNING")
                return False
        except requests.exceptions.ConnectionError:
            self.log(f"{name} is UNREACHABLE.", "FAIL")
            return False
        except Exception as e:
            self.log(f"{name} Error: {str(e)}", "FAIL")
            return False

    def run(self):
        print("\n=== PROMETHEUS SYSTEM VERIFIER ===\n")
        
        backend_status = self.check_service("Backend Core", BACKEND_URL)
        frontend_status = self.check_service("Frontend GUI", FRONTEND_URL)
        
        print("\n----------------------------------")
        if backend_status and frontend_status:
            print("SYSTEM STATUS: GREEN (OPERATIONAL)")
            sys.exit(0)
        else:
            print("SYSTEM STATUS: RED (DEGRADED)")
            sys.exit(1)

if __name__ == "__main__":
    verifier = PrometheusVerifier()
    verifier.run()
