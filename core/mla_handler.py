"""
Multilogin API Controller
Interfaces with MLA Local API v2 and manages browser automation via Selenium
"""

import requests
import logging
import time
import json
from typing import Optional, Dict, Any, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

logger = logging.getLogger(__name__)


class MultiloginController:
    """
    Controller for Multilogin Local API interaction and browser automation
    Does NOT use undetected_chromedriver - connects to MLA-provided browser
    """
    
    MLA_API_BASE = "http://127.0.0.1:35000/api/v2"
    MLA_API_TIMEOUT = 30
    
    def __init__(self, mla_port: int = 35000):
        """
        Initialize Multilogin controller
        
        Args:
            mla_port: Local API port (default: 35000)
        """
        self.api_base = f"http://127.0.0.1:{mla_port}/api/v2"
        self.current_profile_id: Optional[str] = None
        self.driver: Optional[webdriver.Chrome] = None
        self.remote_port: Optional[int] = None
        
        # Verify API accessibility
        if not self._verify_api():
            raise ConnectionError(
                f"Multilogin API not accessible at {self.api_base}. "
                "Ensure Multilogin is running with Local API enabled."
            )
    
    def _verify_api(self) -> bool:
        """Verify Multilogin Local API is accessible"""
        try:
            response = requests.get(
                f"{self.api_base}/profile",
                timeout=5
            )
            return response.status_code in [200, 401]  # 401 means API exists but needs auth
        except requests.RequestException:
            return False
    
    def start_profile(self, profile_id: str, headless: bool = False) -> Dict[str, Any]:
        """
        Start a Multilogin profile via Local API
        
        Args:
            profile_id: MLA profile identifier
            headless: Run browser in headless mode
            
        Returns:
            API response containing remote debugging port
        """
        try:
            # Prepare start request
            endpoint = f"{self.api_base}/profile/start"
            params = {
                "profileId": profile_id,
                "headless": headless
            }
            
            logger.info(f"Starting profile: {profile_id}")
            
            # Make API request
            response = requests.get(
                endpoint,
                params=params,
                timeout=self.MLA_API_TIMEOUT
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Profile start failed: {response.text}")
            
            data = response.json()
            
            # Extract remote debugging port
            if "value" in data and "port" in data["value"]:
                self.remote_port = data["value"]["port"]
                self.current_profile_id = profile_id
                logger.info(f"Profile started on debugging port: {self.remote_port}")
                return data["value"]
            else:
                raise ValueError(f"Invalid API response format: {data}")
                
        except Exception as e:
            logger.error(f"Failed to start profile: {str(e)}")
            raise
    
    def stop_profile(self, profile_id: Optional[str] = None) -> bool:
        """
        Stop a Multilogin profile
        
        Args:
            profile_id: Profile to stop (uses current if not specified)
            
        Returns:
            Success status
        """
        target_id = profile_id or self.current_profile_id
        
        if not target_id:
            logger.warning("No profile ID specified for stop operation")
            return False
        
        try:
            # Close Selenium driver first if exists
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
            # Stop profile via API
            endpoint = f"{self.api_base}/profile/stop"
            params = {"profileId": target_id}
            
            response = requests.get(
                endpoint,
                params=params,
                timeout=self.MLA_API_TIMEOUT
            )
            
            if response.status_code == 200:
                logger.info(f"Profile stopped: {target_id}")
                if target_id == self.current_profile_id:
                    self.current_profile_id = None
                    self.remote_port = None
                return True
            else:
                logger.error(f"Stop profile failed: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error stopping profile: {str(e)}")
            return False
    
    def connect_selenium(self) -> webdriver.Chrome:
        """
        Connect Selenium WebDriver to running MLA browser instance
        Uses standard ChromeOptions with debugger_address
        
        Returns:
            Configured Chrome WebDriver instance
        """
        if not self.remote_port:
            raise RuntimeError("No profile started. Call start_profile first.")
        
        try:
            # Configure Chrome options for remote debugging connection
            chrome_options = Options()
            chrome_options.add_experimental_option(
                "debuggerAddress", 
                f"127.0.0.1:{self.remote_port}"
            )
            
            # Suppress WebDriver detection flags (MLA handles this)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Connect to MLA browser
            self.driver = webdriver.Chrome(options=chrome_options)
            
            logger.info(f"Selenium connected to port {self.remote_port}")
            return self.driver
            
        except WebDriverException as e:
            logger.error(f"Failed to connect Selenium: {str(e)}")
            raise
    
    def navigate_to(self, url: str, wait_time: int = 3) -> bool:
        """
        Navigate to URL with error handling
        
        Args:
            url: Target URL
            wait_time: Seconds to wait after navigation
            
        Returns:
            Success status
        """
        if not self.driver:
            logger.error("No driver connected. Call connect_selenium first.")
            return False
        
        try:
            self.driver.get(url)
            time.sleep(wait_time)
            logger.info(f"Navigated to: {url}")
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            return False
    
    def generate_browsing_history(self, urls: List[str], dwell_time: int = 2) -> Dict[str, bool]:
        """
        Generate browsing history by visiting multiple URLs
        
        Args:
            urls: List of URLs to visit
            dwell_time: Seconds to wait on each page
            
        Returns:
            Dict mapping URLs to success status
        """
        if not self.driver:
            self.connect_selenium()
        
        results = {}
        
        for url in urls:
            try:
                self.driver.get(url)
                
                # Random human-like scrolling
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(dwell_time)
                
                # Check for basic page load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                results[url] = True
                logger.info(f"Successfully visited: {url}")
                
            except TimeoutException:
                results[url] = False
                logger.warning(f"Timeout loading: {url}")
                
            except Exception as e:
                results[url] = False
                logger.error(f"Error visiting {url}: {str(e)}")
        
        return results
    
    def inject_cookies(self, cookies: List[Dict[str, Any]]) -> int:
        """
        Inject cookies into current browser session
        
        Args:
            cookies: List of cookie dictionaries
            
        Returns:
            Number of successfully injected cookies
        """
        if not self.driver:
            logger.error("No driver connected")
            return 0
        
        injected = 0
        
        for cookie in cookies:
            try:
                # Ensure required fields
                if "name" in cookie and "value" in cookie:
                    self.driver.add_cookie(cookie)
                    injected += 1
            except Exception as e:
                logger.warning(f"Failed to inject cookie: {str(e)}")
        
        logger.info(f"Injected {injected}/{len(cookies)} cookies")
        return injected
    
    def get_profile_info(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """
        Get profile information from MLA API
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            Profile metadata or None
        """
        try:
            endpoint = f"{self.api_base}/profile/{profile_id}"
            response = requests.get(endpoint, timeout=self.MLA_API_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get profile info: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting profile info: {str(e)}")
            return None
    
    def cleanup(self):
        """Cleanup resources - close driver and stop profile"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            if self.current_profile_id:
                self.stop_profile(self.current_profile_id)
                
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")