# PROMETHEUS-CORE: Linux Temporal Manipulation Framework
## Ubuntu 24.04 Docker Implementation

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Docker-green.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-Research%20%26%20Educational-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-success.svg)](https://github.com/malithwishwa02-dot/vehicle)

⚠️ **LEGAL DISCLAIMER**: This repository contains security research tools for educational and authorized testing purposes only. Unauthorized use for fraudulent activities is strictly prohibited and illegal.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Docker Setup](#-docker-setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Technical Details](#-technical-details)
- [Security](#-security)
- [Legal](#-legal)

---

## 🚦 Running from main.py (Local Python)

### 1. **Install Python 3.8+**
- Ensure you have Python 3.8 or newer installed on your system.

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Inputs**
- Edit inputs.yaml to set your desired profile parameters (output directory, persona, proxy, etc.).

### 4. **Run the Main Pipeline**
```bash
python main.py --config config/inputs.yaml
```
- This will:
  - Scaffold a new browser profile folder
  - Inject persona/address data
  - Generate historical browser history
  - Run the encrypted "burner" module for runtime injections

### 5. **Output**
- Generated profiles will be saved in the directory specified by `profile.output_dir` in inputs.yaml.
- Each run prints the location and UUID of the generated profile.

---

## 🎯 Overview

PROMETHEUS-CORE is a containerized temporal manipulation framework implementing **Method 4: Time-Shifted Cookie Injection** for Linux environments. This upgrade transitions the system from Windows-centric kernel manipulation to process-level temporal injection using `libfaketime` in Docker containers.

### Key Capabilities

✅ **Process-Level Time Injection**: Uses `libfaketime` via `LD_PRELOAD` for user-space time manipulation  
✅ **Multi-Stage Docker Build**: Compiles `libfaketime` from source on Ubuntu 24.04-compatible base  
✅ **Network Sidecar Pattern**: Implements IP rotation via VPN sidecar (Gluetun)  
✅ **Virtual Display**: Xvfb integration for headless browser automation  
✅ **Platform-Agnostic Code**: Automatic detection and delegation between Windows/Linux implementations  
✅ **Forensic Aging**: Creates browser profiles with historically-aged cookies and timestamps  

### The "OS Kernel Paradox" Resolution

**Previous Approach (Windows)**:
- Global kernel clock manipulation via `SetSystemTime()`
- Required Administrator privileges
- Affected entire system
- Risk of time drift and NTP conflicts

**New Approach (Linux/Docker)**:
- Process-scoped time injection via `libfaketime`
- Container isolation prevents system-wide impact
- No elevated privileges required for time manipulation
- Automatic restoration when container exits

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐      ┌────────────────────────┐   │
│  │  VPN Sidecar        │      │  PROMETHEUS-CORE       │   │
│  │  (Gluetun)          │◄─────┤  Container             │   │
│  │                     │      │                        │   │
│  │  • IP Rotation      │      │  Stage 1: Builder      │   │
│  │  • Network Isolation│      │  ├─ Compile libfaketime│   │
│  │  • Firewall Rules   │      │  └─ Source: python:3.11│   │
│  └─────────────────────┘      │                        │   │
│                                │  Stage 2: Runtime      │   │
│                                │  ├─ Chrome Stable      │   │
│                                │  ├─ Xvfb Display :99   │   │
│                                │  ├─ libfaketime.so     │   │
│                                │  ├─ LD_PRELOAD inject  │   │
│                                │  └─ Python App         │   │
│                                └────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Application Layer (Platform-Agnostic)          │
├─────────────────────────────────────────────────────────────┤
│  core/chronos.py (Facade)                                   │
│  ├─ Detects platform.system()                              │
│  ├─ Windows? → ChronosWindows (kernel32.dll)               │
│  └─ Linux?   → ChronosLinux (libfaketime verify)           │
└─────────────────────────────────────────────────────────────┘
```

### File Structure

```
vehicle/
├── Dockerfile                    # Multi-stage build (libfaketime + runtime)
├── docker-compose.yml            # Service orchestration (core + VPN sidecar)
├── entrypoint.sh                 # Container initialization script
├── requirements.txt              # Python dependencies
├── core/
│   ├── chronos.py               # Platform-agnostic time manipulation facade
│   ├── chronos_linux.py         # Linux libfaketime verification
│   ├── genesis.py               # Time manipulation orchestration
│   └── ...                      # Other core modules
├── config/
│   └── settings.yaml            # Application configuration
└── profiles/                    # Browser profile storage
```

---

## ⚡ Quick Start

### Prerequisites

- **Docker**: 20.10+ with BuildKit support
- **Docker Compose**: 1.29+
- **System**: Linux host (Ubuntu 20.04/22.04/24.04 recommended)
- **Resources**: 2GB RAM minimum, 4GB+ recommended

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/malithwishwa02-dot/vehicle.git
cd vehicle

# 2. Build the Docker image
docker-compose build

# 3. Start the services
docker-compose up -d

# 4. View logs
docker-compose logs -f prometheus-core
```

### First Run

```bash
# Run with default 90-day aging
docker-compose run --rm prometheus-core python level9_operations.py --age 90

# Custom aging duration
docker-compose run --rm prometheus-core python level9_operations.py --age 60

# With specific profile
docker-compose run --rm prometheus-core python main_v5.py --profile custom_profile
```

**Expected Output**:
```
================================================================
PROMETHEUS-CORE Container Initialization
================================================================
[PHASE 1] Initializing Xvfb Virtual Display on :99...
✓ Xvfb started successfully (PID: 42)
✓ DISPLAY set to :99

[PHASE 2] Calculating FAKETIME offset...
  Genesis Offset: 90 days
  Target Date: 2025-10-23 19:04:21
✓ FAKETIME set to: -90d

[PHASE 3] Validating time shift...
  Host Time (actual): 2026-01-21 19:04:21
  Container Time (shifted): 2025-10-23 19:04:21
✓ LD_PRELOAD active: /usr/local/lib/faketime/libfaketime.so.1

[PHASE 4] Launching PROMETHEUS-CORE application...
================================================================
```

---

## 🐳 Docker Setup

### Dockerfile (Multi-Stage Build)

**Stage 1: Builder**
- Base: `python:3.11-slim-bookworm` (Debian 12, Ubuntu 24.04 kernel compatible)
- Compiles `libfaketime` from source
- Output: `/usr/local/lib/faketime/libfaketime.so.1`

**Stage 2: Runtime**
- Installs: `google-chrome-stable`, `xvfb`, `iptables`, `curl`
- Copies compiled `libfaketime` libraries
- Configures global `LD_PRELOAD` for time interception
- Sets up Python environment and application code

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GENESIS_OFFSET_DAYS` | `90` | Days to shift time backwards |
| `DISPLAY` | `:99` | Xvfb virtual display number |
| `LD_PRELOAD` | `libfaketime.so.1` | libfaketime library injection |
| `FAKETIME_DONT_FAKE_MONOTONIC` | `1` | Preserve monotonic clock |
| `FAKETIME_NO_CACHE` | `1` | Disable time caching |

### Volume Mounts

```yaml
volumes:
  - ./profiles:/app/profiles    # Browser profiles persistence
  - ./logs:/app/logs            # Application logs
  - ./config:/app/config        # Configuration files
```

### Network Configuration

Uses **Network Sidecar Pattern** for IP rotation:
- `prometheus-core` container uses `vpn_sidecar` network stack
- All traffic routes through VPN container
- Firewall rules prevent direct internet access

---

## ⚙️ Configuration

### docker-compose.yml Customization

```yaml
services:
  prometheus-core:
    environment:
      # Change aging duration
      - GENESIS_OFFSET_DAYS=60
      
      # Application settings
      - LOG_LEVEL=DEBUG
      - PYTHONUNBUFFERED=1
    
    # Override default command
    command: python -u main_v5.py --age 60 --profile stripe_profile
```

### VPN Sidecar Configuration

Edit `vpn-config/` directory with your VPN credentials:

```bash
# Example: OpenVPN configuration
mkdir -p vpn-config
cp your-vpn.ovpn vpn-config/
cp your-vpn.crt vpn-config/
cp your-vpn.key vpn-config/
```

Update `docker-compose.yml`:
```yaml
vpn_sidecar:
  environment:
    - VPN_SERVICE_PROVIDER=custom
    - VPN_TYPE=openvpn
    - OPENVPN_CUSTOM_CONFIG=/gluetun/your-vpn.ovpn
```

---

## 🎮 Usage

### Basic Operations

```bash
# Start services
docker-compose up -d

# Run aging operation (90 days)
docker-compose run --rm prometheus-core python level9_operations.py --age 90

# Stop services
docker-compose down

# View logs
docker-compose logs -f prometheus-core

# Enter container shell
docker-compose run --rm prometheus-core /bin/bash
```

### Advanced Usage

```bash
# Custom time offset via environment variable
GENESIS_OFFSET_DAYS=120 docker-compose up

# Run with specific Python script
docker-compose run --rm prometheus-core python main_legacy.py

# Interactive debugging
docker-compose run --rm prometheus-core /bin/bash
root@container:/app# python -c "import datetime; print(datetime.datetime.now())"
```

### Testing Time Shift

```bash
# Verify time shift inside container
docker-compose run --rm prometheus-core bash -c "date && python -c 'import datetime; print(datetime.datetime.now())'"

# Expected output:
# Tue Oct 23 19:04:21 UTC 2025  (shifted time)
```

---

## 🔬 Technical Details

### Method 4: Time-Shifted Cookie Injection

PROMETHEUS-CORE implements temporal manipulation through process-level injection rather than kernel modification:

1. **libfaketime Compilation**: Built from source during Docker image creation
2. **LD_PRELOAD Injection**: Global preload of `libfaketime.so.1` intercepts time syscalls
3. **FAKETIME Variable**: Set to `-{GENESIS_OFFSET_DAYS}d` for relative time shift
4. **Browser Launch**: Chrome spawns with shifted time context
5. **Cookie Generation**: All cookies created with historical timestamps
6. **Process Isolation**: Time shift only affects container processes

### Platform Detection Logic

```python
# core/chronos.py
import platform

if platform.system() == "Windows":
    # Use kernel32.dll SetSystemTime()
    from core.chronos import ChronosWindows
    chronos = ChronosWindows()
elif platform.system() == "Linux":
    # Use libfaketime verification
    from core.chronos_linux import ChronosLinux
    chronos = ChronosLinux()
```

### Linux vs Windows Implementation

| Feature | Windows (ChronosWindows) | Linux (ChronosLinux) |
|---------|--------------------------|----------------------|
| **Time Method** | `kernel32.SetSystemTime()` | `libfaketime` + `LD_PRELOAD` |
| **Scope** | System-wide (kernel) | Process-scoped (user-space) |
| **Privileges** | Administrator required | No special privileges |
| **Reversibility** | Manual restoration needed | Auto-restores on exit |
| **NTP Handling** | Must kill W32Time service | Container isolated by default |
| **Verification** | Direct kernel read | Environment variable check |

### Xvfb Virtual Display

- **Purpose**: Headless browser automation without X11 server
- **Display**: `:99` (configurable)
- **Resolution**: 1920x1080x24
- **Extensions**: GLX, RENDER for WebGL support

---

## 🔒 Security

### Container Security

✅ **Non-Root User**: Application runs as non-privileged user (configurable)  
✅ **Network Isolation**: All traffic routed through VPN sidecar  
✅ **Read-Only Filesystem**: Application code mounted read-only  
✅ **Resource Limits**: CPU/memory limits enforced  
✅ **Secret Management**: Sensitive data in environment variables or Docker secrets  

### Time Manipulation Safety

- **Process-Scoped**: Time shift only affects container, not host system
- **Auto-Restoration**: Time returns to normal on container exit
- **No Kernel Impact**: libfaketime operates in user-space only
- **Audit Trail**: All operations logged to persistent volume

### Known Limitations

⚠️ **Detection Vectors**:
- TLS certificate validation may fail for sites with strict time checks
- Some applications may detect `LD_PRELOAD` or `libfaketime`
- Browser fingerprinting can detect time inconsistencies

⚠️ **Operational Constraints**:
- Requires Docker environment (cannot run directly on host)
- VPN configuration must be manually set up
- Some time-sensitive applications may malfunction

---

## ⚖️ Legal

### Authorized Use Only

This software is provided **EXCLUSIVELY** for:

✅ **Authorized Activities**:
- Security research with proper authorization
- Penetration testing with written permission
- Academic research and education
- Testing your own systems and infrastructure
- Authorized red team operations

❌ **Prohibited Activities**:
- Unauthorized access to computer systems
- Fraud, deception, or identity theft
- Circumventing security controls without permission
- Any illegal activities under applicable laws

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

**⚠️ SERIOUS WARNING**: Misuse of this software may result in severe legal consequences including criminal prosecution, civil liability, and significant fines. Always operate within legal boundaries.

---

## 📚 References

### Technical Documentation

- [libfaketime GitHub](https://github.com/wolfcw/libfaketime) - Time manipulation library
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/) - Build optimization
- [Xvfb Documentation](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml) - Virtual framebuffer
- [Gluetun VPN Client](https://github.com/qdm12/gluetun) - VPN client for Docker

### Related Projects

- [curl_cffi](https://github.com/yifeikong/curl_cffi) - Python bindings for curl-impersonate (JA4 evasion)
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) - Anti-detection ChromeDriver
- [Selenium](https://www.selenium.dev/) - Browser automation framework

---

## 📊 Project Status

- **Version**: 3.0.0 (Ubuntu 24.04 Docker Edition)
- **Status**: Active Development
- **Last Updated**: January 2026
- **Python**: 3.11+
- **Platform**: Linux (Docker)
- **License**: Research & Educational Use Only

### Recent Updates

- ✅ Ubuntu 24.04 Docker containerization
- ✅ Multi-stage build with libfaketime compilation
- ✅ Platform-agnostic chronos facade (Windows/Linux)
- ✅ Network sidecar pattern for IP rotation
- ✅ Xvfb integration for headless operation
- ✅ Comprehensive documentation overhaul

### Roadmap

- [ ] Kubernetes deployment manifests
- [ ] Enhanced ML-based behavior modeling
- [ ] Firefox and Edge browser support
- [ ] Advanced container orchestration
- [ ] CI/CD pipeline for automated testing
- [ ] Helm charts for production deployment

---

## 🆘 Support

### Getting Help

- **Documentation**: Read this README and check `docs/` directory
- **Issues**: Report bugs via [GitHub Issues](https://github.com/malithwishwa02-dot/vehicle/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/malithwishwa02-dot/vehicle/discussions)

### Troubleshooting

**Container won't start**:
```bash
# Check logs
docker-compose logs prometheus-core

# Rebuild image
docker-compose build --no-cache
```

**Time shift not working**:
```bash
# Verify FAKETIME inside container
docker-compose run --rm prometheus-core bash -c "echo \$FAKETIME && date"

# Check LD_PRELOAD
docker-compose run --rm prometheus-core bash -c "echo \$LD_PRELOAD"
```

**VPN not connecting**:
```bash
# Check VPN sidecar logs
docker-compose logs vpn_sidecar

# Verify VPN configuration
docker-compose exec vpn_sidecar cat /gluetun/*.ovpn
```

---

**Made with 🔐 by Security Researchers, for Security Researchers**

**Remember**: With great power comes great responsibility. Use ethically, test responsibly, research legally.
