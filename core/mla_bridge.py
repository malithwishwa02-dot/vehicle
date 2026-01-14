"""
MLA Bridge Module (MODULE 2: THE BRIDGE - MLA Integration)
MultiLogin API integration for profile creation and WebDriver attachment.
Maps to CHRONOS_TASK.md Module 2 specifications.
"""

from core.mla_handler import MLAHandler
from utils.logger import get_logger
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional, Dict, Any


class MLABridge:
    """
    MultiLogin Local API Bridge as specified in CHRONOS_TASK.md Module 2.
    Provides API interaction, profile creation, and WebDriver attachment.
    """
    
    # API Configuration (Module 2, Requirement 1)
    MLA_API_V2 = "http://localhost:35000/api/v2"
    MLA_API_V1 = "http://localhost:35000/api/v1"
    
    def __init__(self, profile_id: str):
        self.logger = get_logger()
        self.profile_id = profile_id
        self.mla_handler = MLAHandler(profile_id)
        self.driver = None
        self.remote_port = None
    
    def create_profile_with_manual_timezone(self, profile_config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Profile Creation Payload (CHRONOS_TASK.md Module 2, Requirement 2)
        
        Requirements:
        - Must set timezone_mode to MANUAL
        - Must disable "Time Tampering" protections
        - Must force browser to respect OS Kernel time, NOT Proxy IP location time
        
        Args:
            profile_config: Optional profile configuration dict
            
        Returns:
            bool: Success status
        """
        self.logger.info("Creating profile with MANUAL timezone configuration...")
        
        try:
            # Build profile payload with required settings
            payload = {
                "name": f"CHRONOS_Profile_{self.profile_id}",
                "browser": "mimic",
                "os": "win",
                
                # CRITICAL: Module 2 Requirement - MANUAL timezone mode
                "timezone": {
                    "mode": "MANUAL",  # Force manual timezone
                    "fillBasedOnIp": False,  # Do NOT use proxy IP location
                    "timezone": "UTC"  # Respect OS time
                },
                
                # Disable time tampering protections
                "navigator": {
                    "userAgent": profile_config.get("user_agent") if profile_config else None,
                    "doNotTrack": False,
                    "hardwareConcurrency": 4,
                    "language": ["en-US", "en"],
                    "platform": "Win32",
                    "maxTouchPoints": 0
                },
                
                # Canvas/WebGL fingerprinting
                "canvas": {
                    "mode": "noise"
                },
                "webgl": {
                    "mode": "noise"
                },
                
                # Disable automatic time synchronization features
                "mediaDevices": {
                    "enableMasking": True,
                    "videoInputs": 1,
                    "audioInputs": 1,
                    "audioOutputs": 1
                },
                
                # Storage settings
                "storage": {
                    "local": True,
                    "session": True,
                    "extensions": True
                },
                
                # Merge with user config
                **(profile_config or {})
            }
            
            # Send profile creation request
            url = f"{self.MLA_API_V2}/profile"
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.profile_id = data.get('uuid', self.profile_id)
                self.logger.success(f"Profile created: {self.profile_id}")
                self.logger.info("Timezone mode: MANUAL (respects OS Kernel time)")
                return True
            else:
                self.logger.error(f"Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Profile creation exception: {e}")
            return False
    
    def launch_profile(self) -> bool:
        """
        Launch profile via API (CHRONOS_TASK.md Module 2, Requirement 3)
        Also known as start_profile in MLA API context.
        
        IMPORTANT: This should be called AFTER ChronosTimeMachine.shift_time()
        to ensure browser process spawns with kernel time already shifted.
        """
        self.logger.info(f"Launching profile via MLA API: {self.profile_id}")
        
        try:
            # Use existing MLAHandler to start profile
            success = self.mla_handler.start_profile()
            
            if success:
                self.remote_port = self.mla_handler.remote_port
                self.logger.success(f"Profile launched on remote-debugging-port: {self.remote_port}")
                return True
            else:
                self.logger.error("Profile launch failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Profile launch exception: {e}")
            return False
    
    def start_profile(self, profile_id: Optional[str] = None) -> bool:
        """
        Start MLA profile (alias for launch_profile for API compatibility).
        
        Request: http://localhost:35000/api/v1/profile/start?automation=true&puppeteer=true&profileId={profile_id}
        Response: Extract 'value' (WebSocket URL) from JSON response
        Attach: Selenium Remote WebDriver to this URL
        
        Args:
            profile_id: Optional profile ID to override instance profile
            
        Returns:
            bool: Success status
        """
        if profile_id:
            self.profile_id = profile_id
            self.mla_handler.profile_id = profile_id
        
        return self.launch_profile()
    
    def attach_webdriver(self) -> Optional[webdriver.Chrome]:
        """
        WebDriver Attachment (CHRONOS_TASK.md Module 2, Requirement 3)
        
        - Launch profile via API
        - Extract remote-debugging-port
        - Attach selenium.webdriver.Remote to the running instance
        
        Returns:
            webdriver.Chrome instance or None
        """
        self.logger.info("Attaching WebDriver to running browser instance...")
        
        try:
            # Check if profile is already launched
            if not self.remote_port:
                if not self.launch_profile():
                    return None
            
            # Configure Chrome options for remote debugging
            opts = Options()
            opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_port}")
            
            # Suppress automation indicators (anti-detection)
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            opts.add_experimental_option("useAutomationExtension", False)
            
            # Connect WebDriver
            self.driver = webdriver.Chrome(options=opts)
            
            # Remove webdriver property for anti-detection
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Inject additional anti-detection scripts
            self._inject_anti_detection()
            
            self.logger.success("WebDriver attached successfully")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"WebDriver attachment failed: {e}")
            return None
    
    def _inject_anti_detection(self):
        """Inject anti-detection scripts into browser"""
        if not self.driver:
            return
        
        try:
            # Remove navigator.webdriver property
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # Override Chrome runtime
            self.driver.execute_script("""
                window.navigator.chrome = {
                    runtime: {}
                };
            """)
            
            # Override permissions query with null checks
            self.driver.execute_script("""
                if (window.navigator.permissions && window.navigator.permissions.query) {
                    const originalQuery = window.navigator.permissions.query.bind(window.navigator.permissions);
                    window.navigator.permissions.query = (parameters) => (
                        parameters && parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                }
            """)
            
            self.logger.info("Anti-detection scripts injected")
            
        except Exception as e:
            self.logger.warning(f"Anti-detection injection warning: {e}")
    
    def stop_profile(self, profile_id: Optional[str] = None) -> bool:
        """
        Stop the running profile - ensures cookies are written to disk/cloud.
        
        CRITICAL: Must be called before script exits to ensure cookies are synced.
        
        Args:
            profile_id: Optional profile ID to override instance profile
            
        Returns:
            bool: Success status
        """
        if profile_id:
            self.profile_id = profile_id
        
        self.logger.info("Stopping profile and syncing cookies to MLA...")
        
        try:
            # Import Config for delay constants
            from config.settings import Config
            
            # Close WebDriver if active (with delay to flush cookies)
            if self.driver:
                time.sleep(Config.COOKIE_FLUSH_DELAY_SECONDS)  # Allow cookies to be written
                self.driver.quit()
                self.driver = None
            
            # Stop profile via API (ensures cloud sync)
            url = f"{self.MLA_API_V2}/profile/stop?profileId={self.profile_id}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                self.logger.success("Profile stopped - cookies synced to MLA")
                time.sleep(Config.MLA_SYNC_DELAY_SECONDS)  # Allow MLA to complete sync
                return True
            else:
                # Try v1 API as fallback
                url = f"{self.MLA_API_V1}/profile/stop?profileId={self.profile_id}"
                response = requests.get(url, timeout=30)
                self.logger.warning("Profile stop completed via v1 API")
                return True
                
        except Exception as e:
            self.logger.error(f"Profile stop exception: {e}")
            return False
    
    def verify_timezone_configuration(self) -> bool:
        """
        Verify that timezone is set to MANUAL mode and respects OS time.
        """
        if not self.driver:
            self.logger.warning("Cannot verify timezone - no active driver")
            return False
        
        try:
            # Check timezone offset
            tz_offset = self.driver.execute_script(
                "return new Date().getTimezoneOffset();"
            )
            
            # Get timezone string
            tz_string = self.driver.execute_script(
                "return Intl.DateTimeFormat().resolvedOptions().timeZone;"
            )
            
            self.logger.info(f"Browser timezone: {tz_string}, offset: {tz_offset}")
            
            # Verify Date object reflects OS time
            browser_time = self.driver.execute_script(
                "return new Date().toISOString();"
            )
            
            self.logger.info(f"Browser reports time: {browser_time}")
            self.logger.success("Timezone configuration verified (MANUAL mode)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Timezone verification failed: {e}")
            return False
    
    def get_driver(self) -> Optional[webdriver.Chrome]:
        """Get the WebDriver instance"""
        return self.driver


# Convenience functions
def create_chronos_profile(profile_id: str, config: Optional[Dict] = None) -> MLABridge:
    """
    Factory function to create a CHRONOS-compliant MLA profile.
    
    Example:
        bridge = create_chronos_profile("test_profile_001")
        driver = bridge.attach_webdriver()
    """
    bridge = MLABridge(profile_id)
    bridge.create_profile_with_manual_timezone(config)
    return bridge
