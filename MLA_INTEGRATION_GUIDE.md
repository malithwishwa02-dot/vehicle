# Multilogin (MLA) Integration & Manual Handover Protocol

## Overview

This repository has been reconfigured to support Multilogin (MLA) exclusively and enforce Method 4 (Time-Shifting) with manual handover protocol. All checkout automation has been disabled.

## Configuration Changes

### 1. Execution Mode (config/settings.yaml)

```yaml
execution:
  mode: "GENERATE_ONLY"  # Stop after cookie generation (no checkout)
```

**Modes:**
- `GENERATE_ONLY`: Stops automation after cookie generation and profile preparation. Browser profile is ready for manual takeover.
- `FULL`: (Legacy) Runs complete automation cycle including checkout operations.

### 2. Multilogin Settings (config/settings.yaml)

```yaml
multilogin:
  browser_type: "multilogin"   # Browser type
  mla_port: 35000              # Default MLA Local API port
  mla_profile_id: ""           # Leave blank for auto-generation
  headless_mode: false         # MLA must be visible
```

### 3. Config Class (config/settings.py)

```python
from config.settings import Config

Config.EXECUTION_MODE    # "GENERATE_ONLY"
Config.BROWSER_TYPE      # "multilogin"
Config.MLA_PORT          # 35000
Config.MLA_PROFILE_ID    # "" (blank)
Config.HEADLESS_MODE     # False
```

## Usage Flow

### Automated Cookie Generation

1. **Time Shift**: Chronos shifts system time backwards (Method 4)
2. **Profile Creation**: Aged profile is created with MLA
3. **Cookie Generation**: Browser visits trust anchors and generates cookies
4. **State Preservation**: Profile state is saved
5. **Forensic Scrubbing**: Temporal artifacts are cleaned
6. **Reality Restoration**: System time is restored
7. **HANDOVER**: Script prints "READY FOR MANUAL TAKEOVER" and exits

### Manual Takeover

After the script completes with `GENERATE_ONLY` mode:

1. Profile cookies are synced to MLA cloud/disk
2. Profile is closed but preserved
3. User can manually open the profile in Multilogin
4. User performs checkout or other operations manually

## Code Integration

### Using MLABridge

```python
from core.mla_bridge import MLABridge
from core.chronos import ChronosTimeMachine

# Initialize components
chronos = ChronosTimeMachine()
mla_bridge = MLABridge(profile_id="my_profile_123")

# CRITICAL: Shift time BEFORE starting profile
chronos.kill_ntp()
chronos.shift_time(days_ago=90)

# Start MLA profile (browser spawns with shifted kernel time)
mla_bridge.start_profile()

# Attach WebDriver for automation
driver = mla_bridge.attach_webdriver()

# ... perform cookie generation ...

# Stop profile (syncs cookies to MLA)
mla_bridge.stop_profile()

# Restore time
chronos.restore_original_time()
chronos.restore_ntp()
```

### Using MLAHandler

```python
from core.mla_handler import MLAHandler

handler = MLAHandler(profile_id="my_profile_123")

# Start profile with MLA API
# GET http://localhost:35000/api/v1/profile/start?automation=true&puppeteer=true&profileId={id}
handler.start_profile()

# Access the WebDriver
driver = handler.driver

# ... automation ...

# Stop profile (ensures cookie sync)
handler.stop_profile()
```

## API Endpoints

### MLA Local API (Default Port: 35000)

**Start Profile:**
```
GET http://localhost:35000/api/v1/profile/start?automation=true&puppeteer=true&profileId={profile_id}

Response:
{
  "value": "ws://127.0.0.1:<port>/devtools/browser/<id>"
  // OR
  "value": {
    "port": <debugging_port>
  }
}
```

**Stop Profile:**
```
GET http://localhost:35000/api/v1/profile/stop?profileId={profile_id}
GET http://localhost:35000/api/v2/profile/stop?profileId={profile_id}
```

## Chronos Integration

### Critical Timing Sequence

⚠️ **IMPORTANT**: `ChronosTimeMachine.shift_time()` MUST be called BEFORE `mla_handler.start_profile()`

**Reason**: The browser process must spawn AFTER the Windows Kernel time has changed for "Natural Generation" to work correctly. If the profile starts before time shift, cookies will have incorrect timestamps.

```python
# CORRECT ORDER ✓
chronos.shift_time(90)        # 1. Shift time first
mla_bridge.start_profile()    # 2. Start browser (spawns with shifted time)

# WRONG ORDER ✗
mla_bridge.start_profile()    # Browser has real timestamps
chronos.shift_time(90)        # Time shift happens too late
```

### Chronos Methods

```python
from core.chronos import Chronos, ChronosTimeMachine

chronos = Chronos()  # or ChronosTimeMachine()

# Kill NTP service (prevents time sync)
chronos.kill_ntp()

# Shift time backwards
chronos.shift_time(days_ago=90)  # or chronos.time_jump(90)

# Restore original time
chronos.restore_original_time()

# Restore NTP service
chronos.restore_ntp()

# Emergency cleanup (call in except blocks)
chronos.cleanup()
```

## Execution Mode Behavior

### GENERATE_ONLY Mode

When `execution.mode = "GENERATE_ONLY"` in settings.yaml:

```python
# After Phase 8: Reality Restoration
if execution_mode == "GENERATE_ONLY":
    logger.info("[+] CHRONOS: Time restored. Cookies synced to MLA.")
    logger.info(">>> AUTOMATION TERMINATED. PROFILE READY FOR MANUAL TAKEOVER. <<<")
    logger.info(f"Profile: {profile_name}")
    logger.info(f"Profile Path: {profile_path}")
    
    # NOTE: These operations are SKIPPED:
    # - perform_checkout()
    # - add_to_cart()
    # - fill_billing_details()
    
    sys.exit(0)  # Hard stop to prevent accidental automation
```

### Full Mode (Legacy)

If mode is not "GENERATE_ONLY", the script continues with full automation cycle (not recommended for manual operations).

## Level 9 Operations

Run with GENERATE_ONLY mode:

```bash
python level9_operations.py --target stripe --age 90 --profile my_profile
```

Output:
```
============================================================
INITIATING LEVEL 9 FINANCIAL OBLIVION
Target: STRIPE
Profile Age: 90 days
Execution Mode: GENERATE_ONLY
============================================================
[PHASE 1] Chronos Time Shift...
[PHASE 2] Profile Genesis...
[PHASE 3] Pre-Auth Warmup...
[PHASE 4] Entropy Injection...
[PHASE 5] Ghost Signal Triangulation...
[PHASE 6] State Preservation...
[PHASE 7] Forensic Scrubbing...
[PHASE 8] Reality Restoration...
============================================================
[+] CHRONOS: Time restored. Cookies synced to MLA.
>>> AUTOMATION TERMINATED. PROFILE READY FOR MANUAL TAKEOVER. <<<
Profile: my_profile
Profile Path: profiles/chrome/my_profile
============================================================
```

## Security Notes

1. **Admin Required**: Time manipulation requires administrator privileges
2. **NTP Blocked**: UDP port 123 is blocked via Windows Firewall during time shift
3. **Cookie Sync**: Profiles must be stopped via API to ensure cookies are written to disk/cloud
4. **Hard Stop**: `sys.exit(0)` prevents accidental continuation into checkout automation

## Troubleshooting

### Profile Not Starting

- Verify Multilogin is running on port 35000
- Check `Config.MLA_PORT` is correct
- Ensure profile ID is valid or blank for auto-generation

### Time Not Shifting

- Run script as Administrator
- Verify Windows Time service can be stopped
- Check firewall rules are being applied

### Cookies Not Syncing

- Ensure `stop_profile()` is called before script exits
- Wait 2 seconds after browser close for file locks to release
- Check MLA API is responding to stop requests

## Summary

This implementation provides:

✅ **Multilogin (MLA) exclusive support**  
✅ **Method 4 (Time-Shifting) enforcement**  
✅ **All checkout automation disabled**  
✅ **Manual handover protocol**  
✅ **Cookie sync to MLA cloud/disk**  
✅ **Proper Chronos → MLA timing sequence**

The system generates aged cookies and profiles, then hands control to the user for manual operations.
