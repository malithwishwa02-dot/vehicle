import requests

endpoints = [
    "/api/v2/profile",
    "/api/v1/profile", 
    "/profile",
    "/api",
    "/",
    "/api/v2/profile/start",
    "/v1.0/profile/start",
    "/v2/profile/start"
]

for ep in endpoints:
    try:
        r = requests.get(f"http://localhost:45000{ep}", timeout=5)
        print(f"{ep}: {r.status_code}")
    except Exception as e:
        print(f"{ep}: ERROR - {e}")
