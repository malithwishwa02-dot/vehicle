"""
METHOD 5: BROWSER ENGINE (NODRIVER)
Protocol: Chrome DevTools Protocol (CDP) Direct
Eliminates: WebDriver binary latency and 'cdc_' variables.
"""

import asyncio
import nodriver as uc
import random
import json
import logging
import os
from pathlib import Path

# Placeholder for bezier path generation if module is missing
try:
    from modules.human_mouse import generate_bezier_path
except ImportError:
    def generate_bezier_path(start, end):
        return [end]

class BrowserEngineV5:
    def __init__(self, profile_path, headless=True, proxy=None):
        self.profile_path = str(Path(profile_path).absolute())
        self.headless = headless
        self.proxy = proxy
        self.browser = None
        self.logger = logging.getLogger("BrowserEngineV5")
        
        # Ensure profile directory exists
        os.makedirs(self.profile_path, exist_ok=True)

    async def launch(self):
        """
        Launches Chrome with Method 5 flags.
        """
        self.logger.info(f"[BROWSER] Launching Nodriver (CDP Mode)...")

        # Method 5 Flags: Disable Automation Indicators
        args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-first-run",
            "--password-store=basic",
            f"--user-data-dir={self.profile_path}"
        ]
        
        if self.proxy:
            args.append(f"--proxy-server={self.proxy}")

        try:
            self.browser = await uc.start(
                headless=self.headless,
                browser_args=args
            )
            self.logger.info("[BROWSER] Connection Established via WebSocket.")
            
            # Inject WebGL Spoof immediately
            await self._inject_fingerprint()
            
            return self.browser
        except Exception as e:
            self.logger.critical(f"[BROWSER] Launch Failed: {e}")
            raise

    async def _inject_fingerprint(self):
        """
        Injects Method 5 JavaScript overrides for WebGL and Screen properties.
        """
        script = """
        (() => {
            // WebGL Spoofing (Apple M3 Simulation)
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Apple Inc.';
                if (parameter === 37446) return 'Apple M3';
                return getParameter(parameter);
            };

            // Screen Spoofing (Retina Display)
            Object.defineProperty(screen, 'width', { get: () => 3024 });
            Object.defineProperty(screen, 'height', { get: () => 1964 });
            Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
            
            // Hardware Concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 12 });
        })();
        """
        # Nodriver doesn't have add_script_to_evaluate_on_new_document easily exposed in high level
        # but we can try to run it on the main tab
        try:
            main_tab = await self.browser.get("about:blank")
            await main_tab.evaluate(script)
            self.logger.info("[FINGERPRINT] WebGL/Screen overrides injected.")
        except Exception as e:
            self.logger.warning(f"[FINGERPRINT] Injection warning: {e}")

    async def navigate(self, url):
        """
        Navigates to a URL with human-like delays.
        """
        if not self.browser:
            await self.launch()
        
        # Use main tab or create new? Nodriver usually manages tabs.
        # Let's just use the first available tab.
        tab = self.browser.main_tab
        await tab.get(url)
        await asyncio.sleep(random.uniform(2.5, 5.0))
        return tab

    async def simulate_human_input(self, selector, text):
        """
        Simulates human typing into an input field.
        """
        tab = self.browser.main_tab
        try:
            # Find element
            element = await tab.select(selector)
            
            # Click with jitter
            await element.click()
            await asyncio.sleep(random.uniform(0.2, 0.5))
            
            # Type characters
            for char in text:
                await element.send_keys(char)
                await asyncio.sleep(random.uniform(0.05, 0.2)) # Variable typing speed
            
            self.logger.info(f"[INPUT] Typed '{text}' into {selector}")
        except Exception as e:
            self.logger.error(f"[INPUT] Failed to type into {selector}: {e}")

    async def close(self):
        if self.browser:
            self.browser.stop()
