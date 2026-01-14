"""
CHRONOS-MULTILOGIN v2.0 Configuration
Central repository for operational parameters
"""

import os

class Config:
    # Execution Mode Configuration
    EXECUTION_MODE = "GENERATE_ONLY"  # GENERATE_ONLY = Stop after cookie generation (no checkout)
    
    # Multilogin API Configuration
    BROWSER_TYPE = "multilogin"       # Browser type: multilogin, chrome, firefox
    MLA_PORT = 35000                  # Default MLA Local API port
    MLA_URL = f"http://127.0.0.1:{MLA_PORT}/api/v1"
    MLA_URL_V2 = f"http://127.0.0.1:{MLA_PORT}/api/v2"
    MLA_PROFILE_ID = ""               # MLA Profile ID (blank by default, auto-generated if needed)
    HEADLESS_MODE = False             # MLA must be visible (cannot run headless)
    
    # Time-Shifting Schedule (Days in the past)
    # 90 days ago (Genesis), 45 days ago (Entropy), 7 days ago (Warmup)
    AGING_SCHEDULE = [90, 45, 21, 7, 1]
    
    # Trust Anchors to visit for cookie seeding
    TRUST_ANCHORS = [
        "https://www.google.com",
        "https://www.amazon.com",
        "https://www.wikipedia.org",
        "https://www.cnn.com",
        "https://www.twitch.tv",
        "https://www.youtube.com",
        "https://www.facebook.com",
        "https://www.twitter.com",
        "https://www.reddit.com",
        "https://www.linkedin.com"
    ]
    
    # Advanced Trust Anchors for deep patina
    DEEP_ANCHORS = [
        "https://accounts.google.com",
        "https://mail.google.com",
        "https://drive.google.com",
        "https://www.paypal.com",
        "https://www.ebay.com",
        "https://www.netflix.com",
        "https://www.spotify.com",
        "https://www.discord.com",
        "https://www.github.com",
        "https://www.stackoverflow.com"
    ]
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    PROFILE_STORE = os.path.expandvars(r"C:\Users\%USERNAME%\.multiloginapp.com\data")
    
    # Forensic Configuration
    FORENSIC_SCRUB = True
    DEEP_SCRUB_ITERATIONS = 2
    CLEAR_USN_JOURNAL = True
    
    # Browser Automation
    PAGE_DWELL_TIME = 3  # Seconds per page
    SCROLL_BEHAVIOR = True
    RANDOM_CLICKS = True
    
    # System Safety
    BLOCK_NTP = True
    RESTORE_TIME_ON_EXIT = True
    ADMIN_REQUIRED = True