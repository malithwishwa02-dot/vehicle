import sqlite3
import os
import time
import random

class HistoryEngine:
    def inject_timeline(self, profile_path, age_days):
        print(f"[*] INJECTING {age_days}-DAY HISTORY TIMELINE...")
        
        db_path = os.path.join(profile_path, "Default", "History")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, url TEXT, title TEXT, visit_count INTEGER, last_visit_time INTEGER, hidden INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY, url INTEGER, visit_time INTEGER, from_visit INTEGER, transition INTEGER, visit_duration INTEGER)")

        # Webkit Epoch: Microseconds since Jan 1, 1601
        now = int(time.time() * 1000000)
        # Offset 'age_days' into the past
        start_time = now - (int(age_days) * 86400 * 1000000)
        
        # The "Success Narrative" Chain
        chain = [
            ("https://www.google.com/search?q=kith+shoes", "Google Search"),
            ("https://kith.com/", "Kith - Homepage"),
            ("https://kith.com/collections/mens", "Kith - Mens Collection"),
            ("https://kith.com/products/example-shoe", "Kith - Product Page"),
            ("https://kith.com/cart", "Kith - Cart"),
            ("https://kith.com/checkouts/cn/c1-47092/information", "Checkout - Information"),
            ("https://kith.com/checkouts/cn/c1-47092/payment", "Checkout - Payment"),
            ("https://kith.com/checkouts/cn/c1-47092/thank_you", "Order Confirmed - Kith")
        ]
        
        current_time = start_time
        
        for url, title in chain:
            # Add random time between visits (30s to 5 mins)
            current_time += random.randint(30000000, 300000000)
            
            c.execute("INSERT INTO urls (url, title, visit_count, last_visit_time, hidden) VALUES (?, ?, 1, ?, 0)", (url, title, current_time))
            url_id = c.lastrowid
            c.execute("INSERT INTO visits (url, visit_time, from_visit, transition, visit_duration) VALUES (?, ?, 0, 0, 0)", (url_id, current_time))
            
        conn.commit()
        conn.close()
