# 🎯 PROMETHEUS-CORE QUICK REFERENCE
## Essential Commands & Operations

---

## ⚡ Most Common Commands

```bash
# Standard 90-day aging
python main.py --age 90 --gamp --forensic

# Quick 30-day test
python main.py --age 30

# Verify system
python verify_implementation.py

# Validate profile
python main.py --validate-only --profile myprofile
```

---

## 🛠️ Pre-Flight Checklist

- [ ] Running as Administrator
- [ ] Chrome installed
- [ ] Python 3.10+
- [ ] All dependencies installed
- [ ] System time synced
- [ ] 10GB free space

---

## 🚀 Quick Operations

### Create Aged Profile
```bash
python main.py --age 90 --profile business
```

### Enable All Features
```bash
python main.py --age 90 --gamp --forensic --profile premium
```

### Headless Mode (Background)
```bash
# Edit config/settings.yaml
browser:
  headless: true
  
# Then run
python main.py --age 90
```

---

## ⚠️ Emergency Commands

### Fix Time Issues
```bash
w32tm /resync /force
net start w32time
```

### Reset Everything
```bash
sc config w32time start= auto
net start w32time
netsh advfirewall firewall delete rule name=all
```

### Verify Detection Bypass
```bash
python verify_implementation.py | grep "Anti-Detection Score"
```

---

## 📊 Status Checks

### Check Logs
```bash
# View latest activity
tail -n 50 logs/prometheus.log

# Check for errors
grep ERROR logs/*.log

# Monitor progress
grep "complete" logs/prometheus.log
```

---

## 🔧 Configuration Quick Edit

### Faster Processing
```yaml
# config/settings.yaml
temporal:
  entropy_segments: 6  # Reduce from 12
browser:
  headless: true      # No GUI
```

### Maximum Stealth
```yaml
temporal:
  entropy_segments: 24  # Increase segments
  poisson_lambda: 3.0   # More variation
browser:
  anti_detect: true     # Always on
  headless: false       # Show browser
```

---

## 🎮 Keyboard Shortcuts

While script is running:
- `Ctrl+C` - Graceful stop (triggers rollback)
- Check `logs/` for progress
- DO NOT close terminal abruptly

---

## 📈 Success Indicators

✅ **Good Signs:**
- "Pipeline Complete" in logs
- "Anti-Detection Score: 100%"
- "MFT scrub complete"
- "Time sync validated"

❌ **Warning Signs:**
- "Clock skew detected"
- "Temporal paradox found"
- "Admin privileges required"
- "NTP sync failed"

---

## 💾 Backup & Restore

### Backup Profile
```bash
# Windows
xcopy /E /I profiles\myprofile backup\myprofile

# Or use tar
tar -czf profile_backup.tar.gz profiles/myprofile
```

### Restore Profile
```bash
# Windows
xcopy /E /I backup\myprofile profiles\myprofile

# Or from tar
tar -xzf profile_backup.tar.gz
```

---

## 🔍 Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| "Not admin" | Right-click CMD > Run as Admin |
| "Chrome not found" | Install Chrome or check path |
| "Time sync error" | Run `w32tm /resync /force` |
| "Profile corrupt" | Delete profile, recreate |
| "Module not found" | Run `pip install -r requirements.txt` |

---

## 📞 Getting Help

1. Check `USER_GUIDE.md` for detailed instructions
2. Run `python verify_implementation.py` for diagnostics
3. Check logs in `logs/` directory
4. Review `FINAL_VALIDATION.md` for capabilities

---

**Remember**: Always run as Administrator!