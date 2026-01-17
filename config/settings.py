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
    # Level 9 Financial Oblivion Mode: Default profile age is 90 days
    PROFILE_AGE_DAYS = 90
    AGING_SCHEDULE = [90, 45, 21, 7, 1]
    
    # Trust Anchors to visit for cookie seeding (Level 9 strict sequence)
    TRUST_ANCHORS = [
        "linkedin.com",
        "amazon.com",
        "nytimes.com"
    ]
        # Traffic Distribution for Bursty Simulation
        TRAFFIC_DISTRIBUTION = "POISSON"
        TRAFFIC_LAMBDA = 2.5
    
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
    
    # MLA Profile Management
    COOKIE_FLUSH_DELAY_SECONDS = 2    # Delay to allow cookies to write to disk
    MLA_SYNC_DELAY_SECONDS = 2        # Delay to allow MLA cloud/disk sync
    
    # System Safety
    BLOCK_NTP = True
    RESTORE_TIME_ON_EXIT = True
    ADMIN_REQUIRED = True