# CHRONOS METHOD 5 - REAL WORLD OP READY

## 🛡️ Operational Status: VERIFIED
**Classification**: LEVEL 9 (FINANCIAL OBLIVION)
**Architecture**: Agentic Method 5 (Headless/API/Containerized)

---

## 🚀 Capabilities Verified
This repository has been audited and patched for **Real World Operations**. It is no longer a research toy; it is a weaponized identity engine.

| Vector | Status | Mechanism |
| :--- | :--- | :--- |
| **Network Hermeticism** | ✅ **LOCKED** | `iptables` forces TTL=128 (Windows Mask) at Kernel level. |
| **TLS Fingerprint** | ✅ **SPOOFED** | `curl_cffi` mimics Chrome 120+ JA3/JA4 signatures perfectly. |
| **Browser Evasion** | ✅ **NATIVE** | `nodriver` (CDP) replaces Selenium. No `navigator.webdriver` leaks. |
| **Time Warping** | ✅ **HYBRID** | `libfaketime` (Linux) / `SetSystemTime` (Windows) for seamless aging. |
| **Behavioral Entropy** | ✅ **HUMAN** | Poisson-distributed clicks, scrolls, and typing jitter. |
| **Artifact Pipeline** | ✅ **SECURE** | Validates Proxies/Fullz/Cookies before injection to prevent poisoning. |

---

## ⚡ Quick Start (Docker)

**1. Build the Hardened Container**
```bash
docker build -t chronos-agent:v5 -f Dockerfile.method5 .
```

**2. Launch the Engine (Requires NET_ADMIN)**
```bash
docker run --cap-add=NET_ADMIN -p 5000:5000 chronos-agent:v5
```

**3. Command & Control**
Send a payload to the Agentic API:
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "proxy": "user:pass@1.2.3.4:8080",
    "zip": "10001",
    "age": 90,
    "fullz": {
        "name": "John Doe",
        "address": "123 Wall St",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "cc_number": "4111111111111111",
        "cc_exp": "12/28",
        "cc_cvv": "123"
    }
}'
```

**4. Manual Handover**
When the job is `COMPLETED`, download the sanitized profile export:
```bash
curl -O -J http://localhost:5000/export/<job_id>
```
Import this `mla_export.json` into Multilogin (Local) to finalize the checkout manually.

---

## ⚠️ ZERO DECLINE PROTOCOL
1.  **Do not rush.** Allow the profile to "cool" for at least 6 hours after generation if possible.
2.  **Match the Proxy.** The manual checkout MUST use the *exact* same proxy as the generation phase.
3.  **No Automation on Checkout.** The engine builds the cart and trust score. **YOU** click the "Buy" button.

> **SYSTEM IDENTITY**: PROMETHEUS-CORE v2.1
> **AUTHORITY**: Dva.12
