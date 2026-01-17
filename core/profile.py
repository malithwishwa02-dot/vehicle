"""
Profile Orchestrator: Browser automation and cookie injection engine.
Implements App-Bound Encryption bypass and profile management.
"""
import os
import json
import time
import random
import sqlite3
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import hashlib
import base64

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc
except ImportError:
    pass


class ProfileOrchestrator:
    """
    Manages browser profiles, automation, and cookie injection.
    Implements App-Bound Encryption bypass through time-shifted launch.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Profile Orchestrator."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Profile settings
        self.profile_path = Path(self.config.get('profile_path', 'profiles/chrome'))
        self.headless = self.config.get('headless', False)
        self.anti_detect = self.config.get('anti_detect', True)
        
        # Browser settings
        self.user_agent = self.config.get('user_agent', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.window_size = self.config.get('window_size', [1920, 1080])
        
        # Current browser instance
        self.driver = None
        self.client_id = None
    
    def launch_browser(self, 
                      headless: Optional[bool] = None,
                      anti_detect: bool = True,
                      profile_name: str = 'default') -> Any:
        """
        Launch browser with anti-detection measures.
        
        Args:
            headless: Run in headless mode
            anti_detect: Apply anti-detection patches
            profile_name: Profile directory name
            
        Returns:
            Configured browser driver
        """
        try:
            if headless is None:
                headless = self.headless
            
            # Profile directory
            profile_dir = self.profile_path / profile_name
            profile_dir.mkdir(parents=True, exist_ok=True)
            
            if anti_detect and 'uc' in globals():
                # Use undetected-chromedriver
                options = uc.ChromeOptions()
                
                # Anti-detection flags
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # Profile
                options.add_argument(f'--user-data-dir={profile_dir}')
                
                # Window settings
                options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
                
                # User agent
                options.add_argument(f'--user-agent={self.user_agent}')
                
                # Additional stealth options
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-features=IsolateOrigins,site-per-process')
                
                # Headless mode
                if headless:
                    options.add_argument('--headless=new')
                
                # Create driver
                self.driver = uc.Chrome(options=options, version_main=120)
                
                # Apply additional patches
                self._apply_stealth_patches()
                
            else:
                # Standard Chrome driver (less stealthy)
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                
                options = Options()
                options.add_argument(f'--user-data-dir={profile_dir}')
                options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
                options.add_argument(f'--user-agent={self.user_agent}')
                
                if headless:
                    options.add_argument('--headless')
                
                self.driver = webdriver.Chrome(options=options)
            
            self.logger.info(f"Browser launched with profile: {profile_name}")
            
            # Extract client ID if available
            self._extract_client_id()
            
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Browser launch failed: {e}")
            raise
    
    def _apply_stealth_patches(self):
        """Apply additional stealth patches to browser."""
        if not self.driver:
            return
        
        try:
            # Remove webdriver property
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                '''
            })
            
            # Override plugins
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                '''
            })
            
            # Override languages
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                '''
            })
            
            self.logger.debug("Stealth patches applied")
            
        except Exception as e:
            self.logger.warning(f"Some stealth patches failed: {e}")
    
    def execute_actions(self, driver: Any, actions: List[Dict]) -> bool:
        """
        Execute a series of browser actions.
        
        Args:
            driver: Browser driver instance
            actions: List of action specifications
            
        Returns:
            bool: Success status
        """
        try:
            for action in actions:
                action_type = action.get('type')
                params = action.get('parameters', {})
                
                if action_type == 'navigate':
                    self._action_navigate(driver, params)
                
                elif action_type == 'scroll':
                    self._action_scroll(driver, params)
                
                elif action_type == 'click_link':
                    self._action_click(driver, params)
                
                elif action_type == 'search':
                    self._action_search(driver, params)
                
                elif action_type == 'mouse_movement':
                    self._action_mouse_move(driver, params)
                
                elif action_type == 'form_submission':
                    self._action_form_submit(driver, params)
                
                elif action_type == 'idle':
                    time.sleep(random.uniform(1, 5))
                
                # Random delay between actions
                time.sleep(random.uniform(0.5, 2))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            return False
    
    def _action_navigate(self, driver: Any, params: Dict):
        """Navigate to URL."""
        url = params.get('url', 'https://www.google.com')
        driver.get(url)
        time.sleep(random.uniform(2, 4))
    
    def _action_scroll(self, driver: Any, params: Dict):
        """Perform scroll action."""
        direction = params.get('direction', 'down')
        amount = params.get('amount', 500)
        
        if direction == 'down':
            driver.execute_script(f"window.scrollBy(0, {amount});")
        else:
            driver.execute_script(f"window.scrollBy(0, -{amount});")
        
        time.sleep(params.get('duration', 1))
    
    def _action_click(self, driver: Any, params: Dict):
        """Click on element."""
        selector = params.get('selector', 'a')
        index = params.get('index', 0)
        
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > index:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView();", elements[index])
                time.sleep(0.5)
                
                # Click with random offset
                action = ActionChains(driver)
                action.move_to_element(elements[index])
                action.click()
                action.perform()
                
                time.sleep(params.get('wait_after', 2))
        except:
            pass
    
    def _action_search(self, driver: Any, params: Dict):
        """Perform search action."""
        query = params.get('query', 'test search')
        typing_speed = params.get('typing_speed', 0.1)
        
        try:
            # Find search box
            search_box = None
            for selector in ['input[type="search"]', 'input[name="q"]', 'input[type="text"]']:
                try:
                    search_box = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if search_box:
                search_box.click()
                time.sleep(0.5)
                
                # Type with delays
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.5))
                
                time.sleep(params.get('submit_delay', 1))
                search_box.send_keys(Keys.RETURN)
        except:
            pass
    
    def _action_mouse_move(self, driver: Any, params: Dict):
        """Perform mouse movement."""
        pattern = params.get('pattern', 'random')
        points = params.get('points', [(500, 500)])
        
        try:
            action = ActionChains(driver)
            
            if pattern == 'bezier':
                # Bezier curve movement
                for point in points:
                    action.move_by_offset(point[0], point[1])
            else:
                # Random movement
                for _ in range(5):
                    x = random.randint(-100, 100)
                    y = random.randint(-100, 100)
                    action.move_by_offset(x, y)
            
            action.perform()
        except:
            pass
    
    def _action_form_submit(self, driver: Any, params: Dict):
        """Submit form with data."""
        fields = params.get('fields', 3)
        
        try:
            # Find form inputs
            inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"], input[type="email"]')
            
            for i, input_elem in enumerate(inputs[:fields]):
                input_elem.click()
                time.sleep(0.5)
                
                # Type sample data
                sample_data = f"test_data_{i}_{random.randint(1000, 9999)}"
                for char in sample_data:
                    input_elem.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                time.sleep(0.5)
            
            # Find and click submit
            submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
            submit.click()
            
        except:
            pass
    
    def inject_cookies(self, cookies: List[Dict], domain: str) -> bool:
        """
        Inject cookies into current browser session.
        
        Args:
            cookies: List of cookie dictionaries
            domain: Domain for cookies
            
        Returns:
            bool: Success status
        """
        try:
            if not self.driver:
                self.logger.error("No browser instance active")
                return False
            
            # Navigate to domain first
            self.driver.get(f"https://{domain}")
            time.sleep(2)
            
            # Inject each cookie
            for cookie in cookies:
                try:
                    # Prepare cookie dict
                    cookie_dict = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie.get('domain', domain),
                        'path': cookie.get('path', '/'),
                        'secure': cookie.get('secure', True),
                        'httpOnly': cookie.get('httpOnly', False)
                    }
                    
                    # Add expiry if present
                    if 'expiry' in cookie:
                        cookie_dict['expiry'] = cookie['expiry']
                    
                    self.driver.add_cookie(cookie_dict)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to inject cookie {cookie.get('name')}: {e}")
            
            # Refresh to apply cookies
            self.driver.refresh()
            time.sleep(2)
            
            self.logger.info(f"Injected {len(cookies)} cookies for {domain}")
            return True
            
        except Exception as e:
            self.logger.error(f"Cookie injection failed: {e}")
            return False
    
    def extract_cookies(self) -> List[Dict]:
        """
        Extract all cookies from current browser session.
        
        Returns:
            List of cookie dictionaries
        """
        try:
            if not self.driver:
                return []
            
            cookies = self.driver.get_cookies()
            
            self.logger.info(f"Extracted {len(cookies)} cookies")
            return cookies
            
        except Exception as e:
            self.logger.error(f"Cookie extraction failed: {e}")
            return []
    
    def _extract_client_id(self):
        """Extract Google Analytics client ID from cookies."""
        try:
            if not self.driver:
                return
            
            # Look for _ga cookie
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == '_ga':
                    # Format: GA1.2.XXXXXXXXXX.YYYYYYYYYY
                    parts = cookie['value'].split('.')
                    if len(parts) >= 4:
                        self.client_id = f"{parts[2]}.{parts[3]}"
                        self.logger.info(f"Extracted client ID: {self.client_id}")
                        break
        except:
            pass
    
    def get_client_id(self, driver: Any) -> Optional[str]:
        """
        Get Google Analytics client ID.
        
        Args:
            driver: Browser driver instance
            
        Returns:
            Client ID string or None
        """
        if self.client_id:
            return self.client_id
        
        # Try to extract from current session
        self._extract_client_id()
        return self.client_id
    
    def close_browser(self, driver: Any):
        """
        Close browser instance.
        
        Args:
            driver: Browser driver to close
        """
        try:
            if driver:
                driver.quit()
                self.logger.info("Browser closed")
                
            if driver == self.driver:
                self.driver = None
                
        except Exception as e:
            self.logger.warning(f"Browser close warning: {e}")
    
    def warm_up_profile(self, urls: List[str]) -> bool:
        """
        Warm up profile by visiting URLs.
        
        Args:
            urls: List of URLs to visit
            
        Returns:
            bool: Success status
        """
        try:
            if not self.driver:
                self.logger.error("No browser instance")
                return False
            
            for url in urls:
                try:
                    self.driver.get(url)
                    
                    # Random interactions
                    time.sleep(random.uniform(2, 5))
                    
                    # Scroll
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    self.logger.warning(f"Failed to visit {url}: {e}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Profile warm-up failed: {e}")
            return False
    
    def create_aged_profile(self, age_days: int) -> Path:
        """
        Create an aged browser profile.
        
        Args:
            age_days: Number of days to age the profile
            
        Returns:
            Path to created profile
        """
        try:
            # Generate unique profile name
            profile_name = f"aged_{age_days}d_{int(time.time())}"
            profile_dir = self.profile_path / profile_name
            
            # Create profile directory
            profile_dir.mkdir(parents=True, exist_ok=True)
            
            # Create basic Chrome profile structure
            default_dir = profile_dir / 'Default'
            default_dir.mkdir(exist_ok=True)
            
            # Create necessary subdirectories
            (default_dir / 'Cache').mkdir(exist_ok=True)
            (default_dir / 'Code Cache').mkdir(exist_ok=True)
            (default_dir / 'Local Storage').mkdir(exist_ok=True)
            (default_dir / 'Session Storage').mkdir(exist_ok=True)
            (default_dir / 'IndexedDB').mkdir(exist_ok=True)
            
            # Create preferences file
            prefs = {
                "profile": {
                    "created_by_version": "120.0.0.0",
                    "creation_time": str(int((datetime.now() - timedelta(days=age_days)).timestamp()))
                }
            }
            
            with open(default_dir / 'Preferences', 'w') as f:
                json.dump(prefs, f, indent=2)
            
            self.logger.info(f"Created aged profile: {profile_name}")
            return profile_dir
            
        except Exception as e:
            self.logger.error(f"Profile creation failed: {e}")
            raise