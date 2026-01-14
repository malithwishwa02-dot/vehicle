# 📚 PROMETHEUS-CORE USER GUIDE
## Complete Manual for Aging-Cookies-v2 Implementation

---

## 🚀 Quick Start

### Prerequisites
- Windows 10/11 (Administrator privileges required)
- Python 3.10 or higher
- Google Chrome installed
- 8GB RAM minimum
- 10GB free disk space

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/malithwishwa02-dot/Aging-cookies-v2.git
cd Aging-cookies-v2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run as Administrator (Required!)
# Right-click Command Prompt > Run as administrator
```

---

## 📖 Table of Contents

1. [Basic Usage](#basic-usage)
2. [Configuration](#configuration)
3. [Advanced Features](#advanced-features)
4. [Security Considerations](#security-considerations)
5. [Troubleshooting](#troubleshooting)
6. [API Reference](#api-reference)

---

## 🎯 Basic Usage

### 1. Simple 90-Day Profile Aging

```bash
# Basic aging with default settings
python main.py --age 90

# With Google Analytics triangulation
python main.py --age 90 --gamp

# Full forensic alignment
python main.py --age 90 --forensic --gamp
```

### 2. Custom Time Periods

```bash
# 30-day aging
python main.py --age 30

# 180-day aging (6 months)
python main.py --age 180

# 365-day aging (1 year)
python main.py --age 365 --forensic
```

### 3. Profile Management

```bash
# Create named profile
python main.py --age 90 --profile business_profile

# Use existing profile
python main.py --validate-only --profile existing_profile

# Multiple profiles
python main.py --age 60 --profile profile_1
python main.py --age 90 --profile profile_2
```

---

## ⚙️ Configuration

### Edit `config/settings.yaml`:

```yaml
temporal:
  target_age_days: 90          # Default aging period
  entropy_segments: 12         # Time advancement segments
  poisson_lambda: 2.5         # Activity distribution
  
browser:
  profile_path: "profiles/chrome"
  headless: false             # Set true for background operation
  anti_detect: true           # Keep true for detection evasion
  
analytics:
  measurement_id: "G-XXXXXXXXXX"  # Your GA4 Measurement ID
  api_secret: "your_api_secret"   # GA4 API Secret
  
safety:
  time_api: "http://worldtimeapi.org/api/ip"
  max_skew_seconds: 5
  rollback_on_error: true
```

### Google Analytics Setup (Optional but Recommended)

1. Go to Google Analytics
2. Admin > Data Streams > Web Stream
3. Copy Measurement ID (G-XXXXXXXXXX)
4. Go to Measurement Protocol > Create API Secret
5. Add to `config/settings.yaml`

---

## 🔧 Advanced Features

### 1. Verification Mode

```bash
# Run full system verification
python verify_implementation.py

# Check specific profile
python main.py --validate-only --profile my_profile
```

### 2. Custom Entropy Patterns

```python
from core.entropy import EntropyGenerator

# Custom activity pattern
gen = EntropyGenerator({
    'poisson_lambda': 3.0,  # Higher activity
    'min_interval_hours': 1,
    'max_interval_hours': 72
})

segments = gen.generate_segments(90)
```

### 3. Browser Automation

```python
from core.profile import ProfileOrchestrator

# Launch browser with custom settings
orchestrator = ProfileOrchestrator({
    'headless': False,
    'window_size': [1920, 1080]
})

driver = orchestrator.launch_browser(
    anti_detect=True,
    profile_name='automated_profile'
)

# Custom actions
actions = [
    {'type': 'navigate', 'parameters': {'url': 'https://example.com'}},
    {'type': 'scroll', 'parameters': {'direction': 'down', 'amount': 500}},
    {'type': 'search', 'parameters': {'query': 'test search'}}
]

orchestrator.execute_actions(driver, actions)
```

### 4. Forensic Operations

```python
from core.forensic import ForensicAlignment

# Timestamp manipulation
forensic = ForensicAlignment()

# Stomp timestamps on directory
from datetime import datetime, timedelta
target_date = datetime.now() - timedelta(days=90)
forensic.stomp_timestamps(Path('profiles/chrome'), target_date)

# MFT scrubbing
forensic.scrub_mft(Path('profiles/chrome'))
```

---

## 🛡️ Security Considerations

### ⚠️ IMPORTANT WARNINGS

1. **Legal Compliance**
   - This tool is for security research and authorized testing only
   - Ensure compliance with all applicable laws
   - Obtain proper authorization before use

2. **System Safety**
   - Always run verification first: `python verify_implementation.py`
   - Keep `rollback_on_error: true` in settings
   - Monitor system time after operations

3. **Operational Security**
   - Use dedicated testing environment
   - Avoid production systems
   - Keep logs encrypted
   - Clear artifacts after testing

### Best Practices

```bash
# 1. Always verify before operations
python verify_implementation.py

# 2. Test with short duration first
python main.py --age 7 --profile test_profile

# 3. Use validation mode
python main.py --validate-only --profile test_profile

# 4. Clean up after testing
rm -rf profiles/test_profile
rm -rf logs/*.log
```

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Administrator Privileges Error
```
Error: Administrator privileges required
```
**Solution**: Run Command Prompt as Administrator

#### 2. Chrome Not Found
```
Error: Chrome installation not detected
```
**Solution**: Install Google Chrome from https://www.google.com/chrome/

#### 3. NTP Service Issues
```
Error: Failed to disable W32Time service
```
**Solution**: 
```bash
# Manual disable
net stop w32time
sc config w32time start= disabled
```

#### 4. Time Synchronization Failed
```
Error: Clock skew detected > 5 seconds
```
**Solution**:
```bash
# Force resync
w32tm /resync /force
```

#### 5. Profile Corruption
```
Error: Profile validation failed
```
**Solution**:
```bash
# Delete and recreate
rm -rf profiles/corrupted_profile
python main.py --age 90 --profile new_profile
```

### Debug Mode

```bash
# Enable verbose logging
python main.py --age 90 --debug

# Check logs
tail -f logs/prometheus.log
```

---

## 📚 API Reference

### Main Functions

#### `PrometheusCore.execute_pipeline()`
```python
execute_pipeline(
    age_days: int = 90,
    enable_gamp: bool = True,
    forensic_mode: bool = True
) -> bool
```

#### `ProfileOrchestrator.launch_browser()`
```python
launch_browser(
    headless: bool = False,
    anti_detect: bool = True,
    profile_name: str = 'default'
) -> WebDriver
```

#### `GenesisController.shift_time()`
```python
shift_time(
    target_datetime: datetime
) -> bool
```

#### `GAMPTriangulation.send_event()`
```python
send_event(
    client_id: str,
    timestamp: datetime,
    event_name: str = "page_view",
    event_params: dict = None
) -> bool
```

### Verification Functions

#### `ImplementationVerifier.run_full_verification()`
```python
verifier = ImplementationVerifier()
results = verifier.run_full_verification()
# Returns dict with all test results
```

#### `AntiDetectionSuite.verify_detection_bypass()`
```python
anti_detect = AntiDetectionSuite()
results = anti_detect.verify_detection_bypass(driver)
# Returns detection score 0-100%
```

---

## 📊 Performance Optimization

### Recommended Settings for Different Use Cases

#### Fast Testing (5-10 minutes)
```yaml
temporal:
  entropy_segments: 6
  poisson_lambda: 1.5
browser:
  headless: true
```

#### Standard Operation (12-15 minutes)
```yaml
temporal:
  entropy_segments: 12
  poisson_lambda: 2.5
browser:
  headless: false
```

#### Maximum Realism (20-30 minutes)
```yaml
temporal:
  entropy_segments: 24
  poisson_lambda: 3.0
browser:
  headless: false
  anti_detect: true
```

---

## 🚨 Emergency Procedures

### System Time Recovery

If system time becomes corrupted:

```bash
# 1. Emergency restore
python -c "from core.safety import SafetyValidator; SafetyValidator().emergency_recovery()"

# 2. Manual restore
w32tm /resync /force
net start w32time
```

### Complete Reset

```bash
# 1. Stop all processes
taskkill /F /IM chrome.exe
taskkill /F /IM python.exe

# 2. Reset services
sc config w32time start= auto
net start w32time

# 3. Clear firewall rules
netsh advfirewall firewall delete rule name="PROMETHEUS_Block_NTP_Out"
netsh advfirewall firewall delete rule name="PROMETHEUS_Block_NTP_In"

# 4. Sync time
w32tm /resync /force
```

---

## 📈 Monitoring & Logs

### Log Locations

```
logs/
├── prometheus.log       # Main application log
├── genesis.log         # Time manipulation log
├── profile.log         # Browser operations
└── forensic.log        # Timestomping operations
```

### Log Analysis

```bash
# View errors only
grep ERROR logs/prometheus.log

# View time shifts
grep "shifted to" logs/genesis.log

# Check detection bypass
grep "bypass" logs/prometheus.log
```

---

## 🔄 Updates & Maintenance

### Keep Updated

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Verify after update
python verify_implementation.py
```

---

## 💡 Tips & Tricks

1. **Start Small**: Test with 7-day aging before attempting 90+ days
2. **Use Profiles**: Create separate profiles for different purposes
3. **Monitor Resources**: Check CPU/RAM usage during operations
4. **Backup Profiles**: Save successful profiles before modifications
5. **Document Settings**: Keep notes on successful configurations

---

## 📞 Support

- **Repository**: https://github.com/malithwishwa02-dot/Aging-cookies-v2
- **Issues**: Report bugs via GitHub Issues
- **Updates**: Watch repository for updates

---

## ⚖️ Legal Disclaimer

This software is provided for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations. The developers assume no liability for misuse or damage caused by this software.

---

## ❓ Frequently Asked Questions (FAQ)

### General Questions

#### Q: What is PROMETHEUS-CORE?

A: PROMETHEUS-CORE is a temporal manipulation framework for security research that implements Method 4 (Time-Shifted Cookie Injection). It creates forensically-aged browser profiles by manipulating system time, generating realistic browsing behavior, and aligning all timestamps.

#### Q: Is this legal?

A: PROMETHEUS-CORE is a security research tool. It is **legal** when used for:
- Authorized penetration testing
- Security research with permission
- Educational purposes
- Testing your own systems

It is **illegal** when used for:
- Unauthorized access to systems
- Fraud or deception
- Identity theft
- Any criminal activity

**Always obtain written authorization before use.**

#### Q: Why does it require administrator privileges?

A: Administrator privileges are required to:
- Modify system time via Win32 APIs
- Disable Windows Time service
- Configure firewall rules
- Access low-level file system operations (MFT)
- Modify registry settings

#### Q: Can I run this on Linux or macOS?

A: Currently, **No**. PROMETHEUS-CORE is Windows-only because:
- Uses Windows-specific Win32 APIs for time manipulation
- Relies on NTFS filesystem for forensic operations
- Uses Windows service management

**Future versions** may support Linux using `clock_settime()` system calls.

#### Q: Will this harm my system?

A: When used correctly, **No**. The framework includes:
- Automatic rollback on errors
- Emergency recovery procedures
- System state validation
- Safe restoration mechanisms

**However**, always operate in a test environment, not production systems.

---

### Technical Questions

#### Q: How does time manipulation work?

A: PROMETHEUS-CORE uses the Windows `SetSystemTime()` API to modify the system clock at the kernel level. Before doing this, it:

1. Disables NTP synchronization
2. Blocks NTP traffic via firewall
3. Detects and disables VM time sync
4. Shifts time to target date
5. Performs operations
6. Restores time using WorldTimeAPI

#### Q: Can detection systems identify this?

A: **Some can**. Detection methods include:

**Detectable by**:
- TPM (Trusted Platform Module) time validation
- Volume Shadow Copy analysis
- NTFS transaction log forensics
- Advanced ML-based behavioral analysis
- Real-time security monitoring

**Not easily detectable by**:
- Standard browser fingerprinting
- Basic timestamp analysis
- Simple behavioral checks
- Cookie age validation

**Mitigation**: The framework implements multiple evasion techniques but cannot guarantee 100% undetectability.

#### Q: What is GAMP Triangulation?

A: GAMP (Google Analytics Measurement Protocol) Triangulation creates server-side validation of the aged profile by:

1. Sending backdated events to Google Analytics
2. Creating a historical activity trail
3. Providing external timestamp validation
4. Making the profile appear in GA4 reports

This adds credibility because GA4 is a trusted third-party with its own timestamps.

#### Q: What is MFT scrubbing?

A: MFT (Master File Table) scrubbing is an advanced forensic technique:

- **Purpose**: Remove traces of timestamp manipulation from NTFS metadata
- **Method**: Cross-volume copy operation to get new MFT entries
- **Effectiveness**: Highly effective against standard forensics
- **Limitations**: Cannot hide from $LogFile analysis or VSS

#### Q: How realistic is the human behavior simulation?

A: Very realistic. The entropy generator uses:

- **Bezier curves** for natural mouse movements
- **Poisson distribution** for realistic timing
- **Variable typing speeds** (40-80 WPM)
- **Natural scrolling patterns**
- **Random hesitations and pauses**
- **Occasional "mistakes"**

Tested against multiple bot detection systems with high success rates.

---

### Usage Questions

#### Q: What should I set the age to?

**Recommendations**:

- **7-30 days**: Quick testing, low-trust scenarios
- **60-90 days**: Standard operations, medium-trust
- **180-365 days**: High-trust scenarios, maximum aging

**Considerations**:
- Longer ages take more time to process
- Very old profiles may trigger different detection logic
- Balance between trust and practical execution time

#### Q: Should I use headless mode?

**Headless: false** (visible browser):
- ✅ More realistic fingerprint
- ✅ Easier to debug
- ✅ Better for manual intervention
- ❌ Slower execution
- ❌ Requires active desktop

**Headless: true** (background):
- ✅ Faster execution
- ✅ Works without display
- ✅ Lower resource usage
- ❌ More detectable
- ❌ Missing some browser features

**Recommendation**: Use headless:false for production operations, headless:true for testing.

#### Q: How often can I reuse a profile?

**Limited reuse recommended**:

- **Same target**: 2-3 times maximum
- **Different targets**: Not recommended
- **Time between reuses**: Wait 24-48 hours

**Why**: Repeated use can create patterns that detection systems may identify.

**Best practice**: Generate fresh profiles for each operation.

#### Q: Can I age multiple profiles simultaneously?

**Not recommended**. Running multiple operations simultaneously:

- Creates system resource conflicts
- Interferes with time manipulation
- Causes unpredictable NTP service state
- May corrupt profiles

**Best practice**: Run operations sequentially, one at a time.

---

### Troubleshooting Questions

#### Q: Operation failed partway through - what do I do?

**Immediate steps**:

```bash
# 1. Run emergency recovery
python -c "from core.safety import SafetyValidator; SafetyValidator().emergency_recovery()"

# 2. Check system time
python -c "from datetime import datetime; print(datetime.now())"

# 3. Verify NTP service
sc query w32time
```

**Investigation**:

```bash
# Check error logs
grep ERROR logs/prometheus.log | tail -20

# Review operation results
cat operations/operation_*.json
```

**Retry**: After fixing the issue, you can retry the operation.

#### Q: System time didn't restore properly - help!

**Manual restoration**:

```bash
# 1. Re-enable NTP service
sc config w32time start=auto
net start w32time

# 2. Force synchronization
w32tm /resync /force

# 3. Verify time
w32tm /query /status

# 4. If still wrong, sync with specific server
w32tm /config /manualpeerlist:"time.windows.com" /syncfromflags:manual /update
w32tm /resync
```

#### Q: Chrome keeps crashing during operation

**Common causes and solutions**:

1. **Insufficient resources**:
   ```yaml
   # Reduce concurrent operations in config/settings.yaml
   temporal:
     entropy_segments: 6  # Reduce from 12
   ```

2. **Chrome profile corruption**:
   ```bash
   # Delete corrupted profiles
   rm -rf profiles/profile_*
   ```

3. **ChromeDriver mismatch**:
   ```bash
   # Update undetected-chromedriver
   pip install --upgrade undetected-chromedriver
   ```

#### Q: Getting "Permission Denied" errors on files

**Solutions**:

```bash
# 1. Close Chrome completely
taskkill /F /IM chrome.exe

# 2. Ensure running as admin
# Right-click terminal → "Run as administrator"

# 3. Check file locks
# Use Process Explorer to identify locked files

# 4. Reboot if persistent
shutdown /r /t 0
```

#### Q: Network connection errors during operation

**Check internet connectivity**:

```bash
# Test basic connectivity
ping 8.8.8.8

# Test DNS resolution
nslookup google.com

# Test HTTPS
curl https://www.google.com
```

**Check firewall rules**:

```bash
# List PROMETHEUS rules
netsh advfirewall firewall show rule name=all | findstr PROMETHEUS

# Temporarily disable (for testing only)
netsh advfirewall set allprofiles state off
```

---

### Configuration Questions

#### Q: What entropy_segments value should I use?

**Impact of entropy_segments**:

- **6 segments**: Fast (~8-10 min), less realistic
- **12 segments**: Balanced (~12-15 min), good realism  
- **24 segments**: Slow (~20-25 min), maximum realism

**Recommendation**: Start with 12, adjust based on needs.

#### Q: What is poisson_lambda?

**Poisson lambda (λ)** controls activity frequency:

- **λ = 1.5**: Low activity (occasional user)
- **λ = 2.5**: Normal activity (regular user) - **recommended**
- **λ = 4.0**: High activity (power user)

Higher values create more events but may trigger rate limiting.

#### Q: Should I enable all features?

**Recommended configuration**:

```yaml
# For production operations
execution:
  mode: "GENERATE_ONLY"

forensic:
  enabled: true          # Yes - important for timestamp alignment
  mft_scrubbing: true   # Yes - adds forensic depth
  timestomping: true    # Yes - essential

analytics:
  enabled: true          # Optional - adds server-side validation

multilogin:
  enabled: false         # Only if using Multilogin
```

**For testing**:

```yaml
forensic:
  enabled: false         # Faster execution
  
analytics:
  enabled: false         # Not needed for testing
```

---

### Advanced Questions

#### Q: Can I customize the browsing behavior?

**Yes!** Edit the entropy generator:

```python
# Custom behavior script
from core.entropy import EntropyGenerator

generator = EntropyGenerator({
    'mouse_speed': 'fast',      # 'slow', 'medium', 'fast'
    'scroll_style': 'reader',   # 'skimmer', 'reader', 'scanner'
    'typing_speed': 65,         # WPM
    'pause_frequency': 0.3      # 0.0-1.0
})
```

#### Q: How do I integrate with Multilogin?

See the complete **MLA_INTEGRATION_GUIDE.md** for detailed instructions.

Quick setup:

1. Install and launch Multilogin
2. Configure in `config/settings.yaml`:
   ```yaml
   multilogin:
     browser_type: "multilogin"
     mla_port: 35000
     mla_profile_id: "your_profile_id"
   ```
3. Run: `python level9_operations.py --target stripe --age 90`

#### Q: Can I export profiles to other tools?

**Yes**, profiles can be exported to:

- **Multilogin**: Built-in export functionality
- **GoLogin**: Manual cookie import
- **AdsPower**: Manual cookie import
- **Standard Chrome**: Direct profile copy

```python
# Export cookies in standard format
from core.profile import ProfileOrchestrator

orchestrator = ProfileOrchestrator()
orchestrator.export_cookies(
    profile_path="profiles/profile_123",
    output_format="netscape"  # or "json"
)
```

#### Q: How do I add custom targets?

**Method 1**: Command line

```bash
python main.py --target https://your-custom-site.com --age 90
```

**Method 2**: Configuration file

```yaml
# config/settings.yaml
targets:
  - name: "custom_site"
    url: "https://your-custom-site.com"
    age_days: 90
    profile_name: "custom_profile"
```

#### Q: Can I schedule automated operations?

**Yes**, using Windows Task Scheduler:

```bash
# Create scheduled task
schtasks /create /tn "PROMETHEUS_Daily" /tr "C:\path\to\python.exe C:\path\to\main.py --target https://example.com --age 90" /sc daily /st 02:00 /ru "SYSTEM"
```

**Important**: Ensure proper error handling and logging for unattended operations.

---

### Performance Questions

#### Q: Why is my operation taking longer than expected?

**Common causes**:

1. **Slow internet**: Profile creation downloads resources
2. **High entropy_segments**: More segments = more time
3. **Resource constraints**: Low RAM/CPU
4. **Antivirus interference**: Security software scanning
5. **Chrome updates**: Automatic updates during operation

**Optimization**:

```yaml
# Faster configuration
temporal:
  entropy_segments: 6     # Reduce from 12

browser:
  headless: true          # Faster than visible
  
forensic:
  mft_scrubbing: false    # Skip if not needed
```

#### Q: How can I monitor progress?

**Real-time monitoring**:

```bash
# Terminal 1: Run operation
python main.py --target https://example.com --age 90

# Terminal 2: Watch logs
tail -f logs/prometheus.log

# Terminal 3: Monitor resources
# Windows: Task Manager
# Or use: python -c "import psutil; print(psutil.cpu_percent(), psutil.virtual_memory().percent)"
```

#### Q: Can I pause and resume operations?

**No**, operations cannot be paused safely because:

- System time would be inconsistent
- Browser state cannot be reliably saved
- NTP isolation must be maintained

**Workaround**: Use shorter aging periods and combine profiles.

---

## 📞 Additional Support

### Documentation Index

1. **QUICKSTART.md** - Get started in 10 minutes
2. **USER_GUIDE.md** - This document
3. **docs/TECHNICAL.md** - Architecture and implementation details
4. **docs/SECURITY.md** - Security considerations and best practices
5. **MLA_INTEGRATION_GUIDE.md** - Multilogin integration guide
6. **README.md** - Project overview and quick reference

### Community Resources

- **GitHub Issues**: https://github.com/malithwishwa02-dot/Aging-cookies-v2/issues
- **GitHub Discussions**: https://github.com/malithwishwa02-dot/Aging-cookies-v2/discussions
- **Security Reports**: security@[repository-domain]

### When Reporting Issues

Please include:

```bash
# System information
python --version
wmic os get caption, version

# Dependency versions
pip list | findstr -i "selenium chrome pywin32"

# Error logs (last 50 lines)
tail -50 logs/prometheus.log

# Configuration (remove sensitive data)
cat config/settings.yaml
```

---

**Version**: 2.0.0  
**Last Updated**: January 2025  
**License**: Research & Educational Use Only