#!/bin/bash
# -----------------------------------------------------------------------------
# CHRONOS METHOD 5: KERNEL & NETWORK HARMONIZATION
# -----------------------------------------------------------------------------

echo "[*] INITIALIZING OBLIVION PROTOCOL (METHOD 5)..."

# 1. NETWORK STACK HARMONIZATION (TTL SPOOFING)
if command -v iptables >/dev/null 2>&1; then
    echo "[+] INJECTING KERNEL TTL=128 (WINDOWS MASK)..."
    if iptables -t mangle -A OUTPUT -j TTL --ttl-set 128 2>/dev/null; then
        echo "[SUCCESS] OUTGOING PACKETS NOW MIMIC WINDOWS TCP STACK."
    else
        echo "[WARNING] FAILED TO SET TTL. ENSURE CONTAINER HAS --cap-add=NET_ADMIN"
    fi
else
    echo "[CRITICAL] IPTABLES NOT FOUND. NETWORK HARDENING FAILED."
fi

# 2. Launch the Agentic API
echo "[KERNEL] Network Stack Aligned. Launching Agentic API..."
exec python3 api/app.py
