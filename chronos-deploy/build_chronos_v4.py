import os
import zipfile
import stat
import shutil

# ===============================================================================
# CHRONOS v4.0 :: HERMETIC VEHICLE GENERATOR
# AUTHORITY: Dva.12
# STATUS: OBLIVION_ACTIVE
# ===============================================================================

PROJECT_NAME = "chronos-deploy"

# [1] DOCKERFILE: The Hardened Kernel
# Merges 'cookies factory' hardening with 'chronos-vehicle' VNC base
DOCKERFILE = """
FROM kasmweb/chrome:1.14.0
USER root

# [LAYER 1] SYSTEM HARDENING & ENTROPY
# 'haveged' is critical for VPS entropy to prevent crypto-stalls
# 'iptables' is mandatory for TTL=128 spoofing
RUN apt-get update && apt-get install -y \
    iptables iproute2 haveged sudo \
    python3 python3-pip python3-dev git make gcc \
    && rm -rf /var/lib/apt/lists/*

# [LAYER 2] TEMPORAL ENGINE (libfaketime)
# Compiling from source to ensure CLOCK_MONOTONIC interception
WORKDIR /tmp
RUN git clone https://github.com/wolfcw/libfaketime.git && \
    cd libfaketime/src && make install && rm -rf /tmp/libfaketime

# [LAYER 3] PYTHON ENVIRONMENT
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app ./app

# [LAYER 4] PERMISSIONS & PIPES
RUN mkdir -p /app/time_control && \
    chown -R 1000:1000 /app && \
    chmod 777 /app/time_control

# [LAYER 5] KERNEL INJECTION
ENV LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
ENV FAKETIME_FOLLOW_FILE=/app/time_control/chronos_clock
ENV FAKETIME_DONT_FAKE_MONOTONIC=1

# [LAYER 6] BOOTLOADER
COPY entrypoint.sh /dockerstartup/custom_startup.sh
RUN chmod +x /dockerstartup/custom_startup.sh

USER 1000
ENTRYPOINT ["/dockerstartup/custom_startup.sh"]
"""

# [2] DOCKER-COMPOSE: Orchestration
COMPOSE = """
version: '3.8'
services:
  chronos:
    build: .
    container_name: chronos_vehicle
    # NET_ADMIN is REQUIRED for iptables TTL spoofing
    cap_add:
      - NET_ADMIN
    # Shared memory for Chrome stability
    shm_size: '2gb'
    ports:
      - "6901:6901" # VNC Access
    environment:
      - VNC_PW=password123
    restart: always
"""

# [3] ENTRYPOINT: The Guardian Script
# Merges network hardening from 'Chronos_2026'
ENTRYPOINT = """#!/bin/bash
set -e
echo "[*] CHRONOS v4.0 INITIALIZING..."

# 1. NETWORK HARDENING (TTL=128)
# This defeats Passive OS Fingerprinting (p0f)
if sudo -n true 2>/dev/null; then
    sudo iptables -t mangle -A POSTROUTING -j TTL --ttl-set 128
    echo "[+] Windows Camouflage (TTL=128): ACTIVE"
else
    echo "[!] WARNING: Root check failed. TTL Spoofing skipped."
fi

# 2. INITIALIZE TIME CLOCK
if [ ! -f /app/time_control/chronos_clock ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > /app/time_control/chronos_clock
fi

# 3. START TEMPORAL CONTROLLER
nohup python3 /app/app/controller.py > /app/controller.log 2>&1 &
echo "[+] Temporal Controller: ONLINE (http://localhost:5000)"

# 4. LAUNCH VNC ENVIRONMENT
export LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
export FAKETIME_FOLLOW_FILE=/app/time_control/chronos_clock
export FAKETIME_DONT_FAKE_MONOTONIC=1

exec /dockerstartup/kasm_default_profile.sh /dockerstartup/vnc_startup.sh /dockerstartup/kasm_startup.sh
"""

# [4] REQUIREMENTS
REQUIREMENTS = """
flask
requests
"""

# [5] CONTROLLER: The Time Machine
CONTROLLER = """
from flask import Flask, jsonify, request, render_template
import datetime
import os

app = Flask(__name__)
TIME_FILE = "/app/time_control/chronos_clock"

@app.route('/')
def index():
    try:
        with open(TIME_FILE, 'r') as f: current = f.read().strip()
    except: current = "REALTIME"
    return render_template('panel.html', time=current)

@app.route('/jump', methods=['POST'])
def jump():
    days = int(request.json.get('days', 0))
    # Logic: Offset from NOW
    target = datetime.datetime.now() + datetime.timedelta(days=days)
    
    # '@' sets absolute time for libfaketime
    formatted = f"@{target.strftime('%Y-%m-%d %H:%M:%S')}"
    
    with open(TIME_FILE, 'w') as f:
        f.write(formatted)
        
    return jsonify({"status": "warped", "target": formatted})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
"""

