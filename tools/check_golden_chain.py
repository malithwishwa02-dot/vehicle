#!/usr/bin/env python3
import sqlite3
from datetime import datetime, timedelta

p='generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84/Default/History'
conn=sqlite3.connect(p)
c=conn.cursor()
c.execute("SELECT urls.url, visits.visit_time FROM visits JOIN urls ON visits.url = urls.id WHERE urls.url LIKE '%target-site.com%' ORDER BY visits.visit_time ASC")
rows=c.fetchall()
print('Found',len(rows),'visit rows for target-site.com')
for url, vt in rows:
    from datetime import datetime
    dt = datetime(1601,1,1) + timedelta(microseconds=vt)
    print(dt.isoformat(), url)
conn.close()