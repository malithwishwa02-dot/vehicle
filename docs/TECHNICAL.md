# PROMETHEUS-CORE Technical Documentation

## Architecture Overview

PROMETHEUS-CORE v2.0.0 implements Method 4 (Time-Shifted Cookie Injection) from the Chronos Architecture specification. This document provides in-depth technical details for developers and security researchers.

---

## System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    PrometheusCore                            │
│                  (Master Orchestrator)                       │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├─► Phase 0: IsolationManager
               │   ├─ NTP service disable
               │   ├─ Firewall UDP 123 blocking
               │   ├─ Hypervisor detection
               │   └─ VM time sync disable
               │
               ├─► Phase 1: GenesisController
               │   ├─ SetSystemTime Win32 API
               │   ├─ UTC time manipulation
               │   └─ Privilege escalation
               │
               ├─► Phase 2: ProfileOrchestrator
               │   ├─ Selenium WebDriver
               │   ├─ Anti-detection suite
               │   ├─ Cookie injection
               │   └─ Browser automation
               │
               ├─► Phase 3: EntropyGenerator
               │   ├─ Poisson distribution
               │   ├─ Bezier mouse curves
               │   ├─ Natural scrolling
               │   └─ Typing variations
               │
               ├─► Phase 4: GAMPTriangulation
               │   ├─ Google Analytics MP v2
               │   ├─ Backdated events
               │   └─ Server-side validation
               │
               ├─► Phase 5: ForensicAlignment
               │   ├─ File timestamp stomping
               │   ├─ MFT $FN scrubbing
               │   └─ Cross-volume operations
               │
               ├─► Phase 6: MultiloginIntegration
               │   ├─ MLA Local API (35000)
               │   ├─ Profile export
               │   └─ Cookie synchronization
               │
               └─► Phase 7: SafetyValidator
                   ├─ WorldTimeAPI sync
                   ├─ Service restoration
                   └─ Rollback mechanisms
```

---

## Core Modules

### 1. GenesisController (core/genesis.py)

**Purpose**: Kernel-level system time manipulation using Windows APIs.

**Key Functions**:

```python
class GenesisController:
    def set_system_time(self, target_datetime: datetime) -> bool:
        """
        Uses ctypes to call SetSystemTime Win32 API
        
        Parameters:
            target_datetime: UTC datetime to set system clock to
            
        Returns:
            bool: True if successful, False otherwise
            
        Requires:
            - Administrator privileges
            - NTP sync disabled
            - Proper SYSTEMTIME structure
        """
```

**Implementation Details**:

- Uses `ctypes.windll.kernel32.SetSystemTime()`
- Converts Python datetime to SYSTEMTIME structure:
  ```c
  typedef struct _SYSTEMTIME {
    WORD wYear;
    WORD wMonth;
    WORD wDayOfWeek;     // Ignored for SetSystemTime
    WORD wDay;
    WORD wHour;
    WORD wMinute;
    WORD wSecond;
    WORD wMilliseconds;
  } SYSTEMTIME;
  ```
- Always uses UTC to avoid DST complications
- Requires `SE_SYSTEMTIME_NAME` privilege

**Error Handling**:

- Privilege verification before operation
- Automatic rollback on failure
- WorldTimeAPI validation after restoration

---

### 2. IsolationManager (core/isolation.py)

**Purpose**: Complete network time synchronization severance.

**Operations**:

1. **NTP Service Disable**:
   ```bash
   net stop w32time
   sc config w32time start=disabled
   reg add HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters /v Type /t REG_SZ /d NoSync /f
   ```

2. **Firewall Configuration**:
   ```bash
   netsh advfirewall firewall add rule name="PROMETHEUS_Block_NTP_Out" dir=out protocol=UDP remoteport=123 action=block
   netsh advfirewall firewall add rule name="PROMETHEUS_Block_NTP_In" dir=in protocol=UDP localport=123 action=block
   ```

3. **Hypervisor Detection**:
   - CPUID check for hypervisor bit
   - WMI queries for VM detection
   - Disable VMware Tools time sync
   - Disable Hyper-V time sync

**Critical**: Must be executed before time manipulation to prevent automatic correction.

---

### 3. ProfileOrchestrator (core/profile.py)

**Purpose**: Browser automation with anti-detection measures.

**Anti-Detection Stack**:

1. **WebDriver Detection Prevention**:
   ```javascript
   // Injected into every page
   Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
   delete navigator.__proto__.webdriver;
   ```

2. **Chrome DevTools Protocol**:
   - Uses `undetected-chromedriver` for evasion
   - Custom Chrome options to hide automation
   - User agent spoofing with realistic profiles

3. **Fingerprint Randomization**:
   - Canvas fingerprint randomization
   - WebGL vendor/renderer spoofing
   - Screen resolution variations
   - Timezone alignment with time shift

**Cookie Injection**:

```python
def inject_cookies(self, driver: WebDriver, cookies: List[Dict]):
    """
    Injects cookies with proper temporal alignment
    
    - Creation timestamp = shifted time
    - Expiry dates set relatively
    - Domain/path properly scoped
    - HttpOnly/Secure flags preserved
    """
