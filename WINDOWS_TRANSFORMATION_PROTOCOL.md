# OP-SOVEREIGN-V3: WINDOWS NATIVE TRANSFORMATION

## OBJECTIVE
Convert Lucid Empire from Docker/Linux to Native Windows (.exe).

### 1. ARCHITECTURAL CHANGES
| Capability   | Linux (Old)         | Windows Native (New)           |
|-------------|---------------------|-------------------------------|
| Runtime     | Docker Container    | PyInstaller Executable (One-File) |
| Time Travel | libfaketime (LD_PRELOAD) | RunAsDate (DLL Injection) or Playwright Overrides |
| Network     | iptables / TUN Interface | Internal SOCKS5 Tunneling     |
| Paths       | /app/storage/...    | AppData\Local\LucidEmpire\storage\... |
| Browser     | Headless Linux Firefox | Headed Windows Firefox (Camoufox) |

### 2. REQUIRED EXTERNAL ASSETS
- **RunAsDate.exe (NirSoft)** - Command line version (x64).
  - Purpose: Launch browser process with a modified system time.
  - Why: Cleaner than writing a custom C++ hook from scratch.

### 3. EXECUTION FLOW
1. User runs LucidEmpire.exe.
2. App launches the local Dashboard (Flask).
3. User clicks "IGNITE".
4. App generates the profile (SQLite/Json) in AppData.
5. App calculates the "Genesis Date".
6. If a Proxy is supplied, the app starts a local HTTP proxy (CONNECT -> upstream SOCKS5) and writes Firefox `user.js` proxy prefs into the profile.
7. App executes: RunAsDate.exe /immediate /date {GENESIS_DATE} "camoufox.exe"
8. Result: Browser opens natively, believing it is 90 days in the past and routing traffic through the local proxy which chains to the upstream SOCKS5.

Note: The local proxy uses PySocks when chaining to an upstream SOCKS5 server. If you plan to use proxy chaining, ensure `pysocks` is installed (setup_windows.bat installs it).

---

**See windows/lucid_launcher.py, windows/time_hook.py, build_exe.spec, setup_windows.bat for implementation details.**
