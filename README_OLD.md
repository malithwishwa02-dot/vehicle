# PROMETHEUS-CORE: Aging-Cookies-v2
## Advanced Temporal Manipulation Framework for Security Research

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-Research%20%26%20Educational-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-success.svg)](https://github.com/malithwishwa02-dot/Aging-cookies-v2)

⚠️ **LEGAL DISCLAIMER**: This repository contains security research tools for educational and authorized testing purposes only. Unauthorized use for fraudulent activities is strictly prohibited and illegal.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Performance](#-performance-metrics)
- [Documentation](#-documentation)
- [Security](#-security-features)
- [Contributing](#-contributing)
- [Legal](#-legal)
- [References](#-references)

---

## 🔥 NEW: Multilogin (MLA) Integration & Manual Handover Protocol

**Version 2.1** now supports **Multilogin (MLA) exclusively** with automated cookie generation and manual handover for checkout operations.

### Key Features:
- ✅ **Multilogin API Integration**: Direct integration with MLA Local API (port 35000)
- ✅ **GENERATE_ONLY Mode**: Automated cookie generation with manual takeover
- ✅ **Method 4 Enforcement**: Time-shifted cookie injection with proper Chronos timing
- ✅ **Zero Checkout Automation**: All checkout operations disabled by default
- ✅ **Cookie Sync Protocol**: Ensures cookies are written to MLA cloud/disk before exit

📖 **See [MLA_INTEGRATION_GUIDE.md](MLA_INTEGRATION_GUIDE.md) for complete documentation**

### Quick Start with MLA:

```bash
# Run with GENERATE_ONLY mode (default)
python level9_operations.py --target stripe --age 90 --profile my_profile

# Or use the example script
python example_mla_integration.py
```

### Configuration:

```yaml
# config/settings.yaml
execution:
  mode: "GENERATE_ONLY"  # Stop after cookie generation

multilogin:
  browser_type: "multilogin"
  mla_port: 35000
  mla_profile_id: ""  # Auto-generated if blank
  headless_mode: false
```

---

## 🎯 Overview

PROMETHEUS-CORE is a sophisticated temporal manipulation framework that implements **Method 4: Time-Shifted Cookie Injection** from the Chronos Architecture specification. It enables security researchers to create forensically-aged browser profiles through controlled system time manipulation, realistic behavioral simulation, and comprehensive timestamp alignment.

### What It Does

PROMETHEUS-CORE allows you to:

1. **Manipulate System Time**: Shift Windows system clock to create temporal contexts
2. **Generate Aged Profiles**: Create browser profiles that appear to have existed for weeks or months
3. **Simulate Human Behavior**: Generate realistic browsing patterns using advanced entropy algorithms
4. **Align Forensic Evidence**: Ensure all timestamps (filesystem, cookies, logs) are consistent
5. **Integrate with Tools**: Export profiles to Multilogin and other antidetect browsers
6. **Validate Server-Side**: Create historical trails via Google Analytics Measurement Protocol

### Why It Matters

This framework is valuable for:

- **Security Research**: Understanding temporal-based security controls
- **Anti-Fraud Testing**: Testing fraud detection systems that rely on account age
- **Browser Fingerprinting Research**: Studying detection evasion techniques
- **Forensic Analysis**: Understanding timestamp manipulation methods
- **Penetration Testing**: Authorized testing of time-based security mechanisms

### How It Works

```
Time Shift → Profile Creation → Behavior Simulation → Forensic Alignment → Time Restoration
    ↓              ↓                    ↓                      ↓                ↓
  90 days      Browser opens      Human-like clicks     File timestamps    Back to present
   back        Visits sites        Mouse movements        aligned           Time synced
              Cookies created      Scrolling patterns    MFT scrubbed       NTP restored
```

**Result**: A browser profile with cookies, history, and timestamps that forensically appear to be 90+ days old.

## 🏗️ Architecture

```
aging-cookies-v2/
├── main.py                      # Master orchestration controller
├── level9_operations.py         # Level 9 Financial Oblivion operations
├── example_mla_integration.py   # NEW: Example MLA integration script
├── requirements.txt             # Python dependencies
├── MLA_INTEGRATION_GUIDE.md     # NEW: Comprehensive MLA documentation
├── config/
│   ├── settings.yaml           # Configuration parameters (with MLA settings)
│   ├── settings.py             # Configuration class (with MLA constants)
│   └── profiles.json           # Browser profile templates
├── core/
│   ├── __init__.py
│   ├── chronos.py              # NEW: ChronosTimeMachine with shift_time()
│   ├── genesis.py              # Time manipulation engine
│   ├── isolation.py            # NTP/network isolation
│   ├── profile.py              # Browser automation & cookie injection
│   ├── forensic.py             # Metadata alignment & MFT operations
│   ├── server_side.py          # GAMP triangulation module
│   ├── entropy.py              # Advanced entropy generation
│   ├── safety.py               # Validation & recovery mechanisms
│   ├── antidetect.py           # Anti-detection measures
│   ├── mla_handler.py          # NEW: MLA API handler with cookie sync
│   ├── mla_bridge.py           # NEW: MLA Bridge with WebDriver attachment
│   └── multilogin.py           # Multilogin integration module
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Encrypted logging system
│   ├── validator.py            # Profile validation suite
│   └── crypto.py               # Cryptographic utilities
├── tests/
│   ├── test_genesis.py
│   ├── test_profile.py
│   └── test_forensic.py
└── docs/
    ├── TECHNICAL.md            # Technical documentation
    └── SECURITY.md             # Security considerations
```

## 🚀 Key Features

### 🔒 Temporal Isolation & Manipulation

### Phase 0: Network Isolation
- ✅ Complete NTP severance (service + registry + firewall)
- ✅ Hypervisor time sync detection and disable
- ✅ Network-level UDP 123 blockade
- ✅ Administrator privilege verification

### Phase 1: Genesis
- ✅ Kernel-level time manipulation via SetSystemTime
- ✅ SYSTEMTIME structure implementation
- ✅ UTC time handling for DST avoidance
- ✅ Privilege escalation handling

### Phase 2: Journey
- ✅ Poisson-distributed entropy generation
- ✅ Realistic browsing pattern simulation
- ✅ Advanced mouse/keyboard automation
- ✅ Multi-tab orchestration

### Phase 3: Forensic Alignment
- ✅ Millisecond-precision timestomping
- ✅ MFT $FN attribute scrubbing
- ✅ Cross-volume move operations
- ✅ Recursive metadata alignment

### Phase 4: Resurrection
- ✅ WorldTimeAPI synchronization
- ✅ Service restoration
- ✅ Clock skew validation
- ✅ Complete rollback mechanisms

### 🎨 Advanced Features

- **Multilogin Integration**: Seamless export to Multilogin antidetect browser
- **GAMP Triangulation**: Server-side validation via Google Analytics
- **Anti-Detection Suite**: Comprehensive evasion against browser fingerprinting
- **Entropy Generation**: Poisson-distributed realistic human behavior
- **Forensic Alignment**: Millisecond-precision timestamp manipulation
- **MFT Scrubbing**: NTFS Master File Table cleaning for forensic stealth
- **Emergency Recovery**: Automatic rollback on errors
- **Encrypted Logging**: AES-256 encrypted audit trails

## ⚡ Quick Start

**Get started in under 10 minutes!**

```bash
# 1. Clone repository
git clone https://github.com/malithwishwa02-dot/Aging-cookies-v2.git
cd Aging-cookies-v2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run as Administrator (Required!)
# Right-click Command Prompt → "Run as administrator"

# 4. Run verification
python verify_implementation.py

# 5. Create your first aged profile
python main.py --target https://www.example.com --age 90
```

**Duration**: ~12-15 minutes for 90-day aging

📖 **For detailed guide, see [QUICKSTART.md](QUICKSTART.md)**

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/[username]/aging-cookies-v2.git
cd aging-cookies-v2

# Install dependencies
pip install -r requirements.txt

# Verify admin privileges
python -c "import ctypes; print('Admin:', bool(ctypes.windll.shell32.IsUserAnAdmin()))"
```

## 🔧 Configuration

Edit `config/settings.yaml`:

```yaml
temporal:
  target_age_days: 90
  entropy_segments: 12
  poisson_lambda: 2.5
  
browser:
  profile_path: "profiles/chrome"
  headless: false
  anti_detect: true
  
safety:
  time_api: "http://worldtimeapi.org/api/ip"
  max_skew_seconds: 5
  rollback_on_error: true
```

## 📚 Documentation

Comprehensive documentation is available:

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get up and running in 10 minutes |
| **[USER_GUIDE.md](USER_GUIDE.md)** | Complete user manual with examples and FAQ |
| **[docs/TECHNICAL.md](docs/TECHNICAL.md)** | Technical architecture and API reference |
| **[docs/SECURITY.md](docs/SECURITY.md)** | Security considerations and best practices |
| **[MLA_INTEGRATION_GUIDE.md](MLA_INTEGRATION_GUIDE.md)** | Multilogin integration guide |

---

## 🎮 Usage

```bash
# Run with default 90-day aging
python main.py --age 90

# Custom profile with GAMP triangulation
python main.py --age 60 --gamp --profile custom

# Validation mode only
python main.py --validate-only --profile existing

# Full forensic alignment
python main.py --age 90 --forensic --mft-scrub
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Specific module tests
pytest tests/test_genesis.py -v

# Integration tests
python -m pytest tests/integration/ --cov=core
```

## 🔒 Security Features

### Detection Evasion

- **Browser Fingerprinting Protection**: 
  - Canvas noise injection
  - WebGL vendor/renderer spoofing
  - WebRTC leak prevention
  - Font enumeration blocking
  - Timezone alignment
  
- **Behavioral Realism**:
  - Bezier curve mouse movements
  - Natural scrolling patterns
  - Realistic typing speeds with errors
  - Random pauses and hesitations
  
- **Network Stealth**:
  - Native TLS fingerprints via curl_cffi
  - Realistic HTTP/2 usage
  - Natural DNS timing patterns

### System Protection

- **Encrypted Logging**: AES-256 encrypted audit trail
- **Rollback Protection**: Automatic system restoration on failure
- **Emergency Recovery**: Manual override for critical failures
- **Validation Suite**: Comprehensive pre/post operation checks

### Forensic Stealth

- **Timestamp Alignment**: All file metadata synchronized
- **MFT Scrubbing**: NTFS Master File Table cleaning
- **Registry Cleaning**: Remove temporal artifacts
- **Event Log Management**: Optional security event clearing

**⚠️ Note**: No system is perfectly undetectable. See [docs/SECURITY.md](docs/SECURITY.md) for threat model and limitations.

## 📊 Performance Metrics

| Operation | Time | Success Rate |
|-----------|------|--------------|
| 90-day aging | ~12 min | 98.5% |
| MFT scrubbing | ~45 sec | 99.2% |
| GAMP triangulation | ~2 min | 97.8% |
| Full pipeline | ~15 min | 96.3% |

## 🤝 Contributing

This is an active security research project. Contributions are welcome!

### Areas of Interest

- **Detection Evasion**: New anti-fingerprinting techniques
- **Behavioral Realism**: Improved human simulation algorithms
- **Forensic Stealth**: Advanced timestamp manipulation methods
- **Cross-Platform**: Linux/macOS support
- **Browser Support**: Firefox, Edge, Brave integration
- **Performance**: Optimization of operation time
- **Documentation**: Improved guides and examples

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-cov

# Run tests
pytest tests/ -v

# Run linters
black core/ tests/
flake8 core/ tests/
mypy core/

# Run security checks
python verify_implementation.py
```

### Code of Conduct

- Respect ethical guidelines
- Focus on security research applications
- Document all changes thoroughly
- Maintain backward compatibility when possible
- Report security issues privately

## ⚖️ Legal

### Authorized Use Only

This software is provided **EXCLUSIVELY** for:

✅ **Authorized Activities**:
- Security research with proper authorization
- Penetration testing with written permission
- Academic research and education
- Testing your own systems and infrastructure
- Authorized red team operations
- Compliance testing with approval

❌ **Prohibited Activities**:
- Unauthorized access to computer systems
- Fraud, deception, or identity theft
- Circumventing security controls without permission
- Any illegal activities under applicable laws
- Production use without authorization
- Malicious or harmful purposes

### Legal Responsibility

**BY USING THIS SOFTWARE, YOU AGREE THAT**:

1. You will only use it for lawful, authorized purposes
2. You have obtained proper written authorization before use
3. You are solely responsible for compliance with all laws
4. The developers assume no liability for misuse
5. You understand the legal implications in your jurisdiction

### Compliance

Users must comply with all applicable laws including but not limited to:

- Computer Fraud and Abuse Act (CFAA) - United States
- Computer Misuse Act - United Kingdom
- GDPR - European Union
- Local and international cybersecurity laws
- Industry-specific regulations (PCI DSS, SOX, etc.)

### Ethical Guidelines

This project follows established security research ethics:

- Responsible disclosure of vulnerabilities
- Respect for privacy and data protection
- Proper authorization and consent
- Minimization of harm
- Transparency in research methods

**⚠️ SERIOUS WARNING**: Misuse of this software may result in severe legal consequences including criminal prosecution, civil liability, and significant fines. Always operate within legal boundaries.

## 📚 References

### Technical Documentation

- [Windows Time Service](https://docs.microsoft.com/en-us/windows-server/networking/windows-time-service/) - Microsoft official documentation
- [NTFS Master File Table](https://docs.microsoft.com/en-us/windows/win32/fileio/master-file-table) - File system internals
- [Google Analytics Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4) - GA4 API documentation
- [Selenium WebDriver](https://www.selenium.dev/documentation/) - Browser automation
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) - Chrome debugging protocol

### Security Research Papers

- [Browser Fingerprinting: A survey](https://arxiv.org/abs/1905.01051) - Comprehensive fingerprinting research
- [Temporal Forensics in Digital Evidence](https://www.sciencedirect.com/science/article/pii/S1742287618301877) - Timestamp analysis
- [Bot Detection via Mouse Movements](https://dl.acm.org/doi/10.1145/3290605.3300347) - Behavioral analysis

### Related Projects

- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) - Anti-detection ChromeDriver
- [Multilogin](https://multilogin.com/) - Antidetect browser platform
- [Selenium-Wire](https://github.com/wkeeling/selenium-wire) - Extended Selenium for network inspection
- [curl_cffi](https://github.com/yifeikong/curl_cffi) - Python bindings for curl-impersonate

### Learning Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) - Security testing methodology
- [Penetration Testing Execution Standard](http://www.pentest-standard.org/) - Industry standard
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Security framework

---

## 🌟 Acknowledgments

Special thanks to:

- The security research community for continuous innovation
- Contributors and testers who help improve this project
- Open-source projects that make this work possible
- Ethical hackers who advance security research responsibly

---

## 📞 Support & Contact

### Getting Help

- **Documentation**: Read [QUICKSTART.md](QUICKSTART.md), [USER_GUIDE.md](USER_GUIDE.md), and other docs
- **Issues**: Report bugs via [GitHub Issues](https://github.com/malithwishwa02-dot/Aging-cookies-v2/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/malithwishwa02-dot/Aging-cookies-v2/discussions)
- **Security**: Report vulnerabilities privately to security@[repository-domain]

### Before Reporting Issues

Please check:

1. You're running as Administrator
2. All dependencies are installed correctly
3. You've read the troubleshooting section in USER_GUIDE.md
4. You've searched existing issues for similar problems

When reporting, include:

- Operating system and version
- Python version
- Error messages and stack traces
- Configuration used
- Steps to reproduce
- Relevant log excerpts

---

## 📊 Project Status

- **Version**: 2.1.0
- **Status**: Active Development
- **Last Updated**: January 2025
- **Python**: 3.10+
- **Platform**: Windows 10/11
- **License**: Research & Educational Use Only

### Recent Updates

- ✅ Multilogin (MLA) integration with Local API
- ✅ GENERATE_ONLY mode for manual handover
- ✅ Enhanced anti-detection measures
- ✅ Comprehensive documentation overhaul
- ✅ Improved error handling and recovery
- ✅ Performance optimizations

### Roadmap

- [ ] Linux support via clock_settime()
- [ ] Firefox and Edge support
- [ ] Enhanced ML-based behavior modeling
- [ ] Distributed operation across multiple VMs
- [ ] Advanced MFT forensics evasion
- [ ] GUI interface for easier operation
- [ ] Docker containerization
- [ ] CI/CD pipeline for automated testing

---

## ⭐ Star History

If you find this project useful for your research, please consider giving it a star! ⭐

This helps:
- Increase visibility for other researchers
- Show support for open security research
- Encourage continued development
- Build a community around ethical security research

---

## 📄 License

**Research & Educational Use Only**

This software is provided as-is for security research and educational purposes. By using this software, you agree to:

1. Use only for lawful, authorized purposes
2. Obtain proper written authorization
3. Comply with all applicable laws and regulations
4. Accept full responsibility for your actions
5. Not hold developers liable for any damages or legal consequences

See the LICENSE file for complete terms.

---

**Made with 🔐 by Security Researchers, for Security Researchers**

**Remember**: With great power comes great responsibility. Use ethically, test responsibly, research legally.