```

---

### 4. EntropyGenerator (core/entropy.py)

**Purpose**: Generate human-like behavioral patterns.

**Algorithms**:

1. **Poisson Distribution for Time Intervals**:
   ```python
   import numpy as np
   
   def generate_intervals(self, lambda_param: float, num_events: int):
       """
       λ = 2.5 (default): average 2.5 events per time unit
       Returns array of time intervals following Poisson process
       """
       return np.random.poisson(lambda_param, num_events)
   ```

2. **Bezier Curves for Mouse Movement**:
   ```python
   def bezier_curve(self, start: Tuple, end: Tuple, control_points: int = 3):
       """
       Generate natural mouse trajectory using cubic Bezier curves
       - Random control points for path variation
       - Variable speed (slow start, fast middle, slow end)
       - Micro-jitter during movement
       """
   ```

3. **Natural Scrolling Patterns**:
   - Variable scroll speeds
   - Pauses at content
   - Reverse scrolling occasionally
   - Edge bounce behavior

4. **Typing Variations**:
   - WPM between 40-80 (configurable)
   - Pause distribution following human patterns
   - Occasional typos and corrections
   - Backspace usage patterns

---

### 5. GAMPTriangulation (core/server_side.py)

**Purpose**: Create server-side validation through Google Analytics.

**Google Analytics Measurement Protocol v2**:

```python
def send_backdated_event(
    self,
    event_name: str,
    timestamp: datetime,
    client_id: str,
    event_params: Dict = None
):
    """
    POST to https://www.google-analytics.com/mp/collect
    
    Headers:
        Content-Type: application/json
    
    Body:
        {
            "client_id": "unique_id",
            "timestamp_micros": timestamp_in_microseconds,
            "events": [{
                "name": "page_view",
                "params": {
                    "page_location": "https://example.com",
                    "engagement_time_msec": "5000"
                }
            }]
        }
    """
```

**Event Strategy**:

- Distribute events across aged period
- Realistic session durations (2-30 minutes)
- Natural engagement patterns
- Multiple event types (page_view, scroll, engagement)

**Verification**:

- GA4 reports show historical data
- Real-time validation not possible (24-48h processing)
- Creates server-side audit trail

---

### 6. ForensicAlignment (core/forensic.py)

**Purpose**: Align filesystem metadata with temporal manipulation.

**File Timestamp Manipulation**:

```python
import win32file
import pywintypes

