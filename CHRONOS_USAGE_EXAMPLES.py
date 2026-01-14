"""
CHRONOS-MLA Framework Usage Examples
Based on CHRONOS_TASK.md specifications

This file demonstrates how to use the CHRONOS-MLA modules that were
implemented according to the CHRONOS_TASK.md specification.

WARNING: This code requires Windows 10/11 with Administrator privileges.
"""

# Example 1: Complete CHRONOS workflow
def example_complete_workflow():
    """
    Complete workflow from CHRONOS_TASK.md:
    1. Network Lock (MODULE 1)
    2. Time Shift (MODULE 1)
    3. Profile Creation (MODULE 2)
    4. Journey Behavior (MODULE 3)
    5. Forensic Scrubbing (MODULE 4)
    6. Cleanup (MODULE 5)
    """
    from core.network_lock import NetworkLock
    from core.time_manager import TimeManager
    from core.mla_bridge import MLABridge
    from modules.journey import PoissonJourney, JourneyBehavior
    from core.forensics import ForensicScrubber
    from core.cleanup import CleanupManager
    
    try:
        # PHASE 1: THE VOID - Network & Time Control
        print("=" * 60)
        print("PHASE 1: THE VOID (Network & Time Control)")
        print("=" * 60)
        
        # Step 1.1: Network Lock
        network_lock = NetworkLock()
        network_lock.enable_full_isolation()
        
        # Step 1.2: Time Shift
        time_manager = TimeManager()
        time_manager.shift_time(days_to_shift=90)  # Go back 90 days
        
        # PHASE 2: THE BRIDGE - MLA Integration
        print("\n" + "=" * 60)
        print("PHASE 2: THE BRIDGE (MLA Integration)")
        print("=" * 60)
        
        # Step 2.1: Create profile with MANUAL timezone
        profile_id = "chronos_test_profile_001"
        mla_bridge = MLABridge(profile_id)
        mla_bridge.create_profile_with_manual_timezone()
        
        # Step 2.2: Launch profile and attach WebDriver
        driver = mla_bridge.attach_webdriver()
        
        if not driver:
            raise Exception("Failed to attach WebDriver")
        
        # Step 2.3: Verify timezone configuration
        mla_bridge.verify_timezone_configuration()
        
        # PHASE 3: THE JOURNEY - Entropy & Behavior
        print("\n" + "=" * 60)
        print("PHASE 3: THE JOURNEY (Entropy & Behavior)")
        print("=" * 60)
        
        # Step 3.1: Generate Poisson-distributed time jumps
        poisson = PoissonJourney(total_days=90)
        time_jumps = poisson.generate_time_jumps(num_segments=12)
        
        print(f"Generated {len(time_jumps)} time jump segments")
        
        # Step 3.2: Execute behavioral patterns
        journey = JourneyBehavior(driver)
        
        # Navigate to a test page
        driver.get("https://www.example.com")
        
        # Execute human-like behaviors
        journey.random_scroll()  # Scroll with regression
        journey.mouse.random_movement()  # Bezier mouse movement
        journey.loss_of_focus()  # Trigger visibilityState: hidden
        
        # PHASE 4: THE LOCK - Forensic Scrubbing
        print("\n" + "=" * 60)
        print("PHASE 4: THE LOCK (Forensic Scrubbing)")
        print("=" * 60)
        
        # Close browser before scrubbing
        mla_bridge.stop_profile()
        
        # Execute forensic scrubbing (WHILE time is still backdated)
        forensic_scrubber = ForensicScrubber()
        forensic_scrubber.scrub_timestamps(profile_id)
        forensic_scrubber.scrub_cookies_db(profile_id)
        
        # PHASE 5: RESURRECTION - Cleanup
        print("\n" + "=" * 60)
        print("PHASE 5: RESURRECTION (Cleanup)")
        print("=" * 60)
        
        cleanup_manager = CleanupManager()
        cleanup_manager.full_cleanup(validate=True)
        
        print("\n" + "=" * 60)
        print("CHRONOS WORKFLOW COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        
        # Emergency cleanup
        from core.cleanup import emergency_restore
        emergency_restore()


# Example 2: Module 1 - Network Lock only
def example_network_lock():
    """
    Example of using Network Lock module (CHRONOS_TASK.md Module 1)
    """
    from core.network_lock import NetworkLock
    
    # Create and engage network lock
    lock = NetworkLock()
    
    # Kill W32Time service
    lock.kill_w32time()
    
    # Block NTP traffic (UDP Port 123)
    lock.block_ntp()
    
    # Verify isolation is active
    if lock.verify_isolation():
        print("Network isolation VERIFIED")
    
    # Restore network when done
    lock.restore_network()


# Example 3: Module 1 - Time Manager only
def example_time_manager():
    """
    Example of using Time Manager module (CHRONOS_TASK.md Module 1)
    """
    from core.time_manager import TimeManager
    
    # Create time manager
    tm = TimeManager()
    
    # Shift time back 90 days
    tm.shift_time(days_to_shift=90)
    
    # Get current (shifted) time
    current_time = tm.get_current_time()
    print(f"System time: {current_time}")
    
    # Restore original time
    tm.restore_original_time()


# Example 4: Module 2 - MLA Bridge
def example_mla_bridge():
    """
    Example of using MLA Bridge module (CHRONOS_TASK.md Module 2)
    """
    from core.mla_bridge import MLABridge
    
    profile_id = "test_profile"
    bridge = MLABridge(profile_id)
    
    # Create profile with MANUAL timezone mode
    profile_config = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "proxy": None
    }
    bridge.create_profile_with_manual_timezone(profile_config)
    
    # Launch profile
    bridge.launch_profile()
    
    # Attach WebDriver
    driver = bridge.attach_webdriver()
    
    if driver:
        # Use driver for automation
        driver.get("https://www.example.com")
        
        # Verify timezone configuration
        bridge.verify_timezone_configuration()
        
        # Stop profile when done
        bridge.stop_profile()


