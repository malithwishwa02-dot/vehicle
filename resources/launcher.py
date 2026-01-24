"""Sovereign launcher (dashboard + ignition)
This is an intentionally safe, minimal dashboard/launcher that does not run
external or privileged actions during import. It uses a threaded ignition
function to simulate launching.
"""
from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Optional Flask import so importing the module doesn't require Flask
try:
    from flask import Flask, request, jsonify, send_file
except Exception:
    Flask = None
    request = None
    jsonify = lambda x: x
    send_file = lambda p: None

app = Flask(__name__) if Flask else None


def calculate_time_shift(age_days: int) -> str:
    past = datetime.utcnow() - timedelta(days=int(age_days))
    return past.strftime("%Y-%m-%d %H:%M:%S")


def _launch_browser_process(profile_id: str, age_days: int, proxy: Optional[str]):
    genesis_time = calculate_time_shift(age_days)
    print(f"[LUCID] (sim) Igniting Profile: {profile_id} | Age: {age_days} days -> {genesis_time}")
    # Simulate some activity
    for i in range(3):
        print(f"[LUCID] (sim) browser tick {i+1}/3")
        time.sleep(0.2)
    print("[LUCID] (sim) Browser session ended.")


def launch_browser_process(profile_id: str, age_days: int = 90, proxy: Optional[str] = None, threaded: bool = True):
    if threaded:
        t = threading.Thread(target=_launch_browser_process, args=(profile_id, age_days, proxy), daemon=True)
        t.start()
        return t
    else:
        _launch_browser_process(profile_id, age_days, proxy)
        return None


if app:
    @app.route('/')
    def index():
        root = Path(__file__).resolve().parents[1]
        dashboard = root / "dashboard.html"
        if dashboard.exists():
            return send_file(str(dashboard))
        return "<html><body>Dashboard placeholder</body></html>"

    @app.route('/api/ignite', methods=['POST'])
    def ignite_route():
        data = request.json or {}
        profile_id = data.get('id', 'TEST')
        age = int(data.get('age', 90))
        proxy = data.get('proxy')
        launch_browser_process(profile_id, age, proxy)
        return jsonify({"status": "IGNITION_SEQUENCE_STARTED"})

    if __name__ == "__main__":
        print("[*] LUCID EMPIRE DASHBOARD: http://localhost:1337")
        app.run(port=1337)
