# GITHUB COPILOT AGENT TASK: PROJECT CHRONOS-MLA implementation

**ROLE:** You are an Expert Python Offensive Security Engineer and Windows Kernel Specialist.
**OBJECTIVE:** Implement the "CHRONOS-MLA" automation framework for synthetic profile generation as described below.
**CONSTRAINTS:**
1.  **Environment:** Windows 10/11 Host (Administrative Privileges required).
2.  **Language:** Python 3.10+ (using `ctypes`, `subprocess`, `requests`).
3.  **Safety:** Code must include safety checks to prevent permanent system damage (e.g., restoring time on exit).
4.  **Style:** Modular, asynchronous where possible, type-hinted, and robust error handling.

---

## CONTEXT: THE CHRONOS ARCHITECTURE

The goal is to create a "Level 9" browser profile that appears to be 90 days old by manipulating the OS Kernel Time before the browser is launched. This forces "Natural Generation" of forensically aged cookies and cache.

### MODULE 1: THE VOID (Network & Time Control)
**File:** `core/network_lock.py` & `core/time_manager.py`

**Requirements:**
1.  **W32Time Kill Switch:**
    *   Check for Admin privileges.
    *   Set `w32time` service to `DISABLED`.
    *   Stop the service.
    *   *Advanced:* Inject registry key `HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters` -> `Type: NoSync`.
2.  **NTP Blockade:**
    *   Use `netsh advfirewall` to create an OUTBOUND BLOCK rule for UDP Port 123.
    *   Ensure this rule takes precedence.
3.  **Kernel Time Shift:**
    *   Use `ctypes.windll.kernel32.SetSystemTime`.
    *   Define the `SYSTEMTIME` C-structure.
    *   Input: `days_to_shift` (integer).
    *   Logic: Calculate Target Time (Now - Days). Convert to UTC. Apply to Kernel.
    *   Validation: Call `GetSystemTime` to verify the shift.

### MODULE 2: THE BRIDGE (MLA Integration)
**File:** `core/mla_bridge.py`

**Requirements:**
1.  **API Interaction:**
    *   Communicate with MultiLogin Local API v2 (`http://localhost:35000/api/v2`).
2.  **Profile Creation Payload:**
    *   Must set `timezone_mode` to `MANUAL`.
    *   Must disable "Time Tampering" protections.
    *   Must force the browser to respect the OS Kernel time, NOT the Proxy IP location time.
3.  **WebDriver Attachment:**
    *   Launch profile via API.
    *   Extract `remote-debugging-port`.
    *   Attach `selenium.webdriver.Remote` to the running instance.

### MODULE 3: THE JOURNEY (Entropy & Behavior)
**File:** `modules/journey.py` & `core/entropy.py`

**Requirements:**
1.  **Poisson Distribution Timing:**
    *   Implement a function that calculates random "Time Jumps" between T-90 days and T-0 (Today).
    *   Ensure the browser is fully closed (process killed) between jumps to flush `.wal` (Write-Ahead Log) files to disk.
2.  **Bezier Curve Mouse Movement:**
    *   Implement `HumanMouse` class.
    *   Use Cubic Bezier math: `B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3`.
    *   Add "Micro-sleeps" (random floats) between movement steps.
3.  **Behavioral Patterns:**
    *   `random_scroll()`: Scroll down, but occasionally scroll up (regression).
    *   `loss_of_focus()`: Switch to `about:blank` for 1-4 seconds to trigger `visibilityState: hidden`.

### MODULE 4: THE LOCK (Forensic Scrubbing)
**File:** `core/forensics.py`

**Requirements:**
1.  **NTFS Mismatch Fix:**
    *   Address the `$FILE_NAME` vs `$STANDARD_INFORMATION` timestamp discrepancy.
2.  **Move-and-Back Strategy:**
    *   Use `shutil.move` to move the profile directory to a temporary location (different volume/partition if possible, or simulate move operation).
    *   Move it back to the original location.
    *   *Constraint:* This must happen WHILE the system time is still backdated.

### MODULE 5: RESURRECTION (Cleanup)
**File:** `core/cleanup.py`

**Requirements:**
1.  **Restoration:**
    *   Delete `netsh` firewall rule.
    *   Enable and Start `w32time`.
    *   Force resync: `w32tm /resync`.
2.  **Validation:**
    *   Query `http://worldtimeapi.org/api/ip`.
    *   Compare with local system time.
    *   Raise `SystemExit` if skew > 1 second.

---

## INTERACTIVE INSTRUCTIONS FOR COPILOT

**How to use this task:**

1.  **Initialize the Environment:**
    *   *Prompt:* "Based on CHRONOS_TASK.md, create the directory structure and a `requirements.txt` file."

2.  **Implement Specific Modules:**
    *   *Prompt:* "Implement the `core/time_manager.py` module using `ctypes` as defined in Module 1 of CHRONOS_TASK.md. Ensure the SYSTEMTIME structure is correct."

3.  **Generate the Orchestrator:**
    *   *Prompt:* "Create `main.py` that orchestrates the 4 phases defined in the CHRONOS_TASK context. It should take a profile ID and a number of days as arguments."

4.  **Security Review:**
    *   *Prompt:* "Review the `network_lock.py` code. Does it correctly handle the `ACCESS_DENIED` error if the script is not run as Admin?"

---
**AUTHORITY: Dva.12 | STATUS: READY_FOR_INJECTION**
