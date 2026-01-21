"""
METHOD 5: BROWSER ENGINE (NODRIVER)
Protocol: Chrome DevTools Protocol (CDP) Direct
Eliminates: WebDriver binary latency and 'cdc_' variables.
"""

import asyncio
import nodriver as uc
import random
import logging
import os
from pathlib import Path
from core.stealth import StealthInjector
from core.genesis import GenesisController

class BrowserEngineV5:
    def __init__(self, profile_path, headless=True, proxy=None):
        self.profile_path = str(Path(profile_path).absolute())
        self.headless = headless
        self.proxy = proxy
        self.browser = None
        self.logger = logging.getLogger("BrowserEngineV5")
        self.stealth = StealthInjector()
        self.genesis = GenesisController(self.logger)
        
        # Ensure profile directory exists
        os.makedirs(self.profile_path, exist_ok=True)

    async def launch(self):
        """
        Launches Chrome with Method 5 flags and Time Shift env vars.
        """
        self.logger.info(f"[BROWSER] Launching Nodriver (CDP Mode)...")

        # Get Time Shift Environment Variables
        env_vars = self.genesis.get_browser_env()
        if env_vars:
            self.logger.info(f"[BROWSER] Applying Time Shift Env: {env_vars}")
            os.environ.update(env_vars)

        # Method 5 Flags: Disable Automation Indicators
        args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-first-run",
            "--password-store=basic",
            f"--user-data-dir={self.profile_path}",
            # Hardening against WebRTC leaks
            "--enforce-webrtc-ip-permission-check",
            "--force-webrtc-ip-handling-policy=default_public_interface_only"
        ]
        
        if self.proxy:
            args.append(f"--proxy-server={self.proxy}")

        try:
            # uc.start doesn't accept 'env' directly, but it inherits os.environ
            self.browser = await uc.start(
                headless=self.headless,
                browser_args=args
            )
            self.logger.info("[BROWSER] Connection Established via WebSocket.")
            
            # Inject Stealth Scripts
            await self._inject_fingerprint()
            
            return self.browser
        except Exception as e:
            self.logger.critical(f"[BROWSER] Launch Failed: {e}")
            raise

    async def _inject_fingerprint(self):
        """
        Injects Method 5 Stealth Scripts via CDP.
        """
        script = self.stealth.get_injection_script()
        try:
            # Inject into current page
            main_tab = self.browser.main_tab
            await main_tab.evaluate(script)
            
            # TODO: Add 'Page.addScriptToEvaluateOnNewDocument' via CDP for persistence
            # nodriver might support this via connection.send
            # await self.browser.connection.send("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            
            self.logger.info("[FINGERPRINT] Stealth overrides injected.")
        except Exception as e:
            self.logger.warning(f"[FINGERPRINT] Injection warning: {e}")

    async def navigate(self, url):
        """
        Navigates to a URL with human-like delays.
        """
        if not self.browser:
            await self.launch()
        
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
            element = await tab.select(selector)
            await element.click()
            await asyncio.sleep(random.uniform(0.2, 0.5))
            
            for char in text:
                await element.send_keys(char)
                await asyncio.sleep(random.uniform(0.05, 0.2))
            
            self.logger.info(f"[INPUT] Typed '{text}' into {selector}")
        except Exception as e:
            self.logger.error(f"[INPUT] Failed to type into {selector}: {e}")

    async def close(self):
        if self.browser:
            self.browser.stop()
