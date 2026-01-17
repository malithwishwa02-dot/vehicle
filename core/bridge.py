import requests
import os
import shutil
import time
from config import settings

class HybridBridge:
    def __init__(self):
        self.token = None

    def authenticate(self):
        url = f"{settings.LAUNCHER_URL}/user/signin"
        data = {"email": settings.MLX_EMAIL, "password": settings.MLX_PASSWORD}
        r = requests.post(url, json=data, verify=False)
        r.raise_for_status()
        self.token = r.json()["data"]["token"]
        return self.token

    def start_profile(self):
        url = f"{settings.LAUNCHER_URL}/profile/f/{settings.FOLDER_ID}/p/{settings.PROFILE_ID}/start"
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.post(url, headers=headers, verify=False)
        r.raise_for_status()
        resp = r.json()["data"]
        return resp["profile_id"], resp["remote_debugging_port"], resp["profile_path"]

    def stop_profile(self):
        url = f"{settings.LAUNCHER_URL}/profile/f/{settings.FOLDER_ID}/p/{settings.PROFILE_ID}/stop"
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.post(url, headers=headers, verify=False)
        r.raise_for_status()

    def kernel_time_shift(self, profile_path):
        # Set all files in profile_path to the target age
        target_time = time.time() - settings.PROFILE_AGE_DAYS * 86400
        for root, dirs, files in os.walk(profile_path):
            for name in files:
                file_path = os.path.join(root, name)
                os.utime(file_path, (target_time, target_time))
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.utime(dir_path, (target_time, target_time))
