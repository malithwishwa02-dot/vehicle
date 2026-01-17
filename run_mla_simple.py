#!/usr/bin/env python3
"""
CHRONOS V3 - Simple MLA Runner
Runs cookie seeding through Multilogin WITHOUT system time modification.
Works without Administrator privileges.
"""

import requests
import time
import random
import yaml
from pathlib import Path
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style, init

init()

# Configuration
MLA_PORT = 45000  # Your MLA port
PROFILE_ID = "37ab1612-c285-4314-b32a-6a06d35d6d84"
TARGET_URL = "https://donate.wikimedia.org"

# Trust anchors to visit (builds browsing history)
TRUST_ANCHORS = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.wikipedia.org",
    "https://www.linkedin.com",
    "https://www.paypal.com",
    "https://www.amazon.com",
    "https://www.reddit.com",
    "https://www.github.com",
]

DEEP_ANCHORS = [
    "https://www.nytimes.com",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://stackoverflow.com",
    "https://medium.com",
]


def print_banner():
    print(f"""
{Fore.CYAN}
    ╔════════════════════════════════════════════════════════════╗
    ║           CHRONOS V3 - SIMPLE MLA RUNNER                   ║
    ║                 Trust Profile Builder                      ║
    ╚════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")


def check_mla_connection():
    """Check if MLA is running"""
    try:
        resp = requests.get(f"http://localhost:{MLA_PORT}/api/v1/profile/active", timeout=5)
        print(f"{Fore.GREEN}[+] MLA API reachable on port {MLA_PORT}{Style.RESET_ALL}")
        return True
    except:
        print(f"{Fore.RED}[!] Cannot reach MLA on port {MLA_PORT}. Start Multilogin!{Style.RESET_ALL}")
        return False


def start_profile():
    """Start MLA profile and return Selenium driver"""
    print(f"\n{Fore.CYAN}[PHASE 1] STARTING PROFILE{Style.RESET_ALL}")
    print(f"  • Profile ID: {PROFILE_ID}")
    
    encoded_id = quote(PROFILE_ID, safe='')
    url = f"http://localhost:{MLA_PORT}/api/v1/profile/start?automation=true&puppeteer=true&profileId={encoded_id}"
    
    try:
        resp = requests.get(url, timeout=60)
        data = resp.json()
        
        if 'value' in data:
            port = data['value'] if isinstance(data['value'], (int, str)) else data['value'].get('port')
            print(f"  {Fore.GREEN}✓ Profile started on port: {port}{Style.RESET_ALL}")
            
            # Attach Selenium
            opts = Options()
            opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            opts.add_argument("--disable-blink-features=AutomationControlled")
            
            driver = webdriver.Chrome(options=opts)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"  {Fore.GREEN}✓ Selenium attached{Style.RESET_ALL}")
            return driver
        else:
            print(f"  {Fore.RED}✗ Failed: {data}{Style.RESET_ALL}")
            return None
            
    except Exception as e:
        print(f"  {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        return None


def organic_pause(action="browsing"):
    """Simulate human reading/interaction time"""
    if random.random() < 0.3:  # 30% chance of long pause
        delay = random.uniform(30, 60)
        print(f"    {Fore.YELLOW}⏸ [ENTROPY] Organic Pause (User Reading)... {delay:.0f}s{Style.RESET_ALL}")
    else:
        delay = random.uniform(3, 12)
    time.sleep(delay)


def seed_trust_anchors(driver):
    """Visit trust anchors to build browsing history"""
    print(f"\n{Fore.CYAN}[PHASE 2] SEEDING TRUST ANCHORS{Style.RESET_ALL}")
    
    all_anchors = TRUST_ANCHORS + DEEP_ANCHORS
    random.shuffle(all_anchors)
    
    for i, url in enumerate(all_anchors, 1):
        try:
            print(f"  [{i}/{len(all_anchors)}] Visiting: {url}")
            driver.get(url)
            organic_pause()
            
            # Random scroll
            if random.random() > 0.5:
                scroll_amount = random.randint(200, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                time.sleep(random.uniform(1, 3))
            
            print(f"    {Fore.GREEN}✓ Trust anchor visited{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"    {Fore.YELLOW}⚠ Skipped: {e}{Style.RESET_ALL}")
            continue
    
    print(f"\n{Fore.GREEN}[+] JOURNEY: All trust anchors visited{Style.RESET_ALL}")


def visit_target(driver):
    """Visit the target URL"""
    print(f"\n{Fore.CYAN}[PHASE 3] TARGET SITE{Style.RESET_ALL}")
    print(f"  • Navigating to: {TARGET_URL}")
    
    try:
        driver.get(TARGET_URL)
        time.sleep(5)
        print(f"  {Fore.GREEN}✓ Target loaded{Style.RESET_ALL}")
        
        # Get cookies
        cookies = driver.get_cookies()
        print(f"  • Cookies collected: {len(cookies)}")
        
        return True
    except Exception as e:
        print(f"  {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        return False


def stop_profile():
    """Stop MLA profile"""
    encoded_id = quote(PROFILE_ID, safe='')
    url = f"http://localhost:{MLA_PORT}/api/v1/profile/stop?profileId={encoded_id}"
    try:
        requests.get(url, timeout=10)
        print(f"\n{Fore.GREEN}[+] Profile stopped{Style.RESET_ALL}")
    except:
        pass


def main():
    print_banner()
    
    # Check MLA connection
    if not check_mla_connection():
        return
    
    # Start profile
    driver = start_profile()
    if not driver:
        return
    
    try:
        # Seed trust anchors
        seed_trust_anchors(driver)
        
        # Visit target
        visit_target(driver)
        
        # Ready for manual takeover
        print(f"""
{Fore.GREEN}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   >>> READY FOR MANUAL TAKEOVER <<<                           ║
║                                                                ║
║   The browser is now on the target site.                      ║
║   You can manually interact with it.                          ║
║                                                                ║
║   Press ENTER when you're done to close the profile...        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
        input()
        
    finally:
        driver.quit()
        stop_profile()
    
    # Ghost wait reminder
    print(f"""
{Fore.YELLOW}
╔════════════════════════════════════════════════════════════════╗
║   🔇 GHOST WAIT PROTOCOL                                       ║
║                                                                ║
║   DO NOT OPEN THE PROFILE FOR 2 HOURS                         ║
║                                                                ║
║   This allows cookie timestamps to propagate properly.        ║
╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")


if __name__ == "__main__":
    main()
