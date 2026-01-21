#!/usr/bin/env python3
"""
Test script to verify Autonomous Cortex implementation.
Tests basic import and initialization without requiring external dependencies.
"""

import sys
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("AutonomousCortexTest")

def test_imports():
    """Test that all new modules can be imported."""
    logger.info("Testing imports...")
    try:
        from core.mcp_interface import MCPClient
        from core.intelligence import IntelligenceCore
        logger.info("✓ All imports successful")
        return True
    except Exception as e:
        logger.error(f"✗ Import failed: {e}")
        return False

def test_mcp_client_init():
    """Test MCPClient initialization."""
    logger.info("Testing MCPClient initialization...")
    try:
        from core.mcp_interface import MCPClient
        client = MCPClient(logger)
        
        # Verify servers are defined
        assert "fetch" in client.servers
        assert "filesystem" in client.servers
        logger.info("✓ MCPClient initialization successful")
        return True
    except Exception as e:
        logger.error(f"✗ MCPClient init failed: {e}")
        return False

def test_intelligence_init():
    """Test IntelligenceCore initialization."""
    logger.info("Testing IntelligenceCore initialization...")
    try:
        from core.intelligence import IntelligenceCore
        brain = IntelligenceCore(logger)
        
        # Should work even without API key (fallback mode)
        logger.info("✓ IntelligenceCore initialization successful")
        return True
    except Exception as e:
        logger.error(f"✗ IntelligenceCore init failed: {e}")
        return False

async def test_intelligence_fallback():
    """Test IntelligenceCore fallback strategy."""
    logger.info("Testing IntelligenceCore fallback strategy...")
    try:
        from core.intelligence import IntelligenceCore
        brain = IntelligenceCore(logger)
        
        # Test with Amazon URL (should return 120 days)
        strategy = await brain.analyze_target("https://www.amazon.com", "sample data")
        
        assert "recommended_age_days" in strategy
        assert "trust_level" in strategy
        assert "risk_assessment" in strategy
        assert strategy["recommended_age_days"] == 120  # Amazon heuristic
        
        logger.info(f"✓ Fallback strategy working: {strategy}")
        return True
    except Exception as e:
        logger.error(f"✗ Fallback strategy failed: {e}")
        return False

def test_main_v5_integration():
    """Test that main_v5.py can be imported with new components."""
    logger.info("Testing main_v5.py integration...")
    try:
        # Note: This may fail if dependencies like nodriver aren't installed,
        # but the core autonomous modules should work
        from core.mcp_interface import MCPClient
        from core.intelligence import IntelligenceCore
        
        # Verify we can at least import and check the source
        with open("main_v5.py", "r") as f:
            content = f.read()
            
        # Check that imports are in the file
        assert "from core.mcp_interface import MCPClient" in content
        assert "from core.intelligence import IntelligenceCore" in content
        
        # Check that initialization happens
        assert "self.mcp = MCPClient(logger)" in content
        assert "self.brain = IntelligenceCore(logger)" in content
        
        # Check that Phase 0 exists
        assert "PHASE 0" in content
        assert "_autonomous_reconnaissance" in content
        
        logger.info("✓ main_v5.py integration successful (source verified)")
        return True
    except Exception as e:
        logger.error(f"✗ main_v5.py integration failed: {e}")
        return False

async def run_tests():
    """Run all tests."""
    logger.info("="*60)
    logger.info("AUTONOMOUS CORTEX - Integration Test Suite")
    logger.info("="*60)
    
    results = []
    
    # Synchronous tests
    results.append(("Imports", test_imports()))
    results.append(("MCPClient Init", test_mcp_client_init()))
    results.append(("IntelligenceCore Init", test_intelligence_init()))
    results.append(("main_v5 Integration", test_main_v5_integration()))
    
    # Async tests
    results.append(("Intelligence Fallback", await test_intelligence_fallback()))
    
    # Summary
    logger.info("="*60)
    logger.info("TEST RESULTS:")
    logger.info("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("="*60)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
