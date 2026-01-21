"""
CHRONOS AGENTIC CONFIGURATION
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS = {
    # Environment
    "base_dir": BASE_DIR,
    "profiles_dir": os.path.join(BASE_DIR, "profiles"),
    "uploads_dir": os.path.join(BASE_DIR, "uploads"),
    "logs_dir": os.path.join(BASE_DIR, "logs"),
    
    # Browser / Nodriver
    "headless": True, # Default to True for container
    "browser_args": [
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars", 
        "--no-first-run",
        "--password-store=basic"
    ],
    
    # Temporal
    "default_age_days": 90,
    "aging_schedule": [90, 60, 30, 7, 1],
    
    # Trust Anchors
    "trust_anchors": [
        "https://www.wikipedia.org",
        "https://www.cnn.com",
        "https://www.nytimes.com",
        "https://www.amazon.com",
        "https://www.reddit.com"
    ],
    
    # OpSec
    "opsec_level": "MAXIMUM",
    "block_ntp": True,  # Now handled via Docker/Entrypoint
    
    # API
    "api_host": "0.0.0.0",
    "api_port": 5000
}

# Ensure directories exist
for path in [SETTINGS["profiles_dir"], SETTINGS["uploads_dir"], SETTINGS["logs_dir"]]:
    os.makedirs(path, exist_ok=True)
