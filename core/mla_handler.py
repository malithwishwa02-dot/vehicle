import os
import json
"""
Multilogin API Controller v2.0
Direct interface with MLA Local API and browser automation
Level 9: Hardware Consistency Enforcement
"""
import requests
import time
import random
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from typing import List, Dict, Optional, Any

class MLAHandler:

        def inject_chronos_cookies(self, profile_id: str, cookie_json_path: str) -> bool:
            """
            Method 4 Kernel Time Shift: Inject Chronos-generated cookies into MLA profile with file timestamp shift.
            1. Reads the Chronos cookie jar (JSON).
            2. Uses os.utime() to set file timestamps to T-90 days (profile creation date).
            3. Calls MLA API /api/v2/profile/cookies/import to push cookies.
            4. Logs "Kernel Time Shift Applied" on success.
            """
            try:
                # Read cookies and extract creation date (T-90 days)
                with open(cookie_json_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                # Use profile age from config (default 90 days)
                profile_age_days = getattr(self.config, 'PROFILE_AGE_DAYS', 90)
                t_90_epoch = int(time.time()) - profile_age_days * 86400
                # Set file timestamps to T-90 days
                os.utime(cookie_json_path, (t_90_epoch, t_90_epoch))
                # Push cookies to MLA API
                url = f"{self.api_v2}/profile/cookies/import"
                payload = {
                    "profileId": profile_id,
                    "cookies": cookies
                }
                resp = requests.post(url, json=payload, timeout=10)
                if resp.status_code == 200:
                    self.logger.info("Kernel Time Shift Applied")
                    return True
                """
                MODULE: core/mla_handler.py
                STATUS: PATCHED (Prometheus v2.1)
                AUTHORITY: Dva.12

                PURPOSE:
                Acts as the bridge between the Orchestrator and the Anti-Detect Browser API (Multilogin/MLA).
                Now enforces ResilientClient usage to prevent API bans.
                """

                import json
                from typing import Dict, Optional, Any
                from core.resilient_api import ResilientClient
                from config.settings import MLA_URL, MLA_API_KEY # Assuming these exist in settings
        from config.settings import Config
        from utils.logger import get_logger
        
        self.config = Config
        self.logger = get_logger()
        
        # API endpoints
        self.api_v1 = Config.MLA_URL
        self.api_v2 = Config.MLA_URL_V2
    
    def validate_profile_config(self, profile_id: str) -> Dict[str, Any]:
        """
        Level 9 Pre-Flight Check: Validate profile configuration before operations.
        
        This function fetches the profile configuration from MLA API and validates:
        1. Canvas/WebGL noise settings (prefer "Real" over "Noise" mode)
        2. Hardware concurrency (CPU cores >= 4)
        3. General hardware consistency
        
        Args:
            profile_id: Multilogin profile ID to validate
            
        Returns:
            Dict with validation results: {
                'valid': bool,
                'warnings': List[str],
                'errors': List[str]
            }
        """
        validation = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Fetch profile data from MLA API with URL-encoded profile_id
            encoded_profile_id = quote(profile_id, safe='')
            url = f"{self.api_v2}/profile?profileId={encoded_profile_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                validation['errors'].append(f"Failed to fetch profile: HTTP {response.status_code}")
                validation['valid'] = False
                return validation
            
            profile_data = response.json()
            
            # Check Canvas/WebGL noise settings
            canvas_settings = profile_data.get('canvas', {})
            webgl_settings = profile_data.get('webgl', {})
            
            canvas_mode = canvas_settings.get('mode', '').lower()
            webgl_mode = webgl_settings.get('mode', '').lower()
            
            if canvas_mode == 'noise':
                validation['warnings'].append(
                    "⚠ LEVEL 9 RECOMMENDATION: Canvas is using 'Noise' mode. "
                    "For maximum consistency, consider using 'Real' or consistent noise settings."
                )
                self.logger.warning("⚠ Canvas: Noise mode detected (Level 9 prefers Real)")
            
            if webgl_mode == 'noise':
                validation['warnings'].append(
                    "⚠ LEVEL 9 RECOMMENDATION: WebGL is using 'Noise' mode. "
                    "For maximum consistency, consider using 'Real' or consistent noise settings."
                )
                self.logger.warning("⚠ WebGL: Noise mode detected (Level 9 prefers Real)")
            
            # Check navigator.hardwareConcurrency
            navigator_settings = profile_data.get('navigator', {})
            hardware_concurrency = navigator_settings.get('hardwareConcurrency', 0)
            
            if hardware_concurrency < 4:
                validation['warnings'].append(
                    f"⚠ LOW SPEC WARNING: navigator.hardwareConcurrency = {hardware_concurrency} (< 4 cores). "
                    "Modern systems typically have 4+ cores. Low-spec systems may be flagged."
                )
                self.logger.warning(f"⚠ Hardware Concurrency: {hardware_concurrency} cores (< 4)")
            
            # Run additional hardware validation
            hardware_validation = self.validate_hardware_config(profile_data)
            validation['warnings'].extend(hardware_validation.get('warnings', []))
            validation['errors'].extend(hardware_validation.get('errors', []))
            
            if hardware_validation.get('valid') is False:
                validation['valid'] = False
            
            # Log final validation status
            if validation['valid'] and not validation['warnings']:
                self.logger.info("✓ Profile Configuration: PASSED")
            elif validation['valid'] and validation['warnings']:
                self.logger.warning(f"⚠ Profile Configuration: PASSED (with {len(validation['warnings'])} warnings)")
            else:
                self.logger.error(f"❌ Profile Configuration: FAILED ({len(validation['errors'])} errors)")
            
        except Exception as e:
            validation['errors'].append(f"Profile validation exception: {e}")
            validation['valid'] = False
            self.logger.error(f"Profile validation error: {e}")
        
        return validation
    
    def validate_hardware_config(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 9 Hardware Consistency Validation
        
        Validates hardware configuration to ensure realistic fingerprints.
        Returns validation results with warnings/errors.
        
        Args:
            profile_data: Profile configuration dictionary with structure:
                {
                    'os': str,              # Operating system (e.g., 'win', 'mac', 'linux')
                    'navigator': {
                        'deviceMemory': int # RAM in GB (e.g., 4, 8, 16)
                    },
                    'webgl': {
                        'vendor': str,      # WebGL vendor (e.g., 'Intel Inc.')
                        'renderer': str     # WebGL renderer (e.g., 'Intel Iris OpenGL')
                    },
                    'mediaDevices': {
                        'audioInputs': int, # Number of audio input devices
                        'audioOutputs': int # Number of audio output devices
                    }
                }
                
        Returns:
            Dict with validation results: {
                'valid': bool,              # True if all critical checks pass
                'warnings': List[str],      # Non-critical issues
                'errors': List[str]         # Critical failures
            }
            
        Example:
            >>> handler = MLAHandler('profile_id')
            >>> result = handler.validate_hardware_config({
            ...     'os': 'win',
            ...     'navigator': {'deviceMemory': 8},
            ...     'webgl': {'vendor': 'Intel Inc.', 'renderer': 'Intel Iris'},
            ...     'mediaDevices': {'audioInputs': 1}
            ... })
            >>> print(result['valid'])
            True
        """
        validation = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Extract hardware configuration
            os_type = profile_data.get('os', 'win').lower()
            navigator = profile_data.get('navigator', {})
            webgl = profile_data.get('webgl', {})
            media_devices = profile_data.get('mediaDevices', {})
            
            # Check 1: WebGL Vendor validation for Windows
            if 'win' in os_type:
                webgl_vendor = webgl.get('vendor', '')
                webgl_renderer = webgl.get('renderer', '')
                
                # Flag SwiftShader (software renderer - bot indicator)
                if 'swiftshader' in webgl_vendor.lower() or 'swiftshader' in webgl_renderer.lower():
                    validation['errors'].append(
                        "CRITICAL: WebGL using SwiftShader (software renderer). "
                        "This is a major bot detection flag. Use hardware acceleration."
                    )
                    validation['valid'] = False
                    self.logger.error("❌ Hardware Check Failed: SwiftShader detected")
                
                # Flag VMware (virtualization indicator)
                if 'vmware' in webgl_vendor.lower() or 'vmware' in webgl_renderer.lower():
                    validation['errors'].append(
                        "CRITICAL: VMware GPU detected. This indicates virtualization. "
                        "Use native hardware or proper GPU passthrough."
                    )
                    validation['valid'] = False
                    self.logger.error("❌ Hardware Check Failed: VMware GPU detected")
            
            # Check 2: RAM validation
            device_memory = navigator.get('deviceMemory', 0)
            if device_memory > 0 and device_memory < 4:
                validation['warnings'].append(
                    f"LOW TRUST: Device memory is {device_memory}GB (< 4GB). "
                    "Low-spec systems may be flagged by advanced fingerprinting."
                )
                self.logger.warning(f"⚠ Low Trust: RAM = {device_memory}GB (< 4GB)")
            
            # Check 3: Audio inputs validation
            # Use None as default to detect when key is actually missing vs explicitly set to 0
            audio_inputs = media_devices.get('audioInputs', None)
            if audio_inputs is not None and audio_inputs == 0:
                validation['warnings'].append(
                    "BOT FLAG: No audio input devices detected. "
                    "Real systems typically have at least 1 microphone. This may trigger bot detection."
                )
                self.logger.warning("⚠ Bot Flag: Audio Inputs = 0")
            
            # Log validation results
            if validation['valid'] and not validation['warnings']:
                self.logger.success("✓ Hardware Consistency: PASSED")
            elif validation['valid'] and validation['warnings']:
                self.logger.warning(f"⚠ Hardware Consistency: PASSED (with {len(validation['warnings'])} warnings)")
            else:
                self.logger.error(f"❌ Hardware Consistency: FAILED ({len(validation['errors'])} errors)")
            
        except Exception as e:
            validation['errors'].append(f"Validation exception: {e}")
            validation['valid'] = False
            self.logger.error(f"Hardware validation error: {e}")
        
        return validation
    
    def start_profile(self) -> bool:
        """
        Start Multilogin profile and attach Selenium driver.
        
        API Specification (MLA Local API v1):
        GET http://localhost:35000/api/v1/profile/start?automation=true&puppeteer=true&profileId={profile_id}
        
        The automation=true and puppeteer=true flags ensure proper WebDriver compatibility.
        """
        self.logger.info(f"Starting Profile: {self.profile_id}")
        
        # URL-encode profile_id for safe URL construction
        encoded_profile_id = quote(self.profile_id, safe='')
        
        # Try v1 API with automation and puppeteer flags (MLA Local API specification)
        url = f"{self.api_v1}/profile/start?automation=true&puppeteer=true&profileId={encoded_profile_id}"
        
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if 'value' in data:
                # Extract the WebSocket URL or debugging port
                if isinstance(data['value'], dict) and 'port' in data['value']:
                    self.remote_port = data['value']['port']
                else:
                    self.remote_port = data['value']
                
                self.logger.success(f"Profile started (v1 API) on port: {self.remote_port}")
                
                # Attach Selenium
                return self._attach_selenium()
            
            # Fallback to v2 API
            url = f"{self.api_v2}/profile/start?profileId={encoded_profile_id}"
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if 'value' in data:
                if isinstance(data['value'], dict) and 'port' in data['value']:
                    self.remote_port = data['value']['port']
                else:
                    self.remote_port = data['value']
                self.logger.success(f"Profile started (v2 API) on port: {self.remote_port}")
                return self._attach_selenium()
            
            self.logger.error(f"Failed to start profile: {data}")
            return False
            
        except Exception as e:
            self.logger.error(f"MLA API Error: {e}")
            return False
    
    def _attach_selenium(self) -> bool:
        """Attach Selenium WebDriver to running browser"""
        try:
            # Configure Chrome options for remote debugging
            opts = Options()
            opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_port}")
            
            # Suppress automation indicators
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            opts.add_experimental_option("useAutomationExtension", False)
            
            # Connect driver
            self.driver = webdriver.Chrome(options=opts)
            
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Level 9 Hardware Consistency Check
            try:
                hardware_concurrency = self.driver.execute_script("return navigator.hardwareConcurrency;")
                self.logger.info(f"[Level 9] navigator.hardwareConcurrency = {hardware_concurrency}")
                
                if hardware_concurrency < 4:
                    self.logger.warning(f"[WARNING] LOW TRUST HARDWARE: {hardware_concurrency} cores detected (< 4)")
                    self.logger.warning("Modern systems typically have 4+ cores. Low-spec hardware may trigger detection.")
            except Exception as e:
                self.logger.warning(f"Could not check hardware concurrency: {e}")
            
            self.logger.success("Browser Driver Attached")
            return True
            
        except WebDriverException as e:
            self.logger.error(f"Selenium attachment failed: {e}")
            return False
    
    def seed_cookies(self, deep_seed: bool = False):
        """
        Visit trust anchors to generate aged cookie timestamps
        
        Args:
            deep_seed: Use extended anchor list for deeper patina
        """
        if not self.driver:
            self.logger.error("No driver attached!")
            return
        
        anchors = self.config.TRUST_ANCHORS
        class MLAHandler:
            def __init__(self):
                # Initialize the Resilient Client (Anti-Ban Logic)
                self.client = ResilientClient(base_url=MLA_URL, api_key=MLA_API_KEY)

            def start_profile(self, profile_id: str) -> Optional[str]:
                """
                Starts a browser profile via MLX/MLA API.
                Returns the WebSocket URL (Puppeteer endpoint) or None on failure.
                """
                endpoint = f"v2/profile/start?profileId={profile_id}&automation=true"
                response = self.client.request("GET", endpoint)
                if response and "value" in response:
                    return response["value"] # Usually the WebSocket URL
                return None

            def stop_profile(self, profile_id: str) -> bool:
                """Stops the profile safely."""
                endpoint = f"v2/profile/stop?profileId={profile_id}"
                response = self.client.request("GET", endpoint)
                return response is not None

            def get_active_profiles(self) -> list:
                """Fetches list of currently running profiles."""
                endpoint = "v2/profile/active"
                response = self.client.request("GET", endpoint)
                return response if isinstance(response, list) else []

            def update_profile_cookies(self, profile_id: str, cookies: list) -> bool:
                """Injects the Level 9 Golden Cookies."""
                endpoint = "v2/profile/cookies"
                payload = {
                    "profileId": profile_id,
                    "cookies": cookies
                }
                response = self.client.request("POST", endpoint, data=payload)
                return response is not None

        # Singleton Instance
        mla = MLAHandler()
            Number of successfully injected cookies
        """
        if not self.driver:
            return 0
        
        injected = 0
        for cookie in cookies:
            try:
                # Ensure required fields
                if 'name' in cookie and 'value' in cookie:
                    # Add domain if missing
                    if 'domain' not in cookie:
                        current_domain = self.driver.execute_script("return document.domain;")
                        cookie['domain'] = current_domain
                    
                    self.driver.add_cookie(cookie)
                    injected += 1
                    
            except Exception as e:
                self.logger.warning(f"Cookie injection failed: {e}")
        
        self.logger.info(f"Injected {injected}/{len(cookies)} cookies")
        return injected
    
    def execute_journey(self, journey_type: str = "standard"):
        """
        Execute predefined browsing journeys for natural history
        
        Args:
            journey_type: Type of journey (standard, shopping, social, news)
        """
        journeys = {
            "standard": [
                "https://www.google.com/search?q=weather",
                "https://www.youtube.com",
                "https://www.wikipedia.org/wiki/Main_Page",
                "https://www.reddit.com"
            ],
            "shopping": [
                "https://www.amazon.com",
                "https://www.ebay.com",
                "https://www.walmart.com",
                "https://www.bestbuy.com"
            ],
            "social": [
                "https://www.facebook.com",
                "https://www.twitter.com",
                "https://www.instagram.com",
                "https://www.linkedin.com"
            ],
            "news": [
                "https://www.cnn.com",
                "https://www.bbc.com",
                "https://www.reuters.com",
                "https://www.apnews.com"
            ]
        }
        
        urls = journeys.get(journey_type, journeys["standard"])
        
        self.logger.info(f"Executing {journey_type} journey...")
        
        for url in urls:
            try:
                self.driver.get(url)
                
                # Varied dwell times
                dwell = random.uniform(3, 8)
                time.sleep(dwell)
                
                # Natural scrolling pattern
                for _ in range(random.randint(1, 3)):
                    scroll = random.randint(100, 400)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll});")
                    time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                self.logger.warning(f"Journey step failed: {e}")
    
    def stop_profile(self):
        """Stop Multilogin profile and cleanup - ensures cookies are written to disk/cloud"""
        self.logger.info("Stopping Profile and syncing cookies...")
        
        # Close Selenium driver first to ensure all cookies are flushed
        if self.driver:
            try:
                # Give browser time to write cookies to disk
                time.sleep(self.config.COOKIE_FLUSH_DELAY_SECONDS)
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        # URL-encode profile_id for safe URL construction
        encoded_profile_id = quote(self.profile_id, safe='')
        
        # Stop profile via API to ensure cloud sync
        try:
            # Try v2 API first
            url = f"{self.api_v2}/profile/stop?profileId={encoded_profile_id}"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                self.logger.success("Profile stopped - cookies synced to MLA cloud/disk")
                time.sleep(self.config.MLA_SYNC_DELAY_SECONDS)  # Allow file locks to release
                return
        except:
            pass
        
        # Fallback to v1 API
        try:
            url = f"{self.api_v1}/profile/stop?profileId={encoded_profile_id}"
            requests.get(url, timeout=10)
            self.logger.success("Profile stopped (v1 API) - cookies synced")
        except:
            self.logger.warning("Profile stop API call failed - cookies may not be fully synced")
        
        time.sleep(self.config.MLA_SYNC_DELAY_SECONDS)  # Allow file locks to release
    
    def cleanup(self):
        """Emergency cleanup"""
        try:
            self.stop_profile()
        except:
            pass