#!/bin/bash
# ==============================================================================
# PROMETHEUS-CORE Entrypoint Script
# Initializes Xvfb and FAKETIME environment for temporal manipulation
# ==============================================================================

set -e

echo "================================================================"
echo "PROMETHEUS-CORE Container Initialization"
echo "================================================================"

# ==============================================================================
# PHASE 1: Xvfb (Virtual Display) Initialization
# ==============================================================================
echo "[PHASE 1] Initializing Xvfb Virtual Display on :99..."

# Start Xvfb in background
Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!

# Wait for Xvfb to be ready
sleep 2

if ps -p $XVFB_PID > /dev/null; then
    echo "✓ Xvfb started successfully (PID: $XVFB_PID)"
else
    echo "✗ ERROR: Xvfb failed to start"
    exit 1
fi

# Set DISPLAY environment variable
export DISPLAY=:99
echo "✓ DISPLAY set to :99"

# ==============================================================================
# PHASE 2: FAKETIME Calculation and Injection
# ==============================================================================
echo ""
echo "[PHASE 2] Calculating FAKETIME offset..."

# Get GENESIS_OFFSET_DAYS from environment (default: 90)
OFFSET_DAYS=${GENESIS_OFFSET_DAYS:-90}
echo "  Genesis Offset: $OFFSET_DAYS days"

# Calculate target date (current date - offset days)
# Format: YYYY-MM-DD HH:MM:SS for libfaketime
TARGET_DATE=$(date -d "$OFFSET_DAYS days ago" "+%Y-%m-%d %H:%M:%S")
echo "  Target Date: $TARGET_DATE"

# Calculate offset for libfaketime (relative format: -Xd)
FAKETIME_OFFSET="-${OFFSET_DAYS}d"

# Export FAKETIME environment variable for global interception
export FAKETIME="$FAKETIME_OFFSET"
echo "✓ FAKETIME set to: $FAKETIME"

# Export additional faketime configuration
export FAKETIME_DONT_FAKE_MONOTONIC=1
export FAKETIME_NO_CACHE=1

# ==============================================================================
# PHASE 3: Time Shift Validation
# ==============================================================================
echo ""
echo "[PHASE 3] Validating time shift..."

# Get actual current time
ACTUAL_TIME=$(TZ=UTC date "+%Y-%m-%d %H:%M:%S")
echo "  Host Time (actual): $ACTUAL_TIME"

# Get faketime-adjusted time
FAKE_TIME=$(date "+%Y-%m-%d %H:%M:%S")
echo "  Container Time (shifted): $FAKE_TIME"

# Verify LD_PRELOAD is active
if [ -n "$LD_PRELOAD" ]; then
    echo "✓ LD_PRELOAD active: $LD_PRELOAD"
else
    echo "✗ WARNING: LD_PRELOAD not set!"
fi

# Verify libfaketime is loaded
if ldd /usr/bin/date | grep -q libfaketime; then
    echo "✓ libfaketime detected in date binary"
else
    echo "⚠ WARNING: libfaketime not detected (may be normal)"
fi

# ==============================================================================
# PHASE 4: Application Launch
# ==============================================================================
echo ""
echo "[PHASE 4] Launching PROMETHEUS-CORE application..."
echo "  Command: $@"
echo "================================================================"
echo ""

# Execute the main command passed to the container
exec "$@"
