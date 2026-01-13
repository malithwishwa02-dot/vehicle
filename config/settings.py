"""
Configuration settings for CHRONOS-MULTILOGIN
Central repository for all configurable parameters
"""

from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
PROFILES_DIR = PROJECT_ROOT / "profiles"
LOGS_DIR = PROJECT_ROOT / "logs"

# Multilogin API Configuration
MLA_CONFIG = {
    "api_host": "127.0.0.1",
    "api_port": 35000,
    "api_version": "v2",
    "timeout": 30,
    "max_retries": 3
}

# Time Shift Configuration (in days)
TIME_SHIFTS = {
    "genesis": -90,      # Initial profile creation
    "phase_1": -45,      # First aging phase
    "phase_2": -21,      # Second aging phase
    "phase_3": -7,       # Third aging phase
    "phase_4": -1,       # Final aging phase
    "current": 0         # Present time
}

# Journey URL Patterns
JOURNEY_URLS = {
    "fingerprint_test": [
        "https://whoer.net",
        "https://browserleaks.com/webrtc",
        "https://pixelscan.net",
        "https://www.deviceinfo.me"
    ],
    "organic_browsing": [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.reddit.com",
        "https://www.youtube.com",
        "https://www.amazon.com",
        "https://www.ebay.com",
        "https://www.twitter.com",
        "https://www.linkedin.com"
    ],
    "news_sites": [
        "https://www.cnn.com",
        "https://www.bbc.com",
        "https://www.reuters.com",
        "https://www.bloomberg.com"
    ],
    "social_media": [
        "https://www.facebook.com",
        "https://www.instagram.com",
        "https://www.tiktok.com",
        "https://www.snapchat.com"
    ]
}

# Browser Automation Settings
AUTOMATION_CONFIG = {
    "page_load_timeout": 30,
    "implicit_wait": 10,
    "dwell_time_min": 2,
    "dwell_time_max": 8,
    "scroll_pause_time": 0.5,
    "human_typing_delay": 0.1
}

# Forensic Scrubbing Configuration
FORENSICS_CONFIG = {
    "scrub_iterations": 2,
    "temp_dir_prefix": "CHRONOS_TEMP",
    "compact_volume": True,
    "clear_usn_journal": True,
    "deep_scrub_enabled": True
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "file_name": "chronos_operations.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5
}

# System Requirements
SYSTEM_REQUIREMENTS = {
    "os": ["Windows 10", "Windows 11"],
    "python_version": "3.10",
    "admin_required": True,
    "multilogin_required": True
}

# Cookie Generation Templates
COOKIE_TEMPLATES = {
    "google": {
        "domain": ".google.com",
        "essential_cookies": ["NID", "SID", "HSID", "SSID", "APISID", "SAPISID"],
        "expiry_days": 365
    },
    "facebook": {
        "domain": ".facebook.com",
        "essential_cookies": ["c_user", "xs", "fr", "datr"],
        "expiry_days": 90
    },
    "amazon": {
        "domain": ".amazon.com",
        "essential_cookies": ["session-id", "session-token", "ubid-main"],
        "expiry_days": 365
    }
}

# Master Configuration Dictionary
CONFIG = {
    "paths": {
        "project_root": PROJECT_ROOT,
        "profiles": PROFILES_DIR,
        "logs": LOGS_DIR
    },
    "mla": MLA_CONFIG,
    "time_shifts": TIME_SHIFTS,
    "urls": JOURNEY_URLS,
    "automation": AUTOMATION_CONFIG,
    "forensics": FORENSICS_CONFIG,
    "logging": LOGGING_CONFIG,
    "system": SYSTEM_REQUIREMENTS,
    "cookies": COOKIE_TEMPLATES
}