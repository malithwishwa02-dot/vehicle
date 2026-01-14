# 🚀 PROMETHEUS-CORE Quick Start Guide

Get up and running with PROMETHEUS-CORE in under 10 minutes!

---

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Windows 10 or 11** (64-bit)
- [ ] **Administrator privileges** (required!)
- [ ] **Python 3.10+** installed
- [ ] **Google Chrome** browser installed
- [ ] **8GB RAM** minimum
- [ ] **10GB free disk space**
- [ ] **Stable internet connection**

---

## Installation (5 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/malithwishwa02-dot/Aging-cookies-v2.git
cd Aging-cookies-v2
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- Browser automation tools (Selenium, undetected-chromedriver)
- Cryptography libraries
- Windows-specific packages (pywin32, wmi)
- And more...

### Step 3: Verify Administrator Access

```bash
# Check if you have admin privileges
python -c "import ctypes; print('✓ Admin Access' if ctypes.windll.shell32.IsUserAnAdmin() else '✗ Need Admin Access')"
```

If you see "✗ Need Admin Access":
1. Right-click on Command Prompt or PowerShell
2. Select "Run as administrator"
3. Navigate back to the project directory

---

## Your First Operation (3 minutes)

### Basic 90-Day Profile Aging

⚠️ **Important**: This will temporarily modify your system time. Ensure you're in a test environment!

```bash
# Run verification first (recommended)
python verify_implementation.py

# Execute basic aging operation
python main.py --target https://www.example.com --age 90
```

### What This Does:

1. **Isolates** your system from NTP time servers
2. **Shifts** system time back 90 days
3. **Creates** an aged browser profile
4. **Generates** cookies with 90-day history
5. **Aligns** file timestamps forensically
6. **Restores** system time to present

**Duration**: Approximately 12-15 minutes

---

## Understanding the Output

You'll see colored output showing progress:

```
🔴 PROMETHEUS-CORE v2.0.0 - LEVEL 9 INITIALIZED
🔴 FINANCIAL OBLIVION MODE: ACTIVE

🔵 Initializing core components...
  ✓ Genesis Controller
  ✓ Isolation Manager
  ✓ Profile Orchestrator
  ✓ Forensic Alignment
  ...

🔵 [PHASE 0] ISOLATION
  • Disabling NTP synchronization...
  • Blocking NTP traffic...
  • Detecting hypervisor...

🔵 [PHASE 1] GENESIS
  • Shifting time to: 2024-10-15 15:30:45
  ✓ Time shifted successfully

...

🟢 OPERATION COMPLETED SUCCESSFULLY
🟢 Profile Path: profiles/profile_1234567890
🟢 Operation ID: op_1234567890
```

---

## Common Use Cases

### Use Case 1: Simple 30-Day Aging

```bash
python main.py --target https://example.com --age 30
```

**When to use**: Quick testing, short-term profiles

**Time required**: ~8 minutes

---

### Use Case 2: Full 90-Day with Forensics

```bash
python main.py --target https://example.com --age 90 --forensic --gamp
```

**When to use**: Production-like profiles with server-side validation

**Time required**: ~15 minutes

**Includes**:
- Complete timestamp alignment
- MFT scrubbing
- Google Analytics event injection

---

### Use Case 3: Multilogin Integration

First, configure Multilogin settings in `config/settings.yaml`:

```yaml
multilogin:
  browser_type: "multilogin"
  mla_port: 35000
  mla_profile_id: "your_profile_id"
  headless_mode: false
```

Then run:

```bash
python level9_operations.py --target stripe --age 90 --profile my_mla_profile
```

**When to use**: Integration with Multilogin antidetect browser

---

### Use Case 4: Verification Only

```bash
python main.py --verify
```

**When to use**: Check system compatibility before operations

**Time required**: ~2 minutes

Tests:
- Administrator privileges
- Python dependencies
- Browser availability
- System compatibility

---

## Configuration Quick Reference

Edit `config/settings.yaml` to customize behavior:

### Basic Settings

```yaml
temporal:
  target_age_days: 90        # How far back to age profile
  entropy_segments: 12       # Number of time segments (more = more realistic)
  poisson_lambda: 2.5       # Activity frequency (higher = more active)

browser:
  headless: false           # Set true for background operation
  anti_detect: true         # Keep true for detection evasion
```

### Advanced Settings

```yaml
safety:
  rollback_on_error: true   # Auto-restore on failure
  max_skew_seconds: 5       # Maximum acceptable time difference

forensic:
  enabled: true
  mft_scrubbing: true       # NTFS Master File Table cleaning
  timestomping: true        # File timestamp alignment
```

### Google Analytics (Optional)

For server-side validation:

```yaml
analytics:
  enabled: true
  measurement_id: "G-XXXXXXXXXX"
  api_secret: "your_api_secret"
```

Get these from Google Analytics → Admin → Data Streams → Measurement Protocol

---

## Troubleshooting

### Issue: "Administrator privileges required"