# Example 5: Module 3 - Journey Behavior
def example_journey_behavior():
    """
    Example of using Journey module (CHRONOS_TASK.md Module 3)
    """
    from modules.journey import (
        HumanMouse,
        JourneyBehavior,
        PoissonJourney,
        generate_poisson_schedule
    )
    from selenium import webdriver
    
    # Create WebDriver (assumes MLA profile is running)
    driver = webdriver.Chrome()
    
    # Create HumanMouse for Bezier curve movement
    mouse = HumanMouse(driver)
    mouse.move_to(target_x=500, target_y=300, duration=1.5)
    mouse.random_movement()
    
    # Create JourneyBehavior for human-like patterns
    journey = JourneyBehavior(driver)
    journey.random_scroll()  # Scroll with occasional regression
    journey.loss_of_focus()  # Switch to about:blank
    journey.random_click()   # Click random elements
    journey.typing_simulation("search query")
    
    # Generate Poisson-distributed time jumps
    schedule = generate_poisson_schedule(days=90, segments=12)
    
    for jump in schedule:
        print(f"Jump {jump['index']}: T-{jump['days_ago']:.1f} days")
        print(f"  Activity level: {jump['activity_level']}")
        print(f"  Actions: {jump['actions']}")
    
    driver.quit()


# Example 6: Module 5 - Cleanup
def example_cleanup():
    """
    Example of using Cleanup module (CHRONOS_TASK.md Module 5)
    """
    from core.cleanup import CleanupManager, emergency_restore
    
    # Create cleanup manager
    cleanup = CleanupManager()
    
    # Restore system services
    cleanup.restore_system()
    
    # Validate time synchronization
    # This will raise SystemExit if skew > 1 second
    try:
        cleanup.validate_time_sync(max_skew_seconds=1)
        print("Time synchronization validated!")
    except SystemExit as e:
        print(f"Time sync failed: {e}")
    
    # Full cleanup with validation
    cleanup.full_cleanup(validate=True)


# Example 7: Factory Functions
def example_factory_functions():
    """
    Example of using convenience factory functions
    """
    from core.network_lock import engage_network_lock
    from core.time_manager import shift_system_time
    from core.mla_bridge import create_chronos_profile
    from modules.journey import generate_poisson_schedule
    from core.cleanup import cleanup_and_restore
    
    # Quick network lock
    lock = engage_network_lock()
    
    # Quick time shift
    tm = shift_system_time(90)
    
    # Quick profile creation
    bridge = create_chronos_profile("test_profile")
    
    # Quick schedule generation
    schedule = generate_poisson_schedule(90, 12)
    
    # Quick cleanup
    cleanup = cleanup_and_restore(validate=True)


# Example 8: Error Handling and Cleanup
def example_with_error_handling():
    """
    Example showing proper error handling with emergency cleanup
    """
    from core.network_lock import NetworkLock
    from core.time_manager import TimeManager
    from core.cleanup import emergency_restore
    
    try:
        # Initialize components
        network_lock = NetworkLock()
        time_manager = TimeManager()
        
        # Enable isolation and shift time
        network_lock.enable_full_isolation()
        time_manager.shift_time(90)
        
        # ... do work ...
        
        # Normal cleanup
        from core.cleanup import CleanupManager
        cleanup = CleanupManager()
        cleanup.full_cleanup(validate=True)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user!")
        emergency_restore()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        emergency_restore()
        
    finally:
        print("Cleanup completed")


if __name__ == "__main__":
    print(__doc__)
    print("\nAvailable examples:")
    print("1. example_complete_workflow() - Full CHRONOS workflow")
    print("2. example_network_lock() - Network isolation only")
    print("3. example_time_manager() - Time manipulation only")
    print("4. example_mla_bridge() - MLA profile creation")
    print("5. example_journey_behavior() - Human-like behaviors")
    print("6. example_cleanup() - System restoration")
    print("7. example_factory_functions() - Quick convenience functions")
    print("8. example_with_error_handling() - Proper error handling")
    print("\nWARNING: Requires Windows 10/11 + Admin privileges")