# [6] UI PANEL: The Control Deck
PANEL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .box { border: 1px solid #333; padding: 20px; max-width: 400px; margin: 0 auto; background: #0a0a0a; box-shadow: 0 0 10px rgba(0,255,65,0.1); }
        .btn { background: #111; border: 1px solid #00ff41; color: #00ff41; padding: 15px; width: 100%; margin: 10px 0; cursor: pointer; font-size: 16px; transition: 0.2s; text-transform: uppercase; font-weight: bold; }
        .btn:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
        .stat { font-size: 12px; color: #666; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        h1 { margin-top: 0; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>CHRONOS v4.0</h1>
        <div class="stat">TEMPORAL STATE: {{ time }}</div>
        
        <button class="btn" onclick="jump(-90)">Genesis (T-90 Days)</button>
        <button class="btn" onclick="jump(-45)">Warmup (T-45 Days)</button>
        <button class="btn" onclick="jump(0)">Sync to Present</button>
    </div>
    
    <script>
        function jump(d) {
            fetch('/jump', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({days: d})
            }).then(() => location.reload());
        }
    </script>
</body>
</html>
"""

# [7] CDP INJECTOR: The Stealth Mask (Advanced)
# Merged from 'Chronos_Identity_Engine_2026'
CDP_INJECTOR = """
class CDPInjector:
    def __init__(self, driver):
        self.driver = driver
    
    def apply_stealth(self):
        # Advanced Injection: WebGL, AudioContext, ClientRects
        js = '''
        // 1. WebGL Spoofing (NVIDIA Signature)
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {
            if (p===37445) return 'Google Inc. (NVIDIA)';
            if (p===37446) return 'ANGLE (NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0)';
            return getParameter.apply(this, arguments);
        };

        // 2. AudioContext Noise (Anti-Fingerprint)
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function(channel) {
            const results = originalGetChannelData.apply(this, arguments);
            for (let i = 0; i < results.length; i += 100) {
                results[i] += Math.random() * 0.0000001; 
            }
            return results;
        };

        // 3. Navigator Overrides
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
        '''
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        except:
            pass
"""


def build():
    print(f"[*] INITIALIZING CHRONOS v4.0 BUILD SEQUENCE...")
    
    # 1. Clean previous
    if os.path.exists(PROJECT_NAME):
        shutil.rmtree(PROJECT_NAME)
    os.makedirs(os.path.join(PROJECT_NAME, "app", "templates"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_NAME, "app", "core"), exist_ok=True)

    # 2. Map Files
    files = {
        "Dockerfile": DOCKERFILE,
        "docker-compose.yaml": COMPOSE,
        "entrypoint.sh": ENTRYPOINT,
        "requirements.txt": REQUIREMENTS,
        "app/controller.py": CONTROLLER,
        "app/templates/panel.html": PANEL_HTML,
        "app/core/cdp_injector.py": CDP_INJECTOR,
        "app/core/__init__.py": ""
    }

    # 3. Write
    for path, content in files.items():
        full_path = os.path.join(PROJECT_NAME, path)
        with open(full_path, "w") as f:
            f.write(content.strip())
        print(f"    -> Assembled: {path}")

    # 4. Permissions
    st = os.stat(os.path.join(PROJECT_NAME, "entrypoint.sh"))
    os.chmod(os.path.join(PROJECT_NAME, "entrypoint.sh"), st.st_mode | stat.S_IEXEC)

    # 5. Zip
    zip_name = f"{PROJECT_NAME}.zip"
    print(f"[*] Compressing artifact: {zip_name}")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_NAME):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PROJECT_NAME)
                zipf.write(file_path, arcname)

    print(f"\n[+] BUILD COMPLETE. ARTIFACT READY: {zip_name}")
    print(f"--------------------------------------------------")
    print(f"DEPLOYMENT INSTRUCTIONS (VPS):")
    print(f"1. scp {zip_name} root@<VPS_IP>:/root/")
    print(f"2. ssh root@<VPS_IP>")
    print(f"3. unzip {zip_name} && cd {PROJECT_NAME}")
    print(f"4. docker-compose up -d --build")
    print(f"--------------------------------------------------")

if __name__ == "__main__":
    build()
