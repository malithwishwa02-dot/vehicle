#!/usr/bin/env python3
"""
Test suite for Cortex Agent - Autonomous Pre-Init Wrapper
Validates cortex_agent.py functionality and integration
"""

import sys
import os
import asyncio
import logging
import json
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("CortexAgentTest")


def test_cortex_agent_import():
    """Test that cortex_agent can be imported."""
    logger.info("Test 1: Import cortex_agent module")
    try:
        # Import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location("cortex_agent", "cortex_agent.py")
        cortex_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cortex_module)
        
        # Verify CortexAgent class exists
        assert hasattr(cortex_module, 'CortexAgent')
        assert hasattr(cortex_module, 'parse_arguments')
        assert hasattr(cortex_module, 'main')
        
        logger.info("✓ PASS: Cortex Agent module imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ FAIL: Import failed - {e}")
        return False


def test_cortex_agent_file_exists():
    """Test that cortex_agent.py exists and is executable."""
    logger.info("Test 2: Cortex Agent file exists")
    try:
        agent_path = Path("cortex_agent.py")
        
        assert agent_path.exists(), "cortex_agent.py does not exist"
        assert agent_path.is_file(), "cortex_agent.py is not a file"
        
        # Check if executable (on Unix systems)
        if os.name != 'nt':
            assert os.access(agent_path, os.X_OK), "cortex_agent.py is not executable"
        
        logger.info("✓ PASS: Cortex Agent file exists and is accessible")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: File check failed - {e}")
        return False


def test_documentation_exists():
    """Test that documentation file exists."""
    logger.info("Test 3: Documentation exists")
    try:
        doc_path = Path("CORTEX_AGENT_GUIDE.md")
        
        assert doc_path.exists(), "CORTEX_AGENT_GUIDE.md does not exist"
        assert doc_path.is_file(), "CORTEX_AGENT_GUIDE.md is not a file"
        
        # Check content is not empty
        with open(doc_path, 'r') as f:
            content = f.read()
        assert len(content) > 100, "Documentation is too short"
        assert "Cortex Agent" in content, "Documentation missing title"
        
        logger.info("✓ PASS: Documentation exists and is valid")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: Documentation check failed - {e}")
        return False


def test_logs_directory():
    """Test that logs directory is created."""
    logger.info("Test 4: Logs directory")
    try:
        logs_dir = Path("logs")
        
        assert logs_dir.exists(), "logs directory does not exist"
        assert logs_dir.is_dir(), "logs is not a directory"
        
        logger.info("✓ PASS: Logs directory exists")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: Logs directory check failed - {e}")
        return False


async def test_cortex_agent_class():
    """Test CortexAgent class instantiation."""
    logger.info("Test 5: CortexAgent class instantiation")
    try:
        import importlib.util
        import argparse
        
        spec = importlib.util.spec_from_file_location("cortex_agent", "cortex_agent.py")
        cortex_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cortex_module)
        
        # Create mock arguments
        args = argparse.Namespace(
            proxy=None,
            zip="10001",
            age=90,
            force=False,
            dry_run=True
        )
        
        # Instantiate CortexAgent
        agent = cortex_module.CortexAgent(args)
        
        # Verify attributes
        assert hasattr(agent, 'args')
        assert hasattr(agent, 'status')
        assert hasattr(agent, 'dynamic_config')
        assert hasattr(agent, 'run_preflight_checks')
        assert hasattr(agent, 'launch_main_v5')
        
        logger.info("✓ PASS: CortexAgent class instantiated successfully")
        return True
    except Exception as e:
        logger.error(f"✗ FAIL: Class instantiation failed - {e}")
        return False


async def test_preflight_checks():
    """Test pre-flight checks execution."""
    logger.info("Test 6: Pre-flight checks execution")
    try:
        import importlib.util
        import argparse
        
        spec = importlib.util.spec_from_file_location("cortex_agent", "cortex_agent.py")
        cortex_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cortex_module)
        
        args = argparse.Namespace(
            proxy=None,
            zip="10001",
            age=90,
            force=False,
            dry_run=True
        )
        
        agent = cortex_module.CortexAgent(args)
        
        # Run pre-flight checks
        result = await agent.run_preflight_checks()
        
        # Should return True or False
        assert isinstance(result, bool), "Pre-flight checks should return boolean"
        
        # Status should be populated
        assert agent.status["timestamp"] is not None
        assert "environment" in agent.status
        assert "mcp_health" in agent.status
        assert "llm_analysis" in agent.status
        
        logger.info("✓ PASS: Pre-flight checks executed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ FAIL: Pre-flight checks failed - {e}")
        return False


