"""
Multilogin API Controller v2.0
Direct interface with MLA Local API and browser automation
"""

import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from typing import List, Dict, Optional

class MLAHandler:
    """
    Multilogin browser controller with cookie seeding capabilities
    Implements trust anchor visitation for synthetic patina generation
    """
    
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.driver = None
        self.remote_port = None
        
        from config.settings import Config
        from utils.logger import get_logger
        
        self.config = Config
        self.logger = get_logger()
        
        # API endpoints
        self.api_v1 = Config.MLA_URL
        self.api_v2 = Config.MLA_URL_V2
    
    def start_profile(self) -> bool:
        """Start Multilogin profile and attach Selenium driver"""
        self.logger.info(f"Starting Profile: {self.profile_id}")
        
        # Try v1 API with automation and puppeteer flags (as per specification)
        url = f"{self.api_v1}/profile/start?automation=true&puppeteer=true&profileId={self.profile_id}"
        
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
            url = f"{self.api_v2}/profile/start?profileId={self.profile_id}"
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
        if deep_seed:
            anchors.extend(self.config.DEEP_ANCHORS)
        
        self.logger.info(f"Seeding cookies across {len(anchors)} trust anchors...")
        
        for url in anchors:
            try:
                self.logger.info(f"Visiting: {url}")
                self.driver.get(url)
                
                # Random human-like behavior
                dwell_time = random.uniform(2, 5)
                time.sleep(dwell_time)
                
                # Random scrolling
                if self.config.SCROLL_BEHAVIOR and random.random() > 0.5:
                    scroll_amount = random.randint(100, 500)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.5, 1.5))
                
                # Random clicks on page (non-interactive elements)
                if self.config.RANDOM_CLICKS and random.random() > 0.7:
                    try:
                        self.driver.execute_script("""
                            var x = Math.floor(Math.random() * window.innerWidth);
                            var y = Math.floor(Math.random() * window.innerHeight);
                            document.elementFromPoint(x, y).click();
                        """)
                    except:
                        pass  # Ignore click errors
                
                self.logger.success(f"Seeded: {url}")
                
            except Exception as e:
                self.logger.warning(f"Failed to visit {url}: {e}")
    
    def inject_cookies(self, cookies: List[Dict]) -> int:
        """
        Directly inject cookies into browser session
        
        Args:
            cookies: List of cookie dictionaries
            
        Returns:
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
                time.sleep(2)
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        # Stop profile via API to ensure cloud sync
        try:
            # Try v2 API first
            url = f"{self.api_v2}/profile/stop?profileId={self.profile_id}"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                self.logger.success("Profile stopped - cookies synced to MLA cloud/disk")
                time.sleep(2)  # Allow file locks to release
                return
        except:
            pass
        
        # Fallback to v1 API
        try:
            url = f"{self.api_v1}/profile/stop?profileId={self.profile_id}"
            requests.get(url, timeout=10)
            self.logger.success("Profile stopped (v1 API) - cookies synced")
        except:
            self.logger.warning("Profile stop API call failed - cookies may not be fully synced")
        
        time.sleep(2)  # Allow file locks to release
    
    def cleanup(self):
        """Emergency cleanup"""
        try:
            self.stop_profile()
        except:
            pass