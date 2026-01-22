#!/usr/bin/env python3
import sqlite3
import sys
p = sys.argv[1] if len(sys.argv)>1 else 'generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84/Default/Web Data'
conn = sqlite3.connect(p)
c = conn.cursor()
try:
    c.execute('SELECT name, value, date_created FROM autofill ORDER BY date_created DESC LIMIT 20')
    rows = c.fetchall()
    print('Autofill rows:', len(rows))
    for r in rows:
        print(r)
except Exception as e:
    print('Error:', e)
finally:
    conn.close()