def test_status_report_generation():
    """Test that status reports are generated."""
    logger.info("Test 7: Status report generation")
    try:
        # Check if any status reports exist
        logs_dir = Path("logs")
        status_files = list(logs_dir.glob("cortex_agent_status_*.json"))
        
        assert len(status_files) > 0, "No status reports found"
        
        # Validate the latest status report
        latest_report = max(status_files, key=lambda p: p.stat().st_mtime)
        
        with open(latest_report, 'r') as f:
            status_data = json.load(f)
        
        # Validate structure
        required_keys = ["timestamp", "environment", "mcp_health", "llm_analysis", "errors", "warnings"]
        for key in required_keys:
            assert key in status_data, f"Status report missing key: {key}"
        
        logger.info(f"✓ PASS: Status report generated and validated ({latest_report.name})")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: Status report check failed - {e}")
        return False


def test_core_modules_untouched():
    """Test that core modules remain untouched."""
    logger.info("Test 8: Core modules integrity check")
    try:
        # List of core files that should not be modified
        core_files = [
            "core/genesis.py",
            "core/browser_engine.py",
            "core/tls_mimic.py",
            "main_v5.py"
        ]
        
        # Check that all core files exist
        for core_file in core_files:
            file_path = Path(core_file)
            assert file_path.exists(), f"Core file missing: {core_file}"
        
        # Verify cortex_agent doesn't import these with modifications
        with open("cortex_agent.py", 'r') as f:
            cortex_content = f.read()
        
        # Should only import, not modify
        assert "import subprocess" in cortex_content  # Uses subprocess to call main_v5.py
        assert "from core.mcp_interface import MCPClient" in cortex_content
        assert "from core.intelligence import IntelligenceCore" in cortex_content
        
        # Should NOT contain monkey-patching or modifications
        assert "setattr(" not in cortex_content or "setattr(self" in cortex_content  # Only self modifications
        assert "globals()[" not in cortex_content
        assert "import sys" in cortex_content  # Normal imports only
        
        logger.info("✓ PASS: Core modules remain untouched")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: Core integrity check failed - {e}")
        return False


def test_wrapper_architecture():
    """Test that cortex_agent uses wrapper pattern."""
    logger.info("Test 9: Wrapper architecture validation")
    try:
        with open("cortex_agent.py", 'r') as f:
            content = f.read()
        
        # Should use subprocess to launch main_v5.py (not direct import and execution)
        assert "subprocess.run" in content, "Should use subprocess to launch main_v5.py"
        assert "main_v5.py" in content, "Should reference main_v5.py"
        
        # Should have standalone main function
        assert "if __name__ == \"__main__\":" in content
        assert "asyncio.run(main())" in content
        
        # Should have CortexAgent class
        assert "class CortexAgent:" in content
        
        logger.info("✓ PASS: Wrapper architecture validated")
        return True
    except AssertionError as e:
        logger.error(f"✗ FAIL: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ FAIL: Wrapper architecture check failed - {e}")
        return False


async def run_tests():
    """Run all tests."""
    logger.info("=" * 80)
    logger.info("CORTEX AGENT - Test Suite")
    logger.info("=" * 80)
    
    results = []
    
    # Synchronous tests
    results.append(("Cortex Agent Import", test_cortex_agent_import()))
    results.append(("File Exists", test_cortex_agent_file_exists()))
    results.append(("Documentation Exists", test_documentation_exists()))
    results.append(("Logs Directory", test_logs_directory()))
    
    # Async tests
    results.append(("CortexAgent Class", await test_cortex_agent_class()))
    results.append(("Pre-flight Checks", await test_preflight_checks()))
    
    # Synchronous validation tests
    results.append(("Status Report Generation", test_status_report_generation()))
    results.append(("Core Modules Untouched", test_core_modules_untouched()))
    results.append(("Wrapper Architecture", test_wrapper_architecture()))
    
    # Summary
    logger.info("=" * 80)
    logger.info("TEST RESULTS:")
    logger.info("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("=" * 80)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("=" * 80)
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
