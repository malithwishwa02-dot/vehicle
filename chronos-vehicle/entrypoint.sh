#!/bin/bash
set -e
echo "[*] CHRONOS VEHICLE INITIALIZING..."

# 0. Ensure the time control directory exists and is writable
if [ ! -d /app/time_control ]; then
  mkdir -p /app/time_control
  chown 1000:1000 /app/time_control || true
  chmod 777 /app/time_control || true
fi

# 1. NETWORK HARDENING (OS FINGERPRINT MASKING)
if [ "$(id -u)" -eq 0 ]; then
    iptables -t mangle -A POSTROUTING -j TTL --ttl-set 128 || echo "[!] iptables not available or failed"
    echo "[+] Windows Camouflage (TTL=128): ACTIVE"
else
    echo "[!] WARNING: Not running as root. TTL Spoofing skipped."
fi

# 2. INITIALIZE TEMPORAL CLOCK (default to server time if empty)
if [ ! -s /app/time_control/chronos_clock ]; then
    date '+%Y-%m-%d %H:%M:%S' > /app/time_control/chronos_clock
fi

# 2.1 Ensure CHRONOS_TOKEN is set (used to protect the /jump endpoint)
if [ -z "${CHRONOS_TOKEN}" ]; then
    echo "[!] CHRONOS_TOKEN not provided. Generating a random token and saving to /app/.env"
    CHRONOS_TOKEN=$(python3 - <<'PY'
import secrets
print(secrets.token_hex(20))
PY
)
    echo "CHRONOS_TOKEN=${CHRONOS_TOKEN}" >> /app/.env
fi
export CHRONOS_TOKEN

# 3. LAUNCH SIDE-CAR CONTROLLER (daemonized)
echo "[+] Launching Temporal Controller on 127.0.0.1:5000"
nohup python3 /app/app/controller.py > /app/controller.log 2>&1 &

# 4. LAUNCH KASM VNC & CHROME (inherit faketime env vars)
export LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
export FAKETIME_FOLLOW_FILE=/app/time_control/chronos_clock
export FAKETIME_DONT_FAKE_MONOTONIC=1

exec /dockerstartup/kasm_default_profile.sh /dockerstartup/vnc_startup.sh /dockerstartup/kasm_startup.sh