def stomp_timestamps(self, filepath: Path, target_time: datetime):
    """
    Modify all file timestamps using Win32 API
    
    Timestamps modified:
        - CreationTime
        - LastAccessTime
        - LastWriteTime
    
    Uses:
        - win32file.CreateFile() with WRITE_ATTRIBUTES
        - win32file.SetFileTime()
    """
    handle = win32file.CreateFile(
        str(filepath),
        win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        win32file.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    
    pytime = pywintypes.Time(target_time)
    win32file.SetFileTime(handle, pytime, pytime, pytime)
    handle.Close()
```

**MFT (Master File Table) Scrubbing**:

**Warning**: Advanced forensics operation requiring deep Windows knowledge.

```python
def scrub_mft_entries(self, directory: Path):
    """
    Manipulate NTFS Master File Table entries
    
    Method:
        1. Copy directory to different volume
        2. Delete original (marks MFT entries as free)
        3. Copy back with new timestamps
        4. MFT entries get new allocation
    
    Effectiveness:
        - Standard forensics: Highly effective
        - Advanced forensics: Detectable via $LogFile
        - Professional forensics: Requires $LogFile analysis
    """
```

**Limitations**:

- NTFS only (no FAT32, exFAT)
- Requires admin privileges
- Does not scrub Volume Shadow Copies (VSS)
- $LogFile and $UsnJrnl maintain records

---

### 7. MultiloginIntegration (core/mla_handler.py)

**Purpose**: Integration with Multilogin antidetect browser platform.

**MLA Local API**:

```python
class MLAHandler:
    def __init__(self, port: int = 35000):
        self.api_base = f"http://localhost:{port}"
    
    def start_profile(self, profile_id: str) -> Dict:
        """
        POST /api/v1/profile/start
        
        Returns:
            {
                "status": "success",
                "value": {
                    "webdriver": "http://localhost:PORT",
                    "status": "Active"
                }
            }
        """
        response = requests.post(
            f"{self.api_base}/api/v1/profile/start",
            json={"uuid": profile_id}
        )
        return response.json()
```

**Profile Export**:

1. Extract Chrome profile data
2. Convert to Multilogin format
3. Inject into MLA profile storage
4. Synchronize cookies to cloud

**Cookie Sync Protocol**:

```python
def sync_cookies_to_disk(self):
    """
    Ensures cookies are persisted before exit
    
    Process:
        1. Close all browser tabs
        2. Wait for SQLite write-ahead log flush
        3. Trigger MLA cloud sync
        4. Verify file modification timestamps
    """
```

---

## Security Considerations

### Detection Vectors

#### 1. Browser Fingerprinting

**Mitigations Implemented**:

- Canvas noise injection
- WebGL vendor/renderer spoofing
- Audio context randomization
- Font enumeration blocking
- Plugin array hiding
- WebRTC leak prevention
- Timezone alignment with system time

**Testing**:

- Verified against:
  - Fingerprint.com
  - Pixelscan.net
  - CreepJS
  - BrowserLeaks
  - Device Info

#### 2. Behavioral Analysis

**Attack Vectors**:

- Mouse movement patterns too perfect
- Scrolling velocity unrealistic
- Zero typing errors
- Perfectly timed actions

**Mitigations**:

- Bezier curve mouse movements
- Natural scroll acceleration
- Random pauses and hesitations
- Occasional "mistakes" in interactions

#### 3. Temporal Forensics

**Red Flags**:

- Cookie age doesn't match file timestamps
- GA4 events mismatch with cookie creation
- MFT entries inconsistent with file data
- Volume Shadow Copy discrepancies

**Mitigations**:

- Complete timestamp alignment
- Server-side event validation via GAMP
- MFT scrubbing via cross-volume moves
- VSS awareness (manual intervention required)

#### 4. Network Analysis

**Detection Methods**:

- TLS fingerprinting
- HTTP header analysis
- WebSocket behavior
- DNS query patterns

**Mitigations**:

- Uses `curl_cffi` for native TLS stacks
- Header order matches real browsers
- Proper HTTP/2 usage
- Realistic DNS timing

---

## Performance Characteristics

### Timing Benchmarks

| Operation | Duration | Variance |
|-----------|----------|----------|
| NTP isolation | 2-3s | ±0.5s |
| Time shift (Genesis) | 0.1-0.2s | ±0.05s |
| Browser launch | 5-8s | ±2s |
| Profile creation | 8-12min | ±3min |
| Entropy generation | 2-5min | ±1min |
| GAMP injection | 1-2min | ±0.5min |
| Forensic alignment | 30-60s | ±15s |
| MFT scrubbing | 45-90s | ±20s |
| Time restoration | 3-5s | ±1s |
| **Total Pipeline** | **12-20min** | **±4min** |

### Resource Usage

**CPU**:
- Peak: 60-80% during browser automation
- Average: 20-30% during entropy generation
- Idle: <5% during time shifts

**Memory**:
- Chrome process: 500MB-1GB
- Python process: 200-400MB
- Total: ~1.5-2GB peak

**Disk**:
- Profile size: 50-200MB
- Log files: 10-50MB per operation
- Temporary files: 100-500MB during operation

**Network**:
- Profile creation: 50-200MB download
- GAMP events: 10-50KB total
- Time sync verification: <5KB

---

## API Reference

### PrometheusCore Class

```python
class PrometheusCore:
    """Master orchestrator for Level 9 operations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize PROMETHEUS-CORE with configuration
        
        Args:
            config: Configuration dictionary or None for defaults
        """
    
    def execute_level9_operation(
        self,
        target_url: str,
        age_days: int = 90
    ) -> Dict[str, Any]:
        """
        Execute complete Level 9 operation
        
        Args:
            target_url: URL for cookie generation
            age_days: Age of profile in days (1-365)
        
        Returns:
            Operation results dictionary with:
                - operation_id: Unique operation identifier
                - status: "completed" or "failed"
                - phases: Results from each phase
                - validation: Final validation results
        
        Raises:
            PermissionError: If not running as administrator
            TimeoutError: If operation exceeds timeout
            ValueError: If parameters are invalid
        """
```

### Configuration Schema

```yaml
# config/settings.yaml

execution:
  mode: "GENERATE_ONLY"  # or "FULL"
  timeout_minutes: 30
  
temporal:
  target_age_days: 90
  entropy_segments: 12
  poisson_lambda: 2.5
  min_interval_hours: 1
  max_interval_hours: 72
  
browser:
  type: "chrome"  # or "multilogin"
  profile_path: "profiles/chrome"
  headless: false
  anti_detect: true
  window_size: [1920, 1080]
  
multilogin:
  enabled: false
  browser_type: "multilogin"
  mla_port: 35000
  mla_profile_id: ""
  headless_mode: false
  
analytics:
  enabled: true
  measurement_id: "G-XXXXXXXXXX"
  api_secret: "your_api_secret"
  client_id: "auto"  # or specific ID
  
forensic:
  enabled: true
  mft_scrubbing: true
  timestomping: true
  vss_aware: false
  
safety:
  time_api: "http://worldtimeapi.org/api/ip"
  max_skew_seconds: 5
  rollback_on_error: true
  emergency_restore: true
  
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "logs/prometheus.log"
  encrypted: true
  rotation: "1MB"
```

---

## Development Guidelines

### Adding New Phases

1. Create module in `core/` directory
2. Implement required interface:
   ```python
   class CustomPhase:
       def execute(self, context: Dict) -> Dict:
           """Execute phase and return results"""
           pass
       
       def validate(self) -> bool:
           """Validate phase can execute"""
           pass
       
       def rollback(self) -> bool:
           """Rollback phase on error"""
           pass
   ```

3. Register in `PrometheusCore._initialize_components()`
4. Add to pipeline in `execute_level9_operation()`
5. Add tests in `tests/test_custom_phase.py`

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_genesis.py -v

# Run with coverage
pytest tests/ --cov=core --cov-report=html

# Run integration tests
pytest tests/integration/ -v --slow
```

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debug mode
python main.py --target https://example.com --debug

# Inspect state at breakpoint
import pdb; pdb.set_trace()
```

---

## Known Limitations

### Technical Limitations

1. **Windows Only**: Core time manipulation requires Win32 APIs
2. **Administrator Required**: Cannot operate without elevated privileges
3. **NTFS Only**: Forensic alignment requires NTFS filesystem
4. **Chrome Focus**: Primary testing with Chrome, limited Firefox support
5. **No WSL Support**: Windows Subsystem for Linux not compatible

### Security Limitations

1. **VSS Detection**: Volume Shadow Copies can reveal temporal manipulation
2. **$LogFile Analysis**: NTFS transaction logs maintain records
3. **TPM Detection**: Trusted Platform Module can detect time changes
4. **Advanced ML**: Sophisticated ML models may detect patterns
5. **Live Monitoring**: Real-time security monitoring can catch time shifts

### Operational Limitations

1. **Internet Required**: For time validation and GAMP triangulation
2. **Time Window**: Must complete operation before NTP auto-restore
3. **Single Target**: Optimized for one URL per operation
4. **Profile Reuse**: Limited reusability of aged profiles

---

## Future Enhancements

### Planned Features

- [ ] Linux support via `clock_settime()`
- [ ] Firefox and Edge anti-detection
- [ ] Multi-target profile creation
- [ ] Distributed operation across VMs
- [ ] Machine learning behavior modeling
- [ ] Advanced MFT analysis evasion
- [ ] TPM bypass research
- [ ] Cloud-based time server

### Research Areas

- [ ] Browser extension detection evasion
- [ ] TLS 1.3 fingerprint randomization
- [ ] HTTP/3 QUIC support
- [ ] WebAssembly-based automation
- [ ] GPU-based entropy generation

---

## References

### Technical Documentation

- [Windows Time Service](https://docs.microsoft.com/en-us/windows-server/networking/windows-time-service/)
- [NTFS Master File Table](https://docs.microsoft.com/en-us/windows/win32/fileio/master-file-table)
- [Google Analytics Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4)
- [Selenium WebDriver](https://www.selenium.dev/documentation/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

### Security Research

- [Browser Fingerprinting: A survey](https://arxiv.org/abs/1905.01051)
- [Temporal Forensics in Digital Evidence](https://www.sciencedirect.com/science/article/pii/S1742287618301877)
- [Bot Detection via Mouse Movements](https://dl.acm.org/doi/10.1145/3290605.3300347)

### Related Projects

- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [Multilogin](https://multilogin.com/)
- [Selenium-Wire](https://github.com/wkeeling/selenium-wire)

---

**Document Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintained By**: PROMETHEUS-CORE Team
