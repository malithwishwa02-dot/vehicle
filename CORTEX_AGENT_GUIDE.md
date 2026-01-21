# Cortex Agent: Autonomous Pre-Init Wrapper

## Overview

**Cortex Agent** is a standalone pre-flight orchestrator that wraps the PROMETHEUS-CORE pipeline (`main_v5.py`). It implements autonomous logic for probing, configuration, and validation **before** any core modules execute.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    CORTEX AGENT                           │
│              (Autonomous Pre-Init Layer)                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  PHASE 0: Pre-Flight Checks                              │
│  ┌────────────────────────────────────────────┐          │
│  │ 1. Environment Validation                  │          │
│  │    - Python version, directories, modules  │          │
│  │                                            │          │
│  │ 2. MCP Infrastructure Probe                │          │
│  │    - Health checks, test fetch             │          │
│  │                                            │          │
│  │ 3. MLA API Health Check                    │          │
│  │    - Multilogin Agent availability         │          │
│  │                                            │          │
│  │ 4. Proxy Health Validation                 │          │
│  │    - IP trust check, location scoring      │          │
│  │                                            │          │
│  │ 5. LLM Configuration Analysis              │          │
│  │    - Context-aware entropy/aging config    │          │
│  └────────────────────────────────────────────┘          │
│                       │                                   │
│                       ▼                                   │
│            ┌──────────────────────┐                       │
│            │  Decision Logic      │                       │
│            │  - Pass: Launch      │                       │
│            │  - Fail: Abort/Force │                       │
│            └──────────────────────┘                       │
│                       │                                   │
└───────────────────────┼───────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      PHASE 1: Execute         │
        │      main_v5.py with          │
        │      Dynamic Config           │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   PROMETHEUS-CORE Pipeline    │
        │   (Legacy code untouched)     │
        └───────────────────────────────┘
```

## Key Features

### 1. **Wrapper Architecture**
- **No Core Module Modification**: All legacy code in `core/`, `main_v5.py`, etc. remains untouched
- **Front-Controller Pattern**: Acts as the entry point before core pipeline
- **Clean Separation**: Agentic logic isolated from operational logic

### 2. **Comprehensive Pre-Flight Checks**

#### Environment Validation
- Python version verification
- Critical directory structure validation
- Core module import validation
- Environment variable checks (OPENAI_API_KEY, etc.)

#### MCP Server Probing
- Health check for MCP (Model Context Protocol) infrastructure
- Test fetch to verify functionality
- Graceful fallback if unavailable

#### MLA API Health Check
- Probes common Multilogin Agent API ports (35000, 45000, 35001)
- Tests multiple endpoints for availability
- Non-blocking (warns if unavailable)

#### Proxy Health Validation
- Validates proxy configuration format
- IP trust check via TLS Mimic
- Location and scoring information
- Supports both proxy and direct modes

#### LLM Configuration Analysis
- Context-aware analysis of target domains
- Dynamic age parameter recommendation
- Risk assessment and trust level scoring
- Fallback to heuristic analysis if LLM unavailable

### 3. **Error Resilience Mesh**
- Comprehensive exception handling at every layer
- Non-critical failures logged as warnings
- Critical failures prevent launch (unless --force used)
- Full status report saved to JSON for audit

### 4. **Dynamic Configuration**
- User overrides respected (--age explicitly set)
- LLM recommendations applied intelligently
- Configuration source tracked (user_input vs llm_analysis)
- All config passed through to main_v5.py

## Usage

### Basic Usage

```bash
# Autonomous mode with proxy
python cortex_agent.py --proxy user:pass@host:port --zip 10001

# Manual age override (LLM recommendation ignored)
python cortex_agent.py --age 150 --zip 10001

# Direct connection mode (no proxy)
python cortex_agent.py --zip 10001
```

### Advanced Options

```bash
# Force launch even if critical checks fail
python cortex_agent.py --force --zip 10001