**Solution**:
```bash
# Close current terminal
# Right-click Command Prompt → "Run as administrator"
cd path\to\Aging-cookies-v2
python main.py --target https://example.com --age 90
```

---

### Issue: "Chrome installation not detected"

**Solution**:
1. Install Google Chrome from https://www.google.com/chrome/
2. Verify installation:
   ```bash
   # Check Chrome path
   dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
   ```

---

### Issue: "Failed to disable W32Time service"

**Solution**:
```bash
# Manual NTP service disable
net stop w32time
sc config w32time start=disabled
```

---

### Issue: "Operation timeout"

**Solution**:

Increase timeout in `config/settings.yaml`:

```yaml
execution:
  timeout_minutes: 45  # Increase from 30 to 45
```

---

### Issue: System time not restored

**Emergency Recovery**:
```bash
# Force time restoration
python -c "from core.safety import SafetyValidator; SafetyValidator().emergency_recovery()"

# Manual NTP sync
w32tm /resync /force
```

---

## Safety Tips

### Before Each Operation

✅ **Do This**:
- Create a system restore point
- Close all other applications
- Ensure stable power supply (laptop plugged in)
- Verify internet connection

❌ **Avoid This**:
- Running on production systems
- Operating without authorization
- Running multiple operations simultaneously
- Interrupting operations mid-execution

### After Each Operation

✅ **Verify**:
```bash
# Check system time is correct
python -c "from datetime import datetime; print(f'System time: {datetime.now()}')"

# Check NTP service
sc query w32time
```

---

## Next Steps

### Learn More

1. **Read the User Guide**: `USER_GUIDE.md`
   - Detailed usage instructions
   - Advanced features
   - API reference

2. **Technical Documentation**: `docs/TECHNICAL.md`
   - Architecture details
   - Module specifications
   - Performance metrics

3. **Security Considerations**: `docs/SECURITY.md`
   - Threat model
   - Best practices
   - Compliance guidelines

### Advanced Features

Once comfortable with basics:

- Custom entropy patterns
- Multilogin integration
- GAMP triangulation
- Forensic alignment
- Profile management

### Join the Community

- Report issues on GitHub
- Contribute improvements
- Share research findings
- Discuss security implications

---

## Quick Command Reference

```bash
# Basic Operations
python main.py --target URL --age DAYS          # Basic aging
python main.py --verify                         # System verification
python verify_implementation.py                 # Full verification

# Advanced Operations
python main.py --target URL --age 90 --gamp     # With GA tracking
python main.py --target URL --age 90 --forensic # With forensic alignment
python level9_operations.py --target stripe     # Level 9 operations

# Multilogin
python example_mla_integration.py               # MLA example script

# Testing
python main.py --test-detection                 # Test anti-detection
pytest tests/ -v                                # Run unit tests

# Configuration
python -c "from config.settings import Config; print(Config.EXECUTION_MODE)"
```

---

## Performance Expectations

| Operation | Time | CPU | Memory | Disk |
|-----------|------|-----|--------|------|
| 30-day aging | ~8 min | 40% | 1.5GB | 100MB |
| 90-day aging | ~15 min | 60% | 2GB | 200MB |
| 180-day aging | ~25 min | 60% | 2GB | 300MB |
| Verification | ~2 min | 10% | 500MB | 10MB |

---

## Getting Help

### Documentation Resources

- **README.md** - Project overview
- **USER_GUIDE.md** - Complete manual
- **docs/TECHNICAL.md** - Technical deep dive
- **docs/SECURITY.md** - Security considerations
- **MLA_INTEGRATION_GUIDE.md** - Multilogin setup

### Community Support

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and community help
- **Security Issues** - security@[repository-domain]

### Before Asking for Help

Please provide:
1. Error messages (full traceback)
2. System information (OS version, Python version)
3. Configuration used
4. Steps to reproduce
5. Logs from `logs/prometheus.log`

---

## Legal Reminder

⚖️ **This tool is for authorized security research only.**

- ✅ Obtain written authorization
- ✅ Operate in test environments
- ✅ Follow all applicable laws
- ✅ Respect ethical guidelines

- ❌ No unauthorized access
- ❌ No fraudulent activities
- ❌ No production systems
- ❌ No illegal activities

**You are responsible for ensuring legal compliance.**

---

## What's Next?

Now that you've completed your first operation:

1. **Review Results**: Check the generated profile in `profiles/`
2. **Examine Logs**: Review `logs/prometheus.log` for detailed execution logs
3. **Experiment**: Try different aging periods and configurations
4. **Learn Advanced Features**: Explore the full USER_GUIDE.md
5. **Contribute**: Share your findings and improvements

---

## Quick Start Checklist

- [ ] Cloned repository
- [ ] Installed dependencies
- [ ] Verified administrator access
- [ ] Ran verification tests
- [ ] Completed first operation
- [ ] Verified system time restored
- [ ] Reviewed generated profile
- [ ] Read user guide

**Congratulations!** You're now ready to use PROMETHEUS-CORE effectively.

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Feedback**: Open an issue on GitHub with suggestions
