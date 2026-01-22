import sqlite3
import os
import datetime
import json
import shutil

# Target Profile Path
PROFILE_PATH = r"E:\New folder\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84"
DEFAULT_DIR = os.path.join(PROFILE_PATH, "Default")

def get_db_connection(db_name):
    path = os.path.join(DEFAULT_DIR, db_name)
    if not os.path.exists(path):
        return None
    # Copy to temp file to avoid locking issues if browser is open (though unlikely here)
    temp_path = f"{db_name}_temp.sqlite"
    try:
        shutil.copy2(path, temp_path)
        return sqlite3.connect(temp_path)
    except Exception as e:
        print(f"[!] Error copying/opening {db_name}: {e}")
        return None

def webkit_to_datetime(ts):
    if not ts: return "N/A"
    try:
        # WebKit timestamp is microseconds since 1601-01-01
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=int(ts))
    except:
        return str(ts)

def analyze_history():
    print("\n--- HISTORY ANALYSIS ---")
    conn = get_db_connection("History")
    if not conn:
        print("History DB not found.")
        return

    c = conn.cursor()
    
    try:
        c.execute("SELECT count(*) FROM visits")
        print(f"Total Visits: {c.fetchone()[0]}")
        
        c.execute("SELECT count(*) FROM urls")
        print(f"Unique URLs: {c.fetchone()[0]}")
        
        c.execute("SELECT min(visit_time), max(visit_time) FROM visits")
        min_ts, max_ts = c.fetchone()
        print(f"History Range: {webkit_to_datetime(min_ts)} to {webkit_to_datetime(max_ts)}")
        
        print("\nTop 5 Visited Domains:")
        c.execute("""
            SELECT substr(url, 0, instr(substr(url, 9), '/') + 9) as domain, count(*) as count 
            FROM urls 
            GROUP BY domain 
            ORDER BY count DESC 
            LIMIT 5
        """)
        for row in c.fetchall():
            print(f"  {row[1]}x - {row[0]}")

    except Exception as e:
        print(f"Error analyzing history: {e}")
    finally:
        conn.close()
        if os.path.exists("History_temp.sqlite"): os.remove("History_temp.sqlite")

def analyze_cookies():
    print("\n--- COOKIES ANALYSIS ---")
    conn = get_db_connection("Cookies")
    if not conn: # Sometimes it's in Network/Cookies depending on version, but usually Default/Cookies
        print("Cookies DB not found in Default root.")
        return

    c = conn.cursor()
    try:
        c.execute("SELECT count(*) FROM cookies")
        print(f"Total Cookies: {c.fetchone()[0]}")
        
        print("\nTop Cookie Domains:")
        c.execute("SELECT host_key, count(*) as count FROM cookies GROUP BY host_key ORDER BY count DESC LIMIT 5")
        for row in c.fetchall():
            print(f"  {row[1]}x - {row[0]}")
            
    except Exception as e:
        print(f"Error analyzing cookies: {e}")
    finally:
        conn.close()
        if os.path.exists("Cookies_temp.sqlite"): os.remove("Cookies_temp.sqlite")

def analyze_web_data():
    print("\n--- WEB DATA (AUTOFILL) ---")
    conn = get_db_connection("Web Data")
    if not conn:
        print("Web Data DB not found.")
        return
        
    c = conn.cursor()
    try:
        # Check for autofill profiles
        try:
            c.execute("SELECT count(*) FROM autofill")
            print(f"Autofill Entries: {c.fetchone()[0]}")
        except: print("Autofill table not found or empty.")

        # Check for credit cards (masked)
        try:
            c.execute("SELECT count(*) FROM credit_cards")
            print(f"Saved Credit Cards: {c.fetchone()[0]}")
        except: print("Credit cards table not found.")
        
    except Exception as e:
        print(f"Error analyzing web data: {e}")
    finally:
        conn.close()
        if os.path.exists("Web Data_temp.sqlite"): os.remove("Web Data_temp.sqlite")

def analyze_local_state():
    print("\n--- LOCAL STATE ---")
    try:
        with open(os.path.join(PROFILE_PATH, "Local State"), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Variations Seed: {data.get('variations', {}).get('seed', 'N/A')}")
        # Check for some flags
        if 'browser' in data:
            print(f"Browser Enabled Labs: {data['browser'].get('enabled_labs_experiments', [])}")
    except Exception as e:
        print(f"Error reading Local State: {e}")

if __name__ == "__main__":
    print(f"Analyzing Profile: {PROFILE_PATH}")
    analyze_history()
    analyze_cookies()
    analyze_web_data()
    analyze_local_state()
