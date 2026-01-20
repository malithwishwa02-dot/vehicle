#!/bin/bash
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