# Dry-run mode (pre-flight only, no launch)
python cortex_agent.py --dry-run --zip 10001
```

### Environment Setup

```bash
# Optional: Enable LLM-powered configuration
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4-turbo-preview"  # Optional, defaults to gpt-4

# Optional: Install MCP servers for autonomous operations
pip install uv
uvx install mcp-server-fetch
uvx install mcp-server-filesystem

# Run the agent
python cortex_agent.py --zip 10001
```

## Operation Modes

### 1. **Full Autonomous Mode**
- Requirements: OPENAI_API_KEY set, MCP servers installed
- Behavior: LLM-powered config with MCP-based data fetching
- Use case: Production deployments with full infrastructure

### 2. **AI-Only Mode**
- Requirements: OPENAI_API_KEY set
- Behavior: LLM-powered config with TLS fallback for data
- Use case: Development environments without MCP

### 3. **Fallback Mode (Zero Friction)**
- Requirements: None
- Behavior: Heuristic-based config, TLS data fetching
- Use case: Testing, minimal dependencies

### 4. **Force Mode**
- Requirements: None
- Behavior: Launch even if pre-flight checks fail
- Use case: Emergency operations, debugging

## Status Reports

Every execution generates a detailed JSON status report:

```json
{
  "timestamp": "2026-01-21T17:45:23.123456",
  "environment": {
    "python_version": "3.12.3",
    "dir_logs": true,
    "dir_profiles": true,
    "core_modules": true,
    "openai_api_key": true
  },
  "mcp_health": {
    "available": true,
    "servers": ["fetch", "filesystem"],
    "test_fetch": "success"
  },
  "mla_health": {
    "available": true,
    "port": 35000,
    "endpoint": "/api/v1/profile/active",
    "status_code": 200
  },
  "proxy_health": {
    "configured": true,
    "healthy": true,
    "ip_info": {
      "ip": "1.2.3.4",
      "city": "New York",
      "country": "US"
    }
  },
  "llm_analysis": {
    "recommended_age_days": 120,
    "trust_level": "medium",
    "risk_assessment": "minimal",
    "strategy_notes": "E-commerce target requires aged profile"
  },
  "errors": [],
  "warnings": ["MLA API: NOT REACHABLE (manual profile export may be required)"]
}
```

Reports are saved to: `logs/cortex_agent_status_<timestamp>.json`

## Log Output Examples

### Successful Autonomous Run

```
2026-01-21 17:45:23,456 - [CORTEX AGENT] - INFO - ================================================================================
2026-01-21 17:45:23,456 - [CORTEX AGENT] - INFO - CORTEX AGENT INITIALIZED - Autonomous Pre-Init Protocol
2026-01-21 17:45:23,456 - [CORTEX AGENT] - INFO - ================================================================================
2026-01-21 17:45:23,457 - [CORTEX AGENT] - INFO - [PHASE 0] PREFLIGHT CHECKS - Starting Autonomous Reconnaissance
2026-01-21 17:45:23,458 - [CORTEX AGENT] - INFO -   > Running: Environment Validation
2026-01-21 17:45:23,459 - [CORTEX AGENT] - INFO -     Python Version: 3.12.3
2026-01-21 17:45:23,460 - [CORTEX AGENT] - INFO -     Core modules available: ✓
2026-01-21 17:45:23,461 - [CORTEX AGENT] - INFO -     OPENAI_API_KEY: Set (LLM analysis enabled)
2026-01-21 17:45:23,462 - [CORTEX AGENT] - INFO -     ✓ PASS: Environment Validation
2026-01-21 17:45:23,463 - [CORTEX AGENT] - INFO -   > Running: MCP Infrastructure Probe
2026-01-21 17:45:23,465 - [MCPClient] - INFO - [MCP] Interface initialized - Zero Friction Mode
2026-01-21 17:45:23,467 - [MCPClient] - INFO - [MCP] Health check passed - uvx available
2026-01-21 17:45:23,468 - [CORTEX AGENT] - INFO -     MCP Infrastructure: ONLINE
2026-01-21 17:45:25,234 - [MCPClient] - INFO - [MCP] Tool execution successful: fetch
2026-01-21 17:45:25,235 - [CORTEX AGENT] - INFO -     MCP Test Fetch: SUCCESS (52341 bytes)
2026-01-21 17:45:25,236 - [CORTEX AGENT] - INFO -     ✓ PASS: MCP Infrastructure Probe
...
2026-01-21 17:45:30,123 - [CORTEX AGENT] - INFO -     LLM Analysis Complete:
2026-01-21 17:45:30,124 - [CORTEX AGENT] - INFO -       Trust Level: high
2026-01-21 17:45:30,125 - [CORTEX AGENT] - INFO -       Risk Assessment: minimal
2026-01-21 17:45:30,126 - [CORTEX AGENT] - INFO -       Recommended Age: 120 days
2026-01-21 17:45:30,127 - [CORTEX AGENT] - INFO -       Strategy Notes: E-commerce site requires aged profile
2026-01-21 17:45:30,128 - [CORTEX AGENT] - INFO -     Age parameter ADJUSTED: 90 -> 120 days
...
2026-01-21 17:45:30,456 - [CORTEX AGENT] - INFO - ================================================================================
2026-01-21 17:45:30,457 - [CORTEX AGENT] - INFO - PREFLIGHT CHECKS: ALL CRITICAL CHECKS PASSED
2026-01-21 17:45:30,458 - [CORTEX AGENT] - INFO - ================================================================================
2026-01-21 17:45:30,459 - [CORTEX AGENT] - INFO - [PHASE 1] LAUNCHING PROMETHEUS-CORE PIPELINE
2026-01-21 17:45:30,460 - [CORTEX AGENT] - INFO -   Target: main_v5.py
2026-01-21 17:45:30,461 - [CORTEX AGENT] - INFO -   Command: python main_v5.py --proxy user:pass@host:port --zip 10001 --age 120
```

### Fallback Mode (LLM Unavailable)

```
2026-01-21 17:45:23,456 - [CORTEX AGENT] - INFO -     OPENAI_API_KEY: Not set (fallback mode)
...
2026-01-21 17:45:25,234 - [IntelligenceCore] - WARNING - [INTELLIGENCE] OPENAI_API_KEY not set - running in fallback mode
2026-01-21 17:45:25,235 - [IntelligenceCore] - INFO - [INTELLIGENCE] Using fallback strategy - Age: 120 days
2026-01-21 17:45:25,236 - [CORTEX AGENT] - INFO -     LLM Analysis Complete:
2026-01-21 17:45:25,237 - [CORTEX AGENT] - INFO -       Trust Level: medium
2026-01-21 17:45:25,238 - [CORTEX AGENT] - INFO -       Risk Assessment: moderate
2026-01-21 17:45:25,239 - [CORTEX AGENT] - INFO -       Recommended Age: 120 days
2026-01-21 17:45:25,240 - [CORTEX AGENT] - INFO -       Strategy Notes: Fallback heuristic analysis (AI unavailable)
```

## Integration with Existing Pipeline

### Before Cortex Agent

```bash
# Old way: Direct execution
python main_v5.py --proxy user:pass@host:port --zip 10001 --age 90
```

### After Cortex Agent

```bash
# New way: Wrapped execution with autonomous pre-flight
python cortex_agent.py --proxy user:pass@host:port --zip 10001
# Age is now dynamically determined by LLM analysis
```

### Backward Compatibility

The old method still works! `cortex_agent.py` is a **wrapper**, not a replacement:

- ✅ `main_v5.py` can still be run directly
- ✅ Core modules unchanged
- ✅ No breaking changes to existing workflows
- ✅ Optional enhancement layer

## Constraints Respected

### Anti-Pivot Directive Compliance

✅ **No Core Module Modification**
- `core/genesis.py` - Untouched
- `core/browser_engine.py` - Untouched
- `core/tls_mimic.py` - Untouched
- `core/mcp_interface.py` - Existing (used, not modified)
- `core/intelligence.py` - Existing (used, not modified)
- All other core modules - Untouched

✅ **No Refactoring/Monkey-Patching**
- No imports modified
- No function signatures changed
- No class inheritance modifications
- Clean wrapper pattern only

✅ **Wrapper-Only Architecture**
- `cortex_agent.py` is standalone
- Imports core modules but doesn't modify them
- Uses subprocess to launch `main_v5.py`
- Full separation of concerns

## Security

### Implemented Safeguards

1. **Input Validation**
   - Proxy URL parsing and validation
   - Age parameter bounds checking
   - Zip code format validation

2. **Error Isolation**
   - Exceptions caught at each check level
   - Critical vs non-critical failure distinction
   - Graceful degradation to fallback modes

3. **Audit Trail**
   - Full status reports saved as JSON
   - Timestamp and error tracking
   - Configuration source attribution

4. **Principle of Least Privilege**
   - No sudo/elevated permissions required
   - File operations limited to logs/ and profiles/
   - Network operations validated and logged

## Testing

### Manual Testing

```bash
# Test environment validation
python cortex_agent.py --dry-run

# Test with proxy
python cortex_agent.py --dry-run --proxy user:pass@host:port

# Test with LLM (requires API key)
export OPENAI_API_KEY="sk-..."
python cortex_agent.py --dry-run

# Test force mode
python cortex_agent.py --force --dry-run
```

### Integration Testing

```bash
# Run existing test suite (should still pass)
python test_autonomous_cortex.py

# Test full pipeline
python cortex_agent.py --zip 10001
```

## Troubleshooting

### Issue: "MCP Infrastructure: OFFLINE"

**Cause**: uvx not installed or MCP servers not available

**Solutions**:
1. Install uv: `pip install uv`
2. Verify uvx: `uvx --version`
3. System will automatically fall back to TLS - no action required

### Issue: "MLA API: NOT REACHABLE"

**Cause**: Multilogin Agent not running

**Solutions**:
1. Start Multilogin desktop application
2. Verify API port (usually 35000)
3. Non-critical - profile export will need manual handling

### Issue: "Proxy validation failed"

**Cause**: Invalid proxy credentials or proxy offline

**Solutions**:
1. Verify proxy URL format: `user:pass@host:port`
2. Test proxy independently
3. Use `--force` to bypass if needed

### Issue: Age parameter not adjusting

**Symptom**: "Age parameter LOCKED (user override)"

**Reason**: User explicitly set `--age` parameter

**Behavior**: Intentional - user overrides take precedence over LLM

## Performance Characteristics

- **Startup Overhead**: ~2-5 seconds for pre-flight checks
- **MCP Probe**: ~1-2 seconds if available
- **LLM Analysis**: ~2-3 seconds with OpenAI API
- **Fallback Mode**: ~0.5 seconds (no API calls)
- **Total Pre-Flight**: ~3-10 seconds depending on mode

## Future Enhancements

Potential improvements (out of current scope):

- Multi-proxy health scoring and rotation
- Profile history and success rate tracking
- A/B testing framework for age parameters
- Real-time trust score monitoring
- Integration with additional MCP servers
- Dashboard for status report visualization

## Support

For issues or questions:

1. Check logs in `logs/cortex_agent.log`
2. Review status report in `logs/cortex_agent_status_*.json`
3. Run with `--dry-run` to isolate pre-flight issues
4. Use `--force` for emergency bypass

## Version

- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-01-21
- **Compatibility**: Python 3.8+

---

**Cortex Agent** - Autonomous Pre-Init Wrapper for PROMETHEUS-CORE Pipeline
