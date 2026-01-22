#!/usr/bin/env python3
import sqlite3
import sys
p = sys.argv[1] if len(sys.argv)>1 else 'generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84/Default/Top Sites'
conn = sqlite3.connect(p)
c = conn.cursor()
c.execute('SELECT url, url_rank, title FROM top_sites ORDER BY url_rank ASC LIMIT 20')
rows = c.fetchall()
print('Top Sites rows:', len(rows))
for r in rows:
    print(r)
conn.close()