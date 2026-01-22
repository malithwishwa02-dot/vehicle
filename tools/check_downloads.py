#!/usr/bin/env python3
import sqlite3
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84/Default/History')
if not p.exists():
    print('History DB not found:', p)
    sys.exit(1)

conn = sqlite3.connect(p)
c = conn.cursor()
try:
    c.execute('SELECT COUNT(*) FROM downloads')
    total = c.fetchone()[0]
    print('downloads count:', total)
    c.execute('SELECT guid, current_path, start_time, end_time, mime_type FROM downloads ORDER BY start_time DESC LIMIT 10')
    rows = c.fetchall()
    for r in rows:
        print(r)
except Exception as e:
    print('Error querying downloads:', e)
finally:
    conn.close()
