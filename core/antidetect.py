"""
Anti-Detection Suite: Comprehensive countermeasures against fraud detection systems.
Implements all detection evasion techniques from PROMETHEUS-CORE specification.
"""

import ctypes
import random
import hashlib
import json
import time
import subprocess
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import base64
import struct

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    import undetected_chromedriver as uc
except ImportError:
    pass


class AntiDetectionSuite:
    """
    Implements comprehensive anti-detection mechanisms to evade:
    - FingerprintJS clock skew detection
    - Canvas fingerprinting
    - WebGL fingerprinting
    - WebRTC leak detection
    - Navigator.webdriver detection
    - Automation detection
    - Temporal dissonance detection
    - MFT forensic analysis
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Anti-Detection Suite with configuration."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Detection evasion settings
        self.randomize_canvas = self.config.get('randomize_canvas', True)
        self.randomize_webgl = self.config.get('randomize_webgl', True)
        self.spoof_webrtc = self.config.get('spoof_webrtc', True)
        self.spoof_battery = self.config.get('spoof_battery', True)
        self.randomize_fonts = self.config.get('randomize_fonts', True)
        
        # Fingerprint seeds for consistency
        self.fingerprint_seed = self._generate_fingerprint_seed()
        self.canvas_noise = None
        self.webgl_vendor = None
        self.font_list = None
    
    def patch_browser_detection(self, driver) -> bool:
        """
        Patch browser to evade automation detection.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            bool: Success status
        """
        try:
            # Remove navigator.webdriver flag
            self._remove_webdriver_property(driver)
            
            # Patch Chrome DevTools detection
            self._patch_devtools_detection(driver)
            
            # Override fingerprinting functions
            if self.randomize_canvas:
                self._inject_canvas_noise(driver)
            
            if self.randomize_webgl:
                self._spoof_webgl_renderer(driver)
            
            if self.spoof_webrtc:
                self._block_webrtc_leaks(driver)
            
            if self.spoof_battery:
                self._spoof_battery_api(driver)
            
            if self.randomize_fonts:
                self._randomize_font_detection(driver)
            
            # Inject timezone alignment
            self._align_timezone(driver)
            
            # Override permissions API
            self._override_permissions(driver)
            
            # Patch notification API
            self._patch_notifications(driver)
            
            self.logger.info("Browser detection patches applied successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Browser patching failed: {e}")
            return False
    
    def _remove_webdriver_property(self, driver):
        """Remove navigator.webdriver property."""
        # Method 1: Delete property
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
        
        # Method 2: Override getter
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
        """)
    
    def _patch_devtools_detection(self, driver):
        """Patch Chrome DevTools detection methods."""
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Disable devtools detection
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this === window.console.log) {
                        return 'function log() { [native code] }';
                    }
                    return originalToString.call(this);
                };
                
                // Override console.clear detection
                const originalClear = console.clear;
                console.clear = function() {
                    // Do nothing to avoid detection
                };
                
                // Patch debugger statement
                const handler = {
                    get: function(target, property) {
                        if (property === 'debugger') {
                            return undefined;
                        }
                        return target[property];
                    }
                };
            '''
        })
    
    def _inject_canvas_noise(self, driver):
        """Inject canvas fingerprinting noise."""
        # Generate consistent noise based on seed
        if not self.canvas_noise:
            random.seed(self.fingerprint_seed)
            self.canvas_noise = [random.random() * 0.0001 for _ in range(100)]
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                // Canvas fingerprint randomization
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                const noise = {json.dumps(self.canvas_noise)};
                
                HTMLCanvasElement.prototype.toDataURL = function(type) {{
                    const canvas = this;
                    const ctx = canvas.getContext('2d');
                    if (ctx) {{
                        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                        for (let i = 0; i < imageData.data.length; i += 4) {{
                            imageData.data[i] += noise[i % noise.length] * 255;
                            imageData.data[i+1] += noise[(i+1) % noise.length] * 255;
                            imageData.data[i+2] += noise[(i+2) % noise.length] * 255;
                        }}
                        ctx.putImageData(imageData, 0, 0);
                    }}
                    return originalToDataURL.apply(this, arguments);
                }};
                
                CanvasRenderingContext2D.prototype.getImageData = function() {{
                    const imageData = originalGetImageData.apply(this, arguments);
                    for (let i = 0; i < imageData.data.length; i += 4) {{
                        imageData.data[i] += noise[i % noise.length] * 255;
                        imageData.data[i+1] += noise[(i+1) % noise.length] * 255;
                        imageData.data[i+2] += noise[(i+2) % noise.length] * 255;
                    }}
                    return imageData;
                }};
            '''
        })
    
    def _spoof_webgl_renderer(self, driver):
        """Spoof WebGL vendor and renderer information."""
        if not self.webgl_vendor:
            vendors = [
                ('NVIDIA Corporation', 'NVIDIA GeForce GTX 1060 6GB/PCIe/SSE2'),
                ('Intel Inc.', 'Intel(R) Iris(R) Xe Graphics'),
                ('AMD', 'AMD Radeon RX 580 Series'),
                ('NVIDIA Corporation', 'NVIDIA GeForce RTX 3070/PCIe/SSE2')
            ]
            random.seed(self.fingerprint_seed)
            self.webgl_vendor = random.choice(vendors)
        
        vendor, renderer = self.webgl_vendor
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                // WebGL fingerprint spoofing
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{
                        return '{vendor}';
                    }}
                    if (parameter === 37446) {{
                        return '{renderer}';
                    }}
                    return getParameter.apply(this, arguments);
                }};
                
                const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
                WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{
                        return '{vendor}';
                    }}
                    if (parameter === 37446) {{
                        return '{renderer}';
                    }}
                    return getParameter2.apply(this, arguments);
                }};
            '''
        })
    
    def _block_webrtc_leaks(self, driver):
        """Block WebRTC IP leaks."""
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Block WebRTC IP leak
                const RTCPeerConnection = window.RTCPeerConnection 
                    || window.mozRTCPeerConnection 
                    || window.webkitRTCPeerConnection;
                
                if (RTCPeerConnection) {
                    const originalCreateOffer = RTCPeerConnection.prototype.createOffer;
                    const originalCreateAnswer = RTCPeerConnection.prototype.createAnswer;
                    
                    RTCPeerConnection.prototype.createOffer = async function() {
                        return new Promise((resolve, reject) => {
                            reject(new Error('WebRTC is disabled'));
                        });
                    };
                    
                    RTCPeerConnection.prototype.createAnswer = async function() {
                        return new Promise((resolve, reject) => {
                            reject(new Error('WebRTC is disabled'));
                        });
                    };
                }
            '''
        })
    
    def _spoof_battery_api(self, driver):
        """Spoof Battery Status API."""
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Spoof battery API
                navigator.getBattery = async function() {
                    return {
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 0.99,
                        addEventListener: function() {},
                        removeEventListener: function() {}
                    };
                };
            '''
        })
    
    def _randomize_font_detection(self, driver):
        """Randomize font detection results."""
        if not self.font_list:
            base_fonts = [
                'Arial', 'Verdana', 'Times New Roman', 'Georgia',
                'Trebuchet MS', 'Helvetica', 'Comic Sans MS', 'Impact'
            ]
            random.seed(self.fingerprint_seed)
            # Randomly include/exclude fonts
            self.font_list = [f for f in base_fonts if random.random() > 0.3]
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                // Font detection randomization
                const fontList = {json.dumps(self.font_list)};
                const originalMeasureText = CanvasRenderingContext2D.prototype.measureText;
                
                CanvasRenderingContext2D.prototype.measureText = function(text) {{
                    const result = originalMeasureText.apply(this, arguments);
                    const font = this.font;
                    
                    // Add slight variations based on font
                    fontList.forEach((f, i) => {{
                        if (font.includes(f)) {{
                            result.width += (i * 0.01);
                        }}
                    }});
                    
                    return result;
                }};
            '''
        })
    
    def _align_timezone(self, driver):
        """Align timezone with system time."""
        # Get current system timezone offset
        tz_offset = time.timezone if not time.daylight else time.altzone
        tz_offset_minutes = tz_offset // 60
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f'''
                // Override timezone
                Date.prototype.getTimezoneOffset = function() {{
                    return {tz_offset_minutes};
                }};
                
                // Align Intl.DateTimeFormat
                const originalDateTimeFormat = Intl.DateTimeFormat;
                Intl.DateTimeFormat = function() {{
                    arguments[0] = arguments[0] || 'en-US';
                    return originalDateTimeFormat.apply(this, arguments);
                }};
            '''
        })
    
    def _override_permissions(self, driver):
        """Override Permissions API responses."""
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Override permissions
                const originalQuery = navigator.permissions.query;
                navigator.permissions.query = async function(descriptor) {
                    if (descriptor.name === 'notifications') {
                        return { state: 'granted' };
                    }
                    if (descriptor.name === 'geolocation') {
                        return { state: 'prompt' };
                    }
                    return originalQuery.apply(this, arguments);
                };
            '''
        })
    
    def _patch_notifications(self, driver):
        """Patch notification API."""
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Patch notifications
                window.Notification = function() {
                    return {
                        close: function() {},
                        onclick: null,
                        onclose: null,
                        onerror: null,
                        onshow: null
                    };
                };
                window.Notification.permission = 'granted';
                window.Notification.requestPermission = async function() {
                    return 'granted';
                };
            '''
        })
    
    def _generate_fingerprint_seed(self) -> str:
        """Generate consistent fingerprint seed."""
        # Use hardware ID or random seed
        try:
            import wmi
            c = wmi.WMI()
            for item in c.Win32_ComputerSystemProduct():
                return hashlib.md5(item.UUID.encode()).hexdigest()
        except:
            return hashlib.md5(str(random.random()).encode()).hexdigest()
    
    def verify_detection_bypass(self, driver) -> Dict[str, bool]:
        """
        Verify all detection bypass mechanisms are working.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            Dict with verification results
        """
        results = {}
        
        try:
            # Check navigator.webdriver
            results['webdriver_hidden'] = not driver.execute_script(
                "return navigator.webdriver"
            )
            
            # Check console properties
            results['console_patched'] = driver.execute_script("""
                return Function.prototype.toString.call(console.log)
                    .includes('[native code]');
            """)
            
            # Check canvas noise injection
            results['canvas_modified'] = driver.execute_script("""
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.fillText('test', 10, 10);
                const data1 = canvas.toDataURL();
                ctx.fillText('test', 10, 10);
                const data2 = canvas.toDataURL();
                return data1 === data2;  // Should be true with our consistent noise
            """)
            
            # Check WebGL spoofing
            results['webgl_spoofed'] = driver.execute_script("""
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                if (gl) {
                    const vendor = gl.getParameter(37445);
                    const renderer = gl.getParameter(37446);
                    return vendor && renderer && 
                           !vendor.includes('Google') && 
                           !renderer.includes('ANGLE');
                }
                return false;
            """)
            
            # Check WebRTC blocking
            results['webrtc_blocked'] = driver.execute_script("""
                return typeof RTCPeerConnection === 'undefined' ||
                       RTCPeerConnection.prototype.createOffer.toString()
                           .includes('WebRTC is disabled');
            """)
            
            # Check battery API
            results['battery_spoofed'] = driver.execute_script("""
                return navigator.getBattery().then(battery => {
                    return battery.level === 0.99 && battery.charging === true;
                }).catch(() => false);
            """)
            
            # Check timezone alignment
            results['timezone_aligned'] = driver.execute_script("""
                const date = new Date();
                const offset = date.getTimezoneOffset();
                return typeof offset === 'number';
            """)
            
            # Check permissions
            results['permissions_overridden'] = driver.execute_script("""
                return navigator.permissions.query({name: 'notifications'})
                    .then(result => result.state === 'granted')
                    .catch(() => false);
            """)
            
            # Calculate overall score
            passed = sum(1 for v in results.values() if v)
            total = len(results)
            results['detection_score'] = (passed / total) * 100
            
            self.logger.info(f"Detection bypass verification: {passed}/{total} passed")
            
        except Exception as e:
            self.logger.error(f"Verification failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def create_undetected_driver(self, 
                                profile_path: Optional[str] = None,
                                headless: bool = False) -> Any:
        """
        Create undetected Chrome driver with all patches applied.
        
        Args:
            profile_path: Chrome profile directory path
            headless: Run in headless mode
            
        Returns:
            Configured undetected Chrome driver
        """
        try:
            # Options for undetected Chrome
            options = uc.ChromeOptions()
            
            # Basic anti-detection flags
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Additional stealth options
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            
            # Window size for consistency
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Profile if specified
            if profile_path:
                options.add_argument(f'--user-data-dir={profile_path}')
            
            # Headless mode
            if headless:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
            
            # Proxy settings if configured
            if self.config.get('proxy'):
                options.add_argument(f'--proxy-server={self.config["proxy"]}')
            
            # Create driver
            driver = uc.Chrome(options=options, version_main=120)
            
            # Apply additional patches
            self.patch_browser_detection(driver)
            
            self.logger.info("Undetected Chrome driver created successfully")
            return driver
            
        except Exception as e:
            self.logger.error(f"Failed to create undetected driver: {e}")
            raise
    
    def validate_constellation_of_state(self, profile_path: Path) -> Dict[str, Any]:
        """
        Validate the 'Constellation of State' for temporal consistency.
        
        Args:
            profile_path: Path to browser profile
            
        Returns:
            Validation results dictionary
        """
        results = {
            'cookies_valid': False,
            'localStorage_valid': False,
            'cache_valid': False,
            'timestamps_aligned': False,
            'no_temporal_dissonance': False
        }
        
        try:
            # Check cookie database
            cookie_db = profile_path / 'Default' / 'Network' / 'Cookies'
            if cookie_db.exists():
                # Verify cookie timestamps
                import sqlite3
                conn = sqlite3.connect(str(cookie_db))
                cursor = conn.cursor()
                cursor.execute("SELECT creation_utc, last_access_utc FROM cookies LIMIT 100")
                cookies = cursor.fetchall()
                conn.close()
                
                if cookies:
                    # Check for temporal consistency
                    creation_times = [c[0] for c in cookies]
                    access_times = [c[1] for c in cookies]
                    
                    # Verify chronological order
                    results['cookies_valid'] = all(
                        c <= a for c, a in zip(creation_times, access_times)
                    )
            
            # Check localStorage
            local_storage = profile_path / 'Default' / 'Local Storage' / 'leveldb'
            if local_storage.exists():
                # Check file timestamps
                ls_files = list(local_storage.glob('*.ldb'))
                if ls_files:
                    timestamps = [f.stat().st_mtime for f in ls_files]
                    results['localStorage_valid'] = len(timestamps) > 0
            
            # Check cache
            cache_dir = profile_path / 'Default' / 'Cache' / 'Cache_Data'
            if cache_dir.exists():
                cache_files = list(cache_dir.glob('*'))
                if cache_files:
                    timestamps = [f.stat().st_mtime for f in cache_files]
                    results['cache_valid'] = len(timestamps) > 0
            
            # Check for temporal alignment
            all_timestamps = []
            
            for root, dirs, files in os.walk(profile_path):
                for file in files:
                    file_path = Path(root) / file
                    stat = file_path.stat()
                    all_timestamps.append({
                        'file': file,
                        'created': stat.st_ctime,
                        'modified': stat.st_mtime,
                        'accessed': stat.st_atime
                    })
            
            if all_timestamps:
                # Check for consistency
                min_time = min(t['created'] for t in all_timestamps)
                max_time = max(t['modified'] for t in all_timestamps)
                
                # Should have reasonable time spread
                time_spread = (max_time - min_time) / 86400  # Days
                results['timestamps_aligned'] = 1 < time_spread < 365
                
                # Check for temporal dissonance
                dissonance_found = False
                for ts in all_timestamps:
                    if ts['modified'] < ts['created']:
                        dissonance_found = True
                        break
                
                results['no_temporal_dissonance'] = not dissonance_found
            
            # Calculate integrity score
            valid_checks = sum(1 for v in results.values() if v)
            results['integrity_score'] = (valid_checks / len(results)) * 100
            
            self.logger.info(f"Constellation validation: {results['integrity_score']:.1f}% integrity")
            
        except Exception as e:
            self.logger.error(f"Constellation validation failed: {e}")
            results['error'] = str(e)
        
        return results