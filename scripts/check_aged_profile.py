import sqlite3
import sys
from pathlib import Path

p = Path(sys.argv[1])
print('Checking:', p)
if not p.exists():
    print('Path does not exist')
    sys.exit(1)
conn = sqlite3.connect(str(p))
cur = conn.cursor()
for table in ['urls','visits','cookies','logins','logins']:
    try:
        cur.execute(f"select count(*) from {table}")
        print(f"{table}:", cur.fetchone()[0])
    except Exception as e:
        print(f"{table} query failed:", e)
conn.close()