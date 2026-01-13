# QUICK AUDIT PROMPT - PROMETHEUS-CORE METHOD 4

## CONCISE VERSION FOR IMMEDIATE CODE GENERATION

Copy and paste this prompt into your AI coding assistant:

---

**PROMPT:**

I need a forensic audit of my 'Aging-cookies-v2' repository against the PROMETHEUS-CORE 'Method 4: Time-Shifted Cookie Injection' specification.

**Already Implemented:**
- W32Time service shutdown
- NTP firewall rules
- Basic kernel time shifting
- Browser automation with undetected_chromedriver
- Basic MFT scrubbing with shutil.move

**MISSING CRITICAL COMPONENTS - Generate Python code for:**

1. **Admin Privilege Check** - `ctypes.windll.shell32.IsUserAnAdmin()`
2. **Registry NTP Disable** - Set `HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters` Type='NoSync'
3. **SYSTEMTIME Structure** - Complete ctypes structure for SetSystemTime
4. **Poisson Distribution Entropy** - Replace uniform random with Poisson intervals
5. **GAMP Server Triangulation** - Google Analytics Measurement Protocol with timestamp_micros
6. **72-Hour Rolling Window** - Manage GAMP backdating limit
7. **WorldTimeAPI Validation** - Check clock sync before/after operations
8. **Millisecond Timestomping** - Use SetFileTime with FILETIME structure
9. **Browser Entropy Enhancement** - Mouse jitter, scroll patterns, tab switching
10. **Complete Error Handling** - Try/except/finally with full system restoration

**DELIVERABLES:**
Generate these Python files with production-ready code:
- `main.py` - Complete orchestration
- `core/server_side.py` - GAMP implementation
- `core/safety.py` - Time validation & recovery
- `core/entropy.py` - Advanced browser automation

No explanations needed. Just provide the working Python code that fills these gaps.

---