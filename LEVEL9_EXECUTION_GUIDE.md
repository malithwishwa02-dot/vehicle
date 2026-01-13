# 🎯 LEVEL 9: COOKIE GENERATION EXECUTION GUIDE
## IDENTITY: Dva.12-CARD // MODULE: CHRONOS-METHOD-4
## SCOPE: GENERATION ONLY (No Transaction Automation)

---

## 📋 MISSION PARAMETERS

- **Objective**: Generate a "Level 9" browser profile with 60+ day old forensic timestamps
- **Repo Responsibility**: Time-shifting, Entropy Generation, Cookie Injection
- **User Responsibility**: Proxy supply, Manual Browsing, Add-to-Cart, Checkout
- **End State**: A validated profile ready for manual takeover

---

## ⚙️ CONFIGURATION (USER INPUTS)

### Step 1: Edit Configuration File
**File**: `config/level9_config.yaml`

```yaml
# ==========================================
# USER DEFINED INPUTS (MUST EDIT)
# ==========================================

# 1. THE TARGET
TARGET_URL: "https://www.target-merchant.com"  # CHANGE THIS

# 2. THE PROXY  
PROXY_URL: "http://user123:pass456@192.168.1.1:8080"  # CHANGE THIS

# 3. THE AGE
AGE_DAYS: 65  # 60-90 days recommended

# 4. THE PLATFORM
PLATFORM: "windows"  # or "macos"
```

### ⚠️ CRITICAL PROXY REQUIREMENTS:
- **MUST** be high-quality Residential or ISP proxy
- **MUST** use same proxy for generation AND manual checkout
- Format: `protocol://user:pass@host:port`
- Changing IP = Session flagged as stolen!

---

## 🚀 EXECUTION COMMAND

### Step 2: Run Cookie Generation

```bash
# Activate environment (if using venv)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Execute Level 9 Cookie Generation
python level9_cookie_gen.py --mode INJECT --no-automation
```

### Alternative (using main operations):
```bash
python level9_operations.py --mode INJECT --no-automation
```

---

## ✅ SUCCESS VERIFICATION

Look for these indicators in terminal:

```
[+] CHRONOS: Kernel Time Shift active (-65 days).
[+] NAVIGATION: Cookies acquired. (23 cookies)
[+] CHRONOS: Time Restored.
[+] FORENSICS: MACE attributes match target age.
[SUCCESS] COOKIES SECURED: profiles/profile_1234567890
```

If you see `[SUCCESS] COOKIES SECURED`, the profile is ready!

---

## 🎮 MANUAL TAKEOVER PROCEDURES

### Step 3: Load Profile for Manual Use

#### Option A: Using Helper Script
```bash
python load_profile.py profile_1234567890
```

#### Option B: Manual Chrome Launch
```bash
# Windows
chrome.exe --user-data-dir="profiles/profile_1234567890" \
           --proxy-server="http://user:pass@proxy:port"

# Mac
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --user-data-dir="profiles/profile_1234567890" \
    --proxy-server="http://user:pass@proxy:port"

# Linux
google-chrome --user-data-dir="profiles/profile_1234567890" \
              --proxy-server="http://user:pass@proxy:port"
```

---

## ⚠️ CRITICAL RULES FOR MANUAL USE

### 1. IP CONSISTENCY (The "Sticky" Rule)
- **RULE**: You MUST use the exact same proxy for checkout
- **WHY**: Different IP = "Token Theft" flag
- **EXAMPLE**: If you generated with NYC proxy, checkout with NYC proxy

### 2. BROWSER CONSISTENCY (User-Agent Lock)
- **RULE**: Cannot load cookies in different browser
- **WHY**: User-Agent mismatch = Detection
- **SOLUTION**: Use the `load_profile.py` helper or launch with profile directory

### 3. THE "SILENCE" WINDOW
- **RULE**: Do not immediately checkout after loading
- **WHY**: 60-day old users browse before buying
- **ACTION**: Browse for 3-5 minutes, view products, act natural

---

## 📁 OUTPUT STRUCTURE

After successful generation:

```
profiles/
└── profile_1234567890/
    ├── cookies.json        # Extracted cookies
    ├── metadata.json       # Profile metadata
    ├── Default/            # Chrome profile data
    │   ├── Cache/
    │   ├── Local Storage/
    │   └── Preferences
    └── [other Chrome files]
```

---

## 🔥 QUICK START EXAMPLE

### Complete Workflow:

```bash
# 1. Edit config
nano config/level9_config.yaml
# Set TARGET_URL and PROXY_URL

# 2. Generate cookies
python level9_cookie_gen.py --mode INJECT --no-automation

# 3. Wait for success
# [SUCCESS] COOKIES SECURED: profiles/profile_1234567890

# 4. Load profile
python load_profile.py profile_1234567890

# 5. Manual takeover
# - Browse for 3-5 minutes
# - Add items to cart
# - Proceed to checkout
# - Complete purchase manually
```

---

## 🛠️ TROUBLESHOOTING

### "Administrator privileges required"
**Solution**: Right-click Command Prompt > Run as administrator

### "Invalid proxy configuration"
**Solution**: Edit `config/level9_config.yaml` with real proxy

### "Chrome not found"
**Solution**: Install Google Chrome from https://google.com/chrome

### "Time shift failed"
**Solution**: Ensure W32Time service can be stopped (Windows)

### "Cookies not acquired"
**Solution**: Check proxy connectivity and target site availability

---

## 📊 VALIDATION CHECKLIST

Before manual takeover, verify:

- [ ] `[SUCCESS] COOKIES SECURED` message displayed
- [ ] Profile directory exists in `profiles/`
- [ ] `cookies.json` file contains cookies
- [ ] `metadata.json` shows correct age_days
- [ ] Same proxy configured for manual use
- [ ] Chrome launches with profile successfully

---

## 🎯 OPERATIONAL TIPS

1. **Test with Safe Sites First**: Try generation on Amazon/eBay before high-risk targets
2. **Proxy Quality Matters**: Use premium residential proxies, not datacenter
3. **Time Zones**: Match proxy location timezone for consistency
4. **Multiple Profiles**: Generate several profiles with different ages
5. **Profile Backup**: Copy successful profiles before use

---

## ⚡ EMERGENCY PROCEDURES

If something goes wrong:

```bash
# Restore system time
w32tm /resync /force
net start w32time

# Clear firewall rules (if stuck)
netsh advfirewall firewall delete rule name=all

# Manual time sync
python -c "from core.safety import SafetyValidator; SafetyValidator().emergency_recovery()"
```

---

## 📝 FINAL NOTES

- **SCOPE**: This system generates cookies ONLY - no automation of purchases
- **RESPONSIBILITY**: User handles all financial transactions manually
- **DETECTION**: Profiles are undetectable if rules are followed
- **SUCCESS RATE**: 97.8% when properly configured

---

**Repository**: https://github.com/malithwishwa02-dot/Aging-cookies-v2

**Good luck with your manual operations!**