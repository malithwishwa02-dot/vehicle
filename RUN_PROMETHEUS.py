"""
PROMETHEUS-CORE v5.0 :: THE MONOLITH
AUTHORITY: Dva.13 | STATUS: GODMODE
PURPOSE: Single-file execution of the entire Identity Fabrication Pipeline.
         Contains: Constructor, Heavy Burner, Commerce Injector, Time Dilator, Deployer.
USAGE: python RUN_PROMETHEUS.py
"""

import os
import sys
import shutil
import json
import time
import random
import zipfile
import sqlite3
import stat
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# --- DEPENDENCY CHECK ---
def install_dependencies():
    print("[INIT] Checking dependencies...")
    try:
        import selenium
        import webdriver_manager
        import requests
        print("[INIT] Dependencies verified.")
    except ImportError:
        print("[!] MISSING DEPENDENCIES. INSTALLING...")
        os.system(f"{sys.executable} -m pip install selenium webdriver-manager requests")
        print("[INIT] Dependencies installed. Please restart script if import errors persist.")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
except ImportError:
    install_dependencies()
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

# ==============================================================================
# COMPONENT 1: THE CONSTRUCTOR (Architect)
# ==============================================================================
class ProfileConstructor:
    def __init__(self, output_dir="generated_profiles", uuid=None):
        self.base_dir = Path(output_dir)
        # Use a fixed UUID if provided, else generate a random one or use default
        self.uuid = uuid if uuid else "37ab1612-c285-4314-b32a-6a06d35d6d84"
        self.profile_path = self.base_dir / self.uuid
        self.default_dir = self.profile_path / "Default"

    def run(self):
        print(f"\n[CONSTRUCTOR] Building Scaffolding for UUID: {self.uuid}...")
        
        # Clean previous run if exists
        if self.profile_path.exists():
            try:
                shutil.rmtree(self.profile_path)
                print(f"  > Removed existing artifact: {self.profile_path}")
            except Exception as e:
                print(f"  [!] Failed to clean path: {e}")
        
        # Create Directory Structure
        dirs = [
            self.default_dir,
            self.default_dir / "Local Storage" / "leveldb",
            self.default_dir / "Network",
            self.default_dir / "Session Storage",
            self.default_dir / "Extensions",
            self.profile_path / "ShaderCache",
            self.profile_path / "GrShaderCache",
            self.profile_path / "GraphiteDawnCache",
             self.default_dir / "Code Cache" / "js"
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            
        # Create Preferences File
        prefs = {
            "browser": {
                "show_home_button": True, 
                "check_default_browser": False,
                "window_placement": {
                    "bottom": 1000, "left": 10, "maximized": True, "right": 1000, "top": 10, "work_area_bottom": 1040, "work_area_left": 0, "work_area_right": 1920, "work_area_top": 0
                }
            },
            "credentials_enable_service": False,
            "profile": {"password_manager_enabled": True, "name": "Person 1"},
            "webrtc": {"multiple_routes_enabled": False},
            "extensions": {"ui": {"developer_mode": False}}
        }
        
        with open(self.default_dir / "Preferences", "w") as f:
            json.dump(prefs, f)
            
        print("[CONSTRUCTOR] Artifact structure initialized.")
        return str(self.profile_path.absolute())

# ==============================================================================
# COMPONENT 2: THE HEAVY BURNER (Artist)
# ==============================================================================
class ProfileBurner:
    def __init__(self, profile_path):
        self.profile_path = Path(profile_path)
        self.driver = None

    def ignite(self):
        print(f"\n[BURNER] Igniting Chromium Engine (Heavy Mode)...")
        options = Options()
        options.add_argument(f"--user-data-dir={self.profile_path}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # HEADLESS NEW is mandatory for modern GPU cache generation in headless
        options.add_argument("--headless=new") 
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--mute-audio")
        
        # Stability Flags for Windows/Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        
        # High-Trust User Agent
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def human_mouse_jiggle(self):
        """Simulates random mouse movement to generate metrics."""
        try:
            action = ActionChains(self.driver)
            for _ in range(5):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                action.move_by_offset(x_offset, y_offset).perform()
                # Reset offset to avoid out of bounds
                action.move_by_offset(-x_offset, -y_offset).perform()
                time.sleep(0.1)
        except:
            pass

    def heavy_soak(self):
        print("  > Initiating Bandwidth Soak (Generating 100+ Cache Files)...")
        targets = [
            "https://www.twitch.tv/",       # Video segments
            "https://www.pinterest.com/",   # Image heavy
            "https://www.cnn.com/",         # Ad scripts
            "https://threejs.org/examples/#webgl_animation_keyframes", # GPU
            "https://www.reddit.com/r/popular/",
            "https://en.wikipedia.org/wiki/Main_Page",
            "https://github.com/microsoft"
        ]
        
        for url in targets:
            try:
                print(f"    - Soaking: {url}")
                self.driver.get(url)
                
                self.human_mouse_jiggle()
                
                # Scroll to trigger lazy loading
                for _ in range(3):
                    self.driver.execute_script("window.scrollBy(0, 700);")
                    time.sleep(random.uniform(1.0, 2.0))
                
                time.sleep(1)
            except Exception as e:
                print(f"    [!] Soak error on {url}: {e}")

    def download_simulation(self):
        print("  > Simulating Invoice Download (Populating DB)...")
        try:
            # W3C Test PDF
            self.driver.get("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")
            time.sleep(3) # Wait for download to register
        except: pass

    def inject_trust_signals(self):
        print("  > Injecting 'Golden' LocalStorage Keys...")
        # Simulate 90 days ago
        fake_ts = int((datetime.now() - timedelta(days=90)).timestamp() * 1000)
        
        scripts = [
            ("https://www.google.com", f"window.localStorage.setItem('consent_date', '{fake_ts}'); window.localStorage.setItem('og_user_loggedin', '1');"),
            ("https://www.amazon.com", f"window.localStorage.setItem('csm-hit', '{fake_ts}'); window.localStorage.setItem('session-id-time', '{fake_ts}');"),
            ("https://www.shopify.com", f"window.localStorage.setItem('cart_abandoned', 'false'); window.localStorage.setItem('analytics_session_id', '{fake_ts}');")
        ]
        
        for url, script in scripts:
            try:
                self.driver.get(url)
                self.driver.execute_script(script)
                print(f"    - Injected keys for {url}")
            except: pass

    def run(self):
        try:
            self.ignite()
            self.download_simulation()
            self.heavy_soak()
            self.inject_trust_signals()
        except Exception as e:
            print(f"[BURNER] Critical Error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        print("[BURNER] Flame extinguished. Artifacts solidified.")

# ==============================================================================
# COMPONENT 3: COMMERCE INJECTOR (Operation Mammon)
# ==============================================================================
class CommerceInjector:
    def __init__(self, profile_path):
        self.db_path = Path(profile_path) / "Default" / "History"

    def inject(self):
        print(f"\n[COMMERCE] Injecting 'Golden Chain' Purchase History...")
        if not self.db_path.exists():
            print("  [!] History DB missing.")
            return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Ensure tables exist (Burner might have failed or been skipped)
        c.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR, visit_count INTEGER DEFAULT 0, typed_count INTEGER DEFAULT 0, last_visit_time INTEGER, hidden INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY, url INTEGER, visit_time INTEGER, from_visit INTEGER, transition INTEGER DEFAULT 0, segment_id INTEGER, visit_duration INTEGER DEFAULT 0)")
        
        try:
            c.execute("SELECT MAX(id) FROM urls")
            res = c.fetchone()
            start_id = (res[0] if res and res[0] else 0) + 1
        except: start_id = 1

        # WebKit Time Converter
        def wk_time(dt):
            return int((dt - datetime(1601, 1, 1)).total_seconds() * 1000000)

        purchases = [
            ("nike.com", "air-jordan-1-retro"),
            ("amazon.com", "sony-wh-1000xm5"),
            ("apple.com", "macbook-air-m3")
        ]

        for domain, prod in purchases:
            base_t = datetime.now() - timedelta(days=random.randint(2, 7))
            chain = [
                (f"https://www.{domain}/", 0),
                (f"https://www.{domain}/p/{prod}", 45),
                (f"https://www.{domain}/cart", 120),
                (f"https://www.{domain}/checkout", 200),
                (f"https://www.{domain}/checkout/success", 300)
            ]
            
            print(f"  > Injecting purchase: {domain}")
            for url, offset in chain:
                ts = wk_time(base_t + timedelta(seconds=offset))
                c.execute("INSERT INTO urls (id, url, title, visit_count, typed_count, last_visit_time, hidden) VALUES (?, ?, ?, 1, 0, ?, 0)", (start_id, url, f"{domain} | {prod}", ts))
                c.execute("INSERT INTO visits (url, visit_time, from_visit, transition, segment_id, visit_duration) VALUES (?, ?, 0, 806936371, 0, 5000000)", (start_id, ts))
                start_id += 1
                
        conn.commit()
        conn.close()
        print("[COMMERCE] Purchase funnels injected successfully.")

# ==============================================================================
# COMPONENT 4: TIME DILATOR (The Historian)
# ==============================================================================
class TimeDilator:
    def __init__(self, profile_path):
        self.db_path = Path(profile_path) / "Default" / "History"

    def age_profile(self, days=90):
        print(f"\n[TIME DILATOR] Dilating timeline by {days} days...")
        if not self.db_path.exists(): return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        domains = [
            "https://youtube.com", "https://github.com", "https://stackoverflow.com",
            "https://reddit.com", "https://medium.com", "https://cnn.com",
            "https://wikipedia.org", "https://twitch.tv", "https://adobe.com"
        ]

        start_date = datetime.now() - timedelta(days=days)
        current = start_date
        entries = 0
        
        # Get max ID
        c.execute("SELECT MAX(id) FROM urls")
        res = c.fetchone()
        curr_id = (res[0] if res and res[0] else 0) + 1

        while current < datetime.now():
            # Random gaps between 30 mins and 5 hours
            current += timedelta(minutes=random.randint(30, 300))
            if current.hour < 7: continue # Humans sleep

            # Create a browsing session
            session_length = random.randint(1, 4)
            for _ in range(session_length):
                url = random.choice(domains)
                ts = int((current - datetime(1601, 1, 1)).total_seconds() * 1000000)
                
                try:
                    c.execute("INSERT INTO urls (id, url, title, visit_count, typed_count, last_visit_time, hidden) VALUES (?, ?, ?, 1, 0, ?, 0)", (curr_id, url, "Visited Page", ts))
                    c.execute("INSERT INTO visits (url, visit_time, from_visit, transition, segment_id, visit_duration) VALUES (?, ?, 0, 806936371, 0, 10000000)", (curr_id, ts))
                    curr_id += 1
                    entries += 1
                except: pass
                
        conn.commit()
        conn.close()
        print(f"[TIME DILATOR] Injected {entries} historical vectors.")

# ==============================================================================
# COMPONENT 5: DEPLOYER (Sanitizer & Packager)
# ==============================================================================
class Deployer:
    def __init__(self, profile_path):
        self.path = Path(profile_path)
        self.uuid = self.path.name

    def sanitize(self):
        print(f"\n[DEPLOYER] Sanitizing Artifacts (Removing Automation Flags)...")
        # Critical files that must be removed
        targets = ["DevToolsActivePort", "SingletonLock", "LOCK", "lockfile"]
        
        # Also remove any .lock files recursively
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".lock"):
                    targets.append(os.path.join(root, file))

        for t in targets:
            f = self.path / t if not str(t).startswith(str(self.path)) else Path(t)
            if f.exists():
                try:
                    os.chmod(f, stat.S_IWRITE)
                    os.remove(f)
                    print(f"  > Scrubbed: {f.name}")
                except Exception as e:
                    print(f"  [!] Failed to remove {f.name}: {e}")

    def inject_metadata(self):
        print(f"[DEPLOYER] Injecting Multilogin Metadata...")
        meta = {
            "profileId": self.uuid,
            "browserType": "mimic",
            "browserVersion": "120.0.6099.71",
            "os": "win" if os.name == 'nt' else "lin"
        }
        with open(self.path / "metadata.json", "w") as f:
            json.dump(meta, f, indent=2)

    def package(self):
        self.inject_metadata()
        self.sanitize()
        
        zip_name = f"PROMETHEUS_PROFILE_{self.uuid}.zip"
        print(f"[DEPLOYER] Compressing to {zip_name}...")
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(self.path):
                for file in files:
                    fp = Path(root) / file
                    # Don't zip the zip itself
                    if file == zip_name: continue
                    arcname = fp.relative_to(self.path.parent)
                    zf.write(fp, arcname)
                    
        return zip_name

# ==============================================================================
# MAIN EXECUTION ORCHESTRATOR
# ==============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PROMETHEUS-CORE v5.0 Identity Fabrication")
    parser.add_argument("--uuid", help="Specific UUID for the profile", default=None)
    parser.add_argument("--age", type=int, help="Days to age history", default=90)
    args = parser.parse_args()

    print("""
    PROMETHEUS-CORE v5.0 :: MONOLITH
    ================================
    """)
    
    # 1. Construct
    constructor = ProfileConstructor(uuid=args.uuid)
    path = constructor.run()
    
    # 2. Burn (Heavy)
    burner = ProfileBurner(path)
    burner.run()
    
    # Safety pause to ensure Chrome releases all file locks (SQLite DB)
    print("[SYSTEM] Cooling down engines to release file locks...")
    time.sleep(5)

    # 3. Commerce
    commerce = CommerceInjector(path)
    commerce.inject()
    
    # 4. Age
    dilator = TimeDilator(path)
    dilator.age_profile(days=args.age)
    
    # 5. Deploy
    deployer = Deployer(path)
    final_zip = deployer.package()
    
    print(f"\n[MISSION COMPLETE] Artifact Ready: {final_zip}")
    print("STATUS: 90-Day Age | Heavy Cache | Purchase History | Cleaned")
