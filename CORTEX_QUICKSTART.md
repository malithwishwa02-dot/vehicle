# Quick Start - Cortex Agent

## What is Cortex Agent?

Cortex Agent is an autonomous pre-initialization wrapper for the PROMETHEUS-CORE pipeline. It performs intelligent pre-flight checks and configuration optimization BEFORE launching the main pipeline.

## Quick Usage

### Basic Run
```bash
# Run with autonomous configuration
python cortex_agent.py --zip 10001

# Run with proxy
python cortex_agent.py --proxy user:pass@host:port --zip 10001

# Run with manual age override
python cortex_agent.py --age 150 --zip 10001
```

### Test Mode
```bash
# Dry-run (pre-flight checks only, no execution)
python cortex_agent.py --dry-run
```

### Force Mode
```bash
# Force execution even if checks fail
python cortex_agent.py --force --zip 10001
```

## What It Does

### Phase 0: Pre-Flight Checks
1. ✅ **Environment Validation** - Checks Python version, directories, modules
2. 🔍 **MCP Infrastructure Probe** - Tests Model Context Protocol servers
3. 🌐 **MLA API Health Check** - Verifies Multilogin Agent availability
4. 🔒 **Proxy Health Validation** - Tests proxy connectivity and IP trust
5. 🤖 **LLM Configuration Analysis** - AI-powered parameter optimization

### Phase 1: Pipeline Launch
- Launches `main_v5.py` with optimized configuration
- Passes dynamic parameters based on analysis
- Respects user overrides

## Example Output

```
================================================================================
CORTEX AGENT INITIALIZED - Autonomous Pre-Init Protocol
================================================================================
[PHASE 0] PREFLIGHT CHECKS - Starting Autonomous Reconnaissance
  > Running: Environment Validation
    Python Version: 3.12.3
    Core modules available: ✓
    OPENAI_API_KEY: Not set (fallback mode)
    ✓ PASS: Environment Validation
  > Running: MCP Infrastructure Probe
    MCP Infrastructure: OFFLINE (will use TLS fallback)
    ⚠ PARTIAL: MCP Infrastructure Probe (non-critical)
  > Running: LLM Configuration Analysis
    Analyzing target: https://www.wikipedia.org
    LLM Analysis Complete:
      Trust Level: medium
      Risk Assessment: moderate
      Recommended Age: 120 days
    Age parameter ADJUSTED: 90 -> 120 days
    ✓ PASS: LLM Configuration Analysis
================================================================================
PREFLIGHT CHECKS: ALL CRITICAL CHECKS PASSED
================================================================================
[PHASE 1] LAUNCHING PROMETHEUS-CORE PIPELINE
  Target: main_v5.py
  Command: python main_v5.py --zip 10001 --age 120
```

## Status Reports

Every run generates a detailed JSON report:

```bash
# View latest status report
ls -lt logs/cortex_agent_status_*.json | head -1
```

Example report:
```json
{
  "timestamp": "2026-01-21 17:50:27",
  "environment": {
    "python_version": "3.12.3",
    "core_modules": true
  },
  "llm_analysis": {
    "recommended_age_days": 120,
    "trust_level": "medium",
    "risk_assessment": "moderate"
  },
  "errors": [],
  "warnings": []
}
```

## Optional: Enable AI Mode

```bash
# Set OpenAI API key for intelligent configuration
export OPENAI_API_KEY="sk-..."

# Run with AI-powered analysis
python cortex_agent.py --zip 10001
```

## Optional: Install MCP Servers

```bash
# Install MCP infrastructure for advanced features
pip install uv
uvx install mcp-server-fetch

# Run with full autonomous capabilities
python cortex_agent.py --zip 10001
```

## Backward Compatibility

You can still run the old way:
```bash
# Direct execution (bypasses Cortex Agent)
python main_v5.py --proxy user:pass@host:port --zip 10001 --age 90
```

## Documentation

- **User Guide**: [CORTEX_AGENT_GUIDE.md](CORTEX_AGENT_GUIDE.md)
- **Implementation Summary**: [CORTEX_AGENT_SUMMARY.md](CORTEX_AGENT_SUMMARY.md)
- **Main README**: [README.md](README.md)

## Troubleshooting

### "MCP Infrastructure: OFFLINE"
Normal - system automatically falls back to TLS mode. No action needed.

### "MLA API: NOT REACHABLE"
Normal if Multilogin is not running. Profile export will require manual handling.

### "Age parameter LOCKED"
You used `--age` flag. System respects your override and won't adjust automatically.

## Support

For issues or questions:
1. Check logs: `logs/cortex_agent.log`
2. Review status report: `logs/cortex_agent_status_*.json`
3. Run dry-run: `python cortex_agent.py --dry-run`

---

**Cortex Agent** - Autonomous Intelligence for PROMETHEUS-CORE
