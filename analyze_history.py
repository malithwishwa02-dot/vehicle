import sqlite3
import os
import datetime

db_path = r"E:\New folder\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84\Default\History"

if not os.path.exists(db_path):
    print("History DB not found")
    exit()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total visits
    cursor.execute("SELECT count(*) FROM visits")
    total_visits = cursor.fetchone()[0]

    # Get total URLs
    cursor.execute("SELECT count(*) FROM urls")
    total_urls = cursor.fetchone()[0]

    # Get date range (WebKit timestamp format: microseconds since 1601-01-01)
    cursor.execute("SELECT min(visit_time), max(visit_time) FROM visits")
    min_ts, max_ts = cursor.fetchone()

    def webkit_to_datetime(ts):
        if not ts: return "N/A"
        return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ts)

    print(f"Total Visits: {total_visits}")
    print(f"Total URLs: {total_urls}")
    print(f"Date Range: {webkit_to_datetime(min_ts)} to {webkit_to_datetime(max_ts)}")

    # Get top domains
    cursor.execute("""
        SELECT substr(url, 0, instr(substr(url, 9), '/') + 9) as domain, count(*) as count 
        FROM urls 
        GROUP BY domain 
        ORDER BY count DESC 
        LIMIT 10
    """)
    print("\nTop Domains:")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    conn.close()

except Exception as e:
    print(f"Error reading DB: {e}")
