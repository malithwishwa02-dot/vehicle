import sqlite3
from pathlib import Path
p=Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84\first_party_sets.db")
conn=sqlite3.connect(p)
c=conn.cursor()
print('Connected to',p)
for row in c.execute("SELECT name, sql FROM sqlite_master WHERE type='table';"):
    print('\nTABLE:',row[0])
    print(row[1])

print('\nSample rows (up to 10) from each table:')
for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print('\n---',t,'---')
    try:
        for r in c.execute(f"SELECT * FROM {t} LIMIT 10;"):
            print(r)
    except Exception as e:
        print('ERROR reading',t,e)
conn.close()