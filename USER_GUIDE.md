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

**Version**: 2.0.0  
**Last Updated**: January 2025  
**License**: Research & Educational Use